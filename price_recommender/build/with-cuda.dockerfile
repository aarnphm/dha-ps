# base for cuda-enabled PyTorch images
FROM pytorch/pytorch:1.6.0-cuda10.1-cudnn7-runtime AS builder

LABEL maintainer="aaronpham0103@gmail.com"

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python \
    && cd /usr/local/bin \
    && ln -s /opt/poetry/bin/poetry poetry

FROM nvidia/cuda:10.1-base-ubuntu16.04

ARG CONDA_DIR=/opt/conda/

ARG POETRY_DIR=/opt/poetry/

ENV PATH $CONDA_DIR/bin:$POETRY_DIR/bin:$PATH

COPY --from=builder /opt/conda/ $CONDA_DIR

COPY --from=builder /opt/poetry $POETRY_DIR

WORKDIR /

COPY ./poetry.lock ./pyproject.toml ./

COPY ./reload-start.sh /reload-start.sh

RUN chmod +x /reload-start.sh && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

COPY ./nlp /app/price_recommender/nlp
COPY ./api /app/price_recommender/api
COPY ./core /app/price_recommender/core
COPY ./internal /app/price_recommender/internal

COPY ./main.py /app/

WORKDIR /app

EXPOSE 5000

CMD ["uvicorn","--reload","--host","0.0.0.0","--port","5000","main.app"]
