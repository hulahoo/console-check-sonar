# console-api - API для консоли управления

## К API обращаются:
- Веб-интерфейс Платформы (Console WEB)
- Консольная команда управления Платформой (Console CLI)

## Запуск

### Без использования Docker
- Создать файл _.env_ в корне проекта и задать в нём значения
    ```
    DEBUG=<True/False>
    SWAGGER=<True/False>

    APP_POSTGRESQL_HOST=
    APP_POSTGRESQL_PASSWORD=
    APP_POSTGRESQL_USER=
    APP_POSTGRESQL_NAME=
    APP_POSTGRESQL_PORT=
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
- Применить дамп файла для бд в контейнере:
    ```bash
    cat restore.sql | docker exec -i db psql -U dbuser -d db
    ```

- Перзапустить контейнер worker


## Информация о файлах конфигурации
```text
│
└── deploy
    ├──envs
        ├──dev/                       ## Конфигурации k8s для dev стенда
... ... ... ...
│
└── src                                 ## Основая директория с хранением данных и доп. сервисами
    ├── console_api
            ├── api/                             ## Директория для api эндпоинтов
            ├── apps/                            ## Модуль отвечающий за описания моделей
            ├── config/                          ## Модуль отвечающий сторонние конфигурации
            ├── settings/                        ## Модуль отвечающий настройки сервиса
            ├── swagger/                         ## Модуль отвечающий за swagger api
... ... ... ...
```