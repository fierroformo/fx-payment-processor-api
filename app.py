from typing import Dict, List

from flask import Flask, request



app = Flask(__name__)
wallet: Dict = {}
AVAILABLE_CURRENCIES: List = ["MXN", "USD"]


@app.route("/wallets/<int:user_id>/fund", methods=("POST",))
def fund_wallet(user_id: int):
    data: Dict = request.get_json()

    if not data.get("currency") in AVAILABLE_CURRENCIES:
        return "Unknown currency", 400
    elif isinstance(data.get("amount"), str):
        return "Invalid amount", 400
    elif data.get("amount") < 0:
        return "Negative amount", 400

    if user_id in wallet:
        wallet[user_id]["funds"].append(request.get_json())
    else:
        wallet[user_id] = {"funds": [request.get_json()]}

    return "Success", 201

@app.route("/wallets/<int:user_id>/balances", methods=("GET",))
def balances(user_id: int):
    return wallet.get(user_id, {}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
