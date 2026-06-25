# DeepFloyd/IF-I-L-v1.0 · Hugging Face
Source: https://huggingface.co/DeepFloyd/IF-I-L-v1.0
DeepFloyd/IF-I-L-v1.0 · Hugging Face



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

      

# [DeepFloyd](/DeepFloyd) / [IF-I-L-v1.0](/DeepFloyd/IF-I-L-v1.0) like 20 Follow DeepFloyd 398

[Text-to-Image](/models?pipeline_tag=text-to-image)[Diffusers](/models?library=diffusers)[PyTorch](/models?library=pytorch)[Safetensors](/models?library=safetensors)[if](/models?other=if)

arxiv: 2205.11487

arxiv: 2110.02861

License: deepfloyd-if-license

[Model card](/DeepFloyd/IF-I-L-v1.0)  [Files Files and versions  

xet](/DeepFloyd/IF-I-L-v1.0/tree/main)  [Community

11](/DeepFloyd/IF-I-L-v1.0/discussions)

 

Copy to bucket new   

Use this model  

### Instructions to use DeepFloyd/IF-I-L-v1.0 with libraries, inference providers, notebooks, and local apps. Follow these links to get started.

* Libraries
* [Diffusers](/DeepFloyd/IF-I-L-v1.0?library=diffusers) 

  How to use DeepFloyd/IF-I-L-v1.0 with Diffusers:

  ```
  pip install -U diffusers transformers accelerate
  ```

  ```
  import torch
  from diffusers import DiffusionPipeline

  # switch to "mps" for apple devices
  pipe = DiffusionPipeline.from_pretrained("DeepFloyd/IF-I-L-v1.0", dtype=torch.bfloat16, device_map="cuda")

  prompt = "Astronaut in a jungle, cold color palette, muted colors, detailed, 8k"
  image = pipe(prompt).images[0]
  ```
 * Notebooks
