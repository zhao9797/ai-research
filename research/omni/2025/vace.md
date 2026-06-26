---
title: "VACE: All-in-One Video Creation and Editing"
org: "Alibaba Tongyi Lab (Wan Team)"
country: China
date: "2025-03"
type: paper
category: video
tags: [video, editing, unified, dit, controllable, inpainting, reference-to-video, wan, ltx-video, iccv2025]
url: "https://arxiv.org/abs/2503.07598"
arxiv: "https://arxiv.org/abs/2503.07598"
pdf_url: "https://arxiv.org/pdf/2503.07598"
github_url: "https://github.com/ali-vilab/VACE"
hf_url: "https://huggingface.co/collections/ali-vilab/vace-67eca186ff3e3564726aff38"
modelscope_url: "https://modelscope.cn/collections/VACE-8fa5fcfd386e43"
project_url: "https://ali-vilab.github.io/VACE-Page/"
downloaded: [arxiv-2503.07598.pdf, vace--readme.md, vace--hf-modelcard.md, vace--hf-modelcard-preview.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
VACE 是阿里通义实验室 Wan 团队基于视频 DiT（Wan2.1 / LTX-Video）打造的「视频领域 all-in-one 创作与编辑」框架：用一个统一接口 **Video Condition Unit (VCU)** 把 文本+视频+图像+掩码 四种模态打包，一个模型即可做 文生视频、参考生视频(R2V)、视频到视频编辑(V2V)、掩码编辑(MV2V，含 inpaint/outpaint/扩展) 以及它们的自由组合（Move/Swap/Reference/Expand/Animate-Anything）。论文宣称这是**首个基于视频 DiT、同时支持如此广泛任务的 all-in-one 模型**，在自建 12 任务 / 480 样本的 VACE-Benchmark 上与各专用模型打平，开源后成为 2025 年开源可控视频的事实标准框架（ICCV 2025）。

## 背景与定位
图像域的「生成+编辑统一」已较成熟——[[acepp]] (ACE/ACE++)、OmniGen、UniReal、OmniControl 等把 ControlNet 式可控生成、局部编辑、参考生成揉进一个图像模型。视频域因为要同时维持**时间和空间**一致性，长期停留在「单任务单模型」：Video-P2P、MagicEdit 做编辑，MotionCtrl 做运动控制，Phantom 做主体一致，各自为政，部署成本高、无法组合。

VACE 的定位就是把图像域 ACE/ACE++ 那套「统一创作+编辑」搬到视频域。它没有从零训基模型，而是站在主流视频 DiT 之上（[[wan]] Wan2.1-T2V 与 LTX-Video），把各类任务的复杂多模态输入抽象成统一格式，再用一个可插拔结构注入到冻结的 DiT 主干上。核心价值：一次推理、一个模型完成绝大多数视频 AI 创作任务，并支持基础任务的**组合扩展**（如长视频重渲染、scribble→视频扩展、参考+inpaint 的换装）。技术脉络上承 [[latent-diffusion-ldm]] / DiT（Peebles & Xie）/ rectified flow（[[stable-diffusion-3]] 系列的 flow matching），与 ACE++ 同源（同一作者团队的 Res-Tuning、SCEdit 思路一脉相承）。

## 模型架构
**Backbone：视频 Diffusion Transformer（DiT）**，不自训基模型，直接复用两套预训练 T2V：
- **Wan-T2V-14B**（[[wan]] Wan2.1，高质量、最高 720p，40 层 DiT）；
- **LTX-Video-2B v0.9**（快、省资源，28 层 DiT，~480p）。
对应放出的权重有 VACE-Wan2.1-1.3B-Preview、Wan2.1-VACE-1.3B、Wan2.1-VACE-14B、VACE-LTX-Video-0.9 四档。视频 token 化沿用各自基模型的 3D 因果 VAE 与文本编码器（Wan 用 umT5；text tokenization 管线复用基模型，VACE 只新增上下文分支）。

**Video Condition Unit (VCU)**——统一输入范式，把任意视频任务表示为 `V = [T; F; M]`：
- `T` 文本 prompt；
- `F` 上下文视频帧序列 {u₁…uₙ}，RGB 归一化到 [-1,1]；
- `M` 掩码序列 {m₁…mₙ}，二值，"1"=要改、"0"=保留。`F`、`M` 在空间 h×w 和时间 n 上对齐。
四类基础任务用同一套 F/M 表达（论文 Tab.1）：
- **T2V**：F 全 0、M 全 1（全部待生成）；
- **R2V**：参考帧 {r₁…r_l} 拼在帧序列前、对应掩码全 0（保留参考）+ 后续全 1；
- **V2V**：F=输入视频、M 全 1；
- **MV2V**：F=输入视频、M=时空掩码（3D ROI）。
任务组合只需拼接 F/M（如 参考+inpaint 的换装：前置 l 张参考帧 + 后续带掩码的视频）。

**上下文 token 化（三步）**：
1. **Concept Decoupling（概念解耦）**：把 F 按掩码拆成两路同形序列——`Fc = F×M`（reactive frames，要改的像素，如控制信号 depth/pose、灰度像素）与 `Fk = F×(1−M)`（inactive frames，要保留的像素，如 V2V/MV2V 不变区、参考图）。论文认为显式分离不同模态/分布的视觉信息对收敛至关重要（消融 Fig.5d 证明能显著降 loss）。
2. **Context Latent Encoding**：Fc、Fk 经视频 VAE 映射到与噪声潜变量 X 同一潜空间，保持时空一致；**参考图单独经 VAE 编码后沿时间维拼接**（避免与视频混淆，解码时再移除对应部分）；M 直接 reshape+插值。最终 Fc、Fk、M 都对齐到 n′×h′×w′。
3. **Context Embedder**：把 Fc、Fk、M 在通道维拼接后 token 化成 context tokens；token 化 Fc/Fk 的权重直接从原视频 embedder 复制，token 化 M 的权重零初始化。

**两种训练注入方式（Fig.3）**：
- (a) **Fully Fine-tuning**：context token 与噪声 token 相加，整个 DiT + 新 Context Embedder 全量微调；
- (b) **Context Adapter Tuning（推荐）**：以 Res-Tuning 方式，从原 DiT 复制若干 Transformer Block 组成**分布式、级联的 Context Blocks** 旁支；主干 DiT 处理 video+text token，旁支处理 context+text token，每个 Context Block 输出以**加性信号**回注主干。此时 DiT 冻结，只训 Context Embedder + Context Blocks——**收敛更快、且可插拔**（不破坏基模型）。Wan-T2V-14B 版用 8 个 context layers `[0,5,10,…,35]`，LTX 版用 14 个 `[0,2,…,26]`。消融（Fig.5c）显示同样数量的 block，**分布式排布优于连续排布**，block 越多越好但收益递减，最终折中用部分分布式。

## 数据
论文有专门的「Datasets / Data Construction」一节，但**未披露训练数据的总规模、来源域和配比的具体数字**（只描述了构造流程，无样本量）。已披露的处理流水线：
- **视频质量预筛**：先做 shot slicing（镜头切分），按 **分辨率、美学分（aesthetic score）、运动幅度** 初筛。
- **实例级理解**：用 **RAM** 给首帧打标 + **Grounding DINO** 检测，按目标区域过大/过小做二次过滤；再用 **SAM2** 做视频分割得到实例级 mask，按 mask 面积阈值算「有效帧比例」在时间维过滤实例。
- **逐任务定制构造**：1) 可控生成任务离线预抽 **depth、scribble、pose、optical flow**，灰度(gray)与 layout 在线生成；2) repaint 任务随机 mask 实例做 inpaint、取反做 outpaint，mask 增广实现无条件 inpaint；3) extension 任务抽取首帧/尾帧/两端帧/随机帧/两端片段以支持多种扩展；4) reference 任务从视频抽人脸/物体实例并做离线/在线增广构造配对。**随机组合上述所有任务联合训练**；所有涉及 mask 的操作都做任意增广以满足不同粒度的局部生成需求。
- 训练支持**任意分辨率、动态时长、可变帧率**。
- **未披露**：训练集总时长/视频数、数据来源（自有/爬取/授权）、re-captioning 用什么模型、合成数据占比、安全过滤细节。

