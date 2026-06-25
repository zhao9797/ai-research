---
title: "Wan 2.2"
org: "阿里巴巴 Wan 团队（Alibaba Wan Team / 通义万相）"
country: China
date: "2025-07"
type: model-card
category: video
tags: [video-generation, t2v, i2v, ti2v, moe, diffusion-transformer, flow-matching, vae, open-source, cinematic]
url: "https://github.com/Wan-Video/Wan2.2"
arxiv: "https://arxiv.org/abs/2503.20314"
pdf_url: "https://arxiv.org/pdf/2503.20314"
github_url: "https://github.com/Wan-Video/Wan2.2"
hf_url: "https://huggingface.co/Wan-AI/Wan2.2-T2V-A14B"
modelscope_url: "https://modelscope.cn/organization/Wan-AI"
project_url: "https://wan.video"
downloaded: [wan-2-2--github-readme.md, wan-2-2--hf-t2v-a14b.md, wan-2-2--hf-ti2v-5b.md, wan-2-2--hf-i2v-a14b.md, wan-2-2--blog.md, arxiv-2503.20314.pdf, arxiv-2503.20314.txt]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
Wan 2.2 是阿里 Wan（通义万相）团队 2025-07 开源的视频生成模型升级版，**首次把 Mixture-of-Experts（MoE）引入视频扩散模型**——按去噪时间步把网络拆成"高噪专家+低噪专家"两个 14B 专家（总 27B 参数，每步只激活 14B，推理成本与 14B 稠密模型持平）；同时放出一个 5B 稠密 TI2V 模型，配合 16×16×4 高压缩 Wan2.2-VAE，**可在单张 RTX 4090（24GB）上 9 分钟内生成 5 秒 720P@24fps 视频**，是当时最快的开源 720P@24fps 模型之一，官方在自建 Wan-Bench 2.0 上声称多维度超越主流闭源商业模型。

## 背景与定位
- **前置工作**：Wan 2.2 建立在 [[wan-2-1]]（arXiv:2503.20314，"Wan: Open and Advanced Large-Scale Video Generative Models"）的基础架构之上。Wan2.1 已确立了基于 [[dit-scalable-diffusion-transformers]] + [[flow-matching]] 的视频扩散范式：3D 因果 VAE（Wan-VAE）+ 视频 DiT + umT5 文本编码器，开源 1.3B/14B 两档，是当时开源视频生成的 SOTA。**注意：arXiv:2503.20314 是 Wan2.1 技术报告，并不覆盖 Wan2.2 的 MoE/新 VAE**；Wan2.2 截至发布没有独立的 arXiv 技术报告，其 Wan2.2 专属方法披露集中在 GitHub README 与 HF model card 的"Introduction of Wan2.2"章节（含 MoE 架构、高压缩 VAE、Wan-Bench 2.0 对比；本页据此摘录）。（落盘的 `wan-2-2--blog.md` 是 wan.video 产品落地页，无技术内容，不作为方法来源。）
- **要解决的问题**：(1) 扩大模型容量但不增加推理成本——LLM 里 MoE 已验证可"涨参数不涨推理算力"，Wan2.2 把这一思路迁移到扩散去噪过程；(2) 让视频生成"上消费级显卡"——通过高压缩 VAE + 5B 稠密模型把 720P 生成拉到 4090 可跑；(3) 电影级美学可控——引入带光照/构图/对比度/色调标注的精选美学数据。
- **技术脉络中的位置**：与 [[hunyuan-video]]、[[mochi]]、[[cogvideox]] 等同期开源视频模型同属 DiT+流匹配阵营；Wan2.2 的差异化在于**MoE 时序专家**（区别于 LLM 的 token 级路由 MoE）与**高压缩比 VAE 下的消费级部署**。

## 模型架构
**整体三段式（沿用 Wan2.1）**：Wan-VAE 把像素视频编码到 latent → 视频 Diffusion Transformer 去噪 → unpatchify 解码。

