from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from src.assets.models import Asset
from src.assets.serializer import AssetsSerializer


class AssetsView(ModelViewSet):
    serializer_class = AssetsSerializer
    queryset = Asset.objects.all()

# class AssetsRefreshPricesView()
