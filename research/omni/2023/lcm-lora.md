---
title: "LCM-LoRA: A Universal Stable-Diffusion Acceleration Module"
org: "Tsinghua University (IIIS) / Hugging Face"
country: China
date: "2023-11"
type: tech-report
category: method
tags: [distillation, lcm, lora, consistency-model, few-step, acceleration, stable-diffusion, sdxl, pf-ode, task-arithmetic]
url: "https://arxiv.org/abs/2311.05556"
arxiv: "https://arxiv.org/abs/2311.05556"
pdf_url: "https://arxiv.org/pdf/2311.05556"
github_url: "https://github.com/luosiallen/latent-consistency-model"
hf_url: "https://huggingface.co/latent-consistency/lcm-lora-sdxl"
modelscope_url: ""
project_url: "https://latent-consistency-models.github.io"
downloaded: [arxiv-2311.05556.pdf, lcm-lora--hf-sdxl-readme.md, lcm-lora--hf-sdv1-5-readme.md, lcm-lora--github-readme.md, lcm-lora--hf-blog.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
LCM-LoRA 把 [[latent-consistency-models|LCM]] 的「少步采样」能力蒸馏进一组可插拔的 LoRA 适配器（acceleration vector），**免再训练**即可叠加到任意 SD/SDXL 微调模型或风格 LoRA 上，把 25–50 步采样压到 2–8 步；本质是一个具备强泛化能力的「神经网络版 PF-ODE 求解器」。在 4090 上 SDXL 出图从 ~3.4s（25 步）降到 ~0.7s（4 步）。

## 背景与定位
扩散模型（[[latent-diffusion-ldm|LDM]]）反向采样慢，长期阻碍实时应用。加速路线有两条：(1) 高阶 ODE-Solver（DDIM、DPM-Solver、DPM-Solver++）——减步但在引入 classifier-free guidance（CFG）后开销仍大；(2) 蒸馏（Guided-Distill 等）——计算昂贵。2023 年的 LCM（Luo et al., 2023，arXiv:2310.04378）把引导反向扩散视为增广 PF-ODE 求解问题，直接在 latent 空间预测 ODE 解，1–4 步出高分辨率图，且只需 ~32 A100 训练小时。

LCM 的痛点：**每个定制模型都要单独蒸馏**——对动漫/写实/奇幻等专用数据集，要么用 LCD（Latent Consistency Distillation）从 teacher 重蒸，要么用 LCF（Latent Consistency Finetuning）微调已有 LCM，都需额外训练，阻碍快速部署。LCM-LoRA 回答的核心问题是：**能否对任意自定义模型做免训练、少步推理？** 做法是把 LCM 蒸馏改成 LoRA 形式，并发现蒸出来的 LoRA 参数可以与风格 LoRA 做线性组合（task arithmetic），无需任何额外训练即获得「该风格 + 少步」的合成模型。它是 LCM 的官方续作（技术报告，非完整论文），由清华 LCM 原作者 + Hugging Face Diffusers 团队联合完成。

## 模型架构
LCM-LoRA 本身**不引入新的网络架构**，它是加在现成 SD 主干上的低秩适配器：

- **被加速的主干**：Stable Diffusion 系列的 U-Net（latent diffusion），配 VAE（latent 空间编解码）与 text encoder（SD-v1.5 用 CLIP；SDXL 用双 CLIP）。报告覆盖三档主干：
  - **SD-V1.5**：全参 0.98B；512×512 出图。
  - **SSD-1B**（Segmind 蒸出的 SDXL，体积小 50%、快 60%）：全参 1.3B；1024×1024。
  - **SDXL**：全参 3.5B；1024×1024。
- **LoRA 注入**：对预训练权重矩阵 W₀∈R^{d×k} 做低秩分解 ΔW = BA（B∈R^{d×r}, A∈R^{r×k}, 秩 r≤min(d,k)），前向 h = W₀x + BAx；训练时 W₀ 冻结，只更新 A、B。可训练参数大幅缩减：
  | 主干 | 全参 | LoRA 可训练参数 |
  |---|---|---|
  | SD-V1.5 | 0.98B | 67.5M |
  | SSD-1B | 1.3B | 105M |
  | SDXL | 3.5B | 197M |
- **核心架构洞见——「acceleration vector」**：把 LCM 蒸馏视为对扩散模型的一次微调，于是蒸出的 LoRA 参数 τ_LCM = θ_LCM − θ_base 就是一个**加速向量**；风格微调得到的 LoRA 参数 τ′ = θ′ − θ_base 是**风格向量**。两者线性组合 τ′_LCM = λ₁τ′ + λ₂τ_LCM，再叠到预训练权重 θ′_LCM = θ_pre + τ′_LCM，即得「既有该风格、又能少步采样」的模型，**无需对组合后参数再训练**（报告用 λ₁=0.8, λ₂=1.0）。
- **推理侧调度器**：使用 LCM 的多步采样器（Diffusers 中的 `LCMScheduler`），步数 2–8。

## 数据
- LCM-LoRA 报告**未单列自己的训练数据集明细**；它沿用 LCM 的蒸馏范式（teacher 即预训练 SD/SDXL，无需新标注的图文对，蒸馏数据为无标注/弱标注图像 latent）。
- LCM 原作（被本报告引用并继承）在 **LAION-5B-Aesthetics** 子集上做蒸馏并刷 SOTA；HF 训练脚本示例用 LAION 这类大规模数据做全模型蒸馏。
- 美学/安全过滤、配比、re-captioning 等细节本报告**未披露**（属 LCM 原文与 SD/SDXL 底模范畴）。蒸馏本质是用 teacher 输出做监督，对人工标注依赖很低，这也是「免数据成本」卖点的来源。

## 训练方法
核心是把 **Latent Consistency Distillation (LCD)** 套进 LoRA：

- **训练目标（一致性蒸馏）**：把引导反向扩散当作增广 PF-ODE，学一个一致性函数 f_θ，使 ODE 轨迹上不同时刻的点都映射到同一原点（一步可达解）。损失为自一致性损失 L(θ,θ⁻) = d(f_θ(z_{t_{n+k}}, ω, c, t_{n+k}), f_{θ⁻}(ẑ^{Ψ,ω}_{t_n}, ω, c, t_n))，其中 ẑ 由 teacher 的 ODE-solver Ψ 一步推进得到，θ⁻ 是 EMA 目标网络（θ⁻ ← stopgrad(μθ⁻ + (1−μ)θ)）。
- **关键 trick**：
  - **CFG 蒸进输入**：把 guidance scale ω 从区间 [ω_min, ω_max] 采样并作为条件喂进网络（ẑ = z + (1+ω)Ψ(z,…,c) − ωΨ(z,…,∅)），从而把 CFG 内化进单次前向，推理时无需再跑两路 CFG。
  - **Skipping-Steps**：用跳步间隔 k 加速收敛（teacher ODE 一次推进 k 步而非 1 步）。
- **LoRA 蒸馏（本报告创新）**：上述 LCD 只更新 LoRA 的 A、B 矩阵 → 训练显存大幅下降，使 SDXL（3.5B）、SSD-1B 等大模型能在有限资源下蒸馏。报告称 LCD 范式「对更大模型适配良好」。
- **超参（报告给出）**：蒸馏时对所有模型固定 CFG ω = 7.5；组合采样用 λ₁=0.8、λ₂=1.0；底模 LCM（teacher 侧）训练成本沿用 ~32 A100 GPU-hours 量级（LCM 原文数字，LCM-LoRA 因只训 LoRA 更省）。
- **免训练组合**：风格 LoRA 与加速 LoRA 的线性叠加是**纯权重空间运算（task arithmetic）**，不做任何梯度更新——这是「universal / training-free」定位的关键。
- **不在本报告范围**：偏好对齐（RLHF/DPO/reward model）等后训练手段 LCM-LoRA **未使用**，它是纯蒸馏加速方法。

## Infra（训练 / 推理工程）
- **训练**：核心卖点是省显存——LoRA 把 SDXL 可训练参数从 3.5B 降到 197M，使大模型蒸馏可在有限 GPU 上完成；本报告**未给出 LCM-LoRA 自身的精确 GPU-时**（仅继承 LCM「~32 A100h」量级，且 LoRA 更省）。训练/微调脚本已随 Diffusers 发布（`examples/consistency_distillation`，含 SD1.5 与 SDXL 两套；训练用 madebyollin 的 fp16 VAE）。
- **推理**：2–8 步采样（推荐 4–6 步）；`guidance_scale` 建议设 1（关 CFG，最快、忽略 negative prompt）或 1–2（启用 negative prompt，>2 失效）。深度集成进 Diffusers（v0.23.0+）：支持 fp16、Apple Silicon `mps`、flash attention、`torch.compile()`、模型 offload、ControlNet / T2I-Adapter / inpainting / img2img 等工作流。社区还支持 ONNX Runtime（C#）、CPU（fastsdcpu）、SD-WebUI、ComfyUI。
- **部署形态**：可插拔权重文件（safetensors LoRA），随用随加载（`load_lora_weights` + `fuse_lora`）；催生了实时（near real-time）视频流 demo。

## 评测 benchmark（把效果讲清楚）
**重要：技术报告本身没有定量质量表（无 FID/CLIP/GenEval 等数字），只给定性图示对比（Fig.2/3）。** 下面的定量数据来自官方 HF 博客（一手源）的**速度基准**，与 LCM 原作的设置：

- **速度（HF 博客，batch size = 1；SDXL 4 步 LCM-LoRA vs SDXL 标准 25 步）**：
  | 硬件 | LCM-LoRA 4 步 | 标准 SDXL 25 步 |
  |---|---|---|
  | Mac M1 Max | 6.5s | 64s |
  | RTX 2080 Ti | 4.7s | 10.2s |
  | RTX 3090 | 1.4s | 7s |
  | RTX 4090 | 0.7s | 3.4s |
  | T4（Colab 免费） | 8.4s | 26.5s |
  | A100 80GB | 1.2s | 3.8s |
  | i9-10980XE CPU（1/36 核） | 29s | 219s |
  即在消费级 GPU 上约 **5–10× 提速**；博客另称 M1 Mac 上 1024×1024 出图从 ~1 分钟降到 ~6s（4 步），4090 近乎实时（<1s）。
- **质量结论（定性，博客 + 报告）**：1 步只出大致形状无纹理；4–6 步通常已令人满意；8 步偏过饱和/卡通化。作为对比，原版 SDXL（Euler 调度）约需 ~20 步才可用、50 步细节最佳——LCM-LoRA 用 4 步逼近其多步质量。
- **泛化性（报告核心实验）**：同一 LCM-LoRA 直接套到 Dreambooth/风格微调模型（如 collage-diffusion、PaperCut LoRA、toy-face LoRA）均能 4 步出图，证明「universal acceleration module」的强泛化。
- **未报告**：FID、CLIPScore、GenEval、T2I-CompBench、HPSv2、ImageReward、PickScore、人评 ELO 等标准生成指标，本工作的一手源**均未提供**——它定位为工程加速模块，质量评估留给定性图示。LCM 原作（arXiv:2310.04378）在 LAION-5B-Aesthetics 上有速度-FID 曲线（768×768、CFG w=8、batch 4、A800），但那是底模 LCM 的数字，非 LCM-LoRA 专属。

## 创新点与影响
**核心贡献**
1. **LoRA 化的一致性蒸馏**：首次把 LCD 套进 LoRA，使 SDXL/SSD-1B 等大模型能在低显存下蒸馏（可训练参数降一个数量级到 67.5M–197M）。
2. **「加速向量」的 task-arithmetic 洞见**：发现 LCM-LoRA 参数是一个可与任意风格 LoRA **线性叠加、免再训练**的通用加速模块——把「神经网络 PF-ODE 求解器」做成即插即用权重。
3. **工程落地**：与 Diffusers 深度集成、训练脚本开源，使「任意 SD 模型 1 秒出图」成为社区标配。

**影响**
- 成为 2023 年底扩散加速的事实标准之一，被 SD-WebUI、ComfyUI、实时画板、Pixart-α×LCM 等广泛集成；直接催生 real-time latent consistency 应用与实时视频流 demo。
- 把「步数蒸馏 + LoRA 可插拔」的范式推向社区，是后续少步/单步加速工作（SDXL-Turbo/ADD、Hyper-SD、LCM 后继、DMD 等对抗/一致性蒸馏路线）的重要参照点。
- 验证了 task arithmetic 在扩散模型权重空间的可行性（加速向量与风格向量正交叠加）。

**已知局限**
- 极少步（1–2 步）质量明显下降；8 步易过饱和。
- 启用 negative prompt 需 guidance_scale∈[1,2]，>2 失效，可控性弱于全步 CFG。
- 质量主要靠定性展示，缺乏标准定量评测，难与同期方法精确横评。
- 组合系数 λ₁/λ₂ 需手调，叠加多个 LoRA 时效果不保证。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2311.05556
- arxiv_pdf: https://arxiv.org/pdf/2311.05556
- hf (sdxl model card): https://huggingface.co/latent-consistency/lcm-lora-sdxl
- hf (sdv1-5 model card): https://huggingface.co/latent-consistency/lcm-lora-sdv1-5
- github / project: https://github.com/luosiallen/latent-consistency-model
- project page: https://latent-consistency-models.github.io
- official HF blog（一等公民，含速度基准）: https://huggingface.co/blog/lcm_lora

## 本地落盘文件
- ../../../sources/omni/2023/arxiv-2311.05556.pdf
- ../../../sources/omni/2023/lcm-lora--hf-sdxl-readme.md
- ../../../sources/omni/2023/lcm-lora--hf-sdv1-5-readme.md
- ../../../sources/omni/2023/lcm-lora--github-readme.md
- ../../../sources/omni/2023/lcm-lora--hf-blog.md
