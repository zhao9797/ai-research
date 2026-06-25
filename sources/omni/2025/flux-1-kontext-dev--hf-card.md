# black-forest-labs/FLUX.1-Kontext-dev · Hugging Face
Source: https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev
black-forest-labs/FLUX.1-Kontext-dev · Hugging Face



[![Hugging Face's logo](/front/assets/huggingface_logo-noborder.svg) Hugging Face](/)

* [Models](/models)
* [Datasets](/datasets)
* [Spaces](/spaces)
* [Buckets new](/storage)
* [Docs](/docs)
* [Enterprise](/enterprise)
* [Pricing](/pricing)
* + Website

    - [Tasks](/tasks)
    - [HuggingChat](/chat)
    - [Collections](/collections)
    - [Languages](/languages)
    - [Organizations](/organizations)
  + Community

    - [Blog](/blog/zh)
    - [Posts](/posts)
    - [Daily Papers](/papers)
    - [Learn](/learn)
    - [Discord](/join/discord)
    - [Forum](https://discuss.huggingface.co/)
    - [GitHub](https://github.com/huggingface)
  + Solutions

    - [Team & Enterprise](/enterprise)
    - [Hugging Face PRO](/pro)
    - [Enterprise Support](/support)
    - [Inference Providers](/inference/models)
    - [Inference Endpoints](/inference-endpoints)
    - [Storage Buckets](/storage)
* ---
* [Log In](/login)
* [Sign Up](/join)

      

# [black-forest-labs](/black-forest-labs) / [FLUX.1-Kontext-dev](/black-forest-labs/FLUX.1-Kontext-dev) like 2.67k Follow Black Forest Labs 38.5k

[Image-to-Image](/models?pipeline_tag=image-to-image)[Diffusers](/models?library=diffusers)[Safetensors](/models?library=safetensors)[Diffusion Single File](/models?library=diffusion-single-file)[English](/models?language=en)[image-generation](/models?other=image-generation)[flux](/models?other=flux)

arxiv: 2506.15742

License: flux-1-dev-non-commercial-license

[Model card](/black-forest-labs/FLUX.1-Kontext-dev)  [Files Files and versions  

xet](/black-forest-labs/FLUX.1-Kontext-dev/tree/main)  [Community

85](/black-forest-labs/FLUX.1-Kontext-dev/discussions)

 

Deploy

  Copy to bucket new   

Use this model  

### Instructions to use black-forest-labs/FLUX.1-Kontext-dev with libraries, inference providers, notebooks, and local apps. Follow these links to get started.

* Libraries
* [Diffusers](/black-forest-labs/FLUX.1-Kontext-dev?library=diffusers) 

  How to use black-forest-labs/FLUX.1-Kontext-dev with Diffusers:

  ```
  pip install -U diffusers transformers accelerate
  ```

  ```
  import torch
  from diffusers import DiffusionPipeline
  from diffusers.utils import load_image

  # switch to "mps" for apple devices
  pipe = DiffusionPipeline.from_pretrained("black-forest-labs/FLUX.1-Kontext-dev", dtype=torch.bfloat16, device_map="cuda")

  prompt = "Turn this cat into a dog"
  input_image = load_image("https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/diffusers/cat.png")

  image = pipe(image=input_image, prompt=prompt).images[0]
  ```
* [Diffusion Single File](/black-forest-labs/FLUX.1-Kontext-dev?library=diffusion-single-file) 

  How to use black-forest-labs/FLUX.1-Kontext-dev with Diffusion Single File:

  ```
  # No code snippets available yet for this library.

  # To use this model, check the repository files and the library's documentation.

  # Want to help? PRs adding snippets are welcome at:
  # https://github.com/huggingface/huggingface.js
  ```
* Inference
* Inference Providers
 * Notebooks
* [Google Colab](/black-forest-labs/FLUX.1-Kontext-dev/colab)
* [Kaggle](/black-forest-labs/FLUX.1-Kontext-dev/kaggle)

## You need to agree to share your contact information to access this model

This repository is publicly accessible, but you have to accept the conditions to access its files and content.

By clicking "Agree", you agree to the [FluxDev Non-Commercial License Agreement](https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev/blob/main/LICENSE.md) and acknowledge the [Acceptable Use Policy](https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev/blob/main/POLICY.md).

 

[Log in](/login?next=%2Fblack-forest-labs%2FFLUX.1-Kontext-dev) or [Sign Up](/join?next=%2Fblack-forest-labs%2FFLUX.1-Kontext-dev) to review the conditions and access this model content.

 

* [Key Features](#key-features "Key Features")
* [Usage](#usage "Usage")
  + [API Endpoints](#api-endpoints "API Endpoints")
    - [Using with diffusers 🧨](#using-with-diffusers-🧨 "Using with diffusers 🧨")
* [Risks](#risks "Risks")
* [License](#license "License")
* [Citation](#citation "Citation")

[![FLUX.1 [dev] Grid](/black-forest-labs/FLUX.1-Kontext-dev/media/main/teaser.png)](/black-forest-labs/FLUX.1-Kontext-dev/blob/main/teaser.png)

`FLUX.1 Kontext [dev]` is a 12 billion parameter rectified flow transformer capable of editing images based on text instructions.
For more information, please read our [blog post](https://bfl.ai/announcements/flux-1-kontext-dev) and our [technical report](https://arxiv.org/abs/2506.15742). You can find information about the `[pro]` version in [here](https://bfl.ai/models/flux-kontext).

# Key Features

1. Change existing images based on an edit instruction.
2. Have character, style and object reference without any finetuning.
3. Robust consistency allows users to refine an image through multiple successive edits with minimal visual drift.
4. Trained using guidance distillation, making `FLUX.1 Kontext [dev]` more efficient.
5. Open weights to drive new scientific research, and empower artists to develop innovative workflows.
6. Generated outputs can be used for personal, scientific, and commercial purposes, as described in the [FLUX.1 [dev] Non-Commercial License](https://github.com/black-forest-labs/flux/blob/main/model_licenses/LICENSE-FLUX1-dev).

# Usage

We provide a reference implementation of `FLUX.1 Kontext [dev]`, as well as sampling code, in a dedicated [github repository](https://github.com/black-forest-labs/flux).
Developers and creatives looking to build on top of `FLUX.1 Kontext [dev]` are encouraged to use this as a starting point.

`FLUX.1 Kontext [dev]` is also available in both [ComfyUI](https://github.com/comfyanonymous/ComfyUI) and [Diffusers](https://github.com/huggingface/diffusers).

## API Endpoints

The FLUX.1 Kontext models are also available via API from the following sources

* bfl.ai: <https://docs.bfl.ai/>
* DataCrunch: <https://datacrunch.io/managed-endpoints/flux-kontext>
* fal: <https://fal.ai/flux-kontext>
* Replicate: <https://replicate.com/blog/flux-kontext>
  + <https://replicate.com/black-forest-labs/flux-kontext-dev>
  + <https://replicate.com/black-forest-labs/flux-kontext-pro>
  + <https://replicate.com/black-forest-labs/flux-kontext-max>
* Runware: <https://runware.ai/blog/introducing-flux1-kontext-instruction-based-image-editing-with-ai?utm_source=bfl>
* TogetherAI: <https://www.together.ai/models/flux-1-kontext-dev>

### Using with diffusers 🧨

```
# Install diffusers from the main branch until future stable release
pip install git+https://github.com/huggingface/diffusers.git
```

Image editing:

```
import torch
from diffusers import FluxKontextPipeline
from diffusers.utils import load_image

pipe = FluxKontextPipeline.from_pretrained("black-forest-labs/FLUX.1-Kontext-dev", torch_dtype=torch.bfloat16)
pipe.to("cuda")

input_image = load_image("https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/diffusers/cat.png")

image = pipe(
  image=input_image,
  prompt="Add a hat to the cat",
  guidance_scale=2.5
).images[0]
```

Flux Kontext comes with an integrity checker, which should be run after the image generation step. To run the safety checker, install the official repository from [black-forest-labs/flux](https://github.com/black-forest-labs/flux) and add the following code:

```
import torch
import numpy as np
from flux.content_filters import PixtralContentFilter

integrity_checker = PixtralContentFilter(torch.device("cuda"))
image_ = np.array(image) / 255.0
image_ = 2 * image_ - 1
image_ = torch.from_numpy(image_).to("cuda", dtype=torch.float32).unsqueeze(0).permute(0, 3, 1, 2)
if integrity_checker.test_image(image_):
raise ValueError("Your image has been flagged. Choose another prompt/image or try again.")
```

For VRAM saving measures and speed ups check out the [diffusers docs](https://huggingface.co/docs/diffusers/en/index)

---

# Risks

Black Forest Labs is committed to the responsible development of generative AI technology. Prior to releasing FLUX.1 Kontext, we evaluated and mitigated a number of risks in our models and services, including the generation of unlawful content. We implemented a series of pre-release mitigations to help prevent misuse by third parties, with additional post-release mitigations to help address residual risks:

1. **Pre-training mitigation**. We filtered pre-training data for multiple categories of “not safe for work” (NSFW) content to help prevent a user generating unlawful content in response to text prompts or uploaded images.
2. **Post-training mitigation.** We have partnered with the Internet Watch Foundation, an independent nonprofit organization dedicated to preventing online abuse, to filter known child sexual abuse material (CSAM) from post-training data. Subsequently, we undertook multiple rounds of targeted fine-tuning to provide additional mitigation against potential abuse. By inhibiting certain behaviors and concepts in the trained model, these techniques can help to prevent a user generating synthetic CSAM or nonconsensual intimate imagery (NCII) from a text prompt, or transforming an uploaded image into synthetic CSAM or NCII.
3. **Pre-release evaluation.** Throughout this process, we conducted multiple internal and external third-party evaluations of model checkpoints to identify further opportunities for improvement. The third-party evaluations—which included 21 checkpoints of FLUX.1 Kontext [pro] and [dev]—focused on eliciting CSAM and NCII through adversarial testing with text-only prompts, as well as uploaded images with text prompts. Next, we conducted a final third-party evaluation of the proposed release checkpoints, focused on text-to-image and image-to-image CSAM and NCII generation. The final FLUX.1 Kontext [pro] (as offered through the FLUX API only) and FLUX.1 Kontext [dev] (released as an open-weight model) checkpoints demonstrated very high resilience against violative inputs, and FLUX.1 Kontext [dev] demonstrated higher resilience than other similar open-weight models across these risk categories. Based on these findings, we approved the release of the FLUX.1 Kontext [pro] model via API, and the release of the FLUX.1 Kontext [dev] model as openly-available weights under a non-commercial license to support third-party research and development.
4. **Inference filters.** We are applying multiple filters to intercept text prompts, uploaded images, and output images on the FLUX API for FLUX.1 Kontext [pro]. Filters for CSAM and NCII are provided by Hive, a third-party provider, and cannot be adjusted or removed by developers. We provide filters for other categories of potentially harmful content, including gore, which can be adjusted by developers based on their specific risk profile. Additionally, the repository for the open FLUX.1 Kontext [dev] model includes filters for illegal or infringing content. Filters or manual review must be used with the model under the terms of the FLUX.1 [dev] Non-Commercial License. We may approach known deployers of the FLUX.1 Kontext [dev] model at random to verify that filters or manual review processes are in place.
5. **Content provenance.** The FLUX API applies cryptographically-signed metadata to output content to indicate that images were produced with our model. Our API implements the Coalition for Content Provenance and Authenticity (C2PA) standard for metadata.
6. **Policies.** Access to our API and use of our models are governed by our Developer Terms of Service, Usage Policy, and FLUX.1 [dev] Non-Commercial License, which prohibit the generation of unlawful content or the use of generated content for unlawful, defamatory, or abusive purposes. Developers and users must consent to these conditions to access the FLUX Kontext models.
7. **Monitoring.** We are monitoring for patterns of violative use after release, and may ban developers who we detect intentionally and repeatedly violate our policies via the FLUX API. Additionally, we provide a dedicated email address ([safety@blackforestlabs.ai](mailto:safety@blackforestlabs.ai)) to solicit feedback from the community. We maintain a reporting relationship with organizations such as the Internet Watch Foundation and the National Center for Missing and Exploited Children, and we welcome ongoing engagement with authorities, developers, and researchers to share intelligence about emerging risks and develop effective mitigations.

# License

This model falls under the [FLUX.1 [dev] Non-Commercial License](https://github.com/black-forest-labs/flux/blob/main/model_licenses/LICENSE-FLUX1-dev).

# Citation

```
@misc{labs2025flux1kontextflowmatching,
      title={FLUX.1 Kontext: Flow Matching for In-Context Image Generation and Editing in Latent Space}, Add commentMore actions
      author={Black Forest Labs and Stephen Batifol and Andreas Blattmann and Frederic Boesel and Saksham Consul and Cyril Diagne and Tim Dockhorn and Jack English and Zion English and Patrick Esser and Sumith Kulal and Kyle Lacey and Yam Levi and Cheng Li and Dominik Lorenz and Jonas Müller and Dustin Podell and Robin Rombach and Harry Saini and Axel Sauer and Luke Smith},
      year={2025},
      eprint={2506.15742},
      archivePrefix={arXiv},
      primaryClass={cs.GR},
      url={https://arxiv.org/abs/2506.15742},
}
```

Downloads last month
:   135,313

 

Inference Providers [NEW](https://huggingface.co/docs/inference-providers)

fal

[Image-to-Image](/tasks/image-to-image "Learn more about image-to-image")

 

Drag image file here or click to browse from your device

Browse for image

  (Optional) Text-guidance if the model has support for it   Generate

View Code Snippets

Maximize

## Model tree for black-forest-labs/FLUX.1-Kontext-dev

Adapters

 [244 models](/models?other=base_model:adapter:black-forest-labs/FLUX.1-Kontext-dev)

Finetunes

 [59 models](/models?other=base_model:finetune:black-forest-labs/FLUX.1-Kontext-dev)

Quantizations

 [18 models](/models?other=base_model:quantized:black-forest-labs/FLUX.1-Kontext-dev)

  

## Spaces using black-forest-labs/FLUX.1-Kontext-dev 100

[![](https://cdn-avatars.huggingface.co/v1/production/uploads/633f7a8f4be90e06da248e0f/m5YoF33abJ09vcwFxt1Mj.png)

black-forest-labs/FLUX.1-Kontext-Dev](/spaces/black-forest-labs/FLUX.1-Kontext-Dev) [👽

prithivMLmods/Photo-Mate-i2i](/spaces/prithivMLmods/Photo-Mate-i2i) [✏️

wcy1122/DreamOmni2-Edit](/spaces/wcy1122/DreamOmni2-Edit) [⚡

Yuanshi/FLUX.1-Kontext-Turbo](/spaces/Yuanshi/FLUX.1-Kontext-Turbo) [🌍🧞‍♀️

AlekseyCalvin/fast-Kontext-Flux-LoRAs-bySilverAgePoets](/spaces/AlekseyCalvin/fast-Kontext-Flux-LoRAs-bySilverAgePoets) [🖼️

wcy1122/DreamOmni2-Gen](/spaces/wcy1122/DreamOmni2-Gen) [👀

rizavelioglu/vae-comparison](/spaces/rizavelioglu/vae-comparison) [🌍

ChenDY/NAG\_FLUX.1-Kontext-Dev](/spaces/ChenDY/NAG_FLUX.1-Kontext-Dev)  + 95 Spaces + 92 Spaces

 

## Collection including black-forest-labs/FLUX.1-Kontext-dev

[#### FLUX.1

Collection

A collection of our FLUX.1 models and LoRAs. • 13 items • Updated Jan 2 •  329](/collections/black-forest-labs/flux1)

 

## Paper for black-forest-labs/FLUX.1-Kontext-dev

[#### FLUX.1 Kontext: Flow Matching for In-Context Image Generation and Editing in Latent Space

Paper • 2506.15742 • Published Jun 17, 2025 •  9](/papers/2506.15742)

 

System theme

Company

[TOS](/terms-of-service) [Privacy](/privacy) [About](/huggingface) [Careers](https://apply.workable.com/huggingface/) 

Website

[Models](/models) [Datasets](/datasets) [Spaces](/spaces) [Pricing](/pricing) [Docs](/docs)



Inference providers allow you to run inference using different serverless providers.

## Run 15,000+ Models Instantly

Inference Providers let you run inference on thousands of models served by our partners using a simple,
unified, OpenAI-compatible serverless API ([Learn more](/docs/inference-providers)).

black-forest-labs/FLUX.1-Kontext-dev is supported by the following Inference Providers:

WaveSpeed

Replicate

fal

View API Code Dismiss
