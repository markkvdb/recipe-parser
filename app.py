from pathlib import Path

from anthropic import Anthropic
from pydantic_settings import BaseSettings, SettingsConfigDict
import httpx
from bs4 import BeautifulSoup

from recipe_parser.models import Recipe

class Settings(BaseSettings):
    api_key: str
    claude_model_name: str

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

settings = Settings()

# load HTML page from the internet
source = httpx.get("https://foodette.fr/recette/saumon-fuma-artisanal-et-lentilles-acidula-es")
soup = BeautifulSoup(source.text, "html.parser")
plain_text = soup.get_text()

plain_text = Path("books/ottolenghi_comfort/recipes/____c10.xhtml_page_290 .pagebreak role__doc-pagebreak_ title__290__Dutch apple cake __c10.xhtml_page_290_anchor .rt_.md").read_text()

client = Anthropic(api_key=settings.api_key)
system_prompt = Path("recipe-prompt.txt").read_text()
tools = [
    {
        "name": "recipe_parser",
        "description": "Parses a recipe from the message according to the provided schema.",
        "input_schema": Recipe.model_json_schema()
    }
]

messages = client.messages.create(
    max_tokens=8192,
    model=settings.claude_model_name,
    system=system_prompt,
    messages=[{
        "role": "user",
        "content": plain_text,
    }],
    tools=tools,
    tool_choice={"type": "tool", "name": "recipe_parser"}
)

x = 0