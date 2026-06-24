# Mistral / Mixtral 家族 训练配方深挖

> 家族：Mistral AI（法国，2023 创立）。本档只收一手官方来源（arXiv 原文、官方博客、官方 HuggingFace 组织页的 config.json）。
> 关键事实：**Mistral 对预训练数据来源/配比、数据 pipeline、算力/卡时、并行策略、优化器/LR/warmup、RL 超参等几乎从不公开**。其技术报告（Mistral 7B、Mixtral、Pixtral）只给「架构表 + 评测」，刻意不写数据与训练细节。因此本档中大量「预训练数据 / 训练细节 / RL」字段会标注**官方未公开**——这是 Mistral 的一贯风格，不是检索不到。
> 调研日期：2026-06-18。

---

## 家族演进脉络

- **2023-09 Mistral 7B (v0.1)**：第一款开源模型，7B 稠密；引入 GQA + 滑动窗口注意力（SWA）+ 滚动缓冲缓存。Apache 2.0。证明「精心设计的小模型可压缩更多知识」。
- **2023-12 Mixtral 8x7B (v0.1)**：首个达到开源 SOTA 的稀疏 MoE（SMoE）；与 Mistral 7B 同架构，但每层 FFN 换成 8 专家 top-2 路由；47B 总参 / 13B 激活；32k 上下文；多语言上采样；Instruct 版用 SFT + DPO。Apache 2.0。
- **2024-04 Mixtral 8x22B (v0.1)**：更大的 SMoE，141B 总参 / 39B 激活，64k 上下文，原生函数调用。Apache 2.0。
- **2024-05 Codestral 22B (v0.1)**：首款代码专用模型，22B 稠密，80+ 编程语言，32k 上下文，支持 FIM（fill-in-the-middle）。Mistral AI Non-Production License（MNPL，非商用）。
- **2024-07 Mistral NeMo 12B (2407)**：与 NVIDIA 合作，12B 稠密，128k 上下文，新 Tekken tokenizer（131072 词表，基于 tiktoken），量化感知训练（QAT）支持无损 FP8 推理。Apache 2.0。
- **2024-07 Mistral Large 2 (2407)**：123B 稠密旗舰，128k 上下文，单节点推理设计，大量代码训练，专门做了减少幻觉的对齐。Mistral Research License（MRL，研究/非商用开权重）。
- **2024-10 Pixtral 12B (2409)**：首个多模态模型，以 Mistral NeMo 12B 为语言主干 + 从零训练的 400M 视觉编码器（Pixtral-ViT，RoPE-2D，原生分辨率），128k 上下文。Apache 2.0。

> 架构家谱：Mistral 7B → (MoE 化) → Mixtral 8x7B/8x22B；Mistral 7B → (扩规模/Tekken/NeMo 合作) → Mistral NeMo 12B → (加 ViT) → Pixtral 12B；Mistral NeMo/Large 配方 → (代码上采样) → Codestral 22B、Mistral Large 2。

### 各代关键参数对比（均来自官方一手：论文架构表 / 官方 config.json / 官方博客）

| 型号 | 总参 / 激活 | 层数 | 隐藏维 dim | FFN维 | 注意力头 | KV头(GQA) | head_dim | MoE | 词表 | 上下文 | RoPE base | 许可 | 一手来源 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Mistral 7B v0.1 | 7B 稠密 | 32 | 4096 | 14336 | 32 | 8 | 128 | — | 32000 | 8192（SWA 窗口 4096） | 论文未列(代码 1e4) | Apache 2.0 | 论文 Table 1 |
| Mixtral 8x7B v0.1 | 47B / 13B | 32 | 4096 | 14336 | 32 | 8 | 128 | 8 专家, top-2 | 32000 | 32768 | 论文未列 | Apache 2.0 | 论文 Table 1 |
| Mixtral 8x22B v0.1 | 141B / 39B | 56 | 6144 | 16384 | 48 | 8 | 128 | 8 专家, top-2 | 32000 | 65536 | 1000000 | Apache 2.0 | 官方 config.json + 博客 |
| Codestral 22B v0.1 | 22B 稠密 | 56 | 6144 | 16384 | 48 | 8 | 128 | — | 32768 | 32768 | 1000000 | MNPL（非商用） | 官方 config.json + 博客 |
| Mistral NeMo 12B (2407) | 12B 稠密 | 40 | 5120 | 14336 | 32 | 8 | 128 | — | 131072 (Tekken) | 131072 | 1000000 | Apache 2.0 | 官方 config.json + 博客 |
| Mistral Large 2 (2407) | 123B 稠密 | 官方 config 受限* | 官方 config 受限* | — | — | — | — | — | 32768(估*) | 128k | — | MRL（研究/非商用） | 官方博客（per-layer 配置 gated） |
| Pixtral 12B (2409) | 12B(解码器)+0.4B(ViT) | 40(解码器)/24(编码器) | 5120/1024 | 14336/4096 | 32/16 | 8/16 | 128/64 | — | 131072 | 131072 | — | Apache 2.0 | 论文 Table 1 |

