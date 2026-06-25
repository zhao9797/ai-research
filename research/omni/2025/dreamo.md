---
title: "DreamO: A Unified Framework for Image Customization"
org: ByteDance
country: China
date: "2025-04"
type: paper
category: edit
tags: [image-customization, dit, flux, lora, subject-driven, identity, try-on, style, feature-routing, unified]
url: "https://arxiv.org/abs/2504.16915"
arxiv: "https://arxiv.org/abs/2504.16915"
pdf_url: "https://arxiv.org/pdf/2504.16915"
github_url: "https://github.com/bytedance/DreamO"
hf_url: "https://huggingface.co/ByteDance/DreamO"
modelscope_url: ""
project_url: "https://mc-e.github.io/project/DreamO"
downloaded: [arxiv-2504.16915.pdf, dreamo--readme.md, dreamo--v1.1.md, dreamo--hf-modelcard.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
DreamO 是字节跳动 Intelligent Creation Team 基于 [[flux-1]]（FLUX.1-dev）的**统一图像定制框架**：只训练一组 LoRA（约 478M 参数），用「**特征路由约束（feature routing constraint）+ 占位符（placeholder）策略 + 三阶段渐进训练**」把主体（subject/IP）、人脸身份（ID）、虚拟试穿（try-on）、风格（style）四类定制任务以及它们的多条件组合塞进**单一模型**，在 DreamBench、Unsplash-50、VITON-HD 等基准上 subject/ID/try-on 一致性与文本对齐均优于 OmniGen、OminiControl、PuLID、MS-Diffusion 等同期方法（如单主体 CLIP-sim 0.9150 / DINO-sim 0.8056、人脸 Face-sim 0.607）。已被 SIGGRAPH Asia 2025 接收。

## 背景与定位
图像定制（image customization）要让生成结果在**特定属性**上与参考图保持一致——身份、主体外观、虚拟试穿、风格等。此前工作几乎都是**单任务专用**：[[ip-adapter]] 系（IP-Adapter）走 cross-attention 注入、InstantID/PuLID 专攻人脸、StyleShot/InstantStyle 专攻风格、MagicClothing/IMAGDressing 专攻试穿。问题是无法把不同条件**自由组合**，做一个统一框架仍是开放难题。

DreamO 的技术脉络承接 DiT 时代的统一可控生成路线：
- **OminiControl**（Tan et al. 2024）：把 text/image/condition token 沿序列维拼接喂进 DiT，训 task-specific LoRA——但**分任务单独训练**，处理多条件吃力。DreamO 沿用其「统一序列条件 + 对角非重叠位置编码 + LoRA」的范式。
- **OmniGen**（Xiao et al. 2024）：基于大语言模型（Phi-3）做通用生成；**UniReal**（Chen et al. 2024）：视频生成预训练 + 全模型后训练。

DreamO 的核心论点（也是其立场）：**高质量、多概念的图像定制不能只靠 LLM 或视频模型的通用能力（如 OmniGen / UniReal）堆出来，而需要专门的架构设计**。它的差异化贡献正是这套「routing 约束 + placeholder + 渐进训练」的专用设计，且**只在冻结的预训练 DiT 上训少量 LoRA 参数**，训练成本低。相关前置工作：[[latent-diffusion-ldm]]、[[dit-scalable-diffusion-transformers]]、[[ddpm]]、[[ip-adapter]]、[[controlnet]]。路由思想直接借鉴 UniPortrait、AnyStory（同组/同领域的 cross-attention 区域约束工作）。

## 模型架构
**Backbone：MMDiT（FLUX.1-dev）冻结 + LoRA。** 不改 backbone 权重，只插入 LoRA（rank=128，总增参 **478M**）。

**统一序列条件（unified sequence conditioning）。** 给定 n 张条件图 C={C₁,…,Cₙ}：
- 复用 FLUX 的 **VAE** 把每张条件图编码到与噪声 latent 相同的 latent 空间（条件图分辨率可变——细节丰富的用高分辨率保真，细节少的用低分辨率省压缩成本）。
- 把 image token、text token、condition token **沿序列维全部拼接**后送入 FLUX。
- 在 FLUX 输入端加一个 **condition mapping layer**（条件映射层）来接纳条件输入。
- 条件 token 的位置编码用 **RoPE**，与噪声 latent 对齐，并仿照 OminiControl 的 non-overlapping PE **沿对角线扩展**（避免条件与生成区位置重叠）。
- 额外引入一个**可训练、按 index 区分的 Condition Embedding（CE）∈ ℝ^{10×c}**，直接加到条件 token 上——用来区分不同条件槽位（最多 10 路），消融显示去掉 CE 会掉一致性。

**Text encoder：** 沿用 FLUX 自带的文本编码器（FLUX 用 T5-XXL + CLIP，论文未额外改动文本侧）。

**两类路由约束（routing constraint）——本文方法核心：**
1. **图到图路由约束（image-to-image）。** DiT 内部条件图 token（Q_cond,i）与噪声图 latent token（K_img）天然存在 cross-attention M = Q_cond,i·K_imgᵀ/√d。把这个 dense 相似度沿条件维平均，得到条件图在生成结果各位置的**全局响应图** M∈ℝ^l。用 **MSE loss** 把该响应图约束到目标主体的 mask（M_target）上（按条件 index 和层 index 双重求和）。效果：让 image-to-image 注意力聚焦到正确主体上 → 提升参考一致性，并在多参考时**解耦不同条件**（防止两个主体特征串味）。
2. **占位符到图路由约束（placeholder-to-image）。** 为第 i 个条件在 prompt 里实例名后追加占位符 `[ref#i]`，如 "A woman from [ref#1] and a woman from [ref#2]…"。训练中用 softmax(Q_cond,i·K_text,iᵀ) 与二值矩阵 B_i 做 MSE：**让 Cᵢ 与 [ref#i] 的相似度为 1、与其它占位符为 0**。效果：占位符能精确绑定到指定参考对象，实现多主体时**按文本位置指定谁放哪**（README 的 multi-condition 能力即源于此）。为兼容无占位符的普通文本输入，训练时以 **50% 概率**用普通文本并丢弃 placeholder loss。

**总损失：** L = λ_diff·L_diff + λ_route·L_route + λ_holder·L_holder（flow-matching 速度回归损失 + 两个路由约束，损失权重未在正文给出具体数值）。两个路由约束几乎不增训练开销（**2.5s/iter vs 3s/iter**）。

**分辨率：** 推理输出 1024×1024；参考图默认缩放到 512×512（v1.1 提示：细节/文字多的参考可调高分辨率以保细节，但增推理时间、降可编辑性）。

## 数据
论文按任务分别构造**大规模训练数据**（均为合成 / 半合成管线，强调廉价可扩展）：

- **身份配对数据（Identity）：** 高质量人脸配对数据难从网上爬，故用开源 ID 定制方法 **PuLID** 构造——用 PuLID-FLUX 生成同一身份的两张图互为参考；再用 PuLID-SDXL（给参考脸 + 风格 prompt）产出风格化训练对。最终 **15 万张写实人脸 + 6 万张风格化身份数据**。
- **主体驱动数据（Subject/IP）：** 用 **Subject200K**（OminiControl 出品，由 FLUX 生成、与基模分布相近）作为部分训练数据；为补人物相关条件，**检索收集 10 万张人物相关配对数据**；多主体场景通过在 Subject200K 上**双列拼接**构造，并引入 **X2I-subject**（OmniGen 出品）数据集。为强化人物驱动，仿 **Movie Gen** 搭管线：长视频 → 内容感知场景检测切短片 → **Mask2Former** 生成人物 mask 并做目标跟踪 → 跨片段实例匹配用 **SigLIP** embedding + 聚类。
- **试穿数据（Try-on）：** 两路来源——(1) 直接从 Web 爬取的「模特+服装」配对；(2) 爬高质量模特图作 GT，再用图像分割（SSSegmentation / IDRNet）抠出服装生成配对。全部**人工过滤**去低质样本，最终 **50 万试穿对**。
- **风格数据（Style）：** 处理两类风格迁移——(1) 风格参考 + 文本描述内容：用内部基于 SDXL 的风格定制模型，对两条不同 prompt 生成**同风格不同内容**的图；(2) 风格参考 + 内容参考图：在类型 1 基础上，用 **Canny-guided FLUX** 为每张风格图产出内容参考。
- **路由 mask 标签：** 用 **LISA**（LLM 驱动的推理分割）按文本描述抠出条件物体 mask 作为 routing 约束（Eq.3）标签；复杂数据集用 **InternVL** 生成目标物体描述。

**涌现的跨任务能力：** 训练数据按任务分开构造，但模型出现训练集中不存在的组合能力，例如 **ID + Try-on 组合**（图 12）。

## 训练方法
**训练目标：flow matching（rectified flow）速度回归**——沿用 FLUX/SD3 的范式，z_t=(1−t)z₀+tε，模型回归目标速度，L_diff = E[‖(z₀−ε)−V_θ(z_t,t,y)‖²]。叠加上面两个路由约束。

**三阶段渐进训练（progressive training）——本文第二个核心设计**（直接在全数据上训会难收敛，且低质样本会污染 FLUX 的生成先验）：
1. **阶段一·一致性预热（约 20K iter）：** 仅在主体驱动数据上训，初始化「一致性保持」能力。用 Subject200K（FLUX 生成、与基模分布相近 → 快收敛）；为快速带起多参考控制，同时用双列拼接的 Subject200K 图。X2I-subject 因是 MS-Diffusion 合成、含较多瑕疵畸变，此阶段不主用。产出：初步 subject-driven 能力 + 强文本跟随。
2. **阶段二·全数据多任务（约 90K iter）：** 纳入**全部数据**做全量微调，让模型在 subject/ID/try-on/style 各子任务上进一步收敛。
3. **阶段三·画质精修（约 3K iter）：** 阶段二后画质被低质训练样本拖累、偏离 FLUX 先验。故用 **FLUX 自生成约 40K 样本**，以原图作参考引导模型**重建自身**；为防 copy-paste，**丢弃参考图 95% 的 token**。短训后画质显著回升、对齐 FLUX 先验。

**关键超参（论文 Implementation Details）：** base = FLUX.1-dev；LoRA rank = 128（增参 478M）；优化器 Adam；学习率 **4e-5**；**8× NVIDIA A100 80G**；batch size = 8；阶段迭代 20K / 90K / 3K。

**v1.1 后训练（仅官方博客 `dreamo_v1.1.md` 披露，论文未含）：** v1 社区反馈两大问题——(1) 过度光泽/塑料感、(2) 结构与解剖（手/身体）易崩。**v1.1 通过在高质量数据集上做 SFT + DPO 后训练**修复：风格化场景结构稳定性大幅提升、写实场景手部与身体渲染更好、脸/场景的塑料感减轻。已知代价：v1.1 在区分同一画面中多个相似主体上略弱于 v1。

## Infra（训练 / 推理工程）
**训练：** 8× A100 80G（注意只训 478M LoRA，基模冻结，故算力门槛远低于全参后训练路线如 OmniGen/UniReal）。论文未报告总 GPU·时、并行/分布式与混合精度细节。

**推理加速：**
- 默认启用 **FLUX-Turbo LoRA**（alimama-creative/FLUX.1-Turbo-Alpha）：把采样步数从 25+ 降到 **12 步**，1024×1024 出图约 **10s**（论文口径，未注明卡型）。README 提示 Turbo 评测结果「有好有坏」但仍推荐默认开启；`--no_turbo` 可关。
- **量化（消费级 GPU 支持，README）：** 支持 int8（optimum-quanto）与 **Nunchaku** 两种量化。原始 bf16 需 ~24GB VRAM；`--quant nunchaku --offload` 可降到 **6.5GB**；社区反馈 nunchaku+offload 在 **3080** 上 1024 出图约 **20s**。给出 8GB / 16GB / 24GB GPU 的具体跑法，并支持 macOS Apple Silicon（MPS）。
- 部分示例输入用 **BEN2** 去背景。

**部署形态：** 官方 Gradio 本地 demo（`app.py`）、HuggingFace 在线 demo（spaces/ByteDance/DreamO）、原生 **ComfyUI** 实现（ToTheBeginning/ComfyUI-DreamO）。权重 Apache-2.0 开源。

## 评测 benchmark（把效果讲清楚）
所有数字来自论文 Tab.1–5（已抓取的一手 PDF）。↑ 越大越好。

**单主体定制（testset：DreamBench；CLIP-sim / DINO-sim 衡量主体一致性，Text-sim 衡量文本对齐）——DreamO 全面领先：**

| 指标 | MS-Diffusion | OmniGen | OminiControl | **DreamO** |
|---|---|---|---|---|
| CLIP-sim ↑ | 0.8989 | 0.8824 | 0.8220 | **0.9150** |
| DINO-sim ↑ | 0.7746 | 0.7582 | 0.6089 | **0.8056** |
| Text-sim ↑ | 31.78 | 31.74 | 31.12 | **31.92** |

**多主体定制（testset：DreamBench 随机选 20 对 ×25 prompt，每样本 4 seed；CLIP/DINO 衡量主体一致性、Text 衡量文本对齐，Tab.1 右半）：** DreamO 三项均最高——CLIP-sim **0.7775**、DINO-sim **0.6253**、Text-sim **31.46**（vs MS-Diffusion 0.7686/0.6113/31.34、OmniGen 0.7605/0.5646/29.55）。

**身份定制（testset：Unsplash-50，每脸 9 prompt；Face-sim 用 CurricularFace ID 余弦相似度）：**

| 指标 | PhotoMaker | InstantID | PuLID | **DreamO** |
|---|---|---|---|---|
| Face-sim ↑ | 0.212 | 0.590 | 0.5829 | **0.607** |
| Text-sim ↑ | 0.2520 | 0.2294 | 0.2534 | **0.2570** |

DreamO 人脸保真与文本可控双优。（README 诚实标注：ID 任务下 DreamO 比 SOTA 的 PuLID **引入了更多 model contamination/模型污染**。）

**虚拟试穿（testset：VITON-HD 选 300 件服装 ×10 prompt；CLIP-sim 衡量服装保真，Text-sim 衡量文本跟随）：**

| 指标 | MagicClothing | IMAGDressing | OmniGen | OminiControl | **DreamO** |
|---|---|---|---|---|---|
| CLIP-sim ↑ | 0.5977 | 0.8405 | 0.7265 | 0.7065 | 0.7613 |
| Text-sim ↑ | 30.17 | 17.74 | 27.83 | 28.79 | **30.47** |

IMAGDressing 服装 CLIP-sim 最高（0.8405）但只能出白底图、几乎不跟随文本（Text-sim 仅 17.74）；DreamO 在**保真与文本跟随之间取得最佳平衡**（Text-sim 最高）。

**文本驱动风格迁移（testset：249 风格图 ×24 prompt；Style-sim 用 CSD 特征衡量风格一致性，Text-sim 用 CLIP image-text 余弦衡量内容/文本对齐，Tab.2）：** DreamO 两项均居首——Style-sim **0.7340**、Text-sim **0.2750**，优于 StyleAlign（0.7122/0.2566）/ StyleShot（0.6922/0.2693）/ InstantStyle（0.6988/0.2721）/ DEADiff（0.7269/0.2656）/ CSGO（0.7296/0.2701），即风格一致性最高且文本/内容跟随最好。

**消融（Tab.5，多主体定制）——三个设计逐一验证有效：**

| 设置 | CLIP-sim ↑ | DINO-sim ↑ | Text-sim ↑ |
|---|---|---|---|
| w/o CE（去条件嵌入） | 0.7697 | 0.6097 | 31.26 |
| w/o RC（去路由约束） | 0.7448 | 0.5540 | 28.42 |
| w/o PT（去渐进训练） | 0.7349 | 0.5381 | 28.31 |
| **DreamO 全量** | **0.7775** | **0.6253** | **31.46** |

- **去路由约束（RC）**：单条件下参考保真下降（如衣服颜色与参考不符）；多条件下出现**条件耦合**（两个玩具特征串味）。
- **去渐进训练（PT）**：复杂任务（多主体一致性）收敛差、画质偏离 FLUX 先验，掉分最严重。
- **去占位符 loss**：占位符无法精确控制对应图（图 6：无法按「左/右来自 [ref#1]/[ref#2]」正确绑定）。
- **去 CE**：参考一致性下降。

**人评（User Study）：** 4 任务（style/object/identity/try-on）各 6 样本、20 名志愿者、0–5 分，从文本对齐 / 参考对齐 / 画质三维打分，DreamO 三项均最优（图 9，论文未给出具体分值）。

## 创新点与影响
**核心贡献：**
1. **统一框架**：单一预训练 DiT + 一组 LoRA（478M），覆盖 subject/ID/try-on/style 四类定制及其**自由组合**，训练成本低（8×A100、仅训 LoRA）。
2. **特征路由约束**：基于 DiT 内部 image-to-image cross-attention 的表示对应关系，用 MSE 把条件响应约束到主体 mask 上 → 同时提升**保真**与多条件**解耦**；这是相对 OminiControl/OmniGen 的关键方法差异（不靠 LLM/视频先验，靠专用注意力约束）。
3. **占位符策略**：`[ref#i]` + placeholder-to-image 约束，把文本里的实例名与具体参考图**显式绑定**，实现多主体的可指派放置。
4. **三阶段渐进训练**：一致性预热 → 全数据多任务 → FLUX 自生成数据画质精修（丢 95% 参考 token 防 copy-paste），解决「LoRA 容量有限难收敛」与「低质数据污染基模先验」两大痛点。
5. **涌现跨任务组合**（如 ID+Try-on）。

**影响：** 作为 2025 年少数**完整开源（Apache-2.0，含代码 + 权重 + ComfyUI + 量化）**的统一定制模型，把 IP-Adapter 系 / 身份 / 试穿 / 风格控制整合进一个 FLUX 之上的轻量 LoRA，社区落地快（Nunchaku 量化、消费级 GPU、ComfyUI 原生节点），并被 SIGGRAPH Asia 2025 接收。v1.1 进一步用 SFT+DPO 后训练打磨画质，示范了「冻结大基模 + 少量适配参数 + 注意力路由约束 + 渐进数据课程」这条统一定制的工程路径。

**已知局限：**
- ID 任务比 SOTA 的 PuLID 引入更多**模型污染**（README）。
- **风格一致性目前较不稳定**，且当前版本**风格无法与其它条件组合**（README，作者称后续改进）。
- v1（论文版）易出**过度光泽/塑料感**与**结构/解剖崩坏**——v1.1 已用 SFT+DPO 缓解，但 v1.1 在区分同画面多个相似主体上略退步。
- LoRA 容量有限是收敛难的根因（靠渐进训练绕过，而非根治）。

## 原始链接
- paper（arXiv abs，v5 / SIGGRAPH Asia 2025）: https://arxiv.org/abs/2504.16915
- pdf: https://arxiv.org/pdf/2504.16915
- github: https://github.com/bytedance/DreamO
- v1.1 release note（官方博客，SFT+DPO 后训练细节）: https://github.com/bytedance/DreamO/blob/main/dreamo_v1.1.md
- hf model（权重 + v1.1）: https://huggingface.co/ByteDance/DreamO
- hf demo: https://huggingface.co/spaces/ByteDance/DreamO
- project page: https://mc-e.github.io/project/DreamO
- ComfyUI 原生实现: https://github.com/ToTheBeginning/ComfyUI-DreamO

## 本地落盘文件
- ../../../sources/omni/2025/arxiv-2504.16915.pdf （论文全文 PDF，SIGGRAPH Asia 2025 版，正文+表至第 7–8 页、参考文献至第 9 页，已精读；PDF 按 .gitignore 不入 git）
- ../../../sources/omni/2025/dreamo--readme.md （GitHub README：任务说明 / 推理 / 量化 / 消费级 GPU）
- ../../../sources/omni/2025/dreamo--v1.1.md （v1.1 官方发布说明：SFT+DPO 后训练）
- ../../../sources/omni/2025/dreamo--hf-modelcard.md （HF model card，仅含链接，信息极少）
