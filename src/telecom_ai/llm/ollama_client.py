from typing import Any

import httpx

from telecom_ai.config import settings


class OllamaError(RuntimeError):
    pass


class OllamaClient:
    def __init__(
        self,
        host: str | None = None,
        model: str | None = None,
        timeout: float | None = None,
    ) -> None:
        self.host = host or settings.ollama_host
        self.model = model or settings.ollama_model
        self.timeout = timeout or settings.request_timeout_seconds

    async def generate_json(
        self,
        system: str,
        user: str,
        schema: dict[str, Any] | None = None,
    ) -> str:
        payload: dict[str, Any] = {
            "model": self.model,
            "stream": False,
            "format": schema if schema is not None else "json",
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(f"{self.host}/api/chat", json=payload)
        if resp.status_code != 200:
            raise OllamaError(f"Ollama returned {resp.status_code}: {resp.text}")
        data = resp.json()
        content = data.get("message", {}).get("content")
        if not isinstance(content, str):
            raise OllamaError(f"Unexpected response shape: {data!r}")
        return content
