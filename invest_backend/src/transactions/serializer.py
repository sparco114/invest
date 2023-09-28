from rest_framework.serializers import ModelSerializer

from src.transactions.models import Transaction


class TransactionsSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
