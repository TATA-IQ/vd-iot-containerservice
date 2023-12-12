import docker

class docker_check:
    def running_status(container_name):
        client = docker.from_env()
        try:
            container = client.containers.get(container_name)
            print("container status=====>", container.status)
            if container.status == 'running':
                return True
            else:
                return False
        except Exception as exp:
            print(f"found exception {exp}")
            return False
        
class docker_class:
    def image_build(image_path):
        client = docker.from_env()
        image_name = image_path.split("/")[-1]
        
        print("docker build started")
            # imagename, stream = client.images.build(path=image_path, tag=image_name,dockerfile="Dockerfile",decode=True)
        _,streamer = client.images.build(path=image_path,tag=f"{image_name}:{image_name}",rm=True,quiet=True,timeout=60)
        print("docker build successful")  
        for i in streamer:
            print(i)
        client.close()
        # try:            
        #     print("docker build started")
        #     # imagename, stream = client.images.build(path=image_path, tag=image_name,dockerfile="Dockerfile",decode=True)
        #     _,streamer = client.images.build(path=image_path,dockerfile="Dockerfile",tag=f"{image_name}:{image_name}",rm=True)
        #     print("docker build successful")  
        #     for i in streamer:
        #         print(i)
        #     # for chunk in streamer:
        #     #     if 'stream' in chunk:
        #     #         for line in chunk['stream'].splitlines():
        #     #             print(line)        
        # except Exception as exp:
        #     print(f"exception raised as {exp}")
        # finally:
        #     client.close()
            
        
    def run(image_name, container_name, port1, port2):
        try:
            client = docker.from_env()
            existing_container = client.containers.get(container_name)            
            existing_container.stop()
            existing_container.remove()

            print(f"Container {container_name} is stopped and removed.")
        except Exception as exp:
            print(f"Exception raised: {exp}")
        finally:
            client.close()
            
        try:
            client = docker.from_env()
            container = client.containers.run({image_name}, name={container_name},network="host",ports={port1: port2}, detach=True)
            # print(["echo","hello", "world"])
        except Exception as exp:
            print(f"exception raised as {exp}")
        finally:
            client.close()
            
# dockerobj = docker_class()   
# image_path = "/data/models/55_yolov8_consumermodel001/" 
# docker_class.image_build(image_path)
