# AI infra

大模型的 AI 基础设施在 2020→2026 间经历了从"让单个超大模型跑起来"到"全栈协同压榨每一分算力"的演进。2020 年前后的主线是**分布式训练并行**（数据/张量/流水/专家/序列并行）与显存优化（ZeRO、激活重计算），让千亿级模型首次可训；2022 年起 **FlashAttention 与量化**把单卡算力利用率推向极限，催生了 vLLM/SGLang 等**推理服务系统**与 PagedAttention、PD 分离、KVCache 中心架构等运行时范式；2023-2024 年随推理模型崛起，**RL/对齐后训练框架**（TRL、OpenRLHF、verl、AReaL）成为新主战场；到 2025-2026 年，DeepSeek 用 FP8 训练 + DualPipe + 开源周一整套工具，把"算法-系统-硬件协同设计"做成了行业标杆，国产 infra 在大规模 MoE 训练/推理上走到台前。以下按子主题分组，组内按时间排序。

## 分布式训练并行与显存优化

- ZeRO (Microsoft DeepSpeed, 2019-10, paper) — 把优化器状态/梯度/参数在数据并行各 rank 间分片以消除显存冗余的奠基算法；三阶段（Pos 4x、Pos+g 8x、Pos+g+p ∝ DP 度），64 DGX-2（1024 V100）训练 100B 模型达 38 TFLOPs/GPU，吞吐超线性扩展。https://arxiv.org/abs/1910.02054
- Megatron-LM (NVIDIA, 2019-09, paper) — 张量并行（intra-layer model parallelism）经典工作，仅在原生 PyTorch 插少量 all-reduce；MLP 按列/行切、注意力按 head 切，512 V100 上 8-way 模型并行训 8.3B GPT-2 达 15.1 PFLOPs（76% 扩展效率）。https://arxiv.org/abs/1909.08053
- GPipe (Google, 2018-11, paper) — 首个通用流水线并行库，micro-batch 切分 + 激活重计算，bubble 比例约 (K-1)/(m+K-1)；训练 557M AmoebaNet 与 6B 多语言 Transformer（128 TPU v3）。https://arxiv.org/abs/1811.06965
- PipeDream-2BW (Microsoft Research / Stanford / CMU, 2020-06, paper) — 内存高效流水线，仅维护 2 份权重版本（double-buffered weights）即保梯度一致，确立 1F1B 稳态调度（后成 Megatron/DeepSpeed 默认），并提供自动 stage 划分 planner。https://arxiv.org/abs/2006.09503
- PyTorch DDP (Meta, 2020-06, paper) — DistributedDataParallel 设计经验，gradient bucketing + 反向中梯度就绪即异步 all-reduce 实现通信计算重叠；256 GPU 近线性，是 FSDP/ZeRO 的基线。https://arxiv.org/abs/2006.15704
- GSPMD (Google, 2021-05, paper) — 基于 XLA 的自动并行编译器，用户对张量维标注 sharding，编译器自动补全整图分片并插通信；统一 data/within-op/pipeline 嵌套，50B-1T 模型在 2048 TPU v3 上 54%-62% FLOPs 利用，是 GShard 思想的通用化。https://arxiv.org/abs/2105.04663
- 3D 并行 PTD-P / Megatron on GPU Clusters (NVIDIA / Stanford / Microsoft, 2021-04, paper) — 把张量+流水+数据并行组合（TP≤8 单节点 NVLink、PP 跨节点、DP 最外层）并提出 interleaved 1F1B 把 bubble 降到 (p-1)/(v·m)；3072 A100 训 1T 模型达 502 PFLOPs（约 52% MFU）。https://arxiv.org/abs/2104.04473
- ZeRO-Infinity (Microsoft DeepSpeed, 2021-04, paper) — ZeRO 的异构内存卸载扩展（GPU HBM ← CPU DRAM ← NVMe SSD）+ memory-centric tiling + 带宽中心通信重叠；512 V100 可训 32T 参数模型，20T 模型达 49 TFLOPs/GPU，单节点可微调 1T 模型。https://arxiv.org/abs/2104.07857
- Alpa (UC Berkeley / Google, 2022-01, paper) — 自动并行编译器，把并行分为 intra-operator（ILP 求每算子最优 sharding）与 inter-operator（DP 切 pipeline stage 与 device mesh），自动生成跨网格执行计划；在 GPT/MoE/异构模型上匹配或超过人工调优的 Megatron/DeepSpeed。https://arxiv.org/abs/2201.12023
- Pathways (Google, 2022-03, paper) — 下一代 ML 系统运行时，single-controller + 异步 gang-scheduling 调度数千 TPU，分片 dataflow + 并行异步派发隐藏跨 pod 延迟，2048 TPU 接近满利用；是训练 PaLM 540B 的底层系统。https://arxiv.org/abs/2203.12533
- Reducing Activation Recomputation (NVIDIA, 2022-05, paper) — 提出序列并行（沿序列维切 LayerNorm/dropout/残差）+ 选择性激活重计算（只重算注意力中 memory-heavy 部分），激活显存约降 5×、重计算算力开销从约 36% 降至约 2%；已合入 Megatron-LM。https://arxiv.org/abs/2205.05198
- Megatron-Core (NVIDIA, 2023-08, github) — 把 Megatron-LM 沉淀为可组合核心库，提供五维并行（TP/PP/DP/EP/CP）+ 混合精度（FP16/BF16/FP8/FP4）+ 分布式 checkpoint，被 NeMo、各厂训练栈集成，附 Megatron Bridge 做 HF 互转。https://github.com/NVIDIA/Megatron-LM
- nanotron (Hugging Face, 2023-09, github) — 极简 3D 并行预训练库，用易读代码实现 TP/PP/DP（含 ZeRO-1）+ 序列并行 + FP8 + 专家并行；是 SmolLM、FineWeb 消融、Ultrascale Playbook 的训练代码基础。https://github.com/huggingface/nanotron
- MegaScale (ByteDance / Peking University, 2024-02, paper) — 生产级万卡训练系统，全栈协同（算法+系统+网络+可观测性），175B 模型在 12288 GPU 上达 55.2% MFU（1.34× over Megatron-LM），核心贡献是大规模才暴露的稳定性问题诊断、容错与 straggler 抑制。https://arxiv.org/abs/2402.15627
- TorchTitan (Meta / PyTorch, 2024-10, paper) — PyTorch 原生预训练框架，基于 DTensor 整合 4D 并行（FSDP2 × TP × PP × CP）+ torch.compile + Float8；Llama3.1 上相对优化基线提速 8B/128GPU +65.08%、70B/256 +12.59%、405B/512 +30%，对标 Megatron-LM。https://arxiv.org/abs/2410.06511
- Streaming DiLoCo (Google DeepMind, 2025-01, paper) — 低通信分布式训练，DiLoCo（inner 多步 AdamW + outer 周期全局动量同步）基础上加 streaming 部分同步 + 通信计算重叠 + outer 梯度量化（探至极低精度），通信量降两个数量级而质量基本不降，利于跨数据中心训练。https://arxiv.org/abs/2501.18512

