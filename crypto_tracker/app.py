from flask import Flask, jsonify
from crypto_tracker.routes.pages import pages_bp
from crypto_tracker.routes.api import api_bp

import logging


app = Flask(__name__)
app.register_blueprint(pages_bp)
app.register_blueprint(api_bp)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# if run with poetry run python crypto_tracker
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
