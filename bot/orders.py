"""Business logic for placing orders."""
from typing import Dict, Any
from binance.exceptions import BinanceAPIException, BinanceRequestException
from bot.client import get_binance_client
from bot.validators import validate_order_input
from bot.logging_config import logger
from bot.exceptions import BinanceAPIError, BotError

def place_order(symbol: str, side: str, order_type: str, quantity: float, price: float = None) -> Dict[str, Any]:
    """
    Places a MARKET or LIMIT order on the Binance Futures Testnet.
    """
    # 1. Validate input
    validate_order_input(symbol, side, order_type, quantity, price)
    
    # 2. Get client
    client = get_binance_client()
    
    # 2.5 Determine position mode to avoid -4061 errors
    try:
        position_mode = client.futures_get_position_mode()
        is_hedge_mode = position_mode.get('dualSidePosition', False)
    except Exception as e:
        logger.warning(f"Could not get position mode: {e}")
        is_hedge_mode = False

    # 3. Prepare order parameters
    params = {
        "symbol": symbol.upper(),
        "side": side.upper(),
        "type": order_type.upper(),
        "quantity": quantity,
    }
    
    if is_hedge_mode:
        params["positionSide"] = "LONG" if side.upper() == "BUY" else "SHORT"
    else:
        params["positionSide"] = "BOTH"
    
    if order_type.upper() == "LIMIT":
        params["price"] = price
        params["timeInForce"] = "GTC"  # Good Till Cancelled is required for LIMIT
        
    logger.info(f"API Endpoint: {client.FUTURES_URL}")
    logger.info(f"Preparing to send order request payload: {params}")
    
    try:
        # 4. Execute order on futures testnet
        response = client.futures_create_order(**params)
        logger.info(f"Order successful. Response payload: {response}")
        return response
        
    except BinanceAPIException as e:
        logger.error(f"Binance API Exception occurred: {e}", exc_info=True)
        raise BinanceAPIError(f"Binance API Error: {e.message} (Code: {e.code})")
    except BinanceRequestException as e:
        logger.error(f"Binance Request Exception occurred: {e}", exc_info=True)
        raise BotError(f"Network error communicating with Binance: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during order placement: {e}", exc_info=True)
        raise BotError(f"Unexpected error: {e}")

def parse_order_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """Parses the raw Binance API response into a structured format for display."""
    return {
        "symbol": response.get("symbol", "N/A"),
        "side": response.get("side", "N/A"),
        "type": response.get("type", "N/A"),
        "quantity": float(response.get("origQty", 0.0)),
        "price": float(response.get("price", 0.0)) if response.get("price") else None,
        "order_id": response.get("orderId", "N/A"),
        "status": response.get("status", "N/A"),
        "executed_qty": float(response.get("executedQty", 0.0)),
        "avg_price": float(response.get("avgPrice", 0.0)) if "avgPrice" in response else None,
    }
