---
pipeline_tag: any-to-any
library_name: transformers
tags:
- text-to-image
- image-editing
- image-understanding
- vision-language
- multimodal
- unified-model
- teacher-model
- diffusion
license: mit
---

## 🌌 UniPic3-Teacher-Model
<div align="center">   
  <img src="logo.png" alt="Skywork Logo" width="500"> 
</div>

<p align="center">
  <a href="https://github.com/SkyworkAI/UniPic">
    <img src="https://img.shields.io/badge/GitHub-UniPic-blue?logo=github" alt="GitHub Repo">
  </a>
  <a href="https://github.com/SkyworkAI/UniPic/stargazers">
    <img src="https://img.shields.io/github/stars/SkyworkAI/UniPic?style=social" alt="GitHub Stars">
  </a>
  <a href="https://github.com/SkyworkAI/UniPic/network/members">
    <img src="https://img.shields.io/github/forks/SkyworkAI/UniPic?style=social" alt="GitHub Forks">
  </a>
</p>

## 📖 Introduction
<div align="center"> <img src="unipic3.png" alt="Model Teaser" width="720"> </div>

**UniPic3-Teacher-Model** is the **high-quality teacher diffusion model** used in the UniPic 3.0 framework.
It is trained with **full multi-step diffusion sampling** and optimized for **maximum perceptual quality, semantic consistency, and realism**.

This model serves as the **teacher backbone** for:
- **Distribution Matching Distillation (DMD)**
- **Consistency / trajectory distillation**
- **Few-step student model training**

Rather than being optimized for fast inference, the teacher model prioritizes **generation fidelity and stability**, providing a strong and reliable supervision signal for downstream distilled models.

---

## 🧠 Model Characteristics

- **Role**: Teacher model (not a distilled student)
- **Sampling**: Multi-step diffusion (high-fidelity)
- **Architecture**: Unified UniPic3 Transformer
- **Tasks Supported**:
  - Single-image editing
  - Multi-image composition (2–6 images)
  - Human–Object Interaction (HOI)
- **Resolution**: Flexible, within pixel budget constraints
- **Training Objective**:
  - Flow Matching / Diffusion loss
  - Used as teacher for DMD & consistency training

---

## 📊 Benchmarks
<div align="center"> <img src="unipic3_eval.png" alt="Model Teaser" width="720"> </div>

This teacher model achieves **state-of-the-art performance** on:
- Image editing benchmarks
- Multi-image composition benchmarks

It provides **high-quality supervision targets** for distilled UniPic3 student models.

---

## ⚠️ Important Note

> **This repository hosts the teacher model.**  
> It is **not optimized for few-step inference**.

If you are looking for:
- ⚡ **4–8 step fast inference**
- 🚀 **Deployment-friendly distilled models**

please refer to the **UniPic3-DMD / distilled checkpoints** instead.

---

## 🧠 Usage (Teacher Model)

### 1. Clone the Repository
```bash
git clone https://github.com/SkyworkAI/UniPic
cd UniPic-3
```

### 2. Set Up the Environment
```bash
conda create -n unipic python=3.10
conda activate unipic3
pip install -r requirements.txt
```


### 3.Batch Inference
```bash
transformer_path = "Skywork/Unipic3"

python -m torch.distributed.launch --nproc_per_node=1 --master_port 29501 --use_env \
    qwen_image_edit_fast/batch_inference.py \
    --jsonl_path data/val.jsonl \
    --output_dir work_dirs/output \
    --distributed \
    --num_inference_steps 50 \
    --true_cfg_scale 4.0 \
    --transformer transformer_path \
    --skip_existing
```

## 📄 License
This model is released under the MIT License.

## Citation
If you use Skywork-UniPic in your research, please cite:
```
@article{wang2025skywork,
  title={Skywork unipic: Unified autoregressive modeling for visual understanding and generation},
  author={Wang, Peiyu and Peng, Yi and Gan, Yimeng and Hu, Liang and Xie, Tianyidan and Wang, Xiaokun and Wei, Yichen and Tang, Chuanxin and Zhu, Bo and Li, Changshi and others},
  journal={arXiv preprint arXiv:2508.03320},
  year={2025}
}
```

```
@article{wei2025skywork,
  title={Skywork unipic 2.0: Building kontext model with online rl for unified multimodal model},
  author={Wei, Hongyang and Xu, Baixin and Liu, Hongbo and Wu, Cyrus and Liu, Jie and Peng, Yi and Wang, Peiyu and Liu, Zexiang and He, Jingwen and Xietian, Yidan and others},
  journal={arXiv preprint arXiv:2509.04548},
  year={2025}
}
```

```
@article{wei2026skywork,
  title={Skywork UniPic 3.0: Unified Multi-Image Composition via Sequence Modeling},
  author={Wei, Hongyang and Liu, Hongbo and Wang, Zidong and Peng, Yi and Xu, Baixin and Wu, Size and Zhang, Xuying and He, Xianglong and Liu, Zexiang and Wang, Peiyu and others},
  journal={arXiv preprint arXiv:2601.15664},
  year={2026}
}
```
