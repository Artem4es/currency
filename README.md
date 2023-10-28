[Что это за currency?] 😺
Currency - это API для конвертации валют.

Как запустить? 👾
Проект можно запустить, используя Docker-compose для этого:

Клонировать репозиторий:

```
git clone git@github.com:Artem4es/currency.git
```
Файл .env специально включён в репозиторий для удобства запуска (Хотя, так делать не надо😱)

Перейти в папку с проектом
```
cd /currency
```

Запустить проект через docker-compose:

```
docker-compose -f docker-compose.yml up --build
```

Пример взаимодействия.

1. Обновление курсов валют. Отправляем GET запрос на /update_rates
    
    В случае удачного ответа получаем ответ вида:
    
    ```
    {
        "status": "Rates updated successfully",
        "update_time": 1698477723
    }
    ```
   где "update_time" - Unix timestamp. Легко пересчитывается в текущее время https://www.unixtimestamp.com/

    прим. Курсы валют автоматически обновляются при запуске и кешируются, поэтому если сразу попытаться обновить возможно сообщение:
    
    ```
    {
        "detail": "Rates are still fresh. Update in 22 seconds, please!"
    }
    ```

2. Узнать когда последний раз было обновление курсов валю. Отправляем GET запрос на эндпоинт /last_update и получаем ответ вида:
   
   ```
   {
        "date": "2023-10-28",
        "timestamp": 1698476764
   }
   ```
    где "timestamp" - Unix timestamp. Легко пересчитывается в текущее время https://www.unixtimestamp.com/


3. Конвертация валют. Отправляем GET запрос с query параметрами на эндпоинт /convert:
   
   ```
      http://localhost:8000/convert?from_curr_amount=10000&from_curr=USD&to_curr=RUB
   ```
    где from_curr_amount cумма конвертации,
    from_curr - код исходной валюты (RUB, USD, EUR и тд)
    to_curr -  код получаемой валюты (RUB, USD, EUR и тд)

📜 В проекте предусмотерно логирование. Логи находятся в папке src/currency_app/logs/ и прокинуты через docker volume.

Исчерпывающая документация проекта: 📘
После запуска проекта доступная документация Swagger и Redoc по адресам: http://localhost:8000/docs/ или тут http://localhost:8000/redoc/
