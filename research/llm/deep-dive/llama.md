# Llama 家族（Meta）训练配方深挖

> 范围：LLaMA 1 / Llama 2 / Llama 2 Long / Code Llama / Llama 3·3.1·3.2（Herd of Models）/ Llama 4（Scout/Maverick/Behemoth）/ Llama Guard。
> 所有数字均抠自官方一手来源（arXiv 原文 PDF、官方 technical report、官方博客、官方 GitHub/model card）。查不到或官方未公开的，逐条标注。
> 注意：本档案不收任何第三方解读/评测聚合站。

---

## 家族演进脉络（一句话主线）

- **LLaMA 1（2023-02）**：证明"纯公开数据 + 小模型训更多 token"可达 SOTA；13B 超 GPT-3(175B)。架构三件套：Pre-norm RMSNorm + SwiGLU + RoPE。
- **Llama 2（2023-07）**：可商用，2.0T token，4K 上下文，34B/70B 引入 GQA；首次完整公开工业级 RLHF 配方（双奖励模型 + 拒绝采样 + PPO + Ghost Attention）。
- **Llama 2 Long（2023-09）**：从 Llama 2 继续预训练（约 +400B token），把有效上下文扩到 32,768；增大 RoPE base θ。
- **Code Llama（2023-08）**：从 Llama 2 继续训练 500B（70B 为 1T）代码 token；FIM 填充、长上下文（θ=1e6 扩到 100K）、Instruct（self-instruct 执行反馈）。
- **Llama 3 / 3.1（2024-04 / 2024-07）**：稠密 Transformer 8B/70B/405B；15.6T token、128K 上下文、词表 128K、GQA(8 KV heads)；放弃 MoE 与 PPO，后训练用 **SFT + 拒绝采样 + DPO 迭代 6 轮**；405B 用最多 16K×H100、4D 并行、3.8×10²⁵ FLOPs。
- **Llama 3.2（2024-09）**：视觉版 11B/90B（cross-attention adapter，drop-in 替换文本模型）+ 端侧纯文本 1B/3B（128K 上下文，蒸馏自 8B/70B）。
- **Llama 4（2025-04）**：首个**原生多模态 MoE**：Scout(17B激活/16专家/109B总/10M上下文)、Maverick(17B激活/128专家/400B总)、Behemoth(288B激活/16专家/≈2T总，教师，仍训练中)；early fusion + iRoPE + FP8 + MetaP + co-distillation；后训练改为**轻量SFT → online RL → 轻量DPO**。
- **Llama Guard（2023-12 起）**：基于 Llama-2-7B 指令微调的输入/输出安全分类器；后续 Guard 2/3/3-Vision。

### 各代关键参数对比（官方一手数字）

| 代次 | 规模 | 预训练 token | 上下文 | 注意力 | 词表 | RoPE θ | 后训练算法 | 算力（旗舰） |
|---|---|---|---|---|---|---|---|---|
| LLaMA 1 | 7B/13B/33B/65B | 1.0T（小）/1.4T（33B,65B） | 2048 | MHA | 32K | 10,000 | 仅 LLaMA-I 实验性 IFT | 65B：2048×A100-80G，~21 天 |
| Llama 2 | 7B/13B/34B*/70B | 2.0T | 4096 | 7B/13B MHA；34B/70B GQA(8 KV) | 32K | 10,000 | SFT + RLHF(拒绝采样+PPO) | 累计 3.3M A100 GPU-h，539 tCO2eq |
| Llama 2 Long | 7B/13B/34B*/70B | +约 400B（继续预训练） | 32,768 | 同 Llama 2 | 32K | 增大（>10,000） | 短指令 SFT + 少量合成长数据 | 官方未给单独算力 |
| Code Llama | 7B/13B/34B/70B ×(base/Python/Instruct) | +500B（70B +1T）代码 | 16,384 训练 / 100K 外推 | 继承 Llama 2 | 32K(+4 FIM 特殊 token) | 1,000,000 | Instruct：proprietary RLHF V5 + self-instruct + rehearsal | 官方未给总卡时 |
| Llama 3 / 3.1 | 8B/70B/405B | 15.6T | 8K→128K | GQA，8 KV heads | 128K（tiktoken 100K+28K） | 500,000 | SFT + 拒绝采样 + DPO，迭代 6 轮 | 405B：最多 16K×H100，BF16，3.8×10²⁵ FLOPs |
| Llama 3.2 | 1B/3B（文本）；11B/90B（视觉） | 1B/3B：最多 9T（剪枝+蒸馏）；视觉用 3.1 文本 backbone | 128K | GQA | 128K | 500,000 | 蒸馏 + SFT/DPO | 官方未给完整卡时 |
| Llama 4 Scout | 17B 激活 / 109B 总 / 16 专家 | 整体混合 >30T（文本+图+视频） | 10M（pre/post 训 256K） | iRoPE（交错 NoPE + RoPE） | 官方未明确给数字 | 部分层 RoPE，部分层 NoPE | 轻量SFT→online RL→轻量DPO | 与 Maverick 共享，FP8 |
| Llama 4 Maverick | 17B 激活 / 400B 总 / 128 专家 + 1 共享 | >30T | 官方未单列 | 交替 dense / MoE 层 | — | iRoPE | 轻量SFT→online RL→轻量DPO | FP8 |
| Llama 4 Behemoth | 288B 激活 / ≈2T 总 / 16 专家 | >30T | — | MoE | — | iRoPE | 轻量SFT(剪 95% 数据)→大规模 RL | FP8，32K GPU，390 TFLOPs/GPU |

