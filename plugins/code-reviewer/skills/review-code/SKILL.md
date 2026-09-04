---
name: review-code
description: Review source code changes, pull requests, and diffs for correctness, security, performance, test coverage, and maintainability. Use when the user asks for a code review, PR review, audit, or review of proposed changes; do not activate for implementation-only requests that do not ask for review.
---

# Review Code

Review the requested change as a careful maintainer. Prioritize defects that could cause incorrect behavior, security exposure, data loss, outages, or meaningful performance regressions. Do not invent findings to fill a checklist.

## Establish the review scope

- Identify the diff, pull request, commit range, or files the user wants reviewed.
- Read repository guidance and the surrounding code needed to understand the change.
- Determine the intended behavior from the request, tests, documentation, and existing interfaces.
- If the exact diff is unavailable, state what was reviewed and avoid implying complete PR coverage.

## Analyze the change

Check the dimensions relevant to the code rather than mechanically reporting on each one:

- Correctness: invalid assumptions, boundary cases, state transitions, concurrency, error paths, and compatibility.
- Security: trust boundaries, authorization, injection, secret exposure, unsafe parsing, and dependency risk.
- Performance: changed complexity, repeated I/O, unbounded work, allocation pressure, and hot-path regressions.
- Reliability: failure recovery, resource cleanup, retries, timeouts, idempotency, and observability.
- Tests: missing coverage for behavior introduced or changed by the patch.
- Maintainability: only issues that materially increase defect risk or make the change difficult to operate.

Trace suspicious behavior to a concrete execution path. Distinguish verified defects from questions or uncertain risks. Ignore pre-existing problems unless the change makes them newly reachable or materially worse.

## Report findings

Lead with actionable findings, ordered by severity. For each finding include:

1. A severity label and concise title.
2. The smallest useful file and line range.
3. The conditions that trigger the problem.
4. The concrete impact.
5. A practical fix when it is not obvious.

Keep each finding self-contained. Do not treat formatting preferences, subjective style, or hypothetical concerns as defects.

If no actionable findings remain, say so directly and mention any important validation gap, such as tests that could not be run. Do not modify code unless the user also asks for fixes.
