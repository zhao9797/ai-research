---
license: mit
tags:
- image-generation
- HiDream.ai
language:
- en
pipeline_tag: text-to-image
library_name: diffusers
---

![HiDream-I1 Demo](demo.jpg)

`HiDream-I1` is a new open-source image generative foundation model with 17B parameters that achieves state-of-the-art image generation quality within seconds.

<span style="color: #FF5733; font-weight: bold">For more features and to experience the full capabilities of our product, please visit [https://vivago.ai/](https://vivago.ai/).</span>

## Project Updates
- 🌟 **July 16, 2025**: We've open-sourced the updated image editing model [**HiDream-E1.1**](https://huggingface.co/HiDream-ai/HiDream-E1-1). 
- 📝 **May 28, 2025**: We've released our technical report [HiDream-I1: A High-Efficient Image Generative Foundation Model with Sparse Diffusion Transformer](https://arxiv.org/abs/2505.22705).
- 🚀 **April 28, 2025**: We've open-sourced the instruction-based-image-editing model [**HiDream-E1-Full**](https://github.com/HiDream-ai/HiDream-E1). Experience at [https://huggingface.co/spaces/HiDream-ai/HiDream-E1-Full](https://huggingface.co/spaces/HiDream-ai/HiDream-E1-Full)!.

## Key Features
- ✨ **Superior Image Quality** - Produces exceptional results across multiple styles including photorealistic, cartoon, artistic, and more. Achieves state-of-the-art HPS v2.1 score, which aligns with human preferences.
- 🎯 **Best-in-Class Prompt Following** - Achieves industry-leading scores on GenEval and DPG benchmarks, outperforming all other open-source models.
- 🔓 **Open Source** - Released under the MIT license to foster scientific advancement and enable creative innovation.
- 💼 **Commercial-Friendly** - Generated images can be freely used for personal projects, scientific research, and commercial applications.

## Quick Start
Please make sure you have installed [Flash Attention](https://github.com/Dao-AILab/flash-attention). We recommend CUDA version 12.4 for the manual installation.
```
pip install -r requirements.txt
```
Clone the GitHub repo:
```
git clone https://github.com/HiDream-ai/HiDream-I1
```

Then you can run the inference scripts to generate images:

```python
# For full model inference
python ./inference.py --model_type full

# For distilled dev model inference
python ./inference.py --model_type dev

# For distilled fast model inference
python ./inference.py --model_type fast
```
> **Note:** The inference script will automatically download `meta-llama/Meta-Llama-3.1-8B-Instruct` model files. If you encounter network issues, you can download these files ahead of time and place them in the appropriate cache directory to avoid download failures during inference.

## Gradio Demo

We also provide a Gradio demo for interactive image generation. You can run the demo with:

```python
python gradio_demo.py 
```

## Evaluation Metrics

### DPG-Bench
| Model           | Overall   | Global    | Entity    | Attribute | Relation  | Other     |
|-----------------|-----------|-----------|-----------|-----------|-----------|-----------|
| PixArt-alpha    |    71.11  | 74.97     | 79.32     | 78.60     | 82.57     | 76.96     |
| SDXL            |    74.65  | 83.27     | 82.43     | 80.91     | 86.76     | 80.41     |
| DALL-E 3        |    83.50  | 90.97     | 89.61     | 88.39     | 90.58     | 89.83     |
| Flux.1-dev      |    83.79  | 85.80     | 86.79     | 89.98     | 90.04     | 89.90     |
| SD3-Medium      |    84.08  | 87.90     | 91.01     | 88.83     | 80.70     | 88.68     |
| Janus-Pro-7B    |    84.19  | 86.90     | 88.90     | 89.40     | 89.32     | 89.48     |
| CogView4-6B     |    85.13  | 83.85     | 90.35     | 91.17     | 91.14     | 87.29     |
| **HiDream-I1**  |  **85.89**| 76.44 	  | 90.22     | 89.48     | 93.74     | 91.83     | 

### GenEval

| Model           | Overall  | Single Obj. | Two Obj. | Counting | Colors   | Position | Color attribution |
|-----------------|----------|-------------|----------|----------|----------|----------|-------------------|
| SDXL            |    0.55  | 0.98        | 0.74     | 0.39     | 0.85     | 0.15     | 0.23              |
| PixArt-alpha    |    0.48  | 0.98        | 0.50     | 0.44     | 0.80     | 0.08     | 0.07              |
| Flux.1-dev      |    0.66  | 0.98        | 0.79     | 0.73     | 0.77     | 0.22     | 0.45              |
| DALL-E 3        |    0.67  | 0.96        | 0.87     | 0.47     | 0.83     | 0.43     | 0.45              |
| CogView4-6B     |    0.73  | 0.99        | 0.86     | 0.66     | 0.79     | 0.48     | 0.58              |
| SD3-Medium      |    0.74  | 0.99        | 0.94     | 0.72     | 0.89     | 0.33     | 0.60              |
| Janus-Pro-7B    |    0.80  | 0.99        | 0.89     | 0.59     | 0.90     | 0.79     | 0.66              |
| **HiDream-I1**  |  **0.83**| 1.00        | 0.98 	  | 0.79 	 | 0.91 	| 0.60 	   | 0.72              |

### HPSv2.1 benchmark

|  Model                  |     Averaged   | Animation  |  Concept-art  |   Painting   |   Photo    |
|-------------------------|----------------|------------|---------------|--------------|------------|
|  Stable Diffusion v2.0  |       26.38    |	27.09   |      26.02    |    25.68     |    26.73   |
|  Midjourney V6          |       30.29    |    32.02   |      30.29    |    29.74     |    29.10   |
|  SDXL	                  |       30.64    |    32.84   |      31.36    |    30.86     |    27.48   |
|  Dall-E3	              |       31.44    |    32.39   |      31.09    |    31.18     |    31.09   |
|  SD3                    |       31.53    |    32.60   |      31.82    |    32.06     |    29.62   |
|  Midjourney V5          |       32.33    |    34.05   |      32.47    |    32.24     |    30.56   |
|  CogView4-6B            |       32.31    |    33.23   |      32.60    |    32.89     |    30.52   |
|  Flux.1-dev             |       32.47    |    33.87   |      32.27    |    32.62     |    31.11   |
|  stable cascade         |       32.95    |    34.58   |      33.13    |    33.29     |    30.78   |
|  **HiDream-I1**         |     **33.82**  |    35.05   |      33.74    |    33.88     |    32.61   |


## License Agreement
The Transformer models in this repository are licensed under the MIT License. The VAE is from `FLUX.1 [schnell]`, and the text encoders from `google/t5-v1_1-xxl` and `meta-llama/Meta-Llama-3.1-8B-Instruct`. Please follow the license terms specified for these components. You own all content you create with this model. You can use your generated content freely, but you must comply with this license agreement. You are responsible for how you use the models. Do not create illegal content, harmful material, personal information that could harm others, false information, or content targeting vulnerable groups.


## Acknowledgements
- The VAE component is from `FLUX.1 [schnell]`, licensed under Apache 2.0. 
- The text encoders are from `google/t5-v1_1-xxl` (licensed under Apache 2.0) and `meta-llama/Meta-Llama-3.1-8B-Instruct` (licensed under the Llama 3.1 Community License Agreement).


## Citation

```bibtex
@article{hidreami1technicalreport,
  title={HiDream-I1: A High-Efficient Image Generative Foundation Model with Sparse Diffusion Transformer},
  author={Cai, Qi and Chen, Jingwen and Chen, Yang and Li, Yehao and Long, Fuchen and Pan, Yingwei and Qiu, Zhaofan and Zhang, Yiheng and Gao, Fengbin and Xu, Peihan and others},
  journal={arXiv preprint arXiv:2505.22705},
  year={2025}
}
```