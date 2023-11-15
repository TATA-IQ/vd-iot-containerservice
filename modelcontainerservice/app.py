import requests
from src.build import Build
from config_parser.parser import ParseConfig
import logging
from logging.handlers import TimedRotatingFileHandler
from fastapi import FastAPI
from src.parser import Config
from model.port_model import PortModel
import docker
from model.request_model import RequestModel



logger = logging.getLogger("Rotating Log")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger.setLevel(logging.ERROR)

handler = TimedRotatingFileHandler("logs/log", "D", 1, 7)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.log(40, msg="Database Started")

conf=Config.yamlconfig("config/config.yaml")
app=FastAPI()



def check_port(url,model_id=None):
    if model_id is not None:
        response=requests.get(url,json={"model_id":model_id})
    else:
        response=requests.get(url,json={})

    return response.json()["data"]

def get_model_config(url,model_id):
    response=requests.get(url,json={"model_id":model_id})
    return response.json()["data"]


def update_port(url,model_id,port_number):
    print(f"update for model id port {model_id} {port_number}")
    response=requests.post(url=url,json={"model_id":model_id,"port_number":port_number})
    print("============pdate data=========")
    print(response.text)


    





def active_model(model_id):
    print("======Requestmodel====")
    
    giturls=conf[0]["giturls"]
    apis=conf[0]["apis"]
    git_ssh_comand=conf[0]["git_ssh_command"]
    local_repo_path= conf[0]["local_repo_path"]
    # model_id=data.model_id
    port_data=check_port(apis["port_details"],model_id)
    model_conf=get_model_config(apis["model_config"],model_id)[0]
    if len(port_data)>0:
        print("===length of port data====")
        print(port_data)
        port_number=port_data[0]["port_number"]
        
    else:
        port_data=check_port(apis["port_details"])
        print("==port data====")
        print(port_data)
        port_number=port_data[0]["port_number"]
        update_port(apis["update_port"],model_id,port_number)
    if model_conf["model_type"].lower()=="object detection":
        model_data=giturls["detection"][model_conf["model_framework"].lower()]
    if model_conf["model_type"].lower()=="ocr":
        model_data=giturls["detection"][model_conf["model_framework"].lower()]
    

    
    
    dictdata={
        "git_url":model_data["url"],
        "git_branch": model_data["branch"],
        "local_repo_path":local_repo_path,

        "model_id": str(model_conf["model_id"]),
        "model_framework": model_conf["model_framework"],
        "model_name": model_conf["model_name"],
        "model_port":port_number,
        "model_type":model_conf["model_type"]

    }
    print("====?",dictdata)
    buld=Build(apis, dictdata,git_ssh_comand)
    response=buld.buildModel()
    return response


def get_docer_status(model_id):
    # model_id=data.model_id
    print("====checking status=====",model_id)
    apis=conf[0]["apis"]
    model_conf=get_model_config(apis["model_config"],model_id)[0]
    container_name=str(model_conf["model_id"])+"_"+str(model_conf["model_framework"])+"_"+str(model_conf["model_name"])
    container_name = "".join(container_name.strip().lower().split())
    print("cotainer name:=>",container_name)
    client = docker.from_env()
    container_list=client.containers.list(filters={"name":container_name})
    print("====container_list=====",container_list)
    if len(container_list)==0:
        return {"status":0,"message":"container does not exist"}
    else:
        status=container_list[0].status
        if status=="running":
            return {"status":1,"message":"container running"}
        else:
            return {"status":1,"message":"container stopped"}
    return {"status":0,"message":"container does not exist"}



def stop_container(model_id):
    model_id=model_id
    apis=conf[0]["apis"]
    model_conf=get_model_config(apis["model_config"],model_id)[0]
    container_name=str(model_conf["model_id"])+"_"+str(model_conf["model_framework"])+"_"+str(model_conf["model_name"])
    container_name = "".join(container_name.strip().lower().split())
    client = docker.from_env()
    
    container_list=client.containers.list(filters={"name":container_name})

    if len(container_list)==0:
        return {"status":0,"message":"container does not exist"}
    else:
        status=container_list[0].status
        if status=="running":
            return {"status":1,"message":"container running"}
        else:
            return {"status":1,"message":"container stopped"}
    return {"status":0,"message":"container does not exist"}



@app.post("/container-service/container")
def call_contatiner_service(data:RequestModel):
    print("===Request data====",data)
    model_id=data.model_id
    action=data.action
    
    if action== "start":
        response=active_model(model_id)
    if action== "status":
        response=get_docer_status(model_id)
    if action== "stop":
        response=stop_container(model_id)

    print("=====Response=====",response)


    return response    
    



