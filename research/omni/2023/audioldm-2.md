---
title: "AudioLDM 2: Learning Holistic Audio Generation with Self-supervised Pretraining"
org: "University of Surrey (CVSSP) / CUHK / ByteDance SAMI"
country: EU
date: "2023-08"
type: paper
category: audio
tags: [audio, text-to-audio, text-to-music, text-to-speech, latent-diffusion, self-supervised, audiomae, gpt-2, unified]
url: "https://arxiv.org/abs/2308.05734"
arxiv: "https://arxiv.org/abs/2308.05734"
pdf_url: "https://arxiv.org/pdf/2308.05734"
github_url: "https://github.com/haoheliu/AudioLDM2"
hf_url: "https://huggingface.co/cvssp/audioldm2"
modelscope_url: ""
project_url: "https://audioldm.github.io/audioldm2/"
downloaded: [arxiv-2308.05734.pdf, audioldm-2--readme.md, audioldm-2--hf-model-card.md, audioldm-2--hf-blog-faster.md]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
AudioLDM 2 是一个**统一语音 / 音乐 / 音效**的文生音频框架：核心创新是用自监督预训练的 **AudioMAE** 把任意音频映射为一个通用中间表示「**音频之语**（Language of Audio, LOA）」，用 **GPT-2** 把文本/音素/CLAP 等条件回归翻译成 LOA，再用 **潜扩散模型（LDM）** 把 LOA 还原成音频——LDM 这一段可在**无标注音频上自监督预训练**。在 AudioCaps 上 FAD 低至 **1.42**（AudioLDM 2-AC-Large）、CLAP 24.9（即 0.249，AudioLDM 2-AC；前 SOTA TANGO 仅 17.6），并首次让通用音频模型生成**可懂语音**（LJSpeech MOS 4.00，超 FastSpeech2）。

## 背景与定位
此前的通用音频生成（[[audioldm]]、Make-an-Audio、AudioGen）虽能生成正确的「音频事件」，但生成的语音**不可懂**；而语音/音乐各自有专门模型（FastSpeech2 用音高/时长预测器、MusicLM 用 w2v-BERT 语义阶段），各域的归纳偏置（inductive bias）互不通用。论文的命题是：能否用**同一套学习方法**统一语音、音乐、音效，且不需要域特定归纳偏置。

技术脉络上，AudioLDM 2 把 MusicLM/AudioLM 的「语义表示 + 声学表示」两阶段思想，从**离散 token**换成**连续表示**（更丰富的信息），并借鉴 regeneration learning 的思想引入中间表示 LOA 作为 C→x 的桥梁。相对 [[latent-diffusion-ldm]]（图像 LDM）与 [[audioldm]]（AudioLDM 1，直接用 CLAP 条件 + LDM）的关键改进：
- 把条件→音频拆成「**条件→LOA（GPT-2 自回归回归）**」+「**LOA→音频（[[ddpm]] / LDM）**」两段；
- LDM 段以 LOA（来自 AudioMAE）为条件，可纯自监督预训练，**摆脱对标注的依赖**；
- 用连续 LOA 替代离散 codec token，序列更短、推理更省、避免自回归误差累积；
- 引入音素编码器与可懂语音能力，把 TTS 纳入同一框架。

## 模型架构
整体三段式：**Any-Modality→LOA Translator（GPT-2）** + **LOA→Audio Generator（Transformer-UNet LDM）** + **Universal Vocoder（HiFi-GAN）**。

**1）语义表示 AudioMAE（计算 LOA）**
- AudioMAE 是 ViT 结构的音频掩码自编码器，在 AudioSet 上自监督预训练（掩码重建 mel patch），下游音频分类 SOTA。论文用其作为「audio→LOA 编码器」A(·)。
- 输入 mel 谱当作图像切 16×16 不重叠 patch，每 10 秒 mel 谱 → 长度 512、维度 768 的特征序列。
- 取 AudioMAE 编码器**最后 16 层 transformer 输出做平均**作为最终特征 E。
- **后处理池化**：对 E 的时频两维做二维 average-max 池化（核与步长均为 λ），得 Yλ，序列长 Lλ = T′F′/λ²。λ 越大序列越短越易建模、但细节越少（图 2 显示 λ=1 重建逼近 GT，λ=2/4 仅保语义）。音频/音乐用 **λ=8**，语音用 **λ=1**（保细粒度音素信息）。

