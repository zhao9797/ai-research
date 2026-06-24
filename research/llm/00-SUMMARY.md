---
title: 大模型技术演进调研 (GPT-3 → 2026-06) · 主汇总
type: source
tags: [llm, survey, pretraining, architecture, ai-infra, post-training, agentic]
created: 2026-06-18
updated: 2026-06-18
---

# 大模型技术演进调研 · 主汇总（GPT-3 2020-05 → 2026-06）

> 只收**一手官方来源**：arXiv 原文、官方技术报告/system card、官方博客、官方 GitHub/model card/HF 组织页。
> **不含任何第三方解读/翻译/二手总结/评测聚合**。
> 五大分类：`预训练数据` · `架构` · `AI infra` · `后训练` · `agentic训练`（每条至少命中其一，可多标）。

---

## 一、语料统计

- **去重后来源**：**532 条**（解析自 667 篇结构化页，按原始 URL 去重）
- **下载原文**：约 **760 份 / ~2.6 GB** —— `*.html/json` 随库（`sources/llm/<scope>/`），**`*.pdf` 走 HF private bucket `jaczhao/ai-research-sources`（存算分离，不入 git）**
- **开源模型深挖档案**：14 份（`deep-dive/`，含「2026 调研后增量补录」段）
- **分类汇总章节**：6 篇（`sections/`，末尾附 2026 增量补录）

**按年（去重）**：2018→1 · 2019→4 · 2020→36 · 2021→32 · 2022→58 · 2023→102 · 2024→136 · 2025→110 · 2026(H1)→53

**按国别（去重）**：美国/西方 303 · 中国 196 · 欧洲 20 · 其它 ~13 —— 中美 top 公司全部覆盖

**按分类（去重，可多标）**：架构 ~298 · 后训练 ~283 · AI infra ~180 · 预训练数据 ~178 · agentic训练 ~143

---

## 二、怎么读这份调研

按从"结论"到"原文"的粒度，四层：

1. **五大分类汇总（核心，先读这个）** — `sections/`
   - [预训练数据](sections/pretrain-data.md)
   - [架构](sections/architecture.md)
   - [AI infra](sections/ai-infra.md)
   - [后训练](sections/post-training.md)
   - [agentic训练](sections/agentic.md)
   - [开源模型训练配方（横向对比）](sections/open-model-recipes.md)
2. **开源模型深挖档案（要训练/数据/配比/RL/架构细节看这个）** — `deep-dive/`（见第四节）
3. **全量来源索引（按年月，可点开每条）** — [01-INDEX.md](01-INDEX.md)
4. **单条结构化页** — `2020/`…`2026/`、`themes/`；**下载的原文** — `sources/llm/<scope>/`（html/json 随库，pdf 在 HF bucket）

---

## 三、五大分类脉络速览

### 1) 预训练数据 → [完整章节](sections/pretrain-data.md)（173 条）
从 GPT-3 的 CommonCrawl 粗过滤（~300B token）→ 质量分类器与去重成为标配（The Pile、C4、RefinedWeb）→ 配方公开化（LLaMA 配比、Dolma/RedPajama 全开）→ **数据质量 > 数据量**（Phi "教科书"、FineWeb-Edu edu 分类器、DCLM）→ 多阶段/退火与合成数据（MiniCPM WSD、Nemotron 合成、Llama 3 15T+退火）→ 万亿-十万亿 token、长上下文阶段、强 decontamination。
- 里程碑：[Scaling Laws](2020/scaling-laws-for-neural-language-models.md) · [Chinchilla 计算最优](2022/chinchilla-training-compute-optimal-large-language-models.md) · [The Pile] · [LLaMA] · [Dolma](deep-dive/data-pipelines.md) · [FineWeb/FineWeb-Edu](deep-dive/data-pipelines.md) · [DCLM](deep-dive/data-pipelines.md) · [Phi Textbooks]

