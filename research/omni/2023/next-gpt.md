---
title: "NExT-GPT: Any-to-Any Multimodal LLM"
org: "National University of Singapore (NExT++)"
country: Singapore
date: "2023-09"
type: paper
category: omni
tags: [any-to-any, mm-llm, omni, diffusion-decoder, imagebind, vicuna, instruction-tuning, mosit, projection-layer]
url: "https://arxiv.org/abs/2309.05519"
arxiv: "https://arxiv.org/abs/2309.05519"
pdf_url: "https://arxiv.org/pdf/2309.05519"
github_url: "https://github.com/NExT-GPT/NExT-GPT"
hf_url: "https://huggingface.co/ChocoWu/nextgpt_7b_tiva_v0"
modelscope_url: ""
project_url: "https://next-gpt.github.io/"
downloaded: [arxiv-2309.05519.pdf, next-gpt--readme.md]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
NExT-GPT 是首个端到端、通用的「任意到任意」（any-to-any）多模态大语言模型：用 **冻结的 LLM（Vicuna-7B）+ 冻结的统一编码器（ImageBind）+ 冻结的扩散解码器（Stable Diffusion / AudioLDM / Zeroscope）**，仅训练中间薄薄的输入/输出投影层（**全系统仅约 1% 参数可训**，131M / 12.4B），即可在 **文/图/音/视** 四模态的任意输入组合 ↔ 任意输出组合之间生成。核心创新是用 LLM 自回归产出的「模态信号 token」当作开关与条件去驱动扩散解码器，并提出 **模态切换指令微调（MosIT）**+ 人工标注 5K 高质量对话数据。ICML 2024 Oral。

## 背景与定位
2023 年的多模态 LLM（[[blip-2]]、[[llava]]、[[minigpt-4]]、Video-LLaMA、PandaGPT、SpeechGPT 等）几乎全是「**只进不出**」——只能在输入侧理解多模态、输出侧仍只吐文本。要走向更接近人类的 AGI，需要 **输入和输出都能是任意模态** 的系统。

当时已有两条路线，都不理想：
- **CoDi**（[[codi]]，Composable Diffusion）：用可组合扩散实现了任意模态并行生成，但 **没有 LLM 作为推理核心**，缺乏复杂指令理解与决策，只能做简单的成对/并行内容生成。
- **工具调用流水线**（Visual-ChatGPT、HuggingGPT、AudioGPT）：用 LLM 当调度器调外部工具。但模块间靠 **离散文本** 传递信息，级联噪声/误差累积；整个系统只做推理、**没有端到端训练**，对隐含复杂指令理解很弱。

NExT-GPT 取两者之长：**以 LLM 为推理核心 + 端到端可训**，但又通过「只训投影层」把端到端的训练成本压到极低。它解决的问题是：如何低成本地把一个文本 LLM 扩展成真正能「听说读看画」的全模态智能体。技术脉络上承接 [[gill]]（用 LLM 产 token 触发图像生成）的思路，把它从「文→图」一条线推广到「任意↔任意」四模态，并接上 [[latent-diffusion-ldm]] 系扩散解码器。

## 模型架构
三层（three-tier）松耦合结构（论文 Fig.1 / Table 1）：

**第一层 · 多模态编码（输入端）**
- 统一编码器：采用 **ImageBind（huge，约 1.2B）**——一个把图/视/音等六模态绑到同一嵌入空间的编码器，从而省去为每种模态各配一个异构编码器。文本直接进 LLM、不过编码器。
- **输入投影层（Input Projection）**：每模态一个 **Linear / Transformer-based** 投影，把 ImageBind 表征映射成「类语言」表征喂给 LLM。参数量：image 4M、video 33M、audio（与 image 共享 ImageBind，单独投影）等，量级很小。

**第二层 · LLM 理解与推理（核心）**
- 核心 LLM：**Vicuna-7B**（论文 v1 用 vicuna-7b-delta-v0；README/开源版升级为 vicuna-7b-v1.5）。
- LLM 输出两类东西：① 直接的文本 token；② **「模态信号 token」**——特殊 token，指示解码层「是否生成 / 生成什么模态」。
  - 设计：`<IMGi>`（i=0…4，5 个图像信号 token）、`<AUDi>`（i=0…8，9 个音频信号 token）、`<VIDi>`（i=0…24，25 个视频信号 token）。
  - 若 LLM 不输出某模态的信号 token，即表示该模态解码器「关闭」（推理时灰显/停用，论文 Fig.2）。

