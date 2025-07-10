from typing import List, Optional, Tuple

from app.http_status import HTTPStatus


AVAILABLE_CURRENCIES: List = ["MXN", "USD"]


class ValidateFunds:
    @staticmethod
    def validate(currency: str, amount: float) -> Optional[Tuple]:
        if not currency in AVAILABLE_CURRENCIES:
            return "Unknown currency" ,HTTPStatus.HTTP_400_BAD_REQUEST
        elif isinstance(amount, str):
            return "Invalid amount", HTTPStatus.HTTP_400_BAD_REQUEST
        elif amount < 0:
            return "Negative amount", HTTPStatus.HTTP_400_BAD_REQUEST


class ValidateConvert:
    @staticmethod
    def validate(to_currency: str, from_currency: str, amount: float) -> Optional[Tuple]:
        if not to_currency in AVAILABLE_CURRENCIES or not from_currency in AVAILABLE_CURRENCIES:
            return "Unknown currency", HTTPStatus.HTTP_400_BAD_REQUEST
        elif isinstance(amount, str):
            return "Invalid amount", HTTPStatus.HTTP_400_BAD_REQUEST
        elif amount < 0:
            return "Negative amount", HTTPStatus.HTTP_400_BAD_REQUEST
