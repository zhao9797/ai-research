---
title: "Stable Diffusion Inpainting / img2img (SD v1.5 编辑权重)"
org: "Runway / Stability AI / CompVis"
country: EU
date: "2022-10"
type: model-card
category: edit
tags: [stable-diffusion, inpainting, img2img, sdedit, latent-diffusion, editing, open-weights, runway]
url: "https://huggingface.co/runwayml/stable-diffusion-inpainting"
arxiv: "https://arxiv.org/abs/2112.10752"
pdf_url: "https://arxiv.org/pdf/2112.10752"
github_url: "https://github.com/runwayml/stable-diffusion"
hf_url: "https://huggingface.co/runwayml/stable-diffusion-inpainting"
modelscope_url: ""
project_url: "https://runwayml.com/"
downloaded:
  - sd-inpainting--runwayml-card.md
  - sd-v1-5--hf-card.md
  - sd-runway--github-readme-archive.md
  - sd-compvis--github-readme.md
  - sd-inpaint--diffusers-doc.md
  - sd-img2img--diffusers-doc.md
  - arxiv-2112.10752.pdf
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Runway/Stability/CompVis 在 2022-10 随 SD v1.5 一起发布的**开源局部重绘（inpainting）与图生图（img2img）能力**：img2img 是把 [[sdedit]] 的"加噪—去噪"机制直接套在 SD 上（一个 `strength` 旋钮，无需新训练），inpainting 则是给 UNet **加 5 个输入通道**（4 路掩码图 latent + 1 路掩码）并用合成掩码再训练 44 万步得到的专用权重；其 inpainting 在 LaMa 评测协议下取得 **FID 1.00 / LPIPS 0.141**，优于 LDM-inpaint(1.50)、CoModGAN(1.82)、LaMa(2.21)。它让开源生态第一次拿到**即用的局部重绘 + 图生图编辑权重**，奠定了 SD 编辑工作流（Erase & Replace / outpainting / ControlNet 上游）。

## 背景与定位
2022-08 [[latent-diffusion-ldm]] 衍生出的 Stable Diffusion v1.4 把高质量文生图开源化，但社区拿到的只是 **txt2img**——无法对已有图做受控编辑。本工作补齐编辑这一环，分两条腿：

- **img2img（图生图 / 图像改写）**：不需要任何新权重，复用 [[sdedit]]（Meng et al. 2021, arXiv 2108.01073）提出的 *Stochastic Differential Editing*——对输入图加噪到中间时刻 `t`，再用文生图先验去噪。一个 `strength∈[0,1]` 控制加噪量：越接近 1 变化越大、与原图语义越不一致，越接近 0 越保真。CompVis 上游 README 早已用 `scripts/img2img.py --init-img ... --strength 0.8` 演示"草图→精细画作"。这条路只是采样脚本，**所有 SD 权重通用**。
- **inpainting（局部重绘 / 文本擦除-替换）**：上游 LDM 论文已证明 latent diffusion 可做 inpainting（§4.5，沿用 [[lama]] 的 Places 评测协议），但 SD 没有发布对应权重。Runway 训练并开源了 `sd-v1-5-inpainting.ckpt`，把"按掩码 + 文本擦除并重绘"做成一等公民。Runway 同时上线了产品化的 **Erase & Replace** 工具。

相对前置工作的改进：相较"latent blending"式的免训练 inpaint（用普通 txt2img 权重在掩码区做潜变量混合，diffusers 称 legacy 方案），本专用权重在掩码边界一致性与填充质量上更强（diffusers 官方文档明确推荐用 inpainting 专用 checkpoint）；相较 [[lama]]/CoModGAN 这类 GAN/FFC 专用修复网络，它带文本条件、可"按提示重绘"，且 FID 更低。

> 时间线（原 runwayml/stable-diffusion README 的 News）：**2022-10-18 Inpainting Model**；**2022-10-20 v1.5 Text-to-Image Checkpoint**。

## 模型架构
整体沿用 SD v1 / [[latent-diffusion-ldm]] 的三件套，**编辑能力是在此之上的最小改动**：

