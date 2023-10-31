import asyncio
from concurrent.futures import ThreadPoolExecutor

from asgiref.sync import sync_to_async
from django.db import transaction

from src.assets.models import Asset
from src.services.take_prices._cryptocompare import take_price_cryptocompare_async
from src.services.take_prices._google import take_price_google_async
from src.services.take_prices._moex import take_price_moex_async
from src.services.take_prices._yahoo import take_price_yahoo_async


# from src.services.take_prices._google import take_price_google
# from src.services.take_prices._moex import take_price_moex
# from src.services.take_prices._yahoo import take_price_yahoo
# from src.services.take_prices._cryptocompare import take_price_cryptocompare


async def take_price_async(asset_id: str or None, ticker: str, stock_market: str, asset_class: str,
                           currency: str) -> tuple:
    print("---Данные пришли в take_price:", asset_id, ticker, stock_market, asset_class, currency)
    if stock_market == "MOEX":
        try:
            # print('---------', asset_id)
            new_price = await take_price_moex_async(ticker=ticker, asset_class=asset_class)
            return asset_id, new_price
        except Exception as moex_err:
            err_data = f"Ошибка при получении данных с MOEX для актива '{ticker}': " \
                       f"{type(moex_err)} - {moex_err}"
            # print(err_data)
            raise ValueError(err_data)

    elif asset_class == "Крипто":
        try:
            new_price = await take_price_cryptocompare_async(ticker=ticker, currency=currency)
            return asset_id, new_price
        except Exception as cryptocompare_err:
            err_data = f"Ошибка при получении данных с cryptocompare.com для актива '{ticker}': " \
                       f"{type(cryptocompare_err)} - {cryptocompare_err}"
            raise ValueError(err_data)

    elif asset_class == "Валюта":
        return asset_id, "1.0"

    else:
        parsing_errors = []
        try:
            new_price = await take_price_yahoo_async(ticker=ticker, stock_market=stock_market)
            if new_price:
                return asset_id, new_price

        except Exception as yahoo_err:
            err_data = f"Возможно не верно указан Биржа. Ошибка при получении данных с yahoo.com " \
                       f"для актива '{ticker}': {type(yahoo_err)} - {yahoo_err}"
            # print(err_data)
            parsing_errors.append(err_data)

        try:
            new_price = await take_price_google_async(ticker=ticker, stock_market=stock_market)
            if new_price:
                return asset_id, new_price
        except Exception as google_err:
            err_data = f"Возможно не верно указан Биржа. Ошибка при получении данных с google.com " \
                       f"для актива '{ticker}': {type(google_err)} - {google_err}"
            # print(err_data)
            parsing_errors.append(err_data)
        raise ValueError(parsing_errors)


# def aaa():
#     all_assets = Asset.objects.select_related('stock_market',
#                                                   'asset_class',
#                                                   'currency_of_price'
#                                                   ).only('id',
#                                                          'ticker',
#                                                          'stock_market__name',
#                                                          'asset_class__name',
#                                                          'currency_of_price__name',
#                                                          'one_unit_current_price_in_currency')
#     return all_assets

def _sync_bulk_update_assets(assets, fields):
    with transaction.atomic():
        Asset.objects.bulk_update(assets, fields)


async def all_assets_prices_update_async():
    # all_assets = [
    #     {'id': 4, 'ticker': 'SBER', 'stock_market': 'MOEX', 'currency': 'RUB', 'asset_class': 'Акции'},
    #     {'id': 5, 'ticker': 'NVTK', 'stock_market': 'MOEX', 'currency': 'RUB', 'asset_class': 'Акции'},
    #     {'id': 6, 'ticker': 'AZP', 'stock_market': 'MOEX', 'currency': 'RUB', 'asset_class': 'Акции'},
    #     {'id': 7, 'ticker': 'RU000A105AS5', 'stock_market': 'MOEX', 'currency': 'RUB', 'asset_class': 'Облигации'}]

    assets_queryset = Asset.objects.select_related('stock_market',
                                                   'asset_class',
                                                   'currency_of_price'
                                                   ).only('id',
                                                          'ticker',
                                                          'stock_market__name',
                                                          'asset_class__name',
                                                          'currency_of_price__name',
                                                          'one_unit_current_price_in_currency')
    # print('----asset_filter:', asset_filter)

    all_assets = await sync_to_async(list)(assets_queryset)
    # print(f'---all_assets: "{all_assets}"')

    print('---ASSET', all_assets)
    tasks = [(take_price_async(asset.id,
                               asset.ticker,
                               asset.stock_market.name,
                               asset.asset_class.name,
                               asset.currency_of_price.name)) for asset in all_assets]
    # print('---tasks:', tasks)

    new_prices = {}
    errors_take_prices = []

    for task in asyncio.as_completed(tasks):
        try:
            asset_id, new_price = await task
            # print('--данные получены из new_price:', new_price)
            # print('ASSET:', asset)
            new_prices[asset_id] = new_price
            # print(new_price)
        except Exception as err:
            # err_msg = f"Не удалось обновить цену. Ошибка: {err}"
            errors_take_prices.append({'error': err})

    not_updated_assets = []
    for asset in all_assets:
        if asset.id in new_prices:
            asset.one_unit_current_price_in_currency = new_prices[asset.id]
        else:
            not_updated_assets.append(f"id: {asset.id}, ticker: {asset.ticker}")

    if new_prices:
        print('ЗАПУСК rrrr')
        await sync_to_async(_sync_bulk_update_assets)(all_assets, ['one_unit_current_price_in_currency'])

    all_errors = {}
    if errors_take_prices:
        all_errors['errors_take_prices'] = errors_take_prices
    if not_updated_assets:
        all_errors['not_updated_assets'] = not_updated_assets
    print('---new_prices:', new_prices)
    # print('---errors_take_prices:', errors_take_prices)
    # print('---not_updated_assets:', not_updated_assets)
    print('---all_errors:', all_errors)
    result = all_errors if all_errors else "Данные успешно обновлены"
    print(result)
    return result

