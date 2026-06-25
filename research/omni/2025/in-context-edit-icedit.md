---
title: "ICEdit：用 In-Context 生成范式做指令图像编辑（Enabling Instructional Image Editing with In-Context Generation in Large-Scale DiT）"
org: "浙江大学 ReLER/CCAI · 哈佛 DBMI/HMS"
country: China
date: "2025-04"
type: paper
category: edit
tags: [image-editing, instruction-editing, in-context, flux-fill, lora, moe, inference-time-scaling, dit, rectified-flow, neurips2025]
url: "https://arxiv.org/abs/2504.20690"
arxiv: "https://arxiv.org/abs/2504.20690"
pdf_url: "https://arxiv.org/pdf/2504.20690"
github_url: "https://github.com/River-Zhang/ICEdit"
hf_url: "https://huggingface.co/sanaka87/ICEdit-MoE-LoRA"
modelscope_url: ""
project_url: "https://river-zhang.github.io/ICEdit-gh-pages/"
downloaded: [arxiv-2504.20690.pdf, arxiv-2504.20690.txt, in-context-edit-icedit--readme.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
ICEdit 把指令图像编辑改写成一个 **"双拼图（diptych）in-context 生成"** 问题——直接复用大规模 DiT（FLUX.1 Fill）的固有理解与生成先验，仅用 **5 万训练对（前 SOTA 的 0.1%~0.5%）+ 一组 LoRA-MoE（≈2亿可训参数，前 SOTA 的 1%）** 就拿到指令编辑 SOTA-comparable 效果，VIE-Score 78.2 反超商用 SeedEdit 的 75.7；NeurIPS 2025 接收，全开源（含 ComfyUI、4GB 显存可跑）。

## 背景与定位
指令编辑（"把背景换成夏威夷"这类自然语言改图）此前卡在一个 **精度-效率二选一**：
- **微调派**（InstructPix2Pix / MagicBrush / Emu Edit / UltraEdit / OmniEdit-FluxEdit / ACE++）：靠在大规模编辑对上**全量微调**+改结构（条件嵌入 / 通道扩展 / 接 MLLM），精度高但数据贵到离谱——InstructP2P 45万对、UltraEdit 300万、Emu Edit ~1000万、ACE++ 5400万编辑对（总 7亿样本）。
- **训练-free 派**（SDEdit / Prompt-to-Prompt / MasaCtrl / RF-Solver / StableFlow / FlowEdit）：靠图像反演 + 注意力操控，省训练但**指令理解弱**、要精心调 prompt、改不动复杂指令。

ICEdit 的切入点：近年 DiT（[[latent-diffusion-ldm]] 之后的 [[flux-1-kontext]] 同源 FLUX、SD3、PixArt）有两个被低估的性质——(1) **可扩展的生成保真度**（FLUX 在海量图文上训练，T2I 对齐极强）；(2) **固有上下文感知**：DiT 的双向注意力天然能让"参考内容"和"生成内容"在同一序列里互相看到（这正是 In-Context LoRA、OminiControl、IP-preserve 编辑等工作的基础）。作者的核心追问是：**能不能不加任何外部模块、不大改结构，直接榨出 DiT 的生成力 + 上下文感知来做指令编辑，同时打破精度-效率权衡？**

作者先做了诊断实验，发现裸用 DiT 编辑有两个硬伤：(1) **指令理解差**——模型能读懂"描述型 prompt"，但读不懂"make it… / change it…"这种祈使指令；(2) **布局不稳**——重绘时常把不该动的区域也改了。ICEdit 的两步解法直接对症：把祈使指令**包装成描述型 in-context prompt**；用**极轻量微调**补上 DiT 缺失的"图到图编辑先验"。

## 模型架构
**Backbone：FLUX.1 Fill（12B rectified-flow DiT inpainting 模型，冻结）**。FLUX/FLUX-Fill 是混合架构（multimodal DiT block + parallel DiT block），文本 token `C_T` 与图像 token `X` 拼接后过 Multi-Modal Attention（MMA，带 RoPE）做双向注意力；text encoder 为 **T5**（论文 limitation 明确点名 T5 语义消歧弱）；图像走 VAE 编码进 latent，基于 **flow matching** 训练。

ICEdit 把编辑形式化为 `I_t = E(I_s, T_e) = D(I_IC, M, T_IC)`：
- **D** = 冻结的 inpainting DiT（FLUX.1 Fill）；
- **I_IC** = 把源图 `I_s` 放左半、右半留空，拼成 512×1024 的**双拼图（diptych）**；
- **M** = 固定二值 mask（左侧重建源图、右侧待生成）；
- **T_IC** = 固定格式 **in-context 编辑 prompt**：
  `"A diptych with two side-by-side images of the same scene. On the right, the scene is exactly the same as on the left but {instruction}."`

**两套 training-free 框架（先探路，再二选一）：**
1. **T2I-DiT 版**（基于 FLUX.1 dev）：对源图做 inversion，沿层/步保留 attention 的 value 特征，注入到 diptych 左半 token 做重建，右半按 IC prompt 生成。缺点：需耗时 inversion，且易在 ID/布局上有瑕疵。
2. **Inpainting-DiT 版**（基于 FLUX.1 Fill）：直接喂"左源图 + 右空白 + 固定 mask + IC prompt"，**无需 inversion**，操作最简单。

→ 因为 inpainting 版不用反演、便于继续微调，**最终选 inpainting 框架做主力**。

**关键架构创新——LoRA-MoE（Mixture of LoRAs）**：单一 LoRA 难以同时handle风格迁移、物体移除等需要不同 latent 操作的任务。于是在 MM-attention block 的 **output projection 层** 并联 N 个 LoRA 专家，其余模块用标准 LoRA：
```
Output = BaseLayer(x) + (α/r) · Σ_i G(x)_i · B_i · A_i · x
G(x)_i = softmax(TopK(g(x), k))_i
```
路由器是**单层线性**，按 visual token + text embedding 选专家，**稀疏 Top-k**。最终配置：**4 个专家、rank=32、TopK=1**，可训参数约 **214M（≈0.2B）**。作者发现路由天然均衡，**未加 load-balancing loss**。

**关键设计要点**：全程不引入额外位置/条件编码器，不retrain backbone，纯靠"双拼图结构 + DiT 自身处理能力"——这是它相对 OminiControl / In-Context LoRA / ACE++ 等需要专门 condition/PE 设计的简化。

## 数据
**极小、且故意不精洗**——这正是卖点：
- **总计 50K（实际 53,047）样本**，全部来自公开数据集：
  - **MagicBrush 9K**
  - **OmniEdit 随机抽 40K**（补 MagicBrush 在编辑类型平衡、风格类数据、域多样性上的不足）
- **任务类型分布**（Table 4）：移除 13,272 / 增加 11,938 / 替换 5,823 / 属性修改 11,484 / 风格 10,530。
- **明确声明未严格清洗**（附录 fig.11 展示仍含若干低质样本），作者认为认真 curation + 更高质数据还能继续涨。
- README 补充：base 模型 FLUX 风格覆盖有限，故数据中**风格迁移占比大**；数据**以写实图为主**，对动漫/模糊图成功率掉；**移除任务因移除数据集质量低、成功率相对最低**。

数据效率曲线（fig.18）：10K 即大幅超 training-free，50K→70K 几乎不再涨（该配置下已收敛）。

## 训练方法
- **训练目标**：沿用 FLUX 的 flow matching / rectified-flow 重建损失——最小化模型预测与 GT 编辑结果之间的 reconstruction loss（在 inpainting 框架下对右半区域生成）。
- **PEFT 微调**：backbone 全冻，只训 **LoRA-MoE（4 专家 r=32）+ 其余模块标准 LoRA（r=32）**，所有 LoRA α = rank。**无额外 load-balancing loss**。
- **优化器/超参**：**Prodigy**（无学习率、自适应；开 safeguard warmup + bias correction），weight decay 0.01；batch size=1 + 梯度累积 2 → 有效 batch=2（README 口径：2×2×4GPU=16）；输入 resize 到 **512×512** 再拼成 **512×1024 diptych**；为兼顾速度/显存，**512 分辨率下不开 gradient checkpointing** 训练。
- **三阶段消融贡献（Table 3a，GPT-score）**：
  - training-free 直接喂指令 0.14 → 套 **IC prompt** 升到 0.24（GPT-score 相对 +71%，纯靠 prompt 改写、零训练；注：此为 GPT-4o 编辑评分的相对增幅，非论文给出的"成功率"指标）；
  - 再微调（IC prompt + LoRA）大幅提升，**MoE 比标准 LoRA 再 +13% GPT-score 且参数更少**；
  - 完整方法（IC prompt + LoRA-MoE，214M）→ **GPT 0.68**；去掉 IC prompt 掉到 0.62（证明 IC prompt 在微调后仍有效）。
- **无蒸馏/无步数蒸馏/无 RLHF/DPO**——加速完全靠下面的"早过滤推理时缩放"，不改权重。

**Early Filter Inference-Time Scaling（推理时缩放，方法亮点之一）**：
观察到 (1) 初始噪声显著左右编辑结果（有的种子更合人类偏好）；(2) rectified-flow DiT 下**编辑是否成功在前几步就能看出来**。于是：采样 **M 个初始噪声 → 每个只跑 m 步（m≪n）预览 → 用 VLM 对早期结果做 bubble-sort 式两两比较选最优种子 → 该种子再跑满 n 步出图**。实测配置：**6 个噪声 × 10 早期步 + Qwen2.5-VL-72B（API）评判**，总步数 n=50、guidance scale=50。效果：**SC 分 +19%、整体 VIE-Score +16%**；消融（Table 3b）显示 6 噪声/10 步性价比最佳（NFE=110），用 CLIP 当 verifier 反而掉分（CLIP 不对齐人类偏好）。

## Infra（训练 / 推理工程）
- **训练算力**：**4× A800(80G)，训练约 1 天**（极轻）。
- **推理**：单卡 **A100(40G)**；端到端约 **9 秒/图**（README）。
- **训练显存**（开 gradient checkpointing，bs=1）：512² → 37GB，768² → 39GB，1024² → 42GB；不开 checkpointing：512² 60GB、768² 77GB、1024² OOM。
- **推理显存与部署形态**（社区生态，README）：原生约 35GB（编辑 512×768）；加 `--enable-model-cpu-offload` 降到 24GB（可跑 RTX 3090）；GGUF 量化（FLUX.1-Fill-dev-gguf + T5 gguf）**10GB**；ComfyUI-nunchaku 量化最低 **4GB VRAM**；Windows 一键包量化后 14GB、支持 50 系显卡；昇腾 NPU 移植版亦有。
- **约束**：模型**只能编辑宽=512 的图**（高度不限，否则自动 resize 到 512 宽）。
- 已并入 ComfyUI Comfy Registry，官方 workflow 内置了 diptych 预提示词 + 高分辨率 refine。

## 评测 benchmark（把效果讲清楚）
两大基准：**Emu Edit test**（无 GT，用 CLIP-I/CLIP-Out/DINO + GPT-4o）与 **MagicBrush test**（有 GT，算 L1/CLIP-I/DINO）。对比时**所有模型用单一默认噪声**（关掉 ICEdit 的推理缩放以求公平）。

**Emu Edit test（Table 1）**——ICEdit 基于 FLUX.1 Fill，可训参数 0.2B、数据 0.05M：
| 方法 | base | 训参 | 数据 | CLIP-I↑ | CLIP-Out↑ | DINO↑ | GPT↑ |
|---|---|---|---|---|---|---|---|
| InstructP2P | SD1.5 | 0.9B | 0.45M | 0.856 | 0.292 | 0.773 | 0.36 |
| MagicBrush | SD1.5 | 0.9B | 0.47M | 0.877 | 0.298 | 0.807 | 0.48 |
| EmuEdit（闭源） | — | — | 10M | 0.877 | 0.306 | 0.844 | **0.72** |
| UltraEdit | SD3 | 2.8B | 3M | 0.880 | 0.304 | 0.847 | 0.54 |
| FluxEdit | Flux.1 dev | 12B | 1.2M | 0.852 | 0.282 | 0.760 | 0.22 |
| FLUX.1 Fill（裸） | Flux.1 Fill | — | — | 0.794 | 0.273 | 0.659 | 0.24 |
| RF-Solver Edit* | Flux.1 dev | — | — | 0.797 | 0.309 | 0.683 | 0.32 |
| ACE++ | Flux.1 Fill | 2.5B | 54M | 0.791 | 0.280 | 0.687 | 0.24 |
| **ICEdit（ours）** | Flux.1 Fill | **0.2B** | **0.05M** | **0.907** | 0.305 | **0.866** | **0.68** |

→ ICEdit 的 **CLIP-I(0.907)/DINO(0.866) 全场最高**（最好地保留非编辑区），GPT-score 0.68 **超所有开源模型**、逼平闭源 Emu Edit(0.72) 但只用其 **0.5% 数据**。(*RF-Solver 用了 output caption，故 CLIP-Out 偏高。)

**MagicBrush test（Table 2，越接近 GT 越好）**：ICEdit **L1=0.060 / CLIP-I=0.928 / DINO=0.853 全部第一**，优于 MagicBrush(0.074/0.908/0.847)、UltraEdit(0.066/0.904/0.852)，远超 FluxEdit、裸 FLUX.1 Fill、ACE++。

**VIE-Score（人类偏好对齐，对标商用，fig.8）**：用 GPT-4o 算 SC（指令遵从+非编辑区保持）× PQ（视觉质量）的 √ 几何均。随机种子下接近商用 **SeedEdit(豆包)**；**开启推理时缩放后整体 VIE-Score 78.2 反超 SeedEdit 75.7**。SeedEdit 因输出更"精修"PQ 略高，但在非编辑区 ID 保持上弱于 ICEdit。

**关键消融数字**：
- **IC prompt**：training-free 下 GPT-score 0.14→0.24（相对 +71%，纯 prompt 改写零训练）。
- **LoRA-MoE vs 标准 LoRA**：GPT **+13%**，且只在 output-proj 层加 MoE（"Only MoE"）会掉分，说明全模块微调更优。
- **MoE 配置**（Table 5）：专家 1→4 / rank 8→32 显著涨（GPT 0.59→0.68）；再加到 6/8 专家不再涨反而参数膨胀（路由变难）。
- **推理时缩放**（Table 3b）：6 噪声×10 步 GPT 0.78（NFE 110）性价比最佳；CLIP 当 verifier 掉到 0.65。
- README 对比 GPT-4o/Gemini 商用：在 **角色 ID 保持 + 指令遵从** 上可比甚至更优，且更开源、更便宜、约 9 秒/图。

## 创新点与影响
**核心贡献：**
1. **In-context 编辑范式**：首次系统证明无需改结构/重训，靠"diptych + 固定描述型 IC prompt"就能把大规模 DiT 的生成力与上下文感知直接转化为指令编辑能力——一句 prompt 改写（祈使→描述）就带来 GPT-score 0.14→0.24（相对 +71%）的显著提升。
2. **LoRA-MoE 极致 PEFT**：4 专家 r=32、214M 可训参数、5万数据、4×A800 训一天，达到 SOTA-comparable，把指令编辑的训练成本压到前 SOTA 的 **0.1%~0.5% 数据、1% 参数**。
3. **Early Filter Inference-Time Scaling**：利用 rectified-flow"早几步即可判成败"的特性，VLM 早过滤优选种子，低 NFE 拿到 +16% VIE-Score，是 test-time compute 在编辑场景的实用化样板。

**影响**：作为"**Image Editing is worth a single LoRA**"的代表作，证明了**生成基座足够强时，编辑可退化为轻量适配 + prompt 工程**，给后续 FLUX-Kontext、Step1x-Edit、Qwen-Image-Edit 等"统一编辑"方向提供了 in-context 范式参照；工程上 4GB 可跑 + ComfyUI 生态使其在开源社区迅速流行（HF Space 周榜第 2）。NeurIPS 2025 接收。

**已知局限**：
1. **物体移动类指令**（"把椅子挪到角落"）易失败——通用编辑数据缺少运动类样本；
2. **语义消歧弱**——T5 对多义词（computer mouse vs animal mouse）易混，需未来接 MLLM；
3. **推理缩放依赖 Qwen-VL-72B**（7B VLM 常误判质量），有效率代价（可用蒸馏 7B VLM 缓解）；
4. 风格易被 FLUX 自身偏好带偏、对动漫/模糊图成功率下降、移除任务成功率相对最低（数据质量所致）；当前仅支持 512 宽，更高分辨率 LoRA 仍在 TODO。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2504.20690
- arxiv_pdf: https://arxiv.org/pdf/2504.20690
- github: https://github.com/River-Zhang/ICEdit
- project_page: https://river-zhang.github.io/ICEdit-gh-pages/
- hf_model (MoE-LoRA): https://huggingface.co/sanaka87/ICEdit-MoE-LoRA
- hf_model (normal-LoRA): https://huggingface.co/RiverZ/normal-lora
- hf_demo: https://huggingface.co/spaces/RiverZ/ICEdit

## 本地落盘文件
- ../../../sources/omni/2025/arxiv-2504.20690.pdf
- ../../../sources/omni/2025/arxiv-2504.20690.txt
- ../../../sources/omni/2025/in-context-edit-icedit--readme.md
