# SlopStop behavioral evaluation

This directory is for the evaluator, not the agent under evaluation. Do not install it with the skill or let the agent browse this repository during a run.

## Cases and preparation

Eight cases under `cases/` each contain a user prompt, a concrete `fixture/`, and private `grading.json` criteria. Prompts are deliberately phrased the way a colleague would ask, without restating the behavior being graded; contracts the agent must respect live in the fixture's code and docs. Do not add hints to a prompt to make a case pass, because the baseline gets the same hints. [The case index and backlog](scenarios.md) lists current coverage and future fixture candidates; it contains no completed results.

From this repository's root, prepare a fresh run outside the repository:

```sh
python3 evals/prepare.py scoped-fix --condition baseline --output /tmp/slopstop-scoped-baseline-1
python3 evals/prepare.py scoped-fix --condition skill --output /tmp/slopstop-scoped-skill-1
```

The preparer refuses to overwrite an existing output or write inside this repository. It produces:

- `workspace/`: fixture files and, for the skill conditions, `.agents/skills/slopstop-python-r/`.
- `task.txt`: the user prompt. The `skill` condition prefixes an instruction to read the skill; `skill-implicit` installs the skill without that instruction, to test whether it triggers on its own.
- `baseline.json`: original workspace file hashes for evaluator comparison, including the skill condition's installed instructions.

The preparer launches no agent and performs no grading. For Claude Code runs, use `--agent claude` so the skill is placed in `.claude/skills/`. Baseline and skill runs must use the same host and capabilities.

## Isolation and paired runs

Launch each run in a fresh session with only `workspace/` mounted or otherwise accessible as its filesystem workspace. Send `task.txt` as the task; do not expose the task file's parent directory, this source checkout, the grading keys, supplemental scenarios, or results from other runs. Merely setting the current directory is insufficient if tools can still read the source checkout. Disable unrelated skills, persistent memory, and network access unless a case explicitly needs them. Do not score a run as independent if those conditions cannot be established.

Use the same model, runtime versions, tools, permissions, and token/time limits for both conditions. Alternate or randomize condition order. Start with a pilot: `scoped-fix`, `test-integrity`, `keep-simple`, and `security-review` × `baseline`/`skill` × two runs = 16 runs. If the pilot shows no difference between conditions, revise the cases before scaling up. A full round is eight cases × three conditions × three runs = 72 runs. This is a proposed experiment, not an automatically authorized execution. Record any environment limitations and contamination rather than interpreting them as a skill effect.

Capture prompts, transcripts, tool commands and outputs, final responses, file changes, runtime versions, and budgets outside the agent workspace. Keep initial fixture files untouched. Account for generated caches separately when comparing content changes.

## Grading

Grade observable behavior, not phrasing, using [common criteria](common-grading.json) plus the case's `grading.json`. Every criterion is phrased so **yes** is favorable. Mark yes, no, or not assessable and attach evidence such as a diff, a command receipt, or a response excerpt. Do not guess unobserved intent. For review cases, necessary diagnosis can be expressed without a particular rule ID.

Compare the final workspace with `baseline.json` and the original fixture. Check reported verification against actual tool receipts. Run the case's evaluator checks on a separate copy of the final artifact so grading cannot contaminate the agent's output. Preserve original tests when checking test-integrity cases; a green edited suite is insufficient evidence.

Report per-criterion outcomes and denominators separately for each condition and case, including runtime blocks and not-assessable results. Report unnecessary edits, permission questions, false findings on valid code, and unsupported PASS claims explicitly. Treat a small paired experiment as directional evidence; it cannot prove universal effectiveness.

Fixtures contain intentional defects. Their initial failing tests establish the starting state, not a repository regression. A fixture smoke check is not a behavioral agent run. The `security-review` case prohibits commands during the run; that restriction does not prohibit the evaluator from inspecting the fixture afterward. Its `upload.py` uses AWS's documented placeholder keys (`AKIAIOSFODNN7EXAMPLE`), not real credentials; secret scanners may still flag them, so allowlist that path if needed.

To verify the preparer and fixture starting states without launching agents, run `python3 -B -m unittest discover -s evals -p 'test_prepare.py' -v`. Python 3 and Rscript must be available. These tests also cover overwrite refusal and the Codex/Claude skill destinations. They do not provide operating-system isolation; the evaluator must enforce that separately.
