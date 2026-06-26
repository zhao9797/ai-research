---
title: "ERNIE-ViLG: Unified Generative Pre-training for Bidirectional Vision-Language Generation"
org: "Baidu"
country: China
date: "2021-12"
type: paper
category: unified
tags: [text-to-image, image-captioning, autoregressive, vqgan, unified, chinese, baidu]
url: "https://arxiv.org/abs/2112.15283"
arxiv: "https://arxiv.org/abs/2112.15283"
pdf_url: "https://arxiv.org/pdf/2112.15283"
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: ""
downloaded: [arxiv-2112.15283--ar5iv-fulltext.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
ERNIE-ViLG 是百度 2021 年底提出的 **100 亿参数中文跨模态统一生成模型**：用同一个参数共享的自回归 Transformer，在 **145M 中文图文对**上同时学「文→图」与「图→文」两个方向，把图像离散化成 VQGAN token 后当成序列预测。它在 MS-COCO 文生图上拿到 **FID 7.9（微调）/ 14.7（zero-shot）**——zero-shot 比 DALL-E（120 亿参数）的 27.5 大幅领先 12.8，是文心一格（Wenxin Yige）和后续 [[ernie-vilg-2.0]] 的前身。

## 背景与定位
当时图文双向生成被割裂成两条技术栈：image captioning 走 encoder-decoder（LSTM/Transformer，如 [[oscar]]、Zhou et al. 2020），text-to-image 走 GAN（StackGAN、XMC-GAN）。GAN 路线难以生成多物体复杂场景。2021 年 [[dalle]]（OpenAI）和 [[cogview]]（清华/智谱）把文生图重新表述为「序列到序列」问题：先用 dVAE/VQ 把图像离散成 token，再让 Transformer 在文本 token 后**自回归**预测图像 token——本工作正是这条「离散 token + 自回归」路线在中文域、且**显式做双向统一**的代表。

ERNIE-ViLG 的差异化主张是：**双向统一建模**比单向更有利于跨模态语义对齐。它指出此前虽有 X-LXMERT（Cho et al.）、Huang et al. 2021 尝试统一两个方向，但都用**非自回归**采样生成图像（速度快但因丢弃 target token 间依赖而效果次优）。ERNIE-ViLG 坚持**两个方向都用自回归**，并额外提出文生图的**端到端联合训练**（让生成器和图像重建器联合优化，而非传统两阶段分离训练）。

## 模型架构
**统一 backbone**：单个 **48 层 Transformer encoder**，hidden 4096、64 个注意力头，约 **100 亿参数**，文→图与图→文**共享全部参数**。

- **图像离散化（visual tokenizer）**：先用 **VQGAN**（VQVAE 的增强变体，加对抗训练 + 感知损失，重建更清晰）。下采样因子 **f=8**、codebook 词表 **8192**；图像中心裁剪到 **256×256**，得到 **32×32 = 1024** 个离散视觉 token。
- **文本侧**：WordPiece tokenizer。
- **双向注意力掩码（UniLM/ERNIE-GEN 式）**：把视觉 token 序列和文本 token 序列拼接喂入。source token 之间全可见，target token 只能看 source 和自己左侧——靠**特定 self-attention mask** 在同一个共享模型里同时实现「编码器」和「解码器」两种语境。
  - 文→图：输入流 `[t1…tm, z1…zn]`，自回归预测图像 token，图像注意力模式与 DALL-E 相同。
  - 图→文：输入流 `[z1…zn, t1…tm]`，自回归预测文本 token；关键改动是**让作为 source 的图像 token 内部走双向注意力**（同行/同列/同卷积核内互相可见），而非单向。
- **稀疏注意力（借鉴 DALL-E）**：因视觉序列长（≥1024）算力/显存吃紧，第 i 层按 `i mod 4` 切换 **行注意力 / 列注意力**，最后一层用**卷积注意力**（kernel 11×11，同 DALL-E）。行列注意力实现为 block-wise。作者实测该稀疏实现训练**提速约 25%、省 50% GPU 显存**，且 loss 收敛与 dense 注意力一致，推理提速更显著。
- **文生图两阶段 vs 端到端**：传统两阶段是「生成器产 token → 查 codebook → 重建器还原图」，生成器和重建器**独立训练**。ERNIE-ViLG 提出**端到端**变体：把最后一层 Transformer 输出的图像 token hidden embedding **非线性映射**为 z_emb 直接送重建器，绕过不可导的 ID 查表，使梯度能从重建器反传到生成器——既给重建器更富语义、且带文本感知的特征，又用重建任务增强生成器。**注意：100 亿主模型因 GAN+大模型训练不稳定，最终仍用两阶段（VQGAN decoder 直接当重建器）**，端到端只在 300M 小模型消融里验证。

## 数据
**145M 高质量中文图文对**，三个来源：
- **中文网页 alt-text**：爬取 8 亿原始中文 alt-text-图像对，三步过滤后留 **70M**。过滤规则：(1) alt-text 词数 < 15；(2) 必须含至少一个名词且无特殊字符；(3) 用内部图文匹配模型打分（0–1），相似度 > 0.5 才留。
- **图像搜索引擎**：从内部图搜引擎收集约 **60M** query 文本 + 用户点击图（query 与点击图相关性强）。
- **公开数据集**：从 **CC（Conceptual Captions）+ CC12M** 取 **15M**，英文 caption 经 **百度翻译 API** 译成中文。

（注：未披露图像美学评分过滤、NSFW/安全过滤、去重等细节。）

## 训练方法
- **训练目标**：纯 **next-token 自回归**（非 diffusion、非 flow matching）。多任务损失 `L = L_txt2img + L_img2txt`，两个方向都是对各自 target token 的负对数似然求和（公式 3–5）。VQGAN 训练用标准 VQVAE 损失（重建 + codebook commitment，带 stop-gradient）。
- **图→文阶段**：量化模块（VQGAN encoder + codebook）**预训练后冻结**，只训生成 Transformer（作者称未来可联合更新）。
- **推理 / 采样**：文生图沿用 DALL-E 式采样，并用**内部对比学习图文匹配模型对候选重排**——zero-shot 取 best-of-60、微调取 best-of-10。
- **消融（端到端 vs 两阶段，300M lite 模型）**：用 24 层 / 1024 hidden / 16 头的 300M Transformer，图像离散化换成 dVAE（避开 GAN 不稳定），在 CC+CC12M 上训、MS-COCO zero-shot 评。结论：端到端 FID 39.9，两阶段 41.4，**提升 1.5**；且端到端对生成器、重建器各有独立增益（见下表）。
- **未披露**：偏好对齐（RLHF/DPO/reward model）、步数蒸馏/一致性蒸馏等——本工作是自回归生成，不涉及扩散加速；这些技术均**未报告**（也非该时期方法）。

## Infra（训练 / 推理工程）
基于 **PaddlePaddle（飞桨）** 平台训练 100 亿模型。核心挑战是设备显存与计算效率（双向结构使激活/梯度显存翻倍）。采用的工程组合：
- **Group Sharded 数据并行**（类 ZeRO）：把 optimizer states、梯度、参数分片到多卡消除冗余；论文图示「数据按列维度分片、模型状态按行维度分片，sharding 通信限制在同一台机器内」。
- **激活重计算（activation recomputation）** + **混合精度** 降显存提吞吐。
- **Optimizer-offload**：把分片的 optimizer states 和 master 参数换出到 **CPU**，再与**梯度累积**结合以降低 CPU-GPU 通信频率、提高计算效率。

**未披露**：具体 GPU 数量 / 型号 / GPU·小时 / 训练步数 / 吞吐 / 训练时长，以及推理量化、部署形态等——均**未报告**。

## 评测 benchmark
**文生图（MS-COCO，FID↓，30k 验证集随机采样、caption 经百度翻译成中文）**：

| 设置 | 模型 | FID↓ |
| --- | --- | --- |
| Zero-shot | DALL-E (12B) | 27.5 |
| Zero-shot | CogView | 27.1 |
| Zero-shot | **ERNIE-ViLG** | **14.7** |
| 微调（监督） | XMC-GAN | 9.3 |
| 微调 | NÜWA | 12.9 |
| 微调 | DF-GAN | 21.4 |
| 微调 | Huang et al. 2021（前向统一工作） | 29.9 |
| 微调 | X-LXMERT（前向统一工作） | 37.4 |
| 微调 | **ERNIE-ViLG** | **7.9** |

（表中数字均直接取自各模型原论文；ERNIE-ViLG 之外的完整榜含 AttnGAN 35.5、DM-GAN 32.6，此处略。）

- Zero-shot：比 DALL-E（120 亿参数）领先 **12.8 FID**，几乎追平全监督模型。
- 微调：MS-COCO **SOTA**，比最好的 Transformer 方法（NÜWA 12.9）降 **5.0**、比最好的 GAN 方法（XMC-GAN 9.3）降 **1.4**。前述两个「也尝试统一双向」的前作（X-LXMERT 37.4 / Huang et al. 29.9）因用非自回归采样，FID 远逊本工作的自回归方案——印证了「双向都用自回归」的主张。

**文生图人评（zero-shot，1–5 分，500 文本 best-of-60，对比 CogView）**：清晰度 4.221 vs 3.867、纹理 2.723 vs 2.623、文图相关性 2.641 vs 2.203——三项全胜。人评数据集 500 条覆盖 9 类（Appendix A 表 8）：MS-COCO 102、拟人动物/卡通角色 49、地理 50、多物体+属性+关系 68、单物体+属性 56、反事实 54、不同视角 43、不同风格 43、不同时间/场景 35；其中 102 条取自 MS-COCO 验证集，余皆人工设计。CogView 对比图由作者从其官网手动抓取。

**图像描述（image captioning，字符级）**：
- COCO-CN test：BLEU@4 50.0 / METEOR 31.6 / ROUGE-L 60.3 / CIDEr 138.2，全面超 seq-learn（48.4/29.5/59.2/128.4）。
- AIC-ICC val：BLEU@4 68.2 / METEOR 41.7 / ROUGE-L 72.5 / CIDEr 231.4，超 BriVL（66.1/.../220.7），BLEU@4 **+2.1**。
- 人评（COCO-CN 200 张，流畅/相关/丰富各 0–2）：微调模型均分 **1.62**；zero-shot 流畅度接近微调但相关性/丰富度差距明显（归因于网爬数据 caption 偏短不descriptive）。

**生成式 VQA（FMIQA，200 样本）**：图灵测试通过率 **78.5%**（vs mQA 64.7%，人标 94.8/97.5%），答案质量 1.495（vs mQA 1.454）——验证模型学到了跨模态语义对齐。

**端到端 vs 两阶段消融（300M，MS-COCO zero-shot FID↓）**：

| 生成器 | 重建器 | FID↓ |
| --- | --- | --- |
| 两阶段 G | 两阶段 R | 41.4 |
| 端到端 G | 两阶段 R | 40.5 |
| 端到端 G | 端到端 R | **39.9** |
| Gold 序列 | 两阶段 R | 21.7 |
| Gold 序列 | 端到端 R | **18.6** |

结论：端到端同时改善生成器（41.4→40.5）和重建器（最后两行 21.7→18.6），合计 FID 提升 1.5。

## 创新点与影响
**核心贡献**：(1) **首个把文→图与图→文都用自回归、且参数共享**的统一生成预训练框架（靠 UniLM 式 attention mask + 图像 token 在 img2txt 时走双向）；(2) **首个基于图像离散表示的端到端文生图训练方法**，让生成器和重建器联合优化、超越传统两阶段；(3) **首个 100 亿规模中文跨模态生成模型**，自建 145M 中文图文数据，在中文域把 DALL-E/CogView 路线做到 SOTA。

**影响**：ERNIE-ViLG 是百度 **文心一格（Wenxin Yige）** 文生图产品和 **[[ernie-vilg-2.0]]**（2022，转向扩散 + knowledge-enhanced + mixture-of-denoising-experts）的直接前身，是中文文生图大模型的早期里程碑；其「双向自回归统一 + 离散 token」思路也是后续 unified 生成模型（如 [[emu]]、[[chameleon]]、[[transfusion]]）讨论的脉络之一。

**已知局限**（作者自陈）：① 100 亿主模型因 GAN+大模型训练不稳定**未能用上端到端训练**，端到端只在 300M 小模上验证；② 量化模块冻结、未与生成器联合更新；③ MS-COCO 评测靠 best-of-N 重排（zero-shot best-of-60）拉高分数，单次采样质量未单列；④ 依赖内部图文匹配模型做数据过滤与重排，可复现性受限；⑤ 模型与数据均**未开源**。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2112.15283
- arxiv_pdf: https://arxiv.org/pdf/2112.15283
- ar5iv 全文 HTML（落盘来源）: https://ar5iv.labs.arxiv.org/html/2112.15283

## 一手源存档（sources/）
- [arxiv-2112.15283--ar5iv-fulltext.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2021/arxiv-2112.15283--ar5iv-fulltext.md)
