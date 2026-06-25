---
title: "Zero123++: a Single Image to Consistent Multi-view Diffusion Base Model"
org: "SUDO-AI (UC San Diego / Stanford / Tsinghua / UCLA / Zhejiang Univ.)"
country: US
date: "2023-10"
type: tech-report
category: 3d
tags: [3d, multi-view, novel-view-synthesis, diffusion, stable-diffusion, reference-attention, controlnet, objaverse]
url: "https://arxiv.org/abs/2310.15110"
arxiv: "https://arxiv.org/abs/2310.15110"
pdf_url: "https://arxiv.org/pdf/2310.15110"
github_url: "https://github.com/SUDO-AI-3D/zero123plus"
hf_url: "https://huggingface.co/sudo-ai/zero123plus-v1.1"
modelscope_url: ""
project_url: "https://huggingface.co/spaces/sudo-ai/zero123plus-demo-space"
downloaded: [arxiv-2310.15110.pdf, zero123pp--ar5iv-fulltext.md, zero123pp--readme.md]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
Zero123++ 是把单张图片转成「3×2 拼接的 6 视角一致网格」的图像条件扩散基座，通过从 Stable Diffusion 2（v-prediction）最小化微调来复用 2D 生成先验。核心创新是「拼图建模联合分布 + 噪声调度换 linear + Scaled Reference Attention 局部条件 + FlexDiffuse 全局条件」，在 Objaverse 验证集上 LPIPS 0.177（优于 Zero-1-to-3 XL 的 0.188，且训练数据远少于后者），成为后续众多单图到 3D 管线的标配前端。

## 背景与定位
单图到 3D 的主流路线是借助 2D 扩散先验做新视角合成（NVS）。前作 [[zero-1-to-3]]（Zero123）开创了开放世界单图到 3D 的零样本 NVS，但有两大顽疾：

1. **几何不一致**：Zero123 对每个新视角**独立采样**（建模的是每张图的条件边缘分布），忽略了多视角之间的相关性，导致视角间结构/纹理对不齐，与真实 3D 场景存在 gap。后续 [[one-2-3-45]]、[[syncdreamer]]、Consistent123 都是在 Zero123 之上「加层」去补一致性；DreamFusion / [[prolificdreamer]] / DreamGaussian 等优化类方法则从不一致模型里蒸馏 3D 表征——但它们若有一个原生一致的多视角基座会更好。
2. **没用足 SD 先验**：(a) 训练时把条件图按特征维 concat 进噪声输入，强加了错误的逐像素空间对应；(b) 用了 256 而非 SD 原生 512 分辨率（作者称 512 训练不稳定），低于训练分辨率会拉低 SD 的生成质量。

Zero123++ 的定位就是「重做一个原生多视角一致的扩散基座」，从 [[latent-diffusion-ldm]] 体系的 Stable Diffusion 2 微调而来，把上述问题逐个工程化解决。它不是新范式，而是一组让 2D 扩散先验最大化迁移到 3D 多视角任务的**工程化设计组合拳**。

## 模型架构
- **Backbone**：Stable Diffusion 2 的 U-Net（latent diffusion），并特意选用 **v-prediction 参数化**版本作为微调起点（理由见训练方法的噪声调度部分）。文本编码器为 SD 自带的 CLIP；推理时不加文本条件，T 用空 prompt 编码。
- **多视角联合建模（拼图法）**：把围绕物体的 6 个视角按 **3×2 布局**拼成单张图，让一次去噪建模 6 视角的**联合分布**而非各自的边缘分布——这是保证一致性的最简形式。
- **固定相机位姿（消歧）**：因 Objaverse 物体朝向不规范，用绝对方位训练会让朝向歧义。Zero123++ 用**绝对俯仰角 + 相对方位角**：
  - 方位（相对输入视角）：30°、90°、150°、210°、270°、330°（每个 +60°）。
  - v1.1 俯仰（绝对）：交错的「30° 向下」与「20° 向上」（论文§2.1 原文 "30° downward and 20° upward"；README 以绝对值记为 `30, -20, 30, -20, 30, -20`，-20 即 20° 向上）。v1.2 改为 20° 向下 / 10° 向上（README 记 `20, -10, ...`），并把输出视场角统一到 30°。
  - 这样既消除朝向歧义，又**不需要像 One-2-3-45/DreamGaussian 那样额外跑俯仰角估计模块**（后者会引入误差）。
