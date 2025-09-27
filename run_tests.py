import os
import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime

LOG_DIR = Path("logs")
REPORTS_DIR = Path("reports")
FINAL_LOG = LOG_DIR / "test_coverage_final.log"   # nome exigido pela OPT-21
SUMMARY_LOG = LOG_DIR / "test_summary.txt"
FINAL_REPORT = REPORTS_DIR / "FINAL_TEST_REPORT.txt"

def run_all_tests_comprehensive() -> dict:
    """Executa todos os testes de forma abrangente e retorna resultados detalhados."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # (1) sempre rodar a partir da raiz do repo
    try:
        root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
    except Exception:
        root = str(Path(__file__).resolve().parent)
    os.chdir(root)

    results = {
        "start_time": datetime.now(),
        "tests": {},
        "summary": {},
        "coverage": {}
    }
    
    # Lista de categorias de testes para executar
    test_categories = [
        ("all", "Todos os Testes", []),
        ("benchmark", "Testes de Benchmark", ["-k", "benchmark"]),
        ("performance", "Testes de Performance", ["-k", "performance"]),
        ("metropolitan", "Testes Metropolitanos", ["-k", "metropolitan"]),
        ("algorithms", "Testes de Algoritmos", ["-k", "algorithm"]),
        ("structures", "Testes de Estruturas", ["-k", "structure"]),
        ("integration", "Testes de Integração", ["-k", "integration"]),
        ("validation", "Testes de Validação", ["-k", "validation"])
    ]
    
    print("🚀 EXECUTANDO TODOS OS TESTES DO OPTIROTA")
    print("=" * 60)
    
    for category, description, extra_args in test_categories:
        print(f"\n📊 Executando: {description}")
        start_time = time.time()
        
        # Comando base
        cmd = [sys.executable, "-m", "pytest", "-v", "--tb=short", "--durations=10"]
        cmd.extend(extra_args)
        
        # Garantir que 'src' seja importável
        env = os.environ.copy()
        env["PYTHONPATH"] = env.get("PYTHONPATH", ".")
        
        try:
            # Executar teste
            result = subprocess.run(
                cmd, 
                env=env, 
                capture_output=True, 
                text=True, 
                timeout=600  # 10 minutos por categoria
            )
            
            execution_time = time.time() - start_time
            
            # Parse dos resultados
            output_lines = result.stdout.split('\n')
            passed = len([line for line in output_lines if 'PASSED' in line])
            failed = len([line for line in output_lines if 'FAILED' in line])
            skipped = len([line for line in output_lines if 'SKIPPED' in line])
            errors = len([line for line in output_lines if 'ERROR' in line])
            
            results["tests"][category] = {
                "description": description,
                "execution_time": execution_time,
                "return_code": result.returncode,
                "passed": passed,
                "failed": failed,
                "skipped": skipped,
                "errors": errors,
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "command": " ".join(cmd)
            }
            
            print(f"   ✅ {passed} aprovados, ❌ {failed} falharam, ⏭️ {skipped} ignorados, ⚠️ {errors} erros")
            print(f"   ⏱️ Tempo: {execution_time:.2f}s")
            
        except subprocess.TimeoutExpired:
            results["tests"][category] = {
                "description": description,
                "execution_time": time.time() - start_time,
                "return_code": -1,
                "passed": 0,
                "failed": 0,
                "skipped": 0,
                "errors": 1,
                "success": False,
                "stdout": "",
                "stderr": "TIMEOUT: Teste excedeu 10 minutos",
                "command": " ".join(cmd)
            }
            print(f"   ⏰ TIMEOUT após 10 minutos")
            
        except Exception as e:
            results["tests"][category] = {
                "description": description,
                "execution_time": time.time() - start_time,
                "return_code": -1,
                "passed": 0,
                "failed": 0,
                "skipped": 0,
                "errors": 1,
                "success": False,
                "stdout": "",
                "stderr": f"ERRO: {str(e)}",
                "command": " ".join(cmd)
            }
            print(f"   ❌ ERRO: {str(e)}")
    
    # Calcular resumo geral
    total_passed = sum(test["passed"] for test in results["tests"].values())
    total_failed = sum(test["failed"] for test in results["tests"].values())
    total_skipped = sum(test["skipped"] for test in results["tests"].values())
    total_errors = sum(test["errors"] for test in results["tests"].values())
    total_time = sum(test["execution_time"] for test in results["tests"].values())
    successful_categories = sum(1 for test in results["tests"].values() if test["success"])
    
    results["summary"] = {
        "total_categories": len(results["tests"]),
        "successful_categories": successful_categories,
        "success_rate": (successful_categories / len(results["tests"])) * 100,
        "total_passed": total_passed,
        "total_failed": total_failed,
        "total_skipped": total_skipped,
        "total_errors": total_errors,
        "total_time": total_time,
        "end_time": datetime.now()
    }
    
    return results

def generate_final_report(results: dict) -> Path:
    """Gera relatório final em TXT com todos os resultados."""
    
    with open(FINAL_REPORT, 'w', encoding='utf-8') as f:
        f.write("=" * 100 + "\n")
        f.write("RELATÓRIO FINAL COMPLETO DE TESTES - OPTIROTA\n")
        f.write("=" * 100 + "\n")
        f.write(f"Data/Hora: {results['start_time'].strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write(f"Execução: {results['summary']['end_time'].strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write(f"Duração Total: {results['summary']['total_time']:.2f}s\n")
        f.write("=" * 100 + "\n\n")
        
        # Resumo executivo
        f.write("RESUMO EXECUTIVO\n")
        f.write("-" * 50 + "\n")
        f.write(f"Total de categorias testadas: {results['summary']['total_categories']}\n")
        f.write(f"Categorias bem-sucedidas: {results['summary']['successful_categories']}\n")
        f.write(f"Taxa de sucesso: {results['summary']['success_rate']:.1f}%\n")
        f.write(f"Total de testes aprovados: {results['summary']['total_passed']}\n")
        f.write(f"Total de testes falharam: {results['summary']['total_failed']}\n")
        f.write(f"Total de testes ignorados: {results['summary']['total_skipped']}\n")
        f.write(f"Total de erros: {results['summary']['total_errors']}\n")
        f.write(f"Tempo total de execução: {results['summary']['total_time']:.2f}s\n\n")
        
        # Detalhes por categoria
        f.write("RESULTADOS POR CATEGORIA\n")
        f.write("-" * 50 + "\n")
        
        for category, test_result in results["tests"].items():
            f.write(f"\nCATEGORIA: {test_result['description']}\n")
            f.write("=" * 60 + "\n")
            f.write(f"Status: {'✅ SUCESSO' if test_result['success'] else '❌ FALHA'}\n")
            f.write(f"Tempo de execução: {test_result['execution_time']:.2f}s\n")
            f.write(f"Testes aprovados: {test_result['passed']}\n")
            f.write(f"Testes falharam: {test_result['failed']}\n")
            f.write(f"Testes ignorados: {test_result['skipped']}\n")
            f.write(f"Erros: {test_result['errors']}\n")
            f.write(f"Comando: {test_result['command']}\n")
            
            if test_result['stderr']:
                f.write(f"\nErro: {test_result['stderr']}\n")
            
            f.write("\n" + "=" * 100 + "\n")
        
        # Análise de problemas
        f.write("\nANÁLISE DE PROBLEMAS\n")
        f.write("-" * 50 + "\n")
        
        failed_tests = [test for test in results["tests"].values() if not test["success"]]
        if failed_tests:
            f.write(f"Total de categorias com falhas: {len(failed_tests)}\n\n")
            for test in failed_tests:
                f.write(f"❌ {test['description']}: {test['stderr'][:100]}...\n")
        else:
            f.write("✅ Nenhuma categoria com falhas!\n")
        
        # Recomendações
        f.write("\nRECOMENDAÇÕES\n")
        f.write("-" * 50 + "\n")
        
        if results['summary']['success_rate'] >= 90:
            f.write("✅ Excelente! Sistema funcionando muito bem.\n")
        elif results['summary']['success_rate'] >= 70:
            f.write("⚠️ Bom, mas há algumas falhas para investigar.\n")
        elif results['summary']['success_rate'] >= 50:
            f.write("⚠️ Sistema parcialmente funcional, revisar falhas.\n")
        else:
            f.write("❌ Muitas falhas, revisar implementação.\n")
        
        f.write(f"\nTempo total de execução: {results['summary']['total_time']:.2f}s\n")
        f.write(f"Taxa de sucesso: {results['summary']['success_rate']:.1f}%\n")
        
        f.write("\n" + "=" * 100 + "\n")
        f.write("Relatório gerado automaticamente pelo sistema OptiRota\n")
        f.write("Para mais informações, consulte os logs em logs/\n")
        f.write("=" * 100 + "\n")
    
    return FINAL_REPORT

def main() -> int:
    """Função principal que executa todos os testes e gera relatório final."""
    args = sys.argv[1:]
    
    # Verificar se é modo completo (padrão) ou modo antigo
    if "legacy" in args or "old" in args:
        # Modo antigo para compatibilidade
        low = [a.lower() for a in args]
        fast = "fast" in low
        ci = "ci" in low
        extra = [a for a in args if a.lower() not in ("fast", "ci", "legacy", "old")]
        return run_pytest_legacy(with_coverage=not fast, quiet=ci, extra_args=extra)
    
    # Modo novo: executar todos os testes e gerar relatório
    print("🚀 OPTIROTA - EXECUTOR DE TESTES COMPLETO")
    print("=" * 60)
    
    try:
        # Executar todos os testes
        results = run_all_tests_comprehensive()
        
        # Gerar relatório final
        report_file = generate_final_report(results)
        
        print("\n" + "=" * 60)
        print("✅ EXECUÇÃO COMPLETA FINALIZADA!")
        print("=" * 60)
        print(f"📊 Taxa de sucesso: {results['summary']['success_rate']:.1f}%")
        print(f"⏱️ Tempo total: {results['summary']['total_time']:.2f}s")
        print(f"✅ Testes aprovados: {results['summary']['total_passed']}")
        print(f"❌ Testes falharam: {results['summary']['total_failed']}")
        print(f"⏭️ Testes ignorados: {results['summary']['total_skipped']}")
        print(f"⚠️ Erros: {results['summary']['total_errors']}")
        print(f"📄 Relatório final: {report_file}")
        
        return 0 if results['summary']['success_rate'] >= 70 else 1
        
    except KeyboardInterrupt:
        print("\n⚠️ Execução interrompida pelo usuário.")
        return 1
    except Exception as e:
        print(f"\n❌ Erro durante a execução: {e}")
        return 1

def run_pytest_legacy(with_coverage: bool = True, quiet: bool = False, extra_args=None) -> int:
    """Função legacy para compatibilidade com versão anterior."""
    extra_args = extra_args or []
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    # (1) sempre rodar a partir da raiz do repo
    try:
        root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
    except Exception:
        root = str(Path(__file__).resolve().parent)
    os.chdir(root)

    # (2) comando base
    cmd = [sys.executable, "-m", "pytest"]

    # (3) cobertura e relatórios
    if with_coverage:
        if not quiet:
            print("🔍 Executando testes com cobertura...\n")
        cmd += [
            "--cov=src",
            "--cov-report=term-missing",
            "--cov-report=xml:coverage.xml",
            "-v",
        ]
    else:
        if not quiet:
            print("⚡ Executando testes em modo rápido (sem cobertura)...\n")
        cmd += ["-v"]

    # (4) permite passar flags extras
    cmd += extra_args

    # (5) garantir que 'src' seja importável
    env = os.environ.copy()
    env["PYTHONPATH"] = env.get("PYTHONPATH", ".")
    if Path("pytest.ini").exists():
        cmd[2:2] = ["-c", "pytest.ini"]

    if not quiet:
        print(f"[run_tests] CWD: {Path.cwd()}")
        print(f"[run_tests] Command: {' '.join(cmd)}")
        print(f"[run_tests] Log: {FINAL_LOG}")

    # (6) executar e capturar saída
    proc = subprocess.Popen(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    lines = []
    assert proc.stdout is not None
    with FINAL_LOG.open("a", encoding="utf-8") as logf:
        logf.write("\n" + "=" * 80 + "\n")
        logf.write(f"Run at: {datetime.now().isoformat()}\n")
        logf.write("Command: " + " ".join(cmd) + "\n\n")

        for line in proc.stdout:
            if not quiet:
                print(line, end="")
            lines.append(line)
            logf.write(line)

    rc = proc.wait()

    # (7) extrair resumo
    summary = None
    for line in reversed(lines):
        low = line.lower()
        if any(k in low for k in ("passed", "failed", "skipped", "xpassed", "xfailed", "error")):
            summary = line.strip()
            break

    if summary:
        if not quiet:
            print("\n📊 Resumo dos testes:")
            print("   " + summary)
        SUMMARY_LOG.write_text(summary + "\n", encoding="utf-8")
        if not quiet:
            print(f"📝 Resumo salvo em {SUMMARY_LOG}")
    else:
        if not quiet:
            print("\n⚠️ Não foi possível gerar resumo automático.")

    if not quiet:
        print(f"\n📂 Log completo: {FINAL_LOG}")
        if with_coverage:
            print("🧾 Relatório XML: coverage.xml")

    return rc

if __name__ == "__main__":
    sys.exit(main())

# Exemplos de uso:
#   python run_tests.py                    # Modo novo: executa todos os testes e gera relatório final
#   python run_tests.py legacy             # Modo antigo: testes com cobertura
#   python run_tests.py legacy fast         # Modo antigo: testes rápidos (sem cobertura)
#   python run_tests.py legacy ci           # Modo antigo: testes silenciosos
#   python run_tests.py legacy -k integration  # Modo antigo: apenas testes de integração