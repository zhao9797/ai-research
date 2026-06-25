---
title: "X-Omni: Reinforcement Learning Makes Discrete Autoregressive Image Generative Models Great Again"
org: 腾讯混元 (Tencent Hunyuan X)
country: China
date: 2025-07
type: paper
category: unified
tags: [unified, autoregressive, discrete-token, rl, grpo, text-rendering, image-generation, image-understanding, tokenizer, siglip, flux]
url: https://arxiv.org/abs/2507.22058
arxiv: https://arxiv.org/abs/2507.22058
pdf_url: https://arxiv.org/pdf/2507.22058
github_url: https://github.com/X-Omni-Team/X-Omni
hf_url: https://huggingface.co/collections/X-Omni/x-omni-models-6888aadcc54baad7997d7982
modelscope_url:
project_url: https://x-omni-team.github.io
downloaded: [arxiv-2507.22058.pdf, x-omni--readme.md, x-omni--hf-en-card.md, x-omni--project-page.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
X-Omni 是腾讯混元 X 团队提出的**统一离散自回归多模态模型**：用一个 7B 语言模型（Qwen2.5-7B）对图像与文本 token 做同质的「next-token prediction」，并证明**强化学习（GRPO）能显著修复离散自回归图像生成长期存在的低保真、畸变、指令跟随差的痼疾**——RL 训练 200 步即超过 SFT + best-of-N，在 DPG-Bench 上 87.65 取得统一模型 SOTA，并成为**首个能精确渲染长文本（中英）的统一模型**，且**无需 CFG** 即可保持高质量。

## 背景与定位
- **要解决的问题**：把语言建模的「next token prediction」范式搬到图像，本应得到天然统一的图文模型，但离散自回归图像生成（iGPT/DALL-E→[[chameleon]] [[emu3]]）一直被三大问题困住——视觉保真度低、输出畸变、复杂指令（尤其文字渲染）跟不住。论文归因为两点：自回归推理的**累积误差（cumulative error）**，以及离散量化造成的**信息损失**。
- **领域现状**：正因这个困难，主流转向「图像走 diffusion 目标 + 语言走 AR 目标」的混合路线（[[bagel]] [[blip3-o]] [[show-o2]] [[omnigen2]] [[metaqueries]]），论文认为这反而加剧了跨模态建模的「mismatch」，使统一性被牺牲。
- **本文主张**：回到**纯离散自回归统一框架**，核心洞见是 **RL 能修复 AR 的局限**——配合精心设计的 reward，RL 在整个采样过程提供监督，降低累积误差，并让 AR 产出的 token 分布**对齐离散扩散解码器的期望分布**（弥合 SFT 阶段 tokenizer 与 decoder 各自独立训练带来的 distribution gap）。
- **相对前作的改进**：相比 LaViT（重建 EVA-CLIP 语义特征后接 diffusion decoder）存在「AR 生成 token 与训练 decoder 用的 GT token」之间的分布鸿沟，X-Omni 用 RL 主动对齐这个鸿沟；相比 Emu3/Janus-Pro 重度依赖 CFG，X-Omni 不依赖 CFG。

## 模型架构
三大组件：**SigLIP-VQ 语义图像 tokenizer + 统一自回归模型 + 离线扩散解码器**。

**1) 图像 tokenizer（SigLIP-VQ，冻结）**
- 不用像素重建目标，而是在**视觉理解任务**上训练 tokenizer，使 token 保留丰富语义。
- 视觉语义编码器选 **SigLIP2-g ViT**（[[siglip]] 系列）；在其上加 **vector quantizer**：codebook 词表 **16,384**、维度 **2,048**；VQ 与 LLM 之间用一个 **residual block 作 adapter**，并与一个预训练 **Qwen2.5-1.5B** 对齐做视觉理解。
- 视觉编码器 + VQ 合称 **SigLIP-VQ**；在后续所有训练阶段**全程冻结**，保证 tokenization 稳定一致。

**2) 自回归模型（Qwen2.5-7B 为底座）**
- 为给纯文本 LLM 注入视觉感知，在原 transformer 层**前后各插入 4 个随机初始化的 vision-specific block**（结构同标准 transformer block，但**只作用于图像 token，不影响文本 token**）；并为图像 token 新增随机初始化的 embedding 层与分类头。
- 这种改造「不引入额外基础设施复杂度」，完全兼容 tensor / pipeline / context parallel 等分布式策略。
- 视觉 token 与语言 token 拼成统一多模态序列做 next-token 预测：**理解任务只监督语言 token，生成任务只监督视觉 token**。
- 任意分辨率支持：在视觉 token 前加分辨率前缀，格式为
  `language tokens <SOM> height width <Image> visual tokens <EOM> language tokens`，其中 height/width 是表示 2D 图像尺寸的文本 token，`<Image>` 后接 `height×width` 个展平图像 token。位置编码沿用原 LLM 的 **1D RoPE**，**不加 2D 位置编码**。

