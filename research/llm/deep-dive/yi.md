# Yi 家族（零一万物 / 01.AI）训练配方深挖

> 本文只采一手官方来源：arXiv 原文、官方 technical report、官方 GitHub / Hugging Face 官方组织页（`01-ai`）的 model card / config.json。每个数字尽量标注出处页/字段。官方未公开的项明确写"官方未公开"。

## 家族演进脉络

- **2023-11 Yi-6B / Yi-34B（base）**：从零训练的中英双语稠密 Transformer，预训练 3.1T token，4K 上下文。同期放出 200K 长上下文版（Yi-6B/34B-200K）与 chat 版。数据工程优先路线（"quality over quantity"）。
- **2024-01 Yi-VL-6B / Yi-VL-34B**：基于 Yi-6B/34B-Chat + CLIP ViT-H/14 的视觉语言模型，LLaVA 式三段训练。
- **2024-03 Yi-9B**：用 depth upscaling（深度复制）把 Yi-6B（32 层）扩到 48 层，再继续预训练约 0.8T token；正式技术报告 *Yi: Open Foundation Models by 01.AI*（arXiv 2403.04652）同月发布，把以上全部模型收进一篇报告。
- **2024-05 Yi-1.5（6B/9B/34B）**：在 Yi base 上**继续预训练 500B token** + **3M SFT 样本**，强化 code/math/reasoning/指令跟随。架构与 Yi base 完全一致（HF `LlamaForCausalLM`）。
- **2024-09 Yi-Coder（1.5B/9B）**：基于 Yi-9B / 一个 1.5B 底座，**继续预训练 2.4T 代码 token**，52 种语言，128K 上下文。
- **2024-10 Yi-Lightning（闭源 API 旗舰，有独立技术报告 arXiv 2412.01253）**：增强型 MoE（细粒度专家分割 + PEP 负载均衡 + 跨层 KV 共享 + 滑窗/全注意力混合），多阶段预训练 + 两阶段 SFT + 两阶段（offline/online）DPO。Chatbot Arena 总榜第 6（Arena 1287）。**只开放 API，不放权重**，故架构规模（总参/激活/层数/专家数）官方未公开。

### 各代关键参数对比（仅列官方披露数字）

| 模型 | 类型 | 隐藏维 | 层数 | Q头/KV头(GQA) | FFN中间维 | vocab | 上下文 | rope_theta | 预训练token | 出处 |
|---|---|---|---|---|---|---|---|---|---|---|
| Yi-6B | dense base | 4096 | 32 | 32 / 4 | 11008 | 64000 | 4K(可扩32K) | 5e6 | 3.1T | report Table1 + HF config |
| Yi-34B | dense base | 7168 | 60 | 56 / 8 | 20480 | 64000 | 4K(可扩32K) | 5e6 | 3.1T | report Table1 + HF config |
| Yi-6B-200K | dense base | 4096 | 32 | 32 / 4 | 11008 | 64000 | 200K | (200K版1e7) | 3.1T+~5B长文 | HF config / report §7.1 |
| Yi-34B-200K | dense base | 7168 | 60 | 56 / 8 | 20480 | 64000 | 200K | 1e7 | 3.1T+~5B长文 | HF config / report §7.1 |
| Yi-9B | dense base | 4096 | 48 | 32 / 4 | 11008 | 64000 | 4K | **1e4** | Yi-6B继续~0.8T | report §7.3 + HF config |
| Yi-1.5-6B | dense base | 4096 | 32 | 32 / 4 | 11008 | 64000 | 4K | 5e6 | Yi base + 500B | HF config + GitHub README |
| Yi-1.5-9B | dense base | 4096 | 48 | 32 / 4 | 11008 | 64000 | 4K(32K变体) | 5e6 | Yi base + 500B | HF config |
| Yi-1.5-34B | dense base | 7168 | 60 | 56 / 8 | 20480 | 64000 | 4K | 5e6 | Yi base + 500B | HF config |
| Yi-Coder-1.5B | dense base | 2048 | 24 | 16 / 16(MHA) | 5504 | 64000 | 128K | 1e7 | +2.4T 代码 | HF config + blog |
| Yi-Coder-9B | dense base | 4096 | 48 | 32 / 4 | 11008 | 64000 | 128K | 1e7 | Yi-9B + 2.4T 代码 | HF config + blog |
| Yi-VL-6B / 34B | VLM | (同 6B/34B chat) | — | — | — | — | — | — | — | report §7.2 |
| Yi-Lightning | MoE(闭源) | 官方未公开 | 官方未公开 | 滑窗+全注意力混合 | 细粒度专家分割 | 100352 | 64K | (扩展时增大) | 官方未公开 | report 2412.01253 |