## MoE 训练与专家并行系统

- GShard (Google, 2020-06, paper) — 首个把 MoE 条件计算与自动分片结合的系统性工作，轻量 sharding API + XLA SPMD partitioner，训练 600B 稀疏门控翻译模型（2048 TPU v3、4 天）；提出 top-2 路由、expert capacity、辅助负载均衡损失、随机路由，奠定 MoE 工程范式。https://arxiv.org/abs/2006.16668
- FastMoE (Tsinghua University, 2021-03, paper) — 首个开源 PyTorch MoE 训练系统，把专家分布到多 GPU/多节点（expert parallelism）+ 优化 all-to-all kernel + 灵活 gate 接口；摆脱 Google 专有 TPU 栈，是中文社区（GLM/悟道）早期 MoE 的基础设施。https://arxiv.org/abs/2103.13262
- DeepSpeed-MoE (Microsoft DeepSpeed, 2022-01, paper) — 端到端 MoE 训练+推理方案，提出 PR-MoE（金字塔-残差）架构 + MoS 蒸馏把模型缩小最高 3.7×，自回归 LM 上 MoE 较同质量 dense 省约 5× 训练成本，推理较现有 MoE 方案快 7.3×、较同质量 dense 快 4.5×/便宜 9×。https://arxiv.org/abs/2201.05596
- ST-MoE (Google, 2022-02, paper) — 系统研究 MoE 训练稳定性与微调可迁移性，提出 router z-loss（惩罚 gating logits 的 log-sum-exp，成后续 MoE 标配）；训练 ST-MoE-32B（269B 总参）在 SuperGLUE 等多任务达 SOTA。https://arxiv.org/abs/2202.08906
- Tutel (Microsoft, 2022-06, paper) — 为 MoE 设计运行时自适应并行/流水的系统，用"同一种布局"让所有并行方式零成本切换以适配动态 token 路由负载；单 MoE 层在 16 卡/2048 卡 A100 上较此前 SOTA 快 4.96×/5.75×，SwinV2-MoE 端到端较 Fairseq 快 1.55×/2.11×。https://arxiv.org/abs/2206.03382
- MegaBlocks (Stanford / Microsoft / Google, 2022-11, paper) — 把 MoE 重构为块稀疏（block-sparse）矩阵乘 + 定制 GEMM kernel，dropless-MoE 无 token 丢弃/padding；较 Tutel 端到端训练快最高 40%、较 Megatron dense 约 2.4×，被 Databricks DBRX 用于生产。https://arxiv.org/abs/2211.15841
- DeepEP (DeepSeek-AI, 2025-02, github) — 开源 MoE 专家并行通信库，高吞吐低延迟 all-to-all dispatch/combine kernel（含 FP8、极低 SM 占用）；SM100 NVLink EP8 达 726/740 GB/s（dispatch/combine），V2 较 V1 最高 1.3× 峰值且省 4× SM、支持 EP2048。https://github.com/deepseek-ai/DeepEP
- MegaScale-Infer (ByteDance / Peking University, 2025-04, paper) — 大规模 MoE 推理系统，把每层 attention 与 FFN（专家）模块解耦独立部署，用 ping-pong pipeline parallelism 把 micro-batch 在两类模块间往返流转以隐藏通信 + 定制 M2N 通信库，降低 MoE serving 每 token 成本。https://arxiv.org/abs/2504.02263

