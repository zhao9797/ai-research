---
title: "AnyMAL: An Efficient and Scalable Any-Modality Augmented Language Model"
org: Meta (FAIR & Reality Labs)
country: US
date: "2023-09"
type: paper
category: omni
tags: [any-modality, multimodal-llm, llama-2, perceiver-resampler, frozen-llm, audio, video, imu, instruction-tuning, understanding]
url: https://arxiv.org/abs/2309.16058
arxiv: https://arxiv.org/abs/2309.16058
pdf_url: https://arxiv.org/pdf/2309.16058
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: ""
downloaded: [arxiv-2309.16058.pdf]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
AnyMAL 是 Meta 把 **图像 / 视频 / 音频 / IMU 运动传感器** 四类非文本模态统一对齐到 **冻结的 LLaMA-2-70B-chat** 文本嵌入空间的「any-modality 理解模型」——核心创新是冻结 LLM + 每模态轻量 adapter + 在 70B 上靠 4/8-bit 量化把预训练塞进单卡 80GB GPU；在零样本 COCO captioning（+8.4% CIDEr）、VQAv2（+7.0% 相对精度）、AudioCaps（+10.9pp CIDEr）刷新当时文献 SOTA。

## 背景与定位
2023 年的多模态 LLM 大多只做「文本 + 一种模态」（多为图像，如 [[blip-2]]、[[llava]]、[[minigpt-4]]、[[flamingo]]），或依赖闭源 LLM（GPT-4）。AnyMAL 要解决三件事：(1) **模态数量** 从「文本+图像」扩到图像/视频/音频/IMU 共四种非文本模态、且支持交错输入（image + IMU 同时作为上下文）；(2) **LLM 规模** 把底座推到 70B（多数前作停在 7B/13B），论证「在视觉-语言预训练里扩 LLM 参数同样有用」这一当时少被讨论的点；(3) **全开源资源**——预训练数据、合成数据生成全部只用开源模型（用 LLaMA-2-70B 自蒸馏造指令数据），明确不碰 ChatGPT/GPT-4，与 LLaVA 用 GPT-4 造数据形成对照。

方法上它是 [[frozen]]（Tsimpoukelli 2021，frozen LM + 视觉前缀）路线的放大与多模态泛化版：沿用「冻结 LLM、只训投影」的思想，但换更强的指令调优底座、更大的模态编码器、能处理变长输入的投影层（[[flamingo]] 的 Perceiver Resampler）。它是**纯理解侧**模型（输入多模态、只输出文本），不做生成，是 omni 谱系里「any-modality 理解代表」。

## 模型架构
**整体范式**：每个模态用一个「已经对齐到文本空间的编码器 g(·)」抽特征 → 经一个**模态专属投影模块**映射为固定数量的 token 嵌入 → 拼进 LLM 的文本 token 序列，LLM 当作冻结的因果语言模型在「文本+模态 token」联合空间上自回归。LLM 的文本嵌入空间因此变成「文本/其他模态」共享的联合 token 空间。

- **LLM 底座（冻结）**：主报 LLaMA-2-70B-chat；并给出 7B/13B 消融变体。预训练全程**冻结 LLM 参数**——这既让收敛比端到端从头训快得多，也在推理时保留 LLM 原生推理能力（推理用全精度原始 LLM 以最大化精度）。
- **模态编码器 zoo（均预先对齐文本空间，冻结）**：
  - 图像：CLIP ViT-L（336×336）、CLIP/OpenCLIP ViT-G（224×224）、以及自监督的 DINOv2（做对照）。
  - 音频：CLAP。
  - IMU 运动传感器：IMU2CLIP（作者自家工作，把头戴 IMU 对齐到 CLIP/文本）。
  - 视频：InternVideo（显式视频编码器变体），以及直接用图像编码器逐帧（每片段取 4 或 8 帧）的图像式变体。
