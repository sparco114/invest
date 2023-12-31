import aiohttp
from bs4 import BeautifulSoup


async def _take_board_id_moex_async(ticker: str) -> str:
    """Получение с API (обрабатывается формат xml) актуального board_id Актива для дальнейшего формирования
    ссылки, по которой возможно получить цену Актива.
    :param ticker: тикер Актива
    :return: board_id Актива
    """
    url_board_id_check = f"https://iss.moex.com/iss/securities/" \
                         f"{ticker}.xml?iss.meta=off&iss.only=boards&boards.columns=boardid,is_primary"
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        try:
            async with session.get(url_board_id_check) as response_board_id:
                content = await response_board_id.text()
                bs_req = BeautifulSoup(markup=content, features="xml")
                board_id = bs_req.find("row", {"is_primary": "1"})["boardid"]
                # print(f"board_id для {ticker}: {board_id}")
                return board_id
        except Exception as board_id_err:
            board_id_err.args += (f"Ошибка, не удалось получить board_id на MOEX для актива '{ticker}'. "
                                  f"Адрес запроса: '{url_board_id_check}', "
                                  f"статус ответ {response_board_id.status}",)
            raise board_id_err


async def take_price_moex_async(ticker: str, asset_class: str) -> str:
    """Получение текущей цены Актива с API (обрабатывается формат xml).
    :param ticker: тикер актива
    :param asset_class: класс актива, для формирования url
    :return: цена актива
    """
    # print("-----данные пришли в take_price_moex:", ticker, asset_class)

    # определяем класс актива для формирования ссылки
    if asset_class == "Акции":
        asset = "shares"
    elif asset_class == "Облигации":
        asset = "bonds"
    else:
        raise ValueError(f"Неверно указан Класс актива для поиска на Мосбирже: '{asset_class}'. "
                         f"Возможны только 'Акции' и 'Облигации'")

    # получаем board_id Актива для получения актуальных данных из xml
    board_id = await _take_board_id_moex_async(ticker=ticker)

    #  Если в дальнейшем буду получать сразу списком цен по всем акциям, то можно использовать
    #  эту ссылку "https://iss.moex.com/iss/engines/stock/markets/bonds/boards/TQCB/securities.xml
    #  ?iss.meta=off&iss.only=securities,marketdata"
    # TODO: !!! берет цену как изи-инвест, но не соответствует цене брокера, можно поискать путь к
    #  той цене, которую берет брокер
    url_take_price = f"https://iss.moex.com/iss/engines/stock/markets/{asset}/securities/" \
                     f"{ticker}.xml?iss.meta=off&iss.only=securities,marketdata"
    # print(url_take_price)
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        try:
            async with session.get(url_take_price) as response_price:
                content = await response_price.text()
                bs_req = BeautifulSoup(markup=content, features="xml")
                marketdata = bs_req.find("data", {"id": "marketdata"}).find("row", {"SECID": ticker,
                                                                                    "BOARDID": board_id})
                securities = bs_req.find("data", {"id": "securities"}).find("row", {"SECID": ticker,
                                                                                    "BOARDID": board_id})
                last_price = marketdata.get("LAST")  # текущая последняя цена (если биржа открыта)
                prev_price = securities.get("PREVPRICE")  # предыдущая цена (если биржа закрыта)

                # если текущей цены нет (биржа закрыта), то ебере последнюю актуальную цену до закрытия
                price = last_price or prev_price

                # print(last_price)
                # print(prev_price)
                # print(securities.get("SHORTNAME"))
                # print(securities.get("SECNAME"))
                # print("---price in 'take_price_moex':", price)
                # print(price)

                # если не получены данные о цене - поднимаем ошибку, чтоб не возвращать None
                if not price:
                    raise ValueError()
                return price

        except Exception as moex_err:
            moex_err.args += (f"Адрес запроса для получения Цены и Наименования: '{url_take_price}'"
                              f"Статус ответ: '{response_price.status}' ",)
            raise moex_err

# def _take_board_id_moex(ticker: str) -> str:
#     """Получение board_id актива для дальнейшего формирования ссылки, по которой возможно получить
#     цену актива.
#     :param ticker: тикер актива
#     :return: board_id актива
#     """
#
#     url_board_id_check = f"https://iss.moex.com/iss/securities/" \
#                          f"{ticker}.xml?iss.meta=off&iss.only=boards&boards.columns=boardid,is_primary"
#     try:
#         req_board_id = requests.get(url_board_id_check)
#         bs_req = BeautifulSoup(markup=req_board_id.content, features="xml")
#         board_id = bs_req.find("row", {"is_primary": "1"})["boardid"]
#         print(board_id)
#         return board_id
#     except Exception as board_id_err:
#         board_id_err.args += (f"Ошибка, не удалось получить board_id для актива. Адрес запроса: "
#                               f"'{url_board_id_check}'",)
#         raise board_id_err
#
#
# def take_price_moex(ticker: str, asset_class: str) -> str:
#     """Получение цены криптовалюты с API в формате xml.
#     :param ticker: тикер актива
#     :param asset_class: класс актива, для формирования url
#     :return: цена актива
#     """
#
#     if asset_class == "Акции":
#         asset = "shares"
#     elif asset_class == "Облигации":
#         asset = "bonds"
#     else:
#         raise ValueError("Неверно указан Класс актива для поиска на Мосбирже. "
#                          "Возможны только 'Акции' и 'Облигации'")
#
#     board_id = _take_board_id_moex(ticker=ticker)
#
#     #  Если в дальнейшем буду получать сразу списком цен по всем акциям, то можно использовать
#     #  эту ссылку "https://iss.moex.com/iss/engines/stock/markets/bonds/boards/TQCB/securities.xml
#     #  ?iss.meta=off&iss.only=securities,marketdata"
#     # TODO: !!! берет цену как изи-инвест, но не соответствует цене брокера, можно поискать путь к
#     #  той цене, которую берет брокер
#     url_take_price = f"https://iss.moex.com/iss/engines/stock/markets/{asset}/securities/" \
#                      f"{ticker}.xml?iss.meta=off&iss.only=securities,marketdata"
#     # print(url_take_price)
#     try:
#         req = requests.get(url_take_price)
#         bs_req = BeautifulSoup(markup=req.content, features="xml")
#         marketdata = bs_req.find("data", {"id": "marketdata"}).find("row", {"SECID": ticker,
#                                                                             "BOARDID": board_id})
#         securities = bs_req.find("data", {"id": "securities"}).find("row", {"SECID": ticker,
#                                                                             "BOARDID": board_id})
#         last_price = marketdata.get("LAST")  # текущая последняя цена (если биржа открыта)
#         prev_price = securities.get("PREVPRICE")  # предыдущая цена (если биржа закрыта)
#         price = last_price or prev_price
#         # print(last_price)
#         # print(prev_price)
#         # print(securities.get("SHORTNAME"))
#         # print(securities.get("SECNAME"))
#         print("---price in 'take_price_moex':", price)
#         # print(price)
#         if not price:
#             raise ValueError()
#         return price
#     except Exception as moex_err:
#         moex_err.args += (f"Адрес запроса для получения Цены и Наименования: '{url_take_price}'",)
#         raise moex_err


# ticker = "SBER"
# asset_class = "Акции"


# ticker = "RU000A100BB0"  # погашен
# ticker = "RU000A105AS5"  # действует
# asset_class = "Облигации"

# try:
#     take_price_moex(ticker=ticker, asset_class=asset_class)
# except Exception as err:
#     err_data = f"Ошибка при получении данных с MOEX для актива '{ticker}': {type(err)} - {err}"
#     print(err_data)