- **Backbone**：860M 参数 **UNet**（潜空间扩散，cross-attention 注入文本）。
- **VAE / tokenizer**：下采样因子 **f=8** 的连续 VAE，把 H×W×3 图编码成 H/8×W/8×**4** 通道 latent（非 VQ，是 KL-reg 连续 latent）。
- **Text encoder**：冻结的 **CLIP ViT-L/14**（约 123M），取其非池化（non-pooled）token 序列经 cross-attention 进 UNet——这一"用冻结 CLIP 文本编码器"的设计借鉴 [[imagen]]。
- **分辨率策略**：原生 512×512（v1 先在 256² 预训练再在 512² 微调）。
- **inpainting 的关键架构改动**：把 UNet 的**输入通道从 4 扩到 9**——新增 **5 个通道 = 4（被掩码图像经 VAE 编码后的 latent）+ 1（下采样到 latent 分辨率的掩码本身）**。这 5 个新通道对应的卷积权重在恢复非 inpainting checkpoint 后**零初始化（zero-init）**，保证训练起点等价于原模型、不破坏已学到的生成能力。条件注入方式：掩码图 latent 与掩码沿通道维 concat 到带噪 latent 上，连同文本 cross-attention 一起喂 UNet。这是 concat-conditioning（密集条件）而非 cross-attention 条件。
- **img2img 无架构改动**：直接用 txt2img 的 UNet，差别只在采样起点（从"加噪后的输入图 latent"而非纯高斯噪声起步）。

## 数据
- **基座数据（v1.x 全系）**：**LAION-2B(en)** 及其子集。逐 checkpoint 的数据/步数（来自官方 README / model card）：
  - sd-v1-1：256² 上 laion2B-en 训 237k 步 + 512² 上 laion-high-resolution（LAION-5B 中分辨率 ≥1024² 的 170M 样本）训 194k 步。
  - sd-v1-2：从 v1-1 续训，512² 上 **"laion-improved-aesthetics / laion-aesthetics v2 5+"** 训 515k 步（该子集：原始尺寸 ≥512²、美学分 >5.0、水印概率 <0.5；美学分用 LAION-Aesthetics Predictor V2 估计）。
  - sd-v1-5：从 v1-2 续训，512² 上 "laion-aesthetics v2 5+" 再训 **595k 步**，10% 文本条件 dropout（为 CFG）。
- **inpainting 训练数据**：仍是 **"laion-aesthetics v2 5+"**，512²；关键在掩码合成——**训练时程序化生成合成掩码（synthetic masks），并以 25% 概率"全图掩码"（mask everything）**，使模型既能补小块也能从近乎空白重绘。
- **过滤/安全**：美学过滤 + 水印概率过滤已在基座完成；无额外去重（model card 明示存在记忆/复制风险）；推理脚本带 Safety Checker 与不可见水印。re-captioning：v1 系列**未做**（直接用 LAION 原始 alt-text），这也是后续 SDXL/DALL·E 3 重点改进处。

## 训练方法
- **训练目标**：标准 DDPM 风格的潜空间扩散——在 VAE latent 上对加噪 latent 做噪声预测（ε-prediction）重建损失。**不是** flow matching，也无蒸馏（2022 年 SD 还在多步采样时代）。
- **多阶段**：基座是"256² 预训练 → 512² 微调 → 美学子集续训"。inpainting 是在 **v1-5 之上再续训 440k 步**（恢复非 inpaint checkpoint → zero-init 5 个新通道 → 用合成掩码继续训）。
  - 注：官方源对 inpaint 谱系的措辞有两种写法但可调和——inpainting model card 的训练表写 `sd-v1-5-inpaint.ckpt: Resumed from sd-v1-2.ckpt. 595k steps ... Then 440k steps of inpainting`（即从 v1-2 起，先跑完 595k 等价于 v1-5、再跑 440k inpaint），而 v1-5 base card 与原 Runway GitHub README 直接写 `sd-v1-5-inpainting.ckpt: Resumed from sd-v1-5.ckpt`（再训 440k 步）。二者本质一致（v1-5 = v1-2 + 595k），结论：**inpaint 权重 = v1-5 之上再续训 440k 步**。
