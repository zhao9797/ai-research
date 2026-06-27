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
   - [Pretraining data](llm/sections/pretrain-data.md)
   - [Architecture](llm/sections/architecture.md)
   - [AI infra](llm/sections/ai-infra.md)
   - [Post-training](llm/sections/post-training.md)
   - [Agentic training](llm/sections/agentic.md)
   - [Open-source model training recipes (cross-comparison)](llm/sections/open-model-recipes.md)
2. **Open-source model deep-dive archives (for training/data/mixture-ratio/RL/architecture details)** — `deep-dive/` (see Section 4)
3. **Full source index (by year/month, every entry clickable)** — [[llm/01-INDEX|01-INDEX]]
4. **Per-entry structured pages** — `2020/`…`2026/`, `themes/`; **downloaded primary sources** — `sources/llm/<scope>/` (html/json with the repo, pdf on HF bucket)

---

## 3. Quick Overview of the Five Categories

### 1) Pretraining Data → [full chapter](llm/sections/pretrain-data.md) (173 entries)
From GPT-3's coarse-filtered CommonCrawl (~300B tokens) → quality classifiers and deduplication becoming standard (The Pile, C4, RefinedWeb) → recipes going public (LLaMA mixture ratios, Dolma/RedPajama fully open) → **data quality > data quantity** (Phi "textbooks", FineWeb-Edu edu classifier, DCLM) → multi-stage/annealing and synthetic data (MiniCPM WSD, Nemotron synthetic, Llama 3 15T+annealing) → trillion-to-tens-of-trillions tokens, long-context stages, strong decontamination.
- Milestones: [Scaling Laws](llm/2020/scaling-laws-for-neural-language-models.md) · [Chinchilla compute-optimal](llm/2022/chinchilla-training-compute-optimal-large-language-models.md) · [The Pile] · [LLaMA] · [Dolma](llm/deep-dive/data-pipelines.md) · [FineWeb/FineWeb-Edu](llm/deep-dive/data-pipelines.md) · [DCLM](llm/deep-dive/data-pipelines.md) · [Phi Textbooks]

### 2) Architecture → [full chapter](llm/sections/architecture.md) (291 entries)
Decoder-only Transformer settling in → positional encodings RoPE/ALiBi/YaRN → memory-saving attention MQA/GQA→**MLA** (DeepSeek-V2) → **MoE going mainstream**: GShard/Switch/GLaM → DeepSeekMoE fine-grained + shared experts → auxiliary-loss-free load balancing → trillion-scale sparse (Kimi K2, Ling/Ring-1T, Pangu Ultra-MoE 718B) → linear/hybrid architectures (Mamba, RWKV, RetNet, Jamba, Nemotron-H, MiniMax Lightning/Sparse, Kimi Linear, Falcon-H1) → native multimodal/omni and native sparse attention.
- Milestones: [GShard]·[Switch]·[GLaM]·[DeepSeekMoE](llm/deep-dive/deepseek.md)·[Mamba]·[MLA/DeepSeek-V2](llm/deep-dive/deepseek.md)·[aux-loss-free MoE]·[Native Sparse Attention](llm/themes/ai-infra/native-sparse-attention.md)·[Jamba]·[Nemotron-H](llm/2025/nemotron-h.md)

### 3) AI infra → [full chapter](llm/sections/ai-infra.md) (175 entries)
Training side: Megatron-LM tensor parallelism + DeepSpeed/ZeRO memory sharding → 3D/sequence parallelism, activation recomputation → FP8 training, MegaScale ten-thousand-card → **DeepSeek-V3 FP8+DualPipe** open-sourcing the full stack (open-source week FlashMLA/DeepEP/DeepGEMM/3FS). Inference side: FlashAttention 1/2/3 → PagedAttention/vLLM → SGLang/RadixAttention → quantization (GPTQ/AWQ/SmoothQuant) → PD disaggregation/Mooncake/MegaScale-Infer. RL training systems: DeepSpeed-Chat→OpenRLHF→veRL/HybridFlow→DAPO/AReaL/ProRL.
- Milestones: [ZeRO/DeepSpeed](llm/2020/zero-deepspeed-100b-parameters.md)·[Megatron activation recomputation]·[FlashAttention]·[vLLM/PagedAttention]·[DeepSeek-V3 hardware reflections](llm/themes/ai-infra/deepseek-v3-hardware.md)·[DeepSeek open-source week](llm/themes/ai-infra/deepseek-open-infra-index.md)·[veRL/HybridFlow]

