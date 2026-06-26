---
title: "Step1X-Edit: A Practical Framework for General Image Editing"
org: "阶跃星辰 StepFun"
country: China
date: "2025-04"
type: tech-report
category: edit
tags: [image-editing, instruction-editing, mllm, dit, flux, qwen2.5-vl, rectified-flow, gedit-bench, open-source]
url: "https://arxiv.org/abs/2504.17761"
arxiv: "https://arxiv.org/abs/2504.17761"
pdf_url: "https://arxiv.org/pdf/2504.17761"
github_url: "https://github.com/stepfun-ai/Step1X-Edit"
hf_url: "https://huggingface.co/stepfun-ai/Step1X-Edit"
modelscope_url: "https://www.modelscope.cn/models/stepfun-ai/Step1X-Edit"
project_url: "https://step1x-edit.github.io/"
downloaded: [arxiv-2504.17761.pdf, step1x-edit--readme.md, step1x-edit--hf-card.md, step1x-edit--project-page.md, step1x-edit--safetensors-header.json]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Step1X-Edit 是阶跃星辰 2025 年 4 月开源的通用指令图像编辑框架，核心创新是「**MLLM 语义理解（Qwen2.5-VL-7B）→ 连接器（token refiner）→ FLUX 系 DiT 扩散解码器**」三段式架构 + 自建千万级数据管线（20M 三元组过滤到 1M HQ），并配套发布真实用户指令评测基准 **GEdit-Bench**。在 GEdit-Bench-EN 全量集上总分（GPT-4.1 评）从 v1.0 的 6.44 提升到 v1.1 的 6.97，逼近闭源 Doubao（6.98）、超越 Gemini2 Flash（6.51），把开源指令编辑与 GPT-4o/Gemini 的差距大幅缩小。

## 背景与定位
2025 年初 GPT-4o 原生图像生成与 Gemini2 Flash 把指令编辑（instruction-based editing）推到「理解 + 高保真生成」一体化的新高度，但闭源不可复现。开源侧 [[omnigen]]、ACE++、AnyEdit、InstructPix2Pix、MagicBrush 等在泛化性、编辑精度、出图质量上仍有明显差距。作者诊断两大瓶颈：

1. **数据**：现有开源编辑数据集（AnyEdit 2.5M、OmniEdit 1.2M、SEED-Data-Edit 3.7M…）要么规模不足、要么质量/多样性不够，难以训出对标 GPT-4o 的模型。
2. **架构耦合太浅**：传统 DiT 用 CLIP/T5 文本编码器，对「微妙 / 组合式」编辑指令理解弱，难以在「忠实原图」与「响应指令」之间平衡；多数方法是任务专用、不支持通用编辑。

Step1X-Edit 的定位是「**实用主义的开源通用编辑框架**」——用 MLLM 取代纯文本编码器做深度多模态理解，用自建高质量数据补齐数据短板，再用一个真实场景基准（GEdit-Bench）来诚实衡量与闭源的差距。技术脉络上承接 [[ddpm]] [[latent-diffusion-ldm]] → DiT（Diffusion Transformer）→ [[flux-1]] 系 MMDiT（DiT 基座即 FLUX.1-dev），训练用 [[rectified-flow]] 目标，并吸收 OminiControl 的 token concatenation 条件注入思想。

## 模型架构
论文 Fig.4/Fig.5 给出三大组件（论文本身**未公布**具体层数/维度/参数量）。本页的层数 / 维度 / 参数量数字非来自论文，而是**实读 HF 权重 `step1x-edit-i1258.safetensors` 的 safetensors header**（通过 HTTP Range 取头部 JSON，落盘为 `sources/omni/2025/step1x-edit--safetensors-header.json`；24GB 权重本体未下载）逐键核对得出。

**1) MLLM（理解）— Qwen2.5-VL-7B**
- 参考图 + 用户编辑指令 + 系统前缀拼成一条输入，**单次前向**通过 Qwen2.5-VL，捕捉指令与视觉内容的语义关系。
- **丢弃 prefix 对应的 token embedding**，只保留与「编辑信息」直接对齐的 token embedding，把语义聚焦到编辑需求上。
- 另对有效 embedding 取 **均值（avg pooling）**，过一层线性投影得到一个**全局引导向量（global guidance vector）**，注入 DiT 做全局条件。
- 权重证据（header 实测）：连接器 `connector.S.c_embedder.linear_1.weight` 形状 **[4096, 3584]**——输入维度 **3584**（正是 Qwen2.5-VL-7B 的 hidden size），输出投影到 **4096**（DiT 的 token 维度）。

