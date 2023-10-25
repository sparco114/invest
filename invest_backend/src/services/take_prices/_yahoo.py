import requests
from bs4 import BeautifulSoup


def take_price_yahoo(ticker: str) -> str:
    """Получение цены криптовалюты путем парсинга yahoo.com.
    :param ticker: тикер актива
    :return: цена актива
    """

    url_price = f"https://finance.yahoo.com/quote/{ticker}"
    try:
        req_price = requests.get(url_price)
        soup = BeautifulSoup(markup=req_price.content, features="html.parser")
        name = soup.find("h1", {"class": "D(ib) Fz(18px)"}).text
        price = soup.find("fin-streamer", {"class": "Fw(b) Fz(36px) Mb(-4px) D(ib)"}).text
        # print(page.status_code)
        print("name:", name)
        print("price:", price)
        return price
    except Exception as yahoo_err:
        yahoo_err.args += (f"Адрес запроса для получения Цены и Наименования: '{url_price}'",)
        raise yahoo_err

# ticker = "KO"

# try:
#     take_price_yahoo(ticker=ticker)
# except Exception as err:
#     err_data = f"Ошибка при получении данных с yahoo.com для актива '{ticker}': {type(err)} - {err}"
#     print(err.args)
#     print(err_data)
