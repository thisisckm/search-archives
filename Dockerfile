FROM python:3.10-slim

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get upgrade -y && apt-get install -y default-mysql-client default-libmysqlclient-dev gcc

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Application ENV
ENV SEARCH_ARCHIVES_SECRET_KEY=django-secret
ENV SEARCH_ARCHIVES_DB_NAME=search_archives
ENV SEARCH_ARCHIVES_DB_HOST=db
ENV SEARCH_ARCHIVES_DB_PORT=3306
ENV SEARCH_ARCHIVES_DB_USERNAME=root

# Setup the application user
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# Default cmd to start the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "5", "search_archives.wsgi"]
