from django.db import models


class Asset(models.Model):
    name = models.CharField(max_length=50, unique=True)
    total_quantity = models.DecimalField(max_digits=18, decimal_places=8)
    total_price_in_currency = models.DecimalField(max_digits=10, decimal_places=2)
    