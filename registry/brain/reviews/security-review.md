---
title: Security Review
tags: [review, security, vulnerabilities, audit]
aliases: [Security Review]
---

# Security Review

## Scope

Evaluates the implementation for security vulnerabilities. See [[standards/security|Security Standards]] for the guidelines this review checks against.

## Checklist

- [ ] No SQL injection vectors
- [ ] No XSS vulnerabilities (output is properly escaped)
- [ ] Authentication checks are in place
- [ ] Authorization checks enforce least privilege
- [ ] No secrets or tokens exposed in client code
- [ ] Input validation is performed server-side
- [ ] CSRF protection for state-changing operations
- [ ] Rate limiting applied on sensitive endpoints
- [ ] File uploads are validated and sanitized
- [ ] Dependency has no known CVEs

## Scoring

Score: 0-100

Threshold: score < 80 requires changes (security is higher bar)

### Severity-to-Blocking Rules

- **Critical** findings (authentication bypass, exposed secrets, injection vulnerabilities, arbitrary code execution): `Blocking: true` **independently** of the aggregate score. A single critical finding forces rejection.
- **High** severity: `Blocking: true` if the aggregate score is < 80 or if the finding's `resolution` is `"unresolved"`.
- **Medium** / **Low**: Blocking is determined by the aggregate score threshold (< 80).
- This ensures critical security issues cannot be masked by high scores in other categories.

## Vulnerability Schema

Each vulnerability is an object with the following fields, aligned to the canonical finding schema:

| Field | Type | Description |
|-------|------|-------------|
| `description` | `string` | Description of the vulnerability |
| `category` | `string` | Dimension category (e.g., `"security"`, `"architecture"`, etc.) - maps the vulnerability to a review dimension |
| `severity` | `"critical" \| "high" \| "medium" \| "low"` | Severity level |
| `recommendation` | `string` | Suggested remediation or mitigation |
| `resolution` | `"unresolved" \| "resolved" \| "accepted"` | Current resolution status; `"unresolved"` means the finding has not been addressed |

**Note:** If vulnerabilities are generated from a source that lacks `category` or `recommendation`, an adapter **must** map each vulnerability to the canonical schema before serialization into the review output, providing reasonable defaults (e.g., `category: "security"` and `recommendation: "Review and remediate"`) if the source does not supply them.

### Resolution Values

| Value | Meaning |
|-------|---------|
| `"unresolved"` | Finding has not been addressed (triggers High-severity blocking rule) |
| `"resolved"` | Finding has been fixed or remediated |
| `"accepted"` | Finding is acknowledged but accepted as a risk (e.g., low-impact, documented trade-off) |

## Output

- Score (`number`, 0-100)
- Vulnerabilities found (list of `Vulnerability` objects as defined above)
- Severity level for each
- Recommendations
- `Blocking: boolean` (derived from severity-to-blocking rules above)

> [!warning] Security has a higher bar than other reviews (threshold < 80 vs. < 60). Critical findings override the aggregate score entirely. Results feed into the [[runtime/review-engine|Review Engine]]'s "security" dimension.
