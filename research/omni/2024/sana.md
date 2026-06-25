---
title: "Sana: Efficient High-Resolution Image Synthesis with Linear Diffusion Transformers"
org: "NVIDIA / MIT"
country: US
date: "2024-10"
type: tech-report
category: t2i
tags: [t2i, diffusion-transformer, linear-attention, deep-compression-ae, rectified-flow, efficient, on-device, gemma]
url: "https://arxiv.org/abs/2410.10629"
arxiv: "https://arxiv.org/abs/2410.10629"
pdf_url: "https://arxiv.org/pdf/2410.10629"
github_url: "https://github.com/NVlabs/Sana"
hf_url: "https://huggingface.co/Efficient-Large-Model/Sana_1600M_1024px"
modelscope_url: ""
project_url: "https://nvlabs.github.io/Sana/"
downloaded: [arxiv-2410.10629.pdf, sana--readme.md, sana--hf-modelcard.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Sana 是 NVIDIA+MIT 提出的「极致高效」文生图框架：用 **32× 深度压缩自编码器（DC-AE F32C32P1）+ 线性注意力 DiT（Linear DiT）+ 仅 decoder 的小 LLM（Gemma-2-2B）做文本编码 + Flow-DPM-Solver 少步采样**，把 4K 生成做到比 FLUX-12B **快 100+ 倍、模型小 20 倍**，0.6B 模型可在 16GB 笔记本 GPU 上 <1s 出 1024px 图（量化后 0.37s/张），同时 GenEval 0.64 / DPG 84.3 仍有竞争力。

## 背景与定位
2023–2024 年文生图主流走向四点共识：U-Net→Transformer（[[dit]]→[[pixart-alpha]]/[[stable-diffusion-3]]/[[flux-1]]）、用 VLM 自动打标、改进 VAE 与文本编码器、冲击超高分辨率（[[pixart-sigma]] 是首个能直接出近 4K 图的模型）。但产业模型参数越滚越大：PixArt 0.6B → SD3 8B → LiDiT 10B → Flux 12B → Playground v3 24B，训练/推理成本对普通用户极不友好。

Sana 直面这个矛盾，问"能否做出又快又便宜、云端与边缘都能跑的高分辨率生成器"。它不追求新增能力，而是**系统级地把效率拉满**：算法（DC-AE、Linear DiT、NoPE、Flow-DPM-Solver）与系统（Triton 核融合、W8A8 量化）协同，把 4096×4096 生成延迟从 baseline 469s 一路压到 9.6s（106× 加速）。技术脉络上它站在 [[latent-diffusion-ldm]] → [[dit]] → [[pixart-alpha]]/[[pixart-sigma]] 这条 DiT 文生图谱系上，是「效率派」分支的代表作，并直接催生了 SANA-1.5（训练/推理缩放）、SANA-Sprint（一步蒸馏）、SANA-Video 等后续家族。

## 模型架构
Sana 的 pipeline 由三块自研组件构成（见论文 Fig.5），整体仍保持 DiT 的宏观骨架以保证简单与可扩展性。

**1) Deep Compression Autoencoder（DC-AE，F32C32P1）**：传统 LDM 的 AE 下采样因子 F=8（AE-F8），DiT 再用 patch size P=2 压缩，得到 H/16×W/16 个 token。Sana 把压缩职责全部交给 AE：下采样因子 **F=32、通道 C=32、patch size P=1**（AE-F32C32P1）。相比常见的 AE-F8C4P2/F8C16P2，AE-F32 输出的 latent token 数减少 **16×**（DiT 端 token 数再减 4×）。这是 4K 生成能高效跑起来的核心。AE 内部也用线性注意力块替换自注意力以加速高分辨率收敛，并用多阶段训练（先低分辨率再在 1024px 上 finetune）提升重建质量。消融表明 F32C32 在 MJHQ-30K 上 rFID=0.34、PSNR 29.29、SSIM 0.84，接近 SDXL 的 F8C4（rFID 0.31），远好于此前 SD 的 F32C64（rFID 0.82）；并验证「把 token 压缩放在 AE 而非加大 DiT patch size」更优（F32C32P1 的生成 FID 优于 F8C16P4/F16C32P2，尽管后者重建 rFID 更好）。

