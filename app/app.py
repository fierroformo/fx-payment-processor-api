from typing import Dict, List

from flask import Flask, request

from app.currencies import MXN, USD
from app.http_status import HTTPStatus


app = Flask(__name__)
wallet: Dict = {}
AVAILABLE_CURRENCIES: List = ["MXN", "USD"]


@app.route("/wallets/<int:user_id>/fund", methods=("POST",))
def fund(user_id: int):
    currency: str = request.get_json().get("currency")
    amount: float = request.get_json().get("amount")

    if not currency in AVAILABLE_CURRENCIES:
        return "Unknown currency", HTTPStatus.HTTP_400_BAD_REQUEST
    elif isinstance(amount, str):
        return "Invalid amount", HTTPStatus.HTTP_400_BAD_REQUEST
    elif amount < 0:
        return "Negative amount", HTTPStatus.HTTP_400_BAD_REQUEST

    if not user_id in wallet:
        wallet[user_id] = {"MXN": 0, "USD": 0}

    wallet[user_id][currency] += amount

    return "Success", HTTPStatus.HTTP_201_CREATED


@app.route("/wallets/<int:_user_id>/convert", methods=("POST",))
def convert(_user_id: int):
    to_currency: str = request.get_json().get("to_currency")
    from_currency: str = request.get_json().get("from_currency")
    amount: float = request.get_json().get("amount")

    if not to_currency in AVAILABLE_CURRENCIES or not from_currency in AVAILABLE_CURRENCIES:
        return "Unknown currency", HTTPStatus.HTTP_400_BAD_REQUEST
    elif isinstance(amount, str):
        return "Invalid amount", HTTPStatus.HTTP_400_BAD_REQUEST
    elif amount < 0:
        return "Negative amount", HTTPStatus.HTTP_400_BAD_REQUEST

    result: Dict = {
        "currency": to_currency,
        "amount": amount * USD if to_currency == "MXN" else amount * MXN
    }

    return result, HTTPStatus.HTTP_200_OK


@app.route("/wallets/<int:user_id>/withdraw", methods=("POST",))
def withdraw(user_id: int):
    currency: str = request.get_json().get("currency")
    amount: float = request.get_json().get("amount")

    if not currency in AVAILABLE_CURRENCIES:
        return "Unknown currency", HTTPStatus.HTTP_400_BAD_REQUEST
    elif isinstance(amount, str):
        return "Invalid amount", HTTPStatus.HTTP_400_BAD_REQUEST
    elif amount < 0:
        return "Negative amount", HTTPStatus.HTTP_400_BAD_REQUEST

    if not user_id in wallet or amount > wallet[user_id][currency]:
        return "Insufficient funds", HTTPStatus.HTTP_400_BAD_REQUEST

    wallet[user_id][currency] -= amount

    return "Success", HTTPStatus.HTTP_201_CREATED


@app.route("/wallets/<int:user_id>/balances", methods=("GET",))
def balances(user_id: int):
    return wallet.get(user_id, {}), HTTPStatus.HTTP_200_OK


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
