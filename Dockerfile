FROM python:3.13-slim-bullseye

# Установим Poetry
RUN pip install poetry

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY . .

# config virtualenvs.create false - отключаем создание
# вирутального окружения, так как контейнер итак 
# изолированная среда.
# Следом устанавливаем зависимости из pyproject.toml
RUN poetry config virtualenvs.create false && \
    poetry install --no-root

ENV PYTHONPATH="/app/src:${PYTHONPATH}"

CMD ["bash", "-c", "poetry run uvicorn src.fat.main:app --host 0.0.0.0 --port 8000"]