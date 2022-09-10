# export MLFLOW_TRACKING_URI		:=  https://mlflow.127.0.0.1.nip.io
# export MLFLOW_TRACKING_INSECURE_TLS := true
export MLFLOW_S3_ENDPOINT_URL	:=	https://minio.127.0.0.1.nip.io
export MLFLOW_S3_IGNORE_TLS		:=	true
export AWS_ACCESS_KEY_ID		:=	admin
export AWS_SECRET_ACCESS_KEY	:=	password

export EXPERIMENT 	:=	text-moderation-model

export RUN_ID 		:=	3cfafa786d1643719efc78e9f7251402
export MLFLOW_EXPERIMENT_ID 	:=	1
export MODEL_LOCATION := ./mlruns/1

## using model registry
BUILD_EXTRA_ARGS:=
IMAGE_PREFIX:=
## without model registry
# BUILD_EXTRA_ARGS:=$(shell echo ' -f with_weight_file.dockerfile')
# IMAGE_PREFIX:=standalone-

IMAGE_NAME:=text-classification
IMAGE_VER:=${IMAGE_PREFIX}$(shell git log -1 --format=%H)
IMAGE_FULL_NAME:=${IMAGE_NAME}:${IMAGE_VER}
REGISTRY:=shivamkurtarkar

run: deployment

deployment:
	# python deployment.py
	FLASK_APP=deployment.py  flask run --host=0.0.0.0 --port=8000

test:
	python test_deployment.py

build:
	docker build -t ${IMAGE_FULL_NAME} ${BUILD_EXTRA_ARGS} .
	# kind load docker-image ${IMAGE_NAME}
	docker tag ${IMAGE_FULL_NAME}  ${REGISTRY}/${IMAGE_FULL_NAME}
	docker push ${REGISTRY}/${IMAGE_FULL_NAME}
