# MiniCPM 家族训练配方深挖（面壁智能 ModelBest / OpenBMB / 清华 THUNLP）

> 本文只采信一手官方来源（arXiv 原文 PDF、官方 HF model card / config.json、官方 GitHub）。
> 已落盘 PDF 均逐页精读抠数字；架构数字尽量交叉核对官方 `config.json`。
> 查不到或官方未公开的，明确标注「官方未公开」。
> 编写日期：2026-06-18。

---

## 家族演进脉络

MiniCPM 是面壁智能（ModelBest）联合清华 NLP（OpenBMB）的「端侧小模型 + 可扩展训练策略」系列。核心方法论贯穿始终：

1. **Model Wind Tunnel / ModelTunnel（模型风洞）**：用百万级小模型 + µP（Tensor Program / Maximal Update Parameterization）搜超参（LR、batch size、初始化），把经验迁移到大模型，避免逐尺度调参。
2. **WSD（Warmup-Stable-Decay）学习率调度**：把训练显式拆成「warmup → 高恒定 LR 稳定段 → 末段快速退火（decay/annealing）」。这是 MiniCPM 的招牌创新，支撑：连续训练、低成本测 scaling law、退火段注入高质量数据。
3. **两阶段预训练 + 退火数据注入**：稳定段只用大规模粗质量数据；退火段混入高质量知识/SFT 数据 —— 在退火段加高质量数据收益远大于只在 SFT 阶段加。
4. **高数据-模型比**：MiniCPM 实测 compute-optimal 数据/模型比约 **192:1**（远高于 Chinchilla 的 ~20:1）。

代际主线：

- **MiniCPM v1（2024.02）** — 1.2B / 2.4B 稠密，WSD + 风洞 + 退火，衍生 DPO / 128K / MoE。论文 arXiv 2404.06395。
- **MiniCPM 2.0（2024.04）** — 同 2.4B 基座的 SFT/退火数据升级版（无独立论文，并入 v1 GitHub）。
- **MiniCPM3-4B（2024.09）** — 改用 **MLA（多头潜注意力）**，62 层深瘦结构，function calling / code interpreter，32K 上下文。无独立 arXiv，复用 2404.06395 + HF model card。
- **MiniCPM4 / 4.1（2025.06 / 2025.09）** — 0.5B / 8B，**InfLLM v2 可训练稀疏注意力** + UltraClean/UltraFineWeb 数据 + ModelTunnel v2（µP）+ FP8 + MTP + chunk-wise rollout GRPO + BitCPM4 三值量化。8.3T tokens。论文 arXiv 2506.07900。
- **MiniCPM-SALA（2026.02）** — 9B，**InfLLM-V2 稀疏 + Lightning 线性**混合注意力（1:3）+ HyPE，从 MiniCPM-4.0 中间 ckpt 续训转换，支持 1M 上下文。arXiv 2602.11761。
- **MiniCPM5-1B（2026.05，MiniCPM5 系列首款）** — dense 1B，**回归标准 LlamaForCausalLM**（hidden 1536 / 24 层 / 16 头·2 KV GQA / head_dim 128 / vocab 130560 / 128K / RoPE θ=5e6 / bf16），无自定义 kernel，主流引擎可直接加载。UltraData 分层数据 base→mid→post 三阶段（arXiv 2602.09003）；后训练 **RL + OPD 两阶段 Reasoning RL**（math/code/IF 均分 ↑16、超长回复 ↓29pp）；Think/No-Think 双模 + XML tool-call（SGLang minicpm5 parser）。1B 级开源 SOTA（均分 42.57 vs 35.61）。详见 [2026/minicpm5-1b.md](llm/2026/minicpm5-1b.md)。
- **多模态线 MiniCPM-V / MiniCPM-o**：V 1.0/2.0（2024）→ MiniCPM-Llama3-V 2.5（8B，2024.05，arXiv 2408.01800）→ V 2.6（Qwen2-7B，2024.08）→ o 2.6（Qwen2.5-7B + 全模态，2025.01）→ V 4.5（Qwen3-8B，2025.09，arXiv 2509.18154）→ o 4.5（Qwen3-8B 全模态全双工，2026.04，arXiv 2604.27393）。

> 注意：多模态线从 V 2.6 起 **LLM 骨干换成外部模型**（Qwen2/Qwen2.5/Qwen3），不再用自研 MiniCPM 基座；V 1.0~2.0 与 V2.5 用 MiniCPM/Llama3。

