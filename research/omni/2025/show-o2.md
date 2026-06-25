---
title: "Show-o2: Improved Native Unified Multimodal Models"
org: "Show Lab (新加坡国立大学) / ByteDance"
country: China
date: "2025-06"
type: paper
category: unified
tags: [unified, understanding-generation, autoregressive, flow-matching, 3d-causal-vae, video, qwen2.5, omni-attention]
url: "https://arxiv.org/abs/2506.15564"
arxiv: "https://arxiv.org/abs/2506.15564"
pdf_url: "https://arxiv.org/pdf/2506.15564"
github_url: "https://github.com/showlab/Show-o"
hf_url: "https://huggingface.co/showlab/show-o2-7B"
modelscope_url: ""
project_url: ""
downloaded: [arxiv-2506.15564.pdf, show-o2--github-readme.md, show-o2--hf-modelcard.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Show-o2 是 [[show-o]] 的升级版"原生统一多模态模型"：在 **Wan2.1 的 3D 因果 VAE 连续潜空间** 上，用 **自回归（语言头）+ 流匹配（flow head）双头** 统一文本理解与图像/视频生成，靠 **dual-path 空间(-时间)融合** 同时喂语义+低层特征。仅用 66M 图文对（远少于 Janus-Pro 的 144M），7B 版在 GenEval 0.76、DPG-Bench 86.14、MMU-val 等多个理解/生成 benchmark 上超过同期统一模型，并把统一建模首次扩展到视频（2B 总参在 VBench 上压过 Emu3-8B、VILA-U-7B）。

## 背景与定位
统一多模态模型（UMM）此前分两路：一路是 [[chameleon]]/[[show-o]]/[[transfusion]] 那样用**单一视觉表征**同时做理解和生成；另一路（如 Janus 系列）用 **CLIP 做理解 + VAE 做生成的解耦表征**。Show-o2 属于"native unified"——直接把输出序列解码成 text/image/video，而非当 condition 喂外部 Stable Diffusion。

相对前作 [[show-o]] 的关键改进：
- **从离散 token 转到连续潜空间**：Show-o 用 MAGVIT-v2 离散 VQ token + 掩码生成；Show-o2 改在 Wan2.1 **3D 因果 VAE 连续潜空间**做生成，天然支持图像和视频，并把生成从 masked-token 换成 **flow matching**。
- **理解/生成表征统一且兼顾两类需求**：理解需要高层语义、生成需要低层结构，Show-o2 用 dual-path（语义层 + projector）+ 空间(-时间)融合一次性兼顾。
- **保留语言能力的两阶段训练**：避免像 Emu3/Chameleon 那样需要海量文本语料续训才能不丢语言知识。

## 模型架构
整体 = 文本 tokenizer + 3D 因果 VAE 编码器 → **统一视觉表征** → 基座 LLM（带 LM head + flow head）→ 文本 de-tokenizer + 3D VAE 解码器。

**Backbone（基座 LLM）**：Qwen2.5-1.5B-Instruct 与 Qwen2.5-7B-Instruct 两个变体。生成与理解共享同一 transformer，仅在输出端分双头。

**视觉 tokenizer / VAE**：直接采用 **Wan2.1 的 3D 因果 VAE**（空间 8×、时间 4× 压缩），连续潜空间，图像与视频共用。输入分辨率 432×432 配 2×2 patch embedding → 729=27×27 个 visual latent（与 SigLIP 输出数对齐）；更高分辨率(512/1024)用 bicubic 插值位置编码。

**统一视觉表征（dual-path 空间-时间融合，核心创新）**：
- **语义层 S(·)**：复用 **SigLIP-so400m-patch14-384** 的 ViT block，换一个新的 2×2 patch embedding 层；通过"预蒸馏"让它能从**干净**和**加噪**的 VAE 潜变量里都抽出语义特征（蒸馏目标 = 与原 SigLIP 特征的余弦相似度，最终在 66M 图文对上收敛到约 0.9）。
- **projector P(·)**：一个简单的 2D patch embedding，保留完整低层信息。
- **空间(-时间)融合 STF**：把 S(·) 与 P(·) 的输出沿特征维拼接，RMSNorm + 两层 MLP 融合得到统一表征 u；视频时语义/低层特征做**时间对齐**与全帧融合。给 u 前置一个 time-step t 的 embedding 用于生成建模（干净图 t=1.0）。

**条件注入与注意力**：序列格式 `[BOS]{Text}[BOI/BOV]{Image/Video}[EOI/EOV]{Text}…[EOS]`；采用 **omni-attention**（来自 Show-o/Transfusion）——序列层面因果注意力，但视觉表征**内部**用 full attention。

**双输出头**：
- **LM head**：因果注意力 + next-token prediction，做文本生成。
- **Flow head**：几层 transformer + adaLN-Zero 时间步调制（同 [[dit]]），full attention，用流匹配预测速度场 v_t = dx_t/dt 做图像/视频生成。

**参数与发布**：1.5B / 7B 两档；HF 上有 show-o2-1.5B、1.5B-HQ、7B，以及额外做过视频理解微调的 1.5B/7B-w-video-und。

## 数据
- **生成预训练（66M 图文对）**：从 **CC12M、COYO、LAION-Aesthetic-12M、AI 合成数据**过滤而来，要求图像宽高均 ≥512px；除合成数据外全部用 LMM **重新打标（re-caption）**。
- **高质量生成数据（16M）**：从上述 66M 里**过滤**出的高质子集，用于 stage-1 续训和 stage-2。
- **理解指令数据（9M HQ）**：来自 **DenseFusion-1M、LLaVA-OneVision**（含纯文本指令数据，用于保住语言能力）。
- **视频/交错数据**：WebVid、Panda-70M(Pandas)、OpenVid-1M、VIST、CoMM 等用于视频-文本与交错图文；视频理解微调用 1.6M 视频样本（[145]）+ 1.1M 图像样本。
- **文本渲染增强**：额外引入 **TextAtlas** 子集的富文本图像，并在 512/1024 高分辨率上续训以改善文字渲染。
- **CFG**：生成数据 caption 以 0.1 概率丢弃以支持 classifier-free guidance。

数据**配比对比**值得记一笔：Show-o2 仅 66M 图文对，对照 Janus-Pro 的 144M、BAGEL 的 1600M、Transfusion 的 3.5B、Show-o 的 2.0B（均为生成训练图文对数，见 Table 5），数据效率显著更高（Emu3 的 # Data 论文表中未报告，记为"—"）。

## 训练方法
**训练目标**：双头联合损失 `L = α·L_NTP + L_FM`（next-token + flow matching）。stage-1 中 α=0.2，stage-2 中 α=1.0。

**预蒸馏（前置步骤）**：先把语义层 S(·) 从 SigLIP-so400m 蒸馏 **200K 步**，batch 512、cosine LR 2e-5；最后 20K 步以 0.3 概率对潜变量加噪（按 x_t = t·x1 + (1−t)·x0 的 flow 插值）让它适应噪声输入。

**两阶段配方（核心，目的是不丢语言知识）**：
- **Stage-1（生成预训练）**：只训 projector + 空间-时间融合 + flow head（冻结 LLM）。1.5B 变体用 66M 图文对训 150K 步（AdamW，constant LR 1e-4，分辨率 432×432，单图文对 context length 1024，理解/生成 batch 分别 128/384）。然后换 16M HQ 数据再训 40K 步。视频/交错数据在此阶段渐进加入（视频取 2s、17 帧、间隔 3 帧、context length 7006）。
- **Stage-2（全模型微调）**：解冻全模型（除 VAE），按 LLaVA-OneVision 策略用 9M 理解指令 + 16M HQ 生成数据训约 35K 步。

**Scaling Up（小→大迁移技巧）**：先训好 1.5B 的 flow head，再 **resume 到 7B**，新初始化的空间-时间融合/projector + 一个轻量 MLP 变换（对齐 hidden size）先训 3K 步（2K warmup）快速对齐，然后整体再训，最后照常跑 stage-1/2。7B 因算力成本未纳入交错和视频数据。

**蒸馏/加速**：除上述语义层预蒸馏外，未报告生成步数蒸馏（consistency/LCM/ADD）；推理仍用多步 flow + CFG。

## Infra（训练 / 推理工程）
- **算力**：1.5B 模型 stage-1 主训约 **1.5 天 / 64×H100**；stage-2 约 **15 小时**。7B 模型整个训练约 **2.5 天 / 128×H100**。
- **精度/并行**：论文未披露具体并行策略与混合精度配置。
- **推理**：默认 50 步 flow 采样 + CFG（demo 用 guidance_scale=7.5、num_inference_steps=50）。消融显示 25/50/100 步与 CFG 2.5→10 的影响有限（见下）。理解侧支持 **AnyRes**（推理时把图像 token 从 729 扩到 5×729）显著提升 OCR/文档 VQA。
- **部署**：开源（Apache-2.0），diffusers 库，依赖外部下载 Wan2.1 VAE 权重；提供 1.5B/7B 多个 checkpoint。

## 评测 benchmark（把效果讲清楚）
数字均来自论文表格（已落盘 PDF）。

**多模态理解（Table 3，越大越好）**：
- Show-o2-1.5B：MME-p **1450.9**、GQA 60.0、SEED 65.6、MMB(en) 67.4、MMMU-val 37.1、MMStar 43.4、AI2D 69.0；论文称在 ~1.5B 档于 MME-p、MMMU-val 取最佳，GQA/SEED 有竞争力。
- Show-o2-7B：MME-p **1620.5**、GQA 63.1、SEED 69.8、MMB 79.3、MMMU-val **48.9**、MMStar 56.6、AI2D 78.6；在 MME-p、GQA、MMMU-val、MMStar、AI2D 上超过 Janus-Pro-7B 甚至 14B 的 TokenFlow-XL。

**视频理解（Table 4，零样本，w-video-und 微调版；列顺序按论文表头逐项核对）**：
- 1.5B(32帧)：ActNet-QA 52.7、MVBench 49.8、NExT-QA(mc) 72.1、PerceptionTest 56.1、LongVideoBench 49.2、VideoMME(wo/w-subs) 48.0/51.6。
- 7B(16/32帧)：ActNet-QA 56.4、MVBench 55.8、NExT-QA(mc) 79.0、PerceptionTest 61.9、LongVideoBench 55.5、VideoMME 57.4/60.9。统一模型里属第一梯队（与 LLaVA-OV-7B NExT-QA 79.4 持平、其余有来有回）。

**文生图 GenEval（Table 5，overall）**：Show-o2-1.5B **0.73**、7B **0.76**；超过 Show-o(0.68)、Emu3(0.66)、Transfusion(0.63)、TokenFlow-XL(0.55)；略低于 Janus-Pro(0.80)/BAGEL(0.88)/Mogao(0.89)，但后者数据量大得多（Janus 144M、BAGEL 1600M）。

**文生图 DPG-Bench（Table 6，overall）**：Show-o2-1.5B **85.02**、7B **86.14**，**超过** SD3-Medium(84.08)、Emu3-DPO(81.60)、Janus-Pro(84.19)、Mogao(84.33)，取得表中统一/生成模型里的最佳总分（7B 各子项 Global 89.00 / Entity 91.78 / Attribute 89.96 / Relation 91.81 / Other 91.64，多项领先）。

**OneIG-Bench（Table 7）**：Show-o2 Alignment 0.798(1.5B)/0.817(7B) 有竞争力；**Text/文字渲染分极低（0.002）**，1024×1024 版可提升到 0.125——印证文字渲染是其短板。

**文生视频 VBench（Table 8）**：Show-o2 仅 **2B 总参**，QS 82.10、SS 78.31、OC' 27.00、Dynamic Degree 40.83、Multiple Objects 76.01，整体（Total 81.34）**超过 Emu3-8B(80.96)、VILA-U-7B(74.01)、HaploOmni-9B(78.10)**，与 CogVideoX(81.61)、Step-Video-T2V(81.83) 有可比性。图生视频 VBench(Table 9) 各维度（I2V Subject 96.94、I2V Background 98.83、Background Consistency 97.45、Motion Smoothness 97.76 等）亦具竞争力。

**关键消融**：
- *空间-时间融合*（Table 10，LLaMA-3.2-1B + 1M 数据）：加融合后 MME-p 1164.7→1187.8、GQA 56.2→57.6、FID-5K 21.8→20.5，**理解和生成同时受益**。
- *CFG/步数*（Table 11，1.5B）：CFG>5.0 后 GenEval 收益饱和（0.71），步数 50 已足够；100 步可到 0.73。
- *训练阶段*（Table 12）：stage-2 把 GenEval 0.63→0.73、DPG 83.28→84.70，**stage-2 至关重要**。
- *训练配方对语言能力的保护*（Table 13，最关键）：两阶段配方下 7B 的 MMLU 70.73、GSM8K 75.28、HumanEval 70.73，**几乎无损于原始 Qwen2.5-7B**（71.75/82.49/65.24）；而"一阶段 + RefinedWeb 共训"会灾难性退化（MMLU 28.43、GSM8K 1.52、HumanEval 4.01）——这是 Show-o2 训练配方的核心卖点验证。
- *图像 token 数*（Table 14）：7B 从 729→5×729 token，ChartQA 48.0→66.92、DocVQA 59.34→77.26，AnyRes 推理显著提升细粒度理解。

## 创新点与影响
**核心贡献**：
1. **3D 因果 VAE 连续潜空间上的原生统一**：首次把"自回归理解 + 流匹配生成"的统一建模从图像扩展到**视频**，图像/视频共用同一表征与同一套头。
2. **dual-path 空间(-时间)融合 + 语义层预蒸馏**：用 SigLIP 蒸馏出的语义层（能处理加噪潜变量）+ projector 低层特征融合，单一连续表征同时满足理解（要语义）与生成（要低层结构），消融证明两者互益。
3. **两阶段训练配方**：先冻 LLM 训生成头、再全量微调，**无需海量文本语料即可保住语言能力**（Table 13 量化证明），并能从 1.5B flow head 平滑迁移到 7B。
4. **数据效率**：66M 图文对达到与百M~十亿级数据模型可比甚至更好的生成/理解结果。

**影响**：延续 Show-o 路线，是 2025 年"连续潜空间 + AR+flow 双头"统一多模态范式的代表作之一；其"语义层蒸馏喂理解、VAE 低层喂生成"的表征设计与"保语言两阶段配方"对后续 native UMM 有借鉴价值；开源（含 1.5B/7B + 视频版）便于复现。

**已知局限**（论文自述）：
- **文字渲染弱**（生成数据中富文本图像比例小，OneIG Text 仅 0.002，靠高分辨率+TextAtlas 部分缓解）。
- **小物体细节缺失**（受分辨率限制）。
- ChartQA 偏弱（语义层蒸馏阶段图表数据少）。
- 7B 因算力未训交错/视频数据，视频与混合模态能力主要在 1.5B/2B 上验证。
- 伦理风险：数据含名人/版权内容，可能涉及侵权与伪造信息滥用。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2506.15564
- arxiv_pdf: https://arxiv.org/pdf/2506.15564
- github: https://github.com/showlab/Show-o （show-o2 子目录 https://github.com/showlab/Show-o/tree/main/show-o2）
- hf_modelcard: https://huggingface.co/showlab/show-o2-7B （另有 1.5B / 1.5B-HQ / 7B-w-video-und 等）

## 本地落盘文件
- ../../../sources/omni/2025/arxiv-2506.15564.pdf （v3, 22 页，精读）
- ../../../sources/omni/2025/show-o2--github-readme.md
- ../../../sources/omni/2025/show-o2--hf-modelcard.md
