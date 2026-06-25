---
title: "Lumina-Next: Making Lumina-T2X Stronger and Faster with Next-DiT"
org: Shanghai AI Laboratory
country: China
date: "2024-06"
type: paper
category: t2i
tags: [text-to-image, diffusion-transformer, next-dit, flow-matching, rectified-flow, rope, resolution-extrapolation, few-step-sampling, multilingual, unified-generation]
url: "https://arxiv.org/abs/2406.18583"
arxiv: "https://arxiv.org/abs/2406.18583"
pdf_url: "https://arxiv.org/pdf/2406.18583"
github_url: "https://github.com/Alpha-VLLM/Lumina-T2X"
hf_url: "https://huggingface.co/Alpha-VLLM/Lumina-Next-SFT"
modelscope_url: ""
project_url: ""
downloaded: [arxiv-2406.18583.pdf, lumina-next--t2x-readme.md, lumina-next--t2i-readme.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Lumina-Next 是 [[lumina-t2x]] 的下一代升级：把核心扩散变换器从 Flag-DiT 改造为 **Next-DiT**（3D RoPE + sandwich norm + GQA），配合 **Frequency/Time-Aware Scaled RoPE**（免训练分辨率外推）与 **sigmoid 时间表 + 高阶 ODE 解算器**（5–10 步出图）。一个 **2B Next-DiT + Gemma-2B 文本编码器**的模型，在质量与多语言能力上超过原 Lumina-T2X 的 **5B Flag-DiT + LLaMA-7B**，并把训练/推理成本大幅降低；同一框架零改动可扩展到识别、多视图、音频、音乐、点云。

## 背景与定位
[[lumina-t2x]]（arXiv 2405.05945）提出 flow-based 大扩散变换器 Flag-DiT，主打"低训练资源 + 任意分辨率/宽高比/时长"的统一生成框架，但实测暴露三大短板：**图文对齐弱、推理慢、外推有重复/伪影**——根因是训练不足、数据不足、以及不合适的 1D RoPE 上下文扩展策略。

作者来自 **Shanghai AI Laboratory + 香港中文大学（CUHK）**（论文署名）。Lumina-Next 不是新预训练范式，而是一套**架构 + 外推 + 采样**的系统性手术，目标"更强更快"。技术脉络上：它把 LLM 社区成熟的位置外推方法（[[position-interpolation]]、NTK-Aware Scaled RoPE、[[yarn]]）首次系统迁移到 **3D RoPE 的视觉扩散变换器**，并针对 flow 模型重新设计时间离散化（区别于 [[elucidating-edm]] 等扩散调度）。相对前置工作 [[sit]]、[[dit-scalable-diffusion-transformers]]、[[pixart-alpha]]、[[sdxl]]，它在 ImageNet 上收敛更快，在 2K/全景外推与少步采样上质量更优。Next-DiT 这套骨干后来成为 **Lumina-Image 2.0** 的基础。

## 模型架构
**Backbone：Next-DiT（由 Flag-DiT 升级而来）**。Flag-DiT 本身是带 flow matching、RMSNorm、QK-Norm 的可扩展 DiT。Next-DiT 的关键改动（论文 Fig.2）：

- **1D RoPE → 3D RoPE**：Flag-DiT 把不同模态统一编码为 `[H, W, T, C]` 隐空间帧（图像 T=1、视频 T=帧数、多视图 T=视图数），再展平用 1D RoPE——这丢失了 2D/3D 空间关系（1D RoPE 在 2D 图上的 long-term decay 方向是错的）。Next-DiT 把 head 维度三等分，对 x/y/z 轴**分别**算 RoPE 再拼接复向量，attention score 取 Hermitian 内积实部。图像 1 帧时自动退化为 2D RoPE，给出"同行/同列高注意力"的自然先验。
- **删除可学习标识符**：Flag-DiT 的 `[nextline]`/`[nextframe]` 等 learnable token 不再需要，3D RoPE 已提供充分的时空位置信息。
- **Sandwich Normalization（核心稳定性手术）**：诊断出训练/采样不稳定源于"残差结构里无归一化的长信号通路导致激活逐层失控增长"（用 500 随机样本可视化验证，Fig.4）。方案：在每个 attention 与 MLP **前后各加一个 RMSNorm**。两个 norm 都放在 AdaLN-Zero 的 scale 之前（避免训练初期对全零张量做归一化）；并对 post-norm 后的第二个 scale 预测加 **tanh gating**，防止过大调制值灌入残差分支。配合原有 QK-Norm，输入输出激活幅度都被控住。
- **Grouped-Query Attention（GQA）**：2B 模型把 **32 个 query head 分成 8 组**（8 个共享 KV head），降参降显存，高分辨率生成提速明显。
- **不用 long-skip connection**：消融发现长跳连会导致训练不稳定、显著恶化 Next-DiT，故弃用。

**文本编码器**：解码器式 LLM **Gemma-2B**（相比 Lumina-T2X 的 LLaMA-7B 更小，省显存、提吞吐）。论文还对比了 Qwen-1.8B、InternLM-7B——后两者在中文 prompt（含古诗）上图文对齐显著更好，印证"更强 LLM 文本编码器 → 更好生成"。
**VAE**：stabilityai 微调版 **sdxl-vae**（latent diffusion 范式）。
**参数 / 分辨率**：T2I 主模型 **2B**，训练分辨率 **1024×1024**（也支持 512×2048/2048×512 等），凭外推零样本到 **2K（2048×2048）与全景 1024×4096**。
**预测目标**：Rectified Flow（预测速度场 velocity）。

## 数据
论文是"改进 + 效率"导向，**未给出 T2I 主模型训练数据的来源/规模/配比/过滤的具体数字**（其图文数据基本沿用 [[lumina-t2x]]，论文坦承前代"训练数据不足"是 Lumina-T2X 弱对齐的原因之一）。HF 上有 `Lumina-Next-T2I` 与经 SFT 的 `Lumina-Next-SFT` 两档权重，但 README 也未披露数据明细。**T2I 数据 = 未披露**。

各扩展模态的数据则有明确披露：
- **多视图**：Objaverse 列表 + Cap3D 标注；同一 elevation 下 8 个随机 azimuth 渲染监督视图，再随机选 4 个配随机 elevation 渲染输入图，每物体 4 组训练样本。
- **文生音频**：在 **AudioSet-SL** 上训、**AudioCaps** 上微调；约 **3k 小时 / 1M 音频-文本对**；评测用 AudioCaps validation（494 样本，每条 5 条人标 caption）。预处理：采样率转 16kHz、补/截到 10 秒、FFT 1024 / hop 256、mel 谱 80×624；非标准词与 semiotic class 归一化。无标注音频用 Make-An-Audio 的伪 prompt 增强构造 caption。
- **文生音乐**：仅用 **LP-MusicCaps**，约 **0.92M 音频-文本对 / 3.7k 小时**；按时长分组成 batch 避免过度 padding，截断超 20 秒音频。
- **点云**：label 条件用 ShapeNet（按 [51] 预处理，每云随机采 256 点训练）；text 条件用 Cap3D。

## 训练方法
**训练目标**：**Flow matching / Rectified Flow**——噪声到数据的线性插值、预测常数速度场（沿用 Flag-DiT 的 flow 公式，保证稳定性与可扩展性）。HF 模型卡明确标注 prediction = Rectified Flow。

**采样侧（本文核心创新，多为训练-free）**：
- **优化时间表**：详细分析 Euler 解 Flow ODE 的局部截断误差与曲率——发现误差在 **t≈0（纯噪声）处最大、t≈1（干净数据）处次大**，中间时步最小；这与扩散模型 [[elucidating-edm]]（误差随接近干净数据单调增）相反，故"扩散调度不适配 flow"。提出两个参数化时间表：**Rational**（σ 参数，σ=1 退化为 uniform）与 **Sigmoid**（分段 sigmoid，两端步长大于中间）。全文采用 **sigmoid，µ=0.6, α=6, β=20**。该调度**零额外计算**。
- **高阶 ODE 解算器**：Flow ODE 形式简单（`ẋ=vθ(x,t)`，无扩散的半线性结构），可直接套经典显式 Runge-Kutta。用 **midpoint（二阶 RK）+ sigmoid 调度**，论文 §3.2 / Fig.12 报告在 **10–20 NFE**（midpoint 每步 2 次网络评估，即 5–10 步）持续优于 SDXL/PixArt-α + DPM-Solver；摘要亦表述为"**5–10 步**出高质量图"。**无需任何蒸馏**（README：10 步出图、无 distillation）。
- **Frequency-Aware Scaled RoPE**：诊断 NTK-Aware 在最低频分量做插值是次优——外推时许多维度遇到未见的重复周期 → 内容重复。先定位波长 = 训练序列长度的维度 `d_target = d_head·log_b(L/2π)`，按 `b' = b·s^(d_head/d_target)` 缩放 base，并对 d>d_target 取与 position interpolation 的较大值，显著抑制重复。
- **Time-Aware Scaled RoPE**：结合扩散"先全局后局部"的特性——**去噪早期用 position interpolation 保全局结构、后期渐变到 NTK-Aware 保局部细节**。令频率 base 随时间 t 变：`b'_t = b·s^(d_head/d_t)`，`d_t=(d_head−1)·t+1`。这是全文 2K 外推默认策略。
- **Time-Aware Context Drop（提速每步评估）**：把 ToMe 的复杂 bipartite 匹配换成简单 **average pooling**（只对 K/V 下采样，保留 query 完整视觉内容），并加时间感知：**t=0 全层 drop、t=1 不 drop**。在 1K 生成上 **~2× 加速**，与 Flash Attention 叠加在超高分辨率上收益更大；75% 下采样比下 2K 图质量持平甚至更好。

**多阶段 / 微调**：T2I 有经 SFT 的 `Lumina-Next-SFT` 档（视觉质量更好），但论文未给 SFT/偏好对齐的超参细节，**未报告 RLHF/DPO/reward model**。各扩展模态走"Next-DiT T2I 预训练 → 渐进式（分辨率/视图数）微调"，如多视图 256×256,N=4 → 512×512,N=4 → 512×512,N=8。

## Infra（训练 / 推理工程）
- **T2I 主模型的算力/GPU·时未在论文中给出**（未披露）。
- **多视图 MV-Next-DiT**（用 600M Next-DiT）给出明确成本（Table 2）：256×256 N=4 → **16 GPU × 45h**；512×512 N=4 → **16 GPU × 57h**；512×512 N=8 → **16 GPU × 72h**；total batch 分别 256×(N+1)/128×(N+1)/32×(N+1)，lr=1e-4，各 100k 迭代（A100）。
- **ImageNet 识别**（Next-DiT-base，86M，对标 ViT/DeiT）：固定分辨率预训 300 epoch，AdamW + cosine，lr=1e-3、wd=0.05、batch=1024，follow DeiT recipe；任意分辨率微调再 30 epoch，constant lr=1e-5、wd=1e-8。
- **稳定性工程**：sandwich norm + QK-Norm 支撑混合精度下大模型/长序列稳定训练（继承 Flag-DiT 的可扩展性）。
- **推理加速汇总**：少步（midpoint + sigmoid，10–20 NFE，无蒸馏）+ Time-Aware Context Drop（~2×）+ Flash Attention；2K 与全景全部 tuning-free。
- **部署**：开源代码 + 多档权重（HF / wisemodel）、官方多节点 demo，已并入 HuggingFace **diffusers**（2024-07-08）、社区有 ComfyUI wrapper。

## 评测 benchmark（把效果讲清楚）
本文是方法/效率论文，**T2I 主模型未报告 FID / GenEval / T2I-CompBench / DPG / MJHQ-30K / HPSv2 / ImageReward / PickScore 等标准数值**（多以定性对比呈现：2K/全景外推、少步采样、多语言/emoji 理解，主要对手 SDXL、PixArt-α、Lumina-T2I、MultiDiffusion、DemoFusion、ScaleCrafter）。下列为论文报告了具体数字的部分：

- **架构有效性（ImageNet-256，label 条件）**：Next-DiT 按 FID 与 Inception Score 收敛**显著快于** Flag-DiT 与 [[sit]]（Fig.6，曲线对比，无单点数值表）。
- **任意分辨率识别（ImageNet-1K，Next-DiT-base 86M）Table 1**：224×224 固定分辨率，**100 epoch 即 81.6% Top-1**（≈ DeiT-base 300 epoch 的 81.8%）；**300 epoch 82.3% > DeiT-base 81.8%**。Flexible（任意分辨率）推理：DeiT-base 仅 67.2%，Next-DiT 经 300E+30E 微调达 **84.2%**。
- **文生音频（AudioCaps）Table 4**：**FAD 1.03（↓最优）**、KL 1.45、CLAP 0.630；主观 **MOS-Q 77.53 / MOS-F 76.52**，全面优于 AudioGen-Large、Make-An-Audio(1/2)、AudioLDM(1/2/2-Large)、TANGO 等。消融 Table 5：去掉 dual-encoder → FAD 1.03→1.48、CLAP 0.630→0.601；不在 AudioCaps 微调 → FAD 2.09；换回 Flag-DiT → FAD 1.56/KL 1.91/CLAP 0.573（证明 Next-DiT 全面更优）。
- **文生音乐（MusicCaps）Table 6**：**FAD 3.75 / KL 1.24**，FAD 上超 MusicGen(4.50)、MusicLDM(5.20)、AudioLDM2(3.81) 等（注：AudioLDM2 KL 1.22 略优于本文 1.24）；主观 MOS-Q 83.56 / MOS-F 85.69（文-乐对齐主观分最强）。
- **点云（ShapeNet，CD×10³）Table 7**：Airplane MMD 3.371 / COV 49.21%；Chair MMD 12.975 / COV 48.33%，与 PointFlow、ShapeGF、PDiffusion 等强基线总体相当、互有胜负（MMD 上 ShapeGF 3.306 / PDiffusion 3.276 略低于本文 Airplane 3.371，本文非全面最优）；卖点是单模型训练于 256 点即可推理 256→8192 任意密度。
- **少步采样定性结论**：midpoint + sigmoid 在 **10–20 NFE**（5–10 步）持续优于 SDXL/PixArt-α + DPM-Solver（Fig.12）；uniform 时间表在少步下几乎全黑/全白（Fig.8，Euler 10 步对比）。
- **外推定性结论**：Next-DiT 的 3D RoPE（三维解耦外推）+ sandwich norm（稳输出幅度）使 2K 外推质量显著超 Lumina-T2X，无需 DemoFusion 式特殊推理算法；SDXL/PixArt-α 超训练分辨率即崩。

## 创新点与影响
**核心贡献**：(1) **Next-DiT 架构**——3D RoPE 替代 1D RoPE + 标识符、sandwich norm 控激活、GQA 提效，给出更稳更快收敛的扩散变换器骨干。(2) 首次系统研究 **3D RoPE 上的视觉外推**，提出 Frequency-/Time-Aware Scaled RoPE，实现**免训练 2K 与任意宽高比外推**。(3) 针对 flow 模型的 **sigmoid 时间表 + 高阶 ODE 解算器**，**无蒸馏 5–10 步**出图。(4) **Time-Aware Context Drop** 训练-free 提速每步评估（~2×）。(5) 用**小 2B Next-DiT + Gemma-2B** 超过前代大模型，并展示解码器式 LLM 文本编码器带来的**零样本多语言/emoji** 能力。(6) 同一框架覆盖识别/多视图/音频/音乐/点云，验证通用性。

**影响**：Next-DiT 成为 Lumina 系列后续骨干（Lumina-Image 2.0 的基础）；sandwich norm、3D RoPE、flow 专用时间表、免训练分辨率外推等设计被后续扩散变换器与统一生成工作广泛参考；少步 + Context Drop 给出无蒸馏的实用加速路径。已并入 HuggingFace diffusers，全代码 + 权重开源，可复现性强。

**已知局限**：T2I 标准基准（FID/GenEval/对齐打分）未在论文报告，难与同期 SOTA 做硬指标横评；训练数据明细未披露；前代遗留的弱对齐主要靠数据/SFT 缓解而非本文重点；高密度点云外推时生成密度反而下降（疑因 attention 矩阵过平滑）；多语言能力虽强但主要由英文图文对训练得来、属零样本涌现，非系统多语训练。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2406.18583
- arxiv_pdf: https://arxiv.org/pdf/2406.18583
- github（实际代码在 Lumina-T2X 单仓的 lumina_next_t2i 子目录；worklist 给的独立 Alpha-VLLM/Lumina-Next 仓库 404 不存在）: https://github.com/Alpha-VLLM/Lumina-T2X
- github_subdir: https://github.com/Alpha-VLLM/Lumina-T2X/tree/main/lumina_next_t2i
- hf_model (SFT): https://huggingface.co/Alpha-VLLM/Lumina-Next-SFT
- hf_model (T2I): https://huggingface.co/Alpha-VLLM/Lumina-Next-T2I
- hf_diffusers: https://huggingface.co/Alpha-VLLM/Lumina-Next-SFT-diffusers

## 本地落盘文件
- ../../../sources/omni/2024/arxiv-2406.18583.pdf
- ../../../sources/omni/2024/lumina-next--t2x-readme.md
- ../../../sources/omni/2024/lumina-next--t2i-readme.md
