from flask import Blueprint, jsonify, request, redirect, url_for
from io import StringIO
from datetime import datetime

import csv
import logging

from crypto_tracker.utility.crypto_csv_data_utils import (
    load_csv_data,
    load_csv_data_with_csv_pkg,
    concatenate_csv_data_frames,
    union_and_remaining_csv_data,
    upsert_csv_data_with_auto_id,
    save_data_frame_to_csv
)

from crypto_tracker.utility.deposit_data_utils import load_deposit_csv_data, save_deposit_csv_data


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

api_bp = Blueprint("api", __name__)


DATA_CRYPTO_BUY_CSV_FILE = 'data/purchased_cryptos.csv'
DATA_CRYPTO_SOLD_CSV_FILE = 'data/sold_cryptos.csv'
DATA_CRYPTO_BALANCE_CSV_FILE = 'data/wallet_balance.csv'


@api_bp.route("/api/wallet/history")
def get_trade_history():
    df_buy = load_csv_data(DATA_CRYPTO_BUY_CSV_FILE, True)
    df_buy["type"] = "buy"

    df_sell = load_csv_data(DATA_CRYPTO_SOLD_CSV_FILE, True)
    df_sell["type"] = "sell"

    return jsonify(concatenate_csv_data_frames([df_buy, df_sell]))

@api_bp.route("/api/wallet/dashboard")
def get_last_twenty_trades_history():
    df_buy = load_csv_data(DATA_CRYPTO_BUY_CSV_FILE, True)
    df_buy["type"] = "buy"

    df_sell = load_csv_data(DATA_CRYPTO_SOLD_CSV_FILE, True)
    df_sell["type"] = "sell"

    return jsonify(concatenate_csv_data_frames([df_buy, df_sell], max_rows=20))

@api_bp.route("/api/wallet/buy")
def get_buy_cryptos():
    return jsonify(load_csv_data(DATA_CRYPTO_BUY_CSV_FILE))

@api_bp.route("/api/wallet/sold")
def get_sold_cryptos():
    return jsonify(load_csv_data(DATA_CRYPTO_SOLD_CSV_FILE))

@api_bp.route("/api/wallet/balance")
def get_wallet_balance():
    return jsonify(load_csv_data_with_csv_pkg(DATA_CRYPTO_BALANCE_CSV_FILE))

@api_bp.route("/api/wallet/balance/update")
def update_wallet_balance_csv_table() -> None:
    df_balance = union_and_remaining_csv_data([DATA_CRYPTO_BUY_CSV_FILE, DATA_CRYPTO_SOLD_CSV_FILE], True)
    save_data_frame_to_csv(df_balance, 'data/wallet_balance.csv')
    return jsonify({"message": "OK"}), 200

@api_bp.route("/api/wallet/update", methods=["POST"])
def update_crypto():
    try:
        edit_crypto_form = request.form
        date_obj = datetime.strptime(edit_crypto_form.get("cryptoPurchaseDate"), "%Y-%m-%d")
        formatted_date = date_obj.strftime("%d.%m.%Y")
        updated_data = {
            'crypto_alias': edit_crypto_form.get("cryptoAlias"),
            'crypto_name': edit_crypto_form.get("cryptoName"),
            'broker': edit_crypto_form.get("cryptoBroker"),
            'trade_date': formatted_date,
            'trade_price': edit_crypto_form.get("cryptoPurchasePrice"),
            'amount': float(edit_crypto_form.get("cryptoAmount")),
            'total_trade_price': float(edit_crypto_form.get("cryptoTotalPrice")),
            'meme': 1 if edit_crypto_form.get("cryptoMeme") == "on" else 0
        }
        #update_csv_crypto_data(updated_entry)
        upsert_csv_data_with_auto_id(DATA_CRYPTO_BUY_CSV_FILE, {'id': int(edit_crypto_form.get("recordId"))}, updated_data)
        update_wallet_balance_csv_table()
        return redirect(url_for('pages.wallet_balance_page'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        # return render_template("error.html", error=str(e)), 500

@api_bp.route("/api/wallet/add", methods=["POST"])
def add_crypto():
    try:
        add_crypto_form = request.form
        date_obj = datetime.strptime(add_crypto_form.get("cryptoPurchaseDate"), "%Y-%m-%d")
        formatted_date = date_obj.strftime("%d.%m.%Y")
        new_trade = {
            'crypto_alias': add_crypto_form.get("cryptoAlias"),
            'crypto_name': add_crypto_form.get("cryptoName"),
            'broker': add_crypto_form.get("cryptoBroker"),
            'trade_date': formatted_date,
            'trade_price': add_crypto_form.get("cryptoPurchasePrice"),
            'amount': float(add_crypto_form.get("cryptoAmount")),
            'total_trade_price': float(add_crypto_form.get("cryptoTotalPrice")),
            'meme': 1 if add_crypto_form.get("cryptoMeme") == "on" else 0
        }
        logger.info(add_crypto_form.get("BuyOrSell"))
        if add_crypto_form.get("buyOrSell") == 'buy':
            upsert_csv_data_with_auto_id(DATA_CRYPTO_BUY_CSV_FILE, {}, new_trade)
        else:
            upsert_csv_data_with_auto_id(DATA_CRYPTO_SOLD_CSV_FILE,{}, new_trade)
        update_wallet_balance_csv_table()
        return redirect(url_for('pages.wallet_balance_page'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        # return render_template("error.html", error=str(e)), 500


@api_bp.route("/api/deposit/summary")
def deposit_summary_page():
    deposit, summary = load_deposit_csv_data()
    return jsonify(deposit)


@api_bp.route("/api/deposit/add", methods=["POST"])
def add_deposit():
    try:
        add_deposit_form = request.form
        date_obj = datetime.strptime(add_deposit_form.get("depositDate"), "%Y-%m-%d")
        formatted_date = date_obj.strftime("%d.%m.%Y")
        new_entry = {
            "date": formatted_date,
            "broker": add_deposit_form.get("depositBroker"),
            "amount": float(add_deposit_form.get("depositAmount")),
            "method": add_deposit_form.get("depositMethod")
        }

        save_deposit_csv_data(new_entry)
        return redirect(url_for('api.deposit_summary_page'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        # return render_template("error.html", error=str(e)), 500
