# SlopStop

A loadable skill for writing, cleaning up, and reviewing Python and R code. It targets unnecessary complexity, misleading comments, hidden failures, unsafe dead-code removal, and weak verification while preserving project conventions and public behavior.

## Install and use

Copy the entire [`skills/slopstop-python-r`](skills/slopstop-python-r/SKILL.md) folder, including its references, into your agent's project skill directory. From this repository's root, choose the matching destination below and replace `your-project` with the target project's relative directory:

```sh
# Codex
mkdir -p ../your-project/.agents/skills
cp -R skills/slopstop-python-r ../your-project/.agents/skills/

# Claude Code
mkdir -p ../your-project/.claude/skills
cp -R skills/slopstop-python-r ../your-project/.claude/skills/
```

Check for an existing skill of the same name before copying; review it rather than merging or overwriting it blindly. Other agents may use different directories. `agents/openai.yaml` supplies optional Codex UI metadata; the skill itself is plain Markdown with YAML frontmatter.

In Codex, explicitly invoke `$slopstop-python-r`. In Claude Code, invoke `/slopstop-python-r` or ask to use the skill by name; see the [Claude Code skill documentation](https://code.claude.com/docs/en/skills). For example:

```text
Use slopstop-python-r to simplify the selected functions without changing behavior.
```

```text
Use slopstop-python-r to review this R package. Report findings without editing.
```

You can also ask an agent to read `skills/slopstop-python-r/SKILL.md` directly. Discovery depends on the host agent. This is an instruction package, not a static analyzer or a guarantee of correctness.

## Scope and structure

The broad trigger is intentional: the original scope includes writing Python and R code as well as cleanup and review. The entry point loads the relevant language reference; testing, dead-code, and security references are conditional. Evaluation should determine whether that context cost is justified.

- Cleanup preserves behavior within the requested scope; a focused fix leaves unrelated code alone.
- Reviews are read-only unless edits were requested. Comment-only work preserves executable behavior and directives.
- Python checks cover defaults, closures, optional imports, mutation, dataframes, resources, and built artifacts.
- R checks cover missingness, recycling, dimensions, attributes, conditions, state, and package compatibility.
- Tests must verify behavior and must not be weakened merely to obtain a green result.
- Security guidance follows trust boundaries, preserves existing protections, and covers the team stack: SQL Server, MongoDB, and AWS.
- Verification distinguishes PASS, FAIL, NOT RUN, and N/A, with no arbitrary coverage or function-length quotas.

## Evaluation

[The evaluation guide](evals/README.md) describes fixture preparation, isolated paired runs, and yes/no grading. Prompts, fixtures, grading keys, and supplemental scenarios live under `evals/`, outside the installable skill. The evaluator must keep grading material inaccessible to the agent; directory placement alone is not isolation.

Packaging checks and fixture smoke checks do not establish that the skill improves agent behavior. No paired agent results are claimed until those runs are performed and graded.

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
