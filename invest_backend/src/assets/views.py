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
from src.assets.serializer import AssetsSerializer, PricesAndRatesUpdateSerializer
from src.fin_attributes.models import Currency
from src.services.take_exchange_rates import all_currencies_rates_update
from src.services.take_prices.take_prices import take_price


class AssetsView(ModelViewSet):
    serializer_class = AssetsSerializer
    queryset = Asset.objects.all()


class PricesAndRatesUpdateView(mixins.ListModelMixin, GenericViewSet):
    serializer_class = PricesAndRatesUpdateSerializer

    def list(self, request, *args, **kwargs):

        errors_rate_update = all_currencies_rates_update()

        queryset = Asset.objects.values('id', 'one_unit_current_price_in_currency')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        response_data = {'rates': serializer.data}
        if errors_rate_update:
            response_data['errors'] = errors_rate_update

        return Response(data=response_data)




# class PricesAndRatesUpdateView(mixins.ListModelMixin, GenericViewSet):
#     serializer_class = AllAssetsPricesUpdateSerializer
#
#     queryset = Asset.objects.values('id',
#                                     'ticker',
#                                     'stock_market__name',
#                                     'asset_class__name',
#                                     'currency_of_price__name',
#                                     'one_unit_current_price_in_currency')
#
#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#
#         new_prices = []
#         for asset in queryset:
#             print(asset.get('id'))
#             print(asset.get('ticker'))
#             print(asset.get('stock_market__name'))
#             print(asset.get('asset_class__name'))
#             print(asset.get('currency_of_price__name'))
#             try:
#                 new_price = take_price(ticker=asset.get('ticker'),
#                                        stock_market=asset.get('stock_market__name'),
#                                        asset_class=asset.get('asset_class__name'),
#                                        currency=asset.get('currency_of_price__name'))
#                 new_prices.append({'id': asset['id'],
#                                    'one_unit_current_price_in_currency': new_price,
#                                    'error': None})
#
#             except Exception as err:
#                 err_msg = f"Не удалось обновить цену актива '{asset['ticker']}' - id: '{asset['id']}'. " \
#                           f"Ошибка: {err}"
#                 new_prices.append({'id': asset['id'],
#                                    'one_unit_current_price_in_currency':
#                                        asset['one_unit_current_price_in_currency'],
#                                    'error': err_msg})
#
#                 # TODO: !! выводить пользователю на сайт
#
#         # print('---new_prices:', new_prices)
#
#
#
#         page = self.paginate_queryset(new_prices)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)
#
#         serializer = self.get_serializer(new_prices, many=True)
#         return Response(serializer.data)






# class OneAssetPriceUpdateView(mixins.RetrieveModelMixin, GenericViewSet):
#     serializer_class = AssetsSerializer
#
#     def get_object(self):
#         pk = self.kwargs['pk']
#         try:
#             return Asset.objects.get(pk=pk)
#         except Asset.DoesNotExist:
#             raise NotFound(f"Актив с id '{pk}' не найден")
#
#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#
#         new_price = take_price(ticker=instance.ticker,
#                                stock_market=instance.stock_market.name,
#                                asset_class=instance.asset_class.name,
#                                currency=instance.currency_of_price.name)
#
#         instance.one_unit_current_price_in_currency = new_price
#         instance.save()
#
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)

