FROM python:3.10-slim

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv && \
    apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev libssl-dev && \
    pipenv install --deploy --system && \
    apt-get remove -y gcc python3-dev libssl-dev && \
    apt-get autoremove -y && \
    pip uninstall pipenv -y && \
    rm -rf /var/lib/apt/lists/*

COPY ./*.py ./


ENV RUN_ID 3cfafa786d1643719efc78e9f7251402
RUN mkdir -p ./models/${RUN_ID}
ENV MODEL_PATH_PREFIX /app/models
COPY ./mlruns/1/${RUN_ID} ./models/${RUN_ID}

COPY ./*.py ./

ENV FLASK_APP=/app/deployment.py

ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=9696

ENTRYPOINT flask run 



