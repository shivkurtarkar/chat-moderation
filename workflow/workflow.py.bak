# kubectl create secret generic  kagglekeys --from-file=kaggle.json -o yaml --dry-run=client

import argparse
from hera import Task, Workflow, WorkflowService
from hera import SecretVolume, Resources,ImagePullPolicy, AccessMode, EmptyDirVolume, OutputArtifact, InputArtifact

import download_dataset
from preprocess import run as preprocess_run

def training_pipeline(argo_host, argo_token):
    # workflow_name= 'text_classification_training'
    workflow_name= 'download-preprocess'
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
            download_dataset.download_from_kaggle,
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
            preprocess_run,
            func_params=[{
                "raw_data_path" :dataset_path,
                "dest_path": dataset_path,
                "dataset": "reddit"
            }],
            input_artifacts=[InputArtifact("dataset", dataset_path, "download-kaggle-data", "dataset")],
            # output_artifacts=[OutputArtifact("dataset", dataset_path)],
            image='workflow-python:latest',
            image_pull_policy=ImagePullPolicy.IfNotPresent,
            command=["python"]
        )
        # evaluate_model_task = Task()
        
        download_dataset_task >> preprocess_data_task #train_model_task #>> evaluate_model_task
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