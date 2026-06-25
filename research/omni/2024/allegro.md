---
title: "Allegro: Open the Black Box of Commercial-Level Video Generation Model"
org: "Rhymes AI"
country: US
date: "2024-10"
type: tech-report
category: video
tags: [text-to-video, dit, video-vae, 3d-rope, full-attention, open-weights, flow-free-diffusion, rhymes-ai]
url: "https://arxiv.org/abs/2410.15458"
arxiv: "https://arxiv.org/abs/2410.15458"
pdf_url: "https://arxiv.org/pdf/2410.15458"
github_url: "https://github.com/rhymes-ai/Allegro"
hf_url: "https://huggingface.co/rhymes-ai/Allegro"
modelscope_url: ""
project_url: "https://rhymes.ai/blog-details/allegro-advanced-video-generation-model"
downloaded: [arxiv-2410.15458.pdf, allegro--readme.md, allegro--hf-modelcard.md, allegro--blog.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Allegro 是 Rhymes AI 2024 年 10 月开源（Apache 2.0）的"商用级"文生视频模型，把 VideoVAE + VideoDiT 的**数据/架构/训练/工程全链路黑盒彻底披露**：用 175M 参数 VideoVAE（4×8×8 压缩）+ 2.8B 参数 VideoDiT（32 层、T5 文本编码器、3D RoPE + 3D 全注意力）在 256×H100 上三阶段训练，生成 88 帧 / 720p / 15 FPS（约 6 秒）视频；用户研究中**全维度超越当时所有开源模型**，并在"视频-文本相关性"上**超过所有商用模型**，整体质量仅次于 Hailuo 与 Kling。

## 背景与定位
2024 年文生视频已涌现大量商用系统（Runway Gen-3、Luma Dream Machine、OpenAI Sora、快手 Kling、MiniMax Hailuo、Pika），但与文生图不同，**"如何训出商用级视频模型"的关键工程细节几乎全部闭源**——数据处理、文本-视频对齐、长上下文建模、训练基建都是黑盒。开源社区虽有 [[open-sora]]、Open-Sora-Plan 等复现项目，但报告称其"信息与资源仍不足以达到商用级性能"。

Allegro 的定位不是刷新某个指标的 SOTA，而是**做一份"可复现的商用级配方"**：它直接基于 Open-Sora-Plan v1.2.0 的 VideoDiT 架构，做三处关键改造（换 T5 文本编码器、换自训 VideoVAE、大规模多阶段训练），完整公开 106M 图 + 48M 视频的数据筛选阈值、各阶段 GPU/batch/step、基建优化，并开放全部权重与训练代码。技术脉络上它属于 [[latent-diffusion-ldm]] → [[dit]] → Sora 式 DiT 视频生成一系，承接 [[open-sora]] / Open-Sora-Plan 的开源谱系，核心贡献是"开箱"而非新方法。

## 模型架构
整体为典型 VideoDiT 三件套：**T5 文本编码器 + VideoVAE（视觉 tokenizer）+ Video Transformer（DiT）**，在 VAE 压缩后的潜空间做扩散。

**VideoVAE（视觉 tokenizer，174.96M）**
- 在图像 VAE 上加时序层构建。空间层直接采用 **Playground v2.5 的图像 VAE 架构与权重**；在编/解码器首尾各加 1D 时序 CNN 层，并在每个 ResNet block 后插入一个由 4 个 3D CNN 时序层组成的 temporal block。
- 时序下采样用 stride=2 的步进卷积，上采样用"帧复制 + 反卷积"。
- 压缩比 ST×SH×SW = **4×8×8**（时/高/宽），潜通道 **Cl = 4**（沿用图像 VAE，未扩展）。输入 T×3×H×W → 潜表示 T/4 × 4 × H/8 × W/8。
- 消融发现：temporal block 内 3D CNN 的空间核从 1 改为 **3** 能加速收敛、提升重建质量，故全部上/下采样 temporal block 改用 3D CNN。

**VideoDiT（2.8B，README/HF 卡披露的总参数；论文正文未给单一数字）**
- 基于 Open-Sora-Plan v1.2.0 的 VideoDiT，**32 个 DiT block**（`num_layers=32`）。每个 block 含：① 带 **3D RoPE** 的 self-attention（跨空间+时间维度，官方博客明确为 **3D 全注意力 / 3D full attention**，而非早期 2D 空间+1D 时序的近似）；② cross-attention 注入文本条件；③ feed-forward；④ AdaLN-single 注入扩散 timestep。
- 关键 config（论文附录 B Table 6）：`num_attention_heads=24`、`attention_head_dim=96`（隐藏维 24×96=2304）、`cross_attention_dim=2304`、`caption_channels=4096`（T5 输出维）、`patch_size=2`、`patch_size_t=1`、`sample_size=[90,160]`、`sample_size_t=22`、`norm_type=ada_norm_single`、`activation=gelu-approximate`、`num_embeds_ada_norm=1000`、`use_rope=true`。
- **文本编码器换为 T5**（取代 Open-Sora-Plan 原用的 mT5），max token 512。报告认为在以英文为主的训练数据下，mT5 的多语言能力反而损害语义对齐；换 T5 后文本-视频语义一致性显著提升（5.2 节消融）。
- 条件注入：cross-attention（文本）+ AdaLN-single（timestep）+ 3D RoPE（位置）。
- 分辨率/长度：最终 88 帧 @ 720×1280 @ 15 FPS（≈6 秒），训练上下文长度 **79.2K**。

## 数据
报告把数据 curation 视为头等工程，给出**可直接复用的阈值表**（论文 Table 1）。

**规模**：最终训练集 **106M 图像 + 48M 视频**（与高相关文本配对；注：摘要写 106M、正文 2.1.3 节与 Table 1 写 107M，报告自身两处数字不一致，此处保留二者）。图像从 412M 原始图筛得 107M；视频两子阶段分别从 500M 原始视频筛得 48M（360p）与 18M（720p）；最终微调仅选 ~2M 视频。

**筛选流水线（7 步，图/视频通用，论文 Figure 2）**：
1. 时长/FPS/分辨率过滤：去掉 <360p、<2s、<23 FPS 的素材。
2. 场景切分：用 PySceneDetect 切单场景片段，去掉每段首尾 10 帧避免误判，保留 2–16s 片段。
3. 低层指标过滤：亮度（灰度均值）、清晰度（**DOVER score**）、语义一致性（**LPIPS**）、运动幅度（**UniMatch**）四维联合，保留语义一致且有合理运动的片段。
4. 美学过滤：**LAION Aesthetics Predictor** 打分。
5. 内容无关 artifact 过滤：用 CRAFT 检测文字、用 watermark 检测工具检测水印/黑边，面积比低于阈值则裁剪、否则丢弃。
6. 粗粒度打标：用 **Tag2Text** 给中间帧打 coarse caption（供后续 CLIP 过滤与精标用）。
7. CLIP 相似度过滤：算 caption 与图/视频中帧的 CLIP 余弦相似度，剔除低相关样本。
所有视频统一用 H.264 重编码、固定 30 FPS。

**标注 / re-captioning**：用在视频字幕任务上微调过的 **Aria** 多模态模型生成 fine-grained caption（粗 caption 作为指令注入提升准确度），覆盖主体属性、交互、背景、环境、风格氛围、镜头角度与运动、以及随时间变化的过程。为支持镜头控制，部分数据 caption 以 `Camera [MOTION_PATTERN].` 开头显式标注运镜。每个视频提供**中间帧 caption（偏空间）+ 整段视频 caption（含时序变化）**两条，实现空间/时序双粒度对齐。

**分层（按训练阶段不同阈值）**：T2I 预训练（≥640×368、美学≥4.8、CLIP≥0.17，107M/412M）；T2V 360p 预训练（同上，48M/500M）；T2V 720p 预训练（≥1280×720、美学≥5.0、CLIP≥0.20，18M/500M）；T2V 微调（6–16s、美学≥5.3、加运动幅度 UniMatch∈[1,100]、语义一致性≥0.05、~2M/500M）。

**安全**：免责声明明确模型不渲染名人、可读文字、特定地点/街道/建筑；过滤含 NSFW/水印/文字等。合成数据未使用（均为真实素材筛选+模型 re-caption）。

## 训练方法
**目标**：标准 latent diffusion（DiT 预测噪声，VAE 解码回 RGB）。报告未提及 flow matching / rectified flow，也**未做偏好对齐（无 RLHF/DPO/reward model）、未做步数蒸馏**——这点报告在"More Thinkings"中亦坦承训练流程不含文本编码器训练，且依赖 prompt refiner 弥补泛化。

**三阶段渐进式训练（论文 Table 2，coarse-to-fine）**：
1. **T2I 预训练**：从 Open-Sora-Plan v1.2.0 文生图模型初始化，目标分辨率 1×368×640，换 T5（512 token）+ 自训 VideoVAE，混入静态视频帧作图像联训。**128×H100，batch 4096，170K steps，过 700M 图**。
2. **T2V 预训练（三子阶段）**：
   - 40 帧 @ 368×640：256×H100，batch 1024，85K steps，过 87M 视频（建立基础动态）。
   - 40 帧 @ 720×1280：256×H100，batch 512，41K steps，过 21M 视频（提分辨率/视觉质量）。
   - 88 帧 @ 720×1280：256×H100，batch 256，31K steps，过 8M 视频（增帧数以表征大幅运动）。三子阶段均 15 FPS 采样，最终可出 6s/720p。
3. **T2V 微调**：高质量动态视频 + 多样 caption，256×H100，batch 256，10K steps，过 2.6M 视频，增强对不同长度/格式文本输入的处理。

**VideoVAE 训练（独立，两阶段）**：仅用最短边 >720px 的素材，选 54.7K 视频 + 3.73M 图。损失 = L1（权重 1.0）+ LPIPS（权重 0.1）。① 图+视频联训（1 个 16 帧视频 + 4 张图为一 batch，256×256），32×A100、65K iter；② 冻结空间层、用 24 帧 256×256 视频只微调时序层，32×A100、25K iter。时序增强随机从 [1,3,5,10] 选采样间隔（大间隔显著加速时序层收敛）。

**微调超参（开源训练代码披露）**：bf16 混合精度 + allow_tf32 + stable_fp32；T2V 微调 lr=1e-4、TI2V 微调 lr=1e-5，constant scheduler、无 warmup；CFG dropout 0.1；model_max_length 512；gradient checkpointing。TI2V 用联合训练范式（首帧→视频 0.5 / 首尾帧→视频 0.4 / 视频续写 0.1 三子任务概率）。

## Infra（训练 / 推理工程）
**训练算力**：最多 **256×H100**（T2I 阶段 128×H100），VideoVAE 用 32×A100。报告给出各阶段 GPU×batch×steps（见上表）但未汇总总 GPU·时。

**三大工程优化**：
1. **VAE/文本编码器解耦推理**：观察到 VideoVAE 处理 + 文本编码占训练计算 >30%。把 VideoVAE 与 T5 迁到**中端推理 GPU**，把 H100 的算力/显存留给长上下文与大 batch；用 `torch.compile` JIT 编译 + 批量推理把 VAE/文本编码耗时降 **62%**；对多 epoch 复用的高质量数据**离线缓存编码结果**避免重复计算。
2. **高效注意力**：用全双向注意力；长序列下 attention 占训练计算 **63.3%**、推理 **84.5%**。self-attention 用 **FlashAttention2**、cross-attention 用支持 mask 的 **XFormers** memory-efficient attention；从 XFormers 换到 FlashAttention2 使 self-attention 训练**提速 22%**。
3. **上下文并行（Context Parallel）**：88 帧 720×1280 训练需 **~79.2K 上下文**，单卡放不下；用 CP 把上下文切块分卡并行，softmax-qk attention 前后向间做必要通信；实现参考 **Ring-Attention** 与 **DeepSpeed-Ulysses**；推理同样用 CP。

**VAE 分块推理**：高分辨率长视频直接编解码爆显存，故对视频与潜张量做时空 tiling 分块编解码再拼接。Encoder tile 24×p×p、Decoder tile 6×(p/8)×(p/8)；320p 取 p=256、720p 取 p=320，时空维做线性融合 blending。

**推理形态（README/HF 卡）**：DiT/T5 用 BF16、VAE 最佳为 FP32/TF32；单 H100 约 **20 分钟**，8×H100 约 **3 分钟**（社区 Allegro-VideoSys + PAB 可进一步降至 2–3 分钟）。开 CPU offload 显存仅 **9.3 GB**（不开为 27.5 GB）。100 步采样、CFG guidance_scale 7.5；输出 15 FPS 后用 EMA-VFI 插帧到 30 FPS。已并入 HuggingFace diffusers（0.32.0-dev0 起，`AllegroPipeline`）。

## 评测 benchmark（把效果讲清楚）
**VideoVAE 重建（论文 Table 3，100 段 120 帧 720p 验证集）**：Allegro **PSNR 31.25 / SSIM 0.8553**，优于 Open-Sora（30.64 / 0.8338）与 Open-Sora-Plan（27.65 / 0.8173）；主观上闪烁更少、不过锐化/过平滑。

**VBench（论文 Table 4，946 prompt、每 prompt 5 段共 4730 段；他模型直接取 leaderboard）**——Total Score：
- Hailuo 83.41 > Gen-3 82.32 > Kling 81.85 > **Allegro 81.09** > CogVideoX 80.91 > Pika 80.69 > Open-Sora 79.76 > Open-Sora-Plan 78.00。
- 分维（Allegro）：Quality 83.12、Semantic 72.98、Subject Consist. 96.33、Background Consist. 96.74、**Aesthetic Quality 63.74（全表最高）**、Human Action 91.4、Scene 46.72。
- 即 VBench 上**超越全部开源模型**，商用中仅次于 Gen-3、Kling、Hailuo；其中美学质量为全表第一。

**人评用户研究（论文 Table 5，46 prompt、A-B 测、共 5448 评分，六维 Win/Lose/Tie）**：
- 对**全部开源模型六维全胜**（vs Open-Sora-Plan 整体质量 Win 100%、vs Open-Sora 98%、vs CogVideoX 96%）。
- 对商用：**视频-文本相关性超过所有商用模型**（vs Gen-3 Win 42%/Lose 18%、vs Hailuo 33%/25%、vs Kling 29%/27%、vs Dream Machine 33%/22%、vs Vidu 27%/15%）。
- **整体质量**：胜 PixVerse(96%)/Pika(89%)/Dream Machine(61%)/Vidu(51%)/Gen-3(49%)，仅负于 Hailuo（Win 47%/Lose 49%）与 Kling（Win 22%/Lose 76%）。
- 短板坦诚：**运动幅度**对顶级商用偏弱（vs Kling Lose 76%、vs Gen-3 Lose 60%、vs Hailuo Lose 46%），报告归因于训练数据加速运动不足，建议增大模型规模/加运动数据改善。

**关键消融**：① T5 vs mT5——即便用同数据把 Open-Sora-Plan 的 mT5 T2V 模型充分微调，英文全量数据下 mT5 的语义建模问题仍无法解决；换 T5 后文生图/文生视频均显著提升（5.2 节、Figure 7/8）。② VideoVAE 时序核 1→3、③ temporal 采样间隔加大加速收敛（见上）。④ 多阶段：40×368→40×720（提质）→88×720（增大幅运动表征）→微调（提美学/响应），Figure 9 逐阶段可视化。

## 创新点与影响
**核心贡献**
- **"开箱"价值**：把商用级文生视频从数据阈值表、VideoVAE/VideoDiT 架构改造、三阶段训练资源表（GPU×batch×step）、到长上下文基建（CP + Ring-Attention/DeepSpeed-Ulysses、解耦 VAE 推理、FlashAttention2）全链路公开，且 Apache 2.0 放出全部权重 + 训练代码，是当时**可复现性最高的开源商用级 T2V 配方之一**。
- **数据 curation 工程化**：7 步过滤 + 双粒度（中帧/整段）re-caption + 运镜显式标注的系统化流水线，给出可直接迁移的阈值。
- **架构落地**：用 3D 全注意力 + 3D RoPE + T5 + 自训 4×8×8 VideoVAE，在 2.8B 这个"小而高效"规模上做到商用观感，单卡 9.3GB 即可推理，对社区门槛友好。

**影响**：发布即并入 HuggingFace diffusers；衍生出 Allegro-TI2V（文图生视频，2024-11）、低分辨率/少帧研究版（2024-12）、训练代码（2024-12）、以及社区 Presto（长时长 T2V，基于 Allegro）。其数据/训练披露成为后续开源视频项目的参考配方。

**已知局限（报告自陈）**
- 无偏好对齐 / 无步数蒸馏，100 步采样、单卡 20 分钟，推理仍重；VideoVAE 时序 CNN + 时空 blending 计算开销极高，且对 tile 时长敏感（偏离训练时长会闪烁）。
- 大幅运动、细粒度指令跟随、复杂主体交互、纹理细节仍弱于顶级商用（Hailuo/Kling）。
- 强依赖 prompt refiner：训练 caption 高度结构化，等于把 T2V 简化成 label-to-video，损害泛化，需 refiner 兜底。
- 不渲染名人/可读文字/特定地点；当时仅 T2V（I2V/运动控制为 future work）。
- VideoVAE 难重建线状语义，建议未来引入频域特征 + 增大潜通道。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2410.15458
- arxiv_pdf: https://arxiv.org/pdf/2410.15458
- github: https://github.com/rhymes-ai/Allegro
- hf_model: https://huggingface.co/rhymes-ai/Allegro
- official_blog: https://rhymes.ai/blog-details/allegro-advanced-video-generation-model

## 本地落盘文件
- ../../../sources/omni/2024/arxiv-2410.15458.pdf
- ../../../sources/omni/2024/allegro--readme.md
- ../../../sources/omni/2024/allegro--hf-modelcard.md
- ../../../sources/omni/2024/allegro--blog.md
