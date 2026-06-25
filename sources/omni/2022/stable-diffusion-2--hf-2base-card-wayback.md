# Stable Diffusion v2-base Model Card (HF, Wayback)
Source: http://web.archive.org/web/20240101233658/https://huggingface.co/stabilityai/stable-diffusion-2-base
Note: 现网 https://huggingface.co/stabilityai/stable-diffusion-2-base 已 gated（raw 返回 "Invalid username or password"），https://huggingface.co/stabilityai/stable-diffusion-2 现 404；本卡片经 Wayback Machine（快照 2024-01-01）取回。

---

## Stable Diffusion v2-base Model Card

The model is trained from scratch **550k steps at resolution 256x256** on a subset of LAION-5B filtered for explicit pornographic material, using the LAION-NSFW classifier with **`punsafe=0.1`** and an **aesthetic score >= `4.5`**. Then it is further trained for **850k steps at resolution 512x512** on the same dataset on images with resolution `>= 512x512`.

### Model Details
- **Developed by:** Robin Rombach, Patrick Esser
- **Model type:** Diffusion-based text-to-image generation model
- **Language(s):** English
- **License:** CreativeML Open RAIL++-M License
- **Model Description:** Latent Diffusion Model that uses a fixed, pretrained text encoder (OpenCLIP-ViT/H).
- arxiv tags on card: 2112.10752 (LDM), 2202.00512 (v-prediction), 1910.09700 (ML CO2 impact)

### Training Procedure
- Autoencoder uses relative downsampling factor 8, maps H×W×3 → H/f × W/f × 4 latents.
- Text prompts encoded through OpenCLIP-ViT/H text-encoder; output fed into UNet backbone via cross-attention.
- Loss = reconstruction objective between added noise and UNet prediction; also use the **v-objective** (arXiv:2202.00512).

**Checkpoints (exact step counts):**
- `512-base-ema.ckpt`: **550k steps @ 256x256** (LAION-5B subset, NSFW filtered `punsafe=0.1`, aesthetic `>=4.5`), then **850k steps @ 512x512** on same dataset with resolution `>=512x512`.
- `768-v-ema.ckpt`: **Resumed from 512-base-ema**, trained **150k steps using v-objective** on same dataset, then **resumed another 140k steps on a 768x768 subset**.
- `512-depth-ema.ckpt`: Resumed from 512-base-ema, **finetuned 200k steps**. Added an **extra input channel** to process the (relative) depth prediction produced by **MiDaS (`dpt_hybrid`)** as additional conditioning. Extra U-Net input channels **zero-initialized**.
- `512-inpainting-ema.ckpt`: Resumed from 512-base-ema, trained **another 200k steps**. Follows the **mask-generation strategy from LAMA**; combined with latent VAE representations of the masked image as additional conditioning. Extra U-Net input channels **zero-initialized**.
- `x4-upscaling-ema.ckpt`: Trained for **1.25M steps on a 10M subset of LAION containing images >2048x2048**. Trained on **crops of size 512x512**; text-guided latent upscaling diffusion model. Receives a `noise_level` input parameter to add noise to the low-res input per a predefined diffusion schedule.

**Training infra/hyperparams:**
- **Hardware:** 32 x 8 x A100 GPUs
- **Optimizer:** AdamW
- **Gradient Accumulations:** 1
- **Batch:** 32 x 8 x 2 x 4 = 2048
- **Learning rate:** warmup to 0.0001 for 10,000 steps and then kept constant

### Evaluation Results
Evaluations with different classifier-free guidance scales (1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0) and 50 DDIM sampling steps show the relative improvements of the checkpoints (figure `model-variants.jpg`).
Evaluated using **50 DDIM steps and 10000 random prompts from the COCO2017 validation set, at 512x512 resolution. Not optimized for FID scores.**
(注：卡片只给出相对改进的 pareto 图，**未列出具体 FID/CLIPScore 数值**。)

### Environmental Impact
**注意：本段标题与数字均为 "Stable Diffusion v1" 的估算，被原样沿用进 v2 卡片，并非 v2 自身的实测。**
- Hardware Type: A100 PCIe 40GB
- Hours used: 200000
- Cloud Provider: AWS
- Compute Region: US-east
- Carbon Emitted: 15000 kg CO2 eq.

### Limitations (节选)
- 不达完美照片级真实；无法渲染清晰文字；组合性任务（"红立方在蓝球上"）表现差；人脸/人物可能生成不佳；主要英文 caption；autoencoder 有损；训练于 LAION-5B 子集（含成人/暴力/性内容，已用 LAION NSFW 检测器部分过滤）。

### Bias (节选)
- 主要训练于 LAION-2B(en)，以英文描述为主；非英文社区/文化代表性不足，输出偏向白人与西方文化为默认。

Model card written by: Robin Rombach, Patrick Esser, David Ha; based on SD v1 and DALL-E Mini model cards.
