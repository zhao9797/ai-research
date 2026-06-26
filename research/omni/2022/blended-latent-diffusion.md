---
title: "Blended Latent Diffusion"
org: "The Hebrew University of Jerusalem / Reichman University"
country: EU
date: "2022-06"
type: paper
category: edit
tags: [image-editing, inpainting, local-editing, latent-diffusion, mask-blending, zero-shot, training-free]
url: "https://arxiv.org/abs/2206.02779"
arxiv: "https://arxiv.org/abs/2206.02779"
pdf_url: "https://arxiv.org/pdf/2206.02779"
github_url: "https://github.com/omriav/blended-latent-diffusion"
hf_url: "https://huggingface.co/omriav/blended-latent-diffusion-ldm"
modelscope_url: ""
project_url: "https://omriavrahami.com/blended-latent-diffusion-page/"
downloaded: [arxiv-2206.02779.pdf, blended-latent-diffusion--readme.md, blended-latent-diffusion--project-page.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
把 [[blended-diffusion]] 的"按掩码逐步混合"思想从像素空间搬进 [[latent-diffusion-ldm]] 的潜空间，得到一个**零样本、免训练**的局部文本驱动图像编辑/inpainting 方法：仅修改掩码内区域、背景无缝保留，比像素级 Blended Diffusion **加速约 10–20×**（25 分钟 → 单图约几秒/批处理每图约 3 秒），且在 ImageNet 分类器精度上以大幅领先（batch precision 28.66% vs 次优 10.49%）。

## 背景与定位
论文要解决的是**局部文本编辑**（local text-driven editing）：给定真实图像 `x`、文本提示 `d`、二值掩码 `m`，生成 `x̂` 使掩码内 `x̂⊙m` 符合文本、掩码外 `x⊙(1−m)≈x̂⊙(1−m)` 且过渡无缝。这一场景在实际修图中极常见，但当时只有三种方法显式处理它：[[blended-diffusion]]、GLIDE、DALL·E 2，且其中只有 Blended Diffusion 完整公开。

技术脉络上，前置工作 [[blended-diffusion]]（Avrahami et al. 2022，CVPR）用 ImageNet 上训练的像素级扩散模型作自然图像先验、CLIP 作文本导航，在**像素空间**逐步对带噪图做空间混合。它的两大痛点：(1) 推理慢——单 GPU 约 25 分钟才能出好结果，因为像素级扩散步数多且每步要算 CLIP 梯度；(2) 像素级噪声伪影（像素值越界产生 clipping artifact）。

本文的核心 insight：[[latent-diffusion-ldm]]（Rombach et al. 2022）已把扩散搬进 VAE 压缩后的低维潜空间，速度快一个量级，且自带 text-to-image 条件能力，无需每步 CLIP 梯度。于是只要**在潜空间里复刻"混合"操作**，就能把局部编辑能力嫁接到 LDM 上。本质是一个把已有预训练模型（text-to-image LDM + CLIP）零样本组合起来的推理时方法，**不训练任何新权重**。与并发的 prompt-to-prompt（无掩码、编辑生成图）相比，本文针对的是有掩码、可编辑真实图像的设定。

## 模型架构
本方法本身**不引入新网络**，而是复用预训练组件，关键在推理算法（Algorithm 1）：

- **Backbone（生成器）**：text-to-image **Latent Diffusion Model**（Rombach et al. 2022 发布的 `txt2img-f8-large` 检查点，约 **1.45B** 参数，U-Net 去噪器在潜空间工作）。LDM = VAE 编码器 `E(x)` + 解码器 `D(z)` + 潜空间扩散模型 `(noise, denoise)`。
- **VAE / 压缩**：卷积式 VAE，潜空间相对图像**下采样 8×**（f8）。因此掩码 `m` 需下采样到潜空间得到 `m_latent` 用于混合。
- **Text encoder / 条件注入**：沿用 LDM 自带的文本条件（denoise 直接以提示 `d` 为条件），不再用 CLIP 梯度去引导扩散过程。
- **CLIP 的角色**：仅用于**最终预测排序**（prediction ranking），backbone 用 **ViT-B/16** 的 CLIP（约 **0.15B** 参数），按生成结果与提示的 CLIP 余弦距离挑出最优若干张。
- **参数量对比**（论文 Table 3，base+CLIP）：Ours = 1.45B + 0.15B = **1.60B**；Blended Diffusion = 0.55B+0.15B=0.70B；GLIDE = 5.00B+0.15B=**5.15B**（约本方法 ×3）；GLIDE-filtered = 0.30B+0.15B=0.45B；PaintByWord++ = 0.09B+0.15B=0.24B。
- **分辨率策略**：未单独披露固定分辨率；继承 LDM 的生成尺寸（官方 LDM 实现常用 256 级别）。开源仓库后续追加了基于 Diffusers 的 **Stable Diffusion v2.1** 与 **SDXL** 实现（同一混合算法换更强 backbone）。

**核心方法（三个组件）：**

1. **潜空间混合（Blended Latent Diffusion，§4.1）**：先 `z_init = E(x)`，把掩码下采样得 `m_latent`，一步加噪到噪声水平 k 得 `z_k`。然后从 t=k 到 0 迭代：
   - 前景：`z_fg = denoise(z_t, d, t)`（以文本去噪一步）
   - 背景：`z_bg = noise(z_init, t)`（把原图潜变量加噪到当前水平）
   - 混合：`z_t ← z_fg ⊙ m_latent + z_bg ⊙ (1 − m_latent)`
   最后 `x̂ = D(z_0)`。每步整张潜变量都被改，但混合强制掩码外保持原样，下一步去噪再把拼缝处理得连贯。相比像素级 + CLIP 梯度方案，优势是：推理快一个量级、避免像素级越界伪影、消除 CLIP 梯度带来的对抗样本风险、精度更高。

2. **背景重建（§4.2，可选）**：因 VAE 是**有损**压缩，即使不做任何扩散，`D(E(x))` 在掩码外也会偏离原图（人脸、文字、高频纹理尤其敏感）。作者比较了像素拼接（有可见拼缝）、Poisson 融合（颜色漂移）、潜空间优化（过度平滑），最终采用**逐图微调解码器权重**（per-image decoder weights optimization，灵感来自 GAN inversion 的 pivotal tuning）：
   `θ* = argmin ‖D_θ(z_0)⊙m − x̂⊙m‖ + λ‖D_θ(z_0)⊙(1−m) − x⊙(1−m)‖`，λ=100。该步**仅对最终选中的结果做**，因此不拖慢整批推理。

3. **渐进式掩码收缩（Progressive Mask Shrinking，§4.3）**：细掩码下采样后会更细，导致编辑失效。作者通过可视化发现扩散早期只生成粗糙颜色/形状、晚期才细化；于是**早期用膨胀过的粗掩码、随扩散逐步收缩到原掩码**，只让最后阶段用细 `m_latent` 混合。实现：用 3×3、5×5、7×7 全 1 核膨胀，把扩散过程四等分，从最膨胀到原始掩码逐段使用。

## 数据
本方法**零样本、无训练**，自身不消耗训练数据。所依赖的预训练模型数据：

- **LDM backbone**：在 **LAION-400M**（Schuhmann et al. 2021，4 亿网络爬取图文对，未经策展 non-curated）上训练（论文 §E 明确点出，并讨论由此继承的偏见与不良内容风险）。
- **CLIP**：在 4 亿网络图文对上对比学习预训练（Radford et al. 2021）。
- **评测用图**：论文所用全部输入图为 Creative Commons 自由许可或作者私藏的**真实图像**；定量评测用 50 张随机图 + 随机掩码 + 从 ImageNet 类别随机抽取的文本提示。
- 无任何新数据采集、清洗、re-caption 或合成数据流程（不适用）。

## 训练方法
**不训练生成模型**——这是论文的关键卖点（zero-shot，依赖现成预训练模型）。唯一的"优化"是推理时的两处逐样本优化，均非常规模型训练：

- **解码器权重微调**（背景重建，§4.2）：Adam，学习率 **1e-4**，**每图 75 步**优化，只对选中结果做。
- （早期版本曾比较的）潜变量优化亦用 Adam / lr 1e-4 / 75 步，但因过度平滑被弃用，改为权重微调。
- **训练目标 / flow matching / 多阶段 / RLHF / DPO / 蒸馏**：均**不适用**——没有预训练、continue、SFT、偏好对齐或步数蒸馏环节；加速完全来自"在低维潜空间做扩散 + 免 CLIP 梯度"，不是蒸馏。
- **预测排序作为 trick**：利用扩散随机性生成多张候选，用 CLIP 余弦距离排序取最优（一对多任务）。

## Infra（训练 / 推理工程）
- **训练算力**：不适用（无训练）。论文仅指出像素级扩散训练常耗"数百 GPU 天"，而 LDM 把训练/推理成本降低，正是本方法选 LDM 的动机。
- **推理硬件**：评测在单张 **NVIDIA A10** GPU 上测时延（论文 §5.2 / Table 2）。
- **推理时延（Table 2，batch size 24）**：
  - Ours 无背景优化：单图 6s，整批 53s，**每图约 2.2s**
  - Ours 带背景优化：单图 25s，整批 72s，**每图约 3s**
  - Blended Diffusion：单图 27s，整批（bs=64）1472s，每图 23s
  - Local CLIP-guided diffusion：同上 1472s / 每图 23s
  - PaintByWord++：单图 78s（整批 / 每图均为 `—`，原表未报告批处理时延）
  - GLIDE-filtered：单图 7s，整批 89s，每图 3.7s
  - **加速比（论文明确给出的，§5.2）**：相对 Blended Diffusion / Local CLIP-guided diffusion，**等批大小 ×10，按各自推荐批大小 ×20**。（论文未给出相对 PaintByWord++ / GLIDE-filtered 的加速倍数，从单图时延看 GLIDE-filtered 7s 与 Ours 6s 相当。）
- **加速来源**：(1) 扩散在 8× 下采样的潜空间进行；(2) 取消每步 CLIP 梯度反传；(3) 背景重建只对 top-ranked 结果做。
- **部署形态**：开源 PyTorch 实现（基于 CompVis latent-diffusion）。原 LDM 检查点 5.7GB（`txt2img-f8-large`，HF 镜像 `omriav/blended-latent-diffusion-ldm`）。仓库另提供基于 Diffusers 0.19.3 / PyTorch 2.1 的 **Stable Diffusion v2.1** 与 **SDXL**（更强 GPU）脚本。
- **量化 / 缓存 / 步数蒸馏**：未使用 / 未报告。局限里作者也承认仍需 >1 分钟出一批排序结果，进一步加速是 open problem。

## 评测 benchmark（把效果讲清楚）
评测协议：50 张随机图 + 随机掩码 + ImageNet 类别随机提示；用现成 **ImageNet 分类器**判定掩码区是否符合文本（刻意不用 CLIP 相似度做评判，因 CLIP 对用其梯度生成的方法有对抗失真）。

**定量主表（Table 1，含右侧两列人评，照搬原表）：**

| 方法 | Batch Precision ↑ | Batch Diversity (LPIPS) ↑ | Best-Result Precision ↑ | 人评 Vis.Quality（偏好 Ours %） | 人评 Text Matching（偏好 Ours %） |
|---|---|---|---|---|---|
| Blended Diffusion | 10.4% | 0.106 | 36% | 64% | 55% |
| Local CLIP-guided diffusion | 10.49% | **0.419** | 38% | 74% | 62% |
| PaintByWord++ | — | — | 0% | 94% | 68% |
| GLIDE-filtered | 1.87% | 0.114 | 4% | 26% | 86% |
| **Ours** | **28.66%** | 0.115 | **54%** | — | — |

> 表读法（核对自 PDF Table 1 原表）：右侧两列是 AMT 人评中**偏好 Ours** 的评审比例（对每个 baseline 二选一），故 Ours 自身行为 `—`。**Ours 取得最高 batch precision（28.66%，次优 10.49%）与最高 best-result precision（54%）**；diversity 次优（0.115），仅被 Local CLIP-guided diffusion（0.419，因其改全图、前景约束少）超过。**PaintByWord++ 的 batch precision / diversity 在原表为 `—`（未报告）**，best-result precision = 0%；`1.87% / 0.114 / 4%` 一行属于 **GLIDE-filtered**（其编辑常几乎不改原图，故 precision 极低）。

**人评解读（数据见上表右两列，AMT 二选一偏好 Ours 的比例）：** 除 GLIDE-filtered 的视觉质量外，Ours 在所有对比、两个维度上都被多数评审偏好（≥50%），二项检验（补充材料 Table 2）显示统计显著。GLIDE-filtered 的视觉质量只有 26% 评审偏好 Ours（即多数人觉得 GLIDE-filtered 更"自然"），原因是它**经常几乎不改原图**——看起来自然但没完成编辑；而其文本匹配有 86% 评审偏好 Ours，正好反证 GLIDE-filtered 没真正按文本编辑。

**定性结论**：相对 Blended Diffusion 消除了像素级噪声伪影（pizza、dog collar 例）；相对 GLIDE-masked，过渡更无缝；相对 DALL·E 2 在线 demo，DALL·E 2 常忽略或只部分遵循提示。

**消融/关键结论**：背景重建（解码器微调 f）优于像素拼接(c)/Poisson(d)/潜变量优化(e)；渐进掩码收缩显著改善细掩码编辑；CLIP 排序对挑出 top 结果有效（top 20% 稳定优于 bottom 20%）。

**局限**：(1) 仍需 >1 分钟出一批；(2) CLIP 排序只看掩码区、忽略整图真实性，可能各局部真实但整体不协调；(3) LDM 文字生成能力"双刃剑"——可能把"big mountain"理解成生成写着该词的海报；(4) 对输入提示/掩码/图像的小扰动较敏感。

## 创新点与影响
**核心贡献**（论文自述四点）：(1) 首次把 text-to-image LDM 适配到局部文本编辑；(2) 提出逐图解码器微调解决 LDM 潜空间有损重建破坏背景的问题；(3) 提出渐进掩码收缩解决细掩码失效；(4) 提出 precision / diversity 两个局部文本编辑的定量评测指标。

**影响**：本工作把"潜空间逐步掩码混合"确立为基于 [[latent-diffusion-ldm]] / [[stable-diffusion-1]] 的**高效局部编辑/inpainting 范式代表**，是后续大量训练-free 掩码编辑与 inpainting pipeline（包括 diffusers 生态的 blend/inpaint 思路）的直接前身；其"用 VAE 潜空间混合 + 仅对最终结果做背景修复"的设计被广泛沿用。被收录为 **SIGGRAPH 2023 / ACM TOG**（扩展版 v2，2023-04，27 页），原 arXiv v1 为 2022-06。开源实现持续维护，已扩展到 SD v2.1 / SDXL。

**已知局限**（同上"评测-局限"）：速度仍受扩散步数限制、CLIP 排序非全局、对输入敏感、可能触发 LDM 的"文字海报"偏置、继承 LAION-400M 的数据偏见与不良内容风险。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2206.02779
- arxiv_pdf: https://arxiv.org/pdf/2206.02779
- project_page: https://omriavrahami.com/blended-latent-diffusion-page/
- github: https://github.com/omriav/blended-latent-diffusion
- hf (LDM ckpt mirror): https://huggingface.co/omriav/blended-latent-diffusion-ldm
- video: https://www.youtube.com/watch?v=7ZZXmwJCsKI

## 一手源存档（sources/）
- [arxiv-2206.02779.pdf](https://arxiv.org/pdf/2206.02779)  （论文 v2 全文 27 页，已精读方法/实验/附录）  （arXiv 原文 PDF，不入 git）
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2022/blended-latent-diffusion--readme.md)  （GitHub 仓库页快照，含安装/用法/检查点/SD2.1/SDXL）
- [project-page.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2022/blended-latent-diffusion--project-page.md)  （官方项目页快照）
