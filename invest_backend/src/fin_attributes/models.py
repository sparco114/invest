from django.db import models


class Portfolio(models.Model):
    name = models.CharField(max_length=30)


class Agent(models.Model):
    name = models.CharField(max_length=40)





#
# class StockMarket(models.Model):
#     name = models.CharField(max_length=40)
#
#
# class AssetClass(models.Model):
#     name = models.CharField(max_length=40)
#
#
# class AssetType(models.Model):
#     name = models.CharField(max_length=40)
#
#
# class Currency(models.Model):
#     name = models.CharField(max_length=10)
#
#
# class Region(models.Model):
#     name = models.CharField(max_length=10)