### 2) 架构 → [完整章节](sections/architecture.md)（291 条）
Decoder-only Transformer 定型 → 位置编码 RoPE/ALiBi/YaRN → 注意力省显存 MQA/GQA→**MLA**（DeepSeek-V2）→ **MoE 主流化**：GShard/Switch/GLaM → DeepSeekMoE 细粒度+共享专家 → 无辅助损失负载均衡 → 万亿稀疏（Kimi K2、Ling/Ring-1T、Pangu Ultra-MoE 718B）→ 线性/混合架构（Mamba、RWKV、RetNet、Jamba、Nemotron-H、MiniMax Lightning/Sparse、Kimi Linear、Falcon-H1）→ 原生多模态/omni 与 native sparse attention。
- 里程碑：[GShard]·[Switch]·[GLaM]·[DeepSeekMoE](deep-dive/deepseek.md)·[Mamba]·[MLA/DeepSeek-V2](deep-dive/deepseek.md)·[aux-loss-free MoE]·[Native Sparse Attention](themes/ai-infra/native-sparse-attention.md)·[Jamba]·[Nemotron-H](2025/nemotron-h.md)

### 3) AI infra → [完整章节](sections/ai-infra.md)（175 条）
训练侧：Megatron-LM 张量并行 + DeepSpeed/ZeRO 显存分片 → 3D/序列并行、激活重算 → FP8 训练、MegaScale 万卡 → **DeepSeek-V3 FP8+DualPipe** 开源整套（开源周 FlashMLA/DeepEP/DeepGEMM/3FS）。推理侧：FlashAttention 1/2/3 → PagedAttention/vLLM → SGLang/RadixAttention → 量化(GPTQ/AWQ/SmoothQuant) → PD 分离/Mooncake/MegaScale-Infer。RL 训练系统：DeepSpeed-Chat→OpenRLHF→veRL/HybridFlow→DAPO/AReaL/ProRL。
- 里程碑：[ZeRO/DeepSpeed](2020/zero-deepspeed-100b-parameters.md)·[Megatron 激活重算]·[FlashAttention]·[vLLM/PagedAttention]·[DeepSeek-V3 硬件反思](themes/ai-infra/deepseek-v3-hardware.md)·[DeepSeek 开源周](themes/ai-infra/deepseek-open-infra-index.md)·[veRL/HybridFlow]

### 4) 后训练 → [完整章节](sections/post-training.md)（276 条）
RLHF 奠基（[Learning to summarize](2020/learning-to-summarize-from-human-feedback.md)→InstructGPT）→ Constitutional AI/RLAIF → **离线偏好优化** DPO 及变体(IPO/KTO/ORPO/SimPO) → **可验证奖励 RLVR + GRPO**（DeepSeekMath）→ **推理模型范式**（o1 → DeepSeek-R1 纯 RL "顿悟"，Kimi k1.5）→ 过程奖励 PRM、长 CoT、on-policy 蒸馏、prolonged RL（ProRL）→ 全流程开放（Tülu 3、OLMo 2、MiMo、Nemotron Cascade）。
- 里程碑：[InstructGPT]·[DPO](themes/post-training/dpo.md)·[Constitutional AI]·[DeepSeekMath GRPO](deep-dive/deepseek.md)·[DeepSeek-R1](2025/deepseek-r1.md)·[Kimi k1.5](2025/kimi-k1.5.md)·[Tülu 3](deep-dive/olmo-ai2.md)·[on-policy distillation](themes/post-training/on-policy-distillation.md)

### 5) agentic 训练 → [完整章节](sections/agentic.md)（136 条）
prompt 时代（WebGPT/ReAct/Toolformer/Reflexion/Voyager/Generative Agents）→ tool-use 微调（ToolLLM/AgentTuning/CodeAct）→ 评测驱动（SWE-bench/WebArena/OSWorld/tau-bench）→ **computer/browser use**（Claude computer use、Operator/CUA、UI-TARS）→ **多轮 agent RL 爆发(2025)**（Search-R1/ReTool/RAGEN/ToolRL/DeepResearcher/WebSailor）→ agentic 原生模型（Kimi K2、GLM-4.5 ARC、Qwen3-Coder、Tongyi DeepResearch、Seed2.0）。
- 里程碑：[ReAct]·[Toolformer]·[SWE-bench/SWE-agent]·[UI-TARS](themes/agentic/ui-tars.md)·[Search-R1](themes/agentic/search-r1.md)·[Operator/CUA](themes/agentic/openai-computer-using-agent.md)·[Tongyi DeepResearch](themes/agentic/tongyi-deepresearch.md)

