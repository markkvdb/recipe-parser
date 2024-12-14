"""Split cooking book into separate markdown files."""

import re
from pathlib import Path

BOOK_NAME = "ottolenghi_comfort"
BOOK_PATH = Path(f"books/{BOOK_NAME}")
RECIPES_PATH = BOOK_PATH / "recipes"

# Read the Markdown content from the file
with open(BOOK_PATH / 'book.md', 'r') as file:
    content = file.read()

# Split the content into recipes based on the recipe title pattern
recipe_pattern = re.compile(r'^\s*##\s(.+)\n', re.MULTILINE)
recipes = recipe_pattern.split(content)[1:]

# Create a dictionary to store the recipe titles and content
recipe_dict = {}
for i in range(0, len(recipes), 2):
    title = recipes[i].strip()
    recipe_content = recipes[i + 1].strip()
    recipe_dict[title] = recipe_content

# Save each recipe as a separate Markdown file
if not RECIPES_PATH.exists():
    RECIPES_PATH.mkdir(parents=True, exist_ok=True)

for title, recipe_content in recipe_dict.items():
    filename = re.sub(r'[^\w\-_\. ]', '_', title) + '.md'
    with open(RECIPES_PATH / filename, 'w') as file:
        file.write(f'# {title}\n\n')
        file.write(recipe_content)

print(f"Split {len(recipe_dict)} recipes into separate files.")