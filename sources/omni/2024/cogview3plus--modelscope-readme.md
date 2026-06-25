---
license: apache-2.0
license_link: LICENSE.md

language:
  - en
  
tags:
- text-to-image
- image-generation
- cogview
  
inference: false
---

# CogView3-Plus-3B

<p style="text-align: center;">
  <div align="center">
  <img src=https://github.com/THUDM/CogView3/raw/main/resources/logo.svg width="50%"/>
  </div>
  <p align="center">
  <a href="README_zh.md">📄 中文阅读 </a> | 
  <a href="https://huggingface.co/spaces/THUDM-HF-SPACE/CogView-3-Plus">🤗 Hugging Face Space | </a> 
  <a href="https://github.com/THUDM/CogView3">🌐 Github </a> | 
  <a href="https://arxiv.org/pdf/2403.05121">📜 arxiv </a>
</p>
<p align="center">
📍 Visit <a href="https://chatglm.cn/main/gdetail/65a232c082ff90a2ad2f15e2?fr=osm_cogvideox&lang=zh"> Qingyan </a> and <a href="https://open.bigmodel.cn/?utm_campaign=open&_channel_track_key=OWTVNma9"> API Platform</a> to experience larger-scale commercial video generation models.
</p>

## Inference Requirements and Model Overview

This model is the DiT version of CogView3, a text-to-image generation model, supporting image generation from 512 to 2048px.

+ Resolution: Width and height must meet the range from 512px to 2048px and must be divisible by 32.
+ Inference Speed: 1s / step (tested on A100)
+ Precision: BF16 / FP32 (FP16 is not supported, as it leads to overflow causing black images)

## Memory Consumption

We tested memory consumption at several common resolutions on A100 devices, `batchsize=1, BF16`, as shown in the table below:

| 分辨率         | enable_model_cpu_offload OFF | enable_model_cpu_offload ON |
|-------------|------------------------------|-----------------------------|
| 512 * 512   | 19GB                         | 11GB                        |
| 720 * 480   | 20GB                         | 11GB                        |
| 1024 * 1024 | 23GB                         | 11GB                        |
| 1280 * 720  | 24GB                         | 11GB                        |
| 2048 * 2048 | 25GB                         | 11GB                        |

## Quick Start

First, ensure the `diffusers` library is installed **from source**. 
```
pip install git+https://github.com/huggingface/diffusers.git
```

Then, run the following code:

```python
from diffusers import CogView3PlusPipeline
import torch

pipe = CogView3PlusPipeline.from_pretrained("THUDM/CogView3-Plus-3B", torch_dtype=torch.float16).to("cuda")

# Enable it to reduce GPU memory usage
pipe.enable_model_cpu_offload()
pipe.vae.enable_slicing()
pipe.vae.enable_tiling()

prompt = "A vibrant cherry red sports car sits proudly under the gleaming sun, its polished exterior smooth and flawless, casting a mirror-like reflection. The car features a low, aerodynamic body, angular headlights that gaze forward like predatory eyes, and a set of black, high-gloss racing rims that contrast starkly with the red. A subtle hint of chrome embellishes the grille and exhaust, while the tinted windows suggest a luxurious and private interior. The scene conveys a sense of speed and elegance, the car appearing as if it's about to burst into a sprint along a coastal road, with the ocean's azure waves crashing in the background."
image = pipe(
    prompt=prompt,
    guidance_scale=7.0,
    num_images_per_prompt=1,
    num_inference_steps=50,
    width=1024,
    height=1024,
).images[0]

image.save("cogview3.png")
```

For more content and to download the original SAT weights, please visit our [GitHub](https://github.com/THUDM/CogView3).

## Citation

🌟 If you find our work helpful, feel free to cite our paper and leave a star:

```
@article{zheng2024cogview3,
  title={Cogview3: Finer and faster text-to-image generation via relay diffusion},
  author={Zheng, Wendi and Teng, Jiayan and Yang, Zhuoyi and Wang, Weihan and Chen, Jidong and Gu, Xiaotao and Dong, Yuxiao and Ding, Ming and Tang, Jie},
  journal={arXiv preprint arXiv:2403.05121},
  year={2024}
}
```

## Model License

This Model is released under the [Apache 2.0 License](LICENSE).
