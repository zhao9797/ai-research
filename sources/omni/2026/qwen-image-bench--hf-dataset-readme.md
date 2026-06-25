---
license: apache-2.0
task_categories:
  - image-to-text
language:
  - en
  - zh
size_categories:
  - 1K<n<10K
tags:
  - text-to-image
  - image-generation
  - benchmark
  - evaluation
configs:
  - config_name: default
    data_files:
      - split: test
        path: qwen_image_bench_hf_v0518.jsonl
---

# Qwen-Image-Bench

<p align="center">
  <a href="http://arxiv.org/abs/2605.28091"><img src="https://img.shields.io/badge/Paper-arXiv-b31b1b?logo=arxiv" alt="Paper"></a>
  <a href="https://github.com/QwenLM/Qwen-Image-Bench"><img src="https://img.shields.io/badge/GitHub-Repo-blue?logo=github" alt="GitHub"></a>
  <a href="https://huggingface.co/Qwen/Qwen-Image-Bench"><img src="https://img.shields.io/badge/Judge_Model-HuggingFace-ffd21e?logo=huggingface" alt="Model"></a>
  <a href="https://www.modelscope.cn/models/Qwen/Qwen-Image-Bench"><img src="https://img.shields.io/badge/Judge_Model-ModelScope-624aff?logo=data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB2ZXJzaW9uPSIxLjEiIHdpZHRoPSIyNCIgaGVpZ2h0PSIxNCIgdmlld0JveD0iMCAwIDI0IDE0IiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8dGl0bGU+TW9kZWxTY29wZSBCYWRnZTwvdGl0bGU+CjxnIGZpbGw9Im5vbmUiIGZpbGwtcnVsZT0iZXZlbm9kZCI+CjxnIGZpbGwtcnVsZT0ibm9uemVybyI+CjxwYXRoIGQ9Im0wIDIuNjY3aDIuNjY3djIuNjY3aC0yLjY2N3YtMi42Njd6bTggMi42NjZoMi42Njd2Mi42NjdoLTIuNjY3di0yLjY2N3oiIGZpbGw9IiMzNkNFRDAiLz4KPHBhdGggZD0ibTAgNS4zMzNoMi42Njd2Mi42NjdoLTIuNjY3di0yLjY2N3ptMi42NjcgMi42NjdoMi42NjZ2Mi42NjdoMi42Njd2Mi42NjZoLTUuMzMzdi01LjMzM3ptMC04aDUuMzMzdjIuNjY3aC0yLjY2N3YyLjY2NmgtMi42NjZ2LTUuMzMzem04IDhoMi42Njd2Mi42NjdoLTIuNjY3di0yLjY2N3oiIGZpbGw9IiM2MjRBRkYiLz4KPHBhdGggZD0ibTI0IDIuNjY3aC0yLjY2N3YyLjY2N2gyLjY2N3YtMi42Njd6bS04IDIuNjY2aC0yLjY2N3YyLjY2N2gyLjY2N3YtMi42Njd6IiBmaWxsPSIjMzZDRUQwIi8+CjxwYXRoIGQ9Im0yNCA1LjMzM2gtMi42Njd2Mi42NjdoMi42Njd2LTIuNjY3em0tMi42NjcgMi42NjdoLTIuNjY2djIuNjY3aC0yLjY2N3YyLjY2Nmg1LjMzM3YtNS4zMzN6bTAtOGgtNS4zMzN2Mi42NjdoMi42Njd2Mi42NjZoMi42NjZ2LTUuMzMzeiIgZmlsbD0iIzYyNEFGRiIvPgo8L2c+CjwvZz4KPC9zdmc+Cg==" alt="ModelScope"></a>
  <a href="https://huggingface.co/datasets/Qwen/Qwen-Image-Bench"><img src="https://img.shields.io/badge/Dataset-HuggingFace-ffd21e?logo=huggingface" alt="Dataset"></a>
  <a href="https://www.modelscope.cn/datasets/Qwen/Qwen-Image-Bench"><img src="https://img.shields.io/badge/Dataset-ModelScope-624aff?logo=data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB2ZXJzaW9uPSIxLjEiIHdpZHRoPSIyNCIgaGVpZ2h0PSIxNCIgdmlld0JveD0iMCAwIDI0IDE0IiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8dGl0bGU+TW9kZWxTY29wZSBCYWRnZTwvdGl0bGU+CjxnIGZpbGw9Im5vbmUiIGZpbGwtcnVsZT0iZXZlbm9kZCI+CjxnIGZpbGwtcnVsZT0ibm9uemVybyI+CjxwYXRoIGQ9Im0wIDIuNjY3aDIuNjY3djIuNjY3aC0yLjY2N3YtMi42Njd6bTggMi42NjZoMi42Njd2Mi42NjdoLTIuNjY3di0yLjY2N3oiIGZpbGw9IiMzNkNFRDAiLz4KPHBhdGggZD0ibTAgNS4zMzNoMi42Njd2Mi42NjdoLTIuNjY3di0yLjY2N3ptMi42NjcgMi42NjdoMi42NjZ2Mi42NjdoMi42Njd2Mi42NjZoLTUuMzMzdi01LjMzM3ptMC04aDUuMzMzdjIuNjY3aC0yLjY2N3YyLjY2NmgtMi42NjZ2LTUuMzMzem04IDhoMi42Njd2Mi42NjdoLTIuNjY3di0yLjY2N3oiIGZpbGw9IiM2MjRBRkYiLz4KPHBhdGggZD0ibTI0IDIuNjY3aC0yLjY2N3YyLjY2N2gyLjY2N3YtMi42Njd6bS04IDIuNjY2aC0yLjY2N3YyLjY2N2gyLjY2N3YtMi42Njd6IiBmaWxsPSIjMzZDRUQwIi8+CjxwYXRoIGQ9Im0yNCA1LjMzM2gtMi42Njd2Mi42NjdoMi42Njd2LTIuNjY3em0tMi42NjcgMi42NjdoLTIuNjY2djIuNjY3aC0yLjY2N3YyLjY2Nmg1LjMzM3YtNS4zMzN6bTAtOGgtNS4zMzN2Mi42NjdoMi42Njd2Mi42NjZoMi42NjZ2LTUuMzMzeiIgZmlsbD0iIzYyNEFGRiIvPgo8L2c+CjwvZz4KPC9zdmc+Cg==" alt="ModelScope"></a>
