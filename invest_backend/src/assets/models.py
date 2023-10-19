from django.db import models
from decimal import Decimal

from src.fin_attributes.models import Portfolio, Agent, StockMarket, AssetClass, AssetType, Currency, Region


# TODO: подумать есть ли смысл брать курс прямо на текущий момент, если стоимости акций будут взяты из таблицы,
#   то есть их стоимости будут на какой-то другой момент. Или  лучше курс тоже записывать в ту же таблицу,
#   и обновлять одновременно и курс, и стоимости акций.
def take_current_currency_rate_to_rub():
    """
    TODO: написать функционал
    Обращается к стороннему апи, чтобы получить курс рубля к валюте (а так же в этот
    момент добавляться в таблицу, в которой будут храниться данные о ценах активов и курсах валют.
    Эти таблицы будут обновляться с API по кнопке)
    :return: текущий курс рубля к валюте
    """
    print('СРАБОТАЛ --- take_current_currency_rate_to_rub')
    return 4


class Asset(models.Model):
    # TODO: подумать нужно ли здесь тоже добавить поля 'дата создания' и 'дата последнего изменения'
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
    one_unit_current_price_in_currency = models.DecimalField(max_digits=10, decimal_places=2)  # цена за единицу

    total_expenses_in_currency = models.DecimalField(max_digits=10, decimal_places=2)  # сумма затрат в RUB
    total_expenses_in_rub = models.DecimalField(max_digits=10, decimal_places=2)  # сумма затрат в RUB
    average_buying_price_of_one_unit_in_currency = models.DecimalField(max_digits=10, decimal_places=2)
    average_buying_price_of_one_unit_in_rub = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price_in_currency(self):
        # TODO: возможно нужно будет другое округление. Так же можно перенести это в annotate во view
        # сначала переводим DecimalField в строку, а затем в Decimal, т.к. DecimalField невозможно умножать
        price = Decimal(str(self.one_unit_current_price_in_currency)) * Decimal(str(self.total_quantity))
        print(price)
        print(type(price))
        print(price.quantize(Decimal('.01')))
        return price

    @property
    def total_price_change_in_currency(self):
        # TODO: возможно нужно будет другое округление. Так же можно перенести это в annotate во view
        # сначала переводим DecimalField в строку, а затем в Decimal, т.к. DecimalField невозможно умножать
        price_change = Decimal(str(self.total_price_in_currency)) - Decimal(str(self.total_expenses_in_currency))
        print(price_change)
        print(type(price_change))
        print(price_change.quantize(Decimal('.01')))
        return price_change

    # asset_price_change_rub = models.DecimalField(max_digits=10, decimal_places=2)  # изменение в RUB

    @property
    def total_price_change_percent_in_currency(self):
        # TODO: возможно нужно будет другое округление. Так же можно перенести это в annotate во view
        # сначала переводим DecimalField в строку, а затем в Decimal, т.к. DecimalField невозможно умножать
        if self.total_expenses_in_currency:
            price_change = Decimal(str(self.total_price_change_in_currency)) / Decimal(str(
                self.total_expenses_in_currency)) * Decimal(100)
            print(price_change)
            print(type(price_change))
            print(price_change.quantize(Decimal('.01')))
        else:
            price_change = 0
        return price_change.quantize(Decimal('.01'))

    @property
    def total_price_in_rub(self):
        # TODO: возможно нужно будет другое округление. Так же можно перенести это в annotate во view
        # сначала переводим DecimalField в строку, а затем в Decimal, т.к. DecimalField невозможно умножать
        price = Decimal(str(self.one_unit_current_price_in_currency)) * Decimal(str(self.total_quantity)) * Decimal(str(
            take_current_currency_rate_to_rub()))
        print(price)
        print(type(price))
        print(price.quantize(Decimal('.01')))
        return price

    @property
    def total_price_change_in_rub(self):
        # TODO: возможно нужно будет другое округление. Так же можно перенести это в annotate во view
        # сначала переводим DecimalField в строку, а затем в Decimal, т.к. DecimalField невозможно умножать
        price_change = Decimal(str(self.total_price_in_rub)) - Decimal(str(self.total_expenses_in_rub))
        print(price_change)
        print(type(price_change))
        print(price_change.quantize(Decimal('.01')))
        return price_change

    @property
    def total_price_change_percent_in_rub(self):
        # TODO: возможно нужно будет другое округление. Так же можно перенести это в annotate во view
        # сначала переводим DecimalField в строку, а затем в Decimal, т.к. DecimalField невозможно умножать
        if self.total_expenses_in_rub:
            price_change = (Decimal(str(self.total_price_change_in_rub))
                            / Decimal(str(self.total_expenses_in_rub))
                            * Decimal(100))
            print(price_change)
            print(type(price_change))
            print(price_change.quantize(Decimal('.01')))
        else:
            price_change = 0
        return price_change.quantize(Decimal('.01'))

    # asset_price_change_percent_rub = models.DecimalField(max_digits=6, decimal_places=2)  # изменение в % (RUB)

    # TODO: скорее всего должны идти в другую таблицу (с доходами), а не храниться в активе
    #  актив будет просто как ForeignKey.
    # income = models.DecimalField(max_digits=10, decimal_places=2)  # дивиденды и купоны

    def __str__(self):
        return f"id: {self.pk} - '{self.ticker}'"
