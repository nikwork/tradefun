import os


def is_true(env_val: str):
    """Checks if an environment variable value is truthy."""
    if env_val is None:
        return False  # Or your desired default for an unset variable
    return env_val.lower() in ("true", "yes", "on", "1")


def get_bool_env_var(var_name: str, required: bool = True):
    try:
        env_val = os.environ[var_name]
        return is_true(env_val)
    except KeyError:
        if required:
            raise ValueError(f"The '{var_name}' environment variable is not set.")
        return False
