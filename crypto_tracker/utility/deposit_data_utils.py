from pathlib import Path
from collections import defaultdict

import json
import csv

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

DATA_DEPOSIT_CSV_FILE = Path("data/deposit.csv")


def load_deposit_csv_data() -> tuple[list[dict], float]:
    """
    load and read deposit from CSV file and return a list of Dictionaries
    with numeric fields correctly converted to float/int.
    """
    if not DATA_DEPOSIT_CSV_FILE.exists():
        return []

    data = []
    summary = 0
    try:
        with DATA_DEPOSIT_CSV_FILE.open(mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                try:
                    amount = round(float(row.get('amount', 0)), 2)
                    row['amount'] = amount
                    summary += amount
                except ValueError:
                    row['amount'] = 0.00

                data.append(row)
    except (csv.Error, UnicodeDecodeError, OSError) as e:
        logger.error(f"Error at reading CSV File: {e}")
        return [], 0

    return data, summary


def save_deposit_csv_data(data: dict[str, str | float | int]) -> None:
    """Save crypto purchases to CSV file."""
    fieldnames = ["date", "amount", "broker", "method"]

    rows: list[dict[str, str]] = []

    if DATA_DEPOSIT_CSV_FILE.exists():
        with DATA_DEPOSIT_CSV_FILE.open(mode="r", newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)

    rows.insert(0, {key: str(data.get(key, "")) for key in fieldnames})

    with DATA_DEPOSIT_CSV_FILE.open("w", newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