---

## 各代关键参数对比（稠密/MoE LLM 线）

| 型号 | 总参(非emb) | 层数 L | 隐藏 d_model | FFN d_ff | 注意力 | 头 nq / KV nkv | vocab | 上下文 | tokenizer | 训练 token | LR sched |
|---|---|---|---|---|---|---|---|---|---|---|---|
| MiniCPM-1.2B | 1.247B | 52 | 1,536 | 3,840 | GQA, head_dim 64 | 24 / 8 | 73,440 | 4K | 自研 BPE | 1.1T | WSD |
| MiniCPM-2.4B | 2.442B | 40 | 2,304 | 5,760 | MHA, head_dim 64 | 36 / 36 | 122,753 | 4K | 自研 BPE | 1.1T | WSD |
| MiniCPM-2.4B-128K | 同上 | 40 | 2,304 | 5,760 | MHA | 36 / 36 | 122,753 | 128K(ABF+NTK) | 同上 | 续训(20B 5000步退火) | WSD |
| MiniCPM-MoE-8x2B | 13.6B 总 / ~4B 激活 | 40 | 2,304 | 5,760 | MHA + MoE | 8 专家 top-2 | 122,753 | 4K | 同 2.4B | upcycle，130K 步 | WSD |
| MiniCPM3-4B | ~4B(含 emb) | 62 | 2,560 | 6,400 | **MLA** (q_lora 768, kv_lora 256, rope32+nope64) | 40 / 40 | 73,448 | 32K(LongRoPE) | 自研 | 官方未公开总量 | WSD(推断) |
| MiniCPM4-0.5B | 0.5B | 24 | 1,024 | 4,096 | GQA, InfLLM v2 | 16 / 2 | 73,448 | 32K(train)→128K(YaRN) | 自研 | 官方未公开(0.5B 单列) | WSD |
| MiniCPM4-8B | 8B | 32 | 4,096 | 16,384 | GQA, InfLLM v2 | 32 / 2 | 73,448 | 32K(train)→128K(YaRN) | 自研 | **8.3T** | WSD(7T稳+1.3T退火) |
| MiniCPM4.1-8B | 8B(混合推理) | 32 | 4,096 | 16,384 | GQA, InfLLM v2 | 32 / 2 | 73,448 | 64K→128K(YaRN) | 自研 | 续 4-8B + long-CoT | WSD + SFT+RL |
| MiniCPM-SALA-9B | 9B | 官方未公开 L | 官方未公开 | 官方未公开 | **InfLLM-V2 + Lightning 混合(1:3)** + HyPE | GQA(继承) | 官方未公开 | 1M | 自研 | 转换续训 ~2T | 多阶段(5 stage) |

> µP 相关：MiniCPM4 全系 `dim_model_base=256, scale_emb=12, scale_depth=1.4`（µP 缩放系数），`tie_word_embeddings` 在 0.5B 为 true、8B 为 false。所有 MiniCPM 系自研 tokenizer vocab 在 73,440/73,448 与 2.4B 的 122,753 两套。

---

## MiniCPM v1（MiniCPM-1.2B / 2.4B，arXiv 2404.06395）

家族奠基论文，WSD / 风洞 / 退火 / scaling law 细节最丰富。以下数字全部抠自 PDF 原文。

### 架构细节（Table 2）
- **MiniCPM-2.4B**：非 emb 参数 **2,442,057,984**；d_model 2,304；d_ff 5,760；head_dim 64；nq=36，nkv=36（**MHA，未改注意力**）；L=40 层；batch 4M tokens；训练 1.1T。
- **MiniCPM-1.2B**：非 emb 参数 **1,247,442,432**；d_model 1,536；d_ff 3,840；head_dim 64；nq=24，nkv=8（**GQA**，受 MobileLLM 启发以省参）；L=52 层（**更深更瘦**）；batch 2M→4M；训练 1.1T。
- **深瘦网络**：2.4B 用 40 层（对比 Phi-2 的 32 层）；1.2B 进一步深瘦到 52 层。
- **Vocabulary**：2.4B 用 **122,753** 词表，1.2B 用 **73,440** 词表（小词表利于端侧效率）。含 embedding 后总参分别 +0.3B / +0.2B。
- **Shared Input-output Embedding（权重绑定）**：两个模型都做输入/输出 embedding 共享以省参。
- **激活/Norm**：SwiGLU + RMSNorm（系列惯例，论文未单列但 config 体现）。位置编码 RoPE。

