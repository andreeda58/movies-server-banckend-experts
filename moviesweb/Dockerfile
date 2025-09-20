# moviesweb/Dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Paquetes nativos: psycopg2 + Pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev gcc libjpeg62-turbo-dev zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# requirements en la RAÍZ del repo: subimos uno solo al contenedor
COPY ../requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# Copiamos TODO el repo (para que /app/moviesweb exista)
COPY .. /app

EXPOSE 8000

# Ejecuta migraciones, collectstatic y lanza Gunicorn (prod)
CMD ["bash", "-lc", "\
  python moviesweb/manage.py migrate && \
  python moviesweb/manage.py collectstatic --noinput && \
  gunicorn moviesserver.wsgi:application --chdir moviesweb --bind 0.0.0.0:8000 --workers 3 --timeout 120 \
"]
