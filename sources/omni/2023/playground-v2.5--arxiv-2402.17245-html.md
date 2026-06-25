# Playground v2.5: Three Insights towards Enhancing Aesthetic Quality in Text-to-Image Generation
Source: https://arxiv.org/html/2402.17245v1 (fetched via chrome MCP; arxiv.org blocked via cloakbrowser proxy in this env)
Authors: Daiqing Li, Aleks Kamko, Ehsan Akhgari, Ali Sabet, Linmiao Xu, Suhail Doshi (Playground Research)

NOTE: This is the Playground v2.5 technical report. It is the closest first-party
technical source that documents Playground v2's design (the original v2 blog at
blog.playgroundai.com/playground-v2/ is now offline; archive.org unreachable in this env).
Below are the v2-relevant facts extracted; full v2.5 text follows.

## Key Playground v2 facts stated in this report
- Playground v2 was open-sourced in December 2023.
- Playground v2 amassed over 135,000 downloads in the last month (from HuggingFace) at the time of v2.5.
- v2.5 "chose not to change the underlying model architecture" — i.e. v2 and v2.5 share the SDXL architecture (latent diffusion, U-Net, two text encoders OpenCLIP-ViT/G + CLIP-ViT/L).
- Playground v2 uses **offset noise** and a **DDPM (Ho et al. 2020) noise schedule** (v2.5 switched to the EDM framework, Karras et al. 2022).
- "SDXL adopts the strategy of adding offset noise in the last stage of training, as does Playground v2."
- User study: images from Playground v2 were favored **2.5x more than SDXL** (Internal-1K prompt set; same study setup as v2.5; v2.5 reached 4.8x).
- MJHQ-30K benchmark (introduced with v2): FID on 30K images curated from Midjourney 5.2, 10 categories × 3K samples, filtered by aesthetic score + CLIP score; FID computed at 1024×1024.
- Citation key: playground-v2 = "Daiqing Li, Aleks Kamko, Ali Sabet, Ehsan Akhgari, Linmiao Xu, and Suhail Doshi. Playground v2." (ref [20])

## Full v2.5 report text (for methodology context)

In this work, we share three insights for achieving state-of-the-art aesthetic quality in text-to-image generative models. We focus on three critical aspects: enhancing color and contrast, improving generation across multiple aspect ratios, and improving human-centric fine details. First, the significance of the noise schedule in training a diffusion model. Second, accommodating various aspect ratios via a balanced bucketed dataset. Lastly, aligning model outputs with human preferences. Playground v2.5 demonstrates state-of-the-art aesthetic quality, outperforming SDXL and Playground v2, and closed-source DALL-E 3 and Midjourney v5.2.

### Introduction
Playground v2 was open-sourced in December 2023; over 135,000 downloads in the last month from HuggingFace; cited by Stable Cascade. Following Playground v2, the team chose not to change the underlying model architecture for v2.5; instead focused on improving the training recipe.

### 2.1 Enhanced Color and Contrast
Latent diffusion models struggle to generate high color contrast / vibrant color since SD1.5. SDXL cannot generate a pure black or pure white image. This stems from the noise scheduling of the diffusion process (Lin et al.): the SNR of Stable Diffusion is too high even at maximum discrete noise level. Fixes: offset noise (Guttenberg/CrossLabs), Zero Terminal SNR (Lin et al.). SDXL adds offset noise in the last training stage, **as does Playground v2**. But SDXL still has muted color/contrast.

For Playground v2.5: trained from scratch using the **EDM framework** (Karras et al. 2022). EDM advantages: (1) like Zero Terminal SNR, near-zero SNR at final timestep, removing need for Offset Noise and fixing muted colors; (2) first-principles design of training/sampling/preconditioning of the U-Net → better image quality and faster convergence. Also inspired by Hoogeboom et al. to skew noise schedule noisier when training on high-resolution images. **Playground v2 uses offset noise and a DDPM (Ho et al. 2020) noise schedule.**

### 2.2 Generation Across Multiple Aspect Ratios
Diffusion models don't generalize well to other aspect ratios when trained only on square images (NovelAI). NovelAI proposes bucketed sampling; SDXL adopted bucketing + size conditioning. SDXL's dataset has unbalanced aspect-ratio buckets (mostly square) → learned bias. v2.5 followed a bucketing strategy similar to SDXL's but with a more balanced bucket sampling strategy to avoid catastrophic forgetting and bias.

### 2.3 Human Preference Alignment
Humans sensitive to errors in hands/faces/torsos. Generative models maximize log-likelihood not human preference → hallucinations. SFT (supervised fine-tuning) aligns base model with a small high-quality dataset (often outperforms RLHF — LIMA). Emu introduces SFT-like alignment for T2I. Inspired by Emu, v2.5 built a system to automatically curate a high-quality dataset from multiple sources via user ratings; iterative human-in-the-loop training; monitored by empirical evaluation on fixed prompt grids. Improvements over SDXL in: facial detail/clarity/liveliness; eye shape and gaze; hair texture; overall lighting/color/saturation/depth-of-field.

### 3 Evaluations
- User study run inside the product; each image pair shown to ≥7 unique users; a pair "wins" only with ≥2-vote margin (1-vote = tie); thousands of unique users per study.
- 3.2 Overall aesthetic preference: Internal-1K prompt set (real user prompts from Playground.com). **v2 was favored 2.5x over SDXL; v2.5 is favored 4.8x over SDXL.** v2.5 also outperforms Midjourney 5.2, DALL-E 3, PIXART-α, and v2.
- 3.3 Multiple aspect ratios (9:16 to 16:9): v2.5 beats SDXL in all.
- 3.4 People-200 prompt set (200 real user people prompts), 3:2 aspect ratio 1254×836; v2.5 beats SDXL and RealStock v2.
- 3.5 MJHQ-30K: FID on 30K images curated from Midjourney 5.2, 10 categories × 3K, aesthetic score + CLIP score filtering, FID at 1024×1024. v2.5 outperforms v2 and SDXL in overall and all per-category FID, especially people and fashion.

### 4 Conclusion
Three insights: color/contrast (EDM noise schedule), multi-aspect-ratio (balanced buckets), human-preference alignment (SFT-like). Goal: unified general-purpose vision system.
