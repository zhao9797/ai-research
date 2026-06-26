---
title: "CogView2: Faster and Better Text-to-Image Generation via Hierarchical Transformers"
org: "Tsinghua / BAAI"
country: China
date: "2022-04"
type: paper
category: t2i
tags: [autoregressive, hierarchical-transformer, bilingual, vqvae, super-resolution, masked-generation, lopar, coglm]
url: "https://arxiv.org/abs/2204.14217"
arxiv: "https://arxiv.org/abs/2204.14217"
pdf_url: "https://arxiv.org/pdf/2204.14217"
github_url: "https://github.com/THUDM/CogView2"
hf_url: "https://huggingface.co/spaces/THUDM/CogView2"
modelscope_url: ""
project_url: ""
downloaded: [arxiv-2204.14217.pdf, cogview2--readme.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
CogView2 是清华/BAAI 在 2022 年提出的中英双语自回归文生图系统：用一个 60 亿参数的跨模态通用语言模型 CogLM 预训练，再分层（低分辨率自回归 → 直接超分 → 局部并行自回归迭代超分 LoPAR）生成 480×480 图像，把高分辨率生成的模型前向次数从 3,600 降到 6（约 1/600），整体比初代 [[cogview]] 快约 10×，并在 MS-COCO 模糊 FID 上达到当时可比方法中的最好结果，质量逼近同期 DALL·E-2。

## 背景与定位
2022 年文生图主流是大规模自回归 transformer（[[dall-e-1]]、[[cogview]]）按光栅扫描顺序逐 token 生成图像 token。论文指出这条路线有三大缺陷：
1. **生成慢**——逐 token 自回归即使缓存隐状态也无法利用 GPU 并行，比同 FLOPs 的 GAN 慢得多；
2. **高分辨率训练昂贵**——transformer 注意力对序列长度 n 是 O(n²) 时空复杂度，预算受限下只能取 32×32 token（≈256×256 像素），远低于真实照片密度；
3. **单向性**——光栅顺序使模型生成时看不到右/下文，无法做文本引导填充（infilling），也与 MAE/SimMIM 这类双向掩码 ViT 之间产生鸿沟。

CogView2 用**统一的跨模态掩码预训练 + 分层生成**同时解决这三点：预训练时引入掩码补丁预测使模型具备双向上下文能力（→ 适配双向超分）；分层设计使高分辨率只需关注局部一致性（→ 可用局部注意力降本）；局部并行自回归（LoPAR）把超分阶段的前向次数从数千降到个位数（→ 大幅提速）。它是 CogView 系列从"纯自回归原型"迈向"开源高分辨率双语 T2I 系统"的关键一跳，作者明确把自己定位为在自回归路线内对抗当时正在崛起的扩散模型（[[glide]]、[[dall-e-2]]）。

## 模型架构
**Backbone（CogLM，6B）**：带 Sandwich-LayerNorm（沿用 [[cogview]]）的标准 transformer，**60 亿参数 = 48 层 / hidden 3072 / 48 注意力头**。序列长度 512 = 400 图像 token + 1 分隔符 [BOI] + 至多 111 文本 token。整套 CogView2 系统按 README 描述为 **6B-9B-9B**（预训练 CogLM 6B + 两个超分模块各约 9B；超分模块由 CogLM 微调而来，编解码共享大部分权重）。

**CogLM（Cross-Modal general Language Model）的核心机制**：输入是文本+图像 token 的拼接序列，按多种策略采样 k 个掩码区域 R。掩码**不替换输入 token**，而是构造注意力掩码矩阵 A——掩码外的 token 是 context，可被所有 token 注意；掩码内的 token 只能被其后、且同属掩码区域的 token 注意（图 2 中所有掩码 token 的行列共同构成下三角注意力）。只对掩码区域内"倒数第二个起"的 token 计损失（逐 token next-token 预测）。两种采样策略统一了三类任务：
- 掩全部图像 token → 文生图 GPT（同 CogView）；
- 掩随机补丁 + 文本 token → 掩码预测 + 图像描述（类 MAE 的填充 + captioning）；
- 掩文本 token → image captioning。

相对 GPT 的优势是引入双向上下文；相对 GLM 的优势是简单（GLM 需插入哨兵 token、改 token 顺序、新增位置编码，会破坏图像 2D 空间结构、无法用 2D 局部注意力）；相对 MAE 的优势是 decoder-only 更省参数且天然支持生成。**Infilling 技巧**：CogLM 训练时每个掩码区域首 token 不被预测，推理时把每个掩码区域前的最后一个 context token 移入区域内即可补全（代价是不能复用前一区域的缓存隐状态，多区域填充略慢）。

**Visual tokenizer（icetk 内的图像 VQVAE）**：20,000 码本的第一阶段 VQVAE（码本约为 DALL·E/CogView 的 3 倍）。损失 = L1 + MS-SSIM + 感知损失（perceptual loss），论文发现感知损失才是 VQGAN 纹理优于普通 VQVAE 的主因，但纯 VQGAN 在人脸等关键元素上偶有坏例，故折中用 VQVAE + 感知损失。还做了**多压缩率设计**（4²/8²/16²×，共享码本与低层参数；CogView2 实验只用 8²×：160²→20²、480²→60²），架构基本沿用带自注意力的 VQGAN，在 ImageNet 上训练到收敛。

**Text encoder / tokenizer**：无独立文本编码器；文本与图像同序列输入 transformer。统一 tokenizer **icetk**：词典 150,000，前 20,000 是图像 token，其余约 130,000 是文本 token（基于 sentencepiece unigram 在 25GB 半中半英语料上训练，显式分为 common/英文/中文/special 四类，可用采样掩码指定生成语言，实现双语可控）。

**分层生成三步**（CogView2 系统）：
1. 预训练 CogLM 生成一批 **20×20 token（160×160 像素）** 低分辨率图，按 captioning 困惑度（CogView 的 post-selection）过滤坏样本；
2. **直接超分**模块把 20×20 → **60×60 token**：CogLM 微调成 encoder-decoder，encoder 吃 20×20 token，decoder 吃 60×60 个 [MASK]，**不加 cross-attention**，而让 decoder token 同时注意 decoder/encoder 的局部 token（cross-resolution 局部注意力，自定义 CUDA 核）；实践中只微调 decoder 注意力层权重，其余参数 encoder/decoder 共享以省显存。此步是逐 token 独立的边际分布采样，纹理不一致、缺细节；
3. **迭代超分（LoPAR）**：把 CogLM 微调成 60×60 序列上的 BERT 式掩码预测模型（局部注意力），重掩 75% token 并以局部并行自回归方式重生成，得到细节一致的 **480×480 像素** 终图。

## 数据
- **预训练数据**：约 **3,000 万 文本-图像对**，大部分与 [[cogview]] 重叠。从 CogView 数据中**用关键词（如 "abstract"、"texture"）过滤掉约 500 万对**（多为设计用重复纹理背景图，对文生图贡献小），再**补入约 500 万 tag-图像对**。
- **双语**：约一半文本由英文翻译而来，中英文本都保留以训练双语 CogLM；训练时对双语样本随机选一种语言。
- **超分训练数据**：只用分辨率 **≥ 480×480** 的图像训练超分模块。
- **tokenizer 语料**：icetk 文本侧基于 25GB 纯文本（半英半中）。图像 tokenizer（VQVAE）在 ImageNet 上训到收敛。
- 数据量对比：论文称 CogView2 训练用的总数据**仅约为 DALL·E-2 的 5%**。

## 训练方法
- **训练目标**：统一为 **CogLM 的掩码区域内 next-token 自回归预测**（公式 2，按掩码区域归一化的交叉熵），通过不同掩码采样策略覆盖文生图/掩码填充/captioning。
- **掩码策略**：每个训练样本随机选一种策略。掩码预测策略沿用 SimMIM 结论——随机采样 4×4 token 补丁直到 **75% token 被掩**。
- **预训练超参**：6B CogLM，FP16，**batch size 4,096，训练 300,000 步**，序列长 512。
- **超分微调**：直接超分模块只微调 decoder 注意力层；迭代超分模块微调 **20,000 步** 成 BERT 式掩码预测，训练时掩码率从 {0.2, 0.4, 0.6, 0.8, 0.9} 采样；推理时局部窗口 σ=6，把 2σ−1 次迭代压缩并合并首末迭代到 **6 次迭代**完成（靠手工设计的 6×6 排布矩阵）。
- **三个即插即用 trick**（第 4 节）：
  1. **Cluster Sampling（聚类采样）**：20,000 图像 token 用 K-means 按 VQVAE 向量聚成 500 簇，先按簇内概率和 top-k 采样选簇、再簇内采样，解决大码本下 top-k 把大量近似 token（如 ~42 个"白色"token）误截断的"不完全截断"问题。
  2. **Local Attention（局部注意力）**：自定义 CUDA 核支持 2D 局部注意力 / 2D 自回归局部注意力 / 跨分辨率局部注意力，超分用 9×9 感受野；矩阵乘省一半计算、自回归不需因果掩码，**自回归场景下比全局注意力快至多 40×、显存仅 1%**（4,096 序列）。
  3. **Upweighting Textual Attention（上调文本注意力）**：给所有 token 指向文本 token 的注意力分数加常数 c（公式 7），几乎零成本地增强图文相关性，c<3 不损画质。
- **加速核心（LoPAR）**：基于"分层后无需全局依赖、保留 25% 随机 token 即可恢复全局场景（取自 MAE 的比例）"的假设，超分内不同局部窗口可并行生成，并按对角线分批迭代以避免相邻 token 同时生成造成的局部不一致。最终把高分辨率生成的模型运行次数从 **3,600 降到 6（仅 1/600）**。
- 论文未使用扩散 / flow matching；无 RLHF/DPO/偏好对齐；无蒸馏（提速靠并行解码而非步数蒸馏）。

## Infra（训练 / 推理工程）
- **算力**：由 BAAI 提供计算资源；论文**未披露**具体 GPU 数量、GPU·时或集群规模。仅给出训练配置（6B 模型、batch 4,096、30 万步、FP16）。
- **精度/并行**：FP16 训练；具体并行/分布式策略未在正文披露。代码基于 **SwissArmyTransformer（SAT v0.2）** 库实现。
- **自定义 CUDA 核**：为 2D / 跨分辨率局部注意力专门写了 CUDA kernel（图 6 在单头 hidden=64、A100 上 benchmark：局部注意力 vs 全注意力 vs PyTorch unfold/im2col 实现），是降低高分辨率训练与推理成本的工程关键。
- **推理部署**：官方建议用 **A100 GPU**；提供 `--only-first-stage`（仅 20×20 第一阶段）以在弱 GPU 上跑；需编译 Image-Local-Attention CUDA 核（不编译则只能跑第一阶段）。HuggingFace Spaces / Replicate 提供 Web Demo。模型权重托管在 BAAI model 站（coglm / cogview2-dsr / cogview2-itersr 三个文件夹）。
- **推理加速**：核心是 LoPAR 把超分前向从 3,600 次降到 6 次 + 局部注意力核，使 CogView2 比带滑窗超分的 CogView 快约 **10×**（生成相近分辨率且质量更好的图）。

## 评测 benchmark
**机器评测（MS-COCO，下采样回 256×256 比较；报告"模糊 FID"FID-0/1/2/4/8 与 IS）**。论文强调 FID 对 CogView2 不完全公平（优势在高分辨率却要 resize 回 256；英→中翻译有误差；训练数据多单物体，与 COCO "context 中常见物体"分布不同）。表 1 关键数字：

| 模型 | FID-0 | FID-2 | FID-8 | IS |
|---|---|---|---|---|
| CogView [[cogview]] | 27.1 | 13.9 | 23.6 | 18.2 |
| DALL·E | 27.5 | — | — | 17.9 |
| LAFITE | 26.9 | — | — | 26.0 |
| Make-A-Scene* | 7.55 | — | — | — |
| DALL·E-2 | 10.9 | — | — | — |
| **CogView2** | **24.0** | 16.8 | 17.2 | 22.4 |
| **CogView2\*（COCO 微调）** | **17.5** | 10.9 | 10.4 | 25.2 |

（`*` 表示在 MS-COCO 上微调；FID-k 为对图像做 k 级模糊后的 FID。）论文结论：**CogView2 在所有可比方法中取得最佳"模糊 FID"**；COCO 微调能把 FID-0 从 24.0 持续降到 17.5（0→2,500→7,500 步：24.0→19.2→17.5），但**人评质量反而下降**——微调后模型拟合了 COCO 复杂场景风格，而标注者更偏好原模型生成的孤立主体样本。

**消融（表 1，"– technique"）**：去掉 cluster sampling、去掉 attention upweighting 后 FID 均变差（两项均带来提升，具体行对应 36.4 / 24.6 等更高 FID 值，证明两 trick 有效）。

**人评**：按 CogView 设置做大规模人评，共 **4,600 组** COCO caption 对比，对象含 DF-GAN、LAFITE、CogView、CogView2（含 COCO 微调版）及 VQVAE 恢复的 ground truth（CogView2 的 VQVAE 更强、是更强上界）。结果（图 7）：**CogView2 在所有维度上表现最好**；有趣的是 COCO 微调版虽 FID 更好但人评更差。

**速度**：高分辨率生成模型运行次数 3,600 → 6（1/600）；整体比 CogView（滑窗超分）快约 10×；局部注意力核在 4,096 序列自回归场景最高快 40×、显存 1%。

**对比 DALL·E-2**：同期工作（1024×1024），与 CogView2 共享"分层生成"思想；CogView2 仅用约 5% 数据即可合成相似场景（如"lion teacher" vs DALL·E-2 的"panda scientist"）。DALL·E-2 多了第三级超分和"零级"图像先验，作者把三级超分留作 future work。

## 创新点与影响
**核心贡献**：
1. **CogLM**：一个统一文本+图像的跨模态通用语言模型预训练范式，用注意力掩码（不改输入 token）同时覆盖文生图、双向掩码填充、image captioning，兼具自回归一致性与双向上下文理解，且 decoder-only 省参、保留 2D 空间结构以便用局部注意力。
2. **分层生成 + LoPAR**：低分辨率自回归 → 直接超分 → 局部并行自回归迭代超分，把高分辨率自回归的速度短板（3,600→6 次前向）基本抹平，使纯自回归路线在 2022 年仍能与扩散模型在速度上一较高下。
3. **工程 trick**：cluster sampling（解决大码本不完全截断）、自定义 2D/跨分辨率局部注意力 CUDA 核、上调文本注意力增强图文相关性；以及加感知损失 + 多压缩率的 VQVAE 图像 tokenizer。
4. **双语 icetk tokenizer**：150K 统一中英+图像词典，可控语言生成，是中文/双语开源文生图的重要基建。

**影响**：CogView2 是 CogView → [[cogview3]] → CogVideo/[[cogvideox]] 这条 THUDM 多模态生成线的承上启下之作；CogLM 的"统一掩码语言模型"思路、LoPAR 的"分层+局部并行解码"提速思路、icetk 双语 tokenizer 都被后续工作沿用。它也代表了"自回归 vs 扩散"路线之争中自回归阵营在 2022 年的高水位线（此后 CogView3 等转向扩散/中继扩散）。

**已知局限**：FID 评测对其高分辨率优势不友好；COCO 微调提升 FID 却降人评质量，暴露 FID 与人类偏好脱节；小区域文本引导填充时模型倾向只顾上下文一致而忽略文本（需放大区域再填充+超分的工程补救）；只做到 480×480（未做 DALL·E-2 式三级超分到 1024）；训练算力/分布式细节未公开；英文输入质量逊于中文（README 明示 "Chinese input is usually much better than English input"）。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2204.14217
- arxiv_pdf: https://arxiv.org/pdf/2204.14217
- github: https://github.com/THUDM/CogView2
- hf_demo: https://huggingface.co/spaces/THUDM/CogView2
- model_weights: https://model.baai.ac.cn/model-detail/100041
- replicate_demo: https://replicate.com/thudm/cogview2

## 一手源存档（sources/）
- [arxiv-2204.14217.pdf](https://arxiv.org/pdf/2204.14217)  （arXiv 原文 PDF，不入 git）
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2022/cogview2--readme.md)
