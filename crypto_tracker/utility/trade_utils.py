import pandas as pd
import logging
import csv
from pathlib import Path


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def load_csv_data(csv_file: str, data_frame: bool = False) -> pd.DataFrame | list[dict]:
    """Load all data from CSV."""
    try:
        df = pd.read_csv(
            csv_file,
            parse_dates=['trade_date'],
            dayfirst=True,
            dtype={
                "amount": float,
                "trade_price": float,
                "total_trade_price": float
            }
        )
        if df.empty:
            logger.warning(f"CSV file '{csv_file}' contains no data.")
            if data_frame:
                return pd.DataFrame()
            else:
                return []

        df = df.sort_values("trade_date", ascending=False)
        df["trade_date"] =  df["trade_date"].dt.strftime('%Y-%m-%d')

        if data_frame:
            return df
        else:
            return df.to_dict(orient="records")
    except FileNotFoundError:
        logger.error(f"File CSV not found: {csv_file}")
    except Exception as e:
        logger.error(f"Error at loading CSV: {e}")
    return []


def load_all_trades_cached(
    sources: list[tuple[str, str]]
) -> pd.DataFrame:
    """Load and cache merged trade CSVs. Reload only if CSV files changed."""
    global _trade_cache
    global _trade_cache_timestamps
    data_frames = []
    for buy_csv, sold_csv in sources:
        df_buy = load_csv_data(buy_csv, True)
        df_sold = load_csv_data(sold_csv, True)

        if not df_buy.empty:
            df_buy["type"] = "buy"
            data_frames.append(df_buy)

        if not df_sold.empty:
            df_sold["type"] = "sell"
            data_frames.append(df_sold)

    if not data_frames:
        return pd.DataFrame()

    all_trades_df = pd.concat(data_frames, ignore_index=True).sort_values(by="trade_date", ascending=False)
    return all_trades_df


def paginate_dataframe(
    df: pd.DataFrame,
    page: int = 1,
    page_size: int = 25
) -> tuple[pd.DataFrame, dict]:
    """Paginate a DataFrame."""
    total_items = len(df)
    total_pages = (total_items + page_size - 1) // page_size

    if page < 1 or page > total_pages:
        logger.warning(f"Requested page {page} is out of range. Total pages: {total_pages}.")
        return pd.DataFrame(), {
            "total_pages": total_pages,
            "current_page": page
        }

    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_df = df.iloc[start_idx:end_idx]

    meta = {
        "current_page": page,
        "page_size": page_size,
        "total_items": total_items,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_previous": page > 1
    }

    return paginated_df, meta


def load_trades_paginated(
    sources: list[tuple[str, str]],
    page: int = 1,
    page_size: int = 25
) -> dict:
    """Load paginated trade data from multiple CSV sources."""
    all_trades_df = load_all_trades_cached(sources)

    if all_trades_df.empty:
        return {
            "trades": [],
            "meta": {}
        }

    page_df, meta = paginate_dataframe(
        all_trades_df,
        page=page,
        page_size=page_size
    )

    return {
        "trades": page_df.to_dict(orient="records"),
        "meta": meta
    }


def load_all_trades(
    buy_csv: str,
    sold_csv: str,
    data_frame: bool = True
) -> pd.DataFrame | list[dict]:
    """Load and merge all trade data from buy and sold CSV files."""
    df_buy = load_csv_data(buy_csv, True)
    df_sold = load_csv_data(sold_csv, True)

    if df_buy.empty and df_sold.empty:
        return pd.DataFrame()


    try:
        df_buy = pd.read_csv(
            buy_csv,
            parse_dates=['trade_date'],
            dayfirst=True,
            dtype={
                "amount": float,
                "trade_price": float,
                "total_trade_price": float
            }
        )
        df_buy["type"] = "buy"

        df_sold = pd.read_csv(
            sold_csv,
            parse_dates=['trade_date'],
            dayfirst=True,
            dtype={
                "amount": float,
                "trade_price": float,
                "total_trade_price": float
            }
        )
        df_sold["type"] = "sell"

        all_trades_df = pd.concat([df_buy, df_sold], ignore_index=True).sort_values(by="trade_date", ascending=False)

        if data_frame:
            return all_trades_df
        else:
            return all_trades_df.to_dict(orient="records")
    except FileNotFoundError as e:
        logger.error(f"File CSV not found: {e}")
    except Exception as e:
        logger.error(f"Error at loading CSV: {e}")
    return []
