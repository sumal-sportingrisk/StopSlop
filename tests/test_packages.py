import importlib.util
import tempfile
import unittest
from pathlib import Path


script = Path(__file__).resolve().parents[1] / "scripts/check_packages.py"
spec = importlib.util.spec_from_file_location("check_packages", script)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class PackageChecks(unittest.TestCase):
    def make_skill(self, parent):
        directory = Path(parent) / "sample-skill"
        directory.mkdir()
        (directory / "SKILL.md").write_text(
            "---\nname: sample-skill\ndescription: Inspect sample inputs.\n---\n\nRead [details](details.md).\n",
            encoding="utf-8",
        )
        (directory / "details.md").write_text("# Details\n", encoding="utf-8")
        return directory

    def test_self_contained_package_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            checker.check_skill(self.make_skill(directory))

    def test_missing_reference_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            skill = self.make_skill(directory)
            (skill / "details.md").unlink()
            with self.assertRaisesRegex(ValueError, "broken local link"):
                checker.check_skill(skill)

    def test_link_to_external_grading_key_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            skill = self.make_skill(directory)
            (Path(directory) / "grading.md").write_text("Private answers", encoding="utf-8")
            (skill / "details.md").write_text("Read [answers](../grading.md).", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "escapes the distributable skill"):
                checker.check_skill(skill)

    def test_wrong_skill_name_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            skill = self.make_skill(directory)
            text = (skill / "SKILL.md").read_text().replace("name: sample-skill", "name: other")
            (skill / "SKILL.md").write_text(text)
            with self.assertRaisesRegex(ValueError, "name must match"):
                checker.check_skill(skill)


if __name__ == "__main__":
    unittest.main()