- **Backbone：视频 DiT**。每个 transformer block 内：Self-Attention（时空全注意力，建模时空上下文）→ Cross-Attention（注入文本条件）→ FFN，外加 AdaLN 风格的时间步调制。Patchify 用 kernel (1,2,2) 的 3D 卷积，序列长度 L = (1+T/4)×H/16×W/16。时间步 embedding 经一个**全 block 共享的 MLP**（Linear+SiLU）预测 6 个调制参数，每个 block 仅学各自的 bias——该共享设计使参数量约降 25%，同参数规模下性能更好。
- **MoE 时序双专家（Wan2.2 的核心创新，A14B 系列）**：把去噪轨迹按**信噪比 SNR** 切成两段，用两个专门化的专家网络：
  - **高噪专家（high-noise expert）**：去噪早期（t 大、噪声高、SNR 低），负责整体布局/构图；
  - **低噪专家（low-noise expert）**：去噪后期（t 小、SNR 高），负责细节精修。
  - **切换点**：定义阈值步 t_moe，对应 SNR_min 的一半；当 t < t_moe 时从高噪专家切到低噪专家。SNR 随去噪步 t 单调递减，因此切换是确定性的、按时间步路由，而非 LLM 那种 token 级可学习门控。
  - **参数账**：每个专家约 14B，合计 27B 总参数，但**每个去噪步只激活其中一个专家（14B）**，所以推理算力与显存与 14B 稠密模型几乎相同。
  - **消融**：以验证损失曲线对比四种设置——Wan2.1（无 MoE）基线、"Wan2.1 当低噪专家+Wan2.2 高噪专家"、"Wan2.1 当高噪专家+Wan2.2 低噪专家"、完整 Wan2.2(MoE)。完整 MoE 版验证损失最低，收敛与分布拟合最优。
- **Text encoder**：umT5（umT5-xxl），512 token 上下文。选 umT5 的理由（Wan2.1 给出）：多语种（中英 + 视觉文本）编码强、组合性优于同规模单向注意力 LLM、收敛更快。
- **VAE：Wan2.2-VAE（高压缩版，配 5B TI2V）**。3D 因果 VAE，T×H×W 压缩比 **4×16×16**（即总压缩率 64，相比 Wan2.1 的 4×8×8 进一步提升空间压缩），仍保持高质量重建；TI2V-5B 再叠一层 patchification，**整体压缩比达 4×32×32**。因果卷积 + feature-cache 机制保证时序因果性并支持分块/长视频推理。
- **参数量与分辨率策略**：
  - **T2V-A14B / I2V-A14B**：MoE，27B 总 / 14B 激活，支持 480P 与 720P，5 秒视频。
  - **TI2V-5B**：5B 稠密，统一框架内原生支持 t2v 与 i2v，仅 720P（注意其 720P 尺寸是 1280×704 / 704×1280，因 32 倍空间压缩需被 32 整除）、24fps。
  - **条件注入**：文本走 cross-attention；I2V（Wan2.1 机制，Wan2.2 沿用）把首帧条件图与零填充帧沿通道拼接、再叠一个二值 mask（1=保留帧/0=待生成帧），与噪声 latent concat 后送入 DiT，故 I2V DiT 输入通道多于 T2V；另用 CLIP 提条件图特征经投影注入；TI2V 由是否给 `image` 参数自动切 t2v / i2v。

## 数据
Wan2.2 的数据披露偏定性（无独立论文），关键数字来自 README/model card；底层清洗/标注流程沿用 Wan2.1 技术报告。

- **相对 Wan2.1 的规模增量（Wan2.2 官方明确给出）**：训练数据显著扩大——**图像 +65.6%、视频 +83.2%**。官方称这直接提升了运动、语义、美学多维泛化，达到"开源+闭源里 TOP"表现。
- **电影级美学数据（Wan2.2 新增重点）**：精心策划的美学数据，带**光照（lighting）、构图（composition）、对比度（contrast）、色调（color tone）等细粒度标签**，使生成可按用户美学偏好可控地输出电影化风格。
- **底层数据管线（继承自 Wan2.1，PDF 正文）**：
  - 来源：内部版权数据 + 公开可获取数据，先去重；总量"数十亿（billions）图像与视频"。
  - **四步清洗**（基础维度→视觉质量→运动质量→视觉文本）：基础维度含 OCR 文本占比检测、LAION-5B 美学分类器初筛、NSFW 评分、水印/Logo 检测裁剪、黑边检测、过曝检测、**合成图检测**（即便 <10% 生成图污染也显著掉点，故训练专家分类器剔除）、模糊评分、时长（>4 秒）与分辨率门限；这套预处理约**剔除初始数据集 50%**。
  - 视觉质量：分 100 个 cluster 防长尾丢失，人工 1–5 打分训练专家评估模型，再给全量打分。
  - 运动质量：分 6 档（最优运动 / 中等 / 静态 / 镜头驱动 / 低质 / 抖动），不同档调采样比例，静态与纯镜头运动降权。
  - **标注/re-caption**：自研 dense caption 模型给每张图/每段视频生成密集描述；re-caption 数据把简短 tag 扩成详细描述；另有编辑指令 caption、组图描述、OCR 增强 caption、人工标注高质 caption（用于训练末段）。
- **数据配比动态调整**：按训练吞吐在各阶段动态调整运动/质量/类别比例。