**2）声学表示 VAE**
- 卷积 VAE（沿用 AudioLDM 1 结构）把 mel 谱压成低维潜变量 z，重建经 HiFi-GAN vocoder 转回波形。VAE 重建质量/压缩率高于 AudioMAE，故用 VAE 做 mel 压缩、AudioMAE 做语义 LOA（tSNE 显示 AudioMAE 潜空间更具语义聚类结构，VAE 类间更重叠）。

**3）条件→LOA：GPT-2（函数 M）**
- backbone 为预训练 GPT-2（768 维、12 层），用预训练权重初始化后 teacher-forcing 微调，**直接回归连续向量 yl（MSE 损失），不做离散化/token 索引预测**。
- 条件采用 **mixture-of-experts** 多编码器拼接：
  - **CLAP** 文本编码器（默认全局条件，Lk=1）；TTS 因无 caption，训练时用 CLAP 音频编码器、推理时用 CLAP 文本编码器（兼容「说话人提示」控制音色，图 6）。
  - **FLAN-T5**（捕捉文本时序/语义细节，弥补 CLAP 缺时序信息）。
  - **Phoneme Encoder**（仅 TTS）：按 NaturalSpeech 的 transformer 编码器堆叠，用 espeak-ng 音素化、每序列后加停止 token。
  - 各编码器输出经线性层统一到 D0 维后沿序列维拼接为 C。除音素编码器外，所有预训练特征提取模块**冻结**。

**4）LOA→音频：Transformer-UNet 潜扩散（函数 G）**
- 在 VAE 潜空间做 DDPM 式 LDM。backbone 是 **T-UNet**（在 AudioLDM 1 的 UNet 上加更多 transformer 层）：每个 encoder/decoder 卷积块后插 ntrans+1 个 transformer 块，前 ntrans 个为自注意力+FFN，**最后一块把自注意力换成 cross-attention**，以 LOA（GT 的 Y 或 GPT-2 预测的 Ŷ）作 K/V。
- 除 TTS 外，再加一层 cross-attention 接 **FLAN-T5 文本嵌入**作为额外条件——这是 AudioLDM 2 与多数 LDM 的差异：**两套 cross-attention 条件**（GPT-2 的 LOA + Flan-T5 文本）。
- 参数/规模：两档模型，ntrans=2（AudioLDM 2，UNet 350M / 总 1.1B）与 ntrans=6（Large，UNet 750M / 总 1.5B）。训练以 10 秒随机片段为单位、零填充到 10.24 秒；统一 16 kHz。

## 数据
LDM 段「**全部音频不论是否有标注**」自监督训练；GPT-2 段只用有配对文本的音频训练。所用数据集：
- **AudioSet (AS)**：~200 万条 10 秒音频、527 类（当时最大音频分类集）。
- **WavCaps**：ChatGPT 辅助弱标注 caption，403,050 条，平均 68 秒。
- **AudioCaps (AC)**：AudioSet 子集 + 人工 caption，约 46,000 条 10 秒。
- **VGGSound (VS)**：>20 万视频，仅用音频与标签。
- **FMA**：106,574 条音乐、无 caption；**Million Song Dataset (MSD)**：用 ~510,000 条带标签子集。
- **LJSpeech (LJS)**：单说话人 13,100 条 + 转写；**GigaSpeech (GGS)**：多说话人 ~10,000 小时英文（测试/开发集不入训练）。
- 全部重采样到 **16 kHz**。「FULL」组合 = AC+AS+WC+VS+MSD。AudioLDM 2-Full / Full-Large 的训练数据规模为 **29,510 小时**。
- HF 官方 checkpoint 卡另注明发布版 audioldm2 / audioldm2-large 训练数据约 **1150k 小时**、audioldm2-music 约 **665k 小时**（与论文实验配置的小时数口径不同，属发布版扩大数据）。
- 清洗/过滤/re-captioning 等更细的数据处理流程论文**未详细披露**（仅说明用各集原生标签/caption）。

