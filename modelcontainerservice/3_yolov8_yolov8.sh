#!/bin/sh 
cd /data/models/3_yolov8_yolov8
echo model pulling 
docker build -t 3_yolov8_yolov8 .
docker rm -f 3_yolov8_yolov8
docker run -d --network=host -p6501:6501 --name 3_yolov8_yolov8 3_yolov8_yolov8
