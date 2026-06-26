---
title: "Emu Video: Factorizing Text-to-Video Generation by Explicit Image Conditioning"
org: Meta
country: US
date: "2023-11"
type: paper
category: video
tags: [t2v, video-generation, diffusion, image-conditioning, factorized, latent-diffusion, zero-snr, meta]
url: "https://emu-video.metademolab.com/"
arxiv: "https://arxiv.org/abs/2311.10709"
pdf_url: "https://arxiv.org/pdf/2311.10709"
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://emu-video.metademolab.com/"
downloaded: [arxiv-2311.10709.pdf, emu-video--project.md, emu-video--blog.md]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
Emu Video 是 Meta GenAI 2023 年 11 月的文生视频工作，核心创新是把 T2V **分解为两步**——先由文本生成一张图，再以"文本 + 这张生成图"作为更强条件生成视频（即"explicit image conditioning"）；只用**两个**扩散模型（生成 + 插帧）即可直出 512px、4 秒、16fps 视频，无需前作那种深级联（Imagen Video 7 模型、Make-A-Video 5 模型）。人评质量平均胜率 91.8%、文本忠实度 86.6%，对 Make-A-Video 质量胜率 96%、对 Imagen Video 81%，并优于 Gen2、Pika 等商用方案。

## 背景与定位
视频生成相比图像生成更难：要建模更高维的时空输出空间，而条件信号只有一句文本；且视频-文本数据集通常比图文数据集小一个数量级。当时主流范式（[[make-a-video]]、[[imagen-video]]）是用扩散模型**一次性直接生成全部帧**，条件信号始终只有文本。

Emu Video 的核心假设：**强化条件信号**对高质量视频生成至关重要（类比 NLP 中自回归生成——每一步预测都基于前文，条件越来越强）。但用扩散模型做自回归逐帧解码在算力上不现实（生成单帧本身就要多步迭代）。于是作者退而求其次，用一个**显式中间图像**来强化条件：把 T2V 拆成 (1) 文生图、(2) 图+文生视频。直觉上，给模型一张起始图，视频生成就变成"预测这张图如何向未来演化"，任务大大简化。

与同类工作的差异：
- 相对 [[make-a-video]]：MAV 用图像 embedding（语义条件，会丢失图像信息）且 finetune 全部参数（无法保留 T2I 的画质/多样性）；Emu Video 直接把第一帧拼进噪声（保留全部信息）且冻结空间层（保留 T2I 风格）。
- 相对 [[imagen-video]]：IV 用 7 模型像素级深级联；Emu Video 用 latent diffusion，仅 2 模型直出 512px。
- 相对 CogVideo：CogVideo 是自回归 Transformer，与 Emu Video 的显式图像条件在训练/推理机制上根本不同。
- [[stable-video-diffusion]]（SVD）被作者列为**并发工作**，采用了类似的图像条件分解思路。

定位上，Emu Video 是 Meta 视频生成的代表作，也是后续 **Movie Gen** 的思路前身（"先有强图像基座/条件、再生成视频"）。

## 模型架构
**整体**：单个 latent diffusion 模型 F（U-Net）同时承担"文生图"和"图+文生视频"两个角色；外加一个结构相同的**插帧模型** I。

- **Backbone**：U-Net（非 DiT），改编自 Meta 的 T2I 基座模型 [[emu-quality-tuning]]（论文中即 "Emu"，Dai et al. 2023）。
  - U-Net 配置（附录 Table 1）：`model_channels=384`，`channel_multipliers=[1,2,4,4]`，`num_res_blocks=[3,4,4,4]`，`attention_resolutions=[4,2,1]`，transformer `num_layers=2`、`d_head=64`。
  - **总参数 4.3B**：2.7B 空间参数（从 T2I 初始化并**冻结**）+ 1.7B 可训练时间参数。两模型级联（F + I）合计 **6.0B**（远小于 Imagen Video 的 11.6B、Make-A-Video 的 9.6B）。
