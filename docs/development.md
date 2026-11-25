# Development and checks

[GitHub Actions](../.github/workflows/checks.yml) is configured to run package/link checks, unit tests, fixture starting-state checks, R examples, Ruff, Bandit, lintr, and Gitleaks history/current-file scans. It uses read-only repository permissions and pinned action commits; the Gitleaks download is pinned and checksum-verified. It runs on every push and pull request. To make passing CI a merge requirement, add the `quality` and `secrets` jobs as required status checks in the repository's branch protection settings.

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

[The optional pre-commit configuration](../.pre-commit-config.yaml) uses system-installed tools. Install the Python development dependencies, the pre-commit framework, lintr, and Gitleaks 8.30.1 before enabling it with `pre-commit install`. Hook installation changes the current repository's Git configuration and has not been performed here. Local hooks can be bypassed; CI is the shared enforcement point once its checks are required.

Intentional evaluation fixtures are excluded from style/security linting so their seeded defects remain available to evaluate agents. Secret scanning still covers them. [The Gitleaks config](../.gitleaks.toml) uses only the default rules, which already ignore AWS's documented example keys used by the security fixture. It has no path allowlist: gitleaks skips allowlisted paths entirely, which an earlier version of this config did, so the fixture file was never scanned. CI's control check confirms the fixture is scanned and that a non-placeholder token in it is detected. There are no Claude Code hooks or live-account scanners configured.

## Repository layout

- `plugin/`: everything the Claude Code plugin installs, and nothing else. `plugin/skills/` holds the three skills, each with a `SKILL.md` and optional `references/`; `plugin/.claude-plugin/plugin.json` is the plugin manifest.
- `.claude-plugin/marketplace.json`: the marketplace manifest, pointing at `./plugin`. Validate with `claude plugin validate .` and `claude plugin validate plugin`.
- `evals/`: behavioral evaluation cases, grading keys, and results. Never install this with the skills. See [the evaluation guide](../evals/README.md).
- `scripts/` and `tests/`: package, link, secret-scan, and R example checks.
- [AGENTS.md](../AGENTS.md) and [CLAUDE.md](../CLAUDE.md): instructions for agents working in this repository.

