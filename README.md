# telecom-ai-agent-framework

Local-LLM agentic framework for telecom **service provisioning** workflows. Anchor use case: broadband (FTTH) activation, aligned to TMF641/TMF640.

> **Status:** M1 — foundation. The current milestone proves a 7B local model can reliably emit a TMF-aligned `ServiceOrder` JSON. RAG, tools, multi-step workflows, NETCONF integration, and multi-agent orchestration land in later milestones.

## Why local-only

No API keys, no hosted models, no per-token costs — clone the repo and `make up && make smoke` reproduces every result on a laptop.

## Quickstart

```bash
git clone https://github.com/spereir2/telecom-ai-agent-framework.git
cd telecom-ai-agent-framework

# Option A: pip
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# Option B: uv (when installed)
# uv sync --extra dev

# Start Ollama and pull the default model (qwen2.5:7b)
make up

# Smoke test
make smoke
```

Expected output is a JSON `ServiceOrder` for the canonical example:

```bash
nl-order "I'd like 500Mbps FTTH for 12 Baker Street, London W1U 6TS, account holder Jane Doe, jane@example.com"
```

## Run the eval harness

```bash
make eval                          # default model
make eval OLLAMA_MODEL=llama3.1:8b
```

Results land in `evals/results/<model>_<timestamp>.json`. The harness reports schema-validity %, field-accuracy %, and p50/p95 latency.

### Acceptance bar (M1)
- ≥ **90%** schema validity
- ≥ **75%** field accuracy
- on the 10-case `evals/dataset/orders_v1.jsonl`

## Architecture (M1)

See [docs/architecture-m1.md](docs/architecture-m1.md).

## Roadmap

| # | Milestone | Status |
|---|---|---|
| M1 | Foundation: Local LLM + Structured Outputs | In progress |
| M2 | Knowledge Base: RAG over Provisioning Specs | Pending |
| M3 | Single-Tool Agent | Pending |
| M4 | Workflow Decomposition with LangGraph | Pending |
| M5 | Network Device Interaction (Simulated NETCONF/YANG) | Pending |
| M6 | Multi-Agent Orchestration | Pending |
| M7 | Observability + Evaluation | Pending |
| M8 | Packaging & Demo | Pending |

## Development

```bash
make ci      # ruff + mypy + pytest
make fmt     # ruff format
make test    # pytest only
```

Pre-commit hooks: `pre-commit install` (run automatically by `make install`).

## License

[MIT](LICENSE)
