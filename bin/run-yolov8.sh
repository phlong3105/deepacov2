#!/bin/bash

echo "$HOSTNAME"

task=$1
machine=$HOSTNAME
read -e -i "$task" -p "Task [train, test, predict]: " task

# Initialization
script_path=$(readlink -f "$0")
current_dir=$(dirname "$script_path")
root_dir=$(dirname "$current_dir")
yolov8_dir="${root_dir}/src/lib/yolov8"

cd "${yolov8_dir}" || exit

# Train
if [ "$task" == "train" ]; then
  echo -e "\nTraining"
  python train.py \
    --task "detect" \
    --model "${root_dir}/zoo/yolov8/yolov8x6-det-coco.pt" \
    --data "data/aic23-autocheckout-117.yaml" \
    --project "${root_dir}/run/train/aic23" \
    --name "yolov8x6-aic23-autocheckout-117-1920" \
    --epochs 50 \
    --batch 4 \
    --imgsz 1920 \
    --workers 8 \
    --device 0,1 \
    --save \
    --exist-ok \
    --pretrained
fi

cd "${root_dir}" || exit
