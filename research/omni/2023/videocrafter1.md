---
title: "VideoCrafter1: Open Diffusion Models for High-Quality Video Generation"
org: "Tencent AI Lab"
country: China
date: "2023-10"
type: tech-report
category: video
tags: [video, t2v, i2v, diffusion, lvdm, open-source, unet]
url: "https://arxiv.org/abs/2310.19512"
arxiv: "https://arxiv.org/abs/2310.19512"
pdf_url: "https://arxiv.org/pdf/2310.19512"
github_url: "https://github.com/AILab-CVC/VideoCrafter"
hf_url: "https://huggingface.co/VideoCrafter/Text2Video-1024"
modelscope_url: ""
project_url: "https://ailab-cvc.github.io/videocrafter"
downloaded: [arxiv-2310.19512.pdf, videocrafter1--readme.md]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
VideoCrafter1 是腾讯 AI Lab 2023 年 10 月开源的一对视频扩散模型——一个文生视频（T2V）和一个图生视频（I2V）。T2V 基于 SD 2.1 通过插入时序注意力扩展为 3D U-Net，能生成 1024×576、2 秒、电影质感的视频，是当时开源 T2V 里画质最强的；I2V 则是**首个开源的、能严格保持输入参考图内容与结构**的通用图生视频基座模型。

## 背景与定位
2023 年的视频生成处境是：商用产品（Runway Gen-2、Pika Labs、Moonvalley）效果好但闭源，研究者无法触及；开源侧只有少数模型且质量都不理想——ModelScope 只能出 256×256 且画质差，Zeroscope V2 XL 有闪烁和噪点，Hotshot-XL 只能出 8 帧 512×512 的 GIF，AnimateDiff 原生 T2V 效果很差、强依赖外接高质量 LoRA 才能出好结果且被 LoRA 的风格/概念组合能力限制。论文明确指出"开源社区仍缺一个能产出高分辨率高质量视频的通用 T2V 基座模型"。

I2V 一侧更空白：当时唯一的开源通用 I2V 基座是 ModelScope 上的 I2VGen-XL，它用 image embedding 替换 text embedding 去微调一个预训练 T2V，结果只能对齐图像的语义、**不能严格遵循参考图的内容与结构**。VideoCrafter1 正是冲着这两个缺口去的：开源一个高画质 T2V + 一个内容保持的 I2V。

技术脉络上 VideoCrafter1 属于 [[latent-diffusion-ldm]] / Stable Diffusion 一系的"SD 加时序层扩展为视频"路线（同期 [[modelscope-t2v]]、Align-your-Latents、MagicVideo、LVDM 都走这条路），直接构建在自家的 LVDM（Latent Video Diffusion Model）框架上，并复用 SD 的 VAE 与 [[ddpm]] 式扩散过程。它是后续 VideoCrafter2（2024-01，用有限数据克服 WebVid 水印/低质问题）和专用高分 I2V 模型 DynamiCrafter 的前身。

## 模型架构
**整体（T2V）**：一个 Latent Video Diffusion Model（LVDM），两大组件：

- **Video VAE**：直接复用 Stable Diffusion 的预训练图像 VAE，**逐帧独立**编码/解码，不抽取时序信息。视频 x0 经 encoder E 压成视频 latent z0（降维），扩散过程在 z0 上做，最后由 decoder D 解回像素视频。
- **Denoising 3D U-Net**：在 SD 2.1 的 U-Net 基础上插入时序层。由若干"空间-时序块 + 跳连"堆叠组成，每个块含：卷积层、**空间 transformer（ST）** 和 **时序 transformer（TT）**。
  - ST = Proj_in ∘ (Attn_self ∘ Attn_cross ∘ MLP) ∘ Proj_out —— 空间自注意力 + 与文本的交叉注意力。
  - TT = Proj_in ∘ (Attn_temp ∘ Attn_temp ∘ MLP) ∘ Proj_out —— 沿时间维做注意力，保证帧间一致性。
  - 空间参数继承自预训练 SD U-Net，时序层是新增训练。

**条件注入**：
- **文本语义控制**：用 CLIP 文本编码器 ϕ(y) 得到文本 embedding，经交叉注意力注入空间 transformer（Q 来自 video latent token，K/V 来自文本）。
- **运动速度控制（FPS）**：把视频 fps 作为条件。FPS embedder 与 timestep embedder 同构——fps 或 timestep 经正弦编码后过两层 MLP 映成可学习 embedding，timestep embedding 与 fps embedding 逐元素相加，再加到卷积特征上调制中间特征。

