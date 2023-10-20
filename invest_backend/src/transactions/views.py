import decimal
import pandas as pd
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from src.assets.models import Asset
from src.fin_attributes.models import Portfolio, Agent, StockMarket, AssetClass, AssetType, Currency, Region
from src.transactions.models import Transaction
from src.transactions.serializer import TransactionsSerializer


def processing_asset_when_transaction_create(transaction):
    """
    Поиск актива (Asset) для создаваемой транзакции (Transaction), и обновление в нем данных, на основании
    этой транзакции. Если Актив не найден - создание такого Актива и заполнение данными из транзакции, которые
    получены в post запросе.

    :param transaction: Полученный post запрос с данными, которые необходимы для создания новой транзакции
    :type transaction: rest_framework.request.Request

    :raises DoesNotExist: Если Актив не найден в БД и при этом создаваемая транзакция уменьшает количество Актива
    :raises NegativeAssetQuantityError: Если создаваемая транзакция приводит к тому, что количество Актива
        становится отрицательным

    :return: Созданный или обновленный с учетом транзакции Актив
    :rtype: Объект Asset
    """
    print('СРАБОТАЛ----asset_processing_create')
    print(type(transaction))
    need_to_create_asset = False
    transaction_ticker = transaction.data.get('ticker')
    transaction_portfolio_name = transaction.data.get('portfolio_name') or None  # None - если придет пустая строка
    transaction_agent = transaction.data.get('agent')
    transaction_stock_market = transaction.data.get('stock_market')
    transaction_asset_class = transaction.data.get('asset_class')
    transaction_asset_type = transaction.data.get('asset_type') or None  # None - если придет пустая строка
    transaction_currency_of_price = transaction.data.get('currency_of_price')
    transaction_region = transaction.data.get('region') or None  # None - если придет пустая строка
    transaction_currency_of_asset = transaction.data.get('currency_of_asset')

    transaction_name = transaction.data.get('name')
    transaction_quantity = transaction.data.get('quantity')
    transaction_total_price_in_currency = transaction.data.get('total_price_in_currency')
    transaction_total_price_in_rub = transaction.data.get('total_price_in_rub')

    # print('ДО')
    # print(type(decimal.Decimal(quantity)))
    # aaa = decimal.Decimal(total_price_in_rub) / decimal.Decimal(quantity)
    # print(type(decimal.Decimal(str(total_price_in_rub))))
    # print('aaa-------', aaa)
    # return
    # print('portfolio_name_____________', portfolio_name)
    # print('portfolio_name_____________тип', type(portfolio_name))

    def take_price() -> float:
        """
        TODO: написать функционал, возможно необходимо вынести эту функцию из asset_processing_create
        Обращается к стороннему апи, чтобы получить стоимость актива (а так же в этот
        момент добавляться в таблицу, в которой будут храниться данные о ценах на все купленные активы.
        Эти таблицы будут обновляться с API по кнопке)
        :return: текущая цена актива
        """
        print('СРАБОТАЛ----take_price')
        return 300.0

    # проверяем по данным из полученной в запросе транзакции существует ли Актив с такими данными
    try:
        asset = Asset.objects.get(ticker=transaction_ticker,
                                  portfolio_name__name=transaction_portfolio_name,
                                  agent__name=transaction_agent,
                                  stock_market__name=transaction_stock_market,
                                  asset_class__name=transaction_asset_class,
                                  asset_type__name=transaction_asset_type,
                                  currency_of_price__name=transaction_currency_of_price,
                                  region__name=transaction_region,
                                  currency_of_asset__name=transaction_currency_of_asset,
                                  )
        print('asset--------------try', asset)

    except Asset.DoesNotExist as err:
        # print('DoesNotExist---=--====', not_exist)

        # если актив не найден и создаваемая операция увеличивает или не изменяет количество Актива,
        #  то ставим маркер в True, что нужно создать новый Актив
        if transaction_name == 'buy':
            need_to_create_asset = True

        # для остальных операций (которые уменьшают количество Актива) поднимаем эту ошибку и информируем о том,
        #  что количество актива получается отрицательным
        else:
            raise err

    # except Exception as err:
    #     print("Ошибка при получении актива:", type(err), err)
    #     raise err

    # если Актив найден или стоит маркер (True) о необходимости создать Актив
    else:
        # print('asset--------------else', asset.__dict__)
        if transaction_name == 'buy':
            asset.total_quantity += decimal.Decimal(transaction_quantity)
            asset.total_expenses_in_currency += decimal.Decimal(transaction_total_price_in_currency)
            asset.total_expenses_in_rub += decimal.Decimal(transaction_total_price_in_rub)

            # TODO: возможно эти два поля можно перенести в модель и сделать рассчитываемыми (property)
            asset.average_buying_price_of_one_unit_in_currency = (asset.total_expenses_in_currency
                                                                  / asset.total_quantity)
            asset.average_buying_price_of_one_unit_in_rub = (asset.total_expenses_in_rub
                                                             / asset.total_quantity)

        if transaction_name == 'sell':

            # если количество актива 0, то операция продажи невозможна, поднимаем ошибку
            if asset.total_quantity == 0:  # количество актива ДО пересчета
                raise NegativeAssetQuantityError("Невозможно продать Актив, количество которого 0")
            asset_total_quantity_old_value = asset.total_quantity  # используется только для сообщения об ошибке

            # asset.total_expenses_in_currency -= (asset.average_buying_price_of_one_unit_in_currency
            #                                      * decimal.Decimal(quantity))
            # asset.total_expenses_in_rub -= (asset.average_buying_price_of_one_unit_in_rub
            #                                 * decimal.Decimal(quantity))

            # новый способ расчета, чтоб при продаже всего имеющегося количества актива сумма затрат становилась 0,
            #   т.к. при старом способе из-за округления оставался остаток в копейках
            asset.total_expenses_in_currency -= ((asset.total_expenses_in_currency / asset.total_quantity)
                                                 * decimal.Decimal(transaction_quantity))
            asset.total_expenses_in_rub -= ((asset.total_expenses_in_rub / asset.total_quantity)
                                            * decimal.Decimal(transaction_quantity))

            asset.total_quantity -= decimal.Decimal(transaction_quantity)

            # если после продажи количество актива будет 0, то обнуляем так же среднюю стоимость
            #  (в ином случае ее просто не меняем)
            if asset.total_quantity == 0:  # количество актива ПОСЛЕ пересчета
                asset.average_buying_price_of_one_unit_in_currency = 0
                asset.average_buying_price_of_one_unit_in_rub = 0
            elif asset.total_quantity < 0:  # количество актива ПОСЛЕ пересчета
                raise NegativeAssetQuantityError(f"Невозможно продать указанное количество Актива "
                                                 f"({transaction_quantity} единиц), т.к. в наличии "
                                                 f"только {asset_total_quantity_old_value}")

        asset.save()
        return asset  # возвращаем Актив с обновленными данными

    # Создание нового Актива, если он не найден, а текущая транзакция увеличивает или не изменяет его количество
    if need_to_create_asset:
        print('сработал need_to_create_asset----')

        # если в операции заполнено поле Портфель (иначе останется None)
        if transaction_portfolio_name:
            transaction_portfolio_name, portfolio_created = Portfolio.objects.get_or_create(
                name=transaction_portfolio_name)

        transaction_agent, agent_created = Agent.objects.get_or_create(name=transaction_agent)
        print('agent----', transaction_agent)

        transaction_stock_market, stock_market_created = StockMarket.objects.get_or_create(
            name=transaction_stock_market)
        print('stock_market----', transaction_stock_market)

        transaction_asset_class, asset_class_created = AssetClass.objects.get_or_create(name=transaction_asset_class)
        print('asset_class----', transaction_asset_class)

        # если в операции заполнено поле Вид актива (иначе останется None)
        if transaction_asset_type:
            transaction_asset_type, asset_type_created = AssetType.objects.get_or_create(name=transaction_asset_type)
            print('asset_type----', transaction_asset_type)

        # если валюта цены и валюта покупки одинаковая - то создаем валюту в БД один раз
        if transaction_currency_of_price == transaction_currency_of_asset:
            transaction_currency_of_price, currency_of_price_created = Currency.objects.get_or_create(
                name=transaction_currency_of_price)
            print('currency_of_price----', transaction_currency_of_price)
            transaction_currency_of_asset = transaction_currency_of_price

        # если валюта цены и валюта покупки различается - то создаем в БД каждую по отдельности
        else:
            transaction_currency_of_price, currency_of_price_created = Currency.objects.get_or_create(
                name=transaction_currency_of_price)
            print('currency_of_price----', transaction_currency_of_price)
            transaction_currency_of_asset, currency_of_asset_created = Currency.objects.get_or_create(
                name=transaction_currency_of_asset)
            print('currency_of_asset----', transaction_currency_of_asset)

        # если в операции заполнено поле Регион (иначе останется None)
        if transaction_region:
            transaction_region, currency_created = Region.objects.get_or_create(name=transaction_region)
            print('region----', transaction_region)

        # TODO: Добавить условие удаления созданных fin_attributes, если при создании актива будет ошибка
        new_asset = Asset.objects.create(
            ticker=transaction_ticker,

            # выше, при поиске актива не используем поле name (asset_name), потому что наименование (компании)
            # может измениться, в этом случае будет просто записано новое название, полученное в запросе
            name=transaction.data.get('asset_name'),
            portfolio_name=transaction_portfolio_name,
            agent=transaction_agent,
            stock_market=transaction_stock_market,
            asset_class=transaction_asset_class,
            asset_type=transaction_asset_type,
            currency_of_price=transaction_currency_of_price,
            region=transaction_region,
            currency_of_asset=transaction_currency_of_asset,
            total_quantity=transaction_quantity,
            one_unit_current_price_in_currency=take_price(),
            # TODO: подумать где вычитать расходы - здесь или где-то в другом месте
            total_expenses_in_currency=transaction_total_price_in_currency,
            total_expenses_in_rub=transaction_total_price_in_rub,
            average_buying_price_of_one_unit_in_currency=transaction.data.get(
                'one_unit_buying_price_in_currency'),
            average_buying_price_of_one_unit_in_rub=(decimal.Decimal(transaction_total_price_in_rub)
                                                     / decimal.Decimal(transaction_quantity))
        )
        return new_asset  # возвращаем новый созданный Актив, заполненный актуальными данными


