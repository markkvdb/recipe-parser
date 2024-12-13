"""Utility functions."""

def format_fn(name: str):
    # Convert the string to lowercase
    lowercase_name = name.lower()
    
    # Replace spaces with dashes
    return lowercase_name.replace(' ', '-')
