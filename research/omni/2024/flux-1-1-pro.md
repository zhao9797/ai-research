---
title: "FLUX1.1 [pro]"
org: Black Forest Labs
country: EU
date: "2024-10"
type: blog
category: t2i
tags: [t2i, flux, rectified-flow, flow-matching, mmdit, closed-source, api, high-resolution]
url: "https://bfl.ai/blog/24-10-02-flux"
arxiv: ""
pdf_url: ""
github_url: "https://github.com/black-forest-labs/flux"
hf_url: ""
modelscope_url: ""
project_url: "https://bfl.ai"
downloaded: [flux-1-1-pro--blog.md, flux-1-1-pro-ultra-raw--blog.md, flux-1--bfl-launch-blog.md, flux-1--gh-modelcard-dev.md, flux-1--github-readme.md, arxiv-2506.15742.pdf]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位

FLUX1.1 [pro] 是 Black Forest Labs（BFL）2024-10-02 发布的闭源旗舰文生图模型，在不公开权重的前提下把上一代 [[flux-1]] [pro] 的生成速度提升约 6 倍（同时 [pro] 也提速 2 倍），并提升画质、提示遵循与多样性；以代号 "blueberry" 匿名进入 Artificial Analysis 文生图竞技场后登顶 Elo 榜首（截至 2024-10-01）。一个月后（2024-11-06）追加 **Ultra 模式**（4× 分辨率、最高 4MP、单图约 10s）与 **Raw 模式**（更真实的"非合成"摄影质感），并随之上线商业化的 **BFL API**（FLUX1.1 [pro] 定价 4 美分/图）。

## 背景与定位

FLUX1.1 [pro] 不是一篇带论文/技术报告的研究发布，而是 BFL 的**产品级闭源升级 + API 商业化**节点，应放在 FLUX 家族的演进脉络里理解：

- 2024-08-01 BFL 成立，首发 [[flux-1]] 三件套：FLUX.1 [pro]（闭源 API 旗舰）、FLUX.1 [dev]（开放权重、非商用、从 [pro] 指引蒸馏）、FLUX.1 [schnell]（Apache-2.0 少步蒸馏）。三者共享同一 12B rectified-flow transformer 骨干，建立在 [[flow-matching]] / [[rectified-flow]] 与 [[latent-diffusion-ldm]] 的潜空间训练范式之上。
- 2024-10-02 本次发布 FLUX1.1 [pro]：定位为"更快更好"的下一代闭源旗舰，主打**推理效率 × 画质**的更优折中，并首次把 BFL API 推向 GA（beta）。
- 2024-11-06 增量发布 Ultra/Raw 两种模式，把分辨率上限拉到 4MP 并补齐"真实摄影感"这一审美维度。
- 后续家族（[[flux-1-tools]]、FLUX.1 Kontext、FLUX.1 Krea、FLUX.2…）继续在同一骨干上扩展可控编辑与统一生成。

BFL 团队的技术血统直接决定了 FLUX 的方法选择：核心成员是 VQGAN、Latent Diffusion、Stable Diffusion（含 SDXL、Stable Video Diffusion）、Rectified Flow Transformers、以及 Adversarial Diffusion Distillation（ADD）的作者（据 FLUX.1 发布博客）。因此 FLUX1.1 [pro] 本质是"潜空间 rectified-flow MMDiT + 对抗蒸馏加速"这一路线的工程化巅峰。

> 重要边界：BFL **从未为 FLUX.1 / FLUX1.1 系列发布正式技术报告**（发布博客称"will publish a more detailed tech report in the near future"，但针对 t2i 基座始终未兑现）。下面"模型架构/训练方法"中可考证的细节，主要来自同骨干的 **FLUX.1 Kontext 技术报告（arXiv:2506.15742）** 与 FLUX.1 发布博客；凡 FLUX1.1 [pro] 自身未单独披露处，均明确标注为"沿用家族骨干（推断）"或"未披露"。

## 模型架构

FLUX1.1 [pro] 官方未单独公布架构图或参数量。以下为其所属 FLUX.1 骨干家族的公开设计（来自 FLUX.1 发布博客与 arXiv:2506.15742），FLUX1.1 [pro] 是在该骨干上做的迭代版本：

