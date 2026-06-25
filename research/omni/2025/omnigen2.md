---
title: "OmniGen2: Towards Instruction-Aligned Multimodal Generation"
org: "北京智源 BAAI"
country: China
date: "2025-06"
type: paper
category: unified
tags: [unified, multimodal-generation, t2i, image-editing, in-context, decoupled-decoding, omni-rope, grpo, rectified-flow, open-source]
url: "https://arxiv.org/abs/2506.18871"
arxiv: "https://arxiv.org/abs/2506.18871"
pdf_url: "https://arxiv.org/pdf/2506.18871"
github_url: "https://github.com/VectorSpaceLab/OmniGen2"
hf_url: "https://huggingface.co/OmniGen2/OmniGen2"
modelscope_url: "https://www.modelscope.cn/models/OmniGen2/OmniGen2"
project_url: "https://vectorspacelab.github.io/OmniGen2"
downloaded: [arxiv-2506.18871.pdf, arxiv-2506.18871.txt, omnigen2--readme.md, omnigen2--hf-modelcard.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
OmniGen2 是智源 BAAI 的开源统一多模态生成模型，核心创新是**「冻结 VLM + 随机初始化 diffusion decoder」的解耦双路架构**（文本与图像走两套不共享参数的 transformer，图像用独立 tokenizer）外加 **Omni-RoPE 多模态位置编码** 与**多任务渐进式 RL 对齐（Flow-GRPO）**。仅 **4B 可训练参数**就在 GenEval 上拿到 **0.95**（超过 BAGEL 0.88、Qwen-Image），并自建 in-context 评测 **OmniContext（综合 7.95）**，编辑/IC 全面对齐后显著提升。

## 背景与定位
2025 年 GPT-Image-1、FLUX、Qwen-Image、Seedream、Nano-Banana 等模型把"统一多模态生成"（文生图 + 编辑 + in-context 生成）推到通用智能门槛。论文指出该方向有两大痛点：(1) **基座模型不够好用**——开源模型要么专精单任务、要么被过度调到某种美学偏好上而丧失可塑性（plasticity），难以作为对齐起点；(2) **缺乏全面的指令对齐**——需要明确且可覆盖所有任务的 reward 信号。

OmniGen2 是 [[omnigen]]（OmniGen v1，CVPR 2025 同组）的升级：v1 是单 transformer，v2 改为**文本/图像双解码路径、不共享参数、独立图像 tokenizer**。其设计与 [[metaqueries]]（MetaQuery）思路相近——都用 VLM 桥接到 diffusion——但执行不同：MetaQuery 用**定长 learnable query token** 压缩指令（造成信息瓶颈），OmniGen2 直接条件化在 **VLM 变长 hidden states** 上避免瓶颈；且训练期 VLM 大部分时间冻结，比 [[bagel]]（BAGEL）、Mogao 这类全量联合训练更高效。训练目标用 **Rectified Flow**（同 [[latent-diffusion-ldm]] 之后的 flow matching 范式、[[flux-1-kontext]] / SD3 一脉）。

## 模型架构
**总体：解耦双路（Decoupled Pathways）。** 两个独立 transformer 顺序工作（见论文 Fig. 2）：

1. **自回归 transformer（理解 + 高层语义）**：从 VLM **Qwen2.5-VL-3B-Instruct** 初始化，提供世界知识与多模态指令理解。输入图像经 **ViT tokenizer** 喂给文本 transformer。学习一个特殊 token `<|img|>` 区分"理解"与"生成"任务；一旦生成该 token 即触发图像生成，把对应的 VLM 末层 hidden states 抽出来作为 diffusion decoder 的条件（编码高层语义指令）。
2. **diffusion transformer（图像合成）**：**随机初始化**，专做高保真渲染，backbone 沿用 **Lumina-Image 2.0** 架构（**参数跨模态共享**，作者认为语言与视觉共享语义表征，共享参数比维护独立路径更自然高效）。进入核心 transformer block 前，三类条件信号（VLM hidden states、VAE 特征、含噪 latent）先经一个**两层 transformer refiner** 对齐（refiner 与 Lumina-Image 2.0 的 block 同构）。

**两套图像编码器（解耦 tokenizer）**：
- **ViT**（Qwen2.5-VL 自带）编码输入图像 → 进文本 transformer，做理解；
- **Flux-VAE**（来自 [[flux-1-kontext]] / FLUX）编码图像 → 进 diffusion transformer，提供**低层视觉细节**，保证编辑等任务的细粒度一致性。

**条件注入的关键取舍**：diffusion decoder **只用文本 token 对应的 VLM hidden states**（不用图像 token 的 hidden states），因为 VAE 特征已经提供了足够的视觉细节；这避免了对预训练 VLM 做复杂结构改造，保住其指令理解能力。

**Omni-RoPE（统一位置编码）**：把 RoPE 扩展到多模态。每个 token（第 k 张图、坐标 (h,w)）赋三维位置标识 `PosID = (ΔI^(k), h, w)`：`ΔI` 是**实例身份**（区分不同图像/模态，同一图像内所有 token 共享），(h,w) 是**图内 2D 局部坐标**（每张图从 (0,0) 起算）。这样输入图与输出图的对应 patch 拿到**相同的空间嵌入**，保证编辑时空间对齐与编辑一致性；而 `ΔI` 提供显式区分视觉实例的通道，对 in-context 生成与多图推理至关重要。文本 token 退化为标准 1D 索引。

**参数量**：理解侧 **3B**（Qwen2.5-VL-3B），生成侧 **4B**（diffusion transformer，随机初始化）；论文记为 "3B + 4B*"。**可训练参数仅 4B**（VLM 大部分时间冻结）。**分辨率策略**：256²→512²→1024² 渐进 curriculum。

## 数据
全部为自建大规模流水线 + 公开数据混合（论文已开源数据集与构建流水线）。

**基础知识与通用能力（基座）**：
- 多模态理解：采用 **LLaVA-OneVision**；
- 文生图（T2I）：约 **140M** 开源图文对（来自 LAION-5B、PixArt、ShareGPT4V、JourneyDB、DenseFusion-1M、DOCCI、ALLaVA 等多源）+ **10M** 自有图像（用 **Qwen2.5-VL-72B** 标注 caption）。

**编辑 / in-context 高级能力（自建流水线，填补公开数据空白）**：
- 编辑：整合公开的 **SEED-Data-Edit、OmniEdit**，并自建两类数据：
  - **Inpaint 数据**：取少量高质量 T2I 图，用 **FLUX.1-Fill-dev** 随机 inpaint（**不给 inpaint 模型指令**，让它随机填充）得到 input，原图为 target（保证 target 高质量），再用 **Qwen2.5-VL** 根据 (原图, inpaint 图) 对**反写**编辑指令——避开传统"预设指令→inpaint"导致的指令-图像不匹配。
  - **视频数据**：从视频抽帧构造编辑对（覆盖动作修改、物体移动、表情变化等 inpaint 做不出的任务）。流水线：按 RGB 均值 + HSV 滚动差检测场景边界做**场景分割**→用 **DINOv2 + CLIP** 过滤视点变化过大/过小的帧对→把图分块比对**对应块的颜色直方图**判定视点一致性（比 VLM 便宜、比像素相似更鲁棒）→ **Qwen2.5-VL-72B** 生成精确编辑指令。
- in-context 生成/编辑：从视频源构建，用 VLM 做主体检测、分割、语义过滤，得到主体跨场景一致的 triplet。
- **更高层推理（reflection / interleave）**：构建交错帧序列（intra-/inter-scene，最多 5 帧）与**反思（reflection）数据**——模型先生成图，再用 MLLM（**Doubao-1.5-pro**）指出问题与修改建议，把图与反思 append 回指令做 SFT，多轮迭代自反思，增强时序推理与自我纠错。

**RL 阶段数据**：50k T2I prompts（来自 Flow-GRPO）+ 110k 编辑样本（EditScore）+ 180k in-context 数据（Echo-4o）。

## 训练方法
**目标函数**：**Rectified Flow**（flow matching），用 **FlashAttention-2** 处理变长上下文。整体 = **两阶段基座（预训练→SFT）+ 渐进式 RL 对齐**（论文 Table 6）。

**1. 预训练（从零）**：分辨率 curriculum 256²→512²→1024²；每个分辨率**先 T2I-only 建立强文图对齐，再引入混合任务**（编辑 + in-context）扩能力。步数：256² 各 50k（T2I/Mixed）、512² 各 30k、1024² 各 50k。

**2. SFT**：1024² 分辨率，混合任务 **100k** 步；在精选数据 + 蒸馏自闭源模型的数据上训练，提升指令遵循与视觉保真。

**3. 指令对齐（在线 RL，渐进 curriculum）**：用 **Flow-GRPO**（GRPO 用于 flow matching）。不做单阶段联合训练，而是把对齐拆成多个**有序**阶段，避免任务干扰。每个任务 `T = (τ, δ, R)`，τ ∈ {T2I, Edit, IC}：
- **Edit**：用学习型 reward 模型 **EditScore**（同组工作）；
- **T2I**：用 **GenEval**（可验证 reward，与 Edit/IC 重叠度高）；
- **IC**：用 **Qwen2.5-VL-72B** 打分。
- **刻意排除**：美学 reward **HPSv3**（确认会 reward hacking）、OCR 等专用任务（与通用指令遵循无协同）。
- 最终三阶段 curriculum **⟨Edit → T2I(GenEval) → IC⟩**，512² 分辨率共约 **2.4k** 步（T2I/Edit/IC 分别约 1500/700/200 步）。

**消融关键结论（Table 5）**：(1) 技能不重叠的任务会**负迁移**（加 OCR 把 GEdit 从 6.28 降到 6.13）；(2) 技能重叠任务有**强协同**（Edit & GenEval 在各自指标上都超过单任务）；(3) **人类偏好 reward 高风险**（Edit & HPSv3 把 PQ 刷到 8.22 但 SC/IC 崩溃，典型 reward hacking）；(4) **准确性 reward 至关重要**；(5) **训练顺序敏感**——最终顺序 (Edit→GenEval→IC) 比 (Edit→IC→GenEval) 在 GEdit Overall 高 0.15（7.21 vs 7.06），且**编辑优先**始终优于 T2I 优先（编辑监督更丰富，为后续打基础）。RL 对所有任务一致提升（Base 无 RL 的 GEdit 6.28 → 7.21）。

## Infra（训练 / 推理工程）
**训练 infra**：论文未披露 GPU 型号/卡数/GPU·时/并行策略，仅明确用 **FlashAttention-2** 处理变长序列。强调**效率**：VLM 大部分时间冻结，**仅 4B 可训练参数**，"以 15M T2I 对 + 50k RL prompts 训练"即达到 GenEval 0.95 的 SOTA（论文 §9.10 突出"exceptional efficiency"）。

**推理工程（来自 HF model card / GitHub README）**：
- **显存**：原生约 **17GB VRAM**（NVIDIA RTX 3090 等可跑）；开 `enable_model_cpu_offload` **省近 50% 显存**且速度几乎无损；`enable_sequential_cpu_offload` 可压到 **<3GB** 但显著变慢。
- **加速**：支持 **TeaCache**（默认阈值 0.05 约 **30% 加速**，可调 latency/质量权衡）与 **TaylorSeer**（2025-07 起）；减小 `cfg_range_end`（CFG 作用的 timestep 区间末端）可显著减少推理时间、质量影响可忽略（依据 arXiv:2404.07724）。
- **关键推理超参**：双路 CFG——`text_guidance_scale`（文本遵循强度）、`image_guidance_scale`（与参考图相似度，编辑建议 1.2–2.0、in-context 建议 2.5–3.0 以保细节）；`max_pixels` 默认 1024×1024。
- 2025-06-23 起**无需 flash-attn 也可运行**（装上性能更优）。官方在 **A800 GPU** 上给出推理效率表（数据为图，本页未抠到具体数值）。
- **部署**：HF Spaces / 多路 Gradio 在线 demo / Jupyter；权重在 HuggingFace 与 ModelScope。许可 **Apache-2.0**。

## 评测 benchmark（把效果讲清楚）
**理解（Qwen2.5-VL-3B 直出）**：MMBench **79.1**、MMMU **53.1**、MM-Vet **61.8**。

**文生图 T2I**：
- **GenEval 0.95**（LLM rewriter 下）——超过 UniWorld-V1 (0.84)、BAGEL (0.88)，也超专精 T2I 的 Qwen-Image (0.91)；细分见 Table 11。RL 对齐是主要功臣（Base 无 RL 仅 0.78）。
- **OneIG-Bench-EN 0.47**（综合 realism）——超多数现有模型，仅落后大规模模型 Gemini 2.5 Flash Image、Qwen-Image。

**图像编辑**（三基准）：
- **Emu-Edit**：CLIP-Out **0.311**（所有对比模型中**最高**，最有效应用编辑）；CLIP-I **0.896**（第二）、DINO **0.876**（最高）→ 精确局部编辑且不扰动其余区域。
- **GEdit-Bench-EN**：SC **7.58**（第二）、PQ **7.94**（最高）、Overall **7.21**——超过 Gemini-2.5-Flash-Image (7.10)，开源里仅次于 Qwen-Image-Edit-2509 (7.54)。（对照：GPT-4o 7.53、Gemini-2.5-Flash 7.10、Gemini-2.0-Flash 6.32）
- **ImgEdit-Bench 3.69**——超过 BAGEL (3.20) 等强开源模型（Qwen-Image-Edit-2509 4.41、Gemini-2.5-Flash-Image 4.28 更高）。

**in-context 生成（OmniContext，本文新建基准）**：
- 8 个子任务（Character/Object/Scene × SINGLE/MULTIPLE/SCENE，每子任务 50 例），用 **GPT-4.1** 按 Prompt Following (PF)、Subject Consistency (SC)、Overall（PF 与 SC 几何平均）打分（0–10，附 rationale，follow VIEScore）。
- OmniGen2 **Overall 7.95**——开源里**超过 Qwen-Image-Edit-2509 (7.69)**、BAGEL (7.75)、UNO (5.73)、OmniGen v1 (4.34)；在所有任务类型上全面领先开源模型。闭源里 **GPT-4o (8.80)** 最高，Gemini-2.5-Flash-Image (8.44)。子任务示例：SINGLE-Object 8.63、MULTIPLE-Char.+Obj. 7.93、SCENE-Character 7.75。

**综合对比（Table 2）**：OmniGen2 在"理解 + T2I + 编辑 + in-context"四象限同时给出有竞争力的数字，是少数四项全测的统一模型。

## 创新点与影响
**核心贡献**：
1. **解耦双路架构**：冻结 VLM（Qwen2.5-VL-3B）+ 随机初始化 diffusion decoder（Lumina-Image 2.0 backbone）+ **独立双 tokenizer**（ViT 给理解、Flux-VAE 给生成），diffusion 仅条件化在 VLM 文本 token 变长 hidden states 上——比 MetaQuery 的定长 query 无瓶颈，比 BAGEL/Mogao 全量联合训练更省（仅 4B 可训练参数）。
2. **Omni-RoPE**：实例身份 ΔI 与图内 2D 坐标解耦的三维位置编码，toy 实验验证收敛步数从 ~2500（Lumina）/~1200（Qwen2-VL）降到 ~800 且 final loss 最低，提升跨图定位与编辑空间一致性。
3. **多任务渐进式 RL 对齐**：Flow-GRPO 三阶段 curriculum（Edit→T2I→IC）+ 精选 reward（EditScore / GenEval / Qwen2.5-VL-72B，刻意弃 HPSv3 防 reward hacking），系统性证明**任务选择与顺序**对跨任务协同至关重要。
4. **OmniContext 基准**：首个系统评估 in-context（reference-based）生成、支持多输入图、用 MLLM 打分带 rationale 的基准，填补 DreamBench（仅 30 物体/25 模板 + CLIP-I 无解释性）的空白。
5. **全开源**：模型、代码、基准、训练数据、数据构建流水线全开（Apache-2.0）；衍生 OmniGen2-EditScore7B（RL reward LoRA）。

**影响**：为社区提供资源高效（17GB VRAM 可跑）的统一多模态生成基座 + 标准化 in-context 评测；"冻结 VLM + diffusion decoder + 解耦 tokenizer + 多任务 RL"成为开源统一生成的一条主流路线。

**已知局限**（论文 §8.4）：(1) 中文 prompt 明显弱于英文；(2) 难以准确修改人体体型（真实数据稀缺）；(3) 对输入图质量高度敏感（低质/低分辨率输入显著退化）；(4) 多图输入指令有歧义时表现下降，需显式指明"哪张图的哪个物体"；(5) in-context 偶尔无法完美复现参考物体，提高 image guidance 只能部分缓解，作者推测需进一步**扩大模型规模**；reflection 机制易"过度反思"简单指令（受限于 3B MLLM 与反思数据量）。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2506.18871
- arxiv_pdf: https://arxiv.org/pdf/2506.18871
- github: https://github.com/VectorSpaceLab/OmniGen2
- hf: https://huggingface.co/OmniGen2/OmniGen2
- modelscope: https://www.modelscope.cn/models/OmniGen2/OmniGen2
- project_page: https://vectorspacelab.github.io/OmniGen2

## 本地落盘文件
- ../../../sources/omni/2025/arxiv-2506.18871.pdf
- ../../../sources/omni/2025/arxiv-2506.18871.txt
- ../../../sources/omni/2025/omnigen2--readme.md
- ../../../sources/omni/2025/omnigen2--hf-modelcard.md
