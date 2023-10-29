import requests
from bs4 import BeautifulSoup


def take_price_google(ticker: str, stock_market: str) -> str or None:
    """Получение цены криптовалюты путем парсинга google.com.
    :param ticker: тикер актива
    :return: цена актива или None, если не удалось получить
    """

    if stock_market == 'HKEX':
        ticker = f'{ticker}:HKG'
    url_price = f"https://www.google.com/finance/quote/{ticker}"

    try:
        req_price = requests.get(url_price)
        soup = BeautifulSoup(markup=req_price.content, features="html.parser")
        name_block = soup.find("div", {"class": "zzDege"})
        price_block = soup.find("div", {"class": "YMlKec fxKbKc"})
        if not name_block or not price_block:
            raise ValueError()
        name = name_block.text
        price = price_block.text[1:]
        print("name:", name)
        print("price:", price)
        return price
    except Exception as google_err:
        google_err.args += (f"Адрес запроса для получения Цены и Наименования: '{url_price}'. "
                            f"Статус ответа: '{req_price.status_code}'",)
        raise google_err

# ticker = "0001:HKG"
#
# try:
#     take_price_google(ticker=ticker)
# except Exception as err:
#     err_data = f"Ошибка при получении данных с google.com для актива '{ticker}': {type(err)} - {err}"
#     print(err.args)
#     print(err_data)
