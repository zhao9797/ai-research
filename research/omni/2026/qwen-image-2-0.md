---
title: "Qwen-Image-2.0 Technical Report"
org: Alibaba Qwen
country: China
date: "2026-05"
type: tech-report
category: unified
tags: [qwen, mmdit, qwen3-vl, vae, rectified-flow, image-editing, text-rendering, rlhf, grpo, dmd-distillation, unified-generation]
url: https://arxiv.org/abs/2605.10730
arxiv: https://arxiv.org/abs/2605.10730
pdf_url: https://arxiv.org/pdf/2605.10730
github_url: https://github.com/QwenLM/Qwen-Image
hf_url: https://huggingface.co/Qwen/Qwen-Image
modelscope_url: https://modelscope.cn/models/Qwen/Qwen-Image
project_url: https://qwen.ai/blog?id=qwen-image-2.0
downloaded:
  - arxiv-2605.10730.pdf
  - qwen-image-2-0--readme.md
  - qwen-image-2-0--blog.md
created: 2026-06-25
updated: 2026-06-25
release_date: "2026-02-10"
---

## 一句话定位
Qwen-Image-2.0 是阿里通义把"高保真文生图 + 精确指令编辑"统一进单一框架的全能图像基础模型——以冻结的 **Qwen3-VL** 作条件编码器、**MMDiT** 作去噪主干、**16× 高压缩 VAE（f16c64）** 作 tokenizer，支持 **1K-token 指令的超长/多语种文字渲染**（直出 PPT/海报/信息图/漫画）与 **原生 2K 写实生成**；在 LMArena T2I 盲测 ELO=**1168**，全球第 9、中文模型第 1，且超过 Nano Banana。

## 背景与定位
图像生成已从早期 [[latent-diffusion-ldm]] 经 [[dit]] 演进到"VLM 作条件编码器 + DiT 主干"的范式（[[qwen-image]]、[[hunyuanimage-3-0]]、Seedream 系列等）。报告指出，真实创作流仍存在五大瓶颈：**超长文字渲染脆弱**（字数一多就字形失真、漏字、版面崩溃）、**多语种排版欠发达**（多数模型只训中英文字形）、**高分辨率写实退化**（2K 以上出现纹理重复、光照不连贯）、**复杂指令跟随差**（多实体/空间/组合逻辑下漏概念、幻觉），以及**推理成本高**。更根本的是——很少有系统能在**同一个模型、不切换 pipeline** 的前提下同时做好"生成 + 编辑、写实 + 文字"。

Qwen-Image-2.0 正是 Qwen-Image 两条支线（生图支线 [[qwen-image]] 2025-08 → Qwen-Image-2512 2025-12；编辑支线 [[qwen-image-edit]] 2025-08 → Edit-2509 2025-09 → Layered 2025-12 → Edit-2511 2025-12）的合流：把 T2I 与 TI2I（图生图/编辑）统一到一个 omni 模型里，并宣称同时在两个任务上拿到理想结果。模型与官方博客于 **2026-02-10** 发布（blog header / 发展历程时间轴）；frontmatter 的 `date: 2026-05` 指 arXiv 技术报告提交月（arXiv:2605.10730v1, 11 May 2026），二者非同一时点。相对前代主打"更专业的文字渲染、更细腻的真实质感、更强的语义遵循、更轻量的模型架构（更小更快）"。

## 模型架构
整体是 **MMDiT 架构**（沿用 [[sd3]] 的 MMDiT 范式），由三个紧耦合组件构成：

1. **条件编码器 = Qwen3-VL（冻结）**。给定视觉输入 x 与文本输入 y，Qwen3-VL 先编码为模态感知表征 h_x、h_y；随后视觉表征 h_x 被 VAE 提取的 latent E_x **替换**，与文本表征拼接成统一序列 `h = Concat(E_x, h_y)` 送入 DiT。这一设计让模型既借用 Qwen3-VL 的强多模态理解/世界知识，又保留生成所需的灵活性，并天然支持交错的多图输入（多图编辑/参考生成）。
2. **VAE（高压缩 tokenizer）**。详见"数据/训练"下方专述，f16c64，16× 空间下采样。
3. **MMDiT 主干**。文本与图像 token 在共享 transformer 里联合建模，× L 个 Qwen-Image-2.0 Block 堆叠。

