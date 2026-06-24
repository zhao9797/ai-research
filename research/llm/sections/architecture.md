# 架构（Architecture）

> 概述：2020→2026 这六年，LLM 架构沿四条主线交织演进。**(1) Transformer 组件标准化**：从 GPT-3 原始 decoder-only 逐步收敛出今天的事实标准配方——RoPE 位置编码、RMSNorm 归一化、SwiGLU 激活、GQA/MLA 注意力、Pre-Norm + QK-Norm 稳定性技巧。**(2) 突破二次注意力的两条路线**：一条是稀疏/低秩/线性/SSM（Longformer/Reformer/Linformer → Performer → S4 → Mamba → 线性注意力/DeltaNet），另一条是工程化的精确注意力（FlashAttention 系列）与 KV cache 压缩谱系（MQA → GQA → MLA → 原生稀疏注意力 NSA/DSA）。**(3) 稀疏化（MoE）成为大模型主流**：GShard/Switch/GLaM 奠基，DeepSeekMoE 的"细粒度专家 + 共享专家 + 无辅助损失均衡"被广泛复制，2024-2026 几乎所有旗舰（DeepSeek-V3、Llama 4、Qwen3、Kimi K2 等）转向 MoE，激活比越压越低（Kimi K2 1T/32B、Qwen3-Next 80B/3B）。**(4) 从单模态到原生多模态**：CLIP/ViT 提供视觉骨干，经"冻结桥接"（Flamingo/BLIP-2）→"投影 + 指令微调"（LLaVA 范式）→"早融合 token 化"（Chameleon/Llama 4）→"原生全模态"（Qwen2.5-Omni），逐步走向单一骨干原生理解与生成。到 2025-2026，混合架构（Transformer + Mamba/线性注意力）与硬件-系统协同设计成为前沿。

---

## 一、基础组件：归一化 / 激活 / 位置编码 / 训练稳定性

- RMSNorm — Root Mean Square Layer Normalization (爱丁堡大学/苏黎世大学, 2019-10, paper) — 去掉 LayerNorm 的均值中心化，只用均方根缩放：RMSNorm(x)=x/RMS(x)·g，省一项统计、约 7%–64% 提速；成为 LLaMA/Qwen/Gemma/DeepSeek/Mistral 等绝大多数现代 LLM 的默认归一化。 https://arxiv.org/abs/1910.07467
- GLU Variants Improve Transformer — SwiGLU (Google, 2020-02, paper) — Noam Shazeer 测试门控线性单元变体替换 FFN 激活，FFN(x)=(Swish(xW)⊙xV)W2；为保持 FLOPs 相当把中间维设为约 8/3·d；SwiGLU/GEGLU 稳定优于 ReLU/GELU，被几乎所有现代 LLM 采用。 https://arxiv.org/abs/2002.05202
- Query-Key Normalization — QKNorm (Alex Henry 等学术合作, 2020-10, paper) — 注意力打分前对 q/k 沿头维做 ℓ2 归一化，再乘可学习温度 g 取代 1/√d，约束点积到 [-1,1] 防 softmax 饱和；原始在 5 个低资源翻译对 +0.928 BLEU，后被 Chameleon/OLMo-2/Gemma-2/3/Qwen3 用于稳定大规模训练。 https://arxiv.org/abs/2010.04245
- RoFormer — Rotary Position Embedding (RoPE) (追一科技 Zhuiyi, 2021-04, paper) — 用旋转矩阵把绝对位置编进 Q/K（θ_i=10000^(-2i/d)），使注意力内积只依赖相对位置差 (m−n)，统一绝对与相对位置；成为 LLaMA/Qwen/DeepSeek/GLM 等几乎所有主流 LLM 的默认位置编码。 https://arxiv.org/abs/2104.09864
- ALiBi — Attention with Linear Biases (UW/FAIR/AI2, 2021-08, paper) — 不用位置嵌入，softmax 前对分数加 −m·(i−j) 的 head-specific 线性负偏置，实现"短训练、长推理"强外推（1024 训练→2048 推理质量持平），省约 11% 时间/内存；被 BLOOM、MPT 采用。 https://arxiv.org/abs/2108.12409
- DeepNet — Scaling Transformers to 1,000 Layers (DeepNorm) (Microsoft Research, 2022-03, paper) — 提出 DeepNorm x=LayerNorm(α·x+f(x)) 加理论推导初始化 β，兼得 Post-LN 性能与 Pre-LN 稳定性，首次稳定堆到 1000 层（2500 子层）；200 层 3.2B 在 7482 翻译方向上 SOTA。 https://arxiv.org/abs/2203.00555
- Tensor Programs V — muP / muTransfer (Microsoft/OpenAI, 2022-03, paper) — Maximal Update Parametrization 下最优超参随宽度稳定，可在小代理模型调参后零样本迁移到大模型；13M→BERT-large 迁移超过原版、应用到 GPT-3 规模，大幅降低大模型调参成本。 https://arxiv.org/abs/2203.03466
- NoPE — Impact of Positional Encoding on Length Generalization (Mila/McGill/IBM/ServiceNow, 2023-05, paper) — 系统对比五类位置编码，发现 decoder-only 在推理类任务上「不加任何显式位置编码 (NoPE)」长度外推最好，因果注意力可隐式编码绝对位置；思想被 Llama 4 iRoPE 等借鉴。 https://arxiv.org/abs/2305.19466
- nGPT — Normalized Transformer on the Hypersphere (NVIDIA, 2024-10, paper) — 把 embedding/MLP/注意力矩阵/隐状态全部约束到单位超球面，每层视为球面上向目标的可学习步长位移，去掉 LayerNorm 与权重衰减；相同精度训练步数减少约 4×–20×。 https://arxiv.org/abs/2410.01131

