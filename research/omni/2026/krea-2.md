---
title: "Krea 2"
org: Krea
country: US
date: "2026-06"
type: tech-report
category: t2i
tags: [t2i, diffusion-transformer, flow-matching, dit, style-reference, moodboard, open-weights, distillation, rl, dpo, krea]
url: "https://www.krea.ai/blog/krea-2-technical-report"
arxiv: ""
pdf_url: ""
github_url: "https://github.com/krea-ai/krea-2"
hf_url: "https://huggingface.co/krea/Krea-2-Raw"
modelscope_url: ""
project_url: "https://www.krea.ai/krea-2"
downloaded: [krea-2--technical-report.md, krea-2--hf-raw-card.md, krea-2--hf-turbo-card.md, krea-2--github-readme.md, krea-2--open-source.md, krea-2--project-page.md, krea-2--blog.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Krea 2 是创意工具公司 Krea 从零自研的首个图像基础模型系列：一个 12B 稠密 [[dit-scalable-diffusion-transformers]] 扩散 Transformer + Qwen3-VL 文本编码器 + Qwen Image/FLUX 2 VAE，用 rectified-flow 训练，覆盖"预训练→midtraining→SFT→偏好优化(STPO)→多奖励 GRPO RL→步数蒸馏(TDM)"完整后训练栈，主打**美学多样性与创作可控性**（风格参考 + moodboard + prompt 扩写）。开源 RAW(52 步 1K)与 Turbo(8 步、1K–2K、CFG=0)双权重，在 Artificial Analysis 文生图榜上是**独立实验室中排名第一的开源模型**、整体进前十。

## 背景与定位
2026 年的文生图领域已在高分辨率、锐利写实、稠密文字渲染、世界知识、精确 prompt-following 上趋于成熟，但 Krea 团队指出一个副作用：为追求这些可靠能力，主流系统"收敛到一组狭窄的默认美学"，作为生产工具有效，作为**创意探索引擎**却乏力——创作者往往需要在风格、情绪、构图、视觉方向间搜索，而非接受单一打磨过的默认输出。Krea 2 的核心命题就是把图像生成当作"探索性媒介"：足够表达以覆盖多种美学、足够可控以让创作者在其中导航。

Krea 此前的实践是与 [[black-forest-labs]] 合作的 FLUX.1 Krea [dev]（基于 FLUX 蒸馏/微调）；Krea 2 则是其**首个完全从零训练**的基础模型（含自建大规模数据基础设施与分布式训练框架）。技术脉络上承 [[ddpm]] / [[latent-diffusion-ldm]] / [[dit-scalable-diffusion-transformers]] / rectified flow（[[stable-diffusion-3]] 的 [[mmdit]] 路线），并大量借鉴 LLM 架构与训练范式（GQA、SwiGLU、RMSNorm、Muon、midtraining、DPO/GRPO、model merging）。技术报告把 FLUX.2、[[qwen-image]]、Z-Image、Seedream 2/3/4、HunyuanImage 2.1/3.0、LongCat-Image、GPT Image 1.5、Nano Banana Pro 等同期工作列为相关工作/参考脉络（引用计 84 篇），但**未在报告正文做逐项头对头数值对比**——唯一对外定位口径是 Artificial Analysis 榜排名。

时间线：2026-05-12 产品端首发（krea.ai 平台内 K2 工具）；2026-06-22 开源 RAW/Turbo 权重；2026-06-23 发布 58 分钟长技术报告。本页以技术报告 + 开源材料为主。

## 模型架构
**Backbone：12B 稠密单流 DiT/MMDiT**（非 MoE）。架构通过系统消融从一个单流 MMDiT 基线逐项改进，原则按 Stability / Performance / Efficiency / Simplicity 四类划分，且刻意向 LLM 生态靠拢以复用现成 kernel。最终选型（消融表）：

- **注意力**：GQA + sigmoid-gated attention（门控带来更稳的 loss / grad-norm 曲线，几乎不增算力）。曾试 MLA（略优于 GQA 但有额外开销，未采用；扩散是纯 prefill、推理无 KV cache，故 MLA 用上下投影压缩 KV、不解耦 RoPE）。
- **MLP**：SwiGLU（4× 扩展），替换 GeLU MLP，一致提升。
- **归一化**：zero-centered RMSNorm + QKNorm（对其可学习参数加 weight decay）；放弃 Derf（有质量退化）。
- **残差**：标准残差（试过 Laurel 低秩瓶颈分支无明显收益）。
- **位置编码**：3D 轴向 RoPE（frame/height/width 三组维度，文本 token 的 RoPE index 置 0）；Golden Gate RoPE / MRoPE / normalized / partial RoPE 在低分辨率无明显增益，partial RoPE 虽利于 256→512 零样本泛化、无重复伪影，但高分辨率持续训练后反而劣于基线 RoPE。
- **时间步条件（关键效率项）**：用**每块一个可调 bias** 替代常规 per-block MLP（后者占总参 20–30%），把省下的参数分配给注意力/MLP。还试过完全去掉时间步条件（劣于 AdaLN）和 in-context 时间步 token（256px 下 4–16 个 token 即可替代 AdaLN，但 512/1024px 表现差）。
- **流设计**：对比 single-stream / dual-stream / hybrid-stream，差异不大，hybrid 略好，但为简洁最终用 **single-stream**（文/图 token 共享注意力与 MLP 权重）。

**Text encoder：Qwen3-VL**（一个 VLM）。基线 T5-XXL 仍很有竞争力（对比 T5Gemma/umT5/Qwen2.5-VL/Qwen3-VL），但最终选 Qwen3-VL，因 VLM 提供更丰富输入空间（文+图）与更强多语种泛化。受 Unifusion 启发，不取最后一层特征，而用一个**浅层注意力跨层聚合 VLM 隐藏特征**（multilayer feature aggregation，让模型动态选择 coarse-to-fine 文本表征，规避自回归 LLM 末层"为 next-token 优化"而非为图像生成优化的问题）；并在 token 轴加轻量**双向 Transformer 层**以削弱表征的自回归偏置。

**Autoencoder/VAE**：从 FLUX.1-dev AE 基线出发，对比 Qwen Image VAE、DC-AE、FLUX 2 VAE 与内部 VAE。DC-AE 虽提供 32× 空间压缩（利于训练/推理效率），但其重建误差对扩散模型解析细节构成硬上限，弃用。**早期用 Qwen Image VAE，后期大模型改用 FLUX 2 VAE**（二者收敛更快、重建质量优）。开源页明确列：开源版用 **Qwen Image VAE + 12B 稠密 DiT + Qwen3-VL（带多层特征聚合）**。也试过用 DINOv3 语义对齐 + 轻量扩散损失（类 REPA-E）自训内部 VAE，验证可与 Qwen Image VAE 竞争，但因时间约束未采用。

**收敛加速组件**：iREPA（仅用于 256px 第一个 epoch 后移除，鼓励 MMDiT 学自有表征并显著加速早期收敛）、改进 VAE、Qwen3-VL。

**分辨率策略**：RAW 训练到 1K；Turbo 经蒸馏后可生成 1K–2K（推荐 mu=1.15）。

## 数据
**数据策展原则（反主流的关键立场）**：好的数据混合**不等于**只堆"高质量"图。多样性与广域覆盖对"表达力强、风格多样"的目标至关重要。团队明确**批评常规的 aesthetic-score / IQA 模型过滤**会引入隐性偏置（如把运动模糊/柔焦误判为低质，而它们可能是刻意的艺术选择）；且只要 caption 准确描述图像，即使"不理想"的图也有用——模型精确理解了不良行为后，可在后续把生成**引导远离**该分布。

**预训练只过滤掉**这 5 类：①重复样本与过度表征的概念；②VLM 反复无法捕捉关键信息的样本；③诱发偏置/伪影的样本；④低分辨率下难以可靠建模的高视觉复杂度样本；⑤**AI 生成样本**。特别强调**预训练混合中不用任何 AI 生成图**——哪怕少量合成图也会引入偏置（合成图更易学，等于给模型质量设了上限），为此专门训了内部分类器把合成图滤掉。

**Captioning（多阶段）**：先对每图跑 OCR 提取可见文字；再把 OCR 结果 + 可用元数据（相机参数、已知实体等）喂给 captioning 模型生成融合世界知识的富 caption；最后用更便宜的 LLM 把长 caption **改写成多种长度/格式**暴露多样 prompt 风格。经验：长 prompt 提供稠密监督、收敛更快、loss 更低，但短/中长 prompt 的下游表现也重要，故**以长 caption 为主、全程保留短/中长 prompt 曝光**。

**预训练数据**：横跨 256/512/1024px 三个分辨率阶段，构成**课程学习**——把大部分 FLOPs 投在低分辨率阶段建核心能力，再随分辨率上升赋予高保真生成能力。低分辨率阶段数据量达**数十亿图**级别，主用廉价 CPU 过滤（坏文件/分辨率/宽高比/Laplacian 去极端纹理噪声）。为缓解模型生成纯色背景+边框伪影的倾向，用 RGB 熵、黑白像素比、自定义启发式 + 内部分类器过滤。**内部分类器构造法**：大 VLM 写任务专用 system prompt → 产伪标注数据 → 训一个 <1B 的 DINOv3 或 SigLIP-2 小分类器规模化运行（低分辨率阶段任何需 GPU 的过滤模型都控制在 1B 参数内）。**去重**：低分辨率阶段用便宜的 hash（md5 + phash + colorhash 组合；默认 8×8 phash 不顾颜色、误报高，改用 12×12 phash + colorhash）。随分辨率上升才引入质量/美学过滤，且**仅用于丢弃极差图、不据分数过采样**；并用图像复杂度分 + 文字密度（OCR）排除低分辨率下无法有意义表征的图，阈值随训练推进调整。还在 SigLIP-2 embedding 上训了一个**稀疏自编码器(SAE)**，用 VLM 按 top-k 激活样本标注每个 SAE 特征，形成无监督打标系统，用于无须显式分类器即可过滤视觉伪影。

**Midtraining 数据（自顶向下策展）**：与预训练自底向上不同，midtraining 先选好领域/来源（已知有良好风格覆盖与高质量的图源），平滑桥接"通用预训练分布"与"高质量 SFT 分布"。用 FAISS 做**层次化 k-means 聚类**（借鉴 DINOv2 的 Automatic Data Curation），采样以保留长尾视觉概念、不在头部概念上浪费算力；VLM 检视各簇质心近邻图来命名/标记簇，人审后丢弃低质或问题簇；簇内再用 SigLIP 相似度做语义去重。**实体覆盖（PageRank 巧思）**：为保证按名引用的已知实体（运动员/演员等，易被层次采样误丢）被覆盖，用 Danker 在英文维基跑 PageRank 取 top 90% 文章，按 Wikidata 元数据滤掉不可表征主体，对剩约 **500 万概念**在全数据集 caption 上做全文检索评估覆盖度，采样时优先含稀有概念的图，最后复核确认无概念被整体丢失。

**SFT 数据**：小而精的手工策展集，聚焦单个视觉域；团队发现量到一定程度后**质量远比规模重要**。

**HF 模型卡口径**（合规向）：训练数据为公开数据 + 第三方授权数据 + 自有合成数据（注意：此处"合成数据"主要指后训练/偏好阶段，预训练混合明确无 AI 图），训练前过滤掉若干类有害内容并削减低质/重复/无关数据。

## 训练方法
多阶段流水线，明确**仿照现代 LLM 训练栈**：

1. **预训练**：标准 **rectified-flow 损失 + v-参数化**；分辨率 256→512→1024px 递进。256px 首个 epoch 用 iREPA 加速后移除。采用**移位 logit-normal 采样（timeshift）**，随分辨率增大逐步增 shift；按 FLUX 2 VAE 博客的方法对每个分辨率**只 sweep 训练 timeshift**、推理 shift 保持恒定。学习率用 **warmup-stable-decay**；用 **PMA（预训练 model merging）替代 EMA**（性能相当但避开 EMA 的显存开销）。
2. **Midtraining**：在 SFT 前 warmup 模型分布，是**最后一个能给模型装入下游能力（高保真/高分辨率/强域覆盖/文字渲染）的节点**。
3. **SFT**：在小而高美学的专门集上把模型偏向理想美学方向，尤其修复早期 checkpoint 的高饱和与纹理问题。训完多个域专用 SFT checkpoint 后用 **model merging** 合成通才 checkpoint（后期 merging 收益递减，因改进方向开始冲突）。
4. **偏好优化(PO)**：两阶段。第一阶段大规模**合成偏好对**（类 delta learning，保证多数 pair 至少含一个 on-policy 样本）；第二阶段仅用**内部人工标注**校准。针对 DPO 常见的 **policy divergence**（模型靠同时降低胜/负样本似然、但速率不同来拉大 margin，会漂离预训练分布、后期出高频伪影），团队设计了 **STPO**——给原始 DPO 加辅助损失 + 公式修改以抑制该发散。
5. **强化学习(RL)**：流水线最后阶段，用**多奖励 GRPO 风格**方法，4 个奖励模型：①通用美学（在 PO 阶段人工偏好数据上微调开源 VLM 得到）；②prompt-following；③文字渲染；④**伪影/结构奖励**。prompt-following 与文字渲染用**prompt 专属 rubric 奖励**（把每条 prompt 拆成可验证要求逐项打分，而非要求 judge 给单一整体分）。专门训了**伪影奖励模型**检测多指/畸形肢体/扭曲文字等结构错误（这些人眼易见但通用 VLM judge 常漏），防止 RL 为刷 benchmark 信号牺牲视觉正确性（反 reward hacking）。**prompt 选择被当作资源分配问题**：持续分析各组奖励统计，剔除"太易/太难/方差太小"的无信息 prompt，把算力花在仍可学的样本上。**CFG 处理**：经消融，整个 RL 阶段**不用 CFG**训练（保持 rollout 与训练分布一致、省算力），让 no-CFG 样本早期就逼近 guided 样本；推理时 CFG 仍可作为额外控制旋钮开启。
6. **步数蒸馏（可选，产出 Turbo）**：RL 后同时做 guidance 蒸馏 + 步数蒸馏。比较了 DMD/DMD2/Decoupled DMD/piFlow/APT，最终选 **TDM（Trajectory Distribution Matching）**——理由是简单、超参少、data-free 且支持灵活多步蒸馏（排除 GAN 类与需改成多时间步预测模型的 piFlow）。TDM 是把 DMD 推广到**跨时间步在轨迹层面做分布匹配**，而非仅匹配 clean-image 分布。产物 Turbo 为 **8 步、CFG=0** 的蒸馏 checkpoint。

**两个面向用户可控性的辅助系统**（base model 之上）：
- **Prompt Expander**：把用户短/欠定 prompt 映射成接近训练分布的富 caption（distribution-mapping）。先在开源 LLM 上 SFT（用另一 LLM 从长 caption 反向合成"用户口吻短 prompt"得到配对数据，并合成 thinking trace 保留推理）；再用 **GDPO 多奖励 RL** 直接优化"扩写后生成图"的质量与对原意的忠实度（含安全/约束门控）。显式对抗 **diversity collapse**：加 **DINOv3 embedding 组内多样性奖励**并全程保持（一旦权重过小模型迅速塌缩为单一安全 house style）。RL prompt 混合真实用户流量 + 内部下投票/bug 报告/手写失败案例的 hard cases，选"难但非无望"的样本。
- **风格参考系统**：支持多风格平滑语义混合、每个参考的连续强度控制、对复杂风格的 SOTA 贴合。最大失败模式是 style 图的**内容/主体泄漏**到输出，且风格迁移数据难大规模获取。解法：一个**新颖的自监督训练技术** + 后续 PO 对齐（具体机制未在报告展开）。

**优化器**：主用 AdamW。Muon 探索（用 Dion 实现 + Moonlight 的 RMS-matched 设置迁移 AdamW 超参）：初期收敛快但长程劣于 AdamW、且有 loss/grad spike；**排除 MMDiT 首尾线性层**（对应 LLM 中排除 embedding/LM-head）并加 Nesterov 动量后，Muon 在高低分辨率均超过 AdamW 基线——但因时间约束本轮最终预训练未用 Muon，计划下轮采用。

**8-bit 训练**：256/512px 阶段用 8-bit 训练，较 bf16 基线提速 **15–20%**，loss/评测退化极小（256px 用 tensorwise scaling，512px 用更细的 rowwise scaling）；1024px 起及整个 RL 阶段回到标准 bf16。

## Infra（训练 / 推理工程）
**分布式训练框架从零基于 PyTorch 自建**，重度依赖 `DTensor` 抽象与 torchtitan 的 torch-native 特性。绝大多数预训练/后训练用 **FSDP2 + Megatron-LM 式张量并行(TP)**；TP size >2 时通过 `torch.compile` flag 启用 **async-TP**（中等加速）。VAE 参数显存开销小故全设备复制，仅对 text encoder 与主 MMDiT backbone 分片。**节点内 NVLinkSharp，节点间 InfiniBand**。刻意用"更宽（更大 hidden）而更浅（更少层）"的模型：宽 hidden 提升每层计算密度、便于 FSDP2 prefetch 隐藏延迟，减少层数即减少 all-gather/reduce-scatter 次数（显著降低 NCCL 错误）；大矩阵乘还摊薄 8-bit 量化/反量化开销。重度用 `torch.compile`；注意力默认最新 cuDNN kernel，按需用 FlexAttention / FlashAttention 3。低分辨率用选择性激活重计算，高分辨率（激活主导显存）用全激活重计算。

**数据加载**：主格式 Parquet（每行存图引用如 S3 路径、crop/resize 尺寸、captions、元数据）。大型 run **预先 shuffle + pack**，让每个 dataloader worker 加载同宽高比的一批图，可单次 AE pass 编码 latent；预 shuffle 还保证可复现/可调试（精确重放定位致 loss spike 的样本）。为均衡负载，**预先把所有图 crop/resize 到目标训练分辨率**（避免低分辨率阶段实时缩放高分辨率图造成 CPU/IO 不均），并 pad 到完全相同张量形状。

**RL Infra**：把 reward-model 推理与主训练进程**解耦**；因是首次大型 RL 迭代，采简单设计（训练与 rollout GPU 共享），未来计划做训推分离以支持 PipelineRL/异步 RL。

**系统层（Kubernetes）**：研究跑在单一 K8s 集群、GPU 与生产推理共享——设计成研究可在需要时**独占整个 GPU 池**，若全部 GPU 被训练占用，生产推理自动迁移到集群外（基于自研 Virtual Kubelet 层，把 pod 规格转成目标 provider 形式、并继承 K8s 的扩缩/故障恢复语义）。调度用 **Kueue**（两级优先级 + gang-scheduling + borrowing/lending/reclamation）。启动流程：CLI 自动排除故障节点、给训练节点打 label + taint + drain；故障节点清单从文本文件迁到 node label，配 "Packerman" operator 把 dev 机打包到故障节点上、留健康节点给训练。

**可观测性（大规模预训练最大收获）**：通过 DCGM + 自定义 DaemonSet 采 GPU/PCIe/NVLink/InfiniBand 指标。关键发现：GPU 温度 >75–78°C 即增不稳定与节流；`DCGM_FI_DEV_GPU_UTIL` 常误导（只报"有 kernel 在跑的时间占比"）；**张量核活跃度 `DCGM_FI_PROF_PIPE_TENSOR_ACTIVE` 是最佳健康指标**（高分辨率→更高张量核利用，持续下降通常预示故障节点）；PCIe replay 突增、行重映射、XID、自采的 NVLink/InfiniBand 错误用于定位故障节点。**InfiniBand 指标最重要**——fabric 不稳是 run 崩溃的单一最大来源（link flapping、丢包、拥塞、symbol error）。

**规模化经验（坦诚披露）**：失败率随规模增长**超出常规预期**——同代码同数据，<128 GPU 的 run 很稳（常连跑数天），但放大 GPU 数后崩溃骤增，**在很大规模下没有一次 run 能连跑超过 24 小时不崩**，且许多崩溃无明显原因（如指标全健康却 NCCL timeout）。应对策略是优化 MTBF/MTTR（快而频繁的 checkpoint + 改善启动时间）而非追求复杂容错（torchft/DiLoCo 在其规模下非必需）。**文件系统**：早期用 Ceph 是重大错误（规模/用例不匹配），换 **Weka** 后文件系统问题与停机骤降、性能提升；激进 checkpoint 下一次 checkpoint 约 **30 秒**完成。

**数据基础设施（krablet）**：围绕 PostgreSQL 集群自建数据仓库/队列系统，每个分片叫 "krablet"（Postgres 实例 + 异步批处理 funnel 服务），读经大规模 "RPC" 服务代理（替代 PgBouncer）。用 `FOR UPDATE SKIP LOCKED` 把数据处理 DAG 当队列跑，支持自动重试/容错/动态 worker 数/部分处理/即时可见性。**已扩到 208 TB 元数据**、每秒处理数万争用 UPSERT。上层暴露 "pluck" 提供 notebook 友好的 global-map API（UDF 用 cloudpickle 序列化远程执行）。

**算力规模**：未披露具体 GPU 数量 / GPU-小时 / 总 FLOPs（仅以"<128 GPU 稳、放大后不稳"侧面给出量级线索，且明言模型"目前是欠训练的")。