---

## 四、开源模型训练配方深挖（`deep-dive/`）

每份逐型号给出：架构精确 config · 预训练数据来源/token/配比 · 数据处理 pipeline(去重/质量过滤) · 训练(算力/并行/精度/阶段) · SFT · RL/对齐 · infra。横向对比见 [open-model-recipes.md](sections/open-model-recipes.md)。

- [DeepSeek](deep-dive/deepseek.md) — LLM/MoE/V2(MLA)/V3(FP8+DualPipe)/R1(RLVR)/Math(GRPO)/Coder/Prover/V3.1-3.2
- [Qwen 通义千问](deep-dive/qwen.md) — Qwen1→3、2.5/3-Coder/Math、Qwen3-Next、QwQ、VL/Omni
- [Llama](deep-dive/llama.md) — LLaMA1/2/3(Herd 全细节)、Code Llama、Llama Guard
- [OLMo/Dolma/Tülu](deep-dive/olmo-ai2.md) — **最透明全开**（数据+代码+配方+RL 全公开）
- [GLM/ChatGLM](deep-dive/glm.md) · [Mistral/Mixtral](deep-dive/mistral.md) · [Gemma](deep-dive/gemma.md)
- [MiniCPM](deep-dive/minicpm.md) — WSD 调度 + 数据退火细节最丰富
- [InternLM 书生](deep-dive/internlm.md) · [Yi 零一万物](deep-dive/yi.md)
- [Nemotron(NV)+Phi(MS)](deep-dive/nvidia-phi.md) — 合成数据 + 奖励模型 + 教科书数据
- [早期与全开](deep-dive/fully-open.md) — BLOOM/Pythia/GPT-NeoX/Falcon/MAP-Neo/OpenCoder/StarCoder/RedPajama/DCLM
- [新一代开源大 MoE](deep-dive/newgen-moe.md) — Kimi K2 / MiniMax-01 / Hunyuan-Large / Skywork-MoE / Step / dots / Ling / Pangu MoE
- [预训练数据集与处理 pipeline 专题](deep-dive/data-pipelines.md) — FineWeb/DCLM/The Stack/RedPajama/Dolma/Nemotron-CC 的去重·质量过滤·配比·消融

---

## 五、年度时间线（里程碑精选，全条目见 [01-INDEX.md](01-INDEX.md)）

### 2020 — 缩放定律与 RLHF 萌芽
- [GPT-3 175B](2020/language-models-are-few-shot-learners-gpt-3.md)（few-shot 上下文学习）· [Scaling Laws](2020/scaling-laws-for-neural-language-models.md)
- [ZeRO/DeepSpeed](2020/zero-deepspeed-100b-parameters.md) + [ZeRO-2](2020/zero-2-deepspeed.md) · [Turing-NLG 17B](2020/turing-nlg-microsoft.md)
- [Learning to summarize from HF](2020/learning-to-summarize-from-human-feedback.md)（RLHF 奠基）· GShard(MoE) · [DeBERTa](2020/deberta.md) · [Meena](2020/meena-towards-human-like-open-domain-chatbot.md) · CPM(中文) · [OpenAI API](2020/openai-api-launch.md)

### 2021 — 规模化、MoE、指令微调起步
- [Switch Transformer] · GLaM · [Gopher] · Megatron-Turing NLG 530B
- FLAN / T0（指令微调）· [Codex] · [WebGPT] · Anthropic "A General Language Assistant"
- 中国：ERNIE 3.0 · PanGu-α · Yuan 1.0 · Wudao 2.0 · RoPE · ALiBi · ZeRO-Infinity

### 2022 — Chinchilla、RLHF 产品化、CoT、开源潮
- [Chinchilla 计算最优](2022/chinchilla-training-compute-optimal-large-language-models.md) · PaLM · OPT · BLOOM · GLM-130B
- InstructGPT(RLHF) · Chain-of-Thought · Self-Consistency · Emergent Abilities
- FlashAttention · ReAct · Anthropic HH-RLHF + Constitutional AI · **ChatGPT 发布**

