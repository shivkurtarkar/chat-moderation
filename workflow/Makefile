export MLFLOW_S3_ENDPOINT_URL	:=	http://172.18.0.2:30608/
export AWS_ACCESS_KEY_ID		:=	admin
export AWS_SECRET_ACCESS_KEY	:=	password
export MLFLOW_S3_IGNORE_TLS		:=	true

run: download_data train_model

download_data:
	python download.py

train_model:
	python training.py --dataset reddit