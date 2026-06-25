---
title: "Prompt-to-Prompt Image Editing with Cross Attention Control"
org: "Google Research / Tel Aviv University"
country: US
date: "2022-08"
type: paper
category: edit
tags: [diffusion, image-editing, cross-attention, training-free, text-to-image, attention-injection, imagen, stable-diffusion]
url: "https://arxiv.org/abs/2208.01626"
arxiv: "https://arxiv.org/abs/2208.01626"
pdf_url: "https://arxiv.org/pdf/2208.01626"
github_url: "https://github.com/google/prompt-to-prompt"
hf_url: ""
modelscope_url: ""
project_url: "https://prompt-to-prompt.github.io/"
downloaded: [arxiv-2208.01626.pdf, prompt-to-prompt--readme.md, prompt-to-prompt--project-page.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Prompt-to-Prompt（P2P）发现文生图扩散模型里的**交叉注意力图（cross-attention maps）编码了图像空间布局**，提出在去噪过程中把源图的交叉注意力图**注入**到改写 prompt 的生成里——从而**只改文字、不画 mask、不训练、不微调、不优化**就能局部/全局编辑图像并保持原结构。是 training-free 扩散编辑的开山之作（Null-text Inversion、pix2pix-zero 等一系列工作的源头）。论文为定性方法论文，**未报告任何 FID/CLIP 等定量指标**。

## 背景与定位
2022 年大规模文生图模型（[[imagen]]、[[dall-e-2]]、[[parti]]）生成质量爆发，但**缺乏可控编辑**：哪怕只改一个词，固定随机种子重新生成也会得到完全不同结构的图（论文 fig.2 底排：同种子 "lemon cake"→"pumpkin cake" 结构全变）。当时主流编辑方案 [[glide]]、[[blended-diffusion]] 都要求用户**手画 mask** 做 inpainting——既繁琐，又因抹掉 mask 区域而丢失原结构信息（无法只改纹理而保形状）。少数无 mask 方法（VQGAN-CLIP、Text2LIVE）要么只能全局改、要么需为每张图单独训网络。

P2P 的核心命题：**编辑的本质是"保留大部分原图"**，而扩散模型的结构信息恰好藏在交叉注意力里。作者把这一观察变成一个**完全 training-free、几乎零额外算力**的推理时干预手段，第一次实现"纯文本驱动、保结构"的扩散编辑。技术脉络上承 [[ddpm]] / [[ddim]] / [[classifier-free-guidance]]，下启 [[null-text-inversion]]（同组紧接着的真实图反演工作）。

## 模型架构
P2P **本身不是一个模型**，而是嫁接在**预训练文生图扩散模型**上的推理算法，不改任何权重。

- **论文骨干**：[[imagen]]（Google 闭源）。Imagen 由 3 个文条件扩散模型级联——64×64 文生图 + 两级超分（64→256、256→1024）。P2P **只在 64×64 文生图阶段干预**（因为构图/几何主要在此分辨率确定），超分链路原样使用。
- **干预点——交叉注意力**：每个去噪步 U-Net 用交叉注意力把视觉特征与文本嵌入融合。query 来自噪声图深层特征 φ(z_t)（投影 ℓ_Q），key/value 来自文本嵌入 ψ(P)（投影 ℓ_K、ℓ_V）。注意力图 M = Softmax(QKᵀ/√d)，其中 cell M_{ij} 表示第 j 个 token 对像素 i 的权重；输出 φ̂(z_t)=M·V。P2P 的关键洞见：**M 编码了"哪个像素该长成哪个词描述的样子"**，即空间布局。fig.4 可视化显示 "bear" 的像素高亮在熊身上、"bird" 高亮在鸟身上，且**结构在去噪早期步就已确定**。
- **Imagen 的混合注意力（hybrid attention）**：Imagen 部分层把文本嵌入拼到 self-attention 的 key-value 上，同时充当 self+cross。P2P **只干预其中对应文本 token 的通道**（即混合注意力的 cross 部分），self 部分不动。Imagen 64×64 模型在分辨率 [16,8] 用 cross-attention、在 [32,16,8] 用 hybrid attention（见论文附录 A.2）。
- **公开实现的骨干差异（重要）**：官方 GitHub 代码**没有用 Imagen**（闭源），而是基于 huggingface/diffusers 在 **Latent Diffusion（[[latent-diffusion-ldm]]，CompVis/ldm-text2im-large-256）和 Stable Diffusion v1.4** 上复现，text encoder 为 CLIP/BERT 系。代码在 Tesla V100 16GB 上测试，**≥12GB 显存**即可跑。

## 数据
**无训练，无数据集**。P2P 不消耗任何训练/微调数据、不需额外标注或合成数据——这正是其"training-free / no extra data"卖点的一部分。所用的全部"数据"就是用户给的**源 prompt P、目标 prompt P\* 和一个随机种子 s**（真实图编辑时再加一张输入图，见下）。

## 训练方法
**不训练、不微调、不优化**（论文反复强调 "does not require model training, fine-tuning, extra data, or optimization"）。方法是一个推理时的注意力注入算法（论文 Algorithm 1）：

- **总流程**：对源 prompt P 和目标 prompt P\* **用同一随机种子并行跑两条扩散链**。每个去噪步取出源链的注意力图 M_t 和目标链的 M\*_t，用一个 `Edit(M_t, M\*_t, t)` 函数算出注入图 M̂_t，再把 M̂_t 覆盖回目标链该步的注意力（但保留目标 prompt 的 value V）。整个过程相对原始单次推理**只多一步开销**（两条链可同 batch 并行）。固定随机性是前提（否则同 prompt 两个种子也会差异巨大）。
- **三种 Edit 算子**：
  1. **Word Swap（换词，AttentionReplace）**：如 "a big red bicycle"→"...car"。直接把源图注意力 M_t 注入目标链。但全程注入会过约束几何（"car" 被强行长成 bicycle 形状），故引入**软约束阈值 τ**：`Edit = M\*_t if t<τ else M_t`——即**只在前若干步（构图阶段）注入源注意力**，之后放手让目标 prompt 自由调整几何。τ 越大保真度越高、对文本忠实度越低（fig.6：0%→100% 注入步数的渐变扫描）。换词 token 数不等时用 alignment 函数对齐（duplicate/average）。
  2. **Adding a New Phrase（加词/精修，AttentionEditRefine）**：如 "a castle next to a river"→"children drawing of a castle...". 用 alignment 函数 A 找出公共 token，**只对公共 token 注入源注意力**，新加 token 自由生成：`Edit = M_t[i,A(j)] if A(j)≠None else M\*_t[i,j]`。用于风格化、加属性、全局光照/季节改动。
  3. **Attention Re-weighting（注意力重加权，AttentionReweight / "fader control"）**：想"加减 fluffiness/雪量"这类难用文字描述的连续控制。对指定 token j\* 的注意力图乘系数 **c∈[−2,2]**，其余不变，实现该词语义影响的连续滑杆放大/减弱。
- **真实图编辑（real image editing）**：要先做**反演（inversion）**找到能重建输入图的初始噪声。论文用基于 **DDIM 的确定性反演**（x_0→x_T 反向跑），但坦承反演不够准、有可见失真（fig.11 失败案例），并指出 **distortion-editability 权衡**（降低 CFG guidance 改善重建但削弱编辑能力）。补救：从注意力图**自动提取 mask**（无需用户画）保护未编辑区域，连朴素 DDPM 加噪反演也能用（fig.12 猫身份保持）。论文明言真实图反演是"orthogonal endeavor"，留给后续——这直接催生了同组的 [[null-text-inversion]]。
- **公开实现的额外旋钮**（README，论文正文未细讲）：`cross_replace_steps`（交叉注意力替换的步数比例，可按词设字典）、`self_replace_steps`（**自注意力**替换比例——实现里也注入 self-attention，正文未强调）、`local_blend`（LocalBlend 对象做局部融合）、`equalizer`（重加权系数向量）。

## Infra（训练 / 推理工程）
- **训练算力**：无（不训练）。
- **推理开销**：相对原模型**仅 +1 步开销**——两条扩散链（源/目标）可放进同一 batch 并行；注意力注入可在 forward 内联，省掉显式的第二次前向（Algorithm 1 注释）。
- **部署形态**：官方提供 Jupyter notebook（`prompt-to-prompt_ldm.ipynb` / `prompt-to-prompt_stable.ipynb`），基于 PyTorch 1.11 + diffusers，Python 3.8。硬件门槛低：测试于 **Tesla V100 16GB**，**≥12GB VRAM** 可用——这也是它能迅速被社区/diffusers 集成、爆火的工程原因。
- 论文未报告 Imagen 推理的具体吞吐/步数等数字（**未披露**）。

## 评测 benchmark（把效果讲清楚）
**论文未做任何定量评测**——无 FID、CLIPScore、GenEval、人评 ELO 等任何指标，**全部以定性图例呈现**（这是该方向早期方法论文的常态，源里没有就是没有，不编造）。具体展示：

- **保结构编辑**（fig.2）：注入注意力时 "lemon cake"→16 种 cake（pumpkin/pasta/lego/brick…）布局与背景一致；不注入（仅同种子）则结构全变 ⇒ 证明注意力图=结构载体。
- **结构性修改**（fig.6）：能把 bicycle 改成 car/airplane/train（不止改纹理），并用注入步数比例换取保真度↔文本忠实度的连续权衡。
- **单物体保留**（fig.5）：只注入 "butterfly" 的注意力，蝴蝶外形不变而上下文（花/草/蛋糕/披萨…）任意替换。
- **风格化与全局编辑**（fig.7、8）：加 "watercolor/oil painting/snowy/at sunset" 等做全局改动而保留构图；草图→写实。
- **Fader 连续控制**（fig.9）：用 c∈[−2,2] 连续调 "birthday / blossom / snowy / fluffy" 程度（fig.9 实例；附录 fig.15 另有 "smiling teddy bear" 等）。
- **真实图编辑**（fig.10–12）：DDIM 反演 + P2P 编辑真实照片，并展示反演失败案例与注意力 mask 补救。

**关键消融式结论（定性）**：(1) 不注入注意力 → 换一词即整图崩（必要性）；(2) 注入步数 τ 控制 distortion↔editability；(3) 注意力在去噪早期就锁定构图。

## 创新点与影响
**核心贡献**：
1. **机理发现**：首次系统揭示文生图扩散模型的**交叉注意力图 = 像素-词语的空间绑定图**，是可解释、可操纵的"结构旋钮"。
2. **training-free 编辑范式**：仅靠注意力注入即实现保结构编辑，**零训练/零微调/零额外数据/零优化/无 mask**，开销近乎免费（+1 步）。
3. **三种通用算子**（换词/加词/重加权）+ 注入步数 τ 软约束 + fader 连续控制，覆盖局部、结构、全局、风格、强度多种编辑。
4. **从注意力自动抽 mask** 保护未编辑区，免去用户画 mask。

**影响**：成为 training-free 扩散编辑的奠基工作与事实标准模块——
- 直接催生同组 [[null-text-inversion]]（2211.09794，把真实图反演做准，与 P2P 配合编辑真实照片）；
- 被 [[diffedit]]、pix2pix-zero、MasaCtrl、Plug-and-Play 等大量后续 attention-control 编辑工作继承/对比；
- "cross-attention / self-attention 注入"成为 ControlNet 之外的一条主线，并被集成进 huggingface diffusers 生态，是面试/综述里"扩散编辑"绕不开的基线。

**已知局限**（作者自述）：
- 真实图依赖反演，DDIM 反演有可见失真、且需用户自己想出贴切的源 prompt（复杂构图难）；
- 交叉注意力位于网络瓶颈层、**分辨率低**，限制更精细的局部编辑（建议在高分辨率层也加 cross-attention，但需改训练故留待后续）；
- **无法在图中空间平移已有物体**（move object 不支持）。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2208.01626
- arxiv_pdf: https://arxiv.org/pdf/2208.01626
- project_page: https://prompt-to-prompt.github.io/
- github: https://github.com/google/prompt-to-prompt

## 本地落盘文件
- ../../../sources/omni/2022/arxiv-2208.01626.pdf
- ../../../sources/omni/2022/prompt-to-prompt--readme.md
- ../../../sources/omni/2022/prompt-to-prompt--project-page.md