### 训练数据
- 稳定段约 **1T tokens**，绝大多数来自开源数据集。
- 稳定段数据混合（Figure 11，%）：CommonCrawl Chn 中文清洗语料、Dolma、C4、Pile（英文，MinHash 去重）、Code Pretrain（the Stack + StarCoder，内/跨去重）等。给出的占比片段：Code Pretrain 25.0 / CommonCrawl Chn 25.0 / Pile 15.0 / C4 6.7 / Dolma 4.8 / Wikipedia / Book Chinese / Baidu Baike 等。
- 退火段数据混合（更多样、含自有数据）：Dolma 15.7、Code Pretrain 14.6、CommonCrawl Chn、EvolInstruct 19.6、OssInstruct、SlimOrca、Logic SFT、ShareGPT4、Open Web Math 9.5、Arxiv、peS2o、Math SFT、Stack Exchange QA、Math Synthetic、UltraChat、Knowledge SFT、Code SFT、Baidu Baike、Law Pretrain 等（后缀 SFT 的为自有专有数据：LeetCode、K12 教材/题目等）。

### 数据处理 pipeline
- 英文语料（Dolma/C4/Pile）：**MinHash** 算法做语料内 + 跨语料去重。
- Code：the Stack + StarCoder，内去重 + 跨去重。
- CommonCrawl 中文：从原始 CC 经「彻底清洗」得到。
- 论文未细写质量分类器/edu 打分/去毒/PII 等细节（v1 阶段；这些在 MiniCPM4 的 UltraClean 才系统化）。

### 数据配比 / 退火 / 课程
- **两阶段策略**：稳定段只用大规模粗质量数据（可持续续训）；退火段把高质量知识 + SFT 数据混入预训练数据。
- 消融结论：退火段加 SFT 数据（A-2）显著优于只在 SFT 阶段加（A-1）；能力专精应从退火段开始。
- **数据-模型比**：α=0.29、β=0.23、K²=0.01、η=−0.10；实测 compute-optimal **Dopt/Nopt ≈ 192**（C=1e21 时各语料 95~834，平均 ~192），远高于 Chinchilla ~20。

### 训练细节
- 优化器 **Adam**。
- 风洞实验：µP（Tensor Program 宽度 + 深度缩放，未用 attention softmax scaling）；在 0.04B~2.1B 验证最优 base LR 稳定在 **~0.01**。
- 最优 batch size 经验式：`bs = 1.21e9 / L^6.24`（C4 loss）。
- **稳定段**：~1T 数据，batch size **3.93M**，max LR **0.01**，WSD。
- **退火/decay 段**：指数退火 `f(s−T)=0.5^((s−S)/T)`，T=**5000 步（20B tokens）**；退火约占总 token 的 **10%**（论文证明 10% 足够，2.5% 不足）。
- **SFT 段**：约 **6B tokens**，LR 接续退火末端，仍用 WSD 指数退火。
- WSD 训练动力学分析：退火段 loss 骤降；权重更新幅度与 LR 正相关；退火段梯度范数下降、相邻梯度余弦转正、曲率上升（接近局部最优）。算力/卡型/卡时官方未公开（论文未给）。并行策略官方未公开。

### SFT 细节
- 退火 + SFT 用类似数据；SFT 阶段排除预训练数据，约 6B tokens。
- 数据源：UltraChat、SlimOrca、EvolInstruct、OssInstruct、ShareGPT4 + 自有（LeetCode、K12 等）。

### RL / 对齐（MiniCPM-DPO）
- 算法 **DPO**（Rafailov 2024），1 epoch，LR **1e-5**，Cosine LRS。
- 偏好数据：主用 **UltraFeedback**；自建专有偏好集增强 code/math。
- 效果：MTBench 6.89(SFT)→**7.25**（超 Llama2-70B-Chat），但有 alignment tax。

### 衍生变体
- **MiniCPM-2.4B-128K**：从 2.4B 稳定段末 ckpt 续训；4K→32K 用 **ABF（Adjusted Base Frequency）**，32K→128K 用 **NTK-Aware RoPE Scaling + 课程学习**；解除输入/输出 embedding 共享（为 vocab 并行），LM head 由输入 embedding 初始化；长/短数据 = **44% / 56%**；用合成长 QA 数据。
- **MiniCPM-MoE（8x2B）**：**Sparse Upcycling** 从稠密稳定段 ckpt 初始化，每个 MLP 换成 MoE 层（复制原 MLP，router 随机初始化 N(0,0.01²)）；总非 emb **13.6B**，8 专家 **top-2** 激活，激活参 ~4B；**load balancing loss ×0.01**（有辅助损失，非无辅助损失）；batch 4M（稳定+退火）/2M（SFT），预训练（续训+退火）共 **130K 步**。

