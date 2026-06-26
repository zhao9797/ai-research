---
title: "Make Pixels Dance: High-Dynamic Video Generation (PixelDance)"
org: "ByteDance Research"
country: China
date: "2023-11"
type: paper
category: video
tags: [video-generation, diffusion, image-conditioned, first-last-frame, latent-diffusion, high-dynamic, long-video, bytedance]
url: "https://arxiv.org/abs/2311.10982"
arxiv: "https://arxiv.org/abs/2311.10982"
pdf_url: "https://arxiv.org/pdf/2311.10982"
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://makepixelsdance.github.io/"
downloaded: [arxiv-2311.10982.pdf, make-pixels-dance--project-page.md]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
PixelDance 是字节跳动 2023 年 11 月提出的高动态视频生成方法（CVPR 2024），核心创新是把 **`<文本, 首帧图像, 尾帧图像>` 三重条件**注入潜空间扩散模型，让模型专注学习"运动动力学"而非繁重的文本描述，从而生成动作丰富、可处理复杂/域外场景的视频。仅 **1.5B 参数**、主要用公开数据 WebVid-10M 训练，零样本 FVD 在 MSR-VTT 达 **381**、UCF-101 达 **242.8**，并据称生成了"首个 3 分钟、有清晰故事线、跨镜头角色一致"的 AI 视频。它是后续字节 **Seedance** 视频路线的前身。

## 背景与定位
当时（2023 中）的文生视频（T2V）主流方法（[[make-a-video]]、ModelScope、[[cogvideo]] 等）在保持画面保真度的同时，往往只能生成**运动极少**的视频；即便引入图像输入（如 Runway Gen-2、VideoGen 等 image-to-video），生成结果运动幅度依然有限，尤其当输入图像是训练分布外（out-of-domain，如科幻、漫画、卡通）内容时退化更严重。

论文给出的判断是：**仅靠文本指令做视频生成是不充分、次优的**。原因有二：(1) 要让模型理解并跟随精细文本描述以刻画"画面+运动"，需要极昂贵的高质量文本标注（呼应 DALL·E 3 的 re-caption 思路 [4]），且模型需大幅 scale-up 才能学好；(2) 公开视频数据集（如 WebVid-10M）的文本只是粗粒度、与视频弱相关的描述。

PixelDance 的破局思路：用**视频真值帧**作为首帧/尾帧的图像指令（训练时白嫖、零额外标注成本），把"画什么内容"交给图像指令，让模型把建模容量集中在"怎么动（dynamics）"上。这样既能更高效利用 WebVid-10M 这类弱标注公开数据，又能把学到的运动知识泛化到域外图像指令。技术上它建立在 [[ddpm]] 和潜空间扩散（LDM，见 [[stable-diffusion-1]]）之上，沿用了 [[align-your-latents-vldm]]、[[make-a-video]] 等"2D UNet 加时序层"的范式，但条件设计和首尾帧训练/推理技巧是其独有贡献。

## 模型架构
**潜空间扩散 + 3D UNet。** 采用 LDM 框架：在预训练 VAE 的压缩潜空间里做去噪以降低算力。Backbone 是经典 2D UNet（空间下采样—上采样 + skip connection），由两类基本块构成：2D 卷积块、2D 注意力块。

**扩成 3D 的方式（运动建模）：** 在 2D 卷积层后插入**沿时间维的 1D 卷积层**，在 2D 注意力层后插入**沿时间维的 1D 注意力层**（时序注意力用**双向 self-attention**）。模型可图像/视频联合训练——对纯图像输入时禁用 1D 时序算子，以保持空间维的高保真生成能力。

**文本编码：** 用预训练 **CLIP text encoder** 编码文本指令，得到的 `c_text` 通过 UNet 内的 **cross-attention** 注入（hidden states 作 query，`c_text` 作 key/value）。

**图像指令注入（核心设计）：** 首帧/尾帧图像 `{I_first, I_last}` 先用 **VAE encoder** 编码为 `{f_first, f_last}`（`f ∈ R^{C×H×W}`）。为保留时序位置信息，构造图像条件张量：

`c_image = [f_first, PADs, f_last] ∈ R^{F×C×H×W}`，其中 `PADs ∈ R^{(F-2)×C×H×W}`（中间帧位置补零）。

`c_image` 随后**沿通道维**与加噪潜变量 `z_t` 拼接（concat），作为扩散模型输入。也就是说图像条件不是走 cross-attention，而是走 channel-concat 的"in-painting/外推"式输入。

