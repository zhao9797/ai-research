---
title: "Latent Consistency Models (LCM / LCM-LoRA)"
org: "Tsinghua IIIS (+ Hugging Face for LCM-LoRA)"
country: China
date: "2023-10"
type: paper
category: method
tags: [diffusion, distillation, consistency-model, few-step, lora, acceleration, text-to-image, stable-diffusion]
url: "https://arxiv.org/abs/2310.04378"
arxiv: "https://arxiv.org/abs/2310.04378"
pdf_url: "https://arxiv.org/pdf/2310.04378"
github_url: "https://github.com/luosiallen/latent-consistency-model"
hf_url: "https://huggingface.co/SimianLuo/LCM_Dreamshaper_v7"
modelscope_url: ""
project_url: "https://latent-consistency-models.github.io/"
downloaded: [arxiv-2310.04378.pdf, arxiv-2311.05556.pdf, latent-consistency-models--readme.md, latent-consistency-models--project-page.md, lcm-lora--hf-blog.md, lcm-lora--hf-sdxl-readme.md, lcm-lora--hf-sdv1-5-readme.md]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
LCM 把 [[consistency-models]]（Song et al. 2023）从像素空间搬进 Stable Diffusion 的潜空间，提出**一阶段引导一致性蒸馏 + Skipping-Step** 技巧，把一个 768×768 的 2~4 步高清生成模型**只用 32 张 A100 卡时（4000 步）**蒸馏出来；后续技术报告 **LCM-LoRA** 把蒸馏结果固化为一个**即插即用、免训练**的「神经 PF-ODE 求解器」LoRA，可叠加到任意 SD/SDXL 微调模型与风格 LoRA 上——在 4090 上让 SDXL 从 ~3.4s（25 步）降到 **0.7s（4 步）**，成为整个开源生图生态的通用加速器。

## 背景与定位
扩散模型（[[ddpm]]、[[latent-diffusion-ldm]]/Stable Diffusion）质量极高，但**反向迭代采样慢**，实时应用受限。加速路线两类：
1. **训练自由的 ODE 求解器**：DDIM、[[dpm-solver]]/DPM-Solver++，能压到 10~20 步，但配合 CFG 时每步要算两次前向、峰值显存大；
2. **蒸馏**：Progressive Distillation（Salimans & Ho 2022）、Guided-Distill（Meng et al. 2023）。Guided-Distill 用**两阶段**蒸馏支持引导扩散的少步采样，但计算极贵（论文引用估计 2 步推理需 ~45 A100·天），且两阶段误差累积。

Song et al. 2023 的 **Consistency Models (CMs)** 学一个把 PF-ODE 轨迹上任意点映射回轨迹原点的「一致性函数」，可单步生成，但**只做了像素空间的 ImageNet 64×64 / LSUN 256×256**，没探索高分辨率文生图，也**没纳入 CFG**。

LCM 的定位就是补上这两块：把 CM 放进潜空间做高清文生图，并把 CFG 直接吸进蒸馏。作者是清华叉院 Simian Luo / Yiqin Tan 等（导师 Longbo Huang、Jian Li、Hang Zhao）。

## 模型架构
- **不引入新网络结构**：LCM 直接复用教师 LDM（Stable Diffusion）的 **U-Net + VAE 编解码器 + 文本编码器（CLIP）**，权重用教师初始化。整篇方法是「在已有 SD 上做的蒸馏 + 重参数化」，而非新 backbone。
- **潜空间一致性函数**：先用 SD 的自编码器 `E` 把图像压成潜向量 `z=E(x)`，在潜空间定义一致性函数 `f_θ:(z_t, c, t) → z_0`，直接预测 PF-ODE 在 `t=0` 的解。
- **一致性参数化（ε-Prediction）**：`f_θ(z,c,t)=c_skip(t)·z + c_out(t)·((z − σ_t·ε̂_θ(z,c,t))/α_t)`，其中 `c_skip(0)=1, c_out(0)=0` 保证边界条件 `f_θ(z,0)=z`；`ε̂_θ` 用教师噪声预测网络初始化。也可按教师的 x/ε/v 预测方式换参数化（附录 D）。
- **CFG 注入：增广一致性函数**。把 CFG 尺度 ω 作为额外条件喂进网络——`f_θ:(z_t, ω, c, t) → z_0`，`ε̂_θ(z,c,t)` 改成 `ε̂_θ(z,ω,c,t)`，并为 ω 增加少量可训练条件参数。这样把「引导」直接蒸进模型输入，推理时不再需要跑两次前向（条件+无条件），**每步只一次前向**，省时省显存。
- **参数量/分辨率**：教师为 SD-V2.1-Base（512）与 SD-V2.1（768），LCM 与教师同规模（~0.9B U-Net）。LCM-LoRA 阶段扩展到 SD-V1.5、SSD-1B（1.3B）、SDXL（3.5B）。

