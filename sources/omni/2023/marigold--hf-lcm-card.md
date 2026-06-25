---
language:
- en
license: apache-2.0
pipeline_tag: depth-estimation
library_name: diffusers
tags:
- depth estimation
- latent consistency model
- image analysis
- computer vision
- in-the-wild
- zero-shot
new_version: prs-eth/marigold-depth-v1-1
---

<h1 align="center">Marigold Depth LCM v1-0 Model Card</h1>

<p align="center">
<a title="Image Depth" href="https://huggingface.co/spaces/prs-eth/marigold" target="_blank" rel="noopener noreferrer" style="display: inline-block;">
    <img src="https://img.shields.io/badge/%F0%9F%A4%97%20Image%20Depth%20-Demo-yellow" alt="Image Depth">
</a>
<a title="diffusers" href="https://huggingface.co/docs/diffusers/using-diffusers/marigold_usage" target="_blank" rel="noopener noreferrer" style="display: inline-block;">
    <img src="https://img.shields.io/badge/%F0%9F%A4%97%20diffusers%20-Integration%20🧨-yellow" alt="diffusers">
</a>
<a title="Github" href="https://github.com/prs-eth/marigold" target="_blank" rel="noopener noreferrer" style="display: inline-block;">
    <img src="https://img.shields.io/github/stars/prs-eth/marigold?label=GitHub%20%E2%98%85&logo=github&color=C8C" alt="Github">
</a>
<a title="Website" href="https://marigoldcomputervision.github.io/" target="_blank" rel="noopener noreferrer" style="display: inline-block;">
    <img src="https://img.shields.io/badge/%E2%99%A5%20Project%20-Website-blue" alt="Website">
</a>
<a title="arXiv" href="https://arxiv.org/abs/2505.09358" target="_blank" rel="noopener noreferrer" style="display: inline-block;">
    <img src="https://img.shields.io/badge/%F0%9F%93%84%20Read%20-Paper-AF3436" alt="arXiv">
</a>
<a title="Social" href="https://twitter.com/antonobukhov1" target="_blank" rel="noopener noreferrer" style="display: inline-block;">
    <img src="https://img.shields.io/twitter/follow/:?label=Subscribe%20for%20updates!" alt="Social">
</a>
<a title="License" href="https://www.apache.org/licenses/LICENSE-2.0" target="_blank" rel="noopener noreferrer" style="display: inline-block;">
    <img src="https://img.shields.io/badge/License-Apache--2.0-929292" alt="License">
</a>
</p>

<h2 align="center"><span style="color: red;"><b>This model is deprecated. Use the new Marigold Depth v1-1 Model instead.</b></span></h2>
<h2 align="center">
<a href="https://huggingface.co/prs-eth/marigold-depth-v1-1">NEW: Marigold Depth v1-1 Model</a>
</h2>

This is a model card for the `marigold-depth-lcm-v1-0` model for monocular depth estimation from a single image. 
The model is fine-tuned from the `marigold-depth-v1-0` [model](https://huggingface.co/prs-eth/marigold-depth-v1-0) 
using the latent consistency distillation method, as 
described in our papers:
- [CVPR'2024 paper](https://hf.co/papers/2312.02145) titled "Repurposing Diffusion-Based Image Generators for Monocular Depth Estimation"
- [Journal extension](https://hf.co/papers/2505.09358) titled "Marigold: Affordable Adaptation of Diffusion-Based Image Generators for Image Analysis"

### Using the model
- Play with the interactive [Hugging Face Spaces demo](https://huggingface.co/spaces/prs-eth/marigold): check out how the model works with example images or upload your own.
- Use it with [diffusers](https://huggingface.co/docs/diffusers/using-diffusers/marigold_usage) to compute the results with a few lines of code.
- Get to the bottom of things with our [official codebase](https://github.com/prs-eth/marigold).

## Model Details
- **Developed by:** [Bingxin Ke](http://www.kebingxin.com/), [Kevin Qu](https://ch.linkedin.com/in/kevin-qu-b3417621b), [Tianfu Wang](https://tianfwang.github.io/), [Nando Metzger](https://nandometzger.github.io/), [Shengyu Huang](https://shengyuh.github.io/), [Bo Li](https://www.linkedin.com/in/bobboli0202), [Anton Obukhov](https://www.obukhov.ai/), [Konrad Schindler](https://scholar.google.com/citations?user=FZuNgqIAAAAJ).
- **Model type:** Generative latent diffusion-based affine-invariant monocular depth estimation from a single image.
- **Language:** English.
- **License:** [Apache License License Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).
- **Model Description:** This model can be used to generate an estimated depth map of an input image. 
  - **Resolution**: Even though any resolution can be processed, the model inherits the base diffusion model's effective resolution of roughly **768** pixels. 
    This means that for optimal predictions, any larger input image should be resized to make the longer side 768 pixels before feeding it into the model.
  - **Steps and scheduler**: This model was designed for usage with the **LCM** scheduler and between **1 and 4** denoising steps. 
  - **Outputs**:
    - **Affine-invariant depth map**: The predicted values are between 0 and 1, interpolating between the near and far planes of the model's choice.
    - **Uncertainty map**: Produced only when multiple predictions are ensembled with ensemble size larger than 2.
- **Resources for more information:** [Project Website](https://marigoldcomputervision.github.io/), [Paper](https://arxiv.org/abs/2505.09358), [Code](https://github.com/prs-eth/marigold).
- **Cite as:**

```bibtex
@misc{ke2025marigold,
  title={Marigold: Affordable Adaptation of Diffusion-Based Image Generators for Image Analysis},
  author={Bingxin Ke and Kevin Qu and Tianfu Wang and Nando Metzger and Shengyu Huang and Bo Li and Anton Obukhov and Konrad Schindler},
  year={2025},
  eprint={2505.09358},
  archivePrefix={arXiv},
  primaryClass={cs.CV}
}

@InProceedings{ke2023repurposing,
  title={Repurposing Diffusion-Based Image Generators for Monocular Depth Estimation},
  author={Bingxin Ke and Anton Obukhov and Shengyu Huang and Nando Metzger and Rodrigo Caye Daudt and Konrad Schindler},
  booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  year={2024}
}
```