</p>

**A creator-centric benchmark for evaluating Text-to-Image models beyond semantic alignment.**

## Links

| Resource | Link |
|----------|------|
| 📑 Paper | http://arxiv.org/abs/2605.28091 |
| 📊 Benchmark Dataset (HuggingFace) | https://huggingface.co/datasets/Qwen/Qwen-Image-Bench |
| 📊 Benchmark Dataset (ModelScope) | https://www.modelscope.cn/datasets/Qwen/Qwen-Image-Bench |
| 💻 GitHub | https://github.com/QwenLM/Qwen-Image-Bench |
| 🧑‍⚖️ Q-Judger Model | https://huggingface.co/Qwen/Qwen-Image-Bench |
| 🧑‍⚖️ Q-Judger Model | https://modelscope.cn/models/Qwen/Qwen-Image-Bench |


## Overview

<p align="center">
  <img src="assets/show_case.png" alt="Qwen-Image-Bench dimension framework and representative model outputs across all L3 facets">
</p>

Text-to-Image (T2I) generation has evolved from basic image synthesis into a core capability in professional creative workflows. Simple text-image alignment can no longer satisfy the pressing demands for faithful real-world reconstruction and genuine creative expression. Existing benchmarks remain anchored in foundational criteria and fail to reliably distinguish state-of-the-art T2I models. Moreover, many evaluation pipelines rely on a single MLLM as the sole judge, diverging from professional human standards.

**Qwen-Image-Bench** is a creator-centric benchmark co-designed with professional artists and grounded in real-world creation scenarios. Building upon the conventional pillars of *Quality*, *Aesthetics*, and *Text-Image Alignment*, it enriches evaluation with two application-driven dimensions: **Real-world Fidelity** and **Creative Generation**.

## Key Features

### 🏗️ Three-Level Hierarchical Taxonomy

Designed top-down along the staged reasoning of professional artistic workflows (ideation → styling → iterative refinement):

