---
title: "LEDITS++: Limitless Image Editing using Text-to-Image Models"
org: "TU Darmstadt / DFKI / hessian.AI / Hugging Face"
country: EU
date: "2023-11"
type: paper
category: edit
tags: [image-editing, real-image-editing, diffusion-inversion, training-free, semantic-guidance, dpm-solver, multi-edit, implicit-masking]
url: "https://arxiv.org/abs/2311.16711"
arxiv: "https://arxiv.org/abs/2311.16711"
pdf_url: "https://arxiv.org/pdf/2311.16711"
github_url: "https://github.com/ml-research/ledits_pp"
hf_url: "https://huggingface.co/spaces/editing-images/leditsplusplus"
modelscope_url: ""
project_url: "https://leditsplusplus-project.static.hf.space/index.html"
downloaded: [arxiv-2311.16711.pdf, ledits-pp--project-page.md, ledits-pp--github-readme.md, ledits-pp--diffusers-doc.md, ledits-pp--tedbench-dataset.md, ledits-pp--space-readme.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
LEDITS++ 是一种**免微调、免优化、无需用户掩码**的真实图像文本编辑方法：核心创新是把"完美反演（perfect inversion，零重建误差）"从 DDPM 推广到高阶 SDE 求解器 **sde-dpm-solver++**，使整套编辑（反演+生成）仅需约 **20 步**完成；同时支持**多概念同时编辑**且通过**隐式掩码**把改动限制在相关区域。在 TEdBench++ 上以 SD-XL 取得 **87% 编辑成功率（SR）**、LPIPS 0.34，且单次编辑仅 **1.78 秒**（A100），比此前 DDPM 反演快约 6 倍、比 Imagic 快近 200 倍。CVPR 2024 收录。

## 背景与定位
真实图像编辑的难点：要在"忠实保留原图"与"按指令改动"之间取舍。论文指出此前方法的三类痛点：
1. **低效**：Imagic[18]、UniTune[44] 需对每张输入图微调模型；Null-text Inversion[28]、Pix2Pix-Zero[30] 需逐步优化纠错。
2. **不精确**：SDEdit[26] 加噪重生成会大幅偏离原图；DDIM 反演[42]误差逐步累积，开启 CFG 后重建质量进一步恶化。
3. **versatility 受限**：几乎所有方法都无法**同时**编辑多个任意概念。

LEDITS++ 站在两条技术脉络的交汇点：
- **反演脉络**：DDIM 反演 → Null-text/Pix2Pix-Zero（带优化纠错）→ Edit-friendly DDPM[17]（Huberman-Spiegelglas 等，DDPM 噪声空间零误差反演但需 100 步）→ **LEDITS++（把零误差反演性质迁移到高阶 SDE 求解器，步数大降）**。
- **语义控制脉络**：作者团队自家的 **SEGA**[5]（Semantic Guidance，操纵噪声估计实现语义控制）与 **Safe Latent Diffusion**[39] 的思想，被搬到真实图像编辑场景，并叠加交叉注意力掩码（如 Prompt-to-Prompt[14]、DiffEdit[9]）。

定位一句话：**LEDITS++ = 高效完美反演（继承 [[edit-friendly-ddpm-inversion]] 的零误差性质 + DPM-Solver++ 的少步数）+ 多概念语义引导（源自 SEGA）+ 隐式掩码（交叉注意力 ∩ 噪声图）**。相关前置工作：[[ddpm]] [[ddim]] [[latent-diffusion-ldm]] [[dpm-solver]] [[sdedit]] [[imagic]] [[prompt-to-prompt]] [[diffedit]] [[sega]] [[sdxl]]。

## 模型架构
LEDITS++ **不是一个新模型，而是一个 inference-time 编辑算法**，架构无关（architecture-agnostic）——可叠加在任意预训练扩散模型上，无需训练任何参数。

- **Backbone**：复用底座 DM 的 **U-Net** 噪声预测网络 ε̂θ。论文与官方仓库给出三套底座实现：
  - 潜空间模型：**Stable Diffusion 1.5**（`runwayml/stable-diffusion-v1-5`）与 **SD-XL**（`LEditsPPPipelineStableDiffusion` / `LEditsPPPipelineStableDiffusionXL`）。
  - **像素空间模型**：**DeepFloyd-IF**（官方仓库 `IFDiffusion_LEDITS`），用以实证"latent 与 pixel-based 通吃"的架构无关性。
- **Tokenizer / VAE / text encoder**：全部沿用底座（SD 用 VAE + CLIP，SDXL 用双 CLIP，IF 用 T5 + 像素空间），LEDITS++ 本身不引入新组件。
- **条件注入机制（核心三件套）**：
  1. **Component 1 — 完美反演**：给定输入图 x0，构造一条**统计独立**的辅助重建序列 x1..xT（式 6：xt = √ᾱt·x0 + √(1−ᾱt)·ε̃t，ε̃t ~ N(0,I) 相互独立——这点不同于前向扩散里相邻 εt 强相关），再从 sde-dpm-solver++（二阶/多步变体）反解出每步随机量 zt（式 7）。多步变体每个时间步只需**一次** U-Net 评估（复用上一步估计）。可提前在中间步 t∈[0.8T, 0.9T] 停止反演并从该步起编辑，进一步省步。
  2. **Component 2 — 文本编辑**：对每个编辑概念 ei 单独构造引导项 γ（式 8–11）。单概念时 ε̂θ(xt,ce)=ε̂θ(xt)+γ；γ=0 即完美重建原图。γ = ϕ·ψ，其中 ψ 是条件与无条件噪声估计之差 ε̂θ(xt,ce)−ε̂θ(xt)（正向引导用 +，负向用 −，从而"加概念/去概念"对称可控）；ϕ 是带尺度 se 的掩码。**多概念**时各 γti 用各自的 λi、se^i 独立计算后相加（式 11），互不干扰。单概念且 ϕ=se 退化为标准 CFG（式 4）。
  3. **Component 3 — 语义接地（隐式掩码）**：ϕ = se·M¹·M²（式 12）。
     - **M¹（交叉注意力掩码）**：用编辑提示 ei 跑一次 U-Net，取最小分辨率（SD 为 16×16）交叉注意力图，跨所有 head/layer 平均、对所有编辑 token 求和得 Aet，上采样到 xt 尺寸，取第 λ 百分位阈值二值化（式 13）。复用 Component 2 已有的前向评估，**几乎零额外开销**。
     - **M²（噪声掩码）**：直接取引导向量 ψ 的最大绝对值区域（式 14），捕捉物体轮廓/边缘，粒度更细。
     - 两掩码**逐点相乘取交集**：M¹ 接地强但粗，M² 细粒度，交集兼得"对的区域 + 细边界"。λ 越小掩码越大（风格迁移类全图改动用 λ→0；局部物体编辑用与物体占比成比例的 λ）。

## 数据
**LEDITS++ 本身无需训练数据**（零参数方法）。涉及的数据仅用于**评测**：
- **重建误差实验**：从 COCO 2017 validation 随机采 100 张图，在 64×64 latent 上算 RMSE（因 SD VAE 本身有重建误差，故在 latent 而非像素层评估）。
- **隐式掩码质量实验**：COCO panoptic segmentation，去重后 **4983 张图、29307 个分割物体**，用类别标签（如 'person'/'TV'）当编辑概念，按 bbox 相对大小估 λ。
- **多概念编辑实验**：CelebA 中前 100 张不含任一目标属性的人脸；5 属性（glasses/smile/hat/wavy hair/earrings）中每次同时编 3 个 → 10 种组合 × 10 seed × 100 图 = **每方法每超参 10000 张、累计超 100 万张**评估图。
- **TEdBench(++)**：原 TEdBench[18]（Imagic 配套，100 图+编辑指令）→ 作者修订为 **TEdBench++（120 条）**，修正拼写（如 "enterance"→"entrance"，因 tokenizer 会切出完全不同的 token）、消歧（"a standing animal" 已经站着 → 改成更难的 "an {animal} standing on hind legs"），并新增此前缺失的任务类型：**多条件、物体/概念移除、风格迁移、复杂替换**。数据集开源于 `AIML-TUDA/TEdBench_plusplus`（Apache-2.0），含原图、LEDITS++ 编辑结果及复现参数 csv。
- 底座 DM 的训练数据未在本文涉及；论文在 societal impact 部分提到底座模型训练于 LAION-5B[40] 等网络数据，会带入偏见。

## 训练方法
**无任何训练 / 微调 / 优化**——这是方法的核心卖点。LEDITS++ 是纯 inference-time 算法：
- 不像 InstructPix2Pix[6] 那样大规模续训 DM；
- 不像 Imagic[18]/UniTune[44] 那样对每张输入图微调（Imagic 配置：1000 步文本嵌入优化 lr 2e-3 + 1500 步模型微调 lr 5e-7）；
- 不像 Null-text Inversion / Pix2Pix-Zero 那样做逐步优化纠错。

唯一的"训练目标"概念来自底座 DM 已学好的 ε-prediction + **classifier-free guidance**[16]；LEDITS++ 在此之上以解析方式重写引导项（式 8–14）。关键**超参**（论文附录 C 给出复现配置）：
- 反演 20 步 + 生成 20 步，λ=0.1，skip 在 t=0.75T；
- 多概念实验网格搜索：skip 0.2–0.3、引导尺度 10–15、阈值 0.7–0.9。
- 无蒸馏/无 consistency/LCM；其"少步数"完全来自高阶 SDE 求解器本身（dpm-solver++）而非步数蒸馏。

## Infra（训练 / 推理工程）
- **训练算力**：无（零训练）。
- **推理硬件**：全部 runtime 测于单张 **NVIDIA A100-SXM4-40GB**；diffusers 实现版本 0.20.2，底座 SD 1.5。
- **推理效率（论文表 1，"oilpainting" 风格迁移代理任务，100 次平均）**：
  - LEDITS++：**1.78 ±0.03 s**，重建误差 **0.00**（完美反演）。
  - Edit-friendly DDPM[17]：10.36 s（误差 0.00）；DiffEdit 27.65 s；DDIM 反演 37.23 s；Pix2Pix-Zero 56.78 s；Imagic 349.98 s；SDEdit 2.10 s（但误差 0.81，质量差）。
  - 相对 DDIM 反演 **21×** 加速；相对 DDPM 反演 **6×**；与最快但质量差的 SDEdit 持平。
  - 关键工程点：LEDITS++ 40 步总流程只需 **60 次** U-Net 评估（反演每步 1 次无条件 + 生成每步无条件&条件各 1），而 SDEdit 同 40 步却要 80 次评估，故 LEDITS++ 反而比 SDEdit 还快。
- **部署形态**：已**完整集成进 🤗 diffusers**（`LEditsPPPipelineStableDiffusion(XL)`，含 `.invert()` 与 `.__call__()`）；另有官方独立仓库 `ml-research/ledits_pp`（含 SD/SDXL/DeepFloyd-IF 三套 + 自定义 `DPMSolverMultistepSchedulerInject`，`algorithm_type="sde-dpmsolver++"`, `solver_order=2`）。**注意**：diffusers 版因 `DPMSolverMultistepScheduler` 的向后兼容问题**不再保证完美反演**（应用层影响通常可忽略，但做研究建议用官方仓库版）。提供 Colab + HF Space 在线 demo。

## 评测 benchmark（把效果讲清楚）
所有数字均来自论文（已落盘 PDF），未报告项明确标注。

**1. 效率与重建（表 1，SD1.5，A100）**——见上 Infra 节：LEDITS++ 重建 RMSE=0.00、1.78s，且是表中**唯一同时**具备 variation/sampling、semantic grounding、multi-editing 三项能力的方法。

**2. 隐式掩码质量（图 4，COCO panoptic，IoU 越高越好）**：交叉注意力掩码 M¹ ∩ 噪声掩码 M² 的**交集**明显优于任一单独掩码，且接近专用分割模型 **CLIPSeg**[24] 的水平，优于 **DiffEdit**[9] 的掩码——而 LEDITS++ 掩码是推理时隐式算出、几乎零开销。（论文给的是曲线图，未列单一标量数值。）

**3. 多概念人脸编辑（图 5，CelebA，同时编 3 属性，CLIP↑ vs LPIPS↓ 权衡）**：LEDITS++ 最靠近"左上角理想区"（高 CLIP 对齐 + 低 LPIPS 偏离）。只有 edit-friendly DDPM 与 LEDITS++ 能稳定达到平均 **CLIP ≈ 0.25** 的上限（每属性都正确编辑）；Pix2Pix-Zero、Imagic 在此复杂任务常"崩"（漏编辑或大改原图）。

**4. TEdBench / TEdBench++（表 2，成功率 SR↑ / LPIPS↓，人评）**：
| 方法 | 底座 | TEdBench SR | TEdBench LPIPS | TEdBench++ SR | TEdBench++ LPIPS |
|---|---|---|---|---|---|
| Imagic | SD1.5 | 0.55 | 0.56 | 0.58 | 0.57 |
| **LEDITS++** | SD1.5 | **0.75** | **0.28** | **0.79** | **0.30** |
| Imagic | Imagen | 0.83 | 0.59 | — | — |
| **LEDITS++** | SD-XL | **0.84** | **0.33** | **0.87** | **0.34** |

要点：同底座（SD1.5）对比 Imagic，LEDITS++ SR 高约 20 个百分点、LPIPS 几乎减半；用 SD-XL 时（0.84 SR）已超过 Imagic 配 Imagen（0.83 SR）这一更强组合，且 LPIPS 远低（0.33 vs 0.59，即对原图忠实度高得多）。作者注：Imagic 常"生成一张全新图"而无视原图，故其 LPIPS 高。

**消融/关键结论**：(a) 完美反演是低 LPIPS 的根源（不编辑时精确还原原图）；(b) 隐式掩码交集 > 单掩码；(c) 编辑尺度 se 与概念视觉强度（如"微笑"程度）**单调**对应，可直观调节（附录 B 图 8）；(d) 编辑质量强依赖底座能力——SD-XL > SD1.5，且底座不会画的姿态（如"坐着的长颈鹿")会编辑失败（局限）。

