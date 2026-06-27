---
title: 大模型技术演进调研 (GPT-3 → 2026-06) · 主汇总
type: source
tags: [llm, survey, pretraining, architecture, ai-infra, post-training, agentic]
created: 2026-06-18
updated: 2026-06-18
---

# 大模型技术演进调研 · 主汇总（GPT-3 2020-05 → 2026-06）

> 🌐 **English**: [[llm/00-SUMMARY.en|English]]

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
   - [[llm/sections/pretrain-data|预训练数据]]
   - [[llm/sections/architecture|架构]]
   - [[llm/sections/ai-infra|AI infra]]
   - [[llm/sections/post-training|后训练]]
   - [[llm/sections/agentic|agentic训练]]
   - [[llm/sections/open-model-recipes|开源模型训练配方（横向对比）]]
2. **开源模型深挖档案（要训练/数据/配比/RL/架构细节看这个）** — `deep-dive/`（见第四节）
3. **全量来源索引（按年月，可点开每条）** — [[llm/01-INDEX|01-INDEX]]
4. **单条结构化页** — `2020/`…`2026/`、`themes/`；**下载的原文** — `sources/llm/<scope>/`（html/json 随库，pdf 在 HF bucket）

---

## 三、五大分类脉络速览

### 1) 预训练数据 → [[llm/sections/pretrain-data|完整章节]]（173 条）
从 GPT-3 的 CommonCrawl 粗过滤（~300B token）→ 质量分类器与去重成为标配（The Pile、C4、RefinedWeb）→ 配方公开化（LLaMA 配比、Dolma/RedPajama 全开）→ **数据质量 > 数据量**（Phi "教科书"、FineWeb-Edu edu 分类器、DCLM）→ 多阶段/退火与合成数据（MiniCPM WSD、Nemotron 合成、Llama 3 15T+退火）→ 万亿-十万亿 token、长上下文阶段、强 decontamination。
- 里程碑：[[llm/2020/scaling-laws-for-neural-language-models|Scaling Laws]] · [[llm/2022/chinchilla-training-compute-optimal-large-language-models|Chinchilla 计算最优]] · [The Pile] · [LLaMA] · [[llm/deep-dive/data-pipelines|Dolma]] · [[llm/deep-dive/data-pipelines|FineWeb/FineWeb-Edu]] · [[llm/deep-dive/data-pipelines|DCLM]] · [Phi Textbooks]

### 2) 架构 → [[llm/sections/architecture|完整章节]]（291 条）
Decoder-only Transformer 定型 → 位置编码 RoPE/ALiBi/YaRN → 注意力省显存 MQA/GQA→**MLA**（DeepSeek-V2）→ **MoE 主流化**：GShard/Switch/GLaM → DeepSeekMoE 细粒度+共享专家 → 无辅助损失负载均衡 → 万亿稀疏（Kimi K2、Ling/Ring-1T、Pangu Ultra-MoE 718B）→ 线性/混合架构（Mamba、RWKV、RetNet、Jamba、Nemotron-H、MiniMax Lightning/Sparse、Kimi Linear、Falcon-H1）→ 原生多模态/omni 与 native sparse attention。
- 里程碑：[GShard]·[Switch]·[GLaM]·[[llm/deep-dive/deepseek|DeepSeekMoE]]·[Mamba]·[[llm/deep-dive/deepseek|MLA/DeepSeek-V2]]·[aux-loss-free MoE]·[[llm/themes/ai-infra/native-sparse-attention|Native Sparse Attention]]·[Jamba]·[[llm/2025/nemotron-h|Nemotron-H]]

### 3) AI infra → [[llm/sections/ai-infra|完整章节]]（175 条）
训练侧：Megatron-LM 张量并行 + DeepSpeed/ZeRO 显存分片 → 3D/序列并行、激活重算 → FP8 训练、MegaScale 万卡 → **DeepSeek-V3 FP8+DualPipe** 开源整套（开源周 FlashMLA/DeepEP/DeepGEMM/3FS）。推理侧：FlashAttention 1/2/3 → PagedAttention/vLLM → SGLang/RadixAttention → 量化(GPTQ/AWQ/SmoothQuant) → PD 分离/Mooncake/MegaScale-Infer。RL 训练系统：DeepSpeed-Chat→OpenRLHF→veRL/HybridFlow→DAPO/AReaL/ProRL。
- 里程碑：[[llm/2020/zero-deepspeed-100b-parameters|ZeRO/DeepSpeed]]·[Megatron 激活重算]·[FlashAttention]·[vLLM/PagedAttention]·[[llm/themes/ai-infra/deepseek-v3-hardware|DeepSeek-V3 硬件反思]]·[[llm/themes/ai-infra/deepseek-open-infra-index|DeepSeek 开源周]]·[veRL/HybridFlow]