- **时间层**：沿用 Make-A-Video 做法，在每个空间卷积后加 1D 时间卷积、每个空间注意力后加 1D 时间注意力；原空间卷积/注意力对 T 帧独立处理且冻结。时间参数用**恒等初始化**（卷积用 identity kernel，时间注意力最后 MLP 置零），实验中使收敛速度提升 2×。
- **VAE / tokenizer**：图像 VAE（`AutoencoderKL`，8 通道 latent，空间下采样 8×8，`base_channels=128`，`channel_multipliers=[1,2,4,4]`），逐帧应用到视频。512px 图 → 64×64×8 latent。
- **Text encoder**：**双文本编码器**——冻结的 T5-XL + 冻结的 CLIP；U-Net 中用**两套独立 cross-attention** 分别 attend 到这两路文本特征（context_dim 768 和 2048）。
- **图像条件注入**（关键设计）：把起始帧 I 当作单帧视频（T=1）做时间维 **zero-pad** 得到 T×C×H×W；再用一个二值 mask m（T×1×H×W，第一帧位置为 1）标记真实帧位置；将 mask、起始帧、带噪视频 X_t 在**通道维拼接**输入 U-Net。为此在首个空间卷积层 kernel 上加 C+1 个**零初始化**的可学习通道。输入张量形状 `[17, T, 64, 64]`（17 = 8 latent + 8 起始帧 latent + 1 mask），输出 `[8, T, 64, 64]`。
- **插帧模型 I**：架构与 F 相同，从 F 初始化、只训时间参数；输入 8 帧（4fps，零交错填充为 Tp 帧 + mask），输出 Tp=37 帧 @16fps；用"masked zero-interleaving"在每对帧间插 3 帧、首尾各补 4 帧，把 2s 输入扩成 2.3s。
- **分辨率/帧数**：直出 512px 方形视频，T=8 或 16 帧，1/2/4 秒、8fps 或 4fps；最终对外是 512px、4 秒、16fps。

## 数据
- **规模**：**34M licensed video-text pairs**（持牌视频-文本对）。视频长 5–60 秒，覆盖广泛的自然世界概念。
- **配比/清洗**：数据集**未针对特定任务做整理，未按文本-帧相似度或美学过滤**——默认用全量 34M 训练。
- **高质量微调子集**：从训练集中**自动**挑出 **1.6K** 高运动、高质量视频用于最后 HQ finetuning，筛选条件为：CLIP(f1) > 0.25、aesthetic(f1) > 5.7、连续帧最小运动分（H.264 编码运动矢量算出）> 0.5。
- **数据量消融（重要结论）**：在训练步数固定的前提下，**仅用 10% 数据**质量/忠实度也只小幅下降（约 43% 偏好，即接近持平），说明 Emu Video 对数据量不敏感，**只要训练步数足够**即可。相对地，减少低分辨率预训练**步数**（降到 75%/50%/25%）会逐步显著掉点——即"训练步数"比"数据量"更关键。

## 训练方法
- **训练目标**：conditional latent diffusion；MSE 损失，N=1000 步。256px 阶段用 `eps-pred`、512px/HQ/插帧阶段用 **v-prediction**。
- **零终端 SNR 噪声调度（核心 trick）**：作者发现标准噪声调度在终端时刻 N 仍残留信号（非零 SNR），训练-测试不一致；高分辨率视频因时空冗余残留信号更大。解决办法：缩放噪声调度令 αN=0（零终端 SNR rescale，沿用 Lin et al. 2023）。消融显示这对 512px 高分辨率直出**至关重要**（质量胜率 96.8%、忠实度 88.3%），对物体一致性和画质影响显著（对直接 T2V 模型主要影响色彩构图，对分解式方法影响更大）。
- **多阶段多分辨率训练**（消融胜率 81.8%/84.1%）：
  1. **256px / 8fps / 1s**，约 **70K** 迭代（占大头，单步比 512px 快 3.5×，跑满 1 个 epoch）；
  2. **512px / 4fps / 2s**，**15K** 迭代；
  3. （可选）**16 帧 / 4s** 再训 **25K** 迭代以增加时长。
  256px 用标准噪声调度，512px 用零终端 SNR。空间层虽在 512px 预训练，但推理切到 256px 不掉质量。