- **投影模块（唯一可训练部件之一）**：
  - 视觉用 **Perceiver Resampler**（来自 Flamingo），可处理变长输入；超参消融最终用 **6 层 resampler**（论文发现「加 resampler 层数」比「加 batch size / 加 token 数」更显著降 loss，且预算增加少）。
  - 音频 / IMU 用**单层 Linear**。
  - 视频用 **4 层 Resampler**。
- **每模态 token 数（固定，per-adapter）**：图像 64、音频 32、视频 32、IMU 32（论文正文称范围 64–256，附录 Table 12 给出具体配置）。消融显示 64→256 视觉 token 改善很小。
- **条件注入方式**：把模态 token 直接当成 prefix/inline token 拼入序列，输入格式为 `[<instruction> <modality_tokens>]`（SFT 阶段），让回答既 grounded 于文本指令也 grounded 于模态输入；支持多模态**交错**（如 `<img> ... <IMU> ...` 同序列）。

对齐目标即标准的条件语言建模：在「文本 caption ↔ 模态」配对上，最大化 `p(X_text | X_modality) = Π_i p_θ(X_text^[i] | Z_modality, X_text^[1:i-1])`，其中 `Z_modality = Projection_θ(h_latents, g(X_modality))`。

## 数据
**对齐预训练数据（图文/各模态配对）：**
- 图像：LAION-2B 的清洗子集——用 CAT 方法（Filtering/Distillation/Hard-negatives，Radenovic 2023）过滤、并对可检测到的人脸做模糊处理。规模量级约 **200M 图像**（论文贡献处给出 200M images / 28M videos / 2.2M audio / 500K IMU 的总盘子）。
- 音频：AudioSet（2.1M）+ AudioCaps（46K）+ CLOTHO（5K），合计约 2.2M。
- IMU：Ego4D 提供的同步 IMU 传感器数据 + 文本叙述，约 528K 对。
- 视频：除图像式逐帧方案外，另有仅用 HowTo100M 视频 + ASR 转写文本训练的显式视频变体（但作者指出 ASR 与片段对齐弱、内容多样性低，效果反而更差）。

**指令微调数据（MM-IT，作者自建）：**
- **人工标注 60K**：用 Creative-Commons 授权公开图片，由 vendor 标注「严格多模态」的指令-回答对——要求问题脱离模态就无法回答（如「用这张图写首诗」「抽取传单上的电话」），覆盖创意写作、开放式推理等远超简单 QA 的任务。论文强调「少而精、且均衡」的自标注数据带来明显增益。
- **合成增强 150K**：仿 LLaVA 思路，但**只用开源 LLaMA-2-70B**——把图像的文本表示（多条 caption + bbox + 物体列表）喂给 LLaMA-2 生成 QA 对，覆盖多领域多问型；明确不使用 ChatGPT/GPT-4。
- MM-IT 同时被切出 1K 测试集兼作「复杂多模态推理」评测基准（含 detailed-description 子集 MM-IT-Cap）。

**安全过滤**：预训练数据经过滤移除有害文本/图像；推理期另有四道闸（见 Infra/安全）。

## 训练方法
**两阶段：**
1. **模态对齐预训练**：冻结 LLM，只训各模态的投影模块（resampler/linear），目标为上面的条件语言建模。各模态独立训练自己的 adapter，全部对齐到同一个 LLaMA-2-70B-chat，从而天然支持交错多模态 in-context prompting。
2. **多模态指令微调（MM-IT）**：在 60K 人工 + 150K 合成上做 SFT。两种做法消融——(a) 只训投影层、不动 LLM；(b) 额外用 **LoRA / QLoRA**（r=64, α=16，加在所有 linear 层）轻调 LLM 行为。微调同时训 resampler + LoRA adapter，3k 步、batch 128、初始 LR 1e-5。

