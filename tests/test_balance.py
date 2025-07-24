from http import HTTPStatus

from app.app import wallet


class TestBalance:
    user_id: int = 1
    url: str = f"/wallets/{user_id}/balances"

    @classmethod
    def setup_class(cls):
        wallet.clear()

    def test_balances(self, client):
        amount_mxn: float = 666.50
        amount_usd: float = 152.0
        #
        # Fund account of user
        #
        client.post(
            f"/wallets/{self.user_id}/fund",
            json={"currency": "MXN", "amount": amount_mxn}
        )
        client.post(
            f"/wallets/{self.user_id}/fund",
            json={"currency": "USD", "amount": amount_usd}
        )

        response = client.get(self.url)
        assert response.json.get("MXN") == amount_mxn
        assert response.json.get("USD") == amount_usd
        assert response.status_code == HTTPStatus.OK

    def test_balances_user_empty_funds(self, client):
        user_id: int = 11
        response = client.get(f"/wallets/{user_id}/balances")
        assert response.json == {}
        assert response.status_code == HTTPStatus.OK