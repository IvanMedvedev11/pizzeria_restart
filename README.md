# pizzeria_restart
Пиццерия - Система онлайн-заказов
Описание проекта

Это приложение для онлайн-заказа пиццы с возможностью:

    Выбора готовых пицц (Пепперони, Маргарита, Четыре сыра, Гавайская)

    Создания собственной пиццы из доступных ингредиентов

    Заказа "взрослых" товаров (для пользователей старше 18 лет)

Технологии

    Python 3

    Tkinter (для графического интерфейса)

    SQLite (для хранения данных)


Установка и запуск

    Убедитесь, что у вас установлен Python 3

    Клонируйте репозиторий

    Запустите главный файл:
    Copy

    python main.py

Структура проекта

pizzeria/
├── model.py       # Модели данных и работа с БД
├── view.py        # Графический интерфейс
├── controller.py  # Логика приложения
└── database.db    # Файл базы данных

Функционал
Для пользователей:

    Регистрация с указанием ФИО и даты рождения

    Выбор готовых пицц с возможностью указания размера и количества

    Создание собственной пиццы из ингредиентов

    Заказ "взрослых" товаров (при подтверждении возраста)

    Просмотр итогового заказа


База данных

Проект использует SQLite с тремя таблицами:

    Users - информация о пользователях

    Products - основные продукты и ингредиенты

    Products_18 - товары для взрослых