## 注意力 kernel 与长上下文 / 序列并行

- FlashAttention (Stanford / Dao-AILab, 2022-05, paper) — IO 感知精确注意力，tiling + online softmax + kernel fusion 避免把 N×N 矩阵写回 HBM，HBM 访问从 O(N²) 降到 O(N²/M)，反向用重计算；GPT-2 训练约 3× 加速，成现代 LLM 事实标准 kernel。https://arxiv.org/abs/2205.14135
- FlashAttention-2 (Princeton / Stanford / Dao-AILab, 2023-07, paper) — 工程重写，减少 non-matmul FLOP + 沿序列维并行 + 优化 warp 划分；A100 上达 50-73% 理论峰值 FLOPs（约 2× over FA-1），GPT 训练 225 TFLOPs/GPU（72% MFU）。https://arxiv.org/abs/2307.08691
- SARATHI (Microsoft Research India / Georgia Tech, 2023-08, paper) — 提出 chunked-prefill + decode-maximal piggybacking，把长 prefill 切成固定预算块并搭载 decode token 配平每步算力，消除 PP 气泡与 prefill/decode 干扰；演进为 Sarathi-Serve，成主流引擎默认 continuous batching 之一。https://arxiv.org/abs/2308.16369
- DeepSpeed Ulysses (Microsoft DeepSpeed, 2023-09, paper) — 序列并行方案，用两次 all-to-all 在序列维与 head 维间转置，通信量 O(N) 而非 O(N²)；支持 4× 更长序列、约 2.5× 吞吐，可达百万 token 上下文，与 Ring Attention 并为序列并行两条主流路线。https://arxiv.org/abs/2309.14509
- Ring Attention (UC Berkeley, 2023-10, paper) — 把长序列沿设备成环切分，每卡持一段 KV 以环形通信轮转传递并与计算重叠，单卡仅存 1/N 激活、最大上下文 ∝ 设备数，精确无近似；是 Megatron/torchtitan 中 context parallelism 的算法基础。https://arxiv.org/abs/2310.01889
- Flash-Decoding (Dao-AILab / Meta, 2023-10, blog) — 为解码阶段（query 长度=1、batch 小）重写注意力，新增沿 KV 序列长度的并行维 + 跨块 log-sum-exp 归约；CodeLlama-34B 上 512~64k 解码吞吐最高 8×（注意力本身最高快 50×），已并入 FlashAttention≥2.2 与 xFormers。https://pytorch.org/blog/flash-decoding/
- DISTFLASHATTN (UC Berkeley / UCSD / CMU / MBZUAI, 2023-10, paper) — 分布式长上下文训练注意力，token-level 负载均衡（解因果掩码三角负载不均）+ KV 通信重叠 + 重计算感知 checkpoint；32K-512K 序列下较 Ring Self-Attention 提速 4.45-5.64×、较 Megatron+FA 1.24-2.01×。https://arxiv.org/abs/2310.03294
- FlashAttention-3 (Colfax / Meta / NVIDIA / Together / Princeton / Dao-AILab, 2024-07, paper) — 针对 Hopper 重写，warp-specialization 异步让 WGMMA+TMA 与 softmax 重叠 + incoherent processing 保 FP8 精度；H100 FP16 达 740 TFLOPs（75% 峰值，1.5-2× over FA-2），FP8 接近 1.2 PFLOPs、误差较基线低 2.6×。https://arxiv.org/abs/2407.08608
- Native Sparse Attention (DeepSeek-AI / Peking University / UW, 2025-02, paper) — 硬件对齐且可端到端训练的稀疏注意力，三分支（块级压缩 + 动态 top-n token 选择 + 滑动窗口）门控融合，blockwise 选择保证 Tensor Core 友好算术强度 + 定制 Triton kernel；长上下文下较 Full Attention 大幅加速且质量不降。https://arxiv.org/abs/2502.11089

