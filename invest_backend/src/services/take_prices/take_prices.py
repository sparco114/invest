from django.db import transaction

from src.assets.models import Asset
from src.services.take_prices._google import take_price_google
from src.services.take_prices._moex import take_price_moex
from src.services.take_prices._yahoo import take_price_yahoo
from src.services.take_prices._cryptocompare import take_price_cryptocompare


# ticker = "SBER"
# stock_market = ""
# asset_class = "Акции"
# currency = "USD"


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
        parsing_errors = []
        try:
            new_price = take_price_yahoo(ticker=ticker, stock_market=stock_market)
            if new_price:
                return new_price

        except Exception as yahoo_err:
            err_data = f"Возможно не верно указан Биржа. Ошибка при получении данных с yahoo.com " \
                       f"для актива '{ticker}': {type(yahoo_err)} - {yahoo_err}"
            print(err_data)
            parsing_errors.append(err_data)


        try:
            new_price = take_price_google(ticker=ticker, stock_market=stock_market)
            if new_price:
                return new_price
        except Exception as google_err:
            err_data = f"Возможно не верно указан Биржа. Ошибка при получении данных с google.com " \
                       f"для актива '{ticker}': {type(google_err)} - {google_err}"
            print(err_data)
            parsing_errors.append(err_data)
        raise ValueError(parsing_errors)


# try:
#     res = take_price(ticker, stock_market, asset_class, currency)
#     print("--res:", res)
# except Exception as err:
#     print(err)

def all_assets_prices_update() -> list:
    all_assets = Asset.objects.select_related('stock_market',
                                              'asset_class',
                                              'currency_of_price'
                                              ).only('id',
                                                     'ticker',
                                                     'stock_market__name',
                                                     'asset_class__name',
                                                     'currency_of_price__name',
                                                     'one_unit_current_price_in_currency')

    new_prices = []
    errors_take_prices = []
    for asset in all_assets:
        # print('---asset:', asset.currency_of_price.name)
        try:
            new_price = take_price(ticker=asset.ticker,
                                   stock_market=asset.stock_market.name,
                                   asset_class=asset.asset_class.name,
                                   currency=asset.currency_of_price.name)
            print('--данные получены из new_price:', new_price)
            asset.one_unit_current_price_in_currency = new_price
            new_prices.append(asset)
        except Exception as err:
            err_msg = f"Не удалось обновить цену '{asset.ticker}' - id: {asset.id}. Ошибка: {err}"
            errors_take_prices.append({'id': asset.id, 'name': asset.ticker, 'error': err_msg})

    if new_prices:
        with transaction.atomic():
            print("---запускается bulk_update для цен")
            Asset.objects.bulk_update(new_prices, ['one_unit_current_price_in_currency'])

    return errors_take_prices
