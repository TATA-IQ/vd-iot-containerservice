import requests
url="http://172.16.0.204:8051/modelvalidate"
json={"model_id":4,"framework_id":2}
# url="http://172.16.0.204:8001/detection/yolov8/validate"
# json={"model_id":4}

response=requests.post(url,json=json)
print(response.json())