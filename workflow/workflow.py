# kubectl create secret generic  kagglekeys --from-file=kaggle.json -o yaml --dry-run=client

import argparse
from hera import Task, Workflow, WorkflowService
from hera import SecretVolume, Resources,ImagePullPolicy, AccessMode, EmptyDirVolume, OutputArtifact, InputArtifact
from hera import VariableAsEnv

import uuid

def download_from_kaggle(dataset, output_dir, unzip):
    import os
    print("dirs--")
    print(os.listdir())
    print()
    from download_dataset import download_from_kaggle
    print("import sucess")
    download_from_kaggle(dataset, output_dir, unzip)
    print("download success")

def preprocess_data(raw_data_path, dest_path, dataset):
    from preprocess import run as preprocess_run
    preprocess_run(raw_data_path, dest_path, dataset)
    print("preprocess success")

def train_model(data_path, dataset, experiment):
    from training import run as training_run
    training_run(data_path, dataset, experiment)
    print("training success")

def evaluate_model():
    pass

def training_pipeline(argo_host, argo_token):    
    # workflow_name= 'text_classification_training'
    unique_code= str(uuid.uuid4())
    workflow_name= f'download-preprocess-{unique_code}'
    runin_namespace ='argo'
    with Workflow(workflow_name, WorkflowService(
            host=argo_host,
            token=argo_token,
            verify_ssl=False,
            namespace=runin_namespace
        ),
        namespace=runin_namespace
        ) as w:
        dataset_path="/app/output"

        download_dataset_task = Task(
            'download-kaggle-data',
            download_from_kaggle,
            func_params=[{
                "dataset": 'areeves87/rscience-popular-comment-removal',
                "output_dir": './output',
                "unzip":True
            }],
            resources=Resources(volumes=[
                SecretVolume(
                    secret_name="kagglekeys",
                    mount_path="/home/newuser/.kaggle"
                )
            ]),
            output_artifacts=[OutputArtifact("dataset", dataset_path)],
            image='workflow-python:latest',
            image_pull_policy=ImagePullPolicy.IfNotPresent,
            command=["python"]
        )
        preprocess_data_task  = Task(
            'preprocess-data',
            preprocess_data,
            func_params=[{
                "raw_data_path" :dataset_path,
                "dest_path": dataset_path,
                "dataset": "reddit"
            }],
            input_artifacts=[InputArtifact("dataset", dataset_path, "download-kaggle-data", "dataset")],            
            output_artifacts=[OutputArtifact("dataset", dataset_path)],
            image='workflow-python:latest',
            image_pull_policy=ImagePullPolicy.IfNotPresent,
            command=["python"]
        )
        train_model_task  = Task(
            'train-model-task',
            train_model,            
            func_params=[{
                "data_path" :dataset_path,
                "dataset": "reddit",
                "experiment": "text-moderation-model"                
            }],
            variables=[
                VariableAsEnv(name="MLFLOW_TRACKING_URI", value="http://172.18.0.2:31989/"),  # value="http://mlflow-tracking-service:5000/"), 
                VariableAsEnv(name="MLFLOW_S3_ENDPOINT_URL", value="http://172.18.0.2:30608/"),  # value="http://minio:9000/"), 
                VariableAsEnv(name="AWS_ACCESS_KEY_ID", value="admin"),
                VariableAsEnv(name="AWS_SECRET_ACCESS_KEY", value="password"),
                VariableAsEnv(name="MLFLOW_S3_IGNORE_TLS", value="true")
            ],
            input_artifacts=[InputArtifact("dataset", dataset_path, "preprocess-data", "dataset")],            
            # output_artifacts=[OutputArtifact("dataset", dataset_path)],
            image='workflow-python:latest',
            image_pull_policy=ImagePullPolicy.IfNotPresent,
            command=["python"]
        )
        # evaluate_model_task = Task()
        
        download_dataset_task >> preprocess_data_task >> train_model_task #>> evaluate_model_task
    w.create()

def main(argo_host, argo_token):
    training_pipeline(argo_host, argo_token)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--argo_host',
        help='ARGO HOST URL'
    )
    parser.add_argument(
        '--argo_token',
        help='ARGO Token'
    )
    
    args = parser.parse_args()
    main(args.argo_host, args.argo_token)