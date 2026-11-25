---
name: slopstop-python-r
description: Prevent and review AI-generated code bloat in Python and R. Apply when writing, refactoring, or reviewing Python modules, R scripts or packages, notebooks, and data pipelines for clean code, explicit data semantics, and meaningful verification. Also use for requests to remove AI slop from Python or R code. Dedicated security audits and documentation authoring have separate skills.
---

# SlopStop for Python and R

Produce code a maintainer can understand, run, and change. Judge a pattern by the problem it solves and the behavior it preserves. Shorter code is useful only when it remains clear and correct.

## Choose scope from the request

- **Build or fix:** apply the rules while working and complete the requested changes. A request to fix code already authorizes those fixes; do not insert a separate audit approval round.
- **Cleanup, remove slop, or simplify:** use fix mode within the named files and preserve behavior. If no files are named, infer the smallest relevant scope from the request or clarify before broad cleanup.
- **Review or audit:** inspect and report findings without editing unless the user requested edits too. Return findings in the conversation unless a saved report was requested.
- **Comments only:** edit comments and docstrings only. Preserve executable code, directives, licenses, and tool annotations. Report discovered bugs without silently fixing them.

Read applicable repository instructions and nearby code before proposing conventions. Inspect runtime constraints, dependency manifests, formatter/linter settings, and relevant tests. Preserve public interfaces and scientific assumptions unless changing them is part of the request. Ask only about ambiguity that affects correctness or scope; otherwise proceed using the repository's conventions.

Apply these rules to code you write or touch. Keep unrelated improvements out of a focused fix, including elsewhere in the same file. Mention material unrelated defects separately rather than expanding the edit.

Read [the Python reference](references/python.md) for Python work and [the R reference](references/r.md) for R work. Read both for mixed pipelines, including exchanged files and missing-value conventions.

For unused-code reviews or removal, read [the dead-code workflow](references/dead-code.md). Run broader reachability analysis on demand when relevant to the request, rather than at every session start.

For test-quality reviews or substantive changes to tests, read [the testing reference](references/testing.md). Apply it to Python and R using the project's existing test framework.

Preserve security protections in touched code. Report material security issues outside the requested fix separately; do not turn a routine cleanup into an unrequested audit.

## Shared rules

These rule IDs support precise findings. They are not a requirement to produce a finding for every rule.

| ID | Reject | Prefer |
| --- | --- | --- |
| CORE-01 | A factory, registry, base class, wrapper, or configuration layer for a hypothetical future need | A direct implementation; add an abstraction when it hides meaningful complexity, enforces an invariant, or supports an actual caller |
| CORE-02 | Vague names such as `data`, `result`, or `manager` when scope cannot explain them; ambiguous units | Domain names and units at interfaces; ordinary short names in a clear local scope |
| CORE-03 | Splitting a coherent operation into forwarding helpers to meet line or argument quotas | Cohesive functions and explicit inputs; extraction when a name or boundary materially reduces reading effort |
| CORE-04 | Catch-all recovery that presents failure as an empty result, zero, success, or fabricated data | Handle expected failures at the boundary that can recover; preserve unexpected failures and diagnostic context |
| CORE-05 | Repeated defensive checks throughout trusted internal code; hidden coercion or defaulting | Validate external inputs once at a suitable boundary; preserve meaningful distinctions between absent, empty, zero, and invalid |
| CORE-06 | Narration of syntax, docstrings that merely repeat names and types, decorative banners, generated praise, stale examples, and commented-out implementations | Documentation of behavior, units, constraints, side effects, and non-obvious reasoning |
| CORE-07 | Dependencies, flags, files, and abstractions added merely for completeness | Existing project tools and the smallest change that fulfills the task |
| CORE-08 | Tests that assert helper call order, reproduce the algorithm, or pass without checking behavior | Observable results, regression examples, and relevant boundary or failure cases |
| CORE-09 | Invented APIs, package versions, benchmark numbers, test results, or claims of production readiness | Verify against the installed version or authoritative documentation and report the actual evidence |
| CORE-10 | Hidden state, import/source-time work, absolute personal paths, and unexplained data loss | Explicit I/O and state ownership, caller-supplied paths, and visible policies for filtering and missing data |
| CORE-11 | Deleting code solely because a text search or analyzer finds no callers | Establish real entry points, inspect indirect uses and public contracts, then verify a small removal |
| CORE-12 | Changing expectations to match unexplained output, removing assertions, adding skips/xfails, or loosening tolerances merely to obtain a green run | Fix the implementation against the established contract; change tests only when a requirement or demonstrated test defect justifies it, and explain why |
| CORE-13 | Simplifying away authorization, validation at trust boundaries, TLS verification, or security regression tests | Preserve the protection and its legitimate use cases; security behavior changes require an explicit contract and relevant allow/deny checks |

Class definitions, loops, booleans, `None`, `NULL`, comments, and dependencies are legitimate tools. Do not ban them by appearance. A rule violation requires a concrete cost or defect in the current context. Never impose arbitrary line counts, abstraction counts, coverage percentages, or clean-code scores.

## Data and analysis contracts

When data is transformed, establish the relevant schema, units, key uniqueness, ordering, shape, missing-value behavior, and mutation behavior. Do not silently drop rows, replace unknown values with zero, deduplicate, change time zones, or join on guessed keys. Check for row multiplication or loss when a join's cardinality matters.

For statistical or machine-learning work, preserve the estimand, split strategy, grouping, and preprocessing scope. Fit learned preprocessing only on training data. Do not change a model, impute data, remove outliers, or seed every helper as a cosmetic cleanup. Record stochastic configuration at the workflow boundary when reproducibility is required; a seed alone does not establish reproducibility.

For notebooks and reports, inspect cell/chunk order and dependencies. Move reusable logic into modules only when reuse or maintenance justifies it. Do not execute costly jobs, remote writes, or destructive cells just to claim a clean run. A fresh-kernel/session run is useful evidence when it is feasible within the task's authorization.

## Review findings

Report defects first, then maintenance costs. Each finding needs a file and line (or notebook cell), concrete consequence, and smallest useful correction. Cite a rule ID when one fits; do not invent an ID or force a valid finding into the rule table. Distinguish an observed failure from a risk inferred from code.

- **High:** wrong results, data loss, hidden failures, or incompatible public behavior.
- **Medium:** demonstrated maintenance cost or a fragile data contract in the requested scope.
- **Low:** localized clarity or comment problems with a specific reading cost.

Do not fill a quota or invent severity for personal taste. If no actionable issue is found, say so and state what was inspected. Group repeated instances with the same cause.

Example: `High | R-01 | R/summarise.R:18 | na.rm = TRUE drops unknown measurements, changing the reported denominator. Preserve the documented missing-value policy.`

## Finish with evidence

Before delivering changes, inspect the diff for unnecessary helpers, duplicate validation, unused imports, dead code, unrelated formatting, and weakened tests (changed expectations, skips/xfails, deleted assertions, or relaxed tolerances). Apply the relevant language checks to changed behavior. Use configured, available tools; do not install or migrate a toolchain solely for cleanup or review.

Report the changed behavior and relevant verification briefly. Use **PASS** for a check actually performed successfully, **FAIL** for a performed check that failed, and **NOT RUN** with the reason when a check could not be performed. Use **N/A** when a check does not apply. Never call parsing, linting, or a successful import proof of runtime correctness. When blocked by a missing runtime or dependency, return the useful work with that limit stated.

