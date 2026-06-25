---
title: "MagicAnimate: Temporally Consistent Human Image Animation using Diffusion Model"
org: "Show Lab (NUS) / ByteDance"
country: China
date: "2023-11"
type: paper
category: video
tags: [human-animation, pose-driven, densepose, appearance-encoder, temporal-attention, video-diffusion, controlnet, sd15]
url: "https://arxiv.org/abs/2311.16498"
arxiv: "https://arxiv.org/abs/2311.16498"
pdf_url: "https://arxiv.org/pdf/2311.16498"
github_url: "https://github.com/magic-research/magic-animate"
hf_url: "https://huggingface.co/zcxu-eric/MagicAnimate"
modelscope_url: ""
project_url: "https://showlab.github.io/magicanimate/"
downloaded: [arxiv-2311.16498.pdf, magicanimate--preprint.pdf, magicanimate--readme.md, magicanimate--project-page.md, magicanimate--hf-modelcard.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
MagicAnimate 是一个基于 Stable Diffusion 1.5 的**人体图像动画**框架：给一张参考人像 + 一段 **DensePose** 驱动序列，生成时间一致的跳舞/动作视频。核心创新是 **(1) 一个全 UNet 拷贝的 appearance encoder（密集外观条件，替代 CLIP/IP-Adapter）+ (2) 时间注意力的 video diffusion + (3) 推理时滑窗视频融合**。在 TikTok 数据集上视频保真度（FVD）相对最强 baseline（DisCo）提升 **38.8%**，FID-VID 提升 **63.7%**。与 [[animate-anyone]] 同期，是 2023 年末「图驱动人物视频」两大代表作之一。

## 背景与定位
人体图像动画（human image animation）目标：把静态参考图按给定运动信号「动起来」。在 MagicAnimate 之前，主流分两类：
- **GAN-based warping**（FOMM、MRAA、TPS）：估计光流把参考图扭曲到目标姿态，再用 GAN 补全遮挡区域。问题：运动迁移能力受限，跨身份/大姿态变化时遮挡区域出现不真实细节，泛化差。
- **Diffusion-based**（DisCo、DreamPose）：基于 Stable Diffusion + ControlNet 条件于 OpenPose 关键点序列，用 **CLIP** 编码参考外观。两大问题：(a) **逐帧独立生成**，缺乏时序建模 → 闪烁；(b) CLIP 语义级特征太稀疏/紧凑，无法保留身份、衣着、背景的精细细节。

MagicAnimate 三处针对性改进：把 2D 图扩散 inflate 成 **3D 时序 UNet** 解决闪烁；用**密集外观编码器**替代 CLIP 解决细节丢失；用**推理时融合**支持任意长视频。技术脉络上属于 [[latent-diffusion-ldm]] → [[controlnet]] → [[animatediff]]（时序模块思路）一系，外观注入借鉴了 MasaCtrl / Reference-only ControlNet 的 self-attention 共享思想。与同月发布的 [[animate-anyone]]（阿里）形成对照：两者都用「参考网络 + 时序层 + 姿态控制」范式，但 MagicAnimate 用 **DensePose**（稠密表面）做姿态信号、Animate Anyone 用 **OpenPose 骨架**；外观注入方式也不同。

## 模型架构
整体是 **SD1.5 latent diffusion** + 三个并行条件分支，全部在 8× 下采样的 latent 空间（512×512 图 → 64×64 latent，VAE 用 stabilityai `sd-vae-ft-mse`）。

- **Backbone（去噪网络）**：把原始 2D SD1.5 UNet **inflate 成 3D 时序 UNet** `F_T(·;θ_T)`，方式是在 UNet block 中插入**时间注意力层**（AnimateDiff/Tune-a-Video 风格的 motion module）。特征张量在 `[N×C×K×H×W]`（K=帧数）和 `[(N·H·W)×K×C]`（时间维）之间 reshape；时间维加**正弦位置编码**后做标准自注意力，聚合相邻帧信息。仓库实测 motion module 即 `temporal_attention.ckpt`，段长 **K=16 帧**。

- **Appearance Encoder `F_a`（核心创新）**：**再复制一份 base UNet**（`θ_a`，可训练；HF config 显示 `block_out=[320,640,1280,1280]`、`sample_size=64`、`cross_attention_dim=768`，即与 SD1.5 UNet 同构）。它对参考图 `I_ref` 在每个去噪步 t 计算条件特征 `y_a = F_a(z_t | I_ref, t, θ_a)`，`y_a` 是 middle/upsampling block 的一组归一化注意力隐状态。注入方式区别于 ControlNet 的「残差相加」：把 `y_a` **拼接进 UNet 的空间自注意力**——`K=W_K[z_t, y_a]`、`V=W_V[z_t, y_a]`（Q 仍只来自 `z_t`），形成「混合注意力」，让去噪过程能**从参考图 query 内容**（身份、衣着、配饰、背景）。这是相对 CLIP/IP-Adapter「语义 token 经 cross-attention」的根本差异，提供**密集像素级外观条件**。

- **Pose ControlNet `F_p`**：标准 ControlNet（HF config `_class_name=ControlNetModel`、`conditioning_channels=3`、`cross_attention_dim=768`），条件信号是 **DensePose**（而非 OpenPose 关键点）。论文论点：主要身体关键点稀疏、对旋转等运动不鲁棒；DensePose 提供稠密、鲁棒的姿态条件。`y_{p,i}=F_p(z_t|p_i,t,θ_p)`，作为残差加到 UNet 的 middle/upsampling block。

- **Text encoder**：沿用 SD1.5 的 CLIP text encoder（`cross_attention_dim=768`），但动画任务以图像条件为主，文本主要在「结合 T2I（DALL·E3）生成参考图」等下游应用中体现。

- **参数量 / 分辨率**：论文未明确给出总参数量；按结构推断约「3× SD1.5 UNet（去噪+外观+ControlNet 分支）」量级，**论文未披露精确数字**。分辨率 **512×512**（latent 64×64），段长 16 帧。

## 数据
- **训练数据集**：
  - **TikTok**（Jafarian & Park, CVPR'21）：350 段跳舞视频。与 DisCo 用**同一测试集**做公平对比。
  - **TED-talks**（MRAA/Siarohin'21）：1,203 段从 YouTube TED 演讲剪辑的视频，按官方 train/test split。
  - **大规模图像数据集**：image-video 联合训练阶段从 **LAION-400M**（Schuhmann'21，论文引用 [25]）采样人像图像做增广。
- **数据预处理 / 标注**：所有数据集走同一预处理流水线；驱动信号统一用 **DensePose**（论文为 MRAA/TPS 也训了 DensePose 版本以公平对比）。论文正文写"详见补充材料"，但 **arXiv v1 与仓库 preprint PDF 均不含补充材料**，故具体清洗、分辨率裁剪、DensePose 抽取细节**未能从一手 PDF 获取**。
- **配比**：image-video 联合训练用概率阈值控制图/视频采样比例——阶段一阈值 `τ0`、阶段二阈值 `τ1`/`τ2`（论文给出机制但**未披露具体数值**，应在缺失的补充材料中）。
- 无合成数据、无安全/美学过滤的专门描述（此为偏研究的人物动画工作，非通用 T2I 大模型）。

## 训练方法
**多阶段训练 + image-video 联合训练**，训练目标是标准 DDPM **ε-prediction（噪声预测 L2 损失）**，非 flow matching。

- **阶段一（外观与姿态）**：**冻结/省略时间注意力层**，只训 appearance encoder `F_a(θ_a)` + pose ControlNet `F_p(θ_p)`。损失 `L1 = E[‖ε − ε_θ‖²]`，`p_i` 取目标帧 `I_i` 的 DensePose。此阶段引入 **image-video 联合训练**：以概率 `τ0` 从 LAION 采单帧人像，此时条件 pose `p_i` 从 `I_ref` 自身估计，目标退化为**重建**（让外观编码器学到强参考保真）。
- **阶段二（时序）**：**只训时间注意力层** `F_T(θ_T)`，其余冻结。损失 `L2 = E[‖ε^{1:K} − ε_θ^{1:K}‖²]`（在 K 帧段上）。同样用联合训练缓解「加入时序后单帧质量下降」：按 `r∼U(0,1)` 与 `τ1,τ2` 比较，`r≤τ1` 用图像数据（pose=ref，做重建）、`τ1<r≤τ2` 用图像但 pose≠ref、`r>τ2` 用视频数据。
- **去噪条件公式**：`ε_θ^{1:K}(z_t^{1:K}, t, I_ref, p^{1:K}) = F_T(z_t^{1:K} | t, y_a, y_p^{1:K})`，可训练参数集合 `θ = {θ_T, θ_a, θ_p}`。
- **基座 / 初始化**：base model 为 **runwayml/stable-diffusion-v1-5** + **sd-vae-ft-mse**（MSE-finetuned VAE）；时序模块为 AnimateDiff 风格 motion module（仓库 `temporal_attention.ckpt`）。
- **蒸馏 / 加速**：**无**步数蒸馏 / consistency / LCM；走标准多步去噪。
- **关键超参（学习率、batch、训练步数、warmup）**：论文正文未给，应在缺失补充材料中——**未能获取**。

## Infra（训练 / 推理工程）
- **训练算力 / GPU 数 / GPU·时 / 并行策略 / 混合精度 / 吞吐**：论文正文与官方发布均**未披露**（应在缺失的补充材料）。**未能获取**。
- **推理工程**（来自官方仓库一手配置 `configs/prompts/animation.yaml`）：
  - 分辨率 **512×512**；段长 **L=16 帧**；采样 **steps=25**；**CFG guidance_scale=7.5**；`fusion_blocks="midup"`（外观特征注入 middle+up block）。
  - **显存约束下分段处理**：整段视频因显存无法一次生成，按段（K=16）逐段去噪。
  - **长视频推理 = 滑窗 + overlap 平均（核心工程 trick，见下）**。
  - 提供**单卡 / 多卡分布式推理**脚本（`animate.sh` / `animate_dist.sh`），及 Gradio demo（单卡/多卡）。
  - 量化 / 缓存 / 蒸馏：**无**。
- **长视频融合（video fusion）**：把长运动序列切成有重叠的段 `{z^{1:K}, z^{K−s+1:2K−s}, ...}`，重叠步长 `s<K`；**所有段共享同一初始噪声 `z^{1:K}`**（实测能提升画质）；每个去噪步 t 对各段预测的 `ε_θ^{1:K}`，在重叠帧上**简单平均**合并成 `ε_θ^{1:N}`，t=0 得到整段视频。这是「surprisingly simple」的零训练成本推理技巧。

## 评测 benchmark（把效果讲清楚）
两套基准：**TikTok**（单帧质量 + 视频保真）、**TED-talks**。指标：单帧 L1/PSNR/SSIM/LPIPS/FID；视频 FID-VID(FID-FVD)/FVD；TED 额外 AKD/MKR/AED。下列数字均来自已抓取的论文 PDF（Table 1/2）。

**TikTok（Table 1a，↓越低越好除 PSNR/SSIM）：**

| 方法 | L1↓ | PSNR↑ | SSIM↑ | LPIPS↓ | FID↓ | FID-VID↓ | FVD↓ |
|---|---|---|---|---|---|---|---|
| IPA+CtrlN | 7.38e-4 | 28.03 | 0.459 | 0.481 | 69.83 | 113.31 | 802.44 |
| IPA+CtrlN-V | 6.99e-4 | 28.00 | 0.479 | 0.461 | 66.81 | 86.33 | 666.27 |
| **DisCo**（最强 baseline） | 3.78e-4 | 29.03 | 0.668 | 0.292 | **30.75** | 59.90 | 292.80 |
| **MagicAnimate** | **3.13e-4** | **29.16** | **0.714** | **0.239** | 32.09 | **21.75** | **179.07** |

- 相对 DisCo：**SSIM +6.9%、LPIPS +18.2%、FID-VID +63.7%、FVD +38.8%**（FVD 292.80→179.07）。
- 唯一不占优的是 **FID**（32.09 vs DisCo 30.75）——单帧 FID 略逊，但视频级指标全面领先。

**TED-talks（Table 1b）：** MagicAnimate 取得最佳 **FID=22.78、FID-VID=19.00、FVD=131.51**，FVD 相对次优 MRAA(182.78) 提升 **28.1%**；AKD=2.65、MKR=0.013、AED=0.204 均最优（身份保持 + 运动精度最佳）。**局限**：整体 L1 误差(2.92e-4)高于 baseline，因 DensePose 不含背景信息、模型学不到 TED 的动态背景；但**前景人体区域 L1(1.11e-4)** 与最强 baseline MRAA(1.07e-4) 持平。

**消融（Table 2，TikTok）：**
- **(a) 时间注意力**：去掉后 FVD 247.30→179.07（加上时序）、FID-VID 42.21→21.75 大幅改善（时序建模显著去闪烁）。注：去时序时 FID 略低(27.54)，说明时序换来一点点单帧 FID 代价。
- **(b) 外观编码器**：CLIP→IP-Adapter→Ours，FVD 724.96 → 590.99 → **179.07**；SSIM 0.461 → 0.481 → **0.714**——密集外观编码器相对 CLIP/IP-Adapter **碾压式提升**，是最大单点贡献。
- **(c) image-video 联合训练**：单帧+时序均加联合训练，SSIM 0.706→0.714、FVD 158→179（注：FVD 略升但 SSIM/FID 单帧指标改善，论文论点是整体动画质量与细节更好）。
- **(d) 推理视频融合**：去掉则 L1 3.21、FID 32.99；加上 3.13、32.08（小幅提升 + 转场更平滑）。
- **(e) 共享初始噪声**：各段用不同噪声 FID 32.74 vs 同噪声 32.08——**共享同一初始噪声更优**。

**定性 / 应用**：跨身份动画（MRAA/DisCo 在大姿态差异下失败或丢细节，MagicAnimate 鲁棒）；未见域动画（油画、电影角色做跑步/瑜伽）；结合 DALL·E3 生成参考图再动画；多人动画。均为零样本泛化，无定量数字。

## 创新点与影响
**核心贡献**：
1. **Appearance Encoder = 全 UNet 拷贝 + 空间自注意力拼接注入**：用密集像素级外观条件替代 CLIP/IP-Adapter 语义 token，是身份/衣着/背景保真的关键，消融显示 FVD 从 ~725 降到 179。该「ReferenceNet/参考网络」范式与同期 [[animate-anyone]] 殊途同归，成为后续人物视频/可控生成的标准组件。
2. **DensePose 作为驱动信号**：相对 OpenPose 骨架更稠密鲁棒（尤其旋转/大姿态），是 MagicAnimate 区别于 Animate Anyone 的标志性选择；也成为后续工作驱动信号设计的重要参考。
3. **零成本长视频融合**（滑窗 overlap 平均 + 共享初始噪声）：训练 16 帧、推理任意长，工程上简单有效。
4. **image-video 联合训练**：用大规模图像（LAION）补足视频数据稀缺，缓解时序层引入后的单帧质量退化。

**影响**：与 Animate Anyone 共同确立了 2023 末「**参考网络 + 时序模块 + 姿态 ControlNet**」的图驱动人物动画范式，是 EMO、Champ、MimicMotion、UniAnimate 等大量后续工作的直接前身；开源（代码 + checkpoint + HF Space）后社区广泛复现，并被整合进 ComfyUI 等工具链。CVPR 2024 收录。

**已知局限**：
- DensePose 不含背景，动态背景场景（如 TED）L1 误差偏高、背景一致性受限。
- 基于 SD1.5 / 512×512，分辨率与画质受时代基座限制；手部、面部精细动作仍有瑕疵。
- 段长固定 16 帧 + 重叠平均的长视频策略是启发式，长程一致性非端到端建模。
- 训练/推理算力、超参等工程细节因**补充材料缺失而未公开**（见 gaps）。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2311.16498
- arxiv_pdf: https://arxiv.org/pdf/2311.16498
- project_page: https://showlab.github.io/magicanimate/
- github: https://github.com/magic-research/magic-animate
- hf_model: https://huggingface.co/zcxu-eric/MagicAnimate
- hf_space(demo): https://huggingface.co/spaces/zcxu-eric/magicanimate
- repo_preprint_pdf: https://github.com/magic-research/magic-animate/blob/main/assets/preprint/MagicAnimate.pdf

## 本地落盘文件
- ../../../sources/omni/2023/arxiv-2311.16498.pdf （arXiv v1 正文，10 页，精读）
- ../../../sources/omni/2023/magicanimate--preprint.pdf （仓库 preprint，10 页，与 arXiv v1 同，无补充材料）
- ../../../sources/omni/2023/magicanimate--readme.md （GitHub README，基座/checkpoint 结构）
- ../../../sources/omni/2023/magicanimate--project-page.md （项目页快照，确认 CVPR 2024）
- ../../../sources/omni/2023/magicanimate--hf-modelcard.md （HF 模型卡，许可证）
