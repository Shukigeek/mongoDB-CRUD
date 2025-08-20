db-soldier is a FastAPI-based web application that 
stores and manages data about enemy soldiers in a MongoDB database.
The project is fully containerized using Docker and is designed 
to run on OpenShift with Kubernetes. 
It includes manifests for deploying both the MongoDB database 
and the FastAPI app, as well as services 
and routes for external access.

MongoDB stores the data in a persistent volume, 
with credentials and configuration handled via Kubernetes secrets.
The FastAPI service connects to MongoDB using these secrets 
and exposes its endpoints on port 8000. The OpenShift route maps 
the service to an external URL so users can access the API 
and the interactive Swagger documentation (/docs) directly in 
a browser.

There’s also a helper batch script for 
Windows that automates building the Docker image, 
pushing it to a registry, deploying all resources on OpenShift, 
and opening the FastAPI docs automatically. 
This makes it easy to deploy and start interacting 
with the application with minimal manual steps.

In short, the project is a fully containerized, 
OpenShift-deployable FastAPI + MongoDB system with 
secure configuration management and a 
ready-to-use API documentation interface.


infrastructure/k8s/
├─ mongo-pvc.yaml # MongoDB persistent volume claim
├─ mongo-service.yaml # MongoDB service
├─ mongo-deployment.yaml # MongoDB deployment
├─ db-soldier-service.yaml # db-soldier service
├─ db-soldier-deployment.yaml # db-soldier deployment
├─ db-soldier-route.yaml # db-soldier route
deploy-and-open-docs.bat # Deployment script
services/dataloader/ # FastAPI app source code
Dockerfile # Docker image definition
requirements.txt # Python dependencies