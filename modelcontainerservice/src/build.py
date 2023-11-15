import requests
import subprocess
import os
from src.gitcred import GitAuthenticate
class Build:
    def __init__(self,api, config, git_ssh_command,logger=None):
        self.api=api
        self.config=config
        self.git_ssh_command=git_ssh_command
        self.logger=logger
    def buildModel(self):

        git_url = self.config["git_url"]
        git=GitAuthenticate(git_url,self.config["git_branch"],self.config["local_repo_path"], self.git_ssh_command)
        try:
            
            # resContainerModel = requests.get(
            #     api_list["Exist_ContainerModelName"], json=existself.config
            # )
            # print("==>", resContainerModel.json())
            # isContainerModelexist = resContainerModel.json()["self.config"]
            #resContainer = requests.get(api_list["Exist_ContainerName"], json=existself.config)

            #isContainerexist = resContainer.json()["self.config"]
            print("Check ing com")
            self.configinsert=self.config
            model_directory=self.config["local_repo_path"]+"/"+self.config["model_id"]+"_"+self.config["model_framework"]+"_"+self.config["model_name"]
            foldername=self.config["model_id"]+"_"+self.config["model_framework"]+"_"+self.config["model_name"]
            foldername = "".join(foldername.strip().lower().split())
            container_tag=self.config["model_id"]+"_"+self.config["model_framework"]+"_"+self.config["model_name"]
            container_name=self.config["model_id"]+"_"+self.config["model_framework"]+"_"+self.config["model_name"]
            container_tag = "".join(container_tag.strip().lower().split())
            container_name = "".join(container_name.strip().lower().split())
            print("Writing COntainer ",container_name)
            print("Path==>",self.config["git_url"])
            git.gitClone(foldername)
            #gitfoldername=ga.getgitFolder(foldername)
            print("====Folde Name====",foldername)
            
            model_config={"model_id":self.config["model_id"],"model_container":container_name,"port":self.config["model_port"],"framework":self.config["model_framework"]}
            print(model_config)
            git.writeConfig(foldername,model_config,self.config)
            print("=====config write====")
            with open(container_name + ".sh", "w") as f:
                f.write("#!/bin/sh \n")
                #f.write("mkdir "+model_directory+"\n")
                f.write("cd "+model_directory+"\n")
                f.write("echo model pulling \n")
                #f.write("git pull ""\n")
                # folderlist=os.listdir(model_directory)
                # print("folderlist==>",folderlist)
                # f.write("cd "+folderlist[0]+"/app")
                # configself.config={"model_id":self.configinsert["model_id"],"model_container":container_name}
                # file=open("config/model.yaml","w")
                # yaml.dump(employee_dict,file)
                # file.close()
                print("====docker build====")
                f.write("docker build -t " + container_tag + " .\n")
                f.write("docker rm -f " + container_name + "\n")
                print("=====running docker=====")
                print(container_name)
                f.write(
                    "docker run -d"
                    + " --network=host -p"
                    + str(model_config["port"])
                    + ":"
                    + str(model_config["port"])
                    + " --name "
                    + container_name
                    + " "
                    + container_tag
                    + "\n"
                )
            print("======docker run=====")
            print("Calling SUbprocess==>", container_name)
            subprocess.call(["sh", "./" + container_name + ".sh"])
            #subprocess.call(['sh', './'+"cn1"+'.sh'])

            print("Called")
            # outid="9999"
            outid = subprocess.getoutput(
                "docker ps -aqf name=" + container_name
            )
            return {"data": {"status":1,"message":"model starting"}}
        except Exception as ex:
            print("unsuccessfull gitclone")
            return {"data": {"status":0,"message":"model starting"}}

        # check if container table have model with same container_nm
        # if yes rebuild
        # if no insert into container_model, container, build it, deploy it

    def rebuildContainer():
        pass

    def startContainer():
        pass

    def stopContainer():
        pass