**2) Linear DiT**：把 DiT 里所有 vanilla softmax 自注意力换成 **ReLU 线性注意力**（Katharopoulos 2020），复杂度从 O(N²) 降到 O(N)（共享项 ΣReLU(Kⱼ)ᵀVⱼ 与 ΣReLU(Kⱼ)ᵀ 只算一次，对每个 query 复用）。线性注意力缺非线性相似度、收敛慢，故用 **Mix-FFN** 替换原 MLP-FFN——由 inverted residual + 3×3 depth-wise conv + GLU 组成，用深度卷积补回局部信息聚合能力。Mix-FFN 的副产物是 **NoPE（DiT 首次完全去掉位置编码）**：3×3 零填充卷积隐式注入了位置信息，去掉绝对/可学习/RoPE 位置编码后无质量损失，且利于长度泛化。文本以 cross-attention 注入。

**3) Decoder-only 小 LLM 文本编码器**：用 **Gemma-2-2B-IT** 替代 T5，取 decoder 最后一层特征作 text embedding。decoder-only LLM 有更强的指令跟随、CoT、in-context learning 能力；Gemma-2-2B 比 T5-XXL 推理快约 6×、效果相当。配套设计 **Complex Human Instruction（CHI）**：用 in-context 示例引导 Gemma 把用户短 prompt 扩写为细节丰富的「Enhanced prompt」，显著提升图文对齐与短 prompt 稳定性。

**参数与分辨率策略**：Sana-0.6B（width 1152 / depth 28 / FFN 2880 / 36 heads，590M 参数）层宽几乎对齐原始 DiT-XL 与 PixArt-Σ；Sana-1.6B（width 2240 / depth 20 / FFN 5600 / 70 heads，1604M）。分辨率走级联：跳过 256px，**直接从 512px 预训练**，再逐步 finetune 到 1024/2K/4K；2K/4K finetune 阶段会重新引入位置编码（PE 插值，约 10K 迭代即收敛）。

## 数据
官方报告**未披露**训练数据的总规模、来源、配比与版权/安全过滤细节（这是 Sana 报告的明显缺口）。已披露的是**标注与配比方法**：

- **Multi-Caption 自动标注**：对每张图（无论原本有无 prompt），用 4 个 VLM 同时打标——VILA-3B/13B 与 InternVL2-8B/26B，多模型互补提升 caption 的准确性与多样性。
- **CLIP-Score Caption Sampler**：一图多 caption 训练时如何选？提出按 clip score 概率采样 P(cᵢ)=softmax(cᵢ/τ)，温度 τ 控制采样强度（τ→0 只取最高分）。消融（Table 4，65K 步）显示：单 caption / 多随机 / 多 clipscore 的 FID 几乎一致（6.13/6.15/6.12），但 multi-clipscore 的 CLIP-Score 最高（27.10→27.26），即对图文对齐有正收益、对画质影响极小。
- HF model card 标注模型语言为 en + zh，并在 2024/11 发布了多语言（Emoji/中文/英文）SFT 模型；论文附录还报告了**零样本语言迁移**——训练时已过滤掉非英文 prompt，但靠 Gemma-2 的预训练泛化，推理时仍能理解中文/Emoji 并生成对应图像。

## 训练方法
**训练目标：Flow-based / Rectified Flow（velocity 预测）**。沿用 SD3 的分析：扩散统一形式 xₜ=αₜx₀+σₜε，DDPM 做噪声预测 εθ=ε，而 RF 做速度预测 vθ=ε−x₀、EDM 做数据预测 xθ=x₀。在 t≈T 处噪声预测易退化为 xₜ 的线性函数、累积误差大，数据/速度预测更稳更快收敛。256×256 对比（Table 3，120K 步）：DDPM 的 FID 19.5 / CLIP 24.6，Flow Matching 的 FID 16.9 / CLIP 25.7，flow 明显更好。

**采样器：Flow-DPM-Solver**。在 DPM-Solver++ 上改造适配 rectified flow——把缩放因子 αₜ 替换为 1−σₜ，时间步重定义到 [0,1] 并做 time-step shift（更低 SNR，跟随 SD3），模型输出按 data←x₀=x_T−σ_T·vθ 转换。结果：**14~20 步收敛**，优于 Flow-Euler 需要的 28~50 步（且更稳）。

**训练稳定性 trick（用 LLM 当文本编码器的关键）**：直接把 Gemma decoder 特征当 cross-attention 的 K/V 训练会**频繁 NaN**——因为 decoder-only LLM 的 text embedding 方差比 T5 大几个数量级（存在大量大绝对值）。解法：在文本编码器后加 **RMSNorm 把方差归一到 1.0**，再乘一个**初始化为 0.01 的可学习小 scale factor** 加速收敛（消融见 Fig.6，缺 norm 即 NaN）。

