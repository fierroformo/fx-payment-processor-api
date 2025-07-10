import enum


class Messages(enum.auto):
    INSUFFICIENT_FUNDS: str = "Insufficient funds"
    INVALID_AMOUNT: str = "Invalid amount"
    NEGATIVE_AMOUNT: str = "Negative amount"
    UNKNOWN_CURRENCY: str = "Unknown currency"
