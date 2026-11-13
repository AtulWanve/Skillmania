# Complete Runnable Example

A full architect → coder → parallel reviewers → tester pipeline with a self-correction loop. Use this as the scaffold template: copy, then adapt node prompts/State fields to the user's actual workflow.

## requirements.txt

```
langgraph>=0.2
langchain-anthropic
```

## pipeline.py (single-file version for easy sharing)

```python
"""
Multi-agent code pipeline as a LangGraph graph.
Flow: architect -> coder -> [security_review || style_review] -> tester
      tester finds bugs? -> back to coder (max 3 retries) : -> END
Run:  export ANTHROPIC_API_KEY=... && python pipeline.py "your task here"
"""
import operator
import sys
from typing import Annotated, TypedDict

from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, START, END

llm = ChatAnthropic(model="claude-sonnet-4-5", max_tokens=4000)

# ---------- 1. STATE ----------
class State(TypedDict):
    task: str
    plan: str
    code: str
    review_notes: Annotated[list[str], operator.add]   # parallel reviewers append
    bugs: list[str]
    retries: int

# ---------- 2. NODES ----------
def architect(state: State) -> dict:
    r = llm.invoke(
        "You are a software architect. Output ONLY a short implementation plan "
        f"(components, functions, order). Task:\n{state['task']}"
    )
    return {"plan": r.content}

def coder(state: State) -> dict:
    bug_ctx = ""
    if state.get("bugs"):
        bug_ctx = ("\nYour previous attempt had these bugs. Fix them:\n- "
                   + "\n- ".join(state["bugs"])
                   + f"\nPrevious code:\n{state['code']}")
    if state.get("review_notes"):
        bug_ctx += "\nReviewer notes to incorporate:\n- " + "\n- ".join(state["review_notes"])
    r = llm.invoke(
        "You are a coder. Output ONLY code, no prose.\n"
        f"Plan:\n{state['plan']}{bug_ctx}"
    )
    return {"code": r.content, "retries": state.get("retries", 0) + 1,
            "bugs": []}  # clear stale bugs before re-test

def security_review(state: State) -> dict:
    r = llm.invoke(f"Security review. List concrete issues or say CLEAN.\n{state['code']}")
    return {"review_notes": [f"[security] {r.content}"]}

def style_review(state: State) -> dict:
    r = llm.invoke(f"Code style review. List concrete issues or say CLEAN.\n{state['code']}")
    return {"review_notes": [f"[style] {r.content}"]}

def tester(state: State) -> dict:
    r = llm.invoke(
        "You are a strict QA engineer. Find functional bugs in this code. "
        "Respond with one bug per line, or exactly NO_BUGS if none.\n"
        f"Plan (spec):\n{state['plan']}\nCode:\n{state['code']}"
    )
    text = r.content.strip()
    bugs = [] if "NO_BUGS" in text else [b for b in text.splitlines() if b.strip()]
    return {"bugs": bugs}

# ---------- 3. ROUTER (deterministic, no LLM) ----------
MAX_RETRIES = 3

def after_test(state: State) -> str:
    if state["bugs"] and state["retries"] < MAX_RETRIES:
        return "coder"
    return END

# ---------- 4. WIRING ----------
builder = StateGraph(State)
for name, fn in [("architect", architect), ("coder", coder),
                 ("security_review", security_review),
                 ("style_review", style_review), ("tester", tester)]:
    builder.add_node(name, fn)

builder.add_edge(START, "architect")
builder.add_edge("architect", "coder")
builder.add_edge("coder", "security_review")   # fan-out: both reviews
builder.add_edge("coder", "style_review")      # run in parallel
builder.add_edge("security_review", "tester")  # fan-in: tester waits
builder.add_edge("style_review", "tester")     # for both
builder.add_conditional_edges("tester", after_test, ["coder", END])

graph = builder.compile()

# ---------- 5. RUN ----------
if __name__ == "__main__":
    task = sys.argv[1] if len(sys.argv) > 1 else "Write a Python function that validates US phone numbers"
    print(graph.get_graph().draw_ascii())
    final = None
    for chunk in graph.stream(
        {"task": task, "plan": "", "code": "", "review_notes": [], "bugs": [], "retries": 0},
        stream_mode="values",
    ):
        final = chunk
        done = [k for k in ("plan", "code") if chunk.get(k)]
        print(f"[state has: {done} | retries={chunk.get('retries', 0)} | bugs={len(chunk.get('bugs', []))}]")
    print("\n===== FINAL CODE =====\n")
    print(final["code"])
```

## What to point out when handing this to a user

- The **fan-out/fan-in** (coder → two reviewers → tester): tester automatically waits for both parallel branches; `review_notes` uses an append reducer so the parallel writes don't collide.
- The **self-correction loop** (tester → coder) is capped at `MAX_RETRIES = 3`: the graph can never spin forever.
- **Token efficiency in practice**: the tester's prompt contains exactly two State fields (plan + code). No chat history exists anywhere in this system.
- The coder **clears `bugs`** when producing a fix so the next test round starts clean.
- Adapting it = changing the State fields and node prompts; the wiring pattern stays identical for most build-review-fix workflows.
