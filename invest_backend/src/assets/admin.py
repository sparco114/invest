from django.contrib import admin

from src.assets.models import Asset


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    pass
