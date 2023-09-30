import decimal

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from src.assets.models import Asset
from src.transactions.models import Transaction
from src.transactions.serializer import TransactionsSerializer


def asset_processing_create(transaction):
    """
    Поиск актива (Asset) для создаваемой операции, и обновление информации в нем, на основании этой операции.
    Если актив (Asset) не найден - создание такого актива и заполнение информацией из операции.
    """
    print('СРАБОТАЛ----asset_processing_create')
    ticker = transaction.data.get('ticker')
    transaction_name = transaction.data.get('transaction_name')
    quantity = transaction.data.get('quantity')
    print('ticker - в - asset_processing_create')

    def take_price():
        """
        TODO: написать функционал
        Обращается к стороннему апи, чтобы получить стоимость актива, а так же добавляет (а так же в этот
        момент добавляться в таблицу, в которой будут храниться данные о ценах на все купленные активы.
        Эти таблицы будут обновляться с API по кнопке)
        :return: текущая цена актива
        """
        print('СРАБОТАЛ----take_price')
        return 100

    asset, created = Asset.objects.get_or_create(
        ticker=ticker,
        # defaults применится только если актив не найден (сработал create)
        defaults={
            'name': transaction.data.get('asset_name'),
            'portfolio_name': transaction.data.get('portfolio_name'),
            'agent': transaction.data.get('agent'),
            'stock_market': transaction.data.get('stock_market'),
            'asset_class': transaction.data.get('asset_class'),
            'asset_type': transaction.data.get('asset_type'),
            'currency_of_price': transaction.data.get('currency_of_price'),
            'region': transaction.data.get('region'),
            'currency_of_asset': transaction.data.get('currency_of_asset'),
            'total_quantity': transaction.data.get('quantity'),
            'one_unit_price_in_currency': take_price(),  # берем актуальную цену со стороннего API
            'total_expenses_rub': transaction.data.get('total_price_in_currency'),  # общие затраты
        })
    print('created---------', created)
    print('asset------', asset)
    print('asset.one_unit_price_in_currency------', asset.one_unit_price_in_currency)
    if not created:
        # если объект найден (т.е. сработал get)
        if transaction_name == 'buy':
            # прибавляем количество, указанное в операции к общему количеству
            asset.total_quantity += decimal.Decimal(quantity)
        if transaction_name == 'sell':
            # вычитаем количество, указанное в операции из общего количеству
            asset.total_quantity -= decimal.Decimal(quantity)
    asset.save()
    print('возвращаем type(asset.pk)', type(asset.pk))
    return asset.pk


def asset_processing_destroy(transaction):
    """
    Поиск актива (Asset) для удаляемой операции, и обновление информации в нем, на основании удаления операции.
    """
    asset = transaction.asset_name  # получаем объект актива
    transaction_name = transaction.transaction_name
    quantity = transaction.quantity

    if transaction_name == 'buy':
        # вычитаем количество, указанное в удаляемой операции из общемго количества
        asset.total_quantity -= decimal.Decimal(quantity)
    if transaction_name == 'sell':
        # прибавляем количество, указанное в удаляемой операции к общему количеству
        asset.total_quantity += decimal.Decimal(quantity)
    asset.save()
    return


# TODO: добавить логику удаления актива, если его количество == 0
class TransactionsView(ModelViewSet):
    serializer_class = TransactionsSerializer
    queryset = Transaction.objects.all()

    def create(self, request, *args, **kwargs):
        # получаем asset или создаем, если не существет
        print('request.data----------', request.data)
        asset_pk = asset_processing_create(transaction=request)
        print('asset_pk++++++++', asset_pk)
        print('type-asset_pk++++++++', type(asset_pk))
        request_data_for_serialize = request.data.copy()
        # добавялем pk объекта (который создали/получили из БД) вместо имени(str), которое получили в запросе
        request_data_for_serialize['ticker'] = asset_pk
        serializer = self.get_serializer(data=request_data_for_serialize)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        asset_processing_destroy(transaction=instance)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
