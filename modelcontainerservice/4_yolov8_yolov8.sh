#!/bin/sh 
cd /data/models/4_yolov8_yolov8
echo model pulling 
docker build -t 4_yolov8_yolov8 .
docker rm -f 4_yolov8_yolov8
docker run -d --network=host -p6501:6501 --name 4_yolov8_yolov8 4_yolov8_yolov8