**MMDiT 关键设计**：
- **位置编码 MSRoPE**（来自 [[qwen-image]]）：对文本与图像 token 做统一的跨模态联合位置计算。
- **纯乘性调制（bias-free modulation）**：去掉调制的偏置项，用 `h' = αh`（而非常规仿射 `h' = αh + β`），α 为标量调制参数。
- **QK-Norm 用 RMSNorm**，其余归一化层用 LayerNorm。
- **MLP 用 SwiGLU**：作者观察到文本-图像联合训练会诱发**过大的激活幅度**导致神经元过早饱和（massive activations），引入 SwiGLU `h = Φ1(x) ⊗ σ(Φ2(x))` 缓解，提升表达力与训练稳定性。

**VAE（f16c64，重点创新）**：开源 VAE 通常 8× 压缩，本作用 **16× 压缩**进一步加速 DiT 训练。高压缩 VAE 面临"压缩率 / 重建保真 / 可扩散性（diffusability）"三难。对策：
- **残差自编码器**（residual autoencoder，参考 DC-AE）：用非参数化 shortcut 连接保留细粒度空间细节；
- **latent 通道增至 64**（f16c64，与标准 f8c16 保持同等总通道瓶颈，从而在更高压缩下仍能高保真重建）；
- **语义对齐损失**（follow VA-VAE）：在重建+感知损失之外，把 latent 空间与广域图像集合的语义表征对齐以提升可扩散性。两点观察：**动态语义对齐**很关键（早期强约束建立可扩散 latent，后期逐步放松以平衡重建保真与可扩散性）；**大规模 VAE 训练中对抗损失基本冗余**，故移除 GAN 目标以提升稳定性。
- 专门用大规模**文字密集图像语料**（PDF、PPT、海报 + 合成段落，覆盖英文等字母文字与中文等表意文字）训练以提升文字场景重建。
- 规模：编码器 **79M** / 解码器 **259M** 参数（Table 1）。

**Prompt Enhancer（PE，独立模块）**：把不同详略的用户 query 改写成结构化、细节丰富的 prompt。从 **Qwen3.5-9B** 初始化，两阶段训练（SFT → RL）。数据构造用**逆向工程 pipeline**：把精细标注 P_fine 先用 LLM 分到 General/Portrait/Text/Complex Text 四类，再按预定策略池随机"退化"成口语化短 prompt P_short，同时记录逆向推理链 CoT，得到三元组 (P_short, CoT, P_fine) 作监督；编辑任务则用 MLLM 把长标注摘要成简洁编辑指令。RL 阶段用 [[grpo]]：PE 生成候选增强 prompt 喂给冻结的图像生成器，用 MLLM 视觉一致性 + MLLM 美学 + 规则文本约束的组合奖励优化。

**参数量/分辨率策略**：官方主打"更小模型、更快速度"；**报告正文与博客正文均未给出 MMDiT 主干的确切参数量与算力**（前代 [[qwen-image]] 为 20B MMDiT）。博客头图区有一个"白板"演示 prompt 让模型自渲染其规格——其中写到 `[8B Qwen3-VL Encoder] → [7B Diffusion Decoder]`、"7B Efficiency / single 7B architecture"，但这是**模型生成图里的营销文案，并非权威 spec 表**，应谨慎对待（标注为未正式披露的近似口径）。分辨率上报告正文称"native 2K-resolution support"、训练课程覆盖到 **2048P**（256P→2048P 的分辨率课程，Table 2）；"2048×2048" 的方形具体尺寸仅出现在上述白板营销 prompt 内，报告正文未把它作为权威 spec 给出。

## 数据
**采集（三原则：广域覆盖、强指令质量、可靠源-标一致性）**：
- **T2I**：写实摄影、平面设计、艺术内容、合成图像；写实子集覆盖人像/风景/物体等常见域并保留长尾概念；额外纳入幻灯片/海报/渲染资产等"风格丰富、版面敏感"内容以提升美学/构图/视觉意图可控性。
- **编辑（TI2I）**：单图 + 多图两类。单图含属性修改、背景替换、风格迁移、文字编辑、修复、结构感知操纵；多图聚焦参考生成/编辑、主体一致性、跨图风格迁移、组合融合。

