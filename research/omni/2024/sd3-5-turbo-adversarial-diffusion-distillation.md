---
title: "SD3.5 Large Turbo 与 (Latent) Adversarial Diffusion Distillation"
org: Stability AI
country: EU
date: "2024-10"
type: paper
category: method
tags: [distillation, adversarial, few-step, mmdit, rectified-flow, turbo, gan, text-to-image]
url: https://stability.ai/news/introducing-stable-diffusion-3-5
arxiv: https://arxiv.org/abs/2403.12015
pdf_url: https://arxiv.org/pdf/2403.12015
github_url: https://github.com/Stability-AI/sd3.5
hf_url: https://huggingface.co/stabilityai/stable-diffusion-3.5-large-turbo
modelscope_url:
project_url: https://stability.ai/research/adversarial-diffusion-distillation
downloaded: [arxiv-2403.12015.pdf, arxiv-2311.17042.pdf, sd3-5--blog.md, sd3-5-turbo--hf-page.md, sd3-5--github-readme.md, sd3-5--sd3_infer.py]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Stability AI 的对抗式扩散蒸馏家族——先有 **ADD**（pixel 域，DINOv2 判别器，把 SDXL 蒸成 1 步的 SDXL-Turbo），再有 **LADD（Latent ADD）**（latent 域，用扩散教师自身特征做判别器，把 8B 的 SD3 蒸成 4 步的 SD3-Turbo），最终工程化落地为开源产品 **SD3.5 Large Turbo**（8.1B MMDiT，ADD 蒸馏，4 步、`guidance_scale=0`/无 CFG，euler 采样，质量逼近 50 步教师）。核心结果：SD3-Turbo 用 **4 步**即可在人评中匹配其 50 步教师 SD3 的图像质量，并击败 Midjourney v6 等强基线。

## 背景与定位
扩散模型迭代去噪的本质要求数十次网络评估，对 8B 级大模型而言推理慢、难实时。加速一条主线是少步/单步蒸馏：渐进蒸馏（Progressive Distillation，误差累积、需 5+ 轮）、Reflow（合成数据迭代、同样累积误差）、一致性蒸馏 LCM（单阶段但训练不稳、需蒸馏调度与大量调参）。当时少步区间最优的是**对抗训练**类方法。

- **ADD（[[adversarial-diffusion-distillation-add]]，arXiv 2311.17042，2023.11）**：用预训练 **DINOv2** 特征网络当判别器骨干（Projected GAN 范式），把 SDXL 蒸成单步实时 T2I 模型。是「首个用 foundation model 实现单步实时合成」的方法，但有三大短板：① DINOv2 固定且仅在 518×518 像素预训练，限制判别器分辨率；② 无法方便地调节判别器反馈层级（全局形状 vs 局部纹理）；③ 蒸馏 LDM 时必须解码回 RGB 像素空间施加判别器，严重阻碍 >512² 的高分辨率训练。此外对抗模型不遵循 scaling law、训练需大量调参，更大判别器反而常更差，不利于规模化。
- **LADD（本页主角，arXiv 2403.12015，2024.03）**：把对抗蒸馏整体搬进 **latent 空间**，用预训练**扩散模型（教师）自身的生成式特征**替代 DINOv2 判别特征，从而支持多宽高比（MAR）、百万像素、可控反馈层级，且训练更简单、可规模化，把 SD3（8B）蒸成 SD3-Turbo。
- **产品化（SD3.5，2024.10.22）**：开源发布 SD3.5 Large（8.1B 基座）、**SD3.5 Large Turbo**（ADD 蒸馏、4 步）、SD3.5 Medium（2.5B，MMDiT-X）。Turbo 是 ADD 蒸馏方法在 SD3.5 Large 上的工程落地，使「少步实时出图」可在消费级硬件上跑。

技术脉络：[[ddpm]]/[[latent-diffusion-ldm]] → [[sdxl]] → [[stable-diffusion-3]]（rectified flow + MMDiT）→ **ADD（SDXL-Turbo）→ LADD（SD3-Turbo）→ SD3.5 Large Turbo**；可与 [[latent-consistency-models]]、[[flux-1-schnell]] 等少步方案对照。

## 模型架构
**学生/教师 backbone**：SD3-Turbo 与 SD3.5 Large Turbo 都基于 **MMDiT（Multimodal Diffusion Transformer，[[stable-diffusion-3]]）**，并非 U-Net；学生由教师权重初始化，蒸馏前后 backbone 同构。
- **SD3.5 Large Turbo**：由 SD3.5 Large 蒸馏而来、与之同构（ADD 蒸馏不改 backbone），故参数量同为 **8.1B**（官方仅对 SD3.5 Large 直接标注 8.1B / 1 兆像素；Turbo 数字属同构推断）。三个固定预训练文本编码器（OpenAI **CLIP-L/14** + OpenCLIP **bigG** + Google **T5-XXL**，CLIP context length 77、T5 训练分阶段用 77/256），引入 **QK-Normalization**（Query-Key 归一化）稳定训练并便于下游微调；16 通道 VAE 解码器（无 postquantconv step，github README 明确）。
- **LADD 论文默认实验模型**：depth=24 的 MMDiT（约 2B 参数）用于消融，最终大模型为 8B（即 SD3 8B）。

