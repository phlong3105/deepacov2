# DeepACOv2: Improving Deep Learning-based Automatic Checkout System Using Image Enhancement Techniques

This repository contains our team's (SKKU Automation Lab) source code for 
2023 AI City Challenge Track 4 (Multi-Class Product Counting & Recognition for Automated Retail Checkout). 

## Installation
 
The code was implemented and tested on Ubuntu 22.04, Python 3.10 and PyTorch (>=v1.13.0) with `conda` environment.

<details open>
<summary>Installation using Docker (recommended) </summary>

The docker image for inference.

```shell
docker run --name deepacov2 --gpus all -it phlong/deepacov2:infer
```

</details>

## Inference

The directory hierarchy should look like this:
```text
deepacov2
  |__ data 
  |__ bin
  |__ data
  |     |__ aic23-autocheckout
  |           |__ testA
  |           |     |__ testA_1.mp4
  |           |     |__ testA_2.mp4
  |           |     |__ testA_3.mp4
  |           |     |__ testA_4.mp4
  |           |__ testB
  |           |     |__ testB_1.mp4
  |           |     |__ testB_2.mp4
  |           |     |__ testB_3.mp4
  |           |     |__ testB_4.mp4
  |           |     |__ testB_5.mp4
  |           |__ train
  |           |__ val
  |__ run
  |__ src
  |     |__ app
  |     |    |__ supr
  |     |         |__ config
  |     |               |__ aic23_autocheckout
  |     |                    |__ testA_1.py
  |     |                    |__ testA_2.py
  |     |                    |__ testA_3.py
  |     |                    |__ testA_4.py
  |     |                    |__ testB_1.py
  |     |                    |__ testB_2.py
  |     |                    |__ testB_3.py
  |     |                    |__ testB_4.py
  |     |                    |__ testB_5.py
  |     |__ lib
  |     |__ mon
  |__ zoo		
        |__ yolov8
```
  
<details open>
<summary>TestA</summary>

Enter docker container and run the inference script for testA:

```shell
cd /mon
conda activate mon
./bin/run-video.sh "aic23-autocheckout" "testA" "all" "yes"
```
</details>

The results will be located at: `deepacov2/track4.txt`

<details open>
<summary>TestB</summary>

Copy testB videos to `deepacov2/data/aic23-autocheckout/testB/`. Open a new terminal and enter:

```shell
# To obtain the CONTAINER_ID:
docker ps -a

docker cp testB_1.mp4 CONTAINER_ID:/deepacov2/data/aic23-autocheckout/testB/testB_1.mp4
docker cp testB_2.mp4 CONTAINER_ID:/deepacov2/data/aic23-autocheckout/testB/testB_2.mp4
docker cp testB_3.mp4 CONTAINER_ID:/deepacov2/data/aic23-autocheckout/testB/testB_3.mp4
docker cp testB_4.mp4 CONTAINER_ID:/deepacov2/data/aic23-autocheckout/testB/testB_4.mp4
docker cp testB_5.mp4 CONTAINER_ID:/deepacov2/data/aic23-autocheckout/testB/testB_5.mp4
```

Enter docker container and run the inference script for testB:

```shell
cd /mon
conda activate mon
./bin/run-video.sh "aic23-autocheckout" "testB" "all" "yes"
```

The results will be located at: `deepacov2/track4.txt`

</details>
  
## Training

Enter docker container and run the training script:
```shell
conda activate mon
cd deepacov2

# Run training script
./bin/run-yolov8.sh "train"

# The new trained weights will be located at: 
# deepacov2/run/train/aic23/aic/yolov8x6-aic23-autocheckout-117-1920/weights/best.pt

# Backup existing pretrained weights first
yes | cp \
zoo/yolov8/yolov8x6-aic23-autocheckout-117-1920.pt \
zoo/yolov8/yolov8x6-aic23-autocheckout-117-1920-backup.pt

# After training is done, copy the best weight and rename it to: 
yes | cp \
run/train/aic23/aic/yolov8x6-aic23-autocheckout-117-1920/weights/best.pt \
zoo/yolov8/yolov8x6-aic23-autocheckout-117-1920.pt
```

## Contact

If you have any questions, feel free to contact Long Pham ([longpham3105@gmail.com](longpham3105@gmail.com) or [phlong@skku.edu](phlong@skku.edu))
