import json

import requests
from django.shortcuts import render
from rest_framework import mixins, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from src.assets.models import Asset
from src.assets.serializer import AssetsSerializer
from src.services.take_prices.take_prices import take_price


class AssetsView(ModelViewSet):
    serializer_class = AssetsSerializer
    queryset = Asset.objects.all()


class OneAssetPriceUpdateView(mixins.ListModelMixin, GenericViewSet):
    serializer_class = AssetsSerializer

    def get_object(self):
        pk = self.kwargs['pk']
        try:
            return Asset.objects.get(pk=pk)
        except Asset.DoesNotExist:
            raise NotFound(f"Актив с id '{pk}' не найден")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        new_price = take_price(ticker=instance.ticker,
                               stock_market=instance.stock_market.name,
                               asset_class=instance.asset_class.name,
                               currency=instance.currency_of_price.name)

        instance.one_unit_current_price_in_currency = new_price
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

# class AllAssetsRefreshPricesView()
