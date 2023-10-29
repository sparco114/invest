"""conf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from src.assets.views import AssetsView, AllPricesAndRatesUpdateView
from src.transactions.views import TransactionsView

router = SimpleRouter()

router.register(r'api/v1/assets', AssetsView)
router.register(r'api/v1/transactions', TransactionsView)
# router.register(r'api/v1/update_one_asset_price', OneAssetPriceUpdateView, basename="one_asset_price_update")
router.register(r'api/v1/update_all_assets_prices', AllPricesAndRatesUpdateView,
                basename="all_asset_price_update")

# router.register(r'api/v1/assets/update_prices', AssetsUpdatePricesView, basename="sss")
# router.register(r'api/v1/assets/recalculation', )
# router.register(r'api/v1/assets/update_data', )

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    # path('api/v1/update_all_assets_prices/', PricesAndRatesUpdateView.as_view()),
    # path('api/v1/update_assets_prices/<int:pk>/', OneAssetPriceUpdateView.as_view({'get': 'retrieve'})),

    # path('api/v1/', include('src.api_urls')),
    path('api/v1/djoser_auth/', include('djoser.urls')),
    path('api/v1/djoser_token/', include('djoser.urls.authtoken')),
]

urlpatterns += router.urls
