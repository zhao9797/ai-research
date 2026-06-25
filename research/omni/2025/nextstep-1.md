---
title: "NextStep-1: Toward Autoregressive Image Generation with Continuous Tokens at Scale"
org: "StepFun (阶跃星辰)"
country: China
date: "2025-08"
type: tech-report
category: t2i
tags: [autoregressive, continuous-tokens, flow-matching, next-token-prediction, t2i, image-editing, qwen2.5, flux-vae, nextstep-grpo, flowgrpo]
url: "https://arxiv.org/abs/2508.10711"
arxiv: "https://arxiv.org/abs/2508.10711"
pdf_url: "https://arxiv.org/pdf/2508.10711"
github_url: "https://github.com/stepfun-ai/NextStep-1"
hf_url: "https://huggingface.co/stepfun-ai/NextStep-1-Large"
modelscope_url: "https://modelscope.cn/models/stepfun-ai/NextStep-1.1"
project_url: "https://stepfun.ai/research/en/nextstep1"
downloaded: [arxiv-2508.10711.pdf, nextstep-1--readme.md, nextstep-1-large--hf-card.md, nextstep-1--blog.md, nextstep-1p1--blog.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
NextStep-1 是阶跃星辰（StepFun）推出的**纯自回归（next-token prediction）文生图大模型**：14B 因果 Transformer 主干（从 Qwen2.5-14B 初始化）+ 仅 157M 的 flow-matching 头，**直接在连续图像 token 上做下一 patch 预测**，既不依赖重量级外挂扩散模型，也不做 VQ 量化（无量化损失）。它把 AR 范式推到与扩散 SOTA 同台竞技的水平——GenEval 0.63（Self-CoT 0.73）、DPG-Bench 85.28、WISE 0.54（rewrite 0.79），编辑 GEdit-Bench-EN 6.58，是 AR 文生图里当时最强的开源模型之一，已被 **ICLR 2026 Oral** 接收。

## 背景与定位
AR 模型在语言上极成功，但搬到图像生成长期落后扩散。现有 AR 文生图主要两条路，各有硬伤：
- **VQ 离散 token 路线**（Emu3、Janus-Pro、LlamaGen、VAR、Infinity 等）：把图像量化成离散视觉词，存在**量化损失**与 **exposure bias**，重建/生成质量上限受限（见重建表：VQ tokenizer PSNR 普遍 <27，难破 30）。
- **AR + 外挂扩散路线**（如 Emu/Transfusion 一类）：AR 先吐一个语义 embedding，再交给一个重量级扩散模型一次性去噪整张图——本质是「Transformer 编排的扩散」，并非纯 NTP。

NextStep-1 走第三条路：**连续 token + patch-wise flow matching 头**，沿用 MAR（Li et al. 2024c）的"用轻量 FM 头建模每个连续 token 的条件分布"思路，但**把它 scale 到 14B 主干 + 大规模数据**，并解决了高维连续潜空间下的训练稳定性问题。核心主张：真正做生成的是**因果 Transformer 主干**（the real artist），FM 头只是个把上下文预测翻译成连续 token 的轻量采样器——这一点用消融强力支撑。技术脉络上承接 [[mar-masked-autoregressive]] 的连续 AR 思想、[[flow-matching]] 目标、[[latent-diffusion-ldm]] 系的 VAE 潜空间范式，并以 [[flux]] VAE 为 tokenizer 起点。

## 模型架构
统一序列：把文本离散 token 与图像连续 token 拼成一条序列，目标即标准 AR 分解 `p(x)=∏ p(x_i|x_<i)`。文本由 LM 头按交叉熵采样，图像 token 由 flow-matching 头按 flow matching 采样。序列格式：`{text} <image_area>h*w <boi> {image} <eoi> ...`，`<image_area>` 携带 2D 尺寸元数据。

**Image Tokenizer（核心创新所在）**：
- 从 **Flux.1-dev VAE** 微调而来，**只用重建 + 感知损失**（不加 KL 等），8× 空间下采样，**16 通道**连续潜空间。
- **Channel-wise normalization**：对每个通道做零均值单位方差标准化——这是稳住高 CFG 下生成的关键（见下）。
- **Stochastic perturbation（噪声正则，借鉴 σ-VAE）**：对归一化潜变量加噪 `z̃ = Norm(z) + α·ε`，其中 `α ~ U[0, γ]`、`ε ~ N(0,I)`；NextStep-1 用 **γ=0.5**。这制造了"反直觉"现象：噪声越大、重建 loss 越高，但 AR 生成质量反而越好（噪声正则让潜空间更鲁棒、更接近标准正态、更"分散"）。
- **Pixel-shuffle 压缩**：对潜变量做 2×2 space-to-depth，把 16ch 潜变量打成 64ch token。256×256 图 → 16×16 网格 × 64ch → 展平成 **256 个 token** 喂给 Transformer。

**Causal Transformer**：decoder-only，**从 Qwen2.5-14B 初始化**（借其语言理解/推理能力）。位置编码只用**标准 1D RoPE**（作者发现对混合文图序列足够有效，不需要 2D/多模态 RoPE）。

**两个轻量头**：
- Language Modeling Head：对文本 hidden 算交叉熵。
- **Patch-wise Flow Matching Head**：对每个图像 patch 的 hidden state 作条件，在时间步 t 去噪目标 patch，算 patch 级 flow-matching MSE 损失。结构为 **12 层、hidden 1536、157M 参数的 MLP**（即"Base"配置）。

总损失 `L = λ_text·L_text + λ_visual·L_visual`，训练中 CE:MSE 权重 **0.01:1**（即图像损失占主导）。整体 14B + 157M。

## 数据
四类语料协同（不同类目承担不同能力）：
- **纯文本 corpus**：从 **Step-3** 采样的 **400B** 文本 token，用于保住 LLM 语言能力。
- **图文对**：从 web 数据、多任务 VQA、富文本文档采集；经**质量过滤**（美学、水印、清晰度、OCR、图文语义对齐）；去重后用 **Step-1o-turbo 重新打 caption**（中英双语、丰富详细）。最终 **550M 高质量图文对**。（GitHub README 进一步透露：实际训练用了约 **10 亿（~1B）张**自有专有图像，无法开源。）
- **指令引导 image-to-image（编辑类）**：合成 1M（用 ControlNet annotator 对高质图文对加标注，用于视觉感知/可控生成）；收集 3.5M（来自 GPT-Image-Edit、Step1X-Edit 及自研内部数据，覆盖图像修复/通用编辑）。经 VLM 过滤（图对质量、合理性、一致性、指令对齐）后得 **~1M 高质量编辑数据**。
- **Interleaved（图文交错）**：四类——通用视频交错数据（**80M** 样本，受 Step-Video 启发，含抽帧/去重/captioning）、教程视频（ASR+OCR，富文本场景）、**character-centric 角色中心数据 NextStep-Video-Interleave-5M**（ArcFace 人脸检测+角色绑定+故事化 caption，强化多轮交互）、multi-view 数据（MV-ImageNet-v2 + Objaverse-XL，强化几何/多视角一致性）。

## 训练方法
训练目标为**双损失混合**：文本交叉熵 + 图像 token 的 flow-matching（rectified-flow 风格，预测把含噪 patch 映回干净 patch 的速度场，MSE）。

**Tokenizer 训练**：从 Flux.1-dev VAE 初始化，在图文数据上微调 50K 步，batch 512，constant LR 1e-5（1000 步 warmup），AdamW(β1=0.9, β2=0.95)。

**预训练三阶段课程**（除 tokenizer 冻结外端到端训练，见 Tab.1）：
- **Stage1**：256×256 固定分辨率，数据配比 文本20% / 图文60% / interleaved20%；LR 1e-4 constant，200K 步、warmup 5K、序列长 16K/rank，**~1.23T token**。
- **Stage2**：动态分辨率（256² 与 512² 基面，多 aspect-ratio bucket），加入更多富文本/视频交错数据；LR 1e-5，100K 步，**~0.61T token**。
- **Annealing**：在严格过滤后的 **20M 高质量子集**上跑 1 epoch（更严美学/清晰度/语义/水印阈值），cosine LR→0，20K 步，**~40B token**，显著提升结构/构图/纹理/美感。

**后训练（SFT → DPO）**：
- **SFT**：**5M** 样本，三部分——① 人选高语义一致+高美感图文对（并掺入其它生成模型的图做蒸馏，增强复杂/想象类 prompt）；② **CoT 数据**（生成前先做一段语言推理）；③ 高质量编辑数据。LR (0→1e-5) cosine、warmup 500、10K 步、序列长 8K/rank、约 5B token（Tab.1，v1）。
- **DPO**（论文写作 "Direct Policy Optimization"，引 Rafailov 的 DPO，受 Diffusion-DPO 启发）：从 ~20,000 prompt 构两类偏好集——**Standard DPO**（SFT 模型每 prompt 生 16 张，用 **ImageReward** 打分，赢者从 top4 随机取、输者从余 12 张随机取）；**Self-CoT DPO**（先让模型生成详细 CoT 扩展原 prompt，再走同样流程）。v1 仅 **300 步** DPO，LR 2e-6 constant（Tab.1）。
- **NextStep-1-Edit**：在 1M 高质量纯编辑数据上微调得到。

**NextStep-1.1（2025-12 发布，方法仅见官方博客，论文未覆盖）**——把 AR 文生图的 RL 后训练做稳：
- **延长预训练**：从 NextStep-1（256px）继续预训练 **500K** 步 @256（LR 1e-4）→ **20K** 步 @512 → **20K** 步 annealing，得 NextStep-1.1-Pretrain。（注：v1.1 博客 Tab.1 列 256px 续训为 500K，而博客正文写 "300K steps"——源内部不一致，此处取表中值。）
- **NextStep-GRPO**（核心新方法）：在 Pretrain 上做全参微调，基座是 **FlowGRPO**，复合奖励 = **PickScore**（人类偏好对齐）+ **OCR**（文字渲染，PaddleOCR）。直接套 FlowGRPO 在类 AR 模型上**不稳定**（梯度尖刺/崩溃、reward hacking、PickScore 持续下滑）。五项稳定化改造：① **重算保证训推一致**——BF16 下逐 token 采样与并行训练有数值偏差，先逐 token 生成、再把完整图文序列并行喂回主干**重算 log-prob** 对齐训练范式；② **训练期关闭 CFG**——CFG 会放大 BF16 数值误差并压缩探索空间，关掉虽降初始 baseline 但显著稳住轨迹、最终 reward 更高；③ **严格 on-policy**——「一采样步一次权重更新」，不在多 timestep 上多次更新；④ **FlowCPS**（Coefficients-Preserving Sampling）替代 FlowGRPO 中易爆梯度的小数除法，提升数值稳定；⑤ **在线拒绝采样**——丢掉奖励均值过高（平凡）或方差过低（探索崩溃）的 prompt 组。v1.1 用 1000 步 GRPO（替代 v1 的 300 步 DPO，SFT 步数置 0）。在标准扩散设置（SD3.5-Medium、同奖励）上验证 NextStep-GRPO 与 FlowGRPO 性能相当且**略优**（PickScore 23.66 vs 23.31、OCR 0.96 vs 0.92），证明稳定化不牺牲性能。

## Infra（训练 / 推理工程）
- **训练 infra**：基于 DeepSpeed（ZERO sharded checkpoint，附 `zero_to_fp32.py` 转换）+ HuggingFace Transformers；自研 `smartrun` 分布式启动器（自动包装 torchrun），数据用 WebDataset(Tar) 格式 + 索引预热。**总算力规模 / GPU 卡时未在论文或博客披露**（仅给出训练步数与 token 量：预训练合计约 1.9T token）。
- **推理形态**：HF `NextStepPipeline`，bf16；默认采样 cfg=7.5、num_sampling_steps=28、timesteps_shift=1.0（HF model card）；512px 推理。**vLLM-Omni**（2026-02）已支持 NextStep-1.1 高性能推理。
- **推理延迟分解**（H100，983 TFLOPS / 3.36 TB/s，batch=1，理论分析）：单 token 延迟里 **LLM 主干串行解码是主瓶颈**（~7.2 ms/token），FM 头多步采样 3.4 ms、LM 头 0.4 ms。累积延迟随序列爆炸：256 token 2.82s、1024 token 11.31s、4096 token 45.77s（去掉 FM 头分别 1.95/7.83/31.86s）。作者指出两条加速路线：FM 头侧（缩小/步数蒸馏/更优少步采样器），主干侧（speculative decoding / multi-token prediction 搬到图像 token）。

## 评测 benchmark（把效果讲清楚）
所有数字来自已抓取的论文 PDF 与官方博客一手源。

**图文对齐 / prompt following**（Tab.2）：
- **GenEval**：**0.63**（Self-CoT **0.73**）——与 SD3.5-Large(0.71)、BAGEL(0.82) 等扩散同档，AR 同行中靠前。
- **GenAI-Bench**：Basic **0.88**（Self-CoT 0.90），Advanced **0.67**（Self-CoT 0.74）。
- **DPG-Bench**：**85.28**（长 prompt 多对象，复杂构图保真可靠）。
- **OneIG-Bench（英文，Tab.3）**：Overall **0.417**，显著超 AR 同行 Emu3(0.311)、Janus-Pro(0.267)；分项 Alignment 0.882、Text(文字渲染) 0.891、Reasoning 0.306、Style 0.418、Diversity 0.197。

**世界知识 WISE**（Tab.4）：Overall **0.54**（Self-CoT **0.67**，rewrite **0.79**、rewrite+CoT **0.83**）——AR 模型最佳，且超多数扩散模型（Flux.1-dev 0.50、SD3.5-Large 0.46）。分项 Cultural 0.51 / Time 0.54 / Space 0.61 / Biology 0.52 / Physics 0.63 / Chemistry 0.48。

**图像编辑 NextStep-1-Edit**（Tab.5，GPT-4.1 评分；1:1 宽高比）：
- **GEdit-Bench-EN** G_SC/G_PQ/G_O = 7.15 / 7.01 / **6.58**；**GEdit-Bench-CN** = 6.88 / 7.02 / **6.40**——与 BAGEL(EN G_O 6.52)、Step1X-Edit 同档，逊于 GPT-4o(7.49)。
- **ImgEdit-Bench**：**3.71**（与 Flux.1-Kontext-dev 持平，逊于 GPT-Image-Edit 3.80、GPT-4o 4.20）。

**Tokenizer 重建**（Tab.8，ImageNet-1K 256×256）：NextStep-1 VAE（32×32×16 潜形，即实际采用的 γ=0.5 加噪版）**PSNR 30.60 / SSIM 0.89**——处于连续 tokenizer 第一梯队，与 Flux.1-dev(32×32×16，PSNR 31.64/SSIM 0.91)、SD3-Medium(30.00/0.88) 同档，明显高于 SD1.5/SDXL(4ch，25.18/26.22)；并显著超过所有 VQ 离散 tokenizer（SBER-MoVQGAN 27.04、Sefltok 26.30、LlamaGen 24.44、VAR 22.12、TiTok-S-128 17.52，多数 PSNR<27）。注意：尽管 γ=0.5 在 Fig.6 的"噪声越大重建 loss 越高"曲线里属高噪声端，Tab.8 报告的最终 NextStep-1 tokenizer 重建仍达 PSNR 30.60。

**关键消融结论**：
1. **FM 头大小几乎不影响生成质量**——40M / 157M / 528M 三种头各自重训 10K 步，GenEval(0.55/0.55/0.56)、GenAI-Bench(0.76/0.75/0.77)、DPG(83.46/84.68/85.50) 几乎一致 ⇒ **核心生成逻辑在 Transformer 主干**，FM 头只是轻量采样器。
2. **Channel-wise normalization 稳住高 CFG**：无归一化时 CFG=3.0 下 per-token 均值/方差对后段 token 显著漂移、出现灰块伪影；归一化后各 CFG（1.5→15.0）统计稳定。根因是 token 级 AR 中全局归一化不保证逐 token 统计一致，高 CFG 放大条件/无条件预测的小差异。
3. **噪声正则反直觉**：tokenizer 训练噪声 γ 越高、生成 loss 越高，但生成图越好（低 loss tokenizer 反而让 AR 输出近似纯噪声）——归因于潜空间鲁棒性 + 分散性（更贴近标准正态，见 Fig.7）。
4. **重建质量是生成质量上限**：连续高保真 VAE（PSNR>30 级）是 AR 高保真生成的前提，VQ 难破此阈。

## 创新点与影响
**核心贡献**：
1. **首个 scale 到 14B 的纯连续-token AR 文生图**，证明因果 Transformer 主干 + 极轻 FM 头即可在 NTP 框架下对连续视觉 token 直接建模、达到扩散 SOTA 量级——重新定义了"AR 图像生成"的边界（非 VQ、非外挂扩散）。
2. **把 tokenizer 摆到第一位**：channel-wise norm + 噪声正则两个简单 trick，系统解决了高维（16ch）连续潜空间下 AR 训练的发散与高 CFG 伪影，是该范式可 scale 的关键工程洞见。
3. **统一序列 + Qwen2.5 初始化**带来强 prompt following / 世界知识（WISE/GenAI-Bench 领先 AR 同行），并天然支持编辑、interleaved 多模态生成。
4. **NextStep-GRPO（v1.1）**：把 FlowGRPO 移植到自回归生成范式上做稳定化（on-policy 重算对齐、关 CFG、FlowCPS、在线拒采），为"AR 图像模型的 RL 后训练"提供了可复用配方，且反向在扩散上也略优于 FlowGRPO。

**已知局限**（论文 6.3 坦诚列出）：
- **高维潜空间伪影**：16ch（vs 4ch）偶发底部噪声/纯色块、grid 网格状伪影、整图噪声（分别归因数值不稳定、欠收敛、1D 位置编码对 2D 关系建模不足）。
- **推理慢**：严格串行解码，长序列累积延迟大（4096 token ~46s）。
- **高分辨率训练难**：AR 串行性使高分辨率收敛需远多步数；扩散的 timestep-shift 等技巧因 FM 头只是采样器而难迁移。
- **SFT 不稳**：小高质数据集上动态不稳——要么提升微弱、要么骤然过拟合，需 million 级样本才稳，找"既对齐目标又保通用"的中间 ckpt 困难（这也是 v1.1 改用延长预训练 + GRPO、SFT 步数置 0 的动因）。

**影响**：作为开源（Apache-2.0）强基线，连同技术报告把"纯 AR 连续-token 生成"推成一条受关注的与扩散并行的路线；ICLR 2026 Oral；后续 v1.1 + vLLM-Omni 支持落地推理。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2508.10711
- arxiv_pdf: https://arxiv.org/pdf/2508.10711
- github: https://github.com/stepfun-ai/NextStep-1
- hf: https://huggingface.co/stepfun-ai/NextStep-1-Large
- hf_collection: https://huggingface.co/collections/stepfun-ai/nextstep-1-689d80238a01322b93b8a3dc
- project_homepage: https://stepfun.ai/research/en/nextstep1
- blog_v1: https://stepfun-ai.github.io/NextStep-1/nextstep_1_blog/
- blog_v1.1 (NextStep-GRPO): https://stepfun-ai.github.io/NextStep-1/nextstep_1p1_blog/
- modelscope_v1.1: https://modelscope.cn/models/stepfun-ai/NextStep-1.1

## 本地落盘文件
- ../../../sources/omni/2025/arxiv-2508.10711.pdf
- ../../../sources/omni/2025/nextstep-1--readme.md
- ../../../sources/omni/2025/nextstep-1-large--hf-card.md
- ../../../sources/omni/2025/nextstep-1--blog.md
- ../../../sources/omni/2025/nextstep-1p1--blog.md
