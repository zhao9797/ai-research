---
title: "HunyuanVideo 1.5"
org: 腾讯混元 (Tencent Hunyuan Foundation Model Team)
country: China
date: "2025-11"
type: tech-report
category: video
tags: [video-generation, dit, t2v, i2v, flow-matching, sparse-attention, sparse-attn, video-super-resolution, open-source, lightweight, muon, distillation]
url: "https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5"
arxiv: "https://arxiv.org/abs/2511.18870"
pdf_url: "https://arxiv.org/pdf/2511.18870"
github_url: "https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5"
hf_url: "https://huggingface.co/tencent/HunyuanVideo-1.5"
modelscope_url: ""
project_url: "https://hunyuan.tencent.com/video/zh"
downloaded: [arxiv-2511.18870.pdf, arxiv-2511.18870.txt, hunyuanvideo-1-5--readme.md, hunyuanvideo-1-5--readme-cn.md, hunyuanvideo-1-5--hf-modelcard.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
HunyuanVideo 1.5 是腾讯混元 2025 年 11 月开源的**轻量级视频生成模型**：仅 **8.3B 参数**的统一 DiT 即可做 t2v/i2v，配合级联视频超分到 1080p，质量在开源阵营做到 SOTA（GSB 对 Wan2.2 T2V 胜率 +17.1%、I2V +12.7%），并靠 16×4 高压缩 3D VAE + SSTA 稀疏注意力把 720p 121 帧端到端推理压到**单张 RTX 4090 峰显存 13.6 GB**（开 offload）、480p I2V 步数蒸馏后单卡 4090 约 **75 秒**出片。

## 背景与定位
2025 年视频生成的 SOTA 被闭源系统垄断（Kling 2.5、Veo 3.1、Sora 2），开源侧虽有 [[hunyuanvideo]]、Step-Video、Wan2.2 等接力，但存在"质量"与"推理效率"难以兼得的结构性缺口：

- Wan2.2 用混合 MoE（两个 14B 专家、共 27B 参数、激活 14B）拉高画质，但参数管理带来显著算力开销；其 5B 轻量版靠高压缩 3D VAE 降显存，却在跨帧运动稳定性与美学细腻度上不及实用需求。
- HunyuanVideo 1.5 的论点是：**用一个紧凑的 8.3B dense DiT，靠数据策展 + 架构创新（SSTA 稀疏注意力 + glyph-aware 文本编码）+ 渐进式训练 + 高效超分，把质量做到逼近闭源、把门槛降到消费级显卡**，成为 2025 年末"开源视频代表"。

技术脉络上它承接 [[latent-diffusion-ldm]] / [[stable-diffusion-3]] 的 rectified-flow（flow matching）扩散范式，沿用 HunyuanVideo 的视频数据管线与 HunyuanImage 3.0 的图像/captioning 管线，并把"文生图先验 → 视频"这条 image-to-video 渐进训练路线走到底。

## 模型架构
**两阶段框架**：第一阶段统一 DiT 出 480p~720p、5~10s 的基础视频；第二阶段专用视频超分网络上采到 1080p。

### 1) Unified Diffusion Transformer（主模型，8.3B）
- **结构超参（Table 1）**：双流 block（dual-stream）× **54** 层；model dim **2048**；FFN dim **8192**；注意力头 **16**，head dim **128**。
- **多任务统一训练**：一个架构联合训 T2I / T2V / I2V。I2V 的参考图用两条互补路径注入——(1) **VAE 编码**：图像 latent 与噪声 latent 沿 channel 维拼接（保细节重建力）；(2) **SigLip 语义特征**：语义 embedding 按序列拼接（强化语义对齐与指令遵循）。用**可学习的 type embedding** 显式区分不同条件类型。
- **VAE**：因果 3D transformer 架构（causal 3D），图像/视频联合编码，**空间压缩 16×、时间压缩 4×、latent 通道数 32**。高压缩率显著减少 token 数，是 8.3B 也能跑长视频的关键。
- **文本编码器（双通道）**：
  - 通用语义通道用视觉-语言多模态编码器 **Qwen2.5-VL**，深度理解场景/人物动作/特定要求；
  - **Glyph-ByT5**（多语言 glyph 编码器）专攻视频内文字渲染准确度（中英双语 + 字形感知，故论文给出"墨滴落到宣纸上晕染成书法字『混元视频 1.5』"这类文字生成示例，Fig.2）。
  - 输入侧还有 Token Refiner、ByT5 Proj、Vision Proj、Patch Emb，配 **3D RoPE** 位置编码。
- **稀疏注意力 SSTA（Selective and Sliding Tile Attention）**：本作核心架构创新，**无参数设计**，可在任意训练阶段无缝接入（实际在蒸馏阶段引入稀疏训练以更好保质）。算法四步（Algorithm 1）：
  1. **3D Block Partition**：把 Q/K 按 tile（tilet×tileh×tilew）切块；
  2. **Selective Mask 生成**：对块做 adaptive pool，算 Q-K 块间相似度 Score_s 与 K-K 块间冗余 Score_r，块重要度 Score_i = λ·Score_s − β·Score_r，取 Top-k 选块；
  3. **STA（Sliding Tile Attention）Mask**：保留局部滑窗 WS=(wt,wh,ww) 内的块（静态局部先验）；
  4. **合并掩码做 block-sparse attention**：M_combined = M_sel ∧ M_sta，再用 flex_block_attention 执行。
  - 即"静态局部滑窗先验 + 动态全局自适应选块"二者协同，剪掉时空冗余 token。配套自研工程库 **flex-block-attn**（基于 ThunderKittens 框架实现 flex_block_attention）。效果：10s/720p 端到端相对 FlashAttention-3 **加速 1.87×**。

### 2) 视频超分网络（VSR，级联）
- 沿用主模型同款 **8.3B Video DiT**，在 **latent 空间**做超分（few-step 少步网络）。
- LR latent 用 channel concat 注入，并单独训一个 **latent upsample block** 做 LR/HR 空间对齐；最终 HR latent 经 VAE decoder 解码出 1080p。
- 流程：基础 DiT 出低分 latent F_LR → upsampler + noise → SR DiT 出 F_HR → VAE decode → HR 视频（Fig.3）。

## 数据
**图像 + 视频混合**，承接 HunyuanImage 3.0 与 HunyuanVideo 的管线并扩量精洗。

- **图像**：沿用 HunyuanImage 3.0 采集/处理管线，从 100 亿+ 图池里**策展 50 亿张**做预训练，**10 亿张**留作后续阶段。
- **视频采集**：多渠道采原始视频，覆盖多样内容/拍摄手法/镜头运动/风格/场景；基础去重 + 去损坏后得 **>1000 万小时**原始视频。
  - **切片**：PySceneDetect + 自研切分算子检测场景边界，切成 **2~10s** 一致片段；再用专门的转场分类器二次过滤掉残留转场片段。
  - **去水印/字幕/logo**：空间裁剪剔除受影响区域；裁后保留面积 <60% 的片段直接丢弃（保构图完整性）。
- **三级数据策展**：
  1. **Basic Filtering**：去 padding 黑边、拼接伪影、网格拼图（collage）、静态/低运动场景；
  2. **Visual Quality**：自研质量评估算子，从**清晰度、细节保真、噪声与伪影、动态范围**四维打分剔除低质；
  3. **Aesthetic Filtering**：基于 UGC 美学技术评估（Wu et al. 2023）打美学分剔除低分。
  - 过滤后**约 8 亿高质量视频片段**进预训练。
- **Captioning（三个专用模型）**：
  - **图像 caption**：同 HunyuanImage 3.0 方法；
  - **视频 caption**：高度结构化多组件描述——多层级文本叙事 + 电影/美学属性集（镜头类型、机位角度、构图、光照、风格、配色、氛围）；
  - **I2V 指令式 caption（新模块）**：描述相对首帧的时间演化/变换，分述前景主体与背景环境的变化。
  - **解决"丰富度 vs 幻觉"权衡**：caption 模型后训练引入 RL，具体用 **OPA-DPO**（On-Policy DPO，缓解 VLM 幻觉），pipeline 为 SFT → Ranking-DPO → OPA-DPO（含 temperature rollout、multi-trajectory rollout、critic model 打分、human corrector），在最大化细节的同时压幻觉。
  - **镜头运动描述**：专门的相机动态识别模型，clip 级 + 序列级识别多种运镜，高置信预测转自然语言并并入结构化 caption，目标是赋能"可控运镜"。

## 训练方法
**flow matching（rectified flow）** 范式，多阶段渐进式预训练 + 多阶段后训练（CT→SFT→RLHF），T2V/I2V 分别后训练。

### 预训练（progressive multi-stage，Table 2）
| Stage | 阶段 | 训练分辨率 | 数据量(视频/图像) | 任务 |
|---|---|---|---|---|
| I | Pretrain | 256p | 50 亿(图) | T2I |
| II | Pretrain | 512p | 10 亿(图) | T2I |
| III | Pretrain | 256p 16fps 2~10s | 8 亿 | T2V/I2V/T2I |
| IV | Pretrain | 480p 16fps 2~10s | 2 亿 | T2V/I2V/T2I |
| V | Pretrain | 720p 16fps 2~10s | 1 亿 | T2V/I2V/T2I |
| VI | Pretrain | 720p 24fps 2~10s | 1 亿 | T2V/I2V/T2I |

- **先训 T2I 打底**：256p→512p 两档，多宽高比按 bucket 组织。论文发现 T2I 先学好"文-图语义对齐"能**显著加速**后续 T2V/I2V 收敛与性能。
- **混合任务配比 T2I:T2V:I2V = 1:6:3**：大规模 T2I 数据增强语义理解与生成多样性，T2V/I2V 保证视频建模。
- **渐进 scaling**：256p/16fps → 480p → 720p/24fps，时长 2~10s。
- **shift 调度**：flow matching 对 shift 超参在 token 长度变化时高度敏感，故设计了一系列**随 token 长度自适应的 shift scheduling** 保证跨阶段训练稳定。

### 后训练（T2V/I2V 各自独立）
- **CT（Continue Training，Stage VII/VIII）**：480p/720p 24fps，每任务 100 万高质量片段，类别均衡、源自优质数据集；T2V 偏好高动态运动片段强化时序，I2V 引入"只描述相对首帧运动/变换"的指令式 caption 强化动作保真。T2V/I2V 的 CT 均从同一最优预训练 ckpt 初始化。
- **SFT**：每任务严选片段（美学、清晰度、运动平滑度严筛），进一步提稳定性/画质/美学/时序一致性。
- **RLHF（人类反馈对齐）**，T2V 与 I2V 策略不同：
  - **I2V — 在线 RL**：用 100+ 类别、高美学图构建的 prompt 集（VLM 生成 + 人工校验图文一致）；微调一个 **VLM-based reward model**，从 **文本对齐 / 图像对齐 / 视觉质量 / 运动动态** 四维打分；训练时混合采样（变 seed + 变 CFG scale），用 **MixGRPO（混合 ODE-SDE 求解器）** 丰富探索同时保采样质量。各指标一致提升，运动真实感增益尤为明显。
  - **T2V — offline-then-online 混合**：先做离线 **DPO**（curate ~O(10K) 平衡 prompt 集，覆盖运动/场景/主体；用高质 SFT ckpt 每 prompt 生 N 个候选配非重复对，人工 GSB 标注语义保真/运动质量/美学），显著减运动伪影、给出更优策略起点；再接与 I2V 同款的在线 RL 框架进一步提画质与语义对齐。
- **优化器 Muon**：本作关键 trick——Muon（来自 Kimi K2）相比 AdamW **仅用一半训练步数就达到更低 loss**，且在多个 T2I benchmark 上性能更优；weight decay=0.01 保稳。训练码已开源并附 Muon。

### 视频超分训练
- 用预训练 T2V 模型权重初始化 SR 模型；构建 100 万高质量片段（1K~4K 多分辨率、3~10s、24fps）+ 一批高分图增强细节；LR latent 与 noise channel concat 输入 DiT，全参可训，flow matching 范式。

### 蒸馏与加速（多版本权重）
- **CFG 蒸馏**：~2× 加速（cfg-distilled 版必须用 50 步才出正确结果）。
- **步数蒸馏（step distill）**：480p I2V 步数蒸馏版可 **8 或 12 步（推荐）** 出片，4 步更快但画质略降；RTX 4090 端到端时间降 ~75%，单卡约 75 秒。SR 也有 step-distilled 版（480→720 用 6 步、720→1080 用 8 步）。
- **稀疏注意力版**：仅 720p 模型配 SSTA；sparse_attn 会自动启用 CFG 蒸馏，需装 flex-block-attn，要求 H 系列 GPU。

## Infra（训练 / 推理工程）
- **训练**：训练码 `train.py` 支持分布式、**FSDP、context parallel、gradient checkpointing**，配 Muon 优化器、LoRA 微调脚本（2025-12-05 开源）。算力总规模/GPU·时未披露。
- **推理（论文实测）**，速度测于 **8× NVIDIA H800 + context parallelism**、CFG 蒸馏模型：
  - **无工程加速**（每扩散步 wall-clock，Table 7）：480p 121 帧 0.91s/步、241 帧 1.70s/步；720p 121 帧 2.01s/步（开 SSTA 1.56s/步）；720p 241 帧 5.51s/步（开 SSTA **2.95s/步**，长序列加速最明显）。
  - **开工程加速**（50 步总时长，Table 8）：用 **SageAttention**（注意力降显存提速）+ **torch.compile** 算子融合 + **feature caching**（非关键步复用缓存特征）。720p 121 帧 28.33s（+SSTA 26.41s）；720p 241 帧 96.78s（+SSTA **58.39s**）。
  - **缓存策略**（README 参数）：cache_start_step=11、cache_end_step=45、cache_step_interval=4。
  - **显存（单卡）**：开 pipeline offloading + group offloading + VAE tiling 后，720p 121 帧 T2V/I2V 端到端**峰显存 13.6 GB**，可在单张 RTX 4090 跑（README 给最低 14 GB）；社区 Wan2GP 可低至 6 GB VRAM。
- **部署形态**：官方 ComfyUI 支持 + 社区插件、LightX2V、Wan2GP、ComfyUI-MagCache（20 步 1.7× 加速）、吐司/TensorArt 在线、官网在线试用、Diffusers 集成（`HunyuanVideo15Pipeline`）。prompt 改写推荐 T2V 用 Qwen3-235B-A22B-Thinking-2507、I2V 用 Qwen3-VL-235B-A22B-Instruct（或 Gemini）。

## 评测 benchmark（把效果讲清楚）
评测用两法：**Rating**（多维打分诊断短板）与 **GSB**（Good/Same/Bad 相对偏好）。300 条文本 prompt + 300 张图样本，每输入单次推理不 cherry-pick，100+ 名专业评审。对手：Wan2.2、Kling2.1 Master、Seedance Pro、Veo3。

### T2V Rating（Table 3，分越高越好；HY1.5 为 720p）
| 维度 | HY1.5 720p | Wan2.2 | Kling2.1 Master | Seedance Pro | Veo3 |
|---|---|---|---|---|---|
| 指令遵循 | **73.77** | 61.57 | 44.07 | 50.03 | 53.19 |
| 美学质量 | 67.98 | 63.30 | 65.98 | 68.00 | **68.22** |
| 视觉质量 | 58.64 | 57.35 | 56.37 | 59.68 | **60.20** |
| 结构稳定性 | 75.62 | **79.75** | 73.75 | 66.74 | 68.69 |
| 运动效果 | **60.81** | 57.67 | 53.08 | 58.59 | 55.17 |

→ HY1.5 在**指令遵循、运动效果**上领先全部对手（含闭源），美学/视觉质量逼近 Veo3/Seedance，结构稳定性略逊 Wan2.2。

### I2V Rating（Table 4）
| 维度 | HY1.5 480pSR | HY1.5 720p | Wan2.2 | Kling2.1 Master | Seedance Pro | Veo3 |
|---|---|---|---|---|---|---|
| 指令遵循 | 63.11 | 63.05 | 56.19 | **68.43** | 62.90 | 67.86 |
| 图像一致性 | 68.82 | 72.07 | **73.53** | 64.09 | 73.06 | 72.19 |
| 视觉质量 | 59.87 | 60.33 | 58.31 | 59.28 | 58.95 | 59.29 |
| 结构稳定性 | 70.13 | 66.67 | 69.03 | 59.71 | 68.01 | 69.25 |
| 运动效果 | 57.60 | 58.62 | 57.41 | 57.36 | 60.47 | **60.91** |

→ I2V 视觉质量小幅领先，其余维度与第一梯队互有胜负。"480pSR"指先出 480p 再用 SR 上采到 720p，与直出 720p 几乎同档，印证级联超分的有效性。

### GSB（720P，HY 净胜率 = HY better − other better；Table 5/6）
- **T2V**：对 Wan2.2 **+17.12%**、对 Kling2.1 Master **+12.6%**、对 Seedance Pro **+11.02%**；对 Veo3 **−10.32%**（落后闭源标杆）。
- **I2V**：对 Wan2.2 **+12.65%**、对 Kling2.1 Master **+9.72%**；对 Seedance Pro **−5.77%**、对 Veo3 **−3.61%**。

→ 结论：在**开源**视频生成里建立新 SOTA（对 Wan2.2 显著胜出），整体逼近但仍略落后于 Veo3/Sora2 量级的顶级闭源。

### 关键消融/工程结论
- **SSTA 加速**：10s/720p 端到端相对 FlashAttention-3 加速 **1.87×**；241 帧场景下每步从 5.51s→2.95s。
- **Muon vs AdamW**：半数训练步达更低 loss，且多 T2I benchmark 更优。
- 注：FID / CLIPScore / VBench / GenEval 等自动指标本技术报告**未报告**，评测以人评 Rating + GSB 为主。

## 创新点与影响
**核心贡献**
1. **轻量高性能架构**：8.3B dense DiT + 16×/4× 高压缩 3D causal VAE，参数量远小于 Wan2.2(27B MoE) 却质量逼近，证明"小而精"路线在视频生成可行。
2. **SSTA 稀疏注意力**：无参数、可任意阶段插入的选块+滑窗双机制稀疏注意力，长视频端到端 1.87× 加速，配自研 flex-block-attn 库（基于 ThunderKittens）开源。
3. **glyph-aware 双语理解**：Qwen2.5-VL + Glyph-ByT5 双通道，强化中英双语理解与视频内文字渲染准确度。
4. **端到端训练优化**：首次系统性把 **Muon 优化器**用于视频生成训练（半步数更低 loss）+ 多阶段渐进训练（T2I 打底 → 渐进 scaling → CT/SFT/RLHF）+ I2V/T2V 差异化 RLHF（MixGRPO 在线 RL + DPO）。
5. **高效级联超分**：少步 SR DiT 在 latent 空间上采到 1080p，纠畸变补细节。
6. **消费级可达性**：720p 121 帧峰显存 13.6 GB / 单卡 4090 可跑；步数蒸馏后 480p I2V 单卡 4090 ~75s。

**影响**
- 2025 年末**开源视频生成的代表作**之一，把"逼近闭源画质"与"消费级显卡可跑"首次较好地统一，显著降低创作与研究门槛。
- 完整开源（推理码、训练码、Muon、LoRA 脚本、多档蒸馏/稀疏权重、Diffusers 集成、ComfyUI），并衍生出 **OmniWeaving**（在 HunyuanVideo 1.5 之上构建的 omni 级统一视频生成模型，支持 T2V/首帧/关键帧/视频编辑/参考生视频/多图组合等）。

**已知局限**
- GSB 上对 **Veo3（T2V −10.32%）、Sora2 量级闭源**仍有差距；I2V 对 Seedance Pro/Veo3 略负。
- 结构稳定性略逊 Wan2.2。
- 算力总规模、GPU·时、并行策略细节及自动化指标（FID/VBench 等）未披露。
- 截至 README 时点，部分权重（720p T2V cfg-distill、稀疏 cfg-distill 等）仍标 "Coming soon"。

## 原始链接
- tech-report (arXiv abs): https://arxiv.org/abs/2511.18870
- tech-report (PDF): https://arxiv.org/pdf/2511.18870
- github: https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5
- hf (model card / 权重): https://huggingface.co/tencent/HunyuanVideo-1.5
- 官网在线试用: https://hunyuan.tencent.com/video/zh?tabIndex=0
- flex-block-attn 稀疏注意力库: https://github.com/Tencent-Hunyuan/flex-block-attn
- OmniWeaving (衍生统一模型): https://github.com/Tencent-Hunyuan/OmniWeaving

## 本地落盘文件
- ../../../sources/omni/2025/arxiv-2511.18870.pdf  （技术报告 PDF，8 页，已精读）
- ../../../sources/omni/2025/arxiv-2511.18870.txt  （pdftotext 全文）
- ../../../sources/omni/2025/hunyuanvideo-1-5--readme.md  （GitHub README 英文）
- ../../../sources/omni/2025/hunyuanvideo-1-5--readme-cn.md  （GitHub README 中文）
- ../../../sources/omni/2025/hunyuanvideo-1-5--hf-modelcard.md  （HF model card）
