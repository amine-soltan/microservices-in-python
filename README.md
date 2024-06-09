  #                                microservices-in-python


## * How to Test the Application


## Prerequisites
* **Docker** 
* **Minikube** 
* **Helm**
  
## Steps

1. **Clone the Repository:**


```bash
   git clone https://github.com/amine-soltan/microservices-in-python.git
   cd microservices-in-python
```

2. **Build and Push the Docker Image:**

```sh
docker build -t aminesoltan/microservice-in-python .
docker push aminesoltan/microservice-in-python:latest
```

3. **Start Minikube:**

```sh
minikube start
```

4. **Deploy with Helm:**

```sh
helm install microservice-release ./charts/microservice-chart
```

5. **Check Deployment Status:**

```sh
kubectl get all
```

6. **Port Forward to Access the Application:**

```sh
kubectl port-forward service/microservice-release-service 5000:5000
```

7. **Test the Endpoints:**

```sh
curl -H "Authorization: 37c9a1b2cf9b1d3a9d87e6be6b37d3a4" http://localhost:5000/current-price
curl -H "Authorization: 37c9a1b2cf9b1d3a9d87e6be6b37d3a4" http://localhost:5000/averages
```
