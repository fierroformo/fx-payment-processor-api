from http import HTTPStatus
from typing import Dict, Optional, Tuple

from flask import Flask, request

from app.currencies import MXN, USD
from app.validate import ValidateConvert, ValidateFund, ValidateWithdraw


app = Flask(__name__)
wallet: Dict = {}


@app.route("/wallets/<int:user_id>/fund", methods=("POST",))
def fund(user_id: int):
    currency: str = request.get_json().get("currency")
    amount: float = request.get_json().get("amount")
    result: Optional[Tuple] = ValidateFund.validate(currency, amount)

    if result: return result

    if not user_id in wallet:
        wallet[user_id] = {"MXN": 0, "USD": 0}

    wallet[user_id][currency] += amount

    return "Success", HTTPStatus.CREATED


@app.route("/wallets/<int:user_id>/convert", methods=("POST",))
def convert(user_id: int):
    to_currency: str = request.get_json().get("to_currency")
    from_currency: str = request.get_json().get("from_currency")
    amount: float = request.get_json().get("amount")
    result: Optional[Tuple] = ValidateConvert.validate(
        wallet[user_id], to_currency, from_currency, amount
    )

    if result: return result

    wallet[user_id][from_currency] -= amount
    wallet[user_id][to_currency] += amount * USD if to_currency == "MXN" else amount * MXN
    result: Dict = {
        "currency": to_currency,
        "amount": amount * USD if to_currency == "MXN" else amount * MXN
    }

    return wallet[user_id], HTTPStatus.CREATED


@app.route("/wallets/<int:user_id>/withdraw", methods=("POST",))
def withdraw(user_id: int):
    currency: str = request.get_json().get("currency")
    amount: float = request.get_json().get("amount")
    result: Optional[Tuple] = ValidateWithdraw.validate(
        wallet.get(user_id, {}), currency, amount
    )

    if result: return result

    wallet[user_id][currency] -= amount

    return "Success", HTTPStatus.CREATED


@app.route("/wallets/<int:user_id>/balances", methods=("GET",))
def balances(user_id: int):
    return wallet.get(user_id, {}), HTTPStatus.OK


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
