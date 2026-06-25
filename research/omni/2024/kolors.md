---
title: "Kolors（可图）: Effective Training of Diffusion Model for Photorealistic Text-to-Image Synthesis"
org: "Kuaishou（快手 Kolors 团队）"
country: China
date: "2024-07"
type: tech-report
category: t2i
tags: [t2i, latent-diffusion, unet, sdxl, chatglm, bilingual, chinese-text-rendering, recaption, open-source]
url: "https://github.com/Kwai-Kolors/Kolors"
arxiv: ""
pdf_url: "https://github.com/Kwai-Kolors/Kolors/blob/master/imgs/Kolors_paper.pdf"
github_url: "https://github.com/Kwai-Kolors/Kolors"
hf_url: "https://huggingface.co/Kwai-Kolors/Kolors"
modelscope_url: "https://modelscope.cn/models/Kwai-Kolors/Kolors"
project_url: "https://kwai-kolors.github.io/"
downloaded: [kolors.pdf, kolors--readme.md, kolors--hf-modelcard.md, kolors--teampage.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Kolors（可图）是快手开源的中英双语写实文生图潜空间扩散模型：在 SDXL 同款 U-Net backbone 上，把文本编码器换成 **ChatGLM3-6B-Base**（自回归 LLM）、用 **CogVLM 重写训练 caption**、配合**两阶段训练 + 自研高分辨率噪声调度**，在自建 KolorsPrompts 人评上**总体满意度 3.59 居首、视觉吸引力 3.99 居首（超 SD3/DALL·E 3/Playground-v2.5，并略超 Midjourney-v6 的 3.92）**，且强在中文语义与中文文字渲染。

## 背景与定位
2024 年的开源 T2I（[[sdxl]]、[[pixart-alpha]]、SD3）大多用 CLIP/T5 系英文编码器，**无法直接理解中文 prompt**；已有中文方案（AltDiffusion、PAI-Diffusion、Taiyi-XL、[[hunyuan-dit]]）仍依赖 CLIP/多语 mT5 做中文编码——而多语 T5 训练语料里中文占比不足 2%，bilingual CLIP 文本嵌入也撑不起复杂长 prompt。Kolors 的判断是：**问题出在文本编码器**，而非 backbone。

技术脉络上 Kolors 站在 [[latent-diffusion-ldm]]/[[sdxl]] 的 U-Net 路线上（论文明言「优化更先进的 backbone 不在本研究范围」，刻意不上 DiT），把创新集中在三处：(1) 用真正双语预训练的 GLM 系 LLM 当文本编码器；(2) 仿 DALL·E 3 用 MLLM 重写 caption 提升 prompt 遵循；(3) 两阶段数据/训练 + 高分辨率噪声调度提升美学。定位是「**用经典 U-Net 也能做到 Midjourney-v6 级视觉效果**」，并把代码与权重全开源以推动中文 T2I 生态。论文结尾预告后续会出 ControlNet/IP-Adapter/LCM 插件，以及一个基于 Transformer（DiT）的新版闭源模型——即后来的 Kolors 2.x 路线。

## 模型架构
- **Backbone**：严格沿用 [[sdxl]] 的 latent U-Net 架构（潜空间扩散，VAE 编码到 latent 后做去噪），论文强调方法对各类扩散模型通用、不限于 latent U-Net。
- **文本编码器（核心创新）**：用开源 **ChatGLM3-6B-Base** 替换 CLIP/T5。GLM 是基于「自回归空白填充（autoregressive blank infilling）」目标的双语（中英）预训练语言模型，论文称其在自然语言理解/生成上显著优于 BERT 与 T5。选 **Base 版而非 Chat 版**做文本表示（Base 更适合表征，经过人类偏好对齐的 Chat 版反而在文字渲染上更强——论文给出此区分）。ChatGLM3 预训练用了超 **1.4 万亿双语 token**，中文理解力强。取 ChatGLM3 的**倒数第二层（penultimate）输出**作文本表示（沿用 SDXL 取倒数第二层的做法）。
- **文本长度**：相比 CLIP 的 77 token，Kolors 直接把文本长度设到 **256 token**，且因 ChatGLM3 本身支持长文本，扩展到更长也容易——这是它能吃复杂长 prompt 的关键。
- **条件注入**：沿用 LDM/U-Net 的 cross-attention 注入文本条件（论文未对注入方式单独改造，重点在编码器替换）。
- **分辨率策略**：低分辨率概念学习阶段用 512，高分辨率质量提升阶段用 1024，人评统一在 **1024×1024**；高分阶段用 **NovelAI 的分桶采样（bucketed sampling）** 支持多种长宽比，且分桶仅在高分阶段启用以省训练资源。
- **参数量**：FID 对比表（Table 4）标注 Kolors 为 **2.6B**——量级与 SDXL U-Net 一致，推测指 U-Net 主体（文本编码器 ChatGLM3-6B 应另算，但论文未明示该 2.6B 是否含编码器）。
- **推理调度器（来自 HF/diffusers 卡）**：默认 `EulerDiscreteScheduler`，推荐 guidance scale=5.0、50 步；也支持 `EDMDPMSolverMultistepScheduler`（guidance 5.0、25 步）。

## 数据
- **规模**：在「数十亿（billions）」图文对上训练（README/技术报告口径一致）。
- **来源**：概念学习阶段数据来自公开数据集（**LAION、DataComp、JourneyDB**）+ 自有专有数据；用**类别均衡（category-balanced）**策略保证覆盖广泛视觉概念。
- **Re-caption（仿 DALL·E 3）**：用 MLLM 给海量图重写细粒度 caption。论文用 5 个维度评 caption 质量——长度、完整性（Completeness）、相关性（Correlation）、幻觉（Hallucination）、主观性（Subjectivity）。对比 LLaVA1.5-13B、InternLM-XComposer-7B、CogAgent-VQA、CogVLM-1.1-chat、GPT-4V 五个模型（10 名评测员评 500 张图）：GPT-4V 综合最高（Avg 4.66）但处理上亿图成本过高；开源里 **CogVLM-1.1-chat（Avg 4.56）** 在完整性/相关性上优于 LLaVA/InternLM，且幻觉/主观性更低，故选 **CogVLM-1.1-chat** 重写全量训练集。
- **原文/合成 caption 配比**：考虑到 MLLM 可能识别不出知识库外的特定概念，采用 **50% 原始文本 + 50% 合成 caption** 的混合比例（与 SD3 的配置一致）。
- **中文文字渲染数据**：(1) 选 **5 万个最常用中文词**，通过数据合成构造**数千万级**中文图文对，仅在概念学习阶段引入；(2) 用 **OCR + MLLM** 给真实世界图（海报、场景文字）生成新描述，约**数百万样本**。论文观察：合成数据初期不真实，但叠加真实数据/高质文字图后，生成文字图的真实感显著提升（即便某些字只出现在合成数据里）。
- **质量提升阶段的高美学数据**：先用传统过滤（分辨率、OCR 准确度、人脸数、清晰度、美学评分）把数据降到约**数千万张**；再人工标注分 5 级，每图标 3 次投票定级以减主观偏差：
  - Level 1 不安全内容（色情/暴力/血腥/恐怖）；Level 2 人工合成痕迹（logo/水印/黑白边/拼接）；Level 3 参数错误（模糊/过曝/欠曝/无明确主体）；Level 4 平庸快照；Level 5 高美学价值（曝光/对比/色调/饱和度得当且有叙事感）。
  - 最终筛出**数百万张 Level 5 高美学图**用于质量提升阶段。
- **安全过滤**：上述 Level 1 即为不安全内容剔除；其余安全细节未单独披露。

## 训练方法
- **训练目标**：基于 [[ddpm]] 的训练范式，采用 **ε-prediction（噪声预测）** 目标（注意：论文明确用 DDPM ε-pred，**不是** SD3 的 rectified flow / flow matching）。
- **两阶段训练**：
  1. **概念学习阶段（concept learning）**：在数十亿图文对的大规模数据上学广泛知识与概念，用类别均衡覆盖；分辨率较低（512），噪声调度与 SDXL 相同。中文文字合成数据、5 万常用词合成图文对仅在此阶段引入。
  2. **质量提升阶段（quality improvement）**：聚焦高分辨率（1024）下的细节与美学，只用数百万张 Level 5 高美学图；启用分桶采样支持多长宽比。
- **高分辨率噪声调度（关键 trick）**：观察到 SDXL 的噪声调度在高分辨率下「破坏不够」——低分图加噪到末端近乎纯噪声，但高分图末端仍残留低频分量，而推理是从纯高斯噪声起步，导致高分训练/推理不一致。Kolors 的解法很「简单」：**把扩散步数从 1000 延长到 1100**，使末端信噪比更低；同时调整 β 值以**保持 αt 曲线形状**（αt 决定 xt = √αt·x0 + √(1−αt)·ε）。论文展示其 αt 轨迹**完全包住** SDXL base 调度的轨迹，而 ZeroSNR、Simple Diffusion 等方案偏离较大——这意味着从低分 base 调度迁移到新调度时，适应与学习难度更小。该调度仅用于高分阶段。
- **偏好对齐 / RLHF / DPO / 蒸馏**：**未使用**（技术报告未报告 RLHF/DPO/reward model，也未做步数蒸馏/LCM/ADD）。论文把 LCM 等列为「未来要发的插件」，说明基础模型本身不含加速蒸馏。
- **关键超参**：文本长度 256；推理默认 guidance 5.0 + 50 步（Euler）。其余优化器/学习率/batch 等训练超参**未披露**。

## Infra（训练 / 推理工程）
- **算力规模 / GPU·时 / 并行策略 / 混合精度 / 吞吐**：技术报告与 README **均未披露**（无 GPU 数、训练时长、分布式/并行框架、FLOPs 等信息）。
- **推理**：HF 卡给出 fp16 variant（`torch_dtype=torch.float16, variant="fp16"`）；默认 50 步（Euler，guidance 5.0），EDMDPMSolver 可 25 步。无量化/缓存/蒸馏加速披露。
- **部署形态**：全开源权重 + 推理代码（Apache-2.0 代码，权重学术免费、商用需登记，MAU 超 3 亿需单独授权）；上线官方平台 kolors.kuaishou.com；生态侧已接入 **Diffusers（KolorsPipeline）、ModelScope、ComfyUI**，并陆续放出 ControlNet（Canny/Depth/Pose）、Inpainting、IP-Adapter-Plus、IP-Adapter-FaceID-Plus、Dreambooth-LoRA、Virtual-Try-On 等配套。

## 评测 benchmark（把效果讲清楚）
**KolorsPrompts 基准（自建）**：超 1000 条 prompt，源自 PartiPrompts、ViLG-300 + 专有 prompt；覆盖 14 个真实场景类别（People 占比最大 29.4%）、按特性分 12 类挑战（Simple words 最多 30.9%）；每条都有中英双语版。

**人评（约 50 名专业评测员，每图评 5 次取均值，1–5 分，1024×1024）**——Kolors 用中文 prompt、对比模型用英文 prompt（2024 年 4 月产品版本）：

| 模型 | 总体满意度 | 视觉吸引力 | 文本忠实度 |
|---|---|---|---|
| Adobe-Firefly | 3.03 | 3.46 | 3.84 |
| Stable Diffusion 3 | 3.26 | 3.50 | 4.20 |
| DALL·E 3 | 3.32 | 3.54 | 4.22 |
| Midjourney-v5 | 3.32 | 3.68 | 4.02 |
| Playground-v2.5 | 3.37 | 3.73 | 4.04 |
| Midjourney-v6 | 3.58 | 3.92 | **4.18** |
| **Kolors** | **3.59** | **3.99** | 4.17 |

结论：Kolors **总体满意度 3.59 第一**、**视觉吸引力 3.99 第一**（领先优势明显，追平/略超 MJ-v6 的 3.92），文本忠实度 4.17 与 MJ-v6/DALL·E 3/SD3 同档（DALL·E 3 的 4.22 略高）。

**MPS（Multi-dimensional Human Preference Score，CVPR 2024，快手自家提出）在 KolorsPrompts 上**：

| 模型 | Overall MPS↑ |
|---|---|
| Adobe-Firefly | 8.5 |
| Stable Diffusion 3 | 8.9 |
| DALL·E 3 | 9.0 |
| Midjourney-v5 | 9.4 |
| Playground-v2.5 | 9.8 |
| Midjourney-v6 | 10.2 |
| **Kolors** | **10.3** |

MPS 自动评分 Kolors 同样居首（10.3），与人评结论一致。

**MS-COCO 零样本 FID-30K（256×256）**：Kolors（2.6B 参数）**FID-30K = 23.15**，反而比多数老模型「更差」（如 GigaGAN 9.09、Imagen 7.27、PixArt-α 10.65、SD 8.32）。论文专门论证：**FID 与视觉美学负相关、不适合衡量现代 T2I 图像质量**，并引多篇工作支持「人评比统计指标更可靠」——即 Kolors 故意不优化 FID，靠人评/MPS 证明效果。

**消融/定性结论**：
- GLM vs CLIP（Fig 2）：同一 backbone 下，Kolors+GLM 能正确生成多主体复杂 prompt（小贩+电话、多人多色属性绑定），Kolors+CLIP 则漏物体、颜色混淆。
- 改进视觉吸引力前后（Fig 6）：高美学数据 + 高分调度后图像细节与美感显著提升。
- 中文文字渲染（Fig 3）：可稳定渲染「我爱和平」「天道酬勤」「KOLORS」「圣诞快乐」等中英文字。
- 第三方背书：2024.07 在 **BAAI FlagEval 多模态文生图榜拿第二**，其中**中英文主观质量评测拿第一**（README 披露）。

## 创新点与影响
**核心贡献**：
1. **用双语 LLM（ChatGLM3-6B-Base）替代 CLIP/T5 当文本编码器**，并把文本长度提到 256，从根上解决中文/长复杂 prompt 理解——区分 Base（做表征）与 Chat（强文字渲染）的洞见也值得注意。
2. **MLLM（CogVLM-1.1-chat）全量 re-caption + 50/50 原文/合成配比**，并为中文文字渲染专门合成「5 万常用词 × 数千万图文对」+ OCR/MLLM 重描数百万真实文字图。
3. **两阶段训练 + 自研高分辨率噪声调度（步数 1000→1100、保 αt 曲线形状）**，证明经典 U-Net 也能达到 MJ-v6 级视觉效果。
4. **KolorsPrompts** 类别均衡基准 + 强调人评/MPS 优于 FID 的评测方法论。

**影响**：作为 2024 年中第一梯队的**全开源中文写实 T2I**，Kolors 被开源生态广泛采用（Diffusers/ComfyUI/ModelScope 一线接入），并衍生 ControlNet/IP-Adapter/Inpainting/LoRA/Virtual-Try-On 等完整插件链，成为中文社区做可控生成/换装/写真的常用底座；也验证了「LLM-as-text-encoder」这条在 SD3、后续 DiT 系工作中持续被采纳的路线。后续快手沿此预告了基于 Transformer（DiT）的新一代模型（Kolors 2.x）。

**已知局限**：
- backbone 仍是 U-Net、训练目标仍是 DDPM ε-pred（非 rectified flow），刻意不追先进 backbone；
- 文本忠实度在 DALL·E 3（4.22）面前略逊；
- **训练 infra 全程未披露**（GPU 规模/时长/并行/精度），不利复现；
- 无 RLHF/DPO 偏好对齐与步数蒸馏，基础模型推理 50 步偏慢（加速靠后续 LCM 插件）；
- FID 客观分较差（虽论文论证 FID 不可靠，但仍是一项可量化短板）。

## 原始链接
- github: https://github.com/Kwai-Kolors/Kolors
- tech-report (PDF): https://github.com/Kwai-Kolors/Kolors/blob/master/imgs/Kolors_paper.pdf
- hf model: https://huggingface.co/Kwai-Kolors/Kolors
- hf diffusers: https://huggingface.co/Kwai-Kolors/Kolors-diffusers
- modelscope: https://modelscope.cn/models/Kwai-Kolors/Kolors
- team page / blog: https://kwai-kolors.github.io/
- official platform: https://kolors.kuaishou.com/

## 本地落盘文件
- ../../../sources/omni/2024/kolors.pdf （技术报告全文，12MB；.gitignore 排除，本地精读）
- ../../../sources/omni/2024/kolors--readme.md （GitHub README，含人评/MPS 表与生态信息）
- ../../../sources/omni/2024/kolors--hf-modelcard.md （HF model card，含推理调度器/超参）
- ../../../sources/omni/2024/kolors--teampage.md （团队博客首页快照）