\* Llama 2 34B 已训练但未发布权重。

---

## LLaMA 1（2023-02）

来源：arXiv 2302.13971，本地 `2023/files/llama.pdf`。

### 架构细节
- 四档：6.7B / 13.0B / 32.5B / 65.2B（Table 2）。
- 维度 / 头 / 层（Table 2）：
  - 7B：dim 4096，32 heads，32 layers，LR 3.0e-4。
  - 13B：dim 5120，40 heads，40 layers，LR 3.0e-4。
  - 33B：dim 6656，52 heads，60 layers，LR 1.5e-4。
  - 65B：dim 8192，64 heads，80 layers，LR 1.5e-4。
- 注意力：标准 MHA（未用 GQA）。
- 激活：**SwiGLU**，FFN 隐藏维用 (2/3)·4d（取代 PaLM 的 4d），即约 (8/3)d。
- norm：**Pre-normalization + RMSNorm**（输入做归一，灵感取自 GPT-3）。
- 位置编码：去掉绝对位置编码，改 **RoPE**（每层加），base θ=10,000。
- tokenizer：**BPE（SentencePiece）**，词表约 32K；数字拆成单个 digit，未知 UTF-8 回退到 byte。
- 上下文：2048。

### 预训练数据（Table 1，约 1.4T token）
- CommonCrawl 67%（5 个 dump 2017–2020，CCNet pipeline）；C4 15%；GitHub 4.5%（仅 Apache/BSD/MIT）；Wikipedia 4.5%（2022 年 6–8 月，20 种语言）；Books（Gutenberg + Books3）4.5%；ArXiv 2.5%；StackExchange 2%。
- 总 token 约 1.4T；多数数据每 token 仅用一次，Wikipedia 与 Books 约 2 个 epoch。

### 数据处理 pipeline
- CommonCrawl：CCNet 行级去重 + fastText 语言识别去非英文 + n-gram LM 质量过滤；另训练线性分类器判定"是否像 Wikipedia 引用页"，丢弃非引用页。
- C4：自带去重 + 语言识别，质量过滤靠启发式（标点、词句数）。
- GitHub：按 line length / 字母数字比例过滤，正则去 boilerplate，文件级精确去重。
- Books：书级去重（>90% 重叠去掉）。
- ArXiv：去掉首节前内容与参考文献，去注释、内联展开宏。

### 数据配比 / 课程
- 固定配比（Table 1），无明确退火/课程阶段。

### 训练细节
- 优化器：AdamW，β1=0.9，β2=0.95；cosine LR（最终 LR = 峰值 10%）；weight decay 0.1；grad clip 1.0；warmup 2000 步；batch size 4M token。
- 算力：65B 在 **2048×A100-80GB** 上约 380 token/sec/GPU，1.4T token 约 **21 天**；用 xformers 高效 causal attention + 激活重计算（手写 backward）+ 模型/序列并行 + 计算通信重叠。

### SFT / RL
- 无正式后训练。仅做了一个实验性指令微调 LLaMA-I（仿 Chung et al. Flan 协议），MMLU(5-shot) 达 68.9%。无 RLHF。

### 来源
- url: https://arxiv.org/abs/2302.13971 ；pdf: https://arxiv.org/pdf/2302.13971
- 本地：`../../../sources/llm/2023/llama.pdf`

---

## Llama 2 / Llama 2-Chat（2023-07）

来源：arXiv 2307.09288，本地 `2023/files/llama-2.pdf` 与 `themes/post-training/files/llama2.pdf`；官方 MODEL_CARD（github.com/meta-llama/llama）。

### 架构细节
- 规模：7B / 13B / 34B（未发布权重）/ 70B；与 Llama 1 相比主要改动 = 上下文翻倍 + GQA。
- 上下文：**4096**。
- 注意力：7B/13B 用 MHA；**34B/70B 用 GQA**（70B：8 KV heads，dim 8192，80 层，64 heads，FFN 28672——与 Llama 3 70B 同维，官方 params.json/MODEL_CARD 确认 GQA）。
- 激活/ norm / 位置：沿用 RMSNorm + SwiGLU + RoPE（θ=10,000）。
- tokenizer：与 Llama 1 相同 BPE(SentencePiece)，词表 **32K**。