**第三层 · 多模态生成（输出端）**
- **输出投影层（Output Projection）**：每模态一个 **Transformer**（image 31M、video 31M、audio 32M），把信号 token 表征映射成扩散模型 **condition encoder** 能懂的条件表征。
- 扩散解码器（全部 off-the-shelf，冻结）：
  - 图像：**Stable Diffusion**（论文 v1 写 SD v1.5，~1.3B；README 升级为 SD v2）
  - 音频：**AudioLDM（l-full，~975M）**
  - 视频：**Zeroscope（zeroscope_v2_576w，~1.8B）**

**参数策略（关键卖点）**：全系统 = 131M 可训 (=4+33+31+31+32) / [131M + 12.275B 冻结 (=ImageBind 1.2 + Vicuna 7 + SD 1.3 + Zeroscope 1.8 + AudioLDM 0.975)] ≈ **1% 可训**。指令微调阶段额外用 **LoRA**（论文 Table 1 标注 LoRA 33M）打开 LLM 的一小撮参数。这种「冻结大模型、只训投影桥」的设计既低成本，又便于以后插入更多模态（换个编码器/解码器 + 训一个新投影即可）。

## 数据
分三类（论文 §5.2 + README §3.2，Table 2）：

**1. T-X 配对数据（用于对齐训练，X-caption 对）**
- 图文：**CC3M**（Conceptual Captions 3M）
- 视频文：**WebVid**
- 音频文：**AudioCaps / AudioCap**
- 还用到 COCO、Visual Genome、LAION、ActivityNet、Clotho、VGGSS 等做不同子任务（论文 Table 2 数据源栏）。

**2. `Text+X → Text` 指令数据（输入侧多模态、输出文本）**
- 直接复用现成：**LLaVA**（视觉指令）、**Alpaca**（纯文本指令）、**VideoChat / Video-ChatGPT**（视频指令）、MiniGPT-4 等。

**3. `Text → Text+X` 指令数据（T2M，输出侧多模态）**——这是 any-to-any 场景独有的，社区当时没有，作者自造：
- 基于现有大量 X-caption 对 + 模板，**借 GPT-4 生成多样的文本指令** 来包裹 caption，得到「文本 → 文本+图/音/视」对。论文 Table 2 列出 T2M 规模约 4.9K/4.9K/4.9K（图/视/音各 4.9K，14.7K 对话）。

**4. MosIT 数据（模态切换指令微调，本文核心贡献）**
- 现有指令数据模态单一、对话短，无法覆盖「多轮中模态动态切换」的真实交互。作者设计了「Human–Machine」模板对话，**用 GPT-4 围绕 100+ 主题/关键词生成更复杂的多轮对话**（每段 3-7 轮 QA，输入/输出侧交替切换模态，要求逻辑连贯、含深度推理）。对话中需要真实多模态内容时，从 **YouTube / Google / Flickr 检索 + Stable-XL(SDXL)/Midjourney 等 AIGC 工具** 配齐最匹配的图/音/视。
- 经人工审查过滤不当样本后，得到 **5K 条高质量多轮对话**（Table 2 标 4K/4K/4K 图/视/音、约 5K 对话、平均 4.8 轮、支持多轮推理）。注：论文正文该句原文为 "obtain a total of 5K dialogues in low quality"，"low" 与 abstract/conclusion 两处 "high-quality" 矛盾，应为笔误（v1 标注 work in progress），此处以 abstract/conclusion 的「高质量」为准。
- 安全/清洗：论文提到「human inspections and filtering of inappropriate instances」，未披露更细的过滤规则与美学/安全模型。

## 训练方法
两阶段轻量对齐 + 一阶段指令微调，共三步（论文 §4-5，README §3.4）：

**Step-1 · 编码侧 LLM-centric 多模态对齐**（论文 §4.1，训练脚本 `pretrain_enc.sh`）
- 只训 **输入投影层**，冻结 ImageBind / LLM / 输出投影。
- 目标：用 X-caption 对，**强制 LLM 对每个模态输入产出其 gold caption**（caption 生成式对齐），从而把各模态表征对齐到 LLM 的文本特征空间。损失即文本生成的交叉熵（梯度回传只更新输入投影）。

