---
title: "图像编辑与可控生成族横向对比：从 ControlNet/InstructPix2Pix 到 Kontext/Step1X/Qwen-Edit"
type: source
created: 2026-06-25
updated: 2026-06-25
tags: [image-editing, controllable-generation, controlnet, instruction-editing, personalization, inversion, attention-control, unified-editing, diffusion, flux, deep-dive]
---

# 图像编辑与可控生成族横向对比

> 本页横向梳理 2022–2026 视觉生成里"可控注入 + 编辑"这一大族：把"在哪、长什么样、改成什么"从文字里解放出来。脉络是**四条主线 + 一次收敛**——(1) 可控注入（空间条件→冻结底模）；(2) 指令编辑（说人话改图）；(3) 个性化（把"我的主体/风格"塞进模型）；(4) inversion/attention 编辑（免训练操控真实图）；(5) 2023 末起这四条线在**统一编辑模型**（Emu-Edit→Kontext/Step1X/Qwen-Edit）里收敛。所有数字均引自单工作页（slug 内链可点开核对）。

---

## 0. 一张总图：四条线的范式分裂

2022 年 8 月是这族的"创世周"——同一个月里 [[textual-inversion]]、[[dreambooth]]、[[prompt-to-prompt]] 三篇并发砸下来，分别奠定了**个性化（改嵌入 vs 改权重）**和**免训练注意力编辑**两大范式；三个月后 [[instructpix2pix]] 开创**指令编辑**；半年后 [[controlnet]] 开创**可控空间注入**。这族的核心矛盾贯穿始终：

- **改不改底模权重**：ControlNet/DreamBooth 加可训练参数 vs P2P/Null-text 纯推理期操控；
- **要不要 mask**：早期 inpainting 要画 mask vs InstructPix2Pix/P2P 无 mask；
- **保真度↔可编辑性权衡（distortion–editability tradeoff）**：几乎每篇都在这条曲线上找点（Textual Inversion 用学习率当旋钮、P2P 用注入步数 τ、IP-Adapter 用 λ、InstructPix2Pix 用双 CFG scale）；
- **专才 vs 通才**：每条件一个 ControlNet vs UniControl/Uni-ControlNet 单模型多条件 vs 最终的统一编辑大模型。

下表先给全族 26 个工作的硬指标速查，后文逐线展开机制。

---

## 1. 可控空间注入：冻结底模 + 适配器加条件

### 1.1 范式确立——零卷积 vs 轻量适配器（2023-01 ~ 02 三子星）

2023 年初三篇并发工作奠定"**冻结大文生图模型 + 外挂可训练模块注入空间条件**"的范式，差异全在"怎么把条件喂进 U-Net"：

- **[[controlnet]]**（Stanford，2023-02，ICCV'23 Marr Prize）：把 SD U-Net 的**编码器 + 中间块克隆一份可训练副本**（约半个 U-Net 的参数量），用**零初始化 1×1 卷积（zero convolution）**接回冻结底模——训练第一步 `y_c=y`，底模行为完全不变，亿级预训练 backbone 不被随机梯度毁掉。最硬的工程结果：深度 ControlNet 仅用 **20 万样本 + 单张 RTX 3090Ti + 5 天**，在用户研究里与"千 GPU-时、1200 万图"训练的工业级 SD2-Depth **几乎无法区分（辨别精度 0.52±0.17，约等于瞎猜）**。零卷积梯度论证（初始 `∂y/∂x=0` 保护 backbone、`∂y/∂W=x≠0` 保证能学）+"突变收敛（通常 <1 万步在某步突然学会跟随条件）"是它的标志洞察。代价：每条件单训一个 ControlNet，且每去噪步都要跑一遍 ControlNet+U-Net。

- **[[t2i-adapter]]**（腾讯 ARC，比 ControlNet 早 6 天）：只训一个 **~77M / ~300M 存储**的小适配器（4 提取块 + 3 下采样块），在 U-Net **encoder 端**逐尺度相加注入。两个标志 trick：**整个去噪过程只前向一次**（条件特征采样前算好，比 ControlNet 省算力）；**cubic 非均匀时间步采样**（发现主体在早期采样步定型，故提高 t 落早期的概率）。COCO 上 text+segmentation **FID 16.78 / CLIP 0.2652**，比纯 SD（24.68）更低。在 SDXL 上把 1251M 的 ControlNet-SDXL 压到 **79M（参数降 93.69%、存储降 94%）**。它是"轻量/快"路线的代表。

- **[[gligen]]**（UW-Madison/MS，2023-01，CVPR'23）：走 **gated self-attention**——在 SD 的 self/cross-attn 之间插新层，`v = v + β·tanh(γ)·TS(SelfAttn([v, h^e]))`，γ 零初始化。卖点是**开放集（open-set）grounded 生成**：靠"同一文本编码器编码 caption 与 grounded 短语 + 共享文本空间"，仅在 COCO 训练即可 grounding 训练词表外概念，**zero-shot LVIS GLIP-score AP 从全监督 LAMA 的 2.0 提到 11.1**；COCO2017 layout2img FID 21.04 / YOLO-AP 22.4。官方对比指出与 ControlNet 的本质区别：GLIGEN 对条件做**拼接+Transformer**（更通用，能吃 box/参考图等离散条件），ControlNet 对条件做**逐元素求和**（更适合空间对齐条件）。

