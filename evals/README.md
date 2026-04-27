# Eval Harness

Measures how reliably a local LLM converts natural-language service orders into valid `ServiceOrder` JSON.

## Run

```bash
make up                 # ensure ollama is running
make eval               # uses default OLLAMA_MODEL=qwen2.5:7b
make eval OLLAMA_MODEL=llama3.1:8b
```

Results are written to `evals/results/<model>_<timestamp>.json` (gitignored).

## Metrics

- **Schema validity %** — share of cases whose response parsed into a `ServiceOrder` after the retry budget.
- **Field accuracy %** — fraction of expected fields (across all cases) that match the model output exactly (case-insensitive for strings).
- **Latency p50 / p95** — wall-clock per case, including retries.

## Adding cases

Append a JSONL line to `dataset/orders_v1.jsonl`:

```json
{"id": "unique-slug", "input": "natural language order", "expected": { ... ServiceOrder fields ... }}
```

Only fields present in `expected` are scored — omit fields you don't want to assert on.
