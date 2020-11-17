namespace=app-dev
kubectl create ns $namespace
kubectl apply -n $namespace -f databaseModel.yaml
kubectl apply -n $namespace -f secret.yaml
kubectl apply -n $namespace -f configMap.yaml
kubectl apply -n $namespace -f deployment.yaml
kubectl apply -n $namespace -f service.yaml
kubectl apply -n $namespace -f ingress.yaml
kubectl apply -n $namespace -f ingress.yaml
