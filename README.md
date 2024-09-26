# Istio-ZeroTrust

An access control solution for microservices deployed on Kubernetes and Istio Service Mesh, verifying every access attempt on every service, and enforcing the principle of least privilege: Who is allowed access, through which service/sub-system, and to which resources and functionality on the target service.

## Blog Post

For more info see the [Blog Post](https://safelyup.net/).

## Local Deployment - Minikube

Kubernetes and Istio must already be deployed.

Build the application Docker images:
```
cd ./auth-app
docker build --no-cache -t auth-app:v1 .
cd ../demo-app
docker build --no-cache -t demo-app:v1 .
cd ../
```

And push the images to a container registry. If you are using Minikube locally, you can load the images to its local cache:
```
minikube image load auth-app:v1
minikube image load demo-app:v1
```

Generate the keys for JWT generation and validation, using the `keygen.py` Python cli tool:

```
python3 -m venv ./venv
source ./venv/bin/activate
pip3 install jwcrypto
python3 keygen.py
```

Update the manfest files `manifests/authz.yaml` and `manifests/workload.yaml` with the 3 keys generated in the previous step.

Next, create the `demo` namespace on Kubernetes and apply the manifests:
```
kubectl create namespace demo
kubectl label namespace demo istio-injection=enabled
cd ./manifests
kubectl apply -f workload.yaml,networking.yaml,authz.yaml
```

## Local Demo - Minikube

Add `auth.local` and `demo.local` to your local `/etc/hosts` file:
```
echo "127.0.0.1	auth.local demo.local" >> /etc/hosts
```

Create the Minikube tunnel to locally access the Istio gateway:
```
minikube tunnel
```

On another terminal use `curl` cli tool to generate JWT, then use that token to call the demo API - services `a` and `b`:
```
curl -X POST auth.local/token -H "Content-Type: application/json" -d '{"username":"demo"}'
"<TOKEN>"

curl -X POST auth.local/validate -H "Content-Type: application/json" -d '{"token":"<TOKEN>"}'
[{"alg":"RS256","typ":"JWT"},{"exp":1727179120,"iat":1727175520,"iss":"demo.local","jti":"1XIC7SG94GTACNpyt-oSOw","nbf":1727175520,"permission":"all","role":"developer","sub":"example","username":"demo"}]

curl demo.local/a -H "Authorization: Bearer <TOKEN>"
curl demo.local/b -H "Authorization: Bearer <TOKEN>"
curl demo.local/a/call/b -H "authorization: Bearer <TOKEN>"
```
