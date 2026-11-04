# Dockerfile KopiKita yang sudah dikeraskan (Lab L3.3), menerapkan pola docs/reference/Dockerfile.secure:
# tag versi spesifik, multi-stage, dependensi produksi saja, pengguna non-root, health check.
ARG PYTHON_VERSION=3.11.11

FROM python:${PYTHON_VERSION}-slim AS build
WORKDIR /build
COPY api/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt gunicorn==23.0.0

FROM python:${PYTHON_VERSION}-slim AS runtime
RUN groupadd --system --gid 10001 app \
 && useradd --system --uid 10001 --gid app --no-create-home app
WORKDIR /app
COPY --from=build /install /usr/local
COPY --chown=app:app api/ ./api/
USER app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 KOPIKITA_DB=/tmp/kopikita.db
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/health', timeout=2)"
CMD ["gunicorn", "--chdir", "api", "--bind", "0.0.0.0:5000", "wsgi:app"]
