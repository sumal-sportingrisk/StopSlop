"""Exercise the placeholder exception without disabling detection in that fixture."""

import json
# subprocess only runs the checksum-verified gitleaks binary with an argument list and no shell.
import subprocess  # nosec B404
import sys
import tempfile
from pathlib import Path


def main(scanner_path):
    scanner = str(Path(scanner_path).resolve(strict=True))
    repo = Path(__file__).resolve().parents[1]
    relative = Path("evals/cases/security-review/fixture/upload.py")
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        fixture = root / relative
        fixture.parent.mkdir(parents=True)
        fixture.write_bytes((repo / relative).read_bytes())
        report = root / "findings.json"
        command = [
            scanner, "dir", str(root), "--config", str(repo / ".gitleaks.toml"),
            "--redact", "--no-banner", "--report-format", "json", "--report-path", str(report),
        ]
        baseline = subprocess.run(command, check=False, timeout=30)  # nosec B603
        if baseline.returncode != 0:
            raise RuntimeError("The documented placeholder fixture did not pass secret scanning")
        canary = "ghp_" + "rA7mQ2sV8bN4xE6kP9hJ3uD5wF0cL1zTgYqR"
        with fixture.open("a", encoding="utf-8") as stream:
            stream.write(f"\ngithub_token = {canary!r}\n")
        if report.exists():
            report.unlink()
        result = subprocess.run(command, check=False, timeout=30)  # nosec B603
        findings = json.loads(report.read_text(encoding="utf-8")) if report.exists() else []
        if result.returncode != 1 or not any(item.get("RuleID") == "github-pat" for item in findings):
            raise RuntimeError("A non-exempt synthetic token in the same fixture was not detected")
    print("PASS: documented placeholders allowed; non-exempt synthetic token detected")


if __name__ == "__main__":
    main(sys.argv[1])