- **局部条件——Scaled Reference Attention**：不再 concat 条件图，而是用 Reference Attention：把参考图（加与去噪输入同等级别的高斯噪声）单独过一遍 U-Net，把其 self-attention 的 K、V 矩阵拼到去噪 U-Net 的对应注意力层里。关键是**对参考 latent 做尺度缩放**——在 ShapeNet Cars 上消融出 **5× 缩放**时与输入图的一致性最高。这套机制无需改 SD 结构、能完整复用先验。
- **全局条件——可训练版 FlexDiffuse**：用 CLIP 图文空间对齐，把 CLIP 全局图像 embedding I（维度 D）按一组**可训练的逐 token 权重** {w_i} 加到 prompt embedding 上：T'_i = T_i + w_i·I，权重按 FlexDiffuse 的线性引导初始化 w_i = i/L。消融显示：缺全局条件时，输入图**可见区域**仍 OK，但**不可见区域**（如物体背面）质量明显崩坏，因为模型推不出全局语义。
- **参数量**：未单独披露（约等于 SD2 U-Net 量级，文中未给具体数字）。
- **分辨率策略**：直接在 SD 原生分辨率训练（不像 Zero123 降到 256），靠下面的噪声调度修正解决高分训练不稳的问题。

## 数据
- **数据集**：Objaverse（§2.5 仅说"Objaverse data rendered with random HDRI"，未给规模；规模数字出自 Future Work——约 **800k objects**，作者称 medium-scale）。
- **渲染**：用**随机 HDRI 环境光照**渲染训练图。
- **深度 ControlNet 数据**：渲染与目标 RGB 对应的**归一化线性深度图**来训练 ControlNet。
- **法线生成器（v1.2，README 披露）**：训练能生成视角空间法线图的 ControlNet，其输出还能比 SAM 更准地抠 mask。
- 数据清洗/过滤/配比、美学与安全过滤、re-captioning 等细节：**未披露**（这是一份偏工程的技术报告，重点在条件机制而非数据工程）。

## 训练方法
- **目标 / 参数化**：diffusion，**v-prediction**。选 v 的核心理由是**噪声调度的可替换性**——
  - **噪声调度换成 linear**：SD 原生的 scaled-linear 调度偏重局部细节、低 SNR 步极少，而低 SNR 的早期去噪步决定全局低频结构；步数太少会让结构变化大，损害多视角全局一致性。作者用一个玩具实验佐证：在 SD2 上微调 LoRA 去过拟合「给 prompt *a police car* 却要输出纯白图」，scaled-linear 调度下 LoRA **学不会**（只把图微微变白），换 linear 调度则能稳定输出纯白图——说明调度强烈影响模型适应新全局需求的能力。
  - 这也解释了 Zero123 为何用低分辨率：低分辨率图在同等绝对噪声下「看起来更糙」，等价于把调度改向更强调全局结构（引用 Ting Chen 关于噪声调度的工作）；同样解释了 Zero123 高分训练不稳。
  - 难点是把预训练模型适配到新调度。实验发现 **v-prediction 模型对换调度极其鲁棒**（推理时直接把 SD2-v 从 scaled-linear 换成 linear 不微调也能出高质量图），而 x0-、ε-参数化换调度会显著掉质量；理论上 v-prediction 也更稳（Progressive Distillation）。故选 SD2 v-model 作基座。
- **分阶段微调**（沿用 Stable Diffusion Image Variations 的 phased schedule，目的是最大化保留 SD 先验、最小化改动）：
  - **阶段一**：只调 self-attention 层 + cross-attention 的 KV 矩阵。AdamW + cosine annealing，峰值 LR **7×10⁻⁵**，**1000 步 warm-up**。
  - **阶段二**：用很保守的**常数 LR 5×10⁻⁶**、**2000 步 warm-up**，调**整个 U-Net**。
  - 全程用 **Min-SNR 加权策略**提高训练效率。
- **深度 ControlNet**：在训好的 Zero123++ 上训一个 ControlNet（[[controlnet]] 范式），以深度控制几何。
- 蒸馏/步数加速（consistency/LCM/ADD 等）：**未使用**（本工作不做加速蒸馏）。
- 算力/GPU·时/总训练步数/batch size：**未披露**。

## Infra（训练 / 推理工程）
- **训练 infra**（并行、混合精度、吞吐、GPU 规模、训练时长）：**未披露**。
- **推理工程**（来自 README，工程细节较实）：
  - 以 `diffusers` 自定义 pipeline 形式发布，零额外代码；推荐 `torch>=2.0`、`diffusers==0.20.2`、`transformers`；torch 1.x 建议装 `xformers`。
  - 调度器用 `EulerAncestralDiscreteScheduler`，`timestep_spacing='trailing'`。
  - **推理步数**：一般真实/合成物体约 **28 步**够用；人脸/动漫等精细细节建议 **75–100 步**（README 默认示例用 75 步）。
  - **显存**：基础 NVS pipeline 约 **5 GB VRAM**；加深度 ControlNet 约 **5.7 GB**；深度 ControlNet 示例用 36 步。
  - 输入需正方形，推荐分辨率 ≥320×320；默认输出为灰背景不透明图（VAE 的 zero），需额外 `rembg` 去背景（v1.2 可用法线图抠更准的 mask）。
  - 部署形态：HuggingFace Spaces 官方 Demo、Google Colab、Replicate、本地 `streamlit run app.py` / `gradio_app.py`。
