# Playground v2: A new leap in creativity (official blog)
Source: https://blog.playgroundai.com/playground-v2/
Published: 2023-12-05T17:50:34Z
Fetched: 2026-06-25 via curl direct (HTTP 200; blog is LIVE, contrary to earlier note)

--- cleaned blog text ---
Playground v2: A new leap in creativity

Home

About

Sign in

Subscribe

Playground v2: A new leap in creativity

We’re providing open weights for Playground v2 - an early preview of our efforts to make increasingly powerful graphics models. You can visit 
playground.com
to try it out. The model is also available on 
HuggingFace
if you wish to download it. Commercial use is permitted.

Benchmarks

Early benchmarks have shown that Playground v2 is preferred 2.5x more than Stable Diffusion XL.

Across thousands of prompts, we asked thousands of users which image they preferred by showing them an image from each model. Below we show the results for each model.

PartiPrompts:

FID

We introduce a new benchmark, 
MJHQ-30K
, for automatic evaluation of a model’s aesthetic quality. The benchmark computes FID on a high-quality dataset to gauge aesthetic quality.

We curate the high-quality dataset from Midjourney with 10 common categories, each category with 3K samples. Following common practice, we use aesthetic score and CLIP score to ensure high image quality and high image-text alignment. Furthermore, we take extra care to make the data diverse within each category.

Below is a comparison table of select prompts to provide a sense of quality, alignment, and aesthetics:

Paying it forward

We're also releasing pre-train weights to push the field of research in environments where compute tends to be limited. The base model weights are available in 
256px
and 
512px
stages on HuggingFace.

If you create anything, we'd love to hear about it.

— Playground Research Team

Team: Daiqing Li, Aleks Kamko, Ali Sabet, Ehsan Akhgari, Lin Xu
Additional support: Patrick Hultquist, Nihanth Subramanya, Tyler Hoyt, Justin Lau

If research like this is exciting to you, 
we're hiring
.

Playground © 2026 — 
Powered by Ghost