### 1.2 图像 prompt——解耦交叉注意力（IP-Adapter）

- **[[ip-adapter]]**（腾讯 AI Lab，2023-08）把同一适配器哲学推到"**图像 prompt**"。诊断核心病根：原 cross-attention 的 K/V 是为文本训练的，把图像特征拼进去会丢图像专有信息。解法是**解耦交叉注意力**——给图像特征单独开一条 KV 分支（每层只多 Wk′/Wv′），输出与文本注意力直接相加。仅 **22M 参数**，COCO 上 CLIP-I=0.828 / CLIP-T=0.588，**碾压同类 adapter**（Uni-ControlNet Global 0.736 / T2I-Adapter Style 0.648 / ControlNet Shuffle 0.616），且**以 22M 打平/超过 860M~1.2B 的全量微调图像 prompt 模型**（SD unCLIP 0.810、Open unCLIP 0.858）。推理 λ 旋钮平衡图文 prompt。它衍生出 FaceID 系列（弃 CLIP 改 InsightFace face embedding + LoRA），是 InstantID/PhotoMaker 的思想前身。

### 1.3 通才化——单模型多条件可组合

每条件单训一个 ControlNet 在条件数 N 增大时成本线性增长，2023-05 两篇并发工作各给一套"单模型统一多条件"方案：

- **[[uni-controlnet]]**（HKU/MS，NeurIPS'23）：把条件二分为 **local（有空间结构）/ global（无空间结构，如 CLIP 图像 embedding）**，对应**只加 2 个 adapter**（恒定，不随 N 增长）。local adapter 借 SPADE 思路用 **FDN（Feature Denormalization）多尺度注入**（在每个分辨率层级注入，缓解深层信息丢失）；global 把图像 embedding 当扩展文本 token 喂所有 cross-attn。反直觉发现：**分开训练 local/global 即可组合，无需联合微调**（联合训反而让 global 欠学）。只用 1000 万 LAION 图训 1 epoch，COCO 上 Canny-FID 17.79 / HED-FID 17.86，多数条件优于逐条件专训的 ControlNet/T2I-Adapter。

- **[[unicontrol]]**（Salesforce/Stanford，NeurIPS'23）：在 ControlNet 上加 **MOE-style Adapter（去门控硬路由专家卷积，每任务 ~70K）+ task-aware HyperNet（任务指令文本调制 zero-conv，"control over control"）**，把 9 类条件压进 **~1.5B 单模型**——等价于把 SD+9 个 ControlNet（~4.3B）压缩近 3 倍。16× A100 训约 5000 GPU-时（≈各 ControlNet 总成本）。感知距离上 5/6 任务优于专训 ControlNet（Depth 25.5→21.3 提升最明显），且能 zero-shot 到去模糊/上色/修复。配套开源 **MultiGen-20M** 数据集（>2000 万三元组）。

> **可控注入这一线的收敛点**：ControlNet 的零卷积、T2I-Adapter 的轻量+一次前向、GLIGEN 的 gated 注入、IP-Adapter 的解耦 cross-attn，共同成为后续所有"给冻结底模加条件"工作的标准模块；Uni-ControlNet/UniControl 的 local/global 二分 + MoE-adapter 思路则被 2025 年统一编辑模型继承（Qwen-Image-Edit-2509 的原生 ControlNet、SeedEdit 3.0 的 task embedding 都是其延伸）。

---

## 2. 指令编辑：对图片说人话就能改图

### 2.1 开山——跨模态大模型合成监督（InstructPix2Pix）

- **[[instructpix2pix]]**（UC Berkeley，2022-11，CVPR'23 Highlight）开创"**指令式编辑**"：一张图 + 一句动作指令（"Turn him into a cyborg"），**单次前向、无 mask、无反演、无逐图微调**完成。最深远的贡献是**数据生成而非模型结构**——用微调 GPT-3 生成"指令+改前/改后 caption"三元组（**454,445** 条），再用 **SD + [[prompt-to-prompt]]** 把每对 caption 变成像素一致的改前/改后图（公开发布 CLIP 过滤版 313,010 对）。模型仅在 SD U-Net 第一层卷积加输入通道（zero-init）拼接源图，**10,000 步微调（8×A100，25.5 小时）**即成。另一标志贡献是**双条件 CFG**——图像 scale `s_I` 与文本 scale `s_T` 两个旋钮（推荐 `s_T∈[5,10]`、`s_I∈[1,1.5]`）连续调节"保真↔编辑强度"，成为后续编辑模型的标准做法。短板：空间推理/计数弱（移动、交换位置都做不了），视觉天花板锁死在 SD v1.5。

### 2.2 数据线——从合成银标到人工金标，再到百万级真实锚点

InstructPix2Pix 后整条"指令编辑"线的进步主要是**数据进步**：

- **[[magicbrush]]**（OSU/Waterloo，2023-06，NeurIPS'23 D&B）：**首个万级人工金标**——10,388 个 (源图,指令,目标图) 三元组（源图取自 COCO，工人用 DALL·E 2 编辑器标注，含单/多轮 × 有/无 mask 四设定）。证明**少量金标微调即大幅超越在 31 万合成数据上训练的原模型**：InstructPix2Pix 微调后 CLIP-I 从 0.8524→0.9332、DINO 0.7428→0.8987，人评一致性多选最优从 33%→51%。从此 MagicBrush test 成为编辑领域事实标准评测集。但暴露了**自动指标与人评不一致**（Text2LIVE 自动分高却人评垫底）。

