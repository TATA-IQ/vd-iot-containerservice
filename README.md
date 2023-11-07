# Introduction 
This is a repo for Deploying detection services, querying the containers of detection service

# How It Works

1. Copy the query from setup_table.txt and run it in db
2. In modelcontainerservice/config/config.yaml, change the configurations like ssh key path and api of services
3. In config specify the local_repo_path, path where detection services code will reside. 




# Dependency
1. This Module is dependent on the https://tatacommiot@dev.azure.com/tatacommiot/Video%20Based%20IoT/_git/vd-iot-dataapiservice


# Installation
1. Install Python3.9 
2. pip install gitpython
3. pip install "fastapi[all]"
4. pip install docker
5. pip install pyyaml

# Run App
sudo python3 app.py

# Docker 
Not Required