## 训练方法
**目标函数**
- LDM：标准 DDPM ε-预测（式 7），在 VAE 潜空间最大化 ELBO（式 6），以 LOA 为条件信号。
- GPT-2：teacher-forcing 下最大化序列似然（式 3），**对连续 LOA 向量做 MSE 回归**（非分类）。

**多阶段 + 联合微调（关键 trick）**
1. LDM 与 GPT-2 **先各自独立训练**。LDM 预训练时 λ∈{1,2,4,8} 随机采样以增强对不同 λ 的鲁棒性（LOA 仅作 cross-attn 的 K/V，长度可变）。
2. **Joint Finetuning**：再联合微调 GPT-2 + LDM。引入「**概率切换器**」(probabilistic switcher) 在训练中动态选择 LDM 的条件来源——以 **Pgt=0.25** 用 GT AudioMAE 特征、**Ppred=0.75** 用 GPT-2 生成的特征。消融（表 V）显示去掉联合微调三项指标全面恶化（FAD 1.67→2.24）。

**条件 dropout / CFG**
- 训练时以 10% 概率丢弃条件 Y，同时训练有条件/无条件 LDM；推理用 classifier-free guidance，DDIM 采样默认 **guidance scale 3.5**。

**关键超参**
- AdamW，学习率 1e-4，10000 步线性 warmup 无衰减；8× NVIDIA A100 80GB；GPT-2 768 维 12 层；joint FT 时 Pgt=0.25 / Ppred=0.75。
- 蒸馏/一致性/LCM 等加速训练**未使用**（推理加速见 Infra，靠 Diffusers 工程优化而非步数蒸馏训练）。

## Infra（训练 / 推理工程）
**训练**：LDM 与 GPT-2 均在 **8× NVIDIA A100 80GB** 上训练/微调。总 GPU·时、并行策略、混合精度、吞吐等**未披露**。

**推理加速（HF 官方博客 "AudioLDM 2, but faster ⚡️" 实测，单 GPU / Colab）**：原生实现一个 10 秒样本约 30 秒，Diffusers 流水线把基线降到约 14 秒，叠加四项优化后 **<1 秒**（博客口径「over 10×」，14 秒→<1 秒）：
1. **SDPA / flash-attention**（PyTorch 2.0 `scaled_dot_product_attention`，Diffusers 默认开启）；
2. **float16 半精度**（速度↑、显存↓，音质几乎无损，官方建议默认开）——比 float32 约快 2 秒；
3. **`torch.compile`**（仅 wrap UNet，`mode="reduce-overhead", fullgraph=True`；首次编译可达 2 分钟，之后稳定）——降到约 4 秒；
4. **换调度器**：默认 DDIM 需 200 步，换 **DPMSolverMultistepScheduler 仅需 20–25 步**得相近质量。
- **显存优化**：`enable_model_cpu_offload()` CPU offload，可一次生成 4 条各 150 秒长音频；Large 版（UNet 750M）显存占用约为 base（350M）两倍多，offload 尤其有用。Diffusers 版整体比原生实现快约 **3×**，并支持任意长度生成。
- 部署形态：pip 包 `audioldm2` 命令行、Gradio Web App、HF Spaces、HF Diffusers `AudioLDM2Pipeline`（v0.21.0+）；支持 cpu/cuda/mps（mps 约需 20GB RAM）。

## 评测 benchmark（把效果讲清楚）

