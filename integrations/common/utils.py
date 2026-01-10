"""Environment variable utilities for bank integrations."""

import os


def is_true(env_val: str | None) -> bool:
    """Check if environment variable value is truthy (true/yes/on/1, case-insensitive)."""
    if env_val is None:
        return False
    return env_val.lower() in ("true", "yes", "on", "1")


def get_bool_env_var(var_name: str, required: bool = True) -> bool:
    """
    Get boolean value from environment variable.

    Args:
        var_name: Name of the environment variable
        required: If True, raise ValueError when variable is missing

    Returns:
        Boolean value of the environment variable, or False if missing and not required

    Raises:
        ValueError: If variable is not set and required=True
    """
    try:
        env_val = os.environ[var_name]
        return is_true(env_val)
    except KeyError:
        if required:
            raise ValueError(f"The '{var_name}' environment variable is not set.")
        return False