**ADD 判别器（pixel 域，原 ADD）**：Projected GAN 范式——固定预训练 **DINOv2 ViT** 作特征网络（默认 ViT-S 最佳），在其不同层特征 Fk 上挂多个轻量判别器头 Dϕ,k；判别器经投影（projection）额外条件于文本嵌入 ctext 与图像的 DINOv2 CLS 嵌入；训练分辨率受 DINOv2 限制在 518×518/512×512。

**LADD 判别器（latent 域，关键创新）**：抛弃 DINOv2，**把教师扩散模型本身当判别器特征网络**——
- 学生生成 latent 后，按 logit-normal 分布在时间步 t̂ 重新加噪（renoise），送入**教师模型**，取每个 attention block 之后的完整 token 序列；
- 在每个 token 序列上挂**独立判别器头**，每个头额外条件于**噪声水平**与 **pooled CLIP 嵌入**；
- 判别器头由 1D 卷积改为 **2D 卷积**：把 token 序列 reshape 回原始空间布局再卷，避免 MAR 设定下 1D 判别器对不同宽高比处理不同 stride 的问题。

用生成式特征的四点收益（论文明确论证）：① 效率——免去解码回像素空间，省显存、简化系统；② **噪声层级可控反馈**——高噪声给全局结构反馈、低噪声给纹理反馈，通过调节噪声采样分布即可直接控制判别器行为；③ 天然支持 **MAR**（教师本就在 MAR 数据上训练）；④ 更贴近人类感知——生成式模型具形状偏好（shape bias），而判别式网络偏纹理。

## 数据
**ADD（原）**：蒸馏 SDXL-Base，使用其训练数据；判别器看真实图像 x0 与学生生成图。

**LADD（核心方法转变）——全合成数据**：
- 关键洞见：自然数据集图文对齐度差异大（COCO 平均 CLIP score 0.29，而 SD3 在 COCO prompts 上可达 0.35），说明生成图平均图文对齐更好。
- 因此 LADD **用教师模型在固定 CFG 值下生成合成 latent 作训练数据**（prompt 采样自 SD3 原始训练集），既保证高且均匀的图文对齐，又可视作蒸馏教师知识的另一种途径。
- 由于在 latent 域训练，可直接由教师生成 latent，**省去对真实数据的编码步骤**。
- 消融结论：合成数据训练**显著优于**真实数据；真实数据下加蒸馏损失有益，但合成数据下蒸馏损失变得多余（仅对抗损失即可）。

SD3.5 Large Turbo 的具体训练语料/规模/清洗配比官方未单独披露（蒸馏继承自 SD3.5 Large 基座，基座数据细节亦未在本批一手源充分公开）→ **未披露**。

## 训练方法
**教师扩散公式**：rectified flow（αt=1−t, σt=t, t∈[0,1]），denoiser D(xt,t)=xt − t·Fθ(xt,t)，score matching 训练。

**ADD（原）双目标**：
- 对抗损失 Ladv：学生欺骗 DINOv2-Projected-GAN 判别器，用 **hinge loss**，判别器加 **R1 梯度惩罚**（在每个判别器头输入上计算，强度 γ）；
- 蒸馏损失 Ldistill：把学生样本 x̂θ 按教师前向过程扩散到 x̂θ,t，用教师去噪预测 x̂ψ(x̂θ,t,t) 作目标（即 score distillation sampling/SDS 思路），距离用 L2 `d(x,y)=‖x−y‖²`；权重 c(t) 论文给两档：**exponential weighting `c(t)=αt`**（高噪声贡献更小，消融默认）与 **SDS weighting**，论文证明取 L2 距离 + 特定 c(t) 时 Ldistill 等价于 SDS 目标；消融最终模型实际用 **NFSD weighting**。蒸馏权重 λ=2.5，R1 强度 γ=10⁻⁵。
- 默认训练设置：DINOv2 **ViT-S** 特征网络、文本+图像条件判别器、预训练学生权重、单教师步、**4000 iterations、batch size 128、512×512**（论文 Table 1 caption 明确）。论文报告的 A100/混合精度仅指 Fig.7 的**推理速度**测量，**训练硬件未披露**。