### 4) Post-training → [full chapter](llm/sections/post-training.md) (276 entries)
RLHF foundations ([Learning to summarize](llm/2020/learning-to-summarize-from-human-feedback.md)→InstructGPT) → Constitutional AI/RLAIF → **offline preference optimization** DPO and variants (IPO/KTO/ORPO/SimPO) → **verifiable-reward RLVR + GRPO** (DeepSeekMath) → **reasoning-model paradigm** (o1 → DeepSeek-R1 pure-RL "aha moment", Kimi k1.5) → process rewards PRM, long CoT, on-policy distillation, prolonged RL (ProRL) → fully open pipelines (Tülu 3, OLMo 2, MiMo, Nemotron Cascade).
- Milestones: [InstructGPT]·[DPO](llm/themes/post-training/dpo.md)·[Constitutional AI]·[DeepSeekMath GRPO](llm/deep-dive/deepseek.md)·[DeepSeek-R1](llm/2025/deepseek-r1.md)·[Kimi k1.5](llm/2025/kimi-k1.5.md)·[Tülu 3](llm/deep-dive/olmo-ai2.md)·[on-policy distillation](llm/themes/post-training/on-policy-distillation.md)

### 5) Agentic Training → [full chapter](llm/sections/agentic.md) (136 entries)
Prompt era (WebGPT/ReAct/Toolformer/Reflexion/Voyager/Generative Agents) → tool-use fine-tuning (ToolLLM/AgentTuning/CodeAct) → evaluation-driven (SWE-bench/WebArena/OSWorld/tau-bench) → **computer/browser use** (Claude computer use, Operator/CUA, UI-TARS) → **multi-turn agent RL explosion (2025)** (Search-R1/ReTool/RAGEN/ToolRL/DeepResearcher/WebSailor) → agentic-native models (Kimi K2, GLM-4.5 ARC, Qwen3-Coder, Tongyi DeepResearch, Seed2.0).
- Milestones: [ReAct]·[Toolformer]·[SWE-bench/SWE-agent]·[UI-TARS](llm/themes/agentic/ui-tars.md)·[Search-R1](llm/themes/agentic/search-r1.md)·[Operator/CUA](llm/themes/agentic/openai-computer-using-agent.md)·[Tongyi DeepResearch](llm/themes/agentic/tongyi-deepresearch.md)

---

## 4. Open-Source Model Training Recipe Deep Dives (`deep-dive/`)

Each gives, model by model: exact architecture config · pretraining data sources/tokens/mixture ratios · data processing pipeline (deduplication/quality filtering) · training (compute/parallelism/precision/stages) · SFT · RL/alignment · infra. For cross-comparison see [open-model-recipes.md](llm/sections/open-model-recipes.md).

- [DeepSeek](llm/deep-dive/deepseek.md) — LLM/MoE/V2(MLA)/V3(FP8+DualPipe)/R1(RLVR)/Math(GRPO)/Coder/Prover/V3.1-3.2
- [Qwen / Tongyi Qianwen](llm/deep-dive/qwen.md) — Qwen1→3, 2.5/3-Coder/Math, Qwen3-Next, QwQ, VL/Omni
- [Llama](llm/deep-dive/llama.md) — LLaMA1/2/3 (Herd full details), Code Llama, Llama Guard
- [OLMo/Dolma/Tülu](llm/deep-dive/olmo-ai2.md) — **the most transparent, fully open** (data + code + recipe + RL all public)
- [GLM/ChatGLM](llm/deep-dive/glm.md) · [Mistral/Mixtral](llm/deep-dive/mistral.md) · [Gemma](llm/deep-dive/gemma.md)
- [MiniCPM](llm/deep-dive/minicpm.md) — richest detail on WSD scheduling + data annealing
- [InternLM](llm/deep-dive/internlm.md) · [Yi / 01.AI](llm/deep-dive/yi.md)
- [Nemotron(NV)+Phi(MS)](llm/deep-dive/nvidia-phi.md) — synthetic data + reward models + textbook data
- [Early and fully open](llm/deep-dive/fully-open.md) — BLOOM/Pythia/GPT-NeoX/Falcon/MAP-Neo/OpenCoder/StarCoder/RedPajama/DCLM
- [New-generation large open MoE](llm/deep-dive/newgen-moe.md) — Kimi K2 / MiniMax-01 / Hunyuan-Large / Skywork-MoE / Step / dots / Ling / Pangu MoE
- [Pretraining dataset & processing pipeline topic](llm/deep-dive/data-pipelines.md) — deduplication · quality filtering · mixture ratios · ablations of FineWeb/DCLM/The Stack/RedPajama/Dolma/Nemotron-CC

