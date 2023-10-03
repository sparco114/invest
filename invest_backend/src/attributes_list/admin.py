from django.contrib import admin

from src.attributes_list.models import Portfolio


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    pass
