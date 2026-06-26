---
title: "Diffusion-DPO: Diffusion Model Alignment Using Direct Preference Optimization"
org: "Salesforce AI / Stanford University"
country: US
date: "2023-11"
type: paper
category: method
tags: [diffusion, dpo, alignment, rlhf, preference-optimization, sdxl, text-to-image]
url: "https://arxiv.org/abs/2311.12908"
arxiv: "https://arxiv.org/abs/2311.12908"
pdf_url: "https://arxiv.org/pdf/2311.12908"
github_url: "https://github.com/SalesforceAIResearch/DiffusionDPO"
hf_url: "https://huggingface.co/mhdang/dpo-sdxl-text2image-v1"
modelscope_url: ""
project_url: ""
downloaded: [arxiv-2311.12908.pdf, diffusion-dpo--readme.md, diffusion-dpo--hf-sdxl-card.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Diffusion-DPO 把语言模型的 [[dpo]]（Direct Preference Optimization）首次推广到扩散模型，用 ELBO 重写偏好似然，得到一条只需"赢/输两张图各加一次噪声做 ε-预测"的可微闭式损失；在 Pick-a-Pic v2 的 85.1 万对人类偏好上微调 SDXL-1.0 base，人评 General Preference 胜率 **70.0%**（vs SDXL-base，PartiPrompts），并以 3.5B 参数击败 6.6B 的 SDXL(base+refiner) 完整管线（胜率 **69%**），成为 t2i 偏好对齐的主流方法之一。

## 背景与定位
LLM 走的是"预训练 → 对齐（SFT + RLHF）"两段式，而 2023 年的 t2i 扩散模型（[[latent-diffusion-ldm]]、SD、[[sdxl]]）几乎都是单阶段扩散目标训练，最多在高美学子集（laion-aesthetics）或精挑细选的数据（Emu）上做一次有监督微调来"偏置"生成分布——这远不如 LLM 的最终对齐阶段灵活、强大。

当时已有的扩散对齐方法各有硬伤（论文 Tab.1 自我定位）：
- **RL 类（DPOK、DDPO）**：只在小词表（<10 / <1000 prompt）有效，开放词表下退化；DDPO 无 KL 正则、靠 early-stop 控分布。作者复现 DDPO 在 Pick-a-Pic 上未能稳定提升 PickScore。
- **奖励回传类（DRaFT、AlignProp）**：把奖励模型梯度直接回传到扩散链，过训会 mode collapse，且只能优化可微奖励；DRaFT 明确报告无法用 CLIP 提升图文对齐。
- **推理期优化（DOODL）**：不学新参数，但单次推理成本上升一个数量级以上。

Diffusion-DPO 是唯一同时满足 **开放词表泛化 + 推理成本不变 + 有分布控制（β）+ 能提升通用图文对齐**的方法。技术血缘上它继承 [[ddpm]]/[[latent-diffusion-ldm]] 的扩散框架与 Rafailov 等的 LLM-DPO，把"reparameterize 奖励 → 直接对策略做二分类"的思路搬到扩散链。

## 模型架构
Diffusion-DPO 是**训练方法（method），不引入新架构**，直接复用被对齐模型的全部组件：
- **Backbone**：[[sdxl]]-1.0 base 的 U-Net（latent diffusion，3.5B 参数；完整 SDXL 含 refiner 共 6.6B）以及 SD1.5 的 U-Net；在各自原生分辨率训练（SD1.5 默认 512²，SDXL 默认 1024² 方形）。
- **VAE / text encoder / 条件注入**：沿用底模——SDXL 用双 CLIP text encoder（OpenCLIP ViT-bigG + CLIP ViT-L）+ size/crop 条件，SD1.5 用 CLIP ViT-L；均为 latent 空间扩散。Diffusion-DPO 不改这些模块。
- **关键设计**：训练时同时持有**可训练策略 ε_θ** 与**冻结参考模型 ε_ref**（用底模初始化两者，ref 不更新），损失对比两者在赢/输样本上的去噪误差差。推理期与底模完全一致，**零额外推理开销**（这是相对 DOODL 的核心优势）。
- **AI-feedback 变体**用到的打分网络：PickScore、HPSv2、CLIP（OpenCLIP ViT-H/14）、LAION Aesthetic Predictor——它们只用于离线给图对排序，不进入生成架构。

## 数据
- **主数据集**：**Pick-a-Pic v2**（Kirstain et al. 2023），来自 Pick-a-Pic 网页应用的众包成对偏好。图像由 SDXL-beta 与 Dreamlike（SD1.5 微调版）生成，prompt 与偏好均来自真实用户。
- **规模与清洗**：剔除约 **12% 的平局对**后，得到 **851,293 对**偏好、**58,960 个唯一 prompt**。每对为 (prompt c, 赢图 x_0^w, 输图 x_0^l)。
- **数据质量观察（5.5 节）**：尽管 SDXL-1.0 底模本身已优于训练数据中的图（连"赢图 y_w"按 PickScore 也不如 SDXL），DPO 仍能显著提升——即在**分布外（OOD）偏好数据**上也有效。对 Dreamlike 用其自生成的 15% 子集做"分布内"训练也能提升，但因子集小提升有限。
- **合成/AI 标注数据（5.4 节）**：用 PickScore 给 Pick-a-Pic 图对**伪标注**（pseudo-labeling，作者视作一种数据清洗），训练效果**反超原始人工标签**——PartiPrompt General Preference 胜率从 59.8% 升到 63.3%。
- **伦理与安全**：作者明确指出 Pick-a-Pic 含露骨内容与对女性的过度性化倾向，承诺在加入安全过滤前不开源模型；未披露专门的美学/NSFW 过滤管线细节（数据过滤"可行但未在本文实施"）。

## 训练方法
**核心推导（这是论文最硬的贡献，第 4 节 + 附录 S2–S4）：**

1. 扩散模型对 x_0 的边际似然 p_θ(x_0|c) 需对所有路径 x_{1:T} 积分，**不可解**。作者引入潜变量 x_{1:T}，把奖励定义在整条链上 R(c, x_{0:T})，并用 r(c,x_0)=E_{p_θ(x_{1:T}|x_0,c)}[R(c,x_{0:T})]，KL 项用其在路径上的联合 KL 上界替代。
2. 套用 DPO 的"奖励重参数化"（最优解 p*∝p_ref·exp(R/β)），把奖励写成 β·log(p_θ/p_ref)+β·logZ，代入 Bradley-Terry 二分类最大似然——**配分函数 Z(c) 在图对相减时抵消**，得到定义在扩散模型上的偏好损失（Eq.11）。
3. 由于 p_θ(x_{1:T}|x_0) 采样既低效（T=1000）又 intractable，用**前向 q(x_{1:T}|x_0) 近似反向**，配合 Jensen 不等式把期望推到外面，得到逐步 KL 形式（Eq.13）。
4. 用反向过程的高斯参数化（Eq.1）化简，最终得到极简损失（**Eq.14**）：

   `L = −E log σ( −βT·ω(λ_t)·( ‖ε^w−ε_θ(x_t^w,t)‖² − ‖ε^w−ε_ref(x_t^w,t)‖² − ‖ε^l−ε_θ(x_t^l,t)‖² + ‖ε^l−ε_ref(x_t^l,t)‖² ) )`

   直觉（Fig.2 损失面）：鼓励 ε_θ **在赢图上比参考模型去噪更好、在输图上相对更差**；β 越大损失面曲率越大、KL 约束越强。

- **理论自洽性**：作者另给两条独立推导得同一目标——多步 RL（off-policy，Control-as-Inference + inverse soft-Bellman 的 telescoping，附录 S3，证明其与 DDPO/DPOK 同设定但 off-policy）与"噪声偏好模型"视角（S4），并指出 DPO 损失隐式学到一个奖励模型。
- **训练设置（关键超参）**：
  - 优化器：SD1.5 用 AdamW；SDXL 用 **Adafactor** 省显存。
  - **有效 batch size = 2048 对**：16×A100，local batch=1 对，梯度累积 128 步。
  - 学习率 `lr = 2000/β × 2.048e-8`（随 β 反比缩放，因 DPO 梯度范数正比于 β），25% 线性 warmup；论文用 constant-with-warmup。
  - **β ∈ [2000, 5000]** 表现最好：SD1.5 主结果 β=2000，SDXL 主结果 β=5000（β 太小退化为纯奖励打分模型，太大则 KL 锁死几乎学不动，附录 S5）。
  - 训练步数：README 注明 SD1.5 约 **24 小时 / 2000 步**；AI-feedback 实验在 SD1.5 上 β=5000 跑 1000 步。
- **SFT 对照（反直觉结论）**：在赢图 (x, y_w) 上做 SFT，能提升 vanilla SD1.5（胜率 55.5%），但**对 SDXL 任何程度的 SFT 都会变差**——因为 Pick-a-Pic 图（来自 SDXL-beta/Dreamlike）质量低于 SDXL-1.0 base；这与原 DPO 论文"摘要任务已对齐模型不再受益于 preferred-FT"一致（附录 S6）。

## Infra（训练 / 推理工程）
- **算力**：16× NVIDIA A100；SDXL 因显存开 gradient checkpointing + Adafactor。未披露总 GPU·时（README 仅给 SD1.5 单机近似：~24h/2000 步）。
- **混合精度**：`accelerate launch --mixed_precision=fp16`（README）；分布式靠 HuggingFace `accelerate`，训练脚本改自 diffusers 库 t2i 示例。
- **推理**：**零额外推理开销**——对齐后模型与底模同架构、同采样步数，可直接换 U-Net 权重（HF 卡示例：加载 SDXL pipeline 后替换 `unet`）。无需蒸馏/缓存/量化等加速（本工作不涉及）。
- **附录 S8 的算力对比**：要让 baseline 的 PickScore 拒绝采样（rejection sampling，从 reference 多次抽样取最高分）追平 DPO 单次生成，平均需 **10× 推理算力**——即对齐把推理期算力"摊销"进了一次性训练。
- **部署形态**：开源 U-Net 权重（HF `mhdang/dpo-sdxl-text2image-v1`、`dpo-sd1.5-text2image-v1`，license openrail++），并入 HuggingFace diffusers 的 `research_projects/diffusion_dpo` 示例。

## 评测 benchmark（把效果讲清楚）
**人评（AMT，每对 5 人投票多数决；Q1 通用偏好 / Q2 视觉吸引力 / Q3 prompt 对齐）：**

- **DPO-SDXL vs SDXL-base（PartiPrompts，1632 prompt）**：Q1 General Preference 胜率 **70.0%**，Q2/Q3 胜率相近。
- **DPO-SDXL vs SDXL-base（HPSv2，3200 prompt）**：Q1 胜率 **64.7%**。
- **DPO-SDXL vs 完整 SDXL(base+refiner)**：PartiPrompts Q1 胜率 **69%**、HPSv2 Q1 胜率 **64%**——3.5B 打赢 6.6B，仅用 53% 参数。即便在 refiner 最擅长的 People 类别，DPO 对 base+refiner 仍胜 **67.2%**（对纯 base 是 73.4%）。
- **图生图编辑（TEdBench，100 对真实图文，SDEdit noise strength 0.6）**：DPO-SDXL 被偏好 **65%**，SDXL **24%**，平局 11%。

**自动指标：**
- **HPSv2 reward**：DPO-SDXL 在 HPSv2 prompt 上平均 reward **28.16**，登顶当时 HPSv2 leaderboard。
- **隐式奖励模型（偏好分类准确率，Pick-a-Pic v2 验证集，Tab.2）**：DPO-SDXL **72.0%**、DPO-SD1.5 **60.8%**；对比 PickScore 64.2%、HPS 59.3%、CLIP 57.1%、Aesthetics 51.4%（注：v1 训练的 PickScore 见过该评测数据仍被 DPO-SDXL 超过）。说明 DPO 目标里隐含的奖励参数化表达力/泛化与经典奖励建模相当。
- **AI-feedback 消融（SD1.5，Fig.6 自动 head-to-head 胜率矩阵）**：用 PickScore/HPS 偏好训练同时提升视觉与图文对齐；用 Aesthetics 训练拉高美学但牺牲 CLIP；**用 CLIP 偏好能提升图文对齐**（DRaFT 做不到，是相对前作的明确改进）。
- **数据清洗效应**：PickScore 伪标注训练 General Preference 胜率 59.8%→63.3%。

**消融结论**：β 在 [2000,5000] 最佳；SFT 对高质量底模（SDXL）有害；前向近似（用 q 近似反向）与 alternative 近似（q(x_t|x_0)p_θ(x_{t-1}|x_t)，误差更低）均给出可用闭式损失。

（说明：本文未报告 FID、GenEval、T2I-CompBench、DPG-Bench、MJHQ-30K、ImageReward、PickScore 绝对分数对比、ELO/Arena 等指标——这些维度在一手源中"未报告"，不臆造。验证集只用 median PickScore 做 checkpoint 选择。）

## 创新点与影响
**核心贡献：**
1. **首次把 DPO 严格推广到扩散模型**：用 ELBO + 前向近似把 intractable 的链上偏好似然化简为只需"两张图各加噪一次、各算一次 ε-预测"的可微闭式损失（Eq.14），训练稳定、无需在线 rollout、无需训练显式奖励模型、无需可微奖励。
2. **三视角自洽推导**（ELBO/Bradley-Terry、多步 off-policy RL、噪声偏好模型）建立其与 DDPO/DPOK 的理论联系并解释后者在开放词表退化的原因（score-function 梯度让高奖励 prompt 主导、无跨条件归一）。
3. **实证 SOTA**：开放词表下显著超 SDXL-base 与 base+refiner 全管线，并打通"扩散模型 + AI feedback"这条此前被认为不可行的路径（DRaFT 失败处）。

**影响：** Diffusion-DPO 成为 t2i/视频偏好对齐的事实标准基线，被后续大量工作扩展（如 step-aware / online / identity-preference 变体，以及 flow-matching 模型上的 DPO 变体），并直接进入 HuggingFace diffusers 作为官方研究示例。它把 LLM 的"对齐阶段"范式正式引入扩散生成。

**已知局限（作者自述）：** ①离线（offline）算法，作者预期 online 学习是下一步增益来源；②受标注者偏好与底模偏见双重影响，可学习并放大这些偏好（含性化倾向）；③偏好非普适（多数人偏爱"高对比、戏剧化"，小众偏好被平均化）；④依赖现成成对偏好数据，个人/小群体偏好对齐仍待探索；⑤未做安全过滤前不开源。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2311.12908
- arxiv_pdf: https://arxiv.org/pdf/2311.12908
- github: https://github.com/SalesforceAIResearch/DiffusionDPO
- hf_model (SDXL): https://huggingface.co/mhdang/dpo-sdxl-text2image-v1
- hf_model (SD1.5): https://huggingface.co/mhdang/dpo-sd1.5-text2image-v1
- diffusers 集成: https://github.com/huggingface/diffusers/tree/main/examples/research_projects/diffusion_dpo

## 一手源存档（sources/）
- [arxiv-2311.12908.pdf](https://arxiv.org/pdf/2311.12908)  （arXiv 原文 PDF，不入 git）
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/diffusion-dpo--readme.md)
- [hf-sdxl-card.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/diffusion-dpo--hf-sdxl-card.md)
