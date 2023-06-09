import requests
import subprocess
class Build():
    def buildModel(api_list,data):
        path=data["path"]
        try:
            print("----")
            existdata={"container_name":data["container_name"]}
            resContainerModel=requests.get(api_list["Exist_ContainerModelName"],json=existdata)
            print("==>",resContainerModel.json())
            isContainerModelexist=resContainerModel.json()["data"]
            resContainer=requests.get(api_list["Exist_ContainerName"],json=existdata)

            isContainerexist=resContainer.json()["data"]

            if isContainerModelexist==False:
                datainsert={"container_name":data["container_name"],"container_tag":data["container_tag"],"model_id":data["model_id"],"model_path":data["model_path"],"model_port":data["model_port"],"file_name":data["file_name"]}
                response=requests.post(api_list["containermodel_insert"],json=datainsert)
                print("container not exist==>",response.json())


            
            with open(data["container_name"]+".sh","w") as f:
                f.write("#!/bin/sh \n")
                f.write("cd "+path+"\n")
                f.write("docker build -t "+data["container_tag"]+" .\n")
                f.write("docker rm -f "+data["container_name"]+"\n")
                f.write("docker run -d "+" --network=host -p"+data["model_port"]+":"+data["model_port"]+" --name "+data["container_name"]+" "+data["container_tag"]+"\n")
            print("Calling SUbprocess==>",data["container_name"])
            subprocess.call(['sh', './'+data["container_name"]+'.sh'])
            #subprocess.call(['sh', './'+"cn1"+'.sh'])
            
            print("Called")
            #outid="9999"
            outid=subprocess.getoutput("docker ps -aqf name="+data["container_name"])
            print("hostid==?",outid)
            if isContainerexist:
                dataupdate={"container_id":outid,"container_name":data["container_name"]}
                response=requests.post(api_list["update_container"],json=dataupdate)
                print("comtainer_exist==>",response.json())
            else:
                datainsert={"container_id":outid,"container_name":data["container_name"],"container_tag":data["container_tag"],"model_id":data["model_id"]}
                response=requests.post(api_list["container_insert"],json=datainsert)
                print("container not exist==>",response.json())
            return {"data":"success"}
        except Exception as ex:
            return {"data":ex}



       
        #check if container table have model with same container_nm
        # if yes rebuild
        # if no insert into container_model, container, build it, deploy it 


    def rebuildContainer():
        pass
    def startContainer():
        pass
    def stopContainer():
        pass

