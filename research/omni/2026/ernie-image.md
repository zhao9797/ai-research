---
title: "ERNIE-Image Technical Report"
org: "Baidu (ERNIE-Image Team)"
country: China
date: "2026-05"
type: tech-report
category: t2i
tags: [text-to-image, dit, single-stream, latent-diffusion, flow-matching, dpo, distillation, dmd, text-rendering, open-weights, chinese]
url: "https://arxiv.org/abs/2605.25347"
arxiv: "https://arxiv.org/abs/2605.25347"
pdf_url: "https://arxiv.org/pdf/2605.25347"
github_url: "https://github.com/baidu/ernie-image"
hf_url: "https://huggingface.co/baidu/ERNIE-Image"
modelscope_url: "https://www.modelscope.cn/models/PaddlePaddle/ERNIE-Image/summary"
project_url: "https://yiyan.baidu.com/blog/posts/ernie-image"
downloaded: [arxiv-2605.25347.pdf, ernie-image--github-readme.md, ernie-image--hf-readme.md, ernie-image-turbo--hf-readme.md, ernie-image--blog.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
ERNIE-Image 是百度文心团队开源的 **8B 单流 DiT 文生图模型**（LDM 框架，Apache-2.0），核心主张是「**用数据挖掘而非参数堆叠**」逼近闭源旗舰：预训练用「自底向上」细粒度数据挖掘 + 后训练用「自顶向下」高需求场景精修 + **稳定化 DPO**（anchor loss 抑制 reward hacking），并以 **MT-DMD（多教师分布匹配蒸馏）** 把模型蒸到 8-NFE 的 ERNIE-Image-Turbo。最亮结果：GenEval **0.8856 居开源/同台第一**，在人评 in-house 测试集上仅次于闭源 Nano Banana 2.0、**为开源最强**，且 24GB 消费级显卡可跑。

## 背景与定位
论文直指当下文生图的两条路线困境：(1) 闭源旗舰（Google Nano Banana、字节 Seedream）效果领先但无法私有部署/垂域微调；(2) 开源侧要么靠**堆参数**（[[qwen-image]]、HunyuanImage）边际收益递减且算力门槛高，要么是 6B Z-Image 这类小而高效模型在「复杂指令遵循 + 中文文字渲染」等硬任务上仍有明显短板。ERNIE-Image 的定位是「**开源、强、人人可用**」——在 8B 这个可在 24GB 显存上部署的规模上，把三项开源模型最欠缺的能力做到 SOTA：**复杂指令遵循、文字渲染、美学生成**。它建立在 [[latent-diffusion-ldm]] 的潜空间扩散范式与 [[dit]] 的单流 Transformer 架构之上，是 2026 年「小模型 + 数据/后训练工程」对抗「大模型 scaling」路线的代表作之一。

## 模型架构
- **Backbone：单流 DiT（single-stream Diffusion Transformer）**，8B 参数（HF tag 标 8B；ERNIE-Image / ERNIE-Image-Turbo 同属一个 DiT 家族，Turbo 为蒸馏版）。「单流」即图像 latent token 与文本条件在同一 Transformer 流中处理（区别于 MMDiT 的双流），架构上更紧凑。
- **VAE：直接复用 [[flux-2]] 的 FLUX.2 VAE**（Black Forest Labs, 2025），论文称其提供了「强开源 latent space」用于高保真生成——这是一个值得注意的工程取舍：不自训 VAE，直接站在开源最强 VAE 肩上。
- **Text encoder：Ministral-3（3B）**（Mistral 系，Liu et al. 2026），而非主流的 T5-XXL/CLIP/大 LLM。这是 ERNIE-Image 区别于其他开源模型的关键设计——**用 3B 小文本编码器进一步压低显存与使用门槛**。论文通过实验论证：小尺寸文本编码器仍能支撑长而复杂的指令输入并提供有效条件空间。
- **Prompt Enhancer（PE）：一个独立的「**微调后的 Ministral 3B**」**（博客明确：fine-tuned Ministral 3B），把简短用户输入扩写成结构化的长 prompt（物体属性、空间关系、场景构图、文本内容、风格意图），生成前自动注入。PE 是即插即用模块，可与 DiT 同进程（`use_pe=True`）或独立部署（vLLM 起 PE 服务、SGLang 起 DiT 服务）。
- **分辨率策略：三阶段渐进**——256×256 → 512×512 → 1024×1024，**全程多宽高比训练**（非仅方图）。推荐推理分辨率：1024×1024、848×1264、1264×848、768×1376、896×1200 等。

## 数据
**预训练——自底向上（bottom-up）数据构建与采样**（与「自顶向下预定义数据分层重采样」相反，从海量原始内部图池出发逐步施加结构）：
1. **细粒度分类**：训练一个图像分类模型，把每张图归入 **10,000 个细粒度视觉类别**之一，作为后续数据均衡的语义划分基础——比粗粒度采样更能保留长尾概念、防止高频类别（dominant categories）压垮预训练分布。
2. **Caption 标注**：用一个微调的强 VLM（Qwen3 系，Yang et al. 2025）为全部图像生成 caption，**特别强调忠实识别并描述图内文字内容**（幻灯片、教学图、海报、UI 截图、文档类图像），因为漏标/错标文字会严重削弱图文对齐。论文核心洞察：**在训练早期就喂入详细图像描述，不仅强化复杂指令遵循，还显著丰富模型的世界知识**——因此「不刻意合成领域数据，而走更有针对性的标注策略」。
3. **美学打分**：用自研 ERNIE-Image-Aes 给全部图像打美学分，作为大规模过滤与采样的统一质量信号（取代纯启发式规则）。
4. **层级采样（hierarchical sampling，两级）**：类间——每个类别的采样权重由「语料规模 + 聚合美学质量」联合决定（既防高频类主导、又给高质量类更多概率质量）；类内——按美学分采样，让更高质量样本出现更频繁。

**后训练 SFT——自顶向下（top-down）数据构建**：先圈定优先领域（**海报设计、游戏截图、人像摄影、产品摄影、动漫风格**等高需求视觉品类），再为每个领域精挑高一致性数据（强调视觉质量 + 风格一致性）。用 VLM 给 SFT 语料生成结构化 caption；再用**更大的 VLM——Kimi K2.5（Team, 2026）**把原始 caption 改写并降采样成多样化 prompt（短关键词式、自然语言请求式、指令式、详细构图式），**对齐真实用户输入风格、缓解 caption 模型引入的偏置**。

数据**总规模、图文对数量、token 数均未披露**（仅称「海量但低质的图池」「内部数据池」）；安全/版权过滤细节未报告。

## 训练方法
- **基础训练目标**：潜空间扩散（LDM）+ Flow Matching（DPO 推导明确基于 FM 的 velocity-field 视角，引用 Lipman et al. 2023），训练采 256→512→1024 三阶段渐进 + 多宽高比 curriculum。
- **SFT**：在预训练基础上做监督微调，提升高价值领域的生成质量与指令对齐（详见数据节）。
- **DPO（在 Flow Matching 上的偏好对齐）**：基于人标偏好对直接优化策略。把 DPO 目标从 velocity-field 角度重写——给定 prompt 隐状态 h、胜样本 x0^win、负样本 x0^lose，用预测速度场 v_θ 的 **L2 重建误差**定义隐式 reward，构造 policy 与冻结 ref 的偏好间隔 Diff_policy / Diff_ref，目标 `L_DPO = −E[log σ(−β(Diff_policy − Diff_ref))]`（式 1–2，借鉴 Wallace et al. 2024 / Qwen-Image）。
  - **稳定化关键：Anchor Losses**。朴素 DPO 用在 DiT 上会 **reward hacking**——模型钻 L2 loss 无上界的空子，疯狂放大负样本误差尺度，导致表征坍塌（representation collapse）。解法是加 anchor 正则把基础生成能力「锚住」：`L_total = L_DPO + λ_win·E[ℓ^win_policy] + λ_lose·E[ℓ^lose_policy]`，其中 ℓ 为标准 FM 重建 loss。**超参明确：β=0.05，λ_win=0.35，λ_lose=0.15**。论文经验：当 base 与 reward model 都足够强时，**只需极少 DPO 步**即可达到目标状态，最小化 reward hacking。
- **蒸馏加速：MT-DMD（Multi-Teacher Distribution Matching Distillation）→ ERNIE-Image-Turbo（8 NFE）**。技术脉络：DMD（Yin 2023）→ DMD2（Yin 2024，解耦比例更新：score model 每更新 5 次、generator 更新 1 次）→ Decoupled DMD（Liu 2025，把优化拆成 CFG Augmentation「矛」与 Distribution Matching「盾」两正交目标避免梯度干扰）→ DMDR（Jiang 2025，引入 RL 原则 + 动态 step-aware LoRA 缩放教师 score model，real-path 引导强度 α_real(t) 用 cosine 调度，式 4）。
  - **MT-DMD 的创新动机——Capability Drift**：单一教师（即便加动态 LoRA 引导 + reward）在高度异质数据上无法给所有语义域提供一致最优监督，在专门子空间（排版/文字、风格化美学）易次优收敛。
  - **方法：Omni-Granular 多教师监督**。编排一个专家教师委员会 E={E1…EK}，各自隐式擅长不同域（**文字渲染专家、数字艺术专家、宏观构图和谐专家**等）。集成去噪预测 `x̂0 = Σ_k W_k(x_t,σ,c,O)·E_k(x_t,σ,c)`（式 5），门控概率 W_k∈[0,1] 自适应于噪声 latent x_t、噪声尺度 σ、语义条件 c、优化目标 O∈{CA,DM} 的联合状态空间。该路由形成「**单次训练实例内的非对称梯度拓扑**」：DM 罚项查询数字艺术专家保全局风格一致，CA 约束独立优化局部拼写/解剖保真（找文字渲染专家）；并沿扩散轨迹做「**专家无缝接力**」——高噪声段用空间布局专家定宏观构图，低噪声段切换到高频渲染专家（写实光照、材质纹理）。
- 训练总步数、batch、学习率、优化器、各阶段数据量等**未披露**。

## Infra（训练 / 推理工程）
- **训练 infra：几乎完全未披露**——算力规模、GPU·时、并行/分布式策略、混合精度、吞吐均未报告（这是本报告作为偏「方法 + 效果」型 tech report 的明显空白）。
- **推理 / 部署形态**（来自 GitHub README / HF card，一手）：
  - **ERNIE-Image（SFT）**：50 steps，CFG=4.0。**ERNIE-Image-Turbo（蒸馏）**：8 steps，CFG=1.0。权重 bfloat16。
  - **24GB VRAM 消费级显卡即可运行**（论文与博客反复强调的「易部署」卖点）。
  - 框架支持：**Diffusers**（官方 `ErnieImagePipeline`）、**SGLang**（`sglang serve`，OpenAI 兼容 `/v1/images/generations`）、**vLLM**（独立部署 PE 服务，`transformers==5.4.0`）、**ComfyUI**（官方 Turbo workflow 模板）、**Unsloth**（GGUF 量化权重）、**AI-Toolkit**（微调）。
  - PE 部署两种模式：内置 PE（DiT 进程内 `use_pe=True`）或 PE/DiT 分离部署（vLLM 起 PE + SGLang 起 DiT，提速 PE 推理）。
- 量化、缓存、具体单图延迟/吞吐数字未报告（仅给步数）。

## 评测 benchmark（把效果讲清楚）
数字均来自已抓取的一手源（arXiv PDF Table 3–7 + GitHub/HF README benchmark 表，两者一致，README 给到四位小数）。

**① 人类偏好评测（in-house 测试集，Table 3）** —— 7 维（空间结构 / 世界理解 / 物理一致 / 美学设计 / 风格匹配 / 创意 / 知识准确），各模型匿名打 pass/fail。Total HP（Overall）排名：
- Nano Banana 2.0（闭源）**5.39** → **ERNIE-Image 5.07（开源第一、总第二）** → Seedream 5.0 5.03 → Wan2.7-Image 4.96 → Qwen-Image-2512 4.78 → **ERNIE-Image-Turbo 4.65** → FLUX.2-klein-9B 4.59 → Z-Image-Turbo 4.56 → Qwen-Image 4.52。
- 结论：8B 的 ERNIE-Image **超过更大的 Qwen-Image 系列**，逼近最新闭源商业模型；闭源 Nano Banana 2.0 在所有子维领先（如 World Understanding 98.51、Knowledge Accuracy 99.40），ERNIE-Image 紧随（94.05 / 95.24）。

**② GenEval（Table 4，组合生成）** —— ERNIE-Image (w/o PE) **Overall 0.8856（榜首）**，单物体 1.0000、属性绑定 0.7925、位置 0.8550 均为全表最强档（属性绑定全表最高；位置子项 w/o PE 0.8550 与 w/ PE 0.8625 包揽前二）；对比 Qwen-Image 0.8683、FLUX.2-klein-9B 0.8481、Z-Image 0.8400、GPT Image 1 0.84、Z-Image-Turbo 0.8233。ERNIE-Image-Turbo (w/o PE) 0.8667 仍高于多数基线。**注意：position/attribute-binding 上加 PE 反而略降**（PE 主要利好结构化/知识型长 prompt，对 GenEval 这类短组合 prompt 非全面正收益）。

**③ LongText-Bench（Table 5，长文本渲染，中英）** —— ERNIE-Image (w/ PE) Overall **0.973**（EN 0.980 / ZH 0.966），仅次于闭源 Seedream 4.5 (0.988)，**高于 GLM-Image 0.966、Nano Banana 2.0 0.965、Qwen-Image-2512 0.960**。中英差距极小，体现强跨语种文字渲染与字符级空间协调。对照：FLUX.2-klein-9B 的 ZH 仅 0.218（西方模型中文渲染崩塌的典型）。

**④ OneIG-Bench（Table 6 EN / Table 7 ZH，全维评测：对齐/文字/推理/风格/多样性）**：
- OneIG-EN：ERNIE-Image (w/ PE) Overall **0.5750（第三）**，仅次 Nano Banana 2.0 (0.578)、Seedream 4.5 (0.576)，且 Reasoning 0.3566 为全表最高；高于 Seedream 4.0/Qwen-Image/FLUX.2-klein/GLM-Image。
- OneIG-ZH：ERNIE-Image (w/ PE) Overall **0.5543（开源第一、总第二）**，仅次 Nano Banana 2.0 (0.567)，高于 Seedream 4.0/4.5、Qwen-Image、Z-Image、GLM-Image。

**⑤ ERNIE-Image-Aes 美学模型（Table 2，在自建 ERIA-1K / ERNIE-Image-Aes-1K 基准上）** —— 从 ArtiMuse（8B VLM）初始化微调。SRCC/PLCC：**ERNIE-Image-Aes 0.7445 / 0.7598**，碾压 UniPercept (0.4533/0.4748)、ArtiMuse (0.4277/0.4704)、LAION-AES (0.2944/0.3138)。论文还系统揭示了既有美学预测器的偏置：LAION-Aes 给 AI 生成图/随手拍打高分；ArtiMuse/UniPercept 偏好黑白照片。
  - **ERIA-1K 基准**：1000 图，6 类别按真实世界分布配比（摄影 49.28%、插画/动漫 23.16%、平面/海报 11.14%、混合网图 10.44%、胶片摄影 5.42%、产品/收藏 0.56%），由央美、川美、中传等专业美术/设计/摄影背景标注者标注。
  - **标注方法创新——瑞士轮（Swiss-system tournament）成对比较**：相比 Likert 绝对评分（有 score drift）和 ELO（需海量对比才稳定），瑞士轮按当前排名配对、用更少总对比即得可靠排名（tier 1–10）；质控两关键：标注者须过美学校准测试、且每人独立完成完整 tournament（多人混标会因隐式标准互相干扰）。

**⑥ Prompt Enhancement 消融（4.1 节，定性）**：在白板解数学题、HD-2D RPG 截图、网页布局三任务上，无 PE 时模型只「表面遵循」（缺结构）；3B PE 显著补全布局/文字/结构；更大 LM PE 在需推理/世界知识的任务上进一步提升（如白板数学推导的正确性与完整性）。

> 未报告：FID、CLIPScore、T2I-CompBench、MJHQ-30K FID、HPSv2/ImageReward/PickScore、推理延迟/吞吐绝对数字、训练算力。

## 创新点与影响
**核心贡献**：
1. **「数据挖掘 > 参数 scaling」的实证**：用 8B 模型 + 自底向上细粒度数据挖掘（10k 类细分 + 文字感知 caption + 美学打分 + 两级层级采样），在 GenEval 居首、人评开源第一，挑战「文生图必须堆大模型」的惯性认知。
2. **稳定化 DPO（anchor loss）**：针对 DiT 上 DPO 的 reward-hacking/表征坍塌给出工程化解法（β=0.05、λ_win=0.35、λ_lose=0.15），并指出「强 base+强 reward 只需极少步」的实用经验。
3. **MT-DMD 多教师蒸馏**：用域专家委员会 + 动态门控路由缓解单教师蒸馏的 **capability drift**，实现噪声尺度/语义域/优化目标上的「专家接力」，让 8-NFE 学生在文字/风格等专门子空间不掉点。
4. **工业级美学体系开源**：ERNIE-Image-Aes（SOTA 美学模型）+ ERIA-1K（贴近真实分布的人标基准）+ 瑞士轮标注法，给社区一套去偏的美学评估基建。
5. **极致易用**：3B Ministral 文本编码器 + FLUX.2 VAE 复用 + 3B PE，让模型 24GB 显存可跑、Diffusers/SGLang/vLLM/ComfyUI/Unsloth 全链路支持，**Apache-2.0 全量开源**（ERNIE-Image、ERNIE-Image-Turbo、PE、ERNIE-Image-Aes、ERIA-1K）。

**影响**：作为 2026 年「中文强、文字渲染强、消费级可部署」的开源 T2I，直接对标 Qwen-Image / Z-Image / GLM-Image / FLUX.2-klein 等开源同台，并把 anchor-DPO、MT-DMD、瑞士轮美学标注三项方法贡献回社区。

**已知局限**（来自一手源）：训练 infra/算力/数据规模几乎全未披露，可复现性受限；3B PE 在需深度领域知识（数学推理）或极丰富世界知识的任务上会力不从心（博客自陈），需更大 LM PE 补强；GenEval 上 PE 对短组合 prompt 非全面正收益；HF metadata 存在 8B（tags）与 7B（model_size 字段）的标注不一致，论文正文与博客统一称 8B DiT。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2605.25347
- arxiv_pdf: https://arxiv.org/pdf/2605.25347
- blog（官方，一等公民）: https://yiyan.baidu.com/blog/posts/ernie-image
- github: https://github.com/baidu/ernie-image
- hf（ERNIE-Image）: https://huggingface.co/baidu/ERNIE-Image
- hf（ERNIE-Image-Turbo）: https://huggingface.co/baidu/ERNIE-Image-Turbo
- modelscope（ERNIE-Image）: https://www.modelscope.cn/models/PaddlePaddle/ERNIE-Image/summary
- modelscope（ERNIE-Image-Turbo）: https://www.modelscope.cn/models/PaddlePaddle/ERNIE-Image-Turbo/summary
- art gallery: https://ernieimageprompt.com

## 本地落盘文件
- ../../../sources/omni/2026/arxiv-2605.25347.pdf
- ../../../sources/omni/2026/ernie-image--blog.md
- ../../../sources/omni/2026/ernie-image--github-readme.md
- ../../../sources/omni/2026/ernie-image--hf-readme.md
- ../../../sources/omni/2026/ernie-image-turbo--hf-readme.md