> *Mistral Large 2 的官方 HuggingFace 仓库（mistralai/Mistral-Large-Instruct-2407）权重与 config.json 均为 gated（需登录授权），无法以一手身份核实逐层维度。官方博客只确认「123B 参数、128k 上下文」。坊间流传 96 层/hidden 12288/96 头/8 KV，但**非官方一手可验证来源，故不收**。

---

## Mistral 7B (v0.1)

- 发布：2023-09-27（博客）/ 2023-10-10（arXiv 2310.06825）。Apache 2.0。

### 架构细节（论文 Table 1，一手）
- 稠密 decoder-only transformer，7B 参数。
- 层数 n_layers=32；dim=4096；hidden_dim(FFN)=14336；n_heads=32；n_kv_heads=8（**GQA**）；head_dim=128。
- vocab_size=32000（SentencePiece BPE）。
- context_len=8192；**滑动窗口注意力 SWA**，window_size=4096。SWA 利用堆叠层让信息每层前进 W token，k 层后理论注意力跨度 ≈ k×W；最后一层 W=4096 时理论跨度 ≈131K token。
- **滚动缓冲缓存（Rolling Buffer Cache）**：缓存固定大小 W，位置 i 的 kv 存于 i mod W；32k 序列下缓存内存降 8×而不损质量。
- **Pre-fill & Chunking**：长 prompt 按 window 大小分块预填充 kv cache。
- 激活：SwiGLU（沿用 Llama 改动，论文称「uses the same modifications as Llama」隐含 RMSNorm + RoPE + SwiGLU；论文未单独列 norm/激活字段）。
- 工程：对 FlashAttention 与 xFormers 做了改动，16K 序列 + W=4096 下相对 vanilla attention 2× 加速。

### 预训练数据
- **官方未公开**（论文完全未写数据来源、token 数、配比）。

### 数据处理 pipeline
- **官方未公开**。

### 训练细节（算力/并行/优化器）
- **几乎全部官方未公开**。论文致谢仅透露：在 **CoreWeave** 集群训练；用了 **CINECA/EuroHPC 的 Leonardo 超算**资源。无 GPU 卡数、卡时、FLOPs、batch、LR、并行策略。

### SFT 细节（Mistral 7B – Instruct）
- 论文明说：仅用 HuggingFace 上**公开可得的指令数据集**微调，「No proprietary data or training tricks were utilized」；定位为「简单初步演示」。无规模/模板细节。

### RL / 对齐
- v0.1 Instruct **无 RL**（仅 SFT）。论文另给「系统提示词做 guardrails」与「self-reflection 内容审核」演示（precision 99.4% / recall 95.6%）。

### AI infra
- 参考实现开源；推理栈：**vLLM**（PagedAttention）+ SkyPilot 部署；HuggingFace 集成。

### 来源
- arXiv: https://arxiv.org/abs/2310.06825 ｜ PDF: https://arxiv.org/pdf/2310.06825
- 博客: https://mistral.ai/news/announcing-mistral-7b/
- GitHub: https://github.com/mistralai/mistral-src
- 本地: `../../../sources/llm/2023/mistral-7b.pdf`、`.../2023/files/mistral-7b-blog.html`

---

## Mixtral 8x7B (v0.1) — SMoE

- 发布：2023-12-11（博客）/ 2024-01-08（arXiv 2401.04088）。base 与 Instruct 均 Apache 2.0。

