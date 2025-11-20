"""A simple hello world function for the template."""


def hello_world(name: str = "World") -> str:
    """Return a greeting message.

    Args:
        name: The name to greet. Defaults to "World".

    Returns:
        A greeting string.

    Examples:
        >>> hello_world()
        'Hello, World!'

        >>> hello_world("Python")
        'Hello, Python!'
    """
    return f"Hello, {name}!"
