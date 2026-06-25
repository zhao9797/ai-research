---
license: apache-2.0
language:
  - en
  - zh
base_model: Qwen/Qwen3.6-27B
pipeline_tag: image-text-to-text
library_name: transformers
tags:
  - judge-model
  - text-to-image
  - evaluation
  - benchmark
  - qwen
---

# Q-Judger

<p align="center">
  <a href="http://arxiv.org/abs/2605.28091"><img src="https://img.shields.io/badge/Paper-arXiv-b31b1b?logo=arxiv" alt="Paper"></a>
  <a href="https://github.com/QwenLM/Qwen-Image-Bench"><img src="https://img.shields.io/badge/GitHub-Repo-blue?logo=github" alt="GitHub"></a>
  <a href="https://huggingface.co/Qwen/Qwen-Image-Bench"><img src="https://img.shields.io/badge/Judge_Model-HuggingFace-ffd21e?logo=huggingface" alt="Model"></a>
  <a href="https://www.modelscope.cn/models/Qwen/Qwen-Image-Bench"><img src="https://img.shields.io/badge/Judge_Model-ModelScope-624aff?logo=data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB2ZXJzaW9uPSIxLjEiIHdpZHRoPSIyNCIgaGVpZ2h0PSIxNCIgdmlld0JveD0iMCAwIDI0IDE0IiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8dGl0bGU+TW9kZWxTY29wZSBCYWRnZTwvdGl0bGU+CjxnIGZpbGw9Im5vbmUiIGZpbGwtcnVsZT0iZXZlbm9kZCI+CjxnIGZpbGwtcnVsZT0ibm9uemVybyI+CjxwYXRoIGQ9Im0wIDIuNjY3aDIuNjY3djIuNjY3aC0yLjY2N3YtMi42Njd6bTggMi42NjZoMi42Njd2Mi42NjdoLTIuNjY3di0yLjY2N3oiIGZpbGw9IiMzNkNFRDAiLz4KPHBhdGggZD0ibTAgNS4zMzNoMi42Njd2Mi42NjdoLTIuNjY3di0yLjY2N3ptMi42NjcgMi42NjdoMi42NjZ2Mi42NjdoMi42Njd2Mi42NjZoLTUuMzMzdi01LjMzM3ptMC04aDUuMzMzdjIuNjY3aC0yLjY2N3YyLjY2NmgtMi42NjZ2LTUuMzMzem04IDhoMi42Njd2Mi42NjdoLTIuNjY3di0yLjY2N3oiIGZpbGw9IiM2MjRBRkYiLz4KPHBhdGggZD0ibTI0IDIuNjY3aC0yLjY2N3YyLjY2N2gyLjY2N3YtMi42Njd6bS04IDIuNjY2aC0yLjY2N3YyLjY2N2gyLjY2N3YtMi42Njd6IiBmaWxsPSIjMzZDRUQwIi8+CjxwYXRoIGQ9Im0yNCA1LjMzM2gtMi42Njd2Mi42NjdoMi42Njd2LTIuNjY3em0tMi42NjcgMi42NjdoLTIuNjY2djIuNjY3aC0yLjY2N3YyLjY2Nmg1LjMzM3YtNS4zMzN6bTAtOGgtNS4zMzN2Mi42NjdoMi42Njd2Mi42NjZoMi42NjZ2LTUuMzMzeiIgZmlsbD0iIzYyNEFGRiIvPgo8L2c+CjwvZz4KPC9zdmc+Cg==" alt="ModelScope"></a>
  <a href="https://huggingface.co/datasets/Qwen/Qwen-Image-Bench"><img src="https://img.shields.io/badge/Dataset-HuggingFace-ffd21e?logo=huggingface" alt="Dataset"></a>
  <a href="https://www.modelscope.cn/datasets/Qwen/Qwen-Image-Bench"><img src="https://img.shields.io/badge/Dataset-ModelScope-624aff?logo=data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB2ZXJzaW9uPSIxLjEiIHdpZHRoPSIyNCIgaGVpZ2h0PSIxNCIgdmlld0JveD0iMCAwIDI0IDE0IiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8dGl0bGU+TW9kZWxTY29wZSBCYWRnZTwvdGl0bGU+CjxnIGZpbGw9Im5vbmUiIGZpbGwtcnVsZT0iZXZlbm9kZCI+CjxnIGZpbGwtcnVsZT0ibm9uemVybyI+CjxwYXRoIGQ9Im0wIDIuNjY3aDIuNjY3djIuNjY3aC0yLjY2N3YtMi42Njd6bTggMi42NjZoMi42Njd2Mi42NjdoLTIuNjY3di0yLjY2N3oiIGZpbGw9IiMzNkNFRDAiLz4KPHBhdGggZD0ibTAgNS4zMzNoMi42Njd2Mi42NjdoLTIuNjY3di0yLjY2N3ptMi42NjcgMi42NjdoMi42NjZ2Mi42NjdoMi42Njd2Mi42NjZoLTUuMzMzdi01LjMzM3ptMC04aDUuMzMzdjIuNjY3aC0yLjY2N3YyLjY2NmgtMi42NjZ2LTUuMzMzem04IDhoMi42Njd2Mi42NjdoLTIuNjY3di0yLjY2N3oiIGZpbGw9IiM2MjRBRkYiLz4KPHBhdGggZD0ibTI0IDIuNjY3aC0yLjY2N3YyLjY2N2gyLjY2N3YtMi42Njd6bS04IDIuNjY2aC0yLjY2N3YyLjY2N2gyLjY2N3YtMi42Njd6IiBmaWxsPSIjMzZDRUQwIi8+CjxwYXRoIGQ9Im0yNCA1LjMzM2gtMi42Njd2Mi42NjdoMi42Njd2LTIuNjY3em0tMi42NjcgMi42NjdoLTIuNjY2djIuNjY3aC0yLjY2N3YyLjY2Nmg1LjMzM3YtNS4zMzN6bTAtOGgtNS4zMzN2Mi42NjdoMi42Njd2Mi42NjZoMi42NjZ2LTUuMzMzeiIgZmlsbD0iIzYyNEFGRiIvPgo8L2c+CjwvZz4KPC9zdmc+Cg==" alt="ModelScope"></a>
