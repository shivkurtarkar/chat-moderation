# kubectl create secret generic  kagglekeys --from-file=kaggle.json -o yaml --dry-run=client

import argparse
from hera import Task, Workflow, WorkflowService

def say(message:str):
    print(message)


def diamond_wf(argo_host, argo_token):
    with Workflow('diamond', WorkflowService(
            host=argo_host, 
            token=argo_token,
            verify_ssl=False, 
            namespace="argo"
        )) as w:
        a = Task('A', say, func_params=[{'message': 'This is task A!'}])
        b = Task('B', say, func_params=[{'message': 'This is task B!'}])
        c = Task('C', say, func_params=[{'message': 'This is task C!'}])
        d = Task('D', say, func_params=[{'message': 'This is task D!'}])
        a >> b >> d
        a >> c >> d
    w.create()


def main(argo_host, argo_token):
    diamond_wf(argo_host, argo_token)

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