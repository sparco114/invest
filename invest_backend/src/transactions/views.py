from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from src.assets.models import Asset
from src.transactions.models import Transaction
from src.transactions.serializer import TransactionsSerializer


class TransactionsView(ModelViewSet):
    serializer_class = TransactionsSerializer
    queryset = Transaction.objects.all()

    def asset_processing(self, request):
        asset_name = request.data['asset_name']
        print('asset_name++++++++++++++++++++++++++:', asset_name)
        quantity = request.data['quantity']
        price_in_currency = request.data['price_in_currency']
        asset, created = Asset.objects.update_or_create(name=asset_name,
                                                        defaults={
                                                            'total_quantity': quantity,
                                                            'total_price_in_currency': price_in_currency
                                                        })

        print('asset__________________BEFORE', asset.name)

        return asset

    def create(self, request, *args, **kwargs):
        print('request----------------', request)
        asset = self.asset_processing(request)
        request.data['asset_name'] = asset
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

