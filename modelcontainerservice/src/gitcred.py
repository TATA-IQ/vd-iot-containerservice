from git import Repo
import yaml
import os
class GitAuthenticate:
    def __init__(self,repo,branch,localpath,git_ssh_command):
        print("initili")
        self.repo=repo
        self.branch=branch
        self.path=localpath
        self.git_ssh_command=git_ssh_command
        #self.url=
    def gitClone(self,foldername):
        print("===Start Clonning====",self.path)
        print(foldername)
        folderlist=os.listdir(self.path)
        print(foldername,folderlist)
        if len(folderlist)>0 and foldername in folderlist:
            print(foldername)
            gitfolder=os.listdir(self.path+"/"+foldername)
            print("git folder===>",gitfolder)
            if len(gitfolder)>0:
                
                print("===Folder Exist===")
                return False
            else:
                print("===clonng====")
                repo_folder=self.path+"/"+foldername
                print("===clonng====",repo_folder)
                repo = Repo.clone_from(self.repo, repo_folder, env={"GIT_SSH_COMMAND": self.git_ssh_command},branch=self.branch)
                return True
        else:
            print("====inside else==",self.path,foldername)
            os.mkdir(self.path+"/"+foldername)
            repo_folder=self.path+"/"+foldername
            print("===clonng====",repo_folder)
            repo = Repo.clone_from(self.repo,repo_folder, env={"GIT_SSH_COMMAND": self.git_ssh_command},branch=self.branch)
            return True
    # def getgitFolder(self,foldername,path="/data"):
    #     filelist=os.listdir(path+"/"+foldername)
    #     return path+"/"+foldername+"/"+filelist[0]
    def writeConfig(self,foldername,confidata,path="/data/models/"):
        #filelist=os.listdir(path+"/"+foldername)
        # configdata={"model_id":datainsert["model_id"],"model_container":container_name}
        path=self.path+"/"+foldername+"/"+confidata["framework"]
        file=open(path+"/app/"+"config/model.yaml","w")
        yaml.dump(confidata,file)
        file.close()



    
# ga=GitAuthenticate()
# ga.gitClone("https://github.com/adityatataiq/vd-iot-yolov5detectionservice.git","t1")
# #print(ga.getgitFolder("t1"))
# ga.writeConfig("t1",{"model_id":4})