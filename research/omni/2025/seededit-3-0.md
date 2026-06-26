---
title: "SeedEdit 3.0: Fast and High-Quality Generative Image Editing"
org: "ByteDance Seed"
country: China
date: "2025-06"
type: tech-report
category: edit
tags: [image-editing, instruction-editing, diffusion, vlm, reward-model, rectified-flow, distillation, bytedance]
url: "https://seed.bytedance.com/en/tech/seededit"
arxiv: "https://arxiv.org/abs/2506.05083"
pdf_url: "https://arxiv.org/pdf/2506.05083"
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://seed.bytedance.com/en/tech/seededit"
downloaded: [arxiv-2506.05083.pdf, seededit-3-0--blog.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
SeedEdit 3.0 是字节跳动 Seed 团队的**指令式真实图像编辑**模型，把底座从 Seedream 2.0 换成原生 1024×1024 的 [[seedream-3-0]]，靠"meta-info（元信息）数据混合范式 + diffusion loss 与 reward loss 联合训练"两大改进，把真实图编辑的**可用率（Usability Rate）从 SeedEdit 1.6 的 38.4% 拉到 56.1%**，同时显著快于 GPT-4o（约 15s vs 50s），且 GPT-4o（37.1%）、Gemini 2.0（30.3%）均被反超。

## 背景与定位
指令式真实图编辑（"把 STOP 改成 WARM""让女孩变写实""把帽子改成红色"）的核心瓶颈是**高质量配对编辑数据的稀缺**与**真实图域 vs 合成图域的分布鸿沟**。早期工作（[[instructpix2pix]]、HIVE、HQ-Edit、UltraEdit、MagicBrush）用 GPT/Prompt2Prompt 合成编辑对，但合成数据对生成模型有强偏置，迁移到真实图时性能下降；Emu Edit、OmniEdit 改用多个专家模型生成真实图数据。近期统一生成/编辑路线（OmniGen、Transfusion、Mogao）把文本与图像放进单一 transformer，或像 Step1X-Edit、MetaQueries、DreamEngine 那样把 MLLM 的图文 latent 接到 diffusion decoder；GPT-4o、Gemini 2.0 则靠图文联训展现强指令跟随。

SeedEdit 3.0 是 ByteDance **SeedEdit 系列**（SeedEdit 1.0/1.5/1.6 → 3.0，对应论文 arXiv:2411.06686 的 "SeedEdit: Align Image Re-generation to Image Editing"）的最新版，定位**闭源商业产品**——上线于即梦（Jimeng）、豆包（Doubao）等字节 App，核心诉求是真实图上的**指令跟随 + 内容/身份（ID/IP）一致性 + 速度**三者的最佳折中。注意版本号从 1.6 直接跳到 3.0，是为对齐同期发布的底座 [[seedream-3-0]] 的版本号。

## 模型架构
延续 SeedEdit 1.0（arXiv:2411.06686）的**"VLM 在下、causal diffusion 在上、connector 居中"双塔结构**：

- **底层 SeedVLM**（Seed1.5-VL，arXiv:2505.07062）：从输入图推断高层语义信息（编辑意图、任务类型）。
- **顶层 causal diffusion 网络**：复用扩散过程本身作为图像编码器，捕捉输入图的细粒度细节（人脸 ID、发丝纹理等），从而实现高保真保留。架构图中包含 VAE、ViT、MLP、MM-Attn（多模态注意力）、Time Embed 等模块。
- **connector / meta-info embedding 模块**：居中对齐编辑意图（任务类型、编辑 tag）与扩散模型；本版关键改动是引入 **meta-info embedding**，把数据级 task label、像素级 editing tag 通过**独立的 task embedding** 注入扩散模型（而非 HIVE 那种 prompt-based 注入），论文称独立 task embedding 比 prompt 注入更能让模型区分不同数据源的属性。可选叠加 CFG（classifier-free guidance）trick。

本版三个具体架构升级：
1. **底座换代**：把 SeedEdit 1.x 用的 Seedream 2.0 扩散网络换成 [[seedream-3-0]]——可**原生输出约 1024×1024 分辨率、无需 refiner**，直接提升细节保留（人脸/物体身份）和双语文字渲染、字符级文字编辑能力。
2. **独立 task/tag embedding**：分别为 task label 与 tag 设独立 embedding 注入。
3. **可泛化到多模态图像生成**：作者称该结构可轻松推广到多模态图像生成任务。

参数量未披露（仅在 Fig.2 用"点大小"示意模型规模随版本增大）。底层 VLM 为 Seed1.5-VL，VAE/text encoder 具体配置随 Seedream 3.0，论文未单列。

## 数据
数据工程是本报告的最大篇幅，核心是**多源混合 + meta-info 多粒度标签**。

**四类数据源**：
- **合成数据（Synthesized）**：沿用 SeedEdit 1.0 的"给定内部 T2I [[seedream-3-0]] 与 VLM 做 prompt 采样 + noise 采样"的配对采样策略；本版新增 **importance sampling（重要性采样）**，让采样分布感知重要的、长尾的编辑类别与主体，显著拓宽输入与编辑样本空间的覆盖。可生成 >1024×1024、带丰富 caption 的图。
- **编辑专家（Editing specialists）**：以真实图为输入的第一类数据，来自内部社区大量 image editing specialists——ComfyUI 工作流、内部优化的风格化、背景修改、光照调整、身份感知 DreamBooth、文字编辑等；这些 workflow 吃真实图、产出高质量编辑图，特别有助于覆盖真实图输入场景，并能快速补齐产品缺失能力（参考 OmniEdit 思路）。
- **传统编辑算子（Traditional Edit Operators）**：来自传统编辑工具/软件的高质量真实图操作——镜头模糊、光照调整、裁剪、模板海报印刷等（参考 PromptFix）。编辑图基于单一物体多次拍摄或模板化编辑生成；虽覆盖编辑域有限，但能让模型产出**真实、准确**的渲染结果，给真实图域提供准确的 loss 方向。
- **视频帧与多镜头（Video Frames & Multi Shots）**：视频天然提供成组相关图像。先从每个视频片段随机抽若干关键帧，用 **CLIP 图像相似度 + 光流（optical flow）**做粗过滤，再用 VLM 重标注（recaption），大规模补充多样真实图数据以提升泛化。

**数据合并（Data Merging）——多粒度标签策略**（直接混合不同源会因编辑风格差异导致性能退化，故引入三级标签）：
- **Task Label（数据级任务标签）**：区分不同源。例如"change to Paris"在传统编辑里是简单背景替换，在 IP/ID 保留任务里可能要改全部像素；用 task label 消歧。高质量传统指令编辑数据被打**默认 editing label**，并应用于所有测试输入。
- **Re-captioning（文本级重标注）**：把重标注拆成两步——(1) 找出两图的所有差异与相似处；(2) 基于差异生成 caption/指令。解决合成 prompt-to-prompt 对常含 prompt 未描述的意外改动、视频帧只有 clip 级 caption 没有帧间指令等问题，分解式重标注提升了描述准确度与细节。
- **Tagging（像素级标签）**：用 VLM 或专用模型标注 **local editing / face preservation / structure preservation / style preservation** 等 editing tag。训练时模型同时条件于 task label、editing tag、重标注后的编辑 prompt。

**双语平衡**：用 SeedVLM 做中英双语 prompt 采样与重标注，保证双语设置下性能均衡。

**前向/后向双向训练**：重标注、过滤、对齐后，所有数据可同时做正向与反向编辑操作训练，进一步均衡覆盖。

数据**总规模未披露**（论文只说"scale editing data effectively"、"几百张测试图"，训练量级无具体数字）。

## 训练方法
**扩散目标**：采用 **rectified flow matching（修正流匹配）** 作为 diffusion loss（论文此处引用 [13] = Black Forest Labs FLUX）。

**联合学习 pipeline（核心创新之一）——diffusion loss + reward loss 融合**：
普通 diffusion loss 对图像每个部分一视同仁，但人脸身份、某些细节结构、美学对用户尤其高价值。故引入一组 **reward model 联合训练**，修正后的损失为：

```
L = E_{t,q} || v_θ(x_t1, t | c, x0) − (ε − x1) ||²₂  +  Σ_i λ_i · R_i(x0, x*1 | c, t)
```

其中 R_i 是各 reward 模型给出的奖励（如人脸身份、文字渲染、结构保留），c 是条件（指示是否该考虑该 reward），λ_i 为权重。关键设计：reward 只在能从时刻 t 可靠估计输出图 x*1、且指令上下文 c 合适时才施加——例如指令要求"换脸"时就不施加人脸身份保留 reward。作者解释为何用**一组专家 reward 模型而非统一 VLM**：当前 VLM-based 模型不擅长 detail partition（细节分区），专家 reward 模型性能更好，但预期 VLM 进步后这些 reward 可被合并替换。

**多阶段训练**：
- **预训练（pretraining）**：融合所有采集到的图像对。采用 **NaViT（Patch n' Pack）**支持不同分辨率/宽高比混批；按分辨率分组、从低到高**渐进式分辨率训练**，每组动态调整最大 token 长度以保持 batch size 一致，保留前一阶段信息。
- **微调（fine-tuning）**：从 curated 数据重采样大量高质量高分辨率数据，用一组 filter 模型 + 人工过滤共同筛选，保证质量与编辑类别覆盖；该阶段以 diffusion loss 为主，叠加上面的 reward 联合训练稳定编辑表现。
- **与 T2I 联合训练（Joint training with T2I）**：因编辑数据质量明显低于最好的 T2I 数据，故把编辑数据与 T2I 数据联训——好处一：注入高质量高分辨率图显著提升高分辨率编辑能力；好处二：保留模型原有 T2I 能力，提升编辑泛化。

## Infra（训练 / 推理工程）
训练算力/GPU 时/并行策略**未披露**。推理加速是工程重点，**蒸馏 + 量化两条线，端到端 8× 提速（从约 64s 降到 8s，不含 VLM 阶段）**：

**蒸馏（基于 Hyper-SD + RayFlow）**：
- **实例感知轨迹（RayFlow 思路）**：给每个样本分配自己定制的生成路径与独特目标分布，而非把所有样本都推向同一固定高斯先验，减少概率空间中的路径重叠，提升生成稳定性与多样性。
- **CFG 蒸馏**：把 guidance scale 编码成可学习 embedding，与 timestep encoding 融合，靠针对性 CFG 蒸馏让模型在**单次前向**就给出 guided 输出，约 **2×** 提速，同时保留按需调 guidance 强度的能力（原本 CFG 需条件/无条件两次前向）。
- **统一噪声参考（Unified Noise Reference）**：用预训练网络预测单一噪声参考向量作为每步常量引导，对齐去噪过程，减少采样步数而不损保真；理论上最大化前向（data→noise）与反向（noise→data）轨迹的联合似然。
- **自适应时间步采样（Adaptive Timestep Sampling）**：结合 Stochastic Stein Discrepancy（SSD）准则与一个轻量神经模块学习数据驱动的 timestep 分布，集中训练在 loss 下降最大的关键时间步，降方差、加速收敛、省训练成本。
- **少步高保真采样**：用高度压缩的去噪 schedule，步数远少于标准基线，却能在美学、文图对齐、结构准确度上匹配甚至超过需 **75 NFE** 的方法。

**量化与整体提速**：针对 DiT 规模，用 **kernel fusion + 访存合并**优化算子（部分算子性能翻倍以上）；对 GEMM 与 Attention 模块做**低比特量化**——自适应混合量化、离线 smoothing 处理离群值、对敏感层用 search-based 策略找最优量化粒度与缩放因子、最后用 PTQ（训练后量化）逐层调参；配套高效量化算子支持多种粒度/位宽。

**部署形态**：上线即梦（Jimeng）、豆包（Doubao）及其他字节 App，闭源商业服务，无开源权重。

## 评测 benchmark（把效果讲清楚）
评测用**内部基准**（几百张真实+生成图，含 stylization/add/replace/delete 及相机运动、物体位移、场景切换等更难指令，论文称比公开基准更难、更贴近真实用户使用）。

**人评指标（0–5 三维 + 满意率）**：
- 三维：Instruction Response（是否响应指令）、Image Consistency（编辑后是否保留身份）、Image Quality（有无瑕疵）。
- **Usability Rate（可用率）**：不满意点 <3 的结果占比；**Satisfactory Rate（满意率）**：0 不满意点占比。可视化时 Usability 上限设 60%、Satisfaction 上限设 30%（标准严格）。

**核心人评结果（Usability Rate）**：

| 模型 | Usability Rate | 速度 |
|---|---|---|
| **SeedEdit 3.0** | **56.1%** | 约 10–15 s/图 |
| SeedEdit 1.6 | 38.4% | — |
| GPT-4o | 37.1% | 约 50–60 s/图 |
| Gemini 2.0 | 30.3% | — |

结论：GPT-4o 指令跟随最强，但**图像一致性（CLIP image similarity、face similarity）明显偏弱**，拉低人评满意率；SeedEdit 3.0 在指令跟随、内容保留、图像质量三者间取得**最佳折中**，满意率最高且速度快得多（约 15s vs 50s）。

**自动评测（Fig.6，与历代版本及 SoTA 对比）**：
- 指标：CLIP image similarity、CLIP direction score（InstructPix2Pix 提出）、GPT Mean Score（用 GPT-4o 打分，HQ-Edit 方法）、Face Similarity。
- 对比对象：SeedEdit 1.0/1.5/1.6、Step1X-Edit（1024 分辨率开源版）、Gemini 2.0、GPT-4o。SeedEdit 3.0（图中黄点）在 GPT Mean Score–CLIP image similarity 与 GPT Mean Score–Face Similarity 两个平面均位于右上（更优），显著超越历代版本，并优于 Gemini、Step1X。GPT-4o 位于右下角——指令跟随好但图像一致性差。
- 评测公平性处理：Step1X 跑开源 1024 分辨率；GPT-4o/Gemini 走官网对话窗口、每条跑 4 次选最好；未响应的 query（GPT-4o/Gemini 常见）在评测中略去。
- **注**：论文 Fig.6 为散点图，未给出每个数据点的精确数值；下文报告 ablation 即靠"加数据源→加数据合并+reward"逐版提升体现，但**逐点数字未在文本中列出**。

**消融（Ablation）**：通过对比 SeedEdit 1.0 →1.5（加更多数据源）→1.6（加数据合并策略 + reward modeling）→3.0（换 Seedream 3.0 底座 + meta-info + 联合训练），验证各策略的逐级增益。

速度数字：蒸馏+量化前约 64s，之后端到端 8s（不含 VLM）；整体单图约 10–15s。

## 创新点与影响
**核心贡献**：
1. **meta-info 数据混合范式 + meta-info embedding**：用 task label / recaption / tagging 三级粒度标签，把合成/编辑专家/传统算子/视频帧四类异质数据源有效混合，并通过独立 task embedding 紧密连接 VLM 与扩散模型——这是把真实图编辑数据"scale up 而不退化"的关键工程贡献。
2. **diffusion loss + reward loss 联合训练**：用一组条件化、时刻感知的专家 reward 模型（人脸身份/文字/结构）精确约束高价值属性，且按指令上下文 c 智能开关 reward，显著提升真实图的内容/身份一致性。
3. **8× 推理加速管线**：Hyper-SD + RayFlow 实例感知轨迹 + CFG 蒸馏 + 统一噪声参考 + 自适应时间步采样 + 低比特量化，使商业级编辑做到约 10–15s，远快于 GPT-4o。
4. 换代到原生 1024 的 [[seedream-3-0]] 底座，免 refiner，强化细节保留与双语字符级文字编辑。

**影响**：作为字节即梦/豆包的线上编辑引擎，是 2025 年中**闭源真实图编辑产品**在一致性+速度维度对标 GPT-4o/Gemini 2.0 的代表性工作；其 meta-info 多源混合与 reward 联合训练思路对后续编辑模型（尤其需混合真实+合成异质数据者）有借鉴价值。属 [[seedream]] / [[seedance]] 同系 Seed Vision 体系。

**已知局限（论文/伦理声明）**：
- 训练数据规模、模型参数量、训练算力等关键数字**全部未披露**（闭源产品）；自动评测 Fig.6 仅给散点图、无逐点数值。
- 指令跟随能力仍弱于 GPT-4o（作者承认 GPT-4o instruction response 最好），SeedEdit 赢在折中与速度。
- reward 用专家模型而非统一 VLM，是当前 VLM detail partition 能力不足的妥协，未来可能被更强 VLM 取代。
- 继承 T2I 模型的偏见与局限；伦理声明强调不得用于暴力/色情等场景，合成图应标注为 synthetic；训练图来自授权及 Unsplash/Pixabay 等免授权站。
- 无开源权重/代码，复现不可行。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2506.05083
- arxiv_pdf: https://arxiv.org/pdf/2506.05083
- official_blog / tech_report_page: https://seed.bytedance.com/en/tech/seededit
- product (即梦): https://jimeng.jianying.com/
- product (豆包): https://www.doubao.com/
- 前置工作 SeedEdit 1.0: https://arxiv.org/abs/2411.06686

## 一手源存档（sources/）
- [arxiv-2506.05083.pdf](https://arxiv.org/pdf/2506.05083) （技术报告全文 PDF，7 页，已精读正文/实验/附录）
- [blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/seededit-3-0--blog.md) （seed.bytedance.com 官方技术报告页快照）
