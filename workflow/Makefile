export MLFLOW_TRACKING_URI		:=  https://mlflow.127.0.0.1.nip.io
export MLFLOW_TRACKING_INSECURE_TLS := true
export MLFLOW_S3_ENDPOINT_URL	:=	https://minio.127.0.0.1.nip.io
export MLFLOW_S3_IGNORE_TLS		:=	true
export AWS_ACCESS_KEY_ID		:=	admin
export AWS_SECRET_ACCESS_KEY	:=	password

export ARGO_HOST   := https://argo-wf.127.0.0.1.nip.io
# export ARGO_HOST   := https://argo-wf.127.0.0.1.nip.io/api/v1/workflows/argo
# export ARGO_HOST   := https://172.18.0.2:30923

export SECRET := $(shell kubectl get sa argo-server -o=jsonpath='{.secrets[0].name}' -n argo) 	
export ARGO_TOKEN := $(shell kubectl get secret ${SECRET} -o=jsonpath='{.data.token}' -n argo | base64 --decode)
# export ARGO_TOKEN := "Bearer ${ARGO_TOKEN}"

RUN_ID := 316eae0f743b4692a9bcb5149e77407d

run: download_data train_model evaluate_model

preprocess:
	python preprocess.py \
		--raw_data_path './output' \
		--dest_path './output' \
		--dataset reddit
download_data:
	python download.py \
		--dataset 'areeves87/rscience-popular-comment-removal' \
    	--output_dir  './output'

train_model:
	python training.py --dataset reddit

evaluate_model:
	python evaluate.py --dataset reddit --run_id ${RUN_ID}


argo_workflow:	
	python workflow.py --argo_host ${ARGO_HOST}	 --argo_token ${ARGO_TOKEN}

build:
	docker build -t workflow-python .
	kind load docker-image workflow-python 