注：表中"rope_theta/上下文/层数"等取自 HF 官方 `config.json`（`01-ai` 组织页）实测；"预训练token"取自官方报告/README/blog。

---

## Yi-6B / Yi-34B（base + chat + 200K，arXiv 2403.04652）

### 架构细节
- 稠密 decoder-only Transformer，代码基于 LLaMA 实现（report §2.3，明确"NOT a Llama derivative，不用 Llama 权重"）。
- **Yi-6B（Table 1）**：hidden 4096 / Q-heads 32 / KV-heads 4（GQA）/ 32 层 / 预训练序列 4096 / maxLR 3e-4。
- **Yi-34B（Table 1）**：hidden 7168 / Q-heads 56 / KV-heads 8（GQA）/ 60 层 / 预训练序列 4096 / maxLR 1.5e-4。
- **注意力**：6B 与 34B 均用 **GQA**（区别于 LLaMA2 仅 70B 用 GQA），report 称应用 GQA 到 6B 也未见性能退化。
- **激活**：SwiGLU，post-attention 层把 activation size 从 4h 减到 8/3h（补偿 GQA 带来的参数减少）。HF config FFN 中间维：6B/9B=11008，34B=20480。
- **位置编码**：RoPE，并用 **RoPE ABF（调整 base frequency，Xiong et al.）** 支撑长上下文。HF config 中 Yi-6B/34B base 的 rope_theta=5e6；200K 版 rope_theta=1e7。
- **Norm**：RMSNorm（HF config `rms_norm_eps`=1e-5）。
- **Tokenizer**：BPE（SentencePiece 实现），**vocab 64000**；数字按单个数字拆分；罕见字符回退 unicode-byte；用 **identity tokenizer**（不把标点转半角）；不用 dummy prefix（开头空格），因该假设在英文引号开头/中文都不成立（report §2.2）。
- **上下文**：base 4K 训练，推理时可扩到 32K；另出 200K 版（见下）。

### 预训练数据
- **总量 3.1T token**，中英双语；与 LLaMA/Falcon 主要差异是双语 + 更严清洗 → 更高 removal ratio（report 摘要 / §1 / Fig.2）。
- 来源：Common Crawl 网页文档为主，混合多源（Fig.2 给出数据 mixture 饼图，正文未给精确百分比）。
- 数据日期：截至 2023 年 6 月（GitHub model info 表）。
- 设计哲学：刻意"overtrain"（3T >> Chinchilla 最优约 1T），处于 post-Chinchilla 区间，以推理成本换性能（report §1）。**宁要 3T 精炼，也不要 10T 未充分过滤**。

### 数据处理 pipeline（report §2.1，Fig.1）
- 起点：CC 网页 → **CCNet pipeline** 做语言识别 + 困惑度打分。
- **启发式规则过滤**：URL/域名/词黑名单 + 乱码过滤；文档长度、特殊符号比、短/连续/不完整行比；重复词/n-gram/段落；阈值基于大样本统计分析（Nguyen et al.）；同时识别并匿名化 **PII**（邮箱、电话）。
- **学习型过滤器（4 个分类器/打分器）**：
  - Perplexity Scorer（KenLM，按 CCNet）——丢弃困惑度远高于平均的文档；
  - Quality Scorer——分类器，偏好类 Wikipedia 质量页，不达标移除；
  - Document Coherence Scorer——识别句段拼凑、不连贯的低质文档（切分或整篇移除）；
  - Safety Scorer——移除暴力/色情/政治宣传等有毒内容（中文 CC 色情/赌博比例偏高，专门处理）。
