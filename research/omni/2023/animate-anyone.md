---
title: "Animate Anyone: Consistent and Controllable Image-to-Video Synthesis for Character Animation"
org: "Alibaba (Institute for Intelligent Computing)"
country: China
date: "2023-11"
type: paper
category: video
tags: [character-animation, image-to-video, pose-guided, referencenet, diffusion, stable-diffusion, animatediff, human-video]
url: "https://arxiv.org/abs/2311.17117"
arxiv: "https://arxiv.org/abs/2311.17117"
pdf_url: "https://arxiv.org/pdf/2311.17117"
github_url: "https://github.com/HumanAIGC/AnimateAnyone"
hf_url: ""
modelscope_url: ""
project_url: "https://humanaigc.github.io/animate-anyone/"
downloaded: [arxiv-2311.17117.pdf, animate-anyone--readme.md, animate-anyone--project.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Animate Anyone 是阿里巴巴 Institute for Intelligent Computing（智能计算研究院）提出的**姿态驱动角色动画**框架：给定一张角色参考图 + 一段姿态骨架序列，生成与参考图外观高度一致、时序稳定的动画视频。核心创新是 **ReferenceNet**（一个与去噪 UNet 结构对称、共享 SD 权重的并行网络，通过 spatial-attention 把参考图细节注入主网络）。在 UBC fashion 数据集上 FVD 从前 SOTA 的 148.3 降到 **81.6**，TikTok 舞蹈数据集 FVD 从 225.5（SD-I2V 基线）降到 **171.9**，奠定了"参考图 + 姿态 → 一致动画"这条爆款技术路线。

## 背景与定位
角色动画（Character Animation）任务：把静态角色图按给定姿态序列驱动成真实视频，应用于电商、娱乐短视频、虚拟人等。早期 GAN 路线（FOMM、MRAA、TPSMM 等）存在局部扭曲、细节模糊、语义不一致、时序抖动等问题。

扩散模型时代的前置工作各有短板（本文 Related Works 逐一点名）：
- **DreamPose**（[[dreampose]]，扩展 [[stable-diffusion-1]]，用 adapter 融合 CLIP+VAE 特征）需对每个输入样本 finetune，效率低；
- **DisCo**（借鉴 [[controlnet]]，解耦 pose 与 background 控制，用 CLIP 注入角色特征）细节保持差、有帧间抖动；
- 通用 I2V 方法（[[animatediff]]、Gen-2、VideoComposer、VideoCrafter）多样性强但精度不足，难以捕捉角色精细细节，大动作下时序不稳定。

作者判断：当时**没有一种角色动画方法能同时做到泛化性与一致性**。Animate Anyone 的定位就是填这个空——继承 [[stable-diffusion-1]] 的网络设计与预训练权重，通过三个新增组件实现"任意角色 + 任意姿态 → 一致连续视频"。技术脉络上它站在 [[latent-diffusion-ldm]] → [[stable-diffusion-1]] → [[animatediff]]（时序层）+ [[controlnet]]（条件控制思想）的交叉点上。

## 模型架构
整体 pipeline（论文 Fig.2）：多帧噪声输入去噪 UNet；姿态序列经 Pose Guider 编码后与多帧噪声相加；ReferenceNet 提取参考图细节特征经 spatial-attention 注入；CLIP image encoder 提取参考图语义特征经 cross-attention 注入；时序层在 t 维度做 temporal-attention；最后 VAE decoder 解码成视频。

**Backbone（去噪 UNet）**：直接采用 SD 的 UNet 结构与 block 单元，继承 SD 训练权重，改造为接收多帧输入。一个典型 Res-Trans block 含三类计算：2D 卷积、self-attention、cross-attention。本文在其中插入了 spatial-attention 与 temporal-attention。

**ReferenceNet（核心创新）**：
- 与去噪 UNet **结构完全相同（去掉时序层）**，同样从 SD 权重初始化，但**权重独立更新**。
- 特征融合方式：把去噪 UNet 的 self-attention 层替换为 **spatial-attention**。具体——给定去噪 UNet 的特征图 x1∈R^(t×h×w×c) 和 ReferenceNet 的 x2∈R^(h×w×c)，先把 x2 沿时间维复制 t 份，再沿 **w 维（宽度）拼接**到 x1 上，做 self-attention 后**取前半部分**作为输出。
- 设计动机：① 复用 SD 预训练的图像特征建模能力，得到良好初始化；② 因 ReferenceNet 与去噪 UNet 结构、初始化权重一致，主网络可在**同一特征空间**里选择性学习相关特征，显著提升外观细节保持。
- 与 ControlNet 的区别：ControlNet 的控制信息（深度、边缘）与目标图**空间对齐**，而参考图与目标图空间相关但**不对齐**，因此 ControlNet 不适用（论文 4.4 消融实证）。
- 效率：ReferenceNet 参数量与去噪 UNet 相当，但在整个去噪过程中**只需提取一次特征**（去噪 UNet 对所有帧迭代多次去噪），推理开销增加不大。

**CLIP image encoder**：复用 SD 的 cross-attention 通道注入参考图**语义特征**，与文本编码器共享特征空间，作为有益初始化加速训练（CLIP 输入低分辨率 224×224，只提供高层语义，无法保细节——这正是单靠 CLIP 不够、需要 ReferenceNet 的原因）。

**Pose Guider（轻量姿态编码器）**：
- 不另起 ControlNet（去噪 UNet 需 finetune，加额外控制网代价大），改用轻量模块。
- 结构：4 层卷积（4×4 kernel，2×2 stride，通道 16/32/64/128），把姿态图对齐到噪声 latent 分辨率，**直接加到噪声 latent 上**再输入去噪 UNet。
- 初始化：高斯权重，最后投影层用 **zero convolution**。

**Temporal Layer（时序层）**：
- 设计灵感来自 [[animatediff]]，加在 Res-Trans block 的 spatial-attention + cross-attention 之后。
- 对特征图 x∈R^(b×t×h×w×c)，先 reshape 为 R^((b×h×w)×t×c)，沿 t 维做 self-attention（即 temporal-attention），结果经残差连接并入原特征。
- **只用在去噪 UNet**，ReferenceNet 不参与时序建模。
- 论文强调：因 Pose Guider 已提供连续姿态的可控性，时序层只需保证细节的时序平滑连续，**无需复杂运动建模**。

**分辨率**：训练阶段一帧 768×768；第二阶段 24 帧视频片段。

## 数据
- **规模**：从互联网收集 **5K 条角色视频片段**（internal dataset），用于训练通用模型。
- **姿态标注**：用 **DWPose** 提取角色姿态序列（含身体与手部），按 **OpenPose** 格式渲染成姿态骨架图。
- **配比/清洗/re-captioning**：论文**未披露**数据清洗、过滤、美学/安全过滤、配比细节。该方法不依赖文本 caption（条件是参考图 + 姿态骨架，而非文本）。
- **基准对比用数据**：为与各 SOTA 公平比较，另在三个公开数据集上**单独训练**（不加额外数据）：UBC fashion video、TikTok、Ted-talk。

## 训练方法
**训练目标**：标准 LDM/SD 的噪声预测 diffusion 目标 —— L = E[‖ε − ε_θ(z_t, c, t)‖²]，在 latent 空间去噪。**未使用** flow matching / rectified flow，也无偏好对齐（RLHF/DPO）或蒸馏加速。

**两阶段训练（关键 trick）**：
- **阶段一（单帧图像训练）**：去噪 UNet **暂时去掉时序层**，输入单帧噪声；同时训练去噪 UNet、ReferenceNet、Pose Guider。参考图从整段视频片段中**随机选取**。去噪 UNet 与 ReferenceNet 从 SD 预训练权重初始化；Pose Guider 高斯初始化（末层 zero conv）；VAE Encoder/Decoder、CLIP image encoder **全程冻结**。目标：在给定参考图 + 目标姿态下生成高质量动画图像。
- **阶段二（视频时序训练）**：把时序层加入已训练模型，用 [[animatediff]] 预训练权重初始化时序层；输入 **24 帧视频片段**；**只训练时序层，冻结网络其余部分**。

**关键超参（通用模型，4×A100）**：
- 阶段一：分辨率 768×768（resize + center-crop），训练 **30,000 步**，batch size **64**；
- 阶段二：24 帧序列，训练 **10,000 步**，batch size **4**；
- 两阶段学习率均为 **1e-5**。

**两阶段训练的作用**（消融 Tab.6）：若不分阶段直接端到端训练，图像质量指标下降——因为多帧同时优化时网络更关注整体时序连贯性，削弱了对单帧细节的关注。两阶段可同时保证单帧质量与时序平滑。

## Infra（训练 / 推理工程）
- **算力**：实验在 **4 张 NVIDIA A100** 上进行（论文仅此一句，未报告总 GPU·时、并行/分布式策略、混合精度细节、吞吐）。
- **推理**：
  - 把驱动姿态骨架的长度**重缩放**到接近参考图中角色骨架的长度，再用 **DDIM sampler 做 20 步去噪**。
  - 长视频生成：采用 EDGE [43] 的 **temporal aggregation**（时序聚合）方法，把不同 batch 的结果拼接成长视频。
  - ReferenceNet 特征只算一次（见架构节），降低推理成本。
- **生产侧加速（项目页披露，非论文）**：阿里云用 **DeepGPU（AIACC）** 替代原始 pytorch + xformers 方案为 Animate Anyone 推理加速，质量无损、为终端用户减少约 30% 等待时间。给出的具体数字：32 帧 832×640 视频单步生成耗时，在 **A10** 上从 2.45s 降到 1.75s（约 40% 提升），在 **RTX6000** 上从 2.8s 降到 2.25s（约 25% 提升）。
- **未做**步数蒸馏 / consistency / LCM / 量化等加速；论文在 Limitations 中明确：因使用 DDPM，运行效率低于非扩散方法。
- **部署/开源**：官方 GitHub 仓库 `HumanAIGC/AnimateAnyone` 截至落盘时**仅含 README + 引用信息，未释放训练/推理代码与权重**（README 引导到项目页与后续开源工作 Wan-Animate）。社区有多个第三方复现（如 Moore-AnimateAnyone），但非官方。

## 评测 benchmark（把效果讲清楚）
评测指标：图像级 **SSIM↑ / PSNR↑ / LPIPS↓**，视频级 **FVD↓**。自建强基线 **SD-I2V**（组合 SD + ControlNet + IP-Adapter + AnimateDiff）。

**① 时装视频合成（UBC fashion，Tab.1）**：

| 方法 | SSIM↑ | PSNR↑ | LPIPS↓ | FVD↓ |
|---|---|---|---|---|
| MRAA | 0.749 | — | 0.212 | 253.6 |
| TPSMM | 0.746 | — | 0.213 | 247.5 |
| BDMM | 0.918 | 24.07 | 0.048 | 148.3 |
| DreamPose | 0.885 | — | 0.068 | 238.7 |
| DreamPose*（无样本 finetune） | 0.879 | 34.75 | 0.111 | 279.6 |
| SD-I2V | 0.894 | 36.01 | 0.095 | 175.4 |
| **Ours** | **0.931** | **38.49** | **0.044** | **81.6** |

视频指标 FVD 大幅领先（81.6 vs 次优 BDMM 148.3，约 **−45%**）。

**② 人体舞蹈生成（TikTok，Tab.2）**：

| 方法 | SSIM↑ | PSNR↑ | LPIPS↓ | FVD↓ |
|---|---|---|---|---|
| FOMM | 0.648 | 29.01 | 0.335 | 405.2 |
| MRAA | 0.672 | 29.39 | 0.296 | 284.8 |
| TPSMM | 0.673 | 29.18 | 0.299 | 306.1 |
| DisCo | 0.668 | 29.03 | 0.292 | 292.8 |
| SD-I2V | 0.670 | 29.11 | 0.295 | 225.5 |
| **Ours** | **0.718** | **29.56** | **0.285** | **171.9** |

值得注意：DisCo 用了大量图像对做人体属性预训练，而本文**仅在 TikTok 上训练**就反超 DisCo。

**③ 说话手势生成（Ted-talk，Tab.3）**：

| 方法 | SSIM↑ | PSNR↑ | LPIPS↓ | FVD↓ |
|---|---|---|---|---|
| MRAA | 0.826 | 33.86 | 0.160 | 82.8 |
| TPSMM | 0.830 | 33.81 | 0.157 | 80.7 |
| DisCo | 0.754 | 31.25 | 0.193 | 223.5 |
| SD-I2V | 0.773 | 32.11 | 0.179 | 158.3 |
| **Ours** | **0.832** | **33.91** | **0.159** | **80.5** |

注意：MRAA/TPSMM 用 **GT 图像作驱动信号**（视频重建任务），本文**仅用姿态信息**即取得相当或更好结果；在更复杂的 UBC/TikTok 上 MRAA/TPSMM 远落后。

**④ 通用 I2V 对比**：与 AnimateDiff、Gen-2 比（二者无姿态控制，只比外观保真度），定性显示通用 I2V 难以生成大幅角色运动、难保长时外观一致（论文 Fig.7）。

**关键消融**：
- **图像条件建模（Tab.4，UBC）**：仅 CLIP（FVD 208.5）/ ControlNet（213.9）/ CLIP+ControlNet（205.4）均远差于 ReferenceNet（**81.6**）。证明 ControlNet 因缺空间对应性不适用，单 CLIP 保不住细节。
- **ReferenceNet 设计（Tab.5，UBC）**：用 ResNet(ImageNet 权重)替 UNet → FVD 165.4；用 feature-concat 替 spatial-attention → 132.8；本文 → **81.6**。证明必须用 SD 权重 + spatial-attention。
- **时序建模（Tab.6，UBC）**：去掉时序层 FVD 176.7（出现纹理粘连、帧间抖动）；不用两阶段训练 FVD 89.3（图像质量指标下降）；完整方案 **81.6**。

## 创新点与影响
**核心贡献**：
1. **ReferenceNet** —— 用一个与主 UNet 对称、共享 SD 初始化的并行网络，经 **spatial-attention（宽度维拼接 + 取半）** 注入参考图细节，在"参考图与目标空间相关但不对齐"的场景下做到了 ControlNet 做不到的外观细节一致性保持。这是本文最有影响力的设计，被后续大量角色/人物动画工作沿用。
2. **轻量 Pose Guider** —— 4 层卷积 + zero conv，直接加到 latent，避免另起 ControlNet 的开销。
3. **两阶段训练**（先单帧学外观/姿态，再固定主体只学 AnimateDiff 时序层）—— 兼顾单帧细节质量与时序平滑。
4. 在通用 5K 数据上训练即可泛化到**任意角色**（真人全身/半身、卡通、拟人形象），并在三大人体视频基准上刷 SOTA。

**影响**：
- 2023 年底发布后因 demo 效果惊艳成为**现象级爆款**，奠定"reference image + pose sequence → 一致动画"的主流范式；ReferenceNet 思路被 MagicAnimate、Champ、MimicMotion、UniAnimate 等一系列后续工作借鉴或对比。
- 催生大量第三方开源复现（如 Moore-AnimateAnyone）；官方因未放代码/权重，社区复现一度是主要使用入口。
- 是阿里 HumanAIGC 系列工作（项目页关联 OutfitAnyone、VividTalk）的一员，README 明确指向后续开源工作 **Wan-Animate**（基于 [[wan]] 的角色动画）。

**已知局限（论文 Discussion）**：
1. **手部运动**易失稳，出现扭曲与运动模糊；
2. 参考图只提供单视角信息，角色运动中**未见部分（遮挡/背面）**的生成是 ill-posed 问题，存在潜在不稳定；
3. 基于 DDPM，**推理效率低于**非扩散方法。
4. 潜在滥用风险：可被用于制造伪造人物视频（论文提及可用 face anti-spoofing 检测）。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2311.17117
- arxiv_pdf: https://arxiv.org/pdf/2311.17117
- project_page: https://humanaigc.github.io/animate-anyone/
- github: https://github.com/HumanAIGC/AnimateAnyone （仅 README，未开源代码/权重）

## 本地落盘文件
- ../../../sources/omni/2023/arxiv-2311.17117.pdf
- ../../../sources/omni/2023/animate-anyone--project.md
- ../../../sources/omni/2023/animate-anyone--readme.md