**级联分辨率训练**：跳过 256px，512px 起步 → 1024 → 2K → 4K 逐级 finetune（得益于 F32C32P1 的低 token 数）。

**蒸馏/加速**：原始 Sana 论文本身不含一步/少步蒸馏；该方向由后续 **SANA-Sprint**（sCM 连续时间一致性蒸馏 + LADD，一步/少步生成，H100 0.1s/1024px）承接，已并入同一 repo。

**未披露**：训练总 GPU·时、batch size、学习率、总训练步数（论文只给消融用的局部步数如 52K/65K/120K）、优化器主超参（repo 后续提供了 CAME-8bit/FSDP 等省显存方案，但原报告未量化总算力）。

## Infra（训练 / 推理工程）
- **Triton 核融合**：对线性注意力的前/反向都用 Triton 融核——把激活函数、精度转换、padding、除法等 element-wise 操作融进矩阵乘，减少数据搬运开销。1024px 下使 Linear DiT 略快于原始 DiT，高分辨率优势更大；融核带来约 10% 额外加速。
- **W8A8 INT8 量化（端侧部署）**：激活做 per-token 对称 INT8、权重做 per-channel 对称 INT8；保留 normalization、线性注意力、cross-attn 的 KV 投影为全精度以保语义相似度。CUDA C++ 手写 W8A8 GEMM 核 + 核融合（把 ReLU(K)ᵀV 与 QKV 投影融合、GLU 与量化核融合、调整 layout 避免 GEMM/Conv 转置）。结果：笔记本 GPU 上 1024px 生成 **0.88s→0.37s（2.4× 加速）**，CLIP-Score 28.5→28.3、ImageReward 1.03→0.96，近乎无损。
- **测速口径**：所有 throughput/latency 在单张 A100、FP16、batch=1（latency）/ batch=16（throughput）、采样 20 步下测得。
- **后续 repo 工程化（README 披露，超出原论文）**：4bit-Sana（SVDQuant/Nunchaku 引擎）可在 8GB 显存跑；DC-AE tiling 让 4K 推理在 22GB（配 offload+量化后 8GB）显存内完成；FSDP/DDP 训练、CAME-8bit 优化器省显存；diffusers 原生支持 SanaPipeline；代码库 2025/1 起改为 Apache-2.0（模型权重为 NVIDIA Open Model License + Gemma 条款）。
- **未披露**：训练集群规模、并行策略（原论文层面）、训练吞吐。

## 评测 benchmark（把效果讲清楚）
评测指标：FID、CLIP-Score（均在 MJHQ-30K 30K 图上）、GenEval（533 prompt）、DPG-Bench（1065 prompt）、ImageReward（100 prompt）。下列数字均来自论文 Table 7/10/11（A100 FP16，采样 20 步）：

**1024×1024 主表（Table 7）**：

| 模型 | 参数 | 延迟(s) | 加速 | FID↓ | CLIP↑ | GenEval↑ | DPG↑ |
|---|---|---|---|---|---|---|---|
| **Sana-0.6B** | 0.6B | 0.9 | 39.5× | 5.81 | 28.36 | 0.64 | 83.6 |
| **Sana-1.6B** | 1.6B | 1.2 | 23.3× | 5.76 | 28.67 | 0.66 | 84.8 |
| PixArt-Σ | 0.6B | 2.7 | 9.3× | 6.15 | 28.26 | 0.54 | 80.5 |
| SD3-medium | 2.0B | 4.4 | 6.5× | 11.92 | 27.83 | 0.62 | 84.1 |
| FLUX-dev | 12.0B | 23.0 | 1.0×(base) | 10.15 | 27.47 | 0.67 | 84.0 |
| FLUX-schnell | 12.0B | 2.1 | 11.6× | 7.94 | 28.14 | 0.71 | 84.8 |

（加速比以 FLUX-dev=1.0× 为基准；SD3-medium 参数列论文原值为 2.0B。）核心结论：Sana-0.6B 在 DPG 上与 FLUX-dev 持平、GenEval 略低（0.64 vs 0.67），但 **throughput 快 39×**；Sana-1.6B 快 23×。512×512 上 Sana-0.6B throughput 是同体量 PixArt-Σ 的 5×，且 FID/CLIP/GenEval/DPG 全面胜出。

**GenEval 细分（1024px，Table 10）**：Sana-1.6B Overall 0.66（Single 0.99 / Two 0.77 / Counting 0.62 / Colors 0.88 / Position 0.21 / Color-Attr 0.47）；弱项与多数模型一致在 Position/计数。**DPG-Bench 细分（Table 11）**：Sana-1.6B Overall 84.8（Entity 91.5 / Attribute 88.9 / Relation 91.9 / Other 90.7），ImageReward 0.99（Sana-0.6B 0.97）。