### 预训练数据
- **2.0T token**（比 Llama 1 多 40%），全公开数据，**不含 Meta 产品/服务数据**。
- 对最"事实性"的来源做上采样以增知识、抑幻觉；移除已知含大量个人信息的站点。
- 数据知识截止 2022-09（tuning 数据到 2023-07）。

### 数据处理 pipeline
- 比 Llama 1 更强的清洗 + 更新 data mix；官方未在正文给精确去重/分类器阈值（"more robust data cleaning"）。

### 数据配比 / 训练阶段
- 单阶段预训练，全程 global batch 4M token；未提退火（annealing）。

### 训练细节
- 优化器：AdamW，β1=0.9，β2=0.95，eps=1e-5；cosine LR（warmup 2000 步，衰减到峰值 10%）；weight decay 0.1；grad clip 1.0。
- 峰值 LR：7B/13B 3.0e-4；34B/70B 1.5e-4。
- 硬件：Meta RSC（NVIDIA Quantum InfiniBand，400W）+ 生产集群（RoCE/commodity ethernet，350W），均 A100，200 Gbps 端点。结论：RoCE 在 ≤2000 GPU 可几乎媲美 InfiniBand。
- 算力（Table 2）：累计 **3,311,616 A100-80GB GPU-h**（7B 184,320；13B 368,640；34B 1,038,336；70B 1,720,320），总碳排 **539 tCO2eq**（100% 被 Meta 抵消）。
- 稳定性：2T token 后训练损失仍未饱和。

### SFT 细节
- 起步用公开指令数据 bootstrap，后聚焦"少而精"：最终只用 **27,540 条**自有高质量标注（"Quality Is All You Need"），不含 Meta 用户数据。
- SFT 超参：cosine LR 初值 2e-5，weight decay 0.1，batch size 64，序列长 4096，2 个 epoch；拼接所有 prompt+answer，仅在 answer token 上算 loss（prompt token loss 置零）。

### RL / 对齐细节
- **双奖励模型**：Helpfulness RM + Safety RM（均从 chat checkpoint 初始化，回归头取代 next-token 头）。
- 偏好数据：自采 **1,418,091** 条 Meta（Safety+Helpfulness）二元比较；加开源数据后总 **2,919,326** 条（Anthropic HH 122,387+43,966、OpenAI Summarize 176,625、WebGPT 13,333、StackExchange 1,038,480、Stanford SHP 74,882、Synthetic GPT-J 33,139）。4 档偏好强度（significantly/better/slightly/negligibly）。
- RM loss：binary ranking loss + **margin 项 m(r)**（按偏好强度的离散函数），数据规模上来后边际收益递减。
- RM 训练：1 epoch；70B RM 最大 LR 5e-6，其余 1e-5；cosine 衰减到 10%；warmup 3%；有效 batch 512 pairs（1024 行）。
- RM 数据配比：Helpfulness RM = 全 Meta Helpful + 等比例 Meta Safety/开源；Safety RM = 全 Meta Safety + Anthropic Harmless + Helpful/开源按 90/10。
- **迭代 RLHF V1–V5**：V4 之前仅 **Rejection Sampling fine-tuning**（从 K 个样本取最高 RM 分），V4 之后叠加 **PPO**（在拒绝采样 checkpoint 上）。
- 拒绝采样仅用最大 70B 做，小模型在 70B 拒绝采样数据上微调（**大模型→小模型蒸馏**）；后期纳入所有历史迭代的 top 样本以缓解遗忘；最优采样温度随迭代漂移（RLHF 后 T∈[1.2,1.3]）。
- PPO：reward = 安全/有用分段组合 Rc，安全阈值 0.15（precision 0.89 / recall 0.55），whiten + logit；KL 罚 β：7B/13B 0.01，34B/70B 0.005。AdamW，const LR 1e-6，weight decay 0.1，grad clip 1.0，batch 512，clip 0.2，mini-batch 64；训练 200–400 iter；70B 每 iter ≈330 s；用 FSDP，生成阶段把权重 consolidate 到节点再释放以避免约 20× 慢。
- 安全：Safety SFT + Safety RLHF + **Safety Context Distillation**；红队。
- **Ghost Attention (GAtt)**：把系统指令合成进多轮对话训练数据，损失置零中间轮，使系统指令在 20+ 轮保持一致（RLHF V3 后应用）。

### 来源
- url: https://arxiv.org/abs/2307.09288 ；pdf: https://arxiv.org/pdf/2307.09288
- model card: https://github.com/meta-llama/llama/blob/main/MODEL_CARD.md
- 本地：`../../../sources/llm/2023/llama-2.pdf`、`themes/post-training/files/llama2.pdf`

---

## Llama 2 Long（Effective Long-Context Scaling，2023-09）

来源：arXiv 2309.16039，本地 `2023/files/llama-2-long.pdf`。

