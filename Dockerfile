FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir poetry==2.2.1

COPY . .

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

ENV FLASK_APP=crypto_tracker.app
ENV FLASK_DEBUG=0

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "crypto_tracker.app:app"]
