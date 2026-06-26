---
title: "GLIGEN: Open-Set Grounded Text-to-Image Generation"
org: "UW-Madison / Columbia / Microsoft"
country: US
date: "2023-01"
type: paper
category: edit
tags: [grounded-generation, layout2img, controllable-t2i, diffusion, gated-attention, open-set, bounding-box]
url: "https://arxiv.org/abs/2301.07093"
arxiv: "https://arxiv.org/abs/2301.07093"
pdf_url: "https://arxiv.org/pdf/2301.07093"
github_url: "https://github.com/gligen/GLIGEN"
hf_url: "https://huggingface.co/gligen"
modelscope_url: ""
project_url: "https://gligen.github.io/"
downloaded: [arxiv-2301.07093.pdf, gligen--readme.md, gligen--vs-controlnet.md]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
GLIGEN（Grounded-Language-to-Image GENeration）在**冻结**的预训练文生图扩散模型（LDM / Stable Diffusion）上，仅插入新的可训练 **gated self-attention 层**来注入 bounding box / 关键点 / 参考图 / 边缘·深度·法线·语义图等 grounding 条件，实现**开放集（open-set）**的可控布局生成；只在 COCO/检测数据上训练就能 grounding 训练词表外的新概念，零样本 LVIS GLIP-score（AP）从监督基线 LAMA 的 2.0 大幅提升到 11.1，COCO2017 layout2img FID 21.04 / YOLO-AP 22.4 同时超过此前 SOTA（TwFA FID 22.15）。CVPR 2023。

## 背景与定位
2023 年初，大规模文生图扩散模型（[[latent-diffusion-ldm]]、Stable Diffusion、Imagen、DALL·E 2）已能产出惊艳画质，但**唯一输入是文本 caption**，难以精确指定"物体在哪、长什么样"——用自然语言描述精确位置很笨拙，而 bounding box / 关键点天然适合。此前的 layout2img 方法（Layout2Im、LostGAN、LAMA、TwFA 等）都是 **closed-set**：从零训练、只能生成训练集内有限类别（如 COCO 80 类）。

GLIGEN 的核心立意借鉴了**识别领域的范式**：识别模型都从大规模预训练 foundation model 出发，而生成模型却各自从零独立训练。既然扩散模型已在数十亿图文对上预训练、蕴含海量概念知识，能否**复用这份预训练知识**、只为它新增 grounding 输入模态？这样既保留开放词表泛化能力，又获得空间可控性。

技术脉络上，GLIGEN 的"开放集 grounding token"思路直接受 GLIP（Grounded Language-Image Pre-training）启发——用同一文本编码器编码 caption 与每个 grounded 短语，靠**共享文本空间**实现对未见概念的泛化。与并发工作 ReCo（同样基于 SD 实现 open-set，但**微调原权重**，有遗忘风险，且只演示 box）和 eDiff-I（改 attention map 跟随语义图）相比，GLIGEN 强调**冻结原权重 + 多模态条件**的通用性。它与稍后的 ControlNet 是同期"可控扩散"双子星（见下文对比）。

## 模型架构
**Backbone**：U-Net 扩散模型（[[latent-diffusion-ldm]] / Stable Diffusion v1.4），由 ResNet 块 + Transformer 块构成；每个 Transformer 块原本是 `self-attn(visual) → cross-attn(visual, caption)` 两层。GLIGEN **冻结**全部原始权重。

**核心创新——Gated Self-Attention 层**：在原 self-attention 与 cross-attention **之间**插入一个新的可训练 gated self-attention 层。该层把视觉 token `v` 与 grounding token `h^e` 拼接后做自注意力，再用 token selection 只取回视觉 token，以残差形式加回：

```
v = v + β · tanh(γ) · TS( SelfAttn([v, h^e]) )
```

- `γ` 是可学习标量，**初始化为 0**——训练初期新层等于不存在，保证稳定的渐进式学习（思想类似 Flamingo 的 gated 机制，但 Flamingo 用 gated cross-attention；论文消融表明在此任务上 cross-attention 更差，见评测节）。
- `β` 训练时恒为 1，**仅在推理时用于 scheduled sampling**（见训练方法节）。
- 为什么用 self-attention 而非 cross-attention：拼接 + 自注意力让视觉 token 之间也能共享 grounding 信息，这是 cross-attention 缺失的（消融：cross-attn YOLO-AP 仅 16.6 vs self-attn 21.7）。