- **整体范式**：在图像 autoencoder 的潜空间中训练的 **rectified flow transformer**（潜空间扩散/流匹配），而非像素空间建模。
- **VAE / autoencoder**：自训练的卷积 autoencoder，**对抗目标从零训练**；相比同类放大了训练算力并采用 **16 个潜通道（16 latent channels）**，以提升重建质量。该 autoencoder 在下游训练中被冻结使用。
- **DiT 骨干（hybrid MMDiT + 单流）**：由**双流（double stream）块 + 单流（single stream）块**混合构成。
  - 双流块：图文 token 各自独立权重，通过对"图文 token 拼接序列"做注意力实现跨模态混合（即 MMDiT 式设计）。
  - 单流块：双流之后把序列拼接，再过 **38 个单流块**作用于图文 token；最后丢弃文本 token、只解码图像 token。
  - **融合 FFN（fused feed-forward）**：受 Dehghani 等启发，把单流块的调制参数量减半，并将注意力的输入/输出线性层与 MLP 融合成更大矩阵乘，提升训练/推理的 GPU 利用率。
- **位置编码**：**因子化三维旋转位置编码（3D RoPE）**，每个潜 token 以 (t, h, w) 时空坐标索引（单图时 t≡0）。这天然支持任意分辨率/宽高比，也为后续多图上下文（Kontext）与高分辨率（Ultra）扩展铺路。
- **文本编码器**：FLUX1.1 [pro] 官方博客未点名。家族实现（开源 FLUX.1 [dev]/[schnell] 推理代码）使用 **T5（文本主干）+ CLIP（池化文本嵌入做条件调制）** 双文本编码器（开源参考实现公开事实；本页未单独抓取该实现文件，标注为家族常识，非 FLUX1.1 独立披露）。
- **参数量与分辨率策略**：FLUX.1 家族骨干为 **12B 参数**（发布博客）；FLUX1.1 [pro] 未单独公布是否同为 12B（**未披露**）。分辨率上，FLUX.1 家族"支持 0.1–2.0 MP 区间的多种宽高比/分辨率"（发布博客原文）；FLUX1.1 [pro] 发布博客预告"原生支持快速超高分辨率，up to 2k，coming soon"，随后由 2024-11-06 的 **Ultra 模式**兑现为 **4× 分辨率、最高 4MP**，且"不牺牲提示遵循"。标准档 FLUX1.1 [pro] 的默认/最高分辨率官方未单独给出明确数字（**未单独披露**）。

> 与 [pro] 的关系：FLUX1.1 [pro] 是 FLUX.1 [pro] 的换代版本（"our most advanced and efficient model yet"），同代还把旧 FLUX.1 [pro] 更新为"输出不变但快 2 倍"。两者是否为同一权重的不同蒸馏/同一新权重的不同档位，官方**未披露**。

## 数据

**FLUX1.1 [pro] 的训练数据来源、规模、配比、清洗/过滤、re-captioning、合成数据占比均未披露。** BFL 对 t2i 基座既无技术报告也无 data card，本次两篇发布博客只字未提数据。可作为侧面参考的同骨干信息（来自 arXiv:2506.15742，针对 Kontext，但反映家族数据处理取向）：

- 训练时按数据分辨率改变 logit-normal 时间步采样的众数 µ（resolution-dependent shift schedule），说明家族在**多分辨率混合数据**上训练。
- 家族在安全侧采用**基于分类器的过滤 + 对抗训练**，以阻止 NCII/CSAM 等违规内容生成（Kontext 报告明确；FLUX1.1 [pro] 博客也提到 API 提供"content moderation"内容审核选项）。
- Raw 模式"显著提升人物主体多样性、增强自然摄影真实感"的能力，暗示其在数据/微调侧专门强化了**真实摄影分布**与多样性保持，但具体数据细节**未披露**。

结论：数据维度基本为黑盒，本页不臆造任何规模/配比数字。

## 训练方法

FLUX1.1 [pro] 未单独披露训练流程。基于家族骨干（FLUX.1 发布博客 + arXiv:2506.15742）可确证的方法栈：

