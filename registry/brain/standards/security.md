---
title: Security Standards
tags: [standards, security, authentication, validation]
aliases: [Security]
---

# Security Standards

## Input Validation

- Validate all user input server-side
- Use schema validation (Zod, Yup) for API payloads
- Sanitize output by context:
  - **Normal JSX/HTML**: React/Next.js auto-escapes values in JSX expressions; no additional sanitization needed for text content.
  - **URL values**: Validate against sink-specific protocol allowlists:
      - For `href` (links): allow `https:`, `mailto:`, `tel:`, and same-origin relative URLs.
      - For `src` (resources such as images, scripts, iframes): allow `https:` and same-origin relative URLs only. `mailto:` and `tel:` must be rejected for `src`.
      - Same-origin relative URLs (e.g., `/path/to/file`, `./relative/path`) are parsed relative to the current origin and validated to ensure they do not contain protocol injection (e.g., `javascript:`, `data:`) after normalization. Reject any relative URL that contains `:` before the first `/` unless it is a known-safe path segment.
      - For absolute URLs, validate against the sink-specific protocol allowlist above and ensure the URL is well-formed. Reject opaque or non-hierarchical URLs that bypass origin checks.
  - **Style values**: Restrict to a safe subset; avoid user-supplied `style` objects when possible.
  - **Raw HTML** (`dangerouslySetInnerHTML`): Sanitize untrusted content with DOMPurify or similar library before rendering.
- Never concatenate user input into SQL queries

## Authentication

- Use HttpOnly, Secure, and SameSite=Lax (or Strict) cookies for session tokens by default
  - Permit SameSite=None only for legitimate cross-site or embedded flows (e.g., iframed dashboards, cross-origin credentialled API consumers)
  - When using SameSite=None, also require: Secure flag, anti-CSRF tokens, and Origin/Referer header validation on state-changing requests
- Implement CSRF protection for state-changing requests:
  - Use anti-CSRF tokens (e.g., double-submit cookie pattern or server-issued token validated on each mutation)
  - For API routes, require a custom header (e.g., `X-CSRF-Token`) or validate the Origin/Referer header
  - Do not rely solely on SameSite cookies for CSRF protection on sensitive mutations
- Rate-limit authentication endpoints
- Hash passwords with bcrypt or Argon2

## Data Protection

- Never log secrets, tokens, or PII
- Use environment variables for secrets
- Encrypt sensitive data at rest
- Apply least-privilege principle to API keys and tokens

## Dependencies

- Regularly audit dependencies for CVEs
- Pin major versions; use lockfiles
- Avoid eval, exec, or dynamic code generation with user input

> [!seealso] See [[reviews/security-review|Security Review]] for the review checklist and [[standards/nextjs|Next.js Standards]] for Server Action CSRF context.