**I2V 的额外设计——文本对齐的富图像 embedding + 双交叉注意力**：
- 目标是把图像投影到一个与文本对齐的 embedding 空间，让 T2V backbone 能兼容地吃图像信息。
- 用 CLIP 的**图像编码器**抽特征。关键选择：不用全局语义 token f_cls（它语义层面与 caption 对齐但细节弱），而是取 CLIP image ViT 最后一层的**全部 patch 视觉 token** F_vis = {f_i}（包含远更丰富的图像细节）。
- 一个可学习的**投影网络 P** 把 F_vis 变换成目标图像 embedding F_img = P(F_vis)。
- backbone 中间特征 F_in 通过**双交叉注意力**同时融合文本与图像 embedding：F_out = Softmax(QK_text^⊤/√d)·V_text + Softmax(QK_img^⊤/√d)·V_img。**图像交叉注意力复用与文本相同的 Q**，因此每层只新增 W_k′、W_v′ 两个参数矩阵，开销很小。论文用 Fig.5 对比证明：用富 patch token 比只用全局语义 token 的视觉保真度明显更高。

**分辨率/时长**：T2V 出 1024×576、2 秒；当时仓库实际放出的权重有 T2V 576×1024 与 320×512、I2V 320×512（后续才有 640×1024 的 DynamiCrafter）。参数量论文未单独披露（backbone 量级约等于 SD 2.1 U-Net 加时序层）。

## 数据
**图文+视频联合训练策略**（防止只用视频训练导致的概念遗忘 concept forgetting）：

- **图像集**：LAION-COCO（论文记为 LAION COCO 600M）——论文原文只说"约 6 亿张公开网络图片配 generated high-quality captions"，未点名 caption 生成模型（LAION-COCO 项目自述用 BLIP+CLIP 生成，此为外部信息，非本论文披露）。
- **视频集**：
  - 公开的 **WebVid-10M**（约 1000 万条带文本描述的短视频，来自素材网站，内容多样）。
  - 自采的**高质量高分辨率视频集：1000 万条、分辨率均大于 1280×720**，专门用于 T2V 训练。
- 论文给出的总量口径：T2V 在 **2000 万视频 + 6 亿图像**上训练。
- **I2V**：在 LAION-COCO 600M + WebVid-10M 上训练。
- 清洗/过滤/美学打分/re-captioning 等更细的数据处理流程：**论文未披露**（WebVid 本身带水印的问题在 VideoCrafter1 未专门处理，正是后续 VideoCrafter2 要解决的痛点）。

## 训练方法
**训练目标**：标准 latent 扩散去噪（DDPM 式，在 SD VAE latent 空间），U-Net 预测噪声；具体 v-prediction 与否论文未明确写（沿用 SD 训练方式）。

**T2V——低分辨率到高分辨率的渐进式课程训练**（沿用 Stable Diffusion 的 low→high 策略）：
1. 从图像模型扩展出的视频模型起步，在 **256×256** 训练 **80K** 步，batch size **256**。
2. 从 256×256 续训，用视频在 **512×320** 微调 **136K** 步，batch size **128**。
3. 再在 **1024×576** 微调 **45K** 步，batch size **64**。

**I2V——两阶段**：
1. 先单独训练"图像 embedding → 交叉注意力 embedding 空间"的映射（即 I2V 新增的投影网络 P 与图像交叉注意力参数）。
2. 固定文本与图像两套 embedding 的映射，微调视频模型本体以提升对齐。

**蒸馏/步数加速/偏好对齐（RLHF/DPO/consistency 等）**：VideoCrafter1 本身**未涉及**，论文无相关内容。

## Infra（训练 / 推理工程）
论文**未披露**任何训练算力规模、GPU 数量与卡时、并行/分布式策略、混合精度或吞吐细节，也未给推理加速（步数蒸馏、量化、缓存）方案。仅从训练配置可反推：三阶段 batch size 256/128/64、总迭代约 80K+136K+45K≈261K 步，是当时学界/产业可承受量级的训练，但**具体硬件未报告**。

部署形态：开源 PyTorch 推理代码 + HF 上的 checkpoint；作者另把两个模型部署到名为 **Floor33** 的 Discord 频道供用户在线体验（含一个可选的 prompt extension 功能丰富用户提示词）。

## 评测 benchmark（把效果讲清楚）
评测用自家的 **EvalCrafter** 基准（一个评估大型视频生成模型的 benchmark），结合定量指标与用户研究，对比对象为 Gen-2、Pika Labs、ModelScope、I2VGen-XL、Zeroscope 等。

**人类偏好对齐的四维评分（Table 1，分数越高越好；模型名带 * 者为闭源——仅 PikaLab/Gen2；I2VGen-XL 名后的 † 是论文原表标记但 caption 未解释其含义）**——表里同时列了 VideoCrafter 自己 23.04/23.08/23.10 三个迭代版本，可见逐版本提升（原表 VideoCrafter23.04 的 Motion Quality 印作 "56.24*"，此 * 系单元格脚注/排版痕迹，与"闭源"标记无关，此处去掉）：

