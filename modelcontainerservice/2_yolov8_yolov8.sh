#!/bin/sh 
cd /data/models/2_yolov8_yolov8
echo model pulling 
docker build -t 2_yolov8_yolov8 .
docker rm -f 2_yolov8_yolov8
docker run -d --network=host -p6501:6501 --name 2_yolov8_yolov8 2_yolov8_yolov8
