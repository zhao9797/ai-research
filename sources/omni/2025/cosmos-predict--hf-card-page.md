Update available: cloakbrowser 0.3.31 → 0.4.3. Run: pip install --upgrade cloakbrowser
# nvidia/Cosmos-1.0-Diffusion-7B-Text2World · Hugging Face
Source: https://huggingface.co/nvidia/Cosmos-1.0-Diffusion-7B-Text2World
nvidia/Cosmos-1.0-Diffusion-7B-Text2World · Hugging Face



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

      

# [nvidia](/nvidia) / [Cosmos-1.0-Diffusion-7B-Text2World](/nvidia/Cosmos-1.0-Diffusion-7B-Text2World) like 234 Follow NVIDIA 61.1k

[Text-to-Video](/models?pipeline_tag=text-to-video)[Cosmos](/models?library=cosmos)[Diffusers](/models?library=diffusers)[Safetensors](/models?library=safetensors)[NeMo](/models?library=nemo)[nvidia](/models?other=nvidia)

arxiv: 2501.03575

License: nvidia-open-model-license

[Model card](/nvidia/Cosmos-1.0-Diffusion-7B-Text2World)  [Files Files and versions  

xet](/nvidia/Cosmos-1.0-Diffusion-7B-Text2World/tree/main)  [Community

12](/nvidia/Cosmos-1.0-Diffusion-7B-Text2World/discussions)

 

Copy to bucket new   

Use this model  

### Instructions to use nvidia/Cosmos-1.0-Diffusion-7B-Text2World with libraries, inference providers, notebooks, and local apps. Follow these links to get started.

* Libraries
* [Cosmos](/nvidia/Cosmos-1.0-Diffusion-7B-Text2World?library=cosmos) 

  How to use nvidia/Cosmos-1.0-Diffusion-7B-Text2World with Cosmos:

  ```
  # No code snippets available yet for this library.

  # To use this model, check the repository files and the library's documentation.

  # Want to help? PRs adding snippets are welcome at:
  # https://github.com/huggingface/huggingface.js
  ```
* [NeMo](/nvidia/Cosmos-1.0-Diffusion-7B-Text2World?library=nemo) 

  How to use nvidia/Cosmos-1.0-Diffusion-7B-Text2World with NeMo:

  ```
  # tag did not correspond to a valid NeMo domain.
  ```
* [Diffusers](/nvidia/Cosmos-1.0-Diffusion-7B-Text2World?library=diffusers) 

  How to use nvidia/Cosmos-1.0-Diffusion-7B-Text2World with Diffusers:

  ```
  pip install -U diffusers transformers accelerate
  ```

  ```
  import torch
  from diffusers import DiffusionPipeline

  # switch to "mps" for apple devices
  pipe = DiffusionPipeline.from_pretrained("nvidia/Cosmos-1.0-Diffusion-7B-Text2World", dtype=torch.bfloat16, device_map="cuda")

  prompt = "Astronaut in a jungle, cold color palette, muted colors, detailed, 8k"
  image = pipe(prompt).images[0]
  ```
 * Notebooks
* [Google Colab](/nvidia/Cosmos-1.0-Diffusion-7B-Text2World/colab)
* [Kaggle](/nvidia/Cosmos-1.0-Diffusion-7B-Text2World/kaggle)

## You need to agree to share your contact information to access this model

The information you provide will be collected, stored, processed and shared in accordance with the [NVIDIA Privacy Policy](https://www.nvidia.com/en-us/about-nvidia/privacy-policy/).

# NVIDIA Open Model License Agreement

Version Release Date: January 6, 2025  
This NVIDIA Open Model License Agreement (the "Agreement") is a legal agreement between the Legal Entity You represent, or if no entity is identified, You and NVIDIA Corporation and its Affiliates ("NVIDIA") and governs Your use of the Models that NVIDIA provides to You under this Agreement. NVIDIA and You are each a "party" and collectively the "parties."  
NVIDIA models released under this Agreement are intended to be used permissively and enable the further development of AI technologies. Subject to the terms of this Agreement, NVIDIA confirms that:

* Models are commercially usable.
* You are free to create and distribute Derivative Models.
* NVIDIA does not claim ownership to any outputs generated using the Models or Model Derivatives.  
  By using, reproducing, modifying, distributing, performing or displaying any portion or element of the Model or Derivative Model, or otherwise accepting the terms of this Agreement, you agree to be bound by this Agreement.

## 1. Definitions

The following definitions apply to this Agreement:

1.1. "NVIDIA Cosmos Model" means a multimodal Model shared under this Agreement.

1.2. "Derivative Model" means all (a) modifications to the Model, (b) works based on the Model, and (c) any other derivative works of the Model. An output is not a Derivative Model.

1.3. "Legal Entity" means the union of the acting entity and all other entities that control, are controlled by, or are under common control with that entity. For the purposes of this definition, "control" means (a) the power, direct or indirect, to cause the direction or management of such entity, whether by contract or otherwise, or (b) ownership of fifty percent (50%) or more of the outstanding shares, or (c) beneficial ownership of such entity.

1.4. "Model" means the machine learning model, software, checkpoints, learnt weights, algorithms, parameters, configuration files and documentation shared under this Agreement.

1.5. "You" or "Your" means an individual or Legal Entity exercising permissions granted by this Agreement.

## 2. Conditions for Use, License Grant, AI Ethics and IP Ownership

2.1. Conditions for Use. The Model and any Derivative Model are subject to additional terms as described in Section 2 and Section 3 of this Agreement and govern Your use. If You institute copyright or patent litigation against any entity (including a cross-claim or counterclaim in a lawsuit) alleging that the Model or a Derivative Model constitutes direct or contributory copyright or patent infringement, then any licenses granted to You under this Agreement for that Model or Derivative Model will terminate as of the date such litigation is filed. If You bypass, disable, reduce the efficacy of, or circumvent any technical limitation, safety guardrail or associated safety guardrail hyperparameter, encryption, security, digital rights management, or authentication mechanism contained in the Model, your rights under this Agreement will automatically terminate. NVIDIA may update this Agreement to comply with legal and regulatory requirements at any time and You agree to either comply with any updated license or cease Your copying, use, and distribution of the Model and any Derivative Model.

2.2. License Grant. The rights granted herein are explicitly conditioned on Your full compliance with the terms of this Agreement. Subject to the terms and conditions of this Agreement, NVIDIA hereby grants to You a perpetual, worldwide, non-exclusive, no-charge, royalty-free, revocable (as stated in Section 2.1) license to publicly perform, publicly display, reproduce, use, create derivative works of, make, have made, sell, offer for sale, distribute (through multiple tiers of distribution) and import the Model.

2.3. AI Ethics. Use of the Models under the Agreement must be consistent with NVIDIA's Trustworthy AI terms found at <https://www.nvidia.com/en-us/agreements/trustworthy-ai/terms/>.

2.4. NVIDIA owns the Model and any Model Derivatives created by NVIDIA. Subject to NVIDIA's underlying ownership rights in the Model or its Model Derivatives, You are and will be the owner of Your Model Derivatives. NVIDIA claims no ownership rights in outputs. You are responsible for outputs and their subsequent uses. Except as expressly granted in this Agreement, (a) NVIDIA reserves all rights, interests and remedies in connection with the Model and (b) no other license or right is granted to you by implication, estoppel or otherwise.

## 3. Redistribution

You may reproduce and distribute copies of the Model or Derivative Models thereof in any medium, with or without modifications, provided that You meet the following conditions:

3.1. If you distribute the Model, You must give any other recipients of the Model a copy of this Agreement and include the following attribution notice within a "Notice" text file with such copies: "Licensed by NVIDIA Corporation under the NVIDIA Open Model License";

3.2. If you distribute or make available a NVIDIA Cosmos Model, or a product or service (including an AI model) that contains or uses a NVIDIA Cosmos Model, use a NVIDIA Cosmos Model to create a Derivative Model, or use a NVIDIA Cosmos Model or its outputs to create, train, fine tune, or otherwise improve an AI model, you will include "Built on NVIDIA Cosmos" on a related website, user interface, blogpost, about page, or product documentation; and

3.3. You may add Your own copyright statement to Your modifications and may provide additional or different license terms and conditions for use, reproduction, or distribution of Your modifications, or for any such Derivative Models as a whole, provided Your use, reproduction, and distribution of the Model otherwise complies with the conditions stated in this Agreement.

## 4. Trademarks

This Agreement does not grant permission to use the trade names, trademarks, service marks, or product names of NVIDIA, except as required for reasonable and customary use in describing the origin of the Model and reproducing the content of the "Notice" text file.

## **5. Disclaimer of Warranty**

**Unless required by applicable law or agreed to in writing, NVIDIA provides the Model on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied, including, without limitation, any warranties or conditions of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A PARTICULAR PURPOSE. You are solely responsible for determining the appropriateness of using or redistributing the Model, Derivative Models and outputs and assume any risks associated with Your exercise of permissions under this Agreement.**

## **6. Limitation of Liability**

**In no event and under no legal theory, whether in tort (including negligence), contract, or otherwise, unless required by applicable law (such as deliberate and grossly negligent acts) or agreed to in writing, will NVIDIA be liable to You for damages, including any direct, indirect, special, incidental, or consequential damages of any character arising as a result of this Agreement or out of the use or inability to use the Model, Derivative Models or outputs (including but not limited to damages for loss of goodwill, work stoppage, computer failure or malfunction, or any and all other commercial damages or losses), even if NVIDIA has been advised of the possibility of such damages.**

## 7. Indemnity

You will indemnify and hold harmless NVIDIA from and against any claim by any third party arising out of or related to your use or distribution of the Model, Model Derivatives or outputs.

## 8. Feedback

NVIDIA appreciates your feedback, and You agree that NVIDIA may use it without restriction or compensation to You.

## 9. Governing Law

This Agreement will be governed in all respects by the laws of the United States and the laws of the State of Delaware, without regard to conflict of laws principles or the United Nations Convention on Contracts for the International Sale of Goods. The state and federal courts residing in Santa Clara County, California will have exclusive jurisdiction over any dispute or claim arising out of or related to this Agreement, and the parties irrevocably consent to personal jurisdiction and venue in those courts; except that, either party may apply for injunctive remedies or an equivalent type of urgent legal relief in any jurisdiction.

## 10. Trade and Compliance

You agree to comply with all applicable export, import, trade and economic sanctions laws and regulations, as amended, including without limitation U.S. Export Administration Regulations and Office of Foreign Assets Control regulations. These laws include restrictions on destinations, end-users and end-use.

 

[Log in](/login?next=%2Fnvidia%2FCosmos-1.0-Diffusion-7B-Text2World) or [Sign Up](/join?next=%2Fnvidia%2FCosmos-1.0-Diffusion-7B-Text2World) to review the conditions and access this model content.

 

* [**Cosmos-1.0-Diffusion**: A Suite of Diffusion-based World Foundation Models](#cosmos-10-diffusion-a-suite-of-diffusion-based-world-foundation-models "Cosmos-1.0-Diffusion: A Suite of Diffusion-based World Foundation Models")
* [Model Overview](#model-overview "Model Overview")
  + [Description:](#description "Description:")
  + [Model Versions](#model-versions "Model Versions")
    - [License:](#license "License:")
  + [Model Architecture:](#model-architecture "Model Architecture:")
  + [Input/Output Specifications](#inputoutput-specifications "Input/Output Specifications")
  + [Software Integration](#software-integration "Software Integration")
* [Usage](#usage "Usage")
* [Evaluation](#evaluation "Evaluation")
  + [Inference Time and GPU Memory Usage](#inference-time-and-gpu-memory-usage "Inference Time and GPU Memory Usage")
  + [Ethical Considerations](#ethical-considerations "Ethical Considerations")
    - [Plus Plus (++) Promise](#plus-plus--promise "Plus Plus (++) Promise")
    - [Bias](#bias "Bias")
    - [Explainability](#explainability "Explainability")
    - [Privacy](#privacy "Privacy")
    - [Safety](#safety "Safety")

# **Cosmos-1.0-Diffusion**: A Suite of Diffusion-based World Foundation Models

[**Cosmos**](https://huggingface.co/collections/nvidia/cosmos-6751e884dc10e013a0a0d8e6) | [**Code**](https://github.com/NVIDIA/Cosmos) | [**Paper**](https://arxiv.org/abs/2501.03575) | [**Paper Website**](https://research.nvidia.com/labs/dir/cosmos1/)

# Model Overview

## Description:

**Cosmos World Foundation Models**: A family of highly performant pre-trained world foundation models purpose-built for generating physics-aware videos and world states for physical AI development.

The Cosmos diffusion models are a collection of diffusion based world foundation models that generate dynamic, high quality videos from text, image, or video inputs. It can serve as the building block for various applications or research that are related to world generation. The models are ready for commercial use under NVIDIA Open Model license agreement.

**Model Developer**: NVIDIA

## Model Versions

In Cosmos 1.0 release, the Cosmos Diffusion WFM family includes the following models:

* [Cosmos-1.0-Diffusion-7B-Text2World](https://huggingface.co/nvidia/Cosmos-1.0-Diffusion-7B-Text2World)
  + Given a text description, predict an output video of 121 frames.
* [Cosmos-1.0-Diffusion-14B-Text2World](https://huggingface.co/nvidia/Cosmos-1.0-Diffusion-14B-Text2World)
  + Given a text description, predict an output video of 121 frames.
* [Cosmos-1.0-Diffusion-7B-Video2World](https://huggingface.co/nvidia/Cosmos-1.0-Diffusion-7B-Video2World)
  + Given a text description and an image as the first frame, predict the future 120 frames.
* [Cosmos-1.0-Diffusion-14B-Video2World](https://huggingface.co/nvidia/Cosmos-1.0-Diffusion-14B-Video2World)
  + Given a text description and an image as the first frame, predict the future 120 frames.

### License:

This model is released under the [NVIDIA Open Model License](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license). For a custom license, please contact [cosmos-license@nvidia.com](mailto:cosmos-license@nvidia.com).

Under the NVIDIA Open Model License, NVIDIA confirms:

* Models are commercially usable.
* You are free to create and distribute Derivative Models.
* NVIDIA does not claim ownership to any outputs generated using the Models or Derivative Models.

**Important Note**: If you bypass, disable, reduce the efficacy of, or circumvent any technical limitation, **safety guardrail** or
associated safety guardrail hyperparameter, encryption, security, digital rights management, or authentication mechanism contained
in the Model, your rights under [NVIDIA Open Model License Agreement](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license) will automatically terminate.

* [Cosmos-1.0-Guardrail](https://huggingface.co/nvidia/Cosmos-1.0-Guardrail) is the safety guardrail for this model.

## Model Architecture:

Cosmos-1.0-Diffusion-7B-Text2World is a diffusion transformer model designed for video denoising in the latent space. The network is composed of interleaved self-attention, cross-attention and feedforward layers as its building blocks. The cross-attention layers allow the model to condition on input text throughout the denoising process. Before each layers, adaptive layer normalization is applied to embed the time information for denoising. When image or video is provided as input, their latent frames are concatenated with the generated frames along the temporal dimension. Augment noise is added to conditional latent frames to bridge the training and inference gap.

## Input/Output Specifications

* **Input**

  + **Input Type(s)**: Text
  + **Input Format(s)**: String
  + **Input Parameters**: One-dimensional (1D)
  + **Other Properties Related to Input**:
    - The input string should contain fewer than 300 words and should provide descriptive content for world generation, such as a scene description, key objects or characters, background, and any specific actions or motions to be depicted within the 5-second duration.
* **Output**

  + **Output Type(s)**: Video
  + **Output Format(s)**: mp4
  + **Output Parameters**: Three-dimensional (3D)
  + **Other Properties Related to Output**: By default, the generated video is a 5-second clip with a resolution of 1280x704 pixels and a frame rate of 24 frames per second (fps). The video content visualizes the input text description as a short animated scene, capturing key elements within the specified time constraints. Aspect ratios and resolutions are configurable, with options including 1:1 (960x960 pixels), 4:3 (960x704 pixels), 3:4 (704x960 pixels), 16:9 (1280x704 pixels), and 9:16 (704x1280 pixels). The frame rate is also adjustable within a range of 12 to 40 fps.

## Software Integration

**Runtime Engine(s):**

* [Cosmos](https://github.com/NVIDIA/Cosmos)
* [Diffusers](https://github.com/huggingface/diffusers)

**Supported Hardware Microarchitecture Compatibility:**

* NVIDIA Blackwell
* NVIDIA Hopper
* NVIDIA Ampere

**Note**: We have only tested inference with BF16 precision.

**Operating System(s):**

* Linux (We have not tested on other operating systems.)

# Usage

* See [Cosmos](https://github.com/NVIDIA/Cosmos) for details.

Cosmos can also be used with Diffusers!

```
import torch
from diffusers import CosmosTextToWorldPipeline
from diffusers.utils import export_to_video

model_id = "nvidia/Cosmos-1.0-Diffusion-7B-Text2World"
pipe = CosmosTextToWorldPipeline.from_pretrained(model_id, torch_dtype=torch.bfloat16)
pipe.to("cuda")

prompt = "A sleek, humanoid robot stands in a vast warehouse filled with neatly stacked cardboard boxes on industrial shelves. The robot's metallic body gleams under the bright, even lighting, highlighting its futuristic design and intricate joints. A glowing blue light emanates from its chest, adding a touch of advanced technology. The background is dominated by rows of boxes, suggesting a highly organized storage system. The floor is lined with wooden pallets, enhancing the industrial setting. The camera remains static, capturing the robot's poised stance amidst the orderly environment, with a shallow depth of field that keeps the focus on the robot while subtly blurring the background for a cinematic effect."

output = pipe(prompt=prompt).frames[0]
export_to_video(output, "output.mp4", fps=30)
```

Find more information in the diffusers [documentation](https://huggingface.co/docs/diffusers/main/en/api/pipelines/cosmos).

# Evaluation

Please see our [technical paper](https://research.nvidia.com/publication/2025-01_cosmos-world-foundation-model-platform-physical-ai) for detailed evaluations.

## Inference Time and GPU Memory Usage

The numbers provided below may vary depending on system specs and are for reference only.

We report the maximum observed GPU memory usage during end-to-end inference. Additionally, we offer a series of model offloading strategies to help users manage GPU memory usage effectively.

For GPUs with limited memory (e.g., RTX 3090/4090 with 24 GB memory), we recommend fully offloading all models. For higher-end GPUs, users can select the most suitable offloading strategy considering the numbers provided below.

| Offloading Strategy | 7B Text2World | 14B Text2World |
| --- | --- | --- |
| Offload prompt upsampler | 74.0 GB | > 80.0 GB |
| Offload prompt upsampler & guardrails | 57.1 GB | 70.5 GB |
| Offload prompt upsampler & guardrails & T5 encoder | 38.5 GB | 51.9 GB |
| Offload prompt upsampler & guardrails & T5 encoder & tokenizer | 38.3 GB | 51.7 GB |
| Offload prompt upsampler & guardrails & T5 encoder & tokenizer & diffusion model | 24.4 GB | 39.0 GB |

The table below presents the end-to-end inference runtime on a single H100 GPU, excluding model initialization time.

| 7B Text2World (offload prompt upsampler) | 14B Text2World (offload prompt upsampler, guardrails) |
| --- | --- |
| ~380 seconds | ~590 seconds |

## Ethical Considerations

NVIDIA believes Trustworthy AI is a shared responsibility and we have established policies and practices to enable development for a wide array of AI applications. When downloaded or used in accordance with our terms of service, developers should work with their internal model team to ensure this model meets requirements for the relevant industry and use case and addresses unforeseen product misuse.

For more detailed information on ethical considerations for this model, please see the subcards of Explainability, Bias, Safety & Security, and Privacy below. Please report security vulnerabilities or NVIDIA AI Concerns [here](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).

### Plus Plus (++) Promise

We value you, the datasets, the diversity they represent, and what we have been entrusted with. This model and its associated data have been:

* Verified to comply with current applicable disclosure laws, regulations, and industry standards.
* Verified to comply with applicable privacy labeling requirements.
* Annotated to describe the collector/source (NVIDIA or a third-party).
* Characterized for technical limitations.
* Reviewed to ensure proper disclosure is accessible to, maintained for, and in compliance with NVIDIA data subjects and their requests.
* Reviewed before release.
* Tagged for known restrictions and potential safety implications.

### Bias

| Field | Response |
| --- | --- |
| Participation considerations from adversely impacted groups [protected classes](https://www.senate.ca.gov/content/protected-classes) in model design and testing: | None |
| Measures taken to mitigate against unwanted bias: | None |

### Explainability

| Field | Response |
| --- | --- |
| Intended Application & Domain: | World Generation |
| Model Type: | Transformer |
| Intended Users: | Physical AI developers |
| Output: | Videos |
| Describe how the model works: | Generates videos based on video inputs |
| Technical Limitations: | The model may not follow the video input accurately. |
| Verified to have met prescribed NVIDIA quality standards: | Yes |
| Performance Metrics: | Quantitative and Qualitative Evaluation |
| Potential Known Risks: | The model's output can generate all forms of videos, including what may be considered toxic, offensive, or indecent. |
| Licensing: | [NVIDIA Open Model License](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license) |

### Privacy

| Field | Response |
| --- | --- |
| Generatable or reverse engineerable personal information? | None Known |
| Protected class data used to create this model? | None Known |
| Was consent obtained for any personal data used? | None Known |
| How often is dataset reviewed? | Before Release |
| Is a mechanism in place to honor data subject right of access or deletion of personal data? | Not Applicable |
| If personal data was collected for the development of the model, was it collected directly by NVIDIA? | Not Applicable |
| If personal data was collected for the development of the model by NVIDIA, do you maintain or have access to disclosures made to data subjects? | Not Applicable |
| If personal data was collected for the development of this AI model, was it minimized to only what was required? | Not Applicable |
| Is there provenance for all datasets used in training? | Yes |
| Does data labeling (annotation, metadata) comply with privacy laws? | Yes |
| Is data compliant with data subject requests for data correction or removal, if such a request was made? | Not Applicable |

### Safety

| Field | Response |
| --- | --- |
| Model Application(s): | World Generation |
| Describe the life critical impact (if present). | None Known |
| Use Case Restrictions: | [NVIDIA Open Model License](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license) |
| Model and dataset restrictions: | The Principle of least privilege (PoLP) is applied limiting access for dataset generation and model development. Restrictions enforce dataset access during training, and dataset license constraints adhered to. Model checkpoints are made available on Hugging Face, and may become available on cloud providers' model catalog. |

Downloads last month
:   2,171

 

Inference Providers [NEW](https://huggingface.co/docs/inference-providers)

[Text-to-Video](/tasks/text-to-video "Learn more about text-to-video")

  

This model isn't deployed by any Inference Provider. [🙋 1 Ask for provider support](/spaces/huggingface/InferenceSupport/discussions/3454)

## Model tree for nvidia/Cosmos-1.0-Diffusion-7B-Text2World

Quantizations

 [1 model](/models?other=base_model:quantized:nvidia/Cosmos-1.0-Diffusion-7B-Text2World)

   

## Collection including nvidia/Cosmos-1.0-Diffusion-7B-Text2World

[#### Cosmos-Preidct1

Collection

⚠️ This collection is archived.
👉 https://huggingface.co/collections/nvidia/cosmos3 • 14 items • Updated 13 days ago •  304](/collections/nvidia/cosmos-preidct1)

 

## Paper for nvidia/Cosmos-1.0-Diffusion-7B-Text2World

[#### Cosmos World Foundation Model Platform for Physical AI

Paper • 2501.03575 • Published Jan 7, 2025 •  83](/papers/2501.03575)

 

System theme

Company

[TOS](/terms-of-service) [Privacy](/privacy) [About](/huggingface) [Careers](https://apply.workable.com/huggingface/) 

Website

[Models](/models) [Datasets](/datasets) [Spaces](/spaces) [Pricing](/pricing) [Docs](/docs)



Inference providers allow you to run inference using different serverless providers.
