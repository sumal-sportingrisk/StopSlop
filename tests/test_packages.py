import importlib.util
import json
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


    def make_repo(self, parent, source="./plugin", plugin_name="demo"):
        repo = Path(parent)
        (repo / ".claude-plugin").mkdir()
        (repo / ".claude-plugin" / "marketplace.json").write_text(json.dumps(
            {"name": "market", "owner": {"name": "owner"}, "plugins": [{"name": "demo", "source": source}]}))
        plugin = repo / "plugin"
        (plugin / ".claude-plugin").mkdir(parents=True)
        (plugin / ".claude-plugin" / "plugin.json").write_text(json.dumps({"name": plugin_name}))
        (plugin / "skills").mkdir()
        return repo

    def test_valid_plugin_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(len(checker.check_plugin(self.make_repo(directory))), 1)

    def test_invalid_plugin_json_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = self.make_repo(directory)
            (repo / "plugin/.claude-plugin/plugin.json").write_text("{not json")
            with self.assertRaises(json.JSONDecodeError):
                checker.check_plugin(repo)

    def test_mismatched_plugin_name_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "name must match"):
                checker.check_plugin(self.make_repo(directory, plugin_name="other"))

    def test_repository_root_source_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "not the repository root"):
                checker.check_plugin(self.make_repo(directory, source="./"))

    def test_grading_key_inside_plugin_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = self.make_repo(directory)
            (repo / "plugin/skills/grading.json").write_text("{}")
            with self.assertRaisesRegex(ValueError, "evaluation material"):
                checker.check_plugin(repo)

    def test_extra_top_level_plugin_content_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = self.make_repo(directory)
            (repo / "plugin/evals").mkdir()
            with self.assertRaisesRegex(ValueError, "unexpected contents"):
                checker.check_plugin(repo)


if __name__ == "__main__":
    unittest.main()
