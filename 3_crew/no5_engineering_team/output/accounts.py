# accounts.py

class InsufficientFundsError(Exception):
    """Raised when a withdrawal or purchase would result in a negative balance."""
    pass

class InsufficientSharesError(Exception):
    """Raised when attempting to sell more shares than owned."""
    pass

class StockMarket:
    @staticmethod
    def get_share_price(symbol: str) -> float:
        """Return the current price of a stock. For testing, returns fixed prices for AAPL, TSLA, and GOOGL."""
        prices = {"AAPL": 150.0, "TSLA": 700.0, "GOOGL": 2500.0}
        return prices.get(symbol, 0.0)

class Account:
    def __init__(self, account_id: str, initial_deposit: float) -> None:
        """Initialize a new account with an ID and initial deposit."""
        self.account_id = account_id
        self.balance = initial_deposit
        self.initial_deposit = initial_deposit
        self.portfolio = {}
        self.transactions = []

    def deposit(self, amount: float) -> float:
        """Deposit funds into the account. Returns new balance."""
        self.balance += amount
        self.transactions.append({"type": "deposit", "amount": amount})
        return self.balance

    def withdraw(self, amount: float) -> float:
        """Withdraw funds from the account. Returns new balance. Raises InsufficientFundsError if withdrawal would result in negative balance."""
        if amount > self.balance:
            raise InsufficientFundsError("Insufficient funds for withdrawal")
        self.balance -= amount
        self.transactions.append({"type": "withdrawal", "amount": amount})
        return self.balance

    def buy_stock(self, symbol: str, quantity: int) -> None:
        """Buy a stock. Updates portfolio and records transaction. Raises InsufficientFundsError if purchase exceeds available funds."""
        price = StockMarket.get_share_price(symbol)
        total_cost = price * quantity
        if total_cost > self.balance:
            raise InsufficientFundsError("Insufficient funds to buy stock")
        self.balance -= total_cost
        self.portfolio[symbol] = self.portfolio.get(symbol, 0) + quantity
        self.transactions.append({"type": "buy", "symbol": symbol, "quantity": quantity, "price": price})

    def sell_stock(self, symbol: str, quantity: int) -> None:
        """Sell a stock. Updates portfolio and records transaction. Raises InsufficientSharesError if selling more shares than owned."""
        if symbol not in self.portfolio or self.portfolio[symbol] < quantity:
            raise InsufficientSharesError("Insufficient shares to sell")
        price = StockMarket.get_share_price(symbol)
        total_value = price * quantity
        self.balance += total_value
        self.portfolio[symbol] -= quantity
        if self.portfolio[symbol] == 0:
            del self.portfolio[symbol]
        self.transactions.append({"type": "sell", "symbol": symbol, "quantity": quantity, "price": price})

    def get_portfolio_value(self) -> float:
        """Calculate and return the total value of the portfolio."""
        return sum(StockMarket.get_share_price(symbol) * quantity for symbol, quantity in self.portfolio.items())

    def get_profit_loss(self) -> float:
        """Calculate and return the profit/loss relative to the initial deposit."""
        return self.balance + self.get_portfolio_value() - self.initial_deposit

    def get_holdings(self) -> dict[str, dict]:
        """Return current holdings with symbol, quantity, and current value."""
        return {symbol: {"quantity": quantity, "value": StockMarket.get_share_price(symbol) * quantity}
                for symbol, quantity in self.portfolio.items()}

    def get_transaction_history(self) -> list[dict]:
        """Return the list of all transactions."""
        return self.transactions