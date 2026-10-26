# The simulator engine is C++. It is compiled and tested on the same Debian base
# the API runs on, so the library links against the C library it will load, and
# only the built library reaches the runtime image.
FROM python:3.14-slim AS engine
RUN apt-get update \
    && apt-get install -y --no-install-recommends g++ make \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /build
COPY backend/engine ./engine
RUN make -C engine && make -C engine test

FROM python:3.14-slim
# QUANTA_SIM_THREADS matches the two CPUs Compose gives the API; a container may
# otherwise see every core on the host.
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 \
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 QUANTA_SIM_THREADS=2 \
    QUANTA_STORAGE=/app/storage QUANTA_DATA_DIR=/app/data
WORKDIR /app
COPY backend/requirements.lock ./requirements.lock
RUN pip install --no-cache-dir -r requirements.lock \
    && groupadd --gid 10001 quanta \
    && useradd --uid 10001 --gid quanta --no-create-home --shell /usr/sbin/nologin quanta \
    && mkdir -p /app/storage /app/data && chown -R quanta:quanta /app/storage /app/data
COPY --chown=quanta:quanta backend/quanta ./backend/quanta
COPY --from=engine --chown=quanta:quanta /build/engine/build/libquanta_sim.so ./backend/engine/build/libquanta_sim.so
COPY --chown=quanta:quanta content/catalog/curriculum.json ./content/catalog/curriculum.json
# Authored setup guides ground the assistant without shipping project build artifacts.
COPY --chown=quanta:quanta content/projects/algorithm-evaluation/README.md content/projects/algorithm-evaluation/requirements.txt ./content/projects/algorithm-evaluation/
COPY --chown=quanta:quanta content/projects/c-hpc-trading/README.md ./content/projects/c-hpc-trading/
COPY --chown=quanta:quanta content/projects/intelligent-investor/README.md ./content/projects/intelligent-investor/
COPY --chown=quanta:quanta content/projects/news-to-markets/README.md ./content/projects/news-to-markets/
COPY --chown=quanta:quanta content/projects/research/README.md content/projects/research/requirements.txt ./content/projects/research/
COPY --chown=quanta:quanta content/projects/stock-bots/README.md ./content/projects/stock-bots/
COPY --chown=quanta:quanta content/projects/stock-ml/README.md content/projects/stock-ml/requirements.txt ./content/projects/stock-ml/
COPY --chown=quanta:quanta content/projects/strategy-lab/README.md ./content/projects/strategy-lab/
COPY --chown=quanta:quanta content/projects/web3/README.md content/projects/web3/package.json ./content/projects/web3/
COPY --chown=quanta:quanta backend/scripts/import_data.py ./backend/scripts/import_data.py
USER 10001:10001
EXPOSE 8000
HEALTHCHECK --interval=20s --timeout=5s CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/v1/health', timeout=3)" || exit 1
CMD ["python", "-m", "uvicorn", "quanta.main:app", "--app-dir", "backend", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips", "*"]
