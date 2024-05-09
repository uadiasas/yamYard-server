FROM python:3.11
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN pip install --upgrade pip poetry
RUN poetry config virtualenvs.create false --local
COPY poetry.lock pyproject.toml ./
RUN poetry install
COPY yumYard .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
