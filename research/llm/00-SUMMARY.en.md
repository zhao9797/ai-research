> 🌐 English entry page. Deep pages are in Chinese. 中文版 / Chinese: [[llm/00-SUMMARY|中文]]

---
title: LLM Technology Evolution Research (GPT-3 → 2026-06) · Main Summary
type: source
tags: [llm, survey, pretraining, architecture, ai-infra, post-training, agentic]
created: 2026-06-18
updated: 2026-06-18
---

# LLM Technology Evolution Research · Main Summary (GPT-3 2020-05 → 2026-06)

> Primary official sources only: original arXiv papers, official technical reports/system cards, official blogs, official GitHub/model cards/HF organization pages.
> **No third-party interpretations/translations/secondary summaries/benchmark aggregations.**
> Five categories: `pretraining data` · `architecture` · `AI infra` · `post-training` · `agentic training` (each entry hits at least one; may be multi-tagged).

---

## 1. Corpus Statistics

- **Sources after deduplication**: **532 entries** (parsed from 667 structured pages, deduplicated by original URL)
- **Downloaded primary sources**: about **760 files / ~2.6 GB** — `*.html/json` ship with the repo (`sources/llm/<scope>/`); **`*.pdf` lives on the HF private bucket `jaczhao/ai-research-sources` (storage-compute separation, not in git)**
- **Open-source model deep-dive archives**: 14 files (`deep-dive/`, including a "2026 post-research incremental addendum" section)
- **Categorical summary chapters**: 6 (`sections/`, with a 2026 incremental addendum appended)

**By year (deduplicated)**: 2018→1 · 2019→4 · 2020→36 · 2021→32 · 2022→58 · 2023→102 · 2024→136 · 2025→110 · 2026(H1)→53

**By country (deduplicated)**: US/West 303 · China 196 · Europe 20 · Other ~13 — all top Chinese and US companies covered

**By category (deduplicated, multi-tag)**: architecture ~298 · post-training ~283 · AI infra ~180 · pretraining data ~178 · agentic training ~143

---

## 2. How to Read This Research

Four layers, by granularity from "conclusion" to "primary source":

1. **Five categorical summaries (core, read these first)** — `sections/`
   - [[llm/sections/pretrain-data|Pretraining data]]
   - [[llm/sections/architecture|Architecture]]
   - [[llm/sections/ai-infra|AI infra]]
   - [[llm/sections/post-training|Post-training]]
   - [[llm/sections/agentic|Agentic training]]
   - [[llm/sections/open-model-recipes|Open-source model training recipes (cross-comparison)]]
2. **Open-source model deep-dive archives (for training/data/mixture-ratio/RL/architecture details)** — `deep-dive/` (see Section 4)
3. **Full source index (by year/month, every entry clickable)** — [[llm/01-INDEX|01-INDEX]]
4. **Per-entry structured pages** — `2020/`…`2026/`, `themes/`; **downloaded primary sources** — `sources/llm/<scope>/` (html/json with the repo, pdf on HF bucket)

---

## 3. Quick Overview of the Five Categories

### 1) Pretraining Data → [[llm/sections/pretrain-data|full chapter]] (173 entries)
From GPT-3's coarse-filtered CommonCrawl (~300B tokens) → quality classifiers and deduplication becoming standard (The Pile, C4, RefinedWeb) → recipes going public (LLaMA mixture ratios, Dolma/RedPajama fully open) → **data quality > data quantity** (Phi "textbooks", FineWeb-Edu edu classifier, DCLM) → multi-stage/annealing and synthetic data (MiniCPM WSD, Nemotron synthetic, Llama 3 15T+annealing) → trillion-to-tens-of-trillions tokens, long-context stages, strong decontamination.
- Milestones: [[llm/2020/scaling-laws-for-neural-language-models|Scaling Laws]] · [[llm/2022/chinchilla-training-compute-optimal-large-language-models|Chinchilla compute-optimal]] · [The Pile] · [LLaMA] · [[llm/deep-dive/data-pipelines|Dolma]] · [[llm/deep-dive/data-pipelines|FineWeb/FineWeb-Edu]] · [[llm/deep-dive/data-pipelines|DCLM]] · [Phi Textbooks]