## 训练方法
- **训练目标**：沿用基模型的 **flow matching / rectified flow**（采样器 Flow Euler），在 VCU 输入上做条件扩散/流匹配训练；新增 Context Embedder 与 Context Blocks 的参数。
- **分阶段训练（phased）**：① 先练 **基础任务**（inpainting、extension 等，视作对预训练 T2V 的「模态补全」，引入 mask、学时空上下文生成）；② **任务扩展**：从单参考帧→多参考帧、单任务→组合任务渐进；③ **质量微调**：用更高质量数据 + 更长序列收尾。
- **关键超参（Appendix A Tab.3，Wan-T2V-14B 版 / LTX-2B 版）**：
  - 任务设置：12 任务 + 组合任务联合训练；
  - 优化器 **AdamW**，weight decay 0.1；学习率 **5e-5（Wan）/ 1e-4（LTX）**，Constant schedule；
  - **训练步数 200,000**（两版相同）；
  - batch size/GPU = 1/8（Wan）/ 1（LTX），accumulate step 1（Wan）/ 8（LTX）；
  - 分辨率 ~720p（Wan）/ ~480p（LTX）；序列长度 **75600（Wan）/ 4992（LTX）**；
  - timestep **Shifting=True**，加权方案 **uniform**；
  - Context Adapter = Res-Tuning，Concept Decouple=True。
