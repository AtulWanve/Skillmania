# Advanced Patterns

Read this when the user needs more than a linear pipeline with one correction loop.

## Table of Contents
1. Parallel Fan-Out (Send API)
2. Supervisor Pattern
3. Critic Gates (LLM-as-judge, done right)
4. Checkpointing & Human-in-the-Loop
5. Subgraphs (graphs inside graphs)
6. Prebuilt ReAct agents as nodes

---

## 1. Parallel Fan-Out (Send API)

Run N specialized reviewers on the same code simultaneously, then merge.

**Static fan-out** (fixed set of parallel nodes): just add multiple edges from one node; LangGraph runs same-step nodes concurrently:

```python
builder.add_edge("coder", "security_review")
builder.add_edge("coder", "perf_review")
builder.add_edge("coder", "style_review")
# all three then converge:
builder.add_edge("security_review", "merge_reviews")
builder.add_edge("perf_review", "merge_reviews")
builder.add_edge("style_review", "merge_reviews")
```

`merge_reviews` won't run until all three parents finish. CRITICAL: the key the reviewers write to (e.g., `review_notes`) MUST have an `operator.add` reducer or the graph errors on concurrent writes.

**Dynamic fan-out** (N unknown until runtime, e.g., one worker per file) uses `Send`:

```python
from langgraph.types import Send

def dispatch_workers(state: PipelineState):
    return [Send("review_file", {"file": f, "task": state["task"]})
            for f in state["files"]]

builder.add_conditional_edges("planner", dispatch_workers, ["review_file"])
```

Each `Send` spawns an instance of the node with its own private input dict. Results merge back into shared State via reducers.

## 2. Supervisor Pattern

One router agent decides which specialist handles the next step. Use when the workflow order isn't known ahead of time.

```python
def supervisor(state) -> dict:
    resp = llm.with_structured_output(RouteDecision).invoke(
        f"Task status: {state['status']}\nWho should act next: researcher, coder, or FINISH?"
    )
    return {"next_worker": resp.worker}

def route_from_supervisor(state) -> str:
    return state["next_worker"] if state["next_worker"] != "FINISH" else END

builder.add_conditional_edges("supervisor", route_from_supervisor, ["researcher", "coder", END])
builder.add_edge("researcher", "supervisor")   # workers always report back
builder.add_edge("coder", "supervisor")
```

Note the division of labor: the supervisor **node** makes the LLM judgment and writes it to State; the conditional edge just reads the field. Never call an LLM inside the routing function itself.

## 3. Critic Gates

A quality gate = critic node (writes verdict to State) + conditional edge (routes on verdict) + retry cap.

```python
def critic(state) -> dict:
    resp = llm.with_structured_output(Verdict).invoke(
        f"Does this output meet the spec? Spec: {state['plan']}\nOutput: {state['code']}"
    )
    return {"approved": resp.approved, "critique": resp.feedback}

def gate(state) -> str:
    if state["approved"] or state["retries"] >= 3:
        return "publish"
    return "coder"
```

When looping back, pass the `critique` into the coder's context and consider clearing stale fields (e.g., reset `bugs: []`) so the fix attempt starts clean.

## 4. Checkpointing & Human-in-the-Loop

A checkpointer persists State after every node, enabling resume-after-crash, time travel, and pause-for-approval.

```python
from langgraph.checkpoint.memory import MemorySaver  # or SqliteSaver for durable

graph = builder.compile(
    checkpointer=MemorySaver(),
    interrupt_before=["deploy"],        # pause before dangerous nodes
)

config = {"configurable": {"thread_id": "job-42"}}
graph.invoke(initial_state, config)      # runs until the interrupt
# ... human reviews ...
graph.invoke(None, config)               # None = resume from checkpoint
```

Every invocation with the same `thread_id` continues the same persisted run. Inspect state anytime with `graph.get_state(config)`.

## 5. Subgraphs

A compiled graph is itself a node. Use for reusable units (e.g., a "test-and-fix" loop used by several parent pipelines):

```python
test_fix_subgraph = test_builder.compile()
parent.add_node("qa", test_fix_subgraph)   # shares State keys with same names
```

If the subgraph's State schema differs, wrap it in a function that translates keys in/out.

## 6. Prebuilt ReAct agents as nodes

The loop isn't dead; it's demoted. A small tool-using ReAct agent is often the right *implementation of a single node*, with the graph controlling everything around it:

```python
from langgraph.prebuilt import create_react_agent

research_agent = create_react_agent(llm, tools=[web_search, read_file])

def researcher(state) -> dict:
    result = research_agent.invoke({"messages": [("user", state["research_question"])]})
    return {"findings": result["messages"][-1].content}
```

Graph = macro-structure (who, when, retry policy). ReAct = micro-execution inside one node.