### MiniCPM 2.0（2024.04，无独立论文）
- 同 2.4B 基座的 SFT / 退火数据升级版（官方 GitHub 描述为能力增强更新，非新结构）。细节并入 v1 仓库，无独立技术报告。

### 来源
- arXiv abs: https://arxiv.org/abs/2404.06395 ｜ PDF: https://arxiv.org/pdf/2404.06395
- GitHub: https://github.com/OpenBMB/MiniCPM
- 本地：../../../sources/llm/2024/minicpm.pdf

---

## MiniCPM3-4B（2024.09，HF model card + config.json）

无独立 arXiv 技术报告；HF 页 cite 2404.06395。架构数字抠自官方 `config.json`。

### 架构细节（config.json）
- architectures: `MiniCPM3ForCausalLM`；hidden 2,560；**62 层**（极深瘦）；intermediate 6,400；vocab **73,448**；max_position **32,768**。
- **注意力 = MLA（Multi-head Latent Attention，类 DeepSeek-V2）**：num_attention_heads 40，num_key_value_heads 40；`q_lora_rank=768`，`kv_lora_rank=256`，`qk_rope_head_dim=32`，`qk_nope_head_dim=64`。这是 MiniCPM 线首次用 MLA 压 KV cache。
- µP 系数：`dim_model_base=256, scale_emb=12, scale_depth=1.4`。
- 上下文扩展：`rope_scaling.type=longrope`（LongRoPE，长/短 factor 各 16 维）。
- 能力：原生支持 **function calling / code interpreter**（官方主打）。

### 训练数据 / pipeline / 配比
- **官方未公开**预训练总 token 数、语料构成、配比、清洗 pipeline（model card 未给）。延续 WSD + 风洞 + 退火方法论（沿用 2404.06395），但具体数字未单独披露。

### SFT / RL
- model card 未披露 SFT 数据规模、RL 算法等细节，**官方未公开**。

### 来源
- HF: https://huggingface.co/openbmb/MiniCPM3-4B （config.json: /raw/main/config.json）
- GitHub: https://github.com/OpenBMB/MiniCPM
- 关联论文: https://arxiv.org/abs/2404.06395

---

## MiniCPM4 / MiniCPM4.1（0.5B / 8B，arXiv 2506.07900）

「端侧极致高效」系列，四维创新：架构（InfLLM v2）、数据（UltraClean/UltraFineWeb + UltraChat v2）、算法（ModelTunnel v2 + chunk-wise rollout RL + BitCPM4）、推理系统（CPM.cu）。8B 用 Qwen3-8B 约 **22%** 训练数据达到可比性能。

### 架构细节（config.json + 论文）
- **MiniCPM4-8B**：`MiniCPMForCausalLM`，hidden 4,096，**32 层**，intermediate 16,384，**GQA 32 头 / 2 KV**，vocab **73,448**，max_position 32,768，rope_theta 1e4，`tie_word_embeddings=false`，bf16。
- **MiniCPM4-0.5B**：hidden 1,024，24 层，intermediate 4,096，GQA 16 头 / 2 KV，vocab 73,448，`tie_word_embeddings=true`。
- **MiniCPM4.1-8B**（混合推理）：同 8B 结构，`max_position_embeddings=65536`（64K），LongRoPE。
- µP：`dim_model_base=256, scale_emb=12, scale_depth=1.4`。
- **InfLLM v2（可训练稀疏注意力）**：把 KV cache 分块（每块 m tokens），query group 共享同组 KV 块选择（GQA 级别）以省访存；Top-K 块选择 + 语义核（semantic kernels，mean pooling 构造块表示）；初始 token + 局部滑窗 token 恒选；不引入额外注意力输出参数，短序列退化为普通注意力；论文称比 NSA 省 **60%** 计算。预填充 + 解码双阶段都加速。
- 上下文：4K 训练 → 32K 长上下文续训（**LongRoPE**）→ 128K 推理（**YaRN**，RULER-NIAH 验证）。