**2) Connector（连接器）— Token Refiner**
- 论文称用「token refiner」[32,24] 把 MLLM embedding 重排成更紧凑的多模态特征表示，作为 DiT 的多模态条件输入。header 实测：`connector.S.individual_token_refiner.blocks.*` 共多层，`mlp.fc1.weight` 形状 **[16384, 4096]**（即 token refiner 内部 MLP 隐层 16384）。
- 训练时**只用 diffusion loss 联合优化 connector + DiT**（MLLM 主体冻结/复用），无需 mask loss。

**3) DiT（生成）— FLUX.1-dev 系扩散解码器**
- 经 safetensors header 核实：**19 个 double_blocks（MMDiT 双流块）+ 38 个 single_blocks（单流块）**，与 FLUX.1-dev 架构（19 double + 38 single）一致；整个 `step1x-edit-i1258` 文件（connector + DiT，全 BF16）共 **12,427,800,385 参数 ≈ 12.428B**，文件大小 **24,855,692,578 B ≈ 24.86 GB**（即 ≈2 字节/参数）；VAE（`vae.safetensors`）单独 **335,304,388 B ≈ 0.34 GB**；Qwen2.5-VL-7B 不含在此文件内、另行加载。
- 论文明确：起点是一个 text-to-image 模型以保留美学与视觉一致性，「可被 SD3 / FLUX / HiDream-I1 / Flex 等 T2I 模型轻松替换」；**实际开源权重落在 FLUX.1-dev**。
- **条件注入（关键设计）**：参考图经 VAE 编码 → 线性投影成 reference image tokens →（Fig.5 绿框）与 noise image tokens **沿 token 长度维度 concat**，构成最终视觉输入。作者对比并选择了 **token concatenation**（跟随 OminiControl）而非 FLUX-Fill 的 channel concat、也非 SeedEdit 的额外 causal self-attention——理由是更好平衡「响应编辑指令」与「保留细粒度图像细节」。
- 与 Qwen2VL-FLUX（仍保留 T5）、DreamEngine（仅用 MLLM 特征、丢失参考图细节）相比，Step1X-Edit 既保留跨模态理解、又通过 VAE reference tokens 强化图像细节提取。
- 分辨率策略：支持 512 / 768 / 1024（`size_level` 参数），训练/推理多分辨率。

## 数据
**这是本工作最重的投入之一。** 作者把图像编辑系统化为 **11 类编辑任务**（基于常用编辑指令归纳，部分参考 AnyEdit/ICE-Bench）：Subject Addition、Subject Removal、Subject Replacement、Background Change、Color Alteration、Material Modification、Motion Change、Portrait Beautification、Tone Transformation、Text Modification、Style Transfer。

**规模与过滤比**：
- 从互联网（如 Reddit）爬取多样编辑样例做种子分析。
- 自建数据管线生成 **超过 20M（2000 万）** 「源图 + 指令 + 目标图」三元组。
- 经 Multimodal LLM（自家 **step-1o** [52]）+ 人工标注双重严格过滤，**保留 >1M（约 100 万）高质量三元组**，即 **Step1X-Edit-HQ**（过滤保留比约 20:1）。
- Fig.2 横向对比：原始 20M 超过所有现有编辑数据集（GoT 8.6M、SEED-Data-Edit 3.7M、AnyEdit 2.5M、Senorita 2M、OmniEdit 1.2M…）；过滤后的 1M HQ 子集仍与主流数据集体量相当。
- **子任务分布**（Fig.3）：Subject Add&Remove 21.98%、Subject Replacement 21.98%、Motion Change 13.19%、Text Modification 8.79%、Background Change / Color Alteration / Portrait Beautification 各 6.59%、Tone Transformation / Style Transfer 各 5.49%、Material Modification 3.30%。

