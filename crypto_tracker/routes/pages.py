from flask import Blueprint, render_template, request
from datetime import datetime


# Import the helper functions
from crypto_tracker.utility.deposit_data_utils import load_deposit_csv_data
from crypto_tracker.utility.crypto_csv_data_utils import get_csv_data_by_id

pages_bp = Blueprint("pages", __name__)


@pages_bp.route("/")
def index():
    return render_template("index.html", active_page='home')


@pages_bp.route("/page/wallet/history")
def wallet_history_page():
    return render_template("wallet/history.html", active_page='wallet')


@pages_bp.route("/page/wallet/balance")
def wallet_balance_page():
    return render_template("wallet/balance.html", active_page='wallet')


@pages_bp.route("/page/wallet/sold")
def wallet_sold_summary_page():
    return render_template("wallet/sold.html", active_page='wallet')


@pages_bp.route("/page/wallet/add")
def add_to_wallet_page():
    return render_template("wallet/add.html", active_page='crypto-summary')


@pages_bp.route("/page/wallet/edit", methods=["POST"])
def edit_crypto_page():
    update_crypto_form = request.form
    found_crypto = get_csv_data_by_id('data/purchased_cryptos.csv', int(update_crypto_form.get("cryptoRecordId")))
    if found_crypto:
        date_obj = datetime.strptime(found_crypto["trade_date"], "%d.%m.%Y")
        found_crypto["trade_date"] = date_obj.strftime("%Y-%m-%d")
        return render_template(
            "wallet/edit.html",
            active_page='crypto-summary',
            crypto=found_crypto
        )
    else:
        return render_template(
            "wallet/get.html",
            active_page='crypto-summary',
            error=f"Crypto with ID: {update_crypto_form.get('cryptoRecordId')} not found"
        ), 404


@pages_bp.route("/page/wallet/get")
def update_crypto_page():
    return render_template("wallet/get.html", active_page='crypto-summary')


@pages_bp.route("/page/deposit/summary")
def deposit_summary_page():
    all_deposits, summary, summary_by_broker = load_deposit_csv_data()
    return render_template(
        "deposit/summary.html",
        active_page='deposit-summary',
        deposits=all_deposits,
        total_sum=summary
    )


@pages_bp.route("/page/deposit/broker")
def deposit_broker_page():
    all_deposits, summary, summary_by_broker = load_deposit_csv_data()
    return render_template(
        "deposit/broker.html",
        active_page='deposit-summary',
        total_sum=summary,
        summary_by_broker=summary_by_broker
    )


@pages_bp.route("/page/deposit/add")
def add_new_deposit_page():
    return render_template("deposit/add.html", active_page='deposit-summary')


@pages_bp.route("/page/deposit/get")
def update_deposit_page():
    return render_template("deposit/get.html", active_page='deposit-summary')


@pages_bp.route("/page/deposit/edit", methods=["POST"])
def edit_deposit_page():
    update_deposit_form = request.form
    found_deposit = get_csv_data_by_id('data/deposit.csv', int(update_deposit_form.get("depositRecordId")))

    if found_deposit:
        date_obj = datetime.strptime(found_deposit["date"], "%d.%m.%Y")
        found_deposit["date"] = date_obj.strftime("%Y-%m-%d")
        return render_template(
            "deposit/edit.html",
            active_page='deposit-summary',
            deposit=found_deposit
        )
    else:
        return render_template(
            "deposit/get.html",
            active_page='deposit-summary',
            error=f"Deposit with ID: {update_deposit_form.get('depositRecordId')} not found"
        ), 404
