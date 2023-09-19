<script setup>
// import LogBookRecordsList from "../components/logbooks/LogBookRecordsList.vue";

// const logBookRecordAmount = "?ordering=-id";
// TODO: добавить пагинацию, и фильтр в будущем
</script>

<template>
  <div class="pt-3">
    <!-- <LogBookRecordsList :logBookRecordAmount="logBookRecordAmount" /> -->


    <div class="container">
        <h1>Активы</h1>
        <table class="table table-bordered table-hover">
            <thead>
                <tr>
                    <th>Название</th>
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
                    <th>Цена + Валюта</th>
                    <th>Сумма (на текущий момент)</th>
                    <th>Изменение в RUB/USD</th>
                    <th>Изменение в % RUB/USD</th>
                    <th>Дивиденды и купоны</th>
                    <th>Сумма затрат в RUB/USD</th>
                </tr>
            </thead>
            <tbody>
                <!-- Здесь добавьте строки данных, каждая строка представляет один актив -->
                <tr>
                    <td>Актив 1</td>
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
                    <td>Цена + Валюта 1</td>
                    <td>Сумма 1</td>
                    <td>Изменение 1</td>
                    <td>Изменение % 1</td>
                    <td>Дивиденды 1</td>
                    <td>Сумма затрат 1</td>
                </tr>
                <tr>
                    <td>Актив 2</td>
                    <!-- Добавьте данные для остальных столбцов -->
                </tr>
                <!-- Добавьте больше строк, если это необходимо -->
            </tbody>
        </table>
    </div>


    
  </div>
</template>
