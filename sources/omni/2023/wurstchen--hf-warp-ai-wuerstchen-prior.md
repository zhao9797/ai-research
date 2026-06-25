---
license: mit
---
<img src="https://cdn-uploads.huggingface.co/production/uploads/634cb5eefb80cc6bcaf63c3e/i-DYpDHw8Pwiy7QBKZVR5.jpeg" width=1500>

## Würstchen - Overview
Würstchen is a diffusion model, whose text-conditional model works in a highly compressed latent space of images. Why is this important? Compressing data can reduce
computational costs for both training and inference by magnitudes. Training on 1024x1024 images is way more expensive than training on 32x32. Usually, other works make 
use of a relatively small compression, in the range of 4x - 8x spatial compression. Würstchen takes this to an extreme. Through its novel design, we achieve a 42x spatial
compression. This was unseen before because common methods fail to faithfully reconstruct detailed images after 16x spatial compression. Würstchen employs a 
two-stage compression, what we call Stage A and Stage B. Stage A is a VQGAN, and Stage B is a Diffusion Autoencoder (more details can be found in the [paper](https://arxiv.org/abs/2306.00637)).
A third model, Stage C, is learned in that highly compressed latent space. This training requires fractions of the compute used for current top-performing models, allowing
also cheaper and faster inference. 

## Würstchen - Prior
The Prior is what we refer to as "Stage C". It is the text-conditional model, operating in the small latent space that Stage A and Stage B encode images into. During 
inference, its job is to generate the image latents given text. These image latents are then sent to Stages A & B to decode the latents into pixel space. 

### Image Sizes
Würstchen was trained on image resolutions between 1024x1024 & 1536x1536. We sometimes also observe good outputs at resolutions like 1024x2048. Feel free to try it out.
We also observed that the Prior (Stage C) adapts extremely fast to new resolutions. So finetuning it at 2048x2048 should be computationally cheap.
<img src="https://cdn-uploads.huggingface.co/production/uploads/634cb5eefb80cc6bcaf63c3e/5pA5KUfGmvsObqiIjdGY1.jpeg" width=1000>

## How to run
This pipeline should be run together with https://huggingface.co/warp-ai/wuerstchen:

```py
import torch
from diffusers import WuerstchenDecoderPipeline, WuerstchenPriorPipeline
from diffusers.pipelines.wuerstchen import DEFAULT_STAGE_C_TIMESTEPS

device = "cuda"
dtype = torch.float16
num_images_per_prompt = 2

prior_pipeline = WuerstchenPriorPipeline.from_pretrained(
    "warp-ai/wuerstchen-prior", torch_dtype=dtype
).to(device)
decoder_pipeline = WuerstchenDecoderPipeline.from_pretrained(
    "warp-ai/wuerstchen", torch_dtype=dtype
).to(device)

caption = "Anthropomorphic cat dressed as a fire fighter"
negative_prompt = ""

prior_output = prior_pipeline(
    prompt=caption,
    height=1024,
    width=1536,
    timesteps=DEFAULT_STAGE_C_TIMESTEPS,
    negative_prompt=negative_prompt,
	guidance_scale=4.0,
    num_images_per_prompt=num_images_per_prompt,
)
decoder_output = decoder_pipeline(
    image_embeddings=prior_output.image_embeddings,
    prompt=caption,
    negative_prompt=negative_prompt,
    guidance_scale=0.0,
    output_type="pil",
).images
```

### Image Sampling Times
The figure shows the inference times (on an A100) for different batch sizes (`num_images_per_prompt`) on Würstchen compared to [Stable Diffusion XL](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0) (without refiner).
The left figure shows inference times (using torch > 2.0), whereas the right figure applies `torch.compile` to both pipelines in advance.
![image/jpeg](https://cdn-uploads.huggingface.co/production/uploads/634cb5eefb80cc6bcaf63c3e/UPhsIH2f079ZuTA_sLdVe.jpeg)


## Model Details
- **Developed by:** Pablo Pernias, Dominic Rampas
- **Model type:** Diffusion-based text-to-image generation model
- **Language(s):** English
- **License:** MIT
- **Model Description:** This is a model that can be used to generate and modify images based on text prompts. It is a Diffusion model in the style of Stage C from the [Würstchen paper](https://arxiv.org/abs/2306.00637) that uses a fixed, pretrained text encoder ([CLIP ViT-bigG/14](https://huggingface.co/laion/CLIP-ViT-bigG-14-laion2B-39B-b160k)).
- **Resources for more information:** [GitHub Repository](https://github.com/dome272/Wuerstchen), [Paper](https://arxiv.org/abs/2306.00637).
- **Cite as:**

      @misc{pernias2023wuerstchen,
            title={Wuerstchen: Efficient Pretraining of Text-to-Image Models}, 
            author={Pablo Pernias and Dominic Rampas and Marc Aubreville},
            year={2023},
            eprint={2306.00637},
            archivePrefix={arXiv},
            primaryClass={cs.CV}
      }

## Environmental Impact

**Würstchen v2** **Estimated Emissions**
Based on that information, we estimate the following CO2 emissions using the [Machine Learning Impact calculator](https://mlco2.github.io/impact#compute) presented in [Lacoste et al. (2019)](https://arxiv.org/abs/1910.09700). The hardware, runtime, cloud provider, and compute region were utilized to estimate the carbon impact.

- **Hardware Type:** A100 PCIe 40GB
- **Hours used:** 24602
- **Cloud Provider:** AWS
- **Compute Region:** US-east
- **Carbon Emitted (Power consumption x Time x Carbon produced based on location of power grid):** 2275.68 kg CO2 eq.


