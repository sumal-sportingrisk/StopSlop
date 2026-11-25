---
name: slopstop-docs
description: Write or review accurate developer documentation for repositories, APIs, data pipelines, and services. Use for README files, onboarding, tutorials, how-to guides, reference pages, runbooks, architecture explanations, and substantial docstring cleanup. Focus on documented behavior, checked examples, and a clear reader task rather than marketing copy.
---

# SlopStop Documentation

A document succeeds when its intended reader can complete its task without the conversation that produced it. Preserve established project formats and edit only the requested scope. A review is read-only unless edits were requested.

## Establish purpose from available context

Identify the reader, their goal, and the relevant code or configuration. Infer these from the request and repository when possible; ask only when a material gap prevents useful work. A small correction does not require a new outline or interview.

Choose the document's primary job:

| Type | Reader needs | Keep central |
| --- | --- | --- |
| Tutorial | A guided learning experience | A bounded, working path with prerequisites and checkpoints |
| How-to | Completion of a specific real task | Steps, choices, expected outcomes, and recovery |
| Reference | An exact answer during use | Signatures, inputs, defaults, units, outputs, conditions, and limits |
| Explanation | Understanding a design or behavior | Concepts, tradeoffs, evidence, and rationale |

A README is an entry point: orient readers and link to deeper tasks and references. Do not force every document type or template section onto every repository. Use [the README template](assets/README_TEMPLATE.md) when creating a repository README, adapting or dropping sections according to the project.

## Write what the implementation supports

Check commands, paths, imports, signatures, defaults, environment variables, output schemas, and supported versions against current code and configuration. Separate present behavior from plans. Attribute verification to a commit or artifact where useful; never describe an unrun check as current proof.

For architectural explanations, trace a representative request or job from entry point through transformations, storage, outputs, and failures. Cite relevant files and symbols for claims that depend on implementation. Do not infer design intent from the mere existence of code: label inferred rationale and unknown ownership or operational behavior honestly.

Explain credential sources and required permissions, never credential values. Distinguish local examples, test environments, and deployed behavior. Do not document destructive actions, production writes, or cloud provisioning as a routine smoke test.

## Reject filler with no reader value

Remove unsupported claims such as "production-ready", "robust", "seamless", or "scalable" when they replace concrete behavior or evidence. Do not ban a word when it names a meaningful, supported property. Replace generic introductions, repeated conclusions, and decorative headings with information needed for the task.

Docstrings should add contracts the signature cannot express: units, shape, missingness, ownership and mutation, side effects, failure conditions, or examples. Avoid descriptions such as "x (int): The x". Do not invent an exception, return guarantee, or performance claim to fill a template.

## Check examples and reader usability

Make runnable examples complete within their stated prerequisites. Include expected results when they help identify success. Mark placeholders and do not present illustrative fragments as commands that run unchanged.

Run relevant, safe examples in the supported local environment when available. Check results, not just exit status. Use an isolated directory for generated files. Never access live databases, mutate cloud resources, or expose credentials merely to satisfy a documentation check. If execution is unavailable, state the missing prerequisite and the exact limit of source inspection.

For substantial onboarding or runbooks, walk through the page using only its stated prerequisites, in a fresh environment if feasible. An independent reader test can help when authorized: give the reader the document and raw project context, not the author's intended answers or private grading key. Treat misunderstood steps as evidence to improve the page.

## Deliver with evidence

Inspect the diff for inaccurate claims, stale paths, missing prerequisite steps, unnecessary duplication, and unrequested code changes. Check local links. Use configured documentation tooling; do not add a framework just to fix a page.

Report what changed and what was actually checked. Use **PASS**, **FAIL**, **NOT RUN** with a reason, and **N/A** according to the check performed. Distinguish an executed example, a link check, and source inspection. A polished page is not evidence that the software itself was tested or deployed.
