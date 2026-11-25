"""Check preparation boundaries and the intentional starting states of fixtures."""

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from prepare import prepare


REPO = Path(__file__).resolve().parents[1]
CASES = REPO / "evals" / "cases"


class PreparationTests(unittest.TestCase):
    def test_all_conditions_copy_only_inputs_and_inventory_matches(self):
        with tempfile.TemporaryDirectory() as directory:
            for case in sorted(CASES.iterdir()):
                for condition in ("baseline", "skill", "skill-implicit"):
                    for agent in ("codex", "claude"):
                        with self.subTest(case=case.name, condition=condition, agent=agent):
                            output = Path(directory) / f"{case.name}-{condition}-{agent}"
                            prepare(case.name, condition, output, agent)
                            workspace = output / "workspace"
                            for source in (case / "fixture").rglob("*"):
                                if source.is_file():
                                    target = workspace / source.relative_to(case / "fixture")
                                    self.assertEqual(target.read_bytes(), source.read_bytes())

                            inventory = json.loads((output / "baseline.json").read_text())["files"]
                            files = {
                                p.relative_to(workspace).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in workspace.rglob("*")
                                if p.is_file()
                            }
                            self.assertEqual(inventory, files)
                            self.assertFalse(any(p.name == "grading.json" for p in workspace.rglob("*")))
                            self.assertFalse(any(p.name == "scenarios.md" for p in workspace.rglob("*")))
                            fixture_paths = {
                                p.relative_to(case / "fixture").as_posix()
                                for p in (case / "fixture").rglob("*") if p.is_file()
                            }
                            extras = set(files) - fixture_paths
                            if condition == "baseline":
                                self.assertFalse(extras)
                                self.assertEqual((output / "task.txt").read_text(), (case / "prompt.txt").read_text())
                            else:
                                folder = ".claude" if agent == "claude" else ".agents"
                                selection_path = case / "skills.json"
                                selection = json.loads(selection_path.read_text()) if selection_path.exists() else ["slopstop-python-r"]
                                prefixes = [f"{folder}/skills/{name}/" for name in selection]
                                self.assertTrue(extras)
                                self.assertTrue(all(any(p.startswith(prefix) for prefix in prefixes) for p in extras))
                                task = (output / "task.txt").read_text()
                                if condition == "skill":
                                    self.assertTrue(task.startswith("Read and apply "))
                                    for prefix in prefixes:
                                        self.assertIn(f"{prefix}SKILL.md", task.split("\n", 1)[0])
                                else:
                                    self.assertEqual(task, (case / "prompt.txt").read_text())

    def test_existing_output_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "run"
            prepare("scoped-fix", "baseline", output, "codex")
            marker = output / "keep.txt"
            marker.write_text("preserve")
            with self.assertRaises(FileExistsError):
                prepare("scoped-fix", "skill", output, "codex")
            self.assertEqual(marker.read_text(), "preserve")

    def test_output_in_source_checkout_is_refused(self):
        with self.assertRaisesRegex(ValueError, "outside this repository"):
            prepare("scoped-fix", "baseline", REPO / "evals" / "forbidden-run", "codex")
        self.assertFalse((REPO / "evals" / "forbidden-run").exists())

    def test_cli_prepares_and_rejects_unknown_case(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "run"
            result = subprocess.run(
                [sys.executable, "-B", str(REPO / "evals" / "prepare.py"), "scoped-fix",
                 "--condition", "skill", "--agent", "claude", "--output", str(output)],
                capture_output=True, text=True, timeout=10,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((output / "workspace/.claude/skills/slopstop-python-r/SKILL.md").is_file())
            invalid = subprocess.run(
                [sys.executable, "-B", str(REPO / "evals" / "prepare.py"), "nonexistent",
                 "--condition", "baseline", "--output", str(output)],
                capture_output=True, text=True, timeout=10,
            )
            self.assertEqual(invalid.returncode, 2)

    def test_fixture_starting_states_match_declared_checks(self):
        with tempfile.TemporaryDirectory() as directory:
            for case in sorted(CASES.iterdir()):
                output = Path(directory) / case.name
                prepare(case.name, "baseline", output, "codex")
                grading = json.loads((case / "grading.json").read_text())
                self.assertTrue(grading["criteria"], case.name)
                for check in grading["checks"]:
                    with self.subTest(case=case.name, command=check["command"]):
                        result = subprocess.run(  # Trusted fixture commands; never executed from an agent's supplied text.
                            check["command"], cwd=output / "workspace",
                            capture_output=True, text=True, timeout=20,
                        )
                        self.assertEqual(result.returncode, check["initial_exit"], result.stdout + result.stderr)
                        if check["initial_exit"] == 1:
                            if check["command"][0] == "python3":
                                self.assertIn("AssertionError", result.stderr)
                            else:
                                self.assertIn("is not TRUE", result.stderr)


if __name__ == "__main__":
    unittest.main()