### 2023 — GPT-4、开源基座爆发、对齐与 agent 工具化
- 美/西：[GPT-4] · LLaMA / Llama 2 · PaLM 2 · Claude 2 · Gemini · Mistral 7B · [DPO](themes/post-training/dpo.md) · QLoRA · [vLLM/PagedAttention] · Mamba · Toolformer/Reflexion/Voyager · SWE-bench
- 中国：Qwen · Baichuan 2 · InternLM · ChatGLM2/3 · Yi · DeepSeek LLM/Coder/MoE · Qwen-VL

### 2024 — 多模态旗舰、推理起步、MoE 工程化、数据全开
- 美/西：[Llama 3 Herd](2024/llama-3-herd-of-models.md) · [GPT-4o] · [o1 推理](2024/openai-learning-to-reason-with-llms.md) · Claude 3/3.5 · Gemini 1.5 · Gemma 2 · [OLMo+Dolma] · [FineWeb] · Tülu 3 · Nemotron-4 340B · SimPO/KTO/ORPO
- 中国：[DeepSeek-V2(MLA)] · [DeepSeek-V3] · [DeepSeekMath GRPO] · Qwen2/2.5 · GLM-4 · MiniCPM · InternLM2 · Hunyuan-Large · Skywork-MoE

### 2025 — 推理模型规模化 + agentic RL 爆发 + 万亿开源 MoE
- 美/西：[DeepSeek-R1 冲击](2025/deepseek-r1.md)（虽中国，引爆全行业）· [o3/o4-mini](themes/agentic/openai-o3-o4-mini.md) · [GPT-4.5](2025/openai-gpt-4.5-system-card.md) · [GPT-5](2025/openai-gpt-5-system-card.md) · [gpt-oss 开源](2025/openai-gpt-oss.md) · [Claude 3.7](2025/anthropic-claude-3-7-sonnet.md)/[Claude 4](2025/anthropic-claude-4.md) · [Gemini 2.5](2025/gemini-2.5.md) · [Llama 4](2025/meta-llama-4.md) · [Grok 3](2025/xai-grok-3.md)/[4](2025/xai-grok-4.md) · Gemma 3 · [Nemotron-H](2025/nemotron-h.md)
- 中国：[Kimi k1.5](2025/kimi-k1.5.md)/[K2](2025/kimi-k2.md) · [Qwen3](2025/qwen3.md)/[Coder](2025/qwen3-coder.md)/[Next](2025/qwen3-next.md) · [QwQ-32B](2025/qwq-32b.md) · [GLM-4.5](2025/glm-4.5.md)/[4.6](2025/glm-4.6.md) · [MiniMax-01](2025/minimax-01.md)/[M1](2025/minimax-m1.md) · [DeepSeek-V3.1](2025/deepseek-v3.1.md)/[V3.2 稀疏注意力](2025/deepseek-v3.2.md) · [Hunyuan-TurboS](2025/hunyuan-turbos.md) · [Pangu Ultra/Pro/Ultra-MoE](2025/pangu-ultra-moe.md) · [MiMo(小米)](2025/xiaomi-mimo.md) · [LongCat(美团)](2025/longcat-flash.md) · [Ling/Ring(蚂蚁)](2025/ling-2.0.md) · [Step-3](2025/step-3.md) · [Seed1.5-Thinking](2025/seed1.5-thinking.md)
- infra/RL：DeepSeek 开源周(FlashMLA/DeepEP/DeepGEMM/[DualPipe]/[3FS]) · [Native Sparse Attention](themes/ai-infra/native-sparse-attention.md) · DAPO/[AReaL](themes/ai-infra/areal.md)/ProRL · agent RL：[Search-R1](themes/agentic/search-r1.md)/[ReTool](themes/agentic/retool.md)/[RAGEN](themes/agentic/ragen.md)/[Tongyi DeepResearch](themes/agentic/tongyi-deepresearch.md)