**速度（Table 14，多分辨率，相对 FLUX-dev=1×）**：4096×4096 下 Sana-0.6B 延迟 9.6s vs FLUX-dev 1023s（**104×**，Fig.2 用 Sana 自身未优化 baseline 469s→9.6s 口径记为 106×）、Sana-1.6B 5.9s（66×）；2048×2048 Sana-0.6B 2.5s（53.8×）vs FLUX-dev 117s；1024×1024 Sana-0.6B 0.9s vs FLUX-dev 23s。分辨率越高 Sana 优势越大。

**关键消融**：
- Block 设计（Table 8/12）：FullAttn→LinearAttn 延迟 2250→1931ms 但画质降；加 Mix-FFN 补回画质（代价是效率，2425ms）；加 Triton 融核后 Linear DiT 整体略快于原 DiT。AE-F8C4P2→F32C32P1 使 MACs 再降 4×、throughput 升 4×。
- 文本编码器（Table 9/13）：Gemma2-2B-IT 在 Sana-1.6B 上 FID 6.1/CLIP 26.9，与 T5-XXL（FID 6.1/CLIP 27.1）相当但延迟 0.28s vs 1.61s（~6× 快）。
- CHI（Table 2）：从头训 52K 步 GenEval 45.5→47.7（+2.2）；140K+5K finetune 52.8→54.8（+2.0）。
- 端侧量化（Table 5）：W8A8 后 0.37s/张，CLIP/ImageReward 近无损。

（注：README 中 performance 表给出的是发布后更新权重的略好数字，如 Sana-0.6B FID 5.61/GenEval 0.68，与论文表格略有差异，以论文原值为准记录。）

## 创新点与影响
**核心贡献**：(1) **DC-AE F32C32**——把 latent 压缩从 8× 推到 32× 且重建质量逼近 F8C4，是高分辨率高效生成的地基（同期姊妹工作 arXiv:2410.10733）；(2) **Linear DiT + Mix-FFN + NoPE**——首次系统验证线性注意力可在图像生成中媲美 softmax，并首个完全去掉 DiT 位置编码；(3) **decoder-only 小 LLM 当文本编码器 + CHI**——给出 LLM-as-text-encoder 的稳定化方案（RMSNorm + 小 scale，解决 NaN）与指令工程；(4) **Flow-DPM-Solver** 把采样压到 14~20 步；(5) 算法-系统协同（Triton 融核 + W8A8）实现笔记本/4090 端侧亚秒级 1024px 生成。

**影响**：Sana 成为「效率派」文生图的标杆，证明 0.6B 小模型靠系统级设计就能在质量上贴近 12B 巨模型而快两个数量级，显著降低高分辨率/4K 生成的算力门槛。它直接催生庞大的 SANA 家族——SANA-1.5（训练/推理时计算缩放，ICML-2025）、SANA-Sprint（sCM 一步蒸馏，ICCV-2025，H100 0.1s）、SANA-Video（文生视频）、SANA-WM（可控世界模型）、Sol-RL（NVFP4 rollout + BF16 训练的 RL 后训练）等，并被 diffusers/ComfyUI/SGLang/Cosmos-RL 广泛集成。Linear DiT + DC-AE 的「把 token 压缩交给 AE」范式也影响了后续高效视频/3D 生成。

**已知局限**：作者明示——无法完全保证生成内容的安全与可控；text rendering、人脸与手部等复杂情形仍有挑战；GenEval 的 Position/Counting 维度弱于 FLUX。此外**原始报告对训练数据规模/来源、总训练算力均未披露**，可复现性受限（虽代码与权重开源）。

## 原始链接
- tech-report (arXiv abs): https://arxiv.org/abs/2410.10629
- pdf: https://arxiv.org/pdf/2410.10629
- project page: https://nvlabs.github.io/Sana/
- github: https://github.com/NVlabs/Sana
- hf model (Sana-1.6B 1024px): https://huggingface.co/Efficient-Large-Model/Sana_1600M_1024px
- hf collection: https://huggingface.co/collections/Efficient-Large-Model/sana
- DC-AE 姊妹论文: https://arxiv.org/abs/2410.10733

## 本地落盘文件
- ../../../sources/omni/2024/arxiv-2410.10629.pdf
- ../../../sources/omni/2024/sana--readme.md
- ../../../sources/omni/2024/sana--hf-modelcard.md
