# FROM python:3.8
From ubuntu:20.04 
RUN  apt-get update  && apt install python3-pip libpq-dev -y 

WORKDIR /home

RUN pip install mlflow[extras]==1.9.1 && \
    pip install psycopg2-binary==2.8.5 && \
    pip install boto3==1.15.16 && \
    pip install protobuf==3.20.*

# EXPOSE 5000

ENTRYPOINT ["mlflow", "server"]