### 2) Architecture → [[llm/sections/architecture|full chapter]] (291 entries)
Decoder-only Transformer settling in → positional encodings RoPE/ALiBi/YaRN → memory-saving attention MQA/GQA→**MLA** (DeepSeek-V2) → **MoE going mainstream**: GShard/Switch/GLaM → DeepSeekMoE fine-grained + shared experts → auxiliary-loss-free load balancing → trillion-scale sparse (Kimi K2, Ling/Ring-1T, Pangu Ultra-MoE 718B) → linear/hybrid architectures (Mamba, RWKV, RetNet, Jamba, Nemotron-H, MiniMax Lightning/Sparse, Kimi Linear, Falcon-H1) → native multimodal/omni and native sparse attention.
- Milestones: [GShard]·[Switch]·[GLaM]·[[llm/deep-dive/deepseek|DeepSeekMoE]]·[Mamba]·[[llm/deep-dive/deepseek|MLA/DeepSeek-V2]]·[aux-loss-free MoE]·[[llm/themes/ai-infra/native-sparse-attention|Native Sparse Attention]]·[Jamba]·[[llm/2025/nemotron-h|Nemotron-H]]

### 3) AI infra → [[llm/sections/ai-infra|full chapter]] (175 entries)
Training side: Megatron-LM tensor parallelism + DeepSpeed/ZeRO memory sharding → 3D/sequence parallelism, activation recomputation → FP8 training, MegaScale ten-thousand-card → **DeepSeek-V3 FP8+DualPipe** open-sourcing the full stack (open-source week FlashMLA/DeepEP/DeepGEMM/3FS). Inference side: FlashAttention 1/2/3 → PagedAttention/vLLM → SGLang/RadixAttention → quantization (GPTQ/AWQ/SmoothQuant) → PD disaggregation/Mooncake/MegaScale-Infer. RL training systems: DeepSpeed-Chat→OpenRLHF→veRL/HybridFlow→DAPO/AReaL/ProRL.
- Milestones: [[llm/2020/zero-deepspeed-100b-parameters|ZeRO/DeepSpeed]]·[Megatron activation recomputation]·[FlashAttention]·[vLLM/PagedAttention]·[[llm/themes/ai-infra/deepseek-v3-hardware|DeepSeek-V3 hardware reflections]]·[[llm/themes/ai-infra/deepseek-open-infra-index|DeepSeek open-source week]]·[veRL/HybridFlow]

### 4) Post-training → [[llm/sections/post-training|full chapter]] (276 entries)
RLHF foundations ([[llm/2020/learning-to-summarize-from-human-feedback|Learning to summarize]]→InstructGPT) → Constitutional AI/RLAIF → **offline preference optimization** DPO and variants (IPO/KTO/ORPO/SimPO) → **verifiable-reward RLVR + GRPO** (DeepSeekMath) → **reasoning-model paradigm** (o1 → DeepSeek-R1 pure-RL "aha moment", Kimi k1.5) → process rewards PRM, long CoT, on-policy distillation, prolonged RL (ProRL) → fully open pipelines (Tülu 3, OLMo 2, MiMo, Nemotron Cascade).
- Milestones: [InstructGPT]·[[llm/themes/post-training/dpo|DPO]]·[Constitutional AI]·[[llm/deep-dive/deepseek|DeepSeekMath GRPO]]·[[llm/2025/deepseek-r1|DeepSeek-R1]]·[[llm/2025/kimi-k1.5|Kimi k1.5]]·[[llm/deep-dive/olmo-ai2|Tülu 3]]·[[llm/themes/post-training/on-policy-distillation|on-policy distillation]]

