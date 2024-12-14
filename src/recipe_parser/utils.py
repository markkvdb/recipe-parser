"""Utility functions."""

from datetime import timedelta

from pydantic import HttpUrl, ValidationError
from bs4 import BeautifulSoup

def is_valid_http_url(url: str) -> bool:
    try:
        HttpUrl(url)
        return True
    except ValidationError:
        return False

def is_html(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return bool(BeautifulSoup(content, "html.parser").find())

def format_fn(name: str):
    # Convert the string to lowercase
    lowercase_name = name.lower()
    
    # Replace spaces with dashes
    return lowercase_name.replace(' ', '-')


def format_duration(td: timedelta) -> str:
    """
    Convert a timedelta to a human-readable string for recipe durations.
    
    Args:
    td (timedelta): The duration to format
    
    Returns:
    str: A human-readable string representation of the duration
    """
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    parts = []
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours > 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
    if seconds > 0 and not (hours > 0 and minutes > 0):  # Only show seconds if no hours and minutes
        parts.append(f"{seconds} second{'s' if seconds > 1 else ''}")
    
    if len(parts) == 0:
        return "less than a second"
    elif len(parts) == 1:
        return parts[0]
    elif len(parts) == 2:
        return f"{parts[0]} and {parts[1]}"
    else:
        return f"{parts[0]}, {parts[1]} and {parts[2]}"