**参数量与分辨率：** 整模型仅 **1.5B 参数**（论文反复强调相对 CogVideo 15.5B、Video-LDM 4.2B 等"小而强"，并把"未来 scale-up"列为后续方向）。先在 **256×256** 训练（用于定量评测），再微调到更高分辨率。文本编码器与 VAE 在训练中**冻结**。

## 数据
- **主数据：WebVid-10M** —— 约 1000 万短视频片段，平均时长 ~18 秒，主分辨率 336×596，配粗粒度、与内容弱相关的文本。已知缺陷：(1) 文本与视频关联松散；(2) 缺乏多样风格（漫画、卡通等）；(3) **所有视频带水印**，会导致生成结果也带水印。
- **自采补充数据：约 50 万条无水印视频片段**，描绘真实世界实体（人、动物、物体、风景），配粗粒度文本。虽占比很小，但作者发现：把它与 WebVid-10M 混合训练后，**只要图像指令本身无水印，PixelDance 就能生成无水印视频**（一个有意思的"解耦水印"副产物）。
- **图文数据：LAION-400M** —— 与视频联合训练，**每 8 个训练迭代用一次图文数据**（沿 Imagen Video [21] 的图像/视频联合训练做法），以保持空间维高保真。
- **视频采样：** 每条视频随机取 **16 帧连续帧，4 fps**。
- 没有使用昂贵的高质量重标注（这正是其卖点——用真值帧当图像指令绕开标注成本）。

## 训练方法
**目标函数：** 标准扩散，采用 **DDPM**（T=1000 步）、**ε-prediction**（预测噪声）。推理用 **classifier-free guidance**（混合有/无文本条件的 score 估计）。

**首帧指令——强约束。** 训练时直接用真值首帧作为首帧指令，迫使模型**严格遵守**首帧（保证连续片段间的内容连贯性、可衔接长视频）。推理时首帧可由 T2I 模型（如 Stable Diffusion V2.1）生成，或用户直接提供。

**尾帧指令——弱约束（三大技巧，论文精髓）。** 作者**刻意不让模型精确复刻尾帧**，因为推理时拿不到完美尾帧、且要容纳用户手画的粗糙草图。为此设计三技巧：
1. **随机取末三帧之一**作尾帧指令（而非固定最后一帧），降低对精确尾帧的依赖；
2. **给图像指令的编码潜变量 `c_image` 加噪**（对应 100 个时间步的噪声量），提升鲁棒性；
3. **以概率 η（如 25%）随机丢弃尾帧指令**（把对应潜变量置零）。

**对应的推理采样策略：** 在总 T 步去噪的**前 τ 步**用尾帧指令把生成引导向目标结局，**后续步丢弃尾帧指令**以生成更连贯流畅的视频：

`x̃_θ = x̂_θ(z_t, f_first, f_last, c_text)  if t < τ；否则 x̂_θ(z_t, f_first, c_text)`

**τ 是控制旋钮：** 调 τ 即调"对尾帧指令的依赖强度"。τ=0 时退化为"无尾帧"的高动态生成（论文图 7 显示 τ=25 既贴合尾帧又避免"画面突兀地停在尾帧上"）。这一"前期引导、后期放手"的设计是 PixelDance 实现"可控但不僵硬"的关键。

**长视频生成：** 用**自回归**方式——把前一片段的尾帧作为下一片段的首帧指令，逐段生成。因为模型对首帧是强约束，所以跨片段内容/角色能保持一致；论文据此合成了 3 分钟有故事线的视频。

## Infra（训练 / 推理工程）
- **算力：** 256×256 阶段在 **32×A100 GPU**、batch size **192**、训练 **200K 迭代**；随后在更高分辨率再微调 **50K 迭代**。
- **冻结组件：** 文本编码器（CLIP）与 VAE 全程冻结，只训扩散 UNet（含新增时序层）。
- **推理：** DDPM 采样 + CFG；尾帧指令在前 τ 步参与、后续步丢弃（即上文 τ 调度）。零样本视频编辑无需额外训练（把视频编辑转成"编辑首帧+尾帧"的图像编辑任务）。
- 论文**未披露** GPU·小时总量、并行/分布式策略、混合精度、吞吐与具体推理步数、是否做步数蒸馏/缓存等加速。属研究型工作，无量化/部署形态披露。

## 评测 benchmark（把效果讲清楚）
**零样本 T2V（仅文本，首帧由 SD V2.1 生成；256×256）：**