## 数据
- **文生图训练集**：LAION-5B（Schuhmann et al. 2022）的两个美学子集——
  - 512 分辨率：**LAION-Aesthetics-6+，约 12M** 图文对（美学分 >6）；
  - 768 分辨率：**LAION-Aesthetics-6.5+，约 650K** 图文对（美学分 >6.5）。
- **下游微调（LCF）数据**：Pokemon（lambdalabs，BLIP captions）与 Simpsons（Norod78）两个定制小数据集，各数百条图文对，90% 微调 / 10% 测试。
- 蒸馏不需要重新爬数据/重做 caption——直接复用教师 SD 见过的分布，数据处理细节（清洗/再标注/安全过滤）未在论文额外披露（沿用 LAION 原始标注）。

## 训练方法
**核心训练目标：潜空间一致性蒸馏（Latent Consistency Distillation, LCD）。**
- 损失：`L = E[d(f_θ(z_{t_{n+k}}, ω, c, t_{n+k}), f_{θ⁻}(ẑ^{Ψ,ω}_{t_n}, ω, c, t_n))]`，`d` 取平方 ℓ2；目标网络 `θ⁻` 用 EMA 更新（`θ⁻ ← μθ⁻ + (1−μ)θ`）。
- **一阶段引导蒸馏（解增广 PF-ODE）**：把 CFG 的 `ε̃_θ=(1+ω)ε_θ(z,c,t) − ω·ε_θ(z,∅,t)` 代入 PF-ODE 形成「增广 PF-ODE」，训练时对 `ω∈[ω_min,ω_max]` 均匀采样；ODE 一步估计写成 `ẑ ≈ (1+ω)·Ψ(·,c) − ω·Ψ(·,∅)`。相比 Guided-Distill 的两阶段，**只需一阶段**，更简单、误差不累积。
- **Skipping-Step（关键加速 trick）**：SD 离散时间表长达 1000 步，相邻 `t_n, t_{n+1}` 太近导致一致性损失太小、收敛极慢。LCM 改成约束「**当前步与 k 步之外**」的一致性 `t_{n+k} → t_n`，把时间表从上千压到几十。`k=1` 退化为原 CM（慢）；`k` 过大则 ODE 求解误差变大。主实验取 **k=20**，4 步设定下 2000 步内即收敛。
- **训练用 ODE 求解器 Ψ**：DDIM / DPM-Solver / DPM-Solver++（仅用于蒸馏估计，**不用于推理**）。主实验用 DDIM-Solver + k=20。
- **关键超参**：512 设定 batch=72，768 设定 batch=16；学习率 8e-6；EMA `μ=0.999943`；CFG 范围 `[ω_min,ω_max]=[2,14]`；训练 100K 迭代（teaser 中 Dreamshaper-V7 仅 4000 步 ≈ 32 A100 卡时即可出高质量 2~4 步模型）。
- **Latent Consistency Fine-tuning (LCF)**：受 Consistency Training 启发，让预训练 LCM **不依赖教师扩散模型**就能在定制数据集上微调并保持少步推理（Pokemon/Simpsons 各微调 30K 迭代，lr 8e-6）。