**关键超参（Table 12，预训练）：**
| 变体 | Batch | 初始 LR | 步数 | 模态 token | 投影模块 |
|---|---|---|---|---|---|
| 13B/70B Image | 2048 | 2e-4 | 100k | 64 | Resampler(6) |
| 13B/70B Audio | 128 | 1e-4 | 1k | 32 | Linear(1) |
| 13B/70B Video | 1024 | 1e-4 | 20k | 32 | Resampler(4) |
| 7B IMU | 256 | 1e-4 | 2k | 32 | Linear(1) |

**训练 trick / 消融结论：**
- 因 LLM 冻结，13B 与 70B 的可训练参数一致，故只在 13B 上做超参消融再迁到 70B。
- resampler 层数（2→6）是最划算的 loss 杠杆；batch（2048→16384）与视觉 token（64→256）增益甚微。
- 70B 比 13B 训练 loss 更低，且下游一致更好——作者归因于大 LLM 自带推理/知识加速了「视觉概念习得与对齐」，据此主张「视觉-语言预训练里扩 LLM 同样重要」。
- 注意：AnyMAL **不做 RLHF/DPO/reward-model**；偏好对齐止步于 SFT，附录仅把「用人评反馈做 RLHF」列为 future work。无步数蒸馏/一致性蒸馏（这是理解模型，非扩散生成）。

## Infra（训练 / 推理工程）
- **量化预训练（核心工程贡献）**：把 70B 大模型在 200M+ 实例上预训练，常规需 FSDP 分片到多卡。AnyMAL 改为对**冻结的 LLM 部分**做 **4-bit / 8-bit 量化**（QLoRA 风格），只让模态 tokenizer 可训。显存因此降一个数量级——**70B 可在单张 80GB VRAM GPU 上以 batch=4 预训练**。相较 FSDP，量化方案达到**相同吞吐却只用一半 GPU 资源**；代价是训练/验证 loss 持续偏高，但不影响生成质量（推理改用全精度原始 LLM）。
- **硬件**：所有模型在不定数量的 **NVIDIA A100** 上训练（论文未披露总 GPU·时 / 总卡数 / 总训练时长）。
- **代码栈**：PyTorch + HuggingFace Transformers 扩展。
- **推理期安全四闸**：(1) 输入图像用 RegNetY 分类器拦截违规内容；(2) 输入文本用 RoBERTa 分类器拦截暴力/仇恨等；(3) 输出文本用同款分类器逐句检测（支持流式）；(4) 图文「单独无害、组合有害」用多模态分类器拦截。因 LLM 参数未改，LLaMA-2 自带的 RLHF/负例微调等安全措施被原样继承。
- **部署形态**：研究原型，论文未发布权重/代码（无官方 GitHub / HF model card）。

## 评测 benchmark（把效果讲清楚）
所有数字均零样本。注意：因 MM-IT 含部分公开基准的 in-domain 图（如 COCO/TextCap），论文严格区分「纯预训练模型」与「MM-IT 指令调优模型」（后者标 †/MM-IT 表示非严格 zeroshot）。

**图像 captioning（CIDEr，Table 2）：**
- COCO：AnyMAL-13B(ViT-G) **99.5** / 70B(ViT-G) 95.9，显著高于 BLIP-2 (61.6)、LLaVA、CM3Leon (79.4)、Flamingo-80B (84.3)、IDEFICS-80B (91.8)。13B≈70B，说明 caption（核心视觉理解）更吃数据规模与对齐方法、而非 LLM 大小。70B 在 COCO 略低被归因于 LLaMA-70B 偏啰嗦、对短 caption 不利。
- MM-IT-Cap（detailed description）：AnyMAL 13B 15.5 / 70B 15.7（基线多未报或 ≤14.3，Table 2）。

**图像 VQA 零样本（Table 4，6 个数据集）：** AnyMAL-70B(ViT-G) 表现最强：
- Hateful-Meme AUC 69.1、VQAv2 64.2（MM-IT 后 67.8†）、ScienceQA 70.8、VizWiz 33.8、OKVQA 42.6（MM-IT 46.1）；TextVQA 上 ViT-L(336²) 35.4 > ViT-G(224²) 32.9（高分辨率对读字关键）。
- 编码器对照：ViT-G > ViT-L（多数集），DINOv2（自监督、未对齐文本）明显更差——印证「特征空间需对齐文本」的重要性。