### 架构细节（论文 Table 1，一手）
- 稀疏 MoE（SMoE），与 Mistral 7B 同架构，但**每层 FFN 替换为 MoE 层**。
- dim=4096；n_layers=32；head_dim=128；n_heads=32；n_kv_heads=8（GQA）；hidden_dim(每个专家 FFN)=14336；vocab_size=32000。
- **MoE**：num_experts=8，top_k=2（每 token 每层选 2 个专家加权求和）；专家函数=SwiGLU。
- **参数**：总参（sparse）≈47B，激活（active）≈13B/token。论文指出 MoE 仅替换 FFN，所有层都换（不像 GShard 每隔一层换）。
- 门控：`G(x)=Softmax(TopK(x·Wg))`，K=2。
- context_len=32768（**全密集 32k**，非 SWA）。
- 论文未单列 RoPE base / 辅助负载均衡损失系数（与 8x22B 不同，8x22B 的官方 config 显式给出 router_aux_loss_coef=0.001）。
- 路由分析：专家选择更依赖**句法**而非领域；连续 token 有时间局部性（高层重复率显著高于随机）。

### 预训练数据
- **基本官方未公开**。论文唯一披露：「与 Mistral 7B 相比，预训练**显著上采样了多语言数据**比例」，使其在法/德/西/意表现强。无 token 数、来源、具体配比。

### 数据处理 pipeline
- **官方未公开**。

### 训练细节
- **官方未公开**（无算力/并行/优化器/batch/LR）。致谢提到 **CoreWeave、Scaleway** 技术支持；NVIDIA 协助集成 TensorRT-LLM/Triton。

### SFT + RL（Mixtral 8x7B – Instruct）
- 流程（论文明确）：**SFT（指令数据集）→ DPO（Direct Preference Optimization，成对偏好反馈数据集）**。
- 无指令数据规模/来源/是否合成/模板、无 DPO 偏好数据规模/β/KL 等超参。
- 结果：MT-Bench 8.30，2023-12 时最佳开放权重模型；LMSys Arena Elo 1121，超 GPT-3.5-Turbo/Gemini Pro/Claude-2.1/Llama2-70B-chat。

### AI infra
- 向 **vLLM** 提交改动，集成 **Megablocks** CUDA kernels 做高效 MoE 推理（把 FFN 转为大稀疏矩阵乘）；支持 **专家并行 EP**（论文讨论 EP 的负载均衡挑战）；SkyPilot 部署；NVIDIA TensorRT-LLM 集成。

### 来源
- arXiv: https://arxiv.org/abs/2401.04088 ｜ PDF: https://arxiv.org/pdf/2401.04088
- 博客: https://mistral.ai/news/mixtral-of-experts/
- 本地: `../../../sources/llm/themes/architecture/mixtral.pdf`（= `themes/ai-infra/files/mixtral-2401.04088.pdf`）、`.../2023/files/mixtral-blog.html`

---

## Mixtral 8x22B (v0.1) — SMoE

- 发布：2024-04-17（博客）。base 与 Instruct 均 Apache 2.0。无独立技术报告，架构以官方 HuggingFace config.json 为一手依据。

### 架构细节（官方 config.json：mistralai/Mixtral-8x22B-v0.1，一手）
- `model_type=mixtral`，`MixtralForCausalLM`。
- hidden_size(dim)=6144；num_hidden_layers=56；intermediate_size(FFN)=16384；num_attention_heads=48；num_key_value_heads=8（GQA）；head_dim=128（6144/48）。
- **MoE**：num_local_experts=8，num_experts_per_tok=2（top-2）；**router_aux_loss_coef=0.001**（即有负载均衡辅助损失，非「无辅助损失」路由）；output_router_logits=false。
- vocab_size=32000；hidden_act=silu（即 SwiGLU 门控）；rms_norm_eps=1e-5（**RMSNorm**）。
- **rope_theta=1000000**（RoPE base 1e6）；max_position_embeddings=65536（64k）；sliding_window=null（不使用 SWA）；tie_word_embeddings=false；torch_dtype=bfloat16。
- 博客口径：**141B 总参 / 39B 激活**；64k 上下文；原生函数调用 + 约束输出（JSON）。

