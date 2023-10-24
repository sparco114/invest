import json
import requests


ticker = "TRX"
currency = "RUB"


def take_price_cryptocompare(ticker: str, currency: str) -> str:
    url_name = f"https://min-api.cryptocompare.com/data/all/coinlist?fsym={ticker}"
    url_price = f"https://min-api.cryptocompare.com/data/price?fsym=" \
                 f"{ticker}&tsyms={currency}"
    req_name = requests.get(url_name)
    req_price = requests.get(url_price)
    name = req_name.json()["Data"][ticker]["FullName"]
    print(name)
    price = str(req_price.json()[currency])
    # print(type(price))
    print(price)
    return price


take_price_cryptocompare(ticker=ticker, currency=currency)
