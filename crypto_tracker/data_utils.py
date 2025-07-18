from pathlib import Path
import json

DATA_FILE = Path("data/purchased_cryptos.json")


def load_crypto_data() -> list[dict]:
    """Load crypto purchases from JSON file."""
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_crypto_data(data: list[dict]) -> None:
    """Save crypto purchases to JSON file."""
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def filter_by_broker(data: list[dict], broker_name: str) -> list[dict]:
    """filter crypto purchases by broker name."""
    return [entry for entry in data if entry.get("broker") == broker_name]
