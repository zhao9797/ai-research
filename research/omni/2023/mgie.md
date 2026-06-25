---
title: "MGIE: Guiding Instruction-based Image Editing via Multimodal Large Language Models"
org: "Apple / UC Santa Barbara"
country: US
date: "2023-09"
type: paper
category: edit
tags: [instruction-editing, mllm, llava, diffusion, instructpix2pix, expressive-instruction, apple]
url: "https://arxiv.org/abs/2309.17102"
arxiv: "https://arxiv.org/abs/2309.17102"
pdf_url: "https://arxiv.org/pdf/2309.17102"
github_url: "https://github.com/apple/ml-mgie"
hf_url: ""
modelscope_url: ""
project_url: "https://mllm-ie.github.io"
downloaded: [arxiv-2309.17102.pdf, mgie--readme.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
MGIE（MLLM-Guided Image Editing）用一个多模态大模型（LLaVA-7B）把人类那条“太短、太含糊”的编辑指令在线改写成**简洁但视觉感知的富表达指令（expressive instruction）**，再经 8 个 `[IMG]` 视觉 token + 编辑头把这份“视觉想象”注入扩散模型（SD v1.5）做端到端编辑。相对基线 [[instructpix2pix]]，它在 Photoshop 改图（EVR/GIER）、全局调色（MA5k）、局部编辑（MagicBrush）四类任务的自动指标与人评上一致提升（如 MagicBrush 上 DINO 从 67.82→82.22、CTS 从 29.34→30.40），且单图推理仅约 9–10 秒、单张 40GB GPU 可跑。ICLR 2024 Spotlight，Apple 的 “MLLM 引导编辑” 代表作。

## 背景与定位
指令式图像编辑（instruction-based editing）相比“描述式 caption 编辑”或“mask 局部编辑”更贴近人类直觉——直接说“给天空加烟花”即可，不用写详尽描述也不画掩码。代表工作 [[instructpix2pix]]（InsPix2Pix）用一个合成三元组数据集 IPr2Pr（指令由 GPT-3 生成、图像对由 Prompt-to-Prompt 合成）训练扩散模型，并用**冻结的 CLIP 文本编码器**注入指令。

作者指出两个症结：
1. **CLIP 文本编码器是为静态描述训练的**，难以捕捉编辑里“从 A 变到 B 的视觉变换”语义；
2. **人类指令常常太短、太歧义**——例如指令只说“make it healthy”，模型无从知道“healthy”对一张披萨意味着加蔬菜配料。

MGIE 的核心主张：用 MLLM 的跨模态理解+视觉感知，把含糊指令“想象”成显式、视觉相关的富表达指令来提供 explicit guidance。它是**第一个用 MLLM 去改进图像编辑（而非从零生成图像）的工作**——与 GILL / Emu 这类“MLLM 生成新图”路线不同，MGIE 强调对**输入图**的视觉感知来驱动编辑。技术上承接 [[latent-diffusion-ldm]]（SD v1.5 作编辑骨干）、[[ddpm]]（扩散目标）、LLaVA（视觉指令微调）、GILL（`[IMG]` token + 编辑头思路）、BLIP-2（视觉特征提取的 Q-Former 思路）。

## 模型架构
MGIE = **MLLM + 编辑头 T + 潜空间扩散模型 F**，三段串联、端到端联合训练。

- **MLLM（指令改写器）**：从 **LLaVA-7B** 初始化（底座 Vicuna-7B/LLaMA-7B 语言模型 + CLIP-L 视觉编码器 `Enc_vis` + 投影适配器 W）。给定输入图 V 与原指令 X，用提示词 `"what will this image be like if [instruction]"` 让 MLLM 产生编辑后的视觉解释。直接产出的解释往往冗长且含无关描述，故训练阶段用一个预训练摘要器（**Flan-T5-XXL**，专门微调过 summarization）把解释压缩成简洁的 expressive instruction E，再让 MLLM 学习直接生成这个摘要版（教师强制 + 交叉熵 `L_ins`）。**推理时 MGIE 直接产出简洁 E（约 22.7 token），不再 rollout 冗长解释（64.5 token），也不依赖外部摘要器。**
- **`[IMG]` 视觉 token 与编辑头 T**：在 E 之后追加 **N=8 个 `[IMG]` token**（其词嵌入可训练，由 MLLM 的 LM head 生成），作为“视觉想象”的载体（思路源自 GILL）。编辑头 **T 是一个 4 层 Transformer**（seq2seq），把 `[IMG]` 的词嵌入 e（视觉模态的通用表示）与最后一层隐状态 h（实例感知的视觉想象）映射成语义潜变量 U={u₁…u_L} 作为编辑引导（类似 GILL / BLIP-2 的视觉特征提取）。
- **扩散模型 F（编辑器）**：从 **Stable Diffusion v1.5** 初始化的潜空间扩散模型（含 VAE + UNet `ε_θ`）。目标是从保留输入潜变量 v=Enc_VAE(V) 出发、遵循引导 {u} 生成目标潜变量 o。视觉想象 U 通过 **cross-attention** 注入 UNet（Q 来自含噪潜变量 z_t，K/V 来自 {u}）；同时仿 InsPix2Pix 把 v 与 z_t 拼接，使 F 同时以输入图 V 和引导 U 为条件。采用 **classifier-free guidance（双尺度）**：图像引导 α_V 与指令引导 α_X，训练时 5% 数据随机把 v、{u} 或两者置空。推理默认 α_V=1.5、α_X=7.5。
- **可训练参数策略（参数高效）**：MLLM 内大部分权重冻结（self-attention 块），**只训练词嵌入和 LM head**；编辑头 T、扩散模型 F 全量更新。这使端到端训练相对轻量。LM 规模消融用过 MGIE-6.7B（视觉调过的 OPT-6.7B）、7B（LLaVA-7B，默认）、13B（LLaVA-13B）。

## 数据
- **预训练数据：IPr2Pr**（InstructPix2Pix 的 CLIP-filtered 数据），**约 1M 三元组**（输入图 / 目标图 / 指令）。指令由 **GPT-3** 抽取生成，输入-目标图像对由 **Prompt-to-Prompt** 合成。MGIE 在此基础上额外离线产出“摘要版 expressive instruction”用于 `L_ins` 监督（README 的 `process_data.ipynb` 即做此处理）。
- **下游评测/微调数据（覆盖三类编辑场景）**：
  - **EVR**（Tan et al. 2019）：来自 PhotoshopRequest 的 5.7K 三元组，Photoshop 风格修改。
  - **GIER**（Shi et al. 2020）：在线论坛爬取的 29.9K 三元组，含更多全局优化样本。
  - **MA5k**（Shi et al. 2022）：24.8K 三元组，专做整图对比度/亮度/饱和度调整（全局调色）。
  - **MagicBrush**（Zhang et al. 2023）：人工标注的 10.5K 三元组，局部物体编辑。
  - 训练/验证/测试切分沿用各数据集原设置；无特别说明时为 zero-shot（仅在 IPr2Pr 上训练），结果对 5 个随机种子取平均。
- **清洗/标注**：复用 InsPix2Pix 已有的 CLIP-filter；新增的“摘要式富表达指令”是用预训练 Flan-T5-XXL 对 MLLM 长解释做摘要得到的伪标签。美学/安全过滤等其他细节**未披露**。

## 训练方法
- **两条损失联合**：
  - 指令损失 `L_ins`：对 expressive instruction E 逐 token 交叉熵（teacher forcing），让 MLLM 学会直接产出简洁富表达指令。
  - 编辑损失 `L_edit`：标准扩散去噪 MSE（预测加到目标潜变量上的噪声 ε）。
  - **总损失 `L_all = L_ins + 0.5 · L_edit`**，端到端联合优化 MLLM、W、T、F。
- **端到端（E2E）是关键**：消融对比 FZ（把 E 喂给冻结 InsPix2Pix）、FT（用 E 微调 InsPix2Pix）、E2E（联合训扩散模型与 LM）。E2E 让扩散模型与 LM 一起学，从隐状态里提取有用引导、丢弃无关叙述，并避免富表达指令本身的错误传播——故全局调色（MA5k）与局部编辑（MagicBrush）上提升最大。
- **`L_ins` 不可或缺**：去掉 `L_ins` 后 MLLM 会产生冗长引导，MA5k SSIM 从 66.25→58.18、MagicBrush DINO 从 82.22→71.50，LGIE 甚至差于基线；且长指令推理耗时从 9.2s 飙到 29.4s。说明“学简洁指令”既是质量也是效率的关键。
- **关键超参**：优化器 AdamW；batch size 128；MLLM 学习率 5e-4、扩散模型 F 学习率 1e-4。CFG 训练随机置空 5%。README 训练脚本另给出：8 卡 torchrun、40 epoch、per-device batch 4、cosine 调度、warmup 0.03、bf16/tf32、gradient checkpointing、model_max_length 512、DeepSpeed。
- **未用 RL/DPO/奖励模型**：MGIE 不依赖人类反馈（论文特意对比 HIVE——后者用人类偏好+reward feedback 增强 InsPix2Pix——指出 MGIE 不用额外人评就能超过它，更数据高效）。也未用蒸馏/一致性加速等技巧。

## Infra（训练 / 推理工程）
- **算力**：全部实验在 **8× NVIDIA A100 GPU**（PyTorch）上完成。具体 GPU·小时未披露。
- **推理效率**（A100，含 MLLM 改写在内）：单图约 **9.2s**（InsPix2Pix 基线 6.8s）；batch=4 为 20.6s，batch=8 为 36.9s。整套流程可在**单张 40GB GPU** 跑完。因 MGIE 只 rollout <32 token 的简洁指令，效率与 InsPix2Pix 同量级。
- **部署形态**：开源 PyTorch 代码 + Gradio demo（`demo.ipynb`），基于 LLaVA 代码库改造（替换 `llava.py`、`train.py`）。Apple 发布的权重差分（weight differential）以 CC-BY-NC 许可，底座需自取 LLaVA-7B / Vicuna-7B。
- 量化、缓存、步数蒸馏等推理加速**未报告**。

## 评测 benchmark（把效果讲清楚）
指标说明：L1（像素差，↓）、DINO/CVS（DINO 与 CLIP 视觉编码器特征相似度，↑）、SSIM（↑）、LPIPS（感知距离，↓）、CTS（目标 caption 与结果图的文本-视觉相似度，↑）。

**Zero-shot（仅在 IPr2Pr 训练，Table 1）**——InsPix2Pix / LGIE(LLaMA-7B 纯语言改写) / MGIE：

| 数据集 | 指标 | InsPix2Pix | LGIE | MGIE |
|---|---|---|---|---|
| EVR | DINO↑ | 67.82 | 69.71 | **71.49** |
| GIER | SSIM↑ | 57.51 | 56.86 | **59.24** |
| GIER | CVS↑ | 86.63 | 86.99 | **88.59** |
| MA5k | SSIM↑ | 58.92 | 64.60 | **66.25** |
| MA5k | LPIPS↓ | 0.359 | 0.327 | **0.298** |
| MagicBrush | DINO↑ | 71.46 | 80.90 | **82.22** |
| MagicBrush | CVS↑ | 85.22 | 88.87 | **91.14** |
| MagicBrush | CTS↑ | 29.34 | 30.10 | **30.40** |

**Fine-tuned（各数据集上微调，Table 2）**：MagicBrush DINO 87.99→**90.65**、CVS 93.83→**95.28**、CTS 30.93→**31.73**；MA5k LPIPS 0.267→**0.235**。各任务 MGIE 均一致优于 InsPix2Pix 与 LGIE。

**关键消融/对照结论**：
- **MGIE > LGIE 全场**：LGIE 用 LLaMA-7B 仅靠语言改写（无视觉感知），其富表达指令对源图的 CLIP-S 甚至低于原指令（“纯语言想象”不贴源图）；MGIE 因感知输入图，指令与输入/目标图都更对齐——这是其优势根因。
- **架构消融（FZ/FT/E2E，Table 3）**：E2E 最优；FZ 把富表达指令喂冻结 InsPix2Pix 反而可能掉点（场景与训练指令分布不符）。
- **指令编码器对照（Table 5）**：直接把 InsPix2Pix 的 CLIP 编码器换成 LLaMA/LLaVA 只能略微提升，仍显著弱于 MGIE——说明“换更强编码器”不够，端到端联合学习才是关键。MGIE 也无需人类反馈即超过 HIVE。
- **LM 规模（Table 6）**：MGIE-6.7B(OPT) SSIM 63.78 < MGIE-7B(LLaVA) 66.25 < MGIE-13B(LLaVA) 65.91（MagicBrush CTS 13B 达 30.75 最高）——同体量下 LLaVA 强于 OPT；更大 LM 进一步提升，且其指令与视觉更对齐。
- **视觉 token 数**：默认 N=8；少于 4 个 `[IMG]` 显著掉点，多于 4 个后收益趋于饱和。
- **提示词消融**：`"What ..."` 提示优于 `"How ..."`（后者易误解指令）；摘要版 Summ（22.7 token）比 Full / Short 更贴图、更高效。
- **人评**：随机抽 100 例（每数据集 25）、每例 3 标注者排名。指令质量上 **>53%** 认为 MGIE 更实用、**57%** 认为更少幻觉；编辑结果在“指令遵循 / 真值相关性 / 整体质量”三项 MGIE 均居首。
- **FID 不敏感**：作者计算了 FID 但发现各方法差异极小（编辑结果多与原图相近，FID 难辨真伪），故认为 FID 不适合评编辑质量。
- **对照描述式基线**：Text2LIVE / Null-Inv 仅 L1 占优，语义指标（CVS）明显逊于 MGIE，且依赖推理期优化（CLIP 对齐 / DDIM 反演），单图 >200s（MGIE 仅 9.2s）。

## 创新点与影响
**核心贡献**：
1. **首个用 MLLM 改进指令式图像编辑**的框架——把“含糊人类指令”在线改写为“视觉感知的简洁富表达指令”，再驱动扩散，证明 *expressive instruction* 是指令编辑提升的关键，而**视觉感知（vs 纯语言 LGIE）是其中决定性因素**。
2. **`[IMG]` 视觉 token + 4 层编辑头 + 端到端联合训练**的桥接设计：让 MLLM 的“视觉想象”以潜变量形式经 cross-attention 注入 SD，端到端学习既提质量又避免指令错误传播。
3. **参数高效**：MLLM 仅训词嵌入+LM head，单 40GB GPU 可跑，推理 ~9s 与基线同量级，质量却全面领先。

**影响**：成为 “MLLM-guided / LLM-rewrite 指令编辑” 这一范式的代表作（Apple 出品，ICLR'24 Spotlight，开源代码与权重差分），与后续 SEED-X、Emu Edit、SmartEdit、InstructDiffusion 等“强语义理解驱动编辑”路线同属一脉，验证了“把理解力强的多模态模型放进编辑回路”的价值。

**已知局限**：
- 编辑骨干仍是 SD v1.5（512 分辨率级），生成上限受限于该底座；
- 全局上色（colorization）等场景 zero-shot 表现不佳，需微调；
- 依赖 IPr2Pr 这类**合成**三元组数据，质量受合成管线约束；
- 未引入偏好对齐/奖励模型，编辑可控性主要靠 CFG 双尺度（α_V/α_X）手调；
- FID 不可靠、缺乏统一的强编辑 benchmark（论文用多套数据集多指标拼合评估）。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2309.17102
- arxiv_pdf: https://arxiv.org/pdf/2309.17102
- github: https://github.com/apple/ml-mgie
- project_page: https://mllm-ie.github.io
- 预训练权重（CC-BY-NC，Apple）: https://docs-assets.developer.apple.com/ml-research/models/mgie/mgie_7b.tar.gz

## 本地落盘文件
- ../../../sources/omni/2023/arxiv-2309.17102.pdf
- ../../../sources/omni/2023/mgie--readme.md
