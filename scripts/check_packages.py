"""Validate distributable skills and local documentation links without running examples."""

import re
import sys
from pathlib import Path

import yaml


def check_skill(directory):
    text = (directory / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.DOTALL)
    if not match:
        raise ValueError(f"{directory}: missing YAML frontmatter")
    metadata = yaml.safe_load(match.group(1))
    if not isinstance(metadata, dict) or metadata.get("name") != directory.name:
        raise ValueError(f"{directory}: name must match the skill directory")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", directory.name):
        raise ValueError(f"{directory}: invalid skill name")
    description = metadata.get("description")
    if not isinstance(description, str) or not description.strip():
        raise ValueError(f"{directory}: description must be nonempty text")
    for path in directory.rglob("*.md"):
        check_links(path, boundary=directory)
    ui_path = directory / "agents" / "openai.yaml"
    if ui_path.exists():
        interface = yaml.safe_load(ui_path.read_text(encoding="utf-8"))["interface"]
        if f"${directory.name}" not in interface.get("default_prompt", ""):
            raise ValueError(f"{ui_path}: default prompt must name the skill")


def check_links(path, boundary=None):
    text = path.read_text(encoding="utf-8")
    for target in re.findall(r"\]\(([^)\s]+)\)", text):
        if target.startswith(("https://", "http://", "mailto:", "#")):
            continue
        relative = target.split("#", 1)[0]
        resolved = (path.parent / relative).resolve()
        if boundary and not resolved.is_relative_to(boundary.resolve()):
            raise ValueError(f"{path}: link escapes the distributable skill: {target}")
        if not resolved.exists():
            raise ValueError(f"{path}: broken local link: {target}")


def main():
    repo = Path(__file__).resolve().parents[1]
    skills = sorted(path for path in (repo / "skills").iterdir() if path.is_dir())
    for skill in skills:
        check_skill(skill)
    docs = [repo / name for name in ("README.md", "AGENTS.md", "CLAUDE.md", "evals/README.md", "evals/scenarios.md")]
    docs.extend((repo / "docs").rglob("*.md"))
    for path in docs:
        check_links(path)
    print(f"PASS: {len(skills)} skill packages and local documentation links")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, yaml.YAMLError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)
