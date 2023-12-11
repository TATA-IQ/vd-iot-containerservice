import requests
class model_status:
    def update(url, model_id, status, message):
        try:
            print(model_id, status, message)
            json_msg = {"model_id":int(model_id), "status":int(status), "message":message}
            response=requests.post(url,json=json_msg)
            print(response.json())
        except Exception as exp:
            print(exp)
