> 🌐 English entry page. Deep pages are in Chinese. 中文版 / Chinese: [00-SUMMARY.md](00-SUMMARY.md)

---
title: "Omni / Multimodal Generation Technology Evolution Research (2020 → 2026-H1) · Main Summary"
type: source
tags: [omni, multimodal-generation, text-to-image, image-editing, unified-understanding-generation, any-to-any, video-generation, diffusion, autoregressive, survey]
created: 2026-06-25
updated: 2026-06-25
---

# Omni / Multimodal Generation Technology Evolution Research · Main Summary (2020 → 2026-H1)

> Covers **visual/multimodal "generation and editing" models and their enabling methods**: text-to-image · image editing/controllable generation · unified understanding + generation · any-to-any omni-modal · video generation · audio/speech within omni-modal · 3D · and enabling methods such as diffusion/flow/autoregressive.
> Primary official sources only: original arXiv papers, official technical reports/system cards, official blogs/product launches, official GitHub / HuggingFace / ModelScope model cards. **No third-party interpretations/secondary aggregations.**
> Each work page is organized along **six dimensions**: `data · training methods · model architecture · benchmark evaluation · infra` + innovation/impact; all numbers are **adversarially verified line-by-line against primary sources** (no dropped/misattributed/fabricated figures).

---

## 1. Corpus Statistics

- **Primary sources after deduplication**: **~322 entries** (**324 structured work pages**, deduplicated by original URL)
- **Downloaded primary sources**: arXiv PDFs (gitignored, on local disk + HF bucket) + `.md/.html` snapshots of official blogs/model cards (with the repo); see each page's `downloaded:` and `sources/omni/<year>/`
- **Cross-cutting reviews**: 6 `sections/` + 5 model-family `deep-dive/`
- **Quality assurance**: every page is **adversarially verified line-by-line against primary sources** (no dropped/misattributed/fabricated figures); plus one round of **gap-filling review** (added 33 missing cornerstone works such as DiT/MaskGIT/MAR/REPA/AudioLM/3D-GS + fixed broken links, normalized internal links)

**By year (page count)**: 2020→7 · 2021→25 · 2022→45 · 2023→91 · 2024→69 · 2025→66 · 2026(H1)→21

**By country (deduplicated)**: US/West ~150 · China ~130 · Europe ~36 (FLUX/Stability/CompVis/StyleGAN-XL etc.) · Other (CH/KR/SG/IL) a few — full coverage of top US/China/Europe players

**By category (deduplicated, single primary tag)**: text-to-image t2i ~72 · video ~60 · enabling methods ~53 · editing edit ~48 · unified ~46 · 3D ~19 · audio ~11 · omni ~11 · foundation 1

---

## 2. How to Read This Research

Four layers from "conclusion" to "primary source":

1. **Six cross-cutting chapters (core, read first)** — `sections/`
   - [Model architecture evolution](sections/architecture.md) — U-Net→DiT→MMDiT→AR/next-scale/masked→unified omni backbone; tokenizer/VAE/text-encoder evolution
   - [Data: scale · mixture ratios · re-captioning · filtering](sections/data.md) — LAION era → re-captioning wave → staged mixture ratios → copyright/safety filtering
   - [Training methods](sections/training.md) — diffusion/flow-matching/AR/masked objectives · multi-stage · preference alignment (DPO/DDPO/Flow-GRPO/reward) · few-step distillation
   - [Benchmark evaluation](sections/benchmark.md) — FID→CLIPScore→GenEval/DPG/T2I-CompBench→human eval/Arena→editing/video benchmarks + cross-comparison number tables
   - [Infra](sections/infra.md) — training scale/parallelism · tokenizer engineering · inference acceleration · closed-source black-box boundaries
   - [Unified understanding-and-generation & any-to-any omni topic](sections/unified-omni.md) — comparison of the three major paradigms
2. **Model-family cross-comparison** — `deep-dive/`
   - [Stable Diffusion → SDXL → SD3 → FLUX lineage](deep-dive/sd-flux-lineage.md)
   - [Chinese text-to-image/editing families (CogView·Qwen·Hunyuan·Seedream·Kolors·ERNIE)](deep-dive/chinese-t2i-families.md)
   - [Unified/Omni model families (Chameleon·Emu·Janus·Bagel·OmniGen·Show-o·VAR)](deep-dive/unified-omni-families.md)
   - [Video generation families (Sora·Veo·Wan·Movie-Gen·Hunyuan·Kling·CogVideoX)](deep-dive/video-generation-families.md)
   - [Image editing and controllable generation families (ControlNet·InstructPix2Pix·Emu-Edit·Kontext·Step1X·Qwen-Edit)](deep-dive/image-editing-control.md)
3. **Full source index (by year/month, every entry clickable)** — [01-INDEX.md](01-INDEX.md)
4. **Per-work structured pages** — `2020/`…`2026/`; **downloaded primary sources** — `sources/omni/<year>/`

---

## 3. Six-Year Storyline Overview

