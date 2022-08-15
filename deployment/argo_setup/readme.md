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