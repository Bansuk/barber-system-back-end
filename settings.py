"""
Application settings and environment variable management.

Loads variables from a .env file and exposes them
as typed Python constants. This module should be imported anywhere
configuration values are needed.
"""

import os
from dotenv import load_dotenv

load_dotenv()


def get_env(name: str, default=None, *, required=False, cast=None):
    """
    Helper function to retrieve an environment variable with type coercion.

    Args:
        name (str): Name of the environment variable.
        default (Any): Default value if variable is missing (ignored if required=True).
        required (bool): If True, missing variables raise an error.
        cast (Callable): Optional function to cast the value (e.g. int, bool).

    Returns:
        Any: The environment variable value, optionally cast to a type.

    Raises:
        EnvironmentError: If a required variable is missing.
        ValueError: If casting fails.
    """
    value = os.getenv(name, default)

    if required and value is None:
        raise EnvironmentError(
            f"Missing required environment variable: {name}")

    if cast and value is not None:
        try:
            return cast(value)
        except ValueError as exc:
            raise ValueError(
                f"Failed to cast environment variable '{name}' using {cast}"
            ) from exc

    return value


API_KEY = get_env("API_KEY", required=True)
URL = get_env("URL", required=True)
PRETTIFY_JSON_RESPONSE = get_env("PRETTIFY_JSON_RESPONSE", default=1, cast=int)
