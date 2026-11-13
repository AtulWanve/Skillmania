# Setup & Core API

Everything needed to go from zero to a compiled, running graph.

## 1. Installation

```bash
pip install -U langgraph langchain-anthropic
# optional but recommended:
pip install -U "langgraph-checkpoint-sqlite"   # persistent checkpointing
```

Set the API key:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

(For OpenAI models swap in `langchain-openai` and `OPENAI_API_KEY`. The graph code is model-agnostic.)

Recommended project layout when scaffolding for a user:

```
my-agent-graph/
├── requirements.txt
├── state.py          # the shared State schema
├── nodes.py          # node functions (or nodes/ package if large)
├── graph.py          # wiring: nodes + edges + compile
└── main.py           # entry point
```

## 2. State: design this FIRST

State is a `TypedDict`. It is the ONLY communication channel between nodes.

```python
# state.py
import operator
from typing import Annotated, TypedDict

class PipelineState(TypedDict):
    task: str                                   # the user's goal (written once)
    plan: str                                   # written by architect, read by coder
    code: str                                   # written by coder, read by tester
    bugs: list[str]                             # written by tester, read by coder + router
    review_notes: Annotated[list[str], operator.add]  # parallel reviewers APPEND here
    retries: int                                # incremented on each fix loop
```

Key rules:

- **Reducers**: `Annotated[list, operator.add]` means concurrent writes append instead of overwrite. REQUIRED for any key that parallel (fan-out) nodes write to. Without it, two nodes updating the same key in the same step raises an `InvalidUpdateError`.
- Plain keys (no reducer) are last-write-wins.
- For chat-style graphs there's a prebuilt `from langgraph.graph import MessagesState` with a `messages` key and message-append reducer; use it only when nodes genuinely need conversational history.

## 3. Nodes: one job each

A node is a plain function: takes State, returns a **partial** update (only changed keys).

```python
# nodes.py
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-sonnet-4-5")

def architect(state: PipelineState) -> dict:
    """Only plans. Never writes code."""
    resp = llm.invoke(
        f"Create a concise implementation plan (files, functions, order) for:\n{state['task']}"
    )
    return {"plan": resp.content}

def coder(state: PipelineState) -> dict:
    """Only writes code. Gets plan + any bugs from last test round: nothing else."""
    bug_context = f"\nFix these bugs:\n" + "\n".join(state["bugs"]) if state.get("bugs") else ""
    resp = llm.invoke(
        f"Write the code for this plan:\n{state['plan']}{bug_context}\n"
        f"Previous code (if fixing):\n{state.get('code','')}"
    )
    return {"code": resp.content, "retries": state.get("retries", 0) + 1}
```

Notice the token efficiency: each node's prompt is built from 2-3 State fields, not a transcript.

## 4. Edges: wiring and routing

```python
# graph.py
from langgraph.graph import StateGraph, START, END
from state import PipelineState
from nodes import architect, coder, tester

builder = StateGraph(PipelineState)

builder.add_node("architect", architect)
builder.add_node("coder", coder)
builder.add_node("tester", tester)

# Fixed edges: always this path
builder.add_edge(START, "architect")
builder.add_edge("architect", "coder")
builder.add_edge("coder", "tester")

# Conditional edge: the router (cheap, deterministic, no LLM calls)
MAX_RETRIES = 3

def route_after_test(state: PipelineState) -> str:
    if state["bugs"] and state["retries"] < MAX_RETRIES:
        return "coder"        # loop back to fix
    return END                 # clean, or retry budget exhausted

builder.add_conditional_edges("tester", route_after_test, ["coder", END])

graph = builder.compile()
```

`add_conditional_edges(source, router_fn, possible_destinations)`: the router returns the name of the next node (or `END`). The destination list is optional but makes the graph drawable and catches typos.

## 5. Running it

```python
# main.py
from graph import graph

result = graph.invoke({
    "task": "Build a FastAPI endpoint that returns fibonacci(n)",
    "bugs": [],
    "review_notes": [],
    "retries": 0,
})
print(result["code"])
```

Streaming progress node-by-node (great for UX):

```python
for chunk in graph.stream(initial_state, stream_mode="updates"):
    for node_name, update in chunk.items():
        print(f"--- {node_name} finished ---")
```

Visualize the wiring (sanity check, works without API keys):

```python
print(graph.get_graph().draw_ascii())   # or .draw_mermaid()
```

## 6. Compile-time verification checklist

Before handing a graph to the user, verify:

1. `builder.compile()` succeeds (catches orphan nodes / bad edge names)
2. Every backward-pointing conditional edge checks a counter against a cap
3. Every State key written by 2+ parallel nodes has a reducer
4. `START` reaches every node; every path reaches `END`
