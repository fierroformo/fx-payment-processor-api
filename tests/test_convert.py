from http import HTTPStatus
from typing import Dict

from app.app import wallet
from app.currencies import USD
from app.messages import Messages


class TestConvertCurrency:
    user_id: int = 1
    url: str = f"/wallets/{user_id}/convert"

    @classmethod
    def setup_class(cls):
        wallet.clear()

    def test_convert_currency(self, client):
        #
        # Fund account of user
        #
        data_wallet: Dict = {"currency": "USD", "amount": 3}
        client.post(f"/wallets/{self.user_id}/fund", json=data_wallet)

        data: Dict = {"from_currency": "USD", "to_currency": "MXN", "amount": 1}
        response = client.post(self.url, json=data)
        expected_amount_mxn: float = data.get("amount") * USD
        remaining_usd: float = data_wallet.get("amount") - data.get("amount")
        assert wallet[self.user_id]["MXN"] == expected_amount_mxn
        assert wallet[self.user_id]["USD"] == remaining_usd
        assert response.status_code == HTTPStatus.CREATED

    def test_convert_without_funds(self, client):
        data: Dict = {"from_currency": "USD", "to_currency": "MXN", "amount": 5}
        response = client.post(self.url, json=data)
        assert response.text == Messages.INSUFFICIENT_FUNDS
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_convert_currency_invalid_currency(self, client):
        data: Dict = {"from_currency": "MXN", "to_currency": "MONATO-COIN", "amount": 10}
        response = client.post(self.url, json=data)
        assert response.text == Messages.UNKNOWN_CURRENCY
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_convert_currency_negative_amount(self, client):
        data: Dict = {"from_currency": "USD", "to_currency": "MXN", "amount": -152}
        response = client.post(self.url, json=data)
        assert response.text == Messages.NEGATIVE_AMOUNT
        assert response.status_code == HTTPStatus.BAD_REQUEST