**各子任务的合成管线（每类用专门工具链）**：
- **Subject Add/Remove**：Florence-2 标注（检测/分类）→ SAM2 分割 → ObjectRemovalAlpha inpainting；指令由 Step-1o + GPT-4o 生成，人工复核。
- **Subject Replacement / Background Change**：Florence-2 + SAM2 + Qwen2.5-VL + Recognize-Anything 识别目标 → **Flux-Fill** 内容感知重绘；Step-1o 出指令、人工验证。
- **Color / Material Modification**：ZoeDepth 估深度理解几何 → ControlNet + 扩散模型生成保身份、改外观（材质/颜色）。
- **Text Modification**：PPOCR + Step-1o 区分正确/错误文字区域 → 生成指令 → **人工手动修字**收尾。
- **Motion Change**：取 **Koala-36M** 视频帧对 → BiRefNet + RAFT 做前景背景分离与光流，靠「前景流均值 vs 背景流均值范数」筛出仅前景运动的帧对 → GPT-4o 标注动作变化为指令。
- **Portrait Beautification**：公开来源美化对 + 邀请人工修图师真人精修，全程人工校验。
- **Style Transfer**：双向——Ghibli/水墨/3D 动漫风从风格图抽边再 ControlNet 生成写实图；油画/像素风则从写实图出发生成风格图（edge-to-image 管线）。
- **Tone Transformation**：色调/去雾/去雨/季节变换，主要靠算法工具与自动滤镜。

**Caption 策略（标注质量保障）**：
- **冗余增强标注（Redundancy-Enhanced）**：多轮标注，把上一轮结果作为下一轮上下文，递归精炼、抑制 VLM 幻觉、强化确定性信息。
- **上下文示例风格化标注**：给标注者/模型大量风格对齐示例，统一 caption 的语气、结构、粒度。
- **中英双语标注**：所有标注同时给中英文，为多语训练/评测打基础。

## 训练方法
- **训练目标**：**rectified flow（整流流）** 公式下的 diffusion loss（沿用 SD3 的 rectified flow）。**仅用 diffusion loss** 联合优化 connector + 下游 DiT；MLLM 复用预训练 Qwen2.5-VL。
- **无 mask loss trick**：明确区别于 OmniGen，不依赖 mask loss 即可稳定训练；编辑过程不需要任何 mask 输入（统一架构、无 mask 推理）。
- **从 T2I 模型起步**：以预训练 text-to-image 模型（FLUX.1-dev）为初始化，保留美学质量与视觉一致性。
- **关键超参**：学习率固定 **1e−5**，在训练稳定性与收敛速度间取平衡。
- **多版本迭代**（来自 GitHub/HF 官方 News，均为一手）：
  - v1.0（2025-04）：首发。
  - **v1.1（2025-07-09）**：新增 text-to-image 生成能力；编辑质量与指令遵循提升（GEdit-Bench-EN 全量 G_O 6.44→6.97）。
  - **v1.2-preview（2025-09-08）/ v1.2（2025-11-26，论文称 ReasonEdit-S，arXiv:2511.22625）**：原生「推理编辑」模型，**thinking（指令重写推理）+ reflection（反思纠错）**两段机制处理复杂编辑；在 KRIS-Bench / GEdit-Bench 上进一步提升。
- 蒸馏/步数加速：原模型未做步数蒸馏；加速靠推理侧的 TeaCache/RegionE（见 Infra），非训练蒸馏。
- RLHF/DPO/reward model：v1.0–v1.1（本页主体所依据的 arXiv:2504.17761）**未披露**任何偏好对齐/RL/reward model。v1.2/ReasonEdit-S 的 thinking+reflection 机制细节见 ReasonEdit 报告（arXiv:2511.22625，**本页未落盘、未核读**），是否含训练期 RL 本页不下结论。

## Infra（训练 / 推理工程）
- **训练算力规模 / GPU·时 / 并行策略：论文与 README 均未披露**（无 GPU 数量、训练时长、分布式配置）。
- **推理（来自官方 README，均在 H800 上实测，bs=1，含 CFG，28 步）**：

  | 配置 | 峰值显存 (512/768/1024) | 28 步耗时 (512/768/1024) |
  |---|---|---|
  | Step1X-Edit (bf16) | 42.5 / 46.5 / 49.8 GB | 5s / 11s / 22s |
  | FP8 量化 | 31 / 31.5 / 34 GB | 6.8s / 13.5s / 25s |
  | offload | 25.9 / 27.3 / 29.1 GB | 49.6 / 54.1 / 63.2s |
  | FP8 + offload | 18 / 18 / 18 GB | 35 / 40 / 51s |

  官方推荐 80GB 显存 GPU 以获最佳质量与效率。
- **多 GPU 与加速（1024 分辨率，H800）**：
  - **TeaCache**（阈值默认 0.2）：单卡 28 步从 ~22s 降到 16.78s。
  - **xDiT**（序列并行：Ulysses/Ring Attention + CFG Parallelism）：2 卡 12.81s、4 卡 8.17s。
  - TeaCache + xDiT 组合：2 卡 8.94s、4 卡 **5.82s**。
