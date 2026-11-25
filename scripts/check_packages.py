"""Validate the plugin package, distributable skills, and local documentation links without running examples."""

import json
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


NAME = re.compile(r"[a-z0-9][a-z0-9._-]*")
# Only these may be installed. Anything else, such as evals/ or grading keys, would ship to every user.
PLUGIN_CONTENTS = {".claude-plugin", "skills"}


def check_plugin(repo):
    """Check the marketplace and plugin manifests and that the installed directory holds only skills."""
    marketplace = json.loads((repo / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    if not NAME.fullmatch(str(marketplace.get("name", ""))):
        raise ValueError("marketplace.json: name must be lowercase letters, digits, '.', '_' or '-'")
    if not isinstance(marketplace.get("owner"), dict) or not marketplace["owner"].get("name"):
        raise ValueError("marketplace.json: owner.name is required")
    entries = marketplace.get("plugins")
    if not isinstance(entries, list) or not entries:
        raise ValueError("marketplace.json: plugins must be a nonempty list")
    plugin_dirs = []
    for entry in entries:
        name, source = entry.get("name"), entry.get("source")
        if not isinstance(source, str) or not source.startswith("./"):
            raise ValueError(f"marketplace.json: {name}: source must be a relative path starting with ./")
        directory = (repo / source).resolve()
        if directory == repo.resolve() or not directory.is_relative_to(repo.resolve()):
            raise ValueError(f"marketplace.json: {name}: source must be a subdirectory, not the repository root")
        if not directory.is_dir():
            raise ValueError(f"marketplace.json: {name}: source directory {source} does not exist")
        manifest = json.loads((directory / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        if manifest.get("name") != name:
            raise ValueError(f"{source}/.claude-plugin/plugin.json: name must match the marketplace entry {name!r}")
        extra = {path.name for path in directory.iterdir()} - PLUGIN_CONTENTS
        if extra:
            raise ValueError(f"{source}: unexpected contents would be installed: {sorted(extra)}")
        leaked = [path for path in directory.rglob("*") if path.name in ("grading.json", "evals")]
        if leaked:
            raise ValueError(f"{source}: evaluation material would be installed: {leaked[0]}")
        plugin_dirs.append(directory)
    return plugin_dirs


def main():
    repo = Path(__file__).resolve().parents[1]
    plugin_dirs = check_plugin(repo)
    skills = sorted(path for d in plugin_dirs for path in (d / "skills").iterdir() if path.is_dir())
    for skill in skills:
        check_skill(skill)
    docs = [repo / name for name in ("README.md", "AGENTS.md", "CLAUDE.md", "evals/README.md", "evals/scenarios.md")]
    docs.extend((repo / "docs").rglob("*.md"))
    for path in docs:
        check_links(path)
    print(f"PASS: plugin manifests, {len(skills)} skill packages, and local documentation links")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, json.JSONDecodeError, yaml.YAMLError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)