**3) 扩散解码器（FLUX.1-dev 为底，离线）**
- 选用预训练好的扩散模型 **[[flux-1]].1-dev** 作视觉 decoder，从离散语义 token 重建像素：加一个 linear 层把语义 embedding token 映射到 FLUX.1-dev 的特征通道维，并注入其中间层特征；以**图像重建**为目标训练 decoder。

**关键设计取舍**：理解与生成共享同一套 token / 同一网络，相比依赖异构图像编码器的方案（[[janus-pro]] [[bagel]] [[metaqueries]]），多轮图文交错时**无需对生成图重新抽语义 embedding**，架构更精简高效。

## 数据
**预训练（生成 + 理解混合）**
- **图像生成数据**：开源 COYO-700M、DataComp-1B、LAION-2B，经自研 filter 收集约 **200M 高质量图**；因原始 caption 噪声大、信息少，用 **Qwen2.5-VL-72B** 重新生成 **dense caption**（re-captioning）。所有图按原比例 resize 到短边 384、长边最大 1152。tokenize 后图像生成数据共 **600B 多模态 token**。
- **图像理解数据**：**59M** 数据，含 LLaVA-OneVision、BLIP3-KALE、Infinity-MM；同样 resize 策略，产出约 **100B 多模态 token**。

**SFT**
- 30K 来自 BLIP3o-60k 的高质量数据 + 30K 合成 text-to-image 数据 + 从预训练集过滤出的高质量 token；并混入 LLaVA-NeXT、Cauldron、Cambrian-1 的理解数据。SFT 阶段共训 **1.5B token**。

**RL（GRPO，只需文本 prompt，图像由模型自生成）**
- 共 **180K prompt**，三类构成：① 从 midjourney 数据集随机采 **80K** 清洗后的 prompt（贴近真实用户分布）；② 文字渲染：对富文本图数据按文本长度分桶（bucket），每桶随机抽 10K，合计 **50K** text-rendering prompt；③ 从自然图数据随机采 **50K** prompt（提升美学与指令跟随）。

## 训练方法
**训练目标**：图像与文本统一用 **next-token prediction（离散 token 的自回归交叉熵）**，不是 diffusion / flow matching。扩散解码器单独以重建目标训练（离线、推理时冻结）。

**多阶段流程：预训练（3 阶段）→ SFT → RL**

预训练三阶段：
1. **阶段一**：只解冻随机初始化的 vision-specific block 与 vision token embedding，仅用生成数据。batch size 256、序列长 16,384、训 10K 步、共 **42B token**。
2. **阶段二**：放开自回归模型全部参数，生成 + 理解数据混训。同样 bs 256 / 序列 16,384，训 **150K 步、629B token**。前两阶段学习率恒为 **1e-4**。
3. **阶段三**：学习率退火（annealing），用从预训练集过滤的 **42B 高质量 token**。

SFT：只训自回归模型的可学习参数，bs 64、序列 16,384、共 **1.5B token**，学习率从 **1e-5 线性降到 0**；sequence packing 与预训练一致。

RL（核心创新）：
- 算法用 **GRPO**（Group Relative Policy Optimization，省去 critic 网络）。对每个 prompt 用旧策略 rollout 一组 G 条轨迹 → 固定扩散 decoder 解码成图 → reward 打分 → 组内归一化得 advantage → 带 clip 与 KL 正则的策略梯度优化。
- 超参：学习率 **1e-6**、**200 训练步**、batch size **512**、**每 prompt 16 个 rollout**、**KL 系数 β=0.01**、clip ε（论文给公式未给数值）。
- 中文文字渲染模型：在 RL 阶段某个**中间 checkpoint** 上加入中文数据继续训练得到（即 En / Zh 两个发布版本同源）。

