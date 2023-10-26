import requests
from bs4 import BeautifulSoup

from src.fin_attributes.models import Currency


def take_current_exchange_rate_to_rub_from_api(currency: str) -> str:
    """Получение курса валюты к рублю с moex api.
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
    print(rate)
    return rate


# currency = "USD"
# take_current_exchange_rate_to_rub(currency)

def take_current_exchange_rate_to_rub_from_db(currency: str) -> str:
    """Получение курса валюты к рублю из модели Currency(fin_attributes).
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

