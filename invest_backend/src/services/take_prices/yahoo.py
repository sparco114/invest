import requests
from bs4 import BeautifulSoup

ticker = "KO"


def take_price_yahoo(ticker: str) -> str:
    target_url = f"https://finance.yahoo.com/quote/{ticker}"
    page = requests.get(target_url)
    soup = BeautifulSoup(markup=page.content, features="html.parser")

    name = soup.find("h1", {"class": "D(ib) Fz(18px)"}).text
    price = soup.find("fin-streamer", {"class": "Fw(b) Fz(36px) Mb(-4px) D(ib)"}).text
    # print(page.status_code)
    print(name)
    print(price)
    return price

take_price_yahoo(ticker=ticker)
