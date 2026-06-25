---
title: "ModelScopeT2V（ModelScope Text-to-Video Technical Report）"
org: "Alibaba Group / DAMO Academy"
country: China
date: "2023-08"
type: tech-report
category: video
tags: [text-to-video, latent-diffusion, spatio-temporal, unet3d, open-source, webvid, vqgan]
url: "https://arxiv.org/abs/2308.06571"
arxiv: "https://arxiv.org/abs/2308.06571"
pdf_url: "https://arxiv.org/pdf/2308.06571"
github_url: "https://github.com/modelscope/modelscope"
hf_url: "https://huggingface.co/damo-vilab/text-to-video-ms-1.7b"
modelscope_url: "https://modelscope.cn/models/damo/text-to-video-synthesis/summary"
project_url: "https://modelscope.cn/studios/damo/text-to-video-synthesis/summary"
downloaded: [arxiv-2308.06571.pdf, modelscope-t2v--hf-card.md, modelscope-t2v--modelscope-card.md, modelscope-t2v--model-index.json, modelscope-t2v--unet-config.json]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
ModelScopeT2V 是阿里达摩院 2023 年 8 月发布的**首个开源 diffusion 文生视频模型**：在 Stable Diffusion（图像 LDM）基础上插入"时空块（spatio-temporal block）"扩展出时序建模能力，总参数 1.7B（其中 0.5B 专用于时序），用图文+视频文本**多帧联合训练**抗灾难性遗忘。在 MSR-VTT zero-shot 上取得 FID-vid 11.09 / FVD 550（均为当时最好），CLIPSIM 0.2930，与 Make-A-Video、Imagen Video 等闭源 SOTA 同档甚至局部更优，且代码/权重/在线 demo 全开放，成为开源社区最早被广泛使用的 t2v baseline。

## 背景与定位
2023 年视频生成的主要矛盾：训练难、易产生保真度低与运动不连续的视频；同时**领域内没有公开可用的代码库**——图像生成已被 [[latent-diffusion-ldm]] / Stable Diffusion 推动得很成熟，但视频生成还没享受到开源红利。ModelScopeT2V 的定位就是给社区一个"简单、易训练、可复现"的视频生成基线。

它在技术脉络上的位置：
- **继承图像 LDM**：直接从 Stable Diffusion v2.1 的 VQGAN（VAE）与 UNet 初始化空间部分，把成熟的 [[latent-diffusion-ldm]] 范式迁移到视频。
- **时序扩展走"在 2D UNet 上插时序层"路线**：与同期 Make-A-Video（off-the-shelf T2I + 时空分解扩散，无需配对视频文本）、Imagen Video（视频生成 + 级联超分，T5 文本编码器）、Align-Your-Latents（[[align-your-latents-vldm]]，把图像 LDM 时序对齐）、MagicVideo、VideoFusion（同组工作，分解 base+residual 噪声）等并列，但 ModelScopeT2V 的卖点是**全开源 + 工程极简**。
- **两点技术贡献**：①架构上的 spatio-temporal block；②预训练上的 multi-frame training（图文与视频文本联合）。

相对前置工作的改进：不像 Make-A-Video 用 image CLIP embedding（导致运动信息偏弱），ModelScopeT2V 直接在像素/潜空间联合学习文图对应，论文称其生成的视频运动幅度更大；相对 Imagen Video 没有大 T5、没有级联超分、数据量更小，分辨率与细节逊色，但作者明确定位为"baseline + 未来改进的地基"。

## 模型架构
**整体三件套（约 1.7B 参数）**：文本编码器 τ + VQGAN（VAE）+ 去噪 UNet。
- **潜空间与 VQGAN**：沿用 VQGAN（论文记为 VQGAN，diffusers 集成为 `AutoencoderKL`），压缩因子 8，把 256×256 RGB 帧编码为 32×32×4 的潜变量；逐帧编码 `Z0 = [E(f1),…,E(fF)]`，解码同理逐帧 `v = [D(z1),…,D(zF)]`。**VQGAN 在训练/推理中全程冻结**，从 Stable Diffusion v2.1 初始化。
- **文本编码器**：用预训练 CLIP ViT-H/14（OpenCLIP）把 prompt 编码为 `c ∈ R^{Np×Nc}`；最大 token 长 Np=77。论文正文写嵌入维 Nc=768，但**实际发布的 diffusers 检查点 `cross_attention_dim=1024`**（OpenCLIP ViT-H/14 文本输出确为 1024 维），以发布权重为准。仅支持英文输入。
- **去噪 UNet（核心，UNet3D）**：模型绝大多数参数集中于此。diffusers 实现为 `UNet3DConditionModel`，4 级下/上采样：`block_out_channels=[320,640,1280,1280]`，`down_block_types` 为 3 个 `CrossAttnDownBlock3D` + 1 个 `DownBlock3D`，对称 4 个上采样块；`layers_per_block=2`，`attention_head_dim=64`，激活 SiLU，GroupNorm(32)。UNet 由四类块组成：initial block（投影到嵌入空间）、downsampling block、**spatio-temporal block**、upsampling block。
- **文本条件注入**：在 spatial attention 中以文本嵌入 c 作为多头注意力的 key/value 做 cross-attention，使中间特征对齐语言-视觉。

