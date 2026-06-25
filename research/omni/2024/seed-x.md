---
title: "SEED-X: Multimodal Models with Unified Multi-granularity Comprehension and Generation"
org: "Tencent ARC Lab / Tencent AI Lab (AILab-CVC)"
country: China
date: "2024-04"
type: paper
category: unified
tags: [unified, mllm, external-diffuser, sdxl, image-editing, llama2, vit-bridge, comprehension-generation]
url: "https://arxiv.org/abs/2404.14396"
arxiv: "https://arxiv.org/abs/2404.14396"
pdf_url: "https://arxiv.org/pdf/2404.14396"
github_url: "https://github.com/AILab-CVC/SEED-X"
hf_url: "https://huggingface.co/AILab-CVC/SEED-X-17B"
modelscope_url: ""
project_url: "https://arc.tencent.com/en/ai-demos/multimodal"
downloaded: [arxiv-2404.14396.pdf, arxiv-2405.04007.pdf, seed-x--readme.md, seed-x--hf-modelcard.md, seed-data-edit--hf-datasetcard.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
SEED-X 是腾讯 ARC Lab 2024-04 推出的统一多模态基座模型（17B：Llama2-chat-13B + ViT + 外挂 SDXL），用 **64 个可学习 query 回归 ViT 特征、再经"视觉 de-tokenizer"喂给外挂 SDXL U-Net 解码** 这条路线打通"理解+生成"，是 wiki 里反复引用的 **"外挂扩散 / external diffuser"** 范式典型；GenEval Overall 0.51、其衍生的 370 万条 SEED-Data-Edit 编辑数据后来被 [[ming-omni]] 等开源工作直接拿去训练（其 part2/3）。

## 背景与定位
SEED-X 是 SEED 系列（[[seed-llama]] / SEED / SEED-Tokenizer）的第三代续作。前作 SEED-LLaMA 已能在学术 benchmark 上统一理解与生成，但作者认为其"生成内容的精度与多样性仍达不到真实世界需求"。SEED-X 聚焦补两块短板，使基座能落地开放世界：

1. **任意尺寸/长宽比的图像理解**（multi-granularity comprehension）——以往 MLLM 必须把图 resize 到固定方形分辨率，丢失细粒度信息；
2. **多粒度图像生成**（multi-granularity generation）——同时覆盖"高层指令式生成"（按语义画图）和"低层图像操作 / 高精度编辑"（保留原图细节的 manipulation）。

论文 Table 1 给出与同期统一 MLLM（Emu/Emu2、CM3Leon、LaVIT、NExT-GPT、DreamLLM、SEED-LLaMA、VL-GPT、Gemini、Unified-IO 2、Mini-Gemini 等）的能力对照：SEED-X 是当时唯一同时勾选 **检测(detection) + 动态分辨率输入 + 图像生成 + 高精度编辑** 四项的开源工作。它走的是"连续特征 decoder input"路线（区别于 [[chameleon]] 的离散 token 早融合），与 [[mini-gemini]]"LLM 出文本 prompt 再交给现成 SDXL"的弱耦合相比，SEED-X 让 LLM 直接回归连续视觉特征作为 SDXL 的条件，是更紧的桥接。可视为"LLM + 外挂扩散"范式的奠基性开源样板，被 [[bagel]] [[uniworld-v1]] [[liquid-unified]] 等后续工作当作该范式的对照基线引用（其 SEED-Data-Edit 数据则被 [[ming-omni]] 等直接拿去训练）。

## 模型架构
整体 17B，三段拼接：**ViT 视觉 tokenizer → Llama2-chat-13B（LoRA）→ 视觉 de-tokenizer（外挂 SDXL U-Net）**。ViT 特征作为"桥"，把 (de-)tokenizer 的训练与 MLLM 的训练彻底解耦。

- **视觉 tokenizer**：直接复用 **Qwen-VL-Chat 的 ViT 视觉编码器**（冻结），对其输出做 **1D 平均池化得到 N=64 个视觉 embedding**。
- **LLM backbone**：**Llama2-chat-13B**，训练时冻结原参数、只优化 **LoRA** 模块 + 输入/输出两个 cross-attention 层 + 可外推 2D 位置编码。
- **动态分辨率编码**：把输入图按公式 min(Nh·Nw) s.t. H≤Nh·Ht 且 W≤Nw·Wt 切成子图网格，外加一张 resize 到训练分辨率的"全局图"提供全局上下文；所有子图+全局图过 ViT 后特征拼接喂 LLM。每个子图按其归一化中心 (xc,yc) 注入 **可外推 2D 位置编码** p = xc·l+(1−xc)·r+yc·t+(1−yc)·b（l/r/t/b 为左右上下四个可学习 embedding），使模型能泛化到训练时未见过的任意分辨率/比例。
- **生成路径（关键设计）**：用 **N=64 个 learnable query** 输入 LLM，取其输出 hidden states，经一个 cross-attention 层 **回归（MSE）出 64 个 ViT 特征**；以 `<IMG>`/`</IMG>` 两个特殊 token 标记图像起止，`<IMG>` 被训练来预测"何处该出现一张图"。推理时这些回归出的特征喂给视觉 de-tokenizer 解码成真实图像。
- **检测/指代能力**：新增 224 个 bbox token，用 `<box_start><loc-xc><loc-yc><loc-w><loc-h><box_end>` 表示坐标，靠 next-token 交叉熵训练。
- **视觉 de-tokenizer（外挂 SDXL，两阶段）**：
  - 阶段一：64 个 ViT embedding 经 **4 层 cross-attention** 连接到 **预训练 SD-XL 的 U-Net**（替换原文本特征），只优化 cross-attention 层 + U-Net 内部的 key/value（不全量微调）；学会"由 ViT 特征解码语义一致的真实图"。
  - 阶段二（条件化，支持高精度编辑）：仿 **InstructPix2Pix**，把条件图（源图）经 VAE 编码到 latent，与噪声 latent 拼接作为 U-Net 输入，**U-Net 卷积输入通道从 4 扩到 8、全量微调 U-Net**；如此 de-tokenizer 既能吃高层语义特征、又能借条件图恢复源图的细粒度细节（编辑时保留原图细节的核心）。

## 数据
**预训练 158M 样本**，五类（Table 4）：
- 图文对：LAION-COCO（**re-caption**）、SAM（**re-caption**，更详细描述以同时提升理解与生成）、Unsplash、LAION-Aesthetics、JourneyDB、CapFusion；
- grounded 图文对：GRIT；
- 交错图文：MMC4、OBELICS、OpenFlamingo；
- OCR：LLaVAR + 自建 Slides；
- 纯文本：Wikipedia。

**指令微调**用公开+自建数据，覆盖 VQA（LLaVAR / MIMIC-IT / MathQA / ChartQA / AI2D / ScienceQA / KVQA / DVQA + 自建 text-rich/grounded/referencing QA）、对话（LLaVA-150k / ShareGPT / VLIT / LVIS-Instruct4V / Vision-Flan / ALLaVA-4V）、图像生成（沿用预训练同款图文对）、图像编辑、幻灯片生成（自建）、讲故事（VIST）、虚拟试衣（VITON-HD）。

**SEED-Data-Edit（独立技术报告 arXiv:2405.04007）**——总计 **3.7M 编辑对（精确 3,669,644）+ 21K 多轮序列（精确 21,382）**，三部分混合（数字均出自报告 Table 1 与正文）：
- **Part-1 自动管线 3.5M**：管线 (a) 用 LLaVA-1.5 选"适合移除的物体"→ GroundingDINO+SAM 分割 → LaMa inpaint 移除生成"Remove"样本，再反转得"Add"样本（Unsplash 图源，过滤后 1.5M）；管线 (b) 用 ChatGPT 生成编辑指令+目标 caption → PnP（plug-and-play）图引导生成源/目标图，按 CLIP 相似度过滤（目标图与目标 caption 相似度须高于与原 caption，否则丢弃；OpenImages 图源，过滤后 2.0M）。
- **Part-2 真实场景 52K**：从 PhotoshopBattles / Photoshop Gurus / PhotoshopRequest / Zhopped 四站爬取业余摄影者贴出的"原图+修图请求"，由 PS 专家完成编辑、再由人工重标注指令；指令更天马行空、最贴近真实用户意图。
- **Part-3 人工多轮 95K（21K 序列，最多 5 轮）**：PS 专家在真实图上连续多轮编辑（替换/增/删物体、改动作、改文字图案、改数量），图源 Unsplash+SAM+JourneyDB。

对比表显示 SEED-Data-Edit 在"真实图编辑/真实场景/人工标注/编辑量/最大轮数/多轮数"全维度超越 InstructPix2Pix(313K,单轮,全合成)、MagicBrush(10K,3轮)、HQ-Edit(197K,单轮)。

视觉 de-tokenizer 训练图源：JourneyDB、LAION-Aesthetics、Unsplash、LAION-COCO。

## 训练方法
**双训练目标 + 多阶段 LoRA**：
- **预训练（Stage I）**：在交错图文序列上同时做 **next-word prediction（文本/bbox token，交叉熵）** 与 **image feature regression（64 learnable query 输出 vs 64 ViT 特征，MSE）**。从 Llama2-chat-13B 初始化，**只训 LoRA + 输入/输出 cross-attention + 2D 位置编码**；lr=1e-4 cosine decay。
- **指令微调（Stage II）**：在预训练基座上再叠一个 LoRA，同样只优化 LoRA + 两个 cross-attention + 2D 位置编码。先用对话+生成数据微调出通用模型 **SEED-X-I**；再在专用数据上分别微调出 **SEED-X-Edit / SEED-X-PPT / SEED-X-Story / SEED-X-Try-on**。论文明确指出**没有一个 all-in-one 全能模型**，各能力分开微调（坦诚的局限）。
- **生成路线选择 = flow-free**：SEED-X 本体不学扩散/flow matching，而是让 LLM 回归连续 ViT 特征，扩散过程完全外包给冻结桥接的 SDXL；不涉及一致性/步数蒸馏。
- **de-tokenizer 训练**：阶段一只调 cross-attn + U-Net 的 K/V（消融表明全量微调 U-Net 会让细节失真，如人物脚部）；阶段二全量微调 U-Net 并扩通道吃条件图。

## Infra（训练 / 推理工程）
- **MLLM 预训练**：48× **H800-80G**，**10 天**，158M 样本，lr=1e-4 cosine decay，LoRA（冻结 Llama2 主参数）。
- **视觉 de-tokenizer**：32× **A100-40G**；阶段一 42K steps、阶段二 30K steps，lr 均 1e-4 cosine decay。
- **训练框架**：开源代码支持 **DeepSpeed ZeRO-2/ZeRO-3 多节点训练** 与多路高效 datapipe（webdataset/jsonl）。
- **推理形态**：HF 上提供 de-tokenizer / SEED-X(pretrain) / SEED-X-I / SEED-X-Edit 四套权重；官方先放 HF ZeroGPU gradio demo，后在 arc.tencent.com 上线推理更快的 SEED-X-I demo。具体推理吞吐/量化/缓存等工程数字**未披露**。

## 评测 benchmark（把效果讲清楚）
**多模态理解（SEED-X-I，Table 2）** 与专门理解型 MLLM 相比有竞争力：
- POPE **84.1**，MME-P **1457.0**，MMB **70.1**，SEED(img) **66.5**，VQAv2(test) **71.2**，GQA **49.1**，MMMU **35.6**，MM-Vet **43.0**（Table 2 SEED-X 行原值）。
- 在"理解+生成"统一模型一档里（对 DreamLLM/LaVIT/Emu/NExT-GPT/LWM/Gemini-Nano-1），SEED-X 的 MMB 70.1、SEED 66.5、MM-Vet 43.0、MMMU 35.6 等多项领先同档（该档其余模型这些列多为"-"未报告）；但 VQAv2 71.2、GQA 49.1 并不突出（GQA 49.1 在同档内最高，超过 LaVIT 46.8 / LWM 44.8，却明显低于纯理解模型如 LLaVA-v1.5 62.0）。

**文生图（GenEval，Table 3）**：SEED-X **Overall 0.51**，分项 Single 0.96 / Two 0.65 / Counting 0.31 / Colors 0.80 / Position 0.18 / Color-Attri 0.14。
- 对比：其底座 **SDXL overall 0.55 仍高于 SEED-X 0.51**（Table 3）；SEED-X 在 Two-Object(0.65 vs SDXL 0.74)、Counting(0.31 vs 0.39)、Color-Attri(0.14 vs 0.23) 上低于 SDXL，仅 Position(0.18 vs 0.15) 略胜；但在"理解+生成"统一阵营内领先 **LWM(0.47)**。论文将 0.51 解读为"统一模型具备优秀的指令跟随生成能力"，并未声称超越纯生成 SOTA。
- 注：v2 版仅补了 benchmark 数字与消融，**未更新模型权重**（作者自注）。

**编辑（SEED-X-Edit / SEED-Data-Edit 报告）**：技术报告主打数据集贡献与定性结果，称 SEED-X-Edit"取得 promising results"，但**未报告 MagicBrush/GEdit 等编辑基准的定量分数**（写"未报告"）。

**消融结论**：
- de-tokenizer 视觉 token 数：token 越多重建越准（256 能恢复人物姿态，32 已丢结构），但 **64 是折中**——因为让 MLLM 回归 256 个特征反而更难、生成图失真，故全系统选 **N=64**。
- U-Net 只调 K/V 优于全量微调（避免细节失真）。
- 生成头用单层 cross-attention 回归优于多层 resampler（多层缺少对 LLM hidden states 的直接正则）。
- 用 ViT 特征当桥（而非用 MLLM 回归出的特征再训 de-tokenizer）能避免生成图"单调"，验证"ViT 桥解耦"的有效性。

## 创新点与影响
**核心贡献**：
1. **ViT-特征桥接的解耦式统一架构**——LLM 回归连续 ViT 特征、外挂 SDXL 解码，(de-)tokenizer 与 MLLM 独立训练；这套"LLM + 外挂扩散 / external diffuser"成为后续大量统一 MLLM 的参照范式，wiki 在 [[bagel]] [[uniworld-v1]] [[liquid-unified]] [[unified-omni-families]] 中均把 SEED-X 作为该范式的标杆引用。
2. **多粒度生成**：同一基座既能高层指令式生成、又能通过"条件图注入 de-tokenizer"做高精度、保细节的图像编辑。
3. **动态分辨率 + 可外推 2D 位置编码**，支持任意尺寸/比例图像理解。
4. **SEED-Data-Edit（3.7M 混合编辑数据）**：自动管线 + 真实场景爬取 + PS 专家多轮三源混合，规模与真实性显著超越前作（Table 1 在真实图编辑/真实场景/人工标注三项全部 ✓，编辑量 3.67M、最大 5 轮、多轮序列 21.4K 全面碾压 InstructPix2Pix/MagicBrush/HQ-Edit），是该工作对社区的最实在外溢——本 wiki 内 [[ming-omni]] 即直接采用其 part2/3 作为图像生成/编辑训练数据。
5. 自称"首个开源的、统一多模态理解与生成的 MLLM 训练代码"（支持 ZeRO-2/3 多节点）。

**已知局限**：无 all-in-one 全能模型（各能力分开 LoRA 微调）；GenEval 0.51 仍低于其底座 SDXL，组合/计数/位置类弱；编辑无定量 benchmark 数字；生成依赖外挂冻结 SDXL，画质上限受 SDXL 制约；token 数被回归难度压到 64，重建精度与生成稳定性之间存在张力。

## 原始链接
- paper (SEED-X): https://arxiv.org/abs/2404.14396
- paper (SEED-Data-Edit 技术报告): https://arxiv.org/abs/2405.04007
- github: https://github.com/AILab-CVC/SEED-X
- hf model (SEED-X-17B): https://huggingface.co/AILab-CVC/SEED-X-17B
- hf dataset (SEED-Data-Edit): https://huggingface.co/datasets/AILab-CVC/SEED-Data-Edit
- demo: https://arc.tencent.com/en/ai-demos/multimodal

## 本地落盘文件
- ../../../sources/omni/2024/arxiv-2404.14396.pdf
- ../../../sources/omni/2024/arxiv-2405.04007.pdf
- ../../../sources/omni/2024/seed-x--readme.md
- ../../../sources/omni/2024/seed-x--hf-modelcard.md
- ../../../sources/omni/2024/seed-data-edit--hf-datasetcard.md
