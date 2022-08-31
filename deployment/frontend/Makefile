IMAGE_NAME:=messaging-app
IMAGE_VER:=v2
IMAGE_FULL_NAME:=${IMAGE_NAME}:${IMAGE_VER}
REGISTRY:=shivamkurtarkar

run: deployment

deployment:
	streamlit run app.py	

build:
	docker build -t ${IMAGE_FULL_NAME} .
	# kind load docker-image ${IMAGE_NAME}
	docker tag ${IMAGE_FULL_NAME}  ${REGISTRY}/${IMAGE_FULL_NAME}
	docker push ${REGISTRY}/${IMAGE_FULL_NAME}