# Dead-code review and removal

Use this workflow when unused code is part of the requested review or cleanup. A candidate is not confirmed dead merely because its name has no direct callers.

## Establish reachability

Identify roots in the requested scope: applications, scripts, commands, exported library interfaces, tests, framework registrations, scheduled jobs, and notebook/report execution. Include configuration and packaging declarations. Inspect direct callers and indirect registration before classifying a candidate.

Search references with `rg` and use existing static analysis if configured. Check its language support, entry-point configuration, and dynamic-dispatch limits.

Static analysis produces candidates. Dynamic dispatch, external consumers, generated code, and configuration may be outside its view. Report the limits of the inspected scope; passing tests or missing coverage alone cannot establish that code is unused.

Classify findings as:

- **Confirmed unused within scope:** no reachable use after checking applicable roots and contracts. Explain the evidence and scope.
- **Possibly unused:** unresolved dynamic use or consumers outside the repository. Preserve it or report the uncertainty.
- **Intentionally retained:** a documented public interface, registration hook, compatibility path, or other supported use. Do not add suppression comments without a real reason.

A module can be unreachable from application roots while its functions still call each other. Conversely, a function with no direct calls may be a required callback. Check both cases.

## Python checks

Inspect package exports and re-exports, command entry points in packaging metadata, decorators, plugin registration, framework handlers, fixtures, and serialization references. Search string-based imports, `getattr`, registries, and configuration where applicable. Public library symbols may have consumers outside this checkout.

An import may register plugins or perform another required side effect even when its binding is unused. Understand that effect before deleting the import. Remove obsolete side effects only when that behavior change is authorized.

## R checks

Inspect NAMESPACE exports and method registration, S3/S4 dispatch, callbacks, formulas, and code loaded through `source()`. Search relevant `get`, `do.call`, and other string-based lookups, as well as configuration and scripts. A method used by dispatch need not have a direct call under its full name.

Check R Markdown, Quarto, notebooks, package examples, and downstream scripts when they are in scope. A package export is a supported interface, not evidence of dead code. For a function passed as a value, follow where the callback is invoked rather than searching only for `name(`.

## Remove and verify

For a review-only request, report findings without editing. For an authorized cleanup, remove confirmed unused code in small coherent groups and inspect affected callers. Do not mix a deletion with an unrelated redesign.

Check associated imports, dependencies, exports, configuration, docs, and tests. Remove a dependency only when its remaining uses and relevant optional paths have been inspected. Update generated package metadata through the project's established tooling when needed; do not leave exports pointing at removed symbols or edit generated files blindly.

Run relevant tests and entry-point smoke checks after removal; include package loading and method behavior when those contracts are affected. Re-run the relevant analysis to inspect newly orphaned code, stopping at the requested scope. Report what was removed, why it was considered unused, checks actually performed, and unresolved candidates retained.