### 4) 后训练 → [[llm/sections/post-training|完整章节]]（276 条）
RLHF 奠基（[[llm/2020/learning-to-summarize-from-human-feedback|Learning to summarize]]→InstructGPT）→ Constitutional AI/RLAIF → **离线偏好优化** DPO 及变体(IPO/KTO/ORPO/SimPO) → **可验证奖励 RLVR + GRPO**（DeepSeekMath）→ **推理模型范式**（o1 → DeepSeek-R1 纯 RL "顿悟"，Kimi k1.5）→ 过程奖励 PRM、长 CoT、on-policy 蒸馏、prolonged RL（ProRL）→ 全流程开放（Tülu 3、OLMo 2、MiMo、Nemotron Cascade）。
- 里程碑：[InstructGPT]·[[llm/themes/post-training/dpo|DPO]]·[Constitutional AI]·[[llm/deep-dive/deepseek|DeepSeekMath GRPO]]·[[llm/2025/deepseek-r1|DeepSeek-R1]]·[[llm/2025/kimi-k1.5|Kimi k1.5]]·[[llm/deep-dive/olmo-ai2|Tülu 3]]·[[llm/themes/post-training/on-policy-distillation|on-policy distillation]]

### 5) agentic 训练 → [[llm/sections/agentic|完整章节]]（136 条）
prompt 时代（WebGPT/ReAct/Toolformer/Reflexion/Voyager/Generative Agents）→ tool-use 微调（ToolLLM/AgentTuning/CodeAct）→ 评测驱动（SWE-bench/WebArena/OSWorld/tau-bench）→ **computer/browser use**（Claude computer use、Operator/CUA、UI-TARS）→ **多轮 agent RL 爆发(2025)**（Search-R1/ReTool/RAGEN/ToolRL/DeepResearcher/WebSailor）→ agentic 原生模型（Kimi K2、GLM-4.5 ARC、Qwen3-Coder、Tongyi DeepResearch、Seed2.0）。
- 里程碑：[ReAct]·[Toolformer]·[SWE-bench/SWE-agent]·[[llm/themes/agentic/ui-tars|UI-TARS]]·[[llm/themes/agentic/search-r1|Search-R1]]·[[llm/themes/agentic/openai-computer-using-agent|Operator/CUA]]·[[llm/themes/agentic/tongyi-deepresearch|Tongyi DeepResearch]]

---

## 四、开源模型训练配方深挖（`deep-dive/`）

每份逐型号给出：架构精确 config · 预训练数据来源/token/配比 · 数据处理 pipeline(去重/质量过滤) · 训练(算力/并行/精度/阶段) · SFT · RL/对齐 · infra。横向对比见 [[llm/sections/open-model-recipes|open-model-recipes.md]]。

- [[llm/deep-dive/deepseek|DeepSeek]] — LLM/MoE/V2(MLA)/V3(FP8+DualPipe)/R1(RLVR)/Math(GRPO)/Coder/Prover/V3.1-3.2
- [[llm/deep-dive/qwen|Qwen 通义千问]] — Qwen1→3、2.5/3-Coder/Math、Qwen3-Next、QwQ、VL/Omni
- [[llm/deep-dive/llama|Llama]] — LLaMA1/2/3(Herd 全细节)、Code Llama、Llama Guard
- [[llm/deep-dive/olmo-ai2|OLMo/Dolma/Tülu]] — **最透明全开**（数据+代码+配方+RL 全公开）
- [[llm/deep-dive/glm|GLM/ChatGLM]] · [[llm/deep-dive/mistral|Mistral/Mixtral]] · [[llm/deep-dive/gemma|Gemma]]
- [[llm/deep-dive/minicpm|MiniCPM]] — WSD 调度 + 数据退火细节最丰富
- [[llm/deep-dive/internlm|InternLM 书生]] · [[llm/deep-dive/yi|Yi 零一万物]]
- [[llm/deep-dive/nvidia-phi|Nemotron(NV)+Phi(MS)]] — 合成数据 + 奖励模型 + 教科书数据
- [[llm/deep-dive/fully-open|早期与全开]] — BLOOM/Pythia/GPT-NeoX/Falcon/MAP-Neo/OpenCoder/StarCoder/RedPajama/DCLM
- [[llm/deep-dive/newgen-moe|新一代开源大 MoE]] — Kimi K2 / MiniMax-01 / Hunyuan-Large / Skywork-MoE / Step / dots / Ling / Pangu MoE
- [[llm/deep-dive/data-pipelines|预训练数据集与处理 pipeline 专题]] — FineWeb/DCLM/The Stack/RedPajama/Dolma/Nemotron-CC 的去重·质量过滤·配比·消融