**LCM-LoRA（2311.05556 技术报告，与 Hugging Face 合作）——把方法工程化为通用加速器：**
- **LoRA 蒸馏**：把上面的 LCD 当作对扩散模型的一次微调，用 LoRA（`W0+BA`，仅训练低秩 A、B）做蒸馏。可训练参数大幅下降——SD-V1.5 0.98B→**67.5M**、SSD-1B 1.3B→**105M**、SDXL 3.5B→**197M**，显存够低才得以蒸 SDXL/SSD-1B 这类大模型。蒸 SDXL 用固定 ω=7.5。
- **「加速向量」即插即用（任务算术）**：把蒸出来的 LoRA 记为「加速向量」`τ_LCM = θ_LCM − θ_base`，把任意风格微调 LoRA 记为「风格向量」`τ′`。**无需任何额外训练**，直接线性组合 `τ′_LCM = λ1·τ′ + λ2·τ_LCM`（实践 λ1=0.8, λ2=1.0）叠到底模上，就得到「该风格 + 少步加速」的模型。作者将其解释为一类**基于神经网络的、可泛化的 PF-ODE 求解器模块**，对各种 SD 微调模型/LoRA 通用。

## Infra（训练 / 推理工程）
- **训练算力极低**：一个 768×768 的 2~4 步 LCM 仅 **~32 A100 GPU 小时**（4000 步）；对比 Guided-Distill 2 步推理估计需 ~45 A100·天，省两个数量级。
- **推理加速来源**：(1) 步数从 25~50 砍到 **1~8（推荐 4）**；(2) CFG 蒸进输入，每步**只一次 U-Net 前向**（而非条件/无条件两次），省时省峰值显存；(3) LCM-LoRA 免训练即可加速任意底模。
- **部署形态**：官方上线 `LCMScheduler` + `LatentConsistencyModelPipeline` 进入 🧨 Diffusers（v0.22+；LCM-LoRA 需 v0.23+），并迅速被 ComfyUI / SD-WebUI / ONNX Runtime（C#）/ CPU（fastsdcpu）/ Real-Time LCM / Colab 等社区集成。LCM-LoRA 用法：加载 base + `load_lora_weights` + `fuse_lora`，`guidance_scale` 设 0~2，4 步出图（支持 inpainting、叠 ControlNet、叠风格 LoRA）。
- 未披露：具体并行/混合精度训练吞吐、训练框架细节。

## 评测 benchmark（把效果讲清楚）
**LCM 主论文（ω=8，CLIP 用 ViT-g/14，30K 图 / 10K prompt）：**

512×512（LAION-Aesthetic-6+，FID↓ / CLIP↑，1/2/4/8 步）：

| 方法 | FID 1步 | FID 2步 | FID 4步 | FID 8步 | CLIP 4步 | CLIP 8步 |
|---|---|---|---|---|---|---|
| DDIM | 183.29 | 81.05 | 22.38 | 13.83 | 25.89 | 29.29 |
| DPM++ | 185.78 | 72.81 | 18.43 | 12.20 | 26.64 | 29.55 |
| Guided-Distill | 108.21 | 33.25 | 15.12 | 13.89 | 27.25 | 28.17 |
| **LCM (Ours)** | **35.36** | **13.31** | **11.10** | 11.84 | **28.69** | 28.84 |

768×768（LAION-Aesthetic-6.5+）：LCM 4 步 **FID 13.53 / CLIP 28.60**，1 步 FID 34.22 / CLIP 25.32；同区间 DDIM 4 步 FID 24.28、Guided-Distill 4 步 FID 16.70——LCM 在 **1~4 步低步数区间大幅领先**。

**消融（论文 Fig 3/4）：**
- **Skipping-Step**：k=1（原 CM）收敛极慢；k=5/10/20 收敛快很多；DDIM 在大 k 误差变大、DPM/DPM++ 在 k=50 反而更好；折中取 k=20。
- **CFG 尺度 ω**：ω 越大 CLIP（质量）越好但 FID（多样性）变差；**2/4/8 步之间差距极小**，仅 1 步明显有 gap，说明 LCM 在 2~8 步区间稳。