**Step-2 · 解码侧 instruction-following 对齐**（论文 §4.2，脚本 `pretrain_dec.sh`）
- 只训 **输出投影层**，冻结其余。
- 关键 trick：不做「LLM↔整个扩散模型」的全量对齐（太贵），而是 **最小化「LLM 经输出投影后的模态信号 token 表征」与「扩散模型 condition text-encoder 编码的 caption 表征」之间的欧氏距离**（Min. Euclidean Distance）。
- 因为扩散模型只吃文本条件，且 backbone 冻结，所以这步训练 **只用纯 caption 文本、不需要任何真实图/音/视输入**，极度轻量。
- 工程优化：用扩散模型自带 text encoder **预计算 caption 文本嵌入并落盘**（`preprocess_embeddings.py`），训练时直接读，省时省显存。

**Step-3 · 模态切换指令微调（MosIT / IT）**（论文 §5，脚本 `finetune.sh`）
- 同时更新：① LLM（**经 LoRA**）、② 输入投影层、③ 输出投影层。
- 输入一条 IT 对话，LLM 重建输入文本并用模态信号 token 表示要生成的多模态内容；损失 = **文本侧对 gold 标注的交叉熵** + **解码侧信号 token 表征与 gold 多模态 caption 表征的欧氏距离对齐**（Fig.4）。
- 数据用上面三类（Text+X→T、T2M、MosIT 5K）。
- README 还提到 `2023.09.27` 加入 **modality-blended batch sampler**（混合模态批采样器）以平衡多模态训练。

**未披露/未报告**：论文 v1 未给出训练 epoch 数、batch size、学习率、optimizer、warmup 等具体超参，也未报告各阶段训练步数；这些细节散落在开源代码的脚本/配置里，论文正文未列。

## Infra（训练 / 推理工程）
- **训练框架**：README 表明用 **DeepSpeed**，提供 `zero2.json` / `zero3.json` / `zero3_offload.json` 三套 ZeRO 配置（ZeRO-2 / ZeRO-3 / ZeRO-3+offload），即支持显存分片与 CPU offload。
- **可训规模极小**：得益于「冻结大模型 + 只训 131M 投影 + LoRA」，整体显存/算力需求远低于全量训练同规模 MM-LLM，是论文反复强调的低成本卖点。
- **环境**：Python 3.8、PyTorch 2.1.2、CUDA 12.1（README §2）。
- **推理工程**：信号 token 充当模态开关——若某模态无信号 token 则其扩散解码器停用，避免无谓的扩散采样开销（Fig.2 灰显）。解码侧用预计算 caption 嵌入省内存。提供 Gradio 在线 demo（`predict.py` / live demo）。
- **未披露**：论文/README 未报告训练所用 GPU 型号与数量、GPU·小时、总训练时长、吞吐、推理延迟、扩散采样步数与量化/蒸馏加速等具体数字（NExT-GPT 直接复用 SD/AudioLDM/Zeroscope 原生采样，未做额外步数蒸馏）。

## 评测 benchmark（把效果讲清楚）
论文 §6 给出三类任务的量化结果（数字均来自论文 Table 3-11）。整体结论：NExT-GPT 在 **Text→X 生成上与 SOTA 持平**、在 **X→Text 描述上明显优于 CoDi**（因文本由 LLM 直接生成）、在 **文本条件编辑（Text+X→X）上略逊但有竞争力**。

**Text → Image（COCO-caption，FID↓）—— Table 3**
| 方法 | FID↓ |
|---|---|
| CogVideo | 27.10 |
| GLIDE | 12.24 |
| CoDi | 11.26 |
| **SD** | **11.21** |
| **NExT-GPT** | **11.28** |
→ 与 SD/CoDi 基本持平（FID 11.28）。

**Text → Audio（AudioCaps）—— Table 4**
| 方法 | FD↓ | IS↑ |
|---|---|---|
| DiffSound | 47.68 | 4.01 |
| AudioLDM-L | 23.31 | 8.13 |
| CoDi | 22.90 | 8.77 |
| **NExT-GPT** | **23.58** | **8.35** |
→ 接近 AudioLDM-L / CoDi。

**Text → Video（MSR-VTT，zero-shot）—— Table 5**
| 方法 | FID↓ | CLIPSIM↑ |
|---|---|---|
| Make-Video | 13.17 | 0.3049 |
| Latent-VDM | 14.25 | 0.2756 |
| CoDi | — | 0.2890 |
| **NExT-GPT** | **13.04** | **0.3085** |
→ **CLIPSIM 0.3085 为表中最高**，FID 13.04 也优于多数基线。

**X → Text 描述（captioning）——明显强于 CoDi**
- 图→文（COCO，Table 6）：B@4 **44.3** / METEOR **32.9** / CIDEr **156.7**，超过 CoDi（40.2/31.0/149.9），接近/超过 OFA。
- 音→文（AudioCaps，Table 7）：SPIDEr **0.521** / CIDEr **0.802**，均超 CoDi（0.480/0.789）。
- 视→文（MSR-VTT，Table 8）：B@4 **58.4** / METEOR **38.5**，超过 CoDi（52.1/32.5）与 mPLUG-2。