### 预训练数据 / pipeline / 训练细节
- **官方未公开**（无数据来源、token、配比、算力、并行、优化器）。博客只说多语言（英/法/意/德/西）、强数学与代码。

### SFT / RL（Instruct）
- **官方未公开具体配方**。博客只给指标：Instruct 版 GSM8K maj@8 = 90.8%，Math maj@4 = 44.6%。（沿用家族 SFT+DPO 风格，但 8x22B 博客未明写。）

### AI infra
- 同 Mixtral 8x7B 生态：vLLM + Megablocks、EP、TensorRT-LLM。

### 来源
- 博客: https://mistral.ai/news/mixtral-8x22b/
- 官方权重/config: https://huggingface.co/mistralai/Mixtral-8x22B-v0.1 （config.json）
- 本地: `../../../sources/llm/deep-dive/mixtral-8x22b-config.json`、`.../2024/files/mistral-mixtral-8x22b-blog.md`

---

## Codestral 22B (v0.1) — 代码专用稠密模型

- 发布：2024-05-29（博客）。许可：**Mistral AI Non-Production License (MNPL)**，仅研究/测试，商用需另购。

### 架构细节（官方 config.json：mistralai/Codestral-22B-v0.1，一手）
- `model_type=mistral`，`MistralForCausalLM`（稠密，非 MoE）。
- hidden_size=6144；num_hidden_layers=56；intermediate_size(FFN)=16384；num_attention_heads=48；num_key_value_heads=8（GQA）；head_dim=128。
- vocab_size=32768；hidden_act=silu（SwiGLU）；rms_norm_eps=1e-5（RMSNorm）；**rope_theta=1000000**；max_position_embeddings=32768（32k）；sliding_window=null；torch_dtype=bfloat16。
- 注：与 Mixtral 8x22B 同主干维度（56 层/6144/48 头/8 KV），相当于其「单专家稠密版」+ 更大词表（32768）。

### 预训练数据（博客，一手）
- 训练于 **80+ 编程语言**的多样数据集（Python/Java/C/C++/JavaScript/Bash，及 Swift/Fortran 等小众语言）。
- 具体 token 数、代码/文本配比、数据来源与版本：**官方未公开**。

### 数据处理 pipeline / 训练细节
- **官方未公开**（无去重/过滤/污染检测细节，无算力/并行/优化器）。

### 能力 / 微调
- 支持 **FIM（fill-in-the-middle）**：补全函数、写测试、补全部分代码。
- 32k 上下文（对比竞品 4k/8k/16k）→ RepoBench（长程仓库级补全）领先。
- 评测：HumanEval pass@1、MBPP sanitized、CruxEval、RepoBench EM、SQL(Spider)、多语言 HumanEval（C++/bash/Java/PHP/TS/C#）、FIM HumanEval（Python/JS/Java，对标 DeepSeek Coder 33B）。
- SFT/RL 具体配方：**官方未公开**。

### AI infra
- API endpoint（含 instruct 与 completion/FIM）；集成 LlamaIndex / LangChain；mistral-inference / mistral-finetune；自部署。

### 来源
- 博客: https://mistral.ai/news/codestral/
- 官方权重/config: https://huggingface.co/mistralai/Codestral-22B-v0.1 （config.json）
- 本地: `../../../sources/llm/deep-dive/codestral-22b-config.json`、`.../deep-dive/files/codestral-blog.md`

---

## Mistral NeMo 12B (2407) — 与 NVIDIA 合作

- 发布：2024-07-18（博客）。base + instruct 均 Apache 2.0。

### 架构细节（官方 config.json：mistralai/Mistral-Nemo-Base-2407，一手）
- `model_type=mistral`，`MistralForCausalLM`（稠密，标准架构，可作 Mistral 7B 的 drop-in 替换）。
- hidden_size=5120；num_hidden_layers=40；intermediate_size(FFN)=14336；num_attention_heads=32；num_key_value_heads=8（GQA）；**head_dim=128**（显式给出，注意 32×128=4096 ≠ 5120，head_dim 独立于 hidden_size）。
- **vocab_size=131072**（新 Tekken tokenizer）；hidden_act=silu（SwiGLU）；rms_norm_eps=1e-5（RMSNorm）；**rope_theta=1000000**；max_position_embeddings=131072（**128k**）；sliding_window=null；torch_dtype=bfloat16。
- **Tekken tokenizer**（博客）：基于 tiktoken，训于 100+ 语言；比旧 SentencePiece 压缩更优——代码/中文/意/法/德/西/俄约 +30%，韩语 2×、阿语 3×；对约 85% 语言优于 Llama 3 tokenizer。