# TODO: можно вынести кастомные ошибки в отдельный модуль
class NegativeAssetQuantityError(Exception):
    def __init__(self, err_msg):
        self.err_msg = err_msg


class TransactionTypeError(Exception):
    def __init__(self, err_msg):
        self.err_msg = err_msg


def full_revaluation_single_asset(asset, deleting_transaction_id=None):
    """
    # TODO: - в целях практики можно будет переписать эту функцию на классы
    Полный пересчет данных для Актива (Asset) на основании всех операций (Transaction) по нему.
    Из БД выгружаются все транзакции по данному Активу (кроме удаляемой) и на их основе формируется таблица pandas.
    С помощью сформированной таблицы производится построчный расчет для каждой операции значений
    'общее количество актива на дату операции' и 'общая сумма затрат на дату операции' в двух валютах (rub, usd).
    Рассчитанные в последней операции данные являются актуальными на текущий момент и записываются в Актив.

    :param asset: Актив, по которому необходимо сделать пересчет
    :type asset: объект Asset

    :param deleting_transaction_id: id транзакции, которая будет удалена (на случай, если запуск функции будет
        из метода, который удаляет транзакцию), defaults to None.
    :type deleting_transaction_id: int

    :raises NegativeAssetQuantityError: Если значение количества Актива становится отрицательным
    :raises TransactionTypeError: Если по Активу есть транзакция, имя (name) которой не предусмотрено при расчетах, т.е.
        не определено в модели Transaction и не обрабатывается в этой функции

    :return: None
    """
    # print("----получен asset в asset_processing_destroy:", asset)
    print("----получен deleting_transaction_id в asset_processing_destroy:", type(deleting_transaction_id))
    all_transactions_of_asset = Transaction.objects.filter(asset=asset).exclude(id=deleting_transaction_id)
    # print("---all_transactions_of_asset:", all_transactions_of_asset)

    # если по данному Активу нет транзакций (после удаления текущей транзакции), то заполняем нулями данные в Активе
    if not all_transactions_of_asset:
        asset.total_quantity = 0
        asset.total_expenses_in_currency = 0
        asset.total_expenses_in_rub = 0
        asset.average_buying_price_of_one_unit_in_currency = 0
        asset.average_buying_price_of_one_unit_in_rub = 0
        asset.save()
        return

    # если по данному активу есть транзакции - делаем пересчет показателей Актива,
    #   на основе оставшихся транзакций (после удаления текущей транзакции)
    else:
        df_all_transactions_of_asset = pd.DataFrame(all_transactions_of_asset.values())
        # TODO: !! сейчас сортировка по id, но нужно сортировать по порядку, в котором операции совершались
        #  (нужно решить как определять такой порядок)
        sorted_df_all_transactions_of_asset = df_all_transactions_of_asset.sort_values(by="id", ascending=True)

        # добавляем временные столбцы для расчета итоговых показателей Актива
        sorted_df_all_transactions_of_asset["total_quantity_at_transact_date"] = 0.0
        sorted_df_all_transactions_of_asset["total_expenses_in_currency_at_transact_date"] = 0.0
        sorted_df_all_transactions_of_asset["total_expenses_in_rub_at_transact_date"] = 0.0

        # построчно перебираем все операции, и заполняем временные показатели (общее количество и общая сумма затрат)
        #  для каждой операции
        for index, transact in sorted_df_all_transactions_of_asset.iterrows():
            # print(transact)
            print(f"START LOOP {index}")
            previous_ind = int(str(index)) - 1  # индекс предыдущей транзакции
            # print("-----previous_ind:", previous_ind)

            # берем значение 'общего количества актива на дату операции' и 'общей суммы затрат на дату операции'
            #  из предыдущей операции, если она существует
            if previous_ind >= 0:
                previous_total_quantity_at_transact_date = \
                    sorted_df_all_transactions_of_asset.at[previous_ind, "total_quantity_at_transact_date"]

                previous_total_expenses_in_currency_at_transact_date = \
                    sorted_df_all_transactions_of_asset.at[previous_ind, "total_expenses_in_currency_at_transact_date"]

                previous_total_expenses_in_rub_at_transact_date = \
                    sorted_df_all_transactions_of_asset.at[previous_ind, "total_expenses_in_rub_at_transact_date"]

            #  но если предыдущей операции нет (т.е. предыдущий индекс -1), тогда значения указываем как 0.0
            else:
                previous_total_quantity_at_transact_date = 0.0
                previous_total_expenses_in_currency_at_transact_date = 0.0
                previous_total_expenses_in_rub_at_transact_date = 0.0

            # рассчитываем показатели для операции, в случае если это операция buy
            # (используем transact['name'], а не transact.name т.к. иначе берет Name(индекс) строки, а не транзакции
            if transact['name'] == 'buy':
                # преобразуем из decimal в float, для записи в DataFrame, т.к. pd не поддерживает decimal
                total_quantity_at_transact_date = \
                    float(decimal.Decimal(previous_total_quantity_at_transact_date)
                          + transact.quantity)

                total_expenses_in_currency_at_transact_date = \
                    float(decimal.Decimal(previous_total_expenses_in_currency_at_transact_date)
                          + transact.total_price_in_currency)

                total_expenses_in_rub_at_transact_date = \
                    float(decimal.Decimal(previous_total_expenses_in_rub_at_transact_date)
                          + transact.total_price_in_rub)

            # рассчитываем показатели для операции, в случае если это операция sell
            elif transact['name'] == 'sell':
                total_quantity_at_transact_date = float(decimal.Decimal(previous_total_quantity_at_transact_date)
                                                        - transact.quantity)

                # если количество актива после удаления требуемой транзакции будет отрицательным, то поднимаем ошибку
                #  (эта проверка только в транзакциях sell, т.к. только в этих транзакциях производится вычитание из
                #  общего количества, то есть только здесь может получиться отрицательное значение количества актива)
                if total_quantity_at_transact_date < 0:
                    next_transaction_date = sorted_df_all_transactions_of_asset.at[index, 'date']
                    raise NegativeAssetQuantityError(f"Невозможно удалить операцию, т.к. в результате удаления "
                                                     f"возникает отрицательное значение количества этого актива "
                                                     f"'{total_quantity_at_transact_date}' на дату операции: "
                                                     f"{next_transaction_date}")

                # рассчитываем среднюю цену покупки для дальнейшего расчета суммы общих затрат
                previous_average_price_in_currency = (previous_total_expenses_in_currency_at_transact_date
                                                      / previous_total_quantity_at_transact_date)

                previous_average_price_in_rub = (previous_total_expenses_in_rub_at_transact_date
                                                 / previous_total_quantity_at_transact_date)

                # вычитаем из общего количества затрат количество проданного актива умноженное на среднюю цену покупки
                total_expenses_in_currency_at_transact_date = \
                    float(decimal.Decimal(previous_total_expenses_in_currency_at_transact_date)
                          - (transact.quantity * decimal.Decimal(previous_average_price_in_currency)))

                total_expenses_in_rub_at_transact_date = \
                    float(decimal.Decimal(previous_total_expenses_in_rub_at_transact_date)
                          - (transact.quantity * decimal.Decimal(previous_average_price_in_rub)))

            # если в списке будет операция, которая не обрабатывается не в одном из условий выше поднимаем ошибку
            else:
                raise TransactionTypeError(
                    f"Некорректный вид операции - '{transact['name']}' от {transact.date}.")

            # записываем полученное значение 'общего количества актива на дату текущей операции' в таблицу
            sorted_df_all_transactions_of_asset.at[index, "total_quantity_at_transact_date"] = \
                total_quantity_at_transact_date

            # записываем полученное значение 'общей суммы затрат на дату текущей операции' в таблицу
            sorted_df_all_transactions_of_asset.at[index, "total_expenses_in_currency_at_transact_date"] = \
                total_expenses_in_currency_at_transact_date
            sorted_df_all_transactions_of_asset.at[index, "total_expenses_in_rub_at_transact_date"] = \
                total_expenses_in_rub_at_transact_date

        print("----df_all_transactions_of_asset:",
              sorted_df_all_transactions_of_asset.loc[:, ["id",
                                                          "name",
                                                          # "ticker",
                                                          # "asset_id",
                                                          "quantity",
                                                          "one_unit_buying_price_in_currency",
                                                          # "total_price_in_currency",
                                                          "total_price_in_rub",
                                                          # "total_expenses_in_currency_at_transact_date",
                                                          "total_expenses_in_rub_at_transact_date",
                                                          "total_quantity_at_transact_date",
                                                          ]])

        # print(sorted_df_all_transactions_of_asset.at[5, "total_expenses_in_currency_at_transact_date"])
    print(sorted_df_all_transactions_of_asset.iloc[-1, 21])
    print(sorted_df_all_transactions_of_asset.iloc[-1, 22])
    print(sorted_df_all_transactions_of_asset.iloc[-1, 23])

    # перезаписываем в Активе значение 'общее количество' на значение 'общее количество на дату операции', полученное
    #  в последней операции
    asset.total_quantity = decimal.Decimal(sorted_df_all_transactions_of_asset.iloc[-1, 21])

    # если 'общее количество' в Активе получилось 0, то во все необходимые значения в Активе тоже указываем как 0
    if asset.total_quantity == 0:
        asset.total_expenses_in_currency = decimal.Decimal('0.0')
        asset.total_expenses_in_rub = decimal.Decimal('0.0')
        asset.average_buying_price_of_one_unit_in_currency = decimal.Decimal('0.0')
        asset.average_buying_price_of_one_unit_in_rub = decimal.Decimal('0.0')

    # если 'общее количество' в Активе не равно 0, то все необходимые значения в Активе перезаписываем на значения,
    #  рассчитанные в последней операции
    else:
        asset.total_expenses_in_currency = decimal.Decimal(sorted_df_all_transactions_of_asset.iloc[-1, 22])
        asset.total_expenses_in_rub = decimal.Decimal(sorted_df_all_transactions_of_asset.iloc[-1, 23])
        asset.average_buying_price_of_one_unit_in_currency = asset.total_expenses_in_currency / asset.total_quantity
        asset.average_buying_price_of_one_unit_in_rub = asset.total_expenses_in_rub / asset.total_quantity
    asset.save()
    return


