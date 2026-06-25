---
title: "I2VGen-XL: High-Quality Image-to-Video Synthesis via Cascaded Diffusion Models"
org: "Alibaba Group (Tongyi Lab)"
country: China
date: "2023-11"
type: tech-report
category: video
tags: [image-to-video, video-diffusion, cascaded-diffusion, vldm, ldm, sdedit, open-source]
url: "https://arxiv.org/abs/2311.04145"
arxiv: "https://arxiv.org/abs/2311.04145"
pdf_url: "https://arxiv.org/pdf/2311.04145"
github_url: "https://github.com/ali-vilab/VGen"
hf_url: "https://huggingface.co/ali-vilab/i2vgen-xl"
modelscope_url: "https://modelscope.cn/models/iic/i2vgen-xl"
project_url: "https://i2vgen-xl.github.io"
downloaded: [arxiv-2311.04145.pdf, i2vgen-xl--readme.md, i2vgen-xl--hf-model-card.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
I2VGen-XL 是阿里通义实验室（Tongyi Lab of Alibaba Group，据 HF/GitHub README）2023 年 11 月发布的**级联式图生视频（image-to-video）扩散模型**：用一张静态图作为主要条件，先在低分辨率（448×256）做"语义对齐 + 内容保持"的 base 阶段，再用独立的 refinement 阶段把分辨率提到 **1280×720** 并修复时空细节。核心创新是**显式解耦"语义对齐"与"时空清晰度"两个任务**，并用静态图绕开"高质量图文-视频对稀缺"的瓶颈。训练规模为 **3500 万单镜头视频 + 60 亿图文对**。它是开源 i2v 的代表性工作，已开源代码与权重（VGen 仓库）。

## 背景与定位
视频合成在扩散模型推动下进步显著，但仍受三大问题困扰：语义准确性、清晰度、时空连续性。论文把根因归结为两点：(1) **对齐良好的文本-视频数据稀缺**；(2) 视频固有结构复杂，模型很难同时保证语义与画质。

I2VGen-XL 给出两条对策：
- **用静态图做主条件**绕开"文本-视频对齐"难题——图像天然与首帧内容对齐，比文本更强的条件信号；
- **级联解耦**：把"保语义/保内容"和"提分辨率/去伪影"拆成两个独立训练、目标不同的阶段。

技术脉络上，它构建在 [[latent-diffusion-ldm]]（潜空间扩散）之上，3D U-Net backbone 继承自同组的 [[modelscope-t2v]] 与 VideoComposer，spatial 权重用 SD2.1 初始化（受 [[sdxl]] 启发命名 "-XL"）。相对前置工作的改进：

- 对比 **Imagen Video** 这类"多模型逐级提质"路线——后者每一级用相同输入优化相同目标，未显式解耦任务，导致各级学到相似分布、残留可观噪声；I2VGen-XL 让两阶段**用不同条件、不同目标**，避免这种退化。
- 对比需要额外引导/训练的可控视频方法（如 CodeF），I2VGen-XL 只需一张图即可驱动，部署门槛更低。
- refinement 阶段借鉴 [[sdedit]] 的 noising-denoising 思想，把低分辨率结果加噪后用高清模型重去噪，而非从零生成。

## 模型架构
**整体为两阶段级联的 VLDM（video latent diffusion model）**，两阶段都在 LDM 框架下工作，潜空间用预训练 **VQGAN** 编码器把视频 x∈R^(F×H×W×3) 压成 latent z∈R^(F×h×w×c)。

**Backbone：3D U-Net（VLDM）。** 沿用 ModelScope-T2V / VideoComposer 的带时序感知的 3D U-Net（论文记作 VLDM），扩散步数 T=1000。

### Base 阶段（448×256，保语义 + 保内容）
关键设计是**两个层级的图像编码器**，分别注入高层语义与低层细节：

- **High-level semantics（高层语义）**：用**固定的 CLIP 视觉编码器**抽语义特征。但作者发现单用 CLIP 会导致内容/结构保持差（CLIP 训练目标是图文对齐，偏高层语义、忽略细节）。为此**新增一个可训练的 global encoder（G.Enc.，全局编码器）**学习互补特征——其结构见论文 Table 1，是一串 Conv2D + SiLU 的卷积栈，从 H×W×3 逐级下采样到 1×1×1024 的一维向量。CLIP 特征与 G.Enc. 特征**逐元素相加**后，通过 **cross-attention 注入 3D U-Net 的每个 spatial 层**。
- **Low-level details（低层细节）**：即便如此，把图压成低维向量仍会丢细节。于是再用 **VQGAN 编码器（detail encoder, D.Enc.）**抽特征，**直接加到第一帧的输入噪声上**。VQGAN 能完整重建原图，因而能最大限度保留细节。消融发现：用这个 local encoder 比用更复杂的语义编码器更能保内容，但随视频播放会出现失真（语义清晰度下降）——说明两个层级编码器**互补**，需联合使用。

### Refinement 阶段（→1280×720，提清晰度 + 去伪影）
- 训练**一个独立的 VLDM**，专门吃高质量、高分辨率数据（分辨率均 >1280×720）。
- **条件换成用户给的简短文本（几个词），而非原输入图**。作者发现：若两阶段用相同条件，会因引入相似映射而**丧失修复能力**；换一个不同条件能带来有效补偿。文本用 **CLIP 编码**后经 cross-attention 注入 3D U-Net。
- 只在**前 Tr 个去噪 scale** 上训练/作用（聚焦时空细节，默认 Tr=600）。

**参数初始化策略**：base 模型的 spatial 部分用 **SD2.1 预训练参数**初始化以获得初始图像生成能力；refinement 用训好的 base 模型初始化。分辨率策略：base 448×256、refinement 1280×720，均用 center crop。

## 数据
- **总规模**：约 **3500 万单镜头（single-shot）文本-视频对** + **60 亿（6 billion）图文对**，分辨率从 360p 到 2K。
- **公开数据**：**WebVid-10M**（视频）+ **LAION-400M**（图像）。
- **私有数据**：同类型的 video-text 对与 image-text 对（论文称"private datasets"，未披露具体来源与规模拆分）。
- **数据筛选/平衡**：按**美学分数（aesthetic score）、运动强度（motion intensity）、主体占比（proportion of the main subject）**三个维度排序，以实现训练样本的均衡供给。
- **高质量子集**：refinement 阶段最后一轮在**约 100 万条精选高质量视频**上微调。
- 开源模型仅用 WebVid-10M + LAION-400M 训练，限研究/非商业用途（开源版 disclaimer）。
- 注：re-captioning、安全过滤、私有数据配比等细节**未披露**。

## 训练方法
**训练目标**：标准 LDM/扩散 ε-prediction 目标（L_VLDM = E‖ε − ε_θ(z_t,t)‖²），但实际采用 **v-parameterization**（v-参数化）训练扩散模型，并加 **offset noise（强度 0.1）**，noise schedule 用 **linear**。

**多阶段训练流程**：
1. **Base 模型**：spatial 层用 SD2.1 初始化。训练整个 3D U-Net 时，对 **spatial 层施加系数 γ=0.2 的缩小更新**（相对 temporal 层降速更新，保护预训练图像先验、重点学时序）。
2. **Refinement 模型**：用训好的 base 模型初始化，同样的训练策略；只在初始 Tr 个 noise scale 上训练以聚焦时空细节。采用两步走：(i) 在整个高分辨率数据集上做高分辨率训练；(ii) 在约 100 万条精选高质量视频上做最后一轮 fine-tuning 以强化细节感知。

**关键超参/trick**：
- 优化器 **AdamW**，固定学习率 **8×10⁻⁵**。
- **动态帧数 + 动态 FPS**联合训练：帧长 {1,8,16,32} 的供给比为 **1:1:1:5**；FPS {1,4,8,16} 的供给比为 **1:2:4:1**（FPS=1 即表示输入是静态图——把图当作单帧视频，统一图/视频训练）。

**推理（两阶段拼接）**：用 **noising-denoising（SDEdit 式）**串联两段——base 阶段出低分辨率视频后 resize 到 1280×720，用 **DDIM** 做 Tr 步加噪反演到新 latent，再用 refinement 模型对前 Tr 个 scale 去噪得高清结果。采样器按分辨率/质量权衡混用 **DDIM 与 DPM-solver++**。默认 Tr=600（个别样本可变）。形式化为 ε̂_{θ,t}(z_t,c_i,c_t,t)=ε_θ(z_t,c_t,ε̂_{θ,i}(z_t,c_i,T),t)，c_i/c_t 分别为图像/文本条件。

**蒸馏/加速**：本工作本身未做步数蒸馏；同组后续的 **VideoLCM**（Video Latent Consistency Model, 2023.12, arXiv:2312.09109）在 VGen 框架内对这类 VLDM 做了一致性蒸馏加速。

## Infra（训练 / 推理工程）
论文与开源仓库**未披露**算力规模（GPU 数量、GPU·时）、并行/分布式策略、混合精度方案与训练吞吐等工程数字。

可确认的工程信息（来自 VGen 开源仓库）：
- 代码库 **VGen**（ali-vilab/VGen）是通义实验室的完整视频生成 codebase，支持分布式训练（`train_net.py --cfg ...`）、推理、图/视频联合训练、可视化、采样、加速等；模块化注册 ENGINE/MODEL/DATASETS/EMBEDDER/AUTO_ENCODER/VISUAL/DIFFUSION/PRETRAIN。
- 依赖：PyTorch 1.12（cu113）/ 后续支持 torch2.0+ 与 xformers 0.0.22，去除了 flash_attn 依赖。
- 部署形态：开源权重 `i2vgen_xl_00854500.pth`；提供 ModelScope / HuggingFace Spaces 在线 demo、本地 gradio app、Replicate 部署。HF 模型卡许可 **MIT**。
- 推理时长：README 称生成一段高清视频"几分钟"内完成（未给精确数字/硬件）。

## 评测 benchmark（把效果讲清楚）
**这是本工作的一个明显短板：技术报告以定性分析为主，几乎没有给出定量 benchmark 数字**（无 FVD / IS / CLIPScore / VBench 等表格化指标，也无人评 ELO/胜率数字）。已抓取的一手源（arXiv PDF + 开源 README/HF 卡）中**未报告**任何标准定量视频生成指标。

报告给出的是定性与机理分析：
- **与 SOTA 对比（定性）**：用 web 界面对比 **Gen-2** 与 **Pika**，输入伪真实 / 真实 / 抽象画三类图。结论：(i) **运动丰富度**——I2VGen-XL 运动更真实多样（如"飞翔的狗"），而 Gen-2/Pika 结果更偏静态；(ii) **ID 保持度**——Gen-2/Pika 保身份更好，I2VGen-XL 会丢一些输入细节。作者明确指出**ID 保持与运动强度存在 trade-off**，本方法在两者间取折中。
- **refinement 机理分析（频域）**：在频域分析 refinement 前后变化（论文 Fig.7）。发现：低质量视频在高频段的频率分布接近噪声，高质量视频则更接近输入图的分布；refinement 模型**保留低频、平滑高频**，在时空两域上**保低频、抑中频、增高频**——表明时空伪影主要集中在**中频段**。
- **消融结论**：(i) 单 CLIP 编码器保内容差 → 必须加可训练 global encoder 互补；(ii) 用 VQGAN local detail encoder 比复杂语义编码器更能保内容，但单用会随时间失真 → 两层级编码器互补；(iii) 两阶段若用相同条件会丧失修复能力 → refinement 必须换不同条件（文本）。
- **泛化定性结果**：在人脸、3D 卡通、动漫、国画、小动物等多类目上生成合理运动；专门验证了人体运动的鲁棒性。

> 注：因开源训练数据限制，模型在**动漫图像**与**黑色背景图像**上表现欠佳（README 明确说明）。

## 创新点与影响
**核心贡献**：
1. **任务解耦的级联范式**：把"语义/内容对齐"与"时空清晰度/去伪影"显式拆成两阶段、用**不同条件不同目标**训练，避免 Imagen Video 式"各级同目标同输入→分布趋同→残留噪声"的退化。
2. **静态图作为主条件**绕开高质量文本-视频对的稀缺瓶颈，是开源 i2v 的早期代表路线（"先对齐内容、再提分辨率"）。
3. **双层级图像编码器**（固定 CLIP 语义 + 可训练 global encoder + VQGAN detail encoder 注入首帧噪声）实现语义与细节的互补保持。
4. **SDEdit 式两阶段拼接 + 不同条件补偿**，配合 refinement 的频域机理分析，把"超分/修复"做成独立可训练模块。
5. **图/视频统一训练**（FPS=1 即图像）与动态帧数/FPS 供给比这一工程化训练配方。

**影响**：
- 开源代码与权重（VGen 仓库 ali-vilab/VGen）成为开源图生视频的重要基线，被 diffusers 集成（`I2VGenXLPipeline`，HF 卡确认），并衍生 Replicate/HF Spaces/ModelScope 多端部署（README 确认）。（注：仓库 star 数等社区指标随时间变化，已落盘源未给具体数字，此处不引用。）
- VGen 框架孵化了同组一系列后续工作：ModelScope-T2V、VideoComposer、HiGen、TF-T2V、DreamVideo、InstructVideo、VideoLCM、DreamTalk 等，形成"视频生成生态"。
- 是阿里通义视频生成线（后续走向 Wan/通义万相系列）的早期奠基工作之一。

**已知局限（作者自述）**：
1. **人体运动**生成的自由度与自然度仍受限（人体动作复杂）；
2. **长视频能力有限**——只能生成数秒、单镜头短视频，无法做多场景连续叙事；
3. **用户意图理解有限**——文本-视频配对数据稀缺，限制了对 caption/图像输入的理解，交互门槛高。

此外，本报告**缺乏定量 benchmark**，与同期工作横向定量比较困难。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2311.04145
- arxiv_pdf: https://arxiv.org/pdf/2311.04145
- github: https://github.com/ali-vilab/VGen
- project_page: https://i2vgen-xl.github.io
- hf_model: https://huggingface.co/ali-vilab/i2vgen-xl
- hf_space: https://huggingface.co/spaces/damo-vilab/I2VGen-XL
- modelscope: https://modelscope.cn/models/iic/i2vgen-xl

## 本地落盘文件
- ../../../sources/omni/2023/arxiv-2311.04145.pdf
- ../../../sources/omni/2023/i2vgen-xl--readme.md
- ../../../sources/omni/2023/i2vgen-xl--hf-model-card.md
