"""Configuration module for the trading bot."""
import os
from dotenv import load_dotenv
from bot.exceptions import ConfigurationError

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Enforce Testnet endpoint
BINANCE_FUTURES_TESTNET_URL = "https://testnet.binancefuture.com"

def validate_config() -> None:
    """Validates that all required environment variables are set."""
    if not API_KEY or not API_SECRET:
        raise ConfigurationError(
            "API_KEY and API_SECRET must be set in the .env file."
        )
