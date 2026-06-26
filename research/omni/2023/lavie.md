---
title: "LaVie: High-Quality Video Generation with Cascaded Latent Diffusion Models"
org: "Shanghai AI Lab"
country: China
date: "2023-09"
type: paper
category: video
tags: [t2v, video-diffusion, latent-diffusion, cascaded, temporal-attention, rope, joint-image-video, vimeo25m, open-source]
url: "https://arxiv.org/abs/2309.15103"
arxiv: "https://arxiv.org/abs/2309.15103"
pdf_url: "https://arxiv.org/pdf/2309.15103"
github_url: "https://github.com/Vchitect/LaVie"
hf_url: "https://huggingface.co/YaohuiW/LaVie"
modelscope_url: ""
project_url: "https://vchitect.github.io/LaVie-project/"
downloaded: [arxiv-2309.15103.pdf, lavie--readme.md]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
LaVie 是上海 AI Lab（联合南洋理工 S-Lab、港中文、Monash）2023.9 推出的开源文生视频（T2V）框架，总参数约 3B，由「基础 T2V + 时序插帧 + 视频超分」三级级联潜扩散模型组成；核心创新是**只用最简单的时序自注意力 + RoPE** 把预训练的 Stable Diffusion 1.4 改造成视频模型，并用**图像-视频联合微调**避免灾难性遗忘；同时开源了 25M 高清文本-视频数据集 **Vimeo25M**。零样本 UCF101 FVD=526.30（同设定下超 Video LDM 24.31），最终可生成 1280×2048、61 帧的视频。

## 背景与定位
当时 T2V 有两条路线：(a) 从零训练完整时空模型（[[make-a-video]]、[[imagen-video]]），质量高但算力昂贵、优化周期长；(b) 复用预训练 T2I 模型再加时序模块微调（[[align-your-latents-vldm]] / Video LDM、MagicVideo、LVDM、[[animatediff]]）。LaVie 走第二条路并指出其痛点：**仅在视频数据上微调会引发灾难性遗忘**——SD 学到的「概念组合 / 风格 / 角色」先验会迅速衰退，导致创造性下降。

LaVie 的两点核心洞见：
1. **简单即够**：在 SD 的 transformer block 里直接插入一层时序自注意力，并配 RoPE 编码时间位置，就足以捕获视频时序相关性；更复杂的时序设计（时空注意力、时序因果注意力）只带来边际提升，却显著增大模型与训练成本。
2. **图像-视频联合微调是关键**：把图像沿时间轴拼成「伪视频」与真实视频一起训练，让模型在学运动的同时保住图像先验，实现 scene/style/character 从图到视频的知识迁移。

定位上它是基于 [[latent-diffusion-ldm]]（[[ddpm]] 体系）的级联 V-LDM，是 2023 年**开源 T2V 的代表作之一**，也是 Vchitect 视频生成系统的主干（其 I2V 版本为 SEINE）。

## 模型架构
整体是三网络级联，各自独立训练、推理时串联（CLIP text encoder 提供文本条件）：

**1) Base T2V 模型（16×320×512）**
- backbone：在 SD 1.4 的 2D U-Net 上做两处改造把它「膨胀」成时空网络：
  - **伪 3D 卷积**：每个 2D 卷积核 inflate 出一个额外时间维（B×C×H×W → B×C×1×H×W）。
  - **ST-Transformer（Spatio-Temporal Transformer）**：在原 transformer block 的「空间自注意力(SA-S) + 空间交叉注意力(CA-S) + FF」之后，**追加一层时序自注意力(SA-T)**，并把 **RoPE**（来自 LLaMA / RoFormer）用于该时序注意力以编码帧序。与「另起一个独立 Temporal Transformer」的做法不同，这里是直接改 block 本身，更简洁。
- 文本编码器：CLIP（ViT，沿用 SD），论文在 limitations 中指出 CLIP 是多主体混淆的瓶颈，建议换 T5。
- 自编码器/LDM 均从 **Stable Diffusion 1.4** 初始化，在 latent 时空空间做扩散。

**2) Temporal Interpolation (TI) 模型（16→61 帧）**
- 从 base T2V 初始化的扩散 U-Net，专门把帧率**翻 4 倍**：输入 16 帧 base 视频，输出 61 帧。
- 训练时把 base 帧复制到目标帧率，与带噪高帧率帧 concat 后送入 U-Net，学习重建无噪高帧率帧；为适配高/低帧率拼接输入，额外加一层卷积层。
- 关键区别：**每一帧都是新合成的**（输出帧替换对应输入帧），并以文本 prompt 为条件，区别于传统只在原帧间插值的方法。

**3) Video Super-Resolution (VSR) 模型（→1280×2048）**
- 以 Stability 的 **stable-diffusion-x4-upscaler** 为先验，加入时序层（temporal attention + 3D 卷积）做 3D 处理。
- **空间层冻结，只训练新插入的时序层**；patch-wise 训练（320×320 patch），保留卷积特性故可处理任意尺寸输入；低分辨率视频在 latent 内 concat 作为强条件，并接受文本与噪声等级作为附加条件。

