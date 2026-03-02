FROM python:3.11.0-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root --no-interaction --no-ansi

COPY . .

RUN chmod -R 777 /app

EXPOSE 5000

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]