---

## 5. Annual Timeline (selected milestones; full entries in [[llm/01-INDEX|01-INDEX]])

### 2020 — Scaling laws and the dawn of RLHF
- [GPT-3 175B](llm/2020/language-models-are-few-shot-learners-gpt-3.md) (few-shot in-context learning) · [Scaling Laws](llm/2020/scaling-laws-for-neural-language-models.md)
- [ZeRO/DeepSpeed](llm/2020/zero-deepspeed-100b-parameters.md) + [ZeRO-2](llm/2020/zero-2-deepspeed.md) · [Turing-NLG 17B](llm/2020/turing-nlg-microsoft.md)
- [Learning to summarize from HF](llm/2020/learning-to-summarize-from-human-feedback.md) (RLHF foundations) · GShard(MoE) · [DeBERTa](llm/2020/deberta.md) · [Meena](llm/2020/meena-towards-human-like-open-domain-chatbot.md) · CPM(Chinese) · [OpenAI API](llm/2020/openai-api-launch.md)

### 2021 — Scaling up, MoE, instruction tuning takes off
- [Switch Transformer] · GLaM · [Gopher] · Megatron-Turing NLG 530B
- FLAN / T0 (instruction tuning) · [Codex] · [WebGPT] · Anthropic "A General Language Assistant"
- China: ERNIE 3.0 · PanGu-α · Yuan 1.0 · Wudao 2.0 · RoPE · ALiBi · ZeRO-Infinity

### 2022 — Chinchilla, RLHF productization, CoT, open-source wave
- [Chinchilla compute-optimal](llm/2022/chinchilla-training-compute-optimal-large-language-models.md) · PaLM · OPT · BLOOM · GLM-130B
- InstructGPT(RLHF) · Chain-of-Thought · Self-Consistency · Emergent Abilities
- FlashAttention · ReAct · Anthropic HH-RLHF + Constitutional AI · **ChatGPT launch**

### 2023 — GPT-4, explosion of open-source bases, alignment and agent tool-use
- US/West: [GPT-4] · LLaMA / Llama 2 · PaLM 2 · Claude 2 · Gemini · Mistral 7B · [DPO](llm/themes/post-training/dpo.md) · QLoRA · [vLLM/PagedAttention] · Mamba · Toolformer/Reflexion/Voyager · SWE-bench
- China: Qwen · Baichuan 2 · InternLM · ChatGLM2/3 · Yi · DeepSeek LLM/Coder/MoE · Qwen-VL

### 2024 — Multimodal flagships, reasoning takes off, MoE engineering, fully open data
- US/West: [Llama 3 Herd](llm/2024/llama-3-herd-of-models.md) · [GPT-4o] · [o1 reasoning](llm/2024/openai-learning-to-reason-with-llms.md) · Claude 3/3.5 · Gemini 1.5 · Gemma 2 · [OLMo+Dolma] · [FineWeb] · Tülu 3 · Nemotron-4 340B · SimPO/KTO/ORPO
- China: [DeepSeek-V2(MLA)] · [DeepSeek-V3] · [DeepSeekMath GRPO] · Qwen2/2.5 · GLM-4 · MiniCPM · InternLM2 · Hunyuan-Large · Skywork-MoE

