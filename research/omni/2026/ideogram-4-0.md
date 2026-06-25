---
title: "Ideogram 4.0"
org: Ideogram
country: US
date: "2026-06"
type: blog
category: t2i
tags: [t2i, open-weight, dit, single-stream, flow-matching, qwen3-vl, json-prompt, text-rendering, bounding-box]
url: "https://ideogram.ai/blog/ideogram-4.0/"
arxiv: ""
pdf_url: ""
github_url: "https://github.com/ideogram-oss/ideogram4"
hf_url: "https://huggingface.co/collections/ideogram-ai/ideogram-4"
modelscope_url: ""
project_url: "https://ideogram.ai/"
downloaded: [ideogram-4-0--blog.md, ideogram-4-0--github-readme.md, ideogram-4-0--hf-modelcard.md, ideogram-4-0--docs-model_architecture.md, ideogram-4-0--docs-pipeline.md, ideogram-4-0--docs-inference.md, ideogram-4-0--docs-safety.md, ideogram-4-0--docs-prompting.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Ideogram 4.0 是 Ideogram 的**首个开放权重文生图基础模型**——一个 9.3B 参数、从零训练的**全单流（fully single-stream）Diffusion Transformer**，最大的两点差异化是：用**视觉语言模型 Qwen3-VL-8B-Instruct 当 text encoder**（取 13 个中间层 hidden state 拼接），以及**只用结构化 JSON caption 训练/推理**（带逐元素样式、bounding box、调色板）。在设计师盲评 ELO（4366 票）里以 1062 分位列**总榜第 2、开源第 1**（仅次于 GPT Image 2 的 1141），在 9.3B 这个参数量下做出了所有已发布开源模型中最强的图内文字渲染（X-Omni EN OCR 0.97）。

## 背景与定位
Ideogram 此前的旗舰（Ideogram 3.0 等）均为闭源 API 产品；4.0 是其**第一次把基础模型权重公开**（HF 上 gated 但可申请），定位是"缩小闭源前沿与开源差距、并在设计向生成上站到前沿"。它瞄准的是 2025–2026 这一波开源文生图竞赛：[[flux-2-klein]]（FLUX.2 系，32B dev）、[[qwen-image]]（20B）、HunyuanImage 3.0（80B MoE，~13B active）、Z-Image（6.15B）、HiDream-O1（17B）等。

技术脉络上它建立在几条成熟线索之上：DiT（[[dit]] Peebles & Xie 2023）骨架、潜空间扩散（[[latent-diffusion-ldm]] Rombach 2022）的 KL-VAE、flow matching / rectified flow（Lipman 2023、Liu 2023、Esser SD3 2024）训练目标。官方明确指出"近期开源工作已收敛到**文+图 token 单一自注意力序列**"（点名 HunyuanImage 3.0 / Z-Image / HiDream-O1），4.0 follow 同一范式（单流 34 层 DiT），但用**两点设计**把自己与同侪区分开：
1. **text encoder 用 VLM 而非纯文本编码器**——既不是 CLIP/T5 那样取单一 hidden state，也不是某些工作完全不用外部 encoder，而是从 Qwen3-VL 的 13 个中间层各取 hidden state 拼接。
2. **JSON-only 训练**——每条训练 caption 用结构化 JSON 穷举式描述图中每个元素（含 per-element style、可选 bbox 与调色板），训练与推理共用同一格式。注：blog 措辞称推理 pipeline "按 JSON schema 校验、不解析就拒绝"，但 docs-prompting 明确把口径放软——**遵循 schema 并非硬约束，纯文本 prompt 也能跑**，`CaptionVerifier` 对未知键/缺必填键/键序错只**发 warning 而非拒绝**（偏离 schema 等于在训练分布外采样、质量打折）。

定位概括：**小而强**——9.3B 在开源里属"小盘"，却把设计/排版/文字渲染做到了贴近闭源前沿，主打 graphic design 场景（海报、版式、多行多字体图内文字、bbox 布局、调色板控制）。

## 模型架构
官方 model_architecture / pipeline 文档把方法讲得很透，逐项拆解：

**四组件流水线**（仅 DiT 可训练，text encoder 与 VAE 均冻结）：
1. **Text encoder（冻结）：Qwen3-VL-8B-Instruct，text-only 模式**（不喂视觉输入）。用 Qwen3 chat template 分词，过 36 层 transformer，从**第 0,3,6,9,12,15,18,21,24,27,30,33,35 层共 13 个层**抽 hidden state，沿特征维拼接，输出 `(B, L_text, hidden_dim×13)`。理由：早层编码表层 token 信息、晚层编码深层语义，拼接给 DiT 提供多尺度文本表征。这是它与"取单一 hidden slice"的对照点。
2. **DiT backbone（可训练，9.3B）：Ideogram4Transformer**，34 层。**全单流**——文本 token（Qwen3-VL 特征）与图像 latent token 拼成一条序列，过同一组 self-attention，无独立的文/图分支，每层都做跨模态深度交互。
3. **Sampler（运行时）**：Euler flow-matching + **非对称 CFG** + logit-normal noise schedule。
4. **VAE decoder（冻结）：KL autoencoder**（官方流水线图标注为 Flux VAE），8× 空间压缩，把 latent 解到 RGB。

**单 block 内部**（`Ideogram4TransformerBlock`）：
- **Self-attention**：带 **QK-RMSNorm**（Dehghani ViT-22B 同款 QK norm，稳训练）+ **3D Multimodal RoPE（MRoPE）**——文本 token 用 1D 位置广播到 3 轴，图像 token 用 (temporal, height, width) 坐标，使文/图在统一位置空间共存；正因如此，prompt 里的 **bbox 能被模型通过共享 MRoPE 位置空间真正"honor"**。`mrope_section=(24,20,20)`，`rope_theta=5_000_000`。
- **SwiGLU MLP**（Shazeer GLU 变体，SiLU 门控），`intermediate=12288`。
- **AdaLN**：由 flow-matching 时间步 embedding 生成 per-block scale/gate，调制 attention 与 MLP 残差路径，`adaln_dim=512`。

**Model spec（官方表，逐字）**：参数 9.3B；`emb_dim=4608`；`num_layers=34`；`num_heads=18`；`intermediate=12288`（SwiGLU）；`adaln_dim=512`；`rope_theta=5e6`；`mrope_section=(24,20,20)`；**latent channels = 32×2²=128**（VAE 32 通道 + DiT 2×2 patch 再 ×4）；max text tokens=2048；分辨率 256–2048 px/边（须 16 整数倍，长宽比可达 6:1 / 1:6）；量化 nf4 与 fp8；sampler 为 Euler flow-matching + 非对称 CFG。

**潜空间/patch 细节**：VAE 提供每轴 8× 压缩，DiT 内 2×2 patch 再 ×2，所以 1024×1024 图 → 64×64 latent token 网格、每 token 128 通道。

**条件注入方式**：文本以"序列前缀 token"形式进入（拼在 image latent 之前，序列布局 `[text tokens (≤2048) | image latent tokens (grid_h×grid_w)]`），时间步以 AdaLN 注入，bbox/调色板/typed-text 这些控制信号则全部承载在 JSON caption 的文本 token 里、经 MRoPE 位置空间落到具体区域。

## 数据
官方对训练数据的**规模/总图文对数/配比/来源未披露**（无公开数字）。可确证的数据相关方法只有两条，且都是创新点：

- **结构化 JSON caption（唯一训练 caption 形式）**：模型**只在结构化 JSON caption 上训练**。每条 caption 用 `high_level_description` + `style_description`（aesthetics / lighting / photo 或 art_style / medium / color_palette）+ `compositional_deconstruction`（background + elements[]）穷举描述图中所有元素；每个 element 是 `obj` 或 `text` 类型，可带 `bbox`（`[y_min,x_min,y_max,x_max]`，0–1000 归一化，原点左上）与可选 `color_palette`（整图最多 16 个 hex、每元素最多 5 个）；`text` 元素额外携带要渲染的**字面字符串**与独立的样式描述（这是多行/多字体图内文字的机制）。官方解释 JSON-only 的理由：训练与推理共用单一格式；caption 越把"文-图关系"钉死，每个训练对能榨出的**有 grounding 的监督信号就越多**，而不必跨大量稀疏标注样本去推断这些关系（对应参考文献 [21] "Generating an Image From 1,000 Words: Enhancing Text-to-Image With Structured Captions", 2025）。
- **安全/NSFW 预训练过滤**：训练前先用**多类别 NSFW 分类器过滤整个图像数据集**，过滤后的分布才作为预训练输入，目的是让 base 分布不含明确不想复现的内容。

来源、采集方式、合成数据占比、美学打分、re-captioning 的具体管线、训练对总量——**均未披露**。

## 训练方法
- **训练目标：flow matching**。DiT 预测速度场 `v(z_t, t)`，定义从纯噪声到干净 latent 的 ODE（`dz/dt = v`）。推理用 Euler 反向积分（`z_{t-dt}=z_t+v·dt`）。
- **noise schedule：logit-normal**（Esser SD3 同源），由 `(mu, std)` 参数化；mu 越大越偏向高噪声步（高分辨率更需要）。**按分辨率自动调整**：`mu_adjusted = mu_base + 0.5·log(num_pixels / (512·512))`，因此**单套权重覆盖 256 px 缩略图到 2K 横幅**，无需为不同分辨率训练专门模型。
- **从零训练**：官方反复强调是 **trained from scratch**，不是任何已有 checkpoint 的 fine-tune 或蒸馏。
- **后训练安全 mitigation**：预训练后再做 post-training，进一步降低生成 NSFW 概率（**包括对明确请求 NSFW 的 prompt**）。具体后训练方法（是否有 SFT / 偏好对齐 / RLHF / DPO / reward model）**未披露**——文档只提到"post-training procedures designed to further reduce NSFW probability"，未给训练细节。
- **关键 trick：非对称 CFG（asymmetric classifier-free guidance）**。无条件分支**不是把文本替换成 padding，而是整段丢弃文本 token**，让无条件 pass 只在 image token 上跑——既省算（短序列），又能让条件/无条件两支**独立调参**，从而在采样轨迹上**分别调度 prompt 遵从度与图像质量**。
- **采样轨迹整形（polish tail）**：guidance weight 逐步可变。`V4_QUALITY_48` = 前 45 步 `gw=7` + 末 3 步 `gw=3`（near t=0 的"polish"步），收紧细节而不过饱和全局；`V4_DEFAULT_20` 与 `V4_TURBO_12` 同形，分别 2 步、1 步 polish。
- **蒸馏/步数蒸馏**：未提及任何 consistency/LCM/ADD 蒸馏；加速靠**预设步数（48/20/12）+ 非对称 CFG**，不是蒸馏。
- 训练超参（batch、lr、token 数、训练步数、训练算力）**全部未披露**。

## Infra（训练 / 推理工程）
**训练 infra 未披露**——无 GPU 数量、GPU·时、并行/分布式方案、混合精度策略、吞吐等任何数字。

**推理工程（有较多细节）**：
- **采样预设**（步数 / CFG 调度 / mu / std）：`V4_QUALITY_48`（48 步，45@gw7+3@gw3，mu=0.0，std=1.5，默认）；`V4_DEFAULT_20`（20 步，18@gw7+2@gw3，mu=0.0，std=1.75）；`V4_TURBO_12`（12 步，11@gw7+1@gw3，mu=0.5，std=1.75）。
- **量化部署**：发布 **nf4 与 fp8 两种权重**；**nf4 变体可塞进单张 24 GB GPU**（fp8 "All hardware"、nf4 仅 CUDA / Diffusers 支持）。两个 checkpoint 都是 9.3B。
- **Diffusers 集成**：`Ideogram4Pipeline` / `DiffusionPipeline.from_pretrained("ideogram-ai/ideogram-4-fp8")`，bf16。
- **默认参数**：height/width 1024（16 整数倍，256–2048，长宽比 ≤6:1）；num_steps 48；guidance_scale 7.0；mu 0.5；std 1.0。
- **magic prompt（推理前置）**：普通文本 prompt 由一个 "magic prompt" LLM 改写成结构化 JSON caption；默认走 Ideogram 托管的免费 magic-prompt API（服务端展开，读 `IDEOGRAM_API_KEY`，注：该托管展开**与 Ideogram.ai 产品里用的 magic prompt 不是同一个**，结果会有差异）。也可换成自己的 LLM provider——仓库另开源两套 system prompt（`claude-opus-v1` / `claude-sonnet-v1`，经 OpenRouter 调 Claude，读 `MAGIC_PROMPT_API_KEY`；官方仅用 **Claude Opus** 测过这条路）。
- **安全推理过滤**：参考 pipeline 通过 **Hive** 做 prompt + output 双重审核（`HIVE_TEXT_MODERATION_KEY` / `HIVE_VISUAL_MODERATION_KEY`），并**要求任何再分发/托管必须保留等价或更强的过滤**，否则不属支持的部署配置。被拦的 NSFW prompt 返回一张写有 "Image blocked by safety filter" 的灰屏；官方自承**非 JSON 形式 prompt 的误判（false positive）率更高**，留待后续 checkpoint 改进。
- 推理吞吐/单图延迟的绝对数字未给（仅以步数差体现速度档位）。

## 评测 benchmark（把效果讲清楚）
官方在五大能力上对标最强闭源（GPT Image 2、Nano Banana 2 = Gemini 3.1 Flash Image Preview）与所有领先开源模型。数字均来自已抓取的官方博客 / model card：

**标准开源 benchmark（绝对分，0–1，越大越好）**：
- **Layout control（7Bench mIoU）= 0.69**——生成物体落在请求 bbox 内的紧密度；官方称此项**显著优于所有闭源模型**。
- **Text rendering（X-Omni 英文 OCR 准确率）= 0.97**——图内文字 OCR 正确率。
- **Spatial reasoning（SpatialGenEval 准确率）= 0.76**——空间关系 + 基础物体两类问题合并。
- **Prompt alignment（Prism-bench alignment track）= 0.89**——长/组合 prompt 的遵从度。
- 注：SpatialGenEval 改用 `gemini-2.5-flash` 当 judge（而非排行榜默认的 Qwen2.5-VL-72B），但对所有模型统一施加，跨模型可比。雷达图五轴（layout / spatial reasoning / object fidelity / prompt alignment / text rendering）对比 Ideogram 3.0、Nano Banana 2、GPT Image 2，结论是"在每个轴上追平闭源、面积更大更均衡"。雷达图（Figure 2）整体带一个 *With Magic Prompt ON* 脚注（blog 清洗文本里该脚注紧跟在五轴映射说明之后，未精确锁定到单一轴）。

**参数效率（X-Omni EN OCR vs 参数量）**：Ideogram 4.0（9.3B 0.97）**独占"小而强"角落**，在文字渲染上领先所有其他开源发布模型——对照 Z-Image Base（6.15B）、HiDream-O1（17B）、Qwen-Image（20B）、FLUX.2 [dev]（32B）、HunyuanImage v3（80B MoE，~13B active/token）。官方原话："9.3B 参数下做出任何已 benchmark 的开源发布中最好的文字渲染，领先 Qwen-Image(20B)、FLUX.2[dev](32B)、HunyuanImage 3.0(80B MoE) 等大得多的模型。"

**第三方竞技场（model card 披露）**：
- **Design Arena**（专注设计向生成的第三方 ELO 榜）：总榜上是**排名第一的开源模型**，仅落后于 GPT 与 Gemini 系闭源；仅看开源时**大幅领先次优开源模型**。
- **ContraLabs 盲评排版评测**（10 位 Contra 顶尖职业设计师评判）：Ideogram 4 以 **47.9% 首选率**（四选一被选为最佳的占比）居首，远高于 Nano Banana 2 的 30.0%、FLUX.2 [max] 15.5%、Grok Imagine 1.0 15.0%；"是否会用于真实客户工作"评分 **3.55/5** 居首，高于 Nano Banana 2（2.84）、Grok Imagine 1.0（2.61）、FLUX.2 [max]（2.49）。
- **LMArena**（通用文生图第三方榜）：是**排名最高的开源 lab、总体 top-5 image generation lab**，只被预算/资源大得多的巨头击败。

**Ideogram 内部人评（设计师盲评）**：
- **内部人偏好 benchmark（聚焦平面设计与摄影，Bradley-Terry 评分）**：排**总榜第 2**（仅次于 GPT Image 2 medium）、**开源第 1**。
- **设计师偏好 ELO（博客 Figure 4）**：9 条 pipeline、**4366 张图、graphic-designer 盲投**（不告知模型来源）的 pairwise ELO 排名：#1 GPT Image 2(闭源) **1141** > #2 **Ideogram 4.0(开源) 1062** > #3 Nano Banana 2(闭源) 1004 > #4 Grok Imagine(2K) 990 > #5 Luma 1.1(2K) 983 > #6 FLUX.2 Pro 982 > #7 HunyuanImage v3(开源) 978 > #8 Krea v2 Large 959 > #9 FLUX.2 [dev](开源) 900。即**总榜第 2、开源第 1**，每条 bar 标注 95% CI。

**未报告项**：FID、CLIPScore、GenEval（原始）、T2I-CompBench、MJHQ-30K、HPSv2、ImageReward、PickScore、编辑评测（GEdit/MagicBrush，4.0 为纯 t2i 无编辑）等经典指标官方均**未报告**；消融实验（如 13 层 vs 单层 hidden state、JSON vs 纯文本训练、对称 vs 非对称 CFG 的定量对比）**未公开数字**。

## 创新点与影响
**核心贡献**：
1. **Ideogram 首个开放权重基础模型**——把过去闭源 API 才有的设计向生成能力以可下载权重释放（HF gated + 非商用许可），缩小开源与闭源前沿差距。
2. **VLM 当 text encoder + 多层 hidden state 拼接**：用 Qwen3-VL-8B-Instruct（而非 CLIP/T5）并取 13 个中间层拼接，提供从表层到深层语义的多尺度文本表征——这是它相对同侪单流 DiT 的关键差异。
3. **JSON-only 结构化 caption 范式**：训练/推理统一用穷举式结构化 JSON，原生支持 bbox 布局（0–1000 归一化）、整图/逐元素调色板（≤16/≤5 hex）、typed-text 元素（字面串 + 样式分离）——把"可控性"（构图/光照/配色/排版/空间）做到单 prompt 内，并以 magic-prompt LLM 把普通文本自动展开成 JSON，降低使用门槛。
4. **非对称 CFG**：无条件分支整段丢弃文本 token（只跑 image token），既省算又能让两支独立调度 prompt 遵从度与画质，配合 polish-tail 步数调度。
5. **小盘高效**：9.3B 做到开源最强图内文字渲染（X-Omni 0.97）与设计盲评开源第 1，nf4 单张 24 GB 可跑。

**影响**：把"JSON 结构化 caption + VLM encoder + 单流 DiT"这一组合摆上开源台面，为后续可控生成、版式/排版生成、agentic 设计流水线提供了可二次开发的强 baseline；其"小参数 + 强文字/排版"路线对参数军备竞赛是一种对照。

**已知局限**：
- 纯 **t2i**，无图像编辑/inpainting/角色一致性等能力（这些在 Ideogram 产品里以 3.0 等其它能力提供）。
- 训练侧透明度有限：数据规模/来源/配比、训练算力与超参、后训练对齐方法**均未披露**，可复现性受限。
- 权重 **gated** 且 **非商用许可（Ideogram 4 Non-Commercial）**——"open-weight"但非自由商用。
- 强依赖结构化 JSON：纯文本 prompt 能用但效果打折，最佳效果需 JSON 或 magic-prompt 展开。
- 安全过滤为外部 Hive API，且官方要求再分发须保留等价过滤，部署有外部依赖与合规约束。

## 原始链接
- blog (technical details): https://ideogram.ai/blog/ideogram-4.0/
- blog (news alias, 403 未能直接抓取): https://ideogram.ai/news/ideogram-4.0/
- github (code/inference/docs): https://github.com/ideogram-oss/ideogram4
- hf collection: https://huggingface.co/collections/ideogram-ai/ideogram-4
- hf model (fp8): https://huggingface.co/ideogram-ai/ideogram-4-fp8
- hf model (nf4): https://huggingface.co/ideogram-ai/ideogram-4-nf4
- text encoder: https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct
- API: https://developer.ideogram.ai/

## 本地落盘文件
- ../../../sources/omni/2026/ideogram-4-0--blog.md （技术博客全文清洗版，含 model spec 表 / benchmark 数字 / JSON prompt 示例 / 21 条参考文献）
- ../../../sources/omni/2026/ideogram-4-0--github-readme.md （GitHub README：Model Zoo / Performance / Model Summary 架构要点 / Quick Start / Citation）
- ../../../sources/omni/2026/ideogram-4-0--hf-modelcard.md （HF fp8 model card 渲染文本：Design Arena / ContraLabs / LMArena / 内部 Bradley-Terry 评测）
- ../../../sources/omni/2026/ideogram-4-0--docs-model_architecture.md （DiT spec 表 + 架构图）
- ../../../sources/omni/2026/ideogram-4-0--docs-pipeline.md （四组件流水线深度说明：13 层抽取、flow matching、logit-normal、非对称 CFG、VAE patch）
- ../../../sources/omni/2026/ideogram-4-0--docs-inference.md （采样预设 / 参数 / 分辨率表）
- ../../../sources/omni/2026/ideogram-4-0--docs-safety.md （预训练/后训练/Hive 推理三层安全）
- ../../../sources/omni/2026/ideogram-4-0--docs-prompting.md （JSON caption schema：color_palette / bbox 0–1000 / text 元素字段）
