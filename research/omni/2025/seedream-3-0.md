---
title: "Seedream 3.0 Technical Report"
org: "字节跳动 Seed"
country: China
date: "2025-04"
type: tech-report
category: t2i
tags: [t2i, mmdit, flow-matching, bilingual, text-rendering, high-resolution, reward-model, diffusion-acceleration, repa]
url: "https://seed.bytedance.com/en/seedream3_0"
arxiv: "https://arxiv.org/abs/2504.11346"
pdf_url: "https://arxiv.org/pdf/2504.11346"
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://seed.bytedance.com/en/seedream3_0"
downloaded: [arxiv-2504.11346.pdf, seedream-3-0--project-page.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Seedream 3.0 是字节跳动 Seed 团队 2025 年 4 月（官方项目页注明 4 月 16 日发布）的中英双语高分辨率文生图基础模型（豆包/即梦底座），在 [[seedream-2-0]] 的 MMDiT 架构上做了全链路升级：原生 2K 输出、强中文密集小字排版、4–8× 推理加速（1K 图端到端仅 3.0 秒）。发布时在 Artificial Analysis 文生图竞技场以 **Arena ELO 1158**（17.0K 对局）排名全球第一，超过 GPT-4o、Imagen 3、Midjourney v6.1、FLUX1.1 Pro。

## 背景与定位
Seedream 3.0 是对自家 [[seedream-2-0]]（arXiv 2503.07703，原生中英双语 T2I 基础模型）的迭代，针对 2.0 暴露的四类商用瓶颈做改进：

- **复杂 prompt 对齐弱**：数量精确性、多目标空间关系不足。
- **精细排版受限**：小字号、多行上下文、复杂排版细节生成不佳。
- **美学与保真度欠佳**：电影感、人像质感等"高级"美学难捕捉。
- **分辨率受限**：底模原生只到 512×512，必须依赖后处理超分管线。

技术脉络上，它属于 [[latent-diffusion-ldm]] → [[stable-diffusion-3]]（Stable Diffusion 3 引入的 MMDiT + rectified flow）这一支的工程集大成者，并大量吸收了同期开源研究：[[flow-matching]] 训练目标、REPA 表征对齐、Hyper-SD/RayFlow 加速。其差异化定位是"中英双语 + 原生高分辨率 + 专业级文字排版"，把后处理超分与外挂文字插件方案统一进单一底模。本报告为偏工程的技术报告（5 页正文），方法披露较细但**绝对规模数字（参数量、数据条数、算力）基本未公开**。

## 模型架构
- **Backbone**：沿用 [[seedream-2-0]] 的 **MMDiT**（多模态 DiT，参考 SD3 [Esser et al. 2024]），用统一 Transformer 同时处理图像 token 与文本 token、建模两模态关系。Seedream 3.0 **增大了 base model 总参数量**（具体数值未披露），以提升扩展性、泛化与视觉-语言对齐。
- **VAE / Tokenizer / Text encoder**：报告未单独披露 3.0 的 VAE、visual tokenizer、文本编码器细节（沿用 2.0 体系，2.0 使用了字节自研双语文本编码 + 字形/字符级渲染增强）。本页对这些组件标注"未单独披露"。
- **混合分辨率训练（Mixed-resolution Training）**：利用 Transformer 原生支持变长 token 的特性（类比 NaViT），把不同长宽比、不同分辨率的图像打包（packing）一起训练。先在**平均 256² 分辨率**（多种长宽比）预训练，再在 **512²→2048²** 高分辨率上微调；引入 **size embedding** 作为目标分辨率条件，使模型感知目标尺寸，显著增加数据多样性、提升对未训练分辨率的泛化。
- **跨模态 RoPE（Cross-modality RoPE）**：2.0 的 Scaling RoPE 升级版。把文本 token 视为形状 [1, L] 的 2D token 并施加 2D RoPE，文本 token 的列向位置 ID 紧接对应图像 token 之后连续分配，从而统一建模**模态内与跨模态**位置关系，对提升视觉-文本对齐和**文字渲染精度**关键。
- **分辨率策略**：原生支持 512²–2048² 任意分辨率与多种长宽比，**省掉了 Refiner 阶段**（2.0 后训练含 Refiner，3.0 因可直接出任意分辨率图而删除）。

## 数据
- **缺陷感知训练范式（defect-aware training）**：2.0 严格过滤掉含水印/叠字/字幕/马赛克的图（约占原始数据 **35%**），严重限制了可用数据。3.0 训练一个**缺陷检测器**（基于 active learning 引擎挑选的 **15,000 条人工标注样本**），用 bbox 定位缺陷区域；当缺陷总面积 < 图像 **20%**（阈值可配）时保留这些原本被弃的样本，并在**潜空间做掩码优化（mask latent space optimization）**——在 latent 空间算 diffusion loss 时用**空间注意力掩码**屏蔽缺陷区域的特征梯度。该方法使**有效训练数据扩增 21.7%**。
- **双轴协同采样（dual-axis collaborative data sampling）**：从**视觉形态**与**语义分布**两个正交维度联合优化。视觉侧用层次聚类（hierarchical clustering）保证不同视觉模式均衡；文本语义侧用 **TF-IDF** 做语义均衡，解决描述文本长尾问题。
- **跨模态检索系统**：建立图文联合嵌入空间，动态优化数据集：(1) 通过定向概念检索注入专家知识；(2) 相似度加权采样做分布校准；(3) 用检索到的邻近图文对做跨模态增强。报告称该检索系统在所有 benchmark 上达到 SOTA（未给具体指标）。
- **规模**：官方页与报告均称数据集规模**扩大约 100%（翻倍）**，但**未给绝对图文对数量**。
- **标注/re-captioning**：见训练方法中的"美学 caption"——后训练专门训练多版 caption 模型生成含美学/风格/排版的细粒度描述。

## 训练方法
分两大阶段：**预训练** 与 **后训练（CT → SFT → RLHF → PE）**。

### 预训练
- **训练目标**：**flow matching**（rectified flow，线性插值 `x_t = (1−t)x_0 + tε`, `ε∼N(0,I)`），外加**表征对齐损失 REPA**：将 MMDiT 中间特征与预训练视觉编码器 **DINOv2-L** 的特征做余弦距离对齐，损失权重 **λ=0.5**。作者发现引入表征对齐目标能**加速大规模 T2I 训练收敛**。
- **分辨率感知时间步采样（Resolution-aware Timestep Sampling）**：时间步从随数据集自适应的分布 `p(t;D)` 采样——先从 **logit-normal** 分布采样，再按训练分辨率做 **timestep shifting**（参考 SD3）。高分辨率训练时把分布往**更低 SNR**（更高噪声段）偏移；训练时按数据集平均分辨率定 shift，推理时按目标分辨率与长宽比算 shift。

### 后训练
- **CT（Continuing Training）**：继续训练阶段。
- **SFT**：使用**多样化美学 caption**——专门为 CT/SFT 训练了多版 caption 模型，能在美学、风格、排版等专业域给出准确描述，提升模型可控性与 PE 后表现。SFT 中用**分辨率均衡策略**保证各分辨率充分采样，增强不同场景的 prompt-following。
- **RLHF（人类反馈对齐）+ Reward Model Scaling**：核心改进之一。2.0 用 CLIP 当 reward model，3.0 改用 **VLM 作为奖励建模框架**。借鉴 LLM 的**生成式奖励建模（generative RM）**：把指令显式构造成 query，从 **"Yes" 响应 token 的归一化概率**导出奖励，从而利用预训练 LLM 知识并享受 LLM scaling。**系统性把 reward model 从 1B 扩到 >20B 参数**，实证观察到 **reward model scaling 的涌现**——奖励模型容量越大、奖励建模性能越好。
- **PE（Prompt Engineering）**：最后阶段。报告删除了 2.0 中的 **Refiner** 阶段（因可直接出任意分辨率图）。

### 加速（Model Acceleration）
建立在 **Hyper-SD** 与 **RayFlow** 之上，核心思想：让每个样本走**自适应、实例特定（instance-specific）的生成轨迹**，而非强迫所有样本收敛到统一高斯先验、造成轨迹重叠/碰撞、增大随机性与不稳定。
- **一致噪声期望（Consistent Noise Expectation）**：从预训练模型估计一个**统一噪声期望向量**，作为所有时间步的全局参考，对齐去噪过程；理论上最大化"数据→噪声→数据"前后向路径概率，从而**压缩采样步数而不掉质量**。
- **重要性时间步采样（learn to sample important timesteps）**：训练侧用 **Stochastic Stein Discrepancy (SSD)** + 一个神经网络学习数据相关的时间步分布，预测哪些时间步对降 loss 贡献最大并优先采样，降低 loss 方差、加快收敛、省训练算力。
- 量化等其他加速直接沿用 2.0 方案。
- 综合实现**少步采样**：少于未加速基线远少的步数，质量却能**匹配或超过 50 NFE 基线**（美学、图文对齐、结构保真三维度），实测**整体推理 4–8× 提速**。

## Infra（训练 / 推理工程）
- **算力 / GPU·时 / 并行分布式 / 混精度 / 吞吐**：**未披露**（报告无任何训练算力、卡数、并行策略、精度的数字）。
- **推理加速**：见上，靠轨迹定制 + 一致噪声期望 + 重要性采样实现 4–8× 提速、少步采样；量化沿用 2.0。
- **推理时延**：官方端到端**1K 分辨率图仅 3.0 秒**（不含 PE），报告称显著快于其它商业模型。
- **部署形态**：火山引擎（Volcano Engine）开放 API，Model ID `Doubao-Seedream-3.0-t2i`；并于 **2025 年 4 月初**集成进**豆包（Doubao）**与**即梦（Jimeng）** 产品。

## 评测 benchmark（把效果讲清楚）

### 公开竞技场
- **Artificial Analysis Text-to-Image Arena**：发布时 **Arena ELO 1158**、**17.0K** appearances，**总榜第一**，超过 GPT-4o、Recraft V3、HiDream、Reve Image、Imagen 3 (v002)、FLUX1.1 Pro、Midjourney v6.1；在多数子维度（写实/动漫/卡通插画/传统艺术，人像/群像/奇幻/未来/物理空间）也最佳。

### 偏好评测（Table 1，越高越好）
| 指标 | FLUX1.1 | Ideogram 2.0 | MJ v6.1 | Imagen 3 | Seedream 2.0 | **Seedream 3.0** |
|---|---|---|---|---|---|---|
| EvalMuse（图文对齐）| 0.617 | 0.632 | 0.583 | 0.680 | 0.684 | **0.694** |
| HPSv2 | 0.2946 | 0.2932 | 0.2850 | 0.2951 | 0.2994 | **0.3011** |
| MPS | 13.11 | 13.01 | 13.67 | 13.33 | 13.61 | **13.93** |
| Internal-Align | 27.75 | 27.92 | 28.93 | 28.75 | 29.05 | **30.16** |
| Internal-Aes | 25.15 | 26.40 | 27.07 | 26.72 | 26.97 | **27.68** |

Seedream 3.0 在全部 5 项**均第一**。**HPSv2 首次破 0.3**（0.3011）；美学维度（MPS + 内部 Aes）**首次超过 Midjourney**（2.0 此前没做到）。

### 人评（Bench-377）
自建 **377 条 prompt** 基准，覆盖电影/艺术/娱乐/美学设计/实用设计五场景，三准则（图文对齐、结构合理、美学）。Seedream 3.0 在**对齐与结构保真**上显著超 2.0 与对手；**整体美学超 Midjourney**（设计类明显胜出，艺术类略逊）。Imagen 3 对齐/结构可，但美学偏弱；Midjourney 美学强但功能性对齐与结构弱。

### 文字渲染（180 中文 + 180 英文 prompt）
三指标：可用率（availability）、准确率（accuracy `Ra=(1−Ne/N)`，Ne 为编辑距离）、命中率（hit `Rh=Nc/N`）。
- 中英文**可用率均 94%**，**中文可用率较 2.0 提升 16%**；可用率与命中率近乎相等，说明排版/介质类渲染错误极少。
- 擅长**密集小字**长文本排版；对比 Recraft V3、Ideogram 2.0、Imagen 3、FLUX1.1 Pro、Midjourney v6.1、MiracleVision 5.0、Kolors 1.5 均领先（Figure 11）。

### 写实人像（100 prompt，Elo 对战）
公开 **>50,000** 轮对战，Elo（Figure 14）：**Seedream 3.0 1198±19.7**、**Midjourney v6.1 1193±11.1**（并列第一），Ideogram 3.0 1086±13.0，Seedream 2.0 1000±0.0，FLUX1.1 Pro 936±15.8。3.0 皮肤质感（皱纹/绒毛/疤痕）更真实，去"AI 假感"；Midjourney 情绪表达更佳故并列。2K（2048²）直出进一步增强人像纹理。

### 与 GPT-4o 定性对比（无 API 故未系统化）
- **密集文字**：GPT-4o 在小号英文/部分 LaTeX 符号更准，但**中文字体明显受限**；Seedream 3.0 中文密集排版与构图更优。
- **图像编辑**：用 **SeedEdit 1.6**（衍生自 Seedream）对比 GPT-4o / Gemini-2.0：GPT-4o 编辑能力广但难保 IP/ID 一致；Gemini-2.0 像素级保真但色彩自然度与画质差；SeedEdit 1.6 在 ID 保持与 prompt-following 上更均衡（多图参考/多轮编辑仍是其短板）。
- **生成质量**：GPT-4o 图偏暗黄色调且噪声明显，Seedream 3.0 在色彩/纹理/清晰度/美感上更优。

> 消融性结论：缺陷感知扩数据（+21.7% 有效数据）、REPA（加速收敛）、reward model 从 1B→>20B 的 scaling 涌现、一致噪声期望（4–8× 加速且不掉质量）为关键有效设计；但报告**未给逐项消融的量化数字**（无对照表），属定性陈述。

## 创新点与影响
**核心贡献**
1. **缺陷感知训练 + 潜空间掩码**：把"过滤即丢弃"变为"局部屏蔽梯度"，回收 35% 被弃数据，有效数据 +21.7%——一种数据高效的工程范式。
2. **跨模态 RoPE + 混合分辨率训练 + 分辨率感知时间步采样**：把可变分辨率/长宽比与图文位置统一建模，**原生 2K 直出**、省掉超分 Refiner。
3. **VLM 生成式奖励模型 + reward scaling**：首次在 T2I 偏好对齐里系统验证 reward model 1B→>20B 的 **scaling 涌现**，把 LLM 的 generative RM 思路迁到图像偏好。
4. **一致噪声期望 + 重要性时间步采样的加速范式**：实例特定轨迹，**4–8× 提速**、1K 图 3.0 秒、质量匹配 50-NFE 基线。
5. **专业级中文密集小字排版**：94% 双语可用率，graphic design 超 Canva 模板，把"原生文字渲染 vs 外挂插件"之争推向前者。

**影响**：作为**豆包/即梦的文生图底座**，是字节 Seedream/Seedance 系列（后续有 Seedream 4.0/5.0、SeedEdit、Seedance 视频）的关键一环，验证了"MMDiT + rectified flow + REPA + VLM-RM + 实例轨迹加速"这套组合在工业级双语高分辨率 T2I 上的有效性；中文密集文字渲染成为其最强护城河。

**已知局限**：与 GPT-4o 比，小号英文/LaTeX 渲染略逊；SeedEdit 1.6 在多图参考、多轮编辑上受限；情绪化人像表达略弱于 Midjourney。报告**未披露**参数量、数据绝对规模、训练算力等工程数字，复现性有限。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2504.11346
- arxiv_pdf: https://arxiv.org/pdf/2504.11346
- 官方技术报告页 / project page: https://seed.bytedance.com/en/seedream3_0 （= team.doubao.com/tech/seedream3_0，原 worklist 的 team.doubao.com/en/special/seedream3_0 已 404，站点迁移）
- 中文项目页: https://seed.bytedance.com/zh/tech/seedream3_0
- 火山引擎 API（Model ID Doubao-Seedream-3.0-t2i）/ 豆包 https://www.doubao.com/chat/create-image / 即梦 https://jimeng.jianying.com/ai-tool/image/generate

## 本地落盘文件
- ../../../sources/omni/2025/arxiv-2504.11346.pdf （技术报告 PDF，42MB，未入 git）
- ../../../sources/omni/2025/seedream-3-0--project-page.md （英文官方项目页快照）