### 关键细节
- 目标：把 Llama 2 有效上下文扩到 **32,768** token。
- 方法：从 Llama 2 **继续预训练（continual pretraining）**，约额外 **400B token**，对长文本上采样。
- 位置编码：**调整 RoPE base 频率（增大 θ）** 以建模更长依赖（论文分析 RoPE 在长上下文的局限并改进）。
- 关键发现：① 预训练里"大量长文本"不是关键；② 长上下文继续预训练比从头长序列预训练更高效且同样有效。
- 指令微调：仅用短指令数据 + 少量合成长数据（无需人工长标注）；70B 变体在长上下文任务套件超 gpt-3.5-turbo-16k。
- 官方未单列该工作的单独算力卡时。

### 来源
- url: https://arxiv.org/abs/2309.16039 ；pdf: https://arxiv.org/pdf/2309.16039
- 本地：`../../../sources/llm/2023/llama-2-long.pdf`

---

## Code Llama（2023-08，含 70B 2024-01）

来源：arXiv 2308.12950，本地 `2023/files/code-llama.pdf`。

### 架构 / 规模
- 三变体 ×4 尺寸：**Code Llama / Code Llama-Python / Code Llama-Instruct**，7B/13B/34B/70B。
- 均**从 Llama 2 同尺寸权重初始化**继续训练（不是从零）。
- 7B/13B/70B 训练含 **infilling（FIM）目标**；34B 无 FIM。tokenizer 沿用 Llama/Llama 2，并加 **4 个 FIM 特殊 token**（prefix/middle/suffix 开始 + 填充结束）。
- 上下文：LCFT 阶段训练序列 **16,384**，可外推到 **100,000**。

### 数据（Table 1）
- 初始代码训练 **500B token**（Code Llama 70B 为 **1T**）：
  - Code Llama 500B：Code 85%（2.03 epoch，859 GB）、自然语言相关代码 8%（1.39 epoch，78 GB）、自然语言 7%（0.01 epoch，3.5 TB）。
  - Code Llama-Python 额外 **100B**：Python 75%（3.69 epoch，79 GB）、Code 10%、NL 相关代码 10%、NL 5%。
- 近去重的公开代码数据；BPE 同 Llama 2。

### 训练细节
- AdamW，β1=0.9，β2=0.95；cosine（1000 warmup，最终 LR = 峰值 1/30）；batch 4M token（序列 4096）。
- LR：7B 3e-4，13B/34B 1.5e-4；Python 微调初值 1e-4；Instruct batch 524,288 token、共约 **5B token**。
- **FIM**：字符级切 prefix/middle/suffix，应用概率 0.9，PSM 与 SPM 各半；抑制 SentencePiece 隐式前导空格。
- **长上下文微调（LCFT）**：LR 2e-5，序列 16,384，**RoPE base θ 从 10,000 调到 1,000,000**（改 base period 而非线性下采样）；batch 7B/13B 2M、34B 1M token；默认 10,000 步（34B 11,000、7B 3,000）。
- Code Llama 70B：训练 token 翻倍（1T 而非 500B），带 FIM；Instruct 70B 从 Code Llama-Python 70B 训出。

### Instruct 微调（RL/对齐）
- 三类数据：① **proprietary 指令数据**——直接复用 Llama 2 的 **"RLHF V5"**（含数千 SFT + 数百万拒绝采样，含 Helpfulness+Safety）；② **self-instruct（执行反馈）**——Llama 2 70B 生成 62,000 道面试题→去重到约 52,000→Code Llama 7B 生成单测 + 10 个 Python 解→跑单测取首个通过者，得约 **14,000** 三元组；③ **rehearsal**——掺 6% 代码 + 2% 自然语言防遗忘。

### 评测要点（Table 2）
- HumanEval pass@1：Code Llama-Instruct 70B 67.8%，34B 48.8%（base）；MBPP 最高 65.6%（Python 70B）。Code Llama-Python 7B 在 HumanEval/MBPP 超 Llama 2 70B。

### 来源
- url: https://arxiv.org/abs/2308.12950 ；pdf: https://arxiv.org/pdf/2308.12950
- 官方博客：https://ai.meta.com/blog/code-llama-large-language-model-coding/（本地 `2023/files/code-llama-meta-blog.md`）
- 本地：`../../../sources/llm/2023/code-llama.pdf`

---

## Llama 3 / 3.1（The Llama 3 Herd of Models，2024-07）

来源：arXiv 2407.21783（v3，2024-11-23），本地 `themes/post-training/files/llama3-herd.pdf`（另有 `themes/architecture/files/llama3.pdf`、`themes/ai-infra/files/llama3-2407.21783.pdf` 同篇）。论文所有结果均为 **Llama 3.1** 模型。

### 架构细节（Table 3）
| | 8B | 70B | 405B |
|---|---|---|---|
| Layers | 32 | 80 | 126 |
| Model Dimension | 4,096 | 8,192 | 16,384 |
| FFN Dimension | 14,336 | 28,672 | 53,248 |
| Attention Heads | 32 | 64 | 128 |
| Key/Value Heads | 8 | 8 | 8 |
| Peak LR | 3×10⁻⁴ | 1.5×10⁻⁴ | 8×10⁻⁵ |
| Activation | SwiGLU | | |
| Vocab | 128,000 | | |
| Positional | RoPE (θ = 500,000) | | |