## 训练方法
- **训练目标：Flow Matching（Rectified Flow）**。给定 latent x1、噪声 x0~N(0,I)、从 logit-normal 采样的 t∈[0,1]，线性插值 xt = t·x1 + (1−t)·x0，真值速度 vt = x1 − x0，模型预测速度，损失为 MSE：L = E‖u(xt, ctxt, t; θ) − vt‖²。ctxt 为 512-token 的 umT5 文本 embedding。
- **多阶段渐进训练（继承 Wan2.1）**：先 **256px 低分辨率纯文生图预训练**（强制跨模态语义-文本对齐与几何结构保真，避开高分辨率长视频直接联合训练的吞吐塌陷与显存/梯度方差问题）→ 随后图像-视频联合优化，分辨率与时长逐级上调（720P 视频 typ. 81 帧）。
- **MoE 专家训练（Wan2.2）**：两个专家各自负责不同 SNR/噪声区间；消融显示用 Wan2.1 权重热启动任一专家都不如两专家都用 Wan2.2 权重的完整版。注意 README 只给到此颗粒度，**MoE 两专家的具体训练课程、是否共享底座、step 配比未公开披露**。
- **后训练 / 偏好对齐**：Wan2.1 报告提到 post-training 阶段（含人工标注高质 caption 收尾、指令编辑等下游任务）；**Wan2.2 是否做 RLHF/DPO/reward model 偏好对齐未在已获取一手源中明确披露——未披露**。
- **蒸馏与加速（来自 Wan2.1 报告，非 Wan2.2 官方权重特性）**：报告描述了 Latent Consistency Model（LCM）/VideoLCM 把扩散+CFG 蒸馏成 **4 步**一致性模型，配合 Streamer 长视频框架可达 **10–20× 加速、8–16 FPS**；以及 int8（attention/linear）+ TensorRT 量化把 4090 上推到 ~8 FPS。**这些是 Wan2.1 报告里的研究方向；Wan2.2 官方开源仓库默认权重未声明内置步数蒸馏**，社区（LightX2V、FastVideo、cache-dit 等）另行提供 Wan2.2 的步蒸馏/量化/稀疏注意力加速版。

## Infra（训练 / 推理工程）
- **训练并行（Wan2.1 报告，Wan2.2 沿用同栈）**：VAE/Text Encoder 用 DP；DiT 用 **FSDP + 2D Context Parallelism（外层 Ring Attention、内层 Ulysses，类 USP）**。1M token、batch=1 时 DiT 激活存储约 8TB，故对 DiT 专门设计分布式。示例：128 GPU 配置下 CP=16（Ulysses=8 × Ring=2）、FSDP=32、DP=4，全局 batch=8b。2D CP 在 256K 序列/16 GPU 跨 2 机时把通信开销从 Ulysses 的 >10% 降到 <1%。显存优化用**激活 offload**（PCIe 传输与 1–3 个 DiT 层计算重叠）替代部分梯度检查点。**具体训练算力（GPU 型号/卡数/GPU-hours）未在已获取一手源中披露——未披露**。
- **推理工程（Wan2.2 仓库实测）**：
  - 多卡推理用 **PyTorch FSDP + DeepSpeed Ulysses**（`--dit_fsdp --t5_fsdp --ulysses_size 8`），Hopper 上用 FlashAttention3。
  - 显存友好选项：`--offload_model True`（模型 offload）、`--convert_model_dtype`、`--t5_cpu`（文本编码器放 CPU）。
  - **14B MoE**：单卡需 ≥80GB VRAM 跑 720P；可多卡 Ulysses 切分。
  - **TI2V-5B**：单张 **RTX 4090（24GB）** 即可跑 720P；官方称无特别优化下 **5 秒 720P 视频 <9 分钟**，属最快 720P@24fps 之列。
  - VAE 推理用 feature-cache 分块（每块 ≤4 帧）降显存、保因果。
- **生态集成**：Day-0 接入 ComfyUI 与 Diffusers（T2V-A14B / I2V-A14B / TI2V-5B 均有 Diffusers pipeline）；HF Space 上线 5B demo。prompt extension 走 Dashscope（qwen-plus / qwen-vl-max）或本地 Qwen2.5 系列。

