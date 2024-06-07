# microservices-in-python
microservices-in-python

# How to Test the Application
## Prerequisites
- Docker
- Minikube
- Helm
## Steps

1. Clone the Repository:

sh
Copier le code
git clone https://github.com/amine-soltan/microservices-in-python.git
cd microservices-in-python
2. Build and Push the Docker Image:

sh
Copier le code
docker build -t your-dockerhub-username/microservice-in-python .
docker push your-dockerhub-username/microservice-in-python
3. Start Minikube:

sh
Copier le code
minikube start
4. Deploy with Helm:

sh
Copier le code
helm install microservice-release ./charts/microservice-chart
5. Check Deployment Status:

sh
Copier le code
kubectl get all
6. Port Forward to Access the Application:

sh
Copier le code
kubectl port-forward service/microservice-release-service 5000:5000
7.Test the Endpoints:

sh
Copier le code
curl -H "Authorization: 37c9a1b2cf9b1d3a9d87e6be6b37d3a4" http://localhost:5000/current-price
curl -H "Authorization: 37c9a1b2cf9b1d3a9d87e6be6b37d3a4" http://localhost:5000/averages