---

## 二、长上下文：稀疏 / 低秩 / 线性注意力与上下文扩展

- Longformer (Allen Institute for AI, 2020-04, paper) — 用「滑动窗口 + 扩张窗口 + 全局注意力」的稀疏注意力把复杂度从 O(n²) 降到 O(n)，是 sliding-window attention 的代表作。 https://arxiv.org/abs/2004.05150
- Reformer (Google Research / UC Berkeley, 2020-01, paper) — 用局部敏感哈希（LSH）注意力把复杂度降到 O(L log L)，并用可逆残差层省去激活缓存，使单卡也能训练超长序列（最长可达 100 万 token）。 https://arxiv.org/abs/2001.04451
- Linformer (Meta / Facebook AI, 2020-06, paper) — 证明自注意力矩阵低秩，可用两个线性投影把 key/value 序列长度压到常数维度 k，把注意力复杂度从 O(n²) 降到 O(n)。 https://arxiv.org/abs/2006.04768
- Linear Transformers Are RNNs (Idiap / EPFL, 2020-06, paper) — 用核特征映射（elu+1）把 softmax 注意力线性化到 O(N)，并揭示带因果掩码的线性注意力在推理时等价于 RNN，可常数内存自回归生成、推理快达数千倍。 https://arxiv.org/abs/2006.16236
- BigBird (Google Research, 2020-07, paper) — 提出「全局 + 局部窗口 + 随机」三类稀疏注意力组合，把复杂度降到线性，并证明它图灵完备、能逼近完整注意力。 https://arxiv.org/abs/2007.14062
- Performer — FAVOR+ (Google/Cambridge/DeepMind, 2020-09, paper) — 用正交随机特征无偏近似 softmax 注意力核，把注意力降到线性时间/空间复杂度，不依赖稀疏或低秩假设。 https://arxiv.org/abs/2009.14794
- YaRN — Efficient Context Window Extension (Nous Research/EleutherAI/Geneva, 2023-08, paper) — NTK-by-parts 分频插值 + 注意力温度缩放，仅用约 0.1% 预训练 token、约 400 步继续训练即把 LLaMA 上下文从 4K 扩到 64K/128K，长文困惑度与 passkey 检索优于位置插值与纯 NTK。 https://arxiv.org/abs/2309.00071

---

## 三、KV cache 压缩与硬件高效注意力