**Reward 系统（加权聚合多分量）**——这是把效果做上去的关键：
- **Human Preference Score**：HPSv2 评美学与人类偏好（224×224）。
- **Unified Reward Score**：HPSv2 只支持 224×224，分辨率不够，故引入 Unified Reward 模型做高分辨率下的综合人类对齐打分。
- **Text-Image Alignment Score**：用 **Qwen2.5-VL-32B** 评图文语义一致性，抑制语义幻觉。
- **OCR Accuracy Score**：对需渲染文字的 prompt，用 **GOT-OCR2.0 + PaddleOCR** 联合评估渲染文字与 GT 的准确率。

**蒸馏/加速**：论文未涉及 consistency / LCM / ADD / 步数蒸馏等扩散加速；其推理「省算力」来自**不依赖 CFG**（少一倍 AR 前向）。

## Infra（训练 / 推理工程）
- **并行**：架构改造声明完全兼容 **tensor / pipeline / context parallelism**；vision-specific block 只动图像 token，不增加基础设施复杂度。
- **训练规模口径（token 数）**：预训练阶段一 42B + 阶段二 629B + 阶段三 42B；SFT 1.5B；RL 200 步（bs 512、16 rollout/prompt）。**具体 GPU 型号、卡数、GPU·小时、训练吞吐、混合精度策略均未披露**。
- **推理**：自回归采样**不使用 CFG**（既降算力，也表明视觉/语言 token 生成过程更一致）；采样用 min-p（README 给 `--min-p 0.03`、`--cfg-scale 1.0`）。扩散 decoder 走 FLUX.1-dev。**推理步数 / 缓存 / 量化等加速细节未披露**。
- **部署形态**：开源推理代码 + HF 权重（X-Omni-En / X-Omni-Zh / X-Omni-PT 预训练ckpt / X-Omni-SFT），并提供 HF Space 在线 demo；许可证 Apache-2.0。

## 评测 benchmark（把效果讲清楚）
数字均来自论文 Table 1–4（已落盘 arxiv-2507.22058.pdf）。

**文字渲染（Table 1，越高越好）**
- OneIG-Bench 文字渲染：X-Omni 英文 **0.901** / 中文 **0.895**。英文显著超过开源统一模型 [[bagel]](0.244) / OmniGen2(0.680) / Show-o2(0.002)，也超 GPT-4o(英文 0.857)。中文 0.895 超过绝大多数模型（OneIG 中文列 GPT-4o 仅 0.650），与商用专用文生图 Seedream 3.0(0.928) 接近。
- LongText-Bench（作者自建，160 prompt / 8 场景，侧重长文本）：英文 **0.900**（统一模型中显著领先，略逊 GPT-4o 0.956）；中文 **0.814**，**大幅超过所有其他模型**（GPT-4o 0.619、Seedream 3.0 0.878 为对照；在统一模型里第一）。
  > LongText-Bench 构造：GPT-4o 为 8 类文本场景各生成 20 prompt（10 短 + 10 长）后人工复核，评测用 Qwen2.5-VL-7B 做 OCR，长文本下用 **Text Accuracy** 而非 Edit Distance（OCR 不保证文段相对顺序），每 prompt 生 4 图取平均。

**文生图指令跟随**
- **DPG-Bench（Table 2）**：X-Omni Overall **87.65**，**统一模型 SOTA**——超过 GPT-4o(86.23)、Show-o2(86.14)、BAGEL(85.07)、OmniGen2(83.57)、Emu3(80.60)、Janus-Pro(84.19) 及生成专用 FLUX.1-dev(84.00)。分项 Entity 92.59、Relation 94.75 为该列最高；Attribute 90.63（略低于 BAGEL 91.29 / Show-o2 89.96）。
- **GenEval（Table 3，用 prompt rewriting）**：X-Omni Overall **0.83**，与近期统一模型相当（Mogao 0.89、BLIP3-o/UniWorld 0.84、BAGEL 0.88、OmniGen2 0.86、GPT-4o 0.84）；论文定位为「comparable」而非超越。分项 Single 0.98、Two 0.95、Counting 0.75、Colors 0.91、Position 0.71、Color Attr. 0.68。

**图像理解（Table 4，7B LLM）**
- POPE 89.3、GQA 62.8、MMBench 74.8、SEEDBench-Img 74.1、DocVQA 88.6、**OCRBench 704**。
- 与统一模型 Show-o2 相当，超过 Emu3、Janus-Pro；**OCRBench(704) 显著超过 Emu3(687)、Janus-Pro(595) 及理解专用 LLaVA-OneVision(622)**——印证语义 tokenizer（理解任务训练）对 OCR/文字能力的迁移增益。