**标注（细粒度 captioning 框架，按任务/图像特性分四类）**：
- **General captions**：任意分辨率/复杂度的全面自然语言描述（含图中文字内容及其语义、多语种、可变长度）；
- **Text captions**：针对密集文字/抽象符号图（PPT、漫画、海报、教材），多套模板专门抽取密集文字、版面结构、视觉符号及语义关系；
- **Knowledge captions**：注入图像相关背景知识/上下文线索，增强语义 + 世界知识；
- **Structured captions**：针对关系图/流程图/示意图等元素多、关系复杂的图，显式建模实体-属性-关系（层级、拓扑、语义交互）。

**多阶段过滤（基于 [[qwen-image]]，6 个顺序阶段，分布随训练持续精炼）**：
- **S1（256P T2I）**：8 道顺序过滤——损坏文件 → 分辨率 → 去重 → NSFW → 旋转校正 → 熵过滤（剔除信息量异常高/低）→ CLIP 图文对齐过滤 → token 长度过滤，建立干净底座。
- **S2（256P T2I+TI2I）**：引入编辑数据，T2I 与 TI2I 合并，统一低分辨率预训练同时学生成 + 编辑。
- **S3（512P）**：升到 512P，引入**合成数据**丰富分布与多样性。
- **S4（512P/1024P）**：混分辨率；为支持 1024P 增加分辨率过滤、图像质量过滤、美学过滤、压缩质量过滤。
- **S5（512P/1024P/2048P）**：扩到多分辨率，2048P 数据加专用分辨率过滤。
- **S6（SFT）**：分布过滤（复用前阶段算子 + 更严阈值）精炼数据分布与样本质量，产出最终高分辨率高保真模型。

**闭环数据飞轮（Data Flywheel，自动化 + 误差归因驱动）**：① 多源信号采集（标准化模型评测 + 定向 bad case 挖掘 + 线上真实 + 训练自评用户反馈）；② **误差归因路由**到三轨——RL 轨（对齐/策略问题→自动奖励策略调整）、预训练轨（缺知识→向量检索引擎诊断数据稀缺并检索泛化 prompt/指令-图对 + 数据增强，唯一人工介入为审核过滤）、PE 轨（能力够但指令理解/prompt 表述差→自动优化 prompt enhancer）；③ 聚合策略/新数据/参数后自动开下一轮训练，checkpoint 回到①，形成"失败发现-定向修复-模型更新"自强化闭环。

具体数据规模、配比绝对量、安全过滤细节大多以定性描述给出，**未披露具体样本量数字**。

## 训练方法
**生成目标**：扩散/流匹配框架（沿 MMDiT 范式，rectified flow 系；报告未单列损失公式但训练超参表给出 uncond. dropout 等 CFG 相关设置）。

**多阶段训练（Table 2，三主阶段）**：
| 阶段 | Steps | 分辨率 | Batch (K) | T2I:TI2I | LR |
|---|---|---|---|---|---|
| Pre-training | **700K** | 256/512 | 32/16 | **0.9 / 0.1** | 1e-4 |
| Continual Pre-training | **250K** | 512/1024/2048 | 16/8/4 | **0.7 / 0.3** | 2e-5 |
| SFT | **10K** | 512/1024/2048 | 16/8/4 | 0.7 / 0.3 | 1e-5 |

优化器全程 Adam，weight decay 0.001，grad norm clip 1.0，uncond. dropout 0.1。预训练学基础语义表征（低分辨率提吞吐）；继续预训练逐步升分辨率（512–2048）抓细节、把编辑占比从 0.1 提到 0.3 强化编辑同时保 T2I；SFT 用严格过滤 + 人工策展的高美学数据、降 LR 提细节同时保世界知识。

**RLHF（偏好对齐）**：构建 5 个任务专属组合奖励模型——
- T2I：**美学奖励**（构图平衡/真实光照/纹理保真/艺术一致）、**图文对齐奖励**（惩罚漏/曲解/违背 prompt）、**人像奖励**（解剖合理、面部比例、身份保持、皮肤/毛发纹理）；
- TI2I：**指令跟随奖励**（替换/风格迁移等编辑是否准确执行）、**视觉一致性奖励**（未修改区域的几何/拓扑/语义严格一致）。
所有奖励校准到可比尺度，权重训练中动态调整避免单维过优化。