## 量化（训练与推理）

- LLM.int8() (University of Washington / Meta / Hugging Face, 2022-08, paper) — 首个无精度损失的 LLM 8-bit 推理量化，vector-wise INT8 处理常规通道 + 对约 0.1% emergent outlier 维度保留 FP16（6.7B 起出现离群）；175B 模型可单节点 8-bit 推理、无 zero-shot 下降，集成 bitsandbytes + HF。https://arxiv.org/abs/2208.07339
- GPTQ (IST Austria / ETH Zurich / Neural Magic, 2022-10, paper) — 基于近似 Hessian 二阶信息的 one-shot weight-only 量化，逐列贪心 + Cholesky 重排做误差补偿；175B 模型约 4 GPU·hr 量化到 3-4 bit 几乎不掉点，单卡 A100 可推理 175B（INT3 约 3.25× 加速），是开源 4-bit 生态源头。https://arxiv.org/abs/2210.17323
- SmoothQuant (MIT Han Lab / NVIDIA, 2022-11, paper) — W8A8 全 INT8 的 PTQ，用逐通道平滑因子把激活量化难度迁移到权重（X·diag(1/s)、W·diag(s) 数学等价），免训练；OPT/BLOOM/GLM 等 100B+ 模型几乎无损、最高 1.56× 加速、显存减半，被 TensorRT-LLM 集成。https://arxiv.org/abs/2211.10438
- AWQ (MIT Han Lab / SJTU, 2023-06, paper) — 激活感知权重量化，依激活分布找约 1% 显著权重通道并 per-channel 缩放保护，纯权重 INT4（group-wise）、不需反传/重构集、泛化到指令微调与多模态；4-bit 优于 GPTQ，配 TinyChat 引擎桌面/移动端 3-4× over FP16。https://arxiv.org/abs/2306.00978
- QServe (MIT Han Lab / NVIDIA, 2024-05, paper) — W4A8KV4 量化 + 系统协同的推理引擎，QoQ 算法（渐进式分组量化 + SmoothAttention + register-level 反量化降 CUDA core 开销）；A100/L40S 上较 TensorRT-LLM 吞吐最高约 2.4-3.5×，可用更便宜的 L40S 替代 A100。https://arxiv.org/abs/2405.04532