**LADD（简化）**：
- **统一判别器与教师**：不再解码到像素、不再用外部 DINOv2，纯 latent 域，对教师特征施加 Projected GAN 损失；
- **仅对抗损失**（合成数据下丢弃 Ldistill）；
- 教师噪声分布用 logit-normal π(t; m=1, s=1)（偏高噪声改善全局一致性，过高则丢细节）；
- 默认训练 **10k iterations**；
- **多步推理训练**：在 4 个离散时间步 t∈[1, 0.75, 0.5, 0.25] 上训练，混合「全噪声 + 部分噪声」输入以支持多步；高分辨率（>512²）需 warm-up——前 500 iter 初始概率 p=[0,0,0.5,0.5]（偏低噪声），之后转 p=[0.7,0.1,0.1,0.1] 偏全噪声以精炼单步性能；MAR 用 binning 策略。
- **偏好对齐 DPO**：用 **Diffusion-DPO** 对教师注入 rank-256 LoRA 微调 3k iter，再用 DPO 后的模型做 LADD 的学生/教师/数据生成；有趣的是，LADD 训练后**重新套用原 DPO-LoRA 矩阵**可进一步提升——单步下对非-DPO LADD 学生取得 **56% 人评胜率**，多步下提升更明显（修手、去重复物体、增细节）。

**采样器**：2/4 步用一致性采样器（flow consistency sampler，源自 Consistency Models）。SD3.5 Large Turbo 官方默认：`shift=3.0, cfg=1.0（即无 CFG）, steps=4, sampler=euler`（来自 GitHub `sd3_infer.py` CONFIGS）；Diffusers 示例 `num_inference_steps=4, guidance_scale=0.0`。

**蒸馏能扩展到 image-to-image**：先用扩散目标在对应任务数据上继续训练教师，得 SD3-edit（depth=24）/SD3-inpainting（depth=18），再用 LADD 蒸馏 → SD3-edit Turbo / SD3-inpainting Turbo，单步即匹配 50 步教师。

## Infra（训练 / 推理工程）
- **ADD**：训练分辨率 512×512、batch 128、4000 iter（论文 Table 1 caption 明确）；训练用 GPU 数/卡时论文未披露（论文仅在 Fig.7 报告单样本 512² 推理速度走 A100、混合精度）→ 训练 infra **未披露**。
- **LADD**：latent 域训练**避免解码到像素**，显著降低显存、可用大学生+大教师；10k iter；具体 GPU 数/卡时未单独披露 → **未披露**。
- **推理加速形态**：步数从 50 步降至 **4 步（或 1 步）**、关闭 CFG（无需 unconditional 分支，进一步省一半算力）；SD3.5 系列支持消费级硬件（官方称 SD3.5 Medium 仅需 9.9 GB VRAM，不含文本编码器）；Diffusers 支持 bf16。
- **Scaling 结论（资源分配指导）**：在 student/teacher/data-generator 三维中，**学生模型大小影响最大**，教师与数据质量收益会饱和（递减）——故显存受限时应优先放大学生、可用较小教师而几乎不掉点。这是 LADD 相对 ADD 的重要工程价值：对抗蒸馏在此设定下表现出可预测的 scaling 行为。

## 评测 benchmark（把效果讲清楚）
方法论：T2I 主要用**人评 user preference study**（图像质量 + 图文对齐双维），并用 DrawBench/PartiPrompts 上的 CLIP score（ViT-g-14）做消融指标。

**SD3-Turbo（LADD，主结果，均为人评胜率/偏好对比，非绝对分）**：
- 单步设定：SD3-Turbo 在图像质量与图文对齐两项上**明显优于**所有基线。
- 4 步设定：**图像质量匹配其 50 步教师 SD3**（4 步 vs 50 步），图文对齐相对 SD3 略降，但仍**击败 Midjourney v6** 等强基线；与 SDXL-Turbo（下采样到 512²对比）等亦优或持平。
- DPO 消融：单步下 DPO-LADD 学生对非-DPO 学生 **56% 胜率**。
- LADD vs LCM 消融：同一 depth=24 学生，LADD **单步大幅优于 LCM**；LCM 需对 skipping-step/噪声调度/全微调-vs-LoRA 做网格搜索并挑最佳 ckpt，LADD 只训一次取末尾 ckpt 即可，volatility 远低。
- Scaling 消融：学生 depth 是性能主因，教师/数据质量收益饱和。

**Image-to-image 定量（LADD 论文 Fig.13）**：
- 编辑（PIE-Bench，CLIP image-sim vs CLIP direction-sim）：**SD3-edit Turbo 单步匹配 50 步教师 SD3-edit**，代价是失去图像/文本引导强度的可调性。
- 修复 inpainting（COCO，FID↓ / LPIPS↓）：LaMa 27.21 / 0.3137；SD1.5-inpainting 10.29 / 0.3879；**SD3-inpainting 8.94 / 0.3465**（教师，50 步 guidance 4）；**SD3-inpainting Turbo 9.44 / 0.3416**（学生，单步）——学生单步基本持平教师；LaMa 虽 LPIPS 最低但 FID 高、大面积非均匀遮挡时明显变差。