### 预训练数据 + UltraClean pipeline
- **总量 8.3T tokens**（8B），「仅用 8T 量级即可达到满意性能」。
- **UltraFineWeb**：对 FineWeb（英）+ Chinese FineWeb 应用 UltraClean 过滤得到的高质量知识密集语料。
- **UltraClean 过滤 pipeline**：
  - **高效验证策略**：不从头训 LLM 验数据，而是先用 WSD 训一个 1B 模型到 **1.1T tokens（1T 稳 + 0.1T 退火）**，再用两阶段退火在 **10B tokens** 上微调（30% 留验证、70% 默认混比），用「退火段性能增益」当数据质量指标；把单次验证从 1200 GPU·h 降到 ~110 GPU·h（32 卡 <3.5h）。
  - **分类器**：核心假设「能提升 LLM 的高质量种子数据也利于训分类器」。正样本 = 高效验证筛出的 LLM 打分>4 的领域内数据、指令格式集（OH-2.5、ELI5）、教育材料、LLM 合成教科书内容、精选优质 web；负样本 = FineWeb/C4/Dolma/Pile/RedPajama（英）+ CCI3/ChineseWebtext 等（中）。**迭代训练**：用当前分类器推断的正负样本作下一轮训练数据。
  - **FastText 分类器**（非 LLM 分类器）：大幅降推理成本，全 web 规模过滤。

### 训练算法（ModelTunnel v2 + 工程）
- **ModelTunnel v2**：µP（Maximal Update Parameterization）+ 超参搜索，百万级小模型搜 LR/batch/初始化；性能指标改用 ScalingBench；论文对比 µP vs StepLaw vs vanilla。
- **预训练 4 阶段 pipeline**：① 稳定段 **7T tokens**，LR **7e-3**，上下文 4K；② 退火段 **1T tokens**，4K；③ 长上下文 4K→32K，**20B tokens**，LongRoPE；④ 混合 SFT+RL 得 MiniCPM4.1。（论文亦表述为 8.3T 中 7T warmup+stable、1.3T annealing。）
- **MTP（多 token 预测）**：额外预测头为单层 Transformer，embedding/output head 与主模型共享；目标 `L = L_NTP + λ·L_MTP`。也用于提升投机采样接受长度。
- **FP8 混合精度**（仿 DeepSeek-V3）：参数 128×128、激活 128×1 在线分块量化；FP8 MMA + FP32 累加；仅对线性投影用 FP8（前向激活 + 反向输入梯度），参数梯度用 **BF16**。
- 算力：预训练 GPU 集群规模 / 卡时 / FLOPs **官方未公开**（论文只说「充分利用 GPU 集群算力」）。

### SFT 细节（UltraChat v2）
- **UltraChat v2**：合成 SFT 数据，五大能力轨：知识应用、推理、指令遵循、长上下文、工具调用。
- 知识密集数据：从领域语料/考纲/教材抽知识点 → LLM 生成 QA → 指令进化 + 答案多样性进化。
- 推理数据：数学（按学科+学段分层，主动降低易题占比；多解法路径；启发式规则保证可验证）+ 代码（真实 GitHub 片段，配单元测试/IO 做可执行校验，跨语言翻译）。
- 工具调用：含 glaive-function-calling-v2 等。
- 双阶段过滤（自动 + 人工）。

### RL / 对齐（chunk-wise rollout GRPO）
- **先 SFT 长-CoT 蒸馏数据**做冷启动（提供更好 RL 初始化），再 RL。
- 算法 = **改进版 GRPO**，改进点：Dynamic Sampling（过滤全对/全错 prompt）、Clip-Higher（抬高重要性采样上裁剪阈值防熵塌缩）、Token-level Policy Gradient Loss、Overlong Sample Filtering（截断样本不计 loss）。
- **Chunk-wise Rollout（负载均衡 RL）**：限制每轮 rollout 最大输出 token，未完成轨迹存重放缓冲下轮续生，配 KL loss、dual-clip、chunk 级重要性采样、garble filter 稳定。提升 GPU 利用率。
- **奖励 = 规则可验证（RLVR）**：数学用规则匹配 + SymPy 符号验证（数据来自 DAPO、Deepscaler、Numina、Prime）；代码在 **Firejail 沙箱**跑 Python，按通过测试比例给 reward（全过=1.0，数据来自 LeetCode/TACO/Kodcode/Codeforces）。
- 数据过滤：Semhash 去重；用 DeepSeek-R1-Distill-Qwen-1.5B 生成 4 次预测，4 次全对的题滤掉（保留难题）；代码数据上采样。
- RL 实验：**64× A800 GPU**，batch 64（论文 Table 5 上下文）。
- MiniCPM4.1 = 混合推理（deep reasoning / non-reasoning 两模式）。