**关键创新——Spatio-temporal block（时空块）**：把卷积与注意力沿空间/时间分解（factorize），每块含四类子模块，默认数量 (N1,N2,N3,N4)=(2,4,2,2)：
- **空间卷积** N1=2：3×3 2D CNN，逐帧在 H/8×W/8 潜特征上提空间特征。
- **时序卷积** N2=4：kernel=3 的 1D CNN，沿 F 帧维度卷积建立帧间相关。N2=4 层使每个时空块的时序局部感受野达 81，足够覆盖 16 帧输出。
- **空间注意力** N3=2：两种实例化——一个是文本-视觉的 cross-attention，一个是纯视觉自注意力做空间建模；帧在空间尺度展平。
- **时序注意力** N4=2：均为自注意力；把不同帧同位置的变量分组到一起做时序注意。

**参数分布**：UNet 共 1345M 参数，其中时序卷积+时序注意力共 **552M（占 UNet 的 39%）**专用于时序建模——这与摘要"0.5B 参数专用于时序能力"一致。整模型（含 VQGAN + 文本编码器）≈1.7B。

**可变帧数**：UNet 结构对任意帧长自适应——一张图可视为帧长为 1 的视频，这是后面 multi-frame training 与"长视频生成"的结构基础。

## 数据
- **图文对**：LAION-5B 的 `LAION2B-en` 英文子集（模型只吃英文）；HF model card 还列出 ImageNet 作为补充图像数据。
- **视频文本对**：WebVid（约 1000 万视频文本对，多数分辨率 336×596，单段约 30 秒）。训练时取中间正方形区域，**随机抽 16 帧、3 fps**作为训练数据。
- **配比**：视频数据规模比图文小几个数量级；为同时利用两者，采用 multi-frame training——**1/8 的 GPU 跑图文对，其余 7/8 跑视频文本对**（详见训练方法）。
- **清洗/过滤（model card 披露）**：预训练后做美学评分（aesthetic score）、水印评分（watermark score）、去重（deduplication）过滤。论文正文未给更细的过滤阈值/留存比例 → 此处工程细节**未披露**。
- **评测集（不参与训练）**：MSR-VTT，10k 视频每段 20 句标注；FID-vid/FVD 用随机抽的 2048 段、CLIPSIM 用全 test split 约 6 万句 prompt。

## 训练方法
- **生成目标**：标准 DDPM ε-prediction。前向加噪 T=1000 步，损失为预测噪声与真噪声的 MSE：`L = E[ ||ε_gt − ε_θ(Z_t, c, t)||²]`。
- **多阶段/初始化**：空间部分（VQGAN + UNet 的 2D 通路）从 Stable Diffusion v2.1 初始化；**时序卷积与时序注意力的输出层初始化为零**——使训练初期 ModelScopeT2V 退化为逐帧图像生成（有意义但时序不连续），随训练逐步学到帧间对应、产出连续视频。这是"zero-init 时序层"的经典稳定化技巧。
- **Multi-frame training（核心训练贡献）**：只在视频文本对上训会损害语义多样性并造成图像域知识的灾难性遗忘；因此让 **1/8 GPU 训图文对（图像=帧长 1 的视频）、7/8 GPU 训视频文本对**，靠结构对任意帧长的自适应实现混合训练，既保住 SD 的图像语义又学到时序。
- **关键超参**：优化器 AdamW，学习率 5×10⁻⁵；**80GB NVIDIA A100** 上训练；图像 batch size 1400、视频 batch size 3200；共训 **26.7 万（267k）迭代**。
- **采样**：训练用 DDPM(T=1000)；推理默认 DDIM sampler + classifier-free guidance、50 步（diffusers 默认 pipeline 用 `DDIMScheduler`，model card 示例用 `DPMSolverMultistepScheduler` 25 步）。输出分辨率统一 256×256，16 帧。
- **消融结论**：作者发现时序卷积或时序注意力单独都能增强时序能力（呼应 VideoCrafter 只用时序注意力），但**两者同时用时序建模更优**；并观察到时序卷积层数越多时序越好，故取 N2=4；不同帧数设置下无需改参数范围。
- 论文**未做** SFT / 偏好对齐（RLHF/DPO/reward model）/ 蒸馏加速（consistency/LCM/ADD）——这些当时尚未引入该模型，属未涉及。

## Infra（训练 / 推理工程）
- **训练算力**：80GB A100 GPU（论文未给具体卡数与 GPU·时总量；只说 1/8 vs 7/8 的 GPU 分工与上述 batch/迭代数）→ 总算力规模**未披露具体数字**。
- **并行/混合精度/吞吐**：论文未报告分布式并行策略、混合精度、吞吐 → **未披露**。
- **推理/部署形态**：
  - ModelScope 框架 + HuggingFace diffusers（`TextToVideoSDPipeline`）双路集成，已上线 ModelScope Studio 与 HF Space 在线 demo，提供 Colab。
  - Demo 资源需求：约 **16GB CPU RAM + 16GB GPU RAM**（ModelScope card）；fp16 权重发布。
  - **长视频生成**：开启 attention slicing + VAE slicing + Torch 2.0，可在 <16GB 显存生成最长约 25 秒（示例 `num_frames=200`）的视频——靠 UNet 对任意帧长自适应实现。
