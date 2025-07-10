from typing import Dict

from app.app import wallet
from app.http_status import HTTPStatus
from app.messages import Messages


class TestWithdrawFunds:
    user_id: int = 1
    url: str = f"/wallets/{user_id}/withdraw"

    @classmethod
    def setup_class(cls):
        wallet.clear()

    def test_withdraw_funds(self, client):
        #
        # Fund account of user
        #
        client.post(f"/wallets/{self.user_id}/fund", json={"currency": "USD", "amount": 95})

        data: Dict = {"currency": "USD", "amount": 95}
        response = client.post(self.url, json=data)
        assert response.text == "Success"
        assert response.status_code == HTTPStatus.HTTP_201_CREATED

    def test_withdraw_insufficient_funds(self, client):
        data: Dict = {"currency": "MXN", "amount": 950}
        response = client.post(self.url, json=data)
        assert response.text == Messages.INSUFFICIENT_FUNDS
        assert response.status_code == HTTPStatus.HTTP_400_BAD_REQUEST

    def test_withdraw_user_without_funds(self, client):
        user_id: int = 2
        data: Dict = {"currency": "MXN", "amount": 950}
        response = client.post(f"/wallets/{user_id}/withdraw", json=data)
        assert response.text == Messages.INSUFFICIENT_FUNDS
        assert response.status_code == HTTPStatus.HTTP_400_BAD_REQUEST