- **HQ 微调**（消融 65.1%/79.6，主要提升运动忠实度）：在 1.6K 高运动高质量子集上微调，batch 64，10K warmup，峰值 LR 2.5e-5。
- **参数冻结**（消融胜率 55.0%/58.1）：冻结空间层比全参微调效果更好且更省算力。
- **关键超参（附录 Table 3）**：Optimizer AdamW（β1=0.9, β2=0.999）；256px 阶段 batch **512**、峰值 LR 1e-4、warmup 1K、weight decay 0；512px 阶段 weight decay 1e-4；插帧 batch 384。
- **采样**：DDIM **250 步**。
- **CFG（多条件，附录式 1）**：`x̃ = x + w_i·(x(I) - x(∅)) + w_p·(x(I,p) - x(I))`，先图后文的有序组合（实验证明优于先文后图与无序版本）。生成图用 w_img=7.5；视频/插帧用 w_img=2.0、w_txt=7.5。作者发现 **w_p/w_i 之比直接控制运动量**：固定 w_p 增大 w_i → 更贴近初始图、偏相机运动；固定 w_i 增大 w_p → 更多运动但牺牲物体一致性。
- **插帧噪声增强**：训练时对条件帧加 t∈{0,...,250} 随机噪声；推理时对 F 的样本加 t=100。

## Infra（训练 / 推理工程）
- 训练用**标准视频-文本数据集**即可，不需要前作的深级联（如 Imagen Video 的 7 模型），实现大幅简化。
- 单步耗时：256px 阶段比 512px 阶段快 3.5×（分辨率降低带来），因此把约 4× 训练预算花在 256px 阶段。
- 推理流程：给定 prompt，先用 F（关掉时间层）生成图 I → 再用 I+prompt 喂 F 生成 T 帧高分辨率视频 → 用 I 提升 fps。16 帧视频的插帧做法：拆成两段 8 帧分别插帧，丢弃重叠帧后拼接，最终得 65 帧 @16fps（4.06 秒）。
- **GPU 型号、算力规模、GPU·时、并行/分布式策略、混合精度、吞吐量**：论文与博客**均未披露**。
- **量化、缓存、步数蒸馏等推理加速**：**未采用/未报告**（推理仍是 DDIM 250 步）。

## 评测 benchmark（把效果讲清楚）
评测以**人评为主**（作者指出 FVD 等自动指标不能反映质量提升），并提出 **JUICE** 评测协议——要求标注者在二选一时**勾选理由**（质量维度：像素清晰度、运动平滑度、可辨识物体/场景、帧一致性、运动量；忠实度维度：空间/时间文本对齐），并提供训练样例统一理解，显著提升标注者一致性（complete agreement 提升约 28%/24%）。每对比较取 5 名评测者多数投票。

**T2V 人评胜率（Emu Video vs 各方法，质量 Q / 忠实度 F，单位 %）**：
- vs Make-A-Video：96.8 / 85.1（质量/忠实度，图 2；图 6 另给质量偏好 MAV 96.8%、IV 81.8%——均为 Quality）
- vs Imagen Video：81.8 / 56.4（忠实度领先 56%，IV 因要求生成文字字符——latent diffusion 已知弱项）
- vs Align Your Latents：92.3 / 97.0
- vs PYOCO：90.5 / 81.1
- vs Reuse & Diffuse：87.0 / 95.7
- vs CogVideo：100.0 / 100.0
- vs ModelScope：78.5 / 98.4
- vs **Gen2（商用）**：96.9 / 87.7（图 2）；附录 Table 5：vs Gen2 78.5/87.7、vs Gen2 I2V 72.3/78.4
- vs **Pika Labs（商用）**：98.5 / 87.0（图 2）
- **平均**：质量 **91.8%**、忠实度 **86.6%**。