- Multi-Query Attention (MQA) (Google, 2019-11, paper) — Noam Shazeer 提出所有注意力头共享单一 K/V 头、只保留多个 Q 头，把 KV cache 缩到约 1/h、加速增量解码，质量轻微下降；是 KV 压缩谱系（MQA→GQA→MLA）的源头，被 PaLM/Falcon 采用。 https://arxiv.org/abs/1911.02150
- FlashAttention (Stanford / SUNY Buffalo, 2022-05, paper) — 用 tiling + online softmax + IO 感知把精确注意力的 HBM 读写降到次二次，显存从 O(N²) 降到 O(N)、GPT-2 训练约 3× 加速且数值等价（非近似），成为现代 LLM 标准注意力 kernel。 https://arxiv.org/abs/2205.14135
- GQA — Grouped-Query Attention (Google Research, 2023-05, paper) — 把 H 个 query 头分 G 组共享 K/V（介于 MHA 与 MQA 之间，KV cache ∝ G/H），并用约 5% 原预训练算力把 MHA 检查点 uptrain 成 GQA；以接近 MQA 的速度达接近 MHA 的质量，成 LLaMA-2/3、Mistral、Qwen 的默认注意力。 https://arxiv.org/abs/2305.13245
- FlashAttention-3 (Colfax/Meta/NVIDIA/Princeton/Together, 2024-07, paper) — 针对 Hopper(H100) 用异步 WGMMA/TMA、warp 专门化、ping-pong 调度和 FP8 块量化重写注意力 kernel，把 H100 利用率从 35% 提到约 75%（FP16 约 740 TFLOPs/s，FP8 近 1.2 PFLOPs/s），比 FA-2 快约 1.5-2×。 https://arxiv.org/abs/2407.08608
- DeepSeek-V2 / Multi-head Latent Attention (MLA) (DeepSeek-AI, 2024-05, report) — 首次提出 MLA：用低秩潜向量联合压缩 K/V（推理仅缓存潜向量、KV cache 减少 93.3%）+ 解耦 RoPE，结合 DeepSeekMoE 做成 236B 总参/21B 激活、128K 上下文、预训练 8.1T token；训练成本降 42.5%、生成吞吐 ×5.76。 https://arxiv.org/abs/2405.04434
- Native Sparse Attention (NSA) (DeepSeek-AI / 北大 / UW, 2025-02, paper) — 「原生可训练」分层稀疏注意力：compression（块压缩全局视野）+ selection（top-n 块细粒度）+ sliding window，门控融合、端到端可微，配硬件对齐 Triton kernel；27B/3B 激活 MoE、260B token，64K 上下文相对 FA-2 大幅加速不掉点。 https://arxiv.org/abs/2502.11089
- DeepSeek-V3.2-Exp / DeepSeek Sparse Attention (DSA) (DeepSeek-AI, 2025-09, report) — 在 V3.1-Terminus 上唯一架构改动是 DSA：lightning indexer（少量 indexer 头算 index score、可 FP8）+ top-k 细粒度 token 选择，仅经 continued training 引入、沿用 V3 权重，大幅压低长上下文注意力成本，是 NSA 思路的生产落地。 https://github.com/deepseek-ai/DeepSeek-V3.2-Exp

---

## 四、稀疏化：Mixture-of-Experts（MoE）

- GShard (Google, 2020-06, paper) — 把稀疏门控 MoE 引入 Transformer 并配自动分片，训练 600B 参数多语言翻译模型（2048 TPU v3、约 4 天）；top-2 gating、expert capacity、辅助负载均衡损失，是现代大规模 MoE 训练基建的奠基作。 https://arxiv.org/abs/2006.16668
- Switch Transformers (Google, 2021-01, paper) — 把路由简化为 top-1（每 token 选 1 专家），稳定训练到 1.6T 参数、固定算力相对 T5 约 7× 提速；用 capacity factor、选择性 fp32 路由、expert dropout 稳定，并可蒸馏回稠密模型。 https://arxiv.org/abs/2101.03961
- GLaM (Google, 2021-12, paper) — 1.2T 总参 MoE（64 专家/层、top-2 激活约 96.6B≈8%），训练能耗约 GPT-3 的 1/3、推理 FLOPs 约一半，零样本/少样本超过 GPT-3；强调高质量数据过滤对 MoE 的重要性。 https://arxiv.org/abs/2112.06905
- ST-MoE (Google, 2022-02, paper) — 系统解决稀疏专家训练不稳定与微调迁移差，提出 router z-loss 抑制 logits 爆炸；训练 ST-MoE-32B（269B 总参/约 32B 激活），SuperGLUE/XSum/ARC 等多任务 SOTA，给出稀疏模型实用配方。 https://arxiv.org/abs/2202.08906
- DeepSeekMoE (DeepSeek-AI, 2024-01, paper) — 提出「细粒度专家切分 + 共享专家隔离」提升专家专业化，2B/16B（16B 仅 2.8B 激活≈LLaMA2-7B 而省约 60% 算力）匹敌更大稠密模型，验证到 145B；是 DeepSeek-V2/V3 MoE 架构原型。 https://arxiv.org/abs/2401.06066
- Mixtral of Experts (Mistral AI, 2024-01, report) — 开源稀疏 MoE 标杆：每层 8 专家 top-2、47B 总参/13B 激活、32K 上下文，激活成本近 13B dense 而质量匹敌/超过 Llama-2 70B 与 GPT-3.5；基于 Mistral 7B（GQA/SwiGLU/RoPE）架构、Apache 2.0。 https://arxiv.org/abs/2401.04088
- Auxiliary-Loss-Free Load Balancing (DeepSeek-AI, 2024-08, paper) — Loss-Free Balancing：用每专家可动态调整的 bias 项做路由均衡，彻底去掉传统辅助损失的干扰梯度，使负载均衡与模型质量解耦；1B/3B MoE 困惑度优于 aux-loss 基线，被 DeepSeek-V3 采用。 https://arxiv.org/abs/2408.15664

