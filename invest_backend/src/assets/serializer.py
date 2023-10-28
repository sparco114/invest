from rest_framework.serializers import ModelSerializer, ReadOnlyField, DecimalField, Serializer, \
    CharField, IntegerField

from src.assets.models import Asset


class AssetsSerializer(ModelSerializer):
    total_price_in_currency = ReadOnlyField()
    total_price_change_in_currency = ReadOnlyField()
    total_price_change_percent_in_currency = ReadOnlyField()
    total_price_in_rub = ReadOnlyField()
    total_price_change_in_rub = ReadOnlyField()
    total_price_change_percent_in_rub = ReadOnlyField()

    class Meta:
        model = Asset
        fields = '__all__'
        # fields = ['total_price_in_currency']


class AllAssetsPricesUpdateSerializer(Serializer):
    id = IntegerField()
    one_unit_current_price_in_currency = CharField()
    error = CharField()