- 消融还扫了 weighting scheme、timestamp shifting、p-zero 等超参（Fig.5b）。
- **未提及**蒸馏/步数蒸馏/一致性模型/偏好对齐（RLHF/DPO/reward model）——VACE 本体不做 RL 或 distillation，加速主要靠基模型与并行（社区另有量化/LoRA 生态）。

## Infra（训练 / 推理工程）
- **训练算力（Tab.3）**：
  - **Wan-T2V-14B 版：A100×128**，FSDP / Tensor Parallel / BFloat16；
  - **LTX-Video-2B 版：A100×16**，AMP / DDP / BFloat16。
  - 两者均训 200k 步。（未给总 GPU·时。）
- **推理**：
  - LTX 版：单张 A100、无专门加速，采 40 步约 **24 秒**出 ~5 秒视频（guide scale 3.0）；
  - Wan-14B 版：采 25 步、guide 4.0，**~260 秒（8 GPU）**出一段，720p。
  - 多卡推理走 **xfuser ≥0.4.1**，支持 `--dit_fsdp --t5_fsdp` 与 **Ulysses / Ring 序列并行**（如 14B-720p 用 `--ulysses_size 8 --ring_size 1`，1.3B-480p 用 `--ring_size 8`），8 卡 torchrun。
  - 英文 Wan / LTX 用户需开 **prompt extension**（`--use_prompt_extend`）才能发挥完整效果。
- 部署形态：开源代码含 端到端 pipeline（`vace_pipeline.py`）、预处理（`vace_preproccess.py`，含 depth/pose/scribble/flow/mask 等 annotator）、Wan/LTX 两套推理脚本与 Gradio demo；环境 Python 3.10.13 / CUDA 12.4 / PyTorch ≥2.5.1。社区已支持 ComfyUI、Diffusers、量化、LoRA 适配（README 致谢）。

## 评测 benchmark（把效果讲清楚）
**自建 VACE-Benchmark**：因为视频参考生成/编辑缺乏统一评测，作者构建了 **240 段高质量视频、12 类任务**（论文摘要又称 480 评测样本，对应含 input video/mask/reference 等输入模态组合），平均每任务 ~20 样本，涵盖 text-to-video、inpaint、outpaint、extension、grayscale、depth、scribble、pose、optical flow、layout、reference-face、reference-object；同时提供原始 caption（量化用）和针对任务重写的 prompt（评创意）。
评估分两路：**自动评分**取自 [[vbench]] VBench 的 8 个指标（aesthetic quality、background consistency、dynamic degree、imaging quality、motion smoothness、overall consistency、subject consistency、temporal flickering）；**人评**用 MOS（1-5 分）评 prompt following / temporal consistency / video quality。

**关键量化结果（Tab.2，基于 LTX-Video 的 VACE 对比专用模型，部分指标）**：
- **I2V（extension）**：VACE Normalized Average **74.38%**，优于 I2VGenXL(71.54%)、CogVideoX-I2V(73.66%)、LTX-Video(72.89%)；MOS（prompt following / temporal consistency / video quality）3.20/4.00/2.54。
- **Inpaint（移除）**：VACE Normalized **72.05%** > ProPainter(70.15%)；用户研究 MOS ProPainter 2.35/4.00/2.99 vs VACE 2.40/4.00/2.60（两者持平，VACE 略优 prompt following，逊于 video quality）。
- **Outpaint**：VACE Normalized **74.25%** > M3DDM(73.16%) > Follow-Your-Canvas(71.54%)；MOS 三项 3.90/3.92/3.58。
- **Depth 控制**：VACE Normalized **74.99%**，明显高于 Control-A-Video(72.35%)、VideoComposer(70.74%)、ControlVideo(70.07%)；MOS 3.10/3.92/2.66。
- **Pose 控制**：VACE Normalized **76.13%** > ControlVideo(72.45%) > Follow-Your-Pose(66.43%) > Text2Video-Zero(59.69%)。
- **Optical Flow**：VACE Normalized **75.90%** > FLATTEN(74.42%)。
- **R2V（参考生视频）**：对比的是**闭源商业产品** Keling 1.6 / Pika 2.2 / Vidu 2.0。VACE Normalized **76.76%**，自动指标与 Vidu 2.0(76.47%) 相当、略低于 Pika 2.2(77.87%) 与 Keling 1.6(78.81%)，作者坦承「面向快生成的小模型在 R2V 上与商业模型仍有一定差距」。**人评 MOS 上 VACE（prompt following 3.47 / temporal 3.42 / quality 3.30，均值 3.40）反而低于三家商业产品**（Keling 4.04 / Pika 3.91 / Vidu 3.84 均值）——即 R2V 这一项 VACE 在自动指标与人评上均未超越商业闭源。
- **结论**：在 I2V、inpaint、outpaint、depth、pose、optical flow 上，统一 VACE 在 8 项 video quality/consistency 指标与归一化均值上整体优于开源专用方法（论文称人评在多数任务上也更贴合用户偏好）；唯独 R2V 与顶级商业闭源（Keling/Pika/Vidu）在自动指标与人评上均仍有差距。**用一个统一模型达到与各专用开源模型相当或更优的水平**是核心卖点。