- **[[instructdiffusion]]**（MSRA，2023-09）：把指令式像素操作从"语义编辑"泛化到**全部视觉任务**（检测/分割/关键点/编辑/低层视觉），三类输出统一进 RGB（半透明 0.5 掩码做分割、彩色圆点做关键点）。核心假设："**详细自然语言指令（而非任务名指示符）是泛化到未见任务的关键**"——消融显示换成"semantic segmentation"式指示符后性能崩塌（关键点 COCO 71.2→22.7）。48×V100 训 4 天，未见的动物关键点 AP-10K 15.9（超 Painter 15.3），HumanArt 51.4（超 Painter 12.4）。

- **[[mgie]]**（Apple/UCSB，2023-09，ICLR'24 Spotlight）：**首个用 MLLM 改进指令编辑**——用 LLaVA-7B 把含糊指令在线改写成"视觉感知的简洁富表达指令"，再经 8 个 `[IMG]` token + 4 层编辑头注入 SD。zero-shot MagicBrush 上 DINO 从 71.46→82.22、CTS 29.34→30.40，且单图推理仅 ~9 秒。关键对照 LGIE（纯语言改写，无视觉感知）全场被 MGIE 压制——**视觉感知是决定性因素**。

- **[[ultraedit]]**（PKU/BIGAI/THU，2024-07，NeurIPS'24 D&B）：把数据推到 **~410 万样本**。三件套创新：(1) **真实图像锚点**——用 SDEdit 把真实图注入 T2I 生成，系统性抑制纯生成数据的域偏置（消融证明只有用锚点时 scaling 才奏效）；(2) **首个大规模 region-based 编辑数据（108K）**；(3) **SDXL-Turbo（2-4 步）+ P2P 把数据生产提速 ~100×**。结果硬核：**仅 3M 数据训练的 SD1.5 在 Emu Edit Test 的 CLIPdir 上达 0.1076，超过用私有 1000 万数据训练的 Emu Edit（0.1066）**；MagicBrush 单轮 CLIP-I 0.9307 / DINO 0.8982。

> **指令编辑线的脉络**：InstructPix2Pix（合成银标 + 双 CFG）→ MagicBrush（人工金标 + 评测标准）→ InstructDiffusion/MGIE（泛化到全视觉任务 / 引入 MLLM 理解）→ UltraEdit（真实锚点 + 区域掩码 + 百万级）。每一步都在补"数据质量+多样性"，模型结构基本沿用 InstructPix2Pix 的"通道拼接源图 + 双 CFG"，直到 2025 年 MLLM 深度接入才换骨架。

---

## 3. 个性化：把"我的主体/风格"塞进模型

### 3.1 两条奠基路线（2022-08 双子星）

- **[[textual-inversion]]**（Tel Aviv/NVIDIA，2022-08）：3–5 张图，**只优化一个新"伪词"嵌入向量 v\***（不动任何模型权重），存盘仅几 KB。关键发现："**单个 word embedding 足以编码独特概念**"，其语义重建质量在 CLIP 空间上与"直接采样训练集真图"相当。用 GAN inversion 视角系统消融，反而证明多向量/正则化等套路都无用——朴素单向量最优。短板：优化慢（单概念约 2 小时，2×V100 5000 步），难精确还原形状。

- **[[dreambooth]]**（Google/BU，2022-08，CVPR'23）：与 TI 相反——**全量微调模型权重**，用罕见 token `[V]` 把主体植入模型**输出域**而非仅文本嵌入空间，故保真上限更高。首次发现扩散微调的**语言漂移（language drift）**并用**类别先验保持损失（PPL）**——拿模型自生成的类别样本反向监督自己——对抗它。DreamBench（30 主体）上 DINO 0.696 / CLIP-I 0.812，大幅超 Textual Inversion（0.569/0.780），用户研究主体保真 **68% vs 22%**。代价：每主体存整套权重（>1GB），这正是后来 LoRA 化的动因。

### 3.2 提速线——从分钟级到免微调（encoder-based）

DreamBooth/TI 都要"每概念在线优化"，三篇工作把它搬到离线：

- **[[hyperdreambooth]]**（Google，2023-07）：用 HyperNetwork（ViT-H 编码器 + Transformer 解码器，**首次把 Transformer 解码器用作 HyperNetwork**）从单张脸直接**预测**一套极小权重（LiDB：在 rank-1 LoRA 上再做正交基分解，仅 **~30K 变量、约 120KB**，比 DreamBooth 小 ~10000×），再用**秩松弛快速微调（首个 rank-relaxed LoRA，仅 40 步）**补细节。单图约 **20 秒**（比 DreamBooth 快 25×），Face Rec. 0.655 / DINO 0.473 全面领先 DreamBooth(0.618/0.441) 与 TI(0.623/0.289)。

- **[[instantbooth]]**（Adobe，2023-04）：**免测试时微调**——可学习图像编码器把概念压成一个文本 token（concept embedding）+ patch 编码器抽 257 visual token 经 zero-init gated adapter 注入。**比 DreamBooth/TI 快约 100×（6 秒 vs ~600/1500 秒）**，person 类 Alignment 0.314（>DB 0.309）、Face dist 1.19（<DB 1.23）。两旋钮 β/α 缓解 concept token 主导 cross-attention 的 language forgetting。只用文本-图像对训练（不用同主体成对图，person 类 1.43M）。

