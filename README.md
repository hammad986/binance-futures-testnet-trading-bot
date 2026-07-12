# Binance Futures Testnet Trading Bot

A clean, modular Python CLI application that places MARKET and LIMIT orders on the Binance USDT-M Futures Testnet. 

This project demonstrates clean architecture, logging, validation, and error handling practices for a production-grade trading bot, built as a Python Developer internship assignment.

## Features
- **Binance Futures Testnet ONLY**: Hardcoded to never touch the Mainnet.
- **Order Types**: Supports `MARKET` and `LIMIT` orders.
- **Robust Validation**: Enforces strict rules on symbols, quantities, and prices.
- **Professional CLI**: Uses `typer` and `rich` for clean, colored terminal output.
- **Comprehensive Logging**: Detailed application logs stored in `logs/app.log`.
- **Clean Architecture**: Separated concerns (validators, client, orders, config, CLI).

## Folder Structure
```text
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py
│   ├── orders.py
│   ├── validators.py
│   ├── logging_config.py
│   ├── exceptions.py
│   └── config.py
├── logs/
│   ├── app.log
│   ├── sample_market.log
│   └── sample_limit.log
├── cli.py
├── .env.example
├── requirements.txt
├── README.md
└── .gitignore
```

## Setup & Installation

### 1. Binance Futures Testnet Account
1. Go to [Binance Futures Testnet](https://testnet.binancefuture.com/).
2. Create an account or log in with your GitHub/Google account.
3. Generate an API Key and API Secret.

### 2. Environment Setup
Clone the repository, create a virtual environment, and install dependencies.
```bash
git clone <repository_url>
cd trading_bot

# Create and activate virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 3. Configuration
Copy `.env.example` to `.env` and fill in your credentials.
```bash
cp .env.example .env
```
Edit `.env`:
```env
API_KEY=your_testnet_api_key_here
API_SECRET=your_testnet_api_secret_here
```

## Usage

Use the CLI to place orders. The bot validates all inputs before attempting an API request.

### Example 1: MARKET Order
```bash
python cli.py order --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

### Example 2: LIMIT Order
```bash
python cli.py order --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 110000
```

### Expected Output
When an order is successfully placed, you will see a colored output similar to this:
```
╭──────────────── Order Request Summary ────────────────╮
│         Symbol  BTCUSDT                               │
│           Side  BUY                                   │
│     Order Type  MARKET                                │
│       Quantity  0.01                                  │
│       Order ID  1234567890                            │
│         Status  FILLED                                │
│   Executed Qty  0.01                                  │
│  Average Price  64000.50                              │
╰───────────────────────────────────────────────────────╯
```

## Project Assumptions
1. **Testnet Only**: The user intends to test strategies exclusively on the Testnet. The application explicitly enforces the `https://testnet.binancefuture.com` URL.
2. **USDT-M Futures**: The bot targets USDT-Margined futures (e.g., `BTCUSDT`).
3. **No Local State**: Order history is not saved to a local database. The application is stateless and logs all activities to the `logs/` directory.
4. **Time in Force**: LIMIT orders use `GTC` (Good Till Cancelled) by default.
