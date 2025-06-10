# accounts.py

This module implements a simple trading simulation platform account management system.

## Classes

### Account

The main class representing a user's account.

#### Attributes:
- `account_id`: str
- `balance`: float
- `initial_deposit`: float
- `portfolio`: dict[str, int]  # symbol: quantity
- `transactions`: list[dict]  # List of transaction dictionaries

#### Methods:

```python
def __init__(self, account_id: str, initial_deposit: float) -> None:
    """Initialize a new account with an ID and initial deposit."""

def deposit(self, amount: float) -> float:
    """Deposit funds into the account. Returns new balance."""

def withdraw(self, amount: float) -> float:
    """Withdraw funds from the account. Returns new balance. Raises InsufficientFundsError if withdrawal would result in negative balance."""

def buy_stock(self, symbol: str, quantity: int) -> None:
    """Buy a stock. Updates portfolio and records transaction. Raises InsufficientFundsError if purchase exceeds available funds."""

def sell_stock(self, symbol: str, quantity: int) -> None:
    """Sell a stock. Updates portfolio and records transaction. Raises InsufficientSharesError if selling more shares than owned."""

def get_portfolio_value(self) -> float:
    """Calculate and return the total value of the portfolio."""

def get_profit_loss(self) -> float:
    """Calculate and return the profit/loss relative to the initial deposit."""

def get_holdings(self) -> dict[str, dict]:
    """Return current holdings with symbol, quantity, and current value."""

def get_transaction_history(self) -> list[dict]:
    """Return the list of all transactions."""
```

### StockMarket

A class to handle stock price queries and provide a test implementation.

#### Methods:

```python
@staticmethod
def get_share_price(symbol: str) -> float:
    """Return the current price of a stock. For testing, returns fixed prices for AAPL, TSLA, and GOOGL."""
```

## Custom Exceptions

```python
class InsufficientFundsError(Exception):
    """Raised when a withdrawal or purchase would result in a negative balance."""

class InsufficientSharesError(Exception):
    """Raised when attempting to sell more shares than owned."""
```

## Usage Example

```python
# Create a new account
account = Account("user123", 10000)

# Deposit and withdraw
account.deposit(5000)
account.withdraw(2000)

# Buy and sell stocks
account.buy_stock("AAPL", 10)
account.sell_stock("AAPL", 5)

# Get account information
portfolio_value = account.get_portfolio_value()
profit_loss = account.get_profit_loss()
holdings = account.get_holdings()
transactions = account.get_transaction_history()
```

This design provides a complete and self-contained module for managing trading accounts, recording transactions, and calculating portfolio values and profit/loss. The `StockMarket` class includes a test implementation of `get_share_price()` for AAPL, TSLA, and GOOGL as required. The system prevents negative balances, buying stocks beyond available funds, and selling stocks not owned through custom exceptions.