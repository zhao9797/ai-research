---
pipeline_tag: any-to-any
---

<p align="center">
  <img src="https://huggingface.co/InternVL-U/InternVL-U/resolve/main/assets/logo.jpg" width="80" />
</p>

<h1 align="center">InternVL-U: Democratizing Unified Multimodal Models for Understanding, Reasoning, Generation and Editing</h1>


<div align="center">

[![arXiv](https://img.shields.io/badge/ArXiv-2603.09877-b31b1b?logo=arxiv)](https://arxiv.org/abs/2603.09877)&nbsp;
[![GitHub](https://img.shields.io/badge/GitHub-InternVL--U-181717?logo=github)](https://github.com/OpenGVLab/InternVL-U)&nbsp;
[![GenEditEvalKit](https://img.shields.io/badge/GitHub-GenEditEvalKit-181717?logo=github)](https://github.com/open-compass/GenEditEvalKit)&nbsp;
[![TextEdit Benchmark](https://img.shields.io/badge/GitHub-TextEdit%20Benchmark-181717?logo=github)](https://github.com/open-compass/TextEdit)

Shanghai AI Laboratory, InternVL-U Team
</div>

**InternVL-U** is a **4B-parameter unified multimodal model (UMM)** that brings **multimodal understanding, reasoning, image generation, and image editing** into a *single* framework, aiming to **democratize omni-capable multimodal intelligence** with an efficient and practical model size.

It is presented in the paper [InternVL-U: Democratizing Unified Multimodal Models for Understanding, Reasoning, Generation and Editing](https://huggingface.co/papers/2603.09877).

<p align="center">
  <img src="https://huggingface.co/InternVL-U/InternVL-U/resolve/main/assets/teaser1.jpg" width="40%" style="display:inline-block; vertical-align:middle;" />
  &nbsp;&nbsp;
  <img src="https://huggingface.co/InternVL-U/InternVL-U/resolve/main/assets/teaser2.jpg" width="40%" style="display:inline-block; vertical-align:middle;" />
</p>

## ⚡ Quick Start

To get started, first install the required dependencies from the [official repository](https://github.com/OpenGVLab/InternVL-U):
```bash
pip install -r requirements.txt
```

### Sample Usage

#### Generate Text (Multimodal Understanding)
```python
import torch
from PIL import Image
from internvlu import InternVLUPipeline

prompt = "What is the amino acid shown in the picture?"
# Replace with your local path to the image
image = Image.open("assets/amino_acid.png").convert("RGB")

pipeline = InternVLUPipeline.from_pretrained(
    "InternVL-U/InternVL-U",
    torch_dtype=torch.bfloat16,
)

pipeline.to("cuda")

tokenizer = pipeline.processor.tokenizer

with torch.no_grad():
    output = pipeline(
        prompt=prompt,
        image=image,
        max_new_tokens=1024,
        generation_mode="text",
    ).generate_output[0]

print(tokenizer.decode(output, skip_special_tokens=True))
```

#### Generate Image (Text-to-Image)
```python
import torch
from internvlu import InternVLUPipeline

prompt = """In the deep indigo night sky, a grand fireworks festival is at its peak, with countless dazzling Mars arranged precisely, condensed into the huge and dazzling "InternVL-U" words. The letters are composed of highly saturated electric blue and dreamy purple fluorescent particles, presenting a futuristic streamlined font surrounded by scattered golden fragments resembling stardust, and the final "U" gives off a fluid metallic texture. Below is a brightly lit modern city, with the shimmering sea perfectly reflecting this stunning scene. Amidst the swirling smoke, it showcases the ultimate visual allure of technology and romance intertwined."""

pipeline = InternVLUPipeline.from_pretrained(
    "InternVL-U/InternVL-U",
    torch_dtype=torch.bfloat16,
)

pipeline.to("cuda")

with torch.no_grad():
    image = pipeline(
        prompt=prompt,
        generation_mode="image",
        height=576,
        width=1024,
        generator=torch.Generator(device="cuda").manual_seed(42)
    ).images[0]

image.save(f"example_t2i.png")
```

## 🤖 Model Checkpoint Download
You can download the model weights from this repository into the InternVLU project using the following command:
```bash
huggingface-cli download --repo-type model --resume-download InternVL-U/InternVL-U --local-dir "your_local_path_to_store_the_model_weights"
```

## ✨ Citation
If you find our InternVL-U useful, please cite our InternVL-U technical report using this BibTeX.

```bibtex
@article{tian2026internvl,
  title={InternVL-U: Democratizing Unified Multimodal Models for Understanding, Reasoning, Generation and Editing},
  author={Tian, Changyao and Yang, Danni and Chen, Guanzhou and Cui, Erfei and Wang, Zhaokai and Duan, Yuchen and Yin, Penghao and Chen, Sitao and Yang, Ganlin and Liu, Mingxin and others},
  journal={arXiv preprint arXiv:2603.09877},
  year={2026}
}
```