### 5) Agentic Training → [[llm/sections/agentic|full chapter]] (136 entries)
Prompt era (WebGPT/ReAct/Toolformer/Reflexion/Voyager/Generative Agents) → tool-use fine-tuning (ToolLLM/AgentTuning/CodeAct) → evaluation-driven (SWE-bench/WebArena/OSWorld/tau-bench) → **computer/browser use** (Claude computer use, Operator/CUA, UI-TARS) → **multi-turn agent RL explosion (2025)** (Search-R1/ReTool/RAGEN/ToolRL/DeepResearcher/WebSailor) → agentic-native models (Kimi K2, GLM-4.5 ARC, Qwen3-Coder, Tongyi DeepResearch, Seed2.0).
- Milestones: [ReAct]·[Toolformer]·[SWE-bench/SWE-agent]·[[llm/themes/agentic/ui-tars|UI-TARS]]·[[llm/themes/agentic/search-r1|Search-R1]]·[[llm/themes/agentic/openai-computer-using-agent|Operator/CUA]]·[[llm/themes/agentic/tongyi-deepresearch|Tongyi DeepResearch]]

---

## 4. Open-Source Model Training Recipe Deep Dives (`deep-dive/`)

Each gives, model by model: exact architecture config · pretraining data sources/tokens/mixture ratios · data processing pipeline (deduplication/quality filtering) · training (compute/parallelism/precision/stages) · SFT · RL/alignment · infra. For cross-comparison see [[llm/sections/open-model-recipes|open-model-recipes.md]].

- [[llm/deep-dive/deepseek|DeepSeek]] — LLM/MoE/V2(MLA)/V3(FP8+DualPipe)/R1(RLVR)/Math(GRPO)/Coder/Prover/V3.1-3.2
- [[llm/deep-dive/qwen|Qwen / Tongyi Qianwen]] — Qwen1→3, 2.5/3-Coder/Math, Qwen3-Next, QwQ, VL/Omni
- [[llm/deep-dive/llama|Llama]] — LLaMA1/2/3 (Herd full details), Code Llama, Llama Guard
- [[llm/deep-dive/olmo-ai2|OLMo/Dolma/Tülu]] — **the most transparent, fully open** (data + code + recipe + RL all public)
- [[llm/deep-dive/glm|GLM/ChatGLM]] · [[llm/deep-dive/mistral|Mistral/Mixtral]] · [[llm/deep-dive/gemma|Gemma]]
- [[llm/deep-dive/minicpm|MiniCPM]] — richest detail on WSD scheduling + data annealing
- [[llm/deep-dive/internlm|InternLM]] · [[llm/deep-dive/yi|Yi / 01.AI]]
- [[llm/deep-dive/nvidia-phi|Nemotron(NV)+Phi(MS)]] — synthetic data + reward models + textbook data
- [[llm/deep-dive/fully-open|Early and fully open]] — BLOOM/Pythia/GPT-NeoX/Falcon/MAP-Neo/OpenCoder/StarCoder/RedPajama/DCLM
- [[llm/deep-dive/newgen-moe|New-generation large open MoE]] — Kimi K2 / MiniMax-01 / Hunyuan-Large / Skywork-MoE / Step / dots / Ling / Pangu MoE
- [[llm/deep-dive/data-pipelines|Pretraining dataset & processing pipeline topic]] — deduplication · quality filtering · mixture ratios · ablations of FineWeb/DCLM/The Stack/RedPajama/Dolma/Nemotron-CC

---

## 5. Annual Timeline (selected milestones; full entries in [[llm/01-INDEX|01-INDEX]])

### 2020 — Scaling laws and the dawn of RLHF
- [[llm/2020/language-models-are-few-shot-learners-gpt-3|GPT-3 175B]] (few-shot in-context learning) · [[llm/2020/scaling-laws-for-neural-language-models|Scaling Laws]]
- [[llm/2020/zero-deepspeed-100b-parameters|ZeRO/DeepSpeed]] + [[llm/2020/zero-2-deepspeed|ZeRO-2]] · [[llm/2020/turing-nlg-microsoft|Turing-NLG 17B]]
- [[llm/2020/learning-to-summarize-from-human-feedback|Learning to summarize from HF]] (RLHF foundations) · GShard(MoE) · [[llm/2020/deberta|DeBERTa]] · [[llm/2020/meena-towards-human-like-open-domain-chatbot|Meena]] · CPM(Chinese) · [[llm/2020/openai-api-launch|OpenAI API]]

