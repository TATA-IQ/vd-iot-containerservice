import requests
query={"model_id":9,"action":"status"}
url="http://172.16.0.204:8010/container-service/container"
response=requests.post(url,json=query)
print(response.json())