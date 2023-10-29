import requests
from bs4 import BeautifulSoup


def take_price_yahoo(ticker: str, stock_market: str) -> str or None:
    """Получение цены криптовалюты путем парсинга yahoo.com.
    :param ticker: тикер актива
    :return: цена актива или None, если не удалось получить
    """
    if stock_market == 'HKEX':
        ticker = f'{ticker}.HK'
    url_price = f"https://finance.yahoo.com/quote/{ticker}"
    try:
        req_price = requests.get(url_price)
        soup = BeautifulSoup(markup=req_price.content, features="html.parser")

        name_block = soup.find("h1", {"class": "D(ib) Fz(18px)"})
        price_block = soup.find("fin-streamer", {"class": "Fw(b) Fz(36px) Mb(-4px) D(ib)"})
        if not name_block or not price_block:
            raise ValueError()
        name = name_block.text
        price = price_block.text
        print("name:", name)
        print("price:", price)
        return price
    except Exception as yahoo_err:
        yahoo_err.args += (f"Адрес запроса для получения Цены и Наименования: '{url_price}'. "
                           f"Статус ответа: '{req_price.status_code}'",)
        raise yahoo_err

# ticker = "KO"

# try:
#     take_price_yahoo(ticker=ticker)
# except Exception as err:
#     err_data = f"Ошибка при получении данных с yahoo.com для актива '{ticker}': {type(err)} - {err}"
#     print(err.args)
#     print(err_data)