**Text+X → X 文本条件编辑（相对较弱）**
- 图像编辑（COCO，Table 9）：NExT-GPT CLIP 29.31 / FID 6.52（背景 CLIP 27.29 / FID 15.20），相比 PFB-Diff、PTP 等专用编辑方法不占优。
- 音频编辑（VCTK，Table 10）：MCD↓ 指标，NExT-GPT **0.302**，对比 CampNet 0.380 / Make-Audio 0.375 / AudioLDM-L 0.349——表中数值上 NExT-GPT 反而最低（按 MCD↓ 为最好）；但论文正文明确把编辑类任务归为「not that superior, yet competitive」，故此处不宜读作 NExT-GPT 领先（与该表数值存在张力，疑为论文表格/叙述不一致，论文标注 "Preprint, work in progress"）。
- 视频编辑（DAVIS，Table 11）：CLIP-T 0.2683 / CLIP-I 0.9645，低于 Pix2Video（0.2891/0.9767）。

**人评 · 复杂 any-to-any QA（Fig.5）**
- 无现成 benchmark，作者请评测员对不同模态转换打 1-10 分。结论：**生成图像 > 视频/音频**；**生成混合多模态组合 略逊于 单模态生成**（因混合任务更复杂）。

**关键消融/分析结论**：X→Text 优于 CoDi 的核心原因是「文本由 LLM 直接生成、天然是 LLM 强项」；Text→X 受限于底层扩散解码器能力上限（论文 Limitation 明确指出生成质量受扩散模型上限制约）。论文未提供更细的逐组件消融表（如去掉信号 token / 去掉解码侧对齐的对照）。

## 创新点与影响
**核心贡献**
1. **首个端到端通用 any-to-any MM-LLM**：四模态（文/图/音/视）任意输入组合 ↔ 任意输出组合，且以 LLM 为推理核心、整体可训（区别于 CoDi 无 LLM、区别于 HuggingGPT 纯流水线不可训）。
2. **极致参数高效**：「冻结编码器/LLM/解码器 + 只训 1% 投影层 + LoRA」的桥接范式，几乎零成本把文本 LLM 升级为全模态智能体，并天然可扩展新模态。
3. **模态信号 token + 双侧轻量对齐**：用 LLM 自回归产出的 `<IMG>/<AUD>/<VID>` 信号 token 当开关与条件；解码侧用「信号 token 表征 ↔ 扩散 condition 文本表征」的欧氏距离对齐（纯文本、无需真实多模态输入）实现极轻量训练。
4. **MosIT 数据与方法**：提出模态切换指令微调，并人工构建 5K 条多轮、模态交替、含深度推理的高质量对话数据，填补社区空白。

**影响**
- 成为 2023 年 **any-to-any 全模态 LLM 的代表作 / 范式参考**（ICML 2024 Oral），后续诸多统一/全模态工作（如各类 omni-modal LLM、原生统一生成模型）在「LLM 接扩散解码器 / 用特殊 token 触发生成」这一思路上与之同源或对其改进。
- 「冻结大模型、只训投影桥」的低成本扩展思路被广泛借鉴。

**已知局限（论文 Limitation）**
1. 仅支持 4 模态；计划扩展到网页、3D、热力图、表格/图表等及检测/分割/grounding 等任务。
2. 仅实现 7B Vicuna 单一 LLM，未做多型号/多尺寸。
3. **生成质量受限于底层扩散解码器上限**，作者提出可引入检索增强（retrieval-based）来补强生成。
4. MosIT 数据量（5K）偏小，需扩充。
5. 由于信号 token 经投影对齐到扩散文本条件空间，生成可控性/保真度受「对齐桥 + 冻结扩散」双重瓶颈制约；文本条件编辑类任务表现明显弱于专用方法。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2309.05519
- arxiv_pdf: https://arxiv.org/pdf/2309.05519
- github: https://github.com/NExT-GPT/NExT-GPT
- project_page: https://next-gpt.github.io/
- hf_checkpoint: https://huggingface.co/ChocoWu/nextgpt_7b_tiva_v0
- venue: ICML 2024 (Oral), pp. 53366–53397

## 本地落盘文件
- ../../../sources/omni/2023/arxiv-2309.05519.pdf
- ../../../sources/omni/2023/next-gpt--readme.md
