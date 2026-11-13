---
name: handoff
description: Summarize active session progress, decisions, and immediate next steps into a concise handoff note before clearing context.
---

# Session Handoff

Compact the current conversation into a structured handoff document so a fresh session can pick up the task with a clean context.

## Output Structure

Generate a concise markdown handoff with the following sections:

1. **Objective**:
   - The primary feature, bug, or task being worked on in 1-2 sentences.

2. **Completed & Verified**:
   - Exact files created, modified, or deleted.
   - Tests or checks that have run and passed (with command outputs).

3. **Key Decisions & Constraints**:
   - Decisions settled with the user during the session.
   - Trade-offs chosen and alternatives rejected.

4. **Current State & Next Steps**:
   - Where the work stopped (e.g. branch name, uncommitted changes).
   - The exact next step or command the new session should execute.

5. **Resume Prompt**:
   - Provide a copy-pasteable prompt for the user to run in their new session after running `/clear`.