---

## 五、SSM / 线性递归 / 混合架构（突破自回归的二次注意力）

- S4 — Structured State Spaces (Stanford Hazy Research, 2021-10, paper) — 结构化状态空间 + HiPPO 初始化高效建模超长依赖，DPLR 参数化用 Cauchy kernel+FFT 近线性计算；刷新 Long Range Arena、首次在 Path-X(16384) 上超随机，是 Mamba 之前 SSM 路线的奠基作。 https://arxiv.org/abs/2111.00396
- RWKV (EleutherAI / RWKV 社区, 2023-05, paper) — 融合 RNN 与 Transformer：训练并行、推理 O(1)/step；用 R/W/K/V 构造线性可递归的 token/channel-mixing，time-decay 提供类位置衰减，验证到 14B，是早期最成功的非注意力大模型之一。 https://arxiv.org/abs/2305.13048
- RetNet — Retentive Network (Microsoft Research / 清华, 2023-07, paper) — 用带复数衰减的 retention 替代 softmax，同时支持 parallel(训练)/recurrent(O(1) 推理)/chunkwise(长序列线性) 三种等价形式，多尺度衰减提供多分辨率记忆，瞄准「不可能三角」。 https://arxiv.org/abs/2307.08621
- Gated Linear Attention (GLA) (MIT / MIT-IBM Watson, 2023-12, paper) — 给线性注意力加数据相关门控提升表达力，并配套 chunkwise、I/O 感知的 FlashLinearAttention（比 FA-2 还快）；衍生的 fla 库成为后续线性注意力/Mamba2/DeltaNet 工作的通用训练后端。 https://arxiv.org/abs/2312.06635
- Mamba (CMU / Princeton, 2023-12, paper) — 给 SSM 加「选择性」（Δ/B/C 随输入变化）+ 硬件感知并行扫描，无注意力无 MLP、线性复杂度；推理吞吐 ×5、序列线性扩展到百万长度，Mamba-3B 匹敌 2× 大的 Transformer。 https://arxiv.org/abs/2312.00752
- MambaByte (Cornell University, 2024-01, paper) — 把 Mamba 直接在原始字节序列（vocab=256、无分词器）上自回归训练，靠固定大小循环状态避开字节变长的内存暴涨；353M/972M/1.6B 在 PG19 上与子词 Transformer 竞争甚至反超。 https://arxiv.org/abs/2401.13660
- Griffin & Hawk (Google DeepMind, 2024-02, paper) — 提出 RG-LRU 门控线性递归单元；Hawk 为纯递归模型超同规模 Mamba，Griffin 交替堆叠 RG-LRU 与局部注意力、用约 1/6 训练 token 匹敌 Llama-2、可外推超训练长度。 https://arxiv.org/abs/2402.19427
- Jamba (AI21 Labs, 2024-03, report) — 首个生产级 Transformer-Mamba 混合 MoE：按 attention:Mamba≈1:7 混合并周期插 MoE，52B 总参/12B 激活、16 专家 top-2，单 80GB GPU 支持 256K 上下文。 https://arxiv.org/abs/2403.19887
- RecurrentGemma (Google DeepMind, 2024-04, report) — 把 Griffin 架构（RG-LRU 门控线性递归 + 局部注意力）产品化为开放模型 2B/9B，固定大小递归状态、长序列推理省内存高吞吐，与同规模 Gemma 相当但训练 token 更少。 https://arxiv.org/abs/2404.07839
- Mamba-2 (Princeton / CMU, 2024-05, paper) — 提出 State Space Duality (SSD)：证明 SSM 与注意力是结构化半可分矩阵的两种分解，可用 block 分解（对角块走二次、块间走线性）；SSD 层比 Mamba-1 快 2-8×、支持更大 state size，统一线性注意力/Mamba/softmax 视角。 https://arxiv.org/abs/2405.21060
- Samba (Microsoft / UIUC, 2024-06, paper) — 逐层交错 Mamba + 滑动窗口注意力(w=2048) + SwiGLU MLP，构成线性时间、可无限上下文外推的混合架构；3.8B 在短上下文反超 Phi-3-mini，并能从 4K 训练长度零样本外推到 1M。 https://arxiv.org/abs/2406.07522
- Jamba-1.5 (AI21 Labs, 2024-08, report) — 把 Transformer-Mamba 混合 MoE 扩到 Large 398B 总参/94B 激活、Mini 52B/12B，256K 有效上下文；提出 ExpertsInt8 量化（专家存 INT8、计算反量化 BF16，无质量损失），Large 可在 8×80GB 上服务 256K。 https://arxiv.org/abs/2408.12570
- Hymba (NVIDIA, 2024-11, paper) — 同一层内并行放注意力头（高分辨率回忆）与 Mamba SSM 头（高效上下文摘要）后融合，加可学习 meta token + cross-layer KV sharing + 滑窗注意力；Hymba-1.5B 为 sub-2B 公开 SOTA，相比 Llama-3.2-3B cache 约 1/11、吞吐约 3.5×。 https://arxiv.org/abs/2411.13676
- Gated Delta Networks (NVIDIA / MIT CSAIL, 2024-12, paper) — 把门控（自适应记忆擦除 α_t）与 delta 更新规则（定向纠正记忆 β_t）结合，chunkwise 并行训练，语言建模/检索/长度外推超 Mamba2 与 DeltaNet；被 Qwen3-Next 等混合线性架构采用。 https://arxiv.org/abs/2412.06464
- MiniMax-01 — Lightning Attention (MiniMax, 2025-01, report) — 把 lightning attention（chunkwise 线性注意力）与 MoE 大规模结合，每 7 层线性注意力配 1 层 softmax 注意力，456B 总参/45.9B 激活、32 专家；训练 1M 上下文、推理外推 4M，是首个把线性注意力 scale 到数百亿激活的旗舰。 https://arxiv.org/abs/2501.08313
- Falcon-H1 (TII Falcon LLM Team, 2025-07, report) — 并行混合架构模型族：同一层并行运行注意力头与 SSM(Mamba) 头，覆盖 0.5B–34B、30+ checkpoint，平衡效率与性能。 https://arxiv.org/abs/2507.22448
- Qwen3-Next-80B-A3B (Qwen Team, Alibaba, 2025-09, blog) — Gated DeltaNet + Gated Attention 3:1 混合 + 极致稀疏 MoE（80B 总参仅激活约 3B、512 专家/10 路由/1 共享）+ 原生 MTP；注意力输出门控、Zero-Centered RMSNorm 稳定训练，成本不到 Qwen3-32B 的 1/10、长上下文吞吐 10 倍以上。 https://qwen.ai/blog?id=4074cca80393150c248e508aa62983f9cb7d27cd&from=research.latest-advancements-list

