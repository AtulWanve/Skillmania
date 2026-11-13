---
title: TypeScript Standards
tags: [standards, typescript, typing, types]
aliases: [TypeScript]
---

# TypeScript Standards

## Type Safety

- Prefer `unknown` over `any`
- Use strict mode (`strict: true` in tsconfig)
- Avoid type assertions (`as`): use type guards or declare proper types
- Use `interface` for public APIs, `type` for unions and utility types
- Never use `@ts-ignore` or `@ts-expect-error` without a documented reason

## Naming

- Types and interfaces: PascalCase
- Functions and variables: camelCase
- Constants: UPPER_SNAKE_CASE for global constants
- Files: kebab-case for utility files, PascalCase for components

## Imports

- Use ES module syntax
- Prefer named exports over default exports
  - **Exception:** [[standards/nextjs|Next.js]] App Router entry points (`page.tsx`, `layout.tsx`, `loading.tsx`, `error.tsx`, `not-found.tsx`, `template.tsx`) **must** use default exports as required by the framework
- Group imports: externals → internals → relative
- Avoid barrel files (index.ts re-exports) for deep module trees

> [!seealso] Also see [[standards/naming|Naming Standards]] for file and directory naming conventions.