### 2026 H1 — 百万上下文、万亿 MoE 普及、原生 agentic/omni（实时检索所得，见下方说明）
- 美/西：[DeepSeek-V4 百万上下文](2026/deepseek-v4-technical-report.md) · [GPT-5.5](2026/introducing-gpt-5-5.md)/[GPT-Rosalind](2026/gpt-rosalind.md) · [Gemini 3 Pro](2026/gemini-3-pro-model-card.md)/[3.5 Flash](2026/gemini-3-5-flash-model-card.md) · [Claude Opus 4.6](2026/anthropic-risk-report-feb-2026.md) · [Llama Muse Spark(MSL)](2026/meta-muse-spark.md) · [Nemotron 3 Super/Ultra](2026/nemotron-3-ultra.md) · [Mistral Medium 3.5](2026/mistral-medium-3-5.md)
- 中国：[ERNIE 5.0](2026/ernie-5.0-technical-report.md) · [GLM-5](2026/glm-5-vibe-coding-to-agentic-engineering.md) · [Kimi K2.5](2026/kimi-k2.5-visual-agentic-intelligence.md) · [Qwen3.5](2026/qwen3.5-397b-a17b.md)/[Omni](2026/qwen3.5-omni-technical-report.md) · [MiniMax-M2](2026/minimax-m2-series.md)/[Sparse Attention](2026/minimax-sparse-attention.md) · [Ling/Ring 2.6 万亿](2026/ling-ring-2.6-technical-report.md) · [openPangu-Ultra-MoE-718B](2026/openpangu-ultra-moe-718b.md) · [Hunyuan 3 preview](2026/hunyuan-3-preview.md) · [MiMo-V2.5-Pro](2026/mimo-v2.5-pro.md) · [Intern-S1-Pro](2026/intern-s1-pro.md) · [LongCat-Next](2026/longcat-next.md)
- **增量补录（2026-05 后查漏 + 读全论文深挖六维）**：[GLM-5.2](2026/glm-5.2.md)（IndexShare/1M）· [Kimi-K2.6](2026/kimi-k2.6.md)（1T MoE/agent swarm）· [MiniMax-M3](2026/minimax-m3.md)（MSA）· [Qwen-AgentWorld](2026/qwen-agentworld.md)（首个语言世界模型）· [Intern-S2-Preview](2026/intern-s2-preview.md)（task scaling）· [MiniCPM5-1B](2026/minicpm5-1b.md)（端侧 1B SOTA）· [Mistral-Small-4](2026/mistral-small-4.md)（三族统一，2026-03）

---

## 六、方法与局限

**方法**：两阶段、多 agent 并行编排。
- 阶段一（15 agent）：按年 × 中美双轨 + 4 跨年专题，检索一手来源、下载原文、写结构化页 → 初版 5 分类综合。
- 阶段二（30 agent）：补两个中途失败的 scope（2025 美/西方、2024 中国）+ 全 scope 查漏补缺 + 14 个开源家族深挖 + **从磁盘重读**重做 6 篇综合（修掉初版漏 agent 的问题）。

**局限与注意**：
- **2025 下半年 → 2026 的条目完全来自 agent 实时联网检索，超出本模型自身知识截止**，无法逐条独立背书。已做下载完整性抽检：约 760 份原文真实落盘 ~2.6GB（含 2026 的 14MB 级官方 system card / 多份 arXiv PDF），可信度较高；但**最新/最意外的条目（如 GPT-Rosalind、Muse Spark、DeepSeek-V4 等）建议按需打开原文复核**。
- **第三轮补强（本次 review）**：对 2026-05 后查漏出的 7 个模型，凡有论文/报告的均已**读全一手原文**写入六维（GLM-5/Qwen-AgentWorld/MSA/Kimi-K2.5 报告）；7 个模型已并入年度时间线与各分类章节末尾的「增量补录」。`sections/` 主体仍为前两阶段（532 条中的 525 条）综合，增量 7 条以补录段 + 各自专页 + 01-INDEX 体现。
- 跨 agent 难免少量重复；综合章节已按 URL 去重，年份目录与 `themes/` 仍可能并存同一工作（互为入口）。
- 个别 frontmatter 分类标签未严格归一（如英文 `post-training`、`agentic环境与数据`）；综合章节已归到 5 大类。
- 全库 5 个 <2KB 小文件（个别下载失败/极简 README），不影响主体。
- 严格只收官方一手；凡检索不到可验证 URL 的均未收录，未臆造。