### 2021 — Scaling up, MoE, instruction tuning takes off
- [Switch Transformer] · GLaM · [Gopher] · Megatron-Turing NLG 530B
- FLAN / T0 (instruction tuning) · [Codex] · [WebGPT] · Anthropic "A General Language Assistant"
- China: ERNIE 3.0 · PanGu-α · Yuan 1.0 · Wudao 2.0 · RoPE · ALiBi · ZeRO-Infinity

### 2022 — Chinchilla, RLHF productization, CoT, open-source wave
- [[llm/2022/chinchilla-training-compute-optimal-large-language-models|Chinchilla compute-optimal]] · PaLM · OPT · BLOOM · GLM-130B
- InstructGPT(RLHF) · Chain-of-Thought · Self-Consistency · Emergent Abilities
- FlashAttention · ReAct · Anthropic HH-RLHF + Constitutional AI · **ChatGPT launch**

### 2023 — GPT-4, explosion of open-source bases, alignment and agent tool-use
- US/West: [GPT-4] · LLaMA / Llama 2 · PaLM 2 · Claude 2 · Gemini · Mistral 7B · [[llm/themes/post-training/dpo|DPO]] · QLoRA · [vLLM/PagedAttention] · Mamba · Toolformer/Reflexion/Voyager · SWE-bench
- China: Qwen · Baichuan 2 · InternLM · ChatGLM2/3 · Yi · DeepSeek LLM/Coder/MoE · Qwen-VL

### 2024 — Multimodal flagships, reasoning takes off, MoE engineering, fully open data
- US/West: [[llm/2024/llama-3-herd-of-models|Llama 3 Herd]] · [GPT-4o] · [[llm/2024/openai-learning-to-reason-with-llms|o1 reasoning]] · Claude 3/3.5 · Gemini 1.5 · Gemma 2 · [OLMo+Dolma] · [FineWeb] · Tülu 3 · Nemotron-4 340B · SimPO/KTO/ORPO
- China: [DeepSeek-V2(MLA)] · [DeepSeek-V3] · [DeepSeekMath GRPO] · Qwen2/2.5 · GLM-4 · MiniCPM · InternLM2 · Hunyuan-Large · Skywork-MoE

### 2025 — Reasoning-model scaling + agentic RL explosion + trillion-scale open MoE
- US/West: [[llm/2025/deepseek-r1|DeepSeek-R1 shockwave]] (Chinese, but ignited the whole industry) · [[llm/themes/agentic/openai-o3-o4-mini|o3/o4-mini]] · [[llm/2025/openai-gpt-4.5-system-card|GPT-4.5]] · [[llm/2025/openai-gpt-5-system-card|GPT-5]] · [[llm/2025/openai-gpt-oss|gpt-oss open source]] · [[llm/2025/anthropic-claude-3-7-sonnet|Claude 3.7]]/[[llm/2025/anthropic-claude-4|Claude 4]] · [[llm/2025/gemini-2.5|Gemini 2.5]] · [[llm/2025/meta-llama-4|Llama 4]] · [[llm/2025/xai-grok-3|Grok 3]]/[[llm/2025/xai-grok-4|4]] · Gemma 3 · [[llm/2025/nemotron-h|Nemotron-H]]
- China: [[llm/2025/kimi-k1.5|Kimi k1.5]]/[[llm/2025/kimi-k2|K2]] · [[llm/2025/qwen3|Qwen3]]/[[llm/2025/qwen3-coder|Coder]]/[[llm/2025/qwen3-next|Next]] · [[llm/2025/qwq-32b|QwQ-32B]] · [[llm/2025/glm-4.5|GLM-4.5]]/[[llm/2025/glm-4.6|4.6]] · [[llm/2025/minimax-01|MiniMax-01]]/[[llm/2025/minimax-m1|M1]] · [[llm/2025/deepseek-v3.1|DeepSeek-V3.1]]/[[llm/2025/deepseek-v3.2|V3.2 sparse attention]] · [[llm/2025/hunyuan-turbos|Hunyuan-TurboS]] · [[llm/2025/pangu-ultra-moe|Pangu Ultra/Pro/Ultra-MoE]] · [[llm/2025/xiaomi-mimo|MiMo (Xiaomi)]] · [[llm/2025/longcat-flash|LongCat (Meituan)]] · [[llm/2025/ling-2.0|Ling/Ring (Ant)]] · [[llm/2025/step-3|Step-3]] · [[llm/2025/seed1.5-thinking|Seed1.5-Thinking]]
- infra/RL: DeepSeek open-source week (FlashMLA/DeepEP/DeepGEMM/[DualPipe]/[3FS]) · [[llm/themes/ai-infra/native-sparse-attention|Native Sparse Attention]] · DAPO/[[llm/themes/ai-infra/areal|AReaL]]/ProRL · agent RL: [[llm/themes/agentic/search-r1|Search-R1]]/[[llm/themes/agentic/retool|ReTool]]/[[llm/themes/agentic/ragen|RAGEN]]/[[llm/themes/agentic/tongyi-deepresearch|Tongyi DeepResearch]]

