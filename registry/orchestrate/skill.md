---
name: orchestrate
description: Universal multi-agent orchestration for feature planning, deep investigations, surprise bug diagnoses, or audits. Decomposes tasks across isolated subagents to prevent context bloat.
argument-hint: "<task, feature plan, investigation question, or bug hypothesis>"
---

# Universal Multi-Agent Orchestration

Orchestrate complex tasks, deep multi-file investigations, feature planning, or surprise bug hunting without bloating the main conversation context.

## Core Rule: Main Context Remains Pristine
**NEVER read whole files, perform broad sweeps, or dump raw file content into the main conversation.**  
The lead agent is the strategic conductor ("Big Claude"): defining boundaries, dispatching isolated subagents ("empty backpacks"), and synthesizing verified conclusions.

---

## Phase 1: Partition & Fan-Out

1. **Deconstruct the Objective**:
   - Break the user's prompt or investigation into 2 to 5 orthogonal slices:
     - *By Module / Layer*: e.g. Data models vs. API routes vs. Frontend UI.
     - *By Hypothesis*: e.g. Investigating 3 independent theories for why a bug occurred.
     - *By Impact / Seam*: e.g. Identifying what breaks in upstream callers vs. downstream storage.

2. **Launch Isolated Workers**:
   - Use the `Agent` tool to dispatch subagents concurrently.
   - Pick the right subagent type:
     - `subagent_type: "Explore"` for search, file location, and reading patterns.
     - `subagent_type: "general-purpose"` for deep tracing, multi-step logic analysis, or running reproduction checks.
   - In each subagent prompt, enforce:
     - The explicit boundary of what to inspect.
     - The exact question to answer.
     - Return **only** distilled conclusions and file/line references (`file.ext#L123`), never whole file dumps.

---

## Phase 2: Adversarial Verification (The Reality Check)

When workers return critical claims, breaking changes, or reported bugs:
1. **Never accept claims on trust**:
   - The agent that discovered a bug or claimed a dependency often hallucinates or misreads subtle guards.
2. **Dispatch a Skeptic Subagent**:
   - For high-stakes findings, spawn a fresh agent whose explicit instruction is:
     > *"Adversarially verify this claim: [Claim]. Search the actual code to prove whether this is true or a false positive."*
3. **Filter Out Noise**:
   - Discard unconfirmed claims. Keep only battle-tested, verified facts.

---

## Phase 3: Synthesized Delivery

Present the final output directly to the user in a clean, high-density format:

```markdown
## Orchestration Summary: [Objective]

### Architecture / Findings
- **[Component / Topic]**: [1-2 line verified conclusion] ([path/to/file.ext#L42])
- **[Component / Topic]**: [1-2 line verified conclusion] ([path/to/file.ext#L105])

### Trade-offs & Breaking Changes (if applicable)
- [Key constraint or risk discovered during verification]

### Recommended Implementation Steps
1. [Step 1: File to edit and why]
2. [Step 2: File to edit and why]
```

Exit immediately without performing unnecessary edits in the main session until the user approves the synthesized plan.