## 评测 benchmark（把效果讲清楚）
- **Wan-Bench 2.0（Wan2.2 官方自建）**：Wan2.2 在自建的 Wan-Bench 2.0 上与多个主流**闭源商业模型**对比，官方称在**大多数关键评测维度上超越**这些领先模型。**具体逐维分数/对手名单/数值在 README 中以图（assets/performance.png）呈现，已获取的文本一手源未给出可引用的数字表——故此处不编造具体数值。**
- **Wan-Bench（1.0，Wan2.1 报告，方法学参考）**：自动化、人对齐基准，三大核心维度——动态质量、图像质量、指令遵循，细分至 **14 个 fine-grained 指标**（PDF §4.6 原文："14 fine-grained metrics"）；每个候选模型收集 1,035 条样本评测。Wan2.1-14B 在该报告内对 Sora、HunyuanVideo、若干 CN-Top 商业模型、Runway 的 win/draw/loss rate 多数占优（Fig.1 给出的 Wan win rate 落在 **0.60（对 Runway）—0.82** 区间，多数对手 0.65–0.75）。**另注：报告称 Wan-14B 在公开 [[vbench]] 榜达 SOTA，聚合分 86.22%（visual quality 86.67% / semantic consistency 84.44%）；VBench 自身是 16 维基准，勿与 Wan-Bench 的 14 指标混淆。**
- **MoE 消融（Wan2.2，定性）**：完整 Wan2.2(MoE) 验证损失低于 Wan2.1 基线及两种"半 Wan2.1 半 Wan2.2 专家"变体，说明双专家联合训练比复用旧权重更优。
- **缺口**：Wan2.2 未提供 VBench 公开榜的可引用新分数、FID/CLIPScore 等学术指标，亦无独立论文给出完整对照表；本页据已抓取源**只能定性转述官方"多维超越闭源"的结论，具体数字未报告**。

## 创新点与影响
- **核心贡献**：
  1. **首个把 MoE 引入视频扩散模型**的有效方案——按 SNR/去噪时间步把网络拆成高噪/低噪两专家，"涨容量不涨推理成本"（27B 总 / 14B 激活），并以验证损失消融证明优于稠密基线。这是对扩散模型"不同噪声水平需要不同能力"这一直觉的工程化落地，区别于 LLM 的 token 级 MoE 路由。
  2. **高压缩 Wan2.2-VAE（4×16×16，叠 patchify 到 4×32×32）+ 5B 稠密 TI2V**，把 720P@24fps 视频生成拉到**单张 4090 / <9 分钟**，显著降低开源视频生成的算力门槛，统一 t2v+i2v。
  3. **电影级美学可控**：带光照/构图/对比度/色调标签的精选美学数据，支持按美学偏好可控生成。
  4. **数据规模大幅扩张**（图 +65.6% / 视频 +83.2%）带来运动/语义/美学全面提升。
  5. **全开源（Apache-2.0）**：T2V/I2V/TI2V 权重+代码+ComfyUI/Diffusers 集成，并衍生 S2V-14B（音频驱动）、Animate-14B（角色动画/替换）等成员，催生 LightX2V、FastVideo、HuMo、DiffSynth-Studio 等大量社区加速/应用工作。
- **影响**：成为 2025 年下半年开源视频生成的事实标准底座之一；"按去噪阶段分专家"的思路对后续视频/图像扩散 MoE 有示范意义；消费级 720P 部署推动了本地化视频生成工具链。
- **已知局限**：(1) 无独立技术报告，MoE 训练细节、偏好对齐、训练算力、Wan-Bench 2.0 具体数字均未充分披露；(2) 14B MoE 单卡仍需 80GB，真正消费级的是 5B（且 5B 牺牲了 MoE 容量与 480P 选项）；(3) 官方默认权重未内置步数蒸馏，快速推理依赖社区方案；(4) Wan-Bench 2.0 为自建基准，对外可复现性有限。

## 原始链接
- github: https://github.com/Wan-Video/Wan2.2
- hf (T2V-A14B): https://huggingface.co/Wan-AI/Wan2.2-T2V-A14B
- hf (I2V-A14B): https://huggingface.co/Wan-AI/Wan2.2-I2V-A14B
- hf (TI2V-5B): https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B
- modelscope: https://modelscope.cn/organization/Wan-AI
- arxiv (Wan2.1 基础技术报告，非 Wan2.2): https://arxiv.org/abs/2503.20314
- blog / 产品页: https://wan.video

## 本地落盘文件
- ../../../sources/omni/2025/wan-2-2--github-readme.md
- ../../../sources/omni/2025/wan-2-2--hf-t2v-a14b.md
- ../../../sources/omni/2025/wan-2-2--hf-i2v-a14b.md
- ../../../sources/omni/2025/wan-2-2--hf-ti2v-5b.md
- ../../../sources/omni/2025/wan-2-2--blog.md
- ../../../sources/omni/2025/arxiv-2503.20314.pdf
- ../../../sources/omni/2025/arxiv-2503.20314.txt
