---
title: "Imagen 3"
org: Google DeepMind
country: US
date: "2024-08"
type: tech-report
category: t2i
tags: [t2i, latent-diffusion, google, gemini, closed-source, synthetic-caption, human-eval, synthid]
url: "https://arxiv.org/abs/2408.07009"
arxiv: "https://arxiv.org/abs/2408.07009"
pdf_url: "https://arxiv.org/pdf/2408.07009"
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://deepmind.google/models/imagen/"
downloaded: [arxiv-2408.07009.pdf, imagen-3--blog.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Imagen 3 是 Google DeepMind 2024 年的旗舰**闭源潜空间扩散（latent diffusion）T2I 模型**，默认输出 1024×1024（可 2×/4×/8× 上采样到 12MP），核心打法是**用 Gemini 生成的多样化合成 caption + 严格多级数据过滤**换取业界领先的长/复杂 prompt 遵从度；在 GenAI-Bench 等基准上**整体偏好（overall preference）取得 SOTA**，详细 prompt 对齐（DOCCI）领先第二名 +114 Elo / 63% 胜率，计数（GeckoNum）58.6% 超第二名 DALL·E 3（46.0%）12.6 个百分点（视觉吸引力 visual appeal 略逊 Midjourney v6）。

## 背景与定位
Imagen 3 是 Google [[imagen]]（2022，像素空间级联扩散 + T5-XXL 文本编码）→ [[imagen-2]]（2023）家族的第三代，但**架构路线已切换到潜空间扩散**（与 [[latent-diffusion-ldm]] / [[sdxl]] 同范式），不再是初代 Imagen 的纯像素级联超分。技术报告本身把绝大多数篇幅放在**评测与负责任部署（responsible development）**上，对模型与训练的工程细节披露非常克制——这是 Google 闭源旗舰的一贯风格，与开放权重的 [[sdxl]] / [[flux-1]] 形成鲜明对比。

它要解决的核心问题是 T2I 的两大痛点：**长/复杂 prompt 的精确遵从**和**生成质量的整体平衡**。报告的对手是当时的第一梯队：DALL·E 3（见 [[dall-e-3]]）、Midjourney v6、Stable Diffusion 3 Large、[[sdxl]] 1.0，外加自家 Imagen 2。报告结论是 Imagen 3 在「整体偏好」与「prompt 对齐」上领先，在「纯视觉吸引力」上居 Midjourney v6 之后——即它在「听话」与「好看」之间取了更优的折中。2024 年 12 月报告 v3 追加附录 D，发布更高质量的 **Imagen 3-002** 版本，并加测 Recraft v3、Ideogram v2、[[flux-1]] 1.1 [pro]、Nova Canvas、SD 3.5 Large 五个新对手。

## 模型架构
- **基本类型**：latent diffusion model（model card 原文："Imagen 3 is a latent diffusion model"）。默认在 1024×1024 分辨率生成，可跟 2×/4×/8× 上采样（cascade upsampler），最高得到约 12MP（4K）图像。
- **backbone / tokenizer / text encoder / 参数量**：**技术报告未披露**。报告没有公开 denoiser 是 U-Net 还是 DiT、没有公开所用 VAE/visual tokenizer、没有公开文本编码器是 T5 还是 Gemini-based encoder、也没有给参数量。这是本报告最大的「黑箱」部分——它把架构当作产品机密。
  - 可确证的间接信息：**合成 caption 由 Gemini 模型生成**（数据侧用到 Gemini，但这不等于推理时文本编码器就是 Gemini）。早期 Imagen 用 T5-XXL，本报告未声明是否沿用，**不应臆测**。
- **条件注入 / guidance**：报告未给出 classifier-free guidance scale、attention 注入方式等细节（仅在自动评测里把生成结果降采样到各 metric 标准输入尺寸）。
- 一句话：**架构层面几乎全是「未披露」**，能确证的只有「潜空间扩散 + 1024 默认分辨率 + 级联上采样到 12MP」。

## 数据
这是报告披露相对充分的一维（来自正文第 2 节 + model card 附录 A）：
- **构成**：大规模「图像 + 文本 + 关联标注」数据集，规模/总量**未披露**。
- **多级过滤管线**：
  1. 移除不安全、暴力、低质图像（safety & quality filtering）；
  2. **剔除 AI 生成图像**——明确为了避免模型学到 AI 生成图的伪影与偏置；
  3. **去重**：dedup 管线 + 对相似图像**降权（down-weight）**，降低输出过拟合特定训练样本的风险。
- **双 caption 策略（核心创新点之一）**：每张图同时配**原始 caption**（来自 alt-text、人工描述等）与**合成 caption（synthetic caption）**。合成 caption **用 Gemini 模型 + 多样化 prompt 生成**，且明确「leverage multiple Gemini models and instructions」以**最大化合成描述的语言多样性与质量**（引用 Betker 2023 即 DALL·E 3 的 re-captioning 思路、Garg 2024 即 ImageInWords）。合成 caption 让模型学到图中的细节。
- **caption 侧过滤**：再用 filter 移除不安全 caption 及含 PII 的 caption。
- **配比/合成数据占比/具体清洗阈值**：**未披露**。

## 训练方法
报告对训练的披露**极少**：
- **训练目标**：报告未明写具体目标（diffusion / flow matching / rectified flow 等均未声明），只在 model card 说它是 latent diffusion model——可推断为 diffusion 去噪目标，但**未给出是 ε-pred / v-pred / flow matching 中的哪种，亦未给步数/噪声调度**。
- **多阶段 / 偏好对齐**：报告反复提到「pre-training interventions」与「post-training interventions」，但这些主要描述的是**安全/负责任层面的干预**（安全过滤、生产端过滤、SynthID 水印），**没有披露**是否使用了 RLHF / DPO / reward model 做质量偏好对齐，也没有蒸馏 / consistency / LCM / ADD 等加速方法的任何细节。
- **超参 / trick / 训练时长**：**全部未披露**。
- 与 Gemini 的关系：安全策略与 desiderata「follow the Gemini approach」（最大化对用户 prompt 的遵从，而非一味拒答），但这是策略层面对齐，不等于共享训练栈。
- 一句话：**训练方法是本报告披露最弱的一维**，除"用合成 caption 训练 + 安全/生产端后处理"外，方法细节基本为空白。

## Infra（训练 / 推理工程）
来自 model card「Implementation and Sustainability」：
- **硬件**：用 Google 最新一代 **TPU（TPUv4 与 TPUv5）** 训练；强调 TPU Pod 集群可分布式扩展、HBM 大显存利于大模型与大 batch。
- **软件**：训练框架为 **JAX**。
- **算力规模 / GPU·时 / 并行策略 / 吞吐 / 混合精度**：**未披露**。
- **推理侧**：默认 1024×1024 生成 +（可选）2×/4×/8× 级联上采样到 12MP；推理步数、缓存、量化、蒸馏等加速细节**未披露**。
- **部署形态**：集成进 **Gemini App、ImageFX/Google Labs、Vertex AI（企业）**；所有输出加 **SynthID 水印**（不可见水印，溯源 AI 生成）。

## 评测 benchmark（把效果讲清楚）
报告的重头戏。评测分**人评（5 个维度）**与**自动评测**两条线，对手为 Imagen 2 / DALL·E 3 / Midjourney v6 / SD3 Large / SDXL 1.0。

**人评规模**：共收集 **366,569 条评分**、5,943 次提交、3,225 名评分者；71 国参与；每个 side-by-side 研究 2,500 条评分。聚合为 **Elo 分数**（每对模型穷举对比）。

初版（2024-08, Imagen 3-001）核心结论：
- **整体偏好 overall preference**（GenAI-Bench/DrawBench/DALL·E3-Eval）：Imagen 3 在 **GenAI-Bench 显著领先**（Elo 1098，第二 SD3 1068）；DrawBench 小幅领先 SD3；DALL·E3-Eval 上四强接近、Imagen 3 略胜。
- **prompt-image 对齐**：GenAI-Bench 上**显著领先**（Elo 1083 vs SD3 1028）。
- **detailed 对齐（DOCCI-Test-Pivots，平均 136 词长 prompt）**：Imagen 3 对第二名**领先 +114 Elo、63% 胜率**——长 prompt 遵从是它最突出的优势。
- **视觉吸引力 visual appeal**：**Midjourney v6 领先**，Imagen 3 第二（GenAI-Bench 上几乎持平：MJ 1101 vs Imagen 3 1095；DALL·E3-Eval 上 MJ 明显领先）。
- **数值推理 / 计数（GeckoNum 精确数目生成）**：Imagen 3 **58.6%**，最强；DALL·E 3 第二 **46.0%**（领先 12.6 个百分点）。但所有模型在 ≥5 个物体时都很差（报告：平均在"5"上比"1"低 51.6 个百分点）。

**自动评测**：
- 选了 CLIP、Gecko（VQA-based，PaLI backbone）、VQAScore（用 **Gemini 1.5 Pro** 作 backend 的 LVLM-based）三类对齐 metric。结论：**CLIP 不可靠**（与人评一致率仅 43.3%，常排错序）；Gecko 73.3%、**VQAScore 80%** 与人评一致；二者一致时与人评吻合 94.4%。报告主推 **VQAScore**，并指出 **Imagen 3 在四数据集（Gecko-Rel / DOCCI / DALL·E3-Eval / GenAI-Bench）上对齐自动分整体最高**，尤其 DOCCI 长 prompt 上最强；在 color/counting/spatial/compositional 等类别上多数最优。
- **图像分布质量（Table 1，MSCOCO-caption 3 万样本）**：

  | 模型 | FID ↓ | FD-Dino ↓ | CMMD ↓ |
  |---|---|---|---|
  | DALL·E 3 | 20.1 | 284.4 | 0.894 |
  | SDXL 1 | **13.2** | **185.6** | 0.898 |
  | Imagen 3 | 17.2 | 213.9 | **0.854** |

  报告强调 **FID/FD-Dino 不利于 Imagen 3 是因为它和 DALL·E 3 有意把色彩分布偏离 MSCOCO**（追求更鲜艳风格化），而 **CMMD（CLIP 特征 + MMD，更现代的 metric）Imagen 3 最低**，是更可信的质量信号。

**2024-12 更新（Imagen 3-002，附录 D，GenAI-Bench Elo）**：加测 Recraft v3 / Ideogram v2 / FLUX 1.1 [pro] / Nova Canvas / SD 3.5 Large 后，**Imagen 3-002 在三项（overall preference / visual quality / prompt-image alignment）Elo 全部第一**：
- overall preference：Imagen 3-002 ≈ **1115**，Recraft v3 1078，Ideogram v2 1059，Imagen 3-001 1053，FLUX 1.1 [pro] 1001，SD 3.5 L 997，DALL·E 3 982。
- visual quality / prompt-image alignment：Imagen 3-002 同样居首（具体 Elo 见附录 D 图 14），显示二代更新把 002 的视觉质量也拉到了榜首（弥补初版对 MJ v6 的吸引力短板）。

**编辑 / 视频类基准（GEdit/MagicBrush/VBench 等）**：N/A——Imagen 3 是纯 T2I，报告未涉及编辑与视频评测。

## 创新点与影响
**核心贡献**：
1. **「Gemini 生成的多样化合成 caption」工程化**：用多个 Gemini 模型 + 多样 instruction 生成高语言多样性的合成 caption，与原始 caption 双轨训练，是其长/复杂 prompt 遵从领先的关键（沿袭并放大 DALL·E 3 re-captioning 思路，见 [[dall-e-3]]）。
2. **评测方法学样板**：超大规模（36 万条）多维度人评 + Elo 聚合，并系统论证 **CLIP 已不可靠、VQAScore（LVLM-based）更贴近人评**——对后续 T2I 评测有方法学影响。
3. **负责任部署全流程**：多级数据安全过滤、剔除 AI 生成图、SynthID 水印、development/assurance/red-teaming/external 四类安全评测、fairness（Monk 肤色 / 感知性别 / 年龄分布）量化，成为闭源大厂发布范式。

**影响**：作为集成进 **Gemini App / ImageFX / Vertex AI** 的旗舰，把高遵从度 T2I 推向产品规模用户；其「合成 caption + 严过滤」配方与「VQAScore 评测」被广泛参考。后续被 **Imagen 4 / Nano Banana（Gemini native image）** 等迭代取代。

**已知局限（报告自陈）**：① 数值/计数推理仍弱（多物体、复杂句式）；② scale 推理（"房子和猫一样大"）、compositional（"一顶红帽和一本黑玻璃书"）、action（"扔橄榄球"）、spatial 与复杂语言是所有模型最难的类别；③ 纯视觉吸引力初版逊于 Midjourney v6；④ fairness 上仍偏向浅肤色、感知男性、女性偏年轻（但优于 Imagen 2）。**架构与训练方法几乎全未披露**，可复现性低。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2408.07009
- arxiv_pdf: https://arxiv.org/pdf/2408.07009
- blog/product（产品页，原 /technologies/imagen-3/ 已重定向至模型总览页，无 Imagen-3 专属技术内容）: https://deepmind.google/models/imagen/

## 一手源存档（sources/）
- ../../../sources/omni/2024/arxiv-2408.07009.pdf —— 技术报告（含 v3 附录 D 的 Imagen 3-002 更新），本页所有数字均出自此文件
- ../../../sources/omni/2024/imagen-3--blog.md —— deepmind.google/models/imagen 当前产品落地页快照（已迭代到 Imagen 4，仅导航壳 + 示例 prompt，**无 Imagen-3 专属技术内容**，仅作链接留痕）
