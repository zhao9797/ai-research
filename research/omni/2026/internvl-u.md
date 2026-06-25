---
title: "InternVL-U: Democratizing Unified Multimodal Models for Understanding, Reasoning, Generation and Editing"
org: Shanghai AI Laboratory (OpenGVLab)
country: China
date: "2026-03"
type: tech-report
category: unified
tags: [unified, mllm, mmdit, flow-matching, image-editing, text-rendering, cot, internvl]
url: https://arxiv.org/abs/2603.09877
arxiv: https://arxiv.org/abs/2603.09877
pdf_url: https://arxiv.org/pdf/2603.09877
github_url: https://github.com/OpenGVLab/InternVL-U
hf_url: https://huggingface.co/InternVL-U/InternVL-U
modelscope_url:
project_url:
downloaded: [arxiv-2603.09877.pdf, internvl-u--arxiv-abs.html, internvl-u--repo-readme.md, internvl-u--hf-modelcard.md, internvl-u--internvl-main-repo-readme.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
InternVL-U 是上海 AI Lab(OpenGVLab)2026-03 发布的**轻量级 4B 统一多模态模型(UMM)**：把 SOTA 的理解型 MLLM([[InternVL3.5]] 2B)与一颗专门设计的 **MMDiT 视觉生成头(1.7B)** 拼接,通过**解耦视觉表征**(理解走 ViT、生成走 VAE)+**三阶段渐进训练**+**CoT 推理中心化数据合成**,在仅 4B 参数下于多项生成/编辑基准上**超过参数量 3 倍以上的 BAGEL(14B)**,同时保留接近理解型基座的多模态理解能力(GenEval 0.85、DPG-Bench 85.18、MMMU 54.7、加 CoT 后 RISEBench 从 3.6 跃升到 9.4)。

## 背景与定位
统一多模态模型要同时做"理解/推理"和"生成/编辑",存在内在张力:**强语义理解**(需高层语义特征)和**强像素生成**(需可重建低频细节)对视觉表征的诉求相互冲突。论文把现有路线归为两类并指出各自痛点:

- **全原生(fully-native)UMM**(Chameleon、Emu3、[[bagel]] 等):从零或由单模态组件联合训练理解+生成。问题是社区在建模/表征/架构上尚无共识、没有任何方案在性能或效率上占决定性优势;联合训练要平衡冲突的模态数据分布,工程代价巨大;还得放弃社区已有的 SOTA 理解模型,训练成本与风险高。
- **全集成(fully-ensemble)UMM**(MetaQuery、UniWorld 等):把一个独立预训练的图像生成器后接到理解模型上做后对齐。问题是要么把生成头堆到很大(如 [[qwen-image]]、[[hunyuanimage-3]])换顶级画质但训练/部署贵,要么留小头却引入碎片化的多编码器条件管线(如 [[stable-diffusion-3]] 多编码器文本条件、Z-Image 解耦文/图条件),难以干净对齐到单个 MLLM 的隐状态空间。

InternVL-U 属于"集成/混合"路线,但**重新设计了对齐接口与生成头**,使之干净对齐到 MLLM 的隐状态。其核心主张是**三条设计原则**:统一上下文建模 + 模态自适应生成目标、模态特定的模块化(结构效率)、理解与生成解耦的视觉表征。它建立在 [[InternVL3.5]] 这一开源 SOTA MLLM 之上,继承其理解/推理能力,再用自研 MMDiT 头补足生成/编辑。论文还强调一个"诊断":生成模型训练在低语义密度的自然图像(纹理丰富),理解模型训练在高语义密度的文本/结构化数据(GUI/信息图/OCR),这个**数据域差异**是阻碍 AGI 向 UMM 的关键;受 Nano-Banana Pro 强调排版精度与知识忠实的启发,InternVL-U 专门构造高语义密度数据来弥合。

## 模型架构
整体是**编码器式 MLLM 主干 + 专用 MMDiT 生成头**的层次化设计(论文 Figure 3/4,Table 2)。

**三条架构原则**
- **统一上下文建模 + 模态自适应生成目标**:上下文阶段把视觉与语言 token 投到共享隐空间,用统一自回归(AR)+因果掩码做深层语义融合;但预测目标分模态——文本用离散词表上的交叉熵(NTP),图像用**连续空间的 Flow Matching**(diffusion 的广义形式)。即 **hybrid AR + Diffusion** 建模,而非"tokenization-for-all"。
- **模态特定模块化(结构效率)**:不走 MoT 那种完全模态无关的同质架构。主干用**编码器式架构 + 预训练 ViT** 初始化(引入归纳偏置,先把稀疏冗余的视觉 patch 聚合再进统一隐空间);生成则外挂独立 MMDiT 头,让主干专注语义推理、生成头专注像素合成。
- **理解/生成解耦视觉表征**:理解只用 ViT 抽的**高层语义特征**(保语义保真);生成用一颗**专门重建训练的 VAE** 把图像压到适合合成的隐空间。避免"单一编码器既要高层抽象又要低层细节"的优化权衡,也避免把生成目标塞进上下文主干带来的算力与基建复杂度。

**视觉生成头(自研,1.7B)**
- **双投影器**:多模态隐状态(条件)与 VAE 图像 latent(目标)分布差异大,用两个独立线性投影分别映入生成模块的条件空间。观察到上下文 embedding 量级更大、离群更明显,故在 VLM 分支投影前**加一层归一化**把上下文特征方差归一,提升训练稳定性。
- **Dual-Stream MMDiT + 门控注意力**:文本流与视觉流通过 joint self-attention 交互,但 QKVO 投影与 FFN 参数**完全解耦(disentangled)**。在注意力块里引入**逐元素门控** O'=O⊙σ(XW_g),增强非线性、缓解高分辨率长上下文下的 "attention-sink";论文自称这是**首次把门控机制集成进 MMDiT**。
- **Unified MSRoPE + 分辨率插值**:用统一的 **3D 位置编码(时/高/宽)**同时作用于生成目标和上下文中的视觉 token(以往常把上下文视觉 token 当 1D 展平),利于编辑这类需精确空间推理的任务。为缩放分辨率,用 **Resolution Interpolation**:按最大目标分辨率(如 1024px)定义位置范围,低分辨率预训练(512px)时不缩小索引范围而是**增大相邻 token 步长**,使模型从一开始就学到一致的全局空间表征,减小高分辨率微调时的 "tiling artifact"。

**配置(Table 2)**
- 视觉理解编码器(ViT):24 层、Q/KV 头 16/16、head size 64、intermediate 4096、patch 14、**0.3B**。
- 上下文主干(由 InternVL3.5-2B 初始化):28 层、Q/KV 头 16/8、head size 128、intermediate 6144、**2B**。
- 视觉生成头(随机初始化):20 层、Q/KV 头 12/12、head size 128、intermediate 6144、scale factor 2、**1.7B**。
- **总参数 4B**(0.3+2+1.7);实验表里 InternVL-U 多标注为 "2B+1.7B"(理解侧+生成侧),GenExam 正文一处称 "3.7B"。
- 文本 tokenizer 与对话格式沿用 InternVL3.5;**VAE 直接复用 Qwen-Image 的 VAE**。
- 任意分辨率:生成 512–1024px、长宽比 0.5–2.0。

## 数据
数据是这篇报告的最大篇幅与最大卖点——**面向"高语义密度"任务的合成管线 + CoT 推理中心化范式**。

**开源数据池(Table 1)**
- T2I:LAION、BLIP-3o、ShareGPT-4o-Image、OSP、Echo-4o-Image、OpenGPT-4o、FaceCaption、Flux-Reason-6M、HumanCaption、POSTER-TEXT、AutoPoster、CTW。
- 编辑(IT2I):InstructPix2Pix、AnyEdit、PIPE、ImgEdit、SEED-Data-Edit、OmniEdit、UltraEdit、HQEdit、ShareGPT-4o-Image、OpenGPT-4o、X2Edit、X2I2、UniWorld perception、NHR-Edit、GPT-hqedit/omniedit/ultraedit、Nano-consistent-150k、Pico Banana。
- 论文只给数据集清单,**未披露具体样本量/总规模/各任务配比的精确数字**。

**通用预处理与合成(Figure 6)**
- 多维过滤:美学分、分辨率阈值、安全(NSFW)、水印检测;p-hash 去重。
- 双分支扩充:检索式(用图/文查询大规模搜索引擎补长尾)+ 合成式(造已有样本的真实变体)。
- T2I 多粒度再标注:用 **Qwen2.5-VL** 做简洁/密集/人像三类 caption;文本稀缺图用 Qwen-Image 合成补足;做英→中翻译管线保证中英双语。
- 编辑:四类任务(全局/对象级/属性级/组合)。多智能体框架:MLLM 路由器派单 → **Qwen2.5-VL-72B** 生成任务特定指令 → **异构编辑模型集成**按粒度择优生成 → 三元验证(指令遵循/编辑一致性/生成质量)按阈值保留。

**文本中心(text-centric)合成(Figure 7–9)**
- 三类:自然图上语义相关文字渲染、纯色背景文字渲染、图内文字编辑。
- 渲染管线随机采样 mask 图、字色、字体(中:Kaiti/FangSong/Simhei/微软雅黑/AdobeSongStd;英:Arial Unicode/Times 等)、自适应布局(自动换行/字号),再用 Qwen2.5-VL-72B 重标注。
- 文字编辑三步:**PaddleOCR** 检测文字区/置信度/多边形 → Qwen2.5-VL-72B 过滤并产出指令 → **Flux-Text** 做精确上下文感知文字编辑,得到对齐三元组。

**科学中心(science-centric)合成(Figure 10–11)**
- 覆盖物理/化学/生物/计算机;来源含开源科学理解数据集、教材、竞赛(IPHO/高考/考研)。
- 通用科学 T2I:256p 以下剔除、p-hash 去重、**剔除与评测集重复以防数据污染**;**Qwen3-VL-8B** 多维打分过滤、**Qwen3-VL-32B** 标注。
- **SVG 物理编辑**:PaddleOCR 从教材/试卷抽图与上下文 → **Gemini-3-Flash** 生成原图 SVG 代码并决定输入/输出、产出编辑 prompt 与另一张 SVG → 渲染成图对 → Gemini-3-Flash 再过滤。**用 SVG 操控结构化代码而非直接编辑栅格,把每样本成本从 0.16 美元降到 0.03 美元**。
- **计算机科学编辑**:基于 Python 库构数据引擎,覆盖树(拓扑编辑/遍历/BST/堆/Huffman/LCA)、图(k-hop/度/环检测/二分图着色/最短路/可达)、FSM(串追踪/状态角色/转移补全);简单任务用 matplotlib、密集状态机用 Graphviz(circo);固定节点锚点保持图对空间一致;计算节点/边距离做遮挡校验;用传统求解器解题再改写为 CoT 编辑 prompt。

**空间中心(spatial-centric)合成(Figure 12–13)**
- 立体几何(GeoGebra+matplotlib):旋转体、平面对称、点对称、平移、正投影。
- 多视图 CAD:基于开源 **ABC 数据集** + OCC Python 库渲染等距/正/侧/顶视图,随机化颜色材质增多样性,要求由等距视图+指令预测其它视图。
- 空间旋转:基于 **Objaverse**,均匀角度旋转渲染,先生成带背景参考图,经包围盒(长宽比保持 [0.9,1.1])/对象一致性/生成质量三步过滤;两种策略 Object-First(Qwen-Image 合成、GPT-5.1 把关朝向与背景一致性)与 Background-First(Flux.1 Kontext 去物得净背景、Qwen2.5-VL 验证、按包围盒贴回不同朝向对象)。

**幽默中心(meme)合成(Figure 14–15)**:爬取网络/开源 meme,五阶段管线(文字存在检测→模型式指令→用户式 prompt→配对构造[有字用去字 Agent、无字用加字 Agent]→编辑指令生成),产出 meme 生成与编辑数据。

**推理中心(reasoning-centric)合成 / CoT(Figure 16–18)**——本文方法核心之一:引入显式推理模块作为"原始用户指令"与"最终监督信号"之间的解释器,把简短抽象指令自动展开为结构化、可执行的规格(细化目标、子任务分解、可验证约束、有序编辑操作)。覆盖四类:通用图、知识注入图、meme、科学图。例如把"中秋传统食物"→具体描述月饼的金棕外皮/莲蓉红豆馅;把"放一周后的香蕉"→长出褐斑、茎部变暗萎缩。科学图先用 LLM 解析概念产中间推理步骤再生成描述;CS 编辑把求解步骤映射到 **13 个人工预定义模板**,再用 **Qwen3-Max** 改写增多样性。

> 数据合成大量依赖外部强模型(Qwen2.5/3-VL、Qwen-Image、Gemini-3-Flash、GPT-5.1、Flux-Text、Flux.1 Kontext、Nano-Banana Pro 作对照),属典型"蒸馏/合成驱动"配方;**各类合成数据的最终条数与混合比例未在正文逐项披露**(仅在 Table 3 给出训练阶段层面的任务配比)。

## 训练方法
**联合训练目标(§3.2.1)**
- 文本:标准 Next-Token Prediction,ℒ_NTP = -1/T Σ log p_θ(x_t | x_<t, c)。
- 图像:**Flow Matching + 速度参数化**(回归速度场而非噪声 ε)。线性插值路径 z_t = t·z1 + (1-t)·z0,ℒ_FM = E‖v_θ(z_t,t,c) - (z1-z0)‖²。
- 总损失 ℒ_Total = α·ℒ_NTP + β·ℒ_FM,**各阶段动态调 α/β**。

**三阶段渐进训练管线(§3.2.2,Table 3)**——从仅理解的预训练 MLLM 初始化,逐步解锁视觉合成再统一:

| 阶段 | 可训练 | 分辨率 | 数据/任务 | 配比 | Loss 权重(NTP:VP) | LR / scheduler | steps / batch |
|---|---|---|---|---|---|---|---|
| **Stage 1** 生成头预训练 | 冻结主干,仅训生成头+投影器 | 固定 512px(**跳过 256px** 加速收敛) | T2I + IT2I | 4:1 | 0:1 | 3e-4 / Constant | 250k / 2048 |
| **Stage 2** 任意分辨率续训 | 主干仍冻结 | 512–1024px、AR 0.5–2.0 | T2I + IT2I | 3:4 | 0:1 | 1e-4 / Cosine | 60k / 1024 |
| **Stage 3** 统一 SFT | **全解冻(含 MLLM 主干)** 端到端 | 512–1024px | T2I + IT2I + Und | 1:1:2 | 1:20 | 1e-5 / Cosine | 20k / 1024 |

要点:
- Stage 1 **一开始就混入编辑数据**(不像前作只用 T2I 初始化),强迫生成头同时关注文本指令与视觉上下文 token,打牢多模态条件对齐基础。
- Stage 2 二次过滤只留高美学样本、剔除极端长宽比;编辑任务**显式把条件图的 VAE latent 注入生成头**做像素级一致。
- Stage 3 解冻主干 + 加入 **CoT 推理数据**(§4.7),让模型先用文本推理"规划"再在视觉域执行;Loss 权重 NTP:VP=1:20。
- 通用超参:AdamW(β1=0.9,β2=0.999),warm-up 1000 步,diffusion timestep shift=3.0,理解分辨率固定 448px。
- **CFG**:T2I 训练 10% 丢条件;编辑训练 5% 丢全部多模态条件、另 5% 只丢文本保图像。
- **推理加速**:用 **Flow-DPM-Solver、20 步**;CFG scale 全丢=3.5、只丢文本(编辑)=1.5。仓库默认生成分辨率示例 576×1024,bf16 推理。
- **推理模式开关**:`generation_mode="image"`(直接生成,推荐简单场景)/`"text_image"`(先出 CoT 文本再生成,适合复杂推理)。

## Infra(训练 / 推理工程)
- 训练规模可由 Table 3 推:三阶段总训练步约 250k+60k+20k=**33 万步**,Stage 1 batch 2048、Stage 2/3 batch 1024。**GPU 型号、卡数、GPU·小时、并行/分布式策略、混合精度细节、吞吐均未在报告中披露**。
- 工程取巧:Stage 1 跳过 256px 直接 512px、复用 Qwen-Image VAE、生成头 1.7B 保持小体量,均服务于"低成本拿到统一能力"的目标。SVG 物理编辑把数据合成成本从 \$0.16→\$0.03/样本。
- 推理:Flow-DPM-Solver 20 步;部署形态为开源 `InternVLUPipeline`(HF 权重 `InternVL-U/InternVL-U`,bf16,单卡 `cuda`),支持理解/T2I/编辑/CoT 引导生成、多图理解。**量化/蒸馏/步数蒸馏等未提及**。
- 配套开源评测基建:**GenEditEvalKit**(统一 UMM 生成+编辑评测工具)、**TextEdit Benchmark**(2148 样本文字编辑基准),均 open-compass 仓库。

## 评测 benchmark(把效果讲清楚)
所有数字均来自报告 Table 4–19(已抓取 PDF)。理解用 VLMEvalkit,生成/编辑用自研 GenEditEvalKit。

**多模态理解与推理(Table 4,7 benchmark)**
- InternVL-U(2B+1.7B):MME-P **1607.5**、SEED 75.2、ChartQA 76.6、OCRBench **83.9**、MMMU **54.7**、MathVerse 45.6、LogicVista 40.3。
- 显著超过同量级 UMM:Janus-Pro(1.5B,MME-P 1444)、Ovis-U1(MME-P 1508*);MMMU 54.7 ≈ **BAGEL(7B+7B)的 55.3**,几乎追平 3.5× 体量的对手。相对理解型基座 InternVL3.5-2B(MMMU 59.0、OCRBench 83.6)有可控退化,说明统一训练较好保住了理解。

**通用 T2I**
- **GenEval(Table 5)**:Overall **0.85** —— **统一模型中最高**(超 BAGEL 0.82、Janus-Pro 0.80、OmniGen2 0.80),且超多数专用生成模型(FLUX.1-dev 0.66、SD3-Medium 0.74),逼近 Qwen-Image 20B 的 0.87。Position 0.77、Colors 0.91 突出。
- **DPG-Bench(Table 6)**:Overall **85.18**,统一模型最高(BAGEL 85.07、Janus-Pro 84.19),Global 90.39/Entity 90.78 较强;距 Qwen-Image 88.32、Z-Image 88.14 仍有差。
- **TIIF(Table 7/8)**:短 prompt Overall **74.9**(统一模型最高,超 BAGEL 71.5、Lumina-DiMOO 74.7),长 prompt 73.9(超 BAGEL 71.7);Text 子项短 47.5/长 50.7 远好于多数 UMM。与专用生成模型(Qwen-Image 86)仍有明显差距。
- **OneIG(Table 9/10)**:EN Overall **0.50**、ZH **0.50** —— 开源统一模型中最高(BAGEL EN 0.36/ZH 0.37、OmniGen2 EN 0.47);ZH Text 子项 **0.90** 极突出(BAGEL 0.37)。

**文本中心 T2I**
- **CVTG-2k(Table 11)**:平均 word accuracy **0.623**,**统一模型 SOTA**(Lumina-DiMOO 0.590、BAGEL 0.356、Ovis-U1 0.093);NED 0.804、CLIPScore 0.816。
- **LongText-Bench(Table 12)**:EN **0.738**、ZH **0.860**,大幅领先 UMM(OmniGen2 EN 0.561/ZH 0.059、BAGEL 0.373/0.310),"补齐了统一模型在可读文字渲染上的短板"。

**知识注入 T2I(CoT 是关键催化剂)**
- **WISE(Table 13)**:无 CoT Overall 0.46 → **加 CoT 0.58**,超 BAGEL 0.49、UniWorld-V1 0.55,接近 Qwen-Image 0.63。
- **GenExam(Table 14,relaxed)**:无 CoT 20.8 → **加 CoT 22.9**,**统一模型最高**(BAGEL 11.9、Show-o2 12.0);物理/化学/生物突出。距闭源 Nano-Banana Pro 93.7、GPT-Image-1.5 82.3 差距巨大。

**图像编辑**
- **ImgEdit(Table 15)**:Overall(w/ CoT)**3.82**(无 CoT 3.67),近 Ovis-U1 3.97、超 BAGEL 3.20。
- **GEdit-Bench(Table 16)**:Avg **6.66**,超 BAGEL 6.52、Ovis-U1 6.42;**加 CoT→6.88**。专用编辑模型 Qwen-Image-Edit 8.01 仍领先。
- **TextEdit(自建,2148 样本;Table 17/18)**:经典指标 Real F1 **0.71**(=Nano-Banana Pro,远超 Ovis-U1 0.35、BAGEL 0.55);MLLM 评测 Real Avg **0.88**(超 BAGEL 0.53,逼近闭源 GPT-Image-1.5/Nano-Banana Pro 0.90/0.91)。
- **RISEBench(推理编辑,Table 19)**:无 CoT Overall 3.6 → **加 CoT 9.4**,**超 BAGEL 6.1、Qwen-Image-Edit 8.9**;CoT 主要拉动 Instruction Reasoning(35.6→43.9)与 Appearance Consistency(52.7→64.4)。但距闭源 GPT-Image-1.5 50.0、Nano-Banana Pro 47.2 差距很大。

**关键消融/结论**:CoT(text_image 模式)在知识注入生成(WISE/GenExam)与推理编辑(RISEBench)上是**决定性增益来源**,RISEBench 几乎翻 2.6 倍;但在已较直白的通用编辑(ImgEdit/GEdit)上提升温和。**未给出 FID/CLIPScore(GenEval)/HPSv2/PickScore/人评 ELO 等指标**,也未做视频。

## 创新点与影响
**核心贡献**
1. **三原则架构**(统一上下文建模 + 模态特定模块化 + 解耦视觉表征),把生成能力"无损"嫁接到强理解基座,用 4B 拿到此前需 14B(BAGEL)级别的统一能力,实现性能-效率的显著平衡(论文主题词:democratize)。
2. **自研 MMDiT 生成头的三处工程创新**:Dual-Stream 双流解耦参数、**首次在 MMDiT 引入门控注意力**(缓解 attention-sink)、Unified 3D MSRoPE + Resolution Interpolation(利于编辑空间推理与高分辨率扩展)。
3. **面向高语义密度任务的合成管线 + Reasoning-centric CoT 范式**:把抽象指令显式展开为可执行计划,弥合"模糊意图↔精确视觉执行"的鸿沟,显著拉动文字渲染、科学知识、空间推理、幽默生成;SVG-based 物理编辑等把合成成本压到 1/5。
4. 开源**模型 + 推理代码 + 两套评测基建(GenEditEvalKit / TextEdit)**,定位为社区强基线。

**影响**:展示了"强开源理解 MLLM + 轻量专用生成头 + CoT 数据"是一条低成本通向 omni-capable UMM 的可行路径,尤其把"统一模型不会写字"和"统一模型缺知识/推理"两大短板做了实质改善;TextEdit/GenEditEvalKit 为 UMM 评测提供了新工具。

**已知局限(据报告数据与未披露项)**
- 与专用生成/编辑模型(Qwen-Image 20B、Qwen-Image-Edit)及闭源 SOTA(Nano-Banana Pro、GPT-Image-1.5、Seedream 4.5)在 TIIF/GenExam/RISEBench 等高难基准上仍有**显著差距**。
- CoT 收益依赖 text_image 模式,需额外推理开销;部分子维度(如 RISEBench Spatial 加 CoT 反而 5.0→1.8)出现退化,稳定性有限。
- **训练 infra(卡数/GPU·时/并行)、数据总规模与各类合成数据的精确配比、FID/人评等部分指标均未披露**;数据高度依赖外部强模型蒸馏,存在配方可复现性与数据来源合规的隐含问题(报告未展开)。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2603.09877
- arxiv_pdf: https://arxiv.org/pdf/2603.09877
- github: https://github.com/OpenGVLab/InternVL-U
- huggingface (model): https://huggingface.co/InternVL-U/InternVL-U
- huggingface (paper): https://huggingface.co/papers/2603.09877
- GenEditEvalKit: https://github.com/open-compass/GenEditEvalKit
- TextEdit Benchmark: https://github.com/open-compass/TextEdit
- 主仓库(InternVL 家族,含历史模型链接): https://github.com/OpenGVLab/InternVL

## 本地落盘文件
- ../../../sources/omni/2026/arxiv-2603.09877.pdf  (技术报告全文 PDF,~35MB,8 节正文+附录;.gitignore 排除不入 git,本地精读)
- ../../../sources/omni/2026/internvl-u--arxiv-abs.html  (arXiv abstract 页快照,含作者/提交日期)
- ../../../sources/omni/2026/internvl-u--repo-readme.md  (OpenGVLab/InternVL-U 官方仓库 README)
- ../../../sources/omni/2026/internvl-u--hf-modelcard.md  (HuggingFace InternVL-U/InternVL-U model card)
- ../../../sources/omni/2026/internvl-u--internvl-main-repo-readme.md  (InternVL 主仓库 README,作家族背景上下文;截至抓取时尚未收录 InternVL-U 条目)
