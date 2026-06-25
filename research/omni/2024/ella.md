---
title: "ELLA: Equip Diffusion Models with LLM for Enhanced Semantic Alignment"
org: "Tencent"
country: China
date: "2024-03"
type: paper
category: method
tags: [t2i, diffusion, llm-text-encoder, adapter, prompt-following, dpg-bench, resampler, adaln, sd15, sdxl, training-free-unet]
url: "https://arxiv.org/abs/2403.05135"
arxiv: "https://arxiv.org/abs/2403.05135"
pdf_url: "https://arxiv.org/pdf/2403.05135"
github_url: "https://github.com/TencentQQGYLab/ELLA"
hf_url: "https://huggingface.co/QQGYLab/ELLA"
modelscope_url: ""
project_url: "https://ella-diffusion.github.io/"
downloaded: [arxiv-2403.05135.pdf, ella--paper-html.md, ella--arxiv-abs.md, ella--project-page.md, ella--github-readme.md, ella--hf-modelcard.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
ELLA（**E**fficient **L**arge **L**anguage Model **A**dapter，论文标题副名为 "Equip Diffusion Models with LLM for Enhanced Semantic Alignment"）是腾讯 2024.03 提出的**轻量级 LLM 适配器**：在**冻结 U-Net、冻结 LLM、冻结 VAE** 的前提下，只训练一个新模块 **Timestep-Aware Semantic Connector (TSC)**，把 T5/LLaMA-2 等大语言模型的文本特征对接到 CLIP-based 扩散模型（SD1.5/SDXL），显著提升长/复杂（dense）prompt 的语义遵从。最亮眼结果：**ELLA-SDv1.5 仅 0.07B 可训练参数**就在自建 **DPG-Bench 拿到 74.91**（基座 SD1.5 仅 63.18，甚至超过 2.61B 的 SDXL 74.65）；**ELLA-SDXL（0.47B 可训练）达 80.23**，逼近 DALL-E 3 的 83.50，且即插即用兼容 LoRA/ControlNet。

> 注：可训练参数量 ELLA-SDv1.5，论文 Tab.4 表内记 **0.07B**，但正文 5.2 节文字写 "**0.06B**"（原文 self-inconsistent，差 0.01B）；本页统一采用表内的 0.07B。

## 背景与定位
主流 T2I 扩散模型（SD1.x/2.x、SDXL、DALL-E 2）仍用 **CLIP 作文本编码器**，而 CLIP 是在以短文本为主的图文对上训练的，处理"多物体 + 细致属性 + 复杂关系 + 长文本对齐"这类 dense prompt 时力不从心。

已有两条改进路线各有代价：
- **换成 LLM 文本编码器**：Imagen 首次证明纯文本语料预训练的 T5 特征对文图对齐极其有效；[[pixart-alpha]]、DALL-E 3 用 T5；eDiff-I/EMU 同时用 CLIP+T5；ParaDiffusion 甚至**微调 LLaMA-2**。但这些方法**都要全量重训 U-Net**（ParaDiffusion 还要 fine-tune LLM），算力极贵，且难以与开源社区生态（社区微调模型、LoRA、ControlNet）兼容。
- **组合式（compositional）方法**：操纵 cross-attention map / latent，或用 LLM 把 prompt 拆成区域描述再分区生成；但受限于基座可解释性、只能粗粒度控制，且其上限仍被 CLIP 的文本理解能力卡死。

ELLA 走第三条路：**不动基座，只加一个轻量 adapter**。它把"LLM 的语言理解"与"扩散模型的成像能力"用一个可训练连接器桥接，既拿到 LLM 的 dense prompt 理解，又保留了与社区模型/下游工具的即插即用兼容性。与 ELLA 几乎同期、独立完成的相似工作是 **LaVi-Bridge**（arXiv:2403.07860）。相关技术脉络见 [[ddpm]] [[latent-diffusion-ldm]] [[stable-diffusion-xl]] [[pixart-alpha]]。

## 模型架构
整体 pipeline：`文本 → 冻结 LLM 编码 → TSC（可训练，注入 timestep）→ 固定长度 semantic queries → 经 cross-attention 条件化 冻结 U-Net → 冻结 VAE 解码`。**唯一可训练组件就是 TSC。**

**Text Encoder（冻结）。** 兼容任意 SOTA LLM，论文实验了三种：
- **T5-XL encoder**（1.2B，主结果采用，encoder-only 双向注意力）
- **TinyLlama**（1.1B，decoder-only）
- **LLaMA-2 13B**（decoder-only）

取 LLM 的 **last hidden state** 作为综合文本特征；训练 token 长度设为 **128**（以容纳 dense caption 的复杂场景）。

**Timestep-Aware Semantic Connector (TSC)。** 核心创新。接收**任意长度**文本特征 + **timestep embedding**，输出**固定长度**的 semantic queries（学习式 latent queries），再通过 cross-attention 条件化 U-Net。设计动机来自一个观察：扩散模型在去噪**早期（高噪声）预测低频内容**（主体、布局），**后期（低噪声）才精修高频细节**（属性、风格）。因此期望 connector 能**按 timestep 动态提取**不同语义层级——早期给"主体/布局"语义，后期给"细致属性/风格"语义。

论文系统比较了 4 种 connector 设计（消融见下表 6）：
- **MLP**：仿 LLaVA 的投影，把文本特征映射到生成条件空间。缺点：面对变长输入不灵活、难 scale-up。
- **Resampler**：仿 Flamingo 的 Perceiver Resampler，用一组预定义数量的可学习 latent queries 经 transformer block + cross-attention 与冻结文本特征交互，天然处理任意 token 长度。
- **Resampler + timestep via AdaLN**（**最终采用**）：在 resampler 里用 **Adaptive Layer Norm** 注入 timestep，使条件特征随去噪阶段动态变化。
- **Resampler + timestep via AdaLN-Zero**：DiT 里更有效的 zero-init 变体，但**在本框架里反而更差**——AdaLN-Zero 把每个 block 初始化为恒等映射，可能削弱了 LLM 特征对最终条件特征的贡献。

**条件注入**：semantic queries 经 cross-attention 进入冻结 U-Net（与原 CLIP 注入位置一致）。**分辨率策略**：先在 512 分辨率训练做文图对齐，ELLA-SDXL 再在 1024 分辨率上用 10 万张高质量数据 continue-train 提升美学。

**可训练参数量极小**：ELLA-SDv1.5 仅 **0.07B**，ELLA-SDXL 仅 **0.47B**（对比同表 SDXL 整体 2.61B、PixArt-α 0.61B）。

## 数据
- **基础来源**：从 **LAION** 与 **COYO**(COYO-700M) 采集图像，过滤条件为**美学评分 > 6**（improved-aesthetic-predictor）且**短边分辨率 ≥ 512**。
- **重新标注（re-captioning）**：用 SOTA 多模态大模型 **CogVLM** 作自动 captioner，重写出长而密的描述（指明主体、周边、颜色、纹理、空间关系等）。**共标注 30M 图像 caption**。这是 ELLA 数据侧的关键——CogVLM caption 信息密度远高于原 alt-text。
- **多样性补充**：再加入 **4M JourneyDB** 数据（用其原始 caption），提升 prompt 格式多样性与成图质量。
- **总训练规模**：主实验在 **34M 图文对**（512 分辨率）上训练；ELLA-SDXL 额外用 **100K 高质量数据**（1024 分辨率）做美学微调。
- **caption 信息密度量化**（CLIP tokenizer 统计，论文 Tab.1，逐文本平均）：原始 LAION 平均仅 **9.81 词 / 11.88 token**，CogVLM 重写后 **LAION-CogVLM 达 49.87 词 / 62.33 token**；名词 NN 3.59→15.51，形容词/副词 JJ/RB 0.70→8.06，介词 IN 1.87→6.26。COYO 同理（9.83→50.71 词）。即 re-captioning 把 caption 信息量提升约 5 倍。
- **已知局限**：MLLM 合成 caption 对**实体/颜色/纹理敏感且可靠**，但对**形状和空间关系常不可靠**（作者在 Limitation 明确指出，这也解释了为何 ELLA 在 spatial / shape 维度提升相对小）。

## 训练方法
- **训练目标**：标准扩散去噪（沿用基座 SD 的 noise-prediction 目标），**不引入 flow matching / 蒸馏**——ELLA 是在固定基座上训 adapter，不改变扩散公式本身。
- **冻结策略**：LLM、U-Net、VAE 全冻结，**只训 TSC**。这是它"即插即用 + 低算力 + 兼容社区"的根因。
- **优化器与超参**：AdamW，weight decay 0.01；**ELLA-SDv1.5 学习率常数 1e-4**，**ELLA-SDXL 1e-5**；训练 token 长度 128。
- **训练步数**：主实验 **280,000 步**；消融实验受算力限制只训 **140,000 步（约 1 epoch）**。
- **多阶段**：ELLA-SDXL = 512 分辨率文图对齐预训练 → 1024 分辨率 100K 高质量数据美学微调（两阶段）。
- **无 SFT / 无 RLHF / 无偏好对齐 / 无步数蒸馏**：ELLA 不做这些后训练；它的"对齐"提升完全来自 LLM 文本特征 + dense caption 数据 + timestep-aware 条件化。
- **推理侧 trick**（来自官方 README，论文未强调但工程关键）：
  1. **Caption upsampling**：仿 DALL-E 3，用 LLM 的 in-context learning 把短 prompt"升采样"为 3–5 句长描述（指明颜色/形状/纹理/空间关系，禁止氛围性句子），再喂 ELLA，可释放其最大潜力（README 给了 Qwen-72B / GPT-4 改写实例）。
  2. **Flexible token length**：训练用长 caption（max 128 token），测短 prompt 时把 tokenizer `max_length=None`、去掉 padding/truncation，能提升短 caption 成图质量。
  3. **ELLA+CLIP 拼接**：因 ELLA 推理时**完全不用 CLIP**，依赖 trigger word 的社区模型会掉风格；可把 ELLA 输出与 CLIP 输出在序列维拼接（`Bx77x768 + Bx64x768 → Bx141x768`）一并作为 U-Net 条件，以兼容 Textual Inversion / Trigger Word 等 CLIP 生态技术。

## Infra（训练 / 推理工程）
- **算力**：最终模型在 **8 × A100 40G** 上训练，**ELLA-SDv1.5 约 7 天，ELLA-SDXL 约 14 天**。
- **训练成本对比**：ELLA-SDXL 训练时间 **< PixArt-α 的 80%**（PixArt-α 报告 753 A100 GPU-days），凸显"只训 adapter"的算力优势。
- **精度坑（来自 README issue#23）**：绝大多数实验在 **V100**（不支持 bf16）上做，被迫用 **fp16 的 T5**；作者实测 fp16 T5 与 bf16 T5 输出差异不可忽略、会导致成图明显不同，**因此推理也建议用 fp16 T5**。
- **推理加速**：ELLA 本身不改采样步数/不做蒸馏，沿用基座 SD 的采样器；额外开销仅为一次 LLM 编码 + 轻量 TSC 前向，相对全量 LLM-based 重训方案几乎可忽略。
- **部署形态**：开源 **ELLA-SD1.5 checkpoint**（`ella-sd1.5-tsc-t5xl.safetensors`，HF `QQGYLab/ELLA`，apache-2.0）+ 推理脚本 + Gradio demo；**官方 ComfyUI 插件** `TencentQQGYLab/ComfyUI-ELLA`（支持 ControlNet/img2img），社区另有 ExponentialML、kijai 的第三方 ComfyUI 插件。**注意：ELLA-SDXL 权重未开源**（论文有实验但 checkpoint 未释放）。

## 评测 benchmark（把效果讲清楚）

**新基准 DPG-Bench（本工作贡献）**：1,065 条长/密 prompt，专测 dense prompt 遵从；用 GPT-4 从 COCO/PartiPrompts/DSG-1k/Object365 改写生成长描述（人工校验），再仿 DSG 生成 tuple/问题/图；评测时每 prompt 生成 4 图，用 **mPLUG-large** 做 VQA 裁判，按 DSG 规则算 graph score。规模碾压旧基准（论文 Tab.2，CLIP tokenizer 统计平均）：DPG-Bench **distinct-noun 4286、平均 67.12 词 / 83.91 token**，远超 T2I-CompBench（12.65 token）、PartiPrompts（12.20）、DSG-1k（22.56）。

**T2I-CompBench（短组合 prompt，论文 Tab.3，越高越好）**：

| Model | Color | Shape | Texture | Spatial | Non-Spatial |
| --- | --- | --- | --- | --- | --- |
| SD v1.5 | 0.3750 | 0.3724 | 0.4159 | 0.1204 | 0.3088 |
| **ELLA-SDv1.5** | **0.6911** | 0.4938 | 0.6308 | 0.1867 | 0.3062 |
| SDXL | 0.6369 | 0.5408 | 0.5637 | 0.2032 | 0.3110 |
| **ELLA-SDXL** | **0.7260** | **0.5634** | 0.6686 | **0.2214** | 0.3069 |
| PixArt-α | 0.6886 | 0.5582 | 0.7044 | 0.2082 | 0.3179 |

要点：ELLA-SDv1.5 在 Color/Texture 上把 SD1.5 翻了近一倍、部分子项已可比 SDXL；ELLA-SDXL 在多数类别超过 SDXL 与全量训练的 PixArt-α（Texture/Non-Spatial 略逊 PixArt-α）。

**DPG-Bench（密 prompt 遵从，论文 Tab.4，#Params 为可训练参数，越高越好）**：

| Model | #可训练参数 | Average | Global | Entity | Attribute | Relation | Other |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SD v1.5 | 0.86B | 63.18 | 74.63 | 74.23 | 75.39 | 73.49 | 67.81 |
| **ELLA-SDv1.5** | **0.07B** | **74.91** | 84.03 | 84.61 | 83.48 | 84.03 | 80.79 |
| SDXL | 2.61B | 74.65 | 83.27 | 82.43 | 80.91 | 86.76 | 80.41 |
| **ELLA-SDXL** | **0.47B** | **80.23** | 85.90 | 85.34 | 86.67 | 86.16 | 87.41 |
| PixArt-α | 0.61B | 71.11 | 74.97 | 79.32 | 78.60 | 82.57 | 76.96 |
| Playground v2 | 2.61B | 74.54 | 83.61 | 79.91 | 82.67 | 80.62 | 81.22 |
| DALL-E 3 | - | 83.50 | 90.97 | 89.61 | 88.39 | 90.58 | 89.83 |

要点：**ELLA-SDv1.5（0.07B 训练参数）DPG 74.91 已超 2.61B 的 SDXL（74.65）**；ELLA-SDXL 80.23 全面领先开源同期，仅次于闭源 DALL-E 3（83.50）。可训练参数量是全场最小。

**消融 1 — LLM 选择**（基于 SD1.5，统一 6-block resampler，论文 Tab.5）：

| Text Encoder | Color | Shape | Texture | DPG-Bench |
| --- | --- | --- | --- | --- |
| CLIP（原 SD1.5） | 0.3750 | 0.3576 | 0.4156 | 63.18 |
| TinyLlama (1.1B) | 0.4168 | 0.3922 | 0.4639 | 70.27 |
| LLaMA-2 (13B) | 0.4468 | 0.3983 | 0.5137 | 72.05 |
| T5-XL (1.2B) | 0.5570 | 0.4522 | 0.5195 | 71.70 |

结论：任何 LLM 都明显超 CLIP；decoder-only 里 LLaMA-2 13B > TinyLlama；**T5-XL（双向 encoder）在短 prompt 上优势显著**（Color 0.557 远高于 LLaMA-2 的 0.447），但 dense prompt（DPG）略逊 LLaMA-2 13B——作者推测双向注意力捕获更丰富特征利于短 prompt，但 T5-XL 规模偏小限制了复杂文本理解。主结果最终选 **T5-XL**（综合 + 社区友好）。

**消融 2 — connector 架构**（基于 TinyLlama + SD1.5，论文 Tab.6）：

| Module | Norm | Timestep-Aware | 可训练参数 | Color | Shape | Texture | DPG |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MLP | LN | ✗ | 2.16M | 0.3262 | 0.3198 | 0.3957 | 62.55 |
| Resampler (1 block) | LN | ✗ | 8.71M | 0.3569 | 0.3343 | 0.4124 | 66.39 |
| Resampler (6 blocks) | LN | ✗ | 44.16M | 0.4168 | 0.3922 | 0.4639 | 70.27 |
| Resampler (6 blocks) | AdaLN-Zero | ✓ | 73.91M | 0.4774 | 0.3810 | 0.4964 | 70.43 |
| **Resampler (6 blocks)** | **AdaLN（TSC）** | ✓ | 66.82M | **0.5014** | **0.4253** | **0.5175** | **72.91** |

结论：transformer-based resampler > MLP（同规模下迁移 LLM 能力更强且易 scale）；6-block > 1-block；**AdaLN（TSC 最终设计）> AdaLN-Zero**（尽管后者参数更多）。

**User study**：对 SDXL(CLIP) / PixArt-α(T5) / ELLA-SDXL，用 DPG-Bench 成图、每 prompt 4 图、20 名用户按语义对齐与美学排序；ELLA-SDXL 在文图对齐上超过当前 SOTA 开源模型，美学与 SDXL 相当，且人评结论与 DPG-Bench 排名一致（佐证基准可靠性）。

**TSC timestep 行为可视化**：作者可视化文本 token 与可学习 query 的注意力随 timestep 的相对变化——高噪声阶段"颜色（blue/red）、布局（standing next to）"词注意力更强，低噪声阶段"风格词（painting）"注意力更强，主体词（cow/tree）则全程稳定。实证 TSC 确实在做 timestep-aware 的语义提取。

## 创新点与影响
**核心贡献：**
1. **TSC（Timestep-Aware Semantic Connector）**：首次把"扩散去噪低频→高频"的时序先验用 AdaLN 注入 LLM-to-UNet 连接器，让条件随去噪阶段动态变化——这是相对 IP-Adapter/Flamingo-resampler 类静态 adapter 的关键差异。
2. **完全冻结基座的 LLM 对接范式**：证明无需重训 U-Net/LLM，仅用极小 adapter（0.07B）就能把 dense prompt 遵从拉到甚至超过更大基座，且**天然兼容 LoRA/ControlNet/社区微调模型**——这一"即插即用使能"特性是它工程影响力的核心。
3. **DPG-Bench**：填补了"长/密 prompt 遵从"评测空白（1065 条、平均 84 token），并提供 MLLM 自动评测流程，被后续 T2I 工作（如 [[pixart-alpha]] 系列、各类对齐工作）广泛引用为标准基准之一。
4. **数据侧确证 re-captioning 价值**：用 CogVLM 把 30M 图重标注，量化展示了信息密度 5x 提升对 dense prompt 对齐的决定性作用，呼应 DALL-E 3 的"better captions"论点。

**影响：** ELLA 成为 SD1.5/SDXL 生态里提升 prompt-following 的常用即插件（官方 + 社区 ComfyUI 插件落地）；其"冻结基座 + 轻量 timestep-aware adapter 接 LLM"思路启发了后续多模态条件注入工作。作者随即推出 **EMMA**（Efficient Multi-Modal Adapter，arXiv:2406.09162，2024.06），把 ELLA 扩展为可接受交错图文多模态 prompt。

**已知局限：**
- MLLM 合成 caption 对**形状/空间关系不可靠**，导致 ELLA 在 spatial/shape 维度提升有限（与 PixArt-α 等仍有差距）。
- 成图**美学上限被冻结的 U-Net 限制**——ELLA 改善对齐但不改善基座的画质天花板。
- 推理**完全不用 CLIP**，依赖 trigger word 的社区模型会掉风格（需 ELLA+CLIP 拼接缓解）。
- **ELLA-SDXL 权重未开源**（仅开源 SD1.5 版）。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2403.05135
- arxiv_pdf: https://arxiv.org/pdf/2403.05135
- arxiv_html: https://arxiv.org/html/2403.05135v1
- project_page: https://ella-diffusion.github.io/
- github: https://github.com/TencentQQGYLab/ELLA
- hf_model: https://huggingface.co/QQGYLab/ELLA
- comfyui_plugin: https://github.com/TencentQQGYLab/ComfyUI-ELLA
- 后续工作 EMMA: https://arxiv.org/abs/2406.09162

## 本地落盘文件
- ../../../sources/omni/2024/arxiv-2403.05135.pdf
- ../../../sources/omni/2024/ella--paper-html.md
- ../../../sources/omni/2024/ella--arxiv-abs.md
- ../../../sources/omni/2024/ella--project-page.md
- ../../../sources/omni/2024/ella--github-readme.md
- ../../../sources/omni/2024/ella--hf-modelcard.md