MSR-VTT（表 1，指标 CLIPSIM↑ / FVD↓）：
- PixelDance（1.5B，10M data）：**CLIPSIM 0.3125 / FVD 381**
- ModelScope（1.7B）：0.2939 / 550
- Make-A-Video（9.7B，20M）：0.3049 / —
- VideoFactory：0.3005 / —；Latent-Shift：0.2773 / —
- CogVideo(En)（15.5B）：0.2631 / 1294
- → PixelDance 在 FVD 与 CLIPSIM 上**同时取得当时 SOTA**，FVD 381 显著优于此前最优 ModelScope 的 550，且参数量远小于 CogVideo 15.5B。

UCF-101（表 2，指标 IS↑ / FID↓ / FVD↓）：
- PixelDance：**IS 42.10 / FID 49.36 / FVD 242.82**
- Dysen-VDM（10M）：— / — / 325.42（次优 FVD）
- VidRD（5.3M）：— / — / 363.19；Make-A-Video（20M）：— / — / 367.23
- ModelScope（10M）：— / — / 410.00；Video-LDM（10M）：33.45 / — / 550.61
- CogVideo(En)：25.27 / 179.00 / 701.59
- → PixelDance 在 IS / FID / FVD 三项**全面领先**。

**消融（UCF-101，表 3，FID↓ / FVD↓）：**
- ① T2V baseline（同数据训练）：59.35 / 450.58
- ② PixelDance（全条件）：**49.36 / 242.82**
- ③ 去文本指令 `c_text`：51.26 / 375.79
- ④ 去尾帧指令 `f_last`：49.45 / 339.08
- 关键结论：去任一指令都明显掉点；**即便评测时不喂尾帧，带尾帧训练的②(242.8) 仍优于不带尾帧训练的④(339.1)**——说明尾帧指令在训练期帮助模型更好地建模运动动力学与时序一致性，是"训练增益"而非仅"推理外挂"。

**长视频生成（UCF-101，生成 512 条 ×1024 帧，逐 16 帧报 FVD，图 8）：** PixelDance（自回归）相比自回归基线 TATS-AR、LVDM-AR 以及层次化 LVDM-Hi，FVD 更低且随时间变化更平滑（误差累积更小）。具体数值为曲线图，论文未给单点数字。

**定性能力：** 文本指令负责运动（肢体/表情/物体运动/视觉特效）+ 相机控制（zoom in/out、rotate、close-up）+ 跨帧关键元素一致性；首帧提供精细视觉细节并支撑连续片段；尾帧专门用于复杂运动/域外场景/自然转场。还展示了 sketch（HED 边缘图）作尾帧指令的扩展，以及**零样本视频编辑**（编辑首尾帧即可）。

## 创新点与影响
**核心贡献：**
1. **首尾帧 + 文本三重条件**的视频生成范式：用真值帧当图像指令，让模型聚焦"运动动力学"，绕开昂贵的精细文本标注，同时更高效利用弱标注公开数据（WebVid-10M）。
2. **尾帧"弱约束"训练/推理三技巧 + τ 调度**：随机末三帧 / 加噪 / 随机丢弃 + 前 τ 步引导后放手——既能让用户用粗糙草图引导结局，又不让画面僵硬地"卡"在尾帧上，是其可控且自然的关键。
3. 在仅 1.5B 参数、公开数据下，于 MSR-VTT / UCF-101 取得零样本 SOTA，并演示了首个 3 分钟有故事线、角色跨镜头一致的 AI 视频（自回归长视频）。

**影响：** PixelDance 被视为字节跳动 **Seedance** 视频生成路线的前身/技术起点，把"图像指令（尤其首帧/关键帧）+ 文本"确立为高动态、可控视频生成的有效范式，对后续 image-to-video / 关键帧驱动视频生成有方法论影响。CVPR 2024 接收。

**已知局限（作者自述）：** (1) 可受益于高质量、开放域视频数据训练；(2) 特定域微调可进一步增强；(3) 引入标注关键元素/运动的文本可改善指令对齐；(4) 仅 1.5B 参数，**未来需 scale-up**（这也正是后续 Seedance 的方向）。此外论文未披露推理速度、工程加速与部署细节。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2311.10982
- arxiv_pdf: https://arxiv.org/pdf/2311.10982
- project_page: https://makepixelsdance.github.io/
- youtube_demo: https://www.youtube.com/watch?v=QERmPmCg9aQ （项目页给出）

## 一手源存档（sources/）
- [arxiv-2311.10982.pdf](https://arxiv.org/pdf/2311.10982)  （arXiv 原文 PDF，不入 git）
- [project-page.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/make-pixels-dance--project-page.md)
