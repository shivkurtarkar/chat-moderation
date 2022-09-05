# chat-moderation
This is poc of Chat moderation part of chat application.

Problem:
Everyone uses social network platform to interact over long distance or to stay in connected.With
this innovation world has become more intimate, accessible and connected. But with good part comes
bad parts as well. Online bulling, scams, frauds have become easier to perform. Hence there is a 
growing need for better realtime message moderation to alert the platform owners who can take 
actions to keep their users safe. Keeping users safe also helps them become more free and open to
interaction and collabration. Thus benifiting whole community. 


## Dataset 
-   [rscience-popular-comment-removal](https://www.kaggle.com/datasets/areeves87/rscience-popular-comment-removal?resource=download)<br>

-- other datasets
-   [jigsaw-toxic-comment-classification-challenge](https://www.kaggle.com/competitions/jigsaw-toxic-comment-classification-challenge/code)<br>
-   [malignant-comment-classification](https://www.kaggle.com/datasets/surekharamireddy/malignant-comment-classification?select=train.csv)<br>
-   [reddit-comment-score-prediction](https://www.kaggle.com/datasets/ehallmar/reddit-comment-score-prediction)<br>
<br>

## Tech stack
- Deployment platform: kubernetes, 
- Experiment tracking: MLFLOW
- Workflow orchestration: argo workflow
- CI/CD: github, argo workflow, argo cd
- Monitoring: prometheus + graphana


# Getting Started

## Create kind cluster
```
kind create cluster --config kind.config
```

## setup nginx Ingress
```
kubectl apply --filename https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/static/provider/kind/deploy.yaml
kubectl wait --namespace ingress-nginx   --for=condition=ready pod   --selector=app.kubernetes.io/component=controller   --timeout=90s
```

## setup argo-cd
```
kubectl apply -k  deployment/argo-cd/overlays/production/ 
```
access argocd at https://argo-cd.127.0.0.1.nip.io
## setup argo-workflow
```
kubectl apply -k  deployment/argo_workflow/overlays/production/
```
## create secrets
```
kubectl apply secrets-template.yaml
```
access argo workflow at https://argo-wf.127.0.0.1.nip.io

## setup mlflow
```
kubectl apply -k deployment/mlflow_setup/manifest/overlays/production/
```
access mlflow at https://mlflow.127.0.0.1.nip.io
## setup workflows resources
```
kubectl apply -k deployment/cicd-workflow/workflows/
```
## run workflow

## deploy appliation
