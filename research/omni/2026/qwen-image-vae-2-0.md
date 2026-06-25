---
title: "Qwen-Image-VAE-2.0 Technical Report"
org: Alibaba Qwen
country: China
date: "2026-05"
type: tech-report
category: method
tags: [vae, high-compression, latent-diffusion, tokenizer, text-rendering, semantic-alignment, dit, image-generation]
url: https://arxiv.org/abs/2605.13565
arxiv: https://arxiv.org/abs/2605.13565
pdf_url: https://arxiv.org/pdf/2605.13565
github_url: https://github.com/alibaba/OmniDoc-TokenBench
hf_url: https://huggingface.co/datasets/alibabagroup/OmniDoc-TokenBench
modelscope_url: ""
project_url: ""
downloaded: [arxiv-2605.13565.pdf, qwen-image-vae-2-0--github-readme.md, qwen-image-vae-2-0--hf-dataset-card.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位

Qwen-Image-VAE-2.0 是阿里 Qwen 团队推出的**高压缩图像 VAE 套件**（f16 与 f32 空间压缩，远高于主流 f8），通过 **Global Skip Connection (GSC) + 扩大潜空间通道 + DINOv2 语义对齐**，同时拿下"高压缩、重建保真、可扩散性 (diffusability)"三难权衡：f16c128 在文字密集文档基准 OmniDoc-TokenBench 上 SSIM 0.9706 / PSNR 30.45 dB / NED 0.9617，**首次让 f16 自编码器的文字保真度超过所有 f8 VAE（含 FLUX.1-dev）**；它是 [[qwen-image-2-0]] 原生高分辨率生成所用潜空间的方法学基础。

## 背景与定位

潜扩散模型 (LDM, 参见 [[latent-diffusion-ldm]]) 用一个 VAE 把图像压到低维潜空间再做扩散，主流空间压缩比是 f8。但随着行业转向**原生高分辨率合成**，DiT 计算量随潜 token 数**二次方增长**（复杂度 O(L²)=O(H²W²/f⁴)），f8 成为瓶颈。提高压缩比 f 是降本的关键。

难点是一个**三难权衡 (tripartite trade-off)**：

- 压缩比越高 → 重建质量越差，**文字密集场景尤甚**（细笔画丢失）；
- 提高潜空间通道维度 C 可缓解信息瓶颈，但会让潜分布**过复杂、无结构**，损害下游扩散模型的收敛与生成（即 diffusability 变差）。

本工作的定位就是用"扩通道补偿空间损失 + 语义对齐保证可扩散性"这条技术路线，把 f16/f32 高压缩 VAE 做到可用。相对前置工作：DC-AE/SANA (Chen 2024) 提出"信息瓶颈 N(z)=CHW/f²"理论但 f32 文字崩溃；VA-VAE (Yao 2025b) 提出语义对齐加速 DiT 收敛但通道有限；本工作把这些思路推进到**大通道 + 文字保真 + 工程高效**的组合。

## 模型架构

非对称、无注意力的卷积式 Encoder-Decoder 自编码器，核心是三处设计：

**1. 高压缩 + 大通道（设计原则）。** 输入图像 I∈R^{H×W×3} 映射为潜表示 z∈R^{(H/f)×(W/f)×C}，序列长 L=HW/f²。放弃 f8，采用 **f16 与 f32**。关键洞察：重建保真度主要由总信息瓶颈 **N(z)=CHW/f²** 决定，因此**用增大通道 C 来补偿高压缩 f 带来的空间信息损失**。而且扩通道**不增加 DiT 训练成本**——DiT 训练时先用一个线性层把潜表示投到固定隐藏维度，计算复杂度对通道维近乎不变。

**2. Global Skip Connection (GSC)。** 高压缩 VAE 最大挑战是激进下采样中保留细粒度细节。GSC 建立一条**从像素直达深层潜空间的全局残差捷径**，绕过初始下采样阶段：用 space-to-channel 操作 + reshape，把输入图像的空间信息"折叠"进通道维。消融（f16c64 from-scratch）对比 No Skip Connection (NSC) / Local Skip Connection (LSC) / GSC，证明 GSC 通过向网络注入高频信号**显著加速收敛**、提升 PSNR，故全系列采用。

**3. 无注意力 (attention-free) backbone。** 自注意力对序列长 N 是 O(N²) 算力与 O(N²) 激活显存，高分辨率下成吞吐瓶颈；作者观察到去掉注意力模块**无明显性能下降**，故全系列移除注意力以保证训练效率与可扩展性。

**4. Encoder-Decoder 非对称。** 轻量 encoder（编码快、降低下游 DiT 训练延迟）+ 重量 decoder（保证高保真重建、保留细节）。

**模型配置（Table 1，denc/ddec 为编码/解码首投影隐藏维，nlayer 为层数，均用 GSC）：**

| 模型 | f | C | denc | ddec | nlayer | 参数 (Enc/Dec) |
|---|---|---|---|---|---|---|
| f16c64 | 16 | 64 | 96 | 144 | 5 | 76M / 248M |
| f16c128 | 16 | 128 | 96 | 144 | 5 | 76M / 248M |
| f32c128 | 32 | 128 | 96 | 144 | 6 | 77M / 250M |
| f32c192 | 32 | 192 | 96 | 144 | 6 | 78M / 250M |

可见 encoder 仅 ~76–78M、decoder ~248–250M，鲜明体现"轻 encoder 重 decoder"的非对称设计。

## 数据

**规模。** 训练语料扩到**数十亿 (billions) 张图像**，覆盖多类别、多分辨率、多宽高比。大规模数据不可避免含噪声（边缘模糊、压缩伪影），用**清晰度滤波 + 模糊滤波**剔除低质样本，确保 VAE 由高保真信号监督。

**文字密集图像采集（两手策略）。** (1) 用 **OCR 滤波器**从海量真实数据里挑出字符密度高的样本；(2) 专门策展一个**文档语料**：学术论文/PPT 幻灯/海报/复杂网页的截图。训练这些真实文字图像让模型学会优先保留字符锐边与语义结构，实现高压缩 VAE 难以做到的**可读文字重建**。

**数据合成（character-level 监督）。** 自研合成管线把文本文档**渲染成图像**，同时支持字母文字（英文）与表意文字（中文，笔画密度/复杂度不同）。两个关键 trick：
- **背景含入合成 (background-contained synthesis)**：作者发现纯背景合成（白底黑字）泛化差，故把文字渲染到从通用图像随机采样的背景上，弥合与真实"文字叠在复杂纹理上"的差距；
- **多粒度难度**：渲染字符大小从 **5 到 20 像素**不等，构造不同难度合成集以适配不同压缩设置，强制 VAE 捕捉细节，**保证 f32 下仍可读**。

## 训练方法

**训练目标（简化而有效）。** 不同于传统 VAE 引入分布先验 + 对抗范式，本工作专注高保真重建 + 潜空间语义对齐。总损失：

```
L_total = L_recon + λ_lpips · L_lpips + λ_align · L_align
```

其中 L_recon 是像素级 L1 重建损失，L_lpips 是感知损失 (LPIPS)，L_align 是语义对齐损失。

**两项反直觉的删除：**
- **去掉 KL 损失**：KL 约束限制潜空间容量、损害重建保真；更关键的是 KL 惩罚与语义对齐目标**互相竞争**（语义特征非高斯分布，强迫同时满足正态先验和语义流形导致对齐次优，拖慢下游 DiT 收敛）。去掉后潜空间更灵活、更适合生成。
- **去掉 GAN 损失**：当训练预算足够大时，L_recon + L_lpips 即可产生清晰锐利重建；去判别器**简化优化、提升稳定性、加速训练**。

**语义对齐（4.2，可扩散性的核心）。** 受 VA-VAE (Yao 2025b) 启发，把 VAE 潜表示与预训练视觉编码器的语义特征对齐，在低级细节保真与高级语义间平衡，让潜空间更"生成友好"。
- **语义编码器选择**：消融对比 DINOv2 / DINOv3 / MAE / PE-Spatial，**DINOv2 最优**，默认用 **DINOv2-L 特征**。
- **对齐层选择**：用**中间层**（而非常规的最后一层）——中间层空间图更平滑、更易对齐；且发现**简单融合多层会引入噪声破坏对齐信号**，故只对齐**单个最优中间层**。
- **对齐目标（两个互补项）**：① **Marginal Cosine Similarity Loss** L_mcos（margin m_cos）对齐潜表示与目标语义的方向；② **Marginal Distance Matrix Similarity Loss** L_mdms（margin m_dist）保持相对空间布局。先把 VAE 潜表示 z 经可学习线性投影 z'=Wz 投到语义维度，再算两项 ReLU 带 margin 的损失。

**多阶段训练策略（4.3，三条课程并行推进）：**
- **分辨率课程**：从低分辨率起步逐步升到 **2K**，全程混入多样宽高比增强几何鲁棒性；
- **文字注入课程**：先通用图像加速初始收敛 → 渐进引入真实文字密集样本 → 最后引入不同难度的合成文字数据精修字符精度；通用纹理与字符细节保持**平衡配比**；
- **语义对齐校准**：早期用**严格 margin** 做强对齐（对可扩散性帮助大）→ 随训练逐渐**放松对齐 margin**，在语义一致性与像素级重建质量间取得更好平衡（"strict → balanced"）。

## Infra（训练 / 推理工程）

报告未披露具体 GPU 数量、GPU·时、并行/分布式策略与混合精度配置（**未报告**）。可从设计推断的工程取向：

- **轻 encoder**：~76–78M 参数的小 encoder 直接降低下游 DiT 训练时的潜表示提取延迟；
- **attention-free backbone**：去自注意力把算力从 O(N²) 降到卷积的 O(N·k²)、激活显存也从 O(N²) 降下来，**维持超高分辨率输入下的高吞吐**；
- **扩通道不增 DiT 算力**：DiT 入口线性投影到固定隐藏维，使通道扩展对 DiT 训练成本近乎无感；
- 推理加速（步数蒸馏/缓存/量化）**未涉及**——这是 VAE 工作，加速主要体现在"高压缩缩短 DiT 序列长 → 二次方降本"这一层面，而非 VAE 本身的步数。

## 评测 benchmark（把效果讲清楚）

评测分两块：**重建保真**（通用 + 文字密集）与**潜空间可扩散性**（下游 DiT）。所有数字均来自已抓取的技术报告 PDF。

**A. 通用重建 + 无引导生成（Table 2，ImageNet 256p / FFHQ 1K；生成为 SiT 训练 80 epoch、w/o CFG）：**

| 模型 | Setting | IS↑ | gFID↓ | Recon@ImageNet PSNR/SSIM | Recon@FFHQ PSNR/SSIM |
|---|---|---|---|---|---|
| FLUX.1-dev (f8) | f8c16 | 54.64 | 25.41 | 32.84 / 0.9155 | 38.14 / 0.9574 |
| Qwen-Image (f8) | f8c16 | 73.52 | 17.68 | 33.42 / 0.9159 | 38.75 / 0.9512 |
| Wan2.1 (f8) | f8c16 | 78.60 | 16.25 | 31.29 / 0.8870 | 38.16 / 0.9456 |
| FLUX.2-dev (f16) | f16c128 | 91.53 | 10.61 | 34.34 / 0.9358 | 40.36 / 0.9676 |
| **Qwen-Image-VAE-2.0-f16c64** | f16c64 | 102.76 | 9.52 | 32.72 / 0.9086 | 39.14 / 0.9541 |
| **Qwen-Image-VAE-2.0-f16c128** | f16c128 | 92.42 | 10.29 | **35.90 / 0.9519** | **43.10 / 0.9795** |
| DC-AE-sana (f32) | f32c32 | 75.73 | 16.88 | 24.82 / 0.6897 | 31.35 / 0.8303 |
| **Qwen-Image-VAE-2.0-f32c128** | f32c128 | 81.23 | 15.05 | 29.69 / 0.8423 | 35.91 / 0.9177 |
| **Qwen-Image-VAE-2.0-f32c192** | f32c192 | 72.31 | 18.33 | 31.13 / 0.8785 | 37.52 / 0.9381 |

要点：在各自压缩档 (f16/f32) 内重建保真**全面 SOTA**；f16c128 的 ImageNet 重建 PSNR 35.90 / FFHQ 43.10 甚至**超过所有 f8 基线**（f8 中最高仅 Qwen-Image 33.42 / HunyuanVideo 39.85）；f32c192 重建质量**可比肩 f8 VAE（如 Wan2.1）却实现 4× 压缩**。无引导生成 (IS/gFID) 上 f16c64 取得 IS 102.76 / gFID 9.52，**在高压缩 LDM-VAE 基线中领先**（明显优于同档常规 VAE 如 Stepvideo-T2V 45.18 / 33.53），作者据此称其潜空间**可扩散性**更优；注：另一类 ViT-backbone 自编码器 VTP-Large (f16c64) 生成指标更高 (IS 146.22 / gFID 5.25)，但其重建与文字保真崩溃（ImageNet PSNR 26.88、OmniDoc NED 仅 0.4170），属"重生成轻重建"的不同取向，论文将其与 RAE 系列单列为另一组。

**B. 文字密集文档重建 OmniDoc-TokenBench（Table 3；~3K 图，实际 3042 张，256×256；NED 为主指标）：**

| 模型 | Setting | SSIM↑ | PSNR↑ | LPIPS↓ | FID↓ | NED↑ |
|---|---|---|---|---|---|---|
| Qwen-Image (f8) | f8c16 | 0.8998 | 24.94 | 0.0519 | 4.48 | 0.9073 |
| HunyuanVideo (f8) | f8c16 | 0.9227 | 25.26 | 0.0434 | 2.03 | 0.9266 |
| **FLUX.1-dev (f8, 文字最强基线)** | f8c16 | 0.9364 | 26.24 | 0.0246 | 0.55 | 0.9546 |
| Cosmos-0.1-CI16x16 (f16) | f16c16 | 0.5460 | 15.55 | 0.1349 | 7.78 | 0.1547 |
| HunyuanImage-3.0 (f16) | f16c32 | 0.8672 | 22.66 | 0.0650 | 3.49 | 0.7753 |
| **Qwen-Image-VAE-2.0-f16c64** | f16c64 | 0.9279 | 26.00 | 0.0382 | 1.94 | 0.9244 |
| FLUX.2-dev (f16) | f16c128 | 0.9544 | 27.72 | 0.0216 | 0.73 | 0.9535 |
| **Qwen-Image-VAE-2.0-f16c128** | f16c128 | **0.9706** | **30.45** | **0.0167** | 0.79 | **0.9617** |
| HunyuanImage-2.1 (f32) | f32c64 | 0.7805 | 19.85 | 0.0957 | 5.19 | 0.4895 |
| LTX-Video (f32) | f32c128 | 0.8055 | 20.92 | 0.1190 | 17.10 | 0.5651 |
| **Qwen-Image-VAE-2.0-f32c128** | f32c128 | 0.8442 | 22.13 | 0.0642 | 3.36 | 0.7065 |
| **Qwen-Image-VAE-2.0-f32c192** | f32c192 | 0.8908 | 23.84 | 0.0497 | 1.98 | 0.8555 |

要点（一手数字）：
- **f16c128 文字保真 NED 0.9617，超过所有评测 VAE 含 FLUX.1-dev (0.9546)**——作者称"据我们所知这是**首个文字保真度超过 f8 VAE 的 f16 自编码器**"；其 SSIM 0.9706 / PSNR 30.45 也胜过最佳 f8 基线 FLUX.1-dev (0.9364 / 26.24)，**而压缩比高 2×**；
- 即便轻量 f16c64 (NED 0.9244) 也已**与领先 f8 方法相当**（原文 "competitive with leading f8 methods"）：超过 Wan2.1 (0.8021)/Cosmos-0.1 (0.9033)/Qwen-Image (0.9073)，仅略低于 HunyuanVideo (0.9266) 与 FLUX.1-dev (0.9546)；
- **f32c192 NED 0.8555 反超多个 f16 基线**；竞品 f32 在文字上近乎全毁（NED 0.07–0.57，如 DC-AE-sana 0.0692）；
- **NED 必要性**：作者举例单字符错误 "orange→orango" PSNR 损失 <0.5 dB 但 NED 降 16.7%；相关性分析显示像素指标与文字保真**非完美相关**（如 f16 中 Stepvideo-T2V 的 NED 0.8838 > HunyuanImage-3.0 的 0.7753，尽管 SSIM 相近），证明 NED 是必要的互补指标。

**C. 可扩散性（下游 DiT，6.1.3）。** 在 ImageNet 256×256 上训 SiT（严格沿用 Leng 2025 的代码库与默认超参），80 epoch 报告 IS 与 gFID：f8 用 SiT-XL/2，f16/f32 用 SiT-XL/1；因高维潜空间常需更大 CFG，为公平**只报无引导结果**。结论：Qwen-Image-VAE-2.0 一致优于现有高压缩基线，**大潜维度下仍能快速 DiT 收敛**，归因于改进的语义对齐 + 分阶段对齐范式。

**D. 大规模验证。** Qwen-Image-VAE-2.0 已集成进 [[qwen-image-2-0]]（注：实际集成的是本方法学框架派生的**中间变体**），在基础模型规模上验证潜空间可支撑复杂开放词表条件与精细组合约束、精确文字渲染与照片级纹理。

**关键消融汇总**：① GSC vs NSC/LSC（加速收敛、提 PSNR）；② 去 KL / 去 GAN（提保真与稳定性）；③ 语义编码器 DINOv2 最优、中间层最优、单层优于多层融合；④ strict→balanced 对齐范式。

## 创新点与影响

**核心贡献：**
1. **一套 f16/f32 高压缩图像 VAE**（f16c64/f16c128/f32c128/f32c192），为原生高分辨率高效生成提供方案；
2. **GSC 全局跳连 + 大通道**这套"扩通道补偿空间损失"的架构组合，配合去 KL / 去 GAN 的简化训练目标，破解"高压缩 vs 重建保真"瓶颈；
3. **改进语义对齐（DINOv2 中间层 + 双 margin 损失 + strict→balanced 课程）**，证明**大通道 VAE 也能有优秀可扩散性**，正面回应"压缩比 / 重建保真 / 可扩散性"三难权衡；
4. **OmniDoc-TokenBench**：~3K（3042 张）九类真实文档（书/幻灯/彩色教材/试卷/学术论文/杂志/财报/报纸/笔记，中英双语）+ **OCR 驱动的 NED 指标**（基于 PP-OCRv5，用原图 OCR 输出而非标注作参照以抵消 OCR 系统误差），填补了 ImageNet/FFHQ/TokBench 在文字密集重建评测上的空白；数据集与评测工具开源（Apache-2.0）。

**影响：** 把高压缩 VAE 的可用边界推到 f16/f32 文字仍可读，且通过集成进 [[qwen-image-2-0]] 在基础模型规模上落地，为"原生高分辨率 + 低 DiT token 成本"的下一代生成系统提供潜空间底座；NED + OmniDoc-TokenBench 有望成为文字密集重建的标准评测。

**已知局限 / 未披露：**
- **VAE 权重未公开**（探测 `Qwen/Qwen-Image-VAE-2.0` 等 HF 仓库返回 401，公开的仅 OmniDoc-TokenBench 数据集与评测工具）；
- 训练 infra（GPU 规模、GPU·时、并行策略、混合精度、吞吐）**完全未报告**；
- 关键超参（λ_lpips、λ_align、margin 具体数值、各阶段步数/数据配比）**未给出**；
- 数据"数十亿张"无具体来源/版权/安全过滤细节披露；NED 在不做文本归一化时受 OCR 间距伪影影响（作者承认但称对所有模型一致施加以保证公平）。

## 原始链接

- arxiv_abs: https://arxiv.org/abs/2605.13565
- arxiv_pdf: https://arxiv.org/pdf/2605.13565
- github (benchmark + eval toolkit): https://github.com/alibaba/OmniDoc-TokenBench
- hf_dataset (OmniDoc-TokenBench): https://huggingface.co/datasets/alibabagroup/OmniDoc-TokenBench

## 本地落盘文件

- ../../../sources/omni/2026/arxiv-2605.13565.pdf
- ../../../sources/omni/2026/qwen-image-vae-2-0--github-readme.md
- ../../../sources/omni/2026/qwen-image-vae-2-0--hf-dataset-card.md
