from django.db import models

from src.assets.models import Asset


class Transaction(models.Model):
    OPERATION_NAMES = [
        ('buy', 'Покупка'),
        ('sell', 'Продажа'),
        ('transfer', 'Перевод'),
    ]

    transaction_name = models.CharField(max_length=20, choices=OPERATION_NAMES)
    quantity = models.DecimalField(max_digits=18, decimal_places=8)
    price_in_currency = models.DecimalField(max_digits=10, decimal_places=2)  # цена в валюте
    asset_name = models.ForeignKey(Asset, max_length=5, on_delete=models.CASCADE)

    # date = models.DateField()
    # portfolio_name = models.CharField(max_length=20)
    # agent = models.CharField(max_length=40)  # посредник
    # stock_market = models.CharField(max_length=40)
    # asset_class = models.CharField(max_length=40)
    # asset_type = models.CharField(max_length=40)
    # currency_of_price = models.CharField(max_length=10)  # валюта цены
    # region = models.CharField(max_length=40)
    # currency_of_asset = models.CharField(max_length=10)  # валюта актива
    # ticker = models.CharField(max_length=5)
    # deductions = models.DecimalField(max_digits=8, decimal_places=2)  # удержания
    # currency_rate_to_rub = models.DecimalField(max_digits=8, decimal_places=2)
    # sum_in_currency = models.DecimalField(max_digits=18, decimal_places=8)
    # sum_in_rub = models.DecimalField(max_digits=18, decimal_places=8)
    # deductions_in_rub = models.DecimalField(max_digits=8, decimal_places=2)  # удержания в руб







