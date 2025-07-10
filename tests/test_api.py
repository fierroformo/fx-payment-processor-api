from typing import Dict

import pytest

from app.app import app
from app.currencies import USD
from app.http_status import HTTPStatus


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


class TestFundWallet:
    user_id: int = 1
    url: str = f"/wallets/{user_id}/fund"

    def test_fund_wallet(self, client):
        data: Dict = {"currency": "USD", "amount": 1324}
        response = client.post(self.url, json=data)
        assert response.text == "Success"
        assert response.status_code == HTTPStatus.HTTP_201_CREATED

    def test_fund_wallet_unknown_currency(self, client):
        data: Dict = {"currency": "ALE", "amount": 1}
        response = client.post(self.url, json=data)
        assert response.text == "Unknown currency"
        assert response.status_code == HTTPStatus.HTTP_400_BAD_REQUEST

    def test_fund_wallet_negative_amount(self, client):
        data: Dict = {"currency": "USD", "amount": -1}
        response = client.post(self.url, json=data)
        assert response.text == "Negative amount"
        assert response.status_code == HTTPStatus.HTTP_400_BAD_REQUEST

    def test_fund_wallet_invalid_amount(self, client):
        data: Dict = {"currency": "USD", "amount": "one hundred"}
        response = client.post(self.url, json=data)
        assert response.text == "Invalid amount"
        assert response.status_code == HTTPStatus.HTTP_400_BAD_REQUEST


class TestConvertCurrency:
    user_id: int = 1
    url: str = f"/wallets/{user_id}/convert"

    def test_convert_currency(self, client):
        data: Dict = {"from_currency": "USD", "to_currency": "MXN", "amount": 152}
        response = client.post(self.url, json=data)
        expected_amount: float = data.get("amount") * USD
        assert response.json.get("currency") == data.get("to_currency")
        assert response.json.get("amount") == expected_amount
        assert response.status_code == HTTPStatus.HTTP_200_OK

    def test_convert_currency_invalid_currency(self, client):
        data: Dict = {"from_currency": "MXN", "to_currency": "MONATO-COIN", "amount": 10}
        response = client.post(self.url, json=data)
        assert response.text == "Unknown currency"
        assert response.status_code == HTTPStatus.HTTP_400_BAD_REQUEST

    def test_convert_currency_negative_amount(self, client):
        data: Dict = {"from_currency": "USD", "to_currency": "MXN", "amount": -152}
        response = client.post(self.url, json=data)
        assert response.text == "Negative amount"
        assert response.status_code == HTTPStatus.HTTP_400_BAD_REQUEST


class TestWithdrawFunds:
    user_id: int = 1
    url: str = f"/wallets/{user_id}/withdraw"

    def test_withdraw_funds(self, client):
        #
        # Fund account of user
        #
        client.post(f"/wallets/{self.user_id}/fund", data={"currency": "USD", "amount": 95})
        data: Dict = {"currency": "MXN", "amount": 95}
        response = client.post(self.url, data=data)
        print("response", response)
        assert response.json()["data"]["success"] == "true"
        assert response.status_code == HTTPStatus.HTTP_201_CREATED

    def test_withdraw_insufficient_funds(self, client):
        data: Dict = {"currency": "MXN", "amount": 950}
        response = client.post(self.url, data=data)
        assert response.json()["data"]["message"] == "Insufficient funds"
        assert response.status_code == HTTPStatus.HTTP_400_BAD_REQUEST

    def test_withdraw_user_without_funds(self, client):
        user_id: int = 2
        data: Dict = {"currency": "MXN", "amount": 950}
        response = client.post(f"/wallets/{user_id}/withdraw", data=data)
        assert response.json()["data"]["message"] == "Insufficient funds"
        assert response.status_code == HTTPStatus.HTTP_400_BAD_REQUEST


class TestBalance:
    user_id: int = 1
    url: str = f"/wallets/{user_id}/balances"

    def test_balances(self, client):
        amount_mxn: float = 666.50
        amount_usd: float = 152.0
        client.post(
            f"/wallets/{self.user_id}/fund",
            data={"currency": "USD", "amount": amount_mxn}
        )
        client.post(
            f"/wallets/{self.user_id}/fund",
            data={"currency": "USD", "amount": amount_usd}
        )
        response = client.get(self.url)
        assert response.json()["data"]["MXN"] == amount_mxn
        assert response.json()["data"]["USD"] == amount_usd
        assert response.status_code == HTTPStatus.HTTP_200_OK

    def test_user_without_funds(self, client):
        user_id: int = 2
        response = client.get(f"/wallets/{user_id}/balances")
        assert response.json()["data"] == {}
        assert response.status_code == HTTPStatus.HTTP_200_OK
