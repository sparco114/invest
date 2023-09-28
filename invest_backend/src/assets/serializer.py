from rest_framework.serializers import ModelSerializer

from src.assets.models import Asset


class AssetsSerializer(ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'
