"""Take raw input and parse to the Recipe model."""

import base64
from pathlib import Path
from typing import Literal
import httpx
import logging

from pydantic import BaseModel, Base64Bytes
from anthropic import Anthropic
from bs4 import BeautifulSoup

from .models import Recipe
from .utils import is_valid_http_url

FileType = Literal["image/jpeg", "image/png", "image/webp", "application/pdf", "text/plain"]

logger = logging.getLogger(__name__)

class Base64Input(BaseModel):
    """Image input."""

    data: bytes
    file_type: FileType


def source_to_input(path: str) -> str | Base64Input:
    """Read from source path and return Claude-compatible object."""
    if is_valid_http_url(path):
        response = httpx.get(path)
        response.raise_for_status()
        raw_data = response.content
    else:
        raw_data = Path(path).read_bytes()

    file_type = _get_file_type(path)
    logger.info(f"file type is {file_type}")

    # extract only text if file is a HTML file.
    if file_type == "text/plain":
        soup = BeautifulSoup(raw_data.decode("utf-8"), "html.parser")
        raw_data = soup.get_text().encode("utf-8")

    return Base64Input(data=base64.standard_b64encode(raw_data), file_type=file_type)



def parse_input_to_recipe(input: Base64Input, client: Anthropic, model_name: str, system_path: Path) -> Recipe:
    """Parse text to recipe."""
    system_prompt = system_path.read_text()
    tools = [
        {
            "name": "recipe_parser",
            "description": "Parses a recipe from the message according to the provided schema.",
            "input_schema": Recipe.model_json_schema()
        }
    ]
    input_content = _input_to_claude_content(input)

    message = client.messages.create(
        max_tokens=8192,
        model=model_name,
        system=system_prompt,
        messages=[{
            "role": "user",
            "content": [input_content],
        }],
        tools=tools,
        tool_choice={"type": "tool", "name": "recipe_parser"}
    )

    return Recipe(**message.content[0].input)
    

def _input_to_claude_content(input: Base64Input) -> dict:
    """Input to claude content."""
    match input.file_type:
        case "text/plain":
            content = {
                "type": "text",
                "text": input.data.decode("utf-8")
            }
        case "application/pdf":
            content = {
                "type": "document",
                "source": {
                    "type": "base64",
                    "media_type": "application/pdf",
                    "data": input.data.decode("utf-8")
                }
            }
        case _:
            content = {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": input.file_type,
                    "data": input.data.decode("utf-8")
                }
            }
    
    return content 


def _get_file_type(path: str) -> FileType:
    """Get file type from path."""
    _, extension = path.rsplit(".")

    if extension is None:
        logger.warning("No extension provided. Assume it's text.")
        return "text/plain"
    
    extension = extension.lower()
    if extension in ["jpeg", "webp", "png"]:
        return f"image/{extension}"
    elif extension == "pdf":
        return "application/pdf"
    else:
        logger.warning(f"{extension} is assumed to be plain text")
        return "text/plain"
