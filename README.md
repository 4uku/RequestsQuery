![Tests](https://github.com/4uku/RequestsQuery/blob/main/.github/workflows/main.yml/badge.svg)

Для запуска потребуется установленный Docker.

1. Клонируйте репозиторий.
Далее команды выполняются из директории репозитория.
2. Соберите образ: `docker build -t req .`. При сборке образа будут запущены тесты с помощью `pytest`
3. Запустите контейнер на базе образа: `docker run --name req_container -p 8000:8000 req`

Вам будет доступен эндпоинт: `http://127.0.0.1:8000/counts/`.
Документация: `http://127.0.0.1:8000/docs/`