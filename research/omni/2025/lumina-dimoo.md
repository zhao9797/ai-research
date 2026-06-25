---
title: "Lumina-DiMOO: An Omni Diffusion Large Language Model for Multi-Modal Generation and Understanding"
org: "Shanghai AI Laboratory / Alpha-VLLM"
country: China
date: "2025-10"
type: tech-report
category: unified
tags: [discrete-diffusion, unified-multimodal, masked-generation, dllm, t2i, image-editing, image-understanding, self-grpo, open-source]
url: "https://arxiv.org/abs/2510.06308"
arxiv: "https://arxiv.org/abs/2510.06308"
pdf_url: "https://arxiv.org/pdf/2510.06308"
github_url: "https://github.com/Alpha-VLLM/Lumina-DiMOO"
hf_url: "https://huggingface.co/Alpha-VLLM/Lumina-DiMOO"
modelscope_url: ""
project_url: "https://synbol.github.io/Lumina-DiMOO/"
downloaded: [arxiv-2510.06308.pdf, lumina-dimoo--readme.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Lumina-DiMOO 是上海 AI 实验室 Alpha-VLLM 团队 2025 年 9–10 月开源的**全离散扩散（fully discrete diffusion）统一多模态基础模型**——把文本 token、图像 token 全部纳入同一套"掩码-去噪"扩散建模，单一 8B 模型一体支持文生图、图生图（编辑/可控/主体驱动/风格迁移/多视图/稠密预测）与图像理解；相比此前 AR / AR-Diffusion 混合范式采样效率大幅提升（Figure 12：T2I 1024、64 步，裸模 45s vs AR 的 Lumina-mGPT 2.0 768 分辨率 710s ≈ **15.8×**，叠加自研 ML-Cache 至 22s ≈ **32.3×**；与 BAGEL 大致持平），并在 GenEval 拿到 **88%**（Self-GRPO 后 91%）、登顶腾讯混元维护的 UniGenBench 开源统一模型榜首。

## 背景与定位
统一"理解+生成"模型此前主要走三条路（论文 Figure 2）：
1. **纯自回归（AR）**：Chameleon、[[lumina-mgpt]] 把图像也离散成 token 做 next-token 预测——简洁但生成极慢（动辄数分钟）、图像质量偏弱。
2. **AR + Diffusion Head / AR + 离散扩散**：MetaQueries、BLIP3-o 在 AR 后接 diffusion head 解码图像 token（牺牲了"统一"概念）；Show-o 用 AR+离散扩散提速，但文本侧离散扩散探索不充分。
3. **纯离散扩散（dLLM）**：随着 [[llada]]（8B 文本 dLLM）等把离散扩散 scale 上来，同期工作 MMaDA 首次验证了"纯离散扩散统一理解与生成"的可行性，但性能有限、不支持完整下游生成任务。

Lumina-DiMOO 站在第三条路上，定位为"把纯离散扩散统一模型做到 SOTA 且任务完整"的开源工作：以预训练文本 dLLM（LLaDA-Base）为底座扩成多模态，既吃到离散扩散的**并行解码/双向注意力/任意顺序生成/天然 infilling** 红利，又补齐了 MMaDA 缺失的任意分辨率、图像编辑、可控生成、多视图、零样本 inpainting/extrapolation 等能力。相关基础工作可参见 [[discrete-diffusion]] [[maskgit]] [[llada]] [[mmada]]。

## 模型架构
**Backbone：纯离散扩散 Transformer（双向注意力的掩码 dLLM），不是 DiT / U-Net / flow matching。** 直接以 **LLaDA-Base 作为底座、无任何结构改动**（论文 §3.2 "without any structural modifications"），通过扩词表 + 多阶段训练改造成多模态。模型规模 8B（README/各对比表标注 8B；底座 LLaDA 即 8B 量级）。

**统一离散扩散建模（核心）**：把图文混合序列 x=(x₁…x_L) 看成来自联合词表的 token 序列。前向过程按掩码比率 m∈(0,1] 随机抽掩码集 ℳ（|ℳ|=⌊L·m⌋），被选位置替换为特殊 `[Mask]` token；模型 p_θ 在掩码位置**并行预测**原 token，训练目标为掩码位置的交叉熵（公式 1–3）。文本与图像位置**共用同一掩码-去噪目标**——这正是"统一优化目标"的来源。推理时从全掩码出发，经 T 步"预测-采样-重掩码"逐步精修。

**Visual tokenizer（离散，关键选型）**：采用 **aMUSEd-VQ** 码本（16×16 下采样，码本大小 8,192）。团队权衡过 SBER-MoVQGAN（8×8 下采样，重建最好但高分辨率 token 序列过长、算力爆炸）、Chameleon-VQ（重建略差）、Open-MAGVIT2（重建好但 token 格式不匹配建模需求），最终选 16×16 的 aMUSEd-VQ 平衡质量与序列长度。其短板是缺语义信息（不利理解任务），团队靠**扩充理解数据**来补。

**词表扩展**：原 LLaDA 文本词表 126,345，叠加 8,192 个 aMUSEd-VQ 视觉 token，再加一组特殊 token（`<IMAGE></IMAGE>`、`<canny>/<depth>/<openpose>/<hed>` 等条件图标记、`<system>/<user>/<answer>`、`<end-of-line>`、CFG 用的 `<uncondition>`）。**只有新加的视觉 token 和特殊 token 需要学习**，文本能力直接继承。

**Text encoder / 条件注入**：无独立 T5/CLIP text encoder——文本与图像 token 在同一序列里由同一个 dLLM 处理（真正的单塔统一），prompt 即 condition token c；图像生成用 **classifier-free guidance（CFG）**，靠 `<uncondition>` token 实现无条件分支。

**任意分辨率（相对 MMaDA 的关键改进）**：LLaDA 的 1D RoPE 为文本设计，512×1024 与 1024×512 会被拍平成同长序列、丢失长宽比。Lumina-DiMOO 在每行图像 token 末尾插入 `<end-of-line>` token 作为显式行分隔符，从而**无需新设计位置编码**即可从 1D 序列正确解析/重建 2D 形状，支持任意分辨率。对照之下 MMaDA 只能固定 512×512。

**推理采样策略**：
- 图像生成：把整张图的 image token（除 `<end-of-line>`）当作一个生成块，沿用 MaskGIT 思路分四阶段，全掩码起步，每步【Predict → Sample（先把全词表概率约束到 8,192 图像子词表，取最高概率 token，其概率作 confidence；已解码 token confidence 置 −∞）→ Mask Schedule（余弦 schedule 定每步重掩码数 k_t）→ Remask（按 confidence top-k 重掩码）】，跑预定 T 步（默认 **64 步**）。
- 图像理解：产出文本 token，沿用 LLaDA/MMaDA 的半自回归（semi-AR）——全掩码文本序列分块，块内并行预测、块间顺序解码（默认 block length 256、128 步；README 示例脚本 block_length 32）。引入 **early stopping**：当前块完成且检测到 `</answer>` 即停，避免半自回归"总要补满预定长度"的冗余计算。

## 数据
四阶段共采约 **80M（预训练）+ 3M（中训）+ 30M（SFT）** 量级图文数据，全部来源在论文 §5 逐条列出（均为公开/再描述数据集，无自建大规模私有语料的硬声明，仅 SFT 含少量 in-house 合成数据）：

- **Stage-I 预训练（≈80M 图文对）**：30M 来自再描述（re-captioned）公开集（LAION-400M 用于理解预训练、CC12M），50M 来自 Lumina-Image 2.0 / Lumina-mGPT 2.0 用于生成预训练。目标：建立视觉能力 + 图文表征对齐。
- **Stage-II 中训（额外 3M 图像）**：补"难域"理解与图生图。理解侧：MMTable、TinyChart（表格/图表）、AutoGeo、MAVIS（数学公式/几何）、MultiUI（UI 解析），**全部用 Qwen2.5-VL 重新打 caption**。图生图侧：UltraEdit、OmniEdit、OminiControl、Lumina-mGPT 2.0。
- **Stage-III SFT（理解 15M + 生成 15M + 图生图若干）**：理解 15M = MAmmoTH-VL 2M + InternVL-2.5-SFT 13M；生成 15M = Lumina-Image 2.0（仅取最高质量子集）+ Blip3o-60k + ShareGPT-4o-Image + 自建合成数据；图生图含主体驱动/可控/稠密预测/风格迁移各 200K（VisualCloze）、指令编辑 500K（UniWorld）、低层视觉 200K（Lumina-OmniLV，超分/去雾/去噪——论文坦言此类低层任务效果差）、多视图沿用 Lumina-mGPT 数据。
- **Stage-IV Self-GRPO（仅需文本 prompt）**：取 GenRef 中类 GenEval 模板的 prompt 子集，用 DSG 方法抽 (entity, relation, value) 三元组，构造单选题做语义对齐监督；干扰项从全局候选池（实体/关系/数量/颜色）里选语义相近者，保证 QA 既难又有信息量。

清洗/美学/安全过滤的具体阈值与流程**未披露**；re-captioning 用 Qwen2.5-VL（中训）等模型完成。

## 训练方法
**训练目标**：统一的**掩码离散扩散交叉熵**（masked cross-entropy over随机采样的掩码比率 m，文本与图像位置同等对待，公式 3），不是 diffusion 噪声预测、不是 flow matching、也不是标准 next-token。

**四阶段流水线**（超参见论文 Table 2）：
| 阶段 | 目标 | LR | Batch | GPU | 生成分辨率 |
|---|---|---|---|---|---|
| Stage-I 预训练 | 图文对齐、培养视觉能力 | 2e-4 | 1024 | 64×A800 | 256→512（渐进） |
| Stage-II 中训 | 引入多种图生图任务 + 难域理解 | 2e-4 | 512 | 64×A800 | 1024（图生图 512） |
| Stage-III SFT | 指令跟随 + 质量提升 | 2e-5 | 512 | 64×A800 | 1024（图生图 512） |
| Stage-IV Self-GRPO | 自我提升 RL | 3e-6 | 48 | 8×H20 | 1024 |

优化器 AdamW（前三阶段 β=(0.9,0.95)，Self-GRPO β=(0.9,0.99)），constant LR，weight decay 0.1，grad clip 1.0。

- **底座初始化的必要性（消融，§7.2）**：以 LLaDA-SFT 初始化 vs. 从头训（各 5M 生成 + 5M 理解，跳过预训练直接 256 分辨率 SFT）。**从头训会出现极大 gradient norm，几乎无法生成图像/做理解；从 LLaDA 初始化则两者都正常**——证明继承文本 dLLM 能力在离散扩散框架下是必需的（这一点与 AR 多模态里"从头训不影响性能"的结论相反）。
- **渐进分辨率**：预训练从低分辨率（≈256×256，约 256 token）逐步到中分辨率（≈512×512，约 1024 token），缓解长视觉序列的学习难度。
- **Efficient Mid-Training**：图生图任务（处理 2+ 张图、序列长）固定 512 以提效率；T2I 用 1024 抠细节；理解用动态分辨率（原分辨率夹在 512–1024，超 1024 降采到 1024，低于 512 升到 512）。中训/SFT 阶段**只对 target image / target text（answer）算 loss**。

**Self-GRPO（本工作专属创新，§4.4）**：一个**联合优化 T2I 与 MMU 的自改进 RL 框架**，充分利用"同一模型既会生成又会理解"的统一性。机制：给定 prompt p，从当前策略采 G 张候选图（每张 L=4096 token 的序列）；再给一组关于该图的单选题 {q_n}，模型基于自己生成的图回答，得到每样本的 T2I 与 MMU 损失 ℓ_T2I、ℓ_MMU；reward r 定义为答对题数，经 softmax 温度 α 归一化成权重 w，最小化 reward 加权目标（公式 5–8），含 KL 正则。工程优化：①参照 UniRL **去掉 old policy π_old** 省显存；②**step trajectory following**——保留完整采样轨迹但只在选定时间步 𝒯_sel 上算梯度（因 T2I 主体内容在早期步即生成），兼顾轨迹一致性与显存。相比 UniRL（只有 answer-level MMU 监督）和 UniGRPO（忽略生成-推理对齐），Self-GRPO 既有结构化语义反馈又保证轨迹一致。效果：GenEval 整体 +3%（88%→91%），Colors/Attribute 提升最明显。

蒸馏/步数蒸馏/consistency/LCM **未使用**；加速靠下面的训练-free ML-Cache。

## Infra（训练 / 推理工程）
- **算力**：主训练 **64×A800**（Stage-I/II/III），Self-GRPO 阶段 **8×H20**。总 GPU·时/吞吐**未披露**。
- **训练框架**：致谢中明确由华为 **MindSpeed-MM**（面向昇腾 Ascend 芯片优化的大规模多模态分布式训练框架）支持实现。具体并行策略（TP/PP/FSDP）、混合精度配置**未在论文/README 披露**。
- **推理加速 ML-Cache（Max Logit-based Cache，训练-free，§3.3.2）**：双向注意力无法用 AR 的 KV-Cache 做无损加速，但可做**有损缓存**。观察：**最大 logit 越高的 token，其表征在相邻步越稳定**——Figure 4 显示 top 94% 最大 logit 的 token 与上一步余弦相似度 >0.99。于是用 max logit 作代理识别可复用 token：超参 `cache_ratio`（复用比例，越高越快）选 top-cache_ratio 的 token 直接复用上一步的 K/V 与 logits，其余重算；再用 `warmup_ratio`（前若干步全算，避免上下文差时估计不准）和 `refresh_interval`（每隔若干步全算一次，抑制误差累积）控制质量-效率权衡。README 默认 `cache_ratio=0.9, warmup_ratio=0.3, refresh_interval=5`。
- **单卡实测（README，单张 A800，1024×1024）**：原始 58.2s / 38.9 GB → +ML-Cache **32.2s / 45.9 GB**（约 1.8× 提速，显存增 7 GB）。论文 §7.1 给出 ML-Cache 对 T2I 提速 **2.05×**、对理解 **1.87×**。
- **部署形态**：开源 checkpoint 在 HuggingFace（Apache-2.0），提供单卡/DDP（torchrun 多卡）推理脚本、ComfyUI 与 Diffusers 集成、VLMEvalKit 评测接入；理解评测用 LLM-as-judge（需配 OpenAI API）。

## 评测 benchmark（把效果讲清楚）
所有数字来自已落盘的论文 PDF（Tables 3–10、Figure 12）与 README。Lumina-DiMOO 为 8B，纯离散扩散架构。

**文生图（T2I）**
- **GenEval（Table 3）**：整体 **0.88**（Self-GRPO 后 **0.91**），论文正文称超 FLUX.1[Dev]（82%）、Lumina-mGPT 2.0（69%）、Janus-Pro（80%）、BAGEL（82%）、GPT-4o（84%），较同架构 MMaDA（0.63）整体 **+25%**（注：FLUX.1[Dev] 在论文正文记 82%，但 Table 3 同行 Overall 列为 0.66，原文自相矛盾，此处采正文口径）。基础版各分项：Single 1.0 / Two 0.94 / Counting 0.85 / Colors 0.89 / Position 0.85 / Attribute 0.76（强项 Position 与 Attribute——Position 0.85 居统一模型之首，Attribute 0.76 与 OmniGen2 并列最高）。Self-GRPO 版各分项（括号为相对基础版增量，来自 Table 3）：Single 1.0 / Two 0.96(+2) / Counting 0.87(+2) / Colors 0.95(+6) / Position 0.85(+0) / Attribute 0.82(+6) / Overall 0.91(+3)——提升最大的是 Colors 与 Attribute（各 +6pt）。
- **DPG（Table 4）**：整体 **86.04**，超所有对比模型（FLUX.1[Dev] 83.84/85.07、SD3-Medium 84.08、GPT-4o 85.15、BAGEL 85.07）；同架构 MMaDA 自测仅 69.97。Entity/Relation 维度尤强。
- **UniGenBench（Table 5，腾讯混元团队维护）**：整体 **71.12**，超全部统一模型（OmniGen2 63.09、BAGEL 61.53、Janus-Pro 61.61、MMaDA 41.35），在 Layout 与 Attribute 维度尤为突出；**开源统一模型榜单第 1（2025-09-20）**。
- **OneIG-EN（Table 6，五维平均）**：整体 **0.455**，居首，超 FLUX.1[Dev]（0.434）、BAGEL（0.361）、Janus-Pro（0.267）；Alignment（0.816）、Text（0.551）、Reasoning（0.276）三项第一。
- **TIIF（Table 7）**：整体 71.27/68.53（short/long），**第二，仅次于 FLUX.1[dev]（71.09/71.78）**，超 Janus-Pro-7B、Show-o、SD3 等。

**图生图（I2I）**
- **可控生成 Graph-200K（Table 8）**：Canny FID 30.35 / SSIM 0.65、Depth RMSE **8.31**（优于专家模型 ControlNet、OminiControl）/ FID 34.38 / SSIM 0.62，质量与文本一致性领先通用生成模型，depth-to-image 甚至超专家模型。
- **风格迁移 / 主体驱动 / 编辑（Table 9）**：风格迁移文本对齐 0.32 / 风格一致 0.53（较 OmniGen +5%/+1%）；主体驱动 DINOv2 **80.57** / CLIP-I **89.36** / CLIP-T 34.72（较前 SOTA Lumina-mGPT 2.0 分别 +3.97/+1.99/+0.82）；图像编辑（ImgEdit，GPT-4.1 评分）Add **3.82** / Replace **3.83** / Remove 2.76 / Style 4.18——Add、Replace 超 OmniGen、BAGEL、UniWorld-V1，但 Remove、Style 仍有提升空间。
- **零样本 inpainting / extrapolation**：掩码训练范式天然支持，**无需微调**（Figure 7）。

**图像理解（Table 10，5 个 VLM benchmark）**：POPE **87.4** / MME-P 1534.2 / MMB 84.5 / SEED **83.1** / MMMU **58.6**。在统一模型里 POPE、SEED、MMMU 三项领先；显著超同架构 MMaDA（全维度）；MMMU 58.6 也超多数纯理解模型。注意 MME-P（1534.2）低于 BLIP3-o（1682.6）、BAGEL（1687.0）等部分对手。

**效率（Figure 12 / README）**：T2I 1024、64 步，裸模 **45s**——较 AR 的 Lumina-mGPT 2.0（768，710s）≈ **15.8×**、Emu3-Gen（720，545s）更快，与 BAGEL（1024，45s）持平；再叠加 ML-Cache 降到 **22s**（即 2.05×），相对 Lumina-mGPT 2.0 总计 ≈ **32.3×**（注：论文 Figure 12 标的 32.3× 即 ML-Cache 版对 Lumina-mGPT 2.0 的比值，已含 ML-Cache 那一档 2.05×，不可再叠乘；Intro 正文"32× + 额外 2×"的措辞与 Figure 12 的数值口径有出入，以 Figure 12 实测秒数为准）。理解任务（block 256、128 步）17s，因半自回归分块提速幅度较小（ML-Cache 1.87×）。

**消融关键结论**：①从头训失败、必须 LLaDA 初始化（§7.2）；②ML-Cache 提速 T2I 2.05×/理解 1.87×，代价是显存升高（38.9→45.9 GB）；③Self-GRPO 在 GenEval +3%。

## 创新点与影响
**核心贡献**
1. **首个做到 SOTA 且任务完整的纯离散扩散统一多模态模型**：把文/图全部统一进单一掩码-去噪扩散目标，单 8B 模型覆盖 T2I + 多类图生图 + 理解，开源（Apache-2.0，HF 放出 checkpoint、训练/推理/评测代码）。
2. **`<end-of-line>` token 解决任意分辨率**：无需新位置编码即让 1D dLLM 处理 2D 任意长宽比图像，突破 MMaDA 固定 512×512 的限制。
3. **Self-GRPO**：利用"同模型既生成又理解"的统一性做自改进 RL——用模型自己回答关于自己生成图的单选题作 reward，配合去 old-policy、step-trajectory-following 的显存优化，闭合生成-理解训练回路。
4. **ML-Cache**：基于"高 max logit 即表征稳定"的训练-free 缓存，为双向注意力 dLLM 提供 KV-Cache 的有损替代，约 2× 加速。
5. **离散扩散原生新能力**：零样本 inpainting/extrapolation，以及 **Interactive Retouching**——用户框选局部反复重生成而**100% 保证框外内容不变**（论文强调这是 diffusion/AR/GPT-4o/Nano-Banana 等都难做到的）。

**影响与后续**：登顶 UniGenBench 开源统一模型榜首，成为离散扩散统一模型的强开源基线；社区已接入 Diffusers、ComfyUI、VLMEvalKit。团队后续延伸出 **dMLLM-TTS**（扩散 MLLM 的自验证测试时扩展，CVPR 2026）与 **HT-GRPO**（2026-05 论文）等工作，并把仓库扩成"用掩码范式构建世界模型"的指南方向。

**已知局限**（论文/README 自陈）：① aMUSEd-VQ tokenizer 缺语义、需靠扩数据补理解；②低层视觉任务（超分/去雾/去噪）效果差；③图像编辑的 Remove、Style 子项偏弱；④MME-P 等个别理解指标落后 BAGEL/BLIP3-o；⑤理解任务的提速因半自回归而有限；⑥ML-Cache 提速以增显存为代价；⑦尚不支持视频/音频——团队将其列为未来方向（需通用 tokenizer、时序架构、新训练技术）。总 GPU·时、并行细节、数据清洗阈值等工程数字未公开。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2510.06308
- arxiv_pdf: https://arxiv.org/pdf/2510.06308
- github: https://github.com/Alpha-VLLM/Lumina-DiMOO
- huggingface (model): https://huggingface.co/Alpha-VLLM/Lumina-DiMOO
- project_page (demo & benchmark): https://synbol.github.io/Lumina-DiMOO/
- UniGenBench leaderboard: https://huggingface.co/spaces/CodeGoat24/UniGenBench_Leaderboard

## 本地落盘文件
- ../../../sources/omni/2025/arxiv-2510.06308.pdf  （技术报告 PDF v1，2025-10-7，29.9 MB / 33 页：正文 1–24 页（Conclusion 在 p24）+ 其后参考文献；本地精读，未入 git）
- ../../../sources/omni/2025/lumina-dimoo--readme.md  （GitHub 仓库页 markdown 快照，含 HF 链接 / news / ML-Cache 默认超参 / 单卡实测 / 训练框架致谢）