**Grounding token 构造**（按条件类型）：
- **Box + 文本**：实体短语经同一冻结文本编码器（SD 用 CLIP）得到文本特征——取 **"EOS" token** 特征（CLIP 训练中用于对齐图文的那个，含整句信息；直接用投影后 CLIP embedding 反而收敛慢）；box 坐标 `[αmin,βmin,αmax,βmax]` 经 **Fourier embedding**（输出维 64，仿 NeRF）；二者 concat 后过 **3 隐层、512 宽的 MLP**，输出维与文本 embedding 一致（SD 中 768）。最多 30 个 box token。
- **Box + 图像（参考图）**：用 CLIP 图像编码器（ViT-L-14）取 "CLS" embedding，再投影进文本特征空间（`Pt^⊤ Pi hi`）并归一化到 28.7（经验得到的文本特征平均模长），替代文本特征。文本+图像并存时共 60 token。
- **关键点**：每个关键点坐标做 Fourier embedding；额外学习 N 个"person token"（N=10，最多 10 人）以区分多人，COCO 共 10×17=170 个关键点 token。
- **空间对齐条件图**（边缘/深度/法线/语义图）：resize 到 256×256，用 **ConvNeXt-tiny** backbone 编码成 8×8=64 个 grounding token；同时把条件 `l` 下采样后与噪声 latent `z_t` 在 U-Net 输入处 CONCAT（此时 U-Net 第一层 conv 需可训练），可加速训练。

**条件注入路径**：caption 仍走原 cross-attention（保留）；grounding 走新增 gated self-attention（注入）。各 grounding token 经一个线性投影对齐到该层视觉特征维度（如 down 分支首层把 768 → 320）。

## 数据
GLIGEN 不需要专门数据集，而是**统一三种现成标注格式**作为 box grounding 训练数据（仿 GLIP）：
1. **Grounding data**：图配整句 caption，从 caption 抽名词实体并标 box——词表最丰富，最利于开放词表泛化（如 Flickr30k、Visual Genome，合称 GoldG）。
2. **Detection data**：名词实体是预定义闭集类别（如 COCO 80 类、Object365），**无 caption** → 用 classifier-free guidance 的 null caption。检测数据量级大（百万级 vs grounding 的千级），可大幅扩充训练量。
3. **Detection + Caption data**：实体来自检测标注，图另配 caption（二者可能不对应）。

**具体数据集**：闭集实验用 COCO2014 / COCO2017。规模化实验用 **Object365 + GoldG（Flickr + VG）**，再加 **CC3M + SBU**（用 GLIP 生成伪 box 标签）。语义图 checkpoint 仅在 ADE20K 上训，法线图 checkpoint 仅在 DIODE 上训。底层扩散模型在 **LAION-400M**（LDM 基线）或 SD 自带数据上预训练。COCO2014G 用 GLIP 对 caption 名词跑伪 box 标注。无额外美学/安全过滤披露（直接复用底模权重，过滤由底模数据负责）。

## 训练方法
**训练目标**：标准扩散去噪损失（ε-prediction），但仅优化新参数 θ'（所有 gated self-attention 层 + box MLP），在 grounding 指令 `y=(c,e)` 条件下做 **continual learning**：

```
min_{θ'} L = E_{z,ε~N(0,I),t} [ ‖ ε − f_{θ,θ'}(z_t, t, y) ‖² ]
```

直觉：去噪时若能利用"每个物体在哪"的外部知识会更容易，模型自然学会用 grounding 信息，同时因原权重冻结而保留预训练概念知识。

**Scheduled Sampling（推理期关键 trick）**：因原权重冻结、新层可关，推理时可用阈值 τ∈[0,1] 把扩散过程分两段——前 τ·T 步设 β=1（用 grounding，定下布局轮廓），后 (1−τ)·T 步设 β=0（退回原始文生图模型，精修画质细节）。论文取 τ=0.2。好处有二：(1) 提升画质（因 SD 在高美学图上微调过）；(2) **跨域泛化**——只用人体关键点训练的模型，靠 scheduled sampling 能扩展到机器人 / 卡通等类人形体。

