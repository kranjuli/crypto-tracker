from flask import Flask, render_template, jsonify, request, Response
from io import StringIO
import csv

# Import the helper functions
from .data_utils import load_crypto_data, save_crypto_data

app = Flask(__name__)


@app.route("/")
def index():
    # cryptos = load_crypto_data()
    # return render_template("index.html",cryptos=cryptos)
    return render_template("index.html")


@app.route("/add_new_purchased_crypto")
def add_new_purchased_crypto():
    return render_template("add_crypto.html")


@app.route("/api/cryptos")
def get_cryptos():
    return jsonify(load_crypto_data())


@app.route("/api/add", methods=["POST"])
def add_crypto():
    try:
        new_entry = request.get_json(force=True)
        required_fields = {"cryptoName", "purchaseDate", "amount", "totalPriceEUR"}

        if not required_fields.issubset(new_entry):
            return jsonify({"error": "Missing fields"}), 400

        data = load_crypto_data()
        data.append(new_entry)
        save_crypto_data(data)
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/export/csv")
def export_csv():
    data = load_crypto_data()
    output = StringIO()
    fieldnames = ["cryptoName", "purchaseDate", "amount", "totalPriceEUR"]

    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=crypto_purchases.csv"}
    )


# if run with poetry run python crypto_tracker
#if __name__ == "__main__":
#    app.run(host="0.0.0.0", port=8080, debug=True)
