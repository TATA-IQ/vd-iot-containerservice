import requests
query={"model_id":182,"action":"start"}
url="http://172.16.0.206:8011/container-service/container"
response=requests.post(url,json=query)
print(response.json())