</p>

A fine-tuned judge model for evaluating text-to-image (T2I) generation quality. Built on top of Qwen3.6-27B, it scores generated images across **5 hierarchical dimensions** using structured checklists and outputs JSON-formatted evaluation results.

## Links

| Resource | Link |
|----------|------|
| 📑 Paper | http://arxiv.org/abs/2605.28091 |
| 📊 Benchmark Dataset (HuggingFace) | https://huggingface.co/datasets/Qwen/Qwen-Image-Bench |
| 📊 Benchmark Dataset (ModelScope) | https://www.modelscope.cn/datasets/Qwen/Qwen-Image-Bench |
| 💻 GitHub | https://github.com/QwenLM/Qwen-Image-Bench |
| 🧑‍⚖️ Q-Judger Model | https://huggingface.co/Qwen/Qwen-Image-Bench |
| 🧑‍⚖️ Q-Judger Model | https://modelscope.cn/models/Qwen/Qwen-Image-Bench |


## Model Description

Q-Judger is a vision-language model fine-tuned specifically for automated evaluation of text-to-image generated images. Given a text prompt and a generated image, the model evaluates the image on fine-grained quality criteria organized in a 3-level hierarchy and outputs structured JSON scores.

- **Base Model**: Qwen3.6-27B
- **Task**: Image quality evaluation / judging
- **Input**: Text prompt + generated image
- **Output**: Structured JSON with per-dimension scores (0 = Fail, 1 = Pass, 2 = Excel, N/A)
- **Thinking Mode**: Enabled — the model uses chain-of-thought reasoning before producing the final JSON output

## Evaluation Dimensions

The model evaluates images across **5 top-level dimensions**, each with multiple sub-dimensions:

### Quality
- **Realism**: Physical Logic, Material Texture
- **Detail**: Noise, Edge Clarity, Naturalness
- **Resolution**: Resolution

### Aesthetics
- **Composition**: Composition
- **Color Harmony**: Color Harmony
- **Lighting**: Lighting & Atmosphere
- **Anatomical Portraiture**: Anatomical Fidelity
- **Emotional Expression**: Emotional Expression
- **Style Control**: Style Control

### Alignment
- **Attributes**: Quantity, Facial Expression, Material Properties, Color, Shape, Size
- **Actions**: Contact Interaction, Non-contact Interaction, Full-body Action
- **Layout**: 2D Space, 3D Space
- **Relations**: Composition Relationship, Difference/Similarity, Containment
- **Scene**: Real-world Scene, Virtual Scene

### Real-world Fidelity
- **Fairness**: Social Bias, Cultural Fairness
- **Safety & Compliance**: Safety & Compliance
- **World Knowledge**: Animals, Objects, Information Visualization, Temporal Characteristics, Cultural Elements

### Creative Generation
- **Imagination**: Imagination
- **Feature Matching**: Feature Matching
- **Logical Resolution**: Logical Resolution
- **Text Rendering**: Text Accuracy, Text Layout, Font, Cross-lingual Generation
- **Design Applications**: Graphic Design, Product Design, Spatial Design, Fashion Styling, Game Design, Art Design
- **Visual Storytelling**: Cinematic Style, Camera / Lens Style, Storyboard Creation, Shot Sizes, Composition, Angles, Comic Creation

## Scoring Methodology

### Raw Score Mapping

