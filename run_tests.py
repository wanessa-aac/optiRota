import os
import subprocess
import sys

def run_pytest(with_coverage=True, quiet=False):
    """Executa pytest com ou sem cobertura, salva logs e resumo."""
    log_dir = os.path.join("logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "test_coverage.log")
    summary_file = os.path.join(log_dir, "test_summary.txt")

    if with_coverage:
        cmd = [
            sys.executable, "-m", "pytest",
            "--cov=src",
            "--cov-report=term-missing",
            "-v"
        ]
        if not quiet:
            print("🔍 Executando testes com cobertura...\n")
    else:
        cmd = [sys.executable, "-m", "pytest", "-v"]
        if not quiet:
            print("⚡ Executando testes em modo rápido (sem cobertura)...\n")

    env = os.environ.copy()
    env["PYTHONPATH"] = "."

    # Captura saída completa
    process = subprocess.Popen(
        cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )
    output_lines = []
    for line in process.stdout:
        if not quiet:   # imprime no terminal apenas se não estiver em modo CI
            print(line, end="")
        output_lines.append(line)

    # Sempre salva log completo
    with open(log_file, "w", encoding="utf-8") as f:
        f.writelines(output_lines)
    if not quiet:
        print(f"\n📂 Relatório detalhado salvo em {log_file}")

    # Extrai resumo final
    summary = None
    for line in reversed(output_lines):
        if "passed" in line or "failed" in line or "skipped" in line:
            summary = line.strip()
            break

    if summary:
        if not quiet:
            print("\n📊 Resumo dos testes:")
            print("   " + summary)
        with open(summary_file, "w", encoding="utf-8") as f:
            f.write(summary + "\n")
        if not quiet:
            print(f"📝 Resumo salvo em {summary_file}")
    else:
        if not quiet:
            print("\n⚠️ Não foi possível gerar resumo automático.")

def main():
    args = [a.lower() for a in sys.argv[1:]]
    if "fast" in args:
        run_pytest(with_coverage=False, quiet=False)
    elif "ci" in args:
        run_pytest(with_coverage=True, quiet=True)
    else:
        run_pytest(with_coverage=True, quiet=False)

if __name__ == "__main__":
    main()