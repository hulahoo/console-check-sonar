# console-api

API для Консоли Управления, куда ходит Веб-интерфейс Платформы и куда ходит Консольная команда управления Платформой. 

### Запуск приложени

- Скопируйте данный репозиторий

- Запустить создание статических файлов
    ```
    python3 src/manage.py collectstatic
    python3 src/manage.py makemigrations
    python3 src/manage.py makemigrations feed
    python3 src/manage.py makemigrations indicator
    python3 src/manage.py makemigrations source
    python3 src/manage.py makemigrations tag
    python3 src/manage.py makemigrations users
    python3 src/manage.py migrate
    python3 src/manage.py loaddata fixt_user.json
    python3 mamage.py runserver
    ```
- Запуск приложения
    ```
    python3 mamage.py runserver
    ```

## Информаци о ENV-параметрах
Имеющиеся env-параметры в проекте:
```
DEBUG=

POSTGRES_SERVER=
POSTGRES_PASSWORD=
POSTGRES_USER=
POSTGRES_DB=
POSTGRES_PORT=

SWAGGER=(bool)
```

## Информация о файлах конфигурации
```text
.
├── api                                 ## Директория для api эндпоинтов
│   │                                   
│   ├──                                
... ... ... ...
│
├── docs                                ## Документация проекта
│   ├──                                 
... ... ... ...
│
└── settings                            ## Конфигурации, подключаемые в проект.
    ├──
... ... ... ...
│
└── src                                 ## Основая директория с хранением данных и доп. сервисами
    ├── сommon                          ## Константые значения
    ├── models                          ## Всопомогательные данные для моделей Django
    ├── services                        ## Функции отвечающие за бизнес-логику проекта
... ... ... ...
│
└── static                              ## Статические файлы
│
└── swagger                             ## Настройки swagger-документации
```