| 模型 | Visual Quality | Text-Video Alignment | Motion Quality | Temporal Consistency |
|---|---|---|---|---|
| I2VGen-XL† | 55.23 | 47.22 | 59.41 | 59.31 |
| ZeroScope | 56.37 | 46.18 | 54.26 | 61.19 |
| PikaLab* | 63.52 | 54.11 | 57.74 | 69.35 |
| Gen2* | 67.35 | 52.30 | 62.53 | 69.71 |
| VideoCrafter 23.04 | 46.88 | 41.56 | 56.24 | 55.78 |
| VideoCrafter 23.08 | 59.53 | 51.29 | 51.97 | 56.36 |
| VideoCrafter 23.10 | 61.64 | 66.76 | 56.06 | 60.36 |

关键读数：
- 在**开源模型**中，VideoCrafter 23.10 的 Visual Quality（61.64）与 Text-Video Alignment（66.76）均为最佳——尤其文本-视频对齐分数 66.76 **超过所有对比模型（含闭源 Gen-2/Pika）**。
- 相比闭源 Gen-2、Pika，VideoCrafter 在 Visual Quality 与 Temporal Consistency 上仍有差距（Gen-2 67.35 / 69.71 更高），但作者称最新 23.10 版"已达到与 Pika Lab 相当的质量"。
- 自家三版本对比（23.04→23.08→23.10）四个维度大体单调上升，作者归因于训练方法与数据的改进。

**定性结论与消融**：
- T2V：训练时鼓励大物体运动 → 生成视频运动幅度比其他模型大，但大运动有时会牺牲时序一致性。在概念组合（concept composition）上优于开源模型；Zeroscope 画质差、会出重复网格伪影；Gen-2 偶尔概念组合失败且过度平滑；Pika 文本对齐最好但风格常不对。
- I2V 消融（Fig.5）：用 CLIP 全部 patch 视觉 token 比只用全局语义 token，视觉保真度明显更好——这是 I2V 设计的核心实验依据。
- I2V 对比：相比 VideoComposer（首帧像但后续帧外观漂移、时序严重不一致）和 I2VGen-XL（时序好但外观偏离参考图），VideoCrafter1 在时序一致性与运动幅度上更平衡、视觉保真"可接受"；Pika 保真和一致性最好但运动幅度极小，Gen-2 运动好但不稳定（如车的例子会时序漂移）。

注：FID / CLIPScore / VBench 等单点数值论文**未报告**（VideoCrafter1 早于 VBench 流行，主要靠 EvalCrafter 的人评维度评分与用户研究）。

## 创新点与影响
**核心贡献**：
1. 开源了当时画质最强的通用 T2V 基座（1024×576、电影质感），训练于 2000 万视频 + 6 亿图像，填补"开源缺高分辨率高质量 T2V 基座"的空白。
2. 提出并开源**首个内容保持的通用 I2V 基座**——用 CLIP 全 patch 视觉 token + 可学习投影网络 + 复用 Q 的双交叉注意力，以极小新增参数实现严格遵循参考图内容/结构的图生视频，解决了 I2VGen-XL"只对齐语义不保内容"的问题。

**影响**：成为开源视频生成的代表作之一，直接催生 VideoCrafter2（用有限/低质数据训练出更好运动与概念组合）和专用高分 I2V 模型 DynamiCrafter（640×1024、更强动态与连贯性）；其"SD+时序层+图文联合训练+分辨率课程"的配方被后续大量开源视频工作沿用；双交叉注意力的图像条件注入思路与 IP-Adapter 一脉相承，影响了后续 I2V/条件视频生成设计。

**已知局限**（作者自陈）：
- 时长仅 2 秒（受训练帧数限制），需更多帧训练 + 帧插值模型来延长。
- 分辨率上限 1024×576，进一步提升需空间超分模块或配合 ScaleCrafter。
- 运动与画质受数据质量制约（WebVid 等），更高质量数据可改善——这正是 VideoCrafter2 的切入点。
- I2V 仍有成功率不稳、面部伪影等问题。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2310.19512
- arxiv_pdf: https://arxiv.org/pdf/2310.19512
- github: https://github.com/AILab-CVC/VideoCrafter
- project_page: https://ailab-cvc.github.io/videocrafter
- hf_t2v_1024: https://huggingface.co/VideoCrafter/Text2Video-1024
- hf_t2v_512: https://huggingface.co/VideoCrafter/Text2Video-512
- hf_i2v_512: https://huggingface.co/VideoCrafter/Image2Video-512

## 本地落盘文件
- ../../../sources/omni/2023/arxiv-2310.19512.pdf
- ../../../sources/omni/2023/videocrafter1--readme.md
