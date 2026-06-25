---
license: apache-2.0
pipeline_tag: any-to-any
library_name: diffusers
---

<div align="center">
<br>

[//]: # (<h3>Show-o2: Improved Unified Multimodal Models</h3>)

[Jinheng Xie](https://sierkinhane.github.io/)<sup>1</sup>&nbsp;
[Zhenheng Yang](https://scholar.google.com/citations?user=Ds5wwRoAAAAJ&hl=en)<sup>2</sup>&nbsp;
[Mike Zheng Shou](https://sites.google.com/view/showlab)<sup>1</sup> 

<sup>1</sup> [Show Lab](https://sites.google.com/view/showlab/home?authuser=0), National University of Singapore&nbsp; <sup>2</sup> Bytedance&nbsp;
 
[![ArXiv](https://img.shields.io/badge/Arxiv-<2506.15564>-<COLOR>.svg)](https://arxiv.org/abs/2506.15564) [![Code](https://img.shields.io/badge/Code-<GitHub_Repository>-<COLOR>.svg)](https://github.com/showlab/Show-o/tree/main/show-o2) [![WeChat badge](https://img.shields.io/badge/微信-加入-green?logo=wechat&amp)](https://github.com/showlab/Show-o/blob/main/docs/wechat_qa_3.jpg)
</div>

## Abstract

This paper presents improved native unified multimodal models, \emph{i.e.,} Show-o2, that leverage autoregressive modeling and flow matching. Built upon a 3D causal variational autoencoder space, unified visual representations are constructed through a dual-path of spatial (-temporal) fusion, enabling scalability across image and video modalities while ensuring effective multimodal understanding and generation. Based on a language model, autoregressive modeling and flow matching are natively applied to the language head and flow head, respectively, to facilitate text token prediction and image/video generation. A two-stage training recipe is designed to effectively learn and scale to larger models. The resulting Show-o2 models demonstrate versatility in handling a wide range of multimodal understanding and generation tasks across diverse modalities, including text, images, and videos. Code and models are released at this https URL .

## What is the new about Show-o2?
We perform the unified learning of multimodal understanding and generation on the text token and **3D Causal VAE space**, which is scalable for **text, image, and video modalities**. A dual-path of spatial (-temporal) fusion is proposed to accommodate the distinct feature dependency  of multimodal understanding and generation. We employ specific heads with **autoregressive modeling and flow matching** for the overall unified learning of **multimodal understanding, image/video and mixed-modality generation.**
<img src="overview.png" width="1000">

## Pre-trained Model Weigths
The Show-o2 checkpoints can be found on Hugging Face:
* [showlab/show-o2-1.5B](https://huggingface.co/showlab/show-o2-1.5B)
* [showlab/show-o2-1.5B-HQ](https://huggingface.co/showlab/show-o2-1.5B-HQ)
* [showlab/show-o2-7B](https://huggingface.co/showlab/show-o2-7B)
* [showlab/show-o2-1.5B](https://huggingface.co/showlab/show-o2-1.5B-w-video-und) (further unified fine-tuning on video understanding data)
* [showlab/show-o2-7B](https://huggingface.co/showlab/show-o2-7B-w-video-und) (further unified fine-tuning on video understanding data)


## Getting Started
First, set up the environment:
```
bash build_env.sh
```
Login your wandb account on your machine or server.
```
wandb login <your wandb keys>
```
Download Wan2.1 3D causal VAE model weight [here](https://huggingface.co/Wan-AI/Wan2.1-T2V-14B/blob/main/Wan2.1_VAE.pth) and put it on the current directory.

Demo for **Multimodal Understanding** and you can find the results on wandb.

```
# image-level
python3 inference_mmu.py config=configs/showo2_7b_demo_432x432.yaml \
                         mmu_image_path=./docs/mmu/pexels-jane-pham-727419-1571673.jpg question='Describe the image in detail.'

python3 inference_mmu.py config=configs/showo2_7b_demo_432x432.yaml \
                         mmu_image_path=./docs/mmu/pexels-fotios-photos-2923436.jpg question='请告诉我图片中写着什么？'

python3 inference_mmu.py config=configs/showo2_7b_demo_432x432.yaml \
                         mmu_image_path=./docs/mmu/pexels-taryn-elliott-4144459.jpg question='How many avocados (including the halved) are in this image? Tell me how to make an avocado milkshake in detail.'

# video
python3 inference_mmu_vid.py config=configs/showo2_7b_demo_video_understanding.yaml \
                             mmu_video_path='./docs/videos/' question="Describe the video."  \
                             num_video_frames_mmu=32

python3 inference_mmu_vid.py config=configs/showo2_1.5b_demo_video_understanding.yaml \
                             mmu_video_path='./docs/videos/' question="Describe the video."  \
                             num_video_frames_mmu=32

```
Demo for **Text-to-Image Generation** and you can find the results on wandb.
```
python3 inference_t2i.py config=configs/showo2_1.5b_demo_1024x1024.yaml \
                         batch_size=4 guidance_scale=7.5 num_inference_steps=50;
         
python3 inference_t2i.py config=configs/showo2_1.5b_demo_512x512.yaml \
                         batch_size=4 guidance_scale=7.5 num_inference_steps=50;
                                      
python3 inference_t2i.py config=configs/showo2_1.5b_demo_432x432.yaml \
                         batch_size=4 guidance_scale=7.5 num_inference_steps=50;

python3 inference_t2i.py config=configs/showo2_7b_demo_432x432.yaml \
                         batch_size=4 guidance_scale=7.5 num_inference_steps=50;
```

### Citation
To cite the paper and model, please use the below:
```
@article{xie2025showo2,
  title={Show-o2: Improved Native Unified Multimodal Models},
  author={Xie, Jinheng and Yang, Zhenheng and Shou, Mike Zheng},
  journal={arXiv preprint},
  year={2025}
}
```
### Acknowledgments
This work is heavily based on [Show-o](https://github.com/showlab/Show-o).