- **聚类过滤**：无监督语义聚类分组 → 打质量标签，指导 data mixture 优化；自动 + 人工核验剔除低质。
- **去重（cascaded，跟随 Penedo 2023 / RefinedWeb）**：document-level **MinHash** 去重 + sub-document **exact-match** 去重（段落级 + 精确匹配 + MinHash 多级）；report 强调"刻意加大去重强度"。
- **主题模型**：把文档分 news/ads/knowledge 等主题；最终数据集**下采样低价值内容（主要是广告）**以提升信息密度。

### 数据配比 / 训练阶段
- 精确领域百分比官方未给（只有 Fig.2 饼图）。base 报告未提多阶段退火/课程学习（Yi base 是单阶段 3.1T；多阶段 annealing 出现在后续 Yi-Lightning）。
- report §6.1.1 主动说明：**初版刻意不在预训练语料里放大量数学/代码内容**（留待后续继续预训练/微调强化）——这也是 Yi base 在 MATH/HumanEval 偏弱的原因。

### 训练细节（report §4 Infrastructure）
- 算力：report 称"may take months on thousands of GPUs"（未给精确卡数/卡时/FLOPs）→ 卡数级别 thousands，具体官方未公开。
- 并行：**ZeRO-1**（切分优化器状态）+ **TP×PP 3D 并行（节点内 TP+PP，避免跨节点通信瓶颈）**；精心设计 3D 并行以**避免 activation checkpointing 并最小化 pipeline bubble**；**topology-aware ranking**（最小化跨交换机层通信，针对 fat-tree）。
- kernel：FlashAttention + JIT 融合核。
- 稳定性：自动巡检/预测/标注故障节点（taint 临时移出资源池）；任务排队 + 预检 + 故障快速自动恢复；多任务提交/管理控制台。明确列出会遇到 **GPU crash / 通信 fabric error / loss spike**（但未给具体 loss spike 处理超参/z-loss）。
- 精度：BF16（HF config `torch_dtype` bf16；report 未单独强调，base 未用 FP8）。
- LR：见 Table 1（6B maxLR 3e-4，34B 1.5e-4）；global batch / warmup / 总步数官方未公开。

### SFT 细节（report §3）
- **"Quality is all you need"**：SFT 数据 **< 10K 条**多轮指令-回复对，每条由 ML 工程师亲手构造并多轮迭代打磨（对标 LIMA/DEITA，反对 FLAN/UltraChat 的规模化路线）。
- 技巧：prompt 分布选择借鉴 WizardLM（复合指令逐步进化）；回复用 LIMA 式"引言-正文-结论 + bullet"格式；CoT 用"Step-Back"模式（先抽象高层方案再具体推理）；专门减幻觉（剔除可能导致记忆化的回答）与减重复（重写重复轮次）。
- 多样性：InsTag 指令打标系统 + 多样性采样平衡分布；用近似 grid search（每种能力试 {1,1/2,1/4,…,1/64} 比例）定 data mixture。
- 模板：**ChatML** 格式。
- 训练超参：next-word loss 只在 response 上算；AdamW（β1=0.9, β2=0.999, ε=1e-8）；序列长 4096，batch size 64，训练 300 步，**恒定 LR 1e-5**，weight decay 0.1，grad clip 1.0，**NEFTune 噪声 scale 34B=45 / 6B=5**。