## 推理服务系统与运行时

- Efficiently Scaling Transformer Inference (Google, 2022-11, paper) — 给出 500B+ 模型在 TPU v4 上的 partitioning 分析框架，按延迟与芯片数约束选 1D/2D 张量切分，结合 multiquery attention 缩小 KV cache 支撑 32K 上下文；PaLM 540B 在 64 TPU v4 上首 token 约 29ms、吞吐优先约 76% MFU。https://arxiv.org/abs/2211.05102
- TensorRT-LLM (NVIDIA, 2023-08, github) — 官方 LLM 推理优化库，Python API 定义模型并编译为 TensorRT 引擎，集成 FP8/FP4/INT8/INT4 量化（SmoothQuant/AWQ/GPTQ）+ in-flight batching + paged KV cache + TP/PP/EP + speculative decoding + PD 分离；众多 MLPerf Inference 记录的基础。https://github.com/NVIDIA/TensorRT-LLM
- PagedAttention / vLLM (UC Berkeley / Stanford / UCSD, 2023-09, paper) — 把 KV cache 像 OS 虚拟内存分页管理（固定 block 非连续 + block table 映射），显存浪费 <4% 并支持 copy-on-write 前缀/beam 共享；吞吐 2-4× over HF/FasterTransformer，vLLM 现为社区事实标准推理引擎。https://arxiv.org/abs/2309.06180
- SGLang / RadixAttention (Stanford / UC Berkeley, 2023-12, paper) — 面向结构化 LLM 程序的前端 DSL + 后端运行时，RadixAttention 用基数树跨请求自动复用 KV cache 前缀 + 压缩 FSM 约束解码 + API 推测执行；吞吐最高 6.4×（vs vLLM/Guidance），被 DeepSeek、xAI 大规模 serving 采用。https://arxiv.org/abs/2312.07104
- DeepSpeed-FastGen (Microsoft DeepSpeed, 2024-01, paper) — 高吞吐推理系统，Dynamic SplitFuse 把长 prompt 动态切片并与生成 token 组合成均匀 batch 配平算力；较 vLLM 吞吐最高约 2.3×、更低平均/尾延迟（P95/P99），支持 TP 与多副本。https://arxiv.org/abs/2401.08671
- DistServe (Peking University / UCSD, 2024-01, paper) — 提出 prefill/decode 阶段拆到不同 GPU 池（PD 分离），分别针对 TTFT 与 TPOT 优化并按 SLO 独立配比资源 + 带宽感知放置；满足 SLO 下可服务 7.4× 请求或承受 12.6× 更紧 SLO，PD 分离自此成高端推理标配。https://arxiv.org/abs/2401.09670
- Mooncake (Moonshot AI / Tsinghua University, 2024-06, paper) — Kimi 生产服务平台，KVCache 中心的 PD 分离 + 聚合集群闲置 CPU/DRAM/SSD 构建分布式 KV 缓存池 + SLO 感知调度 + 过载预测早拒；模拟最高 +525% 吞吐、真实负载 Kimi 多处理 75% 请求，Transfer Engine 已被 vLLM/SGLang 集成。https://arxiv.org/abs/2407.00079

## FP8 / GEMM kernel 与硬件协同