- **CFG**：训练时 10% 丢弃文本条件，以支持 classifier-free guidance（[[classifier-free-guidance]]）；推理默认 guidance scale 7.5。
- **超参（来自 model card）**：Optimizer **AdamW**；Gradient Accumulation **2**；全局 batch **32×8×2×4 = 2048**；学习率 **10k 步 warmup 到 1e-4 后恒定**；EMA 权重（v1 推理 config 用 EMA-only checkpoint）。
- **采样器**：参考脚本用 **PLMS**（50 步），亦支持 DDIM；img2img 用 SDEdit 的部分加噪起点 + 同样的去噪采样。
- **img2img 无训练**：纯推理技巧，`strength` 决定加噪深度 → 决定保留多少原图结构。

## Infra（训练 / 推理工程）
- **算力（model card 披露）**：**32 × 8 = 256 张 A100**（A100 PCIe 40GB）；估算总用时约 **150,000 GPU·小时**（v1 系列全程，AWS us-east），对应约 11,250 kg CO2eq。具体到 inpainting 这 440k 步单独的 GPU·时未单列。
- **精度/吞吐**：混合精度（`--precision autocast`）；具体并行/吞吐数字未披露（这是开放权重发布而非系统论文，infra 细节有限）。
- **推理形态**：860M UNet + 123M CLIP，**≥10GB VRAM 即可跑**，是当时"消费级可跑"的核心卖点。官方提供：CompVis/Runway 参考脚本（`txt2img.py` / `img2img.py` / `inpaint_st.py` streamlit demo，config `v1-inpainting-inference.yaml`）+ **🧨 diffusers** 集成（`StableDiffusionImg2ImgPipeline` / `StableDiffusionInpaintPipeline`，支持 fp16 revision、attention slicing、xformers memory-efficient attention）。
- **部署/生态**：权重以 OpenRAIL-M 许可开源；很快被 AUTOMATIC1111 WebUI、ComfyUI、InvokeAI、SD.Next 等接入，成为开源编辑工作流默认底座。Runway 侧有云端 Erase & Replace 产品。

## 评测 benchmark（把效果讲清楚）
**inpainting 定量评测**（model card / GitHub README，沿用 [[latent-diffusion-ldm]] 论文的评测协议；因模型接受文本，固定 prompt = *"photograph of a beautiful empty scene, highest quality settings"*）：

| Model | FID ↓ | LPIPS ↓ |
|---|---|---|
| **Stable Diffusion Inpainting** | **1.00** | 0.141 (±0.082) |
| Latent Diffusion Inpainting | 1.50 | 0.137 (±0.080) |
| CoModGAN | 1.82 | 0.15 |
| [[lama]] | 2.21 | 0.134 (±0.080) |

- **结论**：SD-Inpainting 的 **FID 最低（1.00）**，显著优于 LDM-inpaint(1.50)、CoModGAN(1.82)、LaMa(2.21)；LPIPS（与未掩码原图差异）略高于 LaMa/LDM——说明它在"画面整体真实度/质量"上领先，在"逐像素贴近原图"上与专用修复网络相当或略松（文本重绘本就允许更大改写空间）。
- **基座 txt2img 评测**：v1-1→v1-5 用不同 CFG scale（1.5–8.0）+ 50 步 PLMS、COCO2017 验证集 10000 随机 prompt、512² 评估，给出相对改进的 Pareto 曲线（model card 明示**未针对 FID 优化**，只展示版本间相对提升，未给绝对 FID 数）。
- **img2img**：官方未提供独立定量 benchmark（它是 SDEdit 的应用，效果以定性"草图→画作"示例呈现）；SDEdit 原论文报告其在真实度/满意度上较 GAN 基线人评胜出最高 98.09%/91.72%（见 [[sdedit]]，非本权重直接复现）。
- **消融**：inpainting 的关键设计消融（5 通道 concat、zero-init、25% mask-everything）由 model card 以方法描述给出，但未提供逐项 ablation 表；上游 LDM 论文 §4.5 / Tab.6-7 对 latent inpainting 的 first-stage 设计（LDM-1 vs LDM-4、KL vs VQ、是否带 attention）做了效率与 FID 消融，是本权重的方法论依据。

