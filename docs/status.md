# Validation status

What has and has not been checked. For how to run evaluations, see [the evaluation guide](../evals/README.md).

| Area | Status |
| --- | --- |
| Three skill packages and local links | Checked locally; four package-check tests pass |
| Secret-scan control protocol | Unit tests pass with simulated scanner responses; the real Gitleaks 8.30.1 control passes locally and in CI |
| Evaluation preparer and fixture starting states | Five harness tests pass across 15 fixture cases and three loading conditions |
| R reference examples | Executed locally with missingness and dimension checks |
| Ruff and Bandit | Pass locally with `requirements-dev.txt` installed |
| CI (all checks, including lintr and Gitleaks) | Passing on `main` |
| Claude Code plugin | `claude plugin validate .` passes; installed end to end on macOS with `claude plugin install slopstop@stopslop` (Claude Code 2.1.332). Not yet confirmed on Windows or Ubuntu |
| Paired agent evaluation | 16-run pilot completed with in-session subagents, not OS-sandboxed: no correctness difference between conditions (ceiling effect); skill runs redacted secrets and reported check status more reliably. A sandboxed CLI run is still blocked |
| Automatic skill loading | Not verified; `skill-implicit` is implemented in the preparer but has not been run in an agent |

The 16-run pilot compared four cases with baseline/explicit skill loading, twice each, using Claude Opus 5.5 subagents inside a Claude Code session. [The pilot results](../evals/results/2026-11-25-pilot.md) found no correctness difference: all runs passed in both conditions. The skill changed reporting: secrets were redacted and checks were labeled PASS/NOT RUN, but security findings were all rated High (since addressed with a severity scale). Those subagents were instructed, not sandboxed, to stay in their workspaces, and the pilot predates the skill split. A separate [CLI preflight](../evals/results/pilot-preflight.json) for a sandboxed run was blocked before inference. Automatic discovery is untested. To run the harness checks without launching agents:

```sh
python3 -B -m unittest discover -s evals -p 'test_prepare.py' -v
```

Python 3 and Rscript are required for those checks. Documentation and security fixtures are synthetic review tasks, not reconstructions of real team incidents or completed evaluations. A data-correctness skill remains a later option.