**LCM-LoRA 真实墙钟（HF 官方博客，batch=1）：**

| 硬件 | SDXL + LCM-LoRA（4 步） | SDXL 标准（25 步） |
|---|---|---|
| 2080 Ti | 4.7s | 10.2s |
| 4090 | **0.7s** | 3.4s |
| A100(80G) | 1.2s | 3.8s |

博客补充：M1 Mac 上 SDXL 从 ~1 分钟降到 ~6s（4 步，~10×）；LCM-LoRA 质量在 4~6 步通常已很满意；标准 SDXL 要到 ~20 步才可用、50 步才出最佳细节。LCM-LoRA 论文本身**未给定量 FID/CLIP 表**，主要靠定性图与上述墙钟数据论证泛化性（文中如实标注）。

## 创新点与影响
**核心贡献：**
1. 首次把一致性模型搬到**潜空间 + 高清文生图**，实现 SD 的 2~4 步（甚至 1 步）采样；
2. **一阶段引导一致性蒸馏**，把 CFG 直接蒸进模型输入，取代昂贵的两阶段 Guided-Distill，且每步单次前向；
3. **Skipping-Step** 把离散时间表从上千压到几十，是快速收敛的关键；
4. **LCF** 让 LCM 不靠教师即可在定制数据集少步微调；
5. **LCM-LoRA**：把蒸馏结果固化为「加速向量」，借任务算术**免训练**叠到任意 SD/SDXL 微调模型与风格 LoRA 上——一类可泛化的「神经 PF-ODE 求解器」。

**影响：** LCM/LCM-LoRA 成为 2023 年底开源生图生态的**通用加速插件**，被 Diffusers/ComfyUI/SD-WebUI 等迅速原生集成，催生 Real-Time LCM、PixArt-α×LCM 等实时/低延迟应用，并直接推动了后续少步蒸馏研究线（与 [[sdxl-turbo-add|SDXL-Turbo (ADD)]]、[[dmd|DMD]]、后来的 LCM 改进版如 Hyper-SD / PCM 等同属一脉）。其「LoRA = 可叠加加速器」的范式深刻影响了开源社区的部署习惯。

**已知局限：**
- **1 步质量仍有明显 gap**（论文坦承一步存在改进空间）；
- 大 ω 时多样性（FID）下降，质量/多样性需权衡；
- LCM-LoRA 叠加 λ1/λ2 是手调超参，组合质量依赖调参；
- 论文将编辑/inpainting/超分等列为未来工作（后由社区 + LCM-LoRA inpainting 补上）。

## 原始链接
- arxiv_abs (LCM): https://arxiv.org/abs/2310.04378
- arxiv_pdf (LCM): https://arxiv.org/pdf/2310.04378
- arxiv (LCM-LoRA 技术报告): https://arxiv.org/abs/2311.05556
- github: https://github.com/luosiallen/latent-consistency-model
- project_page: https://latent-consistency-models.github.io/
- hf_blog (LCM-LoRA, 一手): https://huggingface.co/blog/lcm_lora
- hf_model (LCM Dreamshaper v7): https://huggingface.co/SimianLuo/LCM_Dreamshaper_v7
- hf_model (lcm-lora-sdxl): https://huggingface.co/latent-consistency/lcm-lora-sdxl
- hf_model (lcm-lora-sdv1-5): https://huggingface.co/latent-consistency/lcm-lora-sdv1-5

## 一手源存档（sources/）
- [arxiv-2310.04378.pdf](https://arxiv.org/pdf/2310.04378)  （arXiv 原文 PDF，不入 git）
- [arxiv-2311.05556.pdf](https://arxiv.org/pdf/2311.05556)  （arXiv 原文 PDF，不入 git）
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/latent-consistency-models--readme.md)
- [project-page.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/latent-consistency-models--project-page.md)
- [lcm-lora--hf-blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/lcm-lora--hf-blog.md)
- [lcm-lora--hf-sdxl-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/lcm-lora--hf-sdxl-readme.md)
- [lcm-lora--hf-sdv1-5-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/lcm-lora--hf-sdv1-5-readme.md)