- **社区/官方加速生态**：FP8 权重（meimeilook/rkfg）、ComfyUI 插件、**RegionE**（2025-12，5 行代码、2.5× 加速且无精度损失）、Diffusers 集成（`Step1XEditPipeline`）。
- **微调成本**：LoRA（rank 64、bs 1）显存 bf16 29.7–33.8 GB / fp8 19.8–23.6 GB，**1024 分辨率可在单张 24GB GPU 上 LoRA 微调**；官方放出修动漫手部 LoRA。
- **部署形态**：开源权重（HF/ModelScope）+ 在线 Demo（HF Space）+ Replicate；后续商业化为 StepFun 开放平台的 **Step Image Edit 2**（2026-04，号称 2 秒内完成生成/编辑，轻量实时）。

## 评测 benchmark（把效果讲清楚）

**GEdit-Bench（自建，本工作核心贡献之一）**
- 从互联网（Reddit 等）收集 **>1K 真实用户编辑实例**，人工归入 11 类、去重后保留 **606 个测试样例**，参考图均来自真实场景。
- 与现有开源编辑基准对比（Table 1）：GEdit-Bench 是少数同时满足「真实图 + 真实用户指令 + 人工过滤 + 11 子任务 + 公开」的基准（EditBench/EmuEdit/HQ-Edit 等多为合成指令、子任务少）。
- 每张图配**英文（EN）+ 中文（CN）双语指令**：EN 集闭源+开源都测；CN 集只测支持中文的闭源系统 + Step1X-Edit。
- **隐私去标识协议**：对用户上传图做反向图搜，找视觉相似+语义一致的公开替代图；找不到则系统化改写编辑指令，兼顾伦理与评测有效性。
- **评测指标（VIEScore）**：SQ（语义一致性 Semantic Consistency）、PQ（感知质量 Perceptual Quality）、O（总分），均 0–10。自动评测用 GPT-4.1（记为 G_*）+ 开源 Qwen2.5-VL-72B（记为 Q_*，便于复现）。报两套：Intersection 子集（所有模型都成功返回，EN=434/CN=422 实例）与 Full 全量集（606，仅对成功返回的样本平均；闭源因安全策略拒答的样本剔除）。

**GEdit-Bench-EN（Table 2，G_* 为 GPT-4.1 评，Full set）**

| 模型 | G_SC | G_PQ | **G_O** | Q_O |
|---|---|---|---|---|
| Instruct-Pix2Pix | 3.296 | 6.189 | 3.219 | 4.578 |
| MagicBrush | 4.517 | 6.371 | 4.185 | 5.558 |
| AnyEdit | 3.053 | 5.882 | 2.854 | 3.635 |
| OmniGen | 5.879 | 5.871 | 5.005 | 6.352 |
| **Step1X-Edit (v1.0)** | 7.131 | 6.998 | **6.444** | 7.067 |
| **Step1X-Edit (v1.1)** | 7.658 | 7.354 | **6.969** | 7.346 |
| Gemini2 Flash | 6.866 | 7.436 | 6.509 | 6.971 |
| Doubao | 7.222 | 7.885 | 6.983 | 7.230 |
| GPT-4o | 7.743 | 8.133 | 7.494 | 7.692 |

要点：v1.0 已**大幅超过所有开源基线**（OmniGen 5.00），**超越 Gemini2 Flash（6.51）**；v1.1（6.97）进一步**逼近/持平 Doubao（6.98）**，与 GPT-4o（7.49）仍有约 0.5 分差距。

**GEdit-Bench-CN（Table 3，G_O Full set）**：Step1X-Edit v1.0 = 6.658、v1.1 = 6.983，**超越 Gemini2 Flash（5.14）与 Doubao（6.84）**，处理中文编辑指令时优势更明显（接近 GPT-4o 的 7.30）。

**分子任务雷达（Fig.7，GPT-4o 评）**：Step1X-Edit 在 11 个维度全面超开源；与闭源比，在 **Style Transfer、Color Alteration** 等轴上甚至超过 GPT-4o。

**用户研究（Table 4）**：55 名参与者盲评 4 个模型（Gemini2 Flash / Doubao / GPT-4o / Step1X-Edit），5 级映射 2/4/6/8/10。Full set 用户偏好（UP-Full）：Gemini 6.603、Doubao 5.678、**GPT-4o 7.134、Step1X-Edit 6.939**——Step1X-Edit 主观质量与顶尖闭源相当，仅略低于 GPT-4o（作者注 Gemini 因强身份保持在 IS 子集偏好分偏高）。

