#!/bin/sh 
cd /data/models/1_yolov8_yolov8
echo model pulling 
docker build -t 1_yolov8_yolov8 .
docker rm -f 1_yolov8_yolov8
docker run -d --network=host -p6500:6500 --name 1_yolov8_yolov8 1_yolov8_yolov8