- **5 L1 Pillars**: Quality, Aesthetics, Alignment, Real-world Fidelity, Creative Generation
- **23 L2 Sub-capabilities**: e.g., World Knowledge, Text Rendering, Visual Storytelling, Design Applications
- **56 L3 Evaluation Facets**: Fine-grained, verifiable rubrics anchoring each assessment

Among the 56 facets, 28 fall under the two application-driven pillars, covering high-frequency creator scenarios such as world knowledge, design applications, visual storytelling, and text rendering.

### 📝 1,000 Expert-Crafted Bilingual Prompts

- Stratified and balanced across length (500 long + 500 short) and language (Chinese/English)
- Each prompt jointly exercises **4+ fine-grained facets** across multiple pillars
- Designed to stress-test both novice-style brief descriptions and professional-grade detailed specifications

### 🧑‍⚖️ Q-Judger: A Unified Diagnostic Judge Model

Instead of a single opaque score, **Q-Judger** (based on Qwen3.6-27B) produces a complete fine-grained score vector across all 56 third-level facets for each sample, enabling precise diagnosis of capability gaps.

- Trained on **130,000+** bilingual expert-annotated prompt-image pairs
- Supervised by **80 professional annotators** from art academies (photography, directing, fine arts)
- Blind labeling with at least **3 independent reviews** per sample
- Achieves **Spearman ρ = 0.92** ranking consistency with human expert judgments

### 📊 Comprehensive Evaluation of 18 Frontier T2I Models

We evaluate 18 representative models including GPT Image 2, Nano Banana Pro, GPT Image 1.5, Seedream 5.0, Imagen 4.0 Ultra, Qwen Image 2.0 Pro, HunyuanImage 3.0, GLM Image, and more.

**Key findings:**
- GPT Image 2 achieves the highest overall score (64.7) across all five pillars
- The two application-driven pillars exhibit the **largest inter-model variance**, confirming they target capability gaps invisible to existing benchmarks
- 18 models naturally separate into **5 performance tiers** with a 16.5-point spread
- Four L3 facets (Physical Logic, Anatomical Fidelity, Animals, Contact Interaction) emerge as **systemic ceilings** where even the best models score below 44


## 🏆 Leaderboard

<!-- [Placeholder: Leaderboard table or link to online leaderboard] -->

| Rank | Model | Quality | Aesthetics | Alignment | Real-world Fidelity | Creative Generation | Overall |
|------|-------|---------|------------|-----------|---------------------|---------------------|---------|
| 1 | GPT Image 2 | **58.65** | **67.53** | **65.85** | **57.38** | **75.23** | **64.69** |
| 2 | Nano Banana 2.0 | 54.77 | 61.08 | 62.40 | 54.28 | 67.05 | 59.82 |
| 3 | GPT Image 1.5 | 55.14 | 60.88 | 61.72 | 53.95 | 66.35 | 59.65 |
| 4 | Nano Banana Pro | 55.67 | 60.26 | 61.25 | 54.07 | 66.23 | 59.45 |
| 5 | Qwen Image 2.0 Pro | 54.39 | 58.67 | 59.28 | 51.83 | 64.94 | 57.84 |
| 6 | Seedream 5.0 | 52.55 | 58.40 | 58.90 | 51.92 | 65.29 | 57.22 |
| 7 | Seedream 4.5 | 54.41 | 58.72 | 57.31 | 51.69 | 60.64 | 56.78 |
| 8 | Seedream 4.0 | 54.01 | 58.81 | 56.64 | 51.05 | 58.15 | 56.21 |
| 9 | FLUX 2 Max | 53.64 | 56.85 | 57.35 | 49.35 | 56.50 | 55.33 |
| 10 | FLUX 2 Pro | 52.30 | 56.94 | 57.01 | 47.29 | 56.18 | 54.57 |
| 11 | GPT Image 1 | 52.34 | 55.09 | 56.28 | 48.14 | 55.78 | 54.07 |
| 12 | Qwen Image 2512 | 51.76 | 54.74 | 52.72 | 47.00 | 50.19 | 52.06 |
| 13 | Imagen 4.0 Ultra | 50.90 | 54.25 | 54.02 | 45.59 | 51.14 | 51.99 |
| 14 | HunyuanImage 3.0 | 50.35 | 53.57 | 52.00 | 44.31 | 49.12 | 50.81 |
| 15 | Imagen 4.0 | 50.16 | 52.68 | 51.64 | 44.84 | 47.94 | 50.29 |
| 16 | Qwen Image | 48.44 | 52.25 | 50.72 | 43.16 | 47.30 | 49.23 |
| 17 | Kling Image 2.1 | 49.11 | 50.15 | 49.18 | 44.74 | 44.67 | 48.26 |
| 18 | GLM Image | 49.26 | 50.64 | 47.90 | 44.69 | 45.23 | 48.19 |

