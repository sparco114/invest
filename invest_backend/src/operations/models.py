from django.db import models


class Operation(models.Model):
    date = models.DateField()
    operation_name = models.CharField(max_length=20)
    portfolio_name = models.CharField(max_length=20)
    agent = models.CharField(max_length=40)  # посредник
    stock_market = models.CharField(max_length=40)
    asset_class = models.CharField(max_length=40)
    asset_type = models.CharField(max_length=40)
    currency_of_price = models.CharField(max_length=10)  # валюта цены
    region = models.CharField(max_length=40)
    currency_of_asset = models.CharField(max_length=10)  # валюта актива
    ticker = models.CharField(max_length=5)
    amount = models.DecimalField(max_digits=18, decimal_places=8)
    price_in_currency = models.DecimalField(max_digits=10, decimal_places=2)  # цена в валюте
    deductions = models.DecimalField(max_digits=8, decimal_places=2)  # удержания
    currency_rate_to_rub = models.DecimalField(max_digits=8, decimal_places=2)
    sum_in_currency = models.DecimalField(max_digits=18, decimal_places=8)
    sum_in_rub = models.DecimalField(max_digits=18, decimal_places=8)
    deductions_in_rub = models.DecimalField(max_digits=8, decimal_places=2)  # удержания в руб







