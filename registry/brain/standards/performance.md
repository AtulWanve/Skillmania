---
title: Performance Standards
tags: [standards, performance, optimization]
aliases: [Performance, Optimization]
---

# Performance Standards

## Bundle Size

- Keep initial JS bundle under 150 KB (gzipped)
- Use dynamic imports for route-level code splitting
- Tree-shake unused exports
- Avoid large libraries for trivial utilities

## Rendering

- Use server components by default in [[standards/nextjs|Next.js]]
- Stream responses with `loading.tsx` and Suspense boundaries
- Memoize expensive computations
- Avoid unnecessary re-renders

## Network

- Minimize API calls; batch when possible
- Use HTTP caching headers
- Compress responses (Brotli / Gzip)
- Implement pagination for large datasets

## Database

- Index query columns
- Use database-side pagination (LIMIT/OFFSET or cursor-based)
- N+1 query detection and prevention
- Connection pooling for production

> [!seealso] Also see [[standards/react|React Standards]] for memoization details and [[reviews/performance-review|Performance Review]] for the review checklist.
