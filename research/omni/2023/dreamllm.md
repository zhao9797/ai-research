---
title: "DreamLLM: Synergistic Multimodal Comprehension and Creation"
org: "Xi'an Jiaotong University / MEGVII / Tsinghua"
country: China
date: "2023-09"
type: paper
category: unified
tags: [unified, mllm, interleaved, diffusion, score-distillation, image-generation, multimodal]
url: "https://openreview.net/forum?id=y01KGvd9Bw"
arxiv: "https://arxiv.org/abs/2309.11499"
pdf_url: "https://arxiv.org/pdf/2309.11499"
github_url: "https://github.com/RunpeiDong/DreamLLM"
hf_url: "https://huggingface.co/collections/RunpeiDong/dreamllm-65fa8297e12a435e55e4b5ca"
modelscope_url: ""
project_url: "https://dreamllm.github.io/"
downloaded: [arxiv-2309.11499.pdf, dreamllm--readme.md]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
DreamLLM 是首个在**原始多模态空间**同时建模理解（语言后验）与生成（图像后验）、且能产出**自由形态图文交错文档**的 MLLM 框架：用一组可学习的 **dream queries** 把 LLM 语义直接喂给冻结的 Stable Diffusion 做 **score distillation**（不去对齐 CLIP 中间空间），由 LLaMA/Vicuna-7B 自回归地用 `<dream>` token 决定"何时画图"。DreamLLM-7B 在 MS-COCO 取得 **8.46 FID**，MMBench 49.9 / MM-Vet 35.9（同期 7B SOTA），并比 Emu-13B 在 VQAv2 上高 +16.6。ICLR 2024 Spotlight。

## 背景与定位
2023 年的 MLLM 主流只做"理解"（图像进、文本出，如 [[llava]] / Flamingo / Kosmos），而"创作"（生成图、文或图文混合）需要同时学语言后验与图像后验，当时尚未充分探索。少数并发工作（GILL、Emu、SEED）让 MLLM 产出**对齐预训练 CLIP**的条件 embedding，再交给 Stable Diffusion 生成图。

DreamLLM 指出这条路的根本缺陷：CLIP 因"modality gap"主要编码**模态共享语义**，丢失模态特有信息；强迫 MLLM 输出去对齐 CLIP 中间空间会引入"冲突而非协同"，使 MLLM 偏离其原生输出空间——论文实验证明加上 CLIP 对齐损失 `L_align` 后模型**直接坍塌不收敛**（Table 3 line 6）。此外 Emu 这类方法还需对 SD 做二阶段微调、且无法生成交错文档。

DreamLLM 的两条核心原则把它和前作区分开：
- **i. Generate Everything as It Is**：输入输出都是原始数据（raw image / raw text），端到端，输出与输入同构（Fig. 1d）；图像后验通过在**像素空间直接采样**建模，由冻结 SD 当 score function（score distillation / DeepDream 式）。
- **ii. Interleaved Generative Pre-Training (I-GPT)**：直接在互联网图文交错文档上做生成式预训练，同时学会编码与**解码**交错图文，从而隐式覆盖所有联合/边缘/条件分布，形成"理解↔创作"协同。

定位：**统一多模态（unified）代表作**，把 [[ddpm]] 的扩散/score matching 与 LLM 自回归在一个因果框架里缝合，区别于纯离散 token 路线（[[chameleon]] / Emu3 走的 VQ + next-token）。技术上更接近 [[latent-diffusion-ldm]] + textual inversion 的"模型寻优式条件学习"。

## 模型架构
**总体（Fig. 2）**：causal decoder-only LLM 作 backbone，外挂视觉 encoder 与扩散 decoder，中间用线性 projector 连接（README 把这套抽象成 **Omni 框架**：LLM=base，CLIP/SD=plugin，projector=connector）。

