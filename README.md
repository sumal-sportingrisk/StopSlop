# SlopStop

[![Checks](https://github.com/sumal-sportingrisk/StopSlop/actions/workflows/checks.yml/badge.svg)](https://github.com/sumal-sportingrisk/StopSlop/actions/workflows/checks.yml)

Three loadable skills for code quality, security, and documentation across Python, R, MongoDB, SQL Server, and AWS. They guide agent decisions while preserving project conventions and public behavior. Mechanical checks are configured separately in CI and optional local hooks.

| Skill | Use it for |
| --- | --- |
| [slopstop-python-r](skills/slopstop-python-r/SKILL.md) | Writing and cleaning up Python/R code, reviewing complexity, dead code, and tests |
| [slopstop-security](skills/slopstop-security/SKILL.md) | Trust boundaries, credentials, SQL/Mongo queries, IAM, and access-control reviews |
| [slopstop-docs](skills/slopstop-docs/SKILL.md) | Accurate README files, how-to guides, reference pages, runbooks, and checked examples |

## Install

**Claude Code** (2.1.275 or later), once per person:

```text
/plugin install slopstop --marketplace sumal-sportingrisk/StopSlop
```

On older versions, run `/plugin marketplace add sumal-sportingrisk/StopSlop`, then `/plugin install slopstop@stopslop`. The skills are then available in every project as `/slopstop:slopstop-python-r`, `/slopstop:slopstop-security`, and `/slopstop:slopstop-docs`, and Claude also loads them when a task matches their descriptions. Auto-update is off by default for third-party marketplaces: turn it on under **Marketplaces** in `/plugin`, or run `/plugin marketplace update stopslop` to pull changes.

The plugin command is the same on Windows, macOS, and Ubuntu because it runs inside Claude Code.

**Codex and other agents:** the [skills CLI](https://github.com/vercel-labs/skills) installs from this repository. It needs Node.js, which provides `npx`. Install a current LTS release if `node --version` fails:

| OS | Install Node.js |
| --- | --- |
| Windows | `winget install OpenJS.NodeJS.LTS`, or the installer from [nodejs.org](https://nodejs.org/) |
| macOS | `brew install node`, or the installer from [nodejs.org](https://nodejs.org/) |
| Ubuntu | [nvm](https://github.com/nvm-sh/nvm) or [NodeSource](https://github.com/nodesource/distributions); the `nodejs` package in older Ubuntu releases may be too old |

Then run this once, in PowerShell on Windows or a terminal on macOS and Ubuntu:

```sh
npx skills add sumal-sportingrisk/StopSlop -g -a codex -y
```

`-g` installs for your user so the skills apply in every project, `-a codex` targets Codex (repeat `-a` for more agents), and `-y` skips the prompts. Without these flags the CLI asks which skills, agents, and scope to use, and installs into the current project only. This command has not yet been tested against this repository.

Without Node.js, clone the repository and copy the skill folders into a project's `.agents/skills/` directory. Do not copy `evals/`.

macOS and Ubuntu:

```sh
git clone https://github.com/sumal-sportingrisk/StopSlop.git
mkdir -p your-project/.agents/skills
cp -R StopSlop/skills/* your-project/.agents/skills/
```

Windows (PowerShell):

```powershell
git clone https://github.com/sumal-sportingrisk/StopSlop.git
New-Item -ItemType Directory -Force your-project\.agents\skills | Out-Null
Copy-Item -Recurse StopSlop\skills\* your-project\.agents\skills\
```

Run `git pull` in `StopSlop` and copy again to update. In Codex, invoke `$slopstop-python-r`, `$slopstop-security`, or `$slopstop-docs`; `agents/openai.yaml` supplies optional Codex UI metadata.

## Use

Ask for a skill by name, or let the agent pick it up from the task. For example:

```text
Use slopstop-python-r to simplify the selected functions without changing behavior.
```

```text
Use slopstop-security to review the selected SQL and MongoDB access code without editing.
```

```text
Use slopstop-docs to update this README against the actual setup commands and code.
```

You can also ask an agent to read a skill's `SKILL.md` directly. Discovery depends on the host agent and remains unverified for these packages. Instructions and passing static checks do not guarantee correctness.

## Scope and structure

The Python/R skill deliberately covers writing as well as cleanup and review; it loads language-specific references and conditionally loads testing or dead-code guidance. Dedicated security and documentation tasks have separate entry points. The Claude Code plugin installs all three; with other agents, each skill folder can be installed on its own. [AGENTS.md](AGENTS.md) and [CLAUDE.md](CLAUDE.md) route repository work to the relevant package; installing the packages elsewhere does not install those routing files.

- Cleanup preserves behavior within the requested scope; a focused fix leaves unrelated code alone.
- Reviews are read-only unless edits were requested. Comment-only work preserves executable behavior and directives.
- Python checks cover defaults, closures, optional imports, mutation, dataframes, resources, and built artifacts.
- R checks cover missingness, recycling, dimensions, attributes, conditions, state, and package compatibility.
- Tests must verify behavior and must not be weakened merely to obtain a green result.
- Security guidance follows trust boundaries, preserves existing protections, and includes checks for SQL Server, MongoDB, and AWS. It is not a complete security audit.
- Verification distinguishes PASS, FAIL, NOT RUN, and N/A, with no arbitrary coverage or function-length quotas.

## Evaluation

[The evaluation guide](evals/README.md) describes fixture preparation, isolated paired runs, and yes/no grading. Prompts, fixtures, grading keys, and a [case index and backlog](evals/scenarios.md) live under `evals/`, outside the installable skill. The evaluator must keep grading material inaccessible to the agent; directory placement alone is not isolation.

Current validation status:

| Area | Status |
| --- | --- |
| Three skill packages and local links | Checked locally; four package-check tests pass |
| Secret-scan control protocol | Unit tests pass with simulated scanner responses; the real Gitleaks 8.30.1 control passes locally and in CI |
| Evaluation preparer and fixture starting states | Five harness tests pass across 15 fixture cases and three loading conditions |
| R reference examples | Executed locally with missingness and dimension checks |
| Ruff and Bandit | Pass locally with `requirements-dev.txt` installed |
| CI (all checks, including lintr and Gitleaks) | Passing on `main` |
| Claude Code plugin | `claude plugin validate .` passes; an end-to-end install has not been confirmed |
| Paired agent evaluation | 16-run pilot completed with in-session subagents, not OS-sandboxed: no correctness difference between conditions (ceiling effect); skill runs redacted secrets and reported check status more reliably. A sandboxed CLI run is still blocked |
| Automatic skill loading | Not verified; `skill-implicit` is implemented in the preparer but has not been run in an agent |

The 16-run pilot compared four cases with baseline/explicit skill loading, twice each, using Claude Opus 5.5 subagents inside a Claude Code session. [The pilot results](evals/results/2026-11-25-pilot.md) found no correctness difference: all runs passed in both conditions. The skill changed reporting: secrets were redacted and checks were labeled PASS/NOT RUN, but security findings were all rated High (since addressed with a severity scale). Those subagents were instructed, not sandboxed, to stay in their workspaces, and the pilot predates the skill split. A separate [CLI preflight](evals/results/pilot-preflight.json) for a sandboxed run was blocked before inference. Automatic discovery is untested. To run the harness checks without launching agents:

```sh
python3 -B -m unittest discover -s evals -p 'test_prepare.py' -v
```

Python 3 and Rscript are required for those checks. Documentation and security fixtures are synthetic review tasks, not reconstructions of real team incidents or completed evaluations. A data-correctness skill remains a later option.

## Checks and enforcement

[GitHub Actions](.github/workflows/checks.yml) is configured to run package/link checks, unit tests, fixture starting-state checks, R examples, Ruff, Bandit, lintr, and Gitleaks history/current-file scans. It uses read-only repository permissions and pinned action commits; the Gitleaks download is pinned and checksum-verified. It runs on every push and pull request. To make passing CI a merge requirement, add the `quality` and `secrets` jobs as required status checks in the repository's branch protection settings.

Install development tools in your Python environment, then run checks from the repository root:

```sh
python3 -m pip install -r requirements-dev.txt
python3 scripts/check_packages.py
python3 -B -m unittest discover -s tests -v
python3 -B -m unittest discover -s evals -p 'test_prepare.py' -v
Rscript --vanilla tests/check_r_examples.R
python3 -m ruff check scripts evals/prepare.py evals/test_prepare.py tests
python3 -m bandit -c pyproject.toml -r scripts evals/prepare.py
```

CI uses Python 3.12 and R 4.5.2. It also checks that the documented credential placeholders are allowed while a non-exempt synthetic token in the same fixture is detected. For the R linter, install lintr in your development R environment and run:

```sh
Rscript --vanilla -e 'install.packages("lintr", repos = "https://cloud.r-project.org")'
Rscript --vanilla -e 'findings <- lintr::lint_dir("tests"); print(findings); if (length(findings)) quit(status = 1L)'
```

[The optional pre-commit configuration](.pre-commit-config.yaml) uses system-installed tools. Install the Python development dependencies, the pre-commit framework, lintr, and Gitleaks 8.30.1 before enabling it with `pre-commit install`. Hook installation changes the current repository's Git configuration and has not been performed here. Local hooks can be bypassed; CI is the shared enforcement point once its checks are required.

Intentional evaluation fixtures are excluded from style/security linting so their seeded defects remain available to evaluate agents. Secret scanning still covers them. [The Gitleaks config](.gitleaks.toml) uses only the default rules, which already ignore AWS's documented example keys used by the security fixture. It has no path allowlist: gitleaks skips allowlisted paths entirely, which an earlier version of this config did, so the fixture file was never scanned. CI's control check confirms the fixture is scanned and that a non-placeholder token in it is detected. There are no Claude Code hooks or live-account scanners configured.

## References consulted

These sources informed independently written guidance. They are optional human references, not runtime dependencies or instructions to fetch while using the skill.

- [Continuous Claude: dead-code](https://github.com/parcadei/continuous-claude-v3/blob/main/.claude/skills/dead-code/SKILL.md): on-demand reachability and impact inspection.
- Posit: [R style](https://github.com/posit-dev/skills/blob/main/r-lib/r-tidyverse-style/SKILL.md), [package development](https://github.com/posit-dev/skills/blob/main/r-lib/r-package-development/SKILL.md), and [lifecycle](https://github.com/posit-dev/skills/blob/main/r-lib/r-lifecycle/SKILL.md): separate style from behavioral changes and preserve supported interfaces.
- Posit: [test review](https://github.com/posit-dev/skills/blob/main/posit-dev/review-testing/SKILL.md) and [testthat](https://github.com/posit-dev/skills/blob/main/r-lib/r-testthat/SKILL.md): useful assertions, isolated state, mocks, and snapshots.
- Python Skills: [code quality](https://github.com/wdm0006/python-skills/blob/main/skills/python/code-quality/SKILL.md), [API design](https://github.com/wdm0006/python-skills/blob/main/skills/python/api-design/SKILL.md), [deferred dependencies](https://github.com/wdm0006/python-skills/blob/main/skills/python/lazy-dependencies/SKILL.md), [packaging](https://github.com/wdm0006/python-skills/blob/main/skills/python/packaging/SKILL.md), and [testing](https://github.com/wdm0006/python-skills/blob/main/skills/python/testing-strategy/SKILL.md): explicit partial results, mutation contracts, cold-path costs, artifact checks, and discriminating regression fixtures.
- [OpenAI security best practices](https://github.com/openai/skills/blob/main/skills/.curated/security-best-practices/SKILL.md) and its [FastAPI reference](https://github.com/openai/skills/blob/main/skills/.curated/security-best-practices/references/python-fastapi-web-server-security.md): framework-aware scope, trusted authority, security-preserving fixes, and evidence-based findings. R guidance here is independently written; that skill does not supply an R reference.
- [Firebase security rules auditor](https://github.com/firebase/agent-skills/blob/main/skills/firebase-security-rules-auditor/SKILL.md): the general points that authority must come from trusted identity and that field restrictions are not ownership checks. Firebase-specific checks were dropped because the team does not use Firebase.
- Stack documentation: SQL Server [`sp_executesql`](https://learn.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/sp-executesql-transact-sql), MongoDB [`$where`](https://www.mongodb.com/docs/manual/reference/operator/query/where/), and [AWS IAM security best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html).
- Official Python documentation: [default arguments](https://docs.python.org/3/tutorial/controlflow.html#default-argument-values), [closure binding](https://docs.python.org/3/faq/programming.html#why-do-lambdas-defined-in-a-loop-with-different-values-all-return-the-same-result), and [pickle trust requirements](https://docs.python.org/3/library/pickle.html).
- Official R documentation: [logical operators](https://stat.ethz.ch/R-manual/R-devel/library/base/html/Logic.html), [sequences](https://stat.ethz.ch/R-manual/R-devel/library/base/html/seq.html), [conditional selection](https://stat.ethz.ch/R-manual/R-devel/library/base/html/ifelse.html), [near equality](https://stat.ethz.ch/R-manual/R-devel/library/base/html/all.equal.html), and [system2 argument quoting](https://stat.ethz.ch/R-manual/R-devel/library/base/html/system2.html).
- pandas documentation: [copy-on-write and assignment](https://pandas.pydata.org/docs/user_guide/copy_on_write.html).
- Documentation: [Diátaxis](https://diataxis.fr/), Anthropic's [doc-coauthoring](https://github.com/anthropics/skills/blob/main/skills/doc-coauthoring/SKILL.md), and AWS's [document-service](https://github.com/awslabs/agent-plugins/blob/main/plugins/codebase-documentor-for-aws/skills/document-service/SKILL.md): distinct reader tasks, source-grounded explanations, and reader testing.
- Security review: Trail of Bits' [differential-review](https://github.com/trailofbits/skills/blob/main/plugins/differential-review/skills/differential-review/SKILL.md) and [sharp-edges](https://github.com/trailofbits/skills/blob/main/plugins/sharp-edges/skills/sharp-edges/SKILL.md): removed controls, affected callers, and misuse-resistant interfaces. The new instructions express these ideas independently; upstream text and required workflows were not copied.
- Verification: [verification-before-completion](https://github.com/obra/superpowers/blob/main/skills/verification-before-completion/SKILL.md): inspect evidence and diffs before making completion claims, adapted to proportional checks and explicit NOT RUN reporting.

Specialist companion candidates are the official [MongoDB skills](https://github.com/mongodb/agent-skills), [AWS SDK Python](https://github.com/aws/agent-toolkit-for-aws/blob/main/skills/core-skills/aws-sdk-python-usage/SKILL.md) and [IAM](https://github.com/aws/agent-toolkit-for-aws/blob/main/skills/core-skills/aws-iam/SKILL.md) skills, and Microsoft's [T-SQL correctness](https://github.com/microsoft/microsoft-sql/blob/main/plugins/microsoft-sql/skills/t-sql-correctness/SKILL.md) and [injection prevention](https://github.com/microsoft/microsoft-sql/blob/main/plugins/microsoft-sql/skills/prevent-sql-injection/SKILL.md). Review each scope, license, and operational permissions before installation; Microsoft's linked skills target Azure SQL Database, so verify details against your SQL Server engine. These companion skills are not bundled or installed by this repository.
