# Security at trust boundaries

Use for requested security reviews or changes to security-relevant code. Identify the actual runtime, framework, deployment context, untrusted inputs, sensitive operations, and enforcement point. These checks apply to both Python and R unless a section names a specific stack. They are not a claim of a complete security audit.

## Preserve protections during cleanup

Boundary validation, permission checks, output restrictions, and size limits can look repetitive while protecting different inputs or operations. Trace their purpose before consolidating them. Do not solve errors by disabling certificate verification, bypassing signature checks, trusting client-supplied roles or owner fields, or broadening permissions. Authentication establishes identity; authorization decides access to each object and operation. Random identifiers do not replace authorization.

Do not log, commit, or reproduce credentials, tokens, signing keys, or sensitive records in examples, fixtures, reports, or notebook outputs. Cite a redacted location and explain the exposure. A secret already committed needs rotation, not only deletion from the latest version. Review environment and deployment configuration without assuming a missing application-level control is also absent from a proxy or hosting platform.

## Untrusted input to sensitive operations

Trace actual input flow rather than flagging every occurrence of an API:

- **Commands:** avoid constructing shell commands from untrusted strings. In Python, prefer a fixed executable and argument list with `shell=False`; still restrict executable choice and dangerous options, since argument injection does not require a shell. In R, `system2()` does not make arbitrary argument strings safe automatically: check quoting with `shQuote()` and the target command's semantics.
- **Files and URLs:** enforce the intended directory or destination policy at the point of use. Account for traversal, symlinks, redirects, and internal network destinations when relevant. A string prefix test or filename extension alone is not a containment or trust check.
- **Code and serialized objects:** do not pass untrusted text to `eval`, `exec`, or R's `eval(parse(...))`/`source()`. Python pickle-backed loaders (including `pandas.read_pickle` and `joblib.load`) and `yaml.load` without a safe loader can execute code; use a data-only format and validate its schema when the input is untrusted.
- **Resource bounds:** where inputs are untrusted, inspect file sizes, decompression, row/array expansion, unbounded queries, outbound requests, retries, and job concurrency. Recommend limits from the service's actual contract, not arbitrary constants added to every helper.

For web code, inspect the installed framework's authentication, sessions, CSRF, escaping, and response-shaping mechanisms as relevant. CORS is not authorization. Distinguish local development settings from deployed settings.

## SQL Server and other SQL databases

- Bind values with the driver's parameters: `?` placeholders in pyodbc, bound parameters with SQLAlchemy `text()`, and `DBI::dbGetQuery(con, sql, params = ...)` or `glue::glue_sql()` in R. f-strings, `.format()`, `%` formatting, `paste0()`, and hand-written quote escaping are not substitutes.
- In T-SQL, dynamic SQL built by concatenation and run with `EXEC(@sql)` is injectable even inside a stored procedure. Use `sp_executesql` with typed parameters for values. Identifiers (sort columns, table names) cannot be parameters: map them through an allowlist and wrap with `QUOTENAME()`.
- Keep connection strings containing `PWD=` or `Password=` out of code, notebooks, and committed config; prefer integrated authentication, managed identity, or a secret store already used by the project.
- `WITH (NOLOCK)` is a correctness decision (dirty and duplicated reads), not a cleanup optimization; do not add or remove it silently.

## MongoDB

- Request JSON can contain query operators. Merging a request body or dict into a filter (`criteria.update(body)`, `{**body}`) lets a caller supply `{"owner_id": {"$ne": null}}` or overwrite a server-set field. Build filters from named, type-checked fields and apply server-derived constraints such as owner or tenant last, so they cannot be overridden.
- Do not pass user input to `$where`, `$function`, `$accumulator`, or `mapReduce` JavaScript. In R, do not `paste0()` user input into `mongolite` JSON query strings; serialize a constructed structure instead.
- Bound reads from untrusted requests with a limit, projection, and `maxTimeMS` where the endpoint contract allows.
- Field-level restrictions do not establish ownership: check which documents a caller may affect, including on updates and upserts.

## AWS

- Do not embed access keys in code, config, notebooks, or fixtures. Use the default credential chain (role, SSO profile, or environment supplied by the platform). Treat a key that looks committed as exposed and recommend rotation.
- Check IAM policies for `"Action": "*"`, service wildcards such as `"s3:*"`, and `"Resource": "*"` where the code needs a narrower set. Match permissions to the operations the code actually performs; do not broaden a policy to fix an access error.
- Check S3 for public ACLs or bucket policies, disabled Block Public Access, and presigned URLs with long expiry or caller-chosen keys.
- Do not log full request payloads, credentials, or sensitive records to CloudWatch or stdout in Lambda and batch jobs.

## Evidence and validation

For each finding, identify the untrusted source, sensitive operation, missing or bypassed check, preconditions, and concrete impact with file/line evidence. State what configuration or execution remains unknown. Absence of evidence in the inspected scope is not proof of a vulnerability or of safety.

Use local fixtures and existing offline tests where available. For an access change, verify an allowed legitimate operation and denied unauthorized operations, including cross-user access and updates. Do not probe live systems, print real secrets, change IAM, apply database permissions, or publish security reports externally as part of an ordinary review. A security review alone authorizes findings, not those side effects.

Report performed checks with the statuses defined in SKILL.md. Do not give a numeric security score or label a project secure because a checklist, parser, or static scan passed.