### RL / 对齐细节
- Yi base 报告的开源 chat 模型**仅经过 SFT**（README 明确"undergone exclusive training using SFT"，未做 RLHF）。
- 但 infra 已为 RLHF/DPO/PPO 准备：异构后端调度（policy 用 **Megatron**、reward 用 **DeepSpeed**），DPO 中 reference model 中间结果可缓存复用（report §4）。真正上 RLHF/DPO 的是 Yi-Lightning。

### AI infra
- 跨云弹性任务调度、自动故障恢复、拓扑感知资源分配（按实时可用 GPU 节点跨集群运行，超参随节点规模无缝缩放）。
- 长上下文工程：computation-communication overlap + sequence parallelism + 通信压缩，支持到 200K 继续预训练/微调；**不改架构（不用 sparse/local/sliding window），200K 仍是 full attention**。
- 推理/serving：**4-bit 模型量化 + 8-bit KV cache 量化**（MMLU/CMMLU 掉点 <1%）+ PagedAttention + Dynamic Batching；34B chat int4 后可在 24G 显存（RTX 4090）服务。

### 能力扩展（同一报告内）
- **长上下文 200K（§7.1）**：base 4K → RoPE ABF + 继续预训练 **5B token，batch 4M，约 100 步**（仅 1-2B token 即收敛到 4K-200K 低 loss）。数据混合 = 原预训练数据 + 长度上采样长文（多来自书籍）+ 多文档 QA 合成数据（答案含原文段落 recitation）。NIAH 近全绿。后续（README 2024-03-07）又用 5B 长文继续训，NIAH 从 89.3% 升到 99.8%。MMLU 短文能力几乎不掉（Table 6）。
- **深度复制 Yi-9B（§7.3）**：用 Kim et al. depth upscaling，把 Yi-6B（32 层）复制中间第 12-28 层 16 层 → 48 层 Yi-9B；选哪些层复制由各层输入/输出 cosine 相似度（接近 1）决定。继续训 **约 800B token 分两阶段，约 70% 为新近收集精选数据**，末阶段增强代码。恒定 LR **3e-5**，batch 从 4M 起 loss 平台期就增大。Yi-9B 在 code/math 大幅超 Yi-6B（Table 8：GSM8K 32.5→52.3，HumanEval 15.9→39.0）。

---

## Yi-VL-6B / Yi-VL-34B（report §7.2）

### 架构
- 三模块：**ViT（CLIP ViT-H/14 初始化）** + **Projection Module（两层 MLP + LayerNorm）** + **LLM（Yi-6B-Chat / Yi-34B-Chat 初始化）**。
- 图像分辨率：Stage1=224²，Stage2/3=448²。

### 三阶段训练
- **Stage 1**：训练 ViT + projection（图像 224²），数据 **LAION-400M 的 1 亿图文对**；目标对齐 ViT↔LLM。
- **Stage 2**：分辨率升到 448²，数据 **LAION-400M 2000 万图文对 + 约 480 万**多源（CLLaVA/LLaVAR/Flickr/VQAv2/RefCOCO/Visual7w…）。
- **Stage 3**：全参数训练，约 **100 万图文对**多模态对话数据（GQA/VizWiz/TextCaps/OCR-VQA/Visual Genome/ShareGPT4V…），单源上限 5 万对。
- 超参：Stage1&2 global batch 4096 / LR 1e-4 / grad clip 0.5 / 1 epoch；Stage3 batch 256 / LR 2e-5 / grad clip 1.0 / 2 epoch。
- 算力：**128× NVIDIA A100**；Yi-VL-6B 约 3 天，Yi-VL-34B 约 10 天。
- 评测：MMMU test 时 Yi-VL-34B 41.6（开源第一档，Table 7）。

---

## Yi-9B（base，report §7.3 + HF config）

