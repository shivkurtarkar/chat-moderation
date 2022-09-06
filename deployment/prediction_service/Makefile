# export MLFLOW_TRACKING_URI		:=  https://mlflow.127.0.0.1.nip.io
# export MLFLOW_TRACKING_INSECURE_TLS := true
export MLFLOW_S3_ENDPOINT_URL	:=	https://minio.127.0.0.1.nip.io
export MLFLOW_S3_IGNORE_TLS		:=	true
export AWS_ACCESS_KEY_ID		:=	admin
export AWS_SECRET_ACCESS_KEY	:=	password

export RUN_ID 		:=	7909fed65ee944eabee7de04cd1ba370
export EXPERIMENT 	:=	text-moderation-model

IMAGE_NAME:=text-classification
IMAGE_VER:=v2
IMAGE_FULL_NAME:=${IMAGE_NAME}:${IMAGE_VER}
REGISTRY:=shivamkurtarkar

run: deployment

deployment:
	# python deployment.py
	FLASK_APP=deployment.py  flask run --host=0.0.0.0 --port=8000

test:
	python test_deployment.py

build:
	docker build -t ${IMAGE_FULL_NAME} .
	# kind load docker-image ${IMAGE_NAME}
	docker tag ${IMAGE_FULL_NAME}  ${REGISTRY}/${IMAGE_FULL_NAME}
	docker push ${REGISTRY}/${IMAGE_FULL_NAME}