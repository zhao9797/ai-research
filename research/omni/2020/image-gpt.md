---
title: "Generative Pretraining from Pixels (Image GPT / iGPT)"
org: OpenAI
country: US
date: "2020-06"
type: paper
category: method
tags: [autoregressive, pixel-transformer, generative-pretraining, representation-learning, gpt, unsupervised]
url: "https://openai.com/index/image-gpt/"
arxiv: ""
pdf_url: "https://cdn.openai.com/papers/Generative_Pretraining_from_Pixels_V2.pdf"
github_url: "https://github.com/openai/image-gpt"
hf_url: ""
modelscope_url: ""
project_url: "https://openai.com/index/image-gpt/"
downloaded: [image-gpt.pdf, image-gpt.txt, image-gpt--blog.md, image-gpt--readme.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
iGPT 把 **GPT-2 原封不动的自回归 Transformer 解码器直接套到「展平成 1D 序列的像素」上**（不引入任何 2D 卷积/相对注意力/2D 位置编码先验），用纯 next-pixel-prediction 做无监督预训练，证明序列生成模型既能采样出可识别物体的连贯图像、又能学到强视觉表征——在 CIFAR-10 上线性探针 **96.3%**（超过有监督 ResNet-152 与 SimCLR）、全量微调 **99.0%**（追平用 ImageNet 标签预训练的 GPiPe），是 [[dall-e-1]] 自回归图像生成路线的直接前身。

## 背景与定位
**要解决的问题**：无监督预训练在 NLP（[[gpt-2]]、BERT）已大获成功，但同一类「纯序列预测」模型一直没能在图像分类上产出有竞争力的特征；视觉自监督当时由对比学习（[[simclr]]、MoCo、CPC v2、AMDIM）和精心设计的 CNN 编码器主导。本文回到「生成式预训练」这一在 2000 年代被遗弃的老路，用现代架构（Transformer）+ 可tractable 似然目标 + 大算力（论文称 2048 TPU cores）重新检验它。

**核心论点**：作者把「Analysis by Synthesis」直接落到无隐变量的自回归模型上——如果一个足够大的 Transformer 能在下一像素预测上把数据分布建模得足够好（采样出有清晰物体的图），那它内部就一定编码了物体类别信息。论文用实验把「生成质量 ↑ ⇒ 表征质量 ↑」这条因果链坐实（Figure 3）。

**技术脉络中的位置**：
- 上承 PixelRNN/PixelCNN（Oord 2016）、Image Transformer（Parmar 2018）、Sparse Transformer（Child 2019）这条「自回归像素建模」线；
- 与 BigBiGAN（Donahue & Simonyan 2019，首个生成模型表征追平自监督）呼应；
- 关键创新是「**去先验、纯靠 scale 换掉手工领域知识**」——刻意不用卷积、相对/稀疏注意力、2D 位置编码，验证「在未知先验的新领域，堆算力 + 通用序列模型」这条路；
- 对后续影响：直接启发 [[dall-e-1]]（dVAE 离散化 + 自回归 Transformer 生成图像 token），并为「图像 = token 序列 → 用 LLM 范式统一处理」的统一多模态路线提供最早的概念验证。

## 模型架构
**backbone**：GPT-2 公式的 Transformer **解码器**，逐字复用 GPT-2 代码（官方 README 明说 fork 自 `gpt-2/src/model.py`，diff 仅含一个新激活函数、若干变量改名、引入一个 start-of-sequence token，**不改动模型架构本身**）。

**Pre-LN 残差块**（与 GPT-2 一致）：
- `n = layer_norm(h)`；`a = h + multihead_attention(n)`；`h_next = a + mlp(layer_norm(a))`——layer norm 前置于 attention 与 mlp，所有操作都在残差路径上，便于 scale。
- AR 目标用标准上三角因果 mask；BERT 目标无需 mask logit，而是把被 mask 位置在输入侧置零。

**关键架构决定（"去 2D 先验"）**：
- **唯一的跨序列混合只在 attention**；用**稠密（full）self-attention**，不用稀疏/局部/相对注意力。
- 学习**独立的 1D 位置编码**（每个序列位置一个），不注入任何 2D 空间结构——BERT 版因此是**置换不变**的（permutation invariant），空间关系全靠训练学出来；AR 版因 raster order 固定了条件分解顺序，不完全置换不变，但仍空间不变。
- 这与 CNN 的「特征应来自空间邻近元素」归纳偏置形成强烈对照。

**没有 visual tokenizer / VAE / VQ**：iGPT **不用学习型离散化器**。像素离散化靠固定的「9-bit 调色板」——把 (R,G,B) 三元组用 k-means（**k=512**，即 9 bit）聚类成 512 个颜色簇，每个像素 → 1 个 token（而非 3 个 RGB 通道 token），序列长度直接缩短 3 倍。注意：这一步打破了颜色通道的置换不变性，但保持空间置换不变性。这是与后来 [[dall-e-1]]（dVAE 学习 token）、[[vq-vae]] 路线的本质区别——iGPT 的「token」就是颜色簇 id。

**无 text encoder**：iGPT 是**纯像素无条件/半图条件**生成，没有文本输入，不涉及 T5/CLIP 文本编码器。

**分辨率策略（Input Resolution IR vs Model Resolution MR）**：因稠密注意力显存随序列长度平方增长，先把图 resize 到低**输入分辨率** IR ∈ {32²×3, 48²×3, 64²×3}，再经 9-bit 调色板压成长度为 **MR**（32²=1024、48²=2304、64²=4096）的 token 序列。即便 32² 也已相当吃算力。

**四档模型（参数量 / 层数 L / 嵌入维 d）**：
| 模型 | 参数量 | L | d | n_head |
|---|---|---|---|---|
| iGPT-S | 76M | 24 | 512 | 8 |
| iGPT-M | 455M | 36 | 1024 | 8 |
| iGPT-L | **1.4B**（表中记 1362M） | 48 | 1536 | 16 |
| iGPT-XL | 6.8B | 60 | 3072 | — |
（n_head 来自官方 README 采样命令；iGPT-L 与 GPT-2 几乎相同，仅 d=1536 vs GPT-2 的 1600。）
> 注：论文正文第 3.3 节把 iGPT-L 写成 "1.4M parameters" 是明显笔误——官方博客、ImageNet 线性探针表（1362M）均确认 iGPT-L 为 **1.4B**。

**特征抽取设计（论文亮点）**：与有监督模型「最好特征在倒数第二层」相反，iGPT 这类生成模型**最好的表征在网络中部**（Figure 2，呈强单峰）。作者解释为两阶段：前半段各位置从上下文聚合信息构建全局图像表征，后半段用该上下文特征解条件 next-pixel 任务——像在单一架构里隐式学出 encoder-decoder/bottleneck。线性探针取**中部某层 post-layernorm 的 attention block 输入、沿序列维平均池化**；微调则池化最后一层 `n_L`。

**初始化**：用 Sparse Transformer 的 layer-dependent 缩放初始化，对产出 logits 的投影做零初始化；token 嵌入矩阵与产 logits 矩阵解绑（untie）。

## 数据
- **主预训练集**：ImageNet **ILSVRC 2012 训练集**（约 1.28M 图），切 4% 作实验验证集，ILSVRC 2012 验证集作 test。**无标签**使用（纯生成预训练）。
- **iGPT-XL 额外数据**：在 ImageNet 之外**额外用 1 亿（100M）张无标签网络图像**，过滤到「与 ImageNet 相似」。博客明确 iGPT-XL 训于 ImageNet + web 图像的混合。
- **下游评测集**（带标签，仅用于探针/微调）：CIFAR-10、CIFAR-100、STL-10（忽略其 unlabeled 子集，因其本就是 ImageNet 子集）。
- **数据增强**：在 web 图像上预训练**不用任何增强**；在 ImageNet 上预训练/微调用轻量增强（短边 resize 到 [256,384] 随机区间 + 随机 224×224 crop；评测时短边 resize 224 + center crop）；CIFAR 全网微调用 Wide-ResNet 式增强（4px reflection pad + 随机 32×32 crop + 水平翻转）。
- **清洗/配比/美学过滤/re-captioning**：**未披露**细节（iGPT 是无条件像素生成，不涉及图文对、不涉及 caption；web 图像的「与 ImageNet 相似」过滤标准未给具体方法）。无安全过滤披露。

## 训练方法
- **训练目标**：两种二选一——
  - **自回归（AR）**：raster order 下最小化负对数似然 `L_AR = E[-log p(x)]`，逐 token 预测下一像素簇；这是主力（论文绝大多数结论基于 AR）。
  - **BERT 式**：随机 mask 15% 像素，从未 mask 像素预测被 mask 的（`L_BERT`）。
- **优化器/超参**：Adam，**β1=0.9，β2=0.95**（特意不用默认 0.999，否则训练出现 loss spike）。学习率从大到小**顺序搜索**（0.01→0.003→0.001→0.0003…），一旦最终验证 loss 开始上升就停；模型越大、可用学习率越低（更大模型在更低 lr 就出现不可恢复的 loss spike）。lr 先 warmup 一个 epoch，再 cosine 衰减到 0。**不用 dropout、不用 weight decay**（0.01 的 weight decay 不改变表征质量）。
- **训练规模**：iGPT-XL **batch 64、训 2M 步**；其余模型 **batch 128、训 1M 步**。各模型/目标/IR 的具体 lr 见论文 Table 5（如 iGPT-L AR @32²=0.001、@48²=0.01；iGPT-XL @64²=0.0003）。
- **iGPT-S 的小 trick**：用 float32（而非 float16）、解绑 token embedding 与 logit 矩阵、对产 token/class logits 的矩阵零初始化，均带来小幅表征质量提升，并推广到所有模型。
- **BERT mask 率消融**：15%（同 Devlin）最佳；20% 持平 15%；25/30/35% 更差。
- **下游适配（微调）**：在分类头基础上，发现**联合目标 `L_GEN + L_CLF`（生成 loss + 分类 loss）优于纯 `L_CLF`**（与 GPT-1 的发现一致）；分类头接在最后一层（虽更慢，但能用满深度，最终优于接中部）；微调 lr 通常比预训练小一个量级，需重新搜；早停防过拟合。
- **加速/蒸馏**：**无**。本文不涉及 consistency/LCM/ADD/步数蒸馏（那是后来扩散模型时代的话题）；采样是逐 token 自回归解码。
- **采样**：温度 1，**不用 beam search / nucleus sampling 等 trick**；half-image completion 直接续采另一半。

## Infra（训练 / 推理工程）
- **算力规模**：论文摘要/引言提 **2048 TPU cores** 量级的算力。博客给出可比口径——**iGPT-L 约 2500 V100-days**，而同等表现的 MoCo 只需约 **70 V100-days**（即 iGPT 为「用算力换手工先验」付出约 35× 的算力代价）。
- **iGPT-XL 训练被中断**：博客与论文脚注均说明，iGPT-XL 在 ImageNet 上的部分实验（线性探针之外）**因需迁移到不同超算设施而未跑完**，故 ImageNet 线性探针只报了 iGPT-XL 一项。
- **显存瓶颈与上下文压缩**：稠密注意力显存随序列长度平方增长——若 naive 训 224²×3 序列，注意力 logits 会比语言模型大数万倍、单层都放不进 GPU。故用两级压缩：① resize 到低 IR；② 9-bit 调色板把序列再缩 3 倍。即便如此 32² 仍很贵。
- **并行/混合精度/吞吐细节**：**未披露**具体并行策略（TP/PP/DP 配置）与吞吐数字。混合精度仅提到 iGPT-S 用 float32 略好（暗示大模型用 fp16）。
- **推理加速/量化/部署形态**：**未涉及**。开源仓库（TensorFlow 1.13）默认 8×GPU 采样/评测，提供 S/M/L 三档 checkpoint（131K/262K/524K/1M 步），不含 iGPT-XL（最大公开为 iGPT-L）。
- **复现锚点**：README 给出 iGPT-S/M/L 在 ImageNet 上的测试生成 loss 应为 **2.0895 / 2.0614 / 2.0466**（对应论文 Figure 3），可用于校验复现。

## 评测 benchmark（把效果讲清楚）
**评测方式**：① 线性探针（取最佳中间层特征 + 逻辑回归/L-BFGS/SGD）；② 全量微调。注意 iGPT 不报 FID/IS——它的「生成质量」靠**验证集 next-pixel 负对数似然（论文 Figure 3 的 "validation generative loss"；README 给出 iGPT-S/M/L 测试值 2.0895/2.0614/2.0466，论文未标注单位）** + 定性样本衡量，分类指标才是其表征质量的主量尺。

**CIFAR / STL-10 线性探针（iGPT-L 32×32，1536 特征）— SOTA**：
| 数据集 | iGPT-L | 次优非 iGPT |
|---|---|---|
| CIFAR-10 | **96.3** | 95.3 SimCLR (8192 特征) / 94.0 ResNet-152 |
| CIFAR-100 | **82.8** | 80.2 SimCLR |
| STL-10 | **95.5** | 94.2 AMDIM-L |
（三个数据集上，对 iGPT-L 特征拟合的线性分类器**全面超过 WideResNet 的端到端有监督训练**。）

**全量微调**：
- CIFAR-10：**99.0%**（追平用 ImageNet 标签预训练的 GPiPe；超过 AutoAugment 98.5、SimCLR 98.6；脚注：用 JFT-300M 的 BiT-L 为 99.3）。
- CIFAR-100：88.5%（略低于 SimCLR 89.0、AutoAugment 89.3、EfficientNet 91.7）。
- ImageNet 32²：微调 66.3%（比线性探针 +6%）；48² 微调 72.6%（+7%）。论文称仍「略低于」Isometric Nets 70.2%（IR 28²×3）——注意此处是论文原文表述（"still slightly underperform"），尽管 72.6 在数值上高于 70.2，对比的是更低 IR 下的同档结果。
- **预训练价值量化**：ImageNet 48² 从随机初始化训分类目标，18 epoch 得 53.2%；预训练模型约 **1 个 epoch 就达到同样 53.2%**，最终高出随机初始化 **19.4%**。

**ImageNet 线性探针（最难设定，因不能在标准 ImageNet 分辨率训练）**：
| 方法 | IR | 特征维 | 参数 | Top-1 |
|---|---|---|---|---|
| Rotation | orig | 8192 | 86M | 55.4 |
| iGPT-L | 32² | 1536 | 1362M | 60.3 |
| BigBiGAN | orig | 16384 | 86M | 61.3 |
| iGPT-L | 48² | 1536 | 1362M | 65.2 |
| AMDIM | orig | 8192 | 626M | 68.1 |
| MoCo | orig | 8192 | 375M | 68.6 |
| iGPT-XL | 64² | 3072 | 6801M | 68.7 |
| SimCLR | orig | 2048 | 24M | 69.3 |
| CPC v2 | orig | 4096 | 303M | 71.5 |
| **iGPT-XL** | 64² | 3072×5 | 6801M | **72.0** |
| SimCLR | orig | 8192 | 375M | **76.5** |
（iGPT-XL 拼接 5 层共 15360 特征达 72.0%，超过 AMDIM/MoCo/CPC v2，但仍明显低于 SimCLR 76.5；iGPT-L 单档 65.2% 也超过 AlexNet。代价：参数与算力远高于对比方法。）

**低数据 CIFAR-10（仅线性探针，无增强/无微调）**：
| 模型 | 40 标签 | 250 标签 | 4000 标签 |
|---|---|---|---|
| Mean Teacher | — | 67.7 | 90.8 |
| MixMatch | 52.5 | 89.0 | 93.6 |
| **iGPT-L** | **73.2** | 87.6 | 94.3 |
| FixMatch CTA | **88.6** | 94.9 | 95.7 |
（用「每类 4 标签」即 40 标签时 73.2%，超 MixMatch 且方差更低；但仍显著低于 SOTA FixMatch。论文也坦承 iGPT-L 在 40 样本极低数据下会快速记忆训练集、泛化差，单纯微调仅 42.1%。）

**关键消融结论**：
- **生成 loss ↓ → 线性探针 acc ↑**（Figure 3，跨 65K/131K/262K/524K/1000K 检查点正相关）——「更好的生成模型学到更好的表征」是全文核心实证。
- **表征质量随深度呈单峰**（中部最好）；在 CIFAR-10 上取最后一层而非最佳层会掉 2.4%（恰是 baseline 与 SOTA 之差）。
- **AR vs BERT**：预训练后 AR 特征明显优于 BERT（线性探针 CIFAR-10 最佳层差 >1%、ImageNet 差 6%）；但**微调后 BERT 追平甚至略超**（BERT 全微调 CIFAR-10 98.6%、ImageNet 66.5% 略超 AR）。BERT 评测时需 mask 输入保持分布一致，采 5 个独立 mask 取众数预测可在 ImageNet 上再涨近 1%。

## 创新点与影响
**核心贡献**：
1. **把语言 GPT-2 一字不改地搬到像素序列**，证明「领域无关的通用序列 Transformer + 纯生成预训练」在视觉上既能采样出可识别物体的连贯图像、又能学到与顶级自监督 CNN 竞争的特征——为「用 LLM 范式统一处理任意模态」提供最早、最干净的概念验证。
2. **坐实「生成质量 ↔ 表征质量」因果链**，把 Analysis-by-Synthesis 推广到无隐变量自回归模型。
3. **9-bit 调色板**（k-means k=512 颜色簇）作为最朴素的「像素离散化」方案，把图像变成可直接喂 GPT 的 token 序列——直接启发 [[dall-e-1]] 用 dVAE 离散 token + 自回归生成。
4. **发现生成模型表征沿深度单峰**（最佳特征在中部），改变了「取倒数第二层特征」的惯例。

**对后续工作的影响**：
- 是 **[[dall-e-1]] 自回归图像生成路线的直接前身**（OpenAI 内部技术血脉：iGPT→DALL·E→…），也是「图像 token 序列 + Transformer」统一多模态生成范式的源头之一；
- 与同期 [[vit]]（ViT，2020-10）共同把 Transformer 推入视觉，但路线互补：ViT 走「图块 + 有监督/对比」判别路线，iGPT 走「像素 + 自回归生成」路线；
- 把「**用 scale 换手工领域先验**」这一 scaling 信条从 NLP 延伸到视觉。

**已知局限（论文/博客自陈）**：
- **算力极其昂贵**：iGPT-L ≈ 2500 V100-days，是同等 MoCo（70 V100-days）的约 35×；稠密注意力平方级显存使其无法在高分辨率训练。
- **只能处理低分辨率**（≤64²），远低于自监督 CNN 能吃的高分辨率；ImageNet 线性探针仍输 SimCLR。
- **需要超大模型**才能学到好表征（iGPT-L 参数是同等 ImageNet 方法的 2–3 倍）。
- 因此论文定位自己**主要是 proof-of-concept**，工程实用性（相对 CNN 自监督）尚不足。
- **偏见风险**：生成模型会继承训练数据偏见（如「科学家」补全偏男性），需关注数据公平性。
- 未来方向自指：高效注意力（局部/稀疏/LSH/多尺度）、领域无关多尺度 Transformer、重审 flow/VAE 等其他生成族的表征能力。

## 原始链接
- blog: https://openai.com/index/image-gpt/
- paper_pdf (V2): https://cdn.openai.com/papers/Generative_Pretraining_from_Pixels_V2.pdf
- paper_pdf (V1, ICML 2020): https://cdn.openai.com/papers/Generative_Pretraining_from_Pixels_V1_ICML.pdf
- github: https://github.com/openai/image-gpt

## 本地落盘文件
- ../../../sources/omni/2020/image-gpt.pdf （论文 V2 全文 PDF；.gitignore 排除，本地精读）
- ../../../sources/omni/2020/image-gpt.txt （PDF 转文本，全文）
- ../../../sources/omni/2020/image-gpt--blog.md （OpenAI 官方博客快照，cloakbrowser）
- ../../../sources/omni/2020/image-gpt--readme.md （GitHub 官方 README，含模型配置与复现锚点）