- 见上"能力扩展-深度复制"。要点：Yi-6B（32 层）→ 复制中间 16 层 → 48 层；继续预训练 ~0.8T（report 写 "approximately 800 billion tokens across two stages，约 70% 新近收集"）。
- HF config 实测：hidden 4096 / 48 层 / Q32-KV4 / FFN 11008 / vocab 64000 / **rope_theta=1e4（注意：与 Yi-6B/34B 的 5e6 不同，Yi-9B base 回到 1e4）** / max_pos 4096 / rms_norm_eps 1e-6。
- 数据日期：与 6B/34B 同，截至 2023-06（README model info）。
- 训练：恒定 LR 3e-5，batch 从 4M 起渐增；其余超参对齐 Yi-6B 配置。

---

## Yi-1.5（6B / 9B / 34B，2024-05，GitHub 01-ai/Yi-1.5 + HF config）

> Yi-1.5 **没有独立 arXiv 论文**，官方仍指向 Yi 报告 2403.04652；训练配方信息来自 GitHub README + HF model card + config.json。

### 架构（与 Yi base 同，HF `LlamaForCausalLM`）
- **Yi-1.5-6B**：hidden 4096 / 32 层 / Q32-KV4(GQA) / FFN 11008 / vocab 64000 / rope_theta 5e6 / max_pos 4096 / rms_norm_eps 1e-6。
- **Yi-1.5-9B**：hidden 4096 / 48 层 / Q32-KV4 / FFN 11008 / 其余同上。
- **Yi-1.5-34B**：hidden 7168 / 60 层 / Q56-KV8 / FFN 20480 / 其余同上。
- 长上下文变体（HF config 实测）：Yi-1.5-9B-32K（max_pos 32768，rope 5e6，48 层）、Yi-1.5-9B-Chat-16K（max_pos 16384）。
- License：Apache-2.0（Yi-1.5 起转为 Apache-2.0）。

### 预训练数据 / 配方
- **在 Yi base 之上继续预训练 500B token 高质量语料**（README Intro 原文："continuously pre-trained on Yi with a high-quality corpus of 500B tokens"）。
- 较 Yi base 显著增强 code/math/reasoning/指令跟随，同时保持语言理解/常识/阅读理解。
- 详细数据来源构成、配比%、是否退火/课程、清洗 pipeline 细节：**官方未公开**（README 未展开，无单独论文）。沿用 Yi 报告同套数据工程是合理推断但官方未明示新增 500B 的具体配比。

### SFT / 对齐
- **3M（300 万）多样化微调样本**（README："fine-tuned on 3M diverse fine-tuning samples"）。注意这与 Yi base 的"<10K 手工 SFT"路线明显不同。
- 是否合成、是否多阶段、是否做 RLHF/DPO、模板：**官方未公开**。

### 训练细节 / infra
- 算力（卡型/卡数/卡时）、并行、精度、batch、LR schedule：**官方未公开**（无技术报告）。仅知 torch_dtype=bf16（config）。

---

## Yi-Coder-1.5B / Yi-Coder-9B（2024-09，GitHub 01-ai/Yi-Coder + 官方 blog + HF config）

### 架构（HF config 实测）
- **Yi-Coder-9B**：基于 **Yi-9B**；hidden 4096 / 48 层 / Q32-KV4(GQA) / FFN 11008 / vocab 64000 / **rope_theta 1e7** / **max_pos 131072（128K）** / rms_norm_eps 1e-5 / bf16。
- **Yi-Coder-1.5B**：hidden 2048 / 24 层 / Q16-KV16（**MHA，full attention**）/ FFN 5504 / vocab 64000 / rope_theta 1e7 / max_pos 131072 / bf16。
- base + chat 两版，均 128K 上下文。

### 预训练数据 / 配方（官方 blog "Meet Yi-Coder"，2024-09-05）
- **Yi-Coder-9B 在 Yi-9B 上额外继续预训练 2.4T 高质量 token**；语料 = GitHub **仓库级（repository-level）代码语料** + 从 CommonCrawl 过滤的代码相关数据。
- **52 种主流编程语言**（Java/Python/JS/C++/… 完整列表见 README）。
- **训练数据截止 2023 年底**（blog 明确，用于 LiveCodeBench 防污染，测 2024-01~09 题）。
- 长上下文：128K，project-level 代码理解/生成。
- 数据清洗细节、配比、SFT/对齐配方、算力：**官方未公开**（仅 blog + README，无技术报告）。

