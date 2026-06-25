# stabilityai/stable-diffusion-3.5-medium · Hugging Face
Source: https://huggingface.co/stabilityai/stable-diffusion-3.5-medium
stabilityai/stable-diffusion-3.5-medium · Hugging Face



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

      

# [stabilityai](/stabilityai) / [stable-diffusion-3.5-medium](/stabilityai/stable-diffusion-3.5-medium) like 986 Follow Stability AI 37.5k

[Text-to-Image](/models?pipeline_tag=text-to-image)[Diffusers](/models?library=diffusers)[Safetensors](/models?library=safetensors)[English](/models?language=en)[stable-diffusion](/models?other=stable-diffusion)

arxiv: 2403.03206

License: stabilityai-ai-community

[Model card](/stabilityai/stable-diffusion-3.5-medium)  [Files Files and versions  

xet](/stabilityai/stable-diffusion-3.5-medium/tree/main)  [Community

36](/stabilityai/stable-diffusion-3.5-medium/discussions)

 

Deploy

  Copy to bucket new   

Use this model  

### Instructions to use stabilityai/stable-diffusion-3.5-medium with libraries, inference providers, notebooks, and local apps. Follow these links to get started.

* Libraries
* [Diffusers](/stabilityai/stable-diffusion-3.5-medium?library=diffusers) 

  How to use stabilityai/stable-diffusion-3.5-medium with Diffusers:

  ```
  pip install -U diffusers transformers accelerate
  ```

  ```
  import torch
  from diffusers import DiffusionPipeline

  # switch to "mps" for apple devices
  pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-3.5-medium", dtype=torch.bfloat16, device_map="cuda")

  prompt = "Astronaut in a jungle, cold color palette, muted colors, detailed, 8k"
  image = pipe(prompt).images[0]
  ```
* Inference
* Inference Providers
 * Notebooks
