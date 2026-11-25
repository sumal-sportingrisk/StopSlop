"""Prepare isolated inputs for a manual paired agent evaluation; never launch agents."""

import argparse
import hashlib
import json
import shutil
from pathlib import Path


def prepare(case_name, condition, output, agent):
    repo = Path(__file__).resolve().parents[1]
    case = repo / "evals" / "cases" / case_name
    if not (case / "fixture").is_dir() or not (case / "prompt.txt").is_file():
        raise ValueError(f"Incomplete evaluation case: {case_name}")
    selection_path = case / "skills.json"
    selection = json.loads(selection_path.read_text(encoding="utf-8")) if selection_path.exists() else ["slopstop-python-r"]
    if not isinstance(selection, list) or not selection:
        raise ValueError(f"{case_name}: skills.json must contain a nonempty list")
    available = {path.name for path in (repo / "skills").iterdir() if path.is_dir()}
    if any(not isinstance(name, str) or name not in available for name in selection):
        raise ValueError(f"{case_name}: unknown skill selection")

    output = output.resolve()
    if output == repo or repo in output.parents:
        raise ValueError("Evaluation output must be outside this repository")
    output.mkdir(parents=True, exist_ok=False)
    workspace = output / "workspace"
    shutil.copytree(case / "fixture", workspace)

    prompt = (case / "prompt.txt").read_text(encoding="utf-8")
    if condition in ("skill", "skill-implicit"):
        directory = ".claude" if agent == "claude" else ".agents"
        entrypoints = []
        for name in selection:
            destination = workspace / directory / "skills" / name
            shutil.copytree(repo / "skills" / name, destination)
            entrypoints.append((destination.relative_to(workspace) / "SKILL.md").as_posix())
        if condition == "skill":
            prompt = f"Read and apply {', '.join(entrypoints)} to this task.\n\n{prompt}"

    (output / "task.txt").write_text(prompt, encoding="utf-8")
    hashes = {
        path.relative_to(workspace).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(workspace.rglob("*"))
        if path.is_file()
    }
    (output / "baseline.json").write_text(
        json.dumps({"case": case_name, "condition": condition, "agent": agent, "skills": selection if condition != "baseline" else [], "files": hashes}, indent=2)
        + "\n",
        encoding="utf-8",
    )
    return output


def main():
    cases = Path(__file__).resolve().parent / "cases"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=sorted(path.name for path in cases.iterdir() if path.is_dir()))
    parser.add_argument("--condition", required=True, choices=("baseline", "skill", "skill-implicit"))
    parser.add_argument("--agent", default="codex", choices=("codex", "claude"))
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        output = prepare(args.case, args.condition, args.output, args.agent)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Preparation failed: {error}\n")
    print(f"Prepared {output}; no agent has been launched.")


if __name__ == "__main__":
    main()