**Text-to-Audio（AudioCaps 评测集，表 II）** — 指标 Duration(h) / Param / FAD↓ / KL↓ / CLAP↑ / OVL↑（人评）/ REL↑（人评）。所有模型用 AudioCaps 训练子集；* = 仅在该子集训练，# = 在该子集微调。CLAP 列为论文原始 0-1 标度（正文写成 ×100，如 0.249→24.9）。
| 模型 | Param | FAD↓ | KL↓ | CLAP↑ | OVL↑ | REL↑ |
|---|---|---|---|---|---|---|
| GroundTruth | — | — | — | 0.251 | 4.04 | 4.08 |
| GT-AudioMAE（上界） | — | 1.84 | 0.19 | 0.239 | 3.87 | 4.02 |
| AudioGen-Large | 1B | 1.82 | 1.69 | — | — | — |
| Make-an-Audio | 453M | 2.66 | 1.61 | — | — | — |
| AudioLDM-Large# | 739M | 1.96 | 1.59 | — | — | — |
| AudioLDM-M | 416M | 4.53 | 1.99 | 0.141 | 3.61 | 3.55 |
| Make-an-Audio 2 | 937M | 2.05 | 1.27 | 0.173 | 3.68 | 3.62 |
| TANGO* | 866M | 1.73 | 1.27 | 0.176 | 3.75 | 3.72 |
| **AudioLDM 2-AC*** | 346M | 1.67 | 1.01 | **0.249** | 3.88 | 3.90 |
| AudioLDM 2-Full | 346M | 1.78 | 1.60 | 0.191 | 3.83 | 3.77 |
| **AudioLDM 2-AC-Large*** | 712M | **1.42** | **0.98** | 0.243 | 3.89 | 3.87 |
| AudioLDM 2-Full-Large | 712M | 1.86 | 1.64 | 0.182 | 3.79 | 3.80 |

- 论文正文：AudioLDM 2-AC 在三项客观指标全面超越前作；CLAP **24.9**（即 0.249，前 SOTA TANGO 17.6 / 0.176），**AudioLDM 2-AC-Large** 拿到最佳 KL **0.98**（前 SOTA 1.27）与 FAD **1.42**（创 TTA 新 SOTA）。AudioLDM 2-AC 人评 OVL 3.88 / REL 3.90，与 GroundTruth 差距仅 0.16 / 0.18。
- **scaling 观察**：加大模型主要提升音质（FAD：AC 1.67→AC-Large 1.42），对 KL/CLAP（音文关系）提升不明显；而 Full（29,510h）相比 AC 子集，因测试集分布窄反而客观指标略降（FAD 1.78 / 1.86）——但相比同为大规模无 AudioCaps 微调的 AudioLDM-M（FAD 4.53），AudioLDM 2-Full（论文称 FAD 1.42~2.13 区间）仍大幅领先。

**Text-to-Music（MusicCaps 评测集，表 III）** — ⋆=用公开实现复现的结果
| 模型 | FAD↓ | KL↓ | CLAP↑ | OVL↑ | REL↑ |
|---|---|---|---|---|---|
| GroundTruth | — | — | 0.253 | 3.82 | 4.26 |
| GT-AudioMAE | 2.18 | 0.27 | 0.257 | 3.59 | 3.92 |
| Riffusion | 14.80 | 2.06 | 0.190 | — | — |
| Mousai | 7.50 | 1.59 | — | — | — |
| MeLoDy | 5.41 | — | — | — | — |
| MusicLM | 4.00 | — | — | — | — |
| MusicGen-Medium | 3.4 | 1.23 | 0.320 | — | — |
| MusicGen-Medium⋆ | 4.89 | 1.35 | 0.291 | 3.37 | 3.38 |
| AudioLDM-M⋆ | 3.20 | 1.29 | 0.360 | 3.03 | 3.25 |
| AudioLDM 2-MSD | 4.47 | 1.32 | 0.294 | 3.41 | 3.30 |
| **AudioLDM 2-Full** | **3.13** | **1.20** | 0.301 | 3.34 | 3.54 |

- AudioLDM 2-Full 相比复现的 **MusicGen-Medium⋆** 在 FAD/KL/CLAP 分别 **+36% / +11% / +3.4%**（论文正文口径）。
- 有趣结论：只训音乐的 AudioLDM 2-MSD（FAD 4.47）反不如通用 AudioLDM 2-Full（FAD 3.13）—— **从通用视角学习反哺专域**。MeLoDy/MusicLM 未开源，部分客观/主观分缺失。AudioLDM-M⋆ 的 CLAP（0.360）异常高，论文指出系训练时直接以 CLAP 为条件、与评测指标对齐所致，不代表真实质量（其主观分较低）。

