"""Custom exceptions for the trading bot."""

class BotError(Exception):
    """Base class for all bot exceptions."""
    pass

class ConfigurationError(BotError):
    """Raised when there is an issue with configuration (e.g., missing API keys)."""
    pass

class ValidationError(BotError):
    """Raised when user input validation fails."""
    pass

class BinanceAPIError(BotError):
    """Raised when the Binance API returns an error."""
    pass
