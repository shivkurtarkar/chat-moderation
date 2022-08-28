FROM python:3.10-slim

WORKDIR /app
ENV PYTHONPATH='/app'
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

RUN chmod 777 /app
RUN mkdir /app/output
RUN chmod 777 /app/output

COPY ./workflow/*.py /app/

RUN useradd -ms /bin/bash newuser
USER newuser
RUN echo $HOME

ENTRYPOINT [ "python" ] 