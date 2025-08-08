from flask import Flask, render_template
import requests

app = Flask(__name__)

# Config : à personnaliser selon ton nœud
GETH_RPC = "http://127.0.0.1:8545"
BEACON_API = "http://127.0.0.1:5052"

def check_geth_sync():
    try:
        payload = {"jsonrpc": "2.0", "method": "eth_syncing", "params": [], "id": 1}
        r = requests.post(GETH_RPC, json=payload, timeout=5)
        data = r.json()
        return "En cours de sync" if data["result"] else "Synchronisé ✅"
    except Exception as e:
        return f"Erreur: {e}"

def check_beacon_sync():
    try:
        r = requests.get(f"{BEACON_API}/eth/v1/node/syncing", timeout=5)
        data = r.json()
        return "En cours de sync" if data["data"]["is_syncing"] else "Synchronisé ✅"
    except Exception as e:
        return f"Erreur: {e}"

@app.route("/")
def index():
    geth_status = check_geth_sync()
    beacon_status = check_beacon_sync()
    return render_template("index.html", geth=geth_status, beacon=beacon_status)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
