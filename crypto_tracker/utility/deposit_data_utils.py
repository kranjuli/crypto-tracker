import pandas as pd

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
    broker_sums = defaultdict(float)
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
                broker = row.get('broker', 'Unknown').strip()
                broker_sums[broker] += amount
                data.append(row)
    except (csv.Error, UnicodeDecodeError, OSError) as e:
        logger.error(f"Error at reading CSV File: {e}")
        return [], 0, []

    # filter by broker_sums and sort descending
    summary_by_broker = [
        {"broker": broker, "amount": round(amount, 2)}
        for broker, amount in sorted(broker_sums.items(), key=lambda x: x[1], reverse=True)
    ]

    return data, summary, summary_by_broker


def save_deposit_csv_data(data: dict[str, str | float | int]) -> None:
    """
    Save crypto purchases to CSV file.
    """
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


def upsert_deposit_csv_data_with_auto_id(csv_file: str, match_criteria: dict, new_values: dict):
    """
    Update a row in CSV file based on match_criteria or insert new row.
    """
    try:
        df = pd.read_csv(csv_file, dayfirst=True)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["id", "date", "amount", "broker", "method"])

    expected_cols = ["id", "date", "amount", "broker", "method"]
    for col in expected_cols:
    	if col not in df.columns:
            df[col] = None
    df = df[expected_cols]

    df["id"] = pd.to_numeric(df["id"], errors="coerce")

    # Check if data already exists
    if not df.empty and match_criteria:
        mask = pd.Series([True] * len(df))
        for key, value in match_criteria.items():
            mask &= df[key] == value
    else:
        mask = pd.Series([False] * len(df))

    if mask.any():
        # update
        for column, value in new_values.items():
            df.loc[mask, column] = value
    else:
        # generate new ID
        if df["id"].notna().any:
            next_id = int(df["id"].max()) + 1
        else:
            next_id = 1

        # insert new data
        new_entry = new_values.copy()
        new_entry["id"] = next_id

	# fill missing columns
        for col in df.columns:
            if col not in new_entry:
                new_entry[col] = None

        df = pd.concat([pd.DataFrame([new_entry]), df], ignore_index=True)

    # save in CSV
    df.to_csv(csv_file, index=False)