### 性能（blog）
- Yi-Coder-9B-Chat：LiveCodeBench 23.4% pass（<10B 唯一破 20%），HumanEval 85.4%，MBPP 73.8%，CRUXEval-O 首个开源破 50%；Aider 54.1%。

---

## Yi-Lightning（2024-10，闭源 API 旗舰，arXiv 2412.01253）

> **只开放 API（platform.lingyiwanwu.com），不放权重**。技术报告刻意不给总参/激活参/层数/隐藏维/专家数/预训练 token 总量等"规模"数字——这些**官方未公开**。报告给的是方法学与少量 infra 数字。Chatbot Arena 总榜第 6（Arena 1287，与 GPT-4o-0513 1285 并肩），中文第 2、Math/Multi-Turn 第 3、Coding/Hard/Longer 第 4。

### 架构创新（report §2）
- **基于增强型 MoE**（参考 DeepSeek/Qwen/Mixtral/Phi 路线）。
- **细粒度专家分割（Fine-grained Expert Segmentation，借鉴 DeepSeekMoE）**：把每个专家 FFN 切成更小功能单元，同时降低中间隐藏维、增大每 token 激活专家数；但发现过度分割伤训练吞吐，故"够用即止"取平衡。
- **专家路由 / 负载均衡（§2.2）**：三级辅助损失叠加——
  - 标准 Switch-Transformer 级 `L_ST`（系数 αST=**1e-6**）；
  - **EP-group 级 `L_EP`**（放松到 Expert-Parallel 组，αEP=**1e-4**）；
  - **Partitioned EP（PEP）`L_PEP`**（组内再切 partition，解决 All-to-All 通信不均，αPEP=**1e-3**）。
  - 注意：是**有辅助损失**的负载均衡（非 DeepSeek-V3 那种 aux-loss-free）。
- **KV Cache 缩减（§2.3）**：
  - **混合注意力块** = 3 层滑窗注意力（sliding window，Mistral 式）+ 1 层全注意力；
  - **跨层 KV cache 复用**（相邻全注意力层共享 KV，全注意力部分内存减半）；
  - 合计**最多减 82.8% 内存**。
- **vocab 扩到 100,352**（较 Yi base 的 64000，增强多语言）；BPE/SentencePiece，数字拆位，unicode-byte 回退。
- 上下文：扩展到 **64K**（RoPE，扩展时增大 base frequency）。

### 预训练（report §3）
- 语料：多语言网页（爬至 2024 年初）+ 书籍 + 论文 + 代码库 + QA 对；沿用 Yi 报告 pipeline 并加强不安全内容/PII 过滤。
- **数学**：CC 上用迭代分类法（DeepSeekMath 式）采集 + 书籍/论文补充；**代码**：GitHub 仓库为主（DeepSeek-Coder 式清洗）；**防污染**：过滤与 MATH/GSM8K/HumanEval/MBPP 的 train/test 共享任意 **30-gram** 的条目。
- **语义聚类拼接**：相似文档聚类拼成长序列，切成 **8192 token** 定长片段；高质量子集留给长上下文阶段。
- 细粒度分类器（文本类型/主题，用小 Yi 模型标注训练）决定最终配比；强调"小量高质领域数据可显著增能"。
- **三阶段训练（§3.2）**：
  1. **初始预训练**：warmup 后 LR 衰减到峰值一半，强调数据多样性建基础能力；
  2. **mid-training**：渐进数据分布迁移 + 上采样高质量数据（复杂推理 + 低资源多语言）+ 扩上下文 + 按 loss 动态调 batch；
  3. **fast-decay（约占总 token 12.5%）**：激进 LR 衰减 + 动态 batch + 强力上采样高质量数据 + 早期 instruction-tuning 适配；设计成可迭代多轮。
