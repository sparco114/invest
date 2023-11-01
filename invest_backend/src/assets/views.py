import asyncio

from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from src.assets.models import Asset
from src.assets.serializer import AssetsSerializer, PricesAndRatesUpdateSerializer
from src.services.take_prices.take_prices import all_assets_prices_update_async
from src.transactions.views import full_recalculation_single_asset


class AssetsView(ModelViewSet):
    serializer_class = AssetsSerializer
    queryset = Asset.objects.all()


class UpdateAllPricesAndRatesView(mixins.ListModelMixin, GenericViewSet):
    serializer_class = PricesAndRatesUpdateSerializer

    def list(self, request, *args, **kwargs):
        # обновление курсов всех Валют в БД со сторонних сервисов
        # errors_rates_update = all_currencies_rates_update()
        rates_update_response = None

        # обновление текущих цен всех Активов в БД со сторонних сервисов
        prices_update_response = asyncio.run(all_assets_prices_update_async())
        # prices_update_response = None

        # получение обновленных цен Активов из БД
        queryset = Asset.objects.values('id', 'one_unit_current_price_in_currency')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        response_data = {'new_assets_prices': serializer.data,
                         'rates_update_response': rates_update_response,
                         'prices_update_response': prices_update_response}

        return Response(data=response_data)


class RecalculateAllAssetsDataView(mixins.ListModelMixin, GenericViewSet):
    serializer_class = PricesAndRatesUpdateSerializer

    def list(self, request, *args, **kwargs):
        all_assets = Asset.objects.all()
        errors_recalculate = []
        for asset in all_assets:
            try:
                full_recalculation_single_asset(asset=asset)
            except Exception as err:
                err_msg = f"Не удалось пересчитать данные. Ошибка: {err}"
                errors_recalculate.append({'id': asset.id, 'name': asset.name, 'error': err_msg})

        # queryset = Asset.objects.all()
        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)
        #
        # serializer = self.get_serializer(queryset, many=True)
        # return Response(serializer.data)
        response_data = "Данные Активов успешно пересчитаны"
        if errors_recalculate:
            response_data = f"Ошибки во время пересчета данных по Активам: {errors_recalculate}"
        return Response(data=response_data)
