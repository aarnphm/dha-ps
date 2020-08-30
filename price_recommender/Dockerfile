FROM python:3.8.5-slim-buster AS base

FROM base AS builder

RUN mkdir /install

WORKDIR /install

COPY ./requirements.txt /requirements.txt

RUN apt-get update && \
    apt-get install -y -qq ca-certificates gcc make && \
    apt-get clean && \
    pip install --prefix=/install  \
        torch==1.6.0+cpu torchvision==0.7.0+cpu -f https://download.pytorch.org/whl/torch_stable.html \
        uvicorn fastapi transformers && \
    pip install --prefix=/install -r /requirements.txt && \
    rm -rf /var/lib/apt/lists/*

FROM base

ENV PATH $HOME/install/bin:$PATH

COPY --from=builder /install /usr/local/

COPY ./api /app/price_recommender/api
COPY ./nlp /app/price_recommender/nlp
COPY ./core /app/price_recommender/core
COPY ./internal /app/price_recommender/internal
COPY ./main.py /app/

WORKDIR /app

EXPOSE 5000

CMD ["python","main.py"]
