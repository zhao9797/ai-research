---
title: "Jukebox: A Generative Model for Music"
org: OpenAI
country: US
date: "2020-04"
type: paper
category: audio
tags: [music-generation, raw-audio, vq-vae, sparse-transformer, autoregressive, codec-tokens, lyrics-conditioning]
url: "https://openai.com/index/jukebox/"
arxiv: "https://arxiv.org/abs/2005.00341"
pdf_url: "https://arxiv.org/pdf/2005.00341"
github_url: "https://github.com/openai/jukebox"
hf_url: ""
modelscope_url: ""
project_url: "https://jukebox.openai.com/"
downloaded: [arxiv-2005.00341.pdf, arxiv-2005.00341.txt, jukebox--blog.md, jukebox--readme.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Jukebox 是 OpenAI 2020 年 4 月发布的第一个能在**原始音频域**直接生成**带可辨歌唱、长达数分钟、可指定流派/艺术家/歌词**的音乐生成模型；核心做法是用**多尺度分层 VQ-VAE** 把 44.1kHz 波形压成离散码（8x/32x/128x 三级，码本各 2048），再用**自回归稀疏 Transformer**（顶层先验 50 亿参数）对这些压缩码建模 + 逐级 upsampler 还原。它是"把音频压成 codec token 再大规模序列建模"这一范式的早期里程碑，直接预示了后来 AudioLM / MusicLM / 各类音频 codec-LM 的路线。

## 背景与定位
- **问题**：直接对原始音频做生成建模极其困难。一首 4 分钟 CD 音质歌曲（44.1kHz、16bit）有超过 1000 万个时间步（blog 对比：GPT-2 只有约 1000 步，OpenAI Five 单局上万步），长程依赖远超当时序列模型能力。
- **此前路线**：① 符号化（piano-roll / MIDI）——OpenAI 自己的 MuseNet、Music Transformer 走这条路，但**无法刻画人声、音色、表现力**；② 原始音频——WaveNet/SampleRNN 等只能生成 20–30 秒的钢琴片段，无歌唱、无长程结构。
- **Jukebox 的位置**：站在 [[vq-vae]]（Oord et al. 2017）与 **VQ-VAE-2**（Razavi et al. 2019，分层离散码）肩上，把"先压缩到离散潜空间、再在潜空间做自回归"的思路从图像迁移到音乐，并针对音频做了关键改造（分离式自编码器、谱损失、码本随机重启）。相对前置工作的核心改进：**第一次把可辨歌唱 + 多流派 + 多分钟连贯性同时做出来**。
- 技术脉络上可与同期图像侧的 [[taming-transformers-vqgan]]（离散码 + 自回归 Transformer）类比，二者共享"VQ 离散化 + AR 先验"骨架，只是 Jukebox 在前、且面向音频。

## 模型架构
两阶段：**(1) 分层 VQ-VAE 压缩** + **(2) 离散码上的自回归 Transformer 先验/upsampler**。

### 阶段一：Music VQ-VAE（约 200 万参数）
- **三个独立的一维 VQ-VAE**（非分层共享，见下"分离式自编码器"），分别把 44.1kHz 音频在时间维压缩 **8x / 32x / 128x**（hop length 8/32/128），对应顶/中/底三级；blog 给出直观数字：压缩后约 **344 个 token/秒**（44100/128），每个 token 是 2048 词表之一。
- **结构**：编码/解码块由 **WaveNet 风格的非因果 1-D 膨胀卷积**残差网络 + 下/上采样（转置）卷积构成；重采样卷积 kernel=4、stride=2，每块改变 hop 一个 2 倍因子，堆 7 块得到 128x（顶层）。膨胀率按 3 倍增长扩感受野；底层残差块数加倍，感受野约 2 秒（实际多为局部）。
- **量化瓶颈**：码本大小 K=2048（每级独立码本），码本用 EMA 更新（γ=0.99），commit 权重 β=0.02。
- **三项关键改造**（相对 VQ-VAE-2）：
  1. **码本随机重启（random restarts）**：某码向量平均使用率低于阈值时，随机重置为当前 batch 中某个编码器输出，防止 codebook collapse；消融显示它让码本利用率从训练早期就更高（Fig.5，2048 码 ≈ 11 bits 熵）。
  2. **分离式自编码器（separated autoencoders）**：不用 VQ-VAE-2 的单编码器分层，而是**三个独立自编码器**，因为分层结构会把信息全压到瓶颈最小的底层、顶层几近坍塌（消融：单分层自编码器顶层 spectral convergence 仅 2.9 dB，几乎不可用）。
  3. **谱损失（spectral loss）** `L_spec = ‖|STFT(x)| − |STFT(x̂)|‖₂`：只用样本级 L2 重建会只学到低频、声音发闷；加谱损失（多组 STFT 参数求和，bins 2048/1024/512）让中高频可重建，但会引入一点 scratchy 噪声。

### 阶段二：先验 + upsampler（自回归 Transformer）
- 把先验分解为 `p(z) = p(z_top)·p(z_mid|z_top)·p(z_bot|z_mid,z_top)`，三者各训一个 Transformer。
- **骨干 = Scalable Transformer**（作者对 Sparse Transformer 的简化版）：
  - **轴对齐稀疏注意力**：用 masked-row + masked-column + unmasked-previous-row 三种因子化注意力替代 Child et al. 的 strided 稀疏注意力，效果/速度相同但**无需自定义 CUDA kernel**（纯 Python 级数组转置/切片即可实现），易扩展到视频。
  - **全 fp16 训练**：权重、梯度、Adam 优化器状态都存半精度；用单一初始化尺度 s（matmul 和输入输出 embedding 用 N(0,s)，位置 embedding 用 N(0,2s)），并对 Adam 状态做**动态缩放**（按 max 缩放到 fp16 范围）以省一半显存；更大模型用 **GPipe** 流水并行。
- **上下文**：三级都用 **8192 个 token** 的上下文，对应顶/中/底约 **24s / 6s / 1.5s** 原始音频——同样算力下顶层建模更长时序。
- **条件注入**：
  - **艺术家 + 流派**：各学一个 embedding，求和后作为序列**第一个 token**；并加**计时信号**（整曲总时长、本段起始、已播放比例），让模型学会开头/间奏/结尾结构。
  - **upsampler 的上层条件**：用深度残差 WaveNet（conditioner）+ 上采样 strided 卷积 + LayerNorm 把上层码作为额外位置信息加到当前级 embedding；下层只 attend 同段对应的上层码块。
  - **歌词条件（LTS, Lyrics-to-Singing）**：encoder-decoder 结构——歌词 Transformer 编码器（带自回归歌词建模损失），音乐解码器中**交错插入 encoder-decoder attention 层**（音乐 query 只能 attend 歌词 key/value），学到的注意力正好对应"当前唱到哪个字"的对齐（Fig.3）。
- **参数与分辨率**：
  - VQ-VAE ≈ **2M**；
  - 两个 **upsampler ≈ 1B**（width 1920、72 层）；
  - **顶层先验 = 5B**（Transformer width **4800、72 层、8 头**，因子化注意力 shape (128,64)；歌词编码器 width 1280、18 层、4 头、512 token；7 个 encoder-decoder attention 层）。

## 数据
- **自爬数据集**：**120 万首歌**（其中约 **60 万首英文**），配对**歌词 + 元数据**（来自 LyricWiki）。
- **元数据**：艺术家、专辑、流派、发行年份，以及常见情绪/歌单关键词。
- **音频格式与增强**：训练用 **32-bit、44.1kHz** 原始音频；数据增强为**随机把左右声道下混为单声道（mono）**。
- **歌词对齐（标注）**：
  - 基线启发式——把歌词字符**线性对齐**到整曲时长，取当前段落中心的固定窗口字符；对快歌词（hip-hop）失效。
  - 改进——用 **Spleeter** 抽人声，再跑 **NUS AutoLyricsAlign** 得到**词级对齐**，取足够大的窗口保证真实歌词大概率落在窗内。
- **训练曲线演进**：最初在 **MAESTRO**（22kHz）上训出高保真古典钢琴；换更大更杂的带标签数据集后才出现多流派与歌唱；最终模型只用**英文为主、以西方音乐为主**的数据训歌词条件模型以保证歌唱可懂。
- 美学/安全过滤：**未披露**（论文仅说用 **Compact Language Detector 2 (CLD2)**（Sites, 2013）按主语言检测把训练歌曲过滤为英文）。

## 训练方法
- **训练目标**：两阶段都是**最大似然 / next-token**——VQ-VAE 用重建（L2 + 谱损失）+ codebook + commit 三项损失（codebook 用 EMA）；先验/upsampler 是离散码上的标准自回归交叉熵。**没有用 diffusion / flow matching**（属于 codec-token + AR 范式，区别于同期 [[ddpm]] 路线）。
- **多阶段**：① 训三个 VQ-VAE；② 训顶层先验、中/底 upsampler（独立）；③ 歌词条件靠**decoder pretraining + model surgery**——复用已训好的无条件顶层先验当解码器，新插入歌词编码器，把新增 MLP/attention 的输出投影**初始化为 0**（恒等初始化），使初始时行为等同预训练解码器，但对编码器仍有梯度，从而逐步学会用歌词。**没有 RLHF / DPO / reward model**（2020 年生成音频尚无偏好对齐阶段）。
- **关键超参**：
  - VQ-VAE：sample length 393216、batch 256、约 38.5 万步、lr 3e-4、β=0.02、EMA γ=0.99。
  - 1B upsampler：context 8192、width 1920、72 层、batch 192/184、约 26.5–27.9 万步、lr 3e-4、Adam β₂=0.95、weight decay 0.01。
  - 5B 顶层先验：context 8192、width 4800、72 层、8 头、batch 512、约 31 万步、lr 1.5e-4、Adam β₂=0.925、weight decay 0.002。
- **加速/蒸馏**：训练时**未做**步数蒸馏；论文将"用并行采样器 + 概率密度蒸馏（Parallel WaveNet 式 KL 蒸馏）"列为**未来工作**以缓解极慢采样。

## Infra（训练 / 推理工程）
- **硬件全程 V100**：
  - VQ-VAE：**256× V100，3 天**；
  - 两个 1B upsampler：**128× V100，2 周**；
  - 5B 顶层先验：**512× V100，4 周**；
  - 歌词条件模型（复用先验 + 小编码器）：**512× V100，2 周**。
- **省显存工程**：全 fp16（含 Adam 状态）+ 动态缩放，把 1B 模型 + 8192 上下文塞进显存；更大模型靠 **GPipe** 流水并行；优化器 Adam（lr 1.5e-4，weight decay 2e-3）。
- **推理极慢（核心工程短板）**：自回归采样串行——**顶层 1 分钟 token 约需 1 小时**，**upsample 1 分钟约 8 小时**，blog 给出端到端**渲染 1 分钟音频约 9 小时**，因此"无法用于交互式应用"。
- **采样方式**：祖先采样（ancestral）；超过上下文长度用**窗口采样**（窗口前移半个 context，可用更小 hop 换质量）；**primed sampling**（把真实片段过 VQ-VAE 得码作为前缀续写）。
- **部署形态**：开源代码 + 三个权重（`5b`、`5b_lyrics`、`1b_lyrics`），PyTorch 1.4 + CUDA 10、MPI 多卡（`mpiexec -n {ngpus}`），并放出 Colab 与 sample explorer（jukebox.openai.com）。仓库现为 archived。

## 评测 benchmark（把效果讲清楚）
- **生成侧未用 FID / MOS 类自动指标**：作者明确指出"因每个人对音乐感受不同，用 MOS 或 FID-like 指标评样本既困难也意义不大"，改为**人工评估** coherence / musicality / diversity / novelty，并放出**数千条非精选样本**。无 ELO/Arena/HPSv2 等数字（彼时音乐生成尚无这些 benchmark）——这些维度**未报告具体分数**。
- **VQ-VAE 重建的定量消融**（用 **spectral convergence(dB)**，越负越好，5000 段 3 秒留出集）：
  - **压缩比 vs 保真度**（Table 1）：底/中/顶 = **−23.0 / −12.4 / −8.3 dB**（带随机重启），压缩越狠重建越差。
  - **随机重启**（Table 1）：底层 −21.1 → **−23.0 dB**（中/顶相同收敛但无重启需更多步、易得次优码）。
  - **码本大小**（Table 2，底层）：256 码 −15.9 dB；2048 码 **−23.0 dB**；不量化（连续）**−40.5 dB**（近完美），印证码本容量是瓶颈。
  - **谱损失 / 分层结构**（Table 3，顶层）：完整 −8.3；去谱损失 −6.3；改用单分层自编码器仅 **2.9 dB**（几乎失效）——验证"分离式自编码器 + 谱损失"对让顶层真正承载信息的必要性。
  - Fig.4 还把各级重建与 **Opus codec**（同比特率）做 Mel 谱对比，Opus 在高压缩级同样丢高频且有可闻 artifact。
- **定性结论**：连贯性在顶层 context（约 24s）内很好、滑窗后保持和声/纹理；能模仿流派/艺术家声线、能唱"训练中未见的歌词"（含 GPT-2 生成的歌词、深度学习术语）；能做 re-rendition、completion、duet、风格 embedding 插值出新声线。**局限**：听不到重复副歌/大尺度曲式；旋律不如人类有趣（缺 antecedent-consequent）；最小尺度偶有噪声/scratchiness；新流派迁移弱（艺术家 embedding 过强）。

## 创新点与影响
- **核心贡献**：
  1. **第一个原始音频域的多分钟、带可辨歌唱、可条件（流派/艺术家/歌词）的音乐生成系统**——把此前 20–30 秒无歌唱推进到数分钟有歌唱。
  2. **三项 VQ-VAE 工程改造**（随机重启、分离式自编码器、谱损失）成为后续离散音频 codec 训练的常用招式。
  3. **Scalable Transformer**：无需自定义 kernel 的轴对齐稀疏注意力 + 全 fp16（含优化器状态）+ 动态缩放，是早期把 Transformer 推到 5B / 8192 上下文的实用工程。
  4. **LTS（歌词到歌唱）对齐**：用 encoder-decoder attention 隐式学到字-音对齐，且 model surgery（零初始化）把无条件先验改造成条件模型。
- **对后续工作的影响**：奠定"**音频→离散 codec token→自回归序列模型**"范式，直接预示 AudioLM、MusicLM、各类 neural audio codec LM（以及更广义的"任意模态压成离散 token 再做 next-token"思路）；其分层码 + 上采样级联也被后续音频/视频生成沿用。
- **已知局限**：采样极慢（不可交互）、无大尺度曲式、单声道/英文为主、有可闻噪声、无偏好对齐、无标准化定量评测。

## 原始链接
- paper (arXiv abs): https://arxiv.org/abs/2005.00341
- paper PDF: https://arxiv.org/pdf/2005.00341
- blog (OpenAI): https://openai.com/index/jukebox/
- github (code + weights): https://github.com/openai/jukebox
- sample explorer: https://jukebox.openai.com/

## 本地落盘文件
- ../../../sources/omni/2020/arxiv-2005.00341.pdf
- ../../../sources/omni/2020/arxiv-2005.00341.txt
- ../../../sources/omni/2020/jukebox--blog.md
- ../../../sources/omni/2020/jukebox--readme.md