**推理产物**：完整四步管线可生成 **61 帧 / 1280×2048（2K）** 视频。总参数约 **3B**。

## 数据
- 训练用两个公开集 + 一个自建集：**WebVid10M** + **LAION-5B**（图像，分辨率≥1024 的子集用于 VSR）+ 自建 **Vimeo25M**。论文指出 WebVid10M 分辨率低、带水印、美学差，不足以支撑高清 T2V。
- 经分辨率 + 美学分过滤后，最终训练用约 **20M 视频 + 400M 图像**。
- **Vimeo25M 数据集**（本文贡献并发布）：
  - 2500 万条高清（>720p）、宽屏、**无水印** 文本-视频对；视频源自 vimeo.com。
  - **caption 自动生成**：用 **VideoChat** 自动打标；标注后过滤掉少于 3 词的 caption，剔除少于 16 帧的片段。
  - **切镜**：用 **PySceneDetect** 做场景检测与切分，得到 2500 万个单场景片段。
  - 分十类（Ads/Commercials、Animation、Branded Content、Comedy、Documentary、Experimental、Music、Sports、Travel、Narrative），类别相对均衡；caption 多在约 10 词。
  - 质量对比：美学分 >6 的占 **16.89%**（WebVid10M 仅 7.22%）；4~6 分区间 **79.12%** vs 72.58%；分辨率整体显著高于 WebVid10M。
- VSR 训练把图像数据通过随机平移模拟手持镜头运动，转成视频片段参与联合训练。

## 训练方法
- **训练目标**：标准 LDM 扩散去噪（ε-prediction，也提到 v-prediction），在 latent 时空空间最小化 MSE。
- **图像-视频联合微调（核心 trick）**：把 M 张图像沿时间轴拼成 T 帧伪视频，与真实视频同时训练，损失为视频损失 + 系数 α 加权的图像损失：
  `L = E‖ε−εθ(E(vt),t,cV)‖² + α·E‖ε−εθ(E(xt),t,cI)‖²`
  实现细节：每个视频 clip 取 **16 帧 / 320×512**，**每条视频拼接 4 张图像**做联合训练。该机制让 base 模型同时具备 T2I 与 T2V 能力。
- **课程学习（curriculum learning）**：先用相对简单的 WebVid10M（配 LAION-5B），再逐步引入更复杂的 Vimeo25M 训练复杂场景/主体/运动。
- **各模块初始化**：base 由 SD 1.4 初始化；TI 由 base T2V 初始化；VSR 空间层由 SD-x4-upscaler 初始化并冻结，仅训时序层。
- TI/VSR 训练后期引入 Vimeo25M 的无水印视频以**去除插帧输出中的水印**。
- 蒸馏/步数加速：**未涉及**（论文未做 consistency / LCM / ADD 等加速；推理默认 50 步 DDPM）。
- 消融（Further Analysis）证明联合微调的必要性：① 整网在 WebVid10M 上微调 → 灾难性遗忘（"teddy bear" 概念逐渐消失）；② 只训时序模块、冻结其余 → 图像空间先验与新学时序信息难对齐、画质受损；③ 联合图像-视频微调 → 有效学到联合分布、画质最佳。

## Infra（训练 / 推理工程）
- **训练算力/GPU 数/GPU·时/并行策略/精度/吞吐：论文与官方 README 均未披露。** 这是该工作公开信息的一个明显缺口。
- 推理工程（来自官方 README）：四选项管线——
  - option1：仅 base，320×512 / 16 帧；
  - option2：base+插帧，320×512 / 61 帧；
  - option3：base+VSR，1280×2048 / 16 帧；
  - option4：全管线，1280×2048 / 61 帧。
  - 采样器支持 ddpm / ddim / eulerdiscrete；默认 `num_sampling_steps=50`、`guidance_scale=7.5`（README 示例用 7.0、seed=400、ddpm）。
- 代码基于 HuggingFace **diffusers** + Stable Diffusion 构建；权重托管 HF（`YaohuiW/LaVie`），另提供 HF Spaces / Replicate / OpenXLab 在线体验。
- 部署/量化/缓存等推理加速：未涉及。

## 评测 benchmark（把效果讲清楚）
**零样本 UCF101（FVD↓，I3D backbone，类名作 prompt，每类 100 样本共 10,100 个，16 帧 320×512）**

| 方法 | 图像预训练 | 图像生成器 | 分辨率 | FVD↓ |
|---|---|---|---|---|
| CogVideo (Chinese) | No | CogView | 480×480 | 751.34 |
| CogVideo (English) | No | CogView | 480×480 | 701.59 |
| Make-A-Video | No | DALL·E2 | 256×256 | **367.23** |
| VideoFusion | Yes | DALL·E2 | 256×256 | 639.90 |
| MagicVideo | Yes | SD | 256×256 | 699.00 |
| LVDM | Yes | SD | 256×256 | 641.80 |
| Video LDM | Yes | SD | 320×512 | 550.61 |
| **LaVie (Ours)** | Yes | SD | 320×512 | **526.30** |

