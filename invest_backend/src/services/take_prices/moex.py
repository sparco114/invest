import requests
from bs4 import BeautifulSoup

ticker = "SBER"
asset_class = "Акции"


# ticker = "RU000A100BB0"
# asset_class = "Облигации"


def _take_board_id_moex(ticker: str) -> str:
    url_board_id_check = f"https://iss.moex.com/iss/securities/{ticker}.xml"
    req = requests.get(url_board_id_check)
    bs_req = BeautifulSoup(markup=req.content, features="xml")
    board_id = bs_req.find("row", {"is_primary": "1"})["boardid"]
    # print(board_id)
    return board_id


# take_board_id(ticker=ticker)

def take_price_moex(ticker: str, asset_class: str) -> str:
    if asset_class == "Акции":
        asset = "shares"
    elif asset_class == "Облигации":
        asset = "bonds"
    else:
        err_msg = "Выводить ошибку, что неверно указан класс актива для Мосбиржи"
        print(err_msg)
        return err_msg

    try:
        board_id = _take_board_id_moex(ticker=ticker)
    except Exception as err:
        err_data = f"Ошибка, не удалось получить board_id для актива: {err}"
        print(err_data)
        raise ValueError(err_data)
    url_take_price = f"https://iss.moex.com/iss/engines/stock/markets/" \
                     f"{asset}/boards/{board_id}/securities.xml"

    # print(url_take_price)
    req = requests.get(url_take_price)
    bs_req = BeautifulSoup(markup=req.content, features="xml")
    marketdata = bs_req.find("data", {"id": "marketdata"}).find("row", {"SECID": ticker})  # текущие данные
    securities = bs_req.find("data", {"id": "securities"}).find("row", {"SECID": ticker})  # предыдущие данные
    last_price = marketdata.get("LAST")  # текущая последняя цена (если биржа открыта)
    prev_price = securities.get("PREVPRICE")  # предыдущая цена (если биржа закрыта)
    price = last_price or prev_price
    # print(last_price)
    # print(prev_price)
    # print(securities.get("SHORTNAME"))
    print(securities.get("SECNAME"))
    print(price)
    return price


try:
    take_price_moex(ticker=ticker, asset_class=asset_class)
except Exception as err:
    print(err)