**2020 — Foundations**: the diffusion trio [[ddpm]] (ε-MSE, FID 3.17) / [[ddim]] (deterministic few-step sampling) / [[score-sde]] (continuous SDE + probability-flow ODE, FID 2.20) established the generative formulation; [[taming-transformers-vqgan]] opened the discrete-token autoregressive track.

**2021 — Guidance and latent space**: [[diffusion-models-beat-gans]] used classifier guidance for diffusion to first surpass GANs on ImageNet; [[classifier-free-guidance]] became the standard knob for all subsequent T2I; [[latent-diffusion-ldm]] moved diffusion into VAE latent space + cross-attention text conditioning (the direct precursor of Stable Diffusion); [[dall-e-1]]/[[glide]]/[[cogview]] pushed "text-to-image" into the public eye.

**2022 — Text-to-image explosion**: [[dall-e-2]] (unCLIP) / [[imagen]] (T5 + pixel cascade) / [[parti]] (autoregressive) / [[stable-diffusion-1]] (open-source ignition) launched together; [[dreambooth]]/[[textual-inversion]]/[[prompt-to-prompt]] pioneered personalization and editing; [[rectified-flow]]/[[flow-matching]]/[[dpm-solver]]/[[elucidating-edm]] solidified the methodological foundations; video [[make-a-video]]/[[imagen-video]]/[[phenaki]] got started.

**2023 — Control, unification, and speedup advancing on three fronts**: editing/control [[controlnet]]/[[instructpix2pix]]/[[ip-adapter]]/[[emu-edit]]; quality [[sdxl]]/[[dall-e-3]] (synthetic captions)/[[pixart-alpha]]; unified multimodal [[chameleon-cm3leon]]/[[emu-multimodal]]/[[next-gpt]]/[[kosmos-g]]; few-step distillation [[consistency-models]]/[[latent-consistency-models]]/[[sdxl-turbo-add]]; preference alignment [[diffusion-dpo]]/[[ddpo]]/[[hps-v2]]; video [[stable-video-diffusion]]/[[animatediff]]/[[emu-video]]; 3D [[zero-1-to-3]]/[[mvdream]].

**2024 — DiT/MMDiT-ization and the "unified generation" paradigm established**: [[stable-diffusion-3]] (MMDiT + rectified flow)/[[flux-1]]/[[hunyuan-dit]]/[[sana]]; autoregressive/unified [[chameleon]]/[[transfusion]]/[[show-o]]/[[emu3]]/[[janus]]/[[var]]; video leap [[sora]]/[[movie-gen]]/[[cogvideox]]/[[kling]]/[[veo-2]]; GPT-4o/[[gemini-2-0-flash-native-image]] previewing "native multimodal generation".

**2025 — Native omni and the explosion of China's contingent**: product-grade native image [[gpt-image-1]]/[[gemini-2-5-flash-image-nano-banana]]; unified flagships [[bagel]]/[[janus-pro]]/[[blip3-o]]/[[omnigen2]]/[[ming-omni]]/[[qwen2-5-omni]]; Chinese text-to-image/editing [[qwen-image]]/[[qwen-image-edit]]/[[seedream-3-0]]/[[seedream-4-0]]/[[hunyuanimage-2-1]]/[[step1x-edit]]/[[flux-1-kontext]]; video [[wan-2-1]]/[[wan-2-2]]/[[veo-3]]/[[sora-2]]/[[hunyuanvideo-1-5]].

**2026-H1 — Omni-modal reasoning and extreme engineering**: [[qwen-image-2-0]]/[[qwen3-5-omni]]/[[ernie-image]]/[[omnigen-ar]]/[[skywork-unipic-3-0]]/[[internvl-u]]/[[flux-2-klein]]/[[gpt-image-2]]/[[seedream-5-0-lite]]/[[reve-2-0]]/[[ideogram-4-0]]/[[nano-banana family]], where unified "understanding—reasoning—generation—editing" and on-device sub-second inference become the frontier.

---

## 4. Four Through-Lines of Technology (details in each section)

1. **Generative formulation**: DDPM discrete chain → score-SDE continuous → rectified flow/flow matching "straight line" (the T2I default since 2024); running in parallel with discrete-token AR / next-scale / masked, and fusing in unified models.
2. **Backbone**: U-Net → DiT (pure Transformer) → MMDiT (text-image dual stream) ｜｜ LLM-style decoder-only AR; from 2025+ a single backbone carries arbitrary modalities.
3. **Conditioning and tokenizer**: text encoder `CLIP→T5→frozen MLLM→no external encoder`; visual `discrete VQ ｜ continuous KL-VAE ｜ semantic RAE ｜ next-scale residual quantization`.
4. **Post-training**: SFT → preference alignment (Diffusion-DPO/DDPO/Flow-GRPO + ImageReward/HPS/PickScore rewards) → few-step distillation (Consistency/LCM/ADD/MeanFlow); editing and in-context capabilities move from "dedicated modules" toward "unified instructions".

---

*Maintenance: research scripts and index generators are under `self-wiki/scripts/tmp/` (`build_index_omni.py` refreshes the index, `normalize_wikilinks.py` normalizes internal links).*
