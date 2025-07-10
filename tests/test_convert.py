from typing import Dict

from app.currencies import USD
from app.http_status import HTTPStatus


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
