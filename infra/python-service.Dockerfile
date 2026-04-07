FROM python:3.13-slim

ARG SERVICE_PATH=backend

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /workspace

COPY backend /workspace/backend

WORKDIR /workspace/${SERVICE_PATH}

RUN python -m pip install --upgrade pip \
    && python -m pip install -r requirements.txt

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
