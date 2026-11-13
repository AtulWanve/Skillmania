---
name: prototype
description: Build a throwaway prototype or mock to answer a specific design, UI, or state question before building production code.
---

# Throwaway Prototype

A prototype is **disposable code designed to answer a single question**. It is never meant to be merged directly.

## Process

1. **Isolate the Question**:
   - Determine what uncertainty is being resolved:
     - **UI / Layout**: What should the visual hierarchy, inputs, and states look like?
     - **State / Logic**: Does the proposed data model handle all transitions cleanly?
     - **Data Flow**: Can two systems connect with acceptable performance?

2. **Choose the Format**:
   - **UI / Frontend**: Create an interactive single-file HTML artifact or component with mock data and basic styling.
   - **CLI / Backend**: Create a standalone scratch script in a temporary location with hardcoded fixtures.

3. **Provide Variations**:
   - Offer 2 to 3 distinct variations that take different approaches to the problem (e.g. compact vs. expanded UI, synchronous vs. event-driven logic).
   - Label each variation with its trade-offs.

4. **Review & Discard**:
   - Present the prototypes to the user to test and select.
   - Once the decision is made, delete the throwaway files and use the agreed interface as the spec for production implementation.