---

## 五、年度时间线（里程碑精选，全条目见 [[llm/01-INDEX|01-INDEX]]）

### 2020 — 缩放定律与 RLHF 萌芽
- [[llm/2020/language-models-are-few-shot-learners-gpt-3|GPT-3 175B]]（few-shot 上下文学习）· [[llm/2020/scaling-laws-for-neural-language-models|Scaling Laws]]
- [[llm/2020/zero-deepspeed-100b-parameters|ZeRO/DeepSpeed]] + [[llm/2020/zero-2-deepspeed|ZeRO-2]] · [[llm/2020/turing-nlg-microsoft|Turing-NLG 17B]]
- [[llm/2020/learning-to-summarize-from-human-feedback|Learning to summarize from HF]]（RLHF 奠基）· GShard(MoE) · [[llm/2020/deberta|DeBERTa]] · [[llm/2020/meena-towards-human-like-open-domain-chatbot|Meena]] · CPM(中文) · [[llm/2020/openai-api-launch|OpenAI API]]

### 2021 — 规模化、MoE、指令微调起步
- [Switch Transformer] · GLaM · [Gopher] · Megatron-Turing NLG 530B
- FLAN / T0（指令微调）· [Codex] · [WebGPT] · Anthropic "A General Language Assistant"
- 中国：ERNIE 3.0 · PanGu-α · Yuan 1.0 · Wudao 2.0 · RoPE · ALiBi · ZeRO-Infinity

### 2022 — Chinchilla、RLHF 产品化、CoT、开源潮
- [[llm/2022/chinchilla-training-compute-optimal-large-language-models|Chinchilla 计算最优]] · PaLM · OPT · BLOOM · GLM-130B
- InstructGPT(RLHF) · Chain-of-Thought · Self-Consistency · Emergent Abilities
- FlashAttention · ReAct · Anthropic HH-RLHF + Constitutional AI · **ChatGPT 发布**

### 2023 — GPT-4、开源基座爆发、对齐与 agent 工具化
- 美/西：[GPT-4] · LLaMA / Llama 2 · PaLM 2 · Claude 2 · Gemini · Mistral 7B · [[llm/themes/post-training/dpo|DPO]] · QLoRA · [vLLM/PagedAttention] · Mamba · Toolformer/Reflexion/Voyager · SWE-bench
- 中国：Qwen · Baichuan 2 · InternLM · ChatGLM2/3 · Yi · DeepSeek LLM/Coder/MoE · Qwen-VL

### 2024 — 多模态旗舰、推理起步、MoE 工程化、数据全开
- 美/西：[[llm/2024/llama-3-herd-of-models|Llama 3 Herd]] · [GPT-4o] · [[llm/2024/openai-learning-to-reason-with-llms|o1 推理]] · Claude 3/3.5 · Gemini 1.5 · Gemma 2 · [OLMo+Dolma] · [FineWeb] · Tülu 3 · Nemotron-4 340B · SimPO/KTO/ORPO
- 中国：[DeepSeek-V2(MLA)] · [DeepSeek-V3] · [DeepSeekMath GRPO] · Qwen2/2.5 · GLM-4 · MiniCPM · InternLM2 · Hunyuan-Large · Skywork-MoE