- **长上下文扩展（§3.3）**：fast-decay 后再做长文训练扩到 **64K**；多区间上采样（8K-16K / 16K-32K / 32K-64K）保持分布一致；**20B token** 即获稳健长上下文能力且不掉短文性能。
- 预训练总 token / 卡数 / FLOPs：**官方未公开**。

### SFT（report §4.1）
- **两阶段，分别 1.3M 与 300K 样本**：
  - 阶段一：靠大量合成数据强化 math/code 基础能力；
  - 阶段二：多样高质通用域数据提升指令跟随/解题；用 small-to-large 扩展（如阶段二从约 **1 万高质种子**扩到 **30 万**）。
- **合成数据**：document augmentation / self-evolution / 翻译造 prompt；通用任务多模型造答 + 自动 + 人工核验；复杂任务（code/math）用 **MCTS + DFS 搜索 + outcome/process reward model（PRM）** 造多样正确解。
- 实现：**sample packing**（多样本拼一序列）+ **block causal attention（BCA）** 掩码隔离样本；**sample reweighting** 均衡各样本 loss 权重（消除长样本主导偏置）。

### RLHF / 对齐（report §4.2）
- **Reward Modeling（两阶段）**：PMP（preference model pre-training，用公开偏好数据，按训单独 RM 在内部 benchmark 表现筛数据集）+ HFFT（human-feedback fine-tuning，人工多维标注 coding 等，取最高/最低分构 pair，分差不足者剔除）；RM 从预训练模型初始化，用 **Bradley-Terry loss**。
- **偏好数据（§4.2.2）**：prompt = 公开采集 + 合成（按复杂度打分选种子 prompt 配高质 web 上下文合成）；多重去重（n-gram / embedding / 随机下采样）；按复杂度/意图清晰度/领域分类平衡；每 prompt 用 SFT 模型不同温度采多答 → RM 评 → 取高低分且保证足够 reward gap 成 pair。
- **对齐算法：DPO（两阶段 offline → online）**：
  - offline：在 §4.2.2 构的偏好集上训；
  - online：用最新模型实时生成，**每 prompt 采 16 个候选**经 RM 成 pair 喂下一轮；**共做 2 轮 online DPO 迭代**。
  - DPO 工程优化：预算并缓存 reference 模型 log-prob（训练时不常驻 reference 于显存）；偏好对共享上下文 → 先批处理正样本再负样本，复用共享上下文 KV-cache。
- KL/β 等 DPO 超参具体值：官方未公开（仅给方法）。无 PPO/GRPO（用 DPO）。

### AI infra（report §5）
- **并行**：MoE 用 **EP（专家并行）+ PP（流水并行）混合**；定制 pipeline stage 划分 + 细粒度梯度重计算；长上下文用 **context parallelism** 并针对混合注意力优化滑窗计算分布，训练**最高提速 70%**。
- **推理引擎**：高性能自研引擎；多模块多进程**异步调度**把 GPU 利用率从 <70% 提到高并发下 **95%**。
- **FP8 量化 + 硬件感知算子**：架构按 GPU（Nvidia Hopper）特性设计以兼容 FP8；自研 **MoE 算子在 Hopper FP8 达 1,200 TFLOPS/卡**（算子提速 >100%）。
- **Goodput（§5.3）**：自研大规模 GPU 集群 **XCloud**；主动（routine/entrance/preflight 测试）+ 反应式（node exporter + 自定义 InfiniBand 指标）故障发现；**基于内存的异步 checkpoint，把保存从数分钟降到 3-5 秒**，goodput **>99%**。

