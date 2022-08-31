FROM python:3.10-slim

WORKDIR /app
COPY Pipfile Pipfile.lock ./

# RUN pipenv install --deploy --ignore-pipfile
# CMD ["pipenv", "run", "python", "hello.py"]

RUN pip install pipenv && \
    apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev libssl-dev && \
    pipenv install --deploy --system && \
    apt-get remove -y gcc python3-dev libssl-dev && \
    apt-get autoremove -y && \
    pip uninstall pipenv -y


COPY . /app

EXPOSE 8501

ENTRYPOINT [ "streamlit", "run" ] 
CMD ["app.py"]