* [Google Colab](/DeepFloyd/IF-I-L-v1.0/colab)
* [Kaggle](/DeepFloyd/IF-I-L-v1.0/kaggle)
 * Local Apps [Settings](/settings/local-apps "Set up your favorite local applications")
 * [Draw Things](https://drawthings.ai/import/diffusers/pipeline.from_pretrained?repo_id=DeepFloyd/IF-I-L-v1.0)
* [DiffusionBee](https://diffusionbee.com/huggingface_import?model_id=DeepFloyd/IF-I-L-v1.0)

## You need to agree to share your contact information to access this model

This repository is publicly accessible, but you have to accept the conditions to access its files and content.

DeepFloyd LICENSE AGREEMENT  
This License Agreement (as may be amended in accordance with this License Agreement, “License”), between you, or your employer or other entity (if you are entering into this agreement on behalf of your employer or other entity) (“Licensee” or “you”) and Stability AI Ltd.. (“Stability AI” or “we”) applies to your use of any computer program, algorithm, source code, object code, or software that is made available by Stability AI under this License (“Software”) and any specifications, manuals, documentation, and other written information provided by Stability AI related to the Software (“Documentation”).  
By clicking “I Accept” below or by using the Software, you agree to the terms of this License. If you do not agree to this License, then you do not have any rights to use the Software or Documentation (collectively, the “Software Products”), and you must immediately cease using the Software Products. If you are agreeing to be bound by the terms of this License on behalf of your employer or other entity, you represent and warrant to Stability AI that you have full legal authority to bind your employer or such entity to this License. If you do not have the requisite authority, you may not accept the License or access the Software Products on behalf of your employer or other entity.

1. LICENSE GRANT  
    a. Subject to your compliance with the Documentation and Sections 2, 3, and 5, Stability AI grants you a non-exclusive, worldwide, non-transferable, non-sublicensable, revocable, royalty free and limited license under Stability AI’s copyright interests to reproduce, distribute, and create derivative works of the Software solely for your non-commercial research purposes. The foregoing license is personal to you, and you may not assign or sublicense this License or any other rights or obligations under this License without Stability AI’s prior written consent; any such assignment or sublicense will be void and will automatically and immediately terminate this License.  
    b. You may make a reasonable number of copies of the Documentation solely for use in connection with the license to the Software granted above.  
    c. The grant of rights expressly set forth in this Section 1 (License Grant) are the complete grant of rights to you in the Software Products, and no other licenses are granted, whether by waiver, estoppel, implication, equity or otherwise. Stability AI and its licensors reserve all rights not expressly granted by this License.
2. RESTRICTIONS  
    You will not, and will not permit, assist or cause any third party to:  
    a. use, modify, copy, reproduce, create derivative works of, or distribute the Software Products (or any derivative works thereof, works incorporating the Software Products, or any data produced by the Software), in whole or in part, for (i) any commercial or production purposes, (ii) military purposes or in the service of nuclear technology, (iii) purposes of surveillance, including any research or development relating to surveillance, (iv) biometric processing, (v) in any manner that infringes, misappropriates, or otherwise violates any third-party rights, or (vi) in any manner that violates any applicable law and violating any privacy or security laws, rules, regulations, directives, or governmental requirements (including the General Data Privacy Regulation (Regulation (EU) 2016/679), the California Consumer Privacy Act, and any and all laws governing the processing of biometric information), as well as all amendments and successor laws to any of the foregoing;  
    b. alter or remove copyright and other proprietary notices which appear on or in the Software Products;  
    c. utilize any equipment, device, software, or other means to circumvent or remove any security or protection used by Stability AI in connection with the Software, or to circumvent or remove any usage restrictions, or to enable functionality disabled by Stability AI; or  
    d. offer or impose any terms on the Software Products that alter, restrict, or are inconsistent with the terms of this License.  
    e. 1) violate any applicable U.S. and non-U.S. export control and trade sanctions laws (“Export Laws”); 2) directly or indirectly export, re-export, provide, or otherwise transfer Software Products: (a) to any individual, entity, or country prohibited by Export Laws; (b) to anyone on U.S. or non-U.S. government restricted parties lists; or (c) for any purpose prohibited by Export Laws, including nuclear, chemical or biological weapons, or missile technology applications; 3) use or download Software Products if you or they are: (a) located in a comprehensively sanctioned jurisdiction, (b) currently listed on any U.S. or non-U.S. restricted parties list, or (c) for any purpose prohibited by Export Laws; and (4) will not disguise your location through IP proxying or other methods.
3. ATTRIBUTION  
    Together with any copies of the Software Products (as well as derivative works thereof or works incorporating the Software Products) that you distribute, you must provide (i) a copy of this License, and (ii) the following attribution notice: “DeepFloyd is licensed under the DeepFloyd License, Copyright (c) Stability AI Ltd. All Rights Reserved.”
4. DISCLAIMERS  
    THE SOFTWARE PRODUCTS ARE PROVIDED “AS IS” and “WITH ALL FAULTS” WITH NO WARRANTY OF ANY KIND, EXPRESS OR IMPLIED. STABILITY AIEXPRESSLY DISCLAIMS ALL REPRESENTATIONS AND WARRANTIES, EXPRESS OR IMPLIED, WHETHER BY STATUTE, CUSTOM, USAGE OR OTHERWISE AS TO ANY MATTERS RELATED TO THE SOFTWARE PRODUCTS, INCLUDING BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, TITLE, SATISFACTORY QUALITY, OR NON-INFRINGEMENT. STABILITY AI MAKES NO WARRANTIES OR REPRESENTATIONS THAT THE SOFTWARE PRODUCTS WILL BE ERROR FREE OR FREE OF VIRUSES OR OTHER HARMFUL COMPONENTS, OR PRODUCE ANY PARTICULAR RESULTS.
5. LIMITATION OF LIABILITY  
    TO THE FULLEST EXTENT PERMITTED BY LAW, IN NO EVENT WILL STABILITY AI BE LIABLE TO YOU (A) UNDER ANY THEORY OF LIABILITY, WHETHER BASED IN CONTRACT, TORT, NEGLIGENCE, STRICT LIABILITY, WARRANTY, OR OTHERWISE UNDER THIS LICENSE, OR (B) FOR ANY INDIRECT, CONSEQUENTIAL, EXEMPLARY, INCIDENTAL, PUNITIVE OR SPECIAL DAMAGES OR LOST PROFITS, EVEN IF STABILITY AI HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES. THE SOFTWARE PRODUCTS, THEIR CONSTITUENT COMPONENTS, AND ANY OUTPUT (COLLECTIVELY, “SOFTWARE MATERIALS”) ARE NOT DESIGNED OR INTENDED FOR USE IN ANY APPLICATION OR SITUATION WHERE FAILURE OR FAULT OF THE SOFTWARE MATERIALS COULD REASONABLY BE ANTICIPATED TO LEAD TO SERIOUS INJURY OF ANY PERSON, INCLUDING POTENTIAL DISCRIMINATION OR VIOLATION OF AN INDIVIDUAL’S PRIVACY RIGHTS, OR TO SEVERE PHYSICAL, PROPERTY, OR ENVIRONMENTAL DAMAGE (EACH, A “HIGH-RISK USE”). IF YOU ELECT TO USE ANY OF THE SOFTWARE MATERIALS FOR A HIGH-RISK USE, YOU DO SO AT YOUR OWN RISK. YOU AGREE TO DESIGN AND IMPLEMENT APPROPRIATE DECISION-MAKING AND RISK-MITIGATION PROCEDURES AND POLICIES IN CONNECTION WITH A HIGH-RISK USE SUCH THAT EVEN IF THERE IS A FAILURE OR FAULT IN ANY OF THE SOFTWARE MATERIALS, THE SAFETY OF PERSONS OR PROPERTY AFFECTED BY THE ACTIVITY STAYS AT A LEVEL THAT IS REASONABLE, APPROPRIATE, AND LAWFUL FOR THE FIELD OF THE HIGH-RISK USE.
6. INDEMNIFICATION  
    You will indemnify, defend and hold harmless Stability AI and our subsidiaries and affiliates, and each of our respective shareholders, directors, officers, employees, agents, successors, and assigns (collectively, the “Stability AI Parties”) from and against any losses, liabilities, damages, fines, penalties, and expenses (including reasonable attorneys’ fees) incurred by any Stability AI Party in connection with any claim, demand, allegation, lawsuit, proceeding, or investigation (collectively, “Claims”) arising out of or related to: (a) your access to or use of the Software Products (as well as any results or data generated from such access or use), including any High-Risk Use (defined below); (b) your violation of this License; or (c) your violation, misappropriation or infringement of any rights of another (including intellectual property or other proprietary rights and privacy rights). You will promptly notify the Stability AI Parties of any such Claims, and cooperate with Stability AI Parties in defending such Claims. You will also grant the Stability AI Parties sole control of the defense or settlement, at Stability AI’s sole option, of any Claims. This indemnity is in addition to, and not in lieu of, any other indemnities or remedies set forth in a written agreement between you and Stability AI or the other Stability AI Parties.
7. TERMINATION; SURVIVAL  
    a. This License will automatically terminate upon any breach by you of the terms of this License.  b. We may terminate this License, in whole or in part, at any time upon notice (including electronic) to you.  c. The following sections survive termination of this License: 2 (Restrictions), 3 (Attribution), 4 (Disclaimers), 5 (Limitation on Liability), 6 (Indemnification) 7 (Termination; Survival), 8 (Third Party Materials), 9 (Trademarks), 10 (Applicable Law; Dispute Resolution), and 11 (Miscellaneous).
8. THIRD PARTY MATERIALS  
    The Software Products may contain third-party software or other components (including free and open source software) (all of the foregoing, “Third Party Materials”), which are subject to the license terms of the respective third-party licensors. Your dealings or correspondence with third parties and your use of or interaction with any Third Party Materials are solely between you and the third party. Stability AI does not control or endorse, and makes no representations or warranties regarding, any Third Party Materials, and your access to and use of such Third Party Materials are at your own risk.
9. TRADEMARKS  
    Licensee has not been granted any trademark license as part of this License and may not use any name or mark associated with Stability AI without the prior written permission of Stability AI, except to the extent necessary to make the reference required by the “ATTRIBUTION” section of this Agreement.
10. APPLICABLE LAW; DISPUTE RESOLUTION  
     This License will be governed and construed under the laws of the State of California without regard to conflicts of law provisions. Any suit or proceeding arising out of or relating to this License will be brought in the federal or state courts, as applicable, in San Mateo County, California, and each party irrevocably submits to the jurisdiction and venue of such courts.
11. MISCELLANEOUS  
     If any provision or part of a provision of this License is unlawful, void or unenforceable, that provision or part of the provision is deemed severed from this License, and will not affect the validity and enforceability of any remaining provisions. The failure of Stability AI to exercise or enforce any right or provision of this License will not operate as a waiver of such right or provision. This License does not confer any third-party beneficiary rights upon any other person or entity. This License, together with the Documentation, contains the entire understanding between you and Stability AI regarding the subject matter of this License, and supersedes all other written or oral agreements and understandings between you and Stability AI regarding such subject matter. No change or addition to any provision of this License will be binding unless it is in writing and signed by an authorized representative of both you and Stability AI.

 

[Log in](/login?next=%2FDeepFloyd%2FIF-I-L-v1.0) or [Sign Up](/join?next=%2FDeepFloyd%2FIF-I-L-v1.0) to review the conditions and access this model content.

 

* [IF-I-L-v1.0](#if-i-l-v10 "IF-I-L-v1.0")
  + [Model Details](#model-details "Model Details")
  + [Using with `diffusers`](#using-with-diffusers "Using with <code>diffusers</code>")
  + [Training](#training "Training")
  + [Evaluation Results](#evaluation-results "Evaluation Results")
* [Uses](#uses "Uses")
  + [Direct Use](#direct-use "Direct Use")
    - [Misuse, Malicious Use, and Out-of-Scope Use](#misuse-malicious-use-and-out-of-scope-use "Misuse, Malicious Use, and Out-of-Scope Use")
  + [Limitations and Bias](#limitations-and-bias "Limitations and Bias")
    - [Limitations](#limitations "Limitations")
    - [Bias](#bias "Bias")

# IF-I-L-v1.0

DeepFloyd-IF is a pixel-based text-to-image triple-cascaded diffusion model, that can generate pictures with new state-of-the-art for photorealism and language understanding. The result is a highly efficient model that outperforms current state-of-the-art models, achieving a zero-shot FID-30K score of `6.66` on the COCO dataset.

*Inspired by* [*Photorealistic Text-to-Image Diffusion Models with Deep Language Understanding*](https://arxiv.org/pdf/2205.11487.pdf)

[![](/DeepFloyd/IF-I-L-v1.0/media/main/pics/if_architecture.jpg)](/DeepFloyd/IF-I-L-v1.0/blob/main/pics/if_architecture.jpg)

## Model Details

* **Developed by:** DeepFloyd, StabilityAI
* **Model type:** pixel-based text-to-image cascaded diffusion model
* **Cascade Stage:** I
* **Num Parameters:** 900M
* **Language(s):** primarily English and, to a lesser extent, other Romance languages
* **License:** [DeepFloyd IF License Agreement](https://huggingface.co/spaces/DeepFloyd/deepfloyd-if-license)
* **Model Description:** DeepFloyd-IF is modular composed of frozen text mode and three pixel cascaded diffusion modules, each designed to generate images of increasing resolution: 64x64, 256x256, and 1024x1024. All stages of the model utilize a frozen text encoder based on the T5 transformer to extract text embeddings, which are then fed into a UNet architecture enhanced with cross-attention and attention-pooling
* **Resources for more information:** [GitHub](https://github.com/deep-floyd/IF), [Website](https://deepfloyd.ai), [All Links](https://linktr.ee/deepfloyd)

## Using with `diffusers`

IF is integrated with the 🤗 Hugging Face [🧨 diffusers library](https://github.com/huggingface/diffusers/), which is optimized to run on GPUs with as little as 14 GB of VRAM.

Before you can use IF, you need to accept its usage conditions. To do so:

1. Make sure to have a [Hugging Face account](https://huggingface.co/join) and be loggin in
2. Accept the license on the model card of [DeepFloyd/IF-I-L-v1.0](https://huggingface.co/DeepFloyd/IF-I-L-v1.0)
3. Make sure to login locally. Install `huggingface_hub`

```
pip install huggingface_hub --upgrade
```

run the login function in a Python shell

```
from huggingface_hub import login

login()
```

and enter your [Hugging Face Hub access token](https://huggingface.co/docs/hub/security-tokens#what-are-user-access-tokens).

Next we install `diffusers` and dependencies:

```
pip install diffusers accelerate transformers safetensors sentencepiece
```

And we can now run the model locally.

By default `diffusers` makes use of [model cpu offloading](https://huggingface.co/docs/diffusers/optimization/fp16#model-offloading-for-fast-inference-and-memory-savings) to run the whole IF pipeline with as little as 14 GB of VRAM.

If you are using `torch>=2.0.0`, make sure to **remove all** `enable_xformers_memory_efficient_attention()` functions.

* **Load all stages and offload to CPU**

```
from diffusers import DiffusionPipeline
from diffusers.utils import pt_to_pil
import torch

# stage 1
stage_1 = DiffusionPipeline.from_pretrained("DeepFloyd/IF-I-L-v1.0", variant="fp16", torch_dtype=torch.float16)
stage_1.enable_xformers_memory_efficient_attention()  # remove line if torch.__version__ >= 2.0.0
stage_1.enable_model_cpu_offload()

# stage 2
stage_2 = DiffusionPipeline.from_pretrained(
    "DeepFloyd/IF-II-L-v1.0", text_encoder=None, variant="fp16", torch_dtype=torch.float16
)
stage_2.enable_xformers_memory_efficient_attention()  # remove line if torch.__version__ >= 2.0.0
stage_2.enable_model_cpu_offload()

# stage 3
safety_modules = {"feature_extractor": stage_1.feature_extractor, "safety_checker": stage_1.safety_checker, "watermarker": stage_1.watermarker}
stage_3 = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-x4-upscaler", **safety_modules, torch_dtype=torch.float16)
stage_3.enable_xformers_memory_efficient_attention()  # remove line if torch.__version__ >= 2.0.0
stage_3.enable_model_cpu_offload()
```

* **Retrieve Text Embeddings**

```
prompt = 'a photo of a kangaroo wearing an orange hoodie and blue sunglasses standing in front of the eiffel tower holding a sign that says "very deep learning"'

# text embeds
prompt_embeds, negative_embeds = stage_1.encode_prompt(prompt)
```

* **Run stage 1**

```
generator = torch.manual_seed(0)

image = stage_1(prompt_embeds=prompt_embeds, negative_prompt_embeds=negative_embeds, generator=generator, output_type="pt").images
pt_to_pil(image)[0].save("./if_stage_I.png")
```

* **Run stage 2**

```
image = stage_2(
    image=image, prompt_embeds=prompt_embeds, negative_prompt_embeds=negative_embeds, generator=generator, output_type="pt"
).images
pt_to_pil(image)[0].save("./if_stage_II.png")
```

* **Run stage 3**

```
image = stage_3(prompt=prompt, image=image, generator=generator, noise_level=100).images
image[0].save("./if_stage_III.png")
```

There are multiple ways to speed up the inference time and lower the memory consumption even more with `diffusers`. To do so, please have a look at the Diffusers docs:

* 🚀 [Optimizing for inference time](https://huggingface.co/docs/diffusers/api/pipelines/if#optimizing-for-speed)
* ⚙️ [Optimizing for low memory during inference](https://huggingface.co/docs/diffusers/api/pipelines/if#optimizing-for-memory)

For more in-detail information about how to use IF, please have a look at [the IF blog post](https://huggingface.co/blog/if) and the [documentation](https://huggingface.co/docs/diffusers/main/en/api/pipelines/if) 📖.

Diffusers dreambooth scripts also supports fine-tuning 🎨 [IF](https://huggingface.co/docs/diffusers/main/en/training/dreambooth#if).
With parameter efficient finetuning, you can add new concepts to IF with a single GPU and ~28 GB VRAM.

## Training

**Training Data:**

1.2B text-image pairs (based on LAION-A and few additional internal datasets)

Test/Valid parts of datasets are not used at any cascade and stage of training. Valid part of COCO helps to demonstrate "online" loss behaviour during training (to catch incident and other problems), but dataset is never used for train.

**Training Procedure:** IF-I-L-v1.0 is pixel-based diffusion cascade which uses T5-Encoder embeddings (hidden states) to generate 64px image. During training,

* Images are cropped to square via shifted-center-crop augmentation (randomly shift from center up to 0.1 of size) and resized to 64px using `Pillow==9.2.0` BICUBIC resampling with reducing\_gap=None (it helps to avoid aliasing) and processed to tensor BxCxHxW
* Text prompts are encoded through open-sourced frozen T5-v1\_1-xxl text-encoder (that completely was trained by Google team), random 10% of texts are dropped to empty string to add ability for classifier free guidance (CFG)
* The non-pooled output of the text encoder is fed into the projection (linear layer without activation) and is used in UNet backbone of the diffusion model via controlled hybrid self- and cross- attention
* Also, the output of the text encode is pooled via attention-pooling (64 heads) and is used in time embed as additional features
* Diffusion process is limited by 1000 discrete steps, with cosine beta schedule of noising image
* The loss is a reconstruction objective between the noise that was added to the image and the prediction made by the UNet
* The training process for checkpoint IF-I-L-v1.0 has 2\_500\_000 steps + 500\_000 extra steps at resolution 64x64 on all datasets, OneCycleLR policy, few-bit backward GELU activations, optimizer AdamW8bit + DeepSpeed-Zero1, fully frozen T5-Encoder

[![](/DeepFloyd/IF-I-L-v1.0/media/main/pics/loss.jpg)](/DeepFloyd/IF-I-L-v1.0/blob/main/pics/loss.jpg)

**Hardware:** 20 x 8 x A100 GPUs

**Optimizer:** [AdamW8bit](https://arxiv.org/abs/2110.02861) + [DeepSpeed ZeRO-1](https://www.deepspeed.ai/tutorials/zero/)

**Batch:** 3200

**Learning rate**: [one-cycle](https://pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.OneCycleLR.html) cosine strategy, warmup 10000 steps, start\_lr=4e-6, max\_lr=1e-4, final\_lr=1e-8;

*for extra 500\_000 steps:* [one-cycle](https://pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.OneCycleLR.html) cosine strategy, warmup 50\_000 steps, start\_lr=1e-8, max\_lr=4e-6, final\_lr=4e-8

[![](/DeepFloyd/IF-I-L-v1.0/media/main/pics/lr.jpg)](/DeepFloyd/IF-I-L-v1.0/blob/main/pics/lr.jpg)

## Evaluation Results

`FID-30K: 8.06`

[![](/DeepFloyd/IF-I-L-v1.0/media/main/pics/fid30k_if.jpg)](/DeepFloyd/IF-I-L-v1.0/blob/main/pics/fid30k_if.jpg)

# Uses

## Direct Use

The model is released for research purposes. Any attempt to deploy the model in production requires not only that the LICENSE is followed but full liability over the person deploying the model.

Possible research areas and tasks include:

* Generation of artistic imagery and use in design and other artistic processes.
* Safe deployment of models which have the potential to generate harmful content.
* Probing and understanding the limitations and biases of generative models.
* Applications in educational or creative tools.
* Research on generative models.

Excluded uses are described below.

### Misuse, Malicious Use, and Out-of-Scope Use

*Note: This section is originally taken from the [DALLE-MINI model card](https://huggingface.co/dalle-mini/dalle-mini), was used for Stable Diffusion but applies in the same way for IF*.

The model should not be used to intentionally create or disseminate images that create hostile or alienating environments for people. This includes generating images that people would foreseeably find disturbing, distressing, or offensive; or content that propagates historical or current stereotypes.

#### Out-of-Scope Use

The model was not trained to be factual or true representations of people or events, and therefore using the model to generate such content is out-of-scope for the abilities of this model.

#### Misuse and Malicious Use

Using the model to generate content that is cruel to individuals is a misuse of this model. This includes, but is not limited to:

* Generating demeaning, dehumanizing, or otherwise harmful representations of people or their environments, cultures, religions, etc.
* Intentionally promoting or propagating discriminatory content or harmful stereotypes.
* Impersonating individuals without their consent.
* Sexual content without consent of the people who might see it.
* Mis- and disinformation
* Representations of egregious violence and gore
* Sharing of copyrighted or licensed material in violation of its terms of use.
* Sharing content that is an alteration of copyrighted or licensed material in violation of its terms of use.

## Limitations and Bias

### Limitations

* The model does not achieve perfect photorealism
* The model was trained mainly with English captions and will not work as well in other languages.
* The model was trained on a subset of the large-scale dataset
  [LAION-5B](https://laion.ai/blog/laion-5b/), which contains adult, violent and sexual content. To partially mitigate this, we have... (see Training section).

### Bias

While the capabilities of image generation models are impressive, they can also reinforce or exacerbate social biases.
IF was primarily trained on subsets of [LAION-2B(en)](https://laion.ai/blog/laion-5b/),
which consists of images that are limited to English descriptions.
Texts and images from communities and cultures that use other languages are likely to be insufficiently accounted for.
This affects the overall output of the model, as white and western cultures are often set as the default. Further, the
ability of the model to generate content with non-English prompts is significantly worse than with English-language prompts.
IF mirrors and exacerbates biases to such a degree that viewer discretion must be advised irrespective of the input or its intent.

*This model card was written by: DeepFloyd Team and is based on the [StableDiffusion model card](https://huggingface.co/CompVis/stable-diffusion-v1-4).*

Downloads last month
:   282

 

Inference Providers [NEW](https://huggingface.co/docs/inference-providers)

[Text-to-Image](/tasks/text-to-image "Learn more about text-to-image")

  

This model isn't deployed by any Inference Provider. [🙋  Ask for provider support](/spaces/huggingface/InferenceSupport/discussions/new?title=DeepFloyd/IF-I-L-v1.0&description=React%20to%20this%20comment%20with%20an%20emoji%20to%20vote%20for%20%5BDeepFloyd%2FIF-I-L-v1.0%5D(%2FDeepFloyd%2FIF-I-L-v1.0)%20to%20be%20supported%20by%20Inference%20Providers.%0A%0A(optional)%20Which%20providers%20are%20you%20interested%20in%3F%20(Novita%2C%20Hyperbolic%2C%20Together%E2%80%A6)%0A)

  

## Spaces using DeepFloyd/IF-I-L-v1.0 4

[🐢

jamesoncrate/CS180-T5-Encoder](/spaces/jamesoncrate/CS180-T5-Encoder) [🐋

Nymbo/image\_gen\_supaqueue](/spaces/Nymbo/image_gen_supaqueue) [🐋

K00B404/image\_gen\_supaqueue\_game\_assets](/spaces/K00B404/image_gen_supaqueue_game_assets) [🐢

konpat/CS180-T5-Encoder](/spaces/konpat/CS180-T5-Encoder)

 

## Collection including DeepFloyd/IF-I-L-v1.0

[#### DeepFloyd's IF models

Collection

5 items • Updated Dec 13, 2024 •  4](/collections/DeepFloyd/deepfloyds-if-models)

 

## Papers for DeepFloyd/IF-I-L-v1.0

[#### Photorealistic Text-to-Image Diffusion Models with Deep Language Understanding

Paper • 2205.11487 • Published May 23, 2022 •  1](/papers/2205.11487)

[#### 8-bit Optimizers via Block-wise Quantization

Paper • 2110.02861 • Published Oct 6, 2021 •  2](/papers/2110.02861)

 

System theme

Company

[TOS](/terms-of-service) [Privacy](/privacy) [About](/huggingface) [Careers](https://apply.workable.com/huggingface/) 

Website

[Models](/models) [Datasets](/datasets) [Spaces](/spaces) [Pricing](/pricing) [Docs](/docs)



Inference providers allow you to run inference using different serverless providers.