*The leaderboard results are computed based on Q-Judger's evaluation of images generated from Chinese prompts. We will release the results for image generation from English prompts soon.

## Results Analysis

### Overall Ranking

<p align="center">
  <img src="assets/figure_1_overall.png" alt="Overall ranking of 18 T2I models on Qwen-Image-Bench">
</p>

GPT Image 2 leads by nearly 5 points over the second-ranked Nano Banana 2.0, with GPT Image 1.5 and Nano Banana Pro following closely to form a tightly clustered second tier. Qwen Image 2.0 Pro ranks fifth overall, heading the third tier. GLM Image sits at the bottom, yielding a 16.5-point spread from the leader and demonstrating the benchmark's effective discriminative power across the full model spectrum. The 18 models naturally separate into **five tiers**:

- **T1 (64+):** GPT Image 2
- **T2 (59–60):** Nano Banana 2.0, GPT Image 1.5, Nano Banana Pro
- **T3 (56–58):** Qwen Image 2.0 Pro, Seedream 5.0, Seedream 4.5, Seedream 4.0
- **T4 (54–56):** FLUX 2 Max, FLUX 2 Pro, GPT Image 1
- **T5 (48–52):** seven remaining models

Notably, GPT Image 2 achieves the highest score on all five L1 pillars simultaneously, forming a dominant profile with no discernible weakness, a rarity among the 18 evaluated models.

### Per-Pillar (L1) Rankings

<p align="center">
  <img src="assets/figure_2_l1_ranking.png" alt="Per-pillar rankings across the five L1 dimensions">
</p>

**Creative Generation produces the largest ranking shifts.** GPT Image 2 leads, followed by Nano Banana 2.0 and GPT Image 1.5. Qwen Image 2.0 Pro ranks sixth on this pillar. The 30.6-point spread between the leader and the bottom-ranked model is the largest among all five pillars, confirming Creative Generation as the most discriminative dimension.

**Quality rankings diverge most from the overall leaderboard.** Nano Banana Pro climbs to second on Quality, demonstrating superior artifact suppression and physical-logic handling. The Seedream series illustrates a noteworthy version-evolution trade-off: Seedream 4.5 scores higher than 5.0 on Quality and Aesthetics, while 5.0 surges ahead on Creative Generation by over 4 points, suggesting that the newer release prioritized creative capabilities at the cost of basic image quality. This trade-off is one that our multi-pillar evaluation makes explicit but a single-score benchmark would obscure.

**Aesthetics and Alignment show the most stable rankings.** The top four models (GPT Image 2, Nano Banana 2.0, GPT Image 1.5, Nano Banana Pro) retain their positions across both pillars. On Alignment, Qwen Image 2.0 Pro rises to fifth, while on Aesthetics the Seedream series (4.0/4.5/5.0) forms a tightly clustered band with near-identical scores occupying ranks 5–8.

**Real-world Fidelity separates production-grade models.** GPT Image 2 leads, with the next cluster (Nano Banana 2.0, GPT Image 1.5, Nano Banana Pro) trailing by roughly 3 points. The 14-point gap between the leader and the lowest-performing models supports the observation that faithful reconstruction of real-world structure and knowledge-grounded content is currently a defining advantage of frontier models.