- **[[styledrop]]**（Google，2023-06）：把个性化对象从"主体"换成"**风格**"，且 backbone 选 **[[muse]]（非自回归掩码 Transformer）** 而非扩散。**单张风格图 + <1% 参数（最小 0.23M adapter）**学风格。核心 trick 是**带反馈的迭代训练**（自生成→CLIP/人评筛选→回训，类拒绝采样对齐）抑制内容泄漏。6 风格上 CLIP Style 0.694（vs Muse 基线 0.556、Imagen 上 DreamBooth 0.644），人评风格一致性偏好 **86%** 压过 DreamBooth-on-Imagen。反直觉结论：**离散 token 的 Muse 在少样本风格迁移上比扩散底模更高效**。

> **个性化线的张力**：改嵌入（轻、便携、保真有限）vs 改权重（重、保真高、易过拟）vs 免微调编码器（快、需大规模离线训练）。这条线的"主体/风格一致性"诉求最终在 2025 年统一编辑模型（Kontext 的角色一致性、Qwen-Edit 的 ID 保持）里被重新吸收为"多轮编辑不漂移"。

---

## 4. Inversion / Attention 编辑：免训练操控真实图

### 4.1 机理发现 + 真实图反演（P2P → Null-text）

- **[[prompt-to-prompt]]**（Google/Tel Aviv，2022-08）：**training-free 扩散编辑的开山之作**。核心机理发现——文生图扩散模型的**交叉注意力图编码了图像空间布局**（M_{ij} = 第 j 个 token 对像素 i 的权重，且构图在去噪早期就锁定）。三种算子（换词/加词/重加权）+ 注入步数 τ 软约束 + fader 连续控制，**零训练/零微调/零额外数据/无 mask**，仅 +1 步开销。纯定性论文，**未报告任何定量指标**。真实图编辑需先做 DDIM 反演（坦承有可见失真），这直接催生——

- **[[null-text-inversion]]**（同组，2022-11）：让 P2P 能作用于**真实照片**的关键使能技术。两件套：**Diffusion Pivotal Inversion**（用 w=1 的 DDIM 反演轨迹当枢轴）+ **Null-text Optimization**（只优化 CFG 中的逐时刻无条件 embedding ∅_t，冻结模型权重与条件 embedding）。关键洞察："**CFG 结果高度依赖无条件分支**"——别人都改条件分支，它改无条件分支。重建逼近 VQAE 上界，单图反演约 1 分钟，用户研究 **65.1%** 偏好其编辑（SDEdit 14.5% / Text2Live 16.6%）。

### 4.2 自注意力路线与结构软约束

- **[[masactrl]]**（东京大学/腾讯 PCG，2023-04，ICCV'23）：把注意力操控从 cross-attn 转向 **self-attention**——**互注意力（mutual self-attention）**：保留目标图 Query，把 Key/Value 换成源图自注意力的 Kₛ/Vₛ，让源图内容成为"生成素材"。首个同时实现"**非刚性编辑（改姿态/视角）+ 内容一致 + 免训练**"的方法（此前 P2P/PnP 免训练但只能刚性，Imagic 能非刚性但需逐图微调 14 分钟）。精确"何时何层"控制（默认 S=4 步、L=10 层，只在解码器+若干步后做）。ICCV 版 Table 1：Text-align 0.2793 / Image-align 0.9286 全面领先，用户偏好 **73.5%**（vs Imagic 21.0%），耗时仅 16s。

- **[[pix2pix-zero]]**（CMU/Adobe，2023-02，SIGGRAPH'23）：**training-free + prompt-free** 结构保持编辑。用 GPT-3 生句 + CLIP 均值差**自动发现编辑方向** Δc_edit（免手写 prompt）；**cross-attention guidance**——把原图注意力图当 **L2 软引导**（而非 P2P 的硬替换），在保结构与真编辑间平衡；**autocorrelation 正则化 DDIM 反演**提升可编辑性。cat→dog 上 CLIP-Acc **92.4% / Structure Dist 0.044 / BG-LPIPS 0.182** 全面占优（对比 P2P 因硬约束常"改不动"，horse→zebra CLIP-Acc 仅 18.4%）。还提供 Co-Mod-GAN 蒸馏分支（A100 上 0.018s/图、~3800× 加速）。

### 4.3 效率收尾——完美反演 + 多概念（LEDITS++）

- **[[ledits-pp]]**（TU Darmstadt/HF，2023-11，CVPR'24）：**免微调、免优化、无 mask** 的真实图编辑。核心是把"完美反演（零重建误差）"从 DDPM 推广到高阶 **sde-dpm-solver++**，使整套编辑（反演+生成）仅 **~20 步**完成。三件套：完美反演 + 多概念语义引导（每概念独立引导项，**唯一原生支持多概念隔离编辑**）+ 隐式掩码（交叉注意力 ∩ 噪声图，零额外开销接近 CLIPSeg）。单次编辑仅 **1.78s**（A100），比 DDPM 反演快 6×、比 DDIM 反演快 21×。TEdBench++ 上 SD-XL 取得 **87% 成功率 / LPIPS 0.34**，超过 Imagic 配 Imagen（0.83 SR / LPIPS 0.59）。架构无关（latent 与 pixel 通吃），已并入 diffusers。

