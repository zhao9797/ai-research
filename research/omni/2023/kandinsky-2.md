---
title: "Kandinsky 2.x (Image Prior + Latent Diffusion)"
org: "Sber AI / AIRI / Skoltech"
country: EU
date: "2023-07"
type: tech-report
category: t2i
tags: [t2i, unclip, image-prior, latent-diffusion, movq, multilingual, open-source, clip]
url: "https://arxiv.org/abs/2310.03502"
arxiv: "https://arxiv.org/abs/2310.03502"
pdf_url: "https://arxiv.org/pdf/2310.03502.pdf"
github_url: "https://github.com/ai-forever/Kandinsky-2"
hf_url: "https://huggingface.co/kandinsky-community/kandinsky-2-2-decoder"
modelscope_url: ""
project_url: "https://fusionbrain.ai/en/editor"
downloaded: [arxiv-2310.03502.pdf, kandinsky-2--github-readme.md, kandinsky-2--hf-2-2-decoder.md, kandinsky-2--hf-2-2-prior.md, kandinsky-2--hf-2-1.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Kandinsky 2.x 是俄罗斯 Sber AI / AIRI 团队的开源文生图模型，独创性地把 **unCLIP 风格的 diffusion image prior（文本 emb→CLIP 图像 emb）** 与 **latent diffusion（LDM）+ 定制 MoVQ 自编码器** 拼接在一起，全模型 3.3B 参数、Apache 2.0 许可、原生多语言（俄/英）；在 COCO-30K 上取得 **FID 8.03（256×256，linear prior 配置）**，是当时**开源模型中的 SOTA FID**，优于 [[stable-diffusion-2]] 2.1（8.59）与 [[deepfloyd-if]]。

## 背景与定位
2022–2023 年文生图分两条主流路线：像素级级联扩散（[[dall-e-2]] / [[imagen]] / [[glide]]）与潜空间扩散（[[latent-diffusion-ldm]] / [[stable-diffusion-1]]）。Kandinsky 想要"两全其美"——既要 [[dall-e-2]]（unCLIP）那种"先用 image prior 把文本嵌入映射到 CLIP 图像嵌入、再解码"的语义对齐能力，又要 LDM 那种在低维潜空间训练/推理的效率。论文明确写道：他们最初尝试纯多语言文本编码器（mT5 / XLM-R / XLMR-CLIP），但发现**直接用 CLIP-image 嵌入作为条件比单独的文本编码器生成质量更好**，于是采纳 image prior 路线，同时保留 XLM-R 文本嵌入做额外条件。

Kandinsky 的演进脉络（同一 GitHub 仓库内）：
- **Kandinsky 2.0（2022）**：纯多语言 LDM，双文本编码器 mCLIP-XLMR(560M) + mT5-small(146M)，UNet 1.2B，在 1B 多语言图文对上训练。COCO-30K FID 20.00（弱）。
- **Kandinsky 2.1（2023-04）**：首次引入 image prior（unCLIP 思路）+ MoVQ，FID 跳到 **8.21**，质变。
- **Kandinsky 2.2（2023-07）**：把 image prior 的 CLIP 图像编码器从 ViT-L/14（427M）换成 **CLIP-ViT-bigG-14-laion2B（1.8B）**，并加入 ControlNet-depth 支持，分辨率上探到 1024×1024 任意宽高比。
- arXiv 技术报告（2310.03502，2023-10 挂出）正式以"Kandinsky"为名总结这套 image-prior + latent-diffusion 架构与消融。

本页以 **2.1/2.2 + arXiv 技术报告**为主体（worklist date=2023-07 对应 2.2 发布）。

## 模型架构
整体三段式：**文本编码 → 嵌入映射（image prior）→ 潜空间扩散（latent diffusion）→ MoVQ 解码**。是 [[dall-e-2]] 的 unCLIP 范式与 LDM 的工程化融合。

**三个推理/训练阶段**
1. **文本编码（冻结）**：两个文本编码器并用——(a) CLIP-text（带 image prior 映射）；(b) XLM-Roberta-Large（多语言，560M）。两者训练期全程 frozen。
2. **Image Prior（可训练，1B）**：从零训练的 transformer-encoder（diffusion prior），用扩散过程把文本嵌入映射到 CLIP 图像嵌入空间。最优配置：`num_layers=20, num_heads=32, hidden_size=2048`，1D-diffusion 标准 transformer-encoder。关键 trick：对视觉嵌入做**基于全数据集统计量的逐元素归一化（element-wise normalization）**，加速扩散收敛；推理时再做逆归一化还原回原始 CLIP-image 空间。
3. **Latent Diffusion UNet（可训练，1.22B）**：条件信号是 **CLIP-image 嵌入 + CLIP-text 嵌入 + XLMR-CLIP 文本嵌入** 的组合。CLIP-image 与 XLMR-CLIP 嵌入合并后作为 UNet 输入，同时把这些嵌入全部**加到 time-embedding 上**做条件注入。
4. **MoVQ 自编码器（Sber-MoVQGAN，67M，冻结于扩散训练但单独训练）**：定制实现的 MoVQGAN（Modulating Quantized Vectors），latent 32×32、码本 16384。一个**反直觉但重要的设计**：推理时**不跳过自编码器的量化步骤**——保留量化反而提升生成图的多样性与质量。

**参数清单（arXiv Table 2，总 3.3B）**
| 部件 | 参数 | 是否训练 |
|---|---|---|
| Diffusion Mapping（image prior） | 1B | 训练 |
| CLIP image encoder（ViT-L/14；2.2 升为 ViT-bigG-14，1.8B） | 427M | 冻结 |
| CLIP text encoder | 340M | 冻结 |
| Text encoder（XLM-R-L） | 560M | 冻结 |
| Latent Diffusion UNet | 1.22B | 训练 |
| MoVQ image autoencoder | 67M | 冻结（独立训练） |

**2.2 相对 2.1 的架构改动**：image prior 的 CLIP 图像编码器 ViT-L/14 → **CLIP-ViT-bigG-14-laion2B-39B-b160k（1.8B）**；新增 **ControlNet** 机制（释放了 controlnet-depth 权重）；支持 512×512 ~ 1536×1536 多分辨率多宽高比，可出 1024×1024 任意比例。

## 数据
- **Image prior 训练**：LAION Improved Aesthetics（laion_improved_aesthetics_6.5plus），再在 **LAION HighRes** 上 fine-tune。
- **主 Text2Image 扩散模型（2.1）**：基于 **LAION HighRes 的 1.7 亿（170M）图文对**训练，硬性条件是图像分辨率 ≥768×768。注：2.1 之所以只用 170M 对，是因为**直接复用了 Kandinsky 2.0 的 UNet 扩散块**，无需从零训练 UNet。
- **高质量 fine-tune（2.1/2.2 共用）**：在自行从公开来源收集的 **200 万（2M）超高质量高分辨率带描述图像**上单独微调，数据集包含 **COYO、anime、landmarks_russia 等**。
- **MoVQGAN（Sber-MoVQGAN）**：在 **LAION HighRes** 上训练，取得图像重建 SOTA。
- **2.2 微调细节**：因换了 CLIP 模型，image prior 重训，Text2Image 扩散模型仅 **fine-tune 2000 iterations**；训练数据覆盖 512×512 到 1536×1536 多种分辨率与宽高比。
- **安全过滤**：训练集清洗掉标注为 harmful/offensive/abusive 的样本；并对输入文本 prompt 做 abusive 检测。

未披露：完整训练总图像量、各源精确配比、re-captioning / 合成数据细节（论文与 model card 均未给出）。

## 训练方法
- **训练目标**：标准 DDPM/扩散去噪。image prior 是在 CLIP 文本/图像嵌入对上跑 1D 扩散，损失为 **MSE Loss**（论文 Fig.1 标注 image-prior 训练用 MSE）；latent diffusion UNet 在 MoVQ 潜空间上做扩散去噪。
- **多阶段**：①独立训练 Sber-MoVQGAN 自编码器 → ②（2.1）复用 2.0 的 UNet，在 170M LAION HighRes 对上训练潜扩散 → ③在 2M 高质量集上 fine-tune → ④独立训练 image prior（diffusion prior）。2.2 在 2.1 基础上换 CLIP-bigG、重训 prior、UNet 仅微调 2000 步。
- **条件机制**：classifier-free guidance；FID-CLIP 曲线用于挑选最优 guidance-scale。
- **image prior 归一化 trick**：全数据集统计的逐元素归一化，显著加速扩散 prior 收敛。
- **关键消融（arXiv Table 3，COCO-30K 256²）**：对比四种 prior 设计——
  - **No prior（直接用文本嵌入）**：FID 25.92（崩），证明 image prior 不可或缺。
  - **Residual prior（18 个残差 MLP 块）**：FID 8.61，CLIP 0.249。
  - **Linear prior（单一线性层）**：**FID 8.03（最佳 FID）**，CLIP 0.261。
  - **Diffusion prior（transformer，含量化）**：FID 9.86；**最佳 CLIP（0.287）与最佳人评分**。
  - 量化对 FID 影响极小（含量化 9.86 vs 不含 9.87），但作者保留量化以增多样性。
  - 有趣发现：最简单的 linear mapping 反而 FID 最优，暗示 CLIP 文本/图像嵌入空间间可能存在近似线性关系；他们甚至用 500 张猫图训了个 "cat prior" 线性映射，仍能高质量生成（Fig.5）。
- 蒸馏/步数加速：论文未报告 consistency/LCM/ADD 等加速；推理默认 decoder ~50 步（2.2）/100~150 步（2.1）。

## Infra（训练 / 推理工程）
- **算力 / GPU·时 / 并行 / 吞吐 / 混合精度**：论文与 model card **均未披露**训练算力规模、GPU 数量、训练时长、分布式策略等工程细节。
- **推理部署**：PyTorch 实现；HF `diffusers` 原生集成（`AutoPipelineForText2Image` / `KandinskyV22Pipeline`），支持 fp16、`enable_model_cpu_offload`。2.2 默认 decoder 50 步、prior_guidance_scale=1.0，可出 768/1024 分辨率。
- **生产形态**：两条面向用户的推理资源——**FusionBrain 网页图像编辑器**（fusionbrain.ai，含 text2image、inpainting、outpainting、滑窗、擦除、缩放、风格选择，支持俄/英 prompt 与 9:16/2:3/1:1/16:9/3:2 宽高比）与 **Telegram bot**（kandinsky21_bot，含 text2image、图文融合、图像融合、image variations）。
- 量化/缓存等推理加速：未报告。

## 评测 benchmark（把效果讲清楚）
**COCO-30K zero-shot FID（256×256，arXiv Table 1，越低越好）**
| 模型 | FID-30K |
|---|---|
| 开源 | |
| **Kandinsky（Ours, linear prior）** | **8.03** |
| Stable Diffusion 2.1 | 8.59 |
| GLIDE | 12.24 |
| IF（DeepFloyd，作者复现）* | 15.10（原作者报 7.19） |
| Kandinsky 1.0 | 15.40 |
| ruDALL-E Malevich | 20.00 |
| GLIGEN | 21.04 |
| 闭源 | |
| eDiff-I | 6.95 |
| Imagen | 7.27 |
| GigaGAN | 9.09 |
| DALL-E 2 | 10.39 |
| DALL-E | 17.89 |

> 注：HF model card 给出的是 **Kandinsky 2.1 FID 8.21**（口径略异于 arXiv 的 8.03，arXiv 报的是最优 linear-prior 配置）。两个数都来自已落盘一手源，此处如实并列。Kandinsky 是当时开源里 FID 最低者，逼近闭源第一梯队（eDiff-I 6.95 / Imagen 7.27）。

**人评（arXiv Fig.6，DrawBench，共 5000 票）**：盲评对比中 Kandinsky（diffusion prior）vs 各竞品。论文结论是 **diffusion prior 拿到最佳 CLIP score 与最佳人评分**，而 linear prior 拿最佳 FID——即"自动指标最优"与"人感知最优"由不同 prior 配置达成。

**Sber-MoVQGAN 重建质量（arXiv Table 4，ImageNet）**：Sber-MoVQGAN 270M 取得 **FID 0.686 / SSIM 0.741 / PSNR 27.04 / L1 0.0393**，全面超过 ViT-VQGAN（1.28）、RQ-VAE（1.83）、原版 Mo-VQGAN（1.12）、VQ/KL CompVis 等，是图像重建 SOTA——作者指出"图像解码是生成质量的主要瓶颈"，故重点优化自编码器。

未报告：GenEval / T2I-CompBench / DPG-Bench / HPSv2 / ImageReward / PickScore 等后续主流文生图 benchmark（这些 benchmark 多在 Kandinsky 之后才流行，论文未涉及）。

## 创新点与影响
**核心贡献**
1. **首个把 image prior（unCLIP）与 latent diffusion 结合**的文生图架构——既有 [[dall-e-2]] 的语义对齐，又有 LDM 的训练/推理效率。
2. **Sber-MoVQGAN**：定制 MoVQGAN，图像重建 SOTA，单独开源（含 67M/102M/270M 多档），解决"解码瓶颈"。
3. **彻底开源 + Apache 2.0 商用许可**：代码、prior/decoder/inpaint/controlnet 全权重上 HF，是当时开源 t2i 里少有的 SOTA-FID 且可商用者。
4. **原生多语言**（俄/英），XLM-R 文本编码器 + 多语言数据，填补非英语 t2i 空白。
5. **prior 消融的反直觉发现**：线性映射即可达最优 FID，揭示 CLIP 文本/图像嵌入间近线性关系，对后续 unCLIP 类工作有方法论启发。
6. 工程化的多模式 demo（FusionBrain 编辑器 + Telegram bot）：text2image / image fusion / text+image fusion / variations / inpainting / outpainting。

**影响**：Kandinsky 成为俄语圈与开源社区重要的 t2i 基座，被 `diffusers` 一等集成；其 image-prior+LDM+MoVQ 的混合范式是 unCLIP 路线在开源界最完整的复现之一。后续 Kandinsky 3.x 转向更大 LLM 文本编码器 + 纯 LDM（弃 prior），但 2.x 的 MoVQ 与多语言遗产延续。

**已知局限（作者自述）**：①文本-图像语义一致性仍有提升空间；②FID 与人评绝对值仍逊于闭源第一梯队；③安全性无法保证（精心构造的 prompt 仍可能产出不良内容，建议外挂分类器/实时审核层）；④Infra/算力细节、完整数据配比未公开。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2310.03502
- pdf: https://arxiv.org/pdf/2310.03502.pdf
- github: https://github.com/ai-forever/Kandinsky-2
- hf (2.2 decoder): https://huggingface.co/kandinsky-community/kandinsky-2-2-decoder
- hf (2.2 prior): https://huggingface.co/kandinsky-community/kandinsky-2-2-prior
- hf (2.1): https://huggingface.co/kandinsky-community/kandinsky-2-1
- demo: https://fusionbrain.ai/en/editor
- Habr 博文（2.2，俄文）: https://habr.com/ru/companies/sberbank/articles/747446/
- Sber-MoVQGAN: https://github.com/ai-forever/MoVQGAN

## 本地落盘文件
- ../../../sources/omni/2023/arxiv-2310.03502.pdf
- ../../../sources/omni/2023/kandinsky-2--github-readme.md
- ../../../sources/omni/2023/kandinsky-2--hf-2-2-decoder.md
- ../../../sources/omni/2023/kandinsky-2--hf-2-2-prior.md
- ../../../sources/omni/2023/kandinsky-2--hf-2-1.md