**Application-driven pillars widen the gap between tiers.** Qwen Image 2.0 Pro ranks fifth on Alignment but sixth on Quality, Real-world Fidelity, and Creative Generation (seventh on Aesthetics). Its gap to GPT Image 2 remains moderate on Quality and Alignment but widens sharply on Aesthetics and Creative Generation. Despite this, Qwen Image 2.0 Pro scores at or above the industry mean on virtually all L3 facets, indicating a solid "no-weakness" baseline.

### Variance Analysis

<p align="center">
  <img src="assets/figure_3_variance.png" alt="Variance across L1, L2, and L3 dimensions">
</p>

**L3 variance pinpoints the sharpest frontiers.** At the finest granularity, Text Accuracy (under Creative Generation) is the single most discriminative facet. Information Visualization (under Real-world Fidelity) and Cross-lingual Generation (under Creative Generation) rank second and third. Of the 15 highest-variance L3 facets, **12 belong to Creative Generation or Real-world Fidelity** (e.g., Storyboard Creation, Graphic Design, Cross-lingual Generation, Game Design), dimensions that jointly test creative imagination, logical reasoning, and execution precision.

**L2 variance confirms application-driven dimensions dominate.** Rolling up to the second level, the highest-variance L2 sub-capability is Text Rendering (under Creative Generation), followed by Style Control (under Aesthetics), Logical Resolution (under Creative Generation), and World Knowledge (under Real-world Fidelity). Among the top six L2 dimensions by variance, four belong to the two application-driven pillars introduced by our benchmark.

**L1 variance reveals where differentiation lies.** At the pillar level, Creative Generation variance is over **11×** that of Quality and over **4×** that of Aesthetics. The low variance on Quality indicates that basic image quality has become a "table-stakes" capability, while Creative Generation, the pillar most unique to our creator-centric design, is precisely where models diverge most sharply.

### L3 Heatmap

<p align="center">
  <img src="assets/heatmap.png" alt="L3-level heatmap of all 18 models across 56 third-level facets">
</p>

The L3-level heatmap provides a comprehensive visualization of all 18 models across all 56 third-level facets. Several patterns are immediately visible.

**A clear left-to-right gradient mirrors the overall ranking tiers.** The heatmap transitions from deep color on the left to light color on the right, mirroring the overall ranking. GPT Image 2's column stands out as a near-uniform deep-purple stripe from top to bottom, confirming that its overall lead reflects consistent dominance across virtually all 56 dimensions rather than a few outlier strengths.

**A sharp color discontinuity within Creative Generation reveals a threshold effect.** Around ranks 5–6, facets such as Text Accuracy, Game Design, Storyboard Creation, and Comic Creation transition abruptly from moderate scores to near-white. Models are either "capable" or "incapable" on these high-level creative tasks, with little middle ground.

**Three rows expose systemic capability ceilings.** Physical Logic, Anatomical Fidelity, and Animals remain uniformly pale across all 18 models, highlighting these as systemic capability ceilings of current T2I technology rather than model-specific weaknesses. Conversely, Material Properties under Alignment shows a consistently dark row (leader: 84.1), indicating that material-attribute adherence is the most reliably followed instruction type across all models.


## Data Fields

Each row in the JSONL file contains:

| Field | Type | Description |
|-------|------|-------------|
| `ID` | int | Unique prompt identifier (1-1000) |
| `prompt_cn` | str | Text prompt in Chinese |
| `prompt_en` | str | Text prompt in English |
| `dims_cn` | str | Evaluation dimensions for this prompt (Chinese) |
| `dims_en` | str | Evaluation dimensions for this prompt (English) |
| `<model_name>` | str | Relative path to the generated image for each model (Use prompt_cn)|
| `quality_response_<model>` | str | Judge model raw output for the Quality dimension |
| `aesthetics_response_<model>` | str | Judge model raw output for the Aesthetics dimension |
| `alignment_response_<model>` | str | Judge model raw output for the Alignment dimension |
| `creative_generation_response_<model>` | str | Judge model raw output for the Creative Generation dimension |
| `real_world_fidelity_response_<model>` | str | Judge model raw output for the Real-world Fidelity dimension |

### Included Models (18)