- **标准稠密 Transformer**（刻意不用 MoE，为训练稳定性 / 管理复杂度）。
- **GQA，8 KV heads**；新增**文档掩码**（同一序列内不同文档间不互相注意——长序列继续预训练时重要）。
- tokenizer：**128K 词表** = tiktoken 100K + 28K 非英文 token；英文压缩率从 3.17 → 3.94 字符/token。
- RoPE base θ = **500,000**（支持长上下文）。
- 405B 选 126 层是按 scaling law 在 3.8×10²⁵ FLOPs 预算下的近 compute-optimal 尺寸。

### 预训练数据
- **约 15T 多语言 token**（旗舰 405B 实训 **15.6T**），知识截止 2023 年底；移除大量 PII 域与成人内容域。
- 最终 data mix（按 token）：**通用知识约 50%、数学与推理 25%、代码 17%、多语言 8%**。

### 数据处理 pipeline
- **PII / 安全过滤**：按 Meta 安全标准 + 成人内容黑名单去域。
- **抽取**：自研 HTML parser（精度优于第三方 article 抽取器）；保留数学/代码结构，保留 image alt（数学常以图片 + alt 给出）；**去掉 markdown 标记**（对 web 训练有害）。
- **去重**：① **URL 级**（保留每 URL 最新版）；② **文档级全局 MinHash**；③ **行级**（仿 ccNet，30M 文档/桶内出现 >6 次的行删除）。
- **启发式过滤**：duplicated n-gram 覆盖率去重复行；"dirty word" 计数去成人站；token 分布 KL 散度去异常 token 文档。
- **基于模型的质量分类器**：fasttext（判定"是否会被 Wikipedia 引用"）+ Roberta-based（在 Llama 2 预测上训练）；用 **DistilRoberta** 给文档打质量分。
- **代码/推理专项**：code 与 reasoning 分类器均为在 Llama 2 标注 web 上训练的 DistilRoberta，domain-specific HTML 抽取 + prompt tuning。
- **多语言**：fasttext 语言识别分 **176 语言**；逐语言文档级/行级去重 + 多语言 Llama 2 分类器做质量排序。
- **data mix 确定**：知识分类（下采样过表征类，如艺术娱乐）+ scaling law 实验（小模型预测大模型表现）。

### 数据配比 / 阶段 / 退火
- **三阶段预训练**：① 初始预训练；② 长上下文预训练；③ **退火（annealing）**。
- 训练中调 mix：增非英文比例、上采样数学数据、后期加更新 web 数据推进知识截止、下采样后识别的低质子集。
- **长上下文**：最终阶段把 8K **分 6 个阶段**逐步扩到 128K，约用 **800B token**；扩展依据短上下文性能恢复 + needle-in-haystack 完美。
- **退火**：最后 **40M token** 把 LR 线性退到 0，维持 128K，上采样极高质量源；对 checkpoint 做 **Polyak 平均**得最终模型。退火把 8B 在 GSM8k/MATH 验证集分别提升 24.0%/6.4%，但对 405B 几乎无效。

### 训练细节（infra / 并行）
- **算力**：405B 用最多 **16K H100**（每卡 700W、80GB HBM3，Grand Teton 平台，每服务器 8 GPU + 2 CPU，机内 NVLink），MAST 调度；峰值 **3.8×10²⁵ FLOPs**（约 Llama 2 最大版的 50×）。
- 存储：Tectonic 文件系统，240 PB / 7,500 SSD 服务器，持续 2 TB/s、峰值 7 TB/s；每 GPU checkpoint 1MB–4GB。
- 网络：405B 用 **RoCE**（Arista 7800 + Minipack2，三层 Clos，24K GPU，pod 3,072 GPU 全 bisection，aggregation 层 1:7 oversubscription）；小模型用 **Nvidia Quantum2 InfiniBand**；均 400 Gbps。自研 E-ECMP 负载均衡 + deep-buffer 交换机，无需 DCQCN。
- **4D 并行 = [TP, CP, PP, DP(FSDP)]**（按网络带宽/延迟排序，TP 在机内最内层）。各阶段配置（Table 4）：
  - 8,192 GPU：TP8/CP1/PP16/DP64，seq 8,192，16M token/batch，430 TFLOPs/GPU，**MFU 43%**。
  - 16,384 GPU：TP8/CP1/PP16/DP128，seq 8,192，16M，400 TFLOPs，**41%**。
  - 16,384 GPU（长上下文）：TP8/**CP16**/PP16/DP8，seq **131,072**，16M，380 TFLOPs，**38%**。