> **inversion/attention 线的脉络**：P2P 发现"交叉注意力=布局载体"→ Null-text 把真实图反演做准 → MasaCtrl 转向自注意力做非刚性 → pix2pix-zero 用软约束 + 自动方向 → LEDITS++ 把效率（20 步/1.78s）和多概念做到位。这条线最大价值是**机理与可解释性**（注意力即结构旋钮），其思想被 2025 年的 in-context 编辑（[[in-context-edit-icedit]] 的免训练 diptych）和 Kontext 的"参考 token 拼接"间接继承。

---

## 5. 收敛：统一编辑大模型（2023 末 ~ 2026）

四条线在 2023 末起收敛——**用一个强生成基座 + MLLM 理解 + 大规模/高质量数据**，把"可控注入 + 指令编辑 + 个性化一致性 + 真实图编辑"统进一个模型。

### 5.1 多任务统一的起点（Emu-Edit）

- **[[emu-edit]]**（Meta GenAI，2023-11）：把 **16 种"编辑+识别+生成"任务统一成生成任务**做多任务训练，为每任务学一个 **task embedding** 注入 U-Net 消解指令歧义（推理用 Flan-T5-XL 预测任务下标）。反直觉发现：**加入检测/分割/im2im 等 CV 识别任务能反哺编辑精度**。底座是缩小版 [[emu]]（512×512）。自建 1000 万样本数据集靠 **Grounded Precise Editing**（Grounding-DINO+SAM 预生成精确 mask，四道过滤掉 70% 数据）。自建测试集上 CLIPdir 0.109 / DINO 0.819，人评对 InstructPix2Pix **77.3%** 偏好。还支持 **Task Inversion**（冻结 U-Net 只学新 task embedding，100 样本逼近 10 万样本专家）。开源的 Emu Edit Test Set（test 3589 例）成为标准评测。

### 5.2 字节 SeedEdit 系列（重建↔再生成的平衡）

- **[[seededit]]**（ByteDance，2024-11）：把编辑重新表述为"**重建与再生成之间的最优平衡**"——从弱 T2I 生成器自举编辑配对数据，再**迭代对齐**蒸馏成强编辑器。架构创新是 **Causal Diffusion with Image Input**（共享参数双分支 + 因果自注意力复用 self-attention 注入图像条件，而非加输入通道；丢掉输入分支即退化回 T2I，允许编辑+T2I 混训）。HQ-Edit GPT 分 **78.54**（in-house DiT），超 InstructPix2Pix(47.50)/MagicBrush(47.51)/UltraEdit(54.17)。

- **[[seededit-3-0]]**（ByteDance Seed，2025-06）：底座换成原生 1024 的 [[seedream-3-0]]，两大改进——(1) **meta-info 多源数据混合**（task label / recaption / pixel tagging 三级标签，融合合成/编辑专家/传统算子/视频帧四类异质源）；(2) **diffusion loss + reward loss 联合训练**（一组条件化、时刻感知的专家 reward 模型管人脸 ID/文字/结构，按指令上下文智能开关）。真实图可用率（Usability Rate）从 SeedEdit 1.6 的 **38.4% → 56.1%**，反超 GPT-4o（37.1%）与 Gemini 2.0（30.3%）；蒸馏（Hyper-SD+RayFlow）+量化端到端 **8× 提速**（64s→8s），单图约 10–15s。

### 5.3 In-context 编辑范式（FLUX.1 Kontext / ICEdit）

2025 年两篇把"in-context"思想（参考图当 context token 拼进序列）做成范式：

- **[[flux-1-kontext]]**（Black Forest Labs，2025-05）：统一"生成+指令编辑"的 **rectified-flow DiT**，把参考图经冻结 FLUX autoencoder 编码成 latent token，**简单序列拼接**到目标 token 后（明确试过 channel-wise concat 效果更差），用 **3D RoPE 常数偏移**把 context 块当"虚拟时间步"分开。最大亮点是**多轮编辑的角色一致性**（用 AuraFace 人脸相似度量化，漂移显著慢于 GPT-Image-1/Runway Gen-4），1024 出图 **3–5 秒**（比 GPT-Image 快约 8×/一个数量级）。[pro] 用 LADD、[dev] 12B 用 guidance distillation。Flux-VAE（16 channel）重建 PSNR 31.1 / SSIM 0.896 全面领先 SD3/SDXL VAE。配套 KontextBench（1026 对）。[dev] 开源后成 2025 开源指令编辑事实标杆。

- **[[in-context-edit-icedit]]**（浙大/哈佛，2025-04，NeurIPS'25）：把编辑改写成 **"双拼图（diptych）in-context 生成"**——源图放左半、右半待生成，配固定描述型 IC prompt（把祈使指令包装成"On the right, the scene is exactly the same but {instruction}"）。仅 **5 万训练对（前 SOTA 的 0.1%~0.5%）+ LoRA-MoE（4 专家 r=32，约 214M 可训参数，前 SOTA 的 1%）**，4×A800 训一天。Emu Edit test CLIP-I **0.907 / DINO 0.866 全场最高**，GPT-score 0.68 超所有开源、逼平闭源 Emu Edit(0.72) 但只用 0.5% 数据。**Early Filter 推理时缩放**（6 噪声×10 早期步 + VLM 早过滤选种子）再 +16% VIE-Score，反超商用 SeedEdit（78.2 vs 75.7）。证明"**生成基座足够强时，编辑可退化为轻量适配 + prompt 工程**"。

