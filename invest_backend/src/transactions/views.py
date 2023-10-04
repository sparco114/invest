import decimal

from django.db.models import Model
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from src.assets.models import Asset
from src.fin_attributes.models import Portfolio, Agent
from src.transactions.models import Transaction
from src.transactions.serializer import TransactionsSerializer


def asset_processing_create(transaction):
    """
    Поиск актива (Asset) для создаваемой операции, и обновление информации в нем, на основании этой операции.
    Если актив (Asset) не найден - создание такого актива и заполнение информацией из операции.
    :return: объект Актив (Asset)
    """
    print('СРАБОТАЛ----asset_processing_create')
    need_to_create_asset = False
    ticker = transaction.data.get('ticker')
    portfolio_name = transaction.data.get('portfolio_name') or None  # None - если прийдет пустая строка
    agent = transaction.data.get('portfolio_name')

    transaction_name = transaction.data.get('transaction_name')
    quantity = transaction.data.get('quantity')


    print('portfolio_name_____________', portfolio_name)
    print('portfolio_name_____________тип', type(portfolio_name))

    def take_price():
        """
        TODO: написать функционал
        Обращается к стороннему апи, чтобы получить стоимость актива (а так же в этот
        момент добавляться в таблицу, в которой будут храниться данные о ценах на все купленные активы.
        Эти таблицы будут обновляться с API по кнопке)
        :return: текущая цена актива
        """
        print('СРАБОТАЛ----take_price')
        return 100

    try:
        asset = Asset.objects.get(ticker=ticker,
                                  portfolio_name__name=portfolio_name,
                                  agent__name=agent,
                                  )
        print('asset--------------try', asset)
    except Asset.DoesNotExist as not_exist:
        print('DoesNotExist---=--====', not_exist)
        need_to_create_asset = True
    # except Exception as err:
    #     print("Ошибка при получении актива:", type(err), err)
    #     raise err
    else:
        print('asset--------------else', asset.__dict__)
        if transaction_name == 'buy':
            # прибавляем количество, указанное в операции к общему количеству
            asset.total_quantity += decimal.Decimal(quantity)
        if transaction_name == 'sell':
            # вычитаем количество, указанное в операции из общего количеству
            asset.total_quantity -= decimal.Decimal(quantity)
        asset.save()
        return asset

    if need_to_create_asset:
        # Создание нового актива (Asset)
        print('сработал need_to_create_asset----')

        # если в операции заполнено поле Портфель
        if portfolio_name:
            print('сработал if portfolio_name:----')

            try:
                # поиск существующего Портфеля
                portfolio_name = Portfolio.objects.get(name=portfolio_name)
                print('portfolio----поиск', portfolio_name)
            except Portfolio.DoesNotExist:
                # если Портфель не существует - создание нового
                portfolio_name = Portfolio.objects.create(name=portfolio_name)
                print('portfolio----создан', portfolio_name)

        try:
            # поиск существующего Портфеля
            agent = Agent.objects.get(name=agent)
            print('agent----поиск', agent)
        except Agent.DoesNotExist:
            # если Портфель не существует - создание нового
            agent = Agent.objects.create(name=agent)
            print('agent----создан', agent)

        new_asset = Asset.objects.create(
            ticker=ticker,
            name=transaction.data.get('asset_name'),
            portfolio_name=portfolio_name,
            agent=agent,
            stock_market=transaction.data.get('stock_market'),
            asset_class=transaction.data.get('asset_class'),
            asset_type=transaction.data.get('asset_type'),
            currency_of_price=transaction.data.get('currency_of_price'),
            region=transaction.data.get('region'),
            currency_of_asset=transaction.data.get('currency_of_asset'),
            total_quantity=transaction.data.get('quantity'),
            one_unit_price_in_currency=take_price(),
            # TODO: подумать где вычитать расходы - здесь или где-то в другм месте
            total_expenses_in_rub=transaction.data.get('total_price_in_rub'),
            total_expenses_in_currency=transaction.data.get('total_price_in_currency'),
        )
        return new_asset


def asset_processing_destroy(transaction):
    """
    Поиск актива (Asset) для удаляемой операции, и обновление информации в нем, на основании удаления операции.
    TODO: добавить уведомление, если при удалении операции получится ситуация, когда количество актива < 0
    """
    asset = transaction.ticker  # получаем объект актива
    transaction_name = transaction.transaction_name
    quantity = transaction.quantity
    print('asset--------', type(asset))

    if transaction_name == 'buy':
        # вычитаем количество, указанное в удаляемой операции из общемго количества
        asset.total_quantity -= decimal.Decimal(quantity)
    if transaction_name == 'sell':
        # прибавляем количество, указанное в удаляемой операции к общему количеству
        asset.total_quantity += decimal.Decimal(quantity)
    asset.save()
    return


class TransactionsView(ModelViewSet):
    serializer_class = TransactionsSerializer
    queryset = Transaction.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            # получаем asset или создаем, если не существет
            asset = asset_processing_create(transaction=request)
            print('asset_полученный в create++++++++', type(asset), asset, asset.__dict__)
        except Exception as err:
            print(f'Не удалось получить/создать Актив для транзакции {request.data}. Ошибка:', type(err), err)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # print('request.data----------', request.data)
        # print('asset_pk++++++++', asset_pk)
        # print('type-asset_pk++++++++', type(asset_pk))
        request_data_for_serialize = request.data.copy()
        # добавялем данные объекта (который создали/получили из БД) вместо имени(str), которое было в запросе
        print('asset.ticker========', asset.id)
        print('asset.portfolio_name========', asset.portfolio_name_id)
        print('asset.agent_id========', asset.agent_id)
        request_data_for_serialize['asset'] = asset.id
        request_data_for_serialize['portfolio_name'] = asset.portfolio_name_id
        request_data_for_serialize['agent'] = asset.agent_id
        serializer = self.get_serializer(data=request_data_for_serialize)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        print('serializer.data----', serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        asset_processing_destroy(transaction=instance)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
