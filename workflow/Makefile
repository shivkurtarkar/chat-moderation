export MLFLOW_S3_ENDPOINT_URL	:=	http://172.18.0.2:30608/
export AWS_ACCESS_KEY_ID		:=	admin
export AWS_SECRET_ACCESS_KEY	:=	password
export MLFLOW_S3_IGNORE_TLS		:=	true

RUN_ID := 316eae0f743b4692a9bcb5149e77407d

run: download_data train_model evaluate_model

download_data:
	python download.py

train_model:
	python training.py --dataset reddit

evaluate_model:
	python evaluate.py --dataset reddit --run_id ${RUN_ID}