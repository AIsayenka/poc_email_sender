def render_template(template: str, context: dict) -> str:
    """
    Renders a template string with the given context.

    :param template: The template content with placeholders, e.g., "Hello {name}"
    :param context: Dictionary of placeholder values, e.g., {"name": "Alex"}
    :return: Rendered template as a string
    """
    try:
        return template.format(**context)
    except KeyError as e:
        raise ValueError(f"Missing placeholder in context: {e}")