优化用改造版 **GRPO**（diffusion RL）。**关键设计——CFG 的混合策略**：rollout 采样时用 CFG 生成高质量候选以获得更可靠奖励信号，但策略优化目标里**排除无条件分支**，既保采样图像保真/结构一致、又省掉优化无条件模型的算力。产物记为 **Qwen-Image-2.0-RL**，在 T2I（纹理保真、整体真实感）与编辑（纹理质量、视觉一致性）上均有一致提升。

**少步蒸馏（Few-step Distillation）**：以 Qwen-Image-2.0-Base 作多步 teacher，用 **DMD（Distribution Matching Distillation）** 蒸成少步 student（选 DMD 因其在异构生成架构上稳定有效）。梯度 `∇_θ ℓ_DMD = E[(s_fake − s_real)∇_θ x_θ]`，其中 s_fake 由在 student 生成样本上以流匹配目标训练的辅助 fake score 模型估计、s_real 由 teacher 在同噪声级给出；x_t = (1−t)x_θ + tξ 线性插值，t 取 logit-normal。结果：**4-NFE student 视觉质量逼近 40 步 teacher**（人像/风景/自然场景跨域），细节、构图、语义对齐基本保持，大幅降推理开销。

## Infra（训练 / 推理工程）
- **训练算力/GPU·时/并行策略/混合精度/吞吐：报告与博客均未披露**（仅给出 steps、batch、分辨率课程等训练超参，见 Table 2）。这是本报告的主要缺口。
- **推理加速**：DMD 蒸馏到 **4 NFE**；官方主打"更小模型、更快速度"（"2K image generation in seconds"，但秒级数字出自博客演示 prompt 而非正式 benchmark）。
- **生态/部署**（来自 GitHub README，多为前代 Qwen-Image/2512/Edit-2511 的 Day-0 支持，可平移参考）：**vLLM-Omni**（长序列并行 + cache 加速 + fast kernels）、**SGLang-Diffusion** Day-0、**Qwen-Image-Lightning / LightX2V**（扩散蒸馏，对 Edit-2511 实现 25× DiT NFE 缩减、整体 42.55× 加速，支持 NVIDIA/海光/沐曦/昇腾/寒武纪多硬件）、**DiffSynth-Studio**（4GB 显存逐层 offload、FP8 量化、LoRA/全量训练）、ComfyUI 原生支持等。Qwen-Image 系列以 **Apache-2.0** 开源（README 明示）。

## 评测 benchmark（把效果讲清楚）
**LMArena T2I 盲测（accessed 2026-04-22）**：用户对同一 prompt 的不同模型输出做匿名两两对比，ELO 排名。Qwen-Image-2.0 **ELO=1168**，**全球第 9、中文模型第 1**，进入第一梯队并**超过 Nano Banana**（[[gemini-2-5-flash-image-nano-banana]] 系列）。Figure 1 显示其在 photorealism、portraits、text rendering、art、product、cartoon、3D modeling 等核心维度相对前代 Qwen-Image/Qwen-Image-2512 均显著提升（各维 ELO 约 1050–1175 区间）。AI Arena（阿里内部 arena）盲测亦显示其作为"生图编辑二合一"模型，**同一模型在 T2I 与图生图基准均取得优越性能**（博客）。

**VAE 重建（Table 1，f16c64 下 SOTA）**：在 ImageNet-256×256 与内部 Text-256×256 两域、PSNR/SSIM 四项全面领先同压缩档对手：
| 模型 | 设置 | Enc/Dec 参数(M) | ImageNet PSNR/SSIM | Text PSNR/SSIM |
|---|---|---|---|---|
| HunyuanImage-3.0 | f16c32 | 389 / 871 | 31.08 / 0.8655 | 29.23 / 0.9521 |
| Wan2.2 | f16c48 | 150 / 555 | 31.30 / 0.8784 | 28.19 / 0.9508 |
| Stepvideo-T2V | f16c64 | 110 / 389 | 31.54 / 0.8973 | 29.62 / 0.9641 |
| **Qwen-Image-2.0** | **f16c64** | **79 / 259** | **33.42 / 0.9225** | **32.81 / 0.9795** |

