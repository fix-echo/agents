import gradio as gr
from accounts import Account, InsufficientFundsError, InsufficientSharesError, StockMarket

# Initialize a single account for demonstration
demo_account = Account("demo", 10000)

def create_account(initial_deposit):
    global demo_account
    demo_account = Account("demo", float(initial_deposit))
    return f"Account created with initial deposit of ${initial_deposit}"

def deposit(amount):
    try:
        new_balance = demo_account.deposit(float(amount))
        return f"Deposit successful. New balance: ${new_balance:.2f}"
    except ValueError:
        return "Invalid amount. Please enter a valid number."

def withdraw(amount):
    try:
        new_balance = demo_account.withdraw(float(amount))
        return f"Withdrawal successful. New balance: ${new_balance:.2f}"
    except InsufficientFundsError:
        return "Insufficient funds for withdrawal."
    except ValueError:
        return "Invalid amount. Please enter a valid number."

def buy_stock(symbol, quantity):
    try:
        demo_account.buy_stock(symbol, int(quantity))
        return f"Successfully bought {quantity} shares of {symbol}"
    except InsufficientFundsError:
        return "Insufficient funds to buy stock."
    except ValueError:
        return "Invalid quantity. Please enter a valid number."

def sell_stock(symbol, quantity):
    try:
        demo_account.sell_stock(symbol, int(quantity))
        return f"Successfully sold {quantity} shares of {symbol}"
    except InsufficientSharesError:
        return "Insufficient shares to sell."
    except ValueError:
        return "Invalid quantity. Please enter a valid number."

def get_portfolio_value():
    value = demo_account.get_portfolio_value()
    return f"Current portfolio value: ${value:.2f}"

def get_profit_loss():
    pl = demo_account.get_profit_loss()
    return f"Current profit/loss: ${pl:.2f}"

def get_holdings():
    holdings = demo_account.get_holdings()
    return "\n".join([f"{symbol}: {data['quantity']} shares, value: ${data['value']:.2f}" for symbol, data in holdings.items()])

def get_transaction_history():
    history = demo_account.get_transaction_history()
    return "\n".join([f"{t['type'].capitalize()}: {t.get('symbol', '')} {t.get('quantity', '')} ${t.get('amount', t.get('price', 0)):.2f}" for t in history])

def get_balance():
    return f"Current balance: ${demo_account.balance:.2f}"

def get_stock_price(symbol):
    price = StockMarket.get_share_price(symbol)
    return f"Current price of {symbol}: ${price:.2f}"

with gr.Blocks() as demo:
    gr.Markdown("# Simple Trading Platform Demo")
    
    with gr.Tab("Account Management"):
        gr.Markdown("## Create Account")
        create_input = gr.Number(label="Initial Deposit")
        create_button = gr.Button("Create Account")
        create_output = gr.Textbox(label="Result")
        create_button.click(create_account, inputs=create_input, outputs=create_output)

        gr.Markdown("## Deposit/Withdraw")
        amount_input = gr.Number(label="Amount")
        deposit_button = gr.Button("Deposit")
        withdraw_button = gr.Button("Withdraw")
        balance_output = gr.Textbox(label="Result")
        deposit_button.click(deposit, inputs=amount_input, outputs=balance_output)
        withdraw_button.click(withdraw, inputs=amount_input, outputs=balance_output)

    with gr.Tab("Trading"):
        gr.Markdown("## Buy/Sell Stocks")
        symbol_input = gr.Textbox(label="Stock Symbol")
        quantity_input = gr.Number(label="Quantity")
        buy_button = gr.Button("Buy")
        sell_button = gr.Button("Sell")
        trade_output = gr.Textbox(label="Result")
        buy_button.click(buy_stock, inputs=[symbol_input, quantity_input], outputs=trade_output)
        sell_button.click(sell_stock, inputs=[symbol_input, quantity_input], outputs=trade_output)

        gr.Markdown("## Get Stock Price")
        price_symbol_input = gr.Textbox(label="Stock Symbol")
        price_button = gr.Button("Get Price")
        price_output = gr.Textbox(label="Result")
        price_button.click(get_stock_price, inputs=price_symbol_input, outputs=price_output)

    with gr.Tab("Portfolio"):
        gr.Markdown("## Portfolio Information")
        balance_button = gr.Button("Get Balance")
        balance_display = gr.Textbox(label="Balance")
        balance_button.click(get_balance, outputs=balance_display)

        value_button = gr.Button("Get Portfolio Value")
        value_display = gr.Textbox(label="Portfolio Value")
        value_button.click(get_portfolio_value, outputs=value_display)

        pl_button = gr.Button("Get Profit/Loss")
        pl_display = gr.Textbox(label="Profit/Loss")
        pl_button.click(get_profit_loss, outputs=pl_display)

        holdings_button = gr.Button("Get Holdings")
        holdings_display = gr.Textbox(label="Holdings")
        holdings_button.click(get_holdings, outputs=holdings_display)

    with gr.Tab("Transaction History"):
        gr.Markdown("## Transaction History")
        history_button = gr.Button("Get Transaction History")
        history_display = gr.Textbox(label="Transaction History")
        history_button.click(get_transaction_history, outputs=history_display)

if __name__ == "__main__":
    demo.launch()