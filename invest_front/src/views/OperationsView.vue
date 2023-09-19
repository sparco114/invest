<script setup>

// TODO: добавить пагинацию, и фильтр в будущем
</script>

<template>
  <div class="pt-3">
  </div>


  <div class="container">
        <h1>Таблица операций</h1>
        <table class="table table-bordered">
            <thead>
                <tr>
                    <th>Дата</th>
                    <th>Операция</th>
                    <th>Портфель</th>
                    <th>Посредник</th>
                    <th>Биржа</th>
                    <th>Класс актива</th>
                    <th>Вид актива</th>
                    <th>Валюта цены</th>
                    <th>Регион</th>
                    <th>Валюта актива</th>
                    <th>Тикер</th>
                    <th>Количество</th>
                    <th>Цена в валюте</th>
                    <th>Удержания</th>
                    <th>Курс валюты к RUB</th>
                    <th>Курс валюты к USD</th>
                    <th>Сумма в валюте</th>
                    <th>Сумма в RUB</th>
                    <th>Удержания в RUB</th>
                    <th>Сумма в USD</th>
                    <th>Удержания в USD</th>
                    <th>Действия</th>
                </tr>
            </thead>
            <tbody>
                <!-- Редактируемая строка -->
                <tr>
                    <td><input type="text" class="form-control"></td>
                    <td><input type="text" class="form-control"></td>
                    <td><input type="text" class="form-control"></td>
                    <td><input type="text" class="form-control"></td>
                    <td><input type="text" class="form-control"></td>
                    <td><input type="text" class="form-control"></td>
                    <td><input type="text" class="form-control"></td>
                    <td><input type="text" class="form-control"></td>
                    <td><input type="text" class="form-control"></td>
                    <td><input type="text" class="form-control"></td>
                    <td><input type="text" class="form-control"></td>
                    <td><input type="text" class="form-control"></td>
                    <td><input type="text" class="form-control"></td>
                    <td><input type="text" class="form-control"></td>
                    <td><input type="text" class="form-control"></td>
                    <td><input type="text" class="form-control"></td>
                    <td><input type="text" class="form-control"></td>
                    <td><input type="text" class="form-control"></td>
                    <td><input type="text" class="form-control"></td>
                    <td><input type="text" class="form-control"></td>
                    <td><input type="text" class="form-control"></td>
                    <td><button class="btn btn-primary">Сохранить</button></td>
                </tr>
                <!-- Строки с данными -->
                <tr>
                  <td>Дата 1</td>
                    <td>Операция 1</td>
                    <td>Портфель 1</td>
                    <td>Посредник 1</td>
                    <td>Биржа 1</td>
                    <td>Класс 1</td>
                    <td>Вид 1</td>
                    <td>Валюта цены 1</td>
                    <td>Регион 1</td>
                    <td>Валюта актива 1</td>
                    <td>Тикер 1</td>
                    <td>Количество 1</td>
                    <td>Цена в валюте 1</td>
                    <td>Удержания 1</td>
                    <td>Курс валюты к RUB 1</td>
                    <td>Курс валюты к USD 1</td>
                    <td>Сумма в валюте 1</td>
                    <td>Сумма в RUB 1</td>
                    <td>Удержания в RUB 1</td>
                    <td>Сумма в USD 1</td>
                    <td>Удержания в USD 1</td>
                    <td>
                        <button class="btn btn-warning">Редактировать</button>
                        <button class="btn btn-danger">Удалить</button>
                    </td>
                </tr>
                <!-- Продолжайте добавлять строки данных, как это необходимо -->
            </tbody>
        </table>
    </div>

  
  
</template>
