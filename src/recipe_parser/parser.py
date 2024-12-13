"""Take raw input and parse to the Recipe model."""

from pathlib import Path

from anthropic import Anthropic

from .models import Recipe


def parse_text_to_recipe(text: str, client: Anthropic, model_name: str, system_path: Path) -> Recipe:
    """Parse text to recipe."""
    system_prompt = system_path.read_text()
    tools = [
        {
            "name": "recipe_parser",
            "description": "Parses a recipe from the message according to the provided schema.",
            "input_schema": Recipe.model_json_schema()
        }
    ]

    message = client.messages.create(
        max_tokens=8192,
        model=model_name,
        system=system_prompt,
        messages=[{
            "role": "user",
            "content": text,
        }],
        tools=tools,
        tool_choice={"type": "tool", "name": "recipe_parser"}
    )

    return Recipe(**message.content[0].input)
    