"""Binance API client wrapper."""
import time
from binance.client import Client
from bot.config import API_KEY, API_SECRET, BINANCE_FUTURES_TESTNET_URL
from bot.exceptions import ConfigurationError
from bot.logging_config import logger

def get_binance_client() -> Client:
    """
    Initializes and returns the Binance client, strictly enforcing the Testnet endpoint.
    """
    from bot.config import validate_config
    validate_config()
    
    try:
        # Initialize client with testnet=True
        client = Client(API_KEY, API_SECRET, testnet=True)
        # Ensure futures requests go to the testnet URL
        client.FUTURES_URL = BINANCE_FUTURES_TESTNET_URL
        
        # Sync time offset to avoid -1021 errors
        try:
            server_time = client.futures_time()['serverTime']
            local_time = int(time.time() * 1000)
            client.timestamp_offset = server_time - local_time
        except Exception as e:
            logger.warning(f"Could not sync time with Binance: {e}")
        
        return client
    except Exception as e:
        logger.error(f"Failed to initialize Binance client: {e}", exc_info=True)
        raise ConfigurationError(f"Failed to initialize Binance client: {e}")