即在 16× 高压缩下，用**更少参数**拿到比 8× 档某些基线（如 FLUX.1-dev 32.84/0.9155、Qwen-Image 33.42/0.9159）还高或相当的重建质量，文字域 PSNR 32.81 大幅领先所有 16× 对手。

**定性对比（大量 figure，未给数值 benchmark）**：报告用多组对比 figure 展示在**中文/超长/多语种文字渲染、人像写实、复杂海报/PPT/漫画/信息图、单图与多图编辑的身份保持**上优于 GPT-Image-2、NanoBanana Pro、Qwen-Image-2512、Wan2.7 Pro、Seedream 5.0 Lite——典型结论："只有 Qwen-Image-2.0 能在《兰亭集序》全文小楷/40 字古诗上同时保证字符级准确、行序正确、版面协调"；多图编辑保猫的身份+正确执行戴帽/放胡萝卜等。**报告未报告 GenEval / DPG-Bench / T2I-CompBench / GEdit / MJHQ-FID / HPSv2 等标准化数值 benchmark**，效果论证以 LMArena ELO + 大量定性 figure 为主。

**消融/关键结论**：VAE 的动态语义对齐对建立可扩散 latent 关键、对抗损失冗余可去；RLHF 的 CFG 混合策略（rollout 用 CFG、优化排除无条件分支）兼顾保真与省算力；DMD 4-NFE ≈ 40 步 teacher。

## 创新点与影响
**核心贡献**：
1. **真正的 omni 统一**——单模型、不切 pipeline 同时做 T2I 生成与指令编辑，且把文生图侧的文字渲染/真实质感增益**全量平移到编辑**（如可直接在任意图上题诗、保持身份的多图合成）。
2. **f16c64 高压缩残差 VAE + 语义对齐损失 + 去 GAN**，在 16× 压缩下以更少参数拿到 SOTA 重建（尤其文字域），为原生 2K 高效扩散打底。
3. **专业级超长/多语种文字渲染**：1K-token 指令直出 PPT/海报/信息图/漫画，作者归纳为"准、多、美、真、齐"五特性（字符准确、可承载大量文字、版式美观、跨介质真实、自动对齐）。
4. **工程化偏好对齐 + 蒸馏**：5 维任务专属奖励 + CFG 混合 GRPO + DMD 4-NFE，兼顾质量与效率；配套**误差归因驱动的闭环数据飞轮**实现自动化迭代。
5. Qwen3-VL 作冻结条件编码器，把强多模态理解/世界知识直接灌入生成-编辑统一栈。

**影响**：延续 [[qwen-image]] 的开源生态（Apache-2.0、vLLM-Omni/SGLang/Lightning/ComfyUI Day-0），把"VLM 编码器 + MMDiT + 高压缩 VAE"的统一生成-编辑配方进一步标准化；在中文/文字密集创作（PPT、海报、信息图、古诗书法）这一垂类上把开源 SOTA 推到可与闭源（Nano Banana Pro / GPT-Image-2 / Seedream 5.0）正面对话的水平。

**已知局限**：① 报告**未披露 MMDiT 主干参数量、训练算力/GPU·时、并行策略**（"7B/8B"仅见于博客演示 prompt 的营销文案，非正式 spec）；② 缺**标准化数值 benchmark**（GenEval/DPG/CompBench/编辑评测等），效果以 ELO + 定性 figure 为主，可比性受限；③ 数据规模/配比绝对量未给数字；④ 小楷《兰亭集序》仍承认"极个别字"有误，超长文字渲染并非 100% 无错。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2605.10730
- arxiv_pdf: https://arxiv.org/pdf/2605.10730
- github: https://github.com/QwenLM/Qwen-Image
- blog（官方中文，一等公民）: https://qwen.ai/blog?id=qwen-image-2.0
- HuggingFace（系列）: https://huggingface.co/Qwen/Qwen-Image
- ModelScope（系列）: https://modelscope.cn/models/Qwen/Qwen-Image
- Qwen Chat 试用: https://chat.qwen.ai/?inputFeature=t2i

## 本地落盘文件
- ../../../sources/omni/2026/arxiv-2605.10730.pdf
- ../../../sources/omni/2026/qwen-image-2-0--readme.md
- ../../../sources/omni/2026/qwen-image-2-0--blog.md
