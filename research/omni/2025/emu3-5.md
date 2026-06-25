---
title: "Emu3.5: Native Multimodal Models are World Learners"
org: "北京智源 BAAI"
country: China
date: "2025-10"
type: tech-report
category: omni
tags: [native-multimodal, autoregressive, next-token-prediction, world-model, interleaved, x2i, discrete-diffusion, open-source]
url: "https://arxiv.org/abs/2510.26583"
arxiv: "https://arxiv.org/abs/2510.26583"
pdf_url: "https://arxiv.org/pdf/2510.26583"
github_url: "https://github.com/baaivision/Emu3.5"
hf_url: "https://huggingface.co/BAAI/Emu3.5"
modelscope_url: ""
project_url: "https://emu.world"
downloaded: [arxiv-2510.26583.pdf, emu3-5--github-readme.md, emu3-5--hf-card.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Emu3.5 是 BAAI 智源的 **34B 原生多模态自回归世界模型**：用**统一 next-token 预测**在 **>10T（实际约 13T）视觉-语言交错 token**（主要来自 6300 万条互联网视频的关键帧+ASR 转写）上端到端预训练，再加大规模多任务 RL（GRPO），并提出 **DiDA（离散扩散适配）**把逐 token 解码转成双向并行解码、**单图推理提速约 20×**。单一 32B/34B 模型在图像生成/编辑上**追平 Gemini 2.5 Flash Image（Nano Banana）**，在交错生成（视觉叙事/视觉引导/世界探索/具身操作）上**对 Nano Banana 胜率 49.2%~67.1%**，且全套开源。

## 背景与定位
- **要解决的问题**：语言模型只见"文字世界"，而人类主要靠视觉、尤其"长视频+语言交错"学习因果与时序一致性。此前 [[emu3]] 等 Emu 系列已证明 next-token 统一建模交错视觉-语言序列可行，但只在**短样本/小规模**上做，留下三个开放问题：(1) 如何把**长视频交错文本**的预训练 scale 上去；(2) 如何做通用多模态后训练；(3) 如何高效预测**上万个视觉 token**（推理太慢）。Emu3.5 分别用 **10T+ 视频交错预训练 / 统一多任务 RL / DiDA** 回应这三点。
- **技术脉络中的位置**：属于"纯离散 token + 自回归"的统一多模态路线（区别于 [[bagel]] 的混合 understanding/generation、[[janus-pro]] 的解耦编码、以及 diffusion/MMDiT 路线如 [[flux-2]]/[[qwen-image]]）。其最大差异点是把"**世界建模**"（world exploration / embodied manipulation）作为一等任务，并首次让 AR 模型在**速度与质量上同时逼近闭源 diffusion**。
- **相对前作改进**：相比 Emu3（8B），参数 4×、视觉 token 减半（同分辨率下 720²用 8100 token → 1024²只用 4096 token），GenEval 0.66→0.86、DPG 80.6→88.26，且推理效率因 DiDA 反而更优。

## 模型架构
**Backbone（统一 Transformer / 纯自回归 decoder-only）**
- 架构沿用类 **Qwen3** 的标准 decoder-only Transformer，做了若干多模态适配。
- 规格（Table 1）：**64 层**，hidden 5120，intermediate 25600，**64 个注意力头 / 8 个 KV 头（GQA）**，**总参数 34.1B**（Transformer 层 31.2B + embedding 层 2.9B），上下文长度 **32768**，dropout 0.1。
- 稳定性 trick：**RMSNorm + pre-norm**，对 Q/K 投影加 **QK-Norm**，**SwiGLU** 激活，**RoPE** 位置编码。
- **词表 282,926**：文本 151,854（直接复用 QwenTokenizer，保多语种）+ **视觉 131,072**。模型由 **Qwen3 初始化**。
- 视觉与文本完全统一为离散 token，拼成"文档式"序列，做标准交叉熵 NTP；**视觉 token loss 权重 0.5**（预训练阶段），防止视觉 token 淹没训练动态。

**Visual Tokenizer（455M，IBQ 框架）**
- 采用 **IBQ** 量化框架，**下采样 f=16**，码本维度 D=256，**码本扩到 131,072**，tokenizer 宽度放大到 **455M 参数**。
- 借鉴 **REPA**，在 tokenizer decoder 中间层蒸馏 **SigLIP（siglip-large-patch16-256）特征**，增强离散 token 的语义性。
- 重建效率：表示同一张图只用 **Emu3 的 1/4 token 数**。1024×1024 图 ≈ 4096 token；512×512 ≈ 1024 token。

**两类可选解码器（条件注入更精细的视觉细节）**
- **Diffusion 图像解码器**（可选，替代 vanilla decoder）：输入同样的量化 token，输出 **2× 分辨率**，显著改善文字区域与人脸细节。用 **Flow-matching** 训练、**SD3.5-medium 初始化**；再用 **LoRA 蒸馏把去噪步数 50→4（约 10× 加速）**。最终支持**最高 2K 分辨率**输出。
- **Diffusion 视频解码器**（DiT 架构，**Wan2.2 5B 初始化**）：以生成的关键帧 token 为条件生成连续视频，用 VQ 量化 embedding 提供细粒度细节、可选帧间文本提供高层语义；加 4 通道 mask 指示哪些帧 token 已给定，支持任意数量中间帧。

## 数据
预训练总量 **>13T 多模态 token**，四大组成（采样比见"训练方法"Table 2）：

**(1) 视频交错数据（最核心，占采样比 0.55）**
- 来源：开源数据集 + 公开网络视频 + 第三方合作视频，共 **约 6300 万条视频**，平均时长 **6.5 分钟**，累计 **约 790 年**连续素材；覆盖教育、科技、How-to、娱乐、体育、游戏、旅行、动画等。
- 处理：**PySceneDetect** 切场景，短场景取中间帧、长场景每 t 秒采一帧并记时间戳（平均 **0.27 关键帧/秒**）；音轨用 **Whisper-large-v2（Faster-Whisper 加速）** 做 ASR，再用 **spaCy** 按停顿+句法切分对齐，最终按时间戳交织成"关键帧+ASR"的天然交错序列。
- 过滤（两阶段）：**基础过滤**（时长/分辨率、talking-head 剔除[人脸检测+Qwen-VL]、语种与静音平衡）；**高级过滤**（DeQA 帧质量、DINO+FG-CLIP 跨帧相似度去冗余、LLM 给 ASR 文本打分）。
- 标注：S1 不额外标注；S2 引入 **LLM 语义分段+摘要、Qwen2.5-VL-7B 视觉字幕、LLM 多模态统一摘要**作为更精确监督。

**(2) 视觉-文本配对数据**：约 **5 亿图文对 + 3000 万视频文本对**，视觉主要来自 Emu3 语料，文本用 **Qwen2.5-VL-7B 重新打标**；并加 FLUX 等开源 T2I 合成图文对，以及 **InfinityMM、LLaVA-OV** 等理解数据。视频对加 motion-score 过滤、按 1 FPS 采样，同源 clip 按时序打包。

**(3) Any-to-Image（X2I）数据**：约 **2735 万样本**。开源部分含 SEED-Data-Edit、PromptFix、OmniGen-X2I、ShareGPT-4o-Image、ImgEdit、OmniGen2-X2I2、MultiRef、GPT-IMAGE-EDIT-1.5M 等；并自建 fully-real / semi-synthetic / fully-synthetic 三类大规模 in-house 数据补足多样性与质量。

**(4) 纯文本数据**：约 **3T token**，在 Emu3 文本基础上加高质量中英开源语料，保语言能力。

**SFT 数据（按任务，Table 3，单位 B token）**：General 29.7、X2I 56.2、视觉叙事 10.1、视觉引导 22.5、世界探索 17.5、具身操作 14.1（论文总述 SFT 规模约 150B 样本量级）。各任务专门构建并加 **双层 CoT（global CoT + image-level CoT）**：视觉叙事 430K 样本、视觉引导 960K、世界探索 200K（基于 Sekai/OpenDV，重标相机轨迹）、具身操作 973K（OXE 920K + AgiBot-World Alpha 40K + 松灵 Aloha 自采 13K）。

## 训练方法
**整体 pipeline**：两阶段预训练（≈13T token）→ 两阶段 SFT（150B）→ 多任务 RL（GRPO）→ DiDA 适配。基础设施统一基于 **FlagScale**。

**预训练（NTP，交叉熵）**
- **Stage 1（S1）**：10T+ token（seen 10.3T），max seq 32768，所有图限制 ≤1024 视觉 token（≈512×512），数据**在线 packing**。LR **5e-4**，cosine，700 warmup / 700k steps，batch 448，TP=8 / CP=2，视觉:文本 loss = 0.5:1.0。以**视频交错数据为中心**（采样比 0.55），图文对/纯文本为辅。
- **Stage 2（S2）**：约 3T token（seen 3.5T）继续训。提升分辨率（动态 token 1024~4096，512²~1024²）、提质、平衡分布、加交错标注。LR 降到 **1e-5**，240k steps，离线 pre-pack。采样比：纯文本 0.18 / 图文对 0.16 / 视频对 0.08 / X2I 0.03 / 视频交错 0.55。
- AdamW（β1=0.9, β2=0.95, ϵ=1e-8），grad clip 5.0，weight decay 0.1。S1 训练 loss 平滑下降，9 个验证集（含 ISG-Bench/OpenING/MMIE 三个 OOD）随算力增加持续下降 → **OOD 泛化随预训练算力 scale**。

**SFT（两阶段，统一接口）**
- Stage 1：各任务标准分辨率（X2I 768px、视觉引导/叙事/具身 512px、世界探索 720px），视觉 loss 权重 1.0，max seq 16384，TP=8/CP=1。
- Stage 2：升分辨率（X2I 1024px、其余交错任务 720px），视觉 loss 权重回 0.5，max seq 32768，TP=8/CP=2。batch 1024，LR **6e-6**，cosine，每阶段 3000 iters。统一 SFT 让任务间**互相迁移增益**（T2I 高保真与 X2I 编辑能力自然迁移到叙事/引导任务）。

**强化学习（首次大规模多任务联合多模态 RL）**
- 算法 **GRPO**，global batch 640，LR **1e-6**，rollout=8；rollout 用 **vLLM 采样引擎集成进 VeRL 框架**。
- **统一奖励系统**三特性：(i) 通用奖励（CLIP 图文相似度、VLM 对齐、美学打分）；(ii) 任务专属奖励（文字渲染用 OCR+布局保真、X2I 人脸用人脸检测+识别保 ID、叙事/推理用 VLM 一致性）；(iii) 统一空间——各奖励归一化到 **[1,10]** 再聚合，端到端单一奖励空间，避免单点 reward hacking。
- 数据：每任务过滤 ≈10K 高质量 prompt + 1K 人类反馈；另收 58K X2I 指令 + 50K T2I 样本做单图专项 RL。RL 平均奖励从 **≈4.5 升到 >7.1**，多任务联合稳定收敛。

**DiDA（离散扩散适配——核心推理加速创新）**
- 把预训练好的 AR 模型上的**视觉 token** 生成从"逐 token 顺序解码"改造为"**双向并行的离散扩散去噪**"，**完全不改文本生成能力**。整张图 token 一次性初始化，经若干离散去噪步并行精修。
- 关键 attention mask 设计（Fig 9）：噪声图像 token 对前面 clean token **因果注意**、对同一图内噪声 token **双向注意**；clean 图像/文本 token 保持原因果模式。
- 训练用自蒸馏数据（图文对+交错序列），适配数据约 **13B token**（含 self-distillation）即可快速改造。

## Infra（训练 / 推理工程）
- **框架**：训练与推理统一基于 **FlagScale**，支持多种并行与异构硬件部署。预训练/SFT 用 **TP=8、CP=2**（部分阶段 CP=1）。论文未披露总 GPU 数 / GPU·小时。
- **DiDA 专用 infra 创新**：
  - 训练侧——集成 **PyTorch FlexAttention**，用 **per-row block mask**（而非完整 4D mask）灵活编码因果/双向/区域注意，省去存全注意力矩阵、降显存；并用 **TP+PP+SP+ZeRO-1 DP** 混合并行 + 激活重计算。
  - 推理侧——构建 **基于有限状态机（FSM）的 hybrid 调度器**（HybridAsyncEngine / HybridScheduler / DiffusionManager），自适应管理文本/图像阶段切换并预分配资源；配合异步请求、运行时状态复用、**FP8 量化**，4 卡上**至少 +50% 吞吐**。
- **推理速度（Table 16，T2I 1024² 4096 token）**：Emu3.5-AR 在 FlagScale 下 **120s**；**DiDA 仅 10s**（约 12×；相对 naive 实现 512s→22s 约 23×，"约 20×"为整体口径），**与连续 diffusion 快采样相当**。社区侧 vLLM 离线推理另带 4–5× 端到端加速（README）。
- **部署形态**：开源 3 个权重（Emu3.5 通用交错、Emu3.5-Image 专精 T2I/X2I、Emu3.5-VisionTokenizer），提供 Transformers/vLLM 推理与 Gradio Demo；官方上线 emu.world Web 与移动端 App。注：截至论文，**DiDA 加速权重与高级图像解码器尚未放出**（README schedule 标 TODO），开源权重为纯 NTP 版（单图需数分钟）。

## 评测 benchmark（把效果讲清楚）
**T2I 通用 + 文字渲染**
- **TIIF-Bench testmini（Table 4）**：Emu3.5 avg **89.48/88.18（short/long）**，整体最佳，Real-World 文字渲染 **100.00/95.93**，超 GPT-Image-1、Qwen-Image、MidJourney v7 等。
- **OneIG-EN（Table 5）**：Overall **0.564**（榜首，超 Gemini-2.5-Flash-Image 0.550、Qwen-Image 0.539、GPT-Image-1 0.533）；其中 Alignment **0.902**、Text **0.994**（最高）。**OneIG-ZH（Table 6）**：Overall **0.529**（第二，仅次 Qwen-Image 0.548），Text 0.941。
- **GenEval / DPG-Bench（Table 16）**：Emu3.5 **GenEval 0.86 / DPG 88.26**（vs Emu3 0.66 / 80.60，大幅提升）；DiDA 版 0.86 / 87.46 基本无损。
- 文字渲染：LeX-Bench、LongText-Bench（英文最高、中文第二）、CVTG-2K 均**大幅领先 SOTA**（Word Accuracy / NED）。

**Any-to-Image（编辑/主体驱动）**
- **ImgEdit（Table 10）**：Overall **4.41**，**超 Gemini 2.5 Flash Image 与 Qwen-Image-Edit-2509**（GPT-4.1 评）。
- **GEdit-Bench-EN（Table 11）**：G_SC **8.11** / G_PQ **7.70** / **G_O 7.59**——全榜最高，超 Qwen-Image-Edit-2509（7.54）、GPT-Image-1[High]（7.53）、Gemini 2.5 Flash Image（7.10）。
- **OmniContext（Table 12）**：Average **8.82**（榜首，超 GPT-4o 8.80、Gemini 2.5 Flash Image 7.84），SINGLE/MULTIPLE/SCENE 多数子项领先。
- **ICE-Bench（Table 13）**：Task 1-31 Overall **0.637**，超 Qwen-Image-Edit-2509（0.616）、Gemini 2.5 Flash Image（0.631）。

**交错生成（核心叙事——对 Nano Banana 自动偏好胜率，Table 14）**

| 任务 | Win% | Tie% | Lose% |
|---|---|---|---|
| 视觉叙事 Visual Narrative | 49.2 | 10.3 | 40.5 |
| 视觉引导 Visual Guidance | 51.5 | 9.5 | 39.0 |
| 世界探索 World Exploration | 65.5 | 0.0 | 34.5 |
| 具身操作 Embodied Manipulation | 67.1 | 2.4 | 30.5 |

即叙事/引导与 Nano Banana **基本持平略胜**，世界探索/具身操作**显著领先**（ChatGPT 作评判，世界探索 8 维、具身操作 6 维评估；具身 benchmark 331 样本含 10 真实拍摄/109 采样/192 合成）。

**Tokenizer 重建（Tokbench，Table 15）**
- Emu3.5-Diffusion Decoder：**T-ACCm 51.11、T-NEDm 70.52、F-Simm 0.22、rFID 0.49**；文字/人脸重建明显优于 VQGAN/Chameleon/LlamaGen/TokenFlow/Open-MAGVIT2 等同 16× 下采样基线。相比 Emu3.5-Vanilla Decoder（T-ACCm 41.52、T-NEDm 65.39），Diffusion 解码器（2× 分辨率）在**文字/人脸精度（T-ACC/T-NED）上大幅提升**；但 rFID（0.42→0.49）、LPIPS（0.08→0.10）反而略升，即整体 FID/感知失真有微小代价，提升主要集中在细粒度文字与人脸。

**关键消融/结论**：DiDA 在 T2I（GenEval/DPG）与编辑（GEdit）上几乎无损地拿到 ~20× 加速；统一 RL 让跨任务互相增益；预训练算力越大，OOD 验证 loss 越低（泛化随 scale 提升）。

## 创新点与影响
**核心贡献**
1. **以"长视频交错文本"为中心的原生多模态预训练范式**：把互联网视频当成"可无限扩展的多模态语料"，用统一 NTP 在 10T+ token 上学到时序一致性与因果——把 next-token 路线 scale 到世界建模的关键一步。
2. **DiDA**：首次把训练好的多模态 AR 模型轻量改造成"文本顺序解码 + 图像双向并行解码"的混合生成器，**单图 ~20× 加速且质量无损**，让 AR 模型**首次在速度与质量上同时逼近闭源 diffusion**。
3. **首次大规模多任务联合多模态 RL（GRPO + 统一 [1,10] 奖励空间）**，避免单点 reward hacking，跨任务协同提升。
4. **把"世界建模"（世界探索 + 具身操作）作为一等可评测能力**，并全套开源（含 tokenizer 与 3 个权重）。

**影响**：为开源社区提供了一个"纯离散 token、统一 NTP、可做世界模型与具身规划"的 32B/34B 基座，证明 AR 统一路线在生成质量与推理速度上可与 diffusion/闭源模型正面竞争；DiDA 这类"AR→并行去噪"的后处理改造对所有自回归图像/多模态模型有借鉴价值。

**已知局限（作者自述）**
- Tokenizer 仍需 1024 token 编码 512×512 图，压缩比有待提升。
- 视觉叙事/视觉引导等新能力**缺乏系统化定量基准**（目前靠 LLM 偏好评判，主观性强）。
- 开源权重为纯 NTP 版，**DiDA 加速权重与高级图像解码器发布时间未定**（README 标 TODO）。
- 视频生成依赖外接 diffusion 视频解码器，并非端到端原生像素级视频自回归。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2510.26583
- arxiv_pdf: https://arxiv.org/pdf/2510.26583
- github: https://github.com/baaivision/Emu3.5
- hf: https://huggingface.co/BAAI/Emu3.5
- project/app: https://emu.world （JS SPA + 网络受限，未能直接抓取页面快照）

## 本地落盘文件
- ../../../sources/omni/2025/arxiv-2510.26583.pdf （45 页技术报告全文，PDF 不入 git）
- ../../../sources/omni/2025/emu3-5--github-readme.md
- ../../../sources/omni/2025/emu3-5--hf-card.md