- 推理加速（量化/缓存/步数蒸馏）论文未涉及；社区后续用 DPMSolver 把步数压到 25。

## 评测 benchmark（把效果讲清楚）
**MSR-VTT zero-shot**（ModelScopeT2V 未在 MSR-VTT 训练；输出 256×256、取中间 16 帧 @3fps）三指标对比（FID-vid↓ / FVD↓ / CLIPSIM↑，源自论文 Table 1）：

| 模型 | FID-vid ↓ | FVD ↓ | CLIPSIM ↑ |
|---|---|---|---|
| NÜWA | 47.68 | — | 0.2439 |
| CogVideo (Chinese) | 24.78 | — | 0.2614 |
| CogVideo (English) | 23.59 | 1294 | 0.2631 |
| MagicVideo | — | 1290 | — |
| Video LDM | — | — | 0.2929 |
| Make-A-Video | 13.17 | — | 0.3049 |
| **ModelScopeT2V (ours)** | **11.09** | **550** | 0.2930 |

要点：
- **FID-vid 11.09 与 FVD 550 均为表中最佳**——表明生成视频在视觉分布上最接近真实视频（FVD 550 远低于 CogVideo 的 1294 与 MagicVideo 的 1290）。
- CLIPSIM 0.2930，仅略低于 Make-A-Video 的 0.3049，与 Video LDM(0.2929)持平；作者指出 Make-A-Video 额外用了 HD-VILA-100M 数据，故其语义对齐略高情有可原。
- 表中部分单元格为空（论文未给该模型对应指标），如实标注为"—"，**未报告**。

**定性对比**：与 Make-A-Video 比，ModelScopeT2V 的"robot/dog"更真实、运动幅度更大（归因于图文联合训练增强了文-视觉对应；Make-A-Video 用 image CLIP embedding 导致运动偏弱）。与 Imagen Video 比，Imagen 更生动细致（归因于 T5 文本编码器 + 更大基模 + 更大数据），ModelScopeT2V 内容达意但细节偏糙——作者坦承差距并归因于规模与数据。

**已知短板（model card）**：达不到影视级画质；无法生成清晰文字；仅英文；复杂组合生成（compositional）能力待提升；输出受 WebVid 训练分布影响（如水印倾向）。

## 创新点与影响
**核心贡献**：
1. **首个开源 diffusion 文生视频模型**，代码/权重/在线 demo 全开放，填补了视频生成"没有公开代码库"的空白。
2. **Spatio-temporal block**：在图像 UNet 上以分解式（2D 空间 + 1D 时序，卷积 + 注意力共四子模块）插入时序建模，时序层零初始化保证训练稳定——成为"图像 LDM → 视频"最朴素有效的范式之一。
3. **Multi-frame training**：图文（帧长 1）与视频文本按 1:7 的 GPU 配比联合训练，缓解灾难性遗忘、保住语义多样性。

**影响**：
- 作为社区**最早被广泛使用的 t2v baseline**，被 diffusers 原生集成（`text-to-video-ms-1.7b` / `UNet3DConditionModel`），催生大量下游：sd-webui-text2video、Text-To-Video-Finetuning 等社区项目，以及短视频创作应用。
- 直接连接同组后续工作：[[align-your-latents-vldm]] 式时序对齐思路、VideoComposer（可控视频合成）、VideoFusion（分解噪声）、I2VGen-XL 等达摩院视频生成线均与之同源。
- 为 2023–2024 "图像扩散模型加时序层做视频" 这一主流路线提供了开源参照系，直到 DiT 化的视频模型（如后来的 Sora 路线）才逐步取代该 UNet3D 范式。

**已知局限**：256×256 低分辨率、16 帧短时长、细节粗糙、仅英文、无超分级联、无 SFT/偏好对齐/蒸馏加速；复杂组合与文字渲染弱。作者展望方向：引入多条件（Composer 式）/ LoRA 控制、生成更长更富语义的视频。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2308.06571
- arxiv_pdf: https://arxiv.org/pdf/2308.06571
- hf (model card): https://huggingface.co/damo-vilab/text-to-video-ms-1.7b
- hf (upstream damo card): https://huggingface.co/damo-vilab/modelscope-damo-text-to-video-synthesis
- modelscope (model): https://modelscope.cn/models/damo/text-to-video-synthesis/summary
- modelscope (studio demo): https://modelscope.cn/studios/damo/text-to-video-synthesis/summary
- github (ModelScope): https://github.com/modelscope/modelscope

## 本地落盘文件
- ../../../sources/omni/2023/arxiv-2308.06571.pdf
- ../../../sources/omni/2023/modelscope-t2v--hf-card.md
- ../../../sources/omni/2023/modelscope-t2v--modelscope-card.md
- ../../../sources/omni/2023/modelscope-t2v--model-index.json
- ../../../sources/omni/2023/modelscope-t2v--unet-config.json