### 预训练数据（博客，一手）
- 面向全球多语言（英/法/德/西/意/葡/中/日/韩/阿/印地等），训练了**函数调用**。
- 具体 token 数 / 来源 / 配比：**官方未公开**。

### 数据处理 pipeline / 训练细节
- **官方未公开**。唯一工程披露：用**量化感知训练（QAT）**，支持**无性能损失的 FP8 推理**。无算力/并行/优化器（虽与 NVIDIA 合作，应用了 Megatron/NeMo 框架，但博客未给参数）。

### SFT / 对齐（instruct）
- 博客：经过「先进的微调与对齐阶段」，比 Mistral 7B 更擅长精确指令遵循、推理、多轮、代码。**无规模/算法（是否 DPO）/模板细节**。

### AI infra
- 推理：mistral-inference；la Plateforme `open-mistral-nemo-2407`；打包为 **NVIDIA NIM** 微服务（ai.nvidia.com）；FP8。

### 来源
- 博客: https://mistral.ai/news/mistral-nemo/
- 官方权重/config: https://huggingface.co/mistralai/Mistral-Nemo-Base-2407 （config.json）、https://huggingface.co/mistralai/Mistral-Nemo-Instruct-2407
- 本地: `../../../sources/llm/deep-dive/mistral-nemo-config.json`、`.../2024/files/mistral-nemo-blog.md`

---

## Mistral Large 2 (2407) — 123B 旗舰

- 发布：2024-07-24（博客）。许可：**Mistral Research License (MRL)**，研究/非商用可用与修改；商用自部署需 Mistral Commercial License。

### 架构细节
- 稠密，**123B 参数**（官方博客），为**单节点长上下文高吞吐推理**设计；128k 上下文。
- **逐层维度（层数/hidden/头数/KV头/词表）：官方 HuggingFace 仓库 mistralai/Mistral-Large-Instruct-2407 的 config.json 为 gated（需授权登录），无法以一手身份核实**，故不收坊间数字。词表大概率与 NeMo 同代（Tekken），但官方未在博客中明示——标注**待核实**。

### 预训练数据（博客，一手定性）
- 「在**非常大比例的代码**上训练」（沿用 Codestral 22B / Codestral Mamba 经验）；80+ 编程语言。
- 「在**大比例多语言数据**上训练」：英/法/德/西/意/葡/荷/俄/中/日/韩/阿/印地。
- 具体 token 数 / 配比 %：**官方未公开**。

### 数据处理 pipeline / 训练细节
- **官方未公开**（无算力/并行/优化器/精度）。

### SFT / 对齐（博客定性，一手）
- 重点做了**减少幻觉**：微调使模型更谨慎、信息不足时**承认「不知道」**而非编造。
- 大幅提升指令遵循、长多轮对话、**回复简洁性**（专门优化生成长度）。
- 训练了**并行与顺序函数调用 / 检索**能力。
- 具体算法（是否 DPO/PPO）、偏好数据规模：**官方未公开**。

### AI infra
- la Plateforme `mistral-large-2407`；HuggingFace instruct 权重 + mistralcdn tar；Vertex AI / Azure AI Studio / Amazon Bedrock / IBM watsonx；支持微调（la Plateforme）。

### 来源
- 博客: https://mistral.ai/news/mistral-large-2407/
- 官方权重（gated）: https://huggingface.co/mistralai/Mistral-Large-Instruct-2407
- 本地: `../../../sources/llm/2024/mistral-large-2-blog.md`

---

## Pixtral 12B (2409) — 多模态

- 发布：2024-09-17（博客）/ arXiv 2410.07073（2024-10）。Apache 2.0。

### 架构细节（论文 Table 1，一手）