---

## 六、旗舰稠密 / MoE 基座模型（确立或集成现代架构配方）

- PaLM (Google Research, 2022-04, report) — 540B dense Transformer，用 Pathways 跨 6144 块 TPU v4 训练，确立了 SwiGLU、并行注意力/FFN、MQA、RoPE 等一整套现代 dense 架构组件。 https://arxiv.org/abs/2204.02311
- Gemma 2 (Google DeepMind, 2024-06, report) — 2B/9B/27B 引入交错局部-全局注意力、GQA、logit soft-capping，并用知识蒸馏训练 2B/9B，性能匹敌 2-3 倍大的模型。 https://arxiv.org/abs/2408.00118
- Llama 3 Herd (Meta AI, 2024-07, report) — dense Transformer 模型族，旗舰 405B/128K 上下文、15T+ token 预训练，详尽公开数据/infra/并行/后训练配方，是最透明的前沿级开源报告之一。 https://arxiv.org/abs/2407.21783
- DeepSeek-V3 (DeepSeek-AI, 2024-12, report) — 671B 总参/37B 激活开源 MoE 旗舰，集 MLA + DeepSeekMoE + 无辅助损失负载均衡 + MTP，并以 FP8 训练在仅 2.788M H800 卡时内完成 14.8T token 预训练。 https://arxiv.org/abs/2412.19437
- DeepSeek-R1 (DeepSeek-AI, 2025-01, report) — 证明纯强化学习（无需人工标注推理轨迹）即可激发 LLM 复杂推理能力，并把能力蒸馏进小模型，是 RLVR / 推理模型范式的里程碑。 https://arxiv.org/abs/2501.12948
- OLMo 2 (Allen Institute for AI / UW, 2025-01, report) — 完全开放（权重+数据+代码+日志）dense 模型族 7B/13B/32B，引入 reordered norm + QK-norm 稳定训练、两阶段预训练，并用 RLVR 对齐。 https://arxiv.org/abs/2501.00656
- Gemma 3 (Google DeepMind, 2025-03, report) — 1B–27B 加多模态、128K 上下文，提高局部注意力比例（5:1 local:global）压 KV cache，蒸馏训练，4B-IT 即可匹敌 Gemma2-27B-IT。 https://arxiv.org/abs/2503.19786
- Llama 4 Herd (Meta AI, 2025-04, blog) — Meta 首个原生多模态 MoE 模型族：Scout（17B 激活/16 专家/10M 上下文）、Maverick（17B 激活/128 专家）、Behemoth（288B 激活 教师模型），采用早融合 + iRoPE。 https://ai.meta.com/blog/llama-4-multimodal-intelligence/
- Qwen3 (Qwen Team, Alibaba, 2025-05, report) — dense + MoE 全谱（0.6B–235B），首创 thinking/non-thinking 统一模型 + thinking budget，用旗舰蒸馏高效造小模型，119 语言、Apache 2.0。 https://arxiv.org/abs/2505.09388
- Kimi K2 (Moonshot AI, 2025-07, report) — 1T 总参/32B 激活 MoE，提出 MuonClip 优化器（Muon + QK-clip）实现 15.5T token 零 loss spike 预训练，强在 agentic 与 coding。 https://arxiv.org/abs/2507.20534
- gpt-oss-120b & 20b (OpenAI, 2025-08, model-card) — OpenAI 时隔多年的开放权重模型（Apache 2.0），罕见公开架构：MoE + 交替带状窗口/全密注意力 + attention sink + RoPE + YaRN，MoE 权重原生 MXFP4 量化，使 120B 装进单张 80GB GPU。 https://openai.com/index/gpt-oss-model-card/
- DeepSeek-V3.2 (DeepSeek-AI, 2025-12, paper) — 2025-12 正式版，结合 DeepSeek Sparse Attention、可扩展 RL 框架与大规模 agentic 任务合成，高算力变体 V3.2-Speciale 在 2025 IMO/IOI 拿金牌、对标 GPT-5/Gemini-3.0-Pro。 https://arxiv.org/abs/2512.02556