- 精度 **BF16**；数值稳定：FSDP 中 FP32 梯度累积 + FP32 reduce-scatter；自研 **NCCLX**（NCCL fork）；自研 PP 调度（可调 N 微批、首末 stage 各减一层均衡）；CP 用 all-gather based（借 GQA 使 K/V 通信小）。
- **优化器/schedule**：AdamW，峰值 LR 8×10⁻⁵，linear warmup 8,000 步，cosine 衰减到 8×10⁻⁷ 历经 1,200,000 步。
- **batch 渐增**：初始 4M token / seq 4,096 → 252M token 后翻倍到 8M / seq 8,192 → 2.87T token 后再翻到 16M。"few loss spikes，无需干预"。
- 可靠性：54 天快照内 **466 次中断**（47 计划 + 419 意外，约 78% 硬件相关，GPU 占意外 58.7%），>90% 有效训练时间，仅 3 次需人工。

### 后训练（Llama 3 后训练流程）
- 整体：在预训练 checkpoint 上做**多轮**（共 **6 轮**）；每轮 = 训 RM → 拒绝采样 → SFT → DPO。
- **明确弃用 PPO，选 DPO**：DPO 大模型更省算力、在 IFEval 等更好。
- **RM**：在预训练 checkpoint 上训；目标同 Llama 2 但**去掉 margin 项**（数据上来后收益递减）；支持第三个 "edited response"（edited > chosen > rejected）；多回答拼一行训练。
- **SFT**：用 RM 对人工 prompt 做拒绝采样（K 典型 10–30，取 RM 最高分）+ 合成数据，标准 cross-entropy（mask prompt token loss）；最大模型 LR 1e-5，训 8.5K–9K 步。用 **PagedAttention** 使拒绝采样吞吐 >2×。
- **DPO**：LR 1e-5，**β=0.1**；主要用最近一轮最强模型采的偏好数据；两项改动 = ① **mask 格式 token**（header/termination）出 loss；② 加 **NLL 正则**（chosen 序列，系数 0.2）。
- **模型平均**：RM/SFT/DPO 各阶段对不同数据/超参的模型做平均。
- 偏好数据统计（Table 6）：General English 81.99% / Coding 6.93% / Multilingual 5.19% / Reasoning&tools 5.89%。SFT 数据（Table 7）：General English 52.66% / Code 14.89% / Reasoning&tools 21.19% / Exam-like 8.14% / Multilingual 3.01% / Long context 0.11%（但平均 38,135 token）。
- 数据清洗：规则去过度 emoji/感叹号/道歉腔；Llama 3 8B 微调成 topic 分类器；RM 分 top quartile + Llama-as-judge 双信号取质量；Instag 难度标注；**RoBERTa 语义去重**（簇内按 质量×难度 贪心选）。

### 能力专项（后训练）
- **代码**：分支主预训练训 **code expert**（约 1T token、>85% 代码，末段 LCFT 到 16K，再 SFT/DPO，专做代码拒绝采样）；合成 **>2.7M** SFT 样本：① 执行反馈（约 1M 对话，静态分析 + 单测，约 20% 初错后自纠）；② 编程语言翻译（补冷门语言）；③ backtranslation（约 1.2M，文档/解释↔代码）；model-as-judge 双标准（正确性+风格）取满分 2。
- **多语言**：训 **multilingual expert**（分支后在 90% 多语言 token 上继训）；多语言 SFT 来源占比 = 人工 2.4% / 其他 NLP 任务 44.2% / 拒绝采样 18.8% / 翻译推理数据 34.6%；尽量不用机翻（仅例外翻译合成定量推理数据）。
- **数学与推理**：源 pre-train 数学数据转 QA；步进式推理 trace 用 Llama 3 生成 + 按答案过滤 + 自验证；训练 outcome RM + **stepwise PRM** 过滤错误中间步；难题用 **MCTS + stepwise RM**；交错 code+text 推理用执行反馈过滤。
- **长上下文**：SFT 混 **0.1%** 合成长上下文数据（QA / 分层摘要 / 代码仓推理，分 16K/32K/64K/128K）即可平衡长短；**DPO 仅用短上下文数据**（步数少不伤长）。
- **工具**：训用 **Brave Search / Python interpreter / Wolfram Alpha**；靠人工标注 + 偏好（message 级），**不做拒绝采样**（无增益）；zero-shot function calling 用 mining The Stack 的真实函数 ground；含单步/多步/嵌套/并行/多轮 function calling。
- **事实性**：知识探测——从预训练数据抽片段→生成事实问→采样回答→Llama 3 判正确性 + 信息量→对"一致自信但错"的生成造拒答；"know what it knows"。
- **可控性**：系统 prompt 控长度/格式/语气/persona，喂进 RM/拒绝采样/SFT/DPO。

### Llama 3.1 发布要点（官方博客补充）
- 8B/70B/405B 均 128K 上下文、支持 8 种语言；405B >16,000 H100 训练。
- 推理量化 **BF16 → FP8**，405B 可单服务器节点部署。
- 许可放开：允许用 Llama 输出（含 405B）做合成数据生成 / 蒸馏改进其他模型。

