import requests
query={"model_id":69,"action":"start"}
url="http://172.16.0.205:8010/container-service/container"
response=requests.post(url,json=query)
print(response.json())