## 创新点与影响
**核心贡献**
1. **把"编辑"补进开源文生图栈**：img2img（免训练，SDEdit 套壳 + `strength` 旋钮）+ inpainting（专用权重）两条编辑路径，让 SD 从"只会生成"变成"能改图"。
2. **inpainting 的工程范式**：UNet **输入通道 4→9（+4 掩码图 latent +1 掩码）、新通道 zero-init、合成掩码 + 25% 全掩码**——这套"加通道 + concat 条件 + zero-init"成为后续可控生成（[[controlnet]] 的 zero-conv、SDXL inpaint、各类 brushnet/powerpaint）反复借用的模板。
3. **产品化**：Runway 的 Erase & Replace 把局部重绘做成面向创作者的工具，验证了编辑能力的产品价值。

**影响**
- 成为开源图像编辑工作流（A1111/ComfyUI/InvokeAI）的事实底座；outpainting、对象移除/替换、迭代精修都建立在它之上。
- diffusers 把 `StableDiffusionInpaintPipeline` / `Img2ImgPipeline` 标准化，后续 SD2-inpaint、SDXL-inpaint 沿用同一接口与 9 通道思路。
- 与 [[dreambooth]] / [[textual-inversion]] / [[instructpix2pix]] / [[controlnet]] 共同构成 2022-2023 的 SD 编辑/定制生态。

**已知局限**
- 非完美写实、不会渲染清晰文本、组合性弱（"红方块在蓝球上"易错）、人脸常失真；多语言弱（英文为主）；VAE 有损；LAION 数据未去重 → 存在记忆/复制与偏见风险（model card 直言不宜直接商用产品化，需额外安全机制）。
- img2img 的 `strength` 是单旋钮，保真 vs 变化二选一，无区域级精细控制（后由 ControlNet/IP-Adapter 等补强）。
- inpainting 仍是多步采样（2022 年无步数蒸馏），实时性有限。
- **生态事件**：原 `runwayml/stable-diffusion` GitHub 仓库与 runwayml HF 组织后被弃用/下架，权重现以 `sd-legacy/stable-diffusion-inpainting`、`stable-diffusion-v1-5/*` 等镜像维护（本页 GitHub 内容取自 2022-11 Wayback 快照）。

## 原始链接
- hf (inpainting model card): https://huggingface.co/runwayml/stable-diffusion-inpainting （镜像 https://huggingface.co/sd-legacy/stable-diffusion-inpainting）
- hf (v1-5 base card): https://huggingface.co/sd-legacy/stable-diffusion-v1-5
- github (原 Runway 仓库, 已下架; Wayback 2022-11-02 快照): https://web.archive.org/web/20221102205559/https://github.com/runwayml/stable-diffusion
- github (CompVis 上游, img2img/SDEdit 原始脚本): https://github.com/CompVis/stable-diffusion
- diffusers doc (inpaint pipeline): https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/inpaint
- diffusers doc (img2img pipeline): https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/img2img
- paper (LDM 架构与 inpainting 评测协议来源): https://arxiv.org/abs/2112.10752
- sdedit (img2img 方法原始论文): https://arxiv.org/abs/2108.01073

## 本地落盘文件
- ../../../sources/omni/2022/sd-inpainting--runwayml-card.md
- ../../../sources/omni/2022/sd-v1-5--hf-card.md
- ../../../sources/omni/2022/sd-runway--github-readme-archive.md
- ../../../sources/omni/2022/sd-compvis--github-readme.md
- ../../../sources/omni/2022/sd-inpaint--diffusers-doc.md
- ../../../sources/omni/2022/sd-img2img--diffusers-doc.md
- ../../../sources/omni/2022/arxiv-2112.10752.pdf