### 2026 H1 — Million-token context, trillion-scale MoE going mainstream, native agentic/omni
- US/West: [[llm/2026/deepseek-v4-technical-report|DeepSeek-V4 million-token context]] · [[llm/2026/introducing-gpt-5-5|GPT-5.5]]/[[llm/2026/gpt-rosalind|GPT-Rosalind]] · [[llm/2026/gemini-3-pro-model-card|Gemini 3 Pro]]/[[llm/2026/gemini-3-5-flash-model-card|3.5 Flash]] · [[llm/2026/anthropic-risk-report-feb-2026|Claude Opus 4.6]] · [[llm/2026/meta-muse-spark|Llama Muse Spark(MSL)]] · [[llm/2026/nemotron-3-ultra|Nemotron 3 Super/Ultra]] · [[llm/2026/mistral-medium-3-5|Mistral Medium 3.5]]
- China: [[llm/2026/ernie-5.0-technical-report|ERNIE 5.0]] · [[llm/2026/glm-5-vibe-coding-to-agentic-engineering|GLM-5]] · [[llm/2026/kimi-k2.5-visual-agentic-intelligence|Kimi K2.5]] · [[llm/2026/qwen3.5-397b-a17b|Qwen3.5]]/[[llm/2026/qwen3.5-omni-technical-report|Omni]] · [[llm/2026/minimax-m2-series|MiniMax-M2]]/[[llm/2026/minimax-sparse-attention|Sparse Attention]] · [[llm/2026/ling-ring-2.6-technical-report|Ling/Ring 2.6 trillion]] · [[llm/2026/openpangu-ultra-moe-718b|openPangu-Ultra-MoE-718B]] · [[llm/2026/hunyuan-3-preview|Hunyuan 3 preview]] · [[llm/2026/mimo-v2.5-pro|MiMo-V2.5-Pro]] · [[llm/2026/intern-s1-pro|Intern-S1-Pro]] · [[llm/2026/longcat-next|LongCat-Next]]
- **Incremental addendum (post-2026-05 gap-filling + full-paper six-dimension deep dives)**: [[llm/2026/glm-5.2|GLM-5.2]] (IndexShare/1M) · [[llm/2026/kimi-k2.6|Kimi-K2.6]] (1T MoE/agent swarm) · [[llm/2026/minimax-m3|MiniMax-M3]] (MSA) · [[llm/2026/qwen-agentworld|Qwen-AgentWorld]] (first language world model) · [[llm/2026/intern-s2-preview|Intern-S2-Preview]] (task scaling) · [[llm/2026/minicpm5-1b|MiniCPM5-1B]] (on-device 1B SOTA) · [[llm/2026/mistral-small-4|Mistral-Small-4]] (three families unified, 2026-03)