- LaVie 超过除 Make-A-Video 外的所有基线；作者强调**同设定下**（基于 SD、直接用类名作 prompt）比 Video LDM 提升 **24.31**。Make-A-Video 用了更大的 WebVid10M+HD-VILA-100M 且为每类手工设计模板句，设定不完全可比。

**零样本 MSR-VTT（CLIPSIM↑，ViT-B-32，测试集每视频随机选 1 caption 共 2,990 个）**

| 方法 | Zero-Shot | CLIPSIM↑ |
|---|---|---|
| GODIVA | No | 0.2402 |
| NÜWA | No | 0.2439 |
| CogVideo (Chinese) | Yes | 0.2614 |
| CogVideo (English) | Yes | 0.2631 |
| Make-A-Video | Yes | **0.3049** |
| Video LDM | Yes | 0.2929 |
| ModelScope | Yes | 0.2930 |
| **LaVie (Ours)** | Yes | **0.2949** |

- LaVie 0.2949，优于/持平多数同期方法（高于 Video LDM、ModelScope），低于 Make-A-Video。

**人评（30 名评分员）**
- 整体画质偏好（成对比较）：LaVie > ModelScope **75.00%**；LaVie > VideoCrafter **75.58%**；ModelScope > VideoCrafter 59.10%。
- 五维细分（good 占比，LaVie vs 两基线）：在 motion smoothness、motion reasonableness、subject consistency、background consistency、face/body/hand quality 上整体领先；但**三方在 motion smoothness 上都不理想**，且 face/body/hand 质量普遍偏低（LaVie 的 face/body/hand "bad" 占 0.46），说明运动连贯性与手部生成仍是公共难题。

**消融结论**：联合图像-视频微调相比「整网视频微调」「只训时序模块」两种方案，在概念保持与画质上明显占优（图 9 定性对比）。

**附加能力**：① 长视频生成——把上一段末帧作为条件自回归递归生成，Fig.10 caption 称自回归 3 次把 2s 扩到 6s（每段 +2s，画质退化很小）；注意论文正文 §5.6 写作 "applied five times"，与图注 "three times" 存在内部不一致，此处采用与 2s→6s 自洽的图注口径；② 个性化 T2V——对空间层做 LoRA 微调（冻结时序模块），可生成特定角色（如 "Misaka Mikoto"）的视频。

## 创新点与影响
**核心贡献**
1. 验证「**最简时序自注意力 + RoPE**」即可把 T2I 模型升级为高质量 T2V，挑战了复杂时序模块的必要性；
2. 提出并系统验证「**图像-视频联合微调**」克服灾难性遗忘、实现图→视频知识迁移；
3. 设计「**base + 插帧 + 超分**」三级级联，达到 1280×2048 / 61 帧的 2K 长视频；
4. 贡献并开源 **Vimeo25M**（25M 高清无水印文本-视频对，VideoChat 自动打标 + PySceneDetect 切镜 + 美学过滤）填补当时高质量 T2V 数据缺口；
5. **代码 Apache-2.0**；**模型权重**对学术研究完全开放并**允许免费商用**（README 原文：weights "fully open for academic research and also allow free commercial usage"，商用许可需联系作者），是 2023 年开源 T2V 的标杆之一（Vchitect 体系主干）。

**影响**：成为后续开源 T2V/级联视频扩散工作的常被对比基线；Vimeo25M 的「网络视频→切镜→自动 caption→美学过滤」数据流水线是后续 T2V 数据构建的常见范式；图像-视频联合训练思路被广泛沿用。后续作者放出 LaVie-2（README 预告，本页未覆盖）。

**已知局限（论文明确）**
- **多主体生成**：>2 个主体时易混淆外观（"Einstein 与 Spiderman 讨论论文" 会糊在一起），归因于 CLIP 文本编码器，建议换 T5；
- **手部生成**：手指数量常出错，需更大更多样的人体视频数据；
- **运动连贯性**：motion smoothness 人评不理想，是当时所有方法的共性短板；
- **训练成本/算力细节未公开**，可复现性受限。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2309.15103
- arxiv_pdf: https://arxiv.org/pdf/2309.15103
- github: https://github.com/Vchitect/LaVie
- project_page: https://vchitect.github.io/LaVie-project/
- hf_weights: https://huggingface.co/YaohuiW/LaVie
- hf_space: https://huggingface.co/spaces/Vchitect/LaVie

## 一手源存档（sources/）
- [arxiv-2309.15103.pdf](https://arxiv.org/pdf/2309.15103)  （arXiv 原文 PDF，不入 git）
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/lavie--readme.md)
