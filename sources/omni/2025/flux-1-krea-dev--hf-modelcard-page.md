# black-forest-labs/FLUX.1-Krea-dev · Hugging Face
Source: https://huggingface.co/black-forest-labs/FLUX.1-Krea-dev
black-forest-labs/FLUX.1-Krea-dev · Hugging Face



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

      

# [black-forest-labs](/black-forest-labs) / [FLUX.1-Krea-dev](/black-forest-labs/FLUX.1-Krea-dev) like 869 Follow Black Forest Labs 38.5k

[Text-to-Image](/models?pipeline_tag=text-to-image)[Diffusers](/models?library=diffusers)[Safetensors](/models?library=safetensors)[English](/models?language=en)[FluxPipeline](/models?other=diffusers%3AFluxPipeline)[image-generation](/models?other=image-generation)[flux](/models?other=flux)

License: flux-1-dev-non-commercial-license

[Model card](/black-forest-labs/FLUX.1-Krea-dev)  [Files Files and versions  

xet](/black-forest-labs/FLUX.1-Krea-dev/tree/main)  [Community

17](/black-forest-labs/FLUX.1-Krea-dev/discussions)

 

Deploy

  Copy to bucket new   

Use this model  

### Instructions to use black-forest-labs/FLUX.1-Krea-dev with libraries, inference providers, notebooks, and local apps. Follow these links to get started.

* Libraries
* [Diffusers](/black-forest-labs/FLUX.1-Krea-dev?library=diffusers) 

  How to use black-forest-labs/FLUX.1-Krea-dev with Diffusers:

  ```
  pip install -U diffusers transformers accelerate
  ```

  ```
  import torch
  from diffusers import DiffusionPipeline

  # switch to "mps" for apple devices
  pipe = DiffusionPipeline.from_pretrained("black-forest-labs/FLUX.1-Krea-dev", dtype=torch.bfloat16, device_map="cuda")

  prompt = "Astronaut in a jungle, cold color palette, muted colors, detailed, 8k"
  image = pipe(prompt).images[0]
  ```
* Inference
* Inference Providers
 * Notebooks