**关键超参（附录）**：
- COCO 系列：batch 64，**16× V100**，100k 迭代。
- 规模化 LDM：400k 迭代；规模化 SD：batch 32、**500k 迭代**。
- 学习率 5e-5，Adam，前 10k 迭代 warm-up。
- caption 与 grounding token 各以 10% 概率随机 drop，用于 classifier-free guidance。
- box token 数上限 30。
- **Inpainting 训练**：先在 generation 任务训好（U-Net 输入 4 通道），再把 checkpoint 改成 9 通道（新增 5 通道：4 给 z0、1 给 mask，0 初始化）继续训，收敛更快、效果更好（仿 GLIDE）。

无蒸馏 / 一致性加速（2023 初 LCM/ADD 尚未出现）。

## Infra（训练 / 推理工程）
- **算力**：COCO 实验 16× NVIDIA V100；未披露规模化实验 GPU 数与总 GPU·时（仅给迭代数 400k/500k）。
- **训练规模**：batch 32–64，单机多卡（README 注明支持 multi-GPU）。
- **混合精度 / 并行策略 / 吞吐**：未披露。
- **推理**：标准扩散采样；scheduled sampling 仅改 β 调度、不增成本；无量化 / 缓存 / 步数蒸馏。官方放出基于 diffusers 的 fork（自动从 HF Hub 下载加载），并集成进 Grounding DINO（语言 prompt → box → GLIGEN inpaint）与 LLaVA-Interactive。
- **部署形态**：开源 10 个 checkpoint（全部基于 **SD-V-1.4**），含 Box+Text、Box+Text+Image、Keypoint、Inpainting（Box+Text / Box+Text+Image）、HED/Canny/Depth/Semantic/Normal map 各一；提供 Gradio demo 与 HF Space。

## 评测 benchmark（把效果讲清楚）
**闭集 COCO2014 val（生成质量 FID + 布局对应 YOLO-score AP/AP50/AP75）**——表 1：
- GLIGEN(COCO2014CD) **FID 5.82**，YOLO 21.7/39.0/21.7；GLIGEN(COCO2014D) **FID 5.61 / YOLO 24.0/42.2/24.1**（画质与布局对应均最佳，因纯检测标注 box 最准）；GLIGEN(COCO2014G) FID 6.38 / YOLO 11.2/21.2/10.7（GLIP 伪标签训练，YOLO 偏低）。
- 对照：LDM* (COCO 微调基线) FID 5.91；同期 SOTA 文生图 LAFITE FID 8.12、Make-a-Scene 7.55、Imagen 7.27（zero-shot 列）。GLIGEN 在加 box 条件的同时**画质不掉**，且 YOLO-AP 远超只能参考的微调 LDM。

**COCO2017 layout2img val（表 2）**：GLIGEN-LDM **FID 21.04 / YOLO-AP 22.4（AP50/75 = 36.5/24.1）**，FID 超过 TwFA（22.15）、LAMA（31.12）、HCSS（33.68）、OCGAN（41.65）、LostGAN-V2（42.55，YOLO-AP 9.1）。注意：表 2 中 **LAMA、TwFA 未报告 YOLO-AP**（原表标"-"），OCGAN YOLO-AP 13.40、HCSS 仅给 AP50/75（28.20/20.12）；GLIGEN 的 22.4 是全表最高 YOLO-AP，不存在与 LAMA"持平"一说。规模化预训练后（表 7）：zero-shot FID 27.03/AP 19.1，finetune 后 FID 21.58/AP 30.8。

**开放集 zero-shot LVIS（1203 长尾类，用 GLIP-score AP；表 3）**——核心卖点：
- 仅用 COCO2014CD 训练就 zero-shot 迁移 LVIS：**AP 6.4**，已超**全监督**基线 LAMA（AP 2.0）3 倍多（LAMA 从零训练，难学 LVIS 大量样本极少的稀有类）。
- 数据规模化后单调提升：GoldG+O365 → AP 10.6；+SBU+CC3M → **AP 11.1**（APr 9.0 / APc 9.8 / APf 13.4）。基于 SD 的版本 AP 10.8。
- Upper-bound（GLIP 跑真实图，256×256）AP 25.2。LVIS finetune 后（表 5）AP 升至 14.9，APf 19.3，远超 LAMA。

