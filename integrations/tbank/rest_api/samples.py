import json
import os

from dotenv import load_dotenv
from tbank_instruments_service import InstrumentsService


def save_json_pretty(data: dict, filename: str):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# Load variables from .env file
load_dotenv()

# Get an environment variable with a default value
token = os.getenv("T_INVEST_API")

with InstrumentsService(
    token=token,
    sandbox=True,
    verify_ssl=False,
) as client:
    bonds = client.bonds()
    shares = client.shares()
    results = client.find_instrument("SBER")
    save_json_pretty(shares, "data/tbank/shares.json")
    print(results)
