"""Logging configuration for the trading bot."""
import logging
import os

def setup_logger() -> logging.Logger:
    """Configures and returns the application logger."""
    os.makedirs("logs", exist_ok=True)
    
    logger = logging.getLogger("trading_bot")
    logger.setLevel(logging.DEBUG)

    # File handler for detailed logging
    file_handler = logging.FileHandler("logs/app.log")
    file_handler.setLevel(logging.DEBUG)

    # Console handler for CLI output (warnings and above, as we use rich for normal output)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)

    # Formatting: Timestamp - Name - Level - Message
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Avoid duplicate handlers if setup_logger is called multiple times
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

logger = setup_logger()