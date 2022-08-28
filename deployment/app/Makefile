export MLFLOW_TRACKING_URI		:= http://172.18.0.2:31989/
export MLFLOW_S3_ENDPOINT_URL	:= http://172.18.0.2:30608/
export AWS_ACCESS_KEY_ID		:= admin
export AWS_SECRET_ACCESS_KEY	:= password
export MLFLOW_S3_IGNORE_TLS		:= true

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