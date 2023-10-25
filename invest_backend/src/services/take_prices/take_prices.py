from src.services.take_prices._moex import take_price_moex
from src.services.take_prices._yahoo import take_price_yahoo
from src.services.take_prices._cryptocompare import take_price_cryptocompare

ticker = "SBER"
stock_market = ""
asset_class = "Акции"
currency = "USD"


def take_price(ticker: str, stock_market: str, asset_class: str, currency: str) -> str:
    print("---Данные пришли в take_price:", ticker, stock_market, asset_class, currency)
    if stock_market == "MOEX":
        try:
            return take_price_moex(ticker=ticker, asset_class=asset_class)
        except Exception as moex_err:
            err_data = f"Ошибка при получении данных с MOEX для актива '{ticker}': " \
                       f"{type(moex_err)} - {moex_err}"
            print(err_data)
            raise moex_err

    elif asset_class == "Крипто":
        try:
            return take_price_cryptocompare(ticker=ticker, currency=currency)
        except Exception as cryptocompare_err:
            err_data = f"Ошибка при получении данных с cryptocompare.com для актива '{ticker}': " \
                       f"{type(cryptocompare_err)} - {cryptocompare_err}"
            print(err_data)

    elif asset_class == "Валюта":
        return "1.0"

    else:
        try:
            return take_price_yahoo(ticker=ticker)
        except Exception as yahoo_err:
            err_data = f"Возможно не верно указан Биржа. Ошибка при получении данных с yahoo.com для актива " \
                       f"'{ticker}': {type(yahoo_err)} - {yahoo_err}"
            print(err_data)


# try:
#     res = take_price(ticker, stock_market, asset_class, currency)
#     print("--res:", res)
# except Exception as err:
#     print(err)
