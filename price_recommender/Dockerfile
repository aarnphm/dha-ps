FROM python:3.8.5-slim-buster AS base

FROM base AS builder

ARG use_pre_train_model=true

RUN mkdir /install

WORKDIR /install

COPY ./requirements.txt /requirements.txt

RUN apt-get update && \
    apt-get install -y -qq ca-certificates gcc make curl unzip && \
    apt-get clean && \
    pip install --prefix=/install torch==1.6.0+cpu torchvision==0.7.0+cpu -f https://download.pytorch.org/whl/torch_stable.html \
    uvicorn fastapi sentence_transformers && \
    pip install --prefix=/install -r /requirements.txt && \
    rm -rf /var/lib/apt/lists/* && \
    if [ "$use_pre_train_model" = "true" ]; then \
    # download model from server
    curl https://sbert.net/models/distilbert-base-nli-stsb-mean-tokens.zip --output model.zip && \
    unzip model.zip -d /model && \
    rm model.zip; \
    fi

FROM base

ENV PATH $HOME/install/bin:$PATH

ARG model_dir=price_recommender/distilbert-base-nli-stsb-mean-tokens/

COPY --from=builder /install /usr/local/

COPY ./api /app/price_recommender/api
COPY --from=builder /model /app/${model_dir}
COPY ./core /app/price_recommender/core
COPY ./internal /app/price_recommender/internal
COPY ./main.py /app/

WORKDIR /app

EXPOSE 5000

CMD ["python","main.py"]
