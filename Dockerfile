FROM python:3.11.0-slim

WORKDIR /app

# Instala dependências do sistema necessárias para compilar pacotes Python
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instala o Poetry
RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false

# Copia apenas os arquivos de dependências primeiro (otimiza o cache do Docker)
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root --no-interaction --no-ansi

# Copia todo o código do seu projeto para dentro de /app
COPY . .

# AJUSTE CRUCIAL: Permissão total na raiz para o SQLite criar o fiap.db
RUN chmod -R 777 /app

EXPOSE 5000

# Garante que os logs apareçam no terminal sem atraso
ENV PYTHONUNBUFFERED=1

# Executa o seu arquivo principal
CMD ["python", "main.py"]