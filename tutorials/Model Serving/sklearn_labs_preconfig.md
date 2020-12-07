# Sklearn Example Pre-Config


Check if your namespace is kfserving ready and disable sidecar.injection:
```
export NAMESPACE=your_namespace

kubectl edit namespace $NAMESPACE

...
apiVersion: v1
kind: Namespace
Labels:       
          istio-injection: enabled <---- remove this line
          serving.kubeflow.org/inferenceservice=enabled
...
```

Related issues to sidecar injection:
```
https://github.com/kubeflow/kfserving/issues/1076
https://github.com/kubeflow/kfserving/issues/1032
```


Right now you have to manually create a role binding to enable creation of the inferenceservice
directly from the Labs:

From your CLI, create a new file [role.yaml]:

```
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: inferenceservice-edit
  namespace: your_namespace
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: kubeflow-kfserving-edit
subjects:
- kind: ServiceAccount
  name: default
  namespace: your_namespace
```
And apply:
```
kubectl apply -f role.yaml
```


Get your session key:

```
Log in to Ydata Dashboard with your user account.

View cookies used in the Kubeflow Central Dashboard site from your browser. 
(Settings -> Cookies and other site data -> See all cookies and site data -> 
<Your YData Instance site> -> authservice_session). 

Copy the session key under the "Content" heading and pass it to the 'session' variable in your Notebook
```


