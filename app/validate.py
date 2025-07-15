from typing import Dict, List, Optional, Tuple
from http import HTTPStatus

from app.messages import Messages


AVAILABLE_CURRENCIES: List = ["MXN", "USD"]


class ValidateFund:
    @staticmethod
    def validate(currency: str, amount: float) -> Optional[Tuple]:
        if not currency in AVAILABLE_CURRENCIES:
            return Messages.UNKNOWN_CURRENCY, HTTPStatus.BAD_REQUEST
        elif isinstance(amount, str):
            return Messages.INVALID_AMOUNT, HTTPStatus.BAD_REQUEST
        elif amount < 0:
            return Messages.NEGATIVE_AMOUNT, HTTPStatus.BAD_REQUEST


class ValidateConvert:
    @staticmethod
    def validate(
        wallet_user: Dict, to_currency: str, from_currency: str, amount: float
    ) -> Optional[Tuple]:
        if not to_currency in AVAILABLE_CURRENCIES or not from_currency in AVAILABLE_CURRENCIES:
            return Messages.UNKNOWN_CURRENCY, HTTPStatus.BAD_REQUEST
        elif isinstance(amount, str):
            return Messages.INVALID_AMOUNT, HTTPStatus.BAD_REQUEST
        elif amount < 0:
            return Messages.NEGATIVE_AMOUNT, HTTPStatus.BAD_REQUEST
        elif amount > wallet_user[from_currency]:
            return Messages.INSUFFICIENT_FUNDS, HTTPStatus.BAD_REQUEST


class ValidateWithdraw:
    @staticmethod
    def validate(wallet_user: Dict, currency: str, amount: float) -> Optional[Tuple]:
        if not currency in AVAILABLE_CURRENCIES:
            return Messages.UNKNOWN_CURRENCY ,HTTPStatus.BAD_REQUEST
        elif isinstance(amount, str):
            return Messages.INVALID_AMOUNT, HTTPStatus.BAD_REQUEST
        elif amount < 0:
            return Messages.NEGATIVE_AMOUNT, HTTPStatus.BAD_REQUEST
        elif not wallet_user or amount > wallet_user[currency]:
            return Messages.INSUFFICIENT_FUNDS, HTTPStatus.BAD_REQUEST
