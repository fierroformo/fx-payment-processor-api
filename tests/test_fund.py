from typing import Dict

from app.app import wallet
from app.http_status import HTTPStatus



class TestFundWallet:
    user_id: int = 1
    url: str = f"/wallets/{user_id}/fund"

    @classmethod
    def setup_class(cls):
        wallet.clear()

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