**奖项**：项目页披露该工作在 **CVPR GenAI Media Generation Challenge Workshop** 获**第二名**。

## 创新点与影响
**核心贡献**：
1. **dpm-solver++ 的完美反演推导**——首次把 Edit-friendly DDPM 的"零重建误差 + edit-friendly 噪声空间（ε̃t 统计独立）"性质迁移到高阶多步 SDE 求解器，使真实图像编辑从上百步压到 **~20 步**、单图 1.78 秒，把"反演式编辑"在效率上拉到与最快近似法（SDEdit）同档却质量无损。
2. **唯一原生支持多概念隔离编辑**——每个编辑概念独立的引导项 + 独立隐式掩码（式 11–12），互不干扰，这是表 1 中所有对比法都不具备的能力。
3. **隐式掩码 = 交叉注意力 ∩ 噪声图**——零额外开销地获得接近 CLIPSeg 的语义接地，且能定位"图中尚不存在的待添加概念"区域。
4. **架构无关**——同一算法通吃 latent（SD/SDXL）与 pixel-based（DeepFloyd-IF）扩散模型。
5. **TEdBench++ 基准**——修订并扩展（120 条，新增多条件/移除/风格/复杂替换），并开源 LEDITS++ 的参考编辑结果，为后续真实图像编辑方法提供更严谨 testbed。

