---
language:
- en
license: apache-2.0
size_categories:
- 1M<n<10M
task_categories:
- text-to-image
- image-to-image
tags:
- text-to-image
- image-to-image
configs:
- config_name: train
  data_files: uno_1m_total_labels.json
---

![image](./assets/uno1m.webp)

<h3 align="center">
    Less-to-More Generalization: Unlocking More Controllability by In-Context Generation
</h3>

<p align="center"> 
<a href="https://github.com/bytedance/UNO"><img alt="Build" src="https://img.shields.io/github/stars/bytedance/UNO"></a> 
<a href="https://bytedance.github.io/UNO/"><img alt="Build" src="https://img.shields.io/badge/Project%20Page-UNO-blue"></a> 
<a href="https://arxiv.org/abs/2504.02160"><img alt="Build" src="https://img.shields.io/badge/arXiv%20paper-UNO-b31b1b.svg"></a>
<a href="https://huggingface.co/bytedance-research/UNO"><img src="https://img.shields.io/static/v1?label=%F0%9F%A4%97%20Hugging%20Face&message=Model&color=green"></a>
<a href="https://huggingface.co/datasets/bytedance-research/UNO-1M"><img src="https://img.shields.io/static/v1?label=%F0%9F%A4%97%20Hugging%20Face&message=Dataset&color=yellow"></a>
<a href="https://huggingface.co/spaces/bytedance-research/UNO-FLUX"><img src="https://img.shields.io/static/v1?label=%F0%9F%A4%97%20Hugging%20Face&message=demo&color=orange"></a>
</p>

## Overview

UNO-1M is a large dataset (~1M paired images) constructed by the in-context generation pipeline introduced in the [UNO](https://arxiv.org/abs/2504.02160) paper. Its advantages include highly diverse categories (>365 categories), high-resolution images (around 1024x1024), variable resolutions (different aspect ratios), high quality (produced by state-of-the-art text-to-image models), and high subject consistency (filtered by VLM-filter CoT). You can train on this dataset to reproduce the [UNO model](https://huggingface.co/bytedance-research/UNO) or build your own state-of-the-art subject-driven model. We now open-source the entire dataset to benefit research.

## Label Format

| Key name         | Type   | Description                                    |
| ---------------- | ------ | ---------------------------------------------- |
| `img_path1`      | `str`  | Reference image information (first image).    |
| `img_path2`      | `str`  | Reference image information (second image).   |
| `caption`        | `dict` | Image caption and subject word.               |
| `vlm_filter_cot` | `dict` | The CoT answer of VLM-filter.                |

## Dataset Structure

### Directory Structure
```bash
output_root/
├── images/
│   ├── split1.tar.gz
│   ├── split2.tar.gz
│   └── ...
├── labels/
│   ├── split1.json
│   ├── split2.json
│   └── ...
```

After extraction:
```bash
output_root/
├── images/
│   ├── split1/
│   │   ├── object365_w1024_h1536_split_Bread_0_0_1_725x1024.png
│   │   ├── object365_w1024_h1536_split_Bread_0_0_2_811x1024.png
│   │   └── ...
│   └── ...
├── labels/
│   ├── split1.json
│   ├── split2.json
│   └── ...
...
```
## Usage

UNO-1M contains rich label information, and we preserve the breakdown of the consistency score as well as the final consistency scores. It can be applied to:

- Text-to-image generation
- Subject-driven generation
- Scored-filter training
- Consistency reward model training

**Note:**
For subject-driven generation, we recommend using data with a consistency score greater than or equal to 3.5 (the key in JSON is `score_final`). In the UNO paper, we use perfect score (score 4) data for training. You can refer to our technical report for more details.

You can see an example below:

```json
{
  "img_path1": "split1/class_generation_w1024_h1536_split_v1_Food_0_0_1_793x1024.png",
  "img_path2": "split1/class_generation_w1024_h1536_split_v1_Food_0_0_2_743x1024.png",
  "caption": {
    "img_path1": "A bowl of beef stew with carrots and garnished with a sprig of parsley, placed on a white surface.",
    "img_path2": "A bowl of beef stew with carrots and garnished with a sprig of parsley, placed on a wooden table surrounded by autumn leaves.",
    "judgment": "same",
    "subject": [
      "beef stew with carrots"
    ]
  },
  "vlm_filter_cot": {
    "score_part": {
      "Beef Chunks": 4.0,
      "Carrots": 3.0,
      "Appearance of the Stew": 4.0,
      "Garnish": 4.0
    },
    "score_final": 3.5
  }
}
```

## Citation

If you find our dataset helpful, please consider citing our work:

```bibtex
@article{wu2025less,
  title={Less-to-more generalization: Unlocking more controllability by in-context generation},
  author={Wu, Shaojin and Huang, Mengqi and Wu, Wenxu and Cheng, Yufeng and Ding, Fei and He, Qian},
  journal={arXiv preprint arXiv:2504.02160},
  year={2025}
}
```