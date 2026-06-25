# Allegro: Advanced Video Generation Model (Rhymes AI official blog)

Source: https://rhymes.ai/blog-details/allegro-advanced-video-generation-model
Captured via Wayback Machine snapshot 20241120074955 (rhymes.ai unreachable directly from fetch env at capture time).
Original blog date: October 20, 2024 · ~10 min read · Rhymes AI Team

---

We're excited to announce the open-source release of Allegro, Rhymes AI's advanced
text-to-video model. Allegro transforms simple text prompts into high-quality, short video clips.

## Allegro at a Glance
6-second videos at 15 FPS and 720p resolution from simple text prompts.

### Key Features
- Open Source: Full model weights and code available to the community, Apache 2.0!
- Versatile Content Creation: close-ups of humans and animals to diverse dynamic scenes.
- High-Quality Output: 6-second videos at 15 FPS with 720x1280 resolution, interpolatable
  to 30 FPS with EMA-VFI.
- Small and Efficient: 175M parameter VAE and a 2.8B parameter DiT model. Supports FP32/BF16/FP16
  and uses 9.3 GB GPU memory in BF16 with CPU offloading. Context length 79.2k = 88 frames.

## The Technology Behind Allegro
1. Large-Scale Video Data Processing — systematic data processing & filtering pipelines
   (sequential stages); a structured data system enables multi-dimensional classification
   and clustering for various training stages/purposes.
2. Compressing Video into Visual Tokens — a Video Variational Autoencoder (VideoVAE) encodes
   raw videos into a spatio-temporal latent space; built on a pre-trained image VAE, extended
   with spatiotemporal modeling layers.
3. Scaling Video Diffusion Transformer — backbone built on DiT with **3D RoPE position
   embedding and 3D full attention**. Compared to traditional UNet diffusion models, the
   Transformer structure is more conducive to model scaling. 3D attention processes both the
   spatial dimensions of video frames and their temporal evolution.

## Future Developments
image-to-video generation, motion control, and longer narrative/storyboard-style video.

(Apache 2.0; weights on Hugging Face; inference code on GitHub.)
