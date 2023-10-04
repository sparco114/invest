from django.db import models

from src.assets.models import Asset
from src.fin_attributes.models import Portfolio, Agent


class Transaction(models.Model):
    TRANSACTION_NAMES = [
        ('buy', 'Покупка'),
        ('sell', 'Продажа'),
        # TODO: для валюты нужны дополнительно операции 'Пополнение', 'Снятие/Расход'
    ]

    date = models.DateField()
    transaction_name = models.CharField(max_length=20, choices=TRANSACTION_NAMES)
    ticker = models.CharField(max_length=5)
    asset = models.ForeignKey(Asset, max_length=5, on_delete=models.CASCADE)
    asset_name = models.CharField(max_length=40)
    portfolio_name = models.ForeignKey(Portfolio, on_delete=models.SET_NULL, blank=True, null=True)
    agent = models.ForeignKey(Agent, on_delete=models.PROTECT)  # посредник
    stock_market = models.CharField(max_length=40)
    asset_class = models.CharField(max_length=40)  # класс актива (акции, облигации, крипта и тд)
    asset_type = models.CharField(max_length=40, blank=True, null=True)  # вид актива (корпоративные, ОФЗ и тд)
    currency_of_price = models.CharField(max_length=10)  # валюта цены
    region = models.CharField(max_length=40, blank=True, null=True)
    currency_of_asset = models.CharField(max_length=10)  # валюта актива
    quantity = models.DecimalField(max_digits=18, decimal_places=8)
    one_unit_price_in_currency = models.DecimalField(max_digits=10, decimal_places=2)  # цена за единицу

    # TODO: написать на фронте логику, чтоб при заполнении one_unit_price_in_currency и quantity
    #  автоматически вычислялся и подставлялся результат в поле total_price_in_currency
    total_price_in_currency = models.DecimalField(max_digits=18, decimal_places=8)  # общая стоимость актива

    # TODO: скорее всего должны идти в другую таблицу (с расходами), а не в актив
    # TODO: должны прибавляться к общим затратам на актив?
    deductions = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)  # удержания

    currency_rate_to_rub = models.DecimalField(max_digits=8, decimal_places=2)  # текущий курс валюты к руб

    # TODO: написать на фронте логику, чтоб при заполнении total_price_in_currency и currency_rate_to_rub
    #  автоматически вычислялся и подставлялся результат в поле total_price_in_rub
    total_price_in_rub = models.DecimalField(max_digits=18, decimal_places=8)

    # TODO: написать на фронте логику, чтоб при заполнении deductions и currency_rate_to_rub
    #  автоматически вычислялся и подставлялся результат в поле deductions_in_rub
    deductions_in_rub = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)