---

## 七、多模态架构（视觉骨干 / 桥接 / 早融合 / 全模态）

- ViT (Google Research Brain, 2020-10, paper) — 把图像切成 16×16 patch 序列直接喂标准 Transformer，证明纯 Transformer 在大规模预训练下可超越 CNN，是多模态视觉编码器的架构基石。 https://arxiv.org/abs/2010.11929
- CLIP (OpenAI, 2021-02, paper) — 用 4 亿图文对做对比学习，训练可零样本迁移的视觉-文本双塔编码器，是几乎所有现代多模态 LLM 视觉编码器的祖先。 https://arxiv.org/abs/2103.00020
- Perceiver (DeepMind, 2021-03, paper) — 用固定数量 latent 通过迭代交叉注意力从超长输入提取信息，把注意力复杂度与输入规模解耦，可统一处理图像/音频/点云等任意模态。 https://arxiv.org/abs/2103.03206
- Flamingo (DeepMind, 2022-04, paper) — Perceiver Resampler + 门控交叉注意力把冻结视觉编码器接到冻结 LLM，实现交错图文输入的少样本多模态学习，是「冻结 LLM + 视觉桥接」范式代表。 https://arxiv.org/abs/2204.14198
- BLIP-2 (Salesforce Research, 2023-01, paper) — 用轻量 Querying Transformer (Q-Former) 桥接冻结图像编码器和冻结 LLM，两阶段预训练，以远少的可训练参数达 VL 任务 SOTA。 https://arxiv.org/abs/2301.12597
- LLaVA — Visual Instruction Tuning (UW-Madison/Microsoft/Columbia, 2023-04, paper) — 用简单线性/MLP 投影把 CLIP 视觉特征接到 LLM，并首创用纯文本 GPT-4 生成多模态指令数据做视觉指令微调，是最具影响力的开源 VLM 范式。 https://arxiv.org/abs/2304.08485
- Qwen-VL (Qwen Team, Alibaba, 2023-08, paper) — Qwen 首个 VLM：Qwen-7B + OpenCLIP ViT-bigG + 位置感知单层 cross-attention 适配器（压到 256 视觉 token），3 阶段训练赋予看图/grounding/OCR，是 Qwen2-VL/2.5-VL 起点。 https://arxiv.org/abs/2308.12966
- Chameleon (FAIR at Meta, 2024-05, paper) — 早融合、token 化的混合模态基础模型：图像也量化成离散 token 与文本 token 放进同一 Transformer，单模型原生理解并生成任意交错图文。 https://arxiv.org/abs/2405.09818
- Qwen2-VL (Qwen Team, Alibaba, 2024-09, report) — 引入 Naive Dynamic Resolution（任意分辨率→动态数量视觉 token）和 Multimodal RoPE (M-RoPE)，统一处理图像与视频，是中文阵营领先开源 VLM。 https://arxiv.org/abs/2409.12191
- Pixtral 12B (Mistral AI, 2024-10, report) — Mistral 多模态模型，配从零训练的原生分辨率/宽高比视觉编码器，128K 上下文可处理任意数量图像，且不牺牲纯文本能力。 https://arxiv.org/abs/2410.07073
- Byte Latent Transformer (BLT) (FAIR at Meta / UW / UChicago, 2024-12, paper) — 无 tokenizer 字节级 LLM：用「下一字节熵」动态切分成可变长 patch 作计算单元，首次在规模上匹配 token-based LLM 并提升推理效率与鲁棒性。 https://arxiv.org/abs/2412.09871
- DeepSeek-VL2 (DeepSeek-AI, 2024-12, report) — 把 MoE + MLA 的语言侧与「动态拼图」高分辨率视觉编码结合，做成稀疏激活的视觉语言 MoE，高效处理任意宽高比高分辨率图像。 https://arxiv.org/abs/2412.10302
- Qwen2.5-VL (Qwen Team, Alibaba, 2025-03, report) — Qwen 视觉语言旗舰，强化精确目标定位、文档/表格结构化解析、小时级长视频理解，引入绝对时间编码与原生分辨率窗口注意力 ViT。 https://arxiv.org/abs/2502.13923
- Qwen2.5-Omni (Qwen Team, Alibaba, 2025-03, report) — 端到端原生全模态：单模型感知文本/图像/音频/视频并流式同时生成文本与语音，核心是 Thinker-Talker 双脑架构 + TMRoPE（时间对齐多模态 RoPE），代表 native omni-modal 路线。 https://arxiv.org/abs/2503.20215

