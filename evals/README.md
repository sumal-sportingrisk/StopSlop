# SlopStop behavioral evaluation

This directory is for the evaluator, not the agent under evaluation. Do not install it with the skill or let the agent browse this repository during a run.

## Cases and preparation

Fifteen cases under `cases/` each contain a user prompt, a concrete `fixture/`, and private `grading.json` criteria: seven code/testing cases, five security cases, and three documentation cases. Prompts are deliberately phrased the way a colleague would ask, without restating the behavior being graded; contracts the agent must respect live in the fixture's code and docs. Do not add hints to a prompt to make a case pass, because the baseline gets the same hints. [The case index and backlog](scenarios.md) lists coverage and future fixture candidates.

Cases can declare the skill under test in `skills.json`, outside the agent workspace. Code cases default to `slopstop-python-r`; security and documentation cases select their respective standalone skill. The preparer copies only those skill packages, not the selection file or grading key.

From this repository's root, prepare a fresh run outside the repository:

```sh
python3 evals/prepare.py scoped-fix --condition baseline --output /tmp/slopstop-scoped-baseline-1
python3 evals/prepare.py scoped-fix --condition skill --output /tmp/slopstop-scoped-skill-1
```

The preparer refuses to overwrite an existing output or write inside this repository. It produces:

- `workspace/`: fixture files and, for the skill conditions, the selected packages under `.agents/skills/`.
- `task.txt`: the user prompt. The `skill` condition prefixes an instruction to read the skill; `skill-implicit` installs the skill without that instruction, to test whether it triggers on its own.
- `baseline.json`: original workspace file hashes for evaluator comparison, including the skill condition's installed instructions.

The preparer launches no agent and performs no grading. For Claude Code runs, use `--agent claude` so the skill is placed in `.claude/skills/`. Baseline and skill runs must use the same host and capabilities.

## Isolation and paired runs

Launch each run in a fresh session with only `workspace/` mounted or otherwise accessible as its filesystem workspace. Send `task.txt` as the task; do not expose the task file's parent directory, this source checkout, the grading keys, supplemental scenarios, or results from other runs. Merely setting the current directory is insufficient if tools can still read the source checkout. Disable unrelated skills, persistent memory, and network access unless a case explicitly needs them. Do not score a run as independent if those conditions cannot be established.

Use the same model, runtime versions, tools, permissions, and token/time limits for both conditions. Alternate or randomize condition order. The authorized pilot is `scoped-fix`, `test-integrity`, `keep-simple`, and `security-review` × `baseline`/`skill` × two runs = 16 runs. It was run with in-session subagents that were not OS-sandboxed; see [the results](results/2026-11-25-pilot.md). A separate sandboxed CLI attempt was blocked before inference; see [the preflight record](results/pilot-preflight.json).

Run each evaluated agent with a fresh, empty Claude Code configuration (for example `CLAUDE_CONFIG_DIR` pointing at a new temporary directory). A normal install of this repository's marketplace clones the whole repository, including these grading keys, into `~/.claude/plugins/marketplaces/`, so an agent using your usual configuration could read them. Record the source commit and installed skill file hashes for each actual run. The skill split and new fixtures must be identified as a different version from the preflight source. Report null results honestly. If later cases are revised to address ambiguity or ceiling effects, keep the earlier results and version the changed cases rather than replacing inconvenient evidence. A full round across all 15 cases, three conditions, and three repeats would be 135 runs; those additional runs have not been authorized or executed.

Capture prompts, transcripts, tool commands and outputs, final responses, file changes, runtime versions, and budgets outside the agent workspace. Keep initial fixture files untouched. Account for generated caches separately when comparing content changes.

## Grading

Grade observable behavior, not phrasing, using [common criteria](common-grading.json) plus the case's `grading.json`. Every criterion is phrased so **yes** is favorable. Mark yes, no, or not assessable and attach evidence such as a diff, a command receipt, or a response excerpt. Do not guess unobserved intent. For review cases, necessary diagnosis can be expressed without a particular rule ID.

Compare the final workspace with `baseline.json` and the original fixture. Check reported verification against actual tool receipts. Run the case's evaluator checks on a separate copy of the final artifact so grading cannot contaminate the agent's output. Preserve original tests when checking test-integrity cases; a green edited suite is insufficient evidence.

Report per-criterion outcomes and denominators separately for each condition and case, including runtime blocks and not-assessable results. Report unnecessary edits, permission questions, false findings on valid code, and unsupported PASS claims explicitly. Treat a small paired experiment as directional evidence; it cannot prove universal effectiveness.

Fixtures contain intentional defects. Their initial failing tests establish the starting state, not a repository regression. A fixture smoke check is not a behavioral agent run. Its `upload.py` uses AWS's documented placeholder keys (`AKIAIOSFODNN7EXAMPLE`), not real credentials. Gitleaks' default rules ignore them; do not allowlist the fixture path, because that stops the file being scanned at all.

To verify the preparer and fixture starting states without launching agents, run `python3 -B -m unittest discover -s evals -p 'test_prepare.py' -v`. Python 3 and Rscript must be available. These tests also cover overwrite refusal and the Codex/Claude skill destinations. They do not provide operating-system isolation; the evaluator must enforce that separately.
