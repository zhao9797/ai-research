---
title: "Janus-Pro: Unified Multimodal Understanding and Generation with Data and Model Scaling"
org: DeepSeek-AI
country: China
date: "2025-01"
type: tech-report
category: unified
tags: [unified-multimodal, autoregressive, decoupled-visual-encoding, t2i, vlm, open-source, deepseek]
url: https://arxiv.org/abs/2501.17811
arxiv: https://arxiv.org/abs/2501.17811
pdf_url: https://arxiv.org/pdf/2501.17811
github_url: https://github.com/deepseek-ai/Janus
hf_url: https://huggingface.co/deepseek-ai/Janus-Pro-7B
modelscope_url: ""
project_url: https://github.com/deepseek-ai/Janus
downloaded: [arxiv-2501.17811.pdf, janus-pro--github-readme.md, janus-pro--hf-modelcard.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Janus-Pro 是 DeepSeek 在 [[janus]] 基础上"加数据、加规模、改训练策略"的增强版统一多模态模型（同一个自回归 Transformer 同时做"看图理解"与"文生图"），核心思路是**解耦视觉编码**（理解用 SigLIP 语义编码、生成用 VQ 离散 tokenizer），开源 1B/7B 两档。最亮眼结果：Janus-Pro-7B 在文生图指令遵循榜 GenEval 拿到 **0.80**、DPG-Bench **84.19**，同时多模态理解 MMBench **79.2**，在统一模型里全面 SOTA，并超过 DALL-E 3(0.67)、SD3-Medium(0.74) 等专用生成模型。

## 背景与定位
统一多模态（理解+生成同一个模型）的主流做法是**用同一个视觉编码器**同时喂理解任务和生成任务（如 [[chameleon]]、[[show-o]]、[[emu3]]、[[vila-u]]、TokenFlow）。但这两个任务对表征的需求不同：理解需要高层语义、生成需要低层像素/纹理细节，共享编码器会产生冲突，拖累理解性能。

前作 [[janus]]（2024-10，arXiv:2410.13848）提出**解耦视觉编码**：理解走一条编码路径、生成走另一条，再共用同一个自回归 Transformer，缓解了两任务冲突，在 1.5B 规模上验证了有效性。但 Janus 因数据量有限、模型容量小，存在两个短板：**短 prompt 文生图质量不稳定**、**整体生成质量偏弱**。

Janus-Pro 不改架构，只从**三个维度**做工程化增强——训练策略、数据、模型规模——把统一模型推到能正面对标专用文生图模型（[[stable-diffusion-3]] SD3-Medium、DALL-E 3、SDXL、PixArt 系列）的水平。定位是"2025 年初开源统一多模态的热点标杆"，1B/7B 全开源、商用许可，可在 HF 直接跑 demo。

## 模型架构
**架构与 Janus 完全相同**（论文原话 "the same as Janus"），核心是解耦视觉编码 + 单一自回归 Transformer（见论文 Figure 3）：

- **理解编码器（Und. Encoder）**：用 **SigLIP-Large-Patch16-384**（[[siglip]]）提取高维语义特征；2-D 网格特征展平成 1-D 序列后，经一个**理解 adaptor（两层 MLP）**映射到 LLM 输入空间。
- **生成编码器（Gen. Encoder）**：用 LlamaGen（arXiv:2406.06525）的 **VQ tokenizer** 把图像转成离散 ID；codebook 大小 **16384**，**下采样倍数 16**；ID 序列展平后经一个**生成 adaptor（两层 MLP）**把每个 ID 对应的 codebook embedding 映射进 LLM 输入空间。
- **统一 backbone**：把理解/生成/文本三种特征序列拼成一条多模态序列，喂进同一个**自回归 Transformer**（即 DeepSeek-LLM）。文本预测用 LLM 自带 head；图像生成用一个**随机初始化的独立 prediction head**。整个模型是纯 next-token 自回归框架（不是 diffusion，也不是 masked-token）。
- **LLM backbone**：**DeepSeek-LLM 1.5B / 7B**（arXiv:2401.02954），最大序列长度 4096。
- **架构超参（Table 1）**：
  - Janus-Pro-1B：vocab 100K，embedding 2048，context 4096，16 heads，24 层。
  - Janus-Pro-7B：vocab 100K，embedding 4096，context 4096，32 heads，30 层。
- **分辨率策略**：统一 **384×384**。理解数据按长边缩放、短边用背景色（RGB 127,127,127）padding 到 384；生成数据短边缩放到 384、长边裁剪到 384。生成端 token 数 = (384/16)²=576。

注意命名细节：HF/README 写 1B，但论文正文与超参表多处写 LLM 实际为 **1.5B**（DeepSeek-LLM 1.5B），"Janus-Pro-1B"是对外模型名。

## 数据
Janus-Pro 相对 Janus 的最大变化之一就是**扩数据**，理解与生成两侧都加（数字均为论文披露）：

- **多模态理解**：
  - Stage II 预训练参考 [[deepseek-vl2]]（arXiv:2412.10302）**新增约 9000 万（90M）样本**，包括图像 caption 数据集（如 YFCC，HF: mehdidc/yfcc15m）以及表格/图表/文档理解数据（如 Docmatix）。
  - Stage III SFT 也补入 DeepSeek-VL2 的额外数据：MEME 理解、中文对话数据、提升对话体验的数据集。
- **视觉生成（关键改动）**：
  - 作者指出前作用的真实世界数据**质量差、噪声大**，导致文生图不稳、美感差。
  - Janus-Pro 引入**约 7200 万（72M）合成美学数据**，使统一预训练阶段**真实:合成 = 1:1**。合成数据的 prompt 公开可得（论文引 Vivym/midjourney-prompts 数据集）。
  - 结论：合成数据让模型**收敛更快**，文生图输出**更稳定、美感显著提升**。

数据清洗/过滤的具体管线（去重、安全过滤、美学打分阈值等细节）**未详细披露**，只给了上述规模与配比口径。

## 训练方法
延续 Janus 的**三阶段训练**，但对策略做了关键修正（这是 Janus-Pro 的核心贡献之一）；训练目标全程是**纯自回归 next-token 预测**（文本与图像 token 都用交叉熵），**不涉及 diffusion / flow matching / RLHF / DPO**（论文未报告任何偏好对齐或蒸馏）。

- **Stage I（训练 adaptor + image head）**：原 Janus 在此阶段训练较短。Janus-Pro **延长 Stage I**，让模型在 ImageNet 上充分训练——发现即使**冻结 LLM 参数**，模型也能学到像素依赖、按类别名生成合理图像。
- **Stage II（统一预训练，除两个视觉编码器外全部更新）**：原 Janus 仿 PixArt 把文生图训练拆两部分——先用 ImageNet（类别名当 prompt）建模像素依赖、再用正常文生图数据，且 **66.67% 的 Stage II 文生图步数花在 ImageNet 上**，作者发现这**低效**。Janus-Pro **直接丢掉 ImageNet 数据**，Stage II 全程用正常文生图数据（dense description）训练，效率与性能双升。Stage II 用**早停**，在 270K 步停止（总规划 360K）。
- **Stage III（SFT，进一步解锁理解编码器参数）**：把 SFT 阶段**多模态:纯文本:文生图**的数据配比从 Janus 的 **7:3:10 改为 5:1:4**——略降文生图占比，在保住生成能力的同时提升理解性能。
- **训练超参（Table 2，1B 与 7B 一致）**：
  - 学习率分阶段 **1e-3 / 1e-4 / 4e-5**，恒定 LR scheduler，weight decay 0，grad clip 1.0。
  - 优化器 **AdamW（β1=0.9, β2=0.95）**；warm-up 仅 Stage I/II 各 600/5000 步，Stage III 为 0。
  - 训练步数：Stage I/II/III = **20K / 360K / 80K（1B）**、**20K / 360K / 40K（7B）**。
  - batch size：**256 / 512 / 128**。
  - 各阶段数据配比（理解:纯文本:生成）：**Stage I 1:0:3、Stage II 2:3:5、Stage III 5:1:4**。
- **训练 trick**：用 **sequence packing** 提升效率；按指定配比在**单个训练步内混合**所有数据类型。

## Infra（训练 / 推理工程）
- **训练框架**：用 **HAI-LLM**（High-flyer 自研，PyTorch 之上的轻量高效分布式训练框架），训练与评测均在其上完成。
- **算力**：Janus-Pro-1.5B 训练约 **9 天 / 16 节点**；Janus-Pro-7B 约 **14 天 / 32 节点**；每节点 **8× Nvidia A100 (40GB)**。即 7B 用 **256 张 A100-40G、约 14 天**。
- **并行/混合精度/吞吐**：论文**未披露**具体并行策略（TP/PP/ZeRO 等）与精度配置；推理示例用 **bfloat16**（HF 代码 `to(torch.bfloat16)`）。
- **推理**：文生图走自回归逐 token 生成 + classifier-free guidance（demo 默认 cfg=5）；理解侧标准 VLM 推理。论文未报告量化、缓存、步数蒸馏等加速。
- **部署形态**：HF 上以 `transformers`（`trust_remote_code=True`）直接加载；提供 Gradio 在线 demo（HF Spaces）与本地脚本。代码 MIT 许可、模型 DeepSeek Model License，**允许商用**。

## 评测 benchmark（把效果讲清楚）
所有数字来自已落盘的论文 PDF（Table 3/4/5），均为一手。

**多模态理解（Table 3，Janus-Pro-7B）**：
- POPE **87.4**，MME-Perception **1567.1**，**MMBench(MMB) 79.2**，SEED **72.1**，GQA **62.0**，MMMU **41.0**，MM-Vet **50.0**。
- MMBench 79.2 超过统一模型 Janus(69.4)、TokenFlow(68.9)、MetaMorph(75.2)；论文称 7B 在除 GQA 外**所有理解基准上超过 13B 的 TokenFlow-XL**。
- Janus-Pro-1B：POPE 86.2，MME-P 1444.0，MMB 75.5，SEED 68.3，GQA 59.3，MMMU 36.3，MM-Vet 39.8。

**文生图 GenEval（Table 4，总分 Overall↑）**：
- **Janus-Pro-7B = 0.80**（Single 0.99 / Two 0.89 / Counting 0.59 / Colors 0.90 / Position 0.79 / Color-Attri 0.66）。
- **Janus-Pro-1B = 0.73**。
- 对比：Janus 0.61、Transfusion 0.63、SD3-Medium 0.74、DALL-E 3 0.67、SDXL 0.55、Emu3-Gen 0.66、Chameleon 0.39。Janus-Pro-7B 超过所有统一模型与列出的专用生成模型。

**文生图 DPG-Bench（Table 5，总分 Overall↑）**：
- **Janus-Pro-7B = 84.19**（Global 86.90 / Entity 88.90 / Attribute 89.40 / Relation 89.32 / Other 89.48）。
- **Janus-Pro-1B = 82.63**。
- 对比：DALL-E 3 83.50、SD3-Medium 84.08、Emu3-Gen 80.60、PixArt-Σ 80.54、Janus 79.68。Janus-Pro-7B 超过表中所有方法（含专用模型）。

**关键消融/结论**：训练策略上证明"延长 Stage I + Stage II 丢 ImageNet"提升效率与质量；数据上证明"1:1 加 72M 合成美学数据"加速收敛、稳定短 prompt 生成、提升美感（Figure 2 定性对比）；规模上证明"1.5B→7B 后理解与生成的 loss 收敛都更快"，验证方法的可扩展性。
**注意**：论文**未报告 FID、CLIPScore、HPSv2、ImageReward、PickScore、人评 ELO/Arena** 等指标，也无视频/编辑评测（该模型不做视频/编辑）。

## 创新点与影响
**核心贡献**：
1. 把"解耦视觉编码"的统一多模态范式从 1.5B 扩到 7B，证明其**强可扩展性**——更大 LLM 下理解与生成 loss 收敛都更快。
2. 一套低成本但有效的**工程配方**：训练策略修正（延长 Stage I、Stage II 去 ImageNet、SFT 配比 7:3:10→5:1:4）+ 数据扩展（理解 +90M、生成 +72M 合成美学、真实:合成=1:1）。
3. 让纯自回归统一模型在 **GenEval/DPG-Bench 上正面超过 DALL-E 3 / SD3-Medium 等专用 diffusion 模型**，且同时保持强理解能力。

**影响**：作为 DeepSeek 在 2025 年初紧随 DeepSeek-R1 热度释出的开源统一多模态模型，1B/7B 全开源 + 商用许可，迅速成为统一多模态方向被对标/复现的基线，推动"解耦编码 + 自回归"路线在社区扩散；与 [[show-o]]、[[emu3]]、[[transfusion]]、[[chameleon]] 共同定义了 2024-2025 统一模型的竞争格局。

**已知局限（论文自陈）**：
- 理解输入分辨率仅 **384×384**，细粒度任务（如 OCR）受限。
- 文生图分辨率低，叠加 VQ tokenizer 的重建损失，导致图像"语义丰富但细节不足"——典型如小人脸区域欠清晰。
- 提升路径明确指向**提高分辨率**。此外模型未做任何偏好对齐（无 RLHF/DPO），美感/安全主要靠数据侧合成数据兜底。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2501.17811
- arxiv_pdf: https://arxiv.org/pdf/2501.17811
- github: https://github.com/deepseek-ai/Janus
- hf (7B): https://huggingface.co/deepseek-ai/Janus-Pro-7B
- hf (1B): https://huggingface.co/deepseek-ai/Janus-Pro-1B
- 前作 Janus: https://arxiv.org/abs/2410.13848
- 前作 JanusFlow: https://arxiv.org/abs/2411.07975

## 一手源存档（sources/）
- [arxiv-2501.17811.pdf](https://arxiv.org/pdf/2501.17811)  （arXiv 原文 PDF，不入 git）
- [github-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/janus-pro--github-readme.md)
- [hf-modelcard.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/janus-pro--hf-modelcard.md)