### BitCPM4（三值/ternary LLM）
- 两阶段 QAT 框架，用预训练高精度模型初始化量化阶段，大幅降 QAT 成本；结合 ModelTunnel v2。

### AI infra / 推理系统
- **CPM.cu**：自研推理框架，集成稀疏注意力（InfLLM v2 kernel）+ 模型量化 + 投机采样。
- **FR-Spec**：频率排序投机采样，draft 模型只用 ~**25%** 高频词表子集，最终分布与标准投机采样一致。
- **P-GPTQ**：前缀感知 PTQ（端侧量化），观察到首 token / 深层下投影层协方差异常。
- 端侧实测：Jetson AGX Orin、RTX 4090 等上长序列 prefill/decode 提速（Figure 1）。

### 来源
- arXiv abs: https://arxiv.org/abs/2506.07900 ｜ PDF: https://arxiv.org/pdf/2506.07900 （v2, 2025-09-04）
- HF: https://huggingface.co/openbmb/MiniCPM4-8B ｜ https://huggingface.co/openbmb/MiniCPM4.1-8B ｜ https://huggingface.co/openbmb/MiniCPM4-0.5B
- GitHub: https://github.com/openbmb/minicpm
- 本地：../../../sources/llm/deep-dive/minicpm4.pdf

---

## MiniCPM-SALA-9B（2026.02，arXiv 2602.11761）

稀疏 + 线性混合注意力的高效长上下文模型；**不是从头训**，而是从 **MiniCPM-4.0 中间 ckpt（已训 7T tokens）转换续训**。

### 架构细节
- **9B 参数**混合架构：**InfLLM-V2 稀疏注意力 + Lightning Attention 线性注意力，按 1:3（25% 稀疏 / 75% 线性）层选择算法交错**。保留 FFN。
- **HyPE（Hybrid Positional Encoding）**：稀疏层用 RoPE，线性层移除 RoPE（靠递归保相对序），调和长短上下文性能；缓解长上下文激活 spike，线性层加输出门。
- 上下文：支持 **1M tokens**；A6000D 上 256K 序列推理速度达全注意力的 **3.5×**；A6000D / 5090 上可跑 1M（Qwen3-8B 此长度 OOM）。
- 继承 MiniCPM-4.0 的 GQA、tokenizer 等；层数/隐藏维等具体配置论文正文未单列（**部分官方未公开**，以 HF 权重为准）。

### 训练细节（转换续训框架）
- 基座 = **MiniCPM-4.0 中间 ckpt（7T tokens）**；**Transformer→hybrid 转换共 ~2T tokens**（约为 MiniCPM-4.0 从头训 8T 的 25%）。
- 五阶段 pipeline（论文 Table 1）：① **HALO（Hybrid Attention via Layer Optimization）架构转换**：全 softmax 注意力先转线性，部分后续作为稀疏注意力训练；② 后续续训 + 长上下文 + 后训练阶段（含 SFT / RL，论文表述「更广泛的 continual pre-training 与 post-training」）。
- 跨架构蒸馏（cross-architecture distillation）用于转换。
- 对标 Qwen3-Next、Kimi-Linear 等线性/混合方案。
- 精度 / 并行 / GPU 卡时 **官方未公开**。

### 来源
- arXiv abs: https://arxiv.org/abs/2602.11761 ｜ PDF: https://arxiv.org/pdf/2602.11761 （v2, 2026-02-28）
- HF: https://huggingface.co/openbmb/MiniCPM-SALA
- GitHub: https://github.com/OpenBMB/MiniCPM
- 本地：../../../sources/llm/2026/minicpm-sala.pdf

---

## MiniCPM-V 系列（多模态，arXiv 2408.01800 为系统报告）

端侧 MLLM。论文以 **MiniCPM-Llama3-V 2.5（8B）** 为例系统介绍 V 系列技术。

