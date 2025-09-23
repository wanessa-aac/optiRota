import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime

LOG_DIR = Path("logs")
FINAL_LOG = LOG_DIR / "test_coverage_final.log"   # nome exigido pela OPT-21
SUMMARY_LOG = LOG_DIR / "test_summary.txt"

def run_pytest(with_coverage: bool = True, quiet: bool = False, extra_args=None) -> int:
    """Executa pytest com/sem cobertura, salva logs e resumo, e retorna exit code."""
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
            "--cov-report=xml:coverage.xml",  # <-- gera coverage.xml (CI/badges)
            "-v",
        ]
    else:
        if not quiet:
            print("⚡ Executando testes em modo rápido (sem cobertura)...\n")
        cmd += ["-v"]

    # (4) permite passar flags extras (ex.: -k integration -q)
    cmd += extra_args

    # (5) garantir que 'src' seja importável
    env = os.environ.copy()
    env["PYTHONPATH"] = env.get("PYTHONPATH", ".")
    # se existir pytest.ini na raiz, force o uso
    if Path("pytest.ini").exists():
        cmd[2:2] = ["-c", "pytest.ini"]

    if not quiet:
        print(f"[run_tests] CWD: {Path.cwd()}")
        print(f"[run_tests] Command: {' '.join(cmd)}")
        print(f"[run_tests] Log: {FINAL_LOG}")

    # (6) executar e capturar saída (tee)
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

    # (7) extrair resumo (última linha com passed/failed/skipped/xpassed/xfail)
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

def main() -> int:
    # aceita 'fast' (sem cobertura) e 'ci' (quiet), e quaisquer flags adicionais do pytest
    args = sys.argv[1:]
    low = [a.lower() for a in args]
    fast = "fast" in low
    ci = "ci" in low
    # flags extras = tudo que não for 'fast'/'ci'
    extra = [a for a in args if a.lower() not in ("fast", "ci")]
    return run_pytest(with_coverage=not fast, quiet=ci, extra_args=extra)

if __name__ == "__main__":
    sys.exit(main())

# Exemplo de uso:
#   python run_tests.py            # testes com cobertura, term-missing + xml, logs em logs/test_coverage_final.log
#   python run_tests.py fast       # testes rápidos (sem cobertura)
#   python run_tests.py ci         # testes silenciosos (bom para CI)
#   python run_tests.py -k integration  # rodar apenas testes de integração