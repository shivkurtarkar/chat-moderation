from mlflow.tracking import MlflowClient
from mlflow.entities import ViewType
from mlflow.entities.model_registry.model_version_status import ModelVersionStatus
from mlflow.exceptions import RestException
import mlflow
import time


class Stages:
    staging     =   'staging'
    production  =   'production'
    archived    =   'archived'

def wait_until_ready(model_name, model_version):
    client=MlflowClient()
    for _ in range(10):
        model_version_details = client.get_model_version(model_name, model_version)
        status =  ModelVersionStatus.from_string(model_version_details.status)
        print(f'Model status: {status}')
        if status == ModelVersionStatus.READY:
            break
        time.sleep(1)

def create_registered_model(registered_model_name, description=None):
    client = MlflowClient()
    try:
        client.create_registered_model(
            name=registered_model_name,
            description=description
        )
        print("model registered")
    except RestException as e:
        if e.error_code=='RESOURCE_ALREADY_EXISTS' :            
            print('Resource already exists, skipping')
        else:
            raise e

def main(experiment_name, registered_model_name):
    # create registerd model
    create_registered_model(registered_model_name)

    # 
    client = MlflowClient()

    experiment = client.get_experiment_by_name(experiment_name)
    print(experiment)

    runs = client.search_runs(
        experiment_ids=experiment.experiment_id,
        run_view_type=ViewType.ACTIVE_ONLY,
        max_results=5        
    )
    print(dir(client))
    
    best_run=runs[0]
    print(best_run)
    print()
    model_version = client.get_latest_versions(name = registered_model_name)
    print(model_version)
    print(f'run_id: {best_run.info.run_id}')
    
    ## register model
    artifact_path='model'
    model_uri = f'runs:/{best_run.info.run_id}/{artifact_path}'
    model_details = mlflow.register_model(model_uri=model_uri, name=registered_model_name)
    wait_until_ready(model_details.name, model_details.version)
    print(f'{model_uri} model registered')

    ## transition to staging
    latest_version_info = client.get_latest_versions(registered_model_name, stages=[Stages.staging])
    if len(latest_version_info)>0:
        last_model_version = latest_version_info[0].version
        model_version_details = client.transition_model_version_stage(
            name=registered_model_name,
            version=last_model_version,
            stage=Stages.archived,
        )
        print(f"The {Stages.archived} current model : '{last_model_version}'")
    model_version_details = client.transition_model_version_stage(
        name=registered_model_name,
        version=model_details.version,
        stage=Stages.staging,
    )    
    print(f"The current model stage is: '{model_version_details.current_stage}'")
    time.sleep(5)

    ## transition to production
    latest_version_info = client.get_latest_versions(registered_model_name, stages=[Stages.production])
    if len(latest_version_info)>0:
        last_model_version = latest_version_info[0].version
        model_version_details = client.transition_model_version_stage(
            name=registered_model_name,
            version=last_model_version,
            stage=Stages.archived,
        )
        print(f"The {Stages.archived} current model : '{last_model_version}'")
    model_version_details = client.transition_model_version_stage(
        name=registered_model_name,
        version=model_details.version,
        stage=Stages.production,
    )
    print(f"The current model stage is: '{model_version_details.current_stage}'")

    # mlflow.register_model(model_uri=best_run.info.run_id, name=registered_model_name)

if __name__ == '__main__':
    experiment_name='text-moderation-model'
    registered_model_name='text-moderation-m1'
    main(experiment_name, registered_model_name)