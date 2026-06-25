---
title: "Seedance 1.0: Exploring the Boundaries of Video Generation Models"
org: "字节跳动 Seed (ByteDance Seed)"
country: China
date: "2025-06"
type: tech-report
category: video
tags: [video, t2v, i2v, dit, mmdit, flow-matching, rlhf, distillation, multi-shot, bytedance, doubao, jimeng]
url: "https://arxiv.org/abs/2506.09113"
arxiv: "https://arxiv.org/abs/2506.09113"
pdf_url: "https://arxiv.org/pdf/2506.09113"
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://seed.bytedance.com/seedance"
downloaded: [arxiv-2506.09113.pdf, arxiv-2506.09113.txt, seedance-1-0--project.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Seedance 1.0 是字节跳动 Seed 的高性能、推理高效的**视频生成基座模型**，用**单一统一模型**原生支持文生视频（T2V）+ 图生视频（I2V）+ 原生多镜头叙事，最关键创新是「**解耦时空层 + 窗口注意力的 MMDiT** + 多维奖励的视频 RLHF + 多阶段蒸馏」；发布时（2025-06-10）在第三方平台 **Artificial Analysis** 视频竞技场的 **T2V 与 I2V 双榜同时登顶**（I2V 上较第二、三名 Veo 3 与 Kling 2.0 领先 100+ Elo），且 1080p 5 秒视频仅需 **41.4 秒**（NVIDIA-L20）即可生成，端到端比未蒸馏快 10×。

## 背景与定位
扩散模型推动视频生成快速进步，但当时的基座模型在**指令遵循、运动合理性、视觉保真度**三者间难以同时兼顾——开源代表 [[wan]]、[[hunyuan-video]]、[[cogvideox]]，商业代表 Veo、可灵（Keling）。Seedance 1.0 的定位是用一个原生双语（中/英）、多任务（T2V + I2V）统一模型把这三个维度同时拉满，并额外攻克两块短板：(1) **原生多镜头叙事**（一条 prompt 生成多个连贯镜头、保持主体/风格一致）；(2) **极致推理速度**（用蒸馏 + 系统优化把商用级延迟压到 41.4 秒/5s@1080p）。

技术脉络上它继承自字节 Seed 系的多项前置工作：VAE 的时序因果压缩借鉴 MAGVIT；DiT 主干用 [[stable-diffusion-3]] 的 MMDiT 设计；位置编码与多镜头能力借鉴自家 Seaweed 与 LCT；图像侧数据/量化方案复用 [[seedream]]（Seedream 系图像模型）。模型已落地火山引擎（Volcano Engine，Model ID `Doubao-Seedance-1.0-pro`）、豆包（Doubao）与即梦（Jimeng）。

## 模型架构
整体是 **VAE + DiT（MMDiT）+ 级联 Diffusion Refiner + LLM Prompt Engineering** 的四件套。

**Variational Autoencoder（VAE）。**
- 时序因果卷积架构（follow MAGVIT），encoder/decoder 都因果，可在 `T = T' = 0` 时无缝退化处理单张图像。
- 联合时空压缩：下采样比 `(rt, rh, rw) = (4, 16, 16)`，潜空间通道数 **C = 48**。
- 为适配更高下采样率、追求更好生成质量，**在 DiT 侧去掉 patchify 操作**（follow DCAE）。
- 训练损失 = L1 重建 + KL + LPIPS 感知 + 对抗损失；判别器用类 PatchGAN 的混合判别器，同时建模外观与运动。

**Diffusion Transformer（主干）。**
- 文本编码器用一个**微调过的 decoder-only LLM**；visual token 与 text token 拼接后送入 transformer。
- **解耦空间层 / 时间层（decoupled spatial & temporal layers）**：空间层在每帧内做注意力聚合，时间层跨帧做注意力；**时间层里对每帧做 window partition（窗口注意力）**，以在时间维获得全局感受野的同时显著降低训/推开销。文本 token 只在空间层参与跨模态交互。
- **MMDiT（follow SD3）**：多模态 self-attention 仅在空间层融合视觉+文本 token；时间层只处理视觉 token。空间层对两种模态用**两套独立权重**（adaptive layernorm、QKV 投影、MLP）。Q/K 在算注意力前做归一化以防训练不稳。
- **Multishot MM-RoPE**：视觉 token 用 3D RoPE，文本 token 额外加 1D 位置编码，构成 3D 多模态 RoPE（follow Seaweed / LCT）；支持视觉与文本 token 的**交错序列**，从而可训练「多镜头」视频——各镜头按动作时间顺序排列、每个镜头有自己的详细 caption。
- **统一任务建模**：把噪声输入与「干净帧 / 零填充帧」沿**通道维拼接**，再用二值 mask 指明哪些帧是要遵循的条件指令——用同一套表达统一 text-to-image / text-to-video / image-to-video，训练时混合各任务并通过控制条件输入调配比例。

**Diffusion Refiner（级联超分）。** 采用级联扩散：base 模型先生成 **480p**，再由学习到的 diffusion refiner 上采到 **720p / 1080p**。Refiner 由预训练 base 初始化，训练时以低分辨率（LR）视频为条件（LR 先上采到高分辨率，再与扩散噪声沿通道维拼接作为 DiT 输入）。

**Prompt Engineering（PE）模型。** 基于 **Qwen2.5-14B** 初始化，把用户 prompt 改写成与训练 caption 一致的「dense video caption」格式；分 SFT（全参微调，区分 i2v / t2v 不同 prompt 风格）+ RL（用正确/错误改写对做 **DPO**，并用 **LoRA** 微调）两阶段。

**参数量与分辨率策略。** 总参数量**未披露**；分辨率走「base 480p → refiner 720p/1080p」级联，预训练分阶段 256px→640px。

## 数据
图像数据准备沿用 [[seedream]] 的方法；视频数据有一套系统化处理流水线（三阶段：多样化采源 → 多阶段筛洗 → 离线打包）。**具体训练集规模/视频对数量未披露**（仅称「large-scale high-quality」）。

**预处理流水线（multi-stage curation）：**
- **多样化采源**：合法/合规来源（public + licensed），最大化覆盖时长、分辨率、主题（人/动物/物体）、场景、动作、题材（纪录片/动画）、艺术风格、运镜、摄影技法等维度。
- **镜头感知时序切分**：用 shot boundary detection 把长视频切成 ≤ 12 秒的短片，每片可含一个或多个时序连贯镜头（保留局部叙事流）。
- **视觉叠加矫正**：用「启发式规则 + 专门目标检测」识别 logo/水印/字幕/角标等叠加物，自适应裁剪以最大保留主体内容。
- **质量与安全过滤**：专门视觉质量模型剔除模糊、抖动、低美学、构图差、过度静止的片段；用分类器过滤色情、暴力、儿童剥削、裸露等违规内容。
- **语义去重**：用自研视频表征模型抽 embedding 聚类，近重复簇内只保留质量分最高的一条。
- **分布再平衡**：按主体类别/场景/动作/题材/风格/时长/分辨率/运动特征量化分布，头部类下采样、尾部类上采样并定向补采。

**视频 captioning。**
- **dense caption 风格**，融合动态特征（动作、运镜、变化元素）与静态特征（核心角色/场景外观、美学、风格）。
- caption 模型基于 **Tarsier2** 训练（强视频理解），**冻结视觉编码器、全参微调语言模型**，中英双语数据训练以获双语能力。
- 推理时用上面的 PE 模型把用户 prompt 改写成与训练 caption 同格式的 dense caption。

## 训练方法
**训练目标。** **Flow matching + velocity prediction**；训练 timestep 采样自 logit-normal 分布，并做**分辨率感知的 shift**——分辨率越高、时长越长，加的噪声扰动越大。

**多阶段训练管线：**
1. **Pre-Training（渐进式）**：先用低分辨率 256px 文生图充分训练初始化 → 阶段1 图-视频联合训练（256px 图 + 3~12 秒、12 fps 视频）→ 阶段2 提分辨率到 640px（时长不变）→ 阶段3 上 24 fps 视频提升流畅度。视频预训练期保留少量 T2I 维持语义对齐，并把 I2V 任务占比设为 **20%** 以激活视觉提示遵循能力。
2. **Continue Training（CT）**：把 I2V 占比从 20% 提到 **40%**，并精挑更高美学、更丰富运动的子集（用美学打分器 + 基于光流的运动评估器）。设计两种 caption：原始长 caption（动静态都描述）与短 caption（去掉首帧对应的静态描述、只描动态），强化与训练目标的语义对齐。GPU 数略少于预训练，用退火学习率。
3. **SFT（监督微调）**：在「人工核验 caption」的高质量视频-文本对上对齐人类偏好（视觉质量 + 运动连贯）。定义数百个类别（按风格/运动类型等）定向采数。**Model Merging（模型合并）**：在不同精选子集上分别训多个专长模型，再合并成一个综合模型；各模型用更小学习率、有限 GPU、early stopping 防过拟合。
4. **RLHF（人类反馈对齐）**——视频专用 RLHF：
   - **反馈数据**：从训练集和线上用户收集 prompt，去重去歧义；收集多源（含模型不同阶段产物）视频对做人工偏好标注，采用**多维标注**（在某维度选最好/最差，并保证最好的在其它维度不劣于最差的）。
   - **三个专门奖励模型**：① Foundational RM（VLM 架构，管图文对齐与结构稳定）② Motion RM（减运动伪影、增运动幅度与生动度）③ Aesthetic RM（从图像空间输入、用视频关键帧，借鉴 Seedream）。
   - **Base Model 反馈学习**：模拟视频推理管线，当 RM 能充分评估时直接预测 x0（干净视频），**直接最大化多个 RM 的复合奖励**。论文称对比 DPO/PPO/GRPO，这种 reward maximization 最高效有效；并在扩散模型与 RM 间做**多轮迭代学习**抬高 RLHF 上界，比动态更新 RM 更稳定可控。
   - **Super-Resolution RLHF**：对 diffusion refiner 也做 RLHF（LR 潜空间表示作条件、HR 输出由多 RM 评估、直接最大化奖励线性组合），且**直接作用在已加速的 refiner** 上，在低 NFE 下也能提升运动质量与视觉保真。

**蒸馏与加速（多阶段蒸馏框架）：**
- **TSCD（Trajectory Segmented Consistency Distillation，源自 HyperSD）**：把去噪轨迹分段、跨段强制预测态与目标态一致，使学生模型用更少步逼近扩散过程——DiT 在 **4× 加速**下仍有竞争力。
- **Score Distillation（源自 RayFlow）**：用期望噪声一致性把学生预测的噪声（score function）对齐教师，支持逐样本的轨迹级优化，低 NFE 下更稳更自适应、减伪影。
- **对抗训练（扩展自 APT 到多步蒸馏）**：引入人类偏好数据监督，学一个判别器引导学生产出人类偏好的输出，缓解激进加速带来的伪影、提升感知真实感。
- 最终蒸馏模型在 prompt 对齐、运动质量、视觉保真、源图一致性四个专家维度上与原模型相当。

## Infra（训练 / 推理工程）
**训练 infra（千卡级）：**
- **高性能 kernel**：torch.compile + 手写 CUDA kernel，把 RoPE、归一化等 memory-bound 算子融成单 kernel，中间结果存寄存器/共享内存，**全局内存流量降低 90%+**。
- **混合并行**：数据并行 + 序列并行——用 **HSDP（Hybrid Sharded Data Parallelism）** 做显存高效权重分片并缓解超千卡的扩展性退化；序列并行 follow **Ulysses**（沿 sequence 与 head 维分片）。
- **MLAC（多级激活检查点）**：异步缓存/预取最大化内存传输与前反向计算的 overlap，优先 offload 重算成本最高算子（attention、MLP 的 FC2）的输出张量，并 offload 激活检查点模块的输入张量做到 GPU 激活近零占用，从而可降低序列并行度、减通信开销。
- **运行时感知负载均衡**：异质数据（长/短视频、不同分辨率）造成 GPU 间计算不均，用额外 all-to-all 在每个 batch 内均衡负载（后台异步预计算，不阻塞主循环）。
- **多级容错**：周期性 checkpoint（支持 FSDP 分片权重、保存 dataloader 状态做 bitwise 精确恢复）+ 启动前机器健康检查剔除慢/坏节点 + PyTorch meta tensor 初始化减少模型初始化开销。
- **后训练 infra**：针对 RL/蒸馏阶段「显存争用（Text Encoder/DiT/VAE/RM 共享）+ 训练态混杂（可训/冻结并存）+ 长短视频负载多变」三难题，自研动态显存管理（CPU offloading + 重算 + 局部静态显存规划减碎片），并用 FSDP + 序列并行多节点扩展；细节包括设 `TORCH_NCCL_AVOID_RECORD_STREAMS=1`、手动管 `free_event_queue`、用 `register_post_backward_reshard_only_hook` 调整冻结模式下显存分配/释放顺序。

**推理 infra：**
- **VAE 优化**：profiling 发现靠近像素空间的解码阶段主导延迟，**收窄这些阶段的通道宽度**得「thin VAE decoder」，固定 encoder 重训，端到端 **2× 加速无质量损失**。
- **高性能 kernel 融合**：核心模块大量 kernel fusion，吞吐累计 **+15%**。
- **量化与稀疏**：基于 Seedream 方案，对 Attention/Gemm 做细粒度混合精度量化；发现 DiT 稀疏性呈层级与块状结构，扩展 **AdaSpa** 做精简调优 + 注意力量化。
- **并行策略**：自适应混合并行切长序列，引入 context parallelism 把通信开销降到 Ulysses 的 **1/4**，并引入 **FP8 通信**进一步降端到端通信开销。
- **Async Offloading**：自适应异步 offload，把大模型部署到显存受限设备上**性能损失 < 2%**。
- **分布式 VAE 混合并行** + PE 侧的 continuous batching / prefix caching / 长视频编码加速。
- 综合效果：1080p 5 秒视频 **41.4 秒**（NVIDIA-L20）生成，端到端比未蒸馏 **>10×** 加速且无性能退化。

## 评测 benchmark（把效果讲清楚）
来源：技术报告（arXiv 2506.09113）+ 官方项目页。注：报告中绝大多数定量结果以**雷达图/柱状图/Elo 折线图**呈现，正文给出的精确数字有限，以下严格只列正文与官方页文字明确给出的数字；图中数值不臆造。

**第三方公开众测 — Artificial Analysis Video Arena（Elo）：**
- 数据截至 **2025-06-09 11:00 (GMT+8)** / 排名时间 **2025-06-10**。
- Seedance 1.0 在 **T2V 与 I2V 双榜同时登顶**（单一统一模型）；竞品含 Veo 3、Kling 2.0、Runway Gen4、OpenAI Sora、Wan 2.1。
- **I2V 任务上较第二、三名（Veo 3、Kling 2.0）领先 100+ Elo 分**。（因 Kling 2.1 公开数据缺失，其 Elo 用 Kling 2.0 代替。）
- 注：正文未给出 Seedance 自身的具体 Elo 数值（在 Figure 1/9 中）。

**内部 SeedVideoBench-1.0（自建基准）：**
- T2V、I2V **各 300 条 prompt**，覆盖特效、电商、PGC 等真实场景；与电影导演专家共建评测标准。
- 评测分类法含 Subject / Subject Description / Action / Action Description / Camera（含环形跟拍、推镜、希区柯克变焦、横摇、跟随等专业运镜）/ Aesthetic（T2V 6 大类；I2V 类似并加首帧标注系统）。
- 四大核心评测维度：Motion Quality（结构准确/运动合理/运动稳定/运动生动）、Prompt Following、Aesthetic Quality、Preservation（I2V 专属：主体/风格/材质/内容/色光一致性）。
- 两套协议：**Absolute Score**（5 分 Likert）+ **GSB（Good-Same-Bad，成对比较）**。
- 对比模型：T2V 对 Kling 2.1(Master)/Veo 3/Wan 2.1/Sora；I2V 把 Sora 换成 Runway Gen4。
- 结论（文字定性，分数在图中）：T2V 上 Seedance 1.0、Kling 2.1、Veo 3 显著领先其余；Kling 2.1 运动与画质强但指令遵循弱、拖累总分；Veo 3 写实强但运动质量较弱限制复杂合成；Seedance 1.0 与 Veo 3 在指令遵循上领先，是其登顶主因。I2V 上 Seedance 1.0 与 Kling 2.1 整体强；Veo 3 在保持参考图（光照/纹理）方面较弱且有油腻/模糊问题；**Seedance 1.0 运动质量比肩 Kling 2.1，且在复杂转场/详细指令场景的指令遵循更优，总体更佳**。

**消融/对比结论（正文文字）：** RLHF 阶段用「直接最大化多 RM 复合奖励」对比 DPO/PPO/GRPO 最高效有效；多轮 RM-扩散迭代学习比动态更新 RM 更稳。TSCD 4× 加速仍具竞争力。

> 报告**未报告** FID / CLIPScore / VBench / GenEval 等公开自动指标的具体数值，主要以人评（Absolute/GSB）+ 第三方 Elo 为准。

## 创新点与影响
**核心贡献：**
1. **统一单模型双任务双语 + 原生多镜头**：用「通道维拼接 + 二值 mask」统一 T2I/T2V/I2V，用 Multishot MM-RoPE + 交错序列原生支持多镜头叙事（主体/风格/氛围跨镜头一致）——区别于「T2V、I2V 各擅一域」的前作，单模型双榜登顶。
2. **高效架构**：解耦时空层 + 时间层窗口注意力，显著降训/推开销；C=48、(4,16,16) 高压缩 VAE 去 DiT 侧 patchify。
3. **视频专用多维奖励 RLHF**：三专门 RM（Foundational/Motion/Aesthetic）+ 直接奖励最大化 + 多轮迭代 + 对加速后 refiner 也做 SR-RLHF。
4. **多阶段蒸馏 + 系统优化达 10× 端到端加速**：TSCD + Score Distillation(RayFlow) + 多步对抗蒸馏(APT)，1080p/5s 仅 41.4s（L20）。

**影响：** 落地豆包、即梦、火山引擎（`Doubao-Seedance-1.0-pro`），把「商用级视频生成」的速度门槛压到数十秒量级，并以单模型统一 T2V/I2V + 多镜头叙事，成为后续 Seedance 系（项目页已见 Seedance 2.0）的基座；其「解耦时空 MMDiT + 视频 RLHF + 多阶段蒸馏」组合是 2025 年中商用视频基座的代表性配方之一。

**已知局限（据报告语境）：** 总参数量、训练数据规模、具体 GPU 卡数、Elo 绝对值等关键工程数字**未公开**；评测以人评 + 第三方 Elo 为主，缺公开自动指标（FID/VBench 等）可复现数值；base 仅 480p、靠 refiner 级联到 1080p。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2506.09113
- arxiv_pdf: https://arxiv.org/pdf/2506.09113
- project_page（官方）: https://seed.bytedance.com/seedance
- 产品入口: 豆包 https://www.doubao.com/chat/create-video ; 即梦 https://jimeng.jianying.com/ai-tool/video/generate ; 火山引擎（Model ID: Doubao-Seedance-1.0-pro）

## 本地落盘文件
- ../../../sources/omni/2025/arxiv-2506.09113.pdf （技术报告原文 PDF，9 页，精读）
- ../../../sources/omni/2025/arxiv-2506.09113.txt （PDF 提取全文）
- ../../../sources/omni/2025/seedance-1-0--project.md （官方项目页快照，cloakbrowser 抓取）
