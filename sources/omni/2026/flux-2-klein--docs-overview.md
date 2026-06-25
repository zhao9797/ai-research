# Overview - Black Forest Labs
Source: https://docs.bfl.ai/flux_2/flux2_overview
Overview - Black Forest Labs
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

FLUX.2

Overview

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

* [What Can You Do?](#what-can-you-do)
* [Which Model to Choose?](#which-model-to-choose)
* [Compare FLUX.2 Models](#compare-flux-2-models)
  + [At a Glance](#at-a-glance)
* [FLUX.2 [klein] Models](#flux-2-klein-models)
  + [API Models](#api-models)
  + [Open Weights (Community)](#open-weights-community)
* [Preview Endpoints](#preview-endpoints)
* [Getting Started](#getting-started)

FLUX.2

# Overview

Copy page

FLUX.2 model family overview — from sub-second generation to highest quality, with multi-reference editing, color control, and up to 4MP output.

Copy page

![Black Forest](https://cdn.sanity.io/images/2gpum2i6/production/61cc0918403fa5644b7778bce4bd4020e8aef7cd-1920x1440.jpg)
**FLUX.2** spans the full spectrum of image generation—from **sub-second inference** with [klein] to **highest quality** with [max]. Generate photorealistic images with precise control over colors, poses, and composition, or edit existing images by referencing up to 10 sources simultaneously.
Choose **[klein]** for real-time, high-volume generation, **[pro]** for production at scale, **[flex]** for fine-grained control, or **[max]** for maximum quality and grounding search.

**Want to try first?** Test FLUX.2 [max], [pro], and [flex] in our [playground](https://playground.bfl.ai). [klein] is available via our [API](/flux_2/flux2_text_to_image) and on [Hugging Face](https://huggingface.co/black-forest-labs).

## [​](#what-can-you-do) What Can You Do?

* Multi-Reference
* Photorealism & Detail
* Grounding Search
* Typography & Text
* Exact Color Control
* Structured Prompting

Combine elements from multiple images while maintaining identity across complex scenes. Create ad variants with consistent faces, product mockups in any context, or fashion editorials where models stay consistent.

![](https://cdn.sanity.io/images/2gpum2i6/production/51696bb4ac2972e1dda5f3e68f748210f392c4f4-4861x1863.jpg)

Fashion editorial: 8 consistent characters from reference images

![](https://cdn.sanity.io/images/2gpum2i6/production/685f20ad37fedb0dcf7cc52c7b012c35734184e9-3392x1967.jpg)

Character + pose guidance combined

![](https://cdn.sanity.io/images/2gpum2i6/production/18bfb7b7d944ea6081babe2cb26ea3b445c993cf-3453x1863.jpg)

Input references used for the scene above

Generate photorealistic images with enhanced detail, texture, and lighting. FLUX.2 produces images that merge seamlessly with real photography—ideal for e-commerce and product marketing.

![](https://cdn.sanity.io/images/2gpum2i6/production/98f466fde69d875943d47cc6238c401d09780537-1440x1152.png)

Cinematic lighting

![](https://cdn.sanity.io/images/2gpum2i6/production/e62db22fa2b77c59d28d02d71133623bf1153cdc-1920x1920.jpg)

Realistic skin texture and lighting

![](https://cdn.sanity.io/images/2gpum2i6/production/20370abfd1d798f34419ccd241a068ca1c997ed2-1552x656.png)

Hyper-realistic close up

![](https://cdn.sanity.io/images/2gpum2i6/production/8be740a34ccb79731d3c4f59e67b73ca871b1d06-1552x656.png)

Product photography quality

Generate images grounded in real-time information with FLUX.2 [max]. It searches the web when needed, so you can create visuals of yesterday’s football game, the weather in real-time of any city, or re-create historical events.

![](https://cdn.sanity.io/images/2gpum2i6/production/5d9c090250ee74dcd77a9b600bafeb6e53c0f692-1680x1680.jpg)

Score of a previous football game

![](https://cdn.sanity.io/images/2gpum2i6/production/d7b0dd9dfc0236ad763cda9de4b17dea9f455b90-1936x1952.jpg)

The weather in real-time of Freiburg

![](https://cdn.sanity.io/images/2gpum2i6/production/23784cfd7989338315503484278d66ede410de02-2032x1808.jpg)

Re-create historical events: 'GC4Q+2V Berlin, Nov. 9th 1989'

![](https://cdn.sanity.io/images/2gpum2i6/production/13aa8ee65ef34a6a6b43f9417ff0de9dfda7b503-2032x1968.jpg)

Next Starlink satellite launch

Reliable text rendering for infographics, UI mockups, and marketing materials.

![](https://cdn.sanity.io/images/2gpum2i6/production/2355f71eb41d1da454ef3c1b820b3d7ce644bd16-1920x1920.jpg)

Data visualization with clean typography

![](https://cdn.sanity.io/images/2gpum2i6/production/216bd6da356153b3b3c9d3cce90225fab86fdc43-1440x960.jpg)

Ad creative with embedded text

![](https://cdn.sanity.io/images/2gpum2i6/production/00ddd4ce8b582891f3b174462dc635dac4e45d46-1456x1920.jpg)

Magazine cover layout

![](https://cdn.sanity.io/images/2gpum2i6/production/dd06b0f7b82ba5776e09d6827605733dcb5a7526-1456x1920.jpg)

Automotive ad with headline

Specify brand colors via hex codes with precision matching. No approximation—get the exact colors you need.**Example**: Gradient colors with hex codes**Prompt**: `A vase on a table in living room, the color of the vase is a gradient of color, starting with color #02eb3c and finishing with color #edfa3c. The flowers inside the vase have the color #ff0088`

![](https://cdn.sanity.io/images/2gpum2i6/production/3a3bf9b588602adf581f7293611b0e59fd50eadb-1552x1520.png)

Hex colors applied to vase and flowers

**Example**: Multiple hex colors for product design**Prompt**: `Luxury eyeshadow palette with 6 pans: top row #B76E79, #E8D5B7, #8B4789; bottom row #CD7F32, #F8F6F0, #800020`

![](https://cdn.sanity.io/images/2gpum2i6/production/0dc0c7638df1869005b1a502211e5f0bf967dfdc-1024x768.jpg)

Brand color matching

Use structured prompts for precise control over generation. Perfect for production workflows and automation.

Example: Structured Prompting

```
{
  "subject": "Mona Lisa painting by Leonardo da Vinci",
  "background": "museum gallery wall, ornate gold frame",
  "lighting": "soft gallery lighting, warm spotlights",
  "style": "digital art, high contrast",
  "camera_angle": "eye level view",
  "composition": "centered, portrait orientation"
}
```

![](https://cdn.sanity.io/images/2gpum2i6/production/bc12fcb7269c9449f2cbc3b1d1f54c59da4850e3-1456x1424.jpg)

Eye Level View

![](https://cdn.sanity.io/images/2gpum2i6/production/8c3fa60821f9e0f30de348f7827547cb82b564c9-1456x1424.jpg)

Worm's Eye View

## [​](#which-model-to-choose) Which Model to Choose?

|  | **[klein]** | **[max]** | **[pro]** | **[flex]** | **[dev]** |
| --- | --- | --- | --- | --- | --- |
| **Best for** | Real-time, high-volume | Highest quality, final assets | Production at scale | Quality with control | Local development |
| **Multi-reference** | Up to 4 | Up to 8 (API), 10 (playground) | Up to 8 (API), 10 (playground) | Up to 8 (API), 10 (playground) | Recommended max 6 |
| **Controls** | Standard | Standard | Standard | Adjustable steps & guidance | Full customization |
| **Grounding search** | No | Yes | No | No | No |
| **Pricing** | from $0.014 / image | from $0.07 / MP | from $0.03 / MP | $0.06 / MP | Free (non-commercial) |

**FLUX.2 [klein]** delivers sub-second inference with open weights. 4B runs on consumer GPUs (~13GB VRAM). Apache 2.0 for 4B, FLUX NCL for 9B. See [model details below](#flux2-klein-models).

**FLUX.2 [max]** includes **grounding search**: when prompted, it performs web searches to access real-time information to visualize trending products, current events, or the latest styles without manually sourcing reference material.

## [​](#compare-flux-2-models) Compare FLUX.2 Models

### [​](#at-a-glance) At a Glance

## [klein]

**Sub-second inference.** Our fastest models with open weights. Runs on consumer GPUs (~13GB VRAM). From $0.014/image via API, or run locally with Apache 2.0 (4B) / FLUX NCL (9B).

## [max]

**Maximum performance.** Highest editing consistency across tasks. Vast world knowledge. Strongest prompt following and faithful style representation.

## [pro]

**Top performance at affordable price.** The high quality, production-grade image editing and generation model.

## [flex]

**Specialized for typography.** Best for text rendering and preserving small details.

## [​](#flux-2-klein-models) FLUX.2 [klein] Models

![FLUX.2 [klein] diverse output examples](https://cdn.sanity.io/images/2gpum2i6/production/900de0722995119df9f27d799bdfed194d2112ac-2127x1400.jpg)

Diverse Outputs

**Open weights available**: [klein] 4B is fully open under **Apache 2.0**. [klein] 9B is available under the **FLUX Non-Commercial License**. Download from [Hugging Face](https://huggingface.co/black-forest-labs).

### [​](#api-models) API Models

|  | **[klein] 4B** | **[klein] 9B** |
| --- | --- | --- |
| **Best for** | High volume, local deployment | Balanced quality and speed |
| **Inference steps** | 4 (step-distilled) | 4 (step-distilled) |
| **Speed** | Sub-second | Sub-second |
| **API Pricing** | 0.014+0.014 + 0.014+0.001/MP | 0.015+0.015 + 0.015+0.002/MP |
| **License** | Apache 2.0 | FLUX Non-Commercial License |

### [​](#open-weights-community) Open Weights (Community)

The **Base** variants are undistilled foundation models with full training signal—ideal for fine-tuning, LoRA training, research, and custom pipelines. Higher output diversity than distilled models.

|  | **[klein] Base 4B** | **[klein] Base 9B** |
| --- | --- | --- |
| **Best for** | Fine-tuning, research, custom pipelines | Maximum quality, research |
| **Output diversity** | High | Highest |
| **Step-distilled** | No (full capacity) | No (full capacity) |
| **License** | Apache 2.0 | FLUX Non-Commercial License |
| **Availability** | [Hugging Face](https://huggingface.co/black-forest-labs) | [Hugging Face](https://huggingface.co/black-forest-labs) |

Base models are available as open weights for local development and research. They are not offered on the public API.

FLUX.2 [klein] does not include prompt upsampling. Write detailed, descriptive prompts for best results. See our [Prompting Guide](/guides/prompting_summary) for techniques.

## [​](#preview-endpoints) Preview Endpoints

Preview endpoints are where our latest improvements land first. They reflect our most recent advances in quality and speed.

| Endpoint | Description |
| --- | --- |
| `flux-2-pro-preview` | Our latest FLUX.2 [pro] model. |
| `flux-2-pro` | A fixed snapshot of FLUX.2 [pro]. This endpoint will not change, making it suitable for workflows that require reproducibility. |
| `flux-2-klein-9b-preview` | Our latest FLUX.2 [klein] 9B model with KV caching for improved performance. |
| `flux-2-klein-9b` | A fixed snapshot of FLUX.2 [klein] 9B. Choose this when you need reproducibility. |

**Which endpoint should I use?** For most use cases, the preview endpoints (`flux-2-pro-preview`, `flux-2-klein-9b-preview`) give you the best results. Choose the non-preview endpoints when you need a pinned model — for example, if your workflow depends on consistent outputs across runs or you have compliance requirements around model stability.

The `flux-2-pro` and `flux-2-klein-9b` endpoints are unchanged. If you are already using them, no action is required.

Both preview and non-preview endpoints share the same API contract — the request and response format is identical. Only the underlying model weights differ.

## [​](#getting-started) Getting Started

[## Try in Playground

Test FLUX.2 [max], [pro], and [flex] in your browser. No setup required.](https://playground.bfl.ai)

[## Download [klein] Weights

Get [klein] weights from Hugging Face for local inference.](https://huggingface.co/black-forest-labs)

[## Text-to-Image API

Generate images from text prompts.](/flux_2/flux2_text_to_image)

[## Image Editing API

Edit images with multi-reference support.](/flux_2/flux2_image_editing)

[## Prompting Guide

Master prompting techniques — basics, style, JSON, editing, and use cases.](/guides/prompting_summary)

[## Local Development

Download [dev] weights for local inference.](https://huggingface.co/black-forest-labs/FLUX.2-dev)

Was this page helpful?

YesNo

[Credits & Billing

Previous](/account_management/credits_billing)[FLUX.2 Image Editing

Next](/flux_2/flux2_image_editing)

⌘I

[Black Forest Labs home page![light logo](https://mintcdn.com/bfl/OQ5B17YmedKOM4zs/logo/logo_light.png?fit=max&auto=format&n=OQ5B17YmedKOM4zs&q=85&s=a11f73fac1ef9254cffa5eb412269198)![dark logo](https://mintcdn.com/bfl/OQ5B17YmedKOM4zs/logo/logo_dark.png?fit=max&auto=format&n=OQ5B17YmedKOM4zs&q=85&s=d933d5452b84db18fc87cd6321e33d08)](/)

[x](https://x.com/bfl_ai)[github](https://github.com/black-forest-labs)[linkedin](https://www.linkedin.com/company/bflai)

Legal

[Impressum](https://bfl.ai/legal/imprint)[Developer Terms of Service](https://bfl.ai/legal/developer-terms-of-service)[Flux API Service Terms](https://bfl.ai/legal/flux-api-service-terms)[Terms of Use](https://bfl.ai/legal/terms-of-use)[Responsible AI Development Policy](https://bfl.ai/legal/responsible-ai-development-policy)[Usage Policy](https://bfl.ai/legal/usage-policy)[Intellectual Property Policy](https://bfl.ai/legal/intellectual-property-policy)[Privacy Policy](https://bfl.ai/legal/privacy-policy)

Company

[Careers](https://bfl.ai/careers)[Help Center](https://help.bfl.ai/)[Contact](https://bfl.ai/contact)

[x](https://x.com/bfl_ai)[github](https://github.com/black-forest-labs)[linkedin](https://www.linkedin.com/company/bflai)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=bfl)

![](https://cdn.sanity.io/images/2gpum2i6/production/18bfb7b7d944ea6081babe2cb26ea3b445c993cf-3453x1863.jpg)

![](https://cdn.sanity.io/images/2gpum2i6/production/685f20ad37fedb0dcf7cc52c7b012c35734184e9-3392x1967.jpg)

![](https://cdn.sanity.io/images/2gpum2i6/production/e62db22fa2b77c59d28d02d71133623bf1153cdc-1920x1920.jpg)

![](https://cdn.sanity.io/images/2gpum2i6/production/51696bb4ac2972e1dda5f3e68f748210f392c4f4-4861x1863.jpg)

![](https://cdn.sanity.io/images/2gpum2i6/production/5d9c090250ee74dcd77a9b600bafeb6e53c0f692-1680x1680.jpg)

![](https://cdn.sanity.io/images/2gpum2i6/production/d7b0dd9dfc0236ad763cda9de4b17dea9f455b90-1936x1952.jpg)

![](https://cdn.sanity.io/images/2gpum2i6/production/23784cfd7989338315503484278d66ede410de02-2032x1808.jpg)

![](https://cdn.sanity.io/images/2gpum2i6/production/13aa8ee65ef34a6a6b43f9417ff0de9dfda7b503-2032x1968.jpg)

![](https://cdn.sanity.io/images/2gpum2i6/production/2355f71eb41d1da454ef3c1b820b3d7ce644bd16-1920x1920.jpg)

![](https://cdn.sanity.io/images/2gpum2i6/production/98f466fde69d875943d47cc6238c401d09780537-1440x1152.png)

![](https://cdn.sanity.io/images/2gpum2i6/production/216bd6da356153b3b3c9d3cce90225fab86fdc43-1440x960.jpg)

![](https://cdn.sanity.io/images/2gpum2i6/production/00ddd4ce8b582891f3b174462dc635dac4e45d46-1456x1920.jpg)

![](https://cdn.sanity.io/images/2gpum2i6/production/dd06b0f7b82ba5776e09d6827605733dcb5a7526-1456x1920.jpg)

![](https://cdn.sanity.io/images/2gpum2i6/production/8be740a34ccb79731d3c4f59e67b73ca871b1d06-1552x656.png)

![](https://cdn.sanity.io/images/2gpum2i6/production/20370abfd1d798f34419ccd241a068ca1c997ed2-1552x656.png)

![](https://cdn.sanity.io/images/2gpum2i6/production/0dc0c7638df1869005b1a502211e5f0bf967dfdc-1024x768.jpg)

![](https://cdn.sanity.io/images/2gpum2i6/production/bc12fcb7269c9449f2cbc3b1d1f54c59da4850e3-1456x1424.jpg)

![](https://cdn.sanity.io/images/2gpum2i6/production/8c3fa60821f9e0f30de348f7827547cb82b564c9-1456x1424.jpg)

![FLUX.2 [klein] diverse output examples](https://cdn.sanity.io/images/2gpum2i6/production/900de0722995119df9f27d799bdfed194d2112ac-2127x1400.jpg)

![](https://cdn.sanity.io/images/2gpum2i6/production/3a3bf9b588602adf581f7293611b0e59fd50eadb-1552x1520.png)
