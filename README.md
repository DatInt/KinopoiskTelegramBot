#**KinopoiskBot**

![Alt-текст](https://avatars.mds.yandex.net/get-kinopoisk-post-img/1374145/09792ccb925715f9b5d85fc22ed445d8/960 "Кинопоиск лого")

##Описание проекта:
KinopoiskBot - бот для мессенджера Telegram, написанный с помощью библиотеки для создания ботов aiogram и неофициального API Кинопоиска
(документация: https://api.kinopoisk.dev/v1/documentation). С помощью этого бота можно легко найти фильмыв базе кинопоиска и получить
информацию о них в формате сообщения. Проект подготовлен как финальная работа курса "Основы Python" от Skillbox.

##Использованные бибилотеки:
+ aiogram
+ peewee ORM
+ python-dotenv
+ etc.

##Функционал:
Бот может обрабатывать сообщения введенные пользователем и выполнять следующие команды:
+ /help - показать список команд
+ /random - получить случайный фильм
+ /search - поиск фильма по названию
+ /adv_search - поиск фильма с фильтрами
+ /history - показать историю запросов, сохраненную в бд

##Установка:
Бот запускается с помощью клонирования репозитория и установки необходимых библиотек (pip install -r requirements.txt).
API_KEY Кинопоиска и TELEGRAM_BOT_KEY прописываются в файле .env

Для запуска в дркере выполнить команды:
`docker compose build`
`docker compose up`

###Автор:
Маслюк Максим 2023

pb2600mah@gmail.com | [Гитхаб](https://github.com/DatInt)