- Transformer Engine (NVIDIA, 2022-09, github) — FP8/FP4 训练与推理加速库，把 Hopper 的 FP8（E4M3/E5M2）落地，用 per-tensor 缩放 + delayed/current scaling 自动管理动态范围保收敛；被 Megatron-LM、NeMo、DeepSpeed、torchtitan 集成，FP8 收敛与 BF16 对齐。https://github.com/NVIDIA/TransformerEngine
- DeepGEMM (DeepSeek-AI, 2025-02, github) — 开源 FP8/FP4/BF16 高性能 tensor core GEMM 库，含细粒度缩放、fused MoE（Mega MoE）、MQA scoring，全 JIT 编译、代码简洁；H800 上 FP8 GEMM 最高 1550 TFLOPS，是 DeepSeek-V3 FP8 训练/推理的矩阵乘底座。https://github.com/deepseek-ai/DeepGEMM
- FlashMLA (DeepSeek-AI, 2025-02, github) — 开源周首日发布的 MLA 高性能注意力 kernel，针对 Hopper 优化变长序列/分页 KV cache 解码（H800 达 3000 GB/s 与 660 TFLOPS），后加 token 级稀疏 MLA（DSA，H800 410 TFLOPS）与 SM100 支持，支撑 DeepSeek-V3/R1 推理。https://github.com/deepseek-ai/FlashMLA
- DualPipe (DeepSeek-AI, 2025-02, github) — DeepSeek-V3 提出并开源的双向流水线并行，从两端同时注入 micro-batch 使前/反向计算-通信完全重叠、几乎隐藏跨节点 all-to-all 并减 bubble（代价 2× 参数副本）；含 Sea AI Lab 的 DualPipeV（设备数减半）。https://github.com/deepseek-ai/DualPipe
- 3FS / Fire-Flyer File System (DeepSeek-AI, 2025-02, github) — 面向 AI 训练/推理的高性能分布式文件系统，基于 NVMe SSD + RDMA，解耦架构 + CRAQ 强一致 + stateless metadata；180 节点读吞吐约 6.6 TiB/s，KVCache 二级缓存峰值 40 GiB/s，统一数据准备/dataloader/checkpoint/KVCache 存储层。https://github.com/deepseek-ai/3FS
- DeepSeek Open Infra Index (DeepSeek-AI, 2025-02, github) — 2025 开源周（连续 5 天放出 FlashMLA / DeepEP / DeepGEMM / DualPipe+EPLB / 3FS+smallpond）的总索引，附 V3/R1 推理系统披露：prefill EP32+TP+DP、decode EP144 大规模专家并行、PD 分离、双 micro-batch 通信重叠。https://github.com/deepseek-ai/open-infra-index
- DeepSeek-V3 Hardware Insights (DeepSeek-AI, 2025-05, paper) — 从 V3（2048 H800）训练实践反思 LLM 与硬件协同设计，系统披露 MLA 提升内存效率、MoE 平衡算力-通信、FP8 混合精度训练要点、Multi-Plane Fat-Tree 网络拓扑降互联成本，并对下一代硬件（低精度、scale-up/out 融合、网络）给建议。https://arxiv.org/abs/2505.09343

## RL / 对齐后训练框架

- TRL (Hugging Face, 2020-03, github) — 官方后训练库，封装 SFT、DPO（及 KTO/IPO/ORPO/CPO）、PPO、GRPO、Reward Modeling 等 trainer，深度集成 Transformers/Accelerate（DeepSpeed ZeRO/FSDP）/PEFT（LoRA/QLoRA）/vLLM 在线生成加速；社区对齐与 RLVR 复现主流入口。https://github.com/huggingface/trl
- OpenRLHF (OpenRLHF community, 2024-05, paper) — 首批可扩展到 70B+ 的 RLHF 框架，Ray 编排 + vLLM 生成 + DeepSpeed ZeRO-3 训练，把 actor/critic/reward/ref 四模型分组调度与卸载；支持 PPO/DPO/KTO/拒绝采样，后演进至 agentic RL（async、REINFORCE++、DAPO、VLM）。https://arxiv.org/abs/2405.11143
- NeMo-Aligner (NVIDIA, 2024-05, paper) — 基于 NeMo 的可扩展对齐工具包，支持 SFT/RM/PPO-RLHF/DPO/SteerLM/SPIN，用 TP/PP/DP 跨数千 GPU、RLHF 生成用 TensorRT-LLM 加速 rollout；产出 Nemotron-4-340B Instruct/Reward、Llama-3.1-Nemotron-70B，后继 NeMo-RL（Ray + Megatron Core）。https://arxiv.org/abs/2405.01481
- HybridFlow / verl (ByteDance / Hong Kong University, 2024-09, paper) — RLHF 框架，single-controller（算法编排）+ multi-controller（分布式执行）混合范式 + 3D-HybridEngine 在训练/生成间零冗余 resharding；较 SOTA 吞吐 1.5-20×，开源为 verl，是当前大规模 RL post-training 最主流框架之一。https://arxiv.org/abs/2409.19256
- DeepSeek-R1 (DeepSeek-AI, 2025-01, report) — 用纯 RL（GRPO + 规则化可验证奖励 RLVR）在 V3-Base 上激发推理的旗舰报告，R1-Zero 完全无 SFT 即涌现长 CoT/自我验证/反思，R1 加冷启动 + 四阶段 RL 对标 o1-1217，并蒸馏到 Qwen/Llama 1.5B-70B dense、全开源。https://arxiv.org/abs/2501.12948
- DAPO (ByteDance Seed / Tsinghua University, 2025-03, paper) — 完全开源的大规模推理 RL 系统与算法（Clip-Higher + Dynamic Sampling + Token-Level PG Loss + Overlong Reward Shaping），基于 verl；Qwen2.5-32B base 在 AIME 2024 达 50 分（vs R1-Zero-Qwen-32B 47）且约半数步数，开源代码+数据。https://arxiv.org/abs/2503.14476
- AReaL (Ant Group / Tsinghua University, 2025-05, paper) — 全异步 RL 训练系统，rollout 与 training 完全解耦（rollout 持续生成、training 攒满即更新），消除"等最长序列"空转，用 interruptible rollout + staleness 控制 + staleness-enhanced PPO 保稳；GPU 利用与端到端速度显著高于同步系统。https://arxiv.org/abs/2505.24298

