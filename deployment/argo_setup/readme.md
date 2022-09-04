# Argo Workflow
-----ingress
kind create cluster --config kind.config
kubectl apply --filename https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/static/provider/kind/deploy.yaml
kubectl wait --namespace ingress-nginx   --for=condition=ready pod   --selector=app.kubernetes.io/component=controller   --timeout=90s

kubectl run hello   --expose   --image nginxdemos/hello:plain-text   --port 80
nano ingress.yaml
kubectl create -f ingress.yaml 
docker run   --add-host hello.dustinspecker.com:172.18.0.2   --net kind   --rm   curlimages/curl:7.71.0


## argo setup
kubectl create ns argo
wget https://raw.githubusercontent.com/argoproj/argo-workflows/stable/manifests/install.yaml .

kubectl apply -f install.yaml -n argo
kubectl -n argo create rolebinding default-admin --clusterrole=admin --serviceaccount=argo:default


kubectl apply -f argo_workflow_ingress.yaml -n argo


SECRET=$(kubectl get sa argo-server -o=jsonpath='{.secrets[0].name}' -n argo) 
ARGO_TOKEN="Bearer $(kubectl get secret $SECRET -o=jsonpath='{.data.token}' -n argo | base64 --decode)"
$echo $ARGO_TOKEN
$curl https://localhost:2746/api/v1/workflows/argo -H "Authorization: $ARGO_TOKEN"

refrence
https://towardsdatascience.com/creating-containerized-workflows-with-argo-ec1011b04370


## ARGOCD 
### install argocd
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

#### change argocd service type
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'
kubectl get svc argocd-server -n argocd

#### get password 
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo

#### argocd cli
sudo apt install argocd

argocd login <server_ip:port>

kubectl config get-contexts -o name
argocd cluster add kind-kind


<!-- kubectl create ns chat-moderation
argocd app create text-classification --repo git@github.com:shivkurtarkar/chat-moderation.git --path deployment/app/manifest  --dest-server https://kubernetes.default.svc --dest-namespace chat-moderation

argocd app get text-classification
argocd app sync text-classification -->