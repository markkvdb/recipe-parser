"""Command line interface for recipe parser."""

from pathlib import Path

import typer
from anthropic import Anthropic
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import HttpUrl, ValidationError, SecretStr

from recipe_parser.parser import parse_input_to_recipe, source_to_input
from recipe_parser.utils import format_fn


class Settings(BaseSettings):
    """Settings for the recipe parser."""

    api_key: SecretStr
    claude_model_name: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


def validate_url(url: str) -> bool:
    """Validate if string is a proper URL using Pydantic."""
    try:
        HttpUrl(url)
        return True
    except ValidationError:
        return False


def source_callback(value: str) -> str:
    """Validate source is either a valid URL or existing file."""
    if validate_url(value):
        return value

    path = Path(value)
    if not path.exists():
        raise typer.BadParameter(f"File {value} does not exist")
    return value


app = typer.Typer()


@app.command()
def parse(
    source: str = typer.Argument(
        ..., help="URL or path to file containing recipe"
    ),
    system_prompt: Path = typer.Option(
        "recipe-prompt.txt",
        "--system-prompt",
        "-s",
        help="Path to system prompt file",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    output_dir: Path = typer.Option(
        Path("./recipes"),
        "--output-dir",
        "-o",
        help="Directory to save parsed recipes",
        file_okay=False,
        dir_okay=True,
    ),
) -> None:
    """Parse a recipe from a URL or file."""
    settings = Settings()

    # Parse source to Claude content
    input = source_to_input(source)

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    client = Anthropic(api_key=settings.api_key.get_secret_value())

    recipe = parse_input_to_recipe(
        input=input,
        client=client,
        model_name=settings.claude_model_name,
        system_path=system_prompt,
    )

    # Save recipe to JSON file
    recipe_path = output_dir / f"{format_fn(recipe.title)}.json"
    recipe_path.write_text(recipe.model_dump_json())


def main():
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