- **LLM backbone**：Vicuna-7B v1.1（基于 LLaMA-1，在 ShareGPT 上训练以获得 instruction-following 能力）。因果、decoder-only，是统一图文自回归建模的核心。
- **Visual encoder（输入侧）**：OpenAI CLIP-L/14，**全程冻结**。图像 resize 到 224×224 对齐 CLIP 预训练，每图 → 256 个 token 的视觉 embedding；再过一层线性 projector `M_ζ` 投到 LLM 空间。视觉序列前后加 `<IMG>` / `<IMG/>` 特殊 token。
- **Image decoder（输出侧）**：Stable Diffusion v2.1（512×512，latent diffusion，U-Net 去噪），**全程冻结、不做任何微调**。这是与 Emu（需二阶段微调 SD）的关键差异。
- **Dream queries（条件注入的核心设计）**：一组**可学习 embedding** `d = {d_q}`，默认 **Q=64**。当 LLM 预测出 `<dream>` token 后，把 64 个 dream queries 接到当前序列后，**因果地 query** 历史多模态上下文，得到条件 embedding `C^DreamLLM = F_θ(d, x_{<t+1}, V_{<K(t)+1})`；再过线性 condition projector `M_ψ` 作为 SD 的 cross-attention 条件。等价于"可学习版的 textual inversion / model-seeking"。论文把这 64 queries 可视化为 64 个"词"，cross-attention map 结构化、解耦、语义化（不同 query 抓不同主体/背景），且因因果性使注意力模式跨 prompt 高度一致（Fig. 6）。
- **交错结构建模**：新增特殊 `<dream>` token 预测"图该插在文本何处"；训练时学预测该 token，推理时模型"凭自由意志"在预测到该 token 时自动生成图——无需像 Emu 那样人工指定生成位置。生成的图会被**回灌**给 LLM 作为后续理解输入。
- **参数量 / 分辨率**：主模型 7B（base LLM），CLIP 输入 224×224、SD 目标 512×512（算 MSE loss 时把图 resize 到 512）。论文亦讨论 13B 配置（README 训练脚本默认 `vicuna-13b`），但正文评测以 7B 为主。
- **开源框架 Omni 的扩展**：README 显示代码支持把 plugin 换成 SDXL、或把生成头换成 MaskGIT-VQGAN（`maskgit-vqgan-imagenet-f16-256`, `vision_vocab_size=8192`）——即框架不绑死扩散路线，可走离散 VQ 路线，体现"通用学习框架"定位。

## 数据
三阶段共用以下数据池（Table 13 / Appendix C.1）：

- **Stage I 对齐（约 30M，pair）**：LLaVAPretrain 558K（BLIP-caption 的 CC3M+SBU+LAION400M 子集）＋ BLIP-LAION 8M ＋ LAION400M 11M ＋ LAION-COCO 11M。
- **Stage II I-GPT（约 4M，interleave/pair）**：MMC4-Core 2M（**按 CLIP score 阈值 0.25 过滤**的交错文档，记作 sMMC4）＋ BLIP-LAION 2M（BLIP 重captioned 的图文对，用来增强 T2I、抵消 MMC4 噪声/低质图）。
- **Stage III SFT（约 120K，instruction）**：LLaVAInstruct 80K（v1）/665K（v1.5）视觉指令数据 ＋ **InstructMMC4 20K**（用 GPT-4 基于 MMC4 文本内容生成"交错文档创作"指令）＋ **Instruct-BLIP-LAION 20K**（GPT-4 基于图像 caption 生成图像合成指令）。后两者是论文自构的指令数据。

**re-captioning / 清洗**：BLIP-LAION 用 BLIP 的 CapFilt 重写高质 caption；MMC4 用 CLIP score 0.25 阈值滤噪。论文在 Limitations 明确点名 **MMC4 噪声严重**（广告等），会污染输出语言/图像风格。README 的数据注册表还登记了 JourneyDB(2.4M Midjourney)、OBELICS(113M)、WebVid(10.7M 视频) 等更大池子，但正文评测未使用。未披露美学/安全（NSFW）过滤的具体细节。

## 训练方法
**目标函数（统一 MLE）**：把交错序列里每个 token（可能是词、也可能是编码后的图）的因果条件后验统一成 `L = -E_t[log p_Θ(x_t | x_{<t})]`（Eq. 6）。其中：
- **文本/理解**：标准 next-token 自回归交叉熵（Eq. 1）。
- **图像/创作**：不是预测离散 token，而是 **conditional score distillation**——以冻结 SD 为 score function，对 dream-query 条件 `C^DreamLLM` 做 denoising score matching（Eq. 4）：`L_DM = E_{t,ε}‖ε_ξ(z_t; C^DreamLLM, t) − ε‖²`，SD 的 ξ 不更新。等价于最小化"条件分布与 SD 预学 score 的 KL"（Eq. 5），即在像素/latent 空间**直接采样建模图像后验**，绕开 CLIP 中间表征的信息损失。

**三阶段训练（Table 13）**：
| 阶段 | 解冻范围 | LR | epochs | 数据 |
|---|---|---|---|---|
| I 对齐 | 仅 visual projector + condition projector + dream embedding（LLM/CLIP/SD 全冻） | 2e-3 | 1 | 30M pair |
| II I-GPT 预训练 | **解冻 LLM** | 2e-5 | 1 | 4M interleave/pair |
| III SFT | 解冻 LLM | 4e-5 | 3 | 120K instruction |

共用超参：AdamW，weight decay 0，warmup ratio 0.003，cosine scheduler，per-GPU batch size 8，max token length 2048。**CLIP/SD 始终冻结**——这是 DreamLLM 区别于 Emu（要微调 SD）、且能"白嫖"预训练扩散先验的关键。

