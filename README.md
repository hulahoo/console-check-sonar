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
- Создать и активировать виртуальное окружение
    ```bash
    $ python -m venv venv
    $ source venv/bin/activate
    ```
- Установить зависимости
    ```bash
    (venv) pip install -r requirements.txt
- Сбилдить приложение
    ```bash
    (venv) python -m pip install .
    ```
- Запустить приложение
    ```bash
    (venv) console-api
    ```
### С использованием Docker
- Создать Dockerfile в корне проекта
    ```docker
    FROM python:3.10.8-slim as deps
    WORKDIR /app
    COPY . ./
    RUN apt-get update -y && apt-get -y install gcc python3-dev
    RUN pip --no-cache-dir install -r requirements.txt
    RUN pip --no-cache-dir install -r requirements.setup.txt
    RUN pip install -e .

    FROM deps as build
    ARG ARTIFACT_VERSION=local
    RUN python setup.py sdist bdist_wheel
    RUN ls -ll /app/
    RUN ls -ll /app/dist/


    FROM python:3.10.8-slim as runtime
    COPY --from=build /app/dist/*.whl /app/
    RUN apt-get update -y && apt-get -y install gcc python3-dev
    RUN pip --no-cache-dir install /app/*.whl

    ENTRYPOINT ["console-api"]
    ```
- Создать docker-compose.yml в корне проекта
    ```docker
    version: '3'

    services:
    postgres_db:
        image: postgres:13.8-alpine
        container_name: db
        restart: unless-stopped
        expose:
        - 5432
        environment:
        POSTGRES_DB: db
        POSTGRES_USER: dbuser
        POSTGRES_PASSWORD: test

    platform:
        restart: always
        build: ./
        ports:
        - "8080:8080"
        environment:
        TOPIC_CONSUME_EVENTS: syslog
        APP_POSTGRESQL_USER: dbuser
        APP_POSTGRESQL_PASSWORD: test
        APP_POSTGRESQL_NAME: db
        APP_POSTGRESQL_HOST: postgres_db
        APP_POSTGRESQL_PORT: 5432
        DEBUG: "y"
        SWAGGER: "y"
        depends_on:
        - postgres_db
    ```
- Сбилдить и запустить проект
    ```bash
    $ docker-compose up --build
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
```