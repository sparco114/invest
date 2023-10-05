from django.contrib import admin

from src.fin_attributes.models import Portfolio, Agent, StockMarket, AssetClass, AssetType, Currency, Region


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    pass


@admin.register(StockMarket)
class StockMarketAdmin(admin.ModelAdmin):
    pass


@admin.register(AssetClass)
class AssetClassAdmin(admin.ModelAdmin):
    pass


@admin.register(AssetType)
class AssetTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    pass