### 2025 — Reasoning-model scaling + agentic RL explosion + trillion-scale open MoE
- US/West: [DeepSeek-R1 shockwave](llm/2025/deepseek-r1.md) (Chinese, but ignited the whole industry) · [o3/o4-mini](llm/themes/agentic/openai-o3-o4-mini.md) · [GPT-4.5](llm/2025/openai-gpt-4.5-system-card.md) · [GPT-5](llm/2025/openai-gpt-5-system-card.md) · [gpt-oss open source](llm/2025/openai-gpt-oss.md) · [Claude 3.7](llm/2025/anthropic-claude-3-7-sonnet.md)/[Claude 4](llm/2025/anthropic-claude-4.md) · [Gemini 2.5](llm/2025/gemini-2.5.md) · [Llama 4](llm/2025/meta-llama-4.md) · [Grok 3](llm/2025/xai-grok-3.md)/[4](llm/2025/xai-grok-4.md) · Gemma 3 · [Nemotron-H](llm/2025/nemotron-h.md)
- China: [Kimi k1.5](llm/2025/kimi-k1.5.md)/[K2](llm/2025/kimi-k2.md) · [Qwen3](llm/2025/qwen3.md)/[Coder](llm/2025/qwen3-coder.md)/[Next](llm/2025/qwen3-next.md) · [QwQ-32B](llm/2025/qwq-32b.md) · [GLM-4.5](llm/2025/glm-4.5.md)/[4.6](llm/2025/glm-4.6.md) · [MiniMax-01](llm/2025/minimax-01.md)/[M1](llm/2025/minimax-m1.md) · [DeepSeek-V3.1](llm/2025/deepseek-v3.1.md)/[V3.2 sparse attention](llm/2025/deepseek-v3.2.md) · [Hunyuan-TurboS](llm/2025/hunyuan-turbos.md) · [Pangu Ultra/Pro/Ultra-MoE](llm/2025/pangu-ultra-moe.md) · [MiMo (Xiaomi)](llm/2025/xiaomi-mimo.md) · [LongCat (Meituan)](llm/2025/longcat-flash.md) · [Ling/Ring (Ant)](llm/2025/ling-2.0.md) · [Step-3](llm/2025/step-3.md) · [Seed1.5-Thinking](llm/2025/seed1.5-thinking.md)
- infra/RL: DeepSeek open-source week (FlashMLA/DeepEP/DeepGEMM/[DualPipe]/[3FS]) · [Native Sparse Attention](llm/themes/ai-infra/native-sparse-attention.md) · DAPO/[AReaL](llm/themes/ai-infra/areal.md)/ProRL · agent RL: [Search-R1](llm/themes/agentic/search-r1.md)/[ReTool](llm/themes/agentic/retool.md)/[RAGEN](llm/themes/agentic/ragen.md)/[Tongyi DeepResearch](llm/themes/agentic/tongyi-deepresearch.md)

### 2026 H1 — Million-token context, trillion-scale MoE going mainstream, native agentic/omni
- US/West: [DeepSeek-V4 million-token context](llm/2026/deepseek-v4-technical-report.md) · [GPT-5.5](llm/2026/introducing-gpt-5-5.md)/[GPT-Rosalind](llm/2026/gpt-rosalind.md) · [Gemini 3 Pro](llm/2026/gemini-3-pro-model-card.md)/[3.5 Flash](llm/2026/gemini-3-5-flash-model-card.md) · [Claude Opus 4.6](llm/2026/anthropic-risk-report-feb-2026.md) · [Llama Muse Spark(MSL)](llm/2026/meta-muse-spark.md) · [Nemotron 3 Super/Ultra](llm/2026/nemotron-3-ultra.md) · [Mistral Medium 3.5](llm/2026/mistral-medium-3-5.md)
- China: [ERNIE 5.0](llm/2026/ernie-5.0-technical-report.md) · [GLM-5](llm/2026/glm-5-vibe-coding-to-agentic-engineering.md) · [Kimi K2.5](llm/2026/kimi-k2.5-visual-agentic-intelligence.md) · [Qwen3.5](llm/2026/qwen3.5-397b-a17b.md)/[Omni](llm/2026/qwen3.5-omni-technical-report.md) · [MiniMax-M2](llm/2026/minimax-m2-series.md)/[Sparse Attention](llm/2026/minimax-sparse-attention.md) · [Ling/Ring 2.6 trillion](llm/2026/ling-ring-2.6-technical-report.md) · [openPangu-Ultra-MoE-718B](llm/2026/openpangu-ultra-moe-718b.md) · [Hunyuan 3 preview](llm/2026/hunyuan-3-preview.md) · [MiMo-V2.5-Pro](llm/2026/mimo-v2.5-pro.md) · [Intern-S1-Pro](llm/2026/intern-s1-pro.md) · [LongCat-Next](llm/2026/longcat-next.md)
- **Incremental addendum (post-2026-05 gap-filling + full-paper six-dimension deep dives)**: [GLM-5.2](llm/2026/glm-5.2.md) (IndexShare/1M) · [Kimi-K2.6](llm/2026/kimi-k2.6.md) (1T MoE/agent swarm) · [MiniMax-M3](llm/2026/minimax-m3.md) (MSA) · [Qwen-AgentWorld](llm/2026/qwen-agentworld.md) (first language world model) · [Intern-S2-Preview](llm/2026/intern-s2-preview.md) (task scaling) · [MiniCPM5-1B](llm/2026/minicpm5-1b.md) (on-device 1B SOTA) · [Mistral-Small-4](llm/2026/mistral-small-4.md) (three families unified, 2026-03)