**图像推理人评（MM-IT 1K，Table 3 & Fig.3）：**
- pairwise 对人工 GT 的胜率：AnyMAL（全量指令调优）**41.1% win**，> LLaVA 34.4% > MiniGPT4 27.0%；BLIP-2/InstructBLIP 在开放式查询上很差（4.1% / 16.7%）。
- Likert：AnyMAL-70B(Human+Synth) Response-Acc **58.0**（vs LLaVA 51.7，相对 +12.2%），Obj-Recognition 79.3，Integrity 99.7。指令调优后物体识别细节略降（因 MM-IT 鼓励简洁回答）。

**音频 captioning（AudioCaps，Table 5）：** AnyMAL-70B(CLAP) **CIDEr 77.8 / SPICE 23.0 / SPICEr 50.4**，较此前 SOTA（PANNs+BERT 66.7 / ACT 等）+10.9pp CIDEr、+5.8pp SPICE；70B >> 13B(72.1) > 7B(70.4)，显示推理模块对音频理解也有用。

**视频 QA 零样本（Table 6）：** AnyMAL-Image-70B(ViT-G, 4 帧) STAR **48.2（SOTA）**、How2QA 68.1、NextQA 57.6，竞争力强于 InternVideo / Flamingo-80B / BLIP-2 等（处理整段未裁剪视频）；显式视频编码器(InternVideo, 8帧)变体反而更弱（ASR 对齐弱）。

**IMU 运动描述（Ego4D，新任务）：** 此前无人做过，AnyMAL-7B 在留出集达 **52.5 CIDEr / 23.2 ROUGE-L**；并展示「仅凭 IMU 推断用户在骑车 → 回答骑车安全停车法」这类无文本/视觉线索的推理。

**总贡献口径**：相对文献 +7.0% VQAv2 相对精度、+8.4% COCO CIDEr、+14.5% AudioCaps CIDEr（abstract 与正文表略有口径差异，以一手表格为准）。

## 创新点与影响
**核心贡献：** (1) 一套「冻结大 LLM + 每模态轻量 adapter」的可扩展配方，把图像/视频/音频/IMU 四模态统一对齐到同一个 LLaMA-2-70B-chat，支持交错多模态 in-context；(2) **量化预训练**让 70B 多模态预训练塞进单卡 80GB、半数 GPU 即达 FSDP 同吞吐，工程上把「扩 LLM 做 MLLM」变得可负担；(3) **全开源资源 + 自蒸馏合成数据**（不依赖 GPT-4），并开创 IMU→文本描述这一新任务；(4) MM-IT——首个高质量人工多模态指令数据集兼复杂推理基准。

**影响：** 是「any-modality 理解」谱系的早期代表，验证了「冻结底座 + 模态 adapter」可廉价扩到多模态多 LLM 规模，且首次系统论证「视觉-语言预训练扩 LLM 参数同样有效」；其 IMU/运动传感器接入预示了可穿戴/AR 场景的多模态助手方向（呼应 Reality Labs 背景）。

**已知局限（作者自陈）：** (1) 因果多模态建模对输入模态的 grounding 仍不够稳——生成时偶尔更信「已生成文本」而非输入图，导致带 LLM 先验偏置的幻觉；要根治可能需改架构或解冻 LLM（成本高）。(2) 视觉概念/实体理解受限于配对图文数据量，未上检索增强。(3) 仅覆盖 4 模态，扩到任意模态需对应配对数据、有效性待证。(4) 偏好对齐止于 SFT，未做 RLHF；模型未开源。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2309.16058
- arxiv_pdf: https://arxiv.org/pdf/2309.16058

## 本地落盘文件
- ../../../sources/omni/2023/arxiv-2309.16058.pdf