### 来源
- url: https://arxiv.org/abs/2407.21783 ；pdf: https://arxiv.org/pdf/2407.21783
- github: https://github.com/meta-llama/llama-models
- 博客：https://ai.meta.com/blog/meta-llama-3-1/ 、https://ai.meta.com/blog/meta-llama-3/
- 本地：`themes/post-training/files/llama3-herd.pdf`、`themes/architecture/files/llama3.pdf`、`themes/ai-infra/files/llama3-2407.21783.pdf`

---

## Llama 3.2（2024-09，视觉 + 端侧）

来源：官方博客 https://ai.meta.com/blog/llama-3-2-connect-2024-vision-edge-mobile-devices/ ，本地 `2024/files/meta-llama-3-2-blog.md`。

### 模型与架构
- **视觉**：11B、90B（图像理解，超 Claude 3 Haiku 级闭源模型）。架构 = 在对应 Llama 3.1 文本 backbone 上加**视觉 adapter（cross-attention 层）**，可 **drop-in 替换**对应纯文本模型（与 Llama 3 论文第 7 章组合式视觉路线一致）。
- **端侧纯文本**：1B、3B，**128K 上下文**；为边缘/移动端设计，高通/联发科首日支持、Arm 优化。

### 训练方法（官方博客层级）
- 1B/3B 用**剪枝 + 知识蒸馏**：从 Llama 3.1 8B/70B 蒸馏（博客明确 1B/3B 为轻量模型，借大模型 logits 蒸馏）。
- 官方博客未给完整卡时 / token 数 / 并行细节（**官方未公开细粒度配方**，需查 HF model card 补充 token 数）。

### 安全
- 配套 **Llama Guard 3**（含视觉版，arXiv 2411.10414）。

### 工具链
- torchtune 微调、torchchat 本地部署；首个官方 **Llama Stack** 发行版（单节点经 Ollama，端侧经 PyTorch ExecuTorch）。

### 来源
- url: https://ai.meta.com/blog/llama-3-2-connect-2024-vision-edge-mobile-devices/
- github: https://github.com/meta-llama/llama-stack
- 本地：`../../../sources/llm/2024/meta-llama-3-2-blog.md`

---

## Llama 4（2025-04，原生多模态 MoE）

来源：官方博客 https://ai.meta.com/blog/llama-4-multimodal-intelligence/（2025-04-05，"12 minute read"），本地 `themes/architecture/files/llama4-blog.html`。
> 截至本档案，Llama 4 尚无 arXiv technical report，以下全部抠自官方博客；很多并行/数据细节官方未公开。

### 架构细节
- **首个 MoE Llama**，**原生多模态（early fusion）**：文本 + 视觉 token 统一进单一 backbone 联合预训练。
- **Llama 4 Scout**：17B 激活 / **109B 总** / **16 专家**；单张 H100（Int4 量化）可部署；上下文 **10M**（pre/post 训均 256K）。
- **Llama 4 Maverick**：17B 激活 / **400B 总** / **128 routed 专家 + 1 共享专家**；**交替 dense 与 MoE 层**；每 token 走共享专家 + 128 中的 1 个 routed 专家；单 H100 DGX host 可跑。
- **Llama 4 Behemoth**：**288B 激活 / 近 2T 总 / 16 专家**；teacher，仍训练中。
- **iRoPE 架构**：interleaved attention（"i"=交错），**部分层无位置编码（NoPE）**，多数层用 RoPE；推理时对 attention 做 **temperature scaling** 增强长度泛化；目标"近无限"上下文。
- 视觉编码器：基于 **MetaCLIP**，与 frozen Llama 协同单独训练；预训练最多 48 图，post-train 测到 8 图良好。
- **MetaP**：新训练技术，可靠设定 per-layer LR 与初始化 scale，超参在不同 batch/宽/深/token 间可迁移。

### 预训练数据
- **整体混合 >30T token**（文本+图+视频），是 Llama 3 预训练混合的 **2 倍多**。
- 多语言：预训练 **200 种语言**（>100 种各 >10 亿 token），多语言 token 是 Llama 3 的 **10×**。
- "mid-training" 阶段做长上下文扩展（专用数据集），解锁 Scout 的 10M 上下文。

### 训练细节（infra / 精度）
- **FP8 精度**预训练；**Behemoth 用 FP8 + 32K GPU，达 390 TFLOPs/GPU**。
- **co-distillation**：Maverick 从 Behemoth 共蒸馏；新 **distillation loss 动态加权 soft/hard target**；预训练期共蒸馏摊薄 teacher forward 成本。
- TP/PP/DP/EP/ZeRO 等具体并行配置、global batch、各专家路由细节、无辅助损失与否——**官方未公开**。