**自动指标（UCF101 zero-shot，Table 2）**：
- Emu Video：**FVD 317.1**（↓最优），**IS 42.7**。
- 对比：PYOCO FVD 355.2 / IS 47.8；Make-A-Video 367.2；Align Your Latents 550.6 / IS 33.0；MagicVideo 655.0 / IS 33.5。
- UCF101 人评 vs Make-A-Video：Q 90.1% / F 80.5%。

**图像动画 / I2V 人评（Table 3，Q/F %）**：
- vs VideoComposer：96.9/96.9（65 prompts）、97.4/91.2（307 prompts）
- vs Pika Labs I2V：84.6/84.6；vs Gen2 I2V：70.8/76.9
- vs VideoCrafter：81.5/80.0；vs SVD：72.3/73.9；vs I2VGen-XL：69.2/66.1
- I2V 自动指标（Table 6）：Emu Video FC 99.3 / IC 94.2 / TC 34.2（略低于 Pika/Gen2，但因这些指标偏好静态视频，而 Emu Video 运动量更大——motion score 4.98 vs Pika 0.63、Gen2 3.29）。

**关键消融（Table 1，采纳某设计 vs 不采纳，Q/F %）**：
- 分解 vs 直接：70.5 / 63.3（分解强偏好）
- 零终端 SNR：96.8 / 88.3（高分辨率直出的决定性设计）
- 多阶段训练：81.8 / 84.1
- HQ 微调：65.1 / 79.6（主要提升运动忠实度）
- 冻结空间层：55.0 / 58.1

**最近邻基线分析**：用文本 CLIP 特征从全量 34M 训练集检索真实视频作强基线，人评中 Emu Video 在忠实度上仍以 81.1% 胜出，证明非简单"检索复读"。

**长视频扩展**：小幅改架构后可条件于过去 16 帧 + 一个"未来 prompt"生成后续 16 帧，扩展视频能同时尊重原视频与未来文本。

## 创新点与影响
**核心贡献**：
1. **显式图像条件的分解式 T2V**——证明"先图后视频"的强条件能大幅提升 T2V 质量/忠实度，且把第一帧原样作为条件（而非语义 embedding）保留全部图像信息。
2. **零终端 SNR + 多阶段多分辨率训练**——使 latent diffusion 能**直出 512px 高分辨率视频**，绕开前作的深级联，把模型数从 5–7 个降到 2 个、参数从 ~10B 降到 6B。
3. **冻结空间层**保留 T2I 基座的风格/多样性，让同一模型天然支持**文生图、文生视频、图像动画（I2V）三种任务**，I2V 还可开箱即用。
4. **JUICE 人评协议**——可复现、高一致性的视频生成主观评测方法。

**影响**：是 Meta 视频生成路线的代表作，"用强图像基座/条件驱动视频生成"的思路被 **Movie Gen** 等后续工作延续；与并发的 [[stable-video-diffusion]] 共同确立了"图像条件分解"作为高质量 T2V 的主流范式之一。

**已知局限**（作者自述）：内容真实感、手/脸等细粒度细节伪影、物理建模、长时长一致性仍待改进；当条件首帧不能很好代表 prompt 时模型恢复能力有限；用纯自回归扩散逐帧解码来进一步强化条件目前算力上不划算。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2311.10709
- arxiv_pdf: https://arxiv.org/pdf/2311.10709
- project_page: https://emu-video.metademolab.com/
- official_blog: https://ai.meta.com/blog/emu-text-to-video-generation-image-editing-research/

## 一手源存档（sources/）
- [arxiv-2311.10709.pdf](https://arxiv.org/pdf/2311.10709) （PDF，gitignore 不入 git，已本地精读）
- [project.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/emu-video--project.md)
- [blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/emu-video--blog.md)
