import requests
from bs4 import BeautifulSoup
from django.db import transaction

from src.fin_attributes.models import Currency


def take_current_exchange_rate_to_rub_from_api(currency: str) -> str:
    """Получение курса валюты к рублю с moex api.
    TODO: !! добавить обработку ошибок
    :param currency: валюта, курс которой необходимо получить (USD, EUR и др.)
    :return: текущий курс валюты к рублю
    """
    if currency == 'RUB':
        return "1.0"

    url_rate_to_rub = f"https://iss.moex.com/iss/statistics/engines/futures/markets/indicativerates" \
                      f"/securities/{currency}/RUB.xml?iss.meta=off&iss.only=securities%2Ecurrent"
    req_rate = requests.get(url_rate_to_rub)
    bs_req_rate = BeautifulSoup(markup=req_rate.content, features="xml")
    rate = bs_req_rate.find("row")['rate']
    if not rate:
        raise ValueError(f"Ошибка, не удалось получить курс для '{currency}'. "
                         f"Адрес запроса - '{url_rate_to_rub}'")
    print(rate)
    return rate


def take_current_exchange_rate_to_rub_from_db(currency: str) -> str:
    """Получение курса валюты к рублю из модели Currency(fin_attributes).
    TODO: !! добавить обработку ошибок
    :param currency: валюта, курс которой необходимо получить (USD, EUR и др.)
    :return: курс валюты к рублю, сохраненный в БД
    """
    if currency == 'RUB':
        return "1.0"
    # print('СРАБОТАЛ --- take_current_exchange_rate_to_rub_from_db')
    rate = Currency.objects.get(name=currency).rate_to_rub
    # print("---rate---take_current_exchange_rate_to_rub_from_db", rate)
    # print(type(rate))
    # print(rate)
    return str(rate)


def all_currencies_rates_update() -> list:
    all_currencies = Currency.objects.all()
    updated_currencies = []
    errors_take_rates = []
    for currency in all_currencies:
        try:
            new_rate = take_current_exchange_rate_to_rub_from_api(currency.name)

            currency.rate_to_rub = new_rate
            updated_currencies.append(currency)
            print('---currency[name]', currency.name, new_rate)

        except Exception as err:
            err_msg = f"Не удалось обновить курс '{currency.name}' - id: {currency.id}. Ошибка: {err}"
            print(err_msg)
            errors_take_rates.append({'id': currency.id, 'name': currency.name, 'error': err_msg})

    if updated_currencies:
        with transaction.atomic():
            print("---запускается bulk_update для курсов")
            Currency.objects.bulk_update(objs=updated_currencies, fields=['rate_to_rub'])

    return errors_take_rates