### 后训练 / RL
- **新流程：轻量 SFT → online RL → 轻量 DPO**（区别于 Llama 3 的 SFT+RS+DPO）。
- 关键经验：SFT/DPO 会过约束、限制 online RL 探索；故用 Llama-as-judge 去掉 **>50% 标为 easy** 的数据，仅在剩下难集上轻量 SFT。
- **continuous online RL**：训练与"用模型过滤、仅保留中-难 prompt"交替；多模态 online RL 选难 prompt 得阶跃提升；最后轻量 DPO 修边角。
- **Behemoth 后训练**：剪 **95% SFT 数据**（小模型剪 50%）；轻量 SFT → **大规模 RL**；RL 配方 = pass@k 采难 prompt + 难度递增课程 + 动态过滤 0 advantage prompt + 多能力混 batch + 多系统指令采样。
- **RL infra**：为 2T 参数模型重构 RL infra，优化 MoE 并行，**全异步 online RL 框架**，模型灵活分配到不同 GPU，训练效率较前代 **约 10×**。

### 安全
- 系统级：Llama Guard、Prompt Guard、CyberSecEval；红队含 **GOAT**（Generative Offensive Agent Testing，多轮自动化对抗）。

### 来源
- url: https://ai.meta.com/blog/llama-4-multimodal-intelligence/
- 本地：`../../../sources/llm/themes/architecture/llama4-blog.html`

---

## Llama Guard（2023-12，及 2/3 系列）

来源：arXiv 2312.06674，本地 `themes/post-training/files/llama-guard.pdf`。

### 模型与任务
- 基座 **Llama-2-7b 指令微调**（选最小尺寸以降推理/部署成本）。
- 两类任务：**prompt classification**（用户输入是否违规）与 **response classification**（模型回答是否违规）——首个明确把两者拆开的工作；仅靠指令措辞切换，单模型完成。
- 输出格式：首 token "safe"/"unsafe"（均为 SentencePiece 单 token，可读出概率分），unsafe 则换行列违规类别（字母 + 1-based 序号）；支持二分类/多标签/1-vs-all。

### 安全分类法（taxonomy，6 类）
- Violence & Hate、Sexual Content、Guns & Illegal Weapons、Regulated/Controlled Substances、Suicide & Self-Harm、Criminal Planning。taxonomy 写进 prompt，推理期可零样本/少样本调整扩展。

### 数据与训练
- 数据：取 Anthropic harmlessness 人类偏好的首条 prompt，用内部 Llama checkpoint 生成 cooperating/refusing 回答，**in-house 红队**按 taxonomy 标 4 标签（prompt-category/response-category/prompt-label/response-label）；清洗后共 **13,997** 条；3:1 切分微调/评测。类别分布见原文 Table 1（Safe prompt 7228 / Criminal Planning 3915 等）。
- 训练：**8×A100-80GB 单机**，batch 2，序列 4096，model parallel 1，LR **2×10⁻⁶**，**500 步 ≈1 epoch**。
- 数据增强：随机丢未违规类别；丢全部违规类别并改标签为 safe；打乱类别序号防格式记忆。

### 评测（AUPRC，Table 2，zero-shot 适配目标 taxonomy）
- 自有测试集 prompt 0.945 / response 0.953；OpenAI Mod 0.847（vs OpenAI API 0.856）；ToxicChat 0.626（优于 OpenAI 0.588 / Perspective 0.532）。few-shot 在 OpenAI Mod 升到 0.872。
- 开源权重，可作 RLHF / agent 流水线输入输出过滤器。后续迭代 **Llama Guard 2 / 3 / 3-Vision**（与 Llama 3.x、4 配套；3-Vision = arXiv 2411.10414）。

### 来源
- url: https://arxiv.org/abs/2312.06674 ；pdf: https://arxiv.org/pdf/2312.06674
- code: https://github.com/meta-llama/PurpleLlama/tree/main/Llama-Guard
- 本地：`../../../sources/llm/themes/post-training/llama-guard.pdf`

---

## 官方未公开 / 未查到的缺口（gaps）

- **Llama 2 数据处理 pipeline 细节**：精确去重算法/质量分类器阈值正文未给（仅"more robust data cleaning"）。
- **Llama 2 Long / Code Llama 单独算力卡时**：论文未单列 GPU-hours / FLOPs。
- **Llama 3.2（1B/3B/11B/90B）细粒度配方**：博客未给 token 数、并行、卡时；需查 HF official model card 补（本档案未抓 HF config 原文）。
- **Llama 4 全面细节**：无 arXiv 技术报告。并行策略（TP/PP/DP/EP/ZeRO 具体）、global batch、各专家路由/容量、是否无辅助损失、Scout/Maverick/Behemoth 各自 token 数、RL 算法名（PPO/GRPO/其它，仅说"online RL"）、reward 形式、Behemoth 总参精确值（"近 2T"）——**官方均未公开**。
- **Llama 3 各代 8B/70B 单独 FLOPs / 卡时**：论文主要给 405B 的 infra 数字，8B/70B 仅说"用相似 recipe"。
