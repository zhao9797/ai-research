---
title: "Stable Audio: Fast Timing-Conditioned Latent Audio Diffusion"
org: Stability AI (Harmonai)
country: UK
date: "2024-02"
type: paper
category: audio
tags: [audio, music-generation, latent-diffusion, text-to-audio, timing-conditioning, stereo, vae, clap]
url: https://arxiv.org/abs/2402.04825
arxiv: https://arxiv.org/abs/2402.04825
pdf_url: https://arxiv.org/pdf/2402.04825
github_url: https://github.com/Stability-AI/stable-audio-tools
hf_url:
modelscope_url:
project_url: https://stability-ai.github.io/stable-audio-demo
downloaded: [arxiv-2402.04825.pdf, stable-audio-latent-audio-diffusion--readme.md, stable-audio-latent-audio-diffusion--metrics-readme.md, stable-audio-latent-audio-diffusion--blog.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Stable Audio 是 Stability AI（音频实验室 Harmonai）提出的首个商业级 **隐空间音频扩散模型**，用 **timing conditioning（seconds_start / seconds_total 两个学习式时长嵌入）** 实现 **变长、长达 95 秒、44.1kHz 立体声** 的文生音乐/音效；研究版可在 **单张 A100（40GB）8 秒** 渲染 95 秒立体声，在 MusicCaps / AudioCaps 两个公开基准上 FDopenl3、KLpasst、CLAPscore 多项领先 MusicGen / AudioLDM2，且是当时唯一能稳定生成"有结构（intro/development/outro）+ 立体声"音乐的模型（ICML 2024）。

## 背景与定位
解决三个一直没人同时啃下来的痛点：(1) 大多数音频扩散模型只能生成 **固定长度**（30 秒训练→只能出 30 秒），用随机裁剪长音频的方式训练会让模型生成"从乐句中间开始/结束"的任意片段，缺乏完整曲式；(2) 自回归模型（[[jukebox]]、MusicLM、MusicGen）能变长但推理慢；(3) 此前没有工作能达到商用音乐规格 **44.1kHz 立体声**（Moûsai/JEN-1 只到 48kHz 立体声但训练长度 10–44 秒，AudioLDM2 48kHz 仅单声道）。

技术脉络上它是 [[latent-diffusion-ldm]] / Stable Diffusion 在音频域的对应物（"audio 版 Stable Diffusion"），并直接借鉴了 Moûsai 的 U-Net 架构思路，但用 **全卷积 end-to-end VAE 取代 Moûsai 的频谱+扩散解码器**（这是其快 10× 的关键），用 **显式 timing conditioning 取代 Jukebox 式的 prompt 内时长信息**。作者：Zach Evans、CJ Carr、Josiah Taylor、Scott H. Hawley、Jordi Pons。

## 模型架构
三件套（结构对标 Stable Diffusion）：**VAE + CLAP 文本编码器 + U-Net 条件扩散模型**。

- **VAE（133M 参数，从头训练）**：全卷积，遵循 **Descript Audio Codec（DAC）** 的 encoder/decoder（**去掉 quantizer**，因此是连续隐空间而非 RVQ token）。采用 **Snake 激活函数**（周期性激活），作者发现它在高压缩比下改善重建。把 `2×L` 的立体声输入下采样 **1024 倍** → `64×L/1024` 的隐编码（隐通道维 64），总体数据压缩比 **32×**。全卷积保证可编码/解码任意长度音频。VRAM 占用比 EnCodec 高，换取重建质量。
- **文本编码器（CLAP，从头训练）**：HTSAT 音频编码器（带 fusion，31M）+ RoBERTa 文本编码器（110M），语言-音频对比损失训练。取 **倒数第二层（penultimate）** 的文本特征（借鉴 NovelAI 用 CLIP 倒数第二层做 Stable Diffusion 条件的经验）。用 CLAP 而非 T5，因其多模态特性让文本特征已含"词-声"关系；消融显示自训 CLAP 略优于开源 CLAP-LAION 和 T5。
- **U-Net 扩散主干（907M 参数）**：受 Moûsai 启发，4 级对称下/上采样 + 跨级 skip connection。4 级通道数 1024/1024/1024/1280，下采样因子 1/2/2/4，最后接 1280 通道 bottleneck。每个 block = 2 个卷积残差层 + 一组 self-attention/cross-attention 层（每 block 三个 attention 层，第一级只有一个）。用 **FlashAttention** 高效注意力支撑长序列。
- **条件注入**：diffusion timestep 通过 **FiLM** 层调制激活；prompt 文本特征 + 两路 timing 嵌入（沿序列维拼接）一起经 **cross-attention** 注入 U-Net。
- **Timing conditioning（核心创新）**：取训练 chunk 时算两个量——`seconds_start`（chunk 在原曲中的起始秒）与 `seconds_total`（原音频总秒数），各自映射为 **逐秒、连续、可学习的嵌入**。例：从 180 秒曲子的第 14 秒取 95 秒 chunk → start=14, total=180；短于训练窗口的文件用静音 pad 到 95 秒。推理时用户给定 start/total 即可控制输出时长（如 start=0、total=30 → 30 秒信号 + 65 秒静音，trim 掉静音得到变长结果）。

## 数据
- **规模**：806,284 条音频，合计 **19,500 小时**，来自 stock 音乐商 **AudioSparx**（商业授权数据，规避版权问题，这是其"商业级"定位的基础）。
- **配比**：按文件数 / 按 GB 内容两种口径——音乐 66% / 94%、音效 25% / 5%、单乐器 stem 9% / 1%。
- **标注与 prompt 构造**：每条音频带自然语言描述 + 结构化元数据（BPM、genre、moods、instruments）。训练时把元数据随机子集拼成 prompt 字符串：一半样本保留元数据类型并用 `|` 连接（`Instruments: Guitar, Drums|Moods: Uplifting`），另一半丢掉类型用逗号连接；列表型值会 shuffle。这样推理时既能指定具体属性也不强制全填。
- 数据集（音频+元数据）作者称在线可查（AudioSparx）。无合成数据、无美学/安全过滤的额外披露。

## 训练方法
分三段独立训练（VAE → CLAP → U-Net 扩散，文本编码器训练扩散时冻结）：

- **VAE**：自动混合精度，**1.1M 步**，有效 batch 256，**16 张 A100**。前 460k 步后**冻结 encoder、仅 fine-tune decoder 再训 640k 步**。损失组合：为立体声设计的多分辨率 sum-and-difference STFT loss（STFT 前先做 A-weighting，window 长度 2048/1024/512/256/128/64/32）+ 对抗损失 + feature matching 损失（多尺度 STFT 判别器改造支持立体声，complex STFT 表示 + patch-based hinge loss）。权重：谱损失 1.0、对抗 0.1、feature matching 5.0、KL 1e-4。
- **CLAP**：在自有数据集上从头训 **100 epoch**，有效 batch **6,144**，**64 张 A100**，语言-音频对比损失。
- **U-Net 扩散模型**：EMA + 自动混合精度，**640,000 步**，**64 张 A100**，有效 batch 256。音频重采样到 44.1kHz、切到 **4,194,304 样本（95.1 秒）**，长文件随机起点裁剪、短文件末尾静音 pad。**v-objective + cosine 噪声 schedule + 连续去噪 timestep**。对条件信号施 **10% dropout** 以支持 classifier-free guidance。
- **推理采样**：**DPM-Solver++**，**CFG scale = 6**，**100 步**扩散（附录 A 显示前 50 步已得大部分质量，100 步是保守选择）。

## Infra（训练 / 推理工程）
- **算力**：VAE 16×A100、CLAP 64×A100、扩散 64×A100；自动混合精度全程。
- **推理效率**：研究版 95 秒立体声 44.1kHz 在单张 **A100(40GB) 8 秒**完成（realtime factor ×10，对比 Moûsai 的 ×1）。官方博客称**商业 flagship 版**借更先进采样技术可在 A100 上 **不到 1 秒** 渲染 95 秒立体声（推断用了更激进的步数/蒸馏，论文未细述这部分工程）。
- 与基线推理时间对比（A100, bs=1）：Stable Audio **8 秒** vs AudioLDM2-large 37 秒 / AudioLDM2-48kHz 242 秒 / MusicGen-large 242 秒 / MusicGen-large-stereo 295 秒——隐空间扩散远快于自回归，且即便处理立体声 44.1kHz 仍比单声道 16kHz 的 AudioLDM2 更快。
- **开源工程**：[stable-audio-tools](https://github.com/Stability-AI/stable-audio-tools)（PyTorch Lightning，支持多 GPU/多节点 DDP 与 DeepSpeed ZeRO-2，WebDataset/S3 数据）与 [stable-audio-metrics](https://github.com/Stability-AI/stable-audio-metrics) 全部开源。

## 评测 benchmark（把效果讲清楚）
作者重新定义了三个适配"长时长 + 全频带 + 立体声"的量化指标：**FDopenl3**（基于 OpenL3 的 Fréchet 距离，支持 48kHz、立体声左右声道独立投影后拼接，↓ 越好）、**KLpasst**（基于 PaSST tagger 在 32kHz、用重叠窗口适配长音频，↓）、**CLAPscore**（CLAP-LAION feature-fusion 处理长音频，↑）。

**MusicCaps（Table 1，全 95 秒输出对比 SOTA）：**

| 模型 | ch/sr | FDopenl3↓ | KLpasst↓ | CLAPscore↑ | 推理时间 |
|---|---|---|---|---|---|
| **Stable Audio** | 2/44.1k | **108.69** | **0.80** | **0.46** | **8 秒** |
| MusicGen-large | 1/32k | 197.12 | 0.85 | 0.36 | 242 秒 |
| MusicGen-large-stereo | 2/32k | 216.07 | 1.04 | 0.32 | 295 秒 |
| AudioLDM2-48kHz | 1/48k | 299.47 | 2.77 | 0.22 | 242 秒 |
| AudioLDM2-large | 1/16k | 339.25 | 1.46 | 0.30 | 37 秒 |

Stable Audio 在 FDopenl3、KLpasst、CLAPscore **三项全部最佳**。（去掉 vocal prompt 的公平对比 Table 4 结论一致，仅 KLpasst 与 MusicGen-large 相当。）

**AudioCaps（Table 2，音效）：** Stable Audio FDopenl3 **103.66**（仅次于 AudioLDM2-48kHz 的 101.11），但 KLpasst 2.89、CLAPscore 0.24 较弱——作者归因训练集中音效占比低（仅 5% 内容量），文本对齐在音效上不如音乐。

**文本编码器消融（23 秒输出）：** MusicCaps 上 CLAPours(0.97/0.44) 略优于 CLAP-LAION(1.09/0.43) 与 T5(1.06/0.41)，故选自训 CLAP。

**人评（Table 3，19 名用户，MOS 0–4）：** MusicCaps 上 Stable Audio 音质 **3.0±0.7**、文本对齐 **2.9±0.8**、musicality **2.7±0.9** 均居首（MusicGen-large 仅 2.1/2.4/2.0）。结构性：**立体声正确率 94.7%**，intro 92.1% / development 65.7% / outro 89.4%——远超 MusicGen-stereo（86.8% / 52.6% / 76.3% / 15.7%）与 AudioLDM2（多项 <16%）；AudioCaps 音效立体声正确率 57%（提示词本身少空间感所致）。

**Timing 准确性（§6.3）：** 指定 30/60/90 秒时实测长度紧贴对角线，40–60 秒区间误差稍大（该时长训练数据少），整体偏向略短，正好便于按预期长度裁剪静音。

**上界参考：** MusicCaps 真实训练数据 FDopenl3=101.47、经 VAE 重建后 117.52（轻微退化但作者称听感基本透明）。

## 创新点与影响
**核心贡献：**(1) 首次把 **timing conditioning（两个学习式时长嵌入）** 引入隐空间扩散，实现单模型**变长、长达 95 秒**生成 + 用户精确控时；(2) 首个达到**商用规格 44.1kHz 立体声** + 完整曲式结构的文生音频扩散模型；(3) 全卷积 DAC-style 连续 VAE（压缩比 32×）带来 ×10 实时因子的极速推理；(4) 一套面向长时长/全频带/立体声的新评测指标（FDopenl3 / KLpasst / 长音频 CLAPscore），开源为 stable-audio-metrics。

**影响：** 作为"音频版 Stable Diffusion"确立了文生音乐的隐扩散范式与商业落地路线（商用 Stable Audio 产品 + 后续开源 stable-audio-open）；其连续 VAE + timing conditioning 思路被后续长音频/音乐生成工作广泛参考；开源 stable-audio-tools 成为社区训练音频扩散模型的基础设施。

**已知局限：**音效（sound effects）表现明显弱于音乐（训练集音效占比低，AudioCaps 文本对齐/语义差）；不生成 vocals/speech（聚焦音乐+音效）；40–60 秒时长 timing 误差略大；商用 flagship 的"<1 秒"加速工程细节未公开；作者在 Impact Statement 中提示训练数据偏置对欠代表文化的适配性问题。

## 原始链接
- paper (arXiv abs): https://arxiv.org/abs/2402.04825
- paper (PDF): https://arxiv.org/pdf/2402.04825
- 官方研究博客: https://stability.ai/research/stable-audio-efficient-timing-latent-diffusion
- demo 页: https://stability-ai.github.io/stable-audio-demo
- code (模型/训练): https://github.com/Stability-AI/stable-audio-tools
- code (评测指标): https://github.com/Stability-AI/stable-audio-metrics

## 本地落盘文件
- ../../../sources/omni/2024/arxiv-2402.04825.pdf
- ../../../sources/omni/2024/stable-audio-latent-audio-diffusion--blog.md
- ../../../sources/omni/2024/stable-audio-latent-audio-diffusion--readme.md
- ../../../sources/omni/2024/stable-audio-latent-audio-diffusion--metrics-readme.md
