---
title: Naming Standards
tags: [standards, naming, conventions]
aliases: [Naming Conventions]
---

# Naming Standards

## Files and Directories

- kebab-case for utility files, config files, and directories
- PascalCase for component files and class files
- camelCase for data files and hook files
- Test files: `<name>.test.ts`, `<name>.spec.ts`, `<name>.test.tsx`, or `<name>.spec.tsx`

## Code

- Functions/methods: verbs or verb phrases (`getUser`, `validateInput`)
- Booleans: prefixes `is`, `has`, `should`, `can` (`isLoading`, `hasPermission`)
- Variables: nouns or noun phrases (`userList`, `config`)
- Constants: UPPER_SNAKE_CASE for module-level immutable values
- Types/interfaces: nouns in PascalCase

## CSS / Styling

- Use Tailwind utility classes when available
- Component-scoped styles for custom CSS
- Avoid global class name collisions

> [!seealso] Also see [[standards/typescript|TypeScript Standards]] for type naming and [[standards/react|React Standards]] for component structure.
