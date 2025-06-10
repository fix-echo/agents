#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from no5_engineering_team.crew import No5EngineeringTeam

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

requirements = """
一个简单的交易模拟平台账户管理系统。
系统应该允许用户创建账户、存入资金和提取资金。
系统应该允许用户记录他们买入或卖出的股票，并提供数量。
系统应该计算用户投资组合的总价值，以及相对于初始存款的盈亏。
系统应该能够随时报告用户的持仓情况。
系统应该能够随时报告用户的盈亏情况。
系统应该能够列出用户随时间进行的交易。
系统应该防止用户提取会导致负余额的资金，或
购买超出其承受能力的股票，或出售他们没有的股票。
系统可以访问函数get_share_price(symbol)，该函数返回股票的当前价格，并包含一个测试实现，为AAPL、TSLA、GOOGL返回固定价格。
"""
module_name = "accounts.py"
class_name = "Account"


def run():
    """
    Run the crew.
    """
    inputs = {
        "requirements": requirements,
        "module_name": module_name,
        "class_name": class_name
    }

    try:
        No5EngineeringTeam().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
