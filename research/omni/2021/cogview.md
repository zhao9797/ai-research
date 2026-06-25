---
title: "CogView: Mastering Text-to-Image Generation via Transformers"
org: "Tsinghua / DAMO Academy (Alibaba) / BAAI"
country: China
date: "2021-05"
type: paper
category: t2i
tags: [autoregressive, vqvae, transformer, gpt, text-to-image, chinese, fp16-stability, sandwich-ln, pb-relax]
url: "https://arxiv.org/abs/2105.13290"
arxiv: "https://arxiv.org/abs/2105.13290"
pdf_url: "https://arxiv.org/pdf/2105.13290"
github_url: "https://github.com/THUDM/CogView"
hf_url: ""
modelscope_url: ""
project_url: "https://wudao.aminer.cn/CogView/index.html"
downloaded: [arxiv-2105.13290.pdf, cogview--readme.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
CogView 是中文首个大规模自回归文生图模型——4B 参数的 GPT 风格单向 Transformer 学习「文本 token + VQ-VAE 图像 token」拼接序列的语言建模目标（即 [[dall-e-1]] 同期独立提出的同一思路），并首创 **PB-relax**（精度瓶颈松弛）与 **Sandwich-LN**（三明治层归一化）两个 trick 把 4B/8.3B 大模型的 FP16 训练从「千步内必 NaN」救活。在模糊化 MS COCO 上取得当时 SOTA FID（FID-2=13.9，优于 DALL-E 与 GAN 基线），是首个开源的大规模文生图 Transformer。

## 背景与定位
- **要解决的问题**：通用域（general-domain）文生图长期是开放难题，需要既强的生成模型又有跨模态理解。早期 GAN 路线（[[stackgan]]、AttnGAN、DM-GAN、DF-GAN 等）在 CUB 这类单域数据上尚可，但在 MS COCO 这类复杂通用场景上效果很差。
- **技术脉络中的位置**：纯像素级自回归（PixelCNN/PixelRNN、Image Transformer、ImageGPT）受限于一张图百万子像素的算力，最大只能做到 96×96。[[vqvae]] 把图像压成低维离散 latent，复活了 CV 中的自回归路线；Esser 等（[[vqgan]]）用 Transformer 拟合先验并把解码器损失从 L2 换成 GAN loss，大幅提升域内无条件生成质量。CogView 的核心思想顺理成章：**对文本 token + VQ-VAE 图像 token 做大规模生成式联合预训练**。
- **相对 DALL-E 的差异（论文自述四点）**：(1) 在模糊 MS COCO 上 FID 大幅超越 DALL-E 与 GAN，且是首个开源大文生图 Transformer；(2) 不止零样本生成，进一步探索微调下游任务（风格学习、超分、图像描述、图文重排序、工业时装设计）；(3) 微调出的 self-reranking 摆脱了 DALL-E 额外用的 CLIP，并提出新指标 Caption Loss；(4) 提出 PB-relax + Sandwich-LN 稳定大 Transformer 在复杂数据集上的训练，能消除 forward 溢出（NaN），让模型几乎全 FP16（O2）训练。

## 模型架构
**两阶段框架（VQ-VAE + GPT），从 VAE 的 ELBO 推导而来**——优化图像与文本联合似然的证据下界，等价于「无文本时退化为 VQ-VAE」的重解释。学习分两阶段：阶段一 encoder/decoder 只为重建损失优化（固定 φ、用 GPT 拟合先验，避免后验坍缩）；阶段二单个 GPT 优化文本 NLL 与图像 z 的 NLL 两项损失。

- **图像 tokenizer（离散自编码器，VQ-VAE stage 1）**：把 256×256×3 图像编码为 32×32 离散 token；codebook 大小 |V|=8192，embedding 维度 d=256，h=w=32。Encoder 是 4 层 CNN（512 隐藏单元、ReLU），前三层感受野 4、stride 2 逐层减半宽高，末层 1×1 卷积把通道压到 256；Decoder 对称（反卷积）。codebook 用 Xavier uniform 初始化。论文系统比较了四种 tokenizer 训练法（最近邻直通估计 / Gumbel 采样直通 / 最近邻移动平均 / 固定 codebook），发现 **L2 loss 曲线基本不分伯仲**——只要初始化得当，codebook embedding 的学习并不重要；预训练实际采用**移动平均**法。
- **文本 tokenizer**：在大规模中文语料上跑 SentencePiece，提取 50,000 个文本 token。
- **主干（backbone）**：单向 Transformer（GPT）。**48 层、hidden size 2560、40 个注意力头、共 4B 参数**。序列模板加 4 个分隔符 token：`[ROI1]`（图像参考文本）、`[BASE]`、`[BOI1]`（图像开始）、`[EOI1]`（图像结束），全部 clip/pad 到长度 **1088**。
- **条件注入**：不是 cross-attention 或 adapter，而是**纯序列拼接**——文本 token 在前、图像 token 在后，统一做自回归语言建模，文本天然成为图像生成的条件前缀。
- **训练目标与一个关键发现**：pretext 是左到右 token 预测（语言建模），图像与文本 token **同等对待**。DALL-E 建议降低文本 token 的损失权重；CogView 反而发现在小规模实验中**文本建模是文生图预训练成功的关键**——若把文本 token 损失权重置零，模型会找不到文图关联、生成与输入完全无关的图。作者假设文本建模在隐层中抽象出知识，供后续图像建模高效利用。

## 数据
- **规模与来源**：约 **3000 万** 高质量（中文）文图对，构成 2.5TB 新数据集（tokenize 后约 250GB），是 WudaoCorpora 项目的扩展。约 **50% 文本是英文**（含 Conceptual Captions），用机器翻译译成中文。
- **数据来源五类**（按占比）：(1) 专业图片网站（中英文，带 caption，占比最高）；(2) Conceptual Captions + ImageNet；(3) 在线新闻图片及其周边文本；(4) 阿里巴巴的少量商品-描述对；(5) 图片搜索引擎——为尽量覆盖常见实体，构建了 1,200 条 query（每条是从大规模知识图谱抽取的实体名，七大类：食物、地区、物种、人名、风景、产品、艺术作品；按英文维基出现频次取 top-k），对每条 query 抓各大搜索引擎返回的 top-100 图。
- **清洗与标注**：论文**坦白未去除水印和白边**，认为不影响研究结论（但承认会影响生成质量）。未提及美学过滤、安全过滤或 re-captioning（这与后来 [[dalle-3]] / [[playground-v3]] 等强调合成 caption 的工作形成对比；CogView 时代尚无此范式）。

## 训练方法
- **预训练**：batch size 6,144 序列（每 batch 670 万 token），训 **144,000 步**，用 512 张 V100（32GB）。Adam，max lr=3e-4、β1=0.9、β2=0.95、weight decay=4e-2；前 2% 步 warmup，cosine annealing 衰减。作者观察到**训练 loss 主要取决于训过的总 token 数**（tokens/batch × steps），加倍 batch（与 lr）在相同 token 数下 loss 几乎一致——故用大 batch 提升并行、降低通信占比。CogView 共训 **96B token**（论文用以解释为何比训了 56B token 的 DALL-E 更优）。
- **FP16 稳定化（本文最核心方法贡献）**：>2B 参数大模型通常依赖 16-bit；普通 pre-LN 4B Transformer 在 1000 步内就 NaN。DALL-E 用复杂的 per-resblock loss scaling + 把 gain/bias/embedding/unembedding 存 32-bit 来「容忍」数值问题；CogView 转而**规整数值**，识别出两类不稳定——溢出（NaN loss）与下溢（loss 发散）：
  - **PB-Relax（精度瓶颈松弛）**：溢出总发生在两个瓶颈算子。① 深层输出值可爆到 10⁴~10⁵ 使 LayerNorm 方差溢出，利用 `LayerNorm(x)=LayerNorm(x/max(x))` 先除最大值松弛；② 注意力分数 QᵀK/√d 可远大于输入，改计算顺序为 Qᵀ(K/√d)，并利用 softmax 平移不变性把 `softmax(QᵀK/√d)` 改写为减去 `max(QᵀK/(α√d))×α`（α 取大数如 32，须至少 head-wise），把注意力分数的最大绝对值也除以 α 防溢出。
  - **Sandwich-LN（三明治层归一化）**：在每个残差分支**末尾再加一个 LayerNorm**（Post-LN/Pre-LN 之外的新结构）。原因：LayerNorm 输出量级 ∝ √d=√2560≈50，若某些维度输入偏大、输出会到 10¹~10²，残差分支放大后加回主干、逐层加剧直至深层值爆炸；Sandwich-LN 把每层输入值约束在合理范围。500M 模型实验显示其对收敛影响可忽略。
  - **Shrink embedding gradient**：token embedding 的梯度远大于其他参数，用 α=0.1 缩小其尺度（`emb=emb*alpha+emb.detach()*(1-alpha)`）抬高动态 loss scale 防下溢，实测不损性能。
  - 这套方法成功稳定了 CogView 4B 与 8.3B 的 CogView-large，并被用于成功消除 10B GLM 训练的溢出。作者推测根因是**数据异质性**（文本与图像 token 在某些隐状态里按尺度可区分）。
- **微调（均可在单台 DGX-2 上一天内完成）**：
  - **超分**：先微调成 16×16→32×32 image token 的条件超分模型，再以「中心连续滑窗」策略把 32×32 token 图逐 patch 放大到 64×64 token（512×512 像素），滑窗顺序优于光栅扫描以保中心区域完整；用约 200 万张图裁 256×256 再下采样 128×128 构造训练对；超分序列超过 max position index 1087，从 `[ROI2]` 处重新从 0 计数位置编码。
  - **图像描述 + self-reranking**：交换序列里文本与图像 token 顺序即得 captioning 模型；提出 **Caption Loss**（CapLoss = 文本 token 的平均交叉熵 = inverse prompting 在文生图上的改造），选 CapLoss 最低的图，替代 DALL-E 的 CLIP 重排，且省算力（只需微调）。
  - **风格学习**：在中国画/油画/素描/卡通四种风格上分别微调，各仅 1,000 张（从 Google/Baidu/Bing 按「An image of {style} style」抓取），生成时用「A {object} of {style} style」迁移预训练学到的物体形状到目标风格。
  - **工业时装设计**：单域下用 VQGAN 替代 VQVAE 求更真实纹理、减参增序列长度提分辨率；训 3B 模型于约 1000 万时装-描述对，用 50×50 VQGAN token 解码到 800×800 像素，**已部署到阿里 Rhino（犀牛）智造**。

## Infra（训练 / 推理工程）
- **算力**：预训练用 **512 张 V100（32GB）**；微调任务单台 DGX-2 一天内完成。
- **混合精度**：几乎全 FP16（O2，即前向反向全 FP16，仅 optimizer state 与 master weight 为 FP32），靠上节 PB-relax/Sandwich-LN 实现；这是相对 DALL-E 复杂混合精度方案的工程简化卖点（不需大多数框架不支持的特殊改动）。
- **三区稀疏注意力（three-region sparse attention，Appendix B）**：每个 token 注意「全部文本 token + 全部 pivot token（随机选的图像 token，类 BigBird，每层重采样，提供全局信息）+ 相邻窗口块内 token（局部信息，blockwise window）」。1-D 窗口注意力可通过 padding/改 stride 原地高效实现；按块分组以省去自定义 CUDA kernel 的反向额外显存。在 4096 token 序列上，三区稀疏注意力（768 文本+pivot，768 窗口）比 vanilla 快 **2.5×、省 40% 显存**，整体训练快 1.5×、省 20% 显存，loss 曲线几乎不变。**注意：4B 主模型预训练并未用稀疏注意力**（担心与超分微调不兼容），只在 CogView-fashion 上成功加速。
- **推理形态**：自回归逐 token 生成（论文明确列为局限——慢）；提供 Wudao/AMiner 与 BAAI 平台 demo（后续 CogView2 demo 更快、支持英文输入）。

## 评测 benchmark（把效果讲清楚）
**机器评测（模糊化 MS COCO，30,000 caption 子集，对图加不同半径 Gaussian filter；caption 机翻成中文；不用超分，从 60 张里按 CapLoss 选最佳，CapLoss 评在 5,000 张子集上，最后把对比度增强 1.5×）**——FID-k 表示用半径 k 的高斯滤波（数据来自论文 Table 1）：

| Model | FID-0 | FID-1 | FID-2 | FID-4 | FID-8 | IS | CapLoss |
|---|---|---|---|---|---|---|---|
| AttnGAN | 35.2 | 44.0 | 72.0 | 108.0 | 100.0 | 23.3 | 3.01 |
| DM-GAN | 26.5 | 39.0 | 73.0 | 119.0 | 112.3 | 32.2 | 2.87 |
| DF-GAN | 26.5 | 33.8 | 55.9 | 91.0 | 97.0 | 18.7 | 3.09 |
| DALL-E | 27.5 | 28.0 | 45.5 | 83.5 | 85.0 | 17.9 | — |
| **CogView** | **27.1** | **19.4** | **13.9** | **19.4** | **23.6** | 18.2 | **2.43** |

- **结论**：CogView 在 FID-1/2/4/8（有模糊）全面领先，FID-2=13.9 远优于 DALL-E 的 45.5；CapLoss=2.43 最低（最好）。IS 上 DM-GAN 最高（32.2）但人评最差，说明 IS/FID 对配对文生图不适配——作者据此论证 **Caption Loss 是更好的、绝对（可跨样本平均）的指标**。
- **self-reranking vs CLIP**：随候选数增加，self-reranking 在 FID-0 上持续更优；CLIP 在提 IS 上更好，但 IS 不适合本任务。
- **CogView 为何在更少数据/参数下 FID 仍优于 DALL-E**（论文猜测）：(1) PB-relax/Sandwich-LN 优化更稳；(2) DALL-E 用了大量卡通/渲染数据，纹理与 COCO 真照片差异大；(3) self-reranking 选图 FID 优于 CLIP；(4) CogView 训得更久（96B vs 56B token）。
- **人评**：2,950 组对比（AttnGAN/DM-GAN/DF-GAN/CogView/复原 ground truth）。CogView 被选为最佳的概率 **37.02%**，逼近复原 ground truth 的 59.53%（理论上界）；超分模型一致提升清晰度，甚至超过复原 ground truth。
- **消融**：tokenizer 四训练法 L2 loss 几乎一致；三区稀疏注意力对收敛无影响（loss 曲线几乎相同）；toy 实验（64 层、1024 hidden、大 lr）显示无 Sandwich-LN 主干溢出、无 PB-relax 注意力溢出、两者皆用才能持续训练。

## 创新点与影响
- **核心贡献**：(1) 中文/通用域首个 4B 级开源自回归文生图 Transformer，确立「VQ-VAE + GPT 联合预训练」范式在中文场景落地；(2) **PB-relax + Sandwich-LN**——通用的大/深 Transformer FP16 稳定化技术，把「千步必 NaN」变为可全 FP16 训练，已外推到 8.3B CogView-large 与 10B GLM；Sandwich-LN 后被多代生成/语言模型沿用；(3) **Caption Loss + self-reranking**——用模型自身（captioning 微调）做后选，免去外挂 CLIP；(4) 一套统一序列框架支持文生图/超分/图像描述/图文重排/风格学习/时装设计多任务微调，时装模型已工业落地阿里 Rhino。
- **对后续工作的影响**：CogView 是 **CogView2 / CogVideo / CogVideoX** 系列的前身，奠定了智谱（THUDM/zai-org）在多模态生成的技术路线；其 FP16 稳定化经验也反哺了 GLM 大语言模型训练。是 2021 年与 DALL-E、[[ernie-vilg]]、[[godiva]] 并列的早期大规模自回归生成代表，处在扩散模型（[[ldm]]/[[glide]]）尚未统治文生图之前的「自回归 + VQ token」时代节点。
- **已知局限（论文自述）**：(1) 自回归逐 token 生成**慢**；(2) VQ-VAE 有损压缩导致生成图**偏模糊**；(3) 未去水印白边影响质量；(4) 存在 Deepfake 滥用与生成模型公平性问题（附录给出「词替换」缓解法）。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2105.13290
- arxiv_pdf: https://arxiv.org/pdf/2105.13290
- github: https://github.com/THUDM/CogView （现重定向至 https://github.com/zai-org/CogView）
- project_demo: https://wudao.aminer.cn/CogView/index.html （Wudao/AMiner demo）
- pretrained_models: https://resource.wudaoai.cn/home （Wudao-Wenhui，含 cogview-base/caption/sr）

## 本地落盘文件
- ../../../sources/omni/2021/arxiv-2105.13290.pdf （论文全文 PDF，已 pdftotext 精读正文+附录 A/B/C）
- ../../../sources/omni/2021/cogview--readme.md （GitHub readme，含模型/下载/训练/推理细节）
