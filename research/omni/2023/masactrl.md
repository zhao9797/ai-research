---
title: "MasaCtrl: Tuning-Free Mutual Self-Attention Control for Consistent Image Synthesis and Editing"
org: "The University of Tokyo / Tencent PCG (ARC Lab)"
country: China
reviewed: 2026-06-25
date: "2023-04"
type: paper
category: edit
tags: [diffusion, image-editing, self-attention, training-free, non-rigid-editing, stable-diffusion, consistency, attention-control]
url: "https://arxiv.org/abs/2304.08465"
arxiv: "https://arxiv.org/abs/2304.08465"
pdf_url: "https://arxiv.org/pdf/2304.08465"
github_url: "https://github.com/TencentARC/MasaCtrl"
hf_url: "https://huggingface.co/TencentARC/MasaCtrl"
modelscope_url: ""
project_url: "https://ljzycmd.github.io/projects/MasaCtrl/"
downloaded: [arxiv-2304.08465.pdf, masactrl-iccv2023.pdf, masactrl--readme.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
MasaCtrl 是一个**免训练 / 免优化（tuning-free）**的文生图扩散模型注意力控制方法：把 Stable Diffusion 中的**自注意力（self-attention）改造成"互注意力（mutual self-attention）"**——让目标图的 Query 去查询源图自注意力里的 Key/Value，从而在改变姿态/视角等**非刚性布局**的同时保持物体的纹理与身份一致。无需对模型或文本嵌入做任何微调，用户研究中 **73.5%** 的参与者偏好其结果（对比 P2P/PnP/Imagic）。

## 背景与定位
2023 年初的文生图编辑方法（如 [[prompt-to-prompt]] P2P、[[plug-and-play-diffusion-features]] PnP、SDEdit）主要操作**交叉注意力（cross-attention）**或注入空间特征，擅长保留原图布局做风格迁移、外观替换，但**做不了"非刚性编辑"**——比如让坐着的狗站起来、让鸟展开翅膀这类姿态/视角的大幅变化，因为它们刻意维持原图的语义布局与结构。

唯一能做非刚性编辑的同期工作是 **Imagic**，但它需要**对整个 T2I 扩散模型微调 + 优化文本嵌入**，每张图都要训练，耗时（论文测得约 14 分钟/张）且对普通用户不友好。

MasaCtrl 的定位正是填补这个空白：**既要非刚性（改布局/姿态）、又要一致性（保身份/纹理）、还要免训练（秒级）**。其核心洞察来自两个观察：(1) 扩散去噪的**早期步骤决定图像布局**，后期步骤填充内容；(2) [[tune-a-video]] 等工作发现**跨 batch 做自注意力能生成相似内容**。MasaCtrl 把这个现象工程化为一套精确的"何时、何层"控制策略。论文基于 [[latent-diffusion-ldm]] / [[stable-diffusion]]，是该路线（"训练免费的注意力操控编辑"）的代表作之一，已被 ICCV 2023 收录（pp. 22560-22570）。

## 模型架构
MasaCtrl **本身不是一个模型，而是一个推理期的注意力替换算子**，挂载在现成的 Stable Diffusion 上，零新增参数。

- **Backbone**：Stable Diffusion v1.4（主实验），time-conditional U-Net（[[ddpm]] 式去噪网络）。每个基础块 = 残差块 + 自注意力 + 交叉注意力。也验证了 SD v1.5、anime 风模型 Anything-V4、DreamBooth 定制模型；GitHub 后续（2023/8）扩展支持 **SDXL**。
- **VAE / latent**：沿用 LDM 的预训练图像自编码器，在 latent 空间去噪。无改动。
- **Text encoder**：沿用 SD 的 CLIP text encoder，无改动。
- **核心算子——互注意力（Mutual Self-Attention）**：
  - 标准自注意力 `Attention(Q,K,V)=Softmax(QKᵀ/√d)·V`，Q/K/V 均来自同一图的空间特征。
  - 互注意力**保留目标图的 Query `Q`，但把 Key/Value 替换为源图重建过程对应自注意力层的 `Kₛ, Vₛ`**——即"把自注意力变成跨两个扩散过程的交叉注意力"。这样目标图就能从源图里"取材"（查询纹理、颜色、身份），同时自身布局由目标 prompt 决定。
  - **关键：不是所有步/所有层都替换。** 直接全程全层替换会得到与源图几乎一样的结果、无视目标 prompt。EDIT 函数定义为（论文 Eq.2）：`当 T−t > S 且 l > L 时用 {Q, Kₛ, Vₛ}，否则用原始 {Q,K,V}`（T 为总去噪步数，故 `T−t > S` 表示已去噪 S 步之后才开始控制）。即**只在去噪若干步之后、且只在 U-Net 解码器（decoder）部分**做互注意力控制。默认 **S=4 步、L=10 层**（DDIM 50 步采样，CFG=7.5）。消融表明：早期步骤需让目标布局先成形；解码器高分辨率层才承载内容，编码器/低分辨率层做控制会丢内容或丢布局。
- **掩码引导互注意力（Mask-Guided Mutual Self-Attention）**：当前景与背景颜色/纹理相似时，互注意力会"前后景串味"产生混乱。解决办法是**从交叉注意力图免费提取掩码**：在 step t 用源/目标 prompt 各前向一遍，取前景物体 token 的交叉注意力图，在 16×16 分辨率上跨所有 head 与层平均，得到源掩码 `Mₛ` 与目标掩码 `M`。然后前景特征只查询源图前景、背景只查询源图背景：`f̄ = f_o·M + f_b·(1−M)`，其中 `f_o = Attention(Q, Kₛ, Vₛ; Mₛ)`、`f_b = Attention(Q, Kₛ, Vₛ; 1−Mₛ)`。掩码全自动、零额外标注/分割网络。
- **可控扩散集成**：可直接套在 [[t2i-adapter]] / [[controlnet]] 之上——用 Adapter/ControlNet（pose/sketch/seg）强约束目标布局，再用 MasaCtrl 从源图查内容。此时因布局被强引导，可把控制提前（实验用 **S=2, L=8**）。

## 数据
**无训练数据**。MasaCtrl 是免训练方法，不涉及任何数据集采集、清洗、配比、re-captioning 或合成数据——它完全复用预训练好的 Stable Diffusion 权重。真实图编辑时，用 **DDIM 确定性反演（deterministic inversion）** 把真图反推成噪声图（此时源 prompt 设为 null），再走互注意力合成。评测用的源图见下文 benchmark 部分（20 张：10 合成 + 10 真实）。

## 训练方法
**不适用——本方法零训练、零微调、零优化。** 这正是其相对 Imagic（需逐图微调全模型 + 优化文本嵌入）的核心卖点。所有"方法"都发生在**推理期的去噪循环里**（见 Algorithm 1）：
1. 对每个去噪步 `t = T … 1`：先用源 prompt `Pₛ` 跑一遍 SD 得到源图的 `εₛ` 与 `{Qₛ,Kₛ,Vₛ}`，采样得 `z_{t−1}ˢ`；
2. 再用目标 prompt `P` 跑目标图，得到 `{Q,K,V}`；
3. 经 EDIT 函数把目标图自注意力的 K/V 换成源图的 `Kₛ,Vₛ`（满足 T−t>S, l>L 时），算出 `{Q*,K*,V*}`，重新前向得 `ε`，采样得 `z_{t−1}`。

不涉及 diffusion/flow-matching 的重新训练，不涉及 SFT/RLHF/DPO，不涉及一致性蒸馏/LCM/ADD 等加速训练。唯一的"超参"是控制起始步 **S** 与起始层 **L**（默认 S=4/L=10；接 Adapter 时 S=2/L=8），以及标准 SD 采样参数（DDIM 50 步、CFG 7.5）。

## Infra（训练 / 推理工程）
- **训练算力**：无（免训练）。
- **推理资源**：单张 ≥16 GB 显存 GPU 即可跑合成（README 明确要求）；基于 diffusers，代码结构类似 Prompt-to-Prompt。
- **推理开销**：因要并行/串行跑"源图重建 + 目标图合成"两条扩散过程，约为单次 SD 采样的~2 倍。论文实测 **Runtime ≈ 16s/张**（与 P2P 15s 同级，远快于 PnP 60s、Imagic 14min）。
- **部署形态**：官方提供 HuggingFace Gradio Demo、Colab、OpenXLab 应用；2024/8 加入基于 diffusers `AttnProcessor` 的 `MasaCtrlProcessor`，可注册进官方 Diffusers pipeline。
- 量化/缓存/步数蒸馏等推理加速：**未涉及**（不是该工作关注点）。

## 评测 benchmark（把效果讲清楚）
> 注意：**arXiv v1 PDF（2304.08465，仅 v1，无后续版本）只有定性图，没有定量表**。下列定量数字来自**已落盘的 ICCV 2023 camera-ready 版**（`masactrl-iccv2023.pdf`，第 5.1 节 Table 1）。

**评测设置**：20 张源图（10 张合成 + 10 张真实），分别用 P2P、PnP、Imagic、MasaCtrl 做编辑。指标：
- **Text-alignment**：目标 prompt 与编辑图在 CLIP 特征空间的对齐度（越高越符合 prompt）。
- **Image-alignment**：源图与编辑图在 CLIP 特征空间的对齐度（越高越保内容一致）。
- **Preference**：用户研究，收集 **700 份**专业参与者答案的偏好占比。
- **Runtime**：单张耗时。

**Table 1（一手数字）：**

| 方法 | Text-alignment ↑ | Image-alignment ↑ | Preference ↑ | Runtime |
|---|---|---|---|---|
| P2P [10] | 0.2691 | 0.8793 | 3.0% | 15s |
| PnP [35] | 0.2589 | 0.8902 | 2.5% | 60s |
| Imagic [12] | 0.2688 | 0.9159 | 21.0% | 14min |
| **Ours (MasaCtrl)** | **0.2793** | **0.9286** | **73.5%** | 16s |

结论：MasaCtrl 在**三项指标全面领先**——既最符合目标 prompt（text-align 0.2793 最高），又最保源图内容一致（image-align 0.9286 最高），用户偏好 73.5%（碾压 Imagic 的 21.0%、P2P 3.0%、PnP 2.5%），且耗时仅 16s（Imagic 需 14 分钟）。

**关键消融（Sec. 5.5，定性）：**
- **起始步 S**：在过早步骤做互注意力控制 → 输出几乎等同源图、忽略目标布局；随 S 增大 → 布局来自目标 prompt、内容来自源图（理想区间）；S 太大 → 逐渐丢失源图内容、退化为无控制的纯目标合成。
- **起始层 L / U-Net 位置**：全层控制 → 等同源图；只在低分辨率层（layer 4~10）→ 既丢内容又丢目标布局；在解码器高分辨率层（layer 10~15）→ 保目标布局、内容可正确迁移。**故定为"解码器 + 若干步之后"**。
- **掩码引导**：前景/背景相似时去掉掩码会串味产生混乱（Fig.2 第二行），加掩码后前后景分离干净。

**定性对比**：在合成图与真实图编辑上均显著优于 P2P/PnP/SDEdit（这三者因依赖原图布局信息而无法做非刚性变化）。在 Anything-V4、DreamBooth 定制模型上泛化良好；接 T2I-Adapter/ControlNet 可做更忠实的非刚性编辑乃至逐帧视频合成。**未报告 FID / GenEval / T2I-CompBench / VBench 等标准 benchmark**（该工作以编辑一致性与用户偏好为主要指标，未跑这些数据集）。

## 创新点与影响
**核心贡献：**
1. **首个同时实现"非刚性编辑 + 内容一致性 + 免训练"的方法**——此前要么免训练但只能刚性编辑（P2P/PnP/SDEdit），要么能非刚性但需逐图微调（Imagic）。
2. **互注意力（mutual self-attention）机制**：把"在交叉注意力上做文章"的主流范式转向**自注意力**——用目标 Query 查源图 K/V，让源图内容成为"生成素材"。这是一个简洁而有效的洞察。
3. **精确的"何时何层"控制策略**：揭示并利用"早期步定布局、解码器层载内容"的扩散规律（EDIT 函数 + S/L 阈值），是本方法 work 的关键。
4. **从交叉注意力免费提取掩码**做前后景解耦，零额外分割模型。

**影响：**
- 成为"训练免费注意力操控编辑/一致性生成"路线的**经典基线与组件**，被大量后续一致性生成、角色一致、参考图编辑工作引用与复用。
- 其"互注意力/共享 K-V"思想被广泛迁移到**视频生成（跨帧共享注意力保时序一致）、多图一致性、风格/身份保持**等场景。
- 工程上易插拔（diffusers AttnProcessor），可与 ControlNet/T2I-Adapter/SDXL/DreamBooth 组合，落地门槛低（单 16GB GPU、秒级）。

**已知局限（论文 Sec. 6 明确）：**
1. 强依赖 SD 用目标 prompt 合成出合理布局——**SD 若生成不出目标布局/形状，MasaCtrl 即失败**（可用 ControlNet/Adapter 缓解但仍可能失败）。
2. **当目标图含源图中不存在的内容**（如源图没有手掌、目标要"鼓掌"），无从查询 → 产生伪影。
3. 即便高度相似，编辑图与源图仍存在**细微差异**（如鸟喙颜色）。
4. **视频扩展只能让前景动、背景几乎静止**，无法生成有背景动态的场景——这是该方法用于视频的显著短板。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2304.08465
- arxiv_pdf: https://arxiv.org/pdf/2304.08465
- iccv_2023_cvf: https://openaccess.thecvf.com/content/ICCV2023/papers/Cao_MasaCtrl_Tuning-Free_Mutual_Self-Attention_Control_for_Consistent_Image_Synthesis_and_ICCV_2023_paper.pdf
- github: https://github.com/TencentARC/MasaCtrl
- project_page: https://ljzycmd.github.io/projects/MasaCtrl/
- hf_model_assets: https://huggingface.co/TencentARC/MasaCtrl
- hf_demo: https://huggingface.co/spaces/TencentARC/MasaCtrl

## 本地落盘文件
- ../../../sources/omni/2023/arxiv-2304.08465.pdf  （arXiv v1 预印本全文，含方法/消融/失败案例）
- ../../../sources/omni/2023/masactrl-iccv2023.pdf  （ICCV 2023 camera-ready，含 Table 1 定量与用户研究——arXiv v1 缺此表）
- ../../../sources/omni/2023/masactrl--readme.md  （官方 GitHub README：实现细节、checkpoint、SDXL/T2I-Adapter 用法、ICCV bibtex）