**关键点 grounding（COCO2017 val，表 6）**：GLIGEN(w caption) FID 27.34 / AP 31.5 / AP50 52.9，远超 pix2pixHD（FID 142.4 / AP 15.8）；upper-bound AP 62.4。

**Inpainting（按物体大小 YOLO-AP，表 4）**：随机 mask 一个物体后重绘，GLIGEN 比 vanilla LDM 更紧贴 mask——小物体(1-3%) 29.7 vs LDM 25.9；中(5-10%) 30.9 vs 23.4；大(30-50%) **25.6 vs 14.6**（差距最大）。

**关键消融**：
- gated **self**-attn vs **cross**-attn（Flamingo 式）：FID 相近（5.8），但 YOLO-AP **21.7 vs 16.6**——证明视觉 token 间共享 grounding 信息的必要性。
- **Fourier** embedding vs MLP 编码 box：FID 几乎相同（5.82/5.80），但布局对应 YOLO-AP **21.7 vs 3.2**——Fourier 位置编码对空间对应至关重要。
- null caption vs 拼接名词成伪句（"cat, cat, dog"）：FID 5.61 → 7.40 变差（预训练文本编码器没见过这种非自然 caption）。
- γ 动态：约 60-70k 迭代时模型开始学到空间对应（γ 曲线峰值），之后回调以兼顾画质。

## 创新点与影响
**核心贡献**：
1. **冻结底模 + gated 残差注入**：首个用"冻结预训练扩散模型 + 新增可训练 gated self-attention（γ 零初始化）"来加条件的范式，避免知识遗忘、训练稳定，且**复用底模海量概念知识**实现下游开放集泛化。
2. **开放集 grounded 生成**：靠"同一文本编码器编码 caption 与 grounded 短语 + 共享文本空间"，仅在 COCO 训练即可 grounding 训练词表外概念（blue jay、croissant、Hello Kitty…），zero-shot LVIS 反超全监督 SOTA。
3. **统一多 grounding 模态**：一套框架支持 box、关键点、参考图、风格图、边缘/深度/法线/语义图，灵活度高于同期工作。

**与 ControlNet 的关系**（官方 docs/gligen_vs_controlnet）：二者都"只加新参数、不改原权重"。差异在 U-Net 内注入方式——
- **GLIGEN**：在 self/cross-attn 间插 gated self-attention，对条件与视觉特征做**拼接 + Transformer**；条件需先经外部网络编码成 token（如 box→MLP token），更通用，能处理离散条件（box、参考图）。
- **ControlNet**：复制一份 encoder 块，对条件与视觉特征做**逐元素求和**，更适合空间对齐条件。
官方结论：GLIGEN 概念上是更一般的形式，但"用额外的外部条件编码网络设计工作换取更高的可控性与灵活性"。

**影响**：GLIGEN 成为"开放集 grounded / layout-to-image 生成"的代表作与常用基线，催生大量布局可控生成研究；其 gated 注入思想与 ControlNet/T2I-Adapter 共同奠定"冻结底模 + 适配器加条件"的可控扩散主流范式。已被集成进 diffusers、Grounding DINO 工作流、LLaVA-Interactive。

**已知局限**：(1) 全部 checkpoint 基于 SD-1.4，分辨率/画质受底模限制；(2) 关键点 grounding 泛化性弱——人体关键点学到的部件结构难迁移到猫/灯等非类人物体（部件不跨类共享，不如 box 通用）；(3) U-Net 早期层 attention 可解释性差（猜测因视觉 token 缺位置编码）；(4) COCO2014D（null caption）模型理解真实 caption 能力弱；(5) 语义图/法线图 checkpoint 各只在单一数据集（ADE20K/DIODE）上训，域窄。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2301.07093
- arxiv_pdf: https://arxiv.org/pdf/2301.07093
- github: https://github.com/gligen/GLIGEN
- project_page: https://gligen.github.io/
- gligen_vs_controlnet: https://github.com/gligen/GLIGEN/blob/master/docs/gligen_vs_controlnet.MD
- hf_models: https://huggingface.co/gligen
- demo: https://huggingface.co/spaces/gligen/demo

## 一手源存档（sources/）
- [arxiv-2301.07093.pdf](https://arxiv.org/pdf/2301.07093)  （arXiv 原文 PDF，不入 git）
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/gligen--readme.md)
- [vs-controlnet.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/gligen--vs-controlnet.md)
