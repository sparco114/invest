from django.db import models


class Portfolio(models.Model):
    name = models.CharField(max_length=30, unique=True)


class Agent(models.Model):
    name = models.CharField(max_length=40, unique=True)


class StockMarket(models.Model):
    name = models.CharField(max_length=40, unique=True)


class AssetClass(models.Model):
    name = models.CharField(max_length=40, unique=True)


class AssetType(models.Model):
    name = models.CharField(max_length=40, unique=True)


class Currency(models.Model):
    name = models.CharField(max_length=10, unique=True)


class Region(models.Model):
    name = models.CharField(max_length=10, unique=True)
