kubectl apply -f redis/redis-deployment.yaml
kubectl apply -f redis/redis-service.yaml
kubectl apply -f minio/minio-external-service.yaml
helm install -f minio/minio-config.yaml -n minio-ns --create-namespace minio-proj bitnami/minio
# kubectl apply -f minio/minio-dep.yaml
# kubectl apply -f minio/minio-external-service.yaml

sleep 5
kubectl apply -f rest/rest-service.yaml
kubectl apply -f rest/rest-deployment.yaml
# kubectl apply -f rest/rest-ingress.yaml
kubectl apply -f js_frontend/frontend-deployment.yaml
kubectl apply -f js_frontend/frontend-service.yaml
# kubectl apply -f worker/worker-deployment.yaml

sleep 10
kubectl port-forward --address 0.0.0.0 service/rest 5000:5000 &
kubectl port-forward --address 0.0.0.0 service/site 3000:3000 &

# If you're using minio from the kubernetes tutorial this will forward those
# kubectl port-forward -n minio-ns --address 0.0.0.0 service/minio-proj 9000:9000 &
# kubectl port-forward -n minio-ns --address 0.0.0.0 service/minio-proj 9001:9001 &
# while true; do kubectl port-forward --namespace minio-ns svc/minio-proj 9001:9001&; done

