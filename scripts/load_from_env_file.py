import os

from dotenv import dotenv_values, load_dotenv

# Load variables from .env file
load_dotenv()
env_config = dotenv_values()

# Print all env variables names.
print("Loaded env variables:")
for i in env_config.keys() & os.environ.keys():
    print(i)
