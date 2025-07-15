import os

USD: float = os.environ.get("VALUE_CURRENCY_USD", 18.7)
MXN: float = os.environ.get("VALUE_CURRENCY_MXN", 0.053)

AVAILABLE_CURRENCIES = (
    os.environ.get("AVAILABLE_CURRENCIES", "USD,MXN").split(",")
)
