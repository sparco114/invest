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
    transaction_name = transaction.data.get('transaction_name')
    asset_name = transaction.data.get('asset_name')
    quantity = transaction.data.get('quantity')
    price_in_currency = transaction.data.get('price_in_currency')
    asset, created = Asset.objects.get_or_create(name=asset_name,
                                                 # defaults применится только если актив не найден (сработал create)
                                                 defaults={
                                                     'total_quantity': quantity,
                                                     'total_price_in_currency': price_in_currency
                                                 })
    if not created:
        # если объект найден (т.е. сработал get)
        if transaction_name == 'buy':
            # прибавляем количество, указанное в операции к общему количеству
            asset.total_quantity += decimal.Decimal(quantity)
        if transaction_name == 'sell':
            # вычитаем количество, указанное в операции из общего количеству
            asset.total_quantity -= decimal.Decimal(quantity)
    asset.save()
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
        asset_pk = asset_processing_create(transaction=request)
        request_data_for_serialize = request.data.copy()
        # добавялем pk объекта (который создали/получили из БД) вместо имени(str), которое получили в запросе
        request_data_for_serialize['asset_name'] = asset_pk
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