| Raw Score | Meaning | Mapped Score |
|-----------|---------|--------------|
| 0 | Fail | 0 |
| 1 | Pass | 60 |
| 2 | Excel | 100 |
| N/A | Not applicable | Excluded |

### Aggregation

1. **Level-3 → Level-2**: Average all non-N/A Level-3 scores within a Level-2 category
2. **Level-2 → Level-1**: Average all Level-2 scores within a Level-1 dimension
3. **Level-1 → Total**: Average all Level-1 dimension scores

## Human Agreement

We validate the judge model against human expert rankings by computing Spearman rank correlation ($\rho$) between the model's rankings and human expert rankings across the five L1 pillars and overall. All correlations are statistically significant ($p < 10^{-4}$, $N = 18$ models).

| Dimension            | Spearman $\rho$ |
|----------------------|:---------------:|
| Quality              | 0.89            |
| Aesthetics           | 0.89            |
| Alignment            | 0.89            |
| Real-world Fidelity  | 0.92            |
| Creative Generation  | 0.92            |
| **Overall**          | **0.92**        |

## Quick Start

### Get the Inference Code

```bash
git clone https://github.com/QwenLM/Qwen-Image-Bench.git
cd Qwen-Image-Bench
```

### Installation

**1. Create and activate a virtual environment with uv:**

```bash
uv venv myenv --python 3.11
source myenv/bin/activate
```

**2. Install PyTorch** (select the command matching your CUDA version):

See the official guide: [https://pytorch.org/get-started/locally/](https://pytorch.org/get-started/locally/)

**3. Install Python dependencies:**

```bash
uv pip install -r requirements.txt
```

This installs all required dependencies including ms-swift.

### Run Inference

```bash
python judge.py \
  --input your_data.jsonl \
  --model Qwen/Qwen-Image-Bench
```

### Input Format

Prepare a CSV, JSON, or JSONL file with the following columns:

| Column | Type | Description |
|--------|------|-------------|
| `ID` | int | Prompt identifier (1-1000), must match benchmark metadata |
| `prompt` | str | The text prompt used to generate the image |
| `image_path` | str | Path to the generated image file |

### Output Format

The model outputs a JSON object per dimension, structured as:

```json
{
  "Level-2 Dimension": {
    "Level-3 Dimension": {"score": 0|1|2|"N/A"}
  }
}
```

Example (Quality dimension):

```json
{
  "Realism": {
    "Physical Logic": {"score": 1},
    "Material Texture": {"score": 2}
  },
  "Detail": {
    "Noise": {"score": 1},
    "Edge Clarity": {"score": 1},
    "Naturalness": {"score": 1}
  },
  "Resolution": {
    "Resolution": {"score": 2}
  }
}
```

### CLI Options

| Argument | Default | Description |
|----------|---------|-------------|
| `--input` | (required) | Input CSV/JSON/JSONL with ID, prompt, image_path |
| `--model` | (required) | HuggingFace model ID or local model path |
| `--hf-bench-repo` | - | HF dataset repo for bench metadata |
| `--local-metadata` | - | Local metadata file path (overrides default) |
| `--max-batch-size` | 24 | ms-swift max_batch_size |
| `--max-new-tokens` | 4096 | Max generation tokens |

## Inference Parameters

The judge model uses fixed inference parameters for reproducibility:

| Parameter | Value |
|-----------|-------|
| `seed` | 42 |
| `temperature` | 0 |
| `top_k` | 1 |
| `top_p` | 1.0 |
| `repetition_penalty` | 1.05 |
| `max_new_tokens` | 4096 |
| `enable_thinking` | True |
| `max_batch_size` | 24 |


## Citation

If you find this model useful, please cite our paper:

```bibtex
@misc{li2026qwenimagebenchgenerationcreationtexttoimage,
      title={Qwen-Image-Bench: From Generation to Creation in Text-to-Image Evaluation}, 
      author={Niantong Li and Guangzheng Hu and Weixu Qiao and Ying Ba and Qichen Hong and Shijun Shen and Jinlin Wang and Fan Zhou and Jianye Kang and Xin Shang and Ziyi He and Wei Wang and Dalin Li and Jiahao Li and Jie Zhang and Kaiyuan Gao and Kun Yan and Lihan Jiang and Ningyuan Tang and Shengming Yin and Tianhe Wu and Xiao Xu and Xiaoyue Chen and Yuxiang Chen and Yan Shu and Yanran Zhang and Yilei Chen and Yixian Xu and Zekai Zhang and Zhendong Wang and Zihao Liu and Zikai Zhou and Hongzhu Shi and Yi Wang and Bing Zhao and Hu Wei and Lin Qu and Chenfei Wu},
      year={2026},
      eprint={2605.28091},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2605.28091}, 
}
```

## License

This project is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).