### 安全 RAISE（report §6）
- **RAISE（Responsible AI Safety Engine）四组件**：RAISE-1 预训练数据安全过滤（Transformer/DNN 分类器）；RAISE-2 后训练 SFT&RLHF 安全（reward engineering 奖安全惩有害）；RAISE-3 推理输入安全；RAISE-4 输出安全（价值对齐/偏见/合规/准确/适当性实时检测）。
- 注：Yi base 报告（2403.04652 §5）已有 RAISE 雏形（预训练 PII/有毒过滤 + 对齐期安全 taxonomy + 攻击模拟 prompt 混入 SFT）。

---

## 关键缺口（官方未公开汇总）

- **Yi base（6B/34B）**：精确算力（卡数仅"thousands"、无卡时/FLOPs）；预训练 global batch / warmup / 总步数；各领域数据精确百分比（仅 Fig.2 饼图）；loss spike 具体处理超参/有无 z-loss。
- **Yi-1.5**：无独立论文；新增 500B 的数据来源/配比、3M SFT 是否合成/多阶段、有无 RLHF、全部训练超参与算力。
- **Yi-Coder**：2.4T 代码语料的精确配比/清洗细节、SFT/对齐配方、算力。
- **Yi-Lightning（最大缺口）**：总参/激活参、层数、隐藏维、专家总数/共享专家/激活专家数、预训练 token 总量、算力（卡型/卡数/卡时/FLOPs）、global batch、各阶段 token 量、DPO 的 β/KL、RM 规模。报告刻意只给方法学，不给规模数字（闭源 API 模型）。
- **Yi-VL**：未给 SFT/RLHF 文本侧细节（沿用 Yi-Chat）。

---

## 来源（一手官方）

- **Yi: Open Foundation Models by 01.AI**（Yi-6B/34B/9B/VL/200K/深度复制）
  - arXiv abs: https://arxiv.org/abs/2403.04652 ；pdf: https://arxiv.org/pdf/2403.04652
  - 本地：`../../../sources/llm/2023/yi-01ai.pdf`（= `/2024/files/yi.pdf`，同一文件）
  - GitHub: https://github.com/01-ai/Yi ；本地 README：`../../../sources/llm/2023/yi-readme.md`
- **Yi-Lightning Technical Report**
  - arXiv abs: https://arxiv.org/abs/2412.01253 ；pdf: https://arxiv.org/pdf/2412.01253 ；HTML: https://arxiv.org/html/2412.01253v5
  - 本地：`../../../sources/llm/deep-dive/yi-lightning-2412.01253.pdf`
- **Yi-1.5**
  - GitHub: https://github.com/01-ai/Yi-1.5
  - HF 官方 config（实测）：https://huggingface.co/01-ai/Yi-1.5-6B/raw/main/config.json ；…/Yi-1.5-9B/… ；…/Yi-1.5-34B/… ；…/Yi-1.5-9B-32K/… ；…/Yi-1.5-9B-Chat-16K/…
  - HF collection model card: https://huggingface.co/collections/01-ai/yi-15-2024-05-663f3ecab5f815a3eaca7ca8
- **Yi-Coder**
  - GitHub: https://github.com/01-ai/Yi-Coder ；raw README: https://raw.githubusercontent.com/01-ai/Yi-Coder/main/README.md
  - 官方 blog（已下线，经 Wayback 取得）: http://web.archive.org/web/20241224080911/https://01-ai.github.io/blog.html?post=en/2024-09-05-A-Small-but-Mighty-LLM-for-Code.md
  - HF config（实测）：https://huggingface.co/01-ai/Yi-Coder-9B/raw/main/config.json ；…/Yi-Coder-1.5B/…
  - HF model card README：本地 `../../../sources/llm/2024/yi-coder-hf-readme.md`
- **Yi base / 200K / 9B config（实测）**：
  - https://huggingface.co/01-ai/Yi-6B/raw/main/config.json ；…/Yi-34B/… ；…/Yi-9B/… ；…/Yi-34B-200K/…
- 官方组织页：HF https://huggingface.co/01-ai ；ModelScope https://www.modelscope.cn/organization/01ai/
