# DeepACOv2: Improving Deep Learning-based Automatic Checkout System Using Image Enhancement Techniques

This repository contains our team's (SKKU Automation Lab) source code for 
2023 AI City Challenge Track 4 (Multi-Class Product Counting & Recognition for Automated Retail Checkout). 

## Installation
 
The code was implemented and tested on Ubuntu 22.04, Python 3.10 and PyTorch (>=v1.13.0) with `conda` environment.

<details open>
<summary>Installation using Docker (recommended) </summary>

The docker image contains all models weights and training data.

```shell
docker run --name deepacov2 --gpus all -it deepacov2
```

</details>

<details open>
<summary>Installation using `conda`</summary>

```shell
mkdir -p deepacov2
mkdir -p deepacov2/data
cd one

# Install `deepacov2` package
git clone https://github.com/phlong3105/deepacov2

conda create --name mon python=3.10
conda activate mon
conda config --add channels conda-forge
conda install cudatoolkit=11.8 cudnn git git-lfs openblas
pip install --root-user-action=ignore poetry setuptools pynvml markdown mkdocs mkdocs-material mkdocstrings sphinx sphinx-paramlinks albumentations ffmpeg-python opencv-python opencv-contrib-python requests matplotlib tensorboard einops flopco-pytorch lightning>=2.0.0 pytorch-lightning==1.9.2 piqa pyiqa thop torch>=2.0.0 torchaudio torchmetrics torchvision ray[tune] filterpy numpy scikit-image scikit-learn scipy click multipledispatch protobuf pyhumps PyYAML typing-extensions validators xmltodict rich tabulate tqdm

poetry config virtualenvs.create false
poetry install --with dev
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
  |			  |__ train
  |			  |__ val
  |__ run
  |__ src
  |		|__ app
  |		|	  |__ supr
  |		|			|__ config
  |		|				  |__ aic23_autocheckout
  |		|						|__ testA_1.py
  |		|						|__ testA_2.py
  |		|						|__ testA_3.py
  |		|						|__ testA_4.py
  |		|						|__ testB_1.py
  |		|						|__ testB_2.py
  |		|						|__ testB_3.py
  |		|						|__ testB_4.py
  |		|__ lib
  |		|__ mon
  |__ zoo		
  	    |__ yolov8
```
  
<details open>
<summary>Docker</summary>

Copy testB videos to `deepacov2/data/aic23-autocheckout/testB/`. Open a new terminal and enter:

```shell
# To obtain the CONTAINER_ID:
docker ps -a

docker cp testB_1.mp4 CONTAINER_ID:/deepacov2/data/aic23-autocheckout/testB/testB_1.mp4
docker cp testB_2.mp4 CONTAINER_ID:/deepacov2/data/aic23-autocheckout/testB/testB_2.mp4
docker cp testB_3.mp4 CONTAINER_ID:/deepacov2/data/aic23-autocheckout/testB/testB_3.mp4
docker cp testB_4.mp4 CONTAINER_ID:/deepacov2/data/aic23-autocheckout/testB/testB_4.mp4
```

Enter docker container and run the inference script for testA:
```shell
cd deepacov2
conda activate mon
./bin/run-video.sh "aic23-autocheckout" "testA" "all" "yes"
```

Enter docker container and run the inference script for testB:
```shell
cd deepacov2
conda activate mon
./bin/run-video.sh "aic23-autocheckout" "testB" "all" "yes"
```

</details>


<details open>
<summary>Conda</summary>

Run the inference code:
```shell
cd aic22_track4/scripts

# Run synchronous processing pipeline
python aic22_retail_checkout_all.py --subset "test_a" --configs "configs_yolov4p5_448" --save_results True

# Run asynchronous processing pipeline
python aic22_retail_checkout_all_async.py --subset "test_a" --configs "configs_yolov4p5_448" --save_results True
```

</details>
  
  
## Training
  
The directory hierarchy should look like this:
```text
one
  |__ datasets (this folder contains the actual raw data)
  |     |__ aicity
  |           |__ aic22retail
  |__ aic22_track4
```

<details open>
<summary>Docker</summary>

Enter docker container and run the training script:
```shell
conda activate one
cd aic22_track4/scripts

# Run training script
python aic22_train_scaled_yolov4.py --run "train" --cfg "yolov4-p5_aic22retail117_448"

# The new trained weights will be located at: 
# aic22_track4/src/aic/pretrained/scaled_yolov4/exp0_yolov4-p5_aic22retail117_448/weights/best.pt

# After training is done, copy the best weight and rename it to: 
yes | cp \
../src/aic/pretrained/scaled_yolov4/exp0_yolov4-p5_aic22retail117_448/weights/best.pt \
../src/aic/pretrained/scaled_yolov4/yolov4-p5_aic22retail117_448_2.pt

# Run inference using the newly trained weights
python aic22_retail_checkout_all.py --subset "test_a" --configs "configs_yolov4p5_448_2" --save_results True
```

</details>

  
<details open>
<summary>Conda</summary>

Download the training data [zip file](https://o365skku-my.sharepoint.com/:u:/g/personal/phlong_o365_skku_edu/EXmFKp_8KKNFv9VC1POLr5cBE6RXIw39HqvIg5ajBXsq7g?e=M0BSLo) and extract it inside `one/datasets/aicity`
  
```shell
conda activate one
cd aic22_track4/scripts

# Run training script
python aic22_train_scaled_yolov4.py --run "train" --cfg "yolov4-p5_aic22retail117_448"

# The new trained weights will be located at: 
# aic22_track4/src/aic/pretrained/scaled_yolov4/exp0_yolov4-p5_aic22retail117_448/weights/best.pt

# After training is done, copy the best weight and rename it to: 
yes | cp \
../src/aic/pretrained/scaled_yolov4/exp0_yolov4-p5_aic22retail117_448/weights/best.pt \
../src/aic/pretrained/scaled_yolov4/yolov4-p5_aic22retail117_448_2.pt

# Run inference using the newly trained weights
python aic22_retail_checkout_all.py --subset "test_a" --configs "configs_yolov4p5_448_2" --save_results True
```

</details>


## Citation

If you find our work useful, please cite the following:

```text
@inreview{Pham2023,  
    author={Long Hoang Pham and Duong Nguyen-Ngoc Tran and Huy-Hung Nguyen and 
            Tai Huu-Phuong Tran and Hyung-Joon Jeon and Hyung-Min Jeon and Jae Wook Jeon},  
    title={Improving Deep Learning-based Automatic Checkout System Using Image Enhancement Techniques},  
    booktitle={CVPR Workshop},
    year={2023}  
}
```

## Contact

If you have any questions, feel free to contact Long Pham ([longpham3105@gmail.com](longpham3105@gmail.com) or [phlong@skku.edu](phlong@skku.edu))