# ticker = "SBER"
# stock_market = ""
# asset_class = "Акции"
# currency = "USD"


# def take_price(ticker: str, stock_market: str, asset_class: str, currency: str) -> str:
#     print("---Данные пришли в take_price:", ticker, stock_market, asset_class, currency)
#     if stock_market == "MOEX":
#         try:
#             return take_price_moex(ticker=ticker, asset_class=asset_class)
#         except Exception as moex_err:
#             err_data = f"Ошибка при получении данных с MOEX для актива '{ticker}': " \
#                        f"{type(moex_err)} - {moex_err}"
#             print(err_data)
#             raise moex_err
#
#     elif asset_class == "Крипто":
#         try:
#             return take_price_cryptocompare(ticker=ticker, currency=currency)
#         except Exception as cryptocompare_err:
#             err_data = f"Ошибка при получении данных с cryptocompare.com для актива '{ticker}': " \
#                        f"{type(cryptocompare_err)} - {cryptocompare_err}"
#             print(err_data)
#
#     elif asset_class == "Валюта":
#         return "1.0"
#
#     else:
#         parsing_errors = []
#         try:
#             new_price = take_price_yahoo(ticker=ticker, stock_market=stock_market)
#             if new_price:
#                 return new_price
#
#         except Exception as yahoo_err:
#             err_data = f"Возможно не верно указан Биржа. Ошибка при получении данных с yahoo.com " \
#                        f"для актива '{ticker}': {type(yahoo_err)} - {yahoo_err}"
#             print(err_data)
#             parsing_errors.append(err_data)
#
#
#         try:
#             new_price = take_price_google(ticker=ticker, stock_market=stock_market)
#             if new_price:
#                 return new_price
#         except Exception as google_err:
#             err_data = f"Возможно не верно указан Биржа. Ошибка при получении данных с google.com " \
#                        f"для актива '{ticker}': {type(google_err)} - {google_err}"
#             print(err_data)
#             parsing_errors.append(err_data)
#         raise ValueError(parsing_errors)


# try:
#     res = take_price(ticker, stock_market, asset_class, currency)
#     print("--res:", res)
# except Exception as err:
#     print(err)

# def all_assets_prices_update() -> list:
#     all_assets = Asset.objects.select_related('stock_market',
#                                               'asset_class',
#                                               'currency_of_price'
#                                               ).only('id',
#                                                      'ticker',
#                                                      'stock_market__name',
#                                                      'asset_class__name',
#                                                      'currency_of_price__name',
#                                                      'one_unit_current_price_in_currency')
#
#     new_prices = []
#     errors_take_prices = []
#     for asset in all_assets:
#         # print('---asset:', asset.currency_of_price.name)
#         try:
#             new_price = take_price(ticker=asset.ticker,
#                                    stock_market=asset.stock_market.name,
#                                    asset_class=asset.asset_class.name,
#                                    currency=asset.currency_of_price.name)
#             print('--данные получены из new_price:', new_price)
#             asset.one_unit_current_price_in_currency = new_price
#             new_prices.append(asset)
#         except Exception as err:
#             err_msg = f"Не удалось обновить цену '{asset.ticker}' - id: {asset.id}. Ошибка: {err}"
#             errors_take_prices.append({'id': asset.id, 'name': asset.ticker, 'error': err_msg})
#
#     if new_prices:
#         with transaction.atomic():
#             print("---запускается bulk_update для цен")
#             Asset.objects.bulk_update(new_prices, ['one_unit_current_price_in_currency'])
#
#     return errors_take_prices
