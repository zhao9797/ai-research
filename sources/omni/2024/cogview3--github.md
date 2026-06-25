# Source: github.com/zai-org/CogView4 (formerly THUDM/CogView3) — fetched via chrome MCP 2026-06-25
# Repo now hosts CogView4, CogView3-Plus and CogView3 (ECCV 2024). CogView3 page redirects here.

CogView4 & CogView3 & CogView-3Plus

Updates:
- 2025/03/24: CogKit toolkit for fine-tuning/inference of CogView4 and CogVideoX series.
- 2025/03/04: diffusers version of CogView-4 (6B params), native Chinese input, Chinese text-to-image.
- 2024/10/13: diffusers version of CogView-3Plus-3B model.
- 2024/9/29: open-sourced CogView3 and CogView-3Plus-3B. CogView3 is a text-to-image system based on
  cascading diffusion using a relay diffusion framework. CogView-3Plus is a series of newly developed
  text-to-image models based on Diffusion Transformer.

Model Comparison:
  CogView4:        Resolution 512<=H,W<=2048, H*W<=2^21, H,W mod 32 = 0; Precision BF16,FP32;
                   Encoder GLM-4-9B; Prompt language Chinese,English; Prompt length 1024 tokens.
  CogView3-Plus-3B: Resolution 512<=H,W<=2048 (H,W mod 32=0); Precision BF16,FP32;
                   Encoder T5-XXL; Prompt language English; Prompt length 224 tokens.

CogView3-Plus uses Diffusion Transformer (DiT) backbone; CogView3 (original paper) uses cascaded relay
diffusion with 3-stage UNet.

Memory Usage (DiT models, BF16, batchsize=4) — CogView4-6B table (for reference):
  512*512:  offload OFF 33GB / ON 20GB / TextEnc 4bit 13G
  1280*720: 35GB / 20GB / 13G
  1024*1024:35GB / 20GB / 13G
  1920*1280:39GB / 20GB / 14G

Benchmarks reported in README are for CogView4-6B (NOT CogView3-Plus):
DPG-Bench: CogView4-6B Overall 85.13 (SDXL 74.65, SD3-Medium 84.08, DALL-E3 83.50, Flux.1-dev 83.79, Janus-Pro-7B 84.19)
GenEval:   CogView4-6B Overall 0.73 (SDXL 0.55, SD3-Medium 0.74, DALL-E3 0.67, Flux.1-dev 0.66, Janus-Pro-7B 0.80)
T2I-CompBench, Chinese Text Accuracy: CogView4-6B only.

Prompt optimization: uses LLM (glm-4-plus) to rewrite prompts; CogView4 and CogView3 use different few-shot examples.

License: Apache 2.0. CogView3 paper accepted to ECCV 2024.
