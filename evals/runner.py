from __future__ import annotations

import argparse
import asyncio
import json
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from telecom_ai.llm.ollama_client import OllamaClient
from telecom_ai.llm.structured import StructuredOutputError, coerce_to_model
from telecom_ai.prompts.order_intake import SYSTEM_PROMPT, build_user_prompt
from telecom_ai.schemas import ServiceOrder

DATASET = Path(__file__).parent / "dataset" / "orders_v1.jsonl"
RESULTS_DIR = Path(__file__).parent / "results"

SCORED_FIELDS = [
    ("customer", "full_name"),
    ("customer", "customer_type"),
    ("service_address", "line1"),
    ("service_address", "city"),
    ("service_address", "postcode"),
    ("service_address", "country_code"),
    ("product", "service_type"),
    ("product", "bandwidth", "downstream"),
    ("product", "bandwidth", "unit"),
]


@dataclass
class CaseResult:
    case_id: str
    schema_valid: bool
    field_matches: int
    field_total: int
    latency_ms: float
    error: str | None


def _get(obj: dict[str, Any], path: tuple[str, ...]) -> Any:
    cur: Any = obj
    for key in path:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(key)
    return cur


def _score_fields(actual: dict[str, Any], expected: dict[str, Any]) -> tuple[int, int]:
    matches = 0
    for path in SCORED_FIELDS:
        a = _get(actual, path)
        e = _get(expected, path)
        if e is None:
            continue
        if isinstance(a, str) and isinstance(e, str):
            if a.strip().lower() == e.strip().lower():
                matches += 1
        elif a == e:
            matches += 1
    total = sum(1 for p in SCORED_FIELDS if _get(expected, p) is not None)
    return matches, total


async def _run_case(client: OllamaClient, case: dict[str, Any]) -> CaseResult:
    started = time.perf_counter()
    try:
        order = await coerce_to_model(
            ServiceOrder,
            system=SYSTEM_PROMPT,
            user=build_user_prompt(case["input"]),
            client=client,
        )
        latency_ms = (time.perf_counter() - started) * 1000
        matches, total = _score_fields(order.model_dump(mode="json"), case["expected"])
        return CaseResult(case["id"], True, matches, total, latency_ms, None)
    except StructuredOutputError as exc:
        latency_ms = (time.perf_counter() - started) * 1000
        _, total = _score_fields({}, case["expected"])
        return CaseResult(case["id"], False, 0, total, latency_ms, str(exc))


async def run(model: str) -> dict[str, Any]:
    client = OllamaClient(model=model)
    cases = [json.loads(line) for line in DATASET.read_text().splitlines() if line.strip()]
    results = [await _run_case(client, c) for c in cases]

    schema_valid_pct = 100 * sum(r.schema_valid for r in results) / len(results)
    total_matches = sum(r.field_matches for r in results)
    total_fields = sum(r.field_total for r in results)
    field_accuracy_pct = 100 * total_matches / total_fields if total_fields else 0.0
    latencies = sorted(r.latency_ms for r in results)
    p50 = latencies[len(latencies) // 2]
    p95 = latencies[max(0, int(0.95 * len(latencies)) - 1)]

    summary = {
        "model": model,
        "timestamp": datetime.now(UTC).isoformat(),
        "n_cases": len(results),
        "schema_validity_pct": round(schema_valid_pct, 2),
        "field_accuracy_pct": round(field_accuracy_pct, 2),
        "latency_p50_ms": round(p50, 1),
        "latency_p95_ms": round(p95, 1),
        "cases": [r.__dict__ for r in results],
    }
    return summary


def _print_summary(summary: dict[str, Any]) -> None:
    print(f"\nModel:              {summary['model']}")
    print(f"Cases:              {summary['n_cases']}")
    print(f"Schema validity:    {summary['schema_validity_pct']}%")
    print(f"Field accuracy:     {summary['field_accuracy_pct']}%")
    print(f"Latency p50/p95:    {summary['latency_p50_ms']} / {summary['latency_p95_ms']} ms")
    failures = [c for c in summary["cases"] if not c["schema_valid"]]
    if failures:
        print(f"\nSchema failures ({len(failures)}):")
        for f in failures:
            print(f"  - {f['case_id']}: {f['error']}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    args = parser.parse_args()

    summary = asyncio.run(run(args.model))
    RESULTS_DIR.mkdir(exist_ok=True)
    out = RESULTS_DIR / f"{args.model.replace(':', '_')}_{int(time.time())}.json"
    out.write_text(json.dumps(summary, indent=2))
    _print_summary(summary)
    print(f"\nFull results: {out}")


if __name__ == "__main__":
    main()
