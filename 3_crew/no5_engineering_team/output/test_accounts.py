import unittest
from accounts import Account, StockMarket, InsufficientFundsError, InsufficientSharesError

class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account('test_account', 1000.0)

    def test_init(self):
        self.assertEqual(self.account.account_id, 'test_account')
        self.assertEqual(self.account.balance, 1000.0)
        self.assertEqual(self.account.initial_deposit, 1000.0)
        self.assertEqual(self.account.portfolio, {})
        self.assertEqual(self.account.transactions, [])

    def test_deposit(self):
        new_balance = self.account.deposit(500.0)
        self.assertEqual(new_balance, 1500.0)
        self.assertEqual(self.account.balance, 1500.0)
        self.assertEqual(len(self.account.transactions), 1)
        self.assertEqual(self.account.transactions[0], {'type': 'deposit', 'amount': 500.0})

    def test_withdraw_success(self):
        new_balance = self.account.withdraw(300.0)
        self.assertEqual(new_balance, 700.0)
        self.assertEqual(self.account.balance, 700.0)
        self.assertEqual(len(self.account.transactions), 1)
        self.assertEqual(self.account.transactions[0], {'type': 'withdrawal', 'amount': 300.0})

    def test_withdraw_insufficient_funds(self):
        with self.assertRaises(InsufficientFundsError):
            self.account.withdraw(1500.0)

    def test_buy_stock_success(self):
        self.account.buy_stock('AAPL', 5)
        self.assertEqual(self.account.balance, 250.0)
        self.assertEqual(self.account.portfolio, {'AAPL': 5})
        self.assertEqual(len(self.account.transactions), 1)
        self.assertEqual(self.account.transactions[0], {'type': 'buy', 'symbol': 'AAPL', 'quantity': 5, 'price': 150.0})

    def test_buy_stock_insufficient_funds(self):
        with self.assertRaises(InsufficientFundsError):
            self.account.buy_stock('TSLA', 2)

    def test_sell_stock_success(self):
        self.account.buy_stock('AAPL', 5)
        self.account.sell_stock('AAPL', 3)
        self.assertEqual(self.account.balance, 700.0)
        self.assertEqual(self.account.portfolio, {'AAPL': 2})
        self.assertEqual(len(self.account.transactions), 2)
        self.assertEqual(self.account.transactions[1], {'type': 'sell', 'symbol': 'AAPL', 'quantity': 3, 'price': 150.0})

    def test_sell_stock_insufficient_shares(self):
        self.account.buy_stock('AAPL', 2)
        with self.assertRaises(InsufficientSharesError):
            self.account.sell_stock('AAPL', 3)

    def test_get_portfolio_value(self):
        self.account.buy_stock('AAPL', 2)
        self.account.buy_stock('TSLA', 1)
        self.assertEqual(self.account.get_portfolio_value(), 1000.0)

    def test_get_profit_loss(self):
        self.account.buy_stock('AAPL', 2)
        self.account.buy_stock('TSLA', 1)
        self.assertEqual(self.account.get_profit_loss(), 0.0)

    def test_get_holdings(self):
        self.account.buy_stock('AAPL', 2)
        self.account.buy_stock('TSLA', 1)
        expected_holdings = {
            'AAPL': {'quantity': 2, 'value': 300.0},
            'TSLA': {'quantity': 1, 'value': 700.0}
        }
        self.assertEqual(self.account.get_holdings(), expected_holdings)

    def test_get_transaction_history(self):
        self.account.deposit(500.0)
        self.account.buy_stock('AAPL', 2)
        self.account.sell_stock('AAPL', 1)
        transactions = self.account.get_transaction_history()
        self.assertEqual(len(transactions), 3)
        self.assertEqual(transactions[0], {'type': 'deposit', 'amount': 500.0})
        self.assertEqual(transactions[1], {'type': 'buy', 'symbol': 'AAPL', 'quantity': 2, 'price': 150.0})
        self.assertEqual(transactions[2], {'type': 'sell', 'symbol': 'AAPL', 'quantity': 1, 'price': 150.0})

class TestStockMarket(unittest.TestCase):
    def test_get_share_price(self):
        self.assertEqual(StockMarket.get_share_price('AAPL'), 150.0)
        self.assertEqual(StockMarket.get_share_price('TSLA'), 700.0)
        self.assertEqual(StockMarket.get_share_price('GOOGL'), 2500.0)
        self.assertEqual(StockMarket.get_share_price('INVALID'), 0.0)

if __name__ == '__main__':
    unittest.main()