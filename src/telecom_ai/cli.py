import asyncio

import typer
from rich import print as rprint

from telecom_ai.llm.ollama_client import OllamaClient
from telecom_ai.llm.structured import coerce_to_model
from telecom_ai.prompts.order_intake import SYSTEM_PROMPT, build_user_prompt
from telecom_ai.schemas import ServiceOrder


def main(
    text: str = typer.Argument(..., help="Natural-language service order"),
    model: str | None = typer.Option(None, "--model", "-m", help="Override Ollama model tag"),
) -> None:
    """Parse a natural-language order into a validated ServiceOrder JSON."""
    client = OllamaClient(model=model) if model else None

    async def _run() -> ServiceOrder:
        return await coerce_to_model(
            ServiceOrder,
            system=SYSTEM_PROMPT,
            user=build_user_prompt(text),
            client=client,
        )

    result = asyncio.run(_run())
    rprint(result.model_dump_json(indent=2))


def app() -> None:
    typer.run(main)


if __name__ == "__main__":
    app()
