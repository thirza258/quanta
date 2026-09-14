FROM python:3.14-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 \
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 QUANTA_STORAGE=/app/storage QUANTA_DATA_DIR=/app/data
WORKDIR /app
COPY backend/requirements.lock ./requirements.lock
RUN pip install --no-cache-dir -r requirements.lock \
    && groupadd --gid 10001 quanta \
    && useradd --uid 10001 --gid quanta --no-create-home --shell /usr/sbin/nologin quanta \
    && mkdir -p /app/storage /app/data && chown -R quanta:quanta /app/storage /app/data
COPY --chown=quanta:quanta backend/quanta ./backend/quanta
COPY --chown=quanta:quanta content/catalog/curriculum.json ./content/catalog/curriculum.json
COPY --chown=quanta:quanta backend/scripts/import_data.py ./backend/scripts/import_data.py
USER 10001:10001
EXPOSE 8000
HEALTHCHECK --interval=20s --timeout=5s CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/v1/health', timeout=3)" || exit 1
CMD ["python", "-m", "uvicorn", "quanta.main:app", "--app-dir", "backend", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips", "*"]