## 增量补录（2026 调研后查漏，架构维度）
- **GLM-5.2** — glm_moe_dsa：MLA+Muon Split、256 专家/8、78 层、**IndexShare**（每4稀疏层共享 indexer，1M FLOPs −2.9×）、改进 MTP。[详](../2026/glm-5.2.md)
- **Kimi-K2.6** — 1T/32B MoE、MLA、384 专家/8+1 共享、61 层、MoonViT 400M、native INT4。[详](../2026/kimi-k2.6.md)
- **MiniMax-M3** — ~428B/23B、**MSA 双分支稀疏注意力**(Index+Main, KL训indexer)、1M。[详](../2026/minimax-m3.md)
- **Qwen-AgentWorld** — 混合 Gated DeltaNet+Gated Attention(3:1)、256 专家/8、MTP。[详](../2026/qwen-agentworld.md)
- **MiniCPM5-1B** — 回归标准 LlamaForCausalLM(1536/24层/GQA 16·2/128K)。[详](../2026/minicpm5-1b.md)
- **Mistral-Small-4** — mistral4 MoE 128/4 active、119B/6.5B、256K、多模态输入。[详](../2026/mistral-small-4.md)
- **Intern-S2-Preview** — qwen3_5_moe_text、256 专家/8、FP8。[详](../2026/intern-s2-preview.md)