### 架构（三模块：视觉编码器 + 压缩层 + LLM）
- **视觉编码器**：**SigLIP SoViT-400m/14**。
- **压缩层**：**perceiver resampler**（单层 cross-attention，2D 位置感知）。每 slice 编码为 1,024 tokens，压缩为 **64 queries（V1&V2）/ 96 tokens（Llama3-V 2.5）**。
- **LLM 骨干**：MiniCPM-Llama3-V 2.5 用 Llama3-8B（V1.0/2.0 用 MiniCPM-2.4B）。
- **自适应视觉编码（LLaVA-UHD）**：任意宽高比图像切片（每 slice 匹配 ViT 预训练分辨率/比例），最高 **1.8M 像素（1344×1344）**；2D 插值适配位置 embedding；slice 间用特殊 token + 空间 schema 包裹。

### 训练（预训练 + SFT + RLAIF-V）
- **预训练（多阶段）**：Stage-1 只训压缩层（其余冻结），视觉编码器固定分辨率；高分辨率阶段额外引入 OCR 数据增强；用辅助模型（GPT-4 标注种子）重写低质量 caption（Table 1 为图文 caption + OCR 数据）。
- **SFT**：part-1 传统 QA/caption（短响应）+ part-2 等。
- **RLAIF-V（对齐/降幻觉）**：响应生成 → 分治式打分（每条响应分 = −n_rej，n_rej 为无效声明数）→ **DPO**。偏好集 = 3K 图、6K 偏好对。基于 RLAIF-V / RLHF-V 技术。
- 端侧部署：量化 + NPU/GPU 加速，解码吞吐从 3.2 → 8.2 tokens/s。

### MiniCPM-V 2.6（2024.08，HF model card）
- **SigLip-400M + Qwen2-7B，总 8B**。新增多图 / 视频理解。基于 RLAIF-V + VisCPM；OpenCompass 65.2。多语言。
- config: vocab 151,700 量级，64 query resampler，slice 模式。
- 预训练 token 总量 / 配比 **官方未公开**（model card 未给）。

### MiniCPM-V 4.5（8B，arXiv 2509.18154）
- **LLM 骨干 = Qwen3-8B；视觉编码器 = SigLIP2-400M；总 8B**（config: LLM hidden 4096 / 36 层 / 32 头 / 8 KV / vocab 151,748 / ctx 40,960 / rope 1e6 = Qwen3-8B）。
- **统一 3D-Resampler**：2D-Resampler 扩到 3D，联合压缩时空；图像 16× 压缩、视频额外 6× 时序压缩；6s/2fps/448×448 视频 → 128 视觉 token（比代表 MLLM 省 12×~24×），视频整体可达 **96× 压缩**（6 帧 448×448 → 64 token）。
- **统一文档知识 + OCR 学习范式**：动态按噪声等级腐蚀文档文本区，逼模型从文档图像直接学知识（无需外部解析器）；relevance-aware masking。
- **训练 recipe**：
  - 预训练 3 stage：① warm-up 只训 2D-Resampler（其余冻结）；② 解冻视觉编码器强化感知；③ 全量训练建跨模态桥。3D-Resampler 经轻量 SFT 阶段从 2D 扩展。
  - SFT 2 阶段：Stage-1 通用 SFT 激活知识；Stage-2 Long-CoT warm-up + 3D-Resampler。
  - **RL = 混合推理 GRPO**：支持短推理（快）/ 长推理（复杂）两模式，rollout 随机切换；GRPO（去掉 KL 与 entropy 项）。奖励 = 规则可验证（简单答案规则匹配 98% 准确）+ **RLPR**（复杂自然语言答案的概率奖励）+ 偏好奖励（RM，人类偏好数据）+ format + repetition penalty 四分量加权。整合 RLAIF-V 提升可信度。
- OpenCompass 77.0（<30B 最强）。

### MiniCPM-V 4.6（2026，GitHub 提及）
- 官方 GitHub README 列出 MiniCPM-V 4.6（最新），具体技术报告 / 数字本次未查到独立一手报告，**官方未公开（待补）**。

### 来源
- V 系统报告 arXiv: https://arxiv.org/abs/2408.01800 ｜ PDF: https://arxiv.org/pdf/2408.01800
- V4.5 arXiv: https://arxiv.org/abs/2509.18154 ｜ PDF: https://arxiv.org/pdf/2509.18154
- HF: https://huggingface.co/openbmb/MiniCPM-V-2_6 ｜ https://huggingface.co/openbmb/MiniCPM-V-4_5
- GitHub: https://github.com/OpenBMB/MiniCPM-V
- 本地：../../../sources/llm/2024/minicpm-v.pdf ｜ ../../../sources/llm/deep-dive/minicpm-v-4.5.pdf

---

## MiniCPM-o 系列（全模态，o 2.6 / o 4.5：arXiv 2604.27393）

