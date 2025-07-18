# 🧮 Crypto Portfolio Tracker (Raspberry Pi – Local Web App)

A lightweight, local web tool for managing and viewing your personal cryptocurrency purchases. Built with Python (Flask) and vanilla HTML/JS, it runs entirely on a Raspberry Pi with no internet login, no external backend, and no cloud required.

## ✅ Features

* 📄 Displays crypto purchases from a local JSON file
* 📈 Fetches current prices using the CoinGecko API
* 💰 Calculates current value and profit/loss in EUR
* 📝 Form to add new purchases
* 📤 One-click export of your data as a CSV file
* 📱 Responsive mobile-friendly design (no framework needed)

## 🧰 Tech Stack

* Python 3
* Flask (lightweight web server)
* HTML5 + JavaScript (vanilla)
* CoinGecko Public API (no auth required)
* No frontend dependencies (no React/Vue/Bootstrap)

## Project Structure

````shell
crypto-tracker/
├── crypto_tracker/
│   ├── app.py                  # Flask web server (only Routing + API)
│   ├── data_utils.py           # Helper functions for JSON data
├── templates/
│   └── index.html              # Web interface
├── static/
│   ├── css/
│   │   └── style.css           # Responsive CSS styles
│   └── js/
│    └── script.js               # Frontend logic (table, prices, API calls)
├── data/
│   └── purchased_cryptos.json  # Purchased cryptos data in json
````

## 🚀 How to Run

1. Install Python dependencies
    ````shell
    poetry install
    poetry shell
    ````
2. Start the webserver
    ````shell
    poetry run python crypto-cracker/app.py
   # with gunicorm
   poetry run gunicorn crypto_tracker.app:app --bind 0.0.0.0:8000
    ````
3. Open the in your browser

   Visit: http://<your-raspberry-pi-ip>:8080

## 📝 Adding New Purchases

Use the form at the top of the page to add new purchases.

Fields:
* Crypto name (e.g., bitcoin, ethereum) → must match CoinGecko ID
* Purchase date
* Amount
* Total price in EUR

Your data is saved directly to purchased_cryptos.json.

## 📤 Export to CSV

Click on “📤 Export as CSV” to download your purchase data as a CSV file – ready to import into Excel or for backup.

## 📚 JSON Format

Example of `data/purchased_cryptos.json`:

````json
[
  {
    "cryptoName": "bitcoin",
    "purchaseDate": "2024-01-15",
    "amount": 0.5,
    "totalPriceEUR": 15000
  },
  {
    "cryptoName": "ethereum",
    "purchaseDate": "2024-02-20",
    "amount": 2,
    "totalPriceEUR": 4000
  }
]
````

Make sure the cryptoName matches the official CoinGecko IDs.

## 🔗 CoinGecko API Usage
To fetch live prices, this tool uses CoinGecko’s free public API:

````shell
https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=eur
````

No API Key or login is required

## 📱 Responsive Design

The web interface is fully responsive:
* Looks great on desktop, tablets, and phones
* Table data collapses into blocks on small screens
* Usable with touch input

## ⚠ Notes

* All data is stored locally on your Raspberry Pi
* The CoinGecko API does not transmit any private data
* You should back up your purchased_cryptos.json manually

# 🚀 Deploying Flask + Poetry + Gunicorn on Raspberry Pi

## ✅ Prerequisites

- Raspberry Pi with Python 3 and Git installed
- Your Flask app uses Poetry for dependency management

## 📦 1. Transfer the project to the Pi

Clone from Git or copy via `scp`:

```shell
git clone <your-repo-url>
cd crypto-tracker
```

## 🧪 2. Install Poetry

```shell
curl -sSL https://install.python-poetry.org | python3 -
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc  # or ~/.bashrc
source ~/.zshrc  # or source ~/.bashrc
```

## 📂 3. Install dependencies

````shell
cd crypto-tracker
poetry install
````

## 🔥 4. Run app with Gunicorn

Make sure your app is in crypto_tracker/app.py with app = Flask(__name__).

```shell
poetry run gunicorn crypto_tracker.app:app --bind 0.0.0.0:8000
```

Access it from your browser via http://<PI-IP>:8000

## ⚙ 5. (Optional) Set up systemd service

* Create `/etc/systemd/system/cryptoapp.service`
* Copy content of file from folder `systemd_services/cryptocapp.service` and insert into.
* Enable and start service:
   ```shell
   sudo systemctl daemon-reload
   sudo systemctl enable cryptoapp
   sudo systemctl start cryptoapp
   ```
Now your app is running continuously and accessible from your local network!
