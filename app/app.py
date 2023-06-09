from src.build import Build
from config_parser.parser import ParseConfig
import logging
from logging.handlers import TimedRotatingFileHandler
from fastapi import FastAPI
config=ParseConfig()

logger = logging.getLogger("Rotating Log")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger.setLevel(logging.ERROR)

handler = TimedRotatingFileHandler("logs/log", 'D', 1, 7)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.log(40,msg="Database Started")


test_data={"path":"/home/aditya.singh/Pocs/vision/AIInference/yolov5","container_name":"yolov5cn3","container_tag":"yolo","model_id":"4","model_usecase":"ppe","model_path":"yolov5/ppe.zip","model_port":"7000","model_framework":"yolov5","file_name":"ppe.zip"}
apilist=ParseConfig.getapi()
print("=======")
Build.buildModel(apilist,test_data)
# @app.post("/insertContainer")
# async def Container_Insert(data:ContainerModel):
#         test_data={"path":data.path,"container_name":data.container_name,"container_tag":data.container_tag,"model_id":data.model_tag}

        
#         return Build.buildModel(apilist,test_data)