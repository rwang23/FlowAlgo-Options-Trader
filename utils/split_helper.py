from iexfinance.stocks import Stock
import arrow
from dotenv import load_dotenv
import os
import json
import math

load_dotenv()
if not os.path.exists("cache"):
    os.makedirs("cache")


def get_splits(symbol):
    stock = Stock(symbol)
    return stock.get_splits(range="5y")


def split_adjust_multiplier(symbol, date):
    path = f"cache/{symbol}_splits.json"

    if os.path.exists(path):
        with open(path) as f:
            splits = json.load(f)
    else:
        splits = get_splits(symbol)
        with open(path, "w") as f:
            json.dump(splits, f, indent=4)

    splits = set([(arrow.get(s["exDate"]), s["toFactor"]) for s in splits])
    splits = filter(lambda s: s[0] > date, splits)
    return 1 / math.prod([s[1] for s in splits])
