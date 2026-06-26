---
title: "Tune-A-Video: One-Shot Tuning of Image Diffusion Models for Text-to-Video Generation"
org: "Show Lab (NUS) / Tencent ARC Lab & PCG"
country: China
date: "2022-12"
type: paper
category: video
tags: [video, t2v, video-editing, one-shot, diffusion, fine-tuning, stable-diffusion, ddim-inversion, attention-inflation]
url: "https://arxiv.org/abs/2212.11565"
arxiv: "https://arxiv.org/abs/2212.11565"
pdf_url: "https://arxiv.org/pdf/2212.11565"
github_url: "https://github.com/showlab/Tune-A-Video"
hf_url: "https://huggingface.co/Tune-A-Video-library"
modelscope_url: ""
project_url: "https://tuneavideo.github.io/"
downloaded: [arxiv-2212.11565.pdf, tune-a-video--readme.md, tune-a-video--project-page.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Tune-A-Video 提出 **One-Shot Video Tuning** 新设定：只用**一对文本-视频**就把一个预训练的 T2I 扩散模型（Stable Diffusion）"膨胀"成 T2V 模型，约 10 分钟 A100 微调即可做文本驱动的视频编辑/生成。它是**首个**用预训练 T2I 模型做 T2V 的框架，开创了"扩散 + DDIM inversion"做视频编辑这一方向；在 DAVIS 评测上帧一致性 CLIP Score 92.40 / 文本对齐 27.58，均超过 CogVideo 与 Plug-and-Play 两个基线。

## 背景与定位
2022 年底，T2I 已被 [[latent-diffusion-ldm]]（Stable Diffusion）、Imagen、DALL·E 2 等推到很高水平，但 T2V 仍受困于两点：缺乏高质量大规模文本-视频数据，以及对时间一致性建模的复杂性。当时主流 T2V（Make-A-Video、Imagen Video、CogVideo、MagicVideo、Gen-1、Dreamix）几乎都走"在 WebVid-10M 这类大规模文本-视频数据上从头/继续训练时空模型"的范式，算力昂贵、耗时，且很多模型与数据不开放。

作者类比人类的"举一反三"能力——看过一段"a man skiing on snow"，人就能想象 panda 如何滑雪。于是提出一个反直觉的问题：**预训练 T2I 能否仅从单条视频样本推断出其他新视频？** 由此定义 One-Shot Video Tuning：只给一对文本-视频，训练一个 T2V 生成器，要求它捕捉输入视频的运动信息，再用编辑后的 prompt 合成新视频。

两个关键观察支撑方法（论文 Fig.2）：
1. **关于运动**：T2I 模型能生成准确反映动词（verb）的静态图，例如"a man is running"会画出在跑（而非走/跳）的瞬间——说明 cross-attention 已能正确 attend 到动词，做"静态运动"生成。
2. **关于一致对象**：把 T2I 里的空间 self-attention 从单图扩展到多图（spatio-temporal attention），并行生成连续帧时，能得到跨帧一致的同一个人、同一片沙滩——说明 self-attention 层是由**空间相似性**而非像素位置驱动的。

相比前置工作的改进：相对基于 Layered Neural Atlases 的 Text2Live（生成一个 atlas 约需 10 小时、编辑能力受限）和逐帧编辑的 Plug-and-Play（无时间感知、帧间闪烁），Tune-A-Video 每段视频仅需约 10 分钟训练 + 1 分钟采样，且天然兼容 [[dreambooth]]、T2I-Adapter、ControlNet 等个性化/可控 T2I 生态。

## 模型架构
**Backbone：把 2D LDM(Stable Diffusion) U-Net 膨胀(inflate)到时空域**，不引入新的大模块，核心是三处注意力改造。

T2I 的 U-Net 由 2D 卷积残差块 + transformer 块组成，每个 transformer 块含：空间 self-attention + cross-attention(图文对齐) + FFN。膨胀做法：
- **伪 3D 卷积**：仿 VDM，把 3×3 卷积核替换为 1×3×3，即在时间维只做退化卷积（不跨帧混合，仅扩到 3D 张量形状）。
- **新增 Temporal Self-Attention (T-Attn)**：在每个 transformer 块追加一层时间自注意力做时间建模。
- **Spatio-Temporal Attention (ST-Attn)**：由原空间 self-attention 扩展而来，是本文核心设计。

**ST-Attn —— 稀疏因果时空注意力**：朴素地做 full attention 或 causal attention 的复杂度均为 O((mN)²)（m 帧、每帧 N 个 token），帧数增大不可行。作者改成**稀疏版因果注意力**：第 i 帧的 query 只看**第一帧 v₁** 和**前一帧 v_{i-1}** 两帧的 key/value：
- Q = W^Q · z_{v_i}
- K = W^K · [z_{v₁}, z_{v_{i-1}}]（拼接）
- V = W^V · [z_{v₁}, z_{v_{i-1}}]

复杂度降到 **O(2m·N²)**（对帧数线性）。投影矩阵 W^Q/W^K/W^V 在时空上共享。第一帧提供全局锚定、前一帧提供局部连续性。

**条件注入 / text encoder / VAE**：完全沿用 Stable Diffusion 自身组件——CLIP text encoder 给 cross-attention 提供文本条件 c=ψ(P*)，VAE 把像素压到 latent（D(E(x))≈x），扩散在 latent 空间进行。本文未替换或重训这些模块。

**分辨率与帧数**：论文实验取 512×512、采样 32 帧（5.1 节）；开源实现默认按 24 帧训练（README），可减少 n_sample_frames 以适配显存。基座沿用 CompVis/stable-diffusion-v1-4 公开权重，膨胀只追加伪 3D 卷积 + 时间自注意力、不引入大规模新模块；**论文未给出参数量数字**（SD v1-4 U-Net 约 8.6 亿参数是社区常引数据，非本文报告）。

## 数据
**这是本工作最特殊之处：不依赖大规模文本-视频数据集训练，每个模型只用"一对文本-视频"做 one-shot 微调。**

- **基础模型的图像数据**：间接来自 Stable Diffusion 在 LAION-5B 上的预训练（本文不重训，直接用 CompVis/stable-diffusion-v1-4 公开权重）。
- **微调数据**：单条输入视频 V（512×512、采样 32 帧或开源 24 帧）+ 一条源 prompt P。源 prompt 的"视频文案"用 **BLIP-2 自动生成 caption**，再人工设计编辑 prompt。
- **评测数据**：从 DAVIS 数据集选 **42 段代表性视频**（涵盖动物、车辆、人类等，附录 Tab.2 列出全部 42 个 clip 名，如 bear/blackswan/boat/car-turn/dog/...）；对每段视频用 BLIP-2 自动生成 caption，再**人工为每段设计 3 条编辑 prompt，共 140 条编辑 prompt**，覆盖 object editing、background change、style transfer 三类应用。
- 无清洗/配比/re-captioning/合成数据/美学安全过滤等大规模数据工程（因为根本不做大规模训练），这些维度对本工作**不适用**。

## 训练方法
**训练目标**：标准 LDM 扩散去噪损失，无任何新损失。即 E_{z,ε~N(0,1),t,c}‖ε − ε_θ(z_t, t, c)‖²₂，c 为文本条件嵌入。

**One-Shot 微调（高效注意力调参，关键 trick）**：不更新全部参数（全调会破坏 T2I 预训练知识、且贵），只更新注意力块里少量投影矩阵：
- **ST-Attn 层**：固定 W^K、W^V，**只更新 W^Q**（因为 K/V 来自其他帧，作为"被查询"的参照应保持稳定）。
- **T-Attn 层**：**整层全部微调**（这是新加的层，需要从头学时间建模）。
- **Cross-Attn 层**：只更新 query 投影 W^Q，用于精炼图文对齐。

直觉：固定 K/V 投影 = 保留 T2I 对开放域概念的既有知识；只动 query = 让模型学会"如何从已有特征里查询出时间一致的内容"。这比 DreamBooth 式全参微调高效得多，同时保住预训练性质。

**推理：DDIM inversion 提供结构引导（关键 trick）**：只微调注意力会让帧间空间一致，但缺乏对像素位移的控制，生成"原地不动/循环停滞"的视频。解决：推理时对源视频 V 做**无文本条件的 DDIM inversion**（DDIM 采样的逆过程）得到 latent 噪声，以此作为 DDIM 采样的初始噪声，再用编辑 prompt T* 引导采样：
- V* = D( DDIM-samp( DDIM-inv(E(V)), T* ) )
- 同一输入视频只需做一次 inversion。inverted latent 携带源视频的结构/运动信息，使输出视频时间连贯、运动平滑。
- 采样用 DDIM sampler + classifier-free guidance。

**关键超参（论文）**：微调 500 步，学习率 3×10⁻⁵，batch size 1。**未使用 flow matching / 蒸馏 / RLHF / DPO / reward model / consistency-LCM** 等（2022 年底，这些尚未成为标配；本工作也无此需求）。

**开源实现超参（README，与论文略有出入，属工程默认）**：24 帧视频通常 300~500 步、单 A100 约 10~15 分钟；推理 num_inference_steps=50、guidance_scale=12.5、fp16。

## Infra（训练 / 推理工程）
- **算力**：单条视频微调约 **10 分钟（论文，32 帧 / 500 步）**或 **10~15 分钟（README，24 帧 / 300~500 步）**，**单张 NVIDIA A100**；采样约 **1 分钟/视频**。对比：HPVAE-GAN 单视频要训 8 天、Text2Live 生成 atlas 约 10 小时，本方法快几个数量级。
- **并行/分布式/混合精度/吞吐**：无多卡分布式（单视频单卡即可）；开源用 `accelerate launch` 训练、推理 `torch.float16`。
- **显存优化（README）**：强烈建议装 **xformers**（`enable_xformers_memory_efficient_attention=True` 默认开）提速省显存；推理用 **VAE slicing**（`enable_vae_slicing()`）；显存不足可减帧数。
- **部署形态**：基于 HuggingFace **diffusers** 实现；提供 Colab demo、HuggingFace Spaces（Training-UI / inference gradio demo，hysts 贡献）、预训练 Tune-A-Video 模型上传到 HF `Tune-A-Video-library`。代码 Apache-2.0，Python 88.3% / Jupyter 11.7%，约 4.4k stars / 390 forks。
- 无量化/步数蒸馏等推理加速（推理本就只 1 分钟）。

## 评测 benchmark（把效果讲清楚）
**评测集**：42 段 DAVIS 视频 + 140 条编辑 prompt（自建 benchmark）。

**自动指标定义**：
- **Frame Consistency（帧一致性）**：对输出视频所有帧计算 CLIP 图像嵌入，报告所有帧对的平均余弦相似度。
- **Textual Faithfulness（文本对齐）**：输出视频所有帧与对应编辑 prompt 的平均 CLIP score。

**定量对比（论文 Tab.1，三个方法）**：

| 方法 | Frame Consistency CLIP Score | Frame Consistency 用户偏好 | Textual Alignment CLIP Score | Textual Alignment 用户偏好 |
|---|---|---|---|---|
| CogVideo | 90.64 | 12.14 | 23.91 | 15.00 |
| Plug-and-Play | 88.89 | 37.86 | 27.56 | 23.57 |
| **Tune-A-Video** | **92.40** | 87.86* / 62.14** | **27.58** | 85.00* / 76.43** |

（用户偏好列：* = Tune-A-Video vs CogVideo，** = Tune-A-Video vs Plug-and-Play 的对比胜率。）

**结论**：Tune-A-Video 在帧一致性(92.40)和文本对齐(27.58)两项 CLIP 指标上**均优于**两个基线；CogVideo 帧一致但文本对齐差，Plug-and-Play 文本对齐尚可但帧间不一致——本方法两头都好。

**用户研究**：5 名标注者(主要为高校学生/同事)对每条 prompt、随机顺序展示两方法视频，问"哪个时间一致性更好""哪个更符合文本"，多数投票。结果如上表用户偏好列，Tune-A-Video 在两维度上对两基线均高偏好。

**基线**：① CogVideo（在 540 万 caption 视频上训练、可 zero-shot 文本直生视频）；② Plug-and-Play（逐帧独立编辑的 SOTA 图像编辑模型）；③ Text2Live（基于 layered neural atlases 的文本引导视频编辑，仅做定性对比 Fig.7/12，未进定量表）。

**消融结论（Fig.8/13）**：
- **w/o ST-Attn**：内容跨帧显著不一致（滑雪者衣服颜色都在变）。
- **w/o inversion**：内容一致但**复刻不了运动**（滑雪动作丢失），视频"停滞"。
- **w/o finetuning**：靠 ST-Attn + inversion 仍能保内容一致，但连续帧运动不平滑、视频闪烁。
- 三个设计缺一不可。

**未报告**：FID、GenEval、T2I-CompBench、DPG-Bench、VBench、ImageReward/PickScore/HPSv2 等本工作均**未报告**（2022 年底这些视频/T2I benchmark 多数尚未出现或不适用，论文只用 CLIP Score + 用户研究）。

**局限（Fig.9）**：输入视频含**多个对象且有遮挡**时易失败（如两只 panda 会"糊"到一起），源于 T2I 模型处理多对象/对象交互的固有局限；作者建议未来用 depth 等额外条件区分对象。

## 创新点与影响
**核心贡献**：
1. 提出 **One-Shot Video Tuning** 新任务设定——只用单对文本-视频训练 T2V 生成器，免去大规模视频数据训练负担。
2. **首个**用预训练 T2I 模型做 T2V 生成/编辑的框架（Tune-A-Video）。
3. **高效注意力微调**（只调 ST-Attn 的 W^Q + 整层 T-Attn + Cross-Attn 的 W^Q）+ **结构反演**（DDIM inversion 提供结构引导），显著提升时间一致性。
4. 天然兼容个性化/可控 T2I 生态：DreamBooth（风格/主体个性化视频）、T2I-Adapter、ControlNet（如 pose 控制），零额外训练成本。

**影响**（注：以下"后续工作/竞赛"为外部背景，非本文落盘源所述）：
- 开创了"**膨胀预训练 T2I + DDIM inversion**"做视频编辑这一范式，成为后续大量 training-free / one-shot 视频编辑工作（如 Video-P2P、FateZero、vid2vid-zero、ControlVideo 等）的直接先驱与常用基线。
- 发表于 **ICCV 2023（pp.7623-7633，据 project page bibtex）**，开源代码约 4.4k stars / 390 forks（README），成为 diffusion 视频编辑领域影响力很大的早期工作之一；亦常被关联到 CVPR 2023 的 LOVEU-TGVE 文本引导视频编辑竞赛（此关联为外部信息，未在落盘源核实）。
- 证明了"T2I 的 self-attention 由空间相似性驱动、可低成本扩到时空"这一洞见（论文 Fig.2 两点观察），影响了后续时空注意力设计。

**已知局限**：
- 仍需**逐视频微调**（10~15 分钟/条），非纯 training-free、非实时；后续工作朝零训练方向演进。
- 多对象 + 遮挡场景易失败（继承 T2I 缺陷）。
- 受限于稀疏 ST-Attn 只看首帧+前帧，长视频/大运动一致性仍有挑战；运动主要靠源视频 inversion"借"来，难生成与源视频结构差异很大的全新运动。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2212.11565
- arxiv_pdf: https://arxiv.org/pdf/2212.11565
- github: https://github.com/showlab/Tune-A-Video
- project_page: https://tuneavideo.github.io/
- hf_library: https://huggingface.co/Tune-A-Video-library
- hf_demo: https://huggingface.co/spaces/Tune-A-Video-library/Tune-A-Video-Training-UI

## 一手源存档（sources/）
- [arxiv-2212.11565.pdf](https://arxiv.org/pdf/2212.11565)  （arXiv 原文 PDF，不入 git）
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2022/tune-a-video--readme.md)
- [project-page.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2022/tune-a-video--project-page.md)
