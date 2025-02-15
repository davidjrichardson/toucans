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

RUN curl --proto '=https' --tlsv1.2 -LsSf https://github.com/astral-sh/uv/releases/download/0.6.0/uv-installer.sh | sh
RUN uv sync --group docker \
  && SECRET_KEY=none \
  DB_NAME=toucans \
  DB_USER=toucans \
  DB_PASSWORD=toucans \
  DB_HOST=localhost \
  DB_PORT=5432 \
  ALLOWED_HOSTS="[]" \
  CSRF_TRUSTED_ORIGINS="[]" \
  uv run --locked manage.py collectstatic --no-input --clear

# Run the WSGI server. It reads GUNICORN_CMD_ARGS, PORT and WEB_CONCURRENCY
# environment variable hence we don't specify a lot options below.
CMD uv run --locked --with gunicorn gunicorn toucans.wsgi:application
