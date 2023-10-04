from django.db import models
from decimal import Decimal

from src.attributes_list.models import Portfolio


class Asset(models.Model):
    ticker = models.CharField(max_length=5)
    name = models.CharField(max_length=50)
    portfolio_name = models.ForeignKey(Portfolio, on_delete=models.SET_NULL, blank=True, null=True)
    agent = models.CharField(max_length=40)  # посредник
    stock_market = models.CharField(max_length=40)
    asset_class = models.CharField(max_length=40)
    asset_type = models.CharField(max_length=40, blank=True, null=True)
    currency_of_price = models.CharField(max_length=10)  # валюта цены
    region = models.CharField(max_length=40, blank=True, null=True)
    currency_of_asset = models.CharField(max_length=10)  # валюта актива
    total_quantity = models.DecimalField(max_digits=18, decimal_places=8)
    # TODO: цена должна тянустья из таблицы, в которой будут храниться данные о ценах на все купленные активы.
    #  Эти таблицы будут обновляться с API по кнопке.
    one_unit_price_in_currency = models.DecimalField(max_digits=10, decimal_places=2)  # цена за единицу

    @property
    def total_price_in_currency(self):
        # TODO: возможно нужно будет другое округление. Так же можно перенести это в annotate во view
        # сначала переводим DecimalField в строку, а затем в Decimal, т.к. DecimalField невозможно умножать
        price = Decimal(str(self.one_unit_price_in_currency)) * Decimal(str(self.total_quantity))
        print(price)
        print(type(price))
        print(price.quantize(Decimal('.01')))
        return price
    # total_price_in_currency = models.DecimalField(max_digits=10, decimal_places=2)  # общая стоимость актива

    total_expenses_rub = models.DecimalField(max_digits=10, decimal_places=2)  # сумма затрат в RUB

    @property
    def asset_price_change_rub(self):
        # TODO: возможно нужно будет другое округление. Так же можно перенести это в annotate во view
        # сначала переводим DecimalField в строку, а затем в Decimal, т.к. DecimalField невозможно умножать
        price_change = Decimal(str(self.total_price_in_currency)) - Decimal(str(self.total_expenses_rub))
        print(price_change)
        print(type(price_change))
        print(price_change.quantize(Decimal('.01')))
        return price_change
    # asset_price_change_rub = models.DecimalField(max_digits=10, decimal_places=2)  # изменение в RUB

    @property
    def asset_price_change_percent_rub(self):
        # TODO: возможно нужно будет другое округление. Так же можно перенести это в annotate во view
        # сначала переводим DecimalField в строку, а затем в Decimal, т.к. DecimalField невозможно умножать
        price_change = Decimal(str(self.asset_price_change_rub)) / Decimal(str(self.total_expenses_rub))
        print(price_change)
        print(type(price_change))
        print(price_change.quantize(Decimal('.01')))
        return price_change
    # asset_price_change_percent_rub = models.DecimalField(max_digits=6, decimal_places=2)  # изменение в % (RUB)

    # TODO: скорее всего должны идти в другую таблицу (с доходами), а не храниться в активе
    #  актив будет просто как ForeignKey.
    # income = models.DecimalField(max_digits=10, decimal_places=2)  # дивиденды и купоны
