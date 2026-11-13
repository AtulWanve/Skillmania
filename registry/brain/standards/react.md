---
title: React Standards
tags: [standards, react, components, hooks]
aliases: [React, React Conventions]
---

# React Standards

## Component Structure

- One component per file
- Use function components with hooks
- Keep components under 200 lines
- Extract reusable logic into custom hooks

## State Management

- Local state: `useState`
- Derived state: compute ordinary values directly during render; use `useMemo` only for expensive calculations or when referential stability is required
- Side effects: `useEffect` with explicit dependencies
- Global state: React Context or dedicated state library
- Avoid prop drilling beyond 3 levels

## Performance

- Memoize expensive computations with `useMemo`
- Memoize callbacks with `useCallback` when passed to memoized children
- Use `React.memo` for pure components that re-render frequently
- Lazy load routes and heavy components

> [!seealso] Also see [[standards/performance|Performance Standards]] and [[reviews/code-quality|Code Quality Review]].