**Text-to-Speech（LJSpeech 测试集，表 IV，MOS↑）**
| 模型 | MOS↑ |
|---|---|
| GroundTruth | 4.63 ± 0.08 |
| GT-AudioMAE（上界） | 4.14 ± 0.13 |
| FastSpeech2（baseline） | 3.78 ± 0.15 |
| AudioLDM 2-LJS | 3.65 ± 0.21 |
| **AudioLDM 2-LJS-Pretrained** | **4.00 ± 0.13** |
- 在 GigaSpeech 上预训练 GPT-2 再微调 LJSpeech，MOS 达 **4.00**，显著超 FastSpeech2（3.78），是首个能生成可懂语音的通用音频框架级结果。

**消融（AudioCaps，表 V）**
- 去 joint finetuning：FAD 1.67→2.24（全面恶化，证明联合微调关键）。
- 去 CLAP（GPT 输入）：FAD→2.48；去 FLAN-T5（GPT 输入）：FAD→2.73、但 CLAP 反升（条件直接对齐评测指标）。
- 去 T-UNet 中 FLAN-T5 cross-attn：FAD 1.67→**1.38**（更好），但 KL/CLAP 显著降——说明仅靠 AudioMAE 条件 FAD 更优，FLAN-T5 补的是音文语义关系。
- 同时去 CLAP+FLAN-T5、直接喂文本给 GPT-2：仍有竞争力（FAD 2.11 / KL 1.06），但 CLAP 明显降。

## 创新点与影响
**核心贡献**
1. 提出通用音频中间表示 **LOA（Language of Audio）**，用自监督 AudioMAE 计算，把语音/音乐/音效统一在**同一套不带域特定归纳偏置**的框架里。
2. 二阶段「**GPT-2 回归 LOA + LDM 还原音频**」设计，使 LDM 可在**无标注音频上自监督预训练**（缓解音频标注稀缺），并兼得自回归建模与扩散建模优势；用**连续表示**替代离散 codec token（序列更短、避免误差累积）。
3. 首次让通用音频生成框架产出**可懂语音**（TTS MOS 4.00），并支持音频 in-context learning、说话人提示控音色（speaker prompt，图 6）。
4. 工程上深度集成 HF Diffusers，开放 5+ checkpoint（full / large / music / speech-gigaspeech / speech-ljspeech / 16k-t5 / 48k 高保真），推理可压到 <1 秒。

**影响**：作为「统一文生音频」的代表框架，被广泛用作音频生成 baseline 与下游基座；后续工作（含作者团队 audiosr/语音超分、48k 高保真扩展）沿此路线。论文 2024 年正式发表于 IEEE/ACM TASLP（vol.32, pp.2871-2883）。

**已知局限**：(1) 当前三个 base 系统仍按任务分别训练，**单模型同时生成 audio/music/speech 的多任务统一未在论文实现**（列为 future work）；(2) 大规模数据在分布窄的测试集上客观指标反降，存在 train/test 分布不匹配；(3) 生成质量对随机种子/硬件敏感（README 明确提示需调 seed）；(4) 200 步 DDIM 原生推理慢（靠 Diffusers 工程优化而非步数蒸馏训练解决）；(5) 数据清洗/合成/配比等细节未充分披露。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2308.05734
- arxiv_pdf: https://arxiv.org/pdf/2308.05734
- github: https://github.com/haoheliu/AudioLDM2
- project_demo: https://audioldm.github.io/audioldm2/
- hf_model_card: https://huggingface.co/cvssp/audioldm2
- hf_blog (inference): https://huggingface.co/blog/audioldm2
- training_code: https://github.com/haoheliu/AudioLDM-training-finetuning
- TASLP 2024: https://doi.org/10.1109/TASLP.2024.3399607

## 一手源存档（sources/）
- [arxiv-2308.05734.pdf](https://arxiv.org/pdf/2308.05734)  （论文 PDF，13 页 v3，gitignore 不入 git）
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/audioldm-2--readme.md)  （GitHub README，checkpoint 列表/用法）
- [hf-model-card.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/audioldm-2--hf-model-card.md)  （HF cvssp/audioldm2 官方 checkpoint 表）
- [hf-blog-faster.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/audioldm-2--hf-blog-faster.md)  （HF 官方推理优化博客）
