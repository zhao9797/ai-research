---
title: "FramePack: Frame Context Packing and Drift Prevention in Next-Frame-Prediction Video Diffusion Models"
org: "Stanford University / MIT"
country: US
date: "2025-04"
type: paper
category: video
tags: [video-generation, long-video, next-frame-prediction, diffusion-transformer, context-compression, anti-drifting, hunyuanvideo, wan, low-vram]
url: "https://arxiv.org/abs/2504.12626"
arxiv: "https://arxiv.org/abs/2504.12626"
pdf_url: "https://arxiv.org/pdf/2504.12626"
github_url: "https://github.com/lllyasviel/FramePack"
hf_url: ""
modelscope_url: ""
project_url: "https://lllyasviel.github.io/frame_pack_gitpage/"
downloaded: [arxiv-2504.12626.pdf, framepack--readme.md, framepack--projectpage.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
FramePack 是一种用于「下一帧（下一帧段）预测」视频扩散模型的**上下文打包结构 + 防漂移采样/训练方法**：它按帧的重要性对历史帧做渐进式压缩，使 transformer 总上下文长度收敛到一个**与视频长度无关的固定上限**（流式生成达到 O(1) 计算复杂度），从而能用 13B 模型在 **6GB 笔记本显存**上以 30fps 生成上千帧（1 分钟、1800 帧）视频；同时用「规划端点 / 反向采样 / 历史离散化」三招抑制长视频漂移。作者为 ControlNet 作者 Lvmin Zhang（张吕敏）等。

## 背景与定位
长视频生成中有两个核心矛盾问题：
- **遗忘（Forgetting）**：模型记不住早期内容，时序一致性退化。
- **漂移（Drifting）**：误差随时间累积导致画质退化（即 exposure / observation bias 曝光/观测偏差）。

二者构成根本性权衡：任何「增强记忆来缓解遗忘」的方法都会同时记住更多误差、加速误差传播从而加重漂移；任何「打断误差传播来缓解漂移」的方法（如对历史帧加噪、重噪、mask）又会削弱时序依赖从而加重遗忘。这一悖论阻碍了 next-frame 预测模型的可扩展性。

朴素地「编码更多历史帧」会因 transformer 注意力的二次复杂度迅速变得不可行；且视频帧之间存在大量时序冗余，全上下文做法非常低效。FramePack 的出发点正是利用这种冗余设计高效压缩系统。

在技术脉络中，FramePack 属于「next-frame / autoregressive 长视频生成 + 高效注意力/压缩」一支，紧邻并对比了 DiffusionForcing（next-token 预测 + full-sequence 扩散）、CausVid（双向蒸馏为快速因果模型）、StreamingT2V（anchor 帧）、HistoryGuidance（历史引导）、RollingDiffusion、LTXVideo（高压缩 latent）、FAR（多级因果注意力 + KV cache）等工作。它本身不训练新基座，而是**对现有预训练视频扩散基座（[[hunyuan-video]]、[[wan]]）做微调改造**。相关基础工作可参考 [[ddpm]] [[latent-diffusion-ldm]] [[diffusion-transformer-dit]]。

> 版本说明：arXiv 2504.12626 已迭代到 v3（2025-10-14，NeurIPS 2025 中稿版），标题更新为「Frame Context Packing and Drift Prevention…」；v1 旧标题为「Packing Input Frame Contexts in Next-Frame Prediction Models for Video Generation」（仅 Lvmin Zhang 与 Maneesh Agrawala 两作者）。本页基于 v3 正文撰写。

## 模型架构
FramePack 不是一个新基座，而是一个**可加在现有 DiT 视频基座输入端的「帧上下文打包」结构**，配合采样/训练方法。

**问题设定**：next-frame-section 预测——给定 T 个输入（历史）帧 F ∈ R^{T×h×w×c}，预测 S 个未知帧 X ∈ R^{S×h×w×c}（S 通常为 1 或很小，关注 T ≫ S 的困难情形）。所有「帧/像素」均指 VAE 编码后的 latent。每帧上下文长度 L_f（在 Hunyuan/Wan/Flux 中 480p 帧约 L_f ≈ 1536–1560 tokens），vanilla DiT 总上下文 L = L_f·(T+S)，T 大时爆炸。

**核心机制 1：按时间邻近度的渐进压缩打包**
- 把历史帧按重要性排序（F0 最重要 = 最近，F_{T-1} 最不重要 = 最旧）。
- 长度函数 φ(F_i) = L_f / λ^i（λ>1 为压缩参数），即越旧的帧压缩越狠、上下文越短。
- 总长度成几何级数（Eq.2: L = S·L_f + L_f·Σ_{i=0}^{T-1} 1/λ^i）；当 T→∞ 时收敛到 L_f·(S + λ/(λ-1))（论文正文把 L_f 提出后写作「(S + λ/(λ-1))」），**与帧数 T 无关**——这就是固定上限、流式 O(1) 的来源。
- 主要讨论 λ=2（硬件对 2 的幂友好）；通过复制/丢弃 2 的幂级数中的特定项可表示任意压缩率（如把 1/2、1/8 项各复制一份得到 2.625）。
- **压缩通过改 transformer 输入层的 patchify 3D 卷积核大小实现**：3D kernel 记为 (p_f, p_h, p_w)。例如 (1,2,2) 让 480p 帧约 1536 tokens，换成 (2,4,4) 则仅 192 tokens。同一压缩率可由多种 kernel 实现（压缩率 64 可用 (1,8,8)/(4,4,4)/(16,2,2)/(64,1,1) 等）。

**打包调度（Packing schedules）**：论文给出多种 kernel 结构变体——几何级数、级别复制（duplication，便于宽高同 kernel 更紧凑）、时序 kernel（把连续多帧压成单 tensor）、对称级数（首尾帧同等重要，利于 image-to-video）、重要起点级数等（Fig.1c）。

**独立 patchify 参数**：经验上为不同压缩率的输入投影使用**独立的神经网络层**能稳定学习。作者把最常用的 (2,4,4)、(4,8,8)、(8,16,16) 设为独立层；更高压缩（如 (16,32,32)）先用 (2,2,2) 下采样再走最大 kernel (8,16,16)。这些独立权重由预训练 patchify 投影（如 HunyuanVideo/Wan 的 (2,4,4)）**插值初始化**。

**Tail 处理**：当帧极多、个别帧 latent 小于最小单元（单个 latent pixel）时，提供 3 种尾帧选项——(1) 直接删除 td；(2) 每尾帧增加单个 latent pixel 上下文 ta；(3) 对所有尾帧做全局平均池化再用最后 kernel 编码 tc。实测三者视觉差异可忽略。

**RoPE 对齐**：不同压缩 kernel 产生不同上下文长度，需要 RoPE 旋转位置编码对齐。作者直接对 RoPE 的复数「相位（phase）」做平均池化下采样以匹配压缩 kernel；防漂移采样涉及非连续时间索引时，则通过**跳过空白相位（indices）**支持随机访问。

**核心机制 2：特征相似度 / 混合打包**——排序不必按时间，可按余弦相似度 sim_cos(F_i, X̂)（历史帧与估计的下一帧段之间）排序，F0 最相似。为避免相似度排序在连续帧上跳变，引入平滑时间项 sim_time = exp(−(time(F_i)−time(X̂))²) 并加权得 sim_hybrid = sim_cos + λ_time·sim_time。该混合方式适合世界模型/视频游戏数据集（需返回曾访问过的场景视角），也可换成人脸身份度量用于强调演员一致性的电影生成。

文本/图像条件、text-to-video 与 image-to-video 都由 next-frame-section 预测天然支持，**无需修改架构**。

## 数据
- **基座数据继承自预训练模型**：FramePack 本身不预训练新基座，而是在 HunyuanVideo / Wan 之上微调，因此大规模图文/视频对预训练数据沿用基座。
- **微调数据采集**：作者**遵循 LTXVideo 的数据采集 pipeline**，在多分辨率、多质量等级上收集数据（更多细节在补充材料，正文未给出具体数量/配比）。
- **历史离散化用的 codebook 数据**：从预编码 latent 视频数据集 Φ ∈ R^{(B×T×H×W)×C} 上做 K-Means 得到 codebook Ω ∈ R^{K×C}。
- 数据规模、来源构成、清洗过滤、re-captioning、美学/安全过滤等具体数字**未在正文披露**（部分指向补充材料）。

## 训练方法
**训练目标**：沿用基座的视频扩散/flow 训练（HunyuanVideo、Wan 均为 flow-matching/DiT 体系）；FramePack 以 **LoRA 微调**为主把现有基座改造成 next-frame-section 预测器。论文一个有意思的发现：因为 next-frame 预测每步生成的 tensor 比整段视频生成小，可以使用**更平衡的扩散调度器、更不极端的 flow shift 时间步**。

**防漂移训练/采样三招（Drift Prevention，Fig.2）**：
1. **规划端点 + 调整采样顺序（Planned endpoints / adjusted sampling order）**：vanilla 采样是严格因果 P(X_t|X_{t-1})，易漂移。改为**第一次迭代同时生成开头段和结尾段**作为锚点，后续迭代填中间空隙——这把因果链打破为双向 P(X_t|X_{t1}, X_{t2})（t1<t<t2）。适合运动幅度小、周期/重复运动（跳舞、说话、旋转）或纹理类运动（火焰、水流）。
2. **反向采样（Inverted sampling，image-to-video 专用）**：把端点规划的顺序反转，使所有生成迭代都朝「逼近高质量用户输入首帧」的方向进行，从而迭代式精修、首帧质量被持续逼近。**这是唯一在所有推理中都把首帧当逼近目标的方法，对 image-to-video 最合适**。
3. **多端点（Multiple endpoints）**：端点规划可用不同 prompt 重复多次再填空，支持更动态的运动与更复杂的叙事/多 prompt 故事。
4. **历史离散化（History Discretization）**：漂移的另一诱因是历史帧在训练/推理分布上的差异。把历史 latent 用 codebook 量化为**离散整数 token**（Q(F)_p = argmin_k ‖F_p − Ω_k‖²，再用 Ω_{Q(F)} 还原）替换训练时的历史帧，降低训练-推理 mode gap。直觉：K=1 时历史变单色、漂移被消除但完全丢失记忆；K→∞ 等价于不离散化、漂移保留。**实测 K=128 给出强防漂移且训练难度最小**（与 Table 2 中用到的 K=256 略有差异，二者均被评测）。

**关键工程能力**：FramePack 实现使 **13B HunyuanVideo 在单台 8×A100-80G 节点、480p、窗口大小 2–3 的 LoRA 训练下达到约 batch size 64**（窗口 4–5 时 batch size 32），把 13B 视频模型的微调拉到「个人/实验室级」规模——这是「video diffusion 训得像 image diffusion」的核心卖点之一。注意 FramePack **不使用 timestep 蒸馏**（项目页明确「No timestep distillation」）。

## Infra（训练 / 推理工程）
**训练**：所有实验在 H100 GPU 集群完成（详细训练超参在补充材料）；典型微调配置为单 8×A100-80G 节点、13B HunyuanVideo、480p、LoRA、batch 64（窗口 2–3）。

**推理 / 部署（README 一手数据）**：
- **显存**：生成 1 分钟（60s @30fps = 1800 帧）13B 模型最低仅需 **6GB GPU 显存**（笔记本可用）。
- **速度**：RTX 4090 桌面约 **2.5 s/帧（未优化）或 1.5 s/帧（开 TeaCache）**；3070ti / 3060 笔记本约慢 4–8×。论文/项目页样例「Image-to-5s（150 帧）」「Image-to-60s（1800 帧）」均在 **RTX 3060 6GB 笔记本 + 13B HY 变体**上跑出。
- **流式可视反馈**：因为是 next-frame-section 预测，每段生成完即可见，无需等整段视频生成完。
- **注意力后端**：默认 PyTorch attention，可选 xformers / flash-attn / sage-attention（开 sage-attention 会轻微影响结果，建议先不开）。
- **加速/量化**：支持 TeaCache（缓存加速，约 30% 用户能得到与原结果接近的输出，但非无损、有时影响明显，建议「TeaCache 试想法 + 完整扩散出成品」）；也支持 bnb 量化、gguf。
- **部署形态**：官方提供桌面软件（Gradio GUI，`demo_gradio.py`，支持 `--share/--port/--server`）与 Windows 一键包（CUDA 12.6 + PyTorch 2.6）；需 RTX 30/40/50 系（支持 fp16/bf16），模型自动从 HuggingFace 下载（>30GB）。官方强调唯一官网是该 GitHub 仓库，framepack.co/.net/.ai 等均为山寨。
- **变体迭代（README News）**：2025-05-03 发布 **FramePack-F1**；2025-06-26 起 **FramePack-P1**（采用 Planned Anti-Drifting + History Discretization 两项设计），2025-07-14 上传纯 text2video 防漂移压力测试结果。

## 评测 benchmark（把效果讲清楚）
评测以 **HunyuanVideo 为基座**（正文报告 HY，Wan 结果在补充材料）。测试输入为 512 条真实用户 prompt（t2v）和 512 对图-prompt（i2v），长视频默认 30s、短视频 5s。

**指标体系**（对齐 VBench/VBench2 思路，全为相对/对比型）：
- 全局质量指标↑：Clarity（MUSIQ）、Aesthetic（LAION 美学）、Motion（运动平滑度，VBench 改的视频插帧模型，论文引 ref[23] 即 RIFE）、Dynamic（动态度，VBench 改 RAFT，与 Motion 互为权衡）、Semantic（ViCLIP 视频-文本一致性）、Anatomy（VBench 预训练 ViT 检测手/脸/身体）、Identity（ArcFace + RetinaFace 人脸一致性）。
- **漂移指标 ∆^M_drift↓**（本文自定义）：start-end 对比 = |M(前 15% 帧) − M(后 15% 帧)|，越小越不漂移；对 Clarity/Motion/Semantic/Anatomy 各算一个。
- 人评：A/B test，每个消融配置 ≥100 次评估，报 ELO-K32 分与排名。

**消融关键结论（Table 1，HunyuanVideo）**：
- **反向防漂移采样（inverted anti-drifting）在 7 个指标中 4 个最优，且在所有漂移指标上最优**；但动态范围（Dynamic）相对小。
- vanilla 采样虽 Dynamic 最高，但很可能是漂移效应而非真实质量（ELO 偏低佐证）。
- **vanilla + 历史离散化（+D）人评极具竞争力，且动态范围大得多**——兼顾防漂移与动态。
- 同一采样方式下、不同具体打包配置之间差异小且随机，说明**整体架构（采样方式）贡献远大于具体 kernel 配置**。
- ELO 排名分档：1030–1050（Rank6）… 1210–1235（Rank1）。反向防漂移系列与 +D 系列稳居 Rank1（ELO 1210–1235）。
- 历史离散化参数 K：K=128 给强防漂移且训练难度最小。

**与其他方法对比（Table 2，HunyuanVideo 基座，关键数字）**：

| 方法 | Clarity↑ | Dynamic↑ | Semantic↑ | ∆Clarity_drift↓ | ELO↑ | Rank |
|---|---|---|---|---|---|---|
| Repeating image-to-video | 56.73% | 91.21% | 17.74% | 9.51% | 1015 | 5 |
| Anchor frames（仿 StreamingT2V） | 69.58% | 74.97% | 25.76% | 2.85% | 1173 | 2 |
| Causal attention（仿 CausVid） | 62.88% | 88.27% | 19.15% | 7.45% | 1087 | 4 |
| DiffusionForcing（σ_test=0.1，随机 σ_train） | 66.08% | 91.59% | 23.14% | 4.84% | 1170 | 2 |
| DiffusionForcing（σ_test=0.5） | 67.41% | 91.08% | 24.03% | 3.55% | 1174 | 2 |
| History guidance（仿 HistoryGuidance） | 68.05% | 73.39% | 24.88% | 7.35% | 1152 | 3 |
| **Inverted anti-drifting（本文）** | **71.15%** | 89.29% | 28.15% | **2.25%** | **1220** | **1** |
| **Vanilla + 离散历史（本文，K=256）** | 70.01% | 91.74% | **28.37%** | 3.13% | **1224** | **1** |

要点：本文两个候选（反向防漂移、vanilla+离散历史）在 ELO 上明显领先（1220 / 1224），漂移指标全面最低；其中反向防漂移漂移最小但动态范围略小，离散历史在漂移与动态间更平衡。简单 Repeating i2v（即手动循环上一帧重生成）质量与抗漂移最差（ELO 1015，∆Clarity_drift 9.51%），印证「朴素循环 5–6 次即崩坏」的项目页论断。

> 补充材料还包含：特征相似度打包在视频游戏（世界模型）基准上的测试、Wan 基座结果、各指标分解、K 的更细致消融。这些具体数字本页未抓取到补充材料正文，故标注「见补充材料」。
> 注：本工作以「相对/消融 + 人评 ELO」为主，**未报告**与外部 SOTA 的标准 FVD / FID / VBench 总分等绝对数值。

## 创新点与影响
**核心贡献**：
1. **帧上下文打包（Frame Context Packing）**：用按重要性的渐进 patchify 压缩，把 next-frame 预测的上下文长度收敛到与视频长度无关的固定上限，实现流式生成 O(1) 复杂度、并支持上千帧推理与较大 batch 训练。
2. **统一直面「遗忘-漂移」权衡**：提出规划端点、反向采样、历史离散化三类防漂移方法，从「打破因果、引入双向上下文」和「缩小训练-推理历史分布差」两条路径系统性抑制漂移，并用消融验证。
3. **可落地的低门槛**：把 13B 视频基座的长视频生成压到 6GB 笔记本显存、把微调拉到 8×A100 单节点 batch 64，「让视频扩散像图像扩散」。

**影响**：FramePack 由 ControlNet 作者发布，开源后在社区迅速流行（Windows 一键包、Gradio 桌面端），成为消费级显卡上做长视频生成的代表性方案；F1/P1 等后续变体持续迭代。项目页「See also」指向作者后续工作《Pretraining Frame Preservation in Autoregressive Video Memory Compression》(arXiv 2512.23851)，延续帧记忆压缩主线。

**已知局限**：
- 反向防漂移采样动态范围偏小（运动幅度受限）。
- 端点规划在大幅/非周期运动时仍可能在端点处漂移（靠端点间足够远使累积误差近似可忽略）。
- 历史离散化 K 过大训练难、过小丢记忆，需折中。
- 极长视频尾帧压缩到 latent 极限时需特殊 tail 处理。
- 数据规模/配比、补充材料中 Wan 与世界模型基准的具体数字未在正文充分披露。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2504.12626
- arxiv_pdf: https://arxiv.org/pdf/2504.12626
- github: https://github.com/lllyasviel/FramePack
- project_page: https://lllyasviel.github.io/frame_pack_gitpage/
- followup (See also): https://arxiv.org/abs/2512.23851

## 一手源存档（sources/）
- [arxiv-2504.12626.pdf](https://arxiv.org/pdf/2504.12626)  （arXiv 原文 PDF，不入 git）
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/framepack--readme.md)
- [projectpage.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/framepack--projectpage.md)
