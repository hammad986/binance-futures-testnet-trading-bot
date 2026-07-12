"""Input validation logic for the trading bot."""
from bot.exceptions import ValidationError

def validate_order_input(symbol: str, side: str, order_type: str, quantity: float, price: float = None) -> None:
    """
    Validates order inputs based on the following rules:
    - Symbol cannot be empty
    - Quantity > 0
    - LIMIT orders require price
    - MARKET orders must not require price
    - Side must be BUY or SELL
    - Type must be MARKET or LIMIT
    """
    if not symbol or not str(symbol).strip():
        raise ValidationError("Symbol cannot be empty.")
    
    if side not in ["BUY", "SELL"]:
        raise ValidationError(f"Invalid side: '{side}'. Must be 'BUY' or 'SELL'.")
        
    if order_type not in ["MARKET", "LIMIT"]:
        raise ValidationError(f"Invalid order type: '{order_type}'. Must be 'MARKET' or 'LIMIT'.")
        
    if quantity <= 0:
        raise ValidationError(f"Quantity must be greater than 0. Got: {quantity}")
        
    if order_type == "LIMIT":
        if price is None:
            raise ValidationError("Price is required for LIMIT orders.")
        if price <= 0:
            raise ValidationError(f"Price must be greater than 0 for LIMIT orders. Got: {price}")
            
    if order_type == "MARKET":
        if price is not None:
            raise ValidationError("Price must not be provided for MARKET orders.")
