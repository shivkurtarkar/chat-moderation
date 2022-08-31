# create config file from file
kubectl create configmap messaging-config --from-file=config/config.ini -o yaml --dry-run=client  > manifest/messaging-config-map.yaml