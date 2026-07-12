"""CLI entry point for the trading bot."""
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from typing import Optional

from bot.orders import place_order, parse_order_response
from bot.exceptions import BotError, ValidationError, ConfigurationError, BinanceAPIError
from bot.logging_config import logger

app = typer.Typer(help="Binance Futures Testnet Trading Bot", add_completion=False)
console = Console()

@app.command()
def order(
    symbol: str = typer.Option(..., "--symbol", help="Trading pair symbol, e.g., BTCUSDT"),
    side: str = typer.Option(..., "--side", help="Order side: BUY or SELL"),
    order_type: str = typer.Option(..., "--type", help="Order type: MARKET or LIMIT"),
    quantity: float = typer.Option(..., "--quantity", help="Quantity to trade"),
    price: Optional[float] = typer.Option(None, "--price", help="Price (Required for LIMIT orders)"),
):
    """
    Place a MARKET or LIMIT order on the Binance Futures Testnet.
    """
    logger.info(f"Application start. CLI arguments: symbol={symbol}, side={side}, type={order_type}, quantity={quantity}, price={price}")
    
    try:
        # Place the order
        raw_response = place_order(symbol, side, order_type, quantity, price)
        
        # Parse the response
        parsed = parse_order_response(raw_response)
        
        # Display the result
        display_order_success(parsed)
        
    except ValidationError as e:
        console.print(f"[bold red]Validation Error:[/bold red] {e}")
        logger.error(f"Validation Error: {e}")
    except ConfigurationError as e:
        console.print(f"[bold red]Configuration Error:[/bold red] {e}")
        logger.error(f"Configuration Error: {e}")
    except BinanceAPIError as e:
        console.print(f"[bold red]Binance API Error:[/bold red] {e}")
        logger.error(f"Binance API Error: {e}")
    except BotError as e:
        console.print(f"[bold red]Application Error:[/bold red] {e}")
        logger.error(f"Application Error: {e}")
    except Exception as e:
        console.print("[bold red]Unexpected Error:[/bold red] An unexpected error occurred. Check logs for details.")
        logger.error(f"Unexpected Error from CLI: {e}", exc_info=True)


def display_order_success(parsed: dict):
    """Displays the successful order summary using rich formatting."""
    table = Table(show_header=False, box=None)
    table.add_column("Field", style="cyan", justify="right")
    table.add_column("Value", style="green")

    table.add_row("Symbol", parsed["symbol"])
    table.add_row("Side", parsed["side"])
    table.add_row("Order Type", parsed["type"])
    table.add_row("Quantity", str(parsed["quantity"]))
    
    if parsed["type"] == "LIMIT" or parsed["price"]:
        table.add_row("Price", str(parsed["price"]))
        
    table.add_row("Order ID", str(parsed["order_id"]))
    table.add_row("Status", parsed["status"])
    table.add_row("Executed Qty", str(parsed["executed_qty"]))
    
    if parsed["avg_price"] is not None:
        table.add_row("Average Price", str(parsed["avg_price"]))

    panel = Panel(table, title="[bold green]Order Request Summary[/bold green]", expand=False)
    console.print(panel)

if __name__ == "__main__":
    app()
