# CI Workflow Specification

Use this specification when executing `/milestone scaffold` to deploy `.github/workflows/ci.yml`.

## Standard Workflow Template

```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  validate:
    name: Lint, Test & Verification
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Setup Runtime Environment
        # Configure toolchain: python, node, go, etc.
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install Dependencies
        run: |
          npm ci || echo "Configure dependency install command"

      - name: Run Automated Tests
        run: |
          npm test || echo "Configure test command"
```

## Flow Recommendation Matrix by Project Type

When scaffolding a project with no existing workflows, inspect root files and suggest the standard quality gates for that ecosystem:

| Project Type | Detection Indicators | Recommended Linter / Formatter | Recommended Typecheck | Recommended Test Runner | Build / Compile Check |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TypeScript / Node** | `package.json`, `tsconfig.json` | `eslint` / `biome` | `tsc --noEmit` | `vitest` or `jest` (`npm test`) | `npm run build` |
| **JavaScript / Node** | `package.json` (no tsconfig) | `eslint` / `biome` | N/A | `vitest` / `node --test` | N/A |
| **Python** | `pyproject.toml`, `requirements.txt` | `ruff check .` | `mypy` or `pyright` | `pytest` | `python -m build` |
| **Go** | `go.mod` | `golangci-lint` | Compiler check | `go test -v ./...` | `go build ./...` |
| **Rust** | `Cargo.toml` | `cargo clippy`, `cargo fmt` | Compiler check | `cargo test` | `cargo build --release` |
| **Docs / Markdown** | Markdown / static files only | `markdownlint` | N/A | Link validation | Static build / N/A |

### Layered Workflow Pipeline
Rather than a single monolithic step, the suggested CI workflow organizes checks into discrete, readable layers:
1. **Lint & Style**: Fast static analysis for syntax, formatting, and anti-patterns.
2. **Typecheck / Analysis**: Verifies type safety and catch compile-time defects before tests run.
3. **Automated Tests**: Unit, smoke, and regression tests.
4. **Build Verification**: Ensures production bundles or binaries compile cleanly.

## Cold-Start Handling (Zero Existing Workflows or Tests)

If a project has no `.github/workflows/` directory or no CI setup:
1. **Toolchain Inspection**: Identify project type from the matrix above.
2. **Directory Creation**: Create `.github/workflows/` if absent.
3. **Missing Test Framework**: If no test framework is installed yet, emit fallback non-blocking test steps (`echo "No automated tests configured yet; add test runner here"`) so the workflow runs cleanly without false failures.
4. **No Remote CLI Dependencies**: All actions execute inside the standard GitHub Actions runner without requiring external tokens, `gh` CLI credentials, or manual authorization.

## Scaffolding Behavior & Runtime Detection

When `/milestone scaffold` is invoked, inspect root configuration files to identify the toolchain and populate build/test steps:
- **Node.js**: Detected via `package.json`. Uses `actions/setup-node@v4` with `npm ci` and `npm test`.
- **Python**: Detected via `pyproject.toml`, `requirements.txt`, or `setup.py`. Uses `actions/setup-python@v5` with `pytest`.
- **Go**: Detected via `go.mod`. Uses `actions/setup-go@v5` with `go test ./...`.
- **Rust**: Detected via `Cargo.toml`. Uses `dtolnay/rust-toolchain@stable` with `cargo test`.
- **Generic / Fallback**: Emits placeholder shell execution steps prompting the developer for explicit test commands.

## Pluggable Automation Extensions (Cloud vs. Self-Hosted)

Projects often need supplementary automations beyond baseline CI (such as automated PR reviews, security/secret auditing, license checks, or performance benchmarking). These tools exist in both paid/SaaS models and open-source/self-hosted alternatives. The scaffolding supports two interchangeable execution models:

### 1. Cloud-Hosted Extension Flow (Standard GitHub Runners)
- **Target**: Public or cloud-native repos using `runs-on: ubuntu-latest`.
- **Integrations**: Cloud SaaS actions (Marketplace actions, API-based reviewers, Codecov, Snyk) authorized via repository secrets.
- **Benefits**: Zero infrastructure management, immediate availability.

### 2. Self-Hosted Extension Flow (`.github/workflows/extensions.yml`)
- **Target**: Private repos or dedicated internal hardware using `runs-on: [self-hosted]`.
- **Integrations**:
  - **Local Subprocess Harnesses**: Invoking installed CLI tools (e.g., executing Claude Code CLI headlessly via subprocess, `gh` scripts, custom audit scripts).
  - **Open-Source Review Tools**: Running open-source alternatives (e.g., `pr-agent`, local linters) without SaaS subscription costs.
  - **Internal Security & Secret Scanners**: Scanning codebases against proprietary internal policies, TruffleHog, or air-gapped security tools.
- **Safety Boundary**: Must include `if: github.event.pull_request.head.repo.full_name == github.repository` to prevent unauthorized execution from forks.

### Extension Workflow Template

```yaml
name: Automation Extensions

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  # Option A: Fast cloud security check
  security-audit:
    name: Secret & Dependency Audit
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4
      - name: Run Audit
        run: |
          echo "Run cloud security check (e.g., npm audit, pip-audit, or TruffleHog)"

  # Option B: Internal / Self-hosted automation (CLI harnesses, review bots)
  internal-tooling:
    name: Local Harness / Review Agent
    runs-on: [self-hosted]
    if: github.event.pull_request.head.repo.full_name == github.repository
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4
      - name: Run Local Review or Subprocess Tool
        run: |
          # Example: invoke local CLI harness or open-source review agent
          echo "Run local subprocess harness or internal tool"
```