## 架构-Infra 协同设计的代表性模型报告

- Mixtral of Experts (Mistral AI, 2024-01, report) — 稀疏 MoE，每层 8 专家、top-2 路由，47B 总参 / 13B 激活、32K 上下文，性能 ≥ Llama 2 70B / GPT-3.5 而推理成本接近 13B dense；Apache-2.0 开源，是推理系统 MoE 支持的常见基准。https://arxiv.org/abs/2401.04088
- DeepSeek-V2 (DeepSeek-AI, 2024-05, report) — 236B 总参 / 21B 激活 MoE，首提 MLA（KV 联合压缩到低维 latent，KV cache 减 93.3%）+ DeepSeekMoE 细粒度专家；vs DeepSeek-67B 训练成本 -42.5%、生成吞吐 +5.76×，8.1T token 预训练、128K 上下文。https://arxiv.org/abs/2405.04434
- The Llama 3 Herd of Models (Meta AI, 2024-07, report) — 405B dense 旗舰在最高 16384 H100 上以 4D 并行（TP+PP+CP+FSDP）训 15.6T token（峰值 3.8×10²⁵ FLOPs、MFU 约 38-43%），后训练用多轮 SFT + DPO（弃 PPO 求稳）；西方少见的工业级 infra 全披露。https://arxiv.org/abs/2407.21783
- DeepSeek-V3 Technical Report (DeepSeek-AI, 2024-12, report) — 671B 总参 / 37B 激活 MoE，MLA + DeepSeekMoE + 无辅助损失负载均衡 + MTP + FP8 混合精度训练 + DualPipe；14.8T token 预训练仅用 2.788M H800 GPU·hr、全程无不可恢复 loss spike，是算法-系统-硬件协同设计的标杆。https://arxiv.org/abs/2412.19437

## 增量补录（2026 调研后查漏，AI infra 维度）
- **GLM-5.2**（承 GLM-5）— **slime 异步 RL**(解耦 gen/train)、PD 分离、DP-attention(EP64/DP64)、FP8 rollout；Muon 零冗余通信、pipeline ZeRO2/激活offload；国产芯片全栈适配(昇腾/摩尔/海光/寒武纪/昆仑芯/沐曦/燧原)。[[llm/2026/glm-5.2|详]]
- **Kimi-K2.6**（承 K2.5）— **Decoupled Encoder Process (DEP)**，多模态训练效率达纯文本 90%；MuonClip。[[llm/2026/kimi-k2.6|详]]
- **MiniMax-M3** — MSA 协同 GPU kernel：exp-free TopK + KV-outer 稀疏注意力 + LSE 融合 + 动态负载均衡；109B 验证 prefill 14.2×/decode 7.6× vs GQA。[[llm/2026/minimax-m3|详]]