* [Google Colab](/stabilityai/stable-diffusion-3.5-medium/colab)
* [Kaggle](/stabilityai/stable-diffusion-3.5-medium/kaggle)
 * Local Apps [Settings](/settings/local-apps "Set up your favorite local applications")
 * [Draw Things](https://drawthings.ai/import/diffusers/pipeline.from_pretrained?repo_id=stabilityai/stable-diffusion-3.5-medium)
* [DiffusionBee](https://diffusionbee.com/huggingface_import?model_id=stabilityai/stable-diffusion-3.5-medium)

## You need to agree to share your contact information to access this model

This repository is publicly accessible, but you have to accept the conditions to access its files and content.

By clicking "Agree", you agree to the [License Agreement](https://huggingface.co/stabilityai/stable-diffusion-3.5-medium/blob/main/LICENSE.md) and acknowledge Stability AI's [Privacy Policy](https://stability.ai/privacy-policy).

 

[Log in](/login?next=%2Fstabilityai%2Fstable-diffusion-3.5-medium) or [Sign Up](/join?next=%2Fstabilityai%2Fstable-diffusion-3.5-medium) to review the conditions and access this model content.

 

* [Stable Diffusion 3.5 Medium](#stable-diffusion-35-medium "Stable Diffusion 3.5 Medium")
  + [Model](#model "Model")
    - [Model Description](#model-description "Model Description")
    - [License](#license "License")
    - [Model Sources](#model-sources "Model Sources")
    - [Implementation Details](#implementation-details "Implementation Details")
    - [Usage & Limitations](#usage--limitations "Usage &amp; Limitations")
    - [Model Performance](#model-performance "Model Performance")
  + [File Structure](#file-structure "File Structure")
  + [Using with Diffusers](#using-with-diffusers "Using with Diffusers")
    - [Quantizing the model with diffusers](#quantizing-the-model-with-diffusers "Quantizing the model with diffusers")
    - [Fine-tuning](#fine-tuning "Fine-tuning")
  + [Uses](#uses "Uses")
    - [Intended Uses](#intended-uses "Intended Uses")
    - [Out-of-Scope Uses](#out-of-scope-uses "Out-of-Scope Uses")
  + [Safety](#safety "Safety")
    - [Integrity Evaluation](#integrity-evaluation "Integrity Evaluation")
    - [Risks identified and mitigations:](#risks-identified-and-mitigations "Risks identified and mitigations:")
    - [Contact](#contact "Contact")

# Stable Diffusion 3.5 Medium

[![3.5 Medium Demo Image](/stabilityai/stable-diffusion-3.5-medium/media/main/sd3.5_medium_demo.jpg)](/stabilityai/stable-diffusion-3.5-medium/blob/main/sd3.5_medium_demo.jpg)

## Model

[![MMDiT-X](/stabilityai/stable-diffusion-3.5-medium/media/main/mmdit-x.png)](/stabilityai/stable-diffusion-3.5-medium/blob/main/mmdit-x.png)

[Stable Diffusion 3.5 Medium](https://stability.ai/news/introducing-stable-diffusion-3-5) is a Multimodal Diffusion Transformer with improvements (MMDiT-X) text-to-image model that features improved performance in image quality, typography, complex prompt understanding, and resource-efficiency.

Please note: This model is released under the [Stability Community License](https://stability.ai/community-license-agreement). Visit [Stability AI](https://stability.ai/license) to learn or [contact us](https://stability.ai/enterprise) for commercial licensing details.

### Model Description

* **Developed by:** Stability AI
* **Model type:** MMDiT-X text-to-image generative model
* **Model Description:** This model generates images based on text prompts. It is a Multimodal Diffusion Transformer
  (<https://arxiv.org/abs/2403.03206>) with improvements that use three fixed, pretrained text encoders, with QK-normalization to improve training stability, and dual attention blocks in the first 12 transformer layers.

### License

* **Community License:** Free for research, non-commercial, and commercial use for organizations or individuals with less than $1M in total annual revenue. More details can be found in the [Community License Agreement](https://stability.ai/community-license-agreement). Read more at <https://stability.ai/license>.
* **For individuals and organizations with annual revenue above $1M**: please [contact us](https://stability.ai/enterprise) to get an Enterprise License.

### Model Sources

For local or self-hosted use, we recommend [ComfyUI](https://github.com/comfyanonymous/ComfyUI) for node-based UI inference, or [diffusers](https://github.com/huggingface/diffusers) or [GitHub](https://github.com/Stability-AI/sd3.5) for programmatic use.

* **ComfyUI:** [Github](https://github.com/comfyanonymous/ComfyUI), [Example Workflow](https://comfyanonymous.github.io/ComfyUI_examples/sd3/)
* **Huggingface Space:** [Space](https://huggingface.co/spaces/stabilityai/stable-diffusion-3.5-medium)
* **Diffusers**: [See below](#using-with-diffusers).
* **GitHub**: [GitHub](https://github.com/Stability-AI/sd3.5).
* **API Endpoints:**

  + [Stability AI API](https://platform.stability.ai/docs/api-reference#tag/Generate/paths/~1v2beta~1stable-image~1generate~1sd3/post)

### Implementation Details

* **MMDiT-X:** Introduces self-attention modules in the first 13 layers of the transformer, enhancing multi-resolution generation and overall image coherence.
* **QK Normalization:** Implements the QK normalization technique to improve training Stability.
* **Mixed-Resolution Training:**

  + Progressive training stages: 256 → 512 → 768 → 1024 → 1440 resolution
  + The final stage included mixed-scale image training to boost multi-resolution generation performance
  + Extended positional embedding space to 384x384 (latent) at lower resolution stages
  + Employed random crop augmentation on positional embeddings to enhance transformer layer robustness across the entire range of mixed resolutions and aspect ratios. For example, given a 64x64 latent image, we add a randomly cropped 64x64 embedding from the 192x192 embedding space during training as the input to the x stream.

These enhancements collectively contribute to the model's improved performance in multi-resolution image generation, coherence, and adaptability across various text-to-image tasks.

* **Text Encoders：**

  + CLIPs: [OpenCLIP-ViT/G](https://github.com/mlfoundations/open_clip), [CLIP-ViT/L](https://github.com/openai/CLIP/tree/main), context length 77 tokens
  + T5: [T5-xxl](https://huggingface.co/google/t5-v1_1-xxl), context length 77/256 tokens at different stages of training
* **Training Data and Strategy:**

  This model was trained on a wide variety of data, including synthetic data and filtered publicly available data.

For more technical details of the original MMDiT architecture, please refer to the [Research paper](https://stability.ai/news/stable-diffusion-3-research-paper).

### Usage & Limitations

* While this model can handle long prompts, you may observe artifacts on the edge of generations when T5 tokens go over 256. Pay attention to the token limits when using this model in your workflow, and shortern prompts if artifacts becomes too obvious.
* The medium model has a different training data distribution than the large model, so it may not respond to the same prompt similarly.
* We recommend sampling with **[Skip Layer Guidance](https://github.com/comfyanonymous/ComfyUI/pull/5404)** for better structure and anatomy coherency.

### Model Performance

See [blog](https://stability.ai/news/introducing-stable-diffusion-3-5) for our study about comparative performance in prompt adherence and aesthetic quality.

## File Structure

Click here to access the [Files and versions tab](https://huggingface.co/stabilityai/stable-diffusion-3.5-medium/tree/main)

```
├── text_encoders/  
│   ├── README.md
│   ├── clip_g.safetensors
│   ├── clip_l.safetensors
│   ├── t5xxl_fp16.safetensors
│   └── t5xxl_fp8_e4m3fn.safetensors
│
├── README.md
├── LICENSE
├── sd3.5_medium.safetensors
├── SD3.5M_example_workflow.json
├── SD3.5M_SLG_example_workflow.json
├── SD3.5L_plus_SD3.5M_upscaling_example_workflow.json
└── sd3_medium_demo.jpg

** File structure below is for diffusers integration**
├── scheduler/
├── text_encoder/
├── text_encoder_2/
├── text_encoder_3/
├── tokenizer/
├── tokenizer_2/
├── tokenizer_3/
├── transformer/
├── vae/
└── model_index.json
```

## Using with Diffusers

Upgrade to the latest version of the [🧨 diffusers library](https://github.com/huggingface/diffusers)

```
pip install -U diffusers
```

and then you can run

```
import torch
from diffusers import StableDiffusion3Pipeline

pipe = StableDiffusion3Pipeline.from_pretrained("stabilityai/stable-diffusion-3.5-medium", torch_dtype=torch.bfloat16)
pipe = pipe.to("cuda")

image = pipe(
    "A capybara holding a sign that reads Hello World",
    num_inference_steps=40,
    guidance_scale=4.5,
).images[0]
image.save("capybara.png")
```

### Quantizing the model with diffusers

Reduce your VRAM usage and have the model fit on 🤏 VRAM GPUs

```
pip install bitsandbytes
```

```
from diffusers import BitsAndBytesConfig, SD3Transformer2DModel
from diffusers import StableDiffusion3Pipeline
import torch

model_id = "stabilityai/stable-diffusion-3.5-medium"

nf4_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)
model_nf4 = SD3Transformer2DModel.from_pretrained(
    model_id,
    subfolder="transformer",
    quantization_config=nf4_config,
    torch_dtype=torch.bfloat16
)

pipeline = StableDiffusion3Pipeline.from_pretrained(
    model_id, 
    transformer=model_nf4,
    torch_dtype=torch.bfloat16
)
pipeline.enable_model_cpu_offload()

prompt = "A whimsical and creative image depicting a hybrid creature that is a mix of a waffle and a hippopotamus, basking in a river of melted butter amidst a breakfast-themed landscape. It features the distinctive, bulky body shape of a hippo. However, instead of the usual grey skin, the creature's body resembles a golden-brown, crispy waffle fresh off the griddle. The skin is textured with the familiar grid pattern of a waffle, each square filled with a glistening sheen of syrup. The environment combines the natural habitat of a hippo with elements of a breakfast table setting, a river of warm, melted butter, with oversized utensils or plates peeking out from the lush, pancake-like foliage in the background, a towering pepper mill standing in for a tree.  As the sun rises in this fantastical world, it casts a warm, buttery glow over the scene. The creature, content in its butter river, lets out a yawn. Nearby, a flock of birds take flight"

image = pipeline(
    prompt=prompt,
    num_inference_steps=40,
    guidance_scale=4.5,
    max_sequence_length=512,
).images[0]
image.save("whimsical.png")
```

### Fine-tuning

Please see the fine-tuning guide [here](https://stabilityai.notion.site/Stable-Diffusion-3-5-Large-Fine-tuning-Tutorial-11a61cdcd1968027a15bdbd7c40be8c6).

## Uses

### Intended Uses

Intended uses include the following:

* Generation of artworks and use in design and other artistic processes.
* Applications in educational or creative tools.
* Research on generative models, including understanding the limitations of generative models.

All uses of the model must be in accordance with our [Acceptable Use Policy](https://stability.ai/use-policy).

### Out-of-Scope Uses

The model was not trained to be factual or true representations of people or events. As such, using the model to generate such content is out-of-scope of the abilities of this model.

## Safety

As part of our safety-by-design and responsible AI deployment approach, we take deliberate measures to ensure Integrity starts at the early stages of development. We implement safety measures throughout the development of our models. We have implemented safety mitigations that are intended to reduce the risk of certain harms, however we recommend that developers conduct their own testing and apply additional mitigations based on their specific use cases.  
For more about our approach to Safety, please visit our [Safety page](https://stability.ai/safety).

### Integrity Evaluation

Our integrity evaluation methods include structured evaluations and red-teaming testing for certain harms. Testing was conducted primarily in English and may not cover all possible harms.

### Risks identified and mitigations:

* Harmful content: We have used filtered data sets when training our models and implemented safeguards that attempt to strike the right balance between usefulness and preventing harm. However, this does not guarantee that all possible harmful content has been removed. TAll developers and deployers should exercise caution and implement content safety guardrails based on their specific product policies and application use cases.
* Misuse: Technical limitations and developer and end-user education can help mitigate against malicious applications of models. All users are required to adhere to our [Acceptable Use Policy](https://stability.ai/use-policy), including when applying fine-tuning and prompt engineering mechanisms. Please reference the Stability AI Acceptable Use Policy for information on violative uses of our products.
* Privacy violations: Developers and deployers are encouraged to adhere to privacy regulations with techniques that respect data privacy.

### Contact

Please report any issues with the model or contact us:

* Safety issues: [safety@stability.ai](mailto:safety@stability.ai)
* Security issues: [security@stability.ai](mailto:security@stability.ai)
* Privacy issues: [privacy@stability.ai](mailto:privacy@stability.ai)
* License and general: <https://stability.ai/license>
* Enterprise license: <https://stability.ai/enterprise>

Downloads last month
:   493,360

 

Inference Providers [NEW](https://huggingface.co/docs/inference-providers)

fal

[Text-to-Image](/tasks/text-to-image "Learn more about text-to-image")

 

Generate

  

View Code Snippets

Maximize

## Model tree for stabilityai/stable-diffusion-3.5-medium

Adapters

 [105 models](/models?other=base_model:adapter:stabilityai/stable-diffusion-3.5-medium)

Finetunes

 [73 models](/models?other=base_model:finetune:stabilityai/stable-diffusion-3.5-medium)

Quantizations

 [6 models](/models?other=base_model:quantized:stabilityai/stable-diffusion-3.5-medium)

  

## Spaces using stabilityai/stable-diffusion-3.5-medium 100

[![](https://cdn-avatars.huggingface.co/v1/production/uploads/643feeb67bc3fbde1385cc25/7vmYr2XwVcPtkLzac_jxQ.png)

stabilityai/stable-diffusion-3.5-medium](/spaces/stabilityai/stable-diffusion-3.5-medium) [🖼️

HorizonRobotics/EmbodiedGen-Image-to-3D](/spaces/HorizonRobotics/EmbodiedGen-Image-to-3D) [🎬

mirun23/ai-yt-factory-backend](/spaces/mirun23/ai-yt-factory-backend) [🤗

multimodalart/civitai-to-hf](/spaces/multimodalart/civitai-to-hf) [📝

HorizonRobotics/EmbodiedGen-Text-to-3D](/spaces/HorizonRobotics/EmbodiedGen-Text-to-3D) [🎨

HorizonRobotics/EmbodiedGen-Texture-Gen](/spaces/HorizonRobotics/EmbodiedGen-Texture-Gen) [🖼️

spykee47/stabilityai-stable-diffusion-3.5-medium](/spaces/spykee47/stabilityai-stable-diffusion-3.5-medium) [🌍

Ratkus/stabilityai-stable-diffusion-3.5-medium](/spaces/Ratkus/stabilityai-stable-diffusion-3.5-medium)  + 95 Spaces + 92 Spaces

 

## Collection including stabilityai/stable-diffusion-3.5-medium

[#### Stable Diffusion 3.5

Collection

6 items • Updated Jan 9, 2025 •  186](/collections/stabilityai/stable-diffusion-35)

 

## Paper for stabilityai/stable-diffusion-3.5-medium

[#### Scaling Rectified Flow Transformers for High-Resolution Image Synthesis

Paper • 2403.03206 • Published Mar 5, 2024 •  71](/papers/2403.03206)

 

System theme

Company

[TOS](/terms-of-service) [Privacy](/privacy) [About](/huggingface) [Careers](https://apply.workable.com/huggingface/) 

Website

[Models](/models) [Datasets](/datasets) [Spaces](/spaces) [Pricing](/pricing) [Docs](/docs)



Inference providers allow you to run inference using different serverless providers.

## Run 15,000+ Models Instantly

Inference Providers let you run inference on thousands of models served by our partners using a simple,
unified, OpenAI-compatible serverless API ([Learn more](/docs/inference-providers)).

stabilityai/stable-diffusion-3.5-medium is supported by the following Inference Providers:

Replicate

fal

View API Code Dismiss
