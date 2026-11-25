# SlopStop

[![Checks](https://github.com/sumal-sportingrisk/StopSlop/actions/workflows/checks.yml/badge.svg)](https://github.com/sumal-sportingrisk/StopSlop/actions/workflows/checks.yml)

Skills that stop AI coding agents from producing slop: bloated code, weakened tests, unsafe queries, and documentation that doesn't match the code.

| Skill | Use it for |
| --- | --- |
| [slopstop-python-r](skills/slopstop-python-r/SKILL.md) | Writing, cleaning up, and reviewing Python and R code, including tests and dead code |
| [slopstop-security](skills/slopstop-security/SKILL.md) | Security reviews: credentials, SQL Server and MongoDB queries, AWS IAM, and access control |
| [slopstop-docs](skills/slopstop-docs/SKILL.md) | READMEs, how-to guides, reference pages, and runbooks that match the code |

## Install in Claude Code

Each person does this once. It then works in every project, and the steps are the same on Windows, macOS, and Ubuntu.

1. Update Claude Code. In a terminal, run:

   ```sh
   claude update
   ```

   Then run `claude --version`. You need 2.1.275 or later.

2. Start Claude Code and type:

   ```text
   /plugin install slopstop --marketplace sumal-sportingrisk/StopSlop
   ```

3. Type `/plugin` and check that `slopstop` is listed as installed.

If you can't update past 2.1.275, use these two commands instead of step 2:

```text
/plugin marketplace add sumal-sportingrisk/StopSlop
/plugin install slopstop@stopslop
```

### Get updates

Updates are not automatic. Either:

- type `/plugin marketplace update stopslop` when you want the latest version, or
- turn on automatic updates once: type `/plugin`, open **Marketplaces**, select `stopslop`, and enable auto-update.

## Install in Codex or other agents

1. You need Node.js. Check with `node --version`. If it is missing, install the current LTS release:

   | OS | Command |
   | --- | --- |
   | Windows | `winget install OpenJS.NodeJS.LTS` |
   | macOS | `brew install node` |
   | Ubuntu | Use [nvm](https://github.com/nvm-sh/nvm). The `nodejs` package in older Ubuntu releases may be too old. |

2. Update Codex to the latest version, using the same method you installed it with. For an npm install:

   ```sh
   npm install -g @openai/codex@latest
   ```

   Older Codex versions may not load skills.

3. Run this once, in PowerShell on Windows or a terminal on macOS and Ubuntu:

   ```sh
   npx skills@latest add sumal-sportingrisk/StopSlop -g -a codex -y
   ```

   `@latest` makes sure `npx` uses the current skills CLI rather than an older cached copy.

This installs the skills for Codex in every project. To install for a different agent, change `codex`. This command has not yet been tested against this repository.

<details>
<summary>Install without Node.js</summary>

Clone the repository and copy the skill folders into your project. Do not copy `evals/`.

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

To update, run `git pull` in `StopSlop` and copy again.

</details>

## Use

You usually don't need to do anything: the agent picks the right skill when your request matches it. For example:

```text
Simplify these functions without changing behavior.
Review this SQL and MongoDB code for security issues. Don't edit anything.
Update the README so it matches the actual setup commands.
```

To call a skill directly:

| Skill | Claude Code | Codex |
| --- | --- | --- |
| Python and R | `/slopstop:slopstop-python-r` | `$slopstop-python-r` |
| Security | `/slopstop:slopstop-security` | `$slopstop-security` |
| Documentation | `/slopstop:slopstop-docs` | `$slopstop-docs` |

The skills guide the agent; they don't guarantee correct code. Review what it produces.

## More

- [Validation status](docs/status.md): what has been tested, and the evaluation results so far.
- [Development and checks](docs/development.md): running the checks, CI, pre-commit hooks, and the repository layout.
- [Evaluation guide](evals/README.md): how the skills are tested against agents.
- [References](docs/references.md): sources that informed the skills, and companion skills worth installing.
