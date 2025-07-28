import pandas as pd
import logging
import csv
from pathlib import Path


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def load_csv_data(csv_file: str, data_frame: bool = False) -> pd.DataFrame | list[dict]:
    """Load crypto data from CSV."""
    try:
        data_frame_cryptos = pd.read_csv(
            csv_file,
            parse_dates=['trade_date'],
            dayfirst=True,
            dtype={
                "amount": float,
                "trade_price": float,
                "total_trade_price": float
            }
        )
        if data_frame_cryptos.empty:
            logger.warning(f"CSV file '{csv_file}' contains no data.")
            if data_frame:
                return pd.DataFrame()
            else:
                return []

        data_frame_cryptos["trade_date"] =  data_frame_cryptos["trade_date"].dt.strftime('%Y-%m-%d')

        if data_frame:
            return data_frame_cryptos
        else:
            return data_frame_cryptos.to_dict(orient="records")
    except FileNotFoundError:
        logger.error(f"File CSV not found: {csv_file}")
    except Exception as e:
        logger.error(f"Error at loading CSV: {e}")
    return []


def concatenate_csv_data_frames(data_frame_list: list[pd.DataFrame], data_frame: bool = False, max_rows: int | None = None) -> pd.DataFrame | list[dict]:
    "concatenate csv data frame."
    concatenated_data_frames = pd.concat(data_frame_list, ignore_index=True).sort_values(by="trade_date",ascending=False)
    if max_rows is not None:
        concatenated_data_frames = concatenated_data_frames.head(max_rows)

    if data_frame:
        return concatenated_data_frames
    else:
        return concatenated_data_frames.to_dict(orient="records")


def union_and_remaining_csv_data(csv_file_list: list[str], data_frame: bool = False) -> pd.DataFrame | list[dict]:
    "union and remaining csv data frame."
    data_frame_cryptos_buy = load_csv_data(csv_file_list[0], True)
    data_frame_cryptos_sold = load_csv_data(csv_file_list[1], True)

    # Check empty DataFrames
    if data_frame_cryptos_buy is None or data_frame_cryptos_buy.empty:
        data_frame_cryptos_buy = pd.DataFrame(columns=['crypto_alias', 'amount', 'crypto_name'])
    if data_frame_cryptos_sold is None or data_frame_cryptos_sold.empty:
        data_frame_cryptos_sold = pd.DataFrame(columns=['crypto_alias', 'amount'])

    # grouping
    data_frame_sum_buy = (
        data_frame_cryptos_buy.groupby('crypto_alias')['amount']
        .sum()
        .reset_index()
        .rename(columns={"amount": "amount_buy"})
    )

    data_frame_sum_sold = (
        data_frame_cryptos_sold.groupby('crypto_alias')['amount']
        .sum()
        .reset_index()
        .rename(columns={"amount": "amount_sold"})
    )

    result = pd.merge(data_frame_sum_buy, data_frame_sum_sold, on="crypto_alias", how="outer").fillna(0)
    result["remaining_amount"] = result["amount_buy"] - result["amount_sold"]

    name_map = data_frame_cryptos_buy[["crypto_alias", "crypto_name"]].drop_duplicates()
    result = pd.merge(result, name_map, on="crypto_alias", how="left")
    
    if data_frame:
        return result
    else:
        return result.to_dict(orient="records")


def save_data_frame_to_csv(data_frame: pd.DataFrame, save_path: str | None = None) -> None:
    """Save data to csv file"""
    if save_path is not None:
        data_frame.to_csv(save_path, index=False)
    else:
        logger.error("empty save path")


def upsert_csv_data_with_auto_id(csv_file: str, match_criteria: dict, new_values: dict):
    """
    Update a row in CSV file based on match_criteria or insert new row.
    """
    try:
        df = pd.read_csv(csv_file, dayfirst=True)
    except FileNotFoundError:
        df = pd.DataFrame(columns=[
            "id", "crypto_alias", "crypto_name", "broker",
            "trade_date", "trade_price", "amount",
            "total_trade_price", "meme"
        ])

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
        if "id" in df.columns and not df.empty:
            next_id = int(df["id"].max()) + 1
        else:
            next_id = 1

        # insert new data
        new_entry = new_values.copy()
        new_entry["id"] = next_id
        for col in df.columns:
            if col not in new_entry:
                new_entry[col] = None

        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)

    # save in CSV
    df.to_csv(csv_file, index=False)


def get_csv_data_by_id(csv_file: str, data_id: int, data_frame: bool = False) -> pd.DataFrame: 
    """Get a record in CSV by id"""
    try:
        df: pd.DataFrame = pd.read_csv(csv_file)
    except (FileNotFoundError, pd.errors.ParserError) as e:
        logger.error(f"Error at loading the CSV file: {e}")
        return None
    record: pd.DataFrame = df[df['id'] == data_id]
    if record.empty:
        return None
    
    return record if data_frame else record.iloc[0].to_dict()


def load_csv_data_with_csv_pkg(csv_file_path: str) -> list[dict]:
    """
    load data from CSV file with csv package and return a list of Dictionaries
    with numeric fields correctly converted to float/int.
    """
    csv_file = Path(csv_file_path)
    if not csv_file.exists():
        return []

    try:
        with csv_file.open(mode='r', encoding='utf-8') as csvfile:
            return list(csv.DictReader(csvfile))
    except (csv.Error, UnicodeDecodeError, OSError) as e:
        logger.error(f"Error at reading CSV File: {e}")
        return []