**影响**：作为**训练-free、tuning-free、mask-free** 的实用编辑方案，已并入 diffusers 主线（`LEditsPP*` 管线），成为社区做"一行代码真实图编辑"的常用基线；其"完美反演 + 语义引导 + 隐式掩码"的组合思路被后续无训练编辑工作广泛参考。

**已知局限（论文 Discussion）**：
- **强依赖底座**：底座 DM 没有的概念/姿态无法编辑；更强底座（SDXL）才有更好效果。
- **物体身份保持权衡**：隐式掩码保住整体构图，但掩码区域内的物体身份可能改变（尤其泛化提示如 "a standing cat" + 强超参时）；Imagic 类微调法则相反——保身份但改背景。缓解可用更具描述性的提示或 textual inversion[12]。
- 自动掩码无法总是猜中用户意图；可选地支持注入用户掩码（附录 F）。
- 社会影响：底座模型的偏见会传导到编辑；可被用于伪造/不当内容，作者呼吁审慎部署，并指出 LEDITS++ 亦可反向用于去偏/数据增广。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2311.16711
- arxiv_pdf: https://arxiv.org/pdf/2311.16711
- project_page: https://leditsplusplus-project.static.hf.space/index.html
- github (官方独立实现，保证完美反演): https://github.com/ml-research/ledits_pp
- diffusers 集成文档: https://github.com/huggingface/diffusers/blob/main/docs/source/en/api/pipelines/ledits_pp.md
- HF Demo Space: https://huggingface.co/spaces/editing-images/leditsplusplus
- TEdBench++ 数据集: https://huggingface.co/datasets/AIML-TUDA/TEdBench_plusplus

## 本地落盘文件
- ../../../sources/omni/2023/arxiv-2311.16711.pdf （CVPR 2024 / arXiv v2 全文+附录，已精读）
- ../../../sources/omni/2023/ledits-pp--project-page.md （官方项目页快照）
- ../../../sources/omni/2023/ledits-pp--github-readme.md （ml-research/ledits_pp README）
- ../../../sources/omni/2023/ledits-pp--diffusers-doc.md （diffusers 官方管线文档）
- ../../../sources/omni/2023/ledits-pp--tedbench-dataset.md （TEdBench++ 数据集卡）
- ../../../sources/omni/2023/ledits-pp--space-readme.md （HF Space 配置 stub）
