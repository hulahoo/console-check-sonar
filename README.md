# console-api - API для консоли управления

## К API обращаются:
- Веб-интерфейс Платформы (Console WEB)
- Консольная команда управления Платформой (Console CLI)

## Запуск

### Без использования Docker
- Создать файл _.env_ в корне проекта и задать в нём значения
    ```
    DEBUG=<True/False>

    POSTGRES_SERVER=
    POSTGRES_PASSWORD=
    POSTGRES_USER=
    POSTGRES_DB=
    POSTGRES_PORT=

    SWAGGER=<True/False>
    ```

- Собрать статику
    ```
    python3 src/console_api/manage.py collectstatic
    ```
- Создать и выполнить миграции
    ```
    python3 src/console_api/manage.py makemigrations

    python3 src/console_api/manage.py makemigrations feed
    python3 src/console_api/manage.py makemigrations indicator
    python3 src/console_api/manage.py makemigrations source
    python3 src/console_api/manage.py makemigrations tag
    python3 src/console_api/manage.py makemigrations users
    python3 src/console_api/manage.py makemigrations detections

    python3 src/console_api/manage.py migrate
- Запустить сервер
    ```
    python3 src/console_api/manage.py runserver
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