Qwen-Image-2.0-pro, Gpt-Image-2, FLUX.2-Max, Nano-Banana-2.0, Nano-Banana-Pro, Seedream-4.0, Seedream-4.5, Seedream-5.0, GLM-Image, Kling-v2.1, Qwen-Image-2512, Qwen-Image, GPT-Image-1, GPT-Image-1.5, HunyuanImage-3.0, Imagen-4.0, Imagen-4.0-Ultra, FLUX.2-Pro

## Evaluation Dimensions

The benchmark uses a **3-level hierarchical scoring system** across 5 top-level dimensions:

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

### Scoring Pipeline

Scores are aggregated bottom-up per sample: L3 → L2 → L1 → Overall. Each sample's overall score is the unweighted mean of its active L1 pillars (3–5 per prompt). The model-level score is the mean across all 1,000 prompts.


## Usage

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

### Compute Scores from Pre-generated Responses

```bash

# From local file
python compute_scores.py --input qwen_image_bench_hf_v0518.jsonl

# Or download from HuggingFace
python compute_scores.py --hf-repo Qwen/Qwen-Image-Bench
```

Output: `scores_result.xlsx` + `scores_detail.json`

### Run Judge Model Inference on Your Own Images

Prepare an input CSV/JSON/JSONL file with columns: `ID`, `prompt`, `image_path`.

The `ID` column must match the benchmark metadata (1-1000), which defines which evaluation dimensions apply to each prompt. The metadata file (`metadata/bench_metadata.json`) is loaded automatically by default.

#### Run Judge Inference

```bash
python judge.py \
  --input your_data.jsonl \
  --model Qwen/Qwen-Image-Bench
# metadata auto-loaded from metadata/bench_metadata.json
```

#### CLI Options for `judge.py`

| Argument | Default | Description |
|----------|---------|-------------|
| `--input` | (required) | Input CSV/JSON/JSONL with ID, prompt, image_path |
| `--model` | (required) | HuggingFace model ID or local model path |
| `--hf-bench-repo` | - | HF dataset repo for bench metadata |
| `--local-metadata` | - | Local metadata file path (overrides default) |
| `--max-batch-size` | 24 | ms-swift PtEngine max_batch_size |
| `--max-new-tokens` | 4096 | Max generation tokens |

### Output Files

After running `judge.py`, three files are written next to your input:

| File | Contents |
|---|---|
| `<input>_judged.{jsonl,csv}` | Per-row results: all original input fields + `judge_model_output` (combined raw scores JSON string across all evaluated L1 dimensions) + `<dim>_judge_output` (raw judge model text for each L1 dimension) |
| `<input>_bench_scores.json` | Bench-level aggregated scores: `level1`, `level2`, `total` |
| `<input>_bench_scores.xlsx` | Same scores in Excel: `Level-1 Summary` sheet + one sheet per L1 dimension with L2 detail |




## Inference Parameters

The judge model uses fixed inference parameters that mirror the ms-swift CLI flags used to generate the dataset's `*_response_*` fields:

| Parameter | Value | swift CLI flag |
|-----------|-------|----------------|
| `seed` | 42 | `--seed 42` |
| `temperature` | 0 | `--temperature 0` |
| `top_k` | 1 | `--top_k 1` |
| `top_p` | 1.0 | `--top_p 1` |
| `repetition_penalty` | 1.05 | `--repetition_penalty 1.05` |
| `max_new_tokens` | 4096 | `--max_new_tokens 4096` |
| `enable_thinking` | True | `--enable_thinking true` |
| `max_batch_size` | 24 | `--max_batch_size 24` |

## File Structure

```
./
├── qwen_image_bench_hf_v0518.jsonl   # Benchmark data with judge responses
├── images/                            # Generated images from 18 models
│   ├── Qwen-Image-2.0-pro/
│   ├── gpt-image-2/
│   └── ...
├── metadata/
│   └── bench_metadata.json            # ID + dims_en metadata for judge inference
├── compute_scores.py                  # Compute scores from pre-generated responses
├── judge.py                           # Run judge model inference on new images
├── score_utils.py                     # Score extraction, mapping, correction, aggregation
├── checklists.py                      # Evaluation prompts and dimension definitions
├── backends/
│   └── ms_swift_backend.py           # ms-swift inference engine
├── requirements.txt
└── README.md
```

## Citation

If you find this benchmark useful, please cite our paper:

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
