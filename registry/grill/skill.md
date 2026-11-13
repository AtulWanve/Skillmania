---
name: grill
description: Relentlessly interview the user about a plan, feature, or design until every branch of the decision tree is settled before writing code.
---

# Grilling

Interview the user relentlessly until you reach a shared understanding. Map the feature or plan as a **design tree**: every decision branches into the decisions that hang off it.

## The Process

1. **Map the Frontier**: 
   - Identify every decision whose prerequisites are already settled.
   - Separate **facts** from **decisions**: if an answer is in the codebase, search and read it yourself with native tools. Do not ask the user for facts the code already records.
   - If an answer is a product choice, edge case, tradeoff, or business logic, it is a **decision** for the user.

2. **Run in Rounds**:
   - Ask all frontier questions in one numbered round (typically 3 to 5 questions).
   - For every question, provide your **recommended answer** so the user can quickly reply with "yes, 2 is end of month, 3: agree".

3. **Advance the Tree**:
   - Once the user answers a round, those decisions settle that layer.
   - Reveal the next frontier of decisions that branch off those answers.
   - Repeat until the frontier is empty.

4. **Exit Condition**:
   - When all branches are resolved, output a concise 1-paragraph summary of the agreed spec and ask for confirmation before writing any code.
