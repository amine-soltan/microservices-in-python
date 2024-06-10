# microservices-in-python



This project contains microservices implemented in Python using Flask. The microservices provide current Bitcoin prices and calculate daily and monthly averages.

## Requirements

- Python 3.8 or higher
- Virtualenv
- SQLite3
- Docker
- Kubernetes (Minikube or any Kubernetes cluster)
- Helm
- HashiCorp Vault
  
## Steps

1. **Clone the Repository:**


```bash
   git clone https://github.com/amine-soltan/microservices-in-python.git
   cd microservices-in-python
```
2. **Set up a virtual environment:**

Local Development Setup

```bash
python -m venv tutorial-env
source tutorial-env/bin/activate  # On Windows use `tutorial-env\Scripts\activate`
```

3. **Install dependencies**

```bash
 pip install -r requirements.txt
```

4. **Start Vault**
   
Ensure Vault is running locally. You can start Vault with the development server for testing:

```bash
vault server -dev
```

5. **Set environment variables**
   
Set the VAULT_ADDR and VAULT_TOKEN environment variables:
For Windows PowerShell:

```bash
$env:VAULT_ADDR="http://127.0.0.1:8200"
$env:VAULT_TOKEN="your-vault-token"
```

6. **Store the token in Vault**

```bash
   vault kv put secret/microservices AUTH_TOKEN='your-auth-token'
```

7. **Run Flask Application**

   ```bash
   python app.py
   ```


8. **Build and Push the Docker Image:**

```sh
docker build -t aminesoltan/microservice-in-python .
docker push aminesoltan/microservice-in-python:latest
```

9. **Start Minikube:**

```sh
minikube start
```

10. **Deploy with Helm:**

```sh
helm install microservice-release ./charts/microservice-chart
```

11. **Check Deployment Status:**

```sh
kubectl get all
```

12. **Port Forward to Access the Application:**

```sh
kubectl port-forward service/microservice-release-service 5000:5000
```

13. **Test the Endpoints:**

Using Curl:

```sh
curl -H "Authorization: your-vault-token" http://localhost:5000/current-price
curl -H "Authorization: your-vault-token" http://localhost:5000/averages
```

Using Postman:

     Open Postman and create a new GET request to http://127.0.0.1:5000/current-price and http://localhost:5000/averages.
     Go to the "Headers" tab.
     Add a new header with the key Authorization and the value set to the token.