# TODO: можно разделить функционал создания, удаления и т.д. на отдельные View
class TransactionsView(ModelViewSet):
    serializer_class = TransactionsSerializer
    queryset = Transaction.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            # получаем Asset или создаем, если не существует
            asset = processing_asset_when_transaction_create(transaction=request)
            print('-----asset_полученный в create:', type(asset), asset, asset.__dict__)

        # обрабатывается случай, когда количество Актива 0, но пришла транзакция, уменьшающая его количество
        except NegativeAssetQuantityError as err:
            err_data = err.err_msg
            return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)

        # обрабатывает один случай DoesNotExist, когда Актива еще нет, но пришла транзакция, уменьшающая его количество
        except Asset.DoesNotExist:
            err_data = "Невозможно осуществить транзакцию продажи, т.к. такого Актива нет в портфеле"
            return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)

        # отлавливаем вся остальные случаи, когда не удалось создать Актив
        except Exception as err:
            err_data = f"Не удалось получить/создать Актив для транзакции."
            print(err_data, type(err), err)
            return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)
        # print('request.data----------', request.data)
        # print('asset_pk++++++++', asset_pk)
        # print('type-asset_pk++++++++', type(asset_pk))

        # делаем копию запроса, чтоб заполнить его созданными fin_attributes перед отправкой на сериализацию
        request_data_for_serialize = request.data.copy()

        # print('asset.id========', asset.id)
        # print('asset.total_quantity========', asset.total_quantity)
        # print('asset.total_quantity========TYPE', type(asset.total_quantity))
        # print('asset.total_price_in_currency========', asset.total_price_in_currency)
        # print('asset.total_price_in_currency========TYPE', type(asset.total_price_in_currency))
        # print('asset.portfolio_name========', asset.portfolio_name_id)
        # print('asset.agent_id========', asset.agent_id)

        # добавляем данные объекта (который создан/получен из БД) вместо значения str, которое было в запросе
        request_data_for_serialize['asset'] = asset.id
        request_data_for_serialize['portfolio_name'] = asset.portfolio_name_id
        request_data_for_serialize['agent'] = asset.agent_id
        request_data_for_serialize['stock_market'] = asset.stock_market_id
        request_data_for_serialize['asset_class'] = asset.asset_class_id
        request_data_for_serialize['asset_type'] = asset.asset_type_id
        request_data_for_serialize['currency_of_price'] = asset.currency_of_price_id
        request_data_for_serialize['region'] = asset.region_id
        request_data_for_serialize['currency_of_asset'] = asset.currency_of_asset_id
        serializer = self.get_serializer(data=request_data_for_serialize)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        print('serializer.data----', serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # TODO: если ничего не потребуется длеать после удаления операции или с request, тогда можно перенести этот
        #  функционал в perform_destroy, то есть переопределить не destroy, а perform_destroy
        instance_asset = instance.asset
        try:
            # пересчет данных актива на основании анализа всех операций по нему
            full_revaluation_single_asset(asset=instance_asset, deleting_transaction_id=instance.id)

        # обрабатывается случай, когда в результате удаления транзакции количество Актива получается отрицательным
        except NegativeAssetQuantityError as err:
            err_data = err.err_msg
            print(err_data, type(err), err)
            return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)

        # обрабатывается случай, когда по Активу есть транзакция с ошибочным именем (name), т.е. не предусмотренным
        #  в модели Transaction
        except TransactionTypeError as err:
            err_data = err.err_msg
            print(err_data, type(err), err)
            return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)

        # отлавливаются остальные случаи, когда не удалось пересчитать данные для Актива
        except Exception as err:
            err_data = f"Не удалось пересчитать показатели Актива. Транзакция не удалена."
            print(err_data, type(err), err)
            return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)

        # print("---ОПЕРАЦИЯ БУДЕТ УДАЛЕНА в perform_destroy")
        self.perform_destroy(instance)
        print("---ОПЕРАЦИЯ УДАЛЕНА в perform_destroy")

        return Response(status=status.HTTP_204_NO_CONTENT)