**后续版本（HF News，一手；用于纵向参照）**：
- v1.2（base/thinking/thinking+reflection）GEdit-Bench G_O 升到 7.24 / 7.36 / **7.58**，KRIS-Bench Overall 升到 56.33 / 58.64 / **60.93**，已超 Flux-Kontext-dev（49.54）并接近/超过 Qwen-Image-Edit-2509（56.15）。

**消融**：论文正文未给独立消融表；架构层面的对照论证（token concat vs channel concat vs causal attention；无 mask loss vs OmniGen 的 mask loss）以设计讨论形式给出，未量化。

## 创新点与影响
**核心贡献**
1. **三段式 MLLM→connector→DiT 架构**：用 Qwen2.5-VL-7B 做深度多模态理解（而非 CLIP/T5 浅层文本编码），token refiner 桥接 + 全局引导向量，VAE reference token 经 **token concatenation** 注入 FLUX DiT，在「忠实原图 / 响应指令」间取得好平衡；统一架构、**推理无需任何 mask**。
2. **千万级编辑数据管线 + 11 类任务体系**：20M 合成、20:1 严格过滤到 1M HQ，每类任务专门工具链（Florence-2/SAM2/Flux-Fill/ControlNet/Koala-36M/RAFT…）+ 冗余增强中英双语标注，是开源编辑数据工程的重要范本。
3. **GEdit-Bench**：基于真实 Reddit 用户指令、含去标识协议、中英双语、VIEScore（GPT-4.1 + Qwen2.5-VL-72B 双评）的 606 样例基准，已成为后续编辑工作（Qwen-Image-Edit、Flux-Kontext 等）的常用对照。

**影响**
- 把开源指令编辑首次拉到「对标 Gemini2 Flash / Doubao、逼近 GPT-4o」的水平，且**模型权重 + 数据管线方法 + 评测基准全开源**，被社区快速生态化（ComfyUI / FP8 / xDiT / TeaCache / RegionE / 单卡 LoRA）。
- 「MLLM 理解 + DiT 生成」的解耦范式成为 2025 年开源编辑的主流路线之一；GEdit-Bench 成为事实标准评测。
- 自身演进出 v1.1（加 T2I）、v1.2/ReasonEdit-S（原生推理编辑 thinking+reflection）、以及商业化的 Step Image Edit 2。

**已知局限**
- 与 GPT-4o 在英文综合分上仍有约 0.5 分差距；用户研究中身份保持（identity preservation）不及 Gemini。
- **训练算力/GPU·时/分布式配置完全未披露**；论文无量化消融表，部分架构选择仅以设计讨论佐证。
- 推理较重：bf16 1024 分辨率峰值 ~50GB 显存、单卡 28 步 ~22s，需 80GB GPU 才好用（后续靠 FP8/xDiT/TeaCache/RegionE 与 Step Image Edit 2 缓解）。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2504.17761
- arxiv_pdf: https://arxiv.org/pdf/2504.17761 （v5, 2025-07-31）
- github: https://github.com/stepfun-ai/Step1X-Edit
- hf_model: https://huggingface.co/stepfun-ai/Step1X-Edit
- hf_dataset(GEdit-Bench): https://huggingface.co/datasets/stepfun-ai/GEdit-Bench
- modelscope: https://www.modelscope.cn/models/stepfun-ai/Step1X-Edit
- project_page: https://step1x-edit.github.io/
- 后续(ReasonEdit/v1.2): https://arxiv.org/abs/2511.22625

## 一手源存档（sources/）
- [arxiv-2504.17761.pdf](https://arxiv.org/pdf/2504.17761) （技术报告全文 PDF，gitignore 不入 git，本地已精读）
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/step1x-edit--readme.md) （GitHub README 快照，含 infra/推理/版本迭代）
- [hf-card.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/step1x-edit--hf-card.md) （HF model card 快照）
- [project-page.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/step1x-edit--project-page.md) （项目主页快照，含 EN/CN/Bagel leaderboard 与 user study 全表）
- [safetensors-header.json](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/step1x-edit--safetensors-header.json) （HF 权重 `step1x-edit-i1258.safetensors` 的 safetensors header 解析结果：块数/连接器维度/参数量/文件大小，本页架构数字的一手依据；24GB 权重本体未下载）