**原 ADD（SDXL-Turbo，arXiv 2311.17042）人评**：ADD-XL 单步胜过 LCM/LCM-XL 与单步 GAN 等所有少步基线，单步除 SDXL 外优于其余对手；**4 步 ADD-XL 在人评中胜过包括其教师 SDXL 1.0（base，无 refiner）在内的所有模型**。

**SD3.5 产品页（官方相对结论，未给绝对数字）**：SD3.5 Large 在 prompt adherence 上领先市场、图像质量比肩更大模型；**SD3.5 Large Turbo 在同尺寸里提供最快推理之一，质量/对齐即便对比同尺寸非蒸馏模型也很有竞争力**。FID/GenEval/T2I-CompBench/DPG/MJHQ-30K/HPSv2/ImageReward/PickScore 等标准 benchmark 的绝对数字官方一手源**未报告**（本批源仅给人评相对胜率与 inpainting FID/LPIPS）。

## 创新点与影响
**核心贡献**：
1. **ADD**：首个用预训练 foundation 特征网络（DINOv2）实现 foundation 扩散模型单步实时合成的方法；adversarial loss + score distillation 混合目标。
2. **LADD**：把对抗蒸馏整体移入 latent 域，**用扩散教师自身特征当判别器**——消除像素解码、天然支持 MAR/百万像素、通过噪声采样分布控制判别器全局/局部反馈、对抗蒸馏首次表现出可预测的 scaling，训练比 ADD 更简单且超越之；统一了「教师+判别器+数据生成器」三角，并证明全合成数据可丢弃蒸馏损失。
3. **方法通用性**：同一蒸馏框架直接迁移到 instruction-based editing 与 inpainting，单步匹配 50 步教师。
4. **产品化**：作为 SD3.5 Large Turbo 落地，把 8.1B 模型的少步实时出图带到开源+消费级硬件。

**影响**：确立「对抗蒸馏 > 一致性蒸馏」在 DiT/MMDiT 少步区间的实践优势；为后续 FLUX.1-schnell、各家 Turbo/Lightning/Hyper 系少步模型提供方法参照；DPO-LoRA「先对齐教师、蒸馏后再叠加」的技巧具迁移价值。

**已知局限**：
- 少步换来 prompt alignment 下降——物体合并/重复、细粒度空间描述、否定（negation）理解变差（教师 SD3 本身也有，但 Turbo 更明显）。
- 编辑任务**失去图像/文本引导强度的可调性**（学生不支持 nested CFG 的 trade-off 控制）。
- 模型有时过度贴合输入（rigidity），大幅修改困难。
- 关闭 CFG + 高 seed 方差：相同 prompt 不同 seed 输出差异大（SD3.5 刻意保留以维持知识广度），prompt 不具体时不确定性上升、美学水平波动。

## 原始链接
- blog（SD3.5 发布，含 Large Turbo 定位）: https://stability.ai/news/introducing-stable-diffusion-3-5
- paper（LADD / SD3-Turbo）: https://arxiv.org/abs/2403.12015 ; PDF https://arxiv.org/pdf/2403.12015
- paper（原 ADD / SDXL-Turbo）: https://arxiv.org/abs/2311.17042
- 方法技术报告页（ADD）: https://stability.ai/research/adversarial-diffusion-distillation
- hf model card（SD3.5 Large Turbo，gated，cloakbrowser 抓取）: https://huggingface.co/stabilityai/stable-diffusion-3.5-large-turbo
- github（推理代码，含 Turbo 默认 CONFIGS）: https://github.com/Stability-AI/sd3.5

## 一手源存档（sources/）
- [arxiv-2403.12015.pdf](https://arxiv.org/pdf/2403.12015)  （LADD / SD3-Turbo 论文）  （arXiv 原文 PDF，不入 git）
- [arxiv-2311.17042.pdf](https://arxiv.org/pdf/2311.17042)  （原 ADD / SDXL-Turbo 论文）  （arXiv 原文 PDF，不入 git）
- [sd3-5--blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/sd3-5--blog.md)  （SD3.5 发布博客）
- [sd3-5-turbo--hf-page.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/sd3-5-turbo--hf-page.md)  （SD3.5 Large Turbo HF model card，cloakbrowser 快照）
- [sd3-5--github-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/sd3-5--github-readme.md)  （SD3.5 推理仓库 README）
- [sd3-5--sd3_infer.py](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/sd3-5--sd3_infer.py)  （SD3.5 推理脚本，含 CONFIGS 的 Turbo 默认 shift/cfg/steps/sampler）
