import json

from pydantic import BaseModel, ValidationError

from telecom_ai.config import settings
from telecom_ai.llm.ollama_client import OllamaClient, OllamaError


class StructuredOutputError(RuntimeError):
    pass


async def coerce_to_model[T: BaseModel](
    model_cls: type[T],
    system: str,
    user: str,
    client: OllamaClient | None = None,
    max_retries: int | None = None,
) -> T:
    """Call Ollama with JSON-mode + schema, then validate against `model_cls`.

    On validation failure, re-asks the model with the validation error
    appended to the user prompt, up to `max_retries` times.
    """
    client = client or OllamaClient()
    retries = settings.max_retries if max_retries is None else max_retries
    schema = model_cls.model_json_schema()
    last_error: Exception | None = None
    current_user = user

    for _ in range(retries + 1):
        try:
            raw = await client.generate_json(system=system, user=current_user, schema=schema)
            data = json.loads(raw)
            return model_cls.model_validate(data)
        except (json.JSONDecodeError, ValidationError, OllamaError) as exc:
            last_error = exc
            current_user = (
                f"{user}\n\nYour previous response was invalid: {exc}\n"
                f"Return ONLY a JSON object matching the provided schema."
            )

    raise StructuredOutputError(f"Failed after {retries + 1} attempts: {last_error}")