* [Google Colab](/black-forest-labs/FLUX.1-Krea-dev/colab)
* [Kaggle](/black-forest-labs/FLUX.1-Krea-dev/kaggle)
 * Local Apps [Settings](/settings/local-apps "Set up your favorite local applications")
 * [Draw Things](https://drawthings.ai/import/diffusers/pipeline.from_pretrained?repo_id=black-forest-labs/FLUX.1-Krea-dev)
* [DiffusionBee](https://diffusionbee.com/huggingface_import?model_id=black-forest-labs/FLUX.1-Krea-dev)

## You need to agree to share your contact information to access this model

This repository is publicly accessible, but you have to accept the conditions to access its files and content.

By clicking "Agree", you agree to the [FluxDev Non-Commercial License Agreement](https://huggingface.co/black-forest-labs/FLUX.1-dev/blob/main/LICENSE.md) and acknowledge the [Acceptable Use Policy](https://huggingface.co/black-forest-labs/FLUX.1-dev/blob/main/POLICY.md).

 

[Log in](/login?next=%2Fblack-forest-labs%2FFLUX.1-Krea-dev) or [Sign Up](/join?next=%2Fblack-forest-labs%2FFLUX.1-Krea-dev) to review the conditions and access this model content.

 

* [Key Features](#key-features "Key Features")
* [Usage](#usage "Usage")
  + [ComfyUI](#comfyui "ComfyUI")
  + [🧨 diffusers](#🧨-diffusers "🧨 diffusers")
* [Limitations](#limitations "Limitations")
* [Out-of-Scope Use](#out-of-scope-use "Out-of-Scope Use")
* [Risks](#risks "Risks")
* [License](#license "License")

[![FLUX.1 Krea [dev] Grid](/black-forest-labs/FLUX.1-Krea-dev/media/main/teaser.png)](/black-forest-labs/FLUX.1-Krea-dev/blob/main/teaser.png)

`FLUX.1 Krea [dev]` is a 12 billion parameter rectified flow transformer capable of generating images from text descriptions.
For more information, please read our [blog post](https://bfl.ai/announcements/flux-1-krea-dev) and [Krea's blog post](https://www.krea.ai/blog/flux-krea-open-source-release).

# Key Features

1. Cutting-edge output quality, with a focus on aesthetic photography.
2. Competitive prompt following, matching the performance of closed source alternatives.
3. Trained using guidance distillation, making `FLUX.1 Krea [dev]` more efficient.
4. Open weights to drive new scientific research, and empower artists to develop innovative workflows.
5. Generated outputs can be used for personal, scientific, and commercial purposes, as described in the [flux-1-dev-non-commercial-license](https://github.com/black-forest-labs/flux/blob/main/model_licenses/LICENSE-FLUX1-dev).

# Usage

`FLUX.1 Krea [dev]` can be used as a drop-in replacement in every system that supports the original `FLUX.1 [dev]`.
A reference implementation of `FLUX.1 [dev]` is in our dedicated [github repository](https://github.com/black-forest-labs/flux).
Developers and creatives looking to build on top of `FLUX.1 [dev]` are encouraged to use this as a starting point.

`FLUX.1 Krea [dev]` is also available in both [ComfyUI](https://github.com/comfyanonymous/ComfyUI) and [diffusers](https://github.com/huggingface/diffusers).

## ComfyUI

To use `FLUX.1 Krea [dev]` in [Comfy UI](https://github.com/comfyanonymous/ComfyUI) download the `*.safetensors` weights [here](https://huggingface.co/black-forest-labs/FLUX.1-Krea-dev/resolve/main/flux1-krea-dev.safetensors)

## 🧨 diffusers

To use `FLUX.1 Krea [dev]` in [diffusers](https://github.com/huggingface/diffusers), first install or upgrade diffusers

```
pip install -U diffusers
```

Then you can use `FluxPipeline` to run the model

```
import torch
from diffusers import FluxPipeline

pipe = FluxPipeline.from_pretrained("black-forest-labs/FLUX.1-Krea-dev", torch_dtype=torch.bfloat16)
pipe.enable_model_cpu_offload() #save some VRAM by offloading the model to CPU. Remove this if you have enough GPU VRAM

prompt = "A frog holding a sign that says hello world"
image = pipe(
    prompt,
    height=1024,
    width=1024,
    guidance_scale=4.5,
).images[0]
image.save("flux-krea-dev.png")
```

To learn more check out the [diffusers](https://huggingface.co/docs/diffusers/main/en/api/pipelines/flux) documentation

---

# Limitations

* This model is not intended or able to provide factual information.
* As a statistical model this checkpoint might amplify existing societal biases.
* The model may fail to generate output that matches the prompts.
* Prompt following is heavily influenced by the prompting-style.

---

# Out-of-Scope Use

The model and its derivatives may not be used

* In any way that violates any applicable national, federal, state, local or international law or regulation.
* For the purpose of exploiting, harming or attempting to exploit or harm minors in any way; including but not limited to the solicitation, creation, acquisition, or dissemination of child exploitative content.
* To generate or disseminate verifiably false information and/or content with the purpose of harming others.
* To generate or disseminate personal identifiable information that can be used to harm an individual.
* To harass, abuse, threaten, stalk, or bully individuals or groups of individuals.
* To create non-consensual nudity or illegal pornographic content.
* For fully automated decision making that adversely impacts an individual's legal rights or otherwise creates or modifies a binding, enforceable obligation.
* Generating or facilitating large-scale disinformation campaigns.
* Please reference our [content filters](https://github.com/black-forest-labs/flux/blob/main/src/flux/content_filters.py) to avoid such generations.

---

# Risks

Black Forest Labs (BFL) and Krea are committed to the responsible development of generative AI technology. Prior to releasing FLUX.1 Krea [dev], BFL and Krea collaboratively evaluated and mitigated a number of risks in the FLUX.1 Krea [dev] model and services, including the generation of unlawful content. We implemented a series of pre-release mitigations to help prevent misuse by third parties, with additional post-release mitigations to help address residual risks:

1. **Pre-training mitigation.** BFL filtered pre-training data for multiple categories of “not safe for work” (NSFW) and unlawful content to help prevent a user generating unlawful content in response to text prompts or uploaded images.
2. **Post-training mitigation.** BFL has partnered with the Internet Watch Foundation, an independent nonprofit organization dedicated to preventing online abuse, to filter known child sexual abuse material (CSAM) from post-training data. Subsequently, BFL and Krea undertook multiple rounds of targeted fine-tuning to provide additional mitigation against potential abuse. By inhibiting certain behaviors and concepts in the trained model, these techniques can help to prevent a user generating synthetic CSAM or nonconsensual intimate imagery (NCII) from a text prompt.
3. **Pre-release evaluation.** Throughout this process, BFL conducted internal and external third-party evaluations of model checkpoints to identify further opportunities for improvement. The third-party evaluations focused on eliciting CSAM and NCII through adversarial testing of the text-to-image model with text-only prompts. We also conducted internal evaluations of the proposed release checkpoints, comparing the model with other leading openly-available generative image models from other companies. The final FLUX.1 Krea [dev] open-weight model checkpoint demonstrated very high resilience against violative inputs, demonstrating higher resilience than other similar open-weight models across these risk categories. Based on these findings, we approved the release of the FLUX.1 Krea [dev] model as openly-available weights under a non-commercial license to support third-party research and development.
4. **Inference filters.** The BFL Github repository for the open FLUX.1 Krea [dev] model includes filters for illegal or infringing content. Filters or manual review must be used with the model under the terms of the FLUX.1 [dev] Non-Commercial License. We may approach known deployers of the FLUX.1 Krea [dev] model at random to verify that filters or manual review processes are in place.
5. **Policies.** Our FLUX.1 [dev] Non-Commercial License prohibits the generation of unlawful content or the use of generated content for unlawful, defamatory, or abusive purposes. Developers and users must consent to these conditions to access the FLUX.1 Krea [dev] model.
6. **Monitoring.** BFL is monitoring for patterns of violative use after release, and may ban developers who we detect intentionally and repeatedly violate our policies. Additionally, BFL provides a dedicated email address ([safety@blackforestlabs.ai](mailto:safety@blackforestlabs.ai)) to solicit feedback from the community. BFL maintains a reporting relationship with organizations such as the Internet Watch Foundation and the National Center for Missing and Exploited Children, and BFL welcomes ongoing engagement with authorities, developers, and researchers to share intelligence about emerging risks and develop effective mitigations.

---

# License

This model falls under the [`FLUX.1 [dev]` Non-Commercial License](https://huggingface.co/black-forest-labs/FLUX.1-dev/blob/main/LICENSE.md).

Downloads last month
:   17,698

 

Inference Providers [NEW](https://huggingface.co/docs/inference-providers)

fal

[Text-to-Image](/tasks/text-to-image "Learn more about text-to-image")

 

Generate

  

View Code Snippets

Maximize

## Model tree for black-forest-labs/FLUX.1-Krea-dev

Base model

[black-forest-labs/FLUX.1-dev](/black-forest-labs/FLUX.1-dev)

Finetuned

 ([580](/models?other=base_model:finetune:black-forest-labs/FLUX.1-dev)) 

this model

 

Adapters

 [26 models](/models?other=base_model:adapter:black-forest-labs/FLUX.1-Krea-dev)

Finetunes

 [17 models](/models?other=base_model:finetune:black-forest-labs/FLUX.1-Krea-dev)

Merges

 [2 models](/models?other=base_model:merge:black-forest-labs/FLUX.1-Krea-dev)

Quantizations

 [10 models](/models?other=base_model:quantized:black-forest-labs/FLUX.1-Krea-dev)

  

## Spaces using black-forest-labs/FLUX.1-Krea-dev 100

[![](https://cdn-avatars.huggingface.co/v1/production/uploads/633f7a8f4be90e06da248e0f/m5YoF33abJ09vcwFxt1Mj.png)

black-forest-labs/FLUX.1-Krea-dev](/spaces/black-forest-labs/FLUX.1-Krea-dev) [🤗

yanze/PuLID-FLUX](/spaces/yanze/PuLID-FLUX) [🧩🖼️

r3gm/DiffuseCraft](/spaces/r3gm/DiffuseCraft) [⚡

bytedance-research/USO](/spaces/bytedance-research/USO) [🎥

alexnasa/Ovi-ZEROGPU](/spaces/alexnasa/Ovi-ZEROGPU) [🥖

prithivMLmods/FLUX-REALISM](/spaces/prithivMLmods/FLUX-REALISM) [🧩🖼️📦

John6666/DiffuseCraftMod](/spaces/John6666/DiffuseCraftMod) [🖼🖼️📦

John6666/votepurchase-multiple-model](/spaces/John6666/votepurchase-multiple-model)  + 95 Spaces + 92 Spaces

 

## Collection including black-forest-labs/FLUX.1-Krea-dev

[#### FLUX.1

Collection

A collection of our FLUX.1 models and LoRAs. • 13 items • Updated Jan 2 •  329](/collections/black-forest-labs/flux1)

 

System theme

Company

[TOS](/terms-of-service) [Privacy](/privacy) [About](/huggingface) [Careers](https://apply.workable.com/huggingface/) 

Website

[Models](/models) [Datasets](/datasets) [Spaces](/spaces) [Pricing](/pricing) [Docs](/docs)



Inference providers allow you to run inference using different serverless providers.

## Run 15,000+ Models Instantly

Inference Providers let you run inference on thousands of models served by our partners using a simple,
unified, OpenAI-compatible serverless API ([Learn more](/docs/inference-providers)).

black-forest-labs/FLUX.1-Krea-dev is supported by the following Inference Providers:

Replicate

fal

View API Code Dismiss
