# M1 Architecture

```mermaid
flowchart LR
    user[CLI user] -->|nl-order text| cli[telecom_ai.cli]
    cli --> structured[coerce_to_model]
    structured -->|JSON-mode + schema| ollama[Ollama API]
    ollama --> model[(qwen2.5:7b / llama3.1:8b / mistral:7b)]
    structured -->|validate| schemas[(Pydantic ServiceOrder)]
    schemas --> cli
    cli -->|JSON| user

    subgraph evaluation
        runner[evals/runner.py] --> structured
        runner --> results[(evals/results/*.json)]
    end
```

## Components

| Component | Purpose | File |
|---|---|---|
| `cli` | Typer entry point `nl-order` | `src/telecom_ai/cli.py` |
| `OllamaClient` | Async HTTP wrapper around Ollama `/api/chat` with JSON-mode | `src/telecom_ai/llm/ollama_client.py` |
| `coerce_to_model` | Reask loop that forces output into a Pydantic model | `src/telecom_ai/llm/structured.py` |
| `ServiceOrder` | TMF641-flavored schema | `src/telecom_ai/schemas/service_order.py` |
| `order_intake` prompt | System prompt + few-shot examples | `src/telecom_ai/prompts/order_intake.py` |
| `evals/runner` | Scores schema-validity, field-accuracy, latency | `evals/runner.py` |

## Out of M1
- No retrieval / RAG (added in M2)
- No tool calls (M3)
- No multi-step workflow (M4)
- No NETCONF (M5)
- No multi-agent (M6)
- No tracing UI (M7)
