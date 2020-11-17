namespace=app-mask
kubectl delete -n $namespace -f databaseModel.yaml
kubectl delete -n $namespace -f secret.yaml
kubectl delete -n $namespace -f configMap.yaml
kubectl delete -n $namespace -f deployment.yaml
kubectl delete -n $namespace -f service.yaml
kubectl delete -n $namespace -f ingress.yaml
kubectl delete -n $namespace -f ingress.yaml
kubectl delete ns $namespace
