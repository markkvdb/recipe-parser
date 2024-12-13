# Recipe Parser

## Quickstart

Start the server with

```bash
uv run python app.py
```

and parse recipes using

```bash
uv run recipe-parser <SOURCE>
```

where SOURCE can be a URL or a path on your local system. The parser will try to create a recipe in a JSON format and is saved in the `recipes` folder by default. This can be configured in the CLI. For more options, please check it out with

```bash
uv run recipe-parser --help
```