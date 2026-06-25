---
title: "HyperHuman: Hyper-Realistic Human Generation with Latent Structural Diffusion"
org: "Snap Inc. / CUHK / HKU / NTU"
country: US
date: "2023-10"
type: paper
category: t2i
tags: [human-generation, latent-diffusion, structural-diffusion, controllable-generation, depth-normal, joint-denoising, pose-conditioned, snap, iclr2024]
url: "https://arxiv.org/abs/2310.08579"
arxiv: "https://arxiv.org/abs/2310.08579"
pdf_url: "https://arxiv.org/pdf/2310.08579"
github_url: "https://github.com/snap-research/HyperHuman"
hf_url: ""
modelscope_url: ""
project_url: "https://snap-research.github.io/HyperHuman/"
downloaded: [arxiv-2310.08579.pdf, hyperhuman--readme.md, hyperhuman--project-page.md]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
HyperHuman 是 Snap 联合港中文/港大/南洋理工提出的**高真实感人体文生图框架**（ICLR 2024），核心创新是用一个统一 U-Net **同时去噪 RGB、深度、法线**三路（Latent Structural Diffusion），把"外观纹理"与"隐式几何结构"在一个网络里联合建模，从而生成解剖结构连贯、姿态自然的人像；在 MS-COCO 人像零样本评测上 FID 17.18（较第二名降 25.2%）、FIDCLIP 7.82（降 31.5%），并配套发布 **3.4 亿（340M）**带姿态/深度/法线标注的人体数据集 HumanVerse。

## 背景与定位
当时的通用 T2I 模型（[[stable-diffusion-1]]、[[dall-e-2]]）尽管整体质量很高，却**普遍画不好人**——胳膊腿数目错乱、姿态扭曲，根因在于"人"是带非刚性形变的关节体，所需的结构信息很难仅靠文本 prompt 描述。

把结构控制引入扩散生成的两条既有路线都有局限：
- **旁路适配器**（[[controlnet]]、T2I-Adapter）：在冻结的预训练 U-Net 上挂一个可学习分支注入控制信号。问题是主干与辅助分支特征存在差异，导致控制信号（如骨架图）与生成图不一致。
- **通道拼接**（HumanSD）：直接把骨架图按通道拼进 U-Net 输入。问题是局限于艺术风格、多样性受限，且只用了姿态一种结构、忽略深度/法线。

HyperHuman 的关键 insight：**人体图像在多粒度上天然结构化**——从粗粒度的骨架到细粒度的空间几何（深度/法线）。要生成连贯自然的人像，必须在**同一个模型里捕捉"显式外观"与"隐式结构"之间的多层关联**，而不是把不同控制信号当作彼此独立的旁路引导。它把 [[latent-diffusion-ldm]] 的去噪范式从"只去噪 RGB"扩展成"RGB+深度+法线联合去噪"，是 2023 年人像生成方向的代表作，作者自称"人体生成基座模型的最早尝试之一"。

## 模型架构
整体是**两阶段管线**：第一阶段 Latent Structural Diffusion（G1）联合去噪出对齐的 RGB/深度/法线；第二阶段 Structure-Guided Refiner（G2）把预测出的结构图作为条件，合成更高分辨率的精细图。推理时只需文本 prompt + 骨架，用户也可自带深度/法线条件喂给 G2。

**第一阶段 Latent Structural Diffusion Model G1**（基于 SD-2.0-base）：
- **同时去噪三个模态**：在同一个 U-Net 里对 RGB 图 x、深度 d、法线 n 三路联合去噪（条件为 caption c + 骨架 p）。这是论文的核心——把外观、空间关系、几何统一建模，每路互为补充（结构感知 + 纹理丰富）。
- **结构专家分支（Structural Expert Branches）+ 共享主干**：把 U-Net 的 `conv_in`、第一个 DownBlock、最后一个 UpBlock、`conv_out` **为每个模态各复制一份**作为"专家分支"，中间的大部分 block 共享；每个分支的 skip-connection 单独维护。设计逻辑：输入端各分支把不同域的噪声 latent 映射到相近分布以便在共享主干里融合特征，输出端再分发回各分支预测各自噪声，保证三路空间对齐。共享层数是个 trade-off——共享越多输出越对齐，但各分支参数不足以刻画各模态分布；共享越少则跨模态特征融合不够。消融证明"复制 conv_in/首 DownBlock/末 UpBlock/conv_out"为最优（FID 17.18，优于"半个 block"22.85 与"两个 block"17.94）。该设计可平凡推广到任意数量的成对分布，只需加分支、计算开销很小。
- **架构超参（Tab.6）**：激活 SiLU；Block Out Channels [320,640,1280,1280]；Cross-Attention 维度 1024；Attention Head Dim [5,10,20,20]；DownBlock 结构 ["CrossAttn"×3,"ResBlock"×1]；text encoder 用 **OpenCLIP ViT-H**；分辨率 512×512。
- **参数量未单独披露具体数字**，但论文明确说 SDXL 用了"两个 text encoder + 3 倍更大的 U-Net、更多 cross-attention 层"才在 CLIP 对齐上更强，言下之意 HyperHuman 第一阶段主干量级与 SD 2.x 同级（约 0.9B U-Net 量级，论文未明确给数）。

**第二阶段 Structure-Guided Refiner G2**（基于冻结的 SDXL-1.0-base）：
- **多条件统一合成**：把 caption c、骨架 p、预测深度 d̂、预测法线 n̂ 四种控制信号在训练阶段统一注入（不像 ControlNet/T2I-Adapter 一次只能处理单一条件）。
- **轻量条件 embedder**：每个条件先从输入尺寸（如 1024×1024）投影到 SDXL latent 尺寸（128×128），各经一个由 4 层堆叠卷积（4×4 kernel、2×2 stride、ReLU）的轻量 embedder 编码；各分支 embedding **逐坐标相加**后送入 SDXL Encoder Blocks 的可训练拷贝。加新结构条件只引入一个极小 encoder，开销可忽略。
- text encoder 用 **CLIP ViT-L + OpenCLIP ViT-bigG**（SDXL 原配双编码器）；分辨率 1024×1024。

## 数据
配套构建大规模人体数据集 **HumanVerse（340M 图像）**，是论文的另一大贡献：
- **来源**：从 [[laion-5b]]（LAION-2B-en）与 COYO-700M 两个公开图文数据集中筛人体子集。最终 COYO 子集 90,948,474 张（91M，占全集 18.12%）、LAION-2B 子集 248,396,109 张（248M，占全集 20.77%），合计约 340M。
- **过滤清洗**：用 YOLOS 做人体检测，**只保留含 1–3 个人体框、且人体面积占比 >15% 的图**；剔除美学分 <4.5、分辨率 <200×200 的样本。相比只训全身人像简单背景的既有做法，覆盖更广（含各种背景、局部人体如衣物/四肢）。
- **标注（三类结构 + caption）**：
  - **2D 姿态**：用 MMPose 框架 + **ViTPose-H** 标注 per-instance 框、关键点坐标与置信度，含全身/身体/手部/面部关键点。
  - **深度 + 法线**：用 **Omnidata** 估单目深度与法线，并按 depth-to-image 管线额外用 **MiDaS** 标注深度。
  - **caption**：licence 列表显示用 **BLIP2-OPT-2.7B** 做图像描述（re-captioning）。
- **Outpaint 提升标注准确性**：因为现成结构估计器多在"完整视图"上训练，团队先用 **SD-2-inpainting** 把每张图向外 outpaint 补全更完整的人体视图，再跑深度/法线估计——但**只采用原始图像区域内的标注**，避免 outpaint 区域伪影污染。
- **标注算力**：整个标注流程用 **640 张 16/32GB V100、并行跑两周**。

## 训练方法
- **训练目标 = v-prediction**（Salimans & Ho 2022）。一阶段把 SD-2.0-base 从 ε-prediction **微调整个 U-Net 到 v-prediction**；二阶段把 SDXL-1.0-base 冻结、微调 refiner 到 ε-prediction。
- **联合学习的两个关键 trick（核心方法）**：
  1. **改进的噪声调度（消除低频泄漏）**：深度/法线是单调图（局部值相近，深度 [0,1]、法线单位向量），普通噪声调度会在训练时泄漏每通道均值这类低频信号，且其 latent 分布与 RGB 不同。做法是先把深度/法线 latent **归一化到接近 RGB latent 的分布**（复用预训练去噪先验），并强制 **zero terminal SNR（αT=0, σT=1）** 消除结构图低频信息。消融显示这一步关键——去掉后 FID 从 17.18 退化到 17.70 且对齐误差变差。
  2. **三路共用同一 timestep t**：若给每个模态采不同 t（如 UniDiffuser 做法），在总步数 T=1000、三模态下每种扰动组合只有 10⁻⁹ 概率被采到，太稀疏学不好；改为**所有模态密集共用同一 t**，模态再多采样稀疏度与学习难度也不增加，且同噪声水平下中间特征分布相近、在共享主干里融合得更好。消融里"不同 timestep"是所有设定中最差的（FID 29.36 vs 17.18）。
- **二阶段鲁棒条件 = Random Dropout**：两阶段管线的隐患是误差累积（G1 预测的深度/法线带伪影，引起 train-test gap）。做法是训练时**随机 mask 掉任一控制信号**（文本换空串、结构图换零值图），让模型不依赖单一引导、均衡各条件影响。条件 dropout 率：一阶段 15%、二阶段 50%。消融显示去掉 dropout 后 FID 从 12.38 退化到 25.69。
- **优化器/超参**：AdamW，lr=1e-5，weight decay=0.01，betas=(0.9,0.999)，warmup steps=0，batch size=2048，训练步数 T=1000，基于 HuggingFace diffusers 实现。训练时对 RGB/深度/法线统一 resize + random-crop 到各阶段目标分辨率，并把原图高宽 + crop 坐标按类似 time embedding 的方式嵌入（借鉴 SDXL 的 size/location conditioning）。
- **未涉及**：无 RLHF/DPO/reward model 偏好对齐；无 consistency/LCM/ADD 步数蒸馏（推理仍走标准 50 步 DDIM）。

## Infra（训练 / 推理工程）
- **训练算力**：一阶段 Latent Structural Diffusion 在 **128 张 80GB A100** 上、batch 2048、训练 **一周**（512×512）；二阶段 Structure-Guided Refiner 在 **256 张 80GB A100**、batch 2048、训练 **一周**（1024×1024）。数据标注另用 640 张 V100 跑两周。
- **小规模验证**：正式大训前先在 ~1M 子集（<全集 3%）上验证方法有效性，用 **8 张 40GB A100 一天**即可联合去噪出对齐的多模态结果。
- **可选优化方向（论文 A.8 列出，未实测）**：换更小骨架（Small SD / Tiny SD）省训练/显存；用 LoRA/Adapter 高效微调共享主干；gradient checkpointing、梯度累积、DeepSpeed 模型并行、fp16、xformers 等工程手段降显存。
- **推理**：标准 DDIM 50 步、CFG scale 默认 7.5（评测时 7.0–8.0 为常用区间）。**具体推理延迟/吞吐/量化未报告**；代码仓库 README 仅含 abstract + citation，**未公开训练/推理代码与权重**（截至论文发布）。

## 评测 benchmark（把效果讲清楚）
**零样本评测集**：从 MS-COCO 2014 validation 过滤出 8,236 张清晰可见人体的图，全部 resize+center-crop 到 512×512。数值比较用第一阶段 RGB 输出（512×512），第二阶段 refiner 仅用于可视化。

**主表（Tab.1，零样本 MS-COCO Human，CFG=7.5）**——HyperHuman 在图像质量与姿态精度上全面领先：
- **FID 17.18**（第二名 SD 2.0 是 22.98 → 降 **25.2%**）
- **KID×1k 4.11**（第二名 T2I-Adapter 7.98 → 降 **48.5%**）
- **FIDCLIP 7.82**（第二名 T2I-Adapter 11.95 → 降 **31.5%**）
- **CLIP Score** 排第二（SDXL 因双 text encoder + 3 倍大 U-Net 在文本对齐上更强；HyperHuman 与同量级 text encoder 的基线相比仍最优）
- 姿态精度（AP/AR/APclean/ARclean）领先 ControlNet、T2I-Adapter、HumanSD（HyperHuman APclean 38.84、ARclean 48.70，均为最佳行）

