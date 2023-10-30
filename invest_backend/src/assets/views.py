import asyncio

from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

# from probe import all_assets_prices_update_probe
from src.assets.models import Asset
from src.assets.serializer import AssetsSerializer, PricesAndRatesUpdateSerializer
from src.services.take_exchange_rates import all_currencies_rates_update
from src.services.take_prices.take_prices import all_assets_prices_update
from src.transactions.views import full_recalculation_single_asset


class AssetsView(ModelViewSet):
    serializer_class = AssetsSerializer
    queryset = Asset.objects.all()


class UpdateAllPricesAndRatesView(mixins.ListModelMixin, GenericViewSet):
    serializer_class = PricesAndRatesUpdateSerializer

    def list(self, request, *args, **kwargs):

        errors_rates_update = all_currencies_rates_update()
        # errors_rates_update = None

        errors_prices_update = all_assets_prices_update()
        # errors_prices_update = None

        # print("---Начало update_data")
        # asyncio.run(all_assets_prices_update_probe())
        # print("---Конец update_data")



        queryset = Asset.objects.values('id', 'one_unit_current_price_in_currency')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        response_data = {'rates': serializer.data}

        if errors_rates_update:
            response_data['errors_rates_update'] = errors_rates_update

        if errors_prices_update:
            response_data['errors_prices_update'] = errors_prices_update

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


