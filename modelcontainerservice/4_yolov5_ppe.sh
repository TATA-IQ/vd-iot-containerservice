#!/bin/sh 
cd /data/models/4_yolov5_ppe
echo model pulling 
docker build -t 4_yolov5_ppe .
docker rm -f 4_yolov5_ppe
docker run  --network=host -p7000:7000 --name 4_yolov5_ppe 4_yolov5_ppe
