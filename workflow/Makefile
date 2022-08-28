export MLFLOW_TRACKING_URI		:=  http://172.18.0.2:31989/
export MLFLOW_S3_ENDPOINT_URL	:=	http://172.18.0.2:30608/
export AWS_ACCESS_KEY_ID		:=	admin
export AWS_SECRET_ACCESS_KEY	:=	password
export MLFLOW_S3_IGNORE_TLS		:=	true

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


ARGO_HOST   := https://172.18.0.2:31784
ARGO_TOKEN  := eyJhbGciOiJSUzI1NiIsImtpZCI6ImhrVVhIeUZYc190a3lFLWpQTDlVMnFUZUV3UlhnV1NqZHZ2bEVBTTdKWFEifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJhcmdvIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImFyZ28tc2VydmVyLXRva2VuLWQ0NHJiIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFyZ28tc2VydmVyIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiODRlNDhmZjAtN2JhNS00MjYyLThjMDQtYTFiYjk1NzQ0NTczIiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50OmFyZ286YXJnby1zZXJ2ZXIifQ.ZsPasuh5VTQ4ASpd_oQTRVKXkN43Ic8xYI_CO-TPcl2Tyarp_OZU7pQuEbukdHSj5KbUz9SbSTCiQBEzzJsnKJvRUjmJsm3MwhvAsc7IHaZ9kLp8MRHpcgz8EjIzB0DX0hnOUM8ZsG9jqOBbH5FhH6RxGiTE8dOr7H1eahkO0JDu9XOhDT1zT7VMt31gzBaRSlAqSIIVXVCU7Kd9w1fBoc7Ar-I2Dpa54IpdJNrUseXA1563Gm9blJYx-zM_ZV1F_n-eULcDKltz3PSZYlAFm_sSVjvc0gL4m1EYoy4NgTm_FJBXWJy4pFcYMGM5zNols4-bhcZ3TAmi6lkjuL8ZBQ

argo_workflow:
	python workflow.py --argo_host ${ARGO_HOST}	 --argo_token ${ARGO_TOKEN}

build:
	docker build -t workflow-python .
	kind load docker-image workflow-python 