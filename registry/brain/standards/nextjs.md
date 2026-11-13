---
title: Next.js Standards
tags: [standards, nextjs, app-router, server-actions]
aliases: [Next.js, App Router]
---

# Next.js Standards

## Routing

- Use the App Router for new routes
- Place page components in `app/<route>/page.tsx`
- Use layout files for shared UI (`app/<route>/layout.tsx`)
- Add loading.tsx, error.tsx, and not-found.tsx conditionally for route segments that require the corresponding UI states; these files are optional per segment

## Data Fetching

- Prefer server components for data fetching
- Use `fetch` with cache options: `force-cache`, `no-store`
- Use `next.revalidate` separately for time-based revalidation (e.g., `{ next: { revalidate: 3600 } }`)
- **Note:** `force-cache` is the default for `fetch` in Next.js App Router for most route types (static routes), but dynamic routes, route handlers with dynamic methods, or usage of `cookies()`/`headers()` may default to `no-store`. Always check the effective cache behavior for the specific route context.
- Use `server actions` for mutations
- Avoid `getServerSideProps` and `getStaticProps` (Pages Router)

## Server Actions

- Limit Server Actions to mutations that originate from the application UI (form submissions, button clicks, etc.)
- Define with `"use server"` directive
- **Authenticate** the caller before performing any side effects (verify session/token)
- **Authorize** the action at the resource level (verify the caller has permission for the specific operation)
- **Apply CSRF protections** suitable for the action type (see [[standards/security|Security Standards]] for guidance)
- Validate inputs with Zod or similar schema library
- Handle errors gracefully with `try/catch`
- Revalidate affected paths with `revalidatePath` or `revalidateTag`
- For public API mutations, webhooks, or third-party integrations, use Route Handlers (`app/api/` route.ts) or the appropriate external HTTP contract instead
