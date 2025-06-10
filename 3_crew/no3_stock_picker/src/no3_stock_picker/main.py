#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from no3_stock_picker.crew import No3StockPicker

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


def run():
    """
    Run the research crew.
    """
    inputs = {
        'sector': 'Technology'
    }

    result = No3StockPicker().crew().kickoff(inputs=inputs)

    print("\n\n=== FINAL DECISION ===\n\n")
    print(result.raw)


if __name__ == "__main__":
    run()