## 评测 benchmark（把效果讲清楚）
一手源给出的是**第三方公开榜单的相对排名**，未提供 FID/CLIPScore/GenEval/DPG-Bench 等具体数值（这是闭源产品+开源混合发布的常见口径）：

- **Artificial Analysis 文生图榜**：Krea 2 进**前十**，且在**独立实验室（independent labs）出品的模型中排名第二**（技术报告原话）；GitHub README 进一步称 Krea 2 是 **Artificial Analysis 上独立实验室出品的文生图第一名(#1)**，并自称"最具美学的开源图像模型"。（两处口径："进前十/独立第二"来自技术报告正文，"独立第一"来自开源 README，可能对应不同时点/不同切片，均为 AA 榜口径。）
- **具体数值指标（FID、GenEval、T2I-CompBench、DPG-Bench、MJHQ-30K、HPSv2、ImageReward、PickScore、人评 ELO 等）**：在所有已抓取一手源中**均未报告**。
- **推理配置（间接性能口径）**：RAW 推荐 52 步 / CFG 3.5 / 1K；Turbo 8 步 / CFG 0 / mu 1.15 / 1K–2K。产品页宣称 K2 在 **≤15 秒**内出图（"远快于其他顶级模型"），但未给标准化吞吐对比数。

**关键消融结论（来自报告，定性为主）**：SwiGLU 一致提升并全程采用；GQA 退化极小但提效；gated sigmoid 不显著提质但显著稳训练；single-stream 与 hybrid 差异小（选简洁的 single-stream）；per-block bias 替代 modulation MLP 省 20–30% 参数而不掉点；8-bit 训练 256/512px 提速 15–20%；iREPA 显著加速早期收敛；DC-AE 因重建误差对细节设硬上限被弃；Muon 排除首尾层 + Nesterov 后超 AdamW（但本轮未用）；prompt expander 必须保持 DINOv3 多样性奖励否则塌缩。

## 创新点与影响
**核心贡献**：
1. **把 LLM 训练范式系统移植到大规模文生图 DiT**：midtraining 阶段、warmup-stable-decay + PMA（替代 EMA）、model merging、Muon 调参、8-bit 低精度训练、GQA/SwiGLU/RMSNorm/QKNorm 等架构组件的逐项消融与采用。
2. **"美学优先而非质量分优先"的数据哲学**：反对用 aesthetic/IQA score 过采样、坚持**预训练零 AI 生成图**、SAE 无监督打标、Wikipedia PageRank 保实体覆盖——一套以"多样性/可控性"为目标函数的数据策展方法论。
3. **效率架构创新**：用 per-block 可调 bias 替代占 20–30% 参数的 modulation MLP；Qwen3-VL 的多层特征聚合 + 双向层削弱自回归偏置。
4. **后训练栈**：STPO（抑制 DPO policy divergence）、多奖励 GRPO + prompt-rubric 奖励 + 专用伪影奖励 + no-CFG RL、TDM 步数蒸馏。
5. **可控创作系统**：prompt expander（含 diversity 反塌缩）与自监督风格参考系统（低内容泄漏 + 连续强度 + 多风格混合）+ moodboard 工作流。
6. **工程透明度**：极其坦诚地披露大规模训练的不稳定性（放大后 24h 内必崩、InfiniBand fabric 是头号杀手、Ceph→Weka 教训）、自建 krablet 数据系统（208TB / FOR UPDATE SKIP LOCKED 队列）与 K8s 研究-生产 GPU 弹性共享方案——对中小团队从零搭 t2i 训练栈有很高参考价值。
7. **开源**：RAW（可微调基座，训 LoRA 用）+ Turbo（8 步快速推理，跑 LoRA 用）双权重，Krea 2 Community License（permissive，商用需联系），已接入 diffusers(`Krea2Pipeline`)、SGLang、ComfyUI、Fal、Replicate、Cloudflare、Together 等生态。"在 RAW 上训 LoRA、在 Turbo 上跑"是其核心使用范式。

**已知局限 / 团队自陈**：①模型**目前欠训练**，更长训练会受益；②本轮保守选型（无 MoE、未用 Muon、未原生 2K/4K、未用稀疏注意力）；③风格参考的自监督技术与风格迁移数据稀缺仍是难点；④下一轮计划：把现代 LLM Transformer 设计（含 MoE）引入 DiT、用稀疏注意力做原生 2K–4K、NVFP4 预训练、Muon 扩展、多教师 on-policy 蒸馏(MOPD)、把 AE/DiT/text-encoder/prompt-expander/style/upscaler **多组件统一进单一模型**、原生编辑/图像参考能力、原生理解 tags/JSON/bbox/Markdown 等多样 prompt 形式。⑤评测仅给第三方榜单相对排名，缺标准化定量指标，难做严格横向对比。

## 原始链接
- tech-report: https://www.krea.ai/blog/krea-2-technical-report （Krea 2 Technical Report，58 min，2026-06-23）
- blog (release note): https://www.krea.ai/index/krea-2-is-here （Releasing Krea 2，2026-05-12）
- project_page: https://www.krea.ai/krea-2
- open-source page: https://www.krea.ai/krea-2-open-source
- github: https://github.com/krea-ai/krea-2
- hf (RAW): https://huggingface.co/krea/Krea-2-Raw
- hf (Turbo): https://huggingface.co/krea/Krea-2-Turbo
- 外部榜单: https://artificialanalysis.ai/image/leaderboard/text-to-image （技术报告/README 引用，未单独抓取）

## 一手源存档（sources/）
- [technical-report.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2026/krea-2--technical-report.md)
- [hf-raw-card.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2026/krea-2--hf-raw-card.md)
- [hf-turbo-card.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2026/krea-2--hf-turbo-card.md)
- [github-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2026/krea-2--github-readme.md)
- [open-source.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2026/krea-2--open-source.md)
- [project-page.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2026/krea-2--project-page.md)
- [blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2026/krea-2--blog.md)
