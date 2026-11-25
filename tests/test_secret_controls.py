from contextlib import redirect_stdout
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


script = Path(__file__).resolve().parents[1] / "scripts/check_secret_controls.py"
spec = importlib.util.spec_from_file_location("check_secret_controls", script)
controls = importlib.util.module_from_spec(spec)
spec.loader.exec_module(controls)


class SecretControlProtocolTests(unittest.TestCase):
    def test_scanner_error_is_not_a_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            scanner = Path(directory) / "scanner"
            scanner.touch()
            with patch.object(controls.subprocess, "run", return_value=SimpleNamespace(returncode=2)):
                with self.assertRaisesRegex(RuntimeError, "placeholder fixture"):
                    controls.main(scanner)

    def test_nonzero_exit_without_findings_is_not_detection(self):
        with tempfile.TemporaryDirectory() as directory:
            scanner = Path(directory) / "scanner"
            scanner.touch()
            responses = [SimpleNamespace(returncode=0), SimpleNamespace(returncode=1)]
            with patch.object(controls.subprocess, "run", side_effect=responses):
                with self.assertRaisesRegex(RuntimeError, "not detected"):
                    controls.main(scanner)

    def test_typed_finding_after_clean_baseline_is_accepted(self):
        with tempfile.TemporaryDirectory() as directory:
            scanner = Path(directory) / "scanner"
            scanner.touch()
            calls = 0

            def scanner_response(command, **kwargs):
                nonlocal calls
                calls += 1
                if calls == 1:
                    return SimpleNamespace(returncode=0)
                report = Path(command[command.index("--report-path") + 1])
                report.write_text(json.dumps([{"RuleID": "github-pat"}]), encoding="utf-8")
                return SimpleNamespace(returncode=1)

            with patch.object(controls.subprocess, "run", side_effect=scanner_response), redirect_stdout(io.StringIO()):
                controls.main(scanner)
            self.assertEqual(calls, 2)


if __name__ == "__main__":
    unittest.main()