### 5.4 MLLM 深度接入的开源 SOTA（Step1X-Edit / Qwen-Image-Edit）

- **[[step1x-edit]]**（StepFun，2025-04）：**MLLM 理解→connector→DiT 生成**三段式——Qwen2.5-VL-7B 抽语义（取代 CLIP/T5 浅层编码）+ token refiner 桥接 + 全局引导向量，VAE reference token 经 **token concatenation** 注入 FLUX.1-dev DiT（实读权重：19 double + 38 single block，连接器输入 3584=Qwen hidden、≈12.43B 参数）。自建 20M 数据严格过滤 20:1 到 1M HQ（11 类任务专门工具链）。配套 **GEdit-Bench**（606 真实用户指令、中英双语，VIEScore）成为后续编辑工作标准评测。GEdit-Bench-EN 总分（GPT-4.1）v1.0 6.44 → v1.1 6.97，逼近 Doubao(6.98)、超 Gemini2 Flash(6.51)，与 GPT-4o(7.49) 约 0.5 分差距；CN 上 v1.1 6.983 超 Gemini(5.14)/Doubao(6.84)。

- **[[qwen-image-edit]]**（阿里 Qwen，2025-08）：基于 20B [[qwen-image]] 基座（MMDiT 60 层 + Qwen2.5-VL + Wan2.1-VAE）的编辑版，核心是**双编码（dual-encoding）**——输入图同时喂 **Qwen2.5-VL（语义/指令控制）和 VAE Encoder（外观/像素控制）**，两路互补，使"语义编辑"与"外观编辑"双路成熟。把基座极强的中文文字渲染延伸到"改图里的字"。GEdit-Bench EN/CN 双榜第一（**EN O 7.56、CN O 7.52**，超 GPT Image 1 [High] 的 7.53/7.30、Step1X-Edit 6.97/6.50）；ImgEdit 总分 **4.27**（略高于 GPT Image 1 [High] 4.20）。2509 版加多图编辑（图像拼接训练，最佳 1–3 张）+ 原生 ControlNet + ID/文字一致性增强；社区 Lightning 蒸馏把 NFE 降 25×、整体 42.55× 提速。

---

## 6. 全族横向对比表（数字均引自单页）

