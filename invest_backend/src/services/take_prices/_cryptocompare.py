import requests


def take_price_cryptocompare(ticker: str, currency: str) -> str:
    """Получение цены криптовалюты с API в формате json.
    :param ticker: тикер актива
    :param currency: валюта, в которой необходимо получить цену
    :return: цена криптоактива (по указанному тикеру) в указанной валюте
    """

    url_price = f"https://min-api.cryptocompare.com/data/price?fsym={ticker}&tsyms={currency}"
    try:
        req_price = requests.get(url_price)
        price = str(req_price.json()[currency])
    except Exception as cryptocompare_price_err:
        cryptocompare_price_err.args += (f"Адрес запроса для получения Цены: '{url_price}'",)
        raise cryptocompare_price_err

    url_name = f"https://min-api.cryptocompare.com/data/all/coinlist?fsym={ticker}"
    try:
        req_name = requests.get(url_name)
        name = req_name.json()["Data"][ticker]["FullName"]
        print(name)
    except Exception as cryptocompare_name_err:
        cryptocompare_name_err.args += (f"Адрес запроса для получения Наименования: '{url_name}'",)
        raise cryptocompare_name_err

    print("name:", name)
    print("price:", price)
    return price

# ticker = "TRX"
# currency = "RUB"

# try:
#     take_price_cryptocompare(ticker=ticker, currency=currency)
# except Exception as err:
#     err_data = f"Ошибка при получении данных с cryptocompare.com для актива '{ticker}': {type(err)} - {err}"
#     print(err_data)