**多模态解码器（语言主干，基于 Mistral NeMo 12B）**
- dim=5120；n_layers=40；head_dim=128；hidden_dim(FFN)=14336；n_heads=32；n_kv_heads=8（GQA）；context_len=131072（128k）；vocab_size=131072。
- 图像 token 与文本 token 同等对待，全部用 RoPE-1D；因果自注意力（支持多图多轮）。

**视觉编码器 Pixtral-ViT（从零训练，约 400M）**
- dim=1024；n_layers=24；head_dim=64；hidden_dim(FFN)=4096；n_heads=16；n_kv_heads=16（编码器用 MHA，非 GQA）；context_len=4096；patch_size=16。
- 4 项关键改动：①**Break tokens**（行间 [IMAGE BREAK]、序列末 [IMAGE END]，区分同面积不同宽高比）；②**FFN 门控**（gating，即 SwiGLU 类）；③**Sequence packing**（多图沿序列展平 + 块对角注意力 mask 防跨图泄漏）；④**RoPE-2D**（相对二维旋转位置，原生支持可变分辨率/宽高比，无需插值）。
- ViT→解码器：两层全连接 + 中间隐层 + **GeLU** 激活，把视觉输出投到解码器嵌入维。

### 预训练数据（论文，一手定性）
- 在**大规模图文交错文档（interleaved image-text）**上预训练，故支持多轮多图对话；是 instruction-tuned 模型。
- 具体 token 数 / 数据来源 / 配比：**官方未公开**（论文按 Mistral 惯例不写数据）。

### 数据处理 pipeline / 训练细节
- **官方未公开**（无算力/并行/优化器；视觉编码器「从零训练」但未给训练超参）。

### SFT / 对齐
- 「instruction tuned」，但**具体 SFT/RL 配方官方未公开**。
- 附带贡献：开源 **MM-MT-Bench**（多模态多轮指令遵循基准，92 段对话，LLM 评判，与 LMSys Vision Elo 高相关）；并主张 Explicit prompts + flexible parsing 的标准化评测协议。

### AI infra
- mistral-inference 推理代码、mistral-evals 评测代码。

### 来源
- arXiv: https://arxiv.org/abs/2410.07073 ｜ PDF: https://arxiv.org/pdf/2410.07073
- 博客: https://mistral.ai/news/pixtral-12b/
- GitHub: https://github.com/mistralai/mistral-inference 、https://github.com/mistralai/mistral-evals
- 本地: `../../../sources/llm/themes/architecture/pixtral.pdf`（= `.../2024/files/2410.07073.pdf`）

---

## 跨型号总结 / 关键观察

- **架构共性**：全家族 = decoder-only transformer + **RMSNorm + RoPE + SwiGLU + GQA(8 KV 头)**。RoPE base 从 7B/8x7B 时代后统一升到 **1e6**（8x22B/Codestral/NeMo config 均为 1000000），以支持长上下文。
- **SWA 的取舍**：仅 Mistral 7B 用滑动窗口（4096）+ 滚动缓冲缓存；Mixtral 8x7B 起改为**全密集 32k**（sliding_window=null），后续型号也都是密集长上下文。
- **MoE 路由**：top-2，8 专家；8x22B 官方 config 显式 **router_aux_loss_coef=0.001**（有负载均衡辅助损失），即**不是**「无辅助损失」式路由；无共享专家概念。
- **Tokenizer 换代**：SentencePiece(32000) → 32768(Codestral) → **Tekken/tiktoken 131072**（NeMo/Pixtral，2024-07 起）。
- **精度**：全部 bfloat16；NeMo 额外做 QAT 支持 FP8 推理。
- **对齐**：唯一明确公开的 RL 算法是 **Mixtral 8x7B 的 SFT→DPO**；其余型号只说「微调与对齐」，未公开是否用 DPO/PPO，更无 RLVR/GRPO 等迹象。
- **一贯的不透明**：Mistral 从不公开预训练 token 数、数据来源/配比 %、数据 pipeline、算力（卡数/卡时/FLOPs）、并行（TP/PP/DP/EP/ZeRO）、优化器/LR/warmup、退火/课程学习——这是与 Llama/OLMo/Qwen/Nemotron 等的最大差异。
