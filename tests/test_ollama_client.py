import json
from collections.abc import Callable
from typing import Any

import httpx
import pytest

from telecom_ai.llm.ollama_client import OllamaClient, OllamaError
from telecom_ai.llm.structured import StructuredOutputError, coerce_to_model
from telecom_ai.schemas import ServiceOrder, ServiceType


def _valid_order_payload() -> dict[str, Any]:
    return {
        "customer": {"full_name": "Jane Doe", "customer_type": "residential"},
        "service_address": {
            "line1": "12 Baker Street",
            "city": "London",
            "postcode": "W1U 6TS",
            "country_code": "GB",
        },
        "product": {
            "service_type": "ftth_residential",
            "bandwidth": {"downstream": 100, "unit": "Mbps"},
        },
    }


def _mock_transport(responses: list[str]) -> httpx.MockTransport:
    iterator = iter(responses)

    def handler(request: httpx.Request) -> httpx.Response:
        content = next(iterator)
        return httpx.Response(200, json={"message": {"content": content}})

    return httpx.MockTransport(handler)


@pytest.fixture
def patched_client(monkeypatch: pytest.MonkeyPatch) -> Callable[[list[str]], OllamaClient]:
    def install(responses: list[str]) -> OllamaClient:
        transport = _mock_transport(responses)

        original_init = httpx.AsyncClient.__init__

        def patched_init(self, *args, **kwargs):  # type: ignore[no-untyped-def]
            kwargs["transport"] = transport
            original_init(self, *args, **kwargs)

        monkeypatch.setattr(httpx.AsyncClient, "__init__", patched_init)
        return OllamaClient(host="http://test", model="test-model")

    return install


async def test_generate_json_success(patched_client: Callable[[list[str]], OllamaClient]) -> None:
    client = patched_client([json.dumps(_valid_order_payload())])
    raw = await client.generate_json(system="sys", user="usr")
    assert json.loads(raw)["customer"]["full_name"] == "Jane Doe"


async def test_coerce_to_model_succeeds_first_try(
    patched_client: Callable[[list[str]], OllamaClient],
) -> None:
    client = patched_client([json.dumps(_valid_order_payload())])
    order = await coerce_to_model(ServiceOrder, system="sys", user="usr", client=client)
    assert order.product.service_type is ServiceType.FTTH_RESIDENTIAL


async def test_coerce_to_model_retries_on_invalid_json(
    patched_client: Callable[[list[str]], OllamaClient],
) -> None:
    client = patched_client(["not json", json.dumps(_valid_order_payload())])
    order = await coerce_to_model(
        ServiceOrder, system="sys", user="usr", client=client, max_retries=1
    )
    assert order.customer.full_name == "Jane Doe"


async def test_coerce_to_model_exhausts_retries(
    patched_client: Callable[[list[str]], OllamaClient],
) -> None:
    client = patched_client(["not json", "still not json"])
    with pytest.raises(StructuredOutputError):
        await coerce_to_model(ServiceOrder, system="sys", user="usr", client=client, max_retries=1)


async def test_ollama_error_on_non_200(monkeypatch: pytest.MonkeyPatch) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, text="boom")

    transport = httpx.MockTransport(handler)
    original_init = httpx.AsyncClient.__init__

    def patched_init(self, *args, **kwargs):  # type: ignore[no-untyped-def]
        kwargs["transport"] = transport
        original_init(self, *args, **kwargs)

    monkeypatch.setattr(httpx.AsyncClient, "__init__", patched_init)
    client = OllamaClient(host="http://test", model="test-model")
    with pytest.raises(OllamaError):
        await client.generate_json(system="s", user="u")
