---
name: agent-graph-orchestration
description: "Build multi-agent AI systems as graphs (LangGraph) instead of single-agent ReAct loops. Sets up the full architecture: shared State object, specialized nodes (architect/coder/tester/critic agents), conditional edges for self-correction loops, and parallel fan-out. Use this skill whenever the user mentions LangGraph, agent graphs, multi-agent systems, agent orchestration, agent swarms, supervisor agents, 'nodes and edges' for AI, replacing a ReAct loop, self-correcting agents, critic gates, or wants multiple specialized AI agents working together on a workflow. Also trigger when a user complains that a single agent loop hallucinates, loses context, or burns tokens; the graph architecture is the fix."
---

# Agent Graph Orchestration

Turn a single-agent loop into a structured graph of specialized agents with shared state, conditional routing, and parallel execution. This skill both **explains** the architecture and **builds** it: when a user asks for an agent graph, scaffold a complete, runnable project for them.

## Core Concepts (30-second version)

The old way is one ReAct loop: reason → pick tool → observe → repeat, all in one giant context window. It degrades as context grows: the agent starts guessing, loops, and burns tokens.

A graph replaces that with three primitives:

1. **State**: one shared, typed object (a `TypedDict`) that every node reads from and writes to. Nodes never need chat history; they need only the fields relevant to their job.
2. **Nodes**: isolated functions or mini-agents with ONE job each (e.g., architect, coder, tester). Each takes State in, returns a partial State update.
3. **Edges**: directional wires between nodes. **Conditional edges** are routing functions that inspect State and decide where to go next (e.g., tester found bugs → route back to coder; clean → route to END).

This gives you: parallel fan-out (N reviewers at once), explicit self-correction loops with retry caps, and token efficiency (each node gets a small, clean context).

## Workflow: What To Do When This Skill Triggers

1. **Identify the pipeline.** Ask (or infer) what stages the user's workflow has. Default for coding tasks: Architect → Coder → Tester → (conditional loop back to Coder, max 3 retries) → END.
2. **Read the relevant reference file** before writing any code:
   - `references/setup-and-core-api.md`: installation, State design, nodes, edges, conditional edges, compiling and running. Read this FIRST for any build.
   - `references/patterns.md`: supervisor pattern, parallel fan-out (Send API), critic gates, checkpointing/human-in-the-loop, subgraphs. Read when the user needs anything beyond a linear pipeline.
   - `references/complete-example.md`: a full, runnable multi-agent code pipeline (architect/coder/tester with self-correction). Use as the template when scaffolding.
3. **Scaffold the project** as standalone files (graph.py, state.py, nodes/, requirements.txt) rather than inline snippets, unless the user only requests an explanation.
4. **Always include:** a retry counter in State with a hard cap on correction loops (prevents infinite cycles), typed State with reducers where lists accumulate, and a `if __name__ == "__main__"` runnable entry point.
5. **Verify** by running the graph structure (compile + `get_graph().draw_ascii()` or print node list) even if API keys aren't available; a compile check catches wiring errors.

## Design Rules (apply to every graph you build)

- **One job per node.** If a node's prompt says "and," consider splitting it.
- **State is the API.** Design the State schema before writing any node. Every field should answer: who writes it, who reads it.
- **Every cycle needs an exit.** Conditional edges that can loop backward MUST check a retry/iteration counter. Default cap: 3.
- **Nodes return deltas, not full state.** Return only the keys the node changed.
- **Keep LLM calls out of routing functions.** Conditional edges should be cheap, deterministic checks on State fields (e.g., `if state["bugs_found"]`). If a judgment call is needed, have a critic *node* write a verdict field to State, then route on that field.
- **Fan-out for independent work only.** Parallel branches must not depend on each other's output; merge results via list-append reducers.

## Common Mistakes to Avoid

- Passing full message history to every node (defeats the purpose: pass only needed State fields)
- Unbounded correction loops (always cap retries)
- One mega-node that does everything (that's just the old loop wearing a graph costume)
- Using conditional edges to make LLM calls (routing should be deterministic)
- Forgetting `Annotated[list, operator.add]` reducers when parallel nodes write to the same list key (causes state-clobbering errors)
