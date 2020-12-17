# CDeC-Net
[![PWC](https://img.shields.io/endpoint.svg?url=https://paperswithcode.com/badge/cdec-net-composite-deformable-cascade-network/table-detection-on-icdar2013-1)](https://paperswithcode.com/sota/table-detection-on-icdar2013-1?p=cdec-net-composite-deformable-cascade-network)
[![PWC](https://img.shields.io/badge/MMDetection-v2.0.0-royalblue)](https://github.com/open-mmlab/mmdetection)



CDeC-Net: Composite Deformable CascadeNetwork for Table Detection in Document Images

Paper Link:
[arXiv](https://arxiv.org/abs/2008.10831) | [Research Gate](https://www.researchgate.net/publication/343877463_CDeC-Net_Composite_Deformable_Cascade_Network_for_Table_Detection_in_Document_Images) | [CVIT, IIIT-H](http://cvit.iiit.ac.in/usodi/cdec-net.php)


## Introduction
CDeC-Net is an end-to-end network for detecting tables in document images. The network consists of a multistage extension of Mask R-CNN with a dual backbone having deformable convolution for detecting tables varying in scale with high detection accuracy at higher IoU threshold. CDeC-Net achieves state-of-the-art results on various publicly available benchmark datasets.
The code is implemented in PyTorch using <a href="https://github.com/open-mmlab/mmdetection">MMdetection</a> framework (Version 2.0.0). 

## Release Notes:
Oct 10, 2020: Our paper has been accepted to ICPR 2020 as oral paper.

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

## Demo
To run inference on single image, use the image_demo.py file by running the following command
```
python demo/image_demo.py demo_image.jpg configs/dcn/db_cascade_mask_rcnn_x101_fpn_dconv_c3-c5_1x_coco.py dataset/coco/logs/latest.pth \
    --score-thr 0.95 --output-img 'output_demo.jpg'
```

## CDeCNet Results
1. Comparison between CDeC-Net and state-of-the-art techniques on the existing benchmark datasets.

| Dataset    | Method                     | Precision            | Recall               | F1                   | mAP                  | Checkpoint |
|------------|----------------------------|----------------------|----------------------|----------------------|----------------------|------------|
|ICDAR-2013  | DeCNT <br>CDeC-Net         | 0.996 <br> **1.000** | 0.996 <br> **1.000** | 0.996 <br> **1.000** | - <br> **1.000**     | <br> [model](https://drive.google.com/file/d/1bip7l0H3Zd9NNWIRRtM-QdnDborWvftf/view?usp=sharing) |
|ICADR-2017  | Yolov3<br>CDeC-Net         | **0.968** <br> 0.924 | **0.975**<br> 0.970  | **0.971** <br> 0.947 | - <br> **0.912**     | <br> [model](https://drive.google.com/file/d/1bbSSqp4_6YE-QqiOVsGX6_HttL2qGYeB/view?usp=sharing) |
|ICADR -2019 | TableRadar<br>CDeC-Net     | **0.940** <br> 0.934 | 0.950 <br> **0.953** | **0.945** <br> 0.944 | - <br> **0.922**     | <br> [model](https://drive.google.com/file/d/1EgF64VgAztQ_nF9I99IM3Tq8L2BI34Mw/view?usp=sharing) |
|UNLV        | GOD <br> CDeC-Net          | 0.910 <br> **0.925** | 0.946 <br> **0.952** | 0.928 <br> **0.938** | - <br> **0.912**     | <br> [model](https://drive.google.com/file/d/1gh5KWVmmex4raRXu_gYeVuGyo8nbdHy4/view?usp=sharing) |
|Marmot      | DeCNT <br> CDeC-Net        | **0.946** <br> 0.930 | 0.849 <br> **0.975** | 0.895 <br> **0.952** | - <br> **0.911**     | <br> [model](https://drive.google.com/file/d/1UJbuQmIxPc7CzRR9fS4evg-aVN9cxQ3R/view?usp=sharing)|
|TableBank   | Li et al. <br> CDeC-Net    | 0.975 <br> **0.979** | 0.987 <br> **0.995** | 0.981 <br> **0.987** | - <br> **0.976**     | <br> [model](https://drive.google.com/file/d/1CGVE5IBaGL6Ssh7dKMv8csz3omezd_HX/view?usp=sharing)|
|PubLayNet   | M-RCNN <br> CDeC-Net       |-<br> **0.970**       |-<br> **0.988**       |-<br> **0.978**       | 0.960 <br> **0.967** | <br> [model](https://drive.google.com/file/d/1NsqIgDWwWIXIU6intibVXUq0tA5yNGAr/view?usp=sharing) |

2. Comparison between our single model CDeC-Net‡ and state-of-the-art techniques on existing benchmark datasets.

| Dataset    | Method                      | Precision            | Recall               | F1                   | mAP                  |
|------------|-----------------------------|----------------------|----------------------|----------------------|----------------------|
|ICDAR-2013  | DeCNT <br>CDeC-Net‡         | **0.996** <br> 0.942 | **0.996** <br> 0.993 | **0.996** <br> 0.968 | - <br> **0.942**     |
|ICADR-2017  | Yolov3<br>CDeC-Net‡         | **0.968** <br> 0.899 | **0.975**<br> 0.969  | **0.971** <br> 0.934 | - <br> **0.880**     |
|ICADR -2019 | TableRadar<br>CDeC-Net‡     | **0.940** <br> 0.930 | 0.950 <br> **0.971** | 0.945 <br> **0.950** | - <br> **0.913**     |
|UNLV        | GOD <br> CDeC-Net‡          | 0.910 <br> **0.915** | 0.946 <br> **0.970** | 0.928 <br> **0.943** | - <br> **0.912**     |
|Marmot      | DeCNT <br> CDeC-Net‡        | **0.946** <br> 0.779 | 0.849 <br> **0.943** | **0.895** <br> 0.861 | - <br> **0.756**     |
|TableBank   | Li et al. <br> CDeC-Net‡    | **0.975** <br> 0.970 | 0.987 <br> **0.990** | **0.981** <br> 0.980 | - <br> **0.965**     |
|PubLayNet   | M-RCNN <br> CDeC-Net‡       | - <br> **0.975**     | - <br> **0.993**     | - <br> **0.984**     |0.960 <br> **0.978**  |

Note: Our single model CDeC-Net‡ is trained on IIIT-AR-13K dataset and fine-tuned with training set of respective datasets (if available). The base model trained on IIIT-AR-13K dataset can be downloaded from the [google drive](https://drive.google.com/file/d/1jTl-pJYJOWFvcWrPV6hH99Z7x-xO9r2f/view?usp=sharing)
 
## Qualitative Results: Table Detection by CDeC-Net
<img src="imgs/qualitative_13_19.png" height="350"/> <br>
<img src="imgs/qualitative_17_marmot.png" height="350"/> <br>

## Issue
Kindly go through the various tutorails and documentation provided in [docs folder](docs). <br>
Most of the common issues were already solved in MMdetection official repo's [Issue Page](https://github.com/open-mmlab/mmdetection/issues). We strongly suggest to go through it before raising a new issue.

## Citation
If you find this work useful for your research, please cite our paper
```
@misc{agarwal2020cdecnet,
    title={CDeC-Net: Composite Deformable Cascade Network for Table Detection in Document Images},
    author={Madhav Agarwal and Ajoy Mondal and C. V. Jawahar},
    year={2020},
    eprint={2008.10831},
    archivePrefix={arXiv},
    primaryClass={cs.CV}
}
```


## Contact
CDeCNet was developed by [Madhav Agarwal](https://www.github.com/mdv3101), Dr. Ajoy Mondal and [Dr. C.V. Jawahar](https://faculty.iiit.ac.in/~jawahar/). <br>
For any query, feel free to drop a mail to [Madhav Agarwal](mailto:madhav.agarwal@research.iiit.ac.in) by explicitly mentioning 'CDeCNet' in the subject.
