---
title: "Lumina-T2X: Transforming Text into Any Modality, Resolution, and Duration via Flow-based Large Diffusion Transformers"
org: "Shanghai AI Laboratory & CUHK"
country: China
date: "2024-05"
type: tech-report
category: unified
tags: [dit, flow-matching, flag-dit, text-to-image, text-to-video, text-to-3d, text-to-speech, rope, resolution-extrapolation, unified-generation]
url: "https://arxiv.org/abs/2405.05945"
arxiv: "https://arxiv.org/abs/2405.05945"
pdf_url: "https://arxiv.org/pdf/2405.05945"
github_url: "https://github.com/Alpha-VLLM/Lumina-T2X"
hf_url: "https://huggingface.co/Alpha-VLLM/Lumina-T2I"
modelscope_url: ""
project_url: ""
downloaded: [arxiv-2405.05945.pdf, lumina-t2x--readme.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Lumina-T2X 是上海 AI Lab 提出的统一 **flow-based 大 DiT（Flag-DiT）** 框架——用一套加了 RoPE / RMSNorm / KQ-Norm / 零初始化注意力 + flow matching 的可扩展 DiT，把文本统一生成为图像/视频/多视角 3D/语音四种模态，且支持任意分辨率、宽高比与时长；最亮眼的是 **Lumina-T2I（5B Flag-DiT + 7B LLaMA 文本编码器）只用 PixArt-α 35% 的训练算力（288 vs 828 A100 GPU-days）**，并且训练在 1024 却能免训练外推到 1792² 甚至改善画质（"免费午餐"）。

## 背景与定位
2024 年初 Sora 展示了把 DiT 扩到任意分辨率/时长生成图像视频的潜力，但闭源、无实现细节；SD3、PixArt-α/Σ 也证明 transformer + flow matching 路线优于 U-Net，但都局限单一任务、单一分辨率，且实现/权重不全开放。本工作的定位就是**做开源版的"Sora 式统一可扩展生成框架"**：
- 相对 [[dit-scalable-diffusion-transformers]]：原版 DiT 最大只到 600M、需全精度训练、用 APE 只能定分辨率单图、用 DDPM 公式。Flag-DiT 通过借鉴 LLM 的工程（RoPE/RMSNorm/KQ-Norm + 混合精度 + FSDP/序列并行）把 DiT 稳定扩到 **7B 参数、128K token 上下文**。
- 相对 [[sit]]（Scalable Interpolant Transformer，flow matching 版 DiT）：Flag-DiT 在同等 600M 下 FID 更低，作者归因于 RMSNorm/RoPE/KQ-Norm 这些 meta-architecture 改动既稳训练又涨点。
- 相对 [[pixart-alpha]]：Lumina-T2I 受其多阶段训练 + 高美学数据启发，但有三点关键差异——backbone 大 8.3 倍（5B vs 0.6B）、**直接在高美学合成数据上训练（不经 ImageNet/SAM 预训练，避免域 gap）**、靠 RoPE+[nextline] 获得 PixArt 没有的分辨率外推能力。
这是 **Lumina 系列的开山之作**，后续衍生 Lumina-Next（Next-DiT + Gemma-2B 文本编码器，2K 生成）、Lumina-mGPT（自回归路线）、Lumina-Image 2.0 等。

## 模型架构
**Backbone：Flag-DiT（Flow-based Large Diffusion Transformer）**——在原版 DiT 上做三类改动以求 stability / flexibility / scalability：
- **Stability**：把所有 LayerNorm 换 **RMSNorm**；在 Q·K 点积前加 **KQ-Norm（key-query normalization）**消除 attention logits 极大值，从而在**混合精度**下不发散，并允许更大学习率。
- **Flexibility**：
  - 用 **RoPE** 替代 DiT 的绝对位置编码（APE）——逐层注入相对位置，带来跨分辨率外推能力。
  - 引入可学习特殊 token **[nextline]（换行）/ [nextframe]（换帧）** + [PAD]，把任意分辨率/宽高比/帧数的 latent 拍平成统一的一维 token 序列（类似 LLM 处理文本），推理时显式摆放这些 token 即可指定任意输出形状/时长。
  - 把 DDPM 公式换成 **flow matching**（线性插值 `x_t = t·x + (1−t)·ε`，回归恒定速度场 `v = x − ε`）。
- **Scalability**：纯 transformer，可直接套用 LLM 的 **FSDP + 序列并行**；在 ImageNet 上从 600M 验证扩到 7B，token 长度扩到 4K，并验证可生成长达 128 帧 / 128K token 的视频。

**条件注入**：除了标签条件（class-conditioned，走 modulation），文本条件用**零初始化注意力（zero-initialized gated cross-attention）**——图像 query 聚合文本 key/value，门控用 `tanh(α)`（α 零初始化）逐步注入。公式：`A = softmax(ĨqĨkᵀ/√d)·Iv + tanh(α)·softmax(ĨqTkᵀ/√d)·Tv`。作者发现该门控诱导**极高稀疏度**：方法节称可关掉跨层跨头约 90% 的文本条件，实验节进一步给出**截断阈值后 80% 的门可被关闭而不损画质**（关键文本条件头集中在中间层），暗示推理时可裁掉大部分 cross-attention、更高效的 T2I 设计空间。时间步 + 全局文本 embedding 走 modulation（scale & shift）。

**统一 pipeline 四件套**（Figure 3）：① frame-wise 编码（图像 T=1 / 视频 T=帧数 / 多视角 T=视角数，逐帧过 SD-1.5 VAE 拼接；语音 spectrogram 走 identity 不过 VAE）→ ② input/target 构造（2×2 patch 拍平 + [nextline]/[nextframe] + flow matching 插值）→ ③ 文本编码（CLIP / LLaMA / SPHINX / Phone 多选）→ ④ Flag-DiT 预测速度。

**Visual tokenizer / latent**：SD-1.5 VAE（图像+视频共享 latent，支持视频）或 SDXL VAE（画质更好，但不支持视频）。Patch 2×2。

**文本编码器**：CLIP-L/G、LLaMA-7B、SPHINX-13B、Phone encoder 任选。默认最强配置 Lumina-T2I = **5B Flag-DiT + 7B LLaMA + SDXL latent**。

**Flag-DiT 规格表（Table 3）**：S(4层/8头/768) · B(8/12/768) · L(12/24/1024) · XL(20/28/1152) · **5B(32层/32头/3072)** · **7B(32层/32头/4096)**。

**各模态配置**：T2I 用 5B Flag-DiT+7B LLaMA+SDXL；T2V/T2MV 因序列可达 ~100 万 token，用 **2B Flag-DiT + CLIP-L/G + SD-1.5 latent**（T2MV 附录里用的是 5B+CLIP-L/G）；T2Speech 直接 tokenize 谱图 + phoneme/pitch encoder，随机初始化从头训。

## 数据
四模态**各自独立从头训练**（不共享权重），数据来源各异，原文给出的规模：

- **Lumina-T2I（图像）**：**14M 高质量（HQ）图文对**（主用 **JourneyDB** 合成高美学数据），三阶段 256/512/1024 分辨率。明确**只用合成域、不用 ImageNet/SAM**——消融发现 JourneyDB 合成图与自然图（LAION/COYO/SAM/ImageNet）分布不同，混训会抬高后续阶段 loss、造成次优初始化；故直接在高美学合成域训既省算力又避域 gap。注：对比 PixArt-α 额外用了 11M HQ 自然图文对。
- **Lumina-T2V（视频）**：**Panda-70M 的一个子集（15M 视频）+ 自采 Pexel 数据集（40,000 视频）**。两阶段：先固定 512×512×32 帧（约 32K token），再放开到任意分辨率/时长但限 128K token。
- **Lumina-T2MV（多视角 3D）**：**Objaverse 的 LVIS 子集（约 40K 个 3D 物体）**，文本描述用 **Cap3D** 生成。每物体渲染 12 视角（仰角固定 30°，方位 0–360° 均匀），按 Zero123++ 方式拼成 3×4 网格大图（12 张 256² → 1024×768；12 张 512² → 2048×1536），白底，不提供相机参数。
- **Lumina-T2Speech（语音）**：**LJSpeech**（13,100 条 22050Hz 单女声，约 24 小时）。文本→phoneme 用开源 g2p 工具；提谱图（FFT 1024 / hop 256 / win 1024）→ 80 mel bins；用 Parselmouth 提 F0。

**清洗/标注**：强调"meticulously curated 高美学帧 + 详细 caption"，但**未披露具体清洗/过滤/美学打分/安全过滤流程的量化细节**。再标注仅 T2MV 用 Cap3D、语音用 g2p，图像/视频 caption 来源细节未详述。

## 训练方法
- **训练目标**：**Conditional Flow Matching loss**（回归速度场 `‖v_θ(x_t,t) − (α̇_t·x + β̇_t·ε)‖²`），线性插值 schedule。框架也兼容 DDPM（"Large-DiT"即 Flag-DiT 的 DDPM 变体，用于和原版 DiT 公平对比）。
- **时间步采样**：**LogNorm（log-normal）resampling**——先从 N(0,1) 采样再用 logistic 映射到 [0,1]，强调中间时间步（速度场学习在 schedule 中段最难）。消融显示比均匀采样收敛更快、FID 更低。
- **多阶段渐进训练**：T2I 走 256→512→1024 分辨率渐进；T2V/T2MV 走"短低分辨率→长高分辨率"渐进。作者核心经验：**用更大模型 + 更高分辨率 + 更长片段反而加速收敛**——虽然单步更慢（transformer 二次复杂度），但收敛所需迭代数大降，总训练时间反而短。
- **从头训 vs ImageNet 初始化**：消融（Figure 5d）显示**从头训比 ImageNet 初始化 loss 更低、收敛更快**，且不受预训练网络配置约束——故 Lumina-T2I 放弃 PixArt 式 ImageNet 预训练。
- **关键 trick**：混合精度（靠 RMSNorm+KQ-Norm 才稳）；零初始化注意力让文本条件平滑注入。
- **加速/蒸馏**：原论文未做步数蒸馏；但 README 记录 Lumina-Next 支持**高阶 solver，无需蒸馏即可 10 步出图**（属后续工作）。
- **超参（部分，Table 1）**：Lumina-T2I-5B 三阶段 batch size 512/256/128，学习率统一 **1e-4**；各阶段约 96 A100-days（合计 288）。语音：Adam(β1=0.9,β2=0.98,ε=1e-9)，batch 64 句，单卡 4090 训 20 万步。

## Infra（训练 / 推理工程）
- **并行**：纯 transformer 架构，复用 LLM 的 **FSDP + 序列并行**支撑大参数与长序列（视频/多视角 token 可达 ~100 万）。
- **混合精度**：Flag-DiT 的核心工程卖点——原版 DiT 混合精度会发散，靠 RMSNorm + KQ-Norm 才能稳定混精训练，吞吐随之提升。
- **吞吐（Table 4，单 8×A100，ImageNet）**：Flag-DiT-XL 256 分辨率 600 imgs/s（DiT-XL 仅 435，约快 40%）；**Flag-DiT-5B 在 1024 分辨率 9 imgs/s，与 DiT-XL 的 10 imgs/s 相当**——即 5B 大模型在高分辨率下吞吐不落后小 DiT。Flag-DiT-5B：256→195 / 512→32 / 1024→9 imgs/s；7B(256)→120。
- **算力规模**：Lumina-T2I 全部仅 **288 A100 GPU-days**（PixArt-α 为 828）；T2MV 在 16×A100(80G) 上低分辨率 batch64×100K iter + 高分辨率 batch16×180K iter；T2Speech 单卡 4090；T2V 用到 8 vs 128 GPU 的 loss 对比（大 batch 才收敛，batch 32→1024）。
- **推理加速**：
  - **NTK-aware scaled RoPE** + **Time Shifting**（重排时间步保持跨分辨率 SNR 一致，默认 shift m=6.0）+ **Proportional Attention**（按 `c=√(log_{L_train} L_infer)` 缩放 attention 分数稳定熵）——三件套实现免训练分辨率外推。
  - Flag-DiT 用自适应 **Dopri-5（ODE）solver** 采样（对比 Large-DiT 用 250 步 DDPM）。
  - README：Lumina-Next 高阶 solver 可 10 步出图（无蒸馏）。
- **部署形态**：全开源（训练+推理代码 + 5B/2B checkpoint），HF/wisemodel 放权重，提供官方在线 demo 节点。

## 评测 benchmark（把效果讲清楚）
**关键说明：原论文对核心产品 Lumina-T2I 没有报告 GenEval / T2I-CompBench / DPG-Bench / MJHQ-30K / HPSv2 / ImageReward / PickScore 等标准 T2I 量化指标**，T2I/T2V/T2MV 结果以**定性图样 + 训练 loss 曲线**为主。可量化的硬指标集中在 ImageNet（验证 Flag-DiT 架构）和语音两块：

**ImageNet 256×256（FID-50K，Table 2）**：
- 无 CFG：**Large-DiT-7B FID 6.09**（256M 训练图），把此前 SOTA SiT-XL/2-G 的 8.60 降到 6.09。
- 带 CFG：**Flag-DiT-3B-G FID 1.96 / IS 284.80 / Prec 0.82 / Rec 0.61**；Large-DiT-3B-G FID 2.10 / IS 304.36。对比 DiT-XL/2-G(2.27)、SiT-XL/2-G(2.06)，**Flag-DiT-3B 仅用约 14% 训练迭代即达更优 FID/IS**（Large-DiT-3B 用约 24%）。
- 收敛：同 600M 下 Flag-DiT(flow matching) FID 全程低于 Large-DiT(DDPM)，也低于 SiT，验证 flow matching + meta-architecture 改动既稳又涨点；LogNorm 采样进一步降 FID。

**ImageNet 512×512（Table 2）**：**Large-DiT-3B-G FID 2.52 / IS 303.70**，对比此前 DiT-XL/2-G 的 3.04 / 240.82，FID 3.04→2.52、IS 240→303。

**Lumina-T2Speech（LJSpeech，Table 5）**：随模型增大稳定提升——
| 配置 | MOS | WER↓ | SIM↑ |
|---|---|---|---|
| GT | 4.34±0.07 | / | / |
| GT(voc.) | 4.18±0.05 | 5.3 | 99.2 |
| Flag-DiT-S | 3.92±0.07 | 6.8 | 97.5 |
| Flag-DiT-B | 3.98±0.06 | 6.4 | 98.0 |
| Flag-DiT-L | 4.02±0.08 | 6.2 | 98.3 |
| Flag-DiT-XL | 4.01±0.07 | 6.3 | 98.4 |

**定性结论**：T2I 可在 512²–1792² 任意分辨率/宽高比生成照片级图像，**外推到 1.5K 还能涨画质与文图对齐（"免费午餐"）**，超过 1.5K→2K 后因域 gap 逐渐失败；PixArt-α 在训练分辨率之外（更低或更高）画质都明显劣化，凸显 RoPE+[nextline] 的外推优势。T2V 可生成 720p、含场景转场的长视频（最长 128K token）。T2MV 不给相机参数也能生成 12 视角空间一致的 3D 物体多视图。

**消融小结**：① flow matching > DDPM（FID）；② RMSNorm/RoPE/KQ-Norm 既稳训又涨点；③ LogNorm 采样加速收敛降 FID；④ 参数越大收敛越快（600M→7B）；⑤ 从头训 > ImageNet 初始化；⑥ Time Shifting m 越大（1→10）外推画质越好；⑦ 零初始化注意力诱导高稀疏（方法节称 ~90% 文本条件可关；实验节示 80% 门可截断不损画质）。

## 创新点与影响
**核心贡献**：
1. **Flag-DiT**：把 LLM 工程（RoPE/RMSNorm/KQ-Norm/混合精度/FSDP+序列并行）系统移植到 DiT，首次把 flow-based DiT 稳定扩到 7B 参数 / 128K token，解决原版 DiT 600M 天花板与混精发散问题。
2. **[nextline]/[nextframe] 一维统一序列**：用 LLM 式 token 占位符把图像/视频/多视角/语音统一成一维序列，**一套框架、一种 flow matching 范式覆盖任意模态/分辨率/宽高比/时长**。
3. **免训练分辨率外推**：RoPE + NTK-scaled RoPE + Time Shifting + Proportional Attention，1024 训练直接外推到 1792² 且画质更好——首个从 flow-based DiT + RoPE 角度系统研究该方向的工作。
4. **极致算力效率**：5B 模型仅 288 A100-days（PixArt-α 35%），实证"放大参数加速生成模型收敛"。
5. **训练免调（tuning-free）下游能力**：分辨率外推、风格一致生成（shared attention）、高分辨率编辑（latent 插值 + 通道归一化去风格泄漏）、组合生成（按区域裁 cross-attention）全部统一在一套框架、无需额外训练。
6. **全开源**：代码 + 5B/2B checkpoint + 多模态 demo，作为开源 Sora 式框架推动社区复现。

**对后续的影响**：开创 Lumina 系列——Lumina-Next（Next-DiT + Gemma-2B，2K 生成、10 步 solver）、Lumina-mGPT（自回归路线）、Lumina-T2Audio/Music、Lumina-Image 2.0；Next-DiT 被并入 HuggingFace diffusers。"LLM 工程移植到 DiT + flow matching + 一维统一序列"成为后续统一生成框架的常见配方。

**已知局限（原文自述）**：
- T2V 与 Sora 仍有明显视频长度/质量差距；T2V 用全注意力 + 随机初始化，训练/推理慢（作者认为潜力更大但吃算力）。
- 分辨率外推超 1.5K→2K 会因训练/推理域 gap 出现伪影、逐渐失败，需高于 1K 的高质数据做少量 PEFT 补救。
- 核心 T2I 缺标准 T2I benchmark 量化（GenEval/CompBench/MJHQ 等均未报告），主要靠定性图与 ImageNet 间接验证。
- 各模态独立从头训，并非真正"一个模型多模态"，而是"一个框架多个模型"。
- 视频缺专门的时空 VAE（逐帧 SD-1.5 VAE），作者明确指出更好的时空编码器 + 更精细数据可进一步提质。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2405.05945
- arxiv_pdf: https://arxiv.org/pdf/2405.05945
- github: https://github.com/Alpha-VLLM/Lumina-T2X
- hf (Lumina-T2I 5B): https://huggingface.co/Alpha-VLLM/Lumina-T2I
- 后续: Lumina-Next https://arxiv.org/abs/2406.18583 ; Lumina-mGPT https://arxiv.org/abs/2408.02657

## 本地落盘文件
- ../../../sources/omni/2024/arxiv-2405.05945.pdf
- ../../../sources/omni/2024/lumina-t2x--readme.md
