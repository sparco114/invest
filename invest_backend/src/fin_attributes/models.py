from django.db import models


class Portfolio(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f"id: {self.pk} - '{self.name}'"


class Agent(models.Model):
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return f"id: {self.pk} - '{self.name}'"


class StockMarket(models.Model):
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return f"id: {self.pk} - '{self.name}'"


class AssetClass(models.Model):
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return f"id: {self.pk} - '{self.name}'"


class AssetType(models.Model):
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return f"id: {self.pk} - '{self.name}'"


class Currency(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"id: {self.pk} - '{self.name}'"


class Region(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"id: {self.pk} - '{self.name}'"