**推理 trick**：classifier-free guidance（CFG），默认 scale 7.5，MS-COCO T2I 评测用 2.0。MS-COCO 每 prompt 采 8 张、按 CLIP score 排序取最好；LN-COCO 因文本超 CLIP 长度限制每 prompt 仅采 1 张不排序。

**关键消融/发现**：
- **协同性（Table 3）**：Creation-only 把 SD 的 FID 从 12.43 → 8.50（LLM 语言理解显著增强 T2I 专家）；用 MMC4 交错数据可提升理解（line 4）；I-GPT 进一步同时提升理解与创作（line 5，joint-learning 给出 MM-Vet 35.9 / VQAv2 56.6 / COCO FID 8.46）；**加 CLIP 对齐损失 `L_align` 直接坍塌**（line 6 N/A）——实证了"对齐 CLIP 有害"。
- **query 数（Table 9a）**：32→9.56、**64→8.46（最优）**、128→14.24（太多反而退化，与数据规模/扩散模型强度耦合）。
- **prompt-rewrite 基线（Table 10）**：DreamLLM 端到端联合学习优于"先用 LLM 改写 prompt 再交给 SD"的 rewrite-then-generate（COCO FID 8.46 vs 11.91）。

未使用任何 RLHF/DPO/reward model；未做 consistency/LCM/步数蒸馏（论文把这些列为**未来可加的提速方向**）。

## Infra（训练 / 推理工程）
- **算力**：全部三阶段均用 **128×NVIDIA A800**。训练时长：Stage I ≈6h、Stage II ≈10h、Stage III ≈1.5h（合计 ≈17.5h，相当轻量——得益于冻结 CLIP+SD、只训 7B LLM+少量 projector/query）。
- **并行/加速**：**Flash Attention** + **PyTorch FSDP**（fully-sharded data parallel）加速训练；混合精度细节未明确给出。
- **推理延迟（Table 9b，A800）**：相对纯 SD，DreamLLM 平均仅多 **~0.2s**（DreamLLM vs SD：50 步 3.65s vs 3.46s；100 步 7.02s vs 6.84s；150 步 10.41s vs 10.22s）——延迟主要来自 U-Net 去噪而非文本条件 embedding。提效方向（论文建议、未实现）：Consistency Models、量化等模型压缩。
- **部署/开源**：代码以 **Omni** 框架开源（Apache-2.0），LLM 为 base、CLIP/SD 为 plugin、projector 为 connector；配置走 Lazy Configs；`torchrun` 启动；HF 上有 checkpoint collection。

## 评测 benchmark（把效果讲清楚）
**多模态理解（Table 1，zero-shot；`*` 为用 LLaVA-1.5 SFT 数据）**
- Caption：COCO CIDEr **115.4**（`*`版 103.7）、Image2Paragraph 17.4。
- VQA：VQAv2 **56.6**（`*`72.9）、OKVQA 44.3（`*`52.2）、VizWiz 45.8（`*`49.3）、TextVQA 34.9（`*`41.8）。**比 Emu 的 VQAv2 40.0 高 +16.6**（论文正文记作 Emu-13B、Table 1 表头记作 Emu-14B，指同一模型）。
- 综合：MMBench **49.9**（`*`58.2；注：论文摘要写 49.1，正文 Table 1/Table 5 均为 49.9，此处采表值）、MM-Vet **35.9**（`*`36.6）——同期 7B 对手中 SOTA。MMBench 细分（Table 5）：RR 关系推理 60.9、AR 属性推理 53.7 等，论文归因于"图像合成学习带来更强空间/关系推理"。
- **抗幻觉 POPE（Table 7，COCO val，三种采样 split）**：以下为 **Random** split——DreamLLM-7B Accuracy **86.36** / Precision 85.92 / Recall 87.93 / F1 **86.91**，Yes 率 52.75（接近理想 50%）。论文口径是"匹配或超过 13B 量级对手"，但需按 split 对齐看：Random split 下 InstructBLIP-14B（Acc 88.57）实际仍**略高于** DreamLLM-7B（86.36）；DreamLLM 的真正优势在**最难的 Adversarial split**——DreamLLM-7B Acc **72.63** / F1 76.47 略胜 InstructBLIP-14B（72.10），取得论文所称"best or second-best"。整体 7B 体量能逼平 13/14B 对手，论文归因于图像合成学习带来的深层对象概念理解。