- **模型许可**：代码 Apache 2.0；权重 **CC-BY-NC 4.0**（非商用，但输出可自由使用）。

## 评测 benchmark（把效果讲清楚）
- **主指标 LPIPS（Objaverse 验证子集，6 视角拼图后整图算 LPIPS，越低越好）**：

  | 模型 | LPIPS ↓ |
  | --- | --- |
  | Zero-1-to-3 | 0.210 ± 0.059 |
  | Zero-1-to-3 XL | 0.188 ± 0.053 |
  | **Zero123++（本文）** | **0.177 ± 0.066** |

  说明：Zero123 系列**可能在训练时见过本文的验证集**，且 XL 变体训练数据远多于 Zero123++，但 Zero123++ 仍取得最佳 LPIPS——佐证其设计有效。SyncDreamer 因不支持改俯仰角而被排除在量化对比外。
- **深度 ControlNet 版**：在同一验证集上 LPIPS 进一步降到 **0.086**。
- **法线生成器 ControlNet（v1.2，README）**：Objaverse 验证集上 alpha（matting 前）IoU **98.81%**，平均法线角误差 **10.75°**，法线 PSNR **26.93 dB**。
- **定性对比**：在 4 张输入图（Objaverse 带背面大不确定性的电子玩具猫、灭火器真实照、SDXL 生成的「坐火箭的狗」、动漫插画）上对比 Zero-1-to-3 XL、SyncDreamer，Zero123++ 一致性与质量更好，且能泛化到 AI 生成图与 2D 插画等域外输入。文中给 Zero123 XL/SyncDreamer 配了 One-2-3-45 的俯仰角估计、用 SAM 抠背景。
- **文本到多视角**：先 SDXL 文生图、再过 Zero123++。对比 [[mvdream]] 与 Zero-1-to-3 XL：MVDream 因 Objaverse 偏置出现卡通化/扁平纹理，Zero123 无法保证多视角一致，Zero123++ 能出真实、一致、高细节的多视角图。
- 关键消融结论：(1) 全局条件对**不可见区域**质量至关重要；(2) Reference Attention latent **缩放 5×** 时与输入一致性最佳；(3) **linear 调度 + v-prediction** 才能稳定适应新全局需求。
- FID/CLIPScore/GenEval/人评 ELO 等：**未报告**（3D NVS 任务以 LPIPS 为主，本文未做这些 2D 文生图指标）。

## 创新点与影响
- **核心贡献**：
  1. **拼图联合建模**——3×2 单帧拼 6 视角，从根上把「独立采样导致不一致」变成「联合分布」，简单且有效。
  2. **固定绝对俯仰 + 相对方位**——消除朝向歧义，**去掉了俯仰角估计模块**这一误差来源。
  3. **噪声调度洞见**——把「换 linear 调度」与「v-prediction 对换调度鲁棒」联系起来，并用玩具实验/低分辨率等价性解释清楚为何调度决定全局一致性能力，是本文最有迁移价值的分析。
  4. **Scaled Reference Attention + 可训练 FlexDiffuse**——分别解决局部与全局条件，且都**完整复用 SD 先验、最小化微调**。
  5. 分阶段微调 + Min-SNR 加权，进一步保护先验。
- **影响**：作为「单图→一致 6 视角」的开源扩散基座，被广泛用作 3D 生成管线的**前端**（后接稀疏视角重建/网格化），是 SUDO-AI 自家 One-2-3-45++ 等管线及社区大量 3D 工具链的事实标准组件；其「拼图建模 + 固定位姿 + Reference Attention」思路被后续多视角扩散工作沿用。
- **已知局限 / Future Work（作者自陈）**：
  - 缺二阶段 refiner——ε-参数化模型局部细节更好，作者设想用 SDXL（ε）做 refiner 的 generate-refine 两阶段。
  - 规模有限——仅在约 800k 的 Objaverse 上训练，计划扩到 Objaverse-XL（10M+）。
  - 多视角图到高质量 3D 网格仍有 gap，文中只给了初步网格重建结果。
  - 权重 CC-BY-NC，不能进商用管线。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2310.15110
- arxiv_pdf: https://arxiv.org/pdf/2310.15110
- github: https://github.com/SUDO-AI-3D/zero123plus
- hf_models: https://huggingface.co/sudo-ai （zero123plus-v1.1 / v1.2 / controlnet-zp11-depth-v1 / controlnet-zp12-normal-gen-v1）
- official_demo: https://huggingface.co/spaces/sudo-ai/zero123plus-demo-space

## 本地落盘文件
- ../../../sources/omni/2023/arxiv-2310.15110.pdf
- ../../../sources/omni/2023/zero123pp--ar5iv-fulltext.md
- ../../../sources/omni/2023/zero123pp--readme.md