**关键消融 / 发现**
- **RL > SFT + best-of-N**（Fig.2b）：RL 的 image-generation reward 很快超过 SFT 模型的 best-of-N（SFT BoN），且持续上升。与语言建模中「RL 难超 SFT+BoN」的经验相反，作者归因：① SFT 阶段 AR 与 diffusion 模块各自用 GT 独立训练导致退化，RL 对齐两者至关重要；② 图像特征是局部、空间复杂的，RL 的整体优化能利用一张图内多区域的丰富信息，学习更高效。
- **不依赖 CFG**（Fig.6）：X-Omni 在有/无 CFG 下质量一致；Emu3、Janus-Pro 去掉 CFG 后质量显著下降。论文所有定性图均**未用 CFG**。表明视觉与语言 token 生成过程一致性更高。
- RL 全程（Fig.2c）：从 SFT→RL-50→100→150→200 步，文字正确性、肢体畸变、指令跟随、美学逐步改善。

## 创新点与影响
**核心贡献**
1. **证明 RL 能「拯救」离散自回归图像生成**：用 GRPO + 多分量 reward（HPSv2 / Unified Reward / Qwen2.5-VL-32B 对齐 / GOT-OCR2.0+PaddleOCR）系统性修复累积误差与畸变，让纯离散 AR 路线重新具备竞争力——呼应标题「Great Again」，意在把研究注意力拉回离散 AR。
2. **真正同质的统一框架**：图文共用同一 next-token 范式、同一网络、同一套 token，多轮图文交错无需重抽语义特征，比异构 encoder 方案更精简；理解与生成能力可互相迁移（OCRBench 提升即一例）。
3. **首个能精确渲染长文本（中英）的统一模型**，并提出 **LongText-Bench**（160 prompt / 8 场景）填补长文本渲染评测空白。
4. **RL 对齐 AR↔扩散 decoder 的分布鸿沟**：把 SFT 时各自独立训练造成的 distribution gap 用 RL 主动闭合，是其无需 CFG 也能高质量的机理性解释。
5. **全面开源**：推理代码 + LongText-Bench + En/Zh/PT/SFT 权重（Apache-2.0），便于社区在预训练/SFT ckpt 上继续微调。

**影响**：为「统一多模态究竟该 AR-only 还是 AR+diffusion 混合」之争提供有力的 AR-only 证据，并示范了 RL（而非更难落地的扩散 RL）在生成模型上的可行路径；多分量 reward + GRPO 的配方对后续统一/文字渲染工作有参考价值。

**已知局限**
- 依赖外部预训练大件（SigLIP2-g、Qwen2.5-7B/1.5B、FLUX.1-dev、Qwen2.5-VL 系列 reward），并非完全自洽训练；GenEval 仅「comparable」而非领先，且需 prompt rewriting。
- 扩散 decoder 离线、tokenizer 全程冻结——质量上限受 FLUX.1-dev 与 SigLIP-VQ codebook(16384) 信息容量约束。
- **训练算力（GPU 卡数/小时）、推理加速细节、reward 各分量权重、CFG/clip ε 具体数值均未披露**。
- LongText-Bench 评测用 Qwen2.5-VL-7B 做 OCR，自评有一定循环依赖风险（reward 与评测都涉及 VLM/OCR 家族）。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2507.22058
- arxiv_pdf: https://arxiv.org/pdf/2507.22058
- github: https://github.com/X-Omni-Team/X-Omni
- project_page: https://x-omni-team.github.io
- hf_models: https://huggingface.co/collections/X-Omni/x-omni-models-6888aadcc54baad7997d7982 （X-Omni-En / X-Omni-Zh / X-Omni-PT / X-Omni-SFT）
- hf_dataset(LongText-Bench): https://huggingface.co/datasets/X-Omni/LongText-Bench
- hf_spaces: https://huggingface.co/collections/X-Omni/x-omni-spaces-6888c64f38446f1efc402de7

## 本地落盘文件
- ../../../sources/omni/2025/arxiv-2507.22058.pdf （论文全文，6 页正文 + 附录 + 参考，已精读）
- ../../../sources/omni/2025/x-omni--readme.md （GitHub 官方 README，含推理命令、超参、News）
- ../../../sources/omni/2025/x-omni--hf-en-card.md （HF X-Omni-En model card，指针型）
- ../../../sources/omni/2025/x-omni--project-page.md （项目主页快照，内容与论文 abstract 一致）
