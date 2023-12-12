import requests
query={"model_id":2,"action":"start"}
url="http://localhost:8010/container-service/container"
response=requests.post(url,json=query)
print(response.json())