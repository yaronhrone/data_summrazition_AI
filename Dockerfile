FROM python:3.9-slim
LABEL maintainer="Yaron"

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r requirements.txt && \
    adduser --disabled-password --no-create-home django-user

COPY . .

ENV PATH="/py/bin:$PATH"

EXPOSE 8000

USER django-user
