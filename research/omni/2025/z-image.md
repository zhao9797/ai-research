---
title: "Z-Image / Z-Image-Turbo：单流扩散 Transformer 的高效 6B 文生图基础模型"
org: "Alibaba Tongyi Lab (Tongyi-MAI)"
country: China
date: "2025-11"
type: tech-report
category: t2i
tags: [t2i, diffusion-transformer, single-stream, dmd, distillation, rlhf, bilingual-text, image-editing, efficient]
url: "https://arxiv.org/abs/2511.22699"
arxiv: "https://arxiv.org/abs/2511.22699"
pdf_url: "https://arxiv.org/pdf/2511.22699"
github_url: "https://github.com/Tongyi-MAI/Z-Image"
hf_url: "https://huggingface.co/Tongyi-MAI/Z-Image-Turbo"
modelscope_url: "https://www.modelscope.cn/models/Tongyi-MAI/Z-Image-Turbo"
project_url: "https://tongyi-mai.github.io/Z-Image-blog/"
downloaded: [arxiv-2511.22699.pdf, arxiv-2511.22699.txt, arxiv-2511.22677.pdf, arxiv-2511.22677.txt, arxiv-2511.13649.pdf, arxiv-2511.13649.txt, z-image--hf-modelcard.md, z-image--readme.md, z-image--blog.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Z-Image 是阿里通义 MAI 实验室 2025-11 开源的 **6.15B 单流扩散 Transformer（S3-DiT）文生图基础模型**，用「数据基础设施 + 单流早融合架构 + 渐进训练课程 + 蒸馏/RL 加速」四根支柱，**只花 314K H800 GPU 小时（约 63 万美元）完成全流程训练**，正面挑战 Qwen-Image(20B)/FLUX.2(32B)/HunyuanImage-3.0(80B) 的「无脑堆参数」路线；蒸馏版 **Z-Image-Turbo 仅 8 NFE、H800 上亚秒级出图、<16GB 显存可跑**，在 Artificial Analysis Image Arena 以 Elo 1161 排名第 8（开源第一），照片级真实感与中英双语文本渲染逼近 Nano Banana Pro / Seedream 等闭源旗舰。

## 背景与定位
高性能文生图当前被两类范式割裂：一边是 Nano Banana Pro、Seedream 4.0 这类闭源「黑箱」，性能强但不可复现；另一边是开源模型走「无止境扩参数」路线（Qwen-Image 20B、FLUX.2 32B、HunyuanImage-3.0 80B），训练/推理/微调对消费级硬件极不友好。还有一条捷径是从闭源模型蒸馏合成数据，但作者批评这会造成「闭环反馈→误差累积→数据同质化」，抑制新视觉能力涌现。

Z-Image 的立意是**用 6B 体量、纯真实世界数据（不蒸馏其它模型）、极低算力**，做出对标顶级模型的端到端方案。它在技术脉络上属于 [[mmdit]] / [[stable-diffusion-3]] 的 MM-DiT 谱系，但把双流改成**单流早融合**（借鉴 decoder-only LLM 的可扩展性），并在推理侧用自研 [[decoupled-dmd]] 与 [[dmdr]] 两套 DMD 改进做少步蒸馏。它是「小模型对抗 scaling」叙事的代表作，与 [[qwen-image]]、[[flux-2]]、[[hunyuanimage-3-0]] 形成「效率派 vs 规模派」对照。

模型家族共四个变体（HF 已开 Z-Image / Z-Image-Turbo，Omni-Base 与 Edit 标注 To be released）：
- **Z-Image-Omni-Base**：仅预训练、未 SFT/RL，生成+编辑通用底座，定位最「raw」的社区微调起点（50 步 + CFG）。
- **Z-Image**：底座上做 SFT 的高质量生成模型（50 步 + CFG，多样性中等、易微调）。
- **Z-Image-Turbo**：在 Z-Image 上做少步蒸馏 + RL，8 步、无 CFG、视觉质量"Very High"但多样性低（已开放）。
- **Z-Image-Edit**：在底座上续训的图像编辑专用变体（50 步 + CFG）。

## 模型架构
**S3-DiT（Scalable Single-Stream DiT）**——这是 Z-Image 的核心。文本 token、图像语义 token（编辑用）、图像 VAE token 在**序列维度拼成一条统一输入流**送进 Transformer 主干，实现每层稠密跨模态交互，相比双流（文本/图像各走一路）大幅提升参数效率。设计灵感来自 decoder-only LLM 的可扩展性。

组件：
- **文本编码器**：轻量 **Qwen3-4B**（看中其中英双语能力），冻结。
- **图像 tokenizer / VAE**：直接复用 **Flux VAE**（看中重建质量），冻结。
- **视觉语义编码器（仅编辑）**：**SigLIP 2**，从参考图抽取抽象语义，冻结。
- **位置编码**：**3D Unified RoPE**——图像 token 沿空间维展开、文本 token 沿时间维递增；编辑任务里参考图与目标图共享空间 RoPE 坐标，但在时间维错开一个单位间隔，并对参考图/目标图施加不同 time-condition 值以区分「干净/带噪」图像。

S3-DiT 结构细节（Table 2）：
- 总参数 **6.15B**，**30 层**，hidden dim **3840**，**32** 个注意力头，FFN 中间维 **10240**，patch 切分 $(d_t,d_h,d_w)=(32,48,48)$。
- 入口先用「模态特定 processor」（每个 2 个 transformer block）做初步对齐，再进单流主干。
- 稳定性设计：**QK-Norm** 调控注意力激活 + **Sandwich-Norm** 约束 attention/FFN 块输入输出信号幅度，统一用 **RMSNorm**。
- 条件注入：把 condition 向量投影成 scale 与 gate，调制 Attention/FFN 的归一化输入输出；该投影做**低秩分解**——一个层无关的共享 down-projection + 各层独立的 up-projection，省参数。velocity 输出走 zero-init gate。

为弥补 6B 体量在世界知识/复杂推理上的不足，架构外挂一个 **Prompt Enhancer（PE）**：用一个固定（不训练）的预训练 VLM + system prompt，把用户原始 prompt 改写增强。PE 在 SFT 阶段就介入（用 PE 增强后的 caption 微调扩散主干），让主干与 PE 对齐，无需额外训练 LLM。带「结构化推理链」的 PE 能把经纬度坐标推断成具体场景（如 30°09′36″N,120°07′12″E→杭州西湖）、把"泡普洱茶步骤"展开成具体分步插画，而非死板渲染文字。

## 数据
**不蒸馏其它模型，纯真实世界数据**，靠一套「Efficient Data Infrastructure」做高效筛选与课程编排（核心理念：在固定算力下最大化「单位算力知识获取率」，从拼数量转向拼数据效率）。四大模块：

1. **Data Profiling Engine（数据画像）**：对海量未筛数据（含大规模内部版权图集）算多维特征——分辨率/文件大小/pHash 去重等元数据；技术质量（压缩痕迹比、自训质量模型打 color cast/模糊/水印/噪声分、信息熵过滤纯色边框/低复杂度图）；语义与美学（自训美学打分模型、按 Imagen 3 做法训 AIGC 检测分类器剔除 AI 生成图、自训 VLM 打语义标签+NSFW 分，特别关注中国文化概念）；跨模态一致性（用 **CN-CLIP** 算图文相关性，低分丢弃）+ 多级 caption。
2. **Cross-modal Vector Engine（跨模态向量引擎）**：在数十亿 embedding 上做语义去重——把 SD3 的去重法改造成基于 k-NN 近邻图 + 社区检测的可扩展方案，全 GPU 流水线**约 8 小时/10 亿条（8×H800，含建索引与 100-NN 查询）**；同时支持跨模态检索，用失败 case 反查并剪除责任数据簇，或检索补齐概念空洞。
3. **World Knowledge Topological Graph（世界知识拓扑图）**：先用全部 Wikipedia 实体+超链建图，再做中心性剪枝（去极低 PageRank 节点）+ 可视生成性剪枝（VLM 剔除无法可视化的抽象概念），再用内部图集 caption 的 tag/embedding 做层次聚类补节点，最后人工上调高频概念权重并注入新潮概念。该图用 BM25 分 + 父子层级关系算「语义级采样权重」，驱动分阶段的均衡采样。
4. **Active Curation Engine（主动策展引擎）**：人在环（human-in-the-loop）主动学习循环，用拓扑图 + reward model 从未标注池抽均衡子集→captioner/reward 打伪标签→人+AI 双验证器过滤，被拒样本触发人工修正→高质量标注回流重训 captioner 与 reward model，形成闭环（论文以"松鼠鳜鱼"长尾概念为例，说明模型缺该菜名概念时会错误地把"松鼠"+"鳜鱼"组合，需靠该引擎补域内数据）。

**Captioner（Z-Captioner）**：自训 all-in-one 图像描述模型，一图给五种 caption（长/中/短 + tags + 模拟用户 prompt）。关键设计：
- **OCR 用 CoT**：先显式识别图中所有文字（强制保留原语言不翻译），再据此生成 caption——作者强调「caption 含显式 OCR 信息」与「生成图准确渲染文字」强绑定，尤其对长/密文本。
- **注入世界知识**：基于元信息做条件 captioning，让 captioner 能正确命名公众人物/地标/事件（如自动识别西湖、雷峰塔），显著抑制幻觉。长 caption 用「平实客观」语言、只描述可见事实、抑制主观联想，以提升数据效率。
- **编辑用 Difference Caption**：三步 CoT（分别给源/目标图详细 caption → 对比分析差异 → 合成简洁编辑指令）。

**编辑数据对构造**（三策略，见 Figure 7）：(a) **Graphical Representation**——对一张输入图用专家模型合成 N 个不同编辑版本，再做任意两两组合，零成本扩到约 $2\binom{N}{2}+1$ 对，还能造混合编辑对和逆向对；(b) **视频帧配对**——从视频帧取天然相关图组，用 CN-CLIP 余弦相似度筛高相关对，天然耦合多种编辑类型；(c) **文本编辑渲染**——可控文本渲染系统精确控制字体/颜色/大小/位置，生成已知 ground-truth 编辑操作的成对图。

数据**规模/总量、配比的绝对数字未披露**（仅给方法与质量控制），编辑续训阶段披露 text-to-image : image-to-image ≈ **4:1** 以防退化。

## 训练方法
训练目标：**flow matching（rectified flow）**。噪声输入按 $x_t=t\cdot x_1+(1-t)\cdot x_0$ 线性插值（$x_0$ 高斯噪声、$x_1$ 真图），模型预测速度场 $v_t=x_1-x_0$，损失 $\mathcal{L}=\mathbb{E}[\|u(x_t,y,t;\theta)-(x_1-x_0)\|^2]$。沿用 SD3 的 logit-normal 时间采样集中训练中间时间步；按 Flux 的 dynamic time shifting 适配多分辨率下的 SNR 差异。

**多阶段课程**（Figure 11）：
1. **低分辨率预训练**：单阶段、纯 256² 文生图，**占总预训练算力一半以上**——作者认为模型大部分基础视觉知识（如中文文字渲染）在此阶段习得。
2. **Omni-Pre-training（全能预训练）**：三层含义——(a) **任意分辨率训练**（原图分辨率经映射函数落到预定义范围，学跨尺度信息）；(b) **联合文生图 + 图生图训练**（利用预训练大算力消化大规模弱对齐图像对，为编辑提供强初始化，且不损 T2I 性能）；(c) **多级双语 caption 训练**（Z-Captioner 生成长/中/短/tag/模拟 prompt，并以小概率混入原始文本元数据补世界知识）。完成后可生成任意分辨率至 1k–1.5k，并能同时以图、文为条件。
3. **PE-aware SFT**：用 PE 增强后的 caption 做监督微调，让主干与 PE 协同。SFT 目的不是修局部瑕疵，而是**收窄生成分布**到高保真子流形（从「多样性最大化」转向「质量最大化」）。三个 trick：(a) **标签重采样做概念均衡**——用拓扑图 + BM25 实时算 rarity 分，上采样长尾概念、下采样高频概念，防灾难性遗忘；(b) **模型合并（Model Merging）**——训多个各偏向不同能力维度（指令遵循 / 美学）的 SFT 变体，再在参数空间线性插值 $\theta_{final}=\sum_i\alpha_i\theta_i$，平滑损失面、中和单一偏置。

**少步蒸馏（Few-Step Distillation）**：SFT 模型用 CFG 需约 100 NFE 出图，目标降到 8 NFE。直接用经典 DMD 会丢高频细节、出色偏，于是提出两项自研改进：
- **Decoupled DMD（arXiv 2511.22677）**：核心洞见是 DMD 的成功并非单一「分布匹配」机制，而是两个独立协作机制的分工——把实际带 CFG 的 DMD 梯度严格分解后，发现真正驱动「多步→少步」转换的是被长期忽视的 **CFG Augmentation (CA)**（把 CFG 信号直接施加到学生输出，是"engine 矛"），而严格符合理论 IKL 推导的 **Distribution Matching (DM)** 主要充当**正则器/盾**（保训练稳定、消伪影）。作者证明 DM 正则不唯一（更简单的非参约束或 GAN 目标也能起稳定作用）。据此为 CA 与 DM **解耦各自的 renoising schedule**，进一步提质——蒸馏后模型在写实感与视觉冲击上甚至超过多步教师。
- **DMDR（DMD meets RL，arXiv 2511.13649）**：把 RL 直接融入少步蒸馏。两阶段——初始阶段用 **Reward-Tilted Distribution Matching (RT-DM)**（向「reward 倾斜的教师分布」蒸馏，优先人类偏好区域），配 **Dynamic Distribution Guidance (DynaDG)** 与 **Dynamic Renoise Sampling (DynaRS)** 退火稳定冷启动；第二阶段转入 **DMD 与 RL 联合优化**——RL 解锁性能、突破"纯模仿教师"的天花板，DM 项作为强正则**抑制 reward hacking**。框架兼容 flow/denoising 基座与 ReFL/DPO/GRPO 等多种 RL。最终 Z-Image-Turbo = SFT 模型 + Decoupled-DMD + DMDR，**8 步推理质量「与 100 步教师难以区分、且常更优」**。

**RLHF（用于非 Turbo 的对齐链路，两阶段）**：先训一个三维 reward model（指令遵循、AIGC 感知、美学）——指令遵循把 prompt 句法/语义分解成 (主体实体/属性/动作交互/空间构图/风格渲染) 五级层级，人工只点未满足元素，按满足比例算分。然后：
- **Stage 1 离线 DPO**：只针对**客观可验证维度**（文本渲染、物体计数等有二值对错判据），用 VLM 批量生成偏好对再人工核验清洗；配 curriculum learning（从单词/少物体起步到多元素复杂布局），并优化正负样本区分度的配对策略。
- **Stage 2 在线 GRPO**：用 reward model 给的多维复合 advantage（写实、美学、指令遵循等聚合）做细粒度在线优化，显著提升写实感/美学/语义准确并减伪影；作者称多维优化明显优于单一 reward。

**编辑续训（Z-Image-Edit，两阶段）**：续训阶段先 512² 快速适配编辑任务数千步，再升 1024² 提质，因编辑数据稀缺贵，混 T2I:I2I=4:1；后续 SFT 阶段手工构造任务均衡高质量子集提升指令遵循，合成数据（如渲染文本）虽 100% 指令正确但偏离真实用户分布，在最终阶段被大幅降采样。

## Infra（训练 / 推理工程）
**全流程算力（Table 1，按 H800 约 \$2/卡时计）**：低分辨率预训练 147.5K 卡时（\$295K）+ Omni 预训练 142.5K 卡时（\$285K）+ 后训练 24K 卡时（\$48K）= **总计 314K H800 GPU 小时 ≈ \$628K**。

训练系统优化：
- 分布式用混合并行——冻结的 VAE/Text Encoder 走标准 **DP**；大 DiT 用 **FSDP2** 切分优化器状态与梯度；全 DiT 层做 **gradient checkpointing**（以算力换显存，支持更大 batch）；DiT block 用 **torch.compile（JIT）** 加速并省显存。
- 针对混合分辨率训练的 padding 浪费：**序列长度感知的批构造**——按元数据估算每样本序列长度，把相近长度样本分到同一 batch；并配 **动态 batch size**（长序列小 batch 防 OOM、短序列大 batch 防资源空置），最大化各分辨率下的硬件利用率。

推理工程：
- **Z-Image-Turbo**：8 NFE（API 调用 `num_inference_steps=9` 实际 8 次 DiT 前向）、**guidance_scale=0（Turbo 不用 CFG）**；**H800 上亚秒级**出图（需 FlashAttention-3 + torch.compile 才达亚秒）；**<16GB 显存**消费级硬件可跑，支持 `enable_model_cpu_offload()` 进一步降显存。
- 基础 Z-Image（非 Turbo）推荐 28–50 步、带 CFG。
- 注意力后端可切 FlashAttention-2 / FlashAttention-3；diffusers 已合入 `ZImagePipeline`（PR #12703、#12715）。
- 社区 Cache-DiT 通过 DBCache + Context/Tensor Parallelism 为 Z-Image 提供推理加速，4 卡上近 **4× 加速**且精度损失可忽略。
- Arena 数据显示 Z-Image-Turbo 推理成本 **\$5.0 / 1000 张**，是 top-10 模型里参数最小（6B）、单图成本最低的。

## 评测 benchmark（把效果讲清楚）
**人类偏好 / Elo（最具说服力）**：
- **Artificial Analysis Image Arena**：Z-Image-Turbo Elo **1161，总榜第 8，开源第一**；性能与 Google Imagen 4、ByteDance Seedream 相当，且是 top-10 里最小参数（6B）、最低单图成本（\$5/1000 张）。
- **Alibaba AI Arena（Table 3）**：Z-Image-Turbo Elo **1025，总榜第 4、开源第一**，胜率 45%；排在 Imagen 4 Ultra(1048)、gemini-2.5-flash-image(1046)、Seedream 4.0(1039) 之后，领先 Seedream 3.0(1012)、Qwen-Image(1008,20B)、GPT Image 1(986)、FLUX.1 Kontext Pro(950)。
- **对 FLUX.2 dev 的人评**（222 样本×3 标注，Table 4）：Z-Image 的 G Rate(好) **46.4%**、S Rate(相当) **41.0%**、B Rate(差) 仅 **12.6%**，G+S 合计 **87.4%**——且 Z-Image 只有 FLUX.2 dev 1/5 参数（6B vs 32B）。

**文本渲染**：
- **CVTG-2K（英文复杂文本，Table 5）**：Z-Image 平均 Word Accuracy **0.8671**，排第 1，超 GPT-Image-1 High(0.8569)、Qwen-Image(0.8288)；Z-Image-Turbo 拿到全场最高 CLIPScore **0.8048** 且 Word Acc 0.8585。
- **LongText-Bench（Table 6）**：EN Z-Image **0.935**（第 3，Qwen-Image 0.943 第 1）；ZH Z-Image **0.936**（第 2，Qwen-Image 0.946 第 1）；Turbo EN 0.917 / ZH 0.926。
- **OneIG-EN（Table 7）**：Z-Image 总分 **0.546 第 1**（超 Qwen-Image 0.539、GPT-Image-1 0.533），其中 Text 子项 **0.987**（EN）/ **0.988**（ZH）刷新 SOTA。**OneIG-ZH（Table 8）**：Z-Image 总分 **0.535 第 2**（Qwen-Image 0.548 第 1），Text 子项 0.988 仍最高。

**通用对齐 / 指令遵循**：
- **GenEval（Table 9）**：Z-Image 总分 **0.84**，与 Seedream 3.0、GPT-Image-1 High 三方并列第 2，仅次于 Qwen-Image(0.87)；Z-Image-Turbo **0.82**（与底座差 2 分）。
- **DPG-Bench（Table 10）**：Z-Image 总分 **88.14 第 3**（Qwen-Image 88.32、Seedream 3.0 88.27 略高），其中 Attribute 维 **93.16** 反超 Qwen-Image(92.02)；Turbo 84.86。
- **TIIF testmini（Table 11）**：Z-Image / Z-Image-Turbo 分列第 4 / 第 5（GPT-Image-1 第 1）。
- **PRISM-Bench**：EN 轨 Z-Image-Turbo **77.4 第 3**（超底座与 Qwen-Image）；ZH 轨 Z-Image **75.3 第 2**（Text Rendering 83.4、Composition 88.6 突出）。

**图像编辑（Z-Image-Edit）**：
- **ImgEdit（Table 14）**：Z-Image-Edit 总分 **4.30 排第 3**（仅次于 UniWorld-V2 4.49、Qwen-Image-Edit[2509] 4.35），在物体添加（Add）/抽取（Extract）等子任务尤强。
- **GEdit-Bench（Table 15）**：Z-Image-Edit EN G_O **7.72 第 3**、CN G_O **7.52 第 3**（指标 G_SC 指令遵循 + G_PQ 视觉自然度），双语编辑稳健。

**关键消融/定性结论**：
- 蒸馏可视化（Figure 13）：SFT → 标准 DMD（模糊纹理+色偏）→ Decoupled-DMD（恢复锐利细节与准确色彩）→ +DMDR（速度与质量最优收敛，8 步常超 100 步教师）。
- RLHF 前后对比（Figure 14）：在少步蒸馏基础上进一步提升写实/美学/指令遵循。
- PE 推理链消融（Figure 15）：有推理链才能把经纬度→具体景点、把抽象指令→分步细节内容。
- 定性上 Z-Image-Turbo 在人物特写皮肤细节、手机随拍真实感、海报小字渲染等场景，常胜 Qwen-Image / HunyuanImage-3.0 / FLUX.2 dev，对标 Nano Banana Pro。

## 创新点与影响
**核心贡献**：
1. **S3-DiT 单流早融合架构**——把文本/语义/VAE token 拼成单序列，每层稠密跨模态交互，6B 体量逼近 20–80B 模型，给出「小模型对抗 scaling」的可行蓝图。
2. **极致成本效率**——314K H800 卡时（~\$63 万）跑完全流程，纯真实数据不蒸馏闭源模型，对学术界/中小团队极具参考价值。
3. **数据基础设施作为一等公民**——Profiling/Vector/拓扑图/主动策展四引擎，把「单位算力知识获取率」做成可工程化的课程学习系统；CN-CLIP 图文过滤 + OCR-CoT captioning + 世界知识注入是文本渲染与世界知识强的根因。
4. **Decoupled-DMD + DMDR 两套蒸馏理论**——重新解释 DMD 成功机理（CA 是矛、DM 是盾），并首次把 DMD 与 RL 联合优化、用 DM 正则抑制 reward hacking，让 8 步 Turbo 超越多步教师。这两套方法本身是可迁移到其它扩散模型的通用技术。
5. **Omni 预训练统一生成+编辑**——一次预训练摊薄到多任务，低成本派生 Z-Image-Edit。
6. **PE 推理链**——外挂固定 VLM + 结构化推理链补 6B 体量的世界知识/推理短板，SFT 即对齐 PE，无需训 LLM。

**影响**：发布即登顶开源 T2I（两大 Arena 开源第一），Apache-2.0 + diffusers 原生支持 + <16GB 消费级可跑，降低了高质量文生图/编辑的部署与微调门槛；中英双语文本渲染达 SOTA，对中文创作场景意义大。Decoupled-DMD/DMDR 作为独立论文，对少步蒸馏与 RL 融合研究有方法学价值。

**已知局限**：
- 6B 体量在世界知识/复杂推理上仍有限，强依赖外挂 PE（关掉 PE 或 PE 失效时能力打折）。
- Turbo 走「质量最大化」路线，**多样性低**（model card 自标 Diversity=Low）；要多样性需用非 Turbo 的 Z-Image（50 步 + CFG）。
- 训练数据**绝对规模/配比未披露**，含「大规模内部版权图集」，复现需自建数据管线。
- 部分能力（Omni-Base、Edit 权重）截至报告仍 To be released。
- 亚秒级推理依赖 FlashAttention-3 + torch.compile，非所有硬件可达。

## 原始链接
- tech-report (arXiv 主报告): https://arxiv.org/abs/2511.22699
- paper (Decoupled-DMD): https://arxiv.org/abs/2511.22677
- paper (DMDR): https://arxiv.org/abs/2511.13649
- blog (官方项目主页): https://tongyi-mai.github.io/Z-Image-blog/
- github: https://github.com/Tongyi-MAI/Z-Image
- model-card (HF, Z-Image-Turbo): https://huggingface.co/Tongyi-MAI/Z-Image-Turbo
- modelscope: https://www.modelscope.cn/models/Tongyi-MAI/Z-Image-Turbo
- DMDR code: https://github.com/vvvvvjdy/dmdr

## 本地落盘文件
- ../../../sources/omni/2025/arxiv-2511.22699.pdf （主报告 PDF，.gitignore 排除）
- ../../../sources/omni/2025/arxiv-2511.22699.txt
- ../../../sources/omni/2025/arxiv-2511.22677.pdf （Decoupled-DMD PDF）
- ../../../sources/omni/2025/arxiv-2511.22677.txt
- ../../../sources/omni/2025/arxiv-2511.13649.pdf （DMDR PDF）
- ../../../sources/omni/2025/arxiv-2511.13649.txt
- ../../../sources/omni/2025/z-image--hf-modelcard.md
- ../../../sources/omni/2025/z-image--readme.md
- ../../../sources/omni/2025/z-image--blog.md
