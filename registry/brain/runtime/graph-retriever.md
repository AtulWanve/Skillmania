---
title: Graph Retriever
tags: [runtime, graph, retrieval, context]
aliases: [Retriever]
---

# Graph Retriever

Determines the minimum context required by querying the graph. Runs after [[runtime/task-classifier|Task Classifier]] and feeds into [[runtime/context-loader|Context Loader]].

## Output Representation

Each affected node is returned as an `AffectedNode` object:

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | Unique node identifier; must match a node in the current snapshot's `nodes.json`, resolved through `graph/manifest.json` via the snapshot-indirection contract |
| `type` | `"module" \| "api" \| "route" \| "component" \| "config" \| "test"` | Node category |
| `path` | `string` | File system path relative to project root |
| `label` | `string` | Human-readable node name |
| `connectedResources` | `{ apis: string[]; routes: string[]; components: string[] }` | Resource references discovered via graph edges |

Return type:

```typescript
{
  affectedNodes: AffectedNode[];
  graphEmpty: boolean;
}
```

- `graphEmpty` is `true` **only** when snapshot resolution succeeds and the parsed `nodes.json` is exactly `[]` (empty array). Resolution follows the snapshot-indirection contract: read `graph/manifest.json`, locate the current version directory (e.g., `graph/v-<timestamp>/`), and read that snapshot's `nodes.json`. It signals [[runtime/context-loader|Context Loader]] to enter **Empty-Graph Fallback Mode**.
- `graphEmpty` is `false` when retrieval succeeds with any nodes. A result of zero affected nodes from a non-empty graph still returns `graphEmpty: false`.
- If manifest resolution fails (missing/unreadable `graph/manifest.json`), the referenced version directory does not exist, or `nodes.json` is missing, malformed, or fails schema validation, the retriever MUST throw a distinct error: it MUST NOT map these failures to `graphEmpty: true`. Only a successfully resolved and parsed `nodes.json` containing exactly `[]` produces `graphEmpty: true`.
- Graph initialization is **not** triggered here: it occurs via [[runtime/graph-updater|Graph Updater]] after the first accepted change.

## Tree-Based Retrieval Strategy (Blueprint)

In addition to graph-based retrieval, the retriever can use **tree-based reasoning** (inspired by [PageIndex](https://github.com/VectifyAI/PageIndex)) when working with hierarchical documents:

- **Tree construction**: Long documents are transformed into a hierarchical tree index (title + summary + children per node)
- **LLM-guided traversal**: Top-down search (at each node, the LLM evaluates relevance and descends into promising branches)
- **Multi-strategy**: Beam search for small trees (< 50 nodes), block retrieval with KV-cache reuse for larger ones (inspired by [ConDB](https://github.com/VectifyAI/ConDB))
- **Multi-resolution**: Retrieve summaries at higher levels, full content at leaves (matches context engineering needs)

See [[memory/vectifyai-blueprints]] for the full pattern specification.

> [!warning] Manifest resolution errors are distinct from empty-graph signals. Missing or malformed manifests MUST throw, not silently return `graphEmpty: true`.

### Empty-Graph Behavior

When the manifest-resolved snapshot's `nodes.json` is `[]`:

1. Return `{ affectedNodes: [], graphEmpty: true }`.
2. [[runtime/context-loader|Context Loader]] enters **Empty-Graph Fallback Mode** when `graphEmpty === true`.
3. Graph initialization is **not** triggered here: it occurs via [[runtime/graph-updater|Graph Updater]] after the first accepted change.
