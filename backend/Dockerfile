# Этап сборки (общий для dev и prod)
FROM python:3.12-alpine3.19 AS build

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY requirements.txt .

COPY . .

# Этап разработки (dev)
FROM python:3.12-alpine3.19 AS dev

WORKDIR /fastapi_app

# Копируем зависимости и код из этапа build
COPY --from=build /fastapi_app .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--reload", "--port=8000", "--host=0.0.0.0"]

# Этап продакшена (prod)
FROM python:3.12-alpine3.19 AS prod

WORKDIR /fastapi_app

# Копируем зависимости и код из этапа build
COPY --from=build /fastapi_app .

RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000

CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app"]