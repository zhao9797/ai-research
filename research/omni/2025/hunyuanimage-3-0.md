---
title: "HunyuanImage 3.0 Technical Report"
org: "腾讯混元（Tencent Hunyuan Foundation Model Team）"
country: China
date: "2025-09"
type: tech-report
category: unified
tags: [t2i, unified-multimodal, autoregressive, moe, diffusion, transfusion, chain-of-thought, open-source, rlhf]
url: "https://arxiv.org/abs/2509.23951"
arxiv: "https://arxiv.org/abs/2509.23951"
pdf_url: "https://arxiv.org/pdf/2509.23951"
github_url: "https://github.com/Tencent-Hunyuan/HunyuanImage-3.0"
hf_url: "https://huggingface.co/tencent/HunyuanImage-3.0"
modelscope_url: ""
project_url: "https://hunyuan.tencent.com/image"
downloaded: [arxiv-2509.23951.pdf, hunyuanimage-3-0--github-readme.md, hunyuanimage-3-0--hf-modelcard.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
HunyuanImage 3.0 是腾讯混元基于自研 80B 总参 / 13B 激活 MoE 大语言模型 [[hunyuan-a13b]] 扩展而成的「原生多模态」统一理解+生成模型——文本走自回归 next-token、图像走扩散预测（[[transfusion]] / [[janusflow]] 路线），把 native Chain-of-Thought「先想后画」内置进生成流程；它是迄今**最大的开源图像生成模型**，人评 GSB 上相对 HunyuanImage 2.1 胜率 +14.1%，相对闭源 Seedream 4.0 / Nano Banana / GPT-Image 也分别取得 +1.17% / +2.64% / +5.00% 的正向胜率。

## 背景与定位
2024–2025 年顶尖图像生成系统（Seedream 4.0、Nano Banana、GPT-Image、Qwen-Image、HunyuanImage 2.1）大多走两条路：DiT 扩散主干（[[latent-diffusion-ldm]] → [[dit]] → [[mmdit-sd3]]）或闭源 native 多模态。它们的共同问题是**多数闭源、不可复现**，且理解管线与生成管线常常割裂。HunyuanImage 3.0 的定位是：

- **用一个 LLM 主干统一理解与生成**：摒弃主流 DiT 架构，直接在预训练 MoE LLM 上扩出视觉理解 + 视觉生成两条通路，使「交错文本对话 / 图像生成 / 图像理解 / 图像编辑」能在同一连续上下文里完成，无需在两套 pipeline 间切换。
- **把 LLM 的世界知识与推理能力带进 T2I**：借 native CoT，让模型在生成前先做一段「思考/改写」，把稀疏提示自动扩写为细节充分的视觉规格，从而提升复杂指令遵循、文字渲染与概念泛化。
- **开源最大规模生成模型**：以「开源即可达到甚至超过闭源」为目标对标商业系统。

它是 [[hunyuanimage-2-1]] 的后继，但架构范式完全不同（2.1 是 DiT，3.0 是 AR+扩散的统一 LLM）。

## 模型架构
整体采用**离散-连续混合建模**：文本 token 用自回归 next-token 预测，图像 token 用扩散预测（flow matching 系，引用 Lipman flow matching）。

- **Backbone**：构建于 Hunyuan-A13B——decoder-only LLM，**80B+ 总参**，MoE 配置 **64 个专家、每 token 激活 8 个专家**，外加 1 个共享 MLP，约 **13B 激活参数 / token**。
- **Text Tokenizer**：沿用 Hunyuan Tokenizer，扩词表加入图像生成/理解的自定义 special token。
- **Image Encoder（生成通路）**：自研 VAE，把像素投到 **32 维 latent**、**下采样因子 16**。论文明确指出，相比 DiT 系常用「8× 下采样 VAE + 额外 patchify 再降 2×」的组合，**单个 16× 下采样 VAE 更简洁也更有效**，生成质量更好。
- **双编码器条件注入**：对「作为条件输入」的图像，采用 dual-encoder——把 VAE latent 与 vision encoder（ViT）特征**拼接**，得到既能生成又能理解的统一表征。这与既往统一模型（按任务分离视觉特征：理解用 ViT、生成用 VAE）不同，是关键区别点。
- **Projector**：两个对齐模块——VAE 特征用 **timestep 调制的残差块**投影；ViT 特征用**两层 MLP**投影；并把 timestep embedding 注入序列以增强扩散条件。
- **Generalized Causal Attention（核心设计）**：融合因果与全注意力——文本 token 只能看前文多模态 token；图像 token 可看「所有前文 token + 同一图像段内的后续图像 token」。训练时按序列中 Gen Image 数量分两类 mask：0 或 1 个 Gen Image 时走标准 generalized causal；多个 Gen Image 时要在下三角挖「洞」（已生成的上文 Gen Image 不被后续 token attend）。推理时同一序列永不超过 1 个 Gen Image（生成完即转为 Cond Image），故 mask 始终是规范形态。
- **Generalized 2D RoPE（向后兼容）**：图像 token 由 1D reshape 成 2D，赋予各向异性的 2D 位置编码 `[cos(xθ0),cos(yθ1),…]`；文本 token 保留 1D RoPE（等价于 2D 的对角线位置）。设计保证无图像 token 时退化为纯 1D RoPE，**最大限度不破坏预训练语言能力**。
- **Automatic Resolution**：扩词表加两组 special token——`<img_size_*>`（256/512/768… 分辨率锚）与 `<img_ratio_0..32>`（覆盖 1:4 到 4:1 的宽高比）。模型据上下文（提示词/条件图）自动预测尺寸与比例 token，也支持用户显式提示（如"3:4"/"vertical"），再据此给图像 token 套 2D RoPE。

## 数据
- **过滤（三阶段）**：从 **100 亿+ 原始图**起，最终保留 **<45%**。
  - 阶段一：技术性剔除——分辨率 <512、坏文件、过曝/欠曝、过饱和；按 MD5 去重。
  - 阶段二（主清洗）：客观过滤器（水印/logo/大量文字 via 自研 hy-OCR / 拼图 / 明显边框 / AIGC 检测）+ 主观打分（清晰度模型 + 自建美学模型，美学由艺术家定义「色彩 / 光影 / 构图」三要素标准）。对 AIGC 用检测模型并整体剔除「高 AIGC 占比」数据源。统一阈值 + 分类目阈值。
  - 阶段三：基于 embedding 聚类再去重（约去 0.5%），并补充 knowledge-augmented / text-related / stylized / graphic-design 专项集。
  - **最终训练集 ≈ 50 亿张图**。
- **配对/多图数据**：另构 **1 亿+ 图像对与多图样本**用于学交错关系。两条来源：①图像聚类（分析 20 亿+ 聚类，抽相似对，过 image-relation 判别器只留有显著编辑关系者，再用图像复杂度模型剔过复杂样本）；②视频片段挖掘（shot 边界检测 → 相机运动分类剔大幅运镜 → 目标检测+语义分割定位规范变换关键帧 → 运动模糊检测过滤）。
- **Captioning**：①双语（中/英）分层 schema——四档描述长度（short→extra-long）、风格属性（艺术风格/镜头/光照/氛围/构图）、事实实体（IP：角色/地标/品牌/艺术品）；②Compositional Caption Synthesis 动态增广——训练时采样组合字段，生成 **30 词到 1000 词**变长变模式的双语 caption；③事实接地——OCR Agent + Named-Entity(IP) Agent 外挂知识，并用**双向校验环（Bidirectional Verification Loop）**交叉核对，只留通过校验的样本；④Image Difference Captioner——对配对图（含两图 caption 与双帧视频）生成前后景变化描述，模拟用户编辑指令。
- **推理数据集**：T2T（文本逻辑推理）、T2TI（文本→推理 trace→图像，含 Wikipedia 信息图）、TI2TI（图像编辑：源图+复杂指令+编辑 trace 分解为原子操作+目标图），用于解锁 CoT 生成/编辑。

## 训练方法
- **预训练（四阶段渐进）**——VAE 分辨率由粗到细递增、ViT 固定 512px、保宽高比支持多分辨率（见下表）：

  | 阶段 | VAE 分辨率锚 | ViT 分辨率锚 | 训练部件 | 任务 |
  |---|---|---|---|---|
  | I | 256px | 512px | Transformer | T2I, LM, MMU |
  | II | 256px | 512px | ViT | MMU |
  | III | 512px | 512px | ViT + Transformer | T2I, LM, MMU, INTL |
  | IV | 1024px | 512px | ViT + Transformer | T2I, LM, MMU, INTL, CoT |

  阶段 I 冻 ViT、低分辨率（256px）+ 大 batch 学数十亿图对齐图文表征；阶段 II 冻 Transformer、只用 MMU 微调 ViT 及 aligner；阶段 III 联合训 ViT+Transformer，提分辨率、降数据量提质，引入交错（编辑/I2I）数据；阶段 IV 进一步收缩到短边 ≥1024 高分辨率子集，引入推理数据使能 CoT-T2I（推理段也走自回归 next-token 建模）。
- **Instruction Tuning**：预训完成后，用指令模板把 T2I / LM / CoT 数据联合做指令微调。
- **后训练（多阶段）**：
  - **SFT**：高质量 T2I 集（风景/人像/OCR）+ 系统配对扩成编辑集（严格过滤保空间一致与身份保持）+ 推理数据；多阶段逐步引入更高保真样本。
  - **DPO（两阶段）**：先用大规模配对数据增采样稳定性与编辑一致性；再用高质量子集精修视觉真实感——抑制结构畸变、采样不稳与合成伪影。
  - **MixGRPO**：在线 RL，把 GRPO 扩到 flow-based 模型（ODE–SDE 混合采样），配自研奖励模型优化美学（风格/构图/光照）、抑畸变与伪影；改进 advantage 估计加速收敛；I2I 多任务（编辑、ID 保持）做平衡联合训练，迭代训练多个针对不同质量维度的奖励模型，并为人脸 ID 保持专门定制奖励模型。
  - **SRPO**：梯度引导在线 RL——直接向 latent 注入噪声先验并单步去噪到 clean image，选去噪轨迹的初始区间优化（此处模型改进空间最大），用正/负文本引导的可微奖励对齐人类偏好，缓解过饱和、光色不连贯、皮肤质感差。
  - **ReDA（自研 Reward Distribution Alignment）**：最小化与高奖励先验的分布散度；用任务特定 projector 映到压缩空间做 ID 一致性/真实感的定向优化；有参考图时引入 transition-based 目标（比对参考与生成的向量差而非静态特征），显著提效；data-centric 设计，能吃数据规模/质量红利。
- **蒸馏加速**：提出新框架把 **MeanFlow** 扩到 80B 统一多模态模型蒸馏，缓解训练不稳定，并把轨迹分布对齐并入 MeanFlow 目标，**把 NFE 降到 4–8 步**仍保竞争力（对应开源的 HunyuanImage-3.0-Instruct-Distil，推荐 8 步采样）。

## Infra（训练 / 推理工程）
- **训练**：报告 abstract 与正文强调「高效 infrastructure 支撑大规模训练与推理」，但**未披露**具体 GPU 数量、卡时、并行/分布式策略（TP/EP/FSDP）、混合精度与吞吐数字。
- **推理 / 部署**：开源三档权重——HunyuanImage-3.0（T2I，base，推荐 ≥3×80GB VRAM）、HunyuanImage-3.0-Instruct（带推理/I2I，≥8×80GB）、Instruct-Distil（8 步蒸馏，≥8×80GB）。MoE 推理支持 `eager` 与 **FlashInfer**（v0.5.0，宣称最高 ~3× 加速；首次因 kernel 编译约 10 分钟）；注意力用 sdpa / flash_attention_2；提供 **vLLM 加速**（2025-10-30 上线）与可选 Taylor Cache。默认扩散推理 50 步，蒸馏版 8 步。环境：Python 3.12 / CUDA 12.8 / torch 2.8.0。

## 评测 benchmark（把效果讲清楚）
报告自带 SSAE 与 GSB 两套评测；README/HF card 中的 SSAE 与 GSB 结果均以热力图/柱状图（PNG 图片）呈现，**文本中未给逐项数字**，故下列只列报告正文给出的确切数字。

- **SSAE（自研机评，Structured Semantic Alignment Evaluation）**：针对 T2I-CompBench / GenEval 的「提示简单化、CLIP Score 与人评脱节」缺陷而提出。收集 500 条多样提示，用 LLM 抽 **3,500 个 key point**，归入 **12 个细粒度字段**（主/次主体的名词·属性·动作、主主体其他属性、场景名词与属性、镜头、风格、构图），经 LLM 一致性过滤+人工修正后固定；再用带 CoT 的先进 MLLM 对生成图按 key point 做 0–1 匹配，算 **Mean Image Accuracy** 与 **Global Accuracy**。结论：HunyuanImage 3.0 在所有细粒度字段上与领先模型**持平（on par）**（具体分值见报告 Figure 6，文本未列）。
- **GSB（人评，Good/Same/Bad）**：1,000 条覆盖均衡场景的提示，每模型单次推理生成等量样本、**不挑图**，100+ 专业评估者评判。关键相对胜率（relative win rate）：
  - vs **HunyuanImage 2.1**（此前最强开源）：**+14.10%** → 坐实「最强开源 T2I」。
  - vs **Seedream 4.0**：**+1.17%**
  - vs **Nano Banana**：**+2.64%**
  - vs **GPT-Image**：**+5.00%**
  - 结论：作为开源模型，图像生成质量达到与领先闭源商业系统**可比**水平。
- **Instruct（I2I/编辑）GSB**：README 提到用 1,000+ 单图/多图编辑 case 做 GSB（100+ 评估者），结果同样以图片呈现，文本无数字。
- **未报告**：FID、CLIPScore、GenEval、T2I-CompBench、DPG-Bench、HPSv2、ImageReward、PickScore、Arena ELO 等标准数值——报告刻意以自研 SSAE/GSB 取代，并论证 CLIP Score 等自动指标与人评脱节。
- **附加发现（专家激活分析）**：随机取 1,000 提示做 T2I，统计各层专家被图像 token/文本 token 激活的分布，发现**层越深、图文激活分布的 KL 散度越大、专家越按模态专精**——提示 MoE 可能通过把不同模态的职责分派给专用专家来增强多模态建模。

## 创新点与影响
- **核心贡献**：①把图像生成统一进预训练 MoE LLM 的**原生多模态 AR+扩散框架**（Transfusion/JanusFlow 路线的大规模工程化落地，80B 总参 / 13B 激活，是最大开源生成模型）；②**Generalized Causal Attention + Generalized 2D RoPE** 让文本因果性与图像全局性共存且向后兼容预训练 LLM；③**native CoT「先想后画」**把 LLM 世界知识/推理引入 T2I 与编辑；④**16× 单 VAE + 双编码器拼接**的简化条件方案；⑤完整后训练栈（SFT→DPO→MixGRPO→SRPO→ReDA）+ MeanFlow 蒸馏到 4–8 步；⑥新评测 SSAE。
- **影响**：作为开源最大规模、可达闭源水平的统一生成模型，为社区提供了「LLM 即生成器」范式的强基座；其 CoT 生成、双编码器统一表征、MoE 模态专精观察均对后续统一多模态工作有参考价值。后续已迭代出 Instruct（带 reasoning + I2I 编辑 + 多图融合，最多 3 输入）与 Distil（8 步）版本。
- **已知局限**：①infra 关键数字（算力/并行/吞吐）未披露——报告 abstract 仅一句「efficient infrastructure enables large-scale training and inference」，正文无任何 GPU 数/卡时/TP/EP/FSDP/吞吐，复现成本高且不透明；②报告本体（含落盘的 v2）正文与 Conclusion 仍以 T2I 为主、明言「I2I 训练进行中」，I2I/编辑/CoT-reasoning 能力是经 README 的 **Instruct checkpoint（2026-01）** 补齐的，论文未给 I2I 训练细节与 GSB 数字（编辑 GSB 仅 README 图片、无文本数值）；③评测以自研 SSAE/GSB 为主、缺标准 benchmark 横向数值（FID/GenEval/CLIPScore 等），外部可比性受限；④部署门槛高（base 需 ≥3×80GB，Instruct/Distil 需 ≥8×80GB VRAM）。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2509.23951
- arxiv_pdf: https://arxiv.org/pdf/2509.23951
- github: https://github.com/Tencent-Hunyuan/HunyuanImage-3.0
- hf (T2I base): https://huggingface.co/tencent/HunyuanImage-3.0
- hf (Instruct, I2I): https://huggingface.co/tencent/HunyuanImage-3.0-Instruct
- hf (Instruct-Distil, 8-step): https://huggingface.co/tencent/HunyuanImage-3.0-Instruct-Distil
- 官方产品页: https://hunyuan.tencent.com/image

## 本地落盘文件
- ../../../sources/omni/2025/arxiv-2509.23951.pdf —— 落盘为 **arXiv v2（标注 2026-02-02），16 页**；正文/abstract 已更新，但 Conclusion 仍保留 v1 措辞「本次仅放出 T2I，I2I 训练进行中」，与 README「2026-01-26 已发布 Instruct（含 I2I）」存在版本滞后，本页据此区分。
- ../../../sources/omni/2025/hunyuanimage-3-0--github-readme.md
- ../../../sources/omni/2025/hunyuanimage-3-0--hf-modelcard.md
