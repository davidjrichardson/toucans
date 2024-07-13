FROM python:3.10-bullseye
LABEL maintainer="david@tankski.co.uk"
EXPOSE 8000

RUN useradd -rm -d /home/toucans -s /bin/bash -u 1001 toucans

# Copy application code.
COPY --chown=toucans . /app/

ENV PYTHONUNBUFFERED=1 \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PYTHONPATH=/app \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_IN_PROJECT=true \
  DJANGO_SETTINGS_MODULE=toucans.settings.base \
  PORT=8000 \
  WEB_CONCURRENCY=3 \
  GUNICORN_CMD_ARGS="--max-requests 1200 --access-logfile -" \
  PATH="/home/toucans/.local/bin:$PATH" \
  FNM_DIR="/usr/share/.fnm"

# Build the frontend
WORKDIR /app/frontend

RUN export SHELL=bash \
	&& mkdir /usr/share/.fnm \
	&& curl -fsSL https://fnm.vercel.app/install | bash -s -- --install-dir $FNM_DIR --skip-shell \
	&& $FNM_DIR/fnm install $(cat .nvmrc) \
	&& chmod -R 777 $FNM_DIR

USER toucans

RUN $FNM_DIR/fnm exec npm ci \
  && $FNM_DIR/fnm exec npm run build:production \
  && $FNM_DIR/fnm exec npm cache clean --force

# # Build & set up backend
WORKDIR /app

RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.5.1 python3 -
RUN poetry install \
  && poetry run pip install "gunicorn==19.10.0" \
  && SECRET_KEY=none \
    DB_NAME=toucans \
    DB_USER=toucans \
    DB_PASSWORD=toucans \
    DB_HOST=localhost \
    DB_PORT=5432 \
    ALLOWED_HOSTS="[]" \
    CSRF_TRUSTED_ORIGINS="[]" \
    poetry run python manage.py collectstatic --no-input --clear

# Run the WSGI server. It reads GUNICORN_CMD_ARGS, PORT and WEB_CONCURRENCY
# environment variable hence we don't specify a lot options below.
CMD poetry run gunicorn toucans.wsgi:application
