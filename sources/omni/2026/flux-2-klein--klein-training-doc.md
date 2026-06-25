# FLUX.2 [klein] Training - Black Forest Labs
Source: https://docs.bfl.ai/flux_2/flux2_klein_training
FLUX.2 [klein] Training - Black Forest Labs
> ## Documentation Index
>
> Fetch the complete documentation index at: </llms.txt>
>
> Use this file to discover all available pages before exploring further.

[Skip to main content](#content-area)

Introducing the official FLUX MCP • [Try now](https://mcp.bfl.ai/)

[Black Forest Labs home page![light logo](https://mintcdn.com/bfl/OQ5B17YmedKOM4zs/logo/logo_light.png?fit=max&auto=format&n=OQ5B17YmedKOM4zs&q=85&s=a11f73fac1ef9254cffa5eb412269198)![dark logo](https://mintcdn.com/bfl/OQ5B17YmedKOM4zs/logo/logo_dark.png?fit=max&auto=format&n=OQ5B17YmedKOM4zs&q=85&s=d933d5452b84db18fc87cd6321e33d08)](/)

Search...

⌘K

* [Help Center](https://help.bfl.ai)
* [API Status](https://status.bfl.ai)
* [API Pricing](https://bfl.ai/pricing)
* [Get API Key](https://dashboard.bfl.ai/)
* [Get API Key](https://dashboard.bfl.ai/)

Search...

Navigation

Training

FLUX.2 [klein] Training

[Documentation](/quick_start/introduction)[Prompting Guide](/guides/prompting_summary)[API Reference](/api-reference/utility/get-result)[Release Notes](/release-notes)

* [Documentation](/quick_start/introduction)
* [Prompting Guide](/guides/prompting_summary)
* [BFL Homepage](https://bfl.ai)
* [Help Center](https://help.bfl.ai)

### Get Started

* [Overview](/quick_start/introduction)
* [Quick Start](/quick_start/get_started)
* [Image Generation](/quick_start/generating_images)
* [API Pricing](/quick_start/pricing)

### Account Management

* [Organizations & Projects](/account_management/organizations_projects)
* [Team Management](/account_management/team_management)
* [Credits & Billing](/account_management/credits_billing)

### FLUX.2

* [Overview](/flux_2/flux2_overview)
* [FLUX.2 Image Editing](/flux_2/flux2_image_editing)
* [FLUX.2 Text to Image](/flux_2/flux2_text_to_image)

### FLUX Tools

* [FLUX Outpainting](/flux_tools/flux_outpainting)
* [FLUX Erase](/flux_tools/flux_erase)
* [FLUX Virtual Try-On](/flux_tools/flux_vto)

### API Integration

* [Integration Guide](/api_integration/integration_guidelines)
* [MCP & Agent Skills](/api_integration/mcp_integration)
* [Errors](/api_integration/errors)

### Training

* [FLUX.2 [klein] Training](/flux_2/flux2_klein_training)
* [FLUX.2 [klein] Style Training](/flux_2/flux2_klein_training_example)

### Legacy Models

* FLUX.1 Kontext
* FLUX1.1 [pro] Models
* FLUX.1 Tools

## On this page

* [Overview](#overview)
* [Why Train FLUX.2 [klein] Models?](#why-train-flux-2-klein-models)
* [Community Tools](#community-tools)
* [Model Variants](#model-variants)
* [System Requirements](#system-requirements)
  + [Minimum Hardware](#minimum-hardware)
* [Training Types](#training-types)
  + [LoRA Training](#lora-training)
  + [Full Fine-tuning](#full-fine-tuning)
* [Getting Started](#getting-started)
  + [Quick Start Resources](#quick-start-resources)
* [Training Best Practices](#training-best-practices)
  + [Dataset Preparation](#dataset-preparation)
  + [Training Parameters](#training-parameters)
* [Using Your Trained LoRA](#using-your-trained-lora)
* [Next Steps](#next-steps)

Training

# FLUX.2 [klein] Training

Copy page

Fine-tune FLUX.2 [klein] models with custom datasets using LoRA training for specialized image generation.

Copy page

![FLUX.2 Klein Training](https://cdn.sanity.io/images/2gpum2i6/production/e09038959c1ec2beaa3aeb077974ffd7b928471b-1440x1072.png)
This guide covers how to train LoRAs and fine-tune FLUX.2 [klein] models on your own datasets. With open weights available under Apache 2.0 (4B) and FLUX Non-Commercial License (9B), you can create custom models tailored to your specific needs.

## [​](#overview) Overview

FLUX.2 [klein] Base models are ideal for fine-tuning due to their undistilled architecture, which preserves the full training signal. This makes them perfect for:

* **LoRA Training**: Lightweight adapters for style transfer and character consistency
* **Full Fine-tuning**: Complete model adaptation for specialized domains
* **Research**: Experimentation with novel training techniques

## [​](#why-train-flux-2-klein-models) Why Train FLUX.2 [klein] Models?

## Style Transfer

Create custom artistic styles that can be applied to any subject matter. Perfect for consistent branding or artistic projects.

## Character Consistency

Train models to generate specific characters or people with consistent features across different scenes and poses.

## Domain Specialization

Adapt models for specialized domains like medical imaging, technical illustrations, or specific art movements.

## Concept Learning

Teach the model new concepts, objects, or visual patterns not well-represented in the base training data.

## [​](#community-tools) Community Tools

Open-source frameworks provide full control over the training process:

[## AI-Toolkit

All-in-one training suite with GUI and CLI. Optimized for consumer GPUs with 12GB+ VRAM.](https://github.com/ostris/ai-toolkit)

[## Diffusers

Official Hugging Face library with DreamBooth and LoRA training examples for FLUX.2.](https://github.com/huggingface/diffusers/blob/main/examples/dreambooth/README_flux2.md)

## [​](#model-variants) Model Variants

Choose the right [klein] variant for your use case:

| Variant | **Best For** | **License** |
| --- | --- | --- |
| [**klein 4B Base**](https://huggingface.co/black-forest-labs/FLUX.2-klein-base-4B) | Quick iterations | Apache 2.0 |
| [**klein 9B Base**](https://huggingface.co/black-forest-labs/FLUX.2-klein-base-9B) | Maximum quality, complex concepts | FLUX Non-Commercial |

Base models are undistilled and provide higher output diversity, making them ideal starting points for fine-tuning. The 4B variant is recommended for most users due to lower hardware requirements.

## [​](#system-requirements) System Requirements

### [​](#minimum-hardware) Minimum Hardware

## For klein 4B Base Training

* **GPU**: NVIDIA with 12GB VRAM (RTX 3060 12GB, RTX 4060 Ti 16GB)
* **RAM**: 32GB system memory

## For klein 9B Base Training

* **GPU**: NVIDIA with 22GB VRAM (RTX 3090, RTX 4090)
* **RAM**: 64GB system memory

## [​](#training-types) Training Types

### [​](#lora-training) LoRA Training

**Low-Rank Adaptation (LoRA)** is the most popular training method:

* ✅ Lightweight (typically 10-200MB)
* ✅ Fast training (1-3 hours on consumer GPUs)
* ✅ Easy to share and combine
* ✅ Minimal hardware requirements

**Use cases**: Style transfer, character consistency, concept learning

### [​](#full-fine-tuning) Full Fine-tuning

Complete model adaptation for maximum control:

* ⚠️ Large file sizes
* ⚠️ Longer training times (days to weeks)
* ⚠️ High-end hardware recommended
* ✅ Maximum flexibility and quality

**Use cases**: Specialized domains, production deployments, checkpoint training, research

## [​](#getting-started) Getting Started

[## Step-by-Step Training Example

Follow our complete hands-on guide with a real dataset example. Learn how to prepare data, configure training, and use your trained LoRA.](/flux_2/flux2_klein_training_example)

### [​](#quick-start-resources) Quick Start Resources

[## Download Base Weights

Get FLUX.2 Klein base models from Hugging Face.](https://huggingface.co/black-forest-labs)

[## Prompting Guide

Learn how to prompt Klein models effectively.](/guides/prompting_summary)

## [​](#training-best-practices) Training Best Practices

### [​](#dataset-preparation) Dataset Preparation

Image Quality

* Use high-resolution images (1024px or higher)
* Ensure consistent quality across all training images
* Remove artifacts and low-quality samples

Caption Writing

* Use descriptive, detailed captions
* Include your trigger word consistently: `[trigger]`
* Describe everything visible except the style/concept you want to teach the model

Dataset Diversity

* Vary poses, angles, and compositions
* Include different lighting conditions
* Mix close-ups with full scenes
* Avoid repetitive backgrounds

### [​](#training-parameters) Training Parameters

Learning Rate

* **LoRA Training**: 8e-5 to 1e-4
* **Full Fine-tuning**: 1e-5 to 5e-5
* Lower rates for style, higher for characters



Training Steps

* **Style LoRAs**: 1500-2500 steps
* **Character LoRAs**: 1500-3000 steps
* Monitor sample outputs to avoid overfitting



Resolution

* Start with 512px for faster iterations
* Use 1024px or higher for final training
* Use higher resolution if you want to capture macro details

## [​](#using-your-trained-lora) Using Your Trained LoRA

After training, you can use your LoRA with various tools:

* BFL API
* Python (Diffusers)
* ComfyUI

Upload your `.safetensors` in the Dashboard under [**Customization → Finetunes**](https://dashboard.bfl.ai/) and call the fine-tuned endpoint with the resulting `finetune_id` — no local GPU required.

```
import os, requests

response = requests.post(
    "https://api.bfl.ai/v1/flux-2-klein-9b-kv-finetuned",
    headers={"x-key": os.environ["BFL_API_KEY"], "Content-Type": "application/json"},
    json={
        "prompt": "a photo of ohwx in a garden on a sunny day",
        "finetune_id": "your-lora-id",
        "finetune_strength": 1.0,
    },
)
print(response.json())
```

See the [LoRA Inference guide](/flux_2/flux2_lora_inference) for the full endpoint reference and managed-serving details.

```
import torch
from diffusers import Flux2KleinPipeline

pipe = Flux2KleinPipeline.from_pretrained(
    "black-forest-labs/FLUX.2-klein-base-9B", torch_dtype=torch.bfloat16
)
pipe.load_lora_weights("path/to/your_lora.safetensors")
pipe.to("cuda")

image = pipe(
    "a photo of ohwx in a garden on a sunny day",  # Use your trigger word
    num_inference_steps=50,
    guidance_scale=4.0,
).images[0]
```

1. Place `.safetensors` file in `ComfyUI/models/loras/`
2. Add “Load LoRA” node to your workflow
3. Connect to your FLUX Klein model
4. Use trigger word in prompts

## [​](#next-steps) Next Steps

[## Training Example

Complete step-by-step guide with real dataset.](/flux_2/flux2_klein_training_example)

[## Serve via BFL API

Upload your LoRA to the Dashboard and serve it through a managed endpoint.](/flux_2/flux2_lora_inference)

[## Prompting Guide

Learn effective prompting techniques.](/guides/prompting_summary)

[## Model Downloads

Download [klein] Base models.](https://huggingface.co/black-forest-labs)

Was this page helpful?

YesNo

[Errors

Previous](/api_integration/errors)[FLUX.2 [klein] Style Training

Next](/flux_2/flux2_klein_training_example)

⌘I

[Black Forest Labs home page![light logo](https://mintcdn.com/bfl/OQ5B17YmedKOM4zs/logo/logo_light.png?fit=max&auto=format&n=OQ5B17YmedKOM4zs&q=85&s=a11f73fac1ef9254cffa5eb412269198)![dark logo](https://mintcdn.com/bfl/OQ5B17YmedKOM4zs/logo/logo_dark.png?fit=max&auto=format&n=OQ5B17YmedKOM4zs&q=85&s=d933d5452b84db18fc87cd6321e33d08)](/)

[x](https://x.com/bfl_ai)[github](https://github.com/black-forest-labs)[linkedin](https://www.linkedin.com/company/bflai)

Legal

[Impressum](https://bfl.ai/legal/imprint)[Developer Terms of Service](https://bfl.ai/legal/developer-terms-of-service)[Flux API Service Terms](https://bfl.ai/legal/flux-api-service-terms)[Terms of Use](https://bfl.ai/legal/terms-of-use)[Responsible AI Development Policy](https://bfl.ai/legal/responsible-ai-development-policy)[Usage Policy](https://bfl.ai/legal/usage-policy)[Intellectual Property Policy](https://bfl.ai/legal/intellectual-property-policy)[Privacy Policy](https://bfl.ai/legal/privacy-policy)

Company

[Careers](https://bfl.ai/careers)[Help Center](https://help.bfl.ai/)[Contact](https://bfl.ai/contact)

[x](https://x.com/bfl_ai)[github](https://github.com/black-forest-labs)[linkedin](https://www.linkedin.com/company/bflai)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=bfl)
