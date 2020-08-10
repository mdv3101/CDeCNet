# CDeC-Net
[![PWC](https://img.shields.io/badge/MMDetection-v2.0.0-royalblue)](https://github.com/open-mmlab/mmdetection)


CDeC-Net: Composite Deformable CascadeNetwork for Table Detection in Document Images

## Introduction
CDeC-Net is an end-to-end network for detecting tables in document images. The network consists of a multistage extension of Mask R-CNN with a dual backbone having deformable convolution for detecting tables varying in scale with high detection accuracy at higher IoU threshold. CDeC-Net achieves state-of-the-art results on various publicly available benchmark datasets.
The code is implemented in PyTorch using <a href="https://github.com/open-mmlab/mmdetection">MMdetection</a> framework (Version 2.0.0). 


## Setup
<b>Dependencies</b><br>
Python = 3.6+ <br>
PyTorch = 1.4.0<br>
Torchvision =  0.5.0<br>
Cuda = 10.0<br>
MMdetection = 2.0.0<br>
mmcv = 0.5.4<br>

1. Clone this repository
```
git clone https://github.com/mdv3101/CDeCNet
```
2. Install the require dependencies
```
pip install torch==1.4.0 torchvision==0.5.0
```
```
cd CDecNet/
pip install -r requirements/build.txt
pip install "git+https://github.com/open-mmlab/cocoapi.git#subdirectory=pycocotools"
pip install -v -e .
```

Please follow [install.md](docs/install.md) for detailed installation steps.

## Training
1. Create a folder 'dataset' in the CDeCNet and put your data into this folder. Your dataset must be in MS-Coco format. The directory structure should be:
```
dataset
  ├── coco
  | ├── annotations
  | ├── train2014
  | ├── val2014
  | ├── logs
```
2. Create a folder 'model' in the CDeCNet and put the pre-trained model on MS-Coco into this directory. The model file can be downloaded from the [google drive](https://drive.google.com/file/d/1JXt2F5pDJmSN5C7DXVKff93ksmMMqdcB/view?usp=sharing)

3. Set ```load_from= /path/of/pre-trained/model``` in [default_runtime.py](configs/_base_/default_runtime.py)
4. To train a model on CDeC-Net, use the following commnand
```
python -u tools/train.py configs/dcn/db_cascade_mask_rcnn_x101_fpn_dconv_c3-c5_1x_coco.py --work-dir dataset/coco/logs/
```
<br>
Note that step 2 and 3 are optional. If you want to train a model from scratch, then you can skip these two steps. (Training a model from scratch will take larger time to converge)

## Evaluation
To evaluate the trained model, run the following command
```
python tools/test.py configs/dcn/db_cascade_mask_rcnn_x101_fpn_dconv_c3-c5_1x_coco.py dataset/coco/logs/latest.pth \
    --format-only --options "jsonfile_prefix=evaluation_result"
```
Details about various training and evaluation methods can be found in [getting_started.md](docs/getting_started.md)


## CDeCNet Results
1. Comparison between CDeC-Net and state-of-the-art techniques on the existing benchmark datasets.

| Dataset    | Method                     | Precision            | Recall               | F1                   | mAP                |
|------------|----------------------------|----------------------|----------------------|----------------------|--------------------|
|ICDAR-2013  | DeCNT <br>CDeC-Net         | 0.996 <br> **1.000** | 0.996 <br> **1.000** | 0.996 <br> **1.000** | <br> **1.000**     |
|ICADR-2017  | Yolov3<br>CDeC-Net         | **0.968** <br> 0.924 | **0.975**<br> 0.970  | **0.971** <br> 0.947 | <br> **0.912**     |
|ICADR -2019 | TableRadar<br>CDeC-Net     | **0.940** <br> 0.934 | 0.950 <br> **0.953** | **0.945** <br> 0.944 | <br> **0.922**     |
|UNLV        | GOD <br> CDeC-Net          | 0.910 <br> **0.925** | 0.946 <br> **0.952** | 0.928 <br> **0.938** | <br> **0.912**     |
|Marmot      | DeCNT <br> CDeC-Net        | **0.946** <br> 0.930 | 0.849 <br> **0.975** | 0.895 <br> **0.952** | <br> **0.911**     |
|TableBank   | Li et al. <br> CDeC-Net    | 0.975 <br> **0.979** | 0.987 <br> **0.995** | 0.981 <br> **0.987** | <br> **0.976**     |
|PubLayNet   | M-RCNN <br> CDeC-Net       | <br> **0.970**       | <br> **0.988**       | <br> **0.978**       |0.960 <br> **0.967**|

2. Comparison between our single model CDeC-Net‡ and state-of-the-art techniques on existing benchmark datasets.

| Dataset    | Method                      | Precision            | Recall               | F1                   | mAP                |
|------------|-----------------------------|----------------------|----------------------|----------------------|--------------------|
|ICDAR-2013  | DeCNT <br>CDeC-Net‡         | **0.996** <br> 0.942 | **0.996** <br> 0.993 | **0.996** <br> 0.968 | <br> **0.942**     |
|ICADR-2017  | Yolov3<br>CDeC-Net‡         | **0.968** <br> 0.899 | **0.975**<br> 0.969  | **0.971** <br> 0.934 | <br> **0.880**     |
|ICADR -2019 | TableRadar<br>CDeC-Net‡     | **0.940** <br> 0.930 | 0.950 <br> **0.971** | 0.945 <br> **0.950** | <br> **0.913**     |
|UNLV        | GOD <br> CDeC-Net‡          | 0.910 <br> **0.915** | 0.946 <br> **0.970** | 0.928 <br> **0.943** | <br> **0.912**     |
|Marmot      | DeCNT <br> CDeC-Net‡        | **0.946** <br> 0.779 | 0.849 <br> **0.943** | **0.895** <br> 0.861 | <br> **0.756**     |
|TableBank   | Li et al. <br> CDeC-Net‡    | **0.975** <br> 0.970 | 0.987 <br> **0.990** | **0.981** <br> 0.980 | <br> **0.965**     |
|PubLayNet   | M-RCNN <br> CDeC-Net‡       | <br> **0.975**       | <br> **0.993**       | <br> **0.984**       |0.960 <br> **0.978**|


## Issue
Kindly go through the various tutorails and documentation provided in [docs folder](docs). <br>
Most of the common issues were already solved in MMdetection official repo's [Issue Page](https://github.com/open-mmlab/mmdetection/issues). We strongly suggest to go through it before raising a new issue.