视觉 + 语音 + 文本全模态，o 4.5 主打实时全双工（full-duplex）。

### MiniCPM-o 2.6（2025.01，HF model card）
- 端到端：**SigLip-400M + Whisper-medium-300M + ChatTTS-200M + Qwen2.5-7B，总 8B**。
- 新增实时语音对话 + 多模态直播流。OpenCompass 70.2（8B 超 GPT-4o-202405 / Gemini 1.5 Pro / Claude 3.5 Sonnet 单图）。
- config: LLM hidden 3584 / 28 层 / 28 头 / 4 KV / vocab 151,700 / ctx 32,768 = Qwen2.5-7B；64 query resampler。
- 训练 token / 配比 **官方未公开**（model card 未给）。

### MiniCPM-o 4.5（2026.04，arXiv 2604.27393）
- **总 9B 参数**，全部组件端到端可微：① 多模态编码器（流式）；② LLM 骨干 = **Qwen3-8B**；③ 语音解码器（交错语音 token 解码器 + 流匹配 decoder）。
  - 视觉：SigLIP ViT（**0.4B**），全双工流模式分辨率 448×448、否则 2240×2240；每 slice 1024 token → resampler 压到 64 token。
  - 音频：**Whisper Medium（0.3B）**，分块流式，50 feat/s → 2 层 MLP 5× 时序压缩 → 10 audio token/s。
  - 文本解码：Qwen3-8B 仅在文本域生成，每秒仅 3-4 解码步（人类语速）。
  - 语音 token 解码器：轻量 **Llama（~0.3B）**，对每个文本 token 加 LLM 隐状态（MLP reshape），文本/语音 token 时间对齐交错。
  - 流匹配 decoder：语音 token → 波形，依据 system prompt 中参考音频。
- **Omni-Flow**：把多模态输入/输出沿共享时间轴对齐，turn-based → full-duplex 连续过程。
- **训练 pipeline（基于 MiniCPM-V 4.5 预训练 ckpt）**：
  - ① 语音预训练：冻结骨干 + 视觉，只训新增语音模块（audio projector、LLM-to-speech projector、speech decoder），对齐 Whisper 特征到 LLM 空间。
  - ② 联合预训练：解冻全部，视觉/语音/全模态平衡混合；不同模态组合分配到不同 DP rank 保每步固定配比；含 proactive / full-duplex 数据，统一 next-token 目标。
  - ③ 联合 SFT：大规模指令调优 + 高质量人工标注两阶段；增广不同分辨率/帧率（0.2–0.4 MP，1–5 FPS）。
  - ④ RL：**GRPO**，accuracy reward（规则验证 + 高效 judge 模型 [SWE/verifier]）+ format reward；引入 **Kimi-K1.5 式平滑长度奖励**（前 480 步用）控 token 效率 + general RM。
- **数据**：语音（数百万小时无标注 + 专业配音对话）；视觉-语言（沿用并扩展 V4.5 数据系统，CapsFusion caption、文档 OCR relevance-aware masking、real-world CoT 重写、dense video caption）；text-only 用 MiniCPM 4.1 后训练数据；全模态全双工（大规模 web 音视频 + 人工构造任务数据，OCR 字幕去除/talking-head 检测/ASR 过滤）。
- GPU 卡时 / 集群 / 并行 / 精度 **官方未公开**（论文未给）。

### 来源
- o4.5 arXiv: https://arxiv.org/abs/2604.27393 ｜ PDF: https://arxiv.org/pdf/2604.27393
- HF: https://huggingface.co/openbmb/MiniCPM-o-2_6
- GitHub: https://github.com/OpenBMB/MiniCPM-o
- 本地：../../../sources/llm/2026/minicpm-o-4.5.pdf

---

## 全局缺口（官方未公开 / 未查到一手报告）

- 所有代次的**预训练 GPU 集群规模、总卡时、FLOPs、并行策略（TP/PP/DP/EP/ZeRO）** 基本未公开（仅 MiniCPM4 RL 段披露 64×A800；MiniCPM4 用 FP8）。
- MiniCPM3-4B、MiniCPM-V 2.6、MiniCPM-o 2.6 的**预训练 token 总量与数据配比%** 未在 model card 披露。
- MiniCPM-SALA 的具体层数/隐藏维/各阶段 token 明细未在论文正文单列。
- MiniCPM-V 4.6 暂未查到独立一手技术报告。