# другая архитектура, возможно частично пригодится
# from rest_framework.viewsets import ModelViewSet
# from rest_framework import status
# from rest_framework.response import Response
# import pandas as pd
#
# from src.assets.models import Asset
# from src.fin_attributes.models import Portfolio, Agent, StockMarket, AssetClass, AssetType, Currency, Region
# from src.transactions.models import Transaction
# from src.transactions.serializer import TransactionsSerializer
#
#
# def take_price():
#     """
#     TODO: написать функционал
#     Обращается к стороннему апи, чтобы получить стоимость актива (а так же в этот
#     момент добавляться в таблицу, в которой будут храниться данные о ценах на все купленные активы.
#     Эти таблицы будут обновляться с API по кнопке)
#     :return: текущая цена актива
#     """
#     print('СРАБОТАЛ----take_price')
#     return 300
#
#
# def get_or_create_fin_attributes(transaction):
#     """
#     :param transaction:
#     :return: dict: словарь с полученными или созданными атрибутами транзакции
#     """
#     print('transaction------получена в get_or_create_fin_attributes', transaction)
#     fin_attributes_data = {}
#
#     portfolio_name = transaction.data.get('portfolio_name') or None  # None - если придет пустая строка
#     agent = transaction.data.get('agent')
#     stock_market = transaction.data.get('stock_market')
#     asset_class = transaction.data.get('asset_class')
#     asset_type = transaction.data.get('asset_type') or None  # None - если придет пустая строка
#     currency_of_price = transaction.data.get('currency_of_price')
#     region = transaction.data.get('region') or None  # None - если придет пустая строка
#     currency_of_asset = transaction.data.get('currency_of_asset')
#
#     # если в операции заполнено поле Портфель (иначе останется None)
#     if portfolio_name:
#         print('сработал if portfolio_name:----')
#         portfolio_name, portfolio_created = Portfolio.objects.get_or_create(name=portfolio_name)
#         print('portfolio----', portfolio_name)
#
#     agent, agent_created = Agent.objects.get_or_create(name=agent)
#     print('agent----', agent)
#
#     stock_market, stock_market_created = StockMarket.objects.get_or_create(name=stock_market)
#     print('stock_market----', stock_market)
#
#     asset_class, asset_class_created = AssetClass.objects.get_or_create(name=asset_class)
#     print('asset_class----', asset_class)
#
#     # если в операции заполнено поле Вид актива (иначе останется None)
#     if asset_type:
#         asset_type, asset_type_created = AssetType.objects.get_or_create(name=asset_type)
#         print('asset_type----', asset_type)
#
#     # если валюта цены и валюта покупки одинаковая - то создаем валюту в БД один раз
#     if currency_of_price == currency_of_asset:
#         currency_of_price, currency_of_price_created = Currency.objects.get_or_create(name=currency_of_price)
#         print('currency_of_price----same', currency_of_price)
#         currency_of_asset = currency_of_price
#         print('currency_of_asset----same', currency_of_asset)
#     # если валюта цены и валюта покупки различается - то создаем в БД каждую по отдельности
#     else:
#         currency_of_price, currency_of_price_created = Currency.objects.get_or_create(name=currency_of_price)
#         print('currency_of_price----diff', currency_of_price)
#         currency_of_asset, currency_of_asset_created = Currency.objects.get_or_create(name=currency_of_asset)
#         print('currency_of_asset----diff', currency_of_asset)
#
#     # если в операции заполнено поле Регион (иначе останется None)
#     if region:
#         region, currency_created = Region.objects.get_or_create(name=region)
#         print('region----', region)
#
#     fin_attributes_data['portfolio_name'] = portfolio_name
#     fin_attributes_data['agent'] = agent
#     fin_attributes_data['stock_market'] = stock_market
#     fin_attributes_data['asset_class'] = asset_class
#     fin_attributes_data['asset_type'] = asset_type
#     fin_attributes_data['currency_of_price'] = currency_of_price
#     fin_attributes_data['currency_of_asset'] = currency_of_asset
#     fin_attributes_data['region'] = region
#
#     print('----fin_attributes_data----на выходе функции:', fin_attributes_data)
#     return fin_attributes_data
#
#
# def asset_recounting_when_transaction_create(transaction, fin_attributes):
#     # print("----получена transaction в asset_recounting_when_transaction_create:", transaction.__dict__)
#     # print("----получена transaction в asset_recounting_when_transaction_create--t:", type(transaction))
#     # print("----получена fin_attributes в asset_recounting_when_transaction_create--t:", fin_attributes)
#
#     ticker = transaction['ticker']
#     asset_name = transaction['asset_name']
#
#     portfolio_name = fin_attributes['portfolio_name']
#     agent = fin_attributes['agent']
#     stock_market = fin_attributes['stock_market']
#     asset_class = fin_attributes['asset_class']
#     asset_type = fin_attributes['asset_type']
#     currency_of_price = fin_attributes['currency_of_price']
#     region = fin_attributes['region']
#     currency_of_asset = fin_attributes['currency_of_asset']
#
#     print('----portfolio_name---', portfolio_name)
#
#     all_transactions_of_asset = Transaction.objects.filter(
#         ticker=ticker,
#         portfolio_name=portfolio_name,
#         agent=agent,
#         stock_market=stock_market,
#         asset_class=asset_class,
#         asset_type=asset_type,
#         currency_of_price=currency_of_price,
#         region=region,
#         currency_of_asset=currency_of_asset,
#     )
#     # print('-------all_transactions_of_asset - filter:', all_transactions_of_asset)
#     df_all_transactions_of_asset = pd.DataFrame(all_transactions_of_asset.values(),
#                                                 # index=all_transactions_of_asset.values('id', 'name')
#                                                 )
#     print('-----df', df_all_transactions_of_asset.loc[:, ["id", "name", "ticker", "quantity", "one_unit_buying_price_in_currency", "total_price_in_currency"]])
#
#
#     df_buy_transactions_of_asset = df_all_transactions_of_asset[
#         df_all_transactions_of_asset['name'] == 'buy']
#     print('----df_buy', df_buy_transactions_of_asset.loc[:, ["id", "name", "ticker", "quantity", "one_unit_buying_price_in_currency", "total_price_in_currency"]])
#
#     df_sell_transactions_of_asset = df_all_transactions_of_asset[
#         df_all_transactions_of_asset['name'] == 'sell']
#     print('----df_sell', df_sell_transactions_of_asset.loc[:, ["id", "name", "ticker", "quantity", "one_unit_buying_price_in_currency", "total_price_in_currency"]])
#
#
#     total_quantity = (df_buy_transactions_of_asset['quantity'].sum()
#                       - df_sell_transactions_of_asset['quantity'].sum())
#     print('----total_quantity', total_quantity)
#
#     one_unit_current_price_in_currency = take_price()
#
#     total_expenses_in_currency = (df_buy_transactions_of_asset['total_price_in_currency'].sum()
#                                   - df_sell_transactions_of_asset['total_price_in_currency'].sum())
#     print('----total_expenses_in_currency', total_expenses_in_currency)
#
#     total_expenses_in_rub = (df_buy_transactions_of_asset['total_price_in_rub'].sum()
#                              - df_sell_transactions_of_asset['total_price_in_rub'].sum())
#     print('----total_expenses_in_rub', total_expenses_in_rub)
#
#     average_buying_price_of_one_unit_in_currency = total_expenses_in_currency / total_quantity
#     print('----average_buying_price_of_one_unit_in_currency', average_buying_price_of_one_unit_in_currency)
#
#     average_buying_price_of_one_unit_in_rub = total_expenses_in_rub / total_quantity
#     print('----average_buying_price_of_one_unit_in_rub', average_buying_price_of_one_unit_in_rub)
#
#     asset = Asset.objects.update_or_create(ticker=ticker,
#                                            portfolio_name=portfolio_name,
#                                            agent=agent,
#                                            stock_market=stock_market,
#                                            asset_class=asset_class,
#                                            asset_type=asset_type,
#                                            currency_of_price=currency_of_price,
#                                            region=region,
#                                            currency_of_asset=currency_of_asset,
#                                            defaults={
#                                                'name': asset_name,
#                                                'total_quantity': total_quantity,
#                                                'one_unit_current_price_in_currency':
#                                                    one_unit_current_price_in_currency,
#                                                'total_expenses_in_currency': total_expenses_in_currency,
#                                                'total_expenses_in_rub': total_expenses_in_rub,
#                                                'average_buying_price_of_one_unit_in_currency':
#                                                    average_buying_price_of_one_unit_in_currency,
#                                                'average_buying_price_of_one_unit_in_rub':
#                                                    average_buying_price_of_one_unit_in_rub,
#                                            })
#     print('-------asset filter после update_or_create:', asset)
#
#
# class TransactionsView(ModelViewSet):
#     serializer_class = TransactionsSerializer
#     queryset = Transaction.objects.all()
#
#     def create(self, request, *args, **kwargs):
#         fin_attributes = get_or_create_fin_attributes(transaction=request)
#         request_data_for_serialize = request.data.copy()
#
#         request_data_for_serialize['portfolio_name'] = \
#             fin_attributes['portfolio_name'].id if fin_attributes['portfolio_name'] else None
#         request_data_for_serialize['agent'] = fin_attributes['agent'].id
#         request_data_for_serialize['stock_market'] = fin_attributes['stock_market'].id
#         request_data_for_serialize['asset_class'] = fin_attributes['asset_class'].id
#         request_data_for_serialize['asset_type'] = \
#             fin_attributes['asset_type'].id if fin_attributes['asset_type'] else None
#         request_data_for_serialize['currency_of_price'] = fin_attributes['currency_of_price'].id
#         request_data_for_serialize['region'] = fin_attributes['region'].id if fin_attributes['region'] else None
#         request_data_for_serialize['currency_of_asset'] = fin_attributes['currency_of_asset'].id
#         print('-----request_data_for_serialize:', request_data_for_serialize)
#
#         serializer = self.get_serializer(data=request_data_for_serialize)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         print('-------сформированная serializer.data', serializer.data)
#         asset_recounting_when_transaction_create(transaction=serializer.data, fin_attributes=fin_attributes)
#
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
