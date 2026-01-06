FROM python:3.9

WORKDIR / project

COPY pyproject.toml ./

RUN pip install poetry

RUN poetry install --no-root

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]