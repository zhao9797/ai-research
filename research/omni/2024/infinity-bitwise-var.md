---
title: "Infinity: Scaling Bitwise AutoRegressive Modeling for High-Resolution Image Synthesis"
org: ByteDance
country: China
date: "2024-12"
type: paper
category: method
tags: [t2i, autoregressive, var, next-scale-prediction, bitwise-tokenizer, bsq, infinite-vocabulary, self-correction, scaling-law]
url: "https://arxiv.org/abs/2412.04431"
arxiv: "https://arxiv.org/abs/2412.04431"
pdf_url: "https://arxiv.org/pdf/2412.04431"
github_url: "https://github.com/FoundationVision/Infinity"
hf_url: "https://huggingface.co/FoundationVision/infinity"
modelscope_url: ""
project_url: "https://foundationvision.github.io/infinity.project/"
downloaded: [arxiv-2412.04431.pdf, infinity-bitwise-var--readme.md, infinity-bitwise-var--project-page.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Infinity 是字节跳动在 [[var-next-scale-prediction]]（视觉自回归 next-scale prediction）基础上提出的**比特级（bitwise）视觉自回归 T2I 框架**：把离散 tokenizer 的词表理论扩到 2^64（"无限词表"），用「无限词表分类器 IVC」预测 d 个比特而非 2^d 个索引、用「比特级自纠正 BSC」消除 teacher-forcing 的训练-推理失配。Infinity-2B 把 GenEval 从 SD3-Medium 的 0.62 提到 0.73、ImageReward 0.87→0.96，人评胜率 66%，并以 0.8 秒生成 1024×1024（比 SD3-Medium 快 2.6×），成为当时最快的 T2I 模型，是首个在多项基准上超越主流扩散模型的离散自回归 T2I（CVPR 2025 Oral）。

## 背景与定位
T2I 生成长期分两派：扩散模型（连续去噪，质量/细节强）与自回归模型（借 LLM 的可扩展性，把图像离散成 token 做 next-token / next-scale 预测）。自回归路线的两大痛点：(1) **离散 tokenizer 量化误差大**——词表受限导致高分辨率细节重建质量远逊连续 VAE；(2) **teacher-forcing 训练带来的训练-推理失配**——前面尺度的错误会逐级传播放大，最终破坏整图。

[[var-next-scale-prediction]]（VAR，NeurIPS 2024 Best Paper）把图像自回归重定义为「由粗到细的 next-scale 预测」，兼具 LLM 的可扩展性与扩散式逐级 refine 的优点。但 VAR 仍沿用 index-wise 离散 tokenizer，受限于词表大小：单纯把现有 tokenizer 词表放大会带来内存/算力的指数爆炸，且大整数索引的监督"模糊"（near-zero 特征的微小扰动会让索引标签完全跳变），难以优化。

Infinity 的定位即：**用比特级建模（bitwise modeling）把整条链路从 index-wise 换成 bitwise**，从而把词表理论扩到无限，同时解决"大词表分类器算不动"与"index 监督模糊"两个问题，再用自纠正补上 VAR 继承自 LLM 的 teacher-forcing 缺陷。相关脉络：[[ldm-stable-diffusion]]、[[sd3-mmdit]]（rectified flow 扩散对手）、[[llamagen]]/[[emu3]]（VQ 自回归）、[[hart-hybrid-tokenizer]]（VAR 上的混合 tokenizer）、[[maskgit]]（masked 生成）。

## 模型架构
整体 = **比特级多尺度视觉 tokenizer** + **带 cross-attention 的因果 VAR transformer**，三大核心组件：比特级 tokenizer、无限词表分类器 IVC、比特级自纠正 BSC。

**Backbone（生成 transformer）**：解码器式因果 transformer，逐 block 重复，每个 block 含 RoPE2d + Self-Attention + Cross-Attention + FFN。
- **条件注入**：文本编码器为 **Flan-T5-XL**，文本嵌入 Ψ(t)∈R^{L×C}，一方面投影成 ⟨SOS⟩∈R^{1×1×h} 作为第一尺度输入，另一方面在**每一层 cross-attention** 中引导生成（区别于纯 prefix 注入）。
- **next-scale 预测**：把图像编码成特征图 F∈R^{h×w×d}，量化成 K 个多尺度残差 (R1…RK)，分辨率由小到大；累积上采样 Fk=Σ up(Ri) 逐步逼近连续特征。预测第 k 尺度时，取上一尺度下采样特征 Ẽk−1=down(Fk−1) 作并行输入，训练用 block-wise causal mask 只看前缀上下文，推理用 KV-Cache 加速、无需 mask。**与 VAR 最大不同：预测目标是 bit labels 而非 index labels**。
- **位置编码**：对每个尺度的特征施加 **RoPE2d** 保留图像 2D 结构 + **可学习的 scale embedding** 区分不同尺度（替代 VAR 的 learnable APE——后者参数多、序列长度变化时易混淆）。消融显示该组合比 learnable APE 收敛更快、训练精度更高。
- **动态长宽比**：不同于只能出方图的 VAR，Infinity 预定义按长宽比组织的 scale schedule，保证各尺度 (hk,wk) 的长宽比≈目标比、且同尺度不同比例下 hk×wk 面积大致相等（训练序列长度大致一致）。

**Visual Tokenizer（比特级多尺度残差量化器）**：把 VAR 的向量量化换成**维度无关的比特量化器**，候选两种——LFQ（qk=sign(zk)）与 **BSQ**（qk=sign(zk/|zk|)·1/√d，输入输出均为单位向量）。BSQ 对 entropy penalty 有 O(d) 近似（LFQ 需 O(2^d) 计算全码本相似度，d=20 即 OOM），故**默认用 BSQ**，使词表扩到 2^64 时显存几乎不增。码本利用率靠 entropy penalty L=E[H(q(z))]−H[E(q(z))] 维持。tokenizer 即 BitVAE（后单独开源训练代码）。

**参数与规模**：transformer 缩放档位（Tab.6）125M / 361M / 940M / 2.2B / 4.7B，对应 hidden 768→2688、heads 8→24、layers 12→40。发布的旗舰为 **Infinity-2B**（layer32, c8）与 **Infinity-8B**，并预告 **Infinity-20B**。分辨率支持 256 / 512 / 1024，stride=16。

## 数据
- **来源**：开源学术数据（**LAION、COYO、OpenImages**）+ 内部高质量收集数据。
- **清洗过滤**：用 **OCR 模型**滤掉文字过多的图，用**水印检测模型**滤掉带水印图，用 **Aesthetic-V2** 滤掉低美学分图。
- **标注 / re-captioning**：训练样本同时带 **long caption（由 InternVL 2.0 生成）** 与可选 short caption（用户 prompt 风格）；数据集按长宽比模板组织成 `[h_div_w]_[num_examples].jsonl`，支持 >100M 量级样本（README）。
- **规模配比**：论文给出训练用量级——预训练用开源学术数据（如图 9/10 的消融用 5M/10M 高质量图文对做对照），1024 精调用"更小、更高质量"的数据集；**具体总体量、各源精确配比未披露**。
- 评测侧自建 40K 图文对验证集量 FID。

## 训练方法
**目标**：next-scale 残差的**比特预测**——对每个尺度的 d 个比特用 IVC 的 d 个并行二分类器预测正/负，交叉熵优化（替代传统 Vd 类大分类器）。这是 Infinity 区别于扩散（flow matching / 去噪）路线的核心：纯离散自回归。

**Infinite-Vocabulary Classifier（IVC）**：传统分类器需权重矩阵 W∈R^{h×Vd}，d=32、h=2048 时达 **8.8 万亿参数**（超算力上限）；IVC 改为 **d 个并行二分类器预测每个 bit 的正负**（d=log2 Vd），Vd=2^16、h=2048 时**省 99.95% 参数与显存**（124M→0.65M，2GB→10MB）。额外好处：当某些维度 near-zero 让模型困惑时，其它维度的监督仍清晰 → 比 index-wise 更易优化。消融（Tab.5）：IVC 重建 loss 0.180<0.184、FID 3.83<4.49、ImageReward 0.91>0.79、HPSv2.1 32.31>31.95，全面优于传统分类器。

**Bitwise Self-Correction（BSC）**：解决 teacher-forcing 训练-推理失配。做法——以 [0,p] 均匀采样的概率**随机翻转 Rk 的部分比特**得 Rk_flip 模拟预测错误，**用翻转后的残差重算 transformer 输入 Ẽk 并重新量化得到新目标 Rk+1**（Alg.2）。关键在"重量化纠错"而非单纯翻转：transformer 把带错误的特征当输入、把重量化后的正确 bit 当标签 → 学会自动纠正前序错误。**不增加额外计算、不破坏并行训练**（只改输入和标签）。消融（Tab.7，5M 高质量数据/512 分辨率）：Baseline FID 9.76 → 单纯随机翻转 9.69（几乎无改善）→ **加 BSC 后 FID 3.48**、ImageReward 0.52→0.76、HPSv2.1 29.53→30.71，证明增益来自"自纠正"机制而非"翻转"本身。翻转强度消融（Tab.8）：p=10%/20% 不足，**p=30% 最优**（FID 3.33、ImageReward 0.775、HPSv2.1 31.05）。

**多阶段渐进训练（以 Infinity-2B 为例）**：
1. 256 分辨率预训练 150k iters，batch 4096，lr 6e-5；
2. 切到 512 分辨率续训 110k iters（同超参）；
3. 1024 分辨率在更小高质量数据上精调 60k iters，batch 2048，lr 2e-5。
所有阶段都用**变长宽比**图像。

**蒸馏/加速**：论文未做步数蒸馏（consistency/LCM/ADD 等）；其速度优势源于 next-scale 范式天然步数少 + KV-Cache，"无额外优化"即为最快（见 Infra/评测）。

**解码（推理 trick）**：得益于 BSC 带来的鲁棒性，Infinity 在**早期尺度也能用大 CFG**，无需 VAR 的 pyramid-CFG（VAR 需金字塔式逐尺度线性增大 CFG 以防早期崩溃）。解码消融（Tab.9）：在 logits 上做 CFG（τ=1, cfg=4）最优——FID 2.82、ImageReward 0.962、HPSv2.1 32.25，优于 greedy / normal / pyramid-CFG。

## Infra（训练 / 推理工程）
- **训练框架**：用 **FlexAttention** 加速训练（要求 torch≥2.5.1）；torchrun 多机多卡（README 给出 8 卡/节点的训练脚本）；推荐 wandb 记录；支持断点自动续训。**具体 GPU 数量 / GPU·时 / 并行策略（TP/PP/数据并行细节）/ 混合精度方案未在论文披露**。
- **tokenizer 显存优势（Tab.3）**：BSQ 在 d=16/18/20/32/64 下显存恒为 **32.4GB**，而 LFQ 在 d=16 为 37.6GB、d=18 为 53.7GB、d≥20 即 **OOM**——这是"无限词表"工程可行的关键。
- **推理加速**：KV-Cache + next-scale 少步数。推理延迟（Tab.2，~2B 规模 1024 出图）：**Infinity-2B 0.8s**，对比 PixArt-Sigma 1.1s、SD3-Medium 2.1s、SD-XL 2.7s。8B 规模下 Infinity 比 SD3.5 快 **7×**——速度优势随模型增大而扩大。
- **部署**：开源权重（HF `FoundationVision/infinity`，含 vae d16/d24/d32/d64 与 2b/8b transformer）、Docker 一键推理（reproduce.py）、Replicate 在线 demo、字节官方 demo 平台、prompt rewriter 工具。

## 评测 benchmark（把效果讲清楚）
**Tokenizer 重建（ImageNet rFID，stride=16，Tab.4 / README）**：词表越大重建越好，离散追平/反超连续 VAE。
- Vd=2^16: IN-256 rFID 1.22 / PSNR 20.9；IN-512 rFID 0.31
- Vd=2^24: 0.75 / 22.0；0.30
- Vd=2^32: **0.61 / 22.7**；0.23（已**超过 SD 连续 VAE 的 0.87**）
- Vd=2^64: **0.33 / 24.9**；0.15
- 对照 SD VAE（连续）IN-256 rFID 0.87。

**GenEval / DPG（Tab.1，Infinity-2B）**：
- **GenEval Overall 0.73†**（带 prompt rewriter；不带为 0.69），其中 Two Obj. 0.85†、Position 子项 0.49†（与 Emu3 0.49† 并列最高）、Color Attri. 0.57†；超过 SD3(d=24) 0.62、SD3(d=38) 0.71、SDXL 0.55、DALL-E 3 0.67†、Emu3 0.66†。
- **DPG Overall 83.46**（Global 93.11、Relation 90.76），超过 SDXL、PixArt-Sigma、DALL-E 3；Relation 子项 **90.76**（论文称为开源 T2I 最高；闭源 DALL-E 3 为 90.58）。

**人评偏好 + 延迟（Tab.2，~2B/1024）**：Infinity 在 **ImageReward 0.962**（SD3-Medium 0.871、PixArt-Sigma 0.872、SD-XL 0.600）与 **HPSv2.1 32.25**（SD3-Medium 30.91、PixArt-Sigma 31.47、SD-XL 30.06）双榜第一，同时延迟最低 0.8s。人评 side-by-side（Fig.5）在整体质量/prompt following/视觉美学三维都更受偏好；摘要给出对 SD3-Medium **66% 人评胜率**。

**模型 ZOO 汇总（README）**：Infinity-2B@1024 GenEval 0.69/0.73†、DPG 83.5、HPSv2.1 32.2；**Infinity-8B@1024 GenEval 0.79†、DPG 86.6**；Infinity-20B "Coming Soon"。

**Scaling 结论（核心消融）**：
- **词表 scaling（Fig.9）**：小模型（125M/361M）Vd=2^16 收敛更快更好；放大到 2.2B 后，**Vd=2^32 在 40K iters 后反超 2^16** → 词表要随 transformer 一起放大。
- **模型 scaling（Fig.10）**：125M→4.7B，验证 loss 随模型尺寸/训练步数平滑下降；验证 loss 与 GenEval/ImageReward/HPSv2 高度负相关，**Pearson 相关系数 −0.983 / −0.981 / −0.979**（近乎线性），即 validation loss 是整体性能的强预测器——为继续 scale 提供依据。

## 创新点与影响
**核心贡献**：
1. **比特级建模（bitwise modeling）范式**：把 VAR 的 index-wise 离散 token 全链路换成 bitwise，理论词表扩到 2^64，使离散 tokenizer 重建质量首次追平/反超连续 VAE，打破"离散自回归细节差"的长期瓶颈。
2. **Infinite-Vocabulary Classifier**：用 d 个并行二分类器替代 2^d 类大分类器，参数从指数级降到线性级（省 99.95%），既解决大词表算不动，又把"模糊的 index 监督"变成"稳健的 bit 监督"。
3. **Bitwise Self-Correction**：零额外开销地修复 teacher-forcing 训练-推理失配，让模型具备自动纠错能力，是 AR-T2I 质量大跃升（FID 9.76→3.48）的关键，也使推理可用大 CFG、抛弃 pyramid-CFG。
4. **首个在 GenEval/DPG/ImageReward/HPSv2 多基准上超越主流扩散（SD3-Medium/SDXL/DALL-E 3）的离散自回归 T2I**，且是当时最快 T2I，并验证了清晰的视觉生成 scaling law。

**影响**：CVPR 2025 Oral；推动 next-scale / VAR 路线在高分辨率高质量 T2I 上的可行性，证明"离散自回归 = 又快又好"的可能；衍生开源生态——BitVAE（tokenizer 训练代码）、Infinity-8B、InfinityStar（基于 VAR & Infinity 的文生视频，2025-11）、后续 GRN（2026 提出"非扩散非自回归的第三条路"）。为"统一 tokenizer 建模 / 离散生成社区"提供新方向（作者称之为 'infinity' 的新可能）。

**已知局限**：训练 infra 细节（算力规模、并行、精度、总数据量与配比）披露有限；纯离散自回归对 tokenizer 质量高度依赖；prompt-rewriter 对 GenEval 分数有明显加成（0.69→0.73），裸 prompt 下与最强扩散差距更小；论文聚焦 T2I，未覆盖编辑/可控生成。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2412.04431
- arxiv_pdf: https://arxiv.org/pdf/2412.04431
- github: https://github.com/FoundationVision/Infinity
- project_page: https://foundationvision.github.io/infinity.project/
- hf_weights: https://huggingface.co/FoundationVision/infinity
- tokenizer(BitVAE): https://github.com/FoundationVision/BitVAE

## 本地落盘文件
- ../../../sources/omni/2024/arxiv-2412.04431.pdf
- ../../../sources/omni/2024/infinity-bitwise-var--readme.md
- ../../../sources/omni/2024/infinity-bitwise-var--project-page.md
