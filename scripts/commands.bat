oc apply -f infrastructure/k8s/mongo-pvc.yaml
oc apply -f infrastructure/k8s/mongo-service.yaml
oc apply -f infrastructure/k8s/mongo-deployment.yaml

docker build -t db-soldier .
docker tag db-soldier shuki120/db-soldier:latest
docker push shuki120/db-soldier:latest

oc apply -f infrastructure/k8s/db-soldier-service.yaml
oc apply -f infrastructure/k8s/db-soldier-deployment.yaml
oc apply -f infrastructure/k8s/db-soldier-route.yaml
