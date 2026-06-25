---
title: "Emu3.5: Native Multimodal Models are World Learners"
org: "北京智源研究院 BAAI"
country: China
date: "2025-10"
type: tech-report
category: omni
tags: [autoregressive, next-token-prediction, unified-multimodal, world-model, interleaved, discrete-diffusion, x2i, embodied]
url: "https://arxiv.org/abs/2510.26583"
arxiv: "https://arxiv.org/abs/2510.26583"
pdf_url: "https://arxiv.org/pdf/2510.26583"
github_url: "https://github.com/baaivision/Emu3.5"
hf_url: "https://huggingface.co/BAAI/Emu3.5"
modelscope_url: ""
project_url: "https://emu.world"
downloaded: [arxiv-2510.26583.pdf, emu3-5--readme.md, emu3-5--hf-card.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Emu3.5 是 BAAI 推出的 34B 原生多模态自回归世界模型，用**单一 next-token prediction 目标**在 **超 10 万亿（端到端约 13T）token 的视觉-语言交错语料**（主要来自互联网视频帧 + ASR 转录）上端到端预训练，实现"统一预测文+图序列的下一个状态"；配合大规模多任务 RL（GRPO）与自创的离散扩散加速 **DiDA（单图推理快约 20×）**，在图像生成/编辑上与闭源 Gemini 2.5 Flash Image（Nano Banana）打平、在长程交错生成（视觉叙事/视觉指引/世界探索/具身操作）上以约 49–67% 胜率超越它，并完整开源。

## 背景与定位
语言模型从纯文本语料获得强推理能力，但文本只能提供"对世界的有限视角"；人类知识更多来自**时空延展的多模态经验**，尤其是图文交错的长视频。前作 [[emu]] 系列（Emu/Emu2/Emu3）证明了用生成式目标（next-token prediction）统一多模态任务、建模交错序列的可行性，但都局限于**短程/小规模**数据，留下三个开放问题：(1) 如何把预训练 scale 到长程多模态数据；(2) 如何实现通用多模态交互；(3) 如何高效预测**上万**视觉 token。

Emu3.5 的核心立场是把"视觉的下一帧/下一状态"和"文本的下一 token"**统一为同一个生成目标**，从而把"世界建模"内化进预训练——它直接从视频的"帧序列 + 时序对齐的 ASR 转录"中学习时序连续性、因果与跨模态对齐，这与短片段视频生成（只抓短时动态）形成对比。相对前作的关键改进：数据从短配对升级到长程交错（790 年量级视频）、规模翻数量级、引入 RL 后训练与 DiDA 推理加速、tokenizer 压缩率 4× 提升。定位上它既是 SOTA 的 any-to-image（X2I）/text-to-image 模型，又是首个在推理速度与生成质量上能与闭源扩散模型抗衡的自回归模型。相关工作内链：[[emu3]] [[chameleon]] [[bagel]] [[janus-pro]] [[qwen-image]] [[gemini-2-5-flash-image-nano-banana]]。

## 模型架构
**Backbone（统一架构）**：纯自回归 decoder-only transformer，沿用 Qwen3 风格设计并从 Qwen3 初始化。
- 64 层，hidden size 5120，intermediate size 25600；64 注意力头 + 8 个 KV 头（GQA）。
- RMSNorm + pre-norm；query/key 加 **QK-Norm** 稳定注意力；SwiGLU 激活；RoPE 位置编码。
- 总参数 **34.1B**（transformer 层 31.2B + embedding 层 2.9B）。
- 词表 **282,926**：文本 151,854（直接复用 QwenTokenizer，强多语种覆盖）+ 视觉 131,072。
- 上下文长度 32,768；dropout 0.1。

**所有视觉信号被完全离散化**为 token，因此训练就是标准跨熵 next-token prediction（视觉 token 的 loss 加权 0.5 防止压制文本动态）。

**Visual Tokenizer**：以 **IBQ** 框架为主，下采样因子 f=16，每个 codebook token 维度 D=256；codebook 扩到 131,072，tokenizer 本体放大到 **455M** 参数（宽度 scaling）。借鉴 **REPA**，把 **SigLIP（siglip-large-patch16-256）** 的特征蒸馏进 tokenizer decoder 中间层，丰富离散 token 的语义。表征效率：表示同一张图只需 Emu3 的 **1/4 token 量**。

**可选解码器（三种）**：
- **Vanilla image decoder**：原生 VQ 解码。
- **Diffusion-based image decoder**：吃同样的量化 token，但输出 **2× 分辨率**，显著改善文字/人脸等局部细节；以 Stable Diffusion 3.5 medium 初始化，flow-matching 训练；再做 **LoRA 蒸馏把 50 步降到 4 步（约 10× 加速）**。最终支持多图输入、输出最高 **2K 分辨率**。
- **Video decoder**：基于 DiT，以生成的关键帧 token 为条件生成连续视频；用 VQ 量化 embedding 提供细粒度细节、可选帧间文本提供高层语义；额外加 4 通道 mask 指示哪些帧 token 已给定，支持任意数量中间帧。以 **Wan2.2 5B** 初始化。

**条件注入与 I/O**：原生接受图文交错输入、生成图文交错输出，**无需 modality adapter 或 task-specific head**。分辨率策略：预训练第二阶段动态 token 数 1024–4096，图像短边最小 512×512、最大 1024×1024 保持原始宽高比。

**推理时的混合生成（DiDA）**：文本仍序列生成，图像转为**双向并行**离散扩散去噪（见训练方法）。

## 数据
预训练总量超 **13 万亿（约 13T）多模态 token**，四大组成：

**(1) 视频交错数据（核心，占比 0.55）**：约 **6300 万个视频**，平均时长 6.5 分钟，累计约 **790 年连续素材**；覆盖教育、科技、How-to、娱乐、体育、游戏、旅行、动画等。处理流水线：
- 帧：PySceneDetect 分场景，短场景取中间帧、长场景每 t 秒采样并记录时间戳（实测每秒平均 0.27 关键帧，优于均匀采样）。
- 音轨：Whisper-large-v2（Faster-Whisper 加速）做 ASR，spaCy 按停顿/句法切分得到语法连贯、时序对齐的转录。
- 帧 + ASR 按时间戳合并成天然交错的"视频-文本序列"。
- **两阶段过滤**：基础过滤（时长/分辨率、talking-head 剔除[人脸检测+Qwen-VL]、多语种与静音平衡）；高级过滤（DeQA 帧质量、DINO+FG-CLIP 去冗余、LLM 评 ASR 文本质量）。
- **标注**（仅第二阶段加）：LLM 语义切分+摘要 ASR、Qwen2.5-VL-7B 视觉 caption、LLM 融合三者生成统一摘要。

**(2) 视觉-文本配对数据**：约 **5 亿图文对 + 3000 万视频-文本对**，视觉主要来自 Emu3 语料但用 Qwen2.5-VL-7B 重标注；补充 SOTA 开源 T2I 模型生成的合成图文对，及 InfinityMM、LLaVA-OV 等开源 VL 数据集增强理解。视频对按运动分过滤、1 FPS 采样、同源 clip 按时序打包成交错序列。

**(3) Any-to-Image（X2I）数据**：约 **2735 万样本**，开源集（SEED-Data-Edit、WeatherStream、PromptFix、OmniGen-X2I、ShareGPT-4o-Image、ImgEdit、OmniGen2-X2I2、MultiRef、GPT-IMAGE-EDIT-1.5M 等）+ 自建数据补足多样性/质量/规模。

**(4) 纯文本数据**：约 **3 万亿 token**，在 Emu3 文本基础上扩中英高质量开源语料，保持语言能力。

**SFT 数据（按任务，单位 B token）**：General 29.7、Any-to-Image 56.2、Visual Narrative 10.1、Visual Guidance 22.5、World Exploration 17.5、Embodied Manipulation 14.1。各任务专门构造：视觉叙事 430k 样本（中英、含 global CoT + image-level CoT）、视觉指引 960k（双层 CoT、2–10 步过滤）、世界探索 200k（基于 Sekai+OpenDV，重标相机轨迹、四种输入×交互组合）、具身操作 973k（OXE 920k + Agi-world Alpha 40k + 自采 Songling Aloha 13k，分解为子任务-关键帧）。

**Tokenizer 训练数据**：图像取 ImageNet/OpenImage/CC3M/CC12M + 自建（含文本丰富集 TextAtlas5M/PosterCraft/LAION、人脸集 Midjourney/COYO-700M/DataComp/JourneyDB）；分辨率<512×512 剔除、质量分<0.4 剔除、LAION 美学过滤、去水印。视频解码器训练用 Koala/Sekai/Agibot + 自建 stock 视频，光流过滤过大/过小运动。

## 训练方法
**总目标**：统一 next-token prediction（跨熵），视觉 token loss 加权 0.5。完整 pipeline：两阶段预训练 → 两阶段 SFT → 多任务 RL → DiDA 适配。

**预训练（两阶段，约 13T token）**：
- **Stage 1（10T token）**：max seq 32768，在线打包到满上下文；图像限 ≤1024 视觉 token（≈512×512 保宽高比）；LR 5e-4 cosine，warmup 700，训练 700k step，batch 448，weight decay 0.1，grad clip 5.0。学习基础多模态对齐。数据配比：文本 0.2 / 图文对 0.2 / 视频-文本 0.05 / X2I 0.0 / 视频交错 0.55。
- **Stage 2（约 3T token）**：提分辨率（动态 1024–4096 视觉 token，512×512→1024×1024）、提数据质量、加交错标注；LR 1e-5，训练 240k step，离线 pre-pack + padding。配比：文本 0.18 / 图文对 0.16 / 视频-文本 0.08 / X2I 0.03 / 视频交错 0.55。
- AdamW（β1=0.9, β2=0.95, ε=1e-8）。**关键观察**：9 个 held-out 验证集（含 ISG-Bench/OpenING/MMIE 等 OOD）loss 随算力持续单调下降——预训练 compute 越大，OOD 多模态任务泛化越强。

**SFT（两阶段，约 150B token）**：建立统一多模态接口、促任务互迁移。
- 第一阶段：各任务标准分辨率（X2I 768px、视觉指引/叙事/具身 512px、世界探索 720px），视觉 token loss 权重 1.0，max seq 16384。
- 第二阶段：高分辨率（X2I 1024px、其余交错任务 720px），视觉 token 权重 0.5，max seq 32768。
- TP=8；阶段一 CP=1、阶段二 CP=2；batch 1024，LR 6e-6，cosine，AdamW(β1=0.9,β2=0.95)，每阶段 3000 iter。

**强化学习（首次大规模多任务联合多模态 RL）**：
- 算法 **GRPO**；global batch 640，LR 1e-6，rollout 数 8；rollout 用 vLLM 采样引擎集成进 **VeRL** 框架。
- **统一奖励系统**三特性：① 通用奖励（CLIP 图文相似度、VLM 对齐准确率、美学打分）；② 任务专属（文字渲染用 OCR+layout 保真、X2I 人物身份用人脸检测/识别、叙事推理用 VLM 一致性）；③ 统一空间（所有奖励归一化到 [1,10] 再合并，避免单一奖励 hacking）。先做一遍全任务混合 RL（同 batch 混任务促跨任务协同），再单独做 X2I/T2I 阶段（额外 58k X2I 指令 + 50k T2I）。RL 平均奖励从约 4.5 稳步升到 >7.1（约 140 step）。

**DiDA（Discrete Diffusion Adaptation，推理加速核心创新）**：
- 把预训练好的自回归模型**扩展为离散扩散**：图像 token 序列一次性初始化为噪声，经若干离散去噪步并行恢复。
- 训练用自蒸馏 + 图文交错数据（仅约 **13B token** 适配，含 SFT 与自蒸馏数据）。
- **改注意力 mask**（见 Fig.9）：每个噪声图像 token 对前面 clean token 因果注意、对同图内噪声 token 双向注意；clean 图像/文本 token 维持原因果模式。
- 结果：**保留文本生成能力不变**，单图推理约 **20× 加速**（详见 benchmark）。

**解码器训练**：image decoder 以 SD3.5 medium 初始化，512px 预训练 200k step（batch 512，LR 5e-5）→ bucket 多分辨率 50k iter → LoRA 蒸馏 6k step 把 50 步降 4 步。video decoder 以 Wan2.2 5B 初始化渐进训练（720/480px 1s clip 80k step → 2–5s 混训 80k step → 1080p 微调）。tokenizer 用 IBQ 加权目标（重建+量化+LPIPS 感知+PatchGAN 对抗+熵+SigLIP 语义蒸馏），Adam(β1=0.5,β2=0.9)，LR 1e-4，500k iter，batch 256。

## Infra（训练 / 推理工程）
- **框架**：训练与推理统一构建在 **FlagScale** 上（BAAI 自研，支持多种并行/异构部署）。
- **预训练并行**：TP=8 + CP（上下文并行）=2。模型从 Qwen3 初始化。
- **DiDA 训练 infra**：在 FlagScale 上集成 **PyTorch FlexAttention**，用 per-row block mask（而非传统 4D mask）灵活编码因果/双向/区域注意力，免存完整注意力矩阵、降显存、利于长序列；混合并行 TP+PP+SP+ZeRO-1 DP + 激活重计算。
- **DiDA 推理 infra**：**基于有限状态机（FSM）的混合推理框架**，自适应调度文本/图像阶段切换并预分配资源、异步请求处理、运行时状态复用、**FP8 量化**；4 卡设置至少 50% 加速。
- **具体算力规模/GPU·时数未披露**（论文未报告总卡数与训练时长）。
- **部署形态**：开源权重（Emu3.5 / Emu3.5-Image / Emu3.5-VisionTokenizer），Transformers 后端 + Gradio demo；2025-11-19 起官方放出 **vLLM 离线推理**（cond/uncond 批调度器，端到端约 4–5× 加速，vLLM 0.11.0）；2025-11-28 上线 Web/移动 App（emu.world / zh.emu.world）。

## 评测 benchmark（把效果讲清楚）
所有数字来自论文（arxiv-2510.26583）。

**Text-to-Image / 指令遵循**：
- **TIIF-Bench testmini** 总分 Avg(short/long) **89.48/88.18**，超 GPT-Image-1（89.15/88.29，long 略低）、Qwen-Image、Seedream 3.0，为最佳/次佳；Text 子项 short=100.0、long=95.93。
- **OneIG-EN** Overall **0.564**（最高，超 Gemini-2.5-Flash-Image 0.550、Qwen-Image 0.539、GPT-Image-1 0.533）；其中 Alignment 0.902、Text 0.994 均为榜首。
- **OneIG-ZH** Overall **0.529**（次于 Qwen-Image 0.548、Seedream 3.0 0.528 附近；Alignment 0.853、Text 0.941）。
- **GenEval 0.86 / DPG-Bench 88.26**（对比 Emu3 的 0.66 / 80.60，且分辨率 1024² vs 720²、视觉 token 近乎减半）。

**文字渲染（强项）**：
- **LeX-Bench**：Hard-recall **0.87**（超 Seedream 3.0 0.77、Gemini 0.74），Easy/Medium/Hard pned 与 recall 综合领先。
- **LongText-Bench**：English **0.976**（最高）、Chinese 0.928（次于 Qwen-Image 0.946）、Average **0.952**（最高）。
- **CVTG-2K**：Word Accuracy average **0.9123**、NED **0.9656**，大幅超 GPT-Image-1（0.8569/0.9478）、Qwen-Image（0.8288/0.9116）。

**Any-to-Image / 编辑（与 Nano Banana 打平或超越）**：
- **ImgEdit** Overall **4.41**，超 Gemini 2.5 Flash Image（4.28）、Qwen-Image-Edit-2509（4.35）、GPT-Image-1[High]（4.20）；子项 Replace 4.84、Style 4.79、Add 4.61。
- **GEdit-Bench-EN** G_O **7.59**（最高，超 Qwen-Image-Edit-2509 7.54、GPT-Image-1 7.53、Gemini 2.5 Flash Image 7.10）；G_SC 8.11、G_PQ 7.70。
- **OmniContext** Average **8.82**（最高，超 GPT-4o 8.80、Gemini 2.5 Flash Image 8.60）；Object 类尤强（Single-Object 9.46、Multiple-Object 9.09）。
- **ICE-Bench** Task1-31 Overall **0.637**（最高，超 Gemini 2.5 Flash Image 0.631）；但 Task2(人脸参考 0.573)、Task3(风格参考 0.522)、Task31(换脸 0.528) 仍是短板。

**长程交错任务（对 Gemini 2.5 Flash Image 自动偏好评测，Win/Tie/Lose%）**：
- Visual Narrative 49.2 / 10.3 / 40.5（基本打平）
- Visual Guidance 51.5 / 9.5 / 39.0（占优）
- World Exploration 65.5 / 0.0 / 34.5（明显占优）
- Embodied Manipulation 67.1 / 2.4 / 30.5（明显占优）

**Tokenizer 重建（Tokbench，f=16）**：Emu3.5-Diffusion Decoder T-ACCm **51.11**、T-NEDm **70.52**、rFID 0.49，文字/人脸表征显著超 VQGAN/Chameleon/LlamaGen/VAR/TokenFlow/Open-MAGVIT2 等离散 tokenizer。

**DiDA 推理加速（关键消融，Table 16）**：
| 模型 | 参数 | 分辨率 | 生成 token | 方法 | Naive(s) | FlagScale(s) | GenEval | DPG | GEdit-EN G_O |
|---|---|---|---|---|---|---|---|---|---|
| Emu3 | 8B | 720² | 8100 | AR | 260 | 68 | 0.66 | 80.60 | – |
| Emu3.5 | 34B | 1024² | 4096 | AR | 512 | 120 | 0.86 | 88.26 | 7.59 |
| Emu3.5 | 34B | 1024² | 4096 | **DiDA** | **22** | **10** | **0.86** | 87.46 | 7.56 |

即 DiDA 把单图从 AR 的 512s（naive）/120s（FlagScale）压到 22s/**10s**，约 **20× 加速且质量几乎无损**（GenEval 持平 0.86，DPG 88.26→87.46，GEdit 7.59→7.56），10s/4096-token 与连续扩散快采样持平——这是首个在速度+质量上与闭源扩散抗衡的自回归模型。

## 创新点与影响
**核心贡献**：
1. **统一原生范式 scale 到长程**：单一 next-token prediction 在 13T 交错 token（790 年视频）上端到端预训练，把"世界建模"内化进自回归框架，单 34B 模型同时胜任 T2I/X2I/视觉叙事/视觉指引/世界探索/具身操作。
2. **首次大规模多任务联合多模态 RL**：统一奖励空间（通用+任务专属+归一化）让 GRPO 在文+图+交错任务上协同优化、避免单奖励 hacking，奖励稳步 4.5→7.1。
3. **DiDA**：把自回归图像解码改造成双向并行离散扩散，仅 13B token 适配即得约 20× 推理加速且不损质量、不动文本能力——破解了多模态 AR 模型"逐 token 解码慢"的痛点。
4. **更强 tokenizer**：IBQ + SigLIP 蒸馏，4× 压缩率提升 + 文字/人脸重建领先 + 可选 2K 扩散解码器。
5. **完整开源**：模型权重（Emu3.5/Emu3.5-Image/VisionTokenizer）、数据流水线、tokenizer、训练与 DiDA 方法全开放。

**影响**：为"统一自回归 + 离散视觉 token"路线提供了能与闭源扩散（Nano Banana）抗衡的有力证据，尤其在长程交错生成与世界建模/具身方向树立开源标杆；DiDA 给"AR 太慢"提供了通用加速答案；"视频交错 + ASR"作为世界知识来源的 scaling 范式可持续扩展。

**已知局限（作者自陈）**：tokenizer 仍需 1024 token 编码 512×512 图（压缩率待提）；推理延迟仍可进一步降；视觉叙事/视觉指引等新能力评测体系尚不完善（多为 ChatGPT 自动偏好评测，缺系统化量化/人评 benchmark）；ICE-Bench 人脸参考/风格参考/换脸等子任务偏弱；总算力/GPU·时未披露。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2510.26583
- arxiv_pdf: https://arxiv.org/pdf/2510.26583
- github: https://github.com/baaivision/Emu3.5
- hf: https://huggingface.co/BAAI/Emu3.5
- hf-collection: https://huggingface.co/collections/BAAI/emu35
- project/app: https://emu.world

## 本地落盘文件
- ../../../sources/omni/2025/arxiv-2510.26583.pdf
- ../../../sources/omni/2025/emu3-5--readme.md
- ../../../sources/omni/2025/emu3-5--hf-card.md
