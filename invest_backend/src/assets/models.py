from django.db import models
from decimal import Decimal

from src.fin_attributes.models import Portfolio, Agent, StockMarket, AssetClass, AssetType, Currency, Region


class Asset(models.Model):
    ticker = models.CharField(max_length=5)
    name = models.CharField(max_length=50)
    portfolio_name = models.ForeignKey(Portfolio, on_delete=models.SET_NULL, blank=True, null=True)
    agent = models.ForeignKey(Agent, on_delete=models.PROTECT)  # посредник
    stock_market = models.ForeignKey(StockMarket, on_delete=models.PROTECT)
    asset_class = models.ForeignKey(AssetClass, on_delete=models.PROTECT)
    asset_type = models.ForeignKey(AssetType, on_delete=models.SET_NULL, blank=True, null=True)
    currency_of_price = models.ForeignKey(Currency,
                                          on_delete=models.PROTECT,
                                          related_name='currency_of_price_in_asset')  # валюта цены
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, blank=True, null=True)
    currency_of_asset = models.ForeignKey(Currency,
                                          on_delete=models.PROTECT,
                                          related_name='currency_of_asset_in_asset')  # валюта актива
    total_quantity = models.DecimalField(max_digits=18, decimal_places=8)
    # TODO: цена должна тянустья из таблицы, в которой будут храниться данные о ценах на все купленные активы.
    #  Эти таблицы будут обновляться с API по кнопке.
    one_unit_price_in_currency = models.DecimalField(max_digits=10, decimal_places=2)  # цена за единицу

    total_expenses_in_rub = models.DecimalField(max_digits=10, decimal_places=2)  # сумма затрат в RUB
    total_expenses_in_currency = models.DecimalField(max_digits=10, decimal_places=2)  # сумма затрат в RUB

    @property
    def total_price_in_currency(self):
        # TODO: возможно нужно будет другое округление. Так же можно перенести это в annotate во view
        # сначала переводим DecimalField в строку, а затем в Decimal, т.к. DecimalField невозможно умножать
        price = Decimal(str(self.one_unit_price_in_currency)) * Decimal(str(self.total_quantity))
        print(price)
        print(type(price))
        print(price.quantize(Decimal('.01')))
        return price

    @property
    def asset_price_change_rub(self):
        # TODO: возможно нужно будет другое округление. Так же можно перенести это в annotate во view
        # сначала переводим DecimalField в строку, а затем в Decimal, т.к. DecimalField невозможно умножать
        price_change = Decimal(str(self.total_price_in_currency)) - Decimal(str(self.total_expenses_in_rub))
        print(price_change)
        print(type(price_change))
        print(price_change.quantize(Decimal('.01')))
        return price_change

    # asset_price_change_rub = models.DecimalField(max_digits=10, decimal_places=2)  # изменение в RUB

    @property
    def asset_price_change_percent_rub(self):
        # TODO: возможно нужно будет другое округление. Так же можно перенести это в annotate во view
        # сначала переводим DecimalField в строку, а затем в Decimal, т.к. DecimalField невозможно умножать
        price_change = Decimal(str(self.asset_price_change_rub)) / Decimal(str(self.total_expenses_in_rub))
        print(price_change)
        print(type(price_change))
        print(price_change.quantize(Decimal('.01')))
        return price_change
    # asset_price_change_percent_rub = models.DecimalField(max_digits=6, decimal_places=2)  # изменение в % (RUB)

    # TODO: скорее всего должны идти в другую таблицу (с доходами), а не храниться в активе
    #  актив будет просто как ForeignKey.
    # income = models.DecimalField(max_digits=10, decimal_places=2)  # дивиденды и купоны