- **训练目标：rectified flow matching（速度预测）**。损失为 L = E‖v_θ(z_t,t,·) − (ε − x)‖²，其中 z_t = (1−t)x + tε 为潜空间中 x 与噪声 ε 的线性插值；时间步 t 采用 **logit-normal shift 调度**，众数 µ 随训练数据分辨率变化。这是 SD3/Rectified-Flow Transformer 一脉的标准做法。
- **多阶段**：家族范式为"先纯文生图预训练 → 再做任务化微调"。对开源档位，FLUX.1 [dev] 通过**指引蒸馏（guidance distillation）**从 FLUX.1 [pro] 蒸出（12B），FLUX.1 [schnell] 为少步蒸馏开放档。FLUX1.1 [pro] 自身的预训练/微调阶段细节**未披露**。
- **加速 / 蒸馏（最关键的"6× 提速"来源，方法层面）**：家族用**对抗扩散蒸馏 / 潜空间对抗扩散蒸馏（ADD / LADD）**把 50–250 步的流匹配采样压缩到极少步数，同时用对抗训练抑制高引导带来的过饱和伪影（arXiv:2506.15742 明确把 LADD 用于 [pro] 档；ADD 是 BFL 团队的代表作）。FLUX1.1 [pro] 博客只给出"比 FLUX.1 [pro] 快 6×、比当前可用的 FLUX.1 [pro] 快 3×"的**结果数字**，未公布它具体是更激进的步数蒸馏、新骨干、还是推理工程优化的组合——**方法归因未单独披露**，但 ADD/LADD 蒸馏是家族公开的加速基石。
- **训练精度/并行/吞吐（家族实践，来自 Kontext 报告）**：FSDP2 + 混合精度（all-gather 用 bfloat16，梯度 reduce-scatter 用 float32 以提升数值稳定性）；用 **selective activation checkpointing** 降低峰值 VRAM；为提吞吐用 **FlashAttention 3** + **对单个 Transformer 块做 regional compilation（局部编译）**。这是 Kontext 的实现，FLUX1.1 [pro] 是否完全一致**未确证**。
- **Ultra 模式**：在保持提示遵循的前提下做 4× 分辨率（≤4MP）生成且仅 ~10s/图、比同类高分模型快 >2.5×——3D RoPE 的任意分辨率特性 + 蒸馏少步采样是其工程基础；是否额外做高分辨率 continue-training/微调**未披露**。

## Infra（训练 / 推理工程）

- **训练算力 / GPU·时 / 集群规模 / 吞吐：全部未披露。** FLUX1.1 [pro] 无技术报告。
- **推理加速**：核心卖点即推理工程——FLUX1.1 [pro] 比初代 FLUX.1 [pro] 快约 **6×**，比"当前可用的 FLUX.1 [pro]"快 **3×**；Ultra 模式 4MP 仅 ~10s/图、比同类高分方案快 **>2.5×**。底层依赖 ADD/LADD 步数蒸馏（家族）。开源 FLUX.1 推理仓库提供 **TensorRT** 支持（NVIDIA PyTorch 镜像、enroot），反映家族推理走 TensorRT 加速路线；FLUX1.1 [pro] 闭源服务端的具体量化/编译细节**未披露**。
- **部署形态**：纯 **API / 托管服务**（闭源、不放权重）。除 BFL 官方 API 外，发布即上线 **Together.ai、Replicate、fal.ai、Freepik** 等第三方平台。
- **商业化**：随发布开放 beta BFL API（docs.bfl.ml / 现 docs.bfl.ai），按图计费——FLUX.1 [dev] 2.5 ¢/图、FLUX.1 [pro] 5 ¢/图、FLUX1.1 [pro] 4 ¢/图、Ultra 模式 6 ¢/图（$0.06/image）。提供模型选择、分辨率、内容审核等可定制项。

## 评测 benchmark（把效果讲清楚）

FLUX1.1 [pro] 的官方评测以"匿名进 Arena 拿 Elo 第一"为核心，**未公布 FID/CLIPScore/GenEval 等量化指标数字**（无技术报告）。可考证的一手结果：

- **Artificial Analysis 文生图竞技场（Image Arena Elo）**：FLUX1.1 [pro] 以代号 **"blueberry"** 匿名进入该众包人评 Arena，**超越榜上所有模型，取得最高综合 Elo 分**（数据为 artificialanalysis.ai 截至 **2024-10-01**；FLUX.1 推理速度为 BFL 内部基准）。官方未在博客中给出具体 Elo 数值，本页据源只陈述"登顶 Elo 榜首"，**不臆造分数**。
- **速度（内部基准）**：相对初代 FLUX.1 [pro] **6× 提速**；相对"当前可用的 FLUX.1 [pro]" **3× 提速**；旧 FLUX.1 [pro] 同步更新为"输出不变、2× 提速"。Ultra 模式 4MP ~10s/图、比同类高分模型 **>2.5×** 快。
- **质量主张（定性）**：相对前代提升 image quality / prompt adherence / diversity；Raw 模式"显著提升人物多样性、增强自然摄影真实感"。这些为官方定性主张，无数字。
- **第三方/后续侧证**：BFL 自家的 FLUX.1 Kontext 技术报告（arXiv:2506.15742）在其 Internal-T2I-Bench（1000 条 prompts，含 DrawBench/PartiPrompts + 真实用户 query；另在 GenAI bench 上补测）中指出"FLUX.1 Kontext 在各类目上**一致地优于其前代 FLUX1.1 [pro]**"，从侧面把 FLUX1.1 [pro] 标定为彼时家族 t2i 的强基线；但**该报告同样未给出 FLUX1.1 [pro] 的独立绝对分数**。

