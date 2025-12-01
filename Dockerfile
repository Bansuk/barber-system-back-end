FROM python:3.10-alpine AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt .
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    libffi-dev \
    python3-dev \
    && pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir --prefix=/install -r requirements.txt \
    && apk del .build-deps

FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/install/bin:$PATH" \
    PYTHONPATH="/install/lib/python3.10/site-packages" \
    PRETTIFY_JSON_RESPONSE=1 \
    FLASK_APP=app.py \
    FLASK_RUN_HOST=0.0.0.0

COPY --from=builder /install /install

RUN addgroup -g 1000 app && \
    adduser -D -u 1000 -G app app

USER app
WORKDIR /app

COPY --chown=app:app . .

EXPOSE 5000

CMD ["flask", "run", "--port=5000"]