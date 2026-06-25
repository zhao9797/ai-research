# FLUX.2 [klein]: Towards Interactive Visual Intelligence | Black Forest Labs
Source: https://bfl.ai/blog/flux2-klein-towards-interactive-visual-intelligence
FLUX.2 [klein]: Towards Interactive Visual Intelligence | Black Forest Labs

* Models
* [Research](/research)
* API
* Open Weights
* [Enterprise](/enterprise)
* Resources

[Contact Sales](/contact)[Get started](https://dashboard.bfl.ai/?landing_page=%2Fblog%2Fflux2-klein-towards-interactive-visual-intelligence)

[Back to index](/blog)

January 15, 2026

# FLUX.2 [klein]: Towards Interactive Visual Intelligence

ModelsNewsResearch
![FLUX.2 [klein]: Towards Interactive Visual Intelligence](/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2F2gpum2i6%2Fproduction%2F41055678178f6fe75ca618b854b195e48dfc55ed-2127x1400.jpg&w=3840&q=75)

## **FLUX.2 [klein]: Towards Interactive Visual Intelligence**

Today, we release the FLUX.2 [klein] model family, our fastest image models to date. FLUX.2 [klein] unifies generation and editing in a single compact architecture, delivering state-of-the-art quality with end-to-end inference as low as under a second. Built for applications that require real-time image generation without sacrificing quality, and runs on consumer hardware with as little as 13GB VRAM.

[**Try it now for free here**](https://bfl.ai/models/flux-2-klein#try-demo)

![](/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2F2gpum2i6%2Fproduction%2F2bd2ec8704480a772cf35f1017ffb8488aab630c-1280x720.gif&w=3840&q=75)

*Demo showing editing with FLUX.2 [klein]*

### **Why go [klein]?**

Visual Intelligence is entering a new era. As AI agents become more capable, they need visual generation that can keep up; models that respond in real-time, iterate quickly, and run efficiently on accessible hardware.

The *klein* name comes from the German word for "small", reflecting both the compact model size and the minimal latency. But FLUX.2 [klein] is anything but limited. These models deliver exceptional performance in text-to-image generation, image editing and multi-reference generation, typically reserved for much larger models.

### **What's New**

* Sub-second inference. Generate or edit images in under 0.5s on modern hardware.
* Photorealistic outputs and high diversity, especially in the base variants.
* Unified generation and editing. Text-to-image, image editing, and multi-reference support in a single model while delivering frontier performance.
* Runs on consumer GPUs. The 4B model fits in ~13GB VRAM (RTX 3090/4070 and above).
* Developer-friendly & Accessible: Apache 2.0 on 4B models, open weights for 9B models. Full open weights for customization and fine-tuning.
* API and open weights. Production-ready API or run locally with full weights.

*Note: The “FLUX [dev] Non-Commercial License” has been renamed to “FLUX Non-Commercial License” and will apply to the 9B Klein models. No material changes have been made to the license.*

![](/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2F2gpum2i6%2Fproduction%2F41055678178f6fe75ca618b854b195e48dfc55ed-2127x1400.jpg&w=3840&q=75)

*Text to Image collage using FLUX.2 [klein]*

### **The FLUX.2 [klein] Model Family**

#### **FLUX.2 [klein] 9B**

Our flagship small model. Defines the Pareto frontier for quality vs. latency across text-to-image, single-reference editing, and multi-reference generation. Matches or exceeds models 5x its size - in under half a second. Built on a 9B flow model with 8B Qwen3 text embedder, step-distilled to 4 inference steps.

Combine multiple input images, blend concepts, and iterate on complex compositions - all at sub-second speed with frontier-level quality. No model this fast has ever done this well.

**License**: FLUX NCL

![](/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2F2gpum2i6%2Fproduction%2F86adb8bf9ea077f3aebe392af1077f0337ed9c48-4544x2805.jpg&w=3840&q=75)

*Imagine editing collage using FLUX.2 [klein]*

#### **FLUX.2 [klein] 4B:**

Fully open under Apache 2.0. Our most accessible model, it runs on consumer GPUs like the RTX 3090/4070. Compact but capable: supports T2I, I2I, and multi-reference at quality that punches above its size. Built for local development and edge deployment.

**License**: Apache 2.0

#### **FLUX.2 [klein] Base 9B / 4B:**

The full-capacity foundation models. Undistilled, preserving complete training signal for maximum flexibility. Ideal for fine-tuning, LoRA training, research, and custom pipelines where control matters more than speed. Higher output diversity than the distilled models.

**License**: 4B Base under Apache 2.0, 9B Base under FLUX NCL

![](/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2F2gpum2i6%2Fproduction%2F900de0722995119df9f27d799bdfed194d2112ac-2127x1400.jpg&w=3840&q=75)

*Output Diversity using FLUX.2 [klein]*

#### **Quantized versions**

We are also releasing FP8 and NVFP4 versions of all [klein] variants, developed in collaboration with NVIDIA for optimized inference on RTX GPUs. Same capabilities, smaller footprint - compatible with even more hardware.

* **FP8:** Up to 1.6x faster, up to 40% less VRAM
* **NVFP4:** Up to 2.7x faster, up to 55% less VRAM

*Benchmarks on RTX 5080/5090, T2I at 1024×1024*Same licenses apply: Apache 2.0 for 4B variants, FLUX NCL for 9B.

#### **Performance Analysis**

![](/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2F2gpum2i6%2Fproduction%2F8ece18115cc75a4d34c42eda81a68bbd78048666-3548x1173.jpg&w=3840&q=75)

![](/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2F2gpum2i6%2Fproduction%2Fc29dea8ec862d79ecdc82e8013f37ee22a148cb8-3541x1173.jpg&w=3840&q=75)

***FLUX.2 [klein] Elo vs Latency (top) and VRAM (bottom) across Text-to-Image, Image-to-Image Single Reference, and Multi-Reference tasks.*** *FLUX.2 [klein] matches or exceeds Qwen's quality at a fraction of the latency and VRAM, and outperforms Z-Image while supporting both text-to-image generation and (multi-reference) image editing in a unified model. The base variants trade some speed for full customizability and fine-tuning, making them better suited for research and adaptation to specific use cases. Speed is measured on a GB200 in bf16.*

### **Into the New**

FLUX.2 [klein] is more than a faster model. It's a step toward our vision of interactive visual intelligence. We believe the future belongs to creators and developers with AI that can see, create, and iterate in real-time. Systems that enable new categories of applications: real-time design tools, agentic visual reasoning, interactive content creation.

### **Resources**

**Try it**

* [Demo](https://bfl.ai/models/flux-2-klein#try-demo)
* [Playground](https://bfl.ai/play)
* [HF Space for [klein] 9B](https://huggingface.co/spaces/black-forest-labs/FLUX.2-klein-9B), [HF Space for [klein] 4B](https://huggingface.co/spaces/black-forest-labs/FLUX.2-klein-4B)

**Build with it**

* [Documentation](https://docs.bfl.ai/flux_2/flux2_overview#flux-2-%5Bklein%5D-models)
* [GitHub](https://github.com/black-forest-labs/flux2)
* [Model Weights](https://huggingface.co/collections/black-forest-labs/flux2)

**Learn more**

* <https://bfl.ai/models/flux-2-klein>

Previous article[Laying the Foundations for Visual Intelligence—Our $300M Series B](/blog/our-300m-series-b)

Next article[Capable, Open, and Safe: Combating AI Misuse](/blog/capable-open-and-safe-combating-ai-misuse)

![](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fbg-footer.c5582a35.png&w=3840&q=75&dpl=dpl_BhmvaEa9MS3ThkDo1YH7YVDvxZBK)

Models

[FLUX.2 Max](/models/flux-2-max)[FLUX.2](/models/flux-2)[FLUX.2 Klein](/models/flux-2-klein)[Flux Tools](/models/flux-tools)

API

[Documentation](https://docs.bfl.ai)[Pricing](/pricing)[Dashboard](https://dashboard.bfl.ai)[Status](https://status.bfl.ai)

Open Weights

[Licensing](/licensing)[Hugging Face](https://huggingface.co/black-forest-labs)[GitHub](https://github.com/black-forest-labs/flux)

Resources

[Documentation](https://docs.bfl.ai)[Help Desk](https://help.bfl.ai)[Blog](/blog)[Creator Program](/creator-program)[Brand](/brand)[GitHub](https://github.com/black-forest-labs)

Company

[About Us](/about)[Careers](/careers)[Trust and Security](https://app.vanta.com/blackforestlabs.ai/trust/0cb6ffww8qmy60nxzo3p5)[Contact Us](/contact)

 [ISO 27001:2022](https://app.vanta.com/blackforestlabs.ai/trust/0cb6ffww8qmy60nxzo3p5)

[SOC 2 Type II](https://app.vanta.com/blackforestlabs.ai/trust/0cb6ffww8qmy60nxzo3p5)

Enterprise

[Learn More](/enterprise)[Contact Sales](/contact)

Legal

[Imprint](/legal/imprint)[Terms of Service](/legal/terms-of-service)[Usage Policy](/legal/usage-policy)[Privacy Policy](/legal/privacy-policy)[Intellectual Property Policy](/legal/intellectual-property-policy)

[Developer Terms of Service](/legal/developer-terms-of-service)[FLUX API Service Terms](/legal/flux-api-service-terms)[Self-Hosted Terms of Service](/legal/self-hosted-commercial-license-terms)[Non-Commercial License Terms](/legal/non-commercial-license-terms)[Responsible AI Development Policy](/legal/responsible-ai-development-policy)[Training Data Disclosure](/transparency)

All rights reserved.

©2026 BLACK FOREST LABS.
