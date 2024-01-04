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
import requests
import consul
import socket
import time
logger = logging.getLogger("Rotating Log")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger.setLevel(logging.ERROR)

handler = TimedRotatingFileHandler("logs/log", "D", 1, 7)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.log(40, msg="Container Service Started")

conf=Config.yamlconfig("config/config.yaml")
consul_conf=conf[0]["consul"]


app=FastAPI()

def get_local_ip():
        '''
        Get the ip of server
        '''
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(("192.255.255.255", 1))
            IP = s.getsockname()[0]
        except:
            IP = "127.0.0.1"
        finally:
            s.close()
        return IP

def register_service(consul_conf,port):
    name=socket.gethostname()
    local_ip=socket.gethostbyname(socket.gethostname())
    local_ip=get_local_ip()
    consul_client = consul.Consul(host=consul_conf["host"],port=consul_conf["port"])
    consul_client.agent.service.register(
    "containerservice",service_id=name+"-containerservice-"+consul_conf["env"],
    port=port,
    address=local_ip,
    tags=["python","container_service",consul_conf["env"]]
)

def get_service_address(consul_client,service_name,env):
    while True:
        
        try:
            services=consul_client.catalog.service(service_name)[1]
            print(services)
            for i in services:
                if env == i["ServiceID"].split("-")[-1]:
                    return i
        except:
            time.sleep(10)
            continue
            
def get_confdata(consul_conf):
    consul_client = consul.Consul(host=consul_conf["host"],port=consul_conf["port"])
    pipelineconf=get_service_address(consul_client,"pipelineconfig",consul_conf["env"])

    
    
    env=consul_conf["env"]
    
    endpoint_addr="http://"+pipelineconf["ServiceAddress"]+":"+str(pipelineconf["ServicePort"])
    print("endpoint addr====",endpoint_addr)
    while True:
        
        try:
            res=requests.get(endpoint_addr+"/")
            endpoints=res.json()
            print("===got endpoints===",endpoints)
            break
        except Exception as ex:
            print("endpoint exception==>",ex)
            time.sleep(10)
            continue
    
    while True:
        try:
            res=requests.get(endpoint_addr+endpoints["endpoint"]["containerservice"])
            containerconf=res.json()
            print("containerconf===>",containerconf)
            break
            

        except Exception as ex:
            print("containerconf exception==>",ex)
            time.sleep(10)
            continue
    print("=======searching for dbapi====")
    while True:
        try:
            print("=====consul search====")
            dbconf=get_service_address(consul_client,"dbapi",consul_conf["env"])
            print("****",dbconf)
            dbhost=dbconf["ServiceAddress"]
            dbport=dbconf["ServicePort"]
            res=requests.get(endpoint_addr+endpoints["endpoint"]["dbapi"])
            dbres=res.json()
            print("===got db conf===")
            print(dbres)
            break
        except Exception as ex:
            print("db discovery exception===",ex)
            time.sleep(10)
            continue
    for i in dbres["apis"]:
        print("====>",i)
        dbres["apis"][i]="http://"+dbhost+":"+str(dbport)+dbres["apis"][i]

    
    print("======dbres======")
    print(dbres)
    print(containerconf)
    return  dbres,containerconf






def check_port(url,model_id=None):
    try:
        if model_id is not None:
            response=requests.get(url,json={"model_id":model_id})
        else:
            response=requests.get(url,json={})

        return response.json()["data"]
    except Exception as exp:
        print(exp)
        return "dbconnectionfailed"

def get_model_config(url,model_id):
    try:
        print(f"url: {url}, modelid:{model_id} ")
        response=requests.get(url,json={"model_id":model_id})
        print("in get model config", response.json())
        return response.json()["data"]
    except Exception as exp:
        print(exp)
        return "dbconnectionfailed"

def update_port(url,model_id,port_number):
    print(f"update for model id port {model_id} {port_number}")
    response=requests.post(url=url,json={"model_id":model_id,"model_port":port_number})
    print("============pdate data=========")
    print(response.text)


    





def active_model(model_id):
    print("======Requestmodel====",containerconf)
    

    giturls=containerconf["giturls"]
    apis=apiconf["apis"]
    git_ssh_comand=containerconf["git_ssh_command"]
    local_repo_path= containerconf["local_repo_path"]
    shell_scripts_path= containerconf["shell_scripts_path"]

    # model_id=data.model_id
    port_data=check_port(apis["port_details"],model_id)
    model_conf=get_model_config(apis["model_config"],model_id)
    print("===port_data====",port_data)
    if port_data != "dbconnectionfailed":
        print("===length of port data====",len(port_data))
        if len(port_data)>0:
            print("===length of port data====",len(port_data))
            print(port_data)
            port_number=port_data[0]["port_number"]
        else:
            port_data=check_port(apis["port_details"])
            print("==port data====")
            print(port_data)
            if len(port_data)==0:
                return {"status":0,"message":"there are no ports available for the model, check in the database"}        
            else:
                port_number=port_data[0]["port_number"]
                update_port(apis["update_port"],model_id,port_number)
    else:
        return {"status":0,"message":"connection with database is failed"} 
    
    if model_conf != "dbconnectionfailed":
        print("model_conf====",model_conf)
        model_conf = model_conf[0]
        if model_conf["model_type"].lower()=="object detection":
            model_data=giturls["detection"][model_conf["model_framework"].lower()]
        if model_conf["model_type"].lower()=="ocr":
            model_data=giturls["detection"][model_conf["model_framework"].lower()]
    else:
        return {"status":0,"message":"connection with database is failed"}  

    
    
    dictdata={
        "git_url":model_data["url"],
        "git_branch": model_data["branch"],
        "local_repo_path":local_repo_path,
        "shell_scripts_path":shell_scripts_path,
        "model_id": str(model_conf["model_id"]),
        "model_framework": model_conf["model_framework"],
        "model_name": model_conf["model_name"],
        "model_port":port_number,
        "model_type":model_conf["model_type"]

    }
    print("====?",dictdata)
    print(f"apis: {apis},git_ssh_comand: {git_ssh_comand}")
    buld=Build(apis, dictdata, git_ssh_comand)
    response=buld.buildModel()
    return response


def get_docer_status(model_id):
    # model_id=data.model_id
    print("====checking status=====",model_id)
    print("=====apiconf====",apiconf)
    apis=apiconf["apis"]
    model_conf=get_model_config(apis["model_config"],model_id)[0]
    container_name=str(model_conf["model_id"])+"_"+str(model_conf["model_framework"])+"_"+str(model_conf["model_name"])
    container_name = "".join(container_name.strip().lower().split())
    client = docker.from_env()
    print("cotainer name:=>",container_name)
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
    
    apis=apiconf["apis"]
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


# register_service(consul_conf)
apiconf, containerconf=get_confdata(consul_conf)
register_service(consul_conf,containerconf["port"])

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
    



