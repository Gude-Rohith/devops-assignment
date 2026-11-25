
from flask import Flask
import random

app = Flask(__name__)

investment_terms = [
    "Investments",
    "Equity",
    "Stocks",
    "buy-the-dip",
    "Mutual-Funds"
]

@app.route("/api/v1", methods=["GET"])
def get_random_term():
    return random.choice(investment_terms)

@app.route("/health", methods=["GET"])
def health_check():
    return "Healthy", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
