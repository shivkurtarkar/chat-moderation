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

ENV FLASK_APP=/app/deployment.py

ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=9696

ENTRYPOINT flask run 



