---
name: slopstop-security
description: Review or improve security in Python, R, SQL Server, MongoDB, and AWS code and configuration. Use for security reviews, permission changes, credential handling, untrusted input, dynamic queries, IAM, and data access boundaries. Keep routine style cleanup and production operations outside the audit scope.
---

# SlopStop Security

Find exploitable failures and preserve useful protections. Read [the stack checks](references/stack.md) for the relevant technologies; apply only sections supported by the code and environment being inspected.

## Set the boundary

For a review, inspect and report without editing unless fixes were requested. For an authorized fix, make the smallest change that enforces the required contract and preserves legitimate use. Follow repository instructions and inspect the installed framework, driver, runtime, deployment model, and existing tests. Do not initiate scans, queries, deployments, IAM changes, or secret rotation against live systems merely because code mentions those systems.

Treat cleanup of validation or authorization as behavior-sensitive. Similar-looking checks can protect different trust boundaries. Do not bypass a protection to make tests or examples pass, and do not weaken tests to hide a defect.

## Trace the change and the authority

For each suspicious path, identify:

- The caller's actual identity and capabilities, including anonymous, cross-user, and cross-tenant cases.
- The untrusted input and the sensitive operation it can reach.
- Where ownership, role, query structure, file destination, or credential choice is established.
- The check that prevents misuse, and whether another path, update, upsert, or later mutation bypasses it.

For diffs, inspect removed controls and affected callers as well as new code. Use relevant history to understand the contract when necessary. Prefer APIs that make the authorized use straightforward; do not invent a new security framework when an existing safe interface suffices.

A pattern match alone is not a finding. For example, a wildcard IAM resource can be required by an action, and a local data conversion does not automatically need a query timeout. Establish preconditions, actual exposure, and the protection's enforcement point. Mark infrastructure controls that are outside the inspected scope as unknown.

## Findings and fixes

Each actionable finding needs a file and line, affected operation, concrete consequence, exploit preconditions, and a minimal correction. Distinguish confirmed defects from unresolved risks. Prioritize unauthorized access, code execution, exposed credentials, and data integrity consequences over stylistic preferences. Do not invent scores, fix quotas, or a secure verdict from a checklist.

Rank severity by exploitability and impact, not by finding type:

- **Critical:** any caller who can reach the code can exploit it without special preconditions, causing unauthorized data access, code execution, or account-wide compromise.
- **High:** serious impact that needs a precondition, such as a leaked credential, an insider, or a specific deployment setting; or a live-looking credential exposed in source.
- **Medium:** limited impact or a defense-in-depth gap, such as an unbounded query or an overly broad permission that is not reachable without another flaw.
- **Low:** hardening with little direct exposure.

Use distinct levels when the findings differ; do not rate everything the same to avoid a judgment.

Never reproduce real credentials or sensitive records in a report. Redact values and cite their location. Recommend the project's rotation process for exposed credentials; do not rotate them without authorization.

When fixing access control, verify both an allowed legitimate operation and a denied unauthorized operation. Include cross-owner access and create-then-update behavior where relevant. Use repository-owned fixtures or an authorized local test service; do not substitute a live account for missing test infrastructure.

## Evidence

Use existing configured tools. Record relevant commands and outcomes, but keep secrets out of logs. A static finding, successful import, or passing parser is not proof of exploitability or of safety. Inspect the actual diff and test assertions rather than trusting an agent's completion report.

Report **PASS** only for checks performed successfully, **FAIL** for checks performed and failed, **NOT RUN** with the reason for checks not performed, and **N/A** for checks that do not apply. State any uninspected deployment or data-access paths and any behavior change introduced by a fix.