| 工作 | 时间 | 机构 | 范式 | 底模/架构 | 可训参数 | 数据规模 | 关键指标（引自单页） |
|---|---|---|---|---|---|---|---|
| [[controlnet]] | 2023-02 | Stanford | 可控注入 | SD1.5/2.1 U-Net + 克隆编码器副本 + zero-conv | ~半个 U-Net | 8万~3M/条件 | 分割 ADE20K FID 15.27；对标 SD2-Depth 辨别 0.52±0.17 |
| [[t2i-adapter]] | 2023-02 | 腾讯 ARC | 可控注入 | SD1.4 + 轻量适配器 | ~77M（SDXL 79M） | COCO 164K~3M | COCO text+seg FID 16.78 / CLIP 0.2652 |
| [[gligen]] | 2023-01 | UW-Madison/MS | grounded 注入 | SD1.4 + gated self-attn | 仅新增层 | O365+GoldG+CC3M | LVIS zero-shot AP 2.0→11.1；COCO17 FID 21.04/AP 22.4 |
| [[ip-adapter]] | 2023-08 | 腾讯 AI Lab | 图像 prompt | SD1.5 + 解耦 cross-attn | **22M** | 10M (LAION+COYO) | COCO CLIP-I 0.828 / CLIP-T 0.588 |
| [[uni-controlnet]] | 2023-05 | HKU/MS | 多条件统一 | SD1.5 + 2 adapter(local/global) | 恒 2 个 | 10M LAION×1ep | Canny-FID 17.79 / HED-FID 17.86 |
| [[unicontrol]] | 2023-05 | Salesforce | 多条件统一 | SD1.5 + MoE-adapter + HyperNet | ~1.5B(含副本) | MultiGen-20M | Depth-FID 25.5→21.3；9 任务压 3× |
| [[instructpix2pix]] | 2022-11 | UC Berkeley | 指令编辑 | SD1.5 U-Net + 通道拼源图 | ≈SD U-Net | 454K(发布313K) | 双 CFG；vs SDEdit 同方向性下一致性更高 |
| [[magicbrush]] | 2023-06 | OSU/Waterloo | 编辑数据/基准 | （微调 IP2P） | — | 10,388 人工 | IP2P 微调后 CLIP-I 0.85→0.93、DINO 0.74→0.90 |
| [[instructdiffusion]] | 2023-09 | MSRA | 通用指令像素 | SD1.5 U-Net | ≈SD U-Net | 关键点245K+分割239K+编辑425K | 关键点 COCO 71.2、AP-10K 15.9、HumanArt 51.4 |
| [[mgie]] | 2023-09 | Apple | MLLM 指令编辑 | LLaVA-7B + SD1.5 | 词嵌入+头+SD | IPr2Pr ~1M | zero-shot MagicBrush DINO 71.46→82.22 |
| [[ultraedit]] | 2024-07 | PKU/BIGAI | 编辑数据 | SD1.5/SDXL/SD3 | ≈基线 | **~410万**(108K区域) | Emu Edit CLIPdir 0.1076 超私有 10M 的 Emu Edit |
| [[dreambooth]] | 2022-08 | Google/BU | 个性化(改权重) | Imagen/SD 全量微调 | 整模型 | 3–5 张/主体 | DreamBench DINO 0.696；保真偏好 68% vs TI 22% |
| [[textual-inversion]] | 2022-08 | Tel Aviv/NVIDIA | 个性化(改嵌入) | LDM(BERT) 词嵌入 | **1 向量(几KB)** | 3–5 张/概念 | 语义重建≈采样真图；单概念 ~2 小时 |
| [[hyperdreambooth]] | 2023-07 | Google | 个性化(预测权重) | SD1.5 + HyperNet | **~30K(120KB)** | CelebA 15K id | Face Rec. 0.655/DINO 0.473；20 秒/快 25× |
| [[instantbooth]] | 2023-04 | Adobe | 个性化(免微调) | SD1.4 + encoder+adapter | encoder FC+adapter | person 1.43M | Align 0.314/Face dist 1.19；6 秒/快 100× |
| [[styledrop]] | 2023-06 | Google | 风格个性化 | **Muse(掩码 Transformer)** + adapter | **0.23M~12.6M** | 单张风格图 | CLIP Style 0.694；人评 86% 压 DreamBooth |
| [[prompt-to-prompt]] | 2022-08 | Google/Tel Aviv | 免训练 attn 编辑 | Imagen/SD（推理算法） | **0（免训练）** | 无 | 仅定性；交叉注意力=布局；+1 步开销 |
| [[null-text-inversion]] | 2022-11 | Google/Tel Aviv | 真实图反演 | SD1.4 + 优化 ∅_t | 仅 ∅_t | 无（COCO 评测） | 重建逼近 VQAE 上界；编辑偏好 65.1% |
| [[masactrl]] | 2023-04 | 东大/腾讯 PCG | 自注意力非刚性编辑 | SD1.4（推理算法） | **0（免训练）** | 无 | Text-align 0.2793/Image-align 0.9286；偏好 73.5% |
| [[pix2pix-zero]] | 2023-02 | CMU/Adobe | 免训练结构保持 | SD1.4（推理算法） | 0（GAN 蒸馏除外） | 无（GAN 用 15K 对） | cat→dog CLIP-Acc 92.4%/StructDist 0.044 |
| [[ledits-pp]] | 2023-11 | TU Darmstadt/HF | 完美反演多概念 | SD/SDXL/IF（架构无关） | **0（免训练）** | 无 | TEdBench++ SR 87%(SDXL)；1.78s/图 |
| [[emu-edit]] | 2023-11 | Meta | 多任务统一编辑 | 缩小版 Emu U-Net(512) | task emb+U-Net | **1000万**(16 任务) | 自建集 CLIPdir 0.109/DINO 0.819；偏好 77.3% |
| [[seededit]] | 2024-11 | ByteDance | 重建↔再生成平衡 | SDXL/in-house DiT + 因果自注意力 | 未披露 | 自举(未披露) | HQ-Edit GPT 78.54（in-house） |
| [[seededit-3-0]] | 2025-06 | ByteDance Seed | reward 对齐编辑 | [[seedream-3-0]](原生1024) + VLM | 未披露 | 多源 meta-info | 可用率 56.1%（超 GPT-4o 37.1%）；8× 提速 |
| [[flux-1-kontext]] | 2025-05 | Black Forest Labs | in-context 统一 | rectified-flow DiT(38 single) | [dev]12B | 数百万对(未披露) | 1024 出图 3–5s；多轮 ID 漂移最慢；VAE PSNR 31.1 |
| [[step1x-edit]] | 2025-04 | StepFun | MLLM→DiT 三段式 | Qwen2.5-VL-7B + FLUX DiT(12.43B) | connector+DiT | 20M→1M HQ | GEdit-EN 6.97(v1.1)；超 Gemini2 Flash 6.51 |
| [[in-context-edit-icedit]] | 2025-04 | 浙大/哈佛 | diptych in-context | FLUX.1 Fill(12B 冻结) + LoRA-MoE | **214M(LoRA)** | **5万** | Emu Edit CLIP-I 0.907/DINO 0.866；VIE 78.2>SeedEdit 75.7 |
| [[qwen-image-edit]] | 2025-08 | 阿里 Qwen | 双编码统一编辑 | 20B MMDiT + Qwen2.5-VL + Wan2.1-VAE | 多任务联训 | 数十亿(基座) | GEdit EN O 7.56/CN 7.52 双榜第一；ImgEdit 4.27 |

---

## 7. 横向对比：机制与评测的几条主线

### 7.1 条件注入方式的演化谱系

把"额外条件怎么进 U-Net/DiT"排成一条谱系，能看清整族的技术连续性：

1. **逐元素求和**（ControlNet zero-conv、T2I-Adapter encoder 端相加）——适合空间对齐条件（边/深度/姿态）；
2. **gated 拼接 + Transformer**（GLIGEN、InstantBooth 的 adapter）——适合离散条件（box/参考图），γ 零初始化保稳定；
3. **解耦 cross-attention 分支**（IP-Adapter 给图像单开 KV）——适合图像 prompt，不挤占文本通道；
4. **通道拼接源图**（InstructPix2Pix/Emu-Edit/InstructDiffusion 在第一层卷积加通道）——指令编辑的标配；
5. **token 序列拼接**（FLUX.1 Kontext / Step1X / ICEdit diptych）——DiT 时代的统一做法，天然支持多图、多分辨率，明确优于 channel concat（Kontext 实验证实）；
6. **双编码并行注入**（Qwen-Image-Edit：VLM 语义流 + VAE 像素流）——2025 年开源 SOTA 的范式，把"理解"和"保真"分到两条路。