### 2025 — 推理模型规模化 + agentic RL 爆发 + 万亿开源 MoE
- 美/西：[[llm/2025/deepseek-r1|DeepSeek-R1 冲击]]（虽中国，引爆全行业）· [[llm/themes/agentic/openai-o3-o4-mini|o3/o4-mini]] · [[llm/2025/openai-gpt-4.5-system-card|GPT-4.5]] · [[llm/2025/openai-gpt-5-system-card|GPT-5]] · [[llm/2025/openai-gpt-oss|gpt-oss 开源]] · [[llm/2025/anthropic-claude-3-7-sonnet|Claude 3.7]]/[[llm/2025/anthropic-claude-4|Claude 4]] · [[llm/2025/gemini-2.5|Gemini 2.5]] · [[llm/2025/meta-llama-4|Llama 4]] · [[llm/2025/xai-grok-3|Grok 3]]/[[llm/2025/xai-grok-4|4]] · Gemma 3 · [[llm/2025/nemotron-h|Nemotron-H]]
- 中国：[[llm/2025/kimi-k1.5|Kimi k1.5]]/[[llm/2025/kimi-k2|K2]] · [[llm/2025/qwen3|Qwen3]]/[[llm/2025/qwen3-coder|Coder]]/[[llm/2025/qwen3-next|Next]] · [[llm/2025/qwq-32b|QwQ-32B]] · [[llm/2025/glm-4.5|GLM-4.5]]/[[llm/2025/glm-4.6|4.6]] · [[llm/2025/minimax-01|MiniMax-01]]/[[llm/2025/minimax-m1|M1]] · [[llm/2025/deepseek-v3.1|DeepSeek-V3.1]]/[[llm/2025/deepseek-v3.2|V3.2 稀疏注意力]] · [[llm/2025/hunyuan-turbos|Hunyuan-TurboS]] · [[llm/2025/pangu-ultra-moe|Pangu Ultra/Pro/Ultra-MoE]] · [[llm/2025/xiaomi-mimo|MiMo(小米)]] · [[llm/2025/longcat-flash|LongCat(美团)]] · [[llm/2025/ling-2.0|Ling/Ring(蚂蚁)]] · [[llm/2025/step-3|Step-3]] · [[llm/2025/seed1.5-thinking|Seed1.5-Thinking]]
- infra/RL：DeepSeek 开源周(FlashMLA/DeepEP/DeepGEMM/[DualPipe]/[3FS]) · [[llm/themes/ai-infra/native-sparse-attention|Native Sparse Attention]] · DAPO/[[llm/themes/ai-infra/areal|AReaL]]/ProRL · agent RL：[[llm/themes/agentic/search-r1|Search-R1]]/[[llm/themes/agentic/retool|ReTool]]/[[llm/themes/agentic/ragen|RAGEN]]/[[llm/themes/agentic/tongyi-deepresearch|Tongyi DeepResearch]]

### 2026 H1 — 百万上下文、万亿 MoE 普及、原生 agentic/omni
- 美/西：[[llm/2026/deepseek-v4-technical-report|DeepSeek-V4 百万上下文]] · [[llm/2026/introducing-gpt-5-5|GPT-5.5]]/[[llm/2026/gpt-rosalind|GPT-Rosalind]] · [[llm/2026/gemini-3-pro-model-card|Gemini 3 Pro]]/[[llm/2026/gemini-3-5-flash-model-card|3.5 Flash]] · [[llm/2026/anthropic-risk-report-feb-2026|Claude Opus 4.6]] · [[llm/2026/meta-muse-spark|Llama Muse Spark(MSL)]] · [[llm/2026/nemotron-3-ultra|Nemotron 3 Super/Ultra]] · [[llm/2026/mistral-medium-3-5|Mistral Medium 3.5]]
- 中国：[[llm/2026/ernie-5.0-technical-report|ERNIE 5.0]] · [[llm/2026/glm-5-vibe-coding-to-agentic-engineering|GLM-5]] · [[llm/2026/kimi-k2.5-visual-agentic-intelligence|Kimi K2.5]] · [[llm/2026/qwen3.5-397b-a17b|Qwen3.5]]/[[llm/2026/qwen3.5-omni-technical-report|Omni]] · [[llm/2026/minimax-m2-series|MiniMax-M2]]/[[llm/2026/minimax-sparse-attention|Sparse Attention]] · [[llm/2026/ling-ring-2.6-technical-report|Ling/Ring 2.6 万亿]] · [[llm/2026/openpangu-ultra-moe-718b|openPangu-Ultra-MoE-718B]] · [[llm/2026/hunyuan-3-preview|Hunyuan 3 preview]] · [[llm/2026/mimo-v2.5-pro|MiMo-V2.5-Pro]] · [[llm/2026/intern-s1-pro|Intern-S1-Pro]] · [[llm/2026/longcat-next|LongCat-Next]]
- **增量补录（2026-05 后查漏 + 读全论文深挖六维）**：[[llm/2026/glm-5.2|GLM-5.2]]（IndexShare/1M）· [[llm/2026/kimi-k2.6|Kimi-K2.6]]（1T MoE/agent swarm）· [[llm/2026/minimax-m3|MiniMax-M3]]（MSA）· [[llm/2026/qwen-agentworld|Qwen-AgentWorld]]（首个语言世界模型）· [[llm/2026/intern-s2-preview|Intern-S2-Preview]]（task scaling）· [[llm/2026/minicpm5-1b|MiniCPM5-1B]]（端侧 1B SOTA）· [[llm/2026/mistral-small-4|Mistral-Small-4]]（三族统一，2026-03）