**人类偏好相关指标（Tab.4）**——HyperHuman 均最优：
- PickScore：偏好 HyperHuman 比例 vs SD2.1 66.87%、vs SDXL 52.11%、vs IF 63.37%、vs ControlNet 74.47%、vs T2I-Adapter 83.25%、vs HumanSD 87.18%（>50% 即更优）
- HPS V2 绝对分：HyperHuman **0.2905**，高于 SD2.1(0.2772)/SDXL(0.2832)/IF(0.2849)/ControlNet(0.2783)/T2I-Adapter(0.2732)/HumanSD(0.2656)。（论文坦言这两个偏好模型偏向 1024 高分合成图、对真实图打分偏低，故提升看似 marginal。）

**用户研究（Tab.3 偏好率 / Tab.8 计分）**——偏好 HyperHuman 的比例：vs SD2.1 89.24%、vs SDXL 60.45%、vs IF 82.45%、vs ControlNet 92.33%、vs T2I-Adapter 98.06%、vs HumanSD 99.08%；细分计分如 vs HumanSD 8160:76、vs T2I-Adapter 8076:160。

**关键消融结论**：
- 联合去噪有效：仅去噪 RGB(FID 21.68) → +Depth(19.89) → 三路全 + 最优专家分支(17.18)；
- 专家分支层数 trade-off：半个 block 太对齐但参数不足(22.85)，两个 block 融合不够(17.94)，"一个 block"最优(17.18)；
- 噪声调度：zero-terminal SNR 关键（去掉退化到 17.70），不同 timestep 严重伤害(29.36)；
- Refiner 条件消融（512×512 toy，Tab.7）：随条件叠加 FID 单调下降，d+n(12.42) 优于单条件，去掉 random dropout 退化到 25.69。

## 创新点与影响
**核心贡献**：
1. **Latent Structural Diffusion**——首次在统一 U-Net 里**同时去噪 RGB + 深度 + 法线**，用"结构专家分支 + 共享主干"在一个模型内联合建模外观、空间关系、几何，且三路空间对齐。这套"统一模型多模态联合去噪 + 专家分支"思路可推广到任意成对分布。
2. 针对单调结构图量身定制的训练 trick：**zero-terminal SNR 噪声归一化 + 三路共用 timestep + v-prediction**，解决了深度/法线低频泄漏与多模态采样稀疏问题。
3. **HumanVerse 340M 人体数据集**——带姿态/深度/法线/caption 的综合标注，作者定位为"人体生成基座模型的早期尝试"，为后续人像/数字人研究提供数据基础。
4. **Structure-Guided Refiner**——多条件统一注入 + random dropout 鲁棒条件，缓解两阶段误差累积，且加新条件几乎零开销。

**影响**：作为 2023 末人像生成代表作，把"显式外观 × 隐式结构联合建模"作为提升人体真实感的范式确立下来；其"在生成图的同时预测对齐的深度/法线几何"思路，与后续"RGBX/几何感知生成""3D 人体生成"方向相通（作者团队同期还有 HumanGaussian 等 3D 人体工作）。

**已知局限（论文自述）**：
- 受限于现成 pose/depth/normal 估计器在 in-the-wild 人体上的精度，**细节如手指、眼睛偶尔仍画不好**；
- 当前管线**仍需输入骨架**，未来可探索用 LLM 等先验做 text-to-pose 实现纯文本驱动；
- 偏好类指标偏向高分辨率合成图，评测有偏；
- 代码/权重未随论文开源（GitHub 仅占位）。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2310.08579
- arxiv_pdf: https://arxiv.org/pdf/2310.08579
- project_page: https://snap-research.github.io/HyperHuman/
- github: https://github.com/snap-research/HyperHuman （README 仅 abstract + citation，未释出代码/权重）
- short_demo: https://www.youtube.com/watch?v=eRPZW1pwxog
- long_demo: https://www.youtube.com/watch?v=CxGfbwZOcyU

## 本地落盘文件
- ../../../sources/omni/2023/arxiv-2310.08579.pdf
- ../../../sources/omni/2023/hyperhuman--readme.md
- ../../../sources/omni/2023/hyperhuman--project-page.md
