import json
import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template
import requests

load_dotenv()

app = Flask(__name__)

BTC_ADDRESS = os.environ.get("BTC_ADDRESS", "YOUR_ADDRESS")

CKPOOL_URL = f"https://solo.ckpool.org/users/{BTC_ADDRESS}"
PUBLICPOOL_URL = f"https://public-pool.io:40557/api/client/{BTC_ADDRESS}"
PUBLICPOOL_NETWORK_URL = "https://public-pool.io:40557/api/network"


def fetch_ckpool():
    """Fetch CKPool data. Handles NDJSON (multiple JSON objects concatenated) by parsing the first."""
    try:
        resp = requests.get(CKPOOL_URL, timeout=10)
        resp.raise_for_status()
        text = resp.text.strip()
        # Try parsing the whole response first (works for pretty-printed JSON)
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        # Fallback: CKPool may return NDJSON — multiple JSON objects on separate lines
        # Find the first complete JSON object by looking for matching braces
        depth = 0
        start = None
        for i, ch in enumerate(text):
            if ch == '{':
                if depth == 0:
                    start = i
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0 and start is not None:
                    return json.loads(text[start:i + 1])
        return {"error": "Empty response from CKPool"}
    except requests.RequestException as e:
        return {"error": f"CKPool unreachable: {e}"}
    except json.JSONDecodeError as e:
        return {"error": f"CKPool bad JSON: {e}"}


def fetch_publicpool():
    """Fetch Public Pool client data."""
    try:
        resp = requests.get(PUBLICPOOL_URL, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        return {"error": f"Public Pool unreachable: {e}"}


def fetch_network():
    """Fetch Bitcoin network info from Public Pool."""
    try:
        resp = requests.get(PUBLICPOOL_NETWORK_URL, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        return {"error": f"Network info unreachable: {e}"}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/lab")
def lab():
    return render_template("lab.html")


@app.route("/api/ckpool")
def api_ckpool():
    return jsonify(fetch_ckpool())


@app.route("/api/publicpool")
def api_publicpool():
    return jsonify(fetch_publicpool())


@app.route("/api/network")
def api_network():
    return jsonify(fetch_network())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