> 诚实标注：FID、CLIPScore、GenEval、T2I-CompBench、DPG-Bench、MJHQ-30K、HPSv2、ImageReward、PickScore 等学术指标在 FLUX1.1 [pro] 一手源中**均未报告**。

## 创新点与影响

**核心贡献（产品/工程层面，非新方法论文）**：
1. **把"画质×速度"折中推到新前沿**：在不降质（甚至提质）前提下相对前代 6× 提速，验证了潜空间 rectified-flow + ADD/LADD 蒸馏路线在旗舰档位的工程可行性。
2. **匿名 Arena 登顶**：以盲测 Elo 第一（2024-10）确立 FLUX 在闭源旗舰 t2i 的领先地位，是 Midjourney/DALL·E 3 之外的强力第三极。
3. **Ultra/Raw 两个产品维度**：Ultra 把"高分辨率"与"快"解耦（4MP/10s），Raw 把"真实摄影感/主体多样性"显式产品化——后者预示了后续社区对"AI 味"反感的纠偏方向（与 FLUX.1 Krea [dev] 的"opinionated 审美"一脉相承）。
4. **BFL API 商业化落地**：4 ¢/图的旗舰定价 + 多第三方分发，确立 FLUX 作为"开放权重（dev/schnell）+ API 旗舰（pro）"双轨商业模式的范本。

**对后续的影响**：FLUX1.1 [pro] 成为 FLUX 家族后续工作（[[flux-1-tools]]、FLUX.1 Kontext、FLUX.2）反复对标的 t2i 基线；其骨干（16-ch VAE + double/single-stream MMDiT + 3D RoPE + flow matching + LADD）被后续可控编辑与统一生成沿用，是 2024 下半年开放生态最具影响力的 DiT 文生图骨干之一。

**已知局限**：
- 闭源、不放权重，仅 API；可复现性与研究价值受限。
- 无技术报告，数据/算力/具体训练与蒸馏配方全程黑盒，本页多处只能标"未披露"。
- 与 GPT-Image-1、Recraft 等相比为"均衡型"，单一维度（如纯审美或纯 prompt 遵循）未必每项最优（侧证见 Kontext 报告对家族的横向描述）。

## 原始链接

- blog（FLUX1.1 [pro] 发布，2024-10-02）: https://bfl.ai/blog/24-10-02-flux
- blog（Ultra & Raw 模式，2024-11-06）: https://bfl.ai/blog/24-11-06-ultra
- blog（BFL 成立 + FLUX.1 发布，含骨干描述，2024-08-01）: https://bfl.ai/blog/24-08-01-bfl
- github（FLUX 开源推理代码 / 家族骨干参考实现）: https://github.com/black-forest-labs/flux
- model-card（FLUX.1 [dev]，12B rectified flow transformer）: https://huggingface.co/black-forest-labs/FLUX.1-dev
- tech-report（FLUX.1 Kontext，同骨干架构/训练细节，arXiv:2506.15742）: https://arxiv.org/abs/2506.15742
- benchmark（Artificial Analysis 文生图 Arena）: https://artificialanalysis.ai/text-to-image
- api docs: https://docs.bfl.ai/

## 一手源存档（sources/）

- [blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/flux-1-1-pro--blog.md) （FLUX1.1 [pro] 发布博客，Chrome MCP 抓取）
- [flux-1-1-pro-ultra-raw--blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/flux-1-1-pro-ultra-raw--blog.md) （Ultra & Raw 模式博客，Chrome MCP 抓取）
- [flux-1--bfl-launch-blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/flux-1--bfl-launch-blog.md) （FLUX.1 发布博客，含骨干描述，已存）
- [flux-1--gh-modelcard-dev.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/flux-1--gh-modelcard-dev.md) （FLUX.1 [dev] model card，已存）
- [flux-1--github-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/flux-1--github-readme.md) （FLUX 仓库 README，已存）
- [arxiv-2506.15742.pdf](https://arxiv.org/pdf/2506.15742) （FLUX.1 Kontext 技术报告 PDF，同骨干架构/训练，已存）