注意 **SeedEdit 的因果自注意力**是另一条路——复用 self-attention 双分支通信，丢掉输入分支即退化回 T2I，是"编辑+T2I 混训"的巧设计。

### 7.2 评测体系的代际变迁

- **2022–2023 早期**：P2P/InstructPix2Pix/DreamBooth 多为**定性 + CLIP 双指标 + 用户研究**，P2P 干脆无任何数字。个性化用 DINO/CLIP-I/CLIP-T，编辑用 CLIP image-sim ↔ CLIP direction 的 tradeoff 曲线。
- **2023 中**：[[magicbrush]] 把 **L1/L2/CLIP-I/DINO/CLIP-T** 标准化，成为指令编辑事实基准；[[emu-edit]] Test Set（3589 例）补上真实图覆盖。
- **2024–2025**：转向 **GPT-as-judge**（GPT-4o/GPT-4.1 评 SC/PQ/O），[[step1x-edit]] 的 **GEdit-Bench**（606 真实用户指令、中英双语 VIEScore）和 [[flux-1-kontext]] 的 **KontextBench**（1026 对 + AuraFace 一致性量化）成为新标准。一个反复出现的教训：**自动指标与人评不一致**（MagicBrush 早就发现 Text2LIVE 自动分高人评垫底；MGIE/InstructPix2Pix 都指出 FID 不适合评编辑）。

### 7.3 "谁把什么指标推到多少"的硬线索串联

- **可控质量**：ControlNet 把分割 FID 推到 15.27 且对标工业模型辨别率 0.52（≈无法区分）；T2I-Adapter 把 COCO seg-FID 压到 16.78（低于纯 SD 24.68）；GLIGEN 把 LVIS zero-shot AP 从 2.0 拉到 11.1。
- **参数效率**：IP-Adapter 用 22M 打平 860M+ 全量微调；HyperDreamBooth 把个性化权重压到 120KB；ICEdit 用 214M LoRA + 5 万数据达到 SOTA-comparable。
- **数据效率/规模**：MagicBrush 证明 1 万金标 > 31 万合成；UltraEdit 用 3M 真实锚点数据超私有 1000 万的 Emu Edit；ICEdit 只用前 SOTA 的 0.5% 数据。
- **真实图可用率与速度**：SeedEdit 3.0 把可用率 38.4%→56.1% 并 8× 提速到 10–15s；Kontext 把统一生成+编辑压到 3–5s；LEDITS++ 把免训练编辑压到 1.78s。
- **开源逼近闭源**：Step1X-Edit v1.1 GEdit-EN 6.97 逼近 Doubao 6.98、距 GPT-4o 7.49 约 0.5 分；Qwen-Image-Edit GEdit EN/CN 双榜第一（7.56/7.52）超 GPT Image 1 [High]、ImgEdit 4.27 略超 GPT Image 1 [High] 4.20——开源指令编辑在 2025 下半年已实质追平甚至反超闭源。

### 7.4 五年演化的三个收敛判断

1. **底模从 SD1.5 U-Net → FLUX/Qwen 的 MMDiT/rectified-flow**：编辑质量天花板长期被底模锁死（InstructPix2Pix/MasaCtrl/MGIE 都卡在 SD1.5），2025 年换 12B~20B DiT 底座后开源编辑才真正起飞。
2. **理解从 CLIP/T5 → MLLM（Qwen2.5-VL/LLaVA）**：MGIE 首倡"MLLM 改写指令"，Step1X/Qwen-Edit 把 MLLM 做成第一编码器——"看懂复杂/组合指令"成为分水岭。
3. **范式从"专门编辑头" → "统一多任务 + in-context"**：Emu-Edit 证明多任务（含 CV 识别任务）反哺编辑，Kontext/ICEdit 证明 in-context 序列拼接是 DiT 时代的统一接口，最终个性化的"一致性"、可控注入的"多条件"、真实图编辑的"反演"全部被吸收进一个统一编辑大模型里。

---

## 参考（本页所有内链单工作页）

可控注入：[[controlnet]] · [[t2i-adapter]] · [[ip-adapter]] · [[gligen]] · [[uni-controlnet]] · [[unicontrol]]
指令编辑：[[instructpix2pix]] · [[magicbrush]] · [[instructdiffusion]] · [[ultraedit]] · [[mgie]]
个性化：[[dreambooth]] · [[textual-inversion]] · [[hyperdreambooth]] · [[instantbooth]] · [[styledrop]]
inversion/attention 编辑：[[prompt-to-prompt]] · [[null-text-inversion]] · [[masactrl]] · [[pix2pix-zero]] · [[ledits-pp]]
统一编辑：[[emu-edit]] · [[seededit]] · [[seededit-3-0]] · [[flux-1-kontext]] · [[step1x-edit]] · [[qwen-image-edit]] · [[in-context-edit-icedit]]
相关底座/方法：[[stable-diffusion-1]] · [[latent-diffusion-ldm]] · [[sdxl]] · [[flux-1]] · [[qwen-image]] · [[seedream-3-0]] · [[muse]] · [[emu]] · [[rectified-flow]] · [[classifier-free-guidance]] · [[ddim]]