**文本到图像（Table 2，zero-shot FID↓）**
- **MS-COCO 30K：8.46**（仅 Stage I 对齐后 8.76；SDv2.1 基线 12.43 → 对齐后降 **3.67**，全流程预训练+SFT 后总降 **3.97**）。**比 Emu-13B（11.66）低 3.20 FID**；优于 GILL-8B(12.20)、CM3Leon-7B(10.82)；接近/优于部分专用 T2I（如 GLIDE 12.24）。
- **LN-COCO（长描述）：20.53**（对齐后 22.42；SDv2.1 基线 34.26 → 对齐降 **11.83**，全流程总降 **13.73**），论文强调这体现 DreamLLM 处理**长上下文**的优势。
- 注：作为 MLLM 路线仍不及顶尖专用大模型（Parti-20B 7.23、Muse-3B 7.88、DALL-E2 10.39），但它是当时唯一兼具理解+创作+**自由交错生成**（FIG 列）的模型。

**图文交错文档创作**
- InstructMMC4 held-out（15K 文档 / 30 主题 / 每主题 500）：用 ground-truth 文本逐句生成图，**FID 36.62 vs 纯 SD 74.77**（大幅领先）。
- **人评图灵测试**：150 样本与真实 MMC4 文档混评，5 名志愿者判"是否 supported"。真实 MMC4 支持率仅 77.24%（因 MMC4 含大量低质/重复图），DreamLLM 达 **60.68%**，超过 30% 的图灵测试门槛——说明生成图质量高且位置合理。
- 支持 in-context 图像编辑、subject-driven 生成、组合生成（zero-shot，Fig. 5）；微调 270K BLIP-Diffusion 风格数据 20 epoch 后可做 subject 一致性生成（Fig. 8）。

**纯语言能力（Table 4，验证多模态适配不损 LLM）**：相对 Vicuna-7B 基线，PIQA 78.6(+1.5)、HellaSwag 77.4(+1.7)、WinoGrande 68.5(+1.0)、BoolQ 75.2(+1.3) 多数小幅提升；MMLU 5-shot 41.8(−3.2) 略降。说明多模态适配基本不损甚至略增语言能力。

## 创新点与影响
**核心贡献**
1. **第一个能生成自由形态图文交错内容的 MLLM**，且图的"何时/何处生成"由模型用 `<dream>` token 自主决定（不需人工指定位置）。
2. **绕开 CLIP 对齐**：用 dream queries + score distillation 在原始/像素空间直接建模图像后验，实证 CLIP 对齐会导致坍塌——为后续"统一模型该不该对齐 CLIP 中间空间"提供了关键反例。
3. **理解↔创作协同（synergy）**的系统性论证：联合学习同时提升两侧，图像合成学习反哺空间/关系推理与抗幻觉。
4. **极简、冻结友好**：CLIP 与 SD 全程冻结、只训 7B LLM + 少量 projector/query，128×A800 约 17h 即可训完，工程门槛低。
5. 开源 **Omni** 通用框架（LLM=base + plugin encoder/decoder + projector），可换 SDXL / MaskGIT-VQGAN，便于扩展到 3D（ShapeLLM 同作者线）等模态。

**影响**：作为 2023 年"统一多模态理解+生成"的代表作之一，DreamLLM 与并发的 Emu/SEED/GILL 一起开启了"MLLM 既懂又会画"的方向，其"原始空间生成 + score distillation 条件"与"交错文档生成式预训练（I-GPT）"成为后续统一模型反复讨论的设计选项（对照后来的 [[chameleon]]、Emu3 走纯离散 token 路线）。ICLR 2024 Spotlight。

**已知局限**（论文 Appendix E 自陈）：
- **规模**：仅到 7B，65B/130B 的潜力未探索。
- **数据**：MMC4 噪声严重（广告等）污染输出风格；高质数据获取成本高。
- **prompt 敏感**：MLLM 对 prompt 措辞敏感，需 tailored prompting 才能给出简短答案（影响 VQA）。
- **失败案例**：多图组合创作（"A and B"）有时会把 A、B 特征**融成单一主体**（更像"A like B"），归因于组合生成本身难且专门数据稀缺。
- **未做**：RL/偏好对齐、步数蒸馏/Consistency 提速、原生高分辨率训练，均列为未来工作。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2309.11499
- arxiv_pdf: https://arxiv.org/pdf/2309.11499
- openreview (ICLR 2024 Spotlight): https://openreview.net/forum?id=y01KGvd9Bw
- github (Omni 框架 + 代码): https://github.com/RunpeiDong/DreamLLM
- project page: https://dreamllm.github.io/
- huggingface checkpoints: https://huggingface.co/collections/RunpeiDong/dreamllm-65fa8297e12a435e55e4b5ca

## 一手源存档（sources/）
- [arxiv-2309.11499.pdf](https://arxiv.org/pdf/2309.11499)  （arXiv 原文 PDF，不入 git）
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/dreamllm--readme.md)