**消融结论**：① Fully FT 与 Context Adapter 效果相近，但后者收敛更快→作为默认；② context block 分布式排布优于连续、数量越多越好（收益递减）；③ Concept Decouple 显著降 loss。

> 注：上述各任务的 Normalized Average 与 MOS（prompt following / temporal consistency / video quality）数字均逐行核对自已落盘的 arxiv-2503.07598.pdf（Tab.2，基于 LTX-Video 的 VACE）。Tab.2 每行 8 项 VBench 细分指标未全列，仅引用确定的归一化均值与三项 MOS。

## 创新点与影响
**核心贡献**：
1. **VCU 统一输入范式**——把文本/视频/图像/掩码统一成 `[T;F;M]`，用一套 F/M 表达覆盖 T2V/R2V/V2V/MV2V 四类基础任务及其任意组合，是视频域「统一创作+编辑」的接口级抽象。
2. **Concept Decoupling**——按掩码把上下文帧拆成 reactive(要改)/inactive(要留) 两路，显式分离控制信号与保留内容，对收敛和质量有实证收益。
3. **Context Adapter（Res-Tuning 旁支）**——可插拔、冻结主干、收敛快，让任意预训练视频 DiT 都能低成本「升级」为 all-in-one 编辑器。
4. **VACE-Benchmark**——填补视频参考/编辑统一评测空白（12 任务、240+ 视频）。

**影响**：作为 2025 年**开源可控视频的事实标准框架**，VACE 随 Wan2.1 生态放出 1.3B/14B 多档权重（Apache-2.0），被 ComfyUI（Kijai workflow）、Diffusers 原生接入，衍生大量 LoRA 与工作流，成为社区做换装(Swap)、运动迁移(Move)、参考生成(Reference)、扩图(Expand)、动画(Animate)的主力底座。它把图像域 ACE/OmniGen 式统一范式成功迁移到视频域，验证了「冻结大视频 DiT + 轻量上下文旁支」的可扩展路线。

**已知局限（Appendix C）**：① 生成质量与整体风格强依赖基模型——小模型省资源但上限受限；② R2V（参考生视频）与顶级商业闭源（Keling/Pika/Vidu）在自动指标与人评 MOS 上均仍有差距（论文将其归因于面向快生成的小模型规模）；③ 论文未公开训练数据规模/来源，复现训练有门槛；④ 存在 misinformation/deepfake 与偏见放大的社会风险，作者呼吁监管配套。

## 原始链接
- paper (arXiv abs): https://arxiv.org/abs/2503.07598
- paper PDF: https://arxiv.org/pdf/2503.07598
- ICCV 2025 open access: https://openaccess.thecvf.com/content/ICCV2025/html/Jiang_VACE_All-in-One_Video_Creation_and_Editing_ICCV_2025_paper.html
- project page: https://ali-vilab.github.io/VACE-Page/
- github: https://github.com/ali-vilab/VACE
- HF collection (ali-vilab): https://huggingface.co/collections/ali-vilab/vace-67eca186ff3e3564726aff38
- HF model (Wan2.1-VACE-14B): https://huggingface.co/Wan-AI/Wan2.1-VACE-14B
- HF model (preview): https://huggingface.co/ali-vilab/VACE-Wan2.1-1.3B-Preview
- ModelScope collection: https://modelscope.cn/collections/VACE-8fa5fcfd386e43
- VACE-Benchmark dataset: https://huggingface.co/datasets/ali-vilab/VACE-Benchmark

## 一手源存档（sources/）
- [arxiv-2503.07598.pdf](https://arxiv.org/pdf/2503.07598)  （arXiv 原文 PDF，不入 git）
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/vace--readme.md)
- [hf-modelcard.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/vace--hf-modelcard.md)
- [hf-modelcard-preview.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/vace--hf-modelcard-preview.md)
