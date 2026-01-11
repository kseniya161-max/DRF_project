FROM python:3.12

RUN apt-get update && apt-get install -y \
    nginx \
    gcc \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry

RUN poetry install --no-root

COPY . .

COPY static /home/kseniya161/app/static

ENV PYTHONPATH=/app

COPY myapp_nginx.conf /etc/nginx/conf.d/

EXPOSE 80 8000

CMD service nginx start && poetry run gunicorn --workers 3 --bind unix:/home/kseniya161/app/myapp.sock config.wsgi:application

# CMD ["sh", "-c", "export PYTHONPATH=/app && poetry run python manage.py runserver 0.0.0.0:8000"]

# CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]