<script setup>
import { RouterLink } from "vue-router";
// import BicyclesList from "../components/bicycles/BicyclesList.vue";

</script>

<template>
  <div class="pt-3">
    <h3>Статистика</h3>

    <div class="container mt-5">
        <!-- Информационное окно "Общая сумма" -->
        <div class="alert alert-info">
            Общая сумма: $100,000
        </div>
        <!-- Вкладки "Общая статистика" и кнопка "Добавить портфель" -->
        <ul class="nav nav-tabs">
            <li class="nav-item">
                <a class="nav-link active" data-toggle="tab" href="#general">Общая статистика</a>
            </li>
            <li class="nav-item">
                <button class="btn btn-primary" id="addPortfolio">Добавить портфель</button>
            </li>
        </ul>
        <!-- Вкладки с содержимым -->
        <div class="tab-content">
            <!-- Вкладка "Общая статистика" -->
            <div class="tab-pane fade show active" id="general">
                <h2>Общая статистика</h2>
                <table class="table table-bordered">
                    <thead>
                        <tr>
                            <th>Портфель</th>
                            <th>Класс актива</th>
                            <th>Вид актива</th>
                            <th>Регион</th>
                            <th>Доля от всех активов</th>
                            <th>Сумма в RUB/USD</th>
                            <th>Изменение в RUB/USD</th>
                            <th>Изменение в % к RUB/USD</th>
                        </tr>
                    </thead>
                    <tbody>
                        <!-- Здесь будет содержимое таблицы для "Общая статистика" -->
                    </tbody>
                </table>
            </div>
            <!-- Здесь будут добавляться вкладки с портфелями -->
        </div>
    </div>

  </div>
</template>
