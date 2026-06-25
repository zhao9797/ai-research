---
license: mit
license_name: deepseek
license_link: LICENSE
pipeline_tag: any-to-any
library_name: transformers
tags:
- muiltimodal
- text-to-image
- unified-model
---


## 1. Introduction

We present JanusFlow, a powerful framework that unifies image understanding and generation in a single model. 
JanusFlow introduces a minimalist architecture that integrates autoregressive
language models with rectified flow, a state-of-the-art method in generative modeling. Our
key finding demonstrates that rectified flow can be straightforwardly trained within the large
language model framework, eliminating the need for complex architectural modifications.

[JanusFlow: Harmonizing Autoregression and Rectified Flow for Unified Multimodal Understanding and Generation](https://arxiv.org/abs/2411.07975)

[**Github Repository**](https://github.com/deepseek-ai/Janus)

<div align="center">
<img alt="image" src="teaser.png" style="width:90%;">
</div>


### 2. Model Summary

JanusFlow is a unified understanding and generation MLLM, which decouples visual encoding for multimodal understanding and generation, which is constructed based on DeepSeek-LLM-1.3b-base.
For multimodal understanding, it uses the [SigLIP-L](https://huggingface.co/timm/ViT-L-16-SigLIP-384) as the vision encoder, which supports 384 x 384 image input. 
For image generation, JanusFlow uses rectified flow and [SDXL-VAE](https://huggingface.co/stabilityai/sdxl-vae) to generate 384 x 384 images.
The provided checkpoint is the EMA checkpoint after pre-training and supervised fine-tuning.

<div align="center">
<img alt="image" src="arch.png" style="width:90%;">
</div>


## 3. Quick Start

Please refer to [**Github Repository**](https://github.com/deepseek-ai/Janus)


## 4. License

This code repository is licensed under [the MIT License](https://github.com/deepseek-ai/DeepSeek-LLM/blob/HEAD/LICENSE-CODE). The use of JanusFlow models is subject to [DeepSeek Model License](https://github.com/deepseek-ai/DeepSeek-LLM/blob/HEAD/LICENSE-MODEL).


## 5. Citation

```
@misc{ma2024janusflow,
      title={JanusFlow: Harmonizing Autoregression and Rectified Flow for Unified Multimodal Understanding and Generation}, 
      author={Yiyang Ma and Xingchao Liu and Xiaokang Chen and Wen Liu and Chengyue Wu and Zhiyu Wu and Zizheng Pan and Zhenda Xie and Haowei Zhang and Xingkai yu and Liang Zhao and Yisong Wang and Jiaying Liu and Chong Ruan},
      journal={arXiv preprint arXiv:2411.07975},
      year={2024}
}
```


## 6. Contact

If you have any questions, please raise an issue or contact us at [service@deepseek.com](mailto:service@deepseek.com).