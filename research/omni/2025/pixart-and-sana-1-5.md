---
title: "SANA 1.5: Efficient Scaling of Training-Time and Inference-Time Compute in Linear Diffusion Transformer"
org: "NVIDIA / MIT / 清华 / Playground / 北大 / HKU"
country: US
date: "2025-01"
type: tech-report
category: t2i
tags: [t2i, linear-attention, dit, model-growth, depth-pruning, inference-scaling, came-8bit, efficient-scaling, geneval, sana]
url: "https://arxiv.org/abs/2501.18427"
arxiv: "https://arxiv.org/abs/2501.18427"
pdf_url: "https://arxiv.org/pdf/2501.18427"
github_url: "https://github.com/NVlabs/Sana"
hf_url: "https://huggingface.co/collections/Efficient-Large-Model/sana-15"
modelscope_url: ""
project_url: "https://nvlabs.github.io/Sana/Sana-1.5/"
downloaded: [arxiv-2501.18427.pdf, arxiv-2501.18427.txt, sana-1-5--readme.md, sana-1-5--project-page.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
SANA-1.5 是 NVIDIA/MIT/清华在线性注意力扩散 Transformer 上做"高效算力扩展"的工作：用**深度生长(model growth)**把 1.6B→4.8B（20→60 层）训练成本省 60%、收敛快 2.5×，配 **8-bit CAME 优化器**让 4.8B 能在单张 RTX 4090 上微调；再用**深度剪枝**把 4.8B 灵活压回 3.2B/1.6B，**推理时缩放(repeat sampling + VLM 评判)**把 GenEval 从 0.81 推到 **0.96**，刷新 GenEval SoTA（超过 24B 的 Playground v3 的 0.76 共 20 个点）。

## 背景与定位
- T2I 模型一年内从 PixArt 的 0.6B 膨胀到 Playground v3 的 24B，训练/推理成本对大多数研究者已不可承受。[[sana]]（SANA-1.0）用**线性注意力 DiT + 32× 深度压缩自编码器 [[dc-ae]]**做到"小而快"（0.6B 比 FLUX-12B 小 20×、快 100×）。SANA-1.5 在此基础上回答两个问题：(i) 线性 DiT 的可扩展性如何？(ii) 如何把大线性 DiT 扩起来同时降训练成本？
- 它不属于"把模型做大"路线，而是反其道：**用更好的优化轨迹（growth）+ 灵活部署（pruning）+ 用算力换容量（inference scaling）**，主张"thoughtful optimization > 单纯堆参数"。三个技术（生长/剪枝/推理缩放）构成一个连贯框架：生长先探索更大优化空间发现更好特征，剪枝识别并保留这些核心特征，推理缩放则在模型容量受限时用额外推理算力补回质量。
- 技术脉络上承 [[latent-diffusion-ldm]] → [[dit-scalable-diffusion-transformers]] → [[pixart-alpha]]（训练成本仅为 SD-v1.5 的 10.8%）→ [[sana]]；剪枝借鉴 LLM 的 Minitron，推理缩放借鉴 LLM 的 "Large Language Monkeys"（log-linear 重复采样规律）。
- 注：本工作 slug 名为 "pixart-and-sana-1-5"，但所抓一手源（arXiv 2501.18427、GitHub、官方页）全部是 **SANA-1.5**；PixArt 仅作为技术脉络前置工作（同一作者团队 Junsong Chen / Enze Xie）出现，本页以 SANA-1.5 为主体。SANA-1.5 被 ICML 2025 接收。

## 模型架构
**骨干：线性扩散 Transformer（Linear DiT）。** 沿用 SANA-1.0 的线性注意力设计，但本文为"大模型稳定训练"做了关键架构补丁。
- **Linear DiT Block 构成**：线性自注意力（ReLU-based linear attention，内容编码）+ vanilla cross-attention（文本条件注入）+ Mix-FFN。线性注意力把复杂度从 O(N²) 降到 O(N)，是高分辨率下高效的根本。
- **QK Norm（核心稳定性补丁）**：在线性自注意力和 cross-attention 的 Query/Key 上加 **RMSNorm**。作者发现 ReLU-based 线性注意力的 attention logits 会不受控增长、频繁超出 FP16 数值范围（6.5e5）导致 NaN；QK-Norm 有效解决了大线性 transformer 的训练不稳定。值得注意：SANA-1.0 1.6B 原本没有 QK-Norm，但仅 1K 步微调就能适配这些新增归一化层。
- **规模/分辨率策略**：最终 SANA-4.8B = **60 层**，通道维 **2240/层**、FFN 维 **5600**（与 SANA-1.6B 一致，只加深度不加宽度——呼应"加 transformer block 比加通道数更参数高效"的 DiT scaling 结论）。1.6B 为 20 层。评测在 512×512 与 1024×1024；SANA 系列另支持 2K/4K（DC-AE tiling）。
- **VAE / tokenizer**：DC-AE（Deep Compression Autoencoder），**32× 图像压缩**（传统 VAE 为 8×），大幅减少 latent token 数，是高分辨率高效的关键。
- **Text encoder**：decoder-only 现代小 LLM（SANA 系列用 Gemma 类小型 decoder-only LLM，带 in-context learning，优于 T5/CLIP 的对齐）；本文未在正文重述 text encoder 细节，沿用 SANA-1.0 配置。
- **条件注入**：cross-attention 注入文本嵌入。Patchify→Linear DiT blocks→Unpatchify→预测，标准 latent diffusion 流程。

## 数据
- **训练数据/超参与 SANA-1.6B 一致**：本文明确"架构、训练数据、其他超参数都与 SANA-1.6B 保持一致"，故大规模图文对的来源/规模/配比沿用 SANA-1.0（本文未重述具体来源与体量）。
- **两阶段数据**：先在大规模数据集预训练，再在高质量数据集 SFT。高质量 SFT 集为从 **50M 预训练数据中筛出的 3M 样本**（按 CLIP score > 25 过滤），用于不同尺寸模型的后训练。
- **多语种自动标注流水线**：用 GPT-4 把仅 **100K 英文 prompt**（作为源）翻译成 3 种目标格式——纯中文 / 中英混合 / emoji 混合（原始英文 caption 一并保留，构成多语种多 caption 训练集）；SANA 仅约 **10K 步**微调即获得稳定准确的中文与 emoji 表达能力（数据高效）。
- **GenEval 风格 SFT 数据（v2，关键提升来源）**：新建 144,291 张图（来自 18,240 个 GenEval 风格 prompt，每 prompt 平均 7.91 张"正确"图、最多 10 张防过拟合），由 **GenEval toolkit 过滤"正确"图**。**刻意排除 GenEval 测试集 prompt，并用 Flux-Schnell 生成图以避免过拟合/泄漏**。该 SFT 数据把 SANA-1.5-4.8B 的 GenEval 从 0.72(v1)→**0.81(v2)**。
- **VILA-Judge 训练数据**：为 inference scaling 训练评判器，构造 2M（正文）/ 2.5M（附录）prompt-matching 数据集；用 15,654 个唯一 prompt × 每 prompt 160 张 Flux-Schnell 图，prompt 风格仿 GenEval（含 Mask2Former 的 80 类物体 + 颜色/空间/数量/关系属性），同样**不与 GenEval 测试集重叠**，用 GenEval toolkit 打 yes/no 标签。
- **安全过滤**：部署时配 ShieldGemma-2B 安全检查模型，用户 prompt 先过 NSFW 检测再生成。

## 训练方法
- **训练目标**：扩散（flow-matching 框架，沿用 SANA-1.0 的 Flow-DPM-Solver 采样；剪枝微调用"与大模型相同的训练损失"监督）。
- **三大方法（本文核心）**：
  1. **高效模型生长(Efficient Model Growth)**：把 N=20 层预训练模型扩到 N+M=60 层。比较 3 种初始化：(a) **Partial Preservation Init**（保留前 N 层预训练权重、新增 M 层随机初始化）；(b) Cyclic Replication（周期重复预训练层）；(c) Block Replication（每层扩成 r 个连续层）。**最终采用 Partial Preservation**——简单稳定，形成"预训练层做特征提取 / 新层从恒等映射出发逐步精化"的分工。Cyclic/Block 复制因 4.8B 与 1.6B 特征分布不同而训练不稳定（NaN loss）。
     - **Identity Mapping 初始化**：对新层的 self-/cross-attention 输出投影、MLP 最后一个 point-wise conv 做**零初始化**（Net2Net 思路），使新 block 初始为恒等函数——精确保留预训练行为、提供稳定优化起点。
     - **关键 trick：丢弃预训练模型最后 2 个 block 再加新层**。直接在所有预训练 block 后追加新 block，会因预训练特征经 skip-connection 主导表示而让新 block 学不到东西、卡在局部最优；末两层任务相关性高，去掉后能促进后续新 block 学习。官方页另述为"用 1.6B 的前 18 层初始化 4.8B"（即 20 去 2 = 18，一致）。
     - **稳定性增强**：所有初始化策略都对 Q/K 加 layer norm（即上述 QK-Norm）以稳早期注意力、防梯度不稳。
  2. **深度剪枝(Model Depth Pruning)**：借鉴 Minitron，用**输入输出相似度**算 block 重要性 `BI_i = 1 − E[ X_i·X_{i+1} / (‖X_i‖‖X_{i+1}‖) ]`，在 100 个多样 prompt 的校准集上跨扩散时间步平均。发现**头尾 block 重要性高、中间 block 输入输出高度相似（重要性低）**——头部把 latent 分布转成扩散分布、尾部转回、中间渐进精化。按排序剪掉低重要性 block（60→40/30/20），剪枝主要损失高频细节但保留布局/语义；再用与大模型相同损失**微调（仅 100 步 / 单 GPU ~5 分钟）即可恢复**。
  3. **推理时缩放(Inference-Time Scaling)**：放弃"加去噪步数"（不能自纠错、20 步后质量很快饱和、2.5× 步数无明显提升），改用**重复采样 best-of-N**。训练专用评判器 **VILA-Judge**（在 NVILA-2B 上微调）：弃用 CLIP/SigLIP（上下文窗口太小，77/66 token）与商用 API（GPT-4o/Gemini-1.5-pro 评分不一致、且对首个选项有强位置偏好）；以 **tournament 锦标赛式两两比较**输出 yes/no——双 yes/no 则比 logprob 置信度，鲁棒过滤不匹配图。
- **多阶段**：预训练（lr=1e-4）→ SFT（lr=2e-5）。0.6B/1.6B 预训练 >200K 步、4.8B >100K 步，各 SFT ~10K 步（SFT 带来 +3~4% GenEval）。
- **优化器：CAME-8bit（自研，本文一等贡献）**：在 CAME（用二阶矩阵分解把内存减半）基础上，对一阶动量做 **block-wise 8-bit 量化**（每 2048 元素块独立 min-max 线性量化到 8-bit，仅量化 >16K 参数的大 linear/1×1 conv 层），二阶统计保持 32-bit 以稳。整体把优化器内存压到 **~AdamW 的 1/8**，使 4.8B 量级模型可在消费级 GPU(RTX 4090) 上微调。

## Infra（训练 / 推理工程）
- **训练硬件**：PyTorch **DDP**，**64× NVIDIA A100**（8 DGX 节点）。全局 batch size 在训练中**动态调整 1024~4096**。codebase 另支持 DDP/FSDP、Multi-Scale WebDataset（TAR）训练。
- **精度**：bf16 混合精度 + CAME-8bit；QK-Norm 解决线性注意力 FP16 溢出问题。
- **内存实测**：1.6B 训练上，CAME-8bit 比 AdamW **省 25% 显存（43GB vs 57GB）且收敛速度无退化**；8-bit 优化器（AdamW-8bit/CAME-8bit）收敛与 32-bit 版相当。内存节省随模型增大而更显著（优化器状态内存正比于模型大小）。
- **训练加速效果**：模型生长比"放大后从头训"**快 2.5×收敛**、省 **60% 训练步**（4.8B 达到同样 0.70 GenEval）。
- **推理部署**：A100 BF16 下，4.8B latency 4.2s（batch=1, 20 步）、throughput 0.26 samples/s（vs FLUX-dev 23.0s / 0.04，约低 5.5× 延迟、高 6.5× 吞吐）；1.6B latency 1.2s。生态：diffusers `SanaPipeline`、ComfyUI、SGLang serving、Replicate API；4bit-SANA（SVDQuant/Nunchaku）可在 **<8GB VRAM** 笔记本 GPU 跑，DC-AE tiling 让 4K 推理在 22GB（量化后 8GB）内完成。
- **推理缩放的算力代价**：采样 N 张图需 N×49,140 GFLOPs（SANA 生成）+ 2N×4,518 GFLOPs（VILA-Judge 评判比较），作者明确把效率优化留作 future work。

## 评测 benchmark（把效果讲清楚）
评测协议：FID/CLIP 在 **MJHQ-30K**（30K Midjourney 图）；GenEval(553 prompt) 与 DPG-Bench(1065 prompt) 测文图对齐，作者尤其看重 GenEval。

**主表（1024px，A100/BF16；Throughput@batch=10，Latency@batch=1/20步）**
| 模型 | Params(B) | FID↓ | CLIP↑ | GenEval↑ | DPG↑ | Throughput | Latency(s) |
|---|---|---|---|---|---|---|---|
| PixArt-Σ | 0.6 | 6.15 | 28.26 | 0.54 | 80.5 | 0.4 | 2.7 |
| FLUX-dev | 12.0 | 10.15 | 27.47 | 0.67 | 84.0 | 0.04 | 23.0 |
| Playground v3 | 24 | — | — | 0.76 | 87.0 | — | — |
| SANA-1.0 1.6B | 1.6 | 5.76 | 28.67 | 0.66 | 84.8 | 1.0 | 1.2 |
| SANA-1.5 4.8B Pre | 4.8 | 5.42 | 29.16 | 0.72 | 85.0 | 0.26 | 4.2 |
| **SANA-1.5 4.8B Ours** | 4.8 | 5.99 | **29.23** | **0.81** | 84.7 | 0.26 | 4.2 |

- **生长收益**：1.6B→4.8B-Pre：GenEval 0.66→0.72(+0.06)、FID 5.76→5.42、DPG 84.8→85.0；后训练(SFT)再到 **GenEval 0.81**，超 Playground v3(24B) 的 0.76，且延迟比 FLUX-dev 低 5.5×、吞吐高 6.5×。
- **README 补充数字**：SANA-1.5 **1.6B** GenEval **0.82**（FID 5.70、CLIP 29.12、DPG 84.5），SANA-1.5 4.8B GenEval 0.81（FID 5.99、CLIP 29.23、DPG 84.7）——即 1.6B 经生长-剪枝后 GenEval 甚至略高于 4.8B。
- **推理缩放（Table 2，2048 样本 best-of-N）**：SANA-1.5 4.8B GenEval **0.81→0.96**（overall +15%），分项 Position 0.59→0.96、Color Attribution 0.65→0.87、Counting 0.86→0.97。**0.96 刷新 GenEval SoTA**，超 Playground v3(24B) 的 0.76 共 20 个点。该方法对小模型同样有效（SD1.5 0.42→0.87；1.6B+scaling > 4.8B 单次生成）。
- **剪枝（Table 3，512px，无高质量 SFT 对齐对比）**：4.8B GenEval 0.693 → 剪到 3.2B 0.673(+FT 0.684) → 剪到 1.6B 0.571(**+FT 仅 100 步即 0.672**)，超过从头训的 SANA-1.0 1.6B(0.664)。2.4B+FT 为 0.675。证明"grow-then-prune"得到任意尺寸模型都优于同尺寸从头训。
- **消融结论**：(1) Partial Preservation Init 稳，Cyclic/Block Replication NaN；(2) 去掉末 2 个预训练 block 才能让新 block 学起来；(3) CAME-8bit 收敛=32-bit 且省 25% 显存；(4) 推理缩放在 GenEval 上随采样数 log-linear 提升；(5) GPT-4o/Gemini 做评判有位置偏好与不一致，需自训 VILA-Judge。
- **局限**：复杂文本渲染与人物细节仍弱；推理缩放算力代价大。

## 创新点与影响
- **核心贡献**：(1) **深度生长 + 部分保留初始化 + 丢末两层 + 恒等映射** 的高效扩参范式（省 60% 训练成本、2.5× 收敛），把 LLM 的 model growth 系统迁到线性扩散 DiT 并解决其特有的稳定性问题（QK-Norm 防线性注意力溢出）；(2) **CAME-8bit** 首个 8-bit CAME 优化器，让 4.8B 扩散模型可在单张消费级 GPU 微调；(3) **基于 block 重要性的深度剪枝**，一次大模型训练换来任意尺寸的灵活部署；(4) 把 LLM 的**推理时缩放(repeat-sampling + VLM-judge)首次系统用于扩散 T2I**，证明"用算力换容量"——小模型+推理缩放 > 大模型，挑战"越大越好"的常识，把 GenEval 推到 0.96。
- **影响**：SANA 全家桶（1.0/1.5/Sprint/Video/WM/Streaming/Sol-RL）的承上启下之作；ICML 2025；权重/代码 Apache-2.0 全开源，进 diffusers/ComfyUI/SGLang/Replicate 生态，4bit 版可在 8GB 笔电 GPU 跑，显著降低了高质量 T2I 的研究与部署门槛。其"grow-prune-inference-scale"三件套与"用更好优化轨迹替代堆参数"的论点，对后续高效生成模型有方法论影响。
- **已知局限**：训练数据具体来源/体量沿用 SANA-1.0 未在本文重述；文本渲染、人物细节仍是短板；推理缩放需 N 倍生成 + 评判算力，效率待优化。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2501.18427
- arxiv_pdf: https://arxiv.org/pdf/2501.18427
- github: https://github.com/NVlabs/Sana
- project_page: https://nvlabs.github.io/Sana/Sana-1.5/
- hf_models: https://huggingface.co/collections/Efficient-Large-Model/sana-15
- 前置工作 SANA-1.0: https://arxiv.org/abs/2410.10629 ; DC-AE: https://arxiv.org/abs/2410.10733

## 一手源存档（sources/）
- [arxiv-2501.18427.pdf](https://arxiv.org/pdf/2501.18427)  （arXiv 原文 PDF，不入 git）
- [arxiv-2501.18427.txt](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/arxiv-2501.18427.txt)
- [sana-1-5--readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/sana-1-5--readme.md)
- [sana-1-5--project-page.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/sana-1-5--project-page.md)
