---
license: agpl-3.0
tags:
- text-to-image
- image-to-text
- image-captioning
- image-variation
- text-variation
- multi-modality
- generative model
---

UniDiffuser is a unified diffusion framework to fit all distributions relevant to a set of multi-modal data in one transformer.
UniDiffuser is able to perform image, text, text-to-image, image-to-text, and image-text pair generation by setting proper timesteps without additional overhead. 



Specifically, UniDiffuser employs a variation of transformer, called [U-ViT](https://github.com/baofff/U-ViT), which parameterizes the joint noise prediction network. Other components perform as encoders and decoders of different modalities, including a pretrained image autoencoder from [Stable Diffusion](https://github.com/CompVis/stable-diffusion), a pretrained [image ViT-B/32 CLIP encoder](https://github.com/openai/CLIP), a pretrained [text ViT-L CLIP encoder](https://huggingface.co/openai/clip-vit-large-patch14), and a [GPT-2](https://github.com/openai/gpt-2) text decoder finetuned by ourselves.


We provide two versions of UniDiffuser:
- [UniDiffuser-v0](https://huggingface.co/thu-ml/unidiffuser-v0): This version is trained on [LAION-5B](https://laion.ai/), which contains noisy webdata of text-image pairs.
- [UniDiffuser-v1](https://huggingface.co/thu-ml/unidiffuser-v1): This version is resumed from UniDiffuser-v0, and is further trained with a set of less noisy internal text-image pairs. It uses a flag as its input to distinguish webdata and internal data during training.


## Download
We provide files for UniDiffuser-v0 in [this link](https://huggingface.co/thu-ml/unidiffuser-v0/tree/main), and files for UniDiffuser-v1 in [this link](https://huggingface.co/thu-ml/unidiffuser-v1/tree/main).
These files are:
- `autoencoder_kl.pth` is the weight of the image autoencoder converted from [Stable Diffusion](https://github.com/CompVis/stable-diffusion).
- `caption_decoder.pth` is the weight of the finetuned GPT-2 text decoder.
- `uvit_v0.pth/uvit_v1.pth` is the weight of U-ViT for UniDiffuser-v0/UniDiffuser-v1.

Note that UniDiffuser-v0 and UniDiffuser-v1 share the same `autoencoder_kl.pth` and `caption_decoder.pth`. You only need to download them once.
As for other components, they will be automatically downloaded.

The `diffusers` pipeline for UniDiffuser-v1 can be downloaded as follows:

```python
from diffusers import UniDiffuserPipeline

pipe = UniDiffuserPipeline.from_pretrained("thu-ml/unidiffuser-v1")
```

## Usage
Use the model with [UniDiffuser codebase](https://github.com/thu-ml/unidiffuser).

Here is an example using UniDiffuser-v1 with `diffusers`:

```python
import requests
import torch
from PIL import Image
from io import BytesIO

from diffusers import UniDiffuserPipeline

device = "cuda"
model_id_or_path = "thu-ml/unidiffuser-v1"
pipe = UniDiffuserPipeline.from_pretrained(model_id_or_path, torch_dtype=torch.float16)
pipe.to(device)

# Joint image-text generation. The generation task is automatically inferred.
sample = pipe(num_inference_steps=20, guidance_scale=8.0)
image = sample.images[0]
text = sample.text[0]
image.save("unidiffuser_sample_joint_image.png")
print(text)

# The mode can be set manually. The following is equivalent to the above:
pipe.set_joint_mode()
sample2 = pipe(num_inference_steps=20, guidance_scale=8.0)

# Note that if you set the mode manually the pipeline will no longer attempt
# to automatically infer the mode. You can re-enable this with reset_mode().
pipe.reset_mode()

# Text-to-image generation.
prompt = "an elephant under the sea"

sample = pipe(prompt=prompt, num_inference_steps=20, guidance_scale=8.0)
t2i_image = sample.images[0]
t2i_image.save("unidiffuser_sample_text2img_image.png")

# Image-to-text generation.
image_url = "https://huggingface.co/datasets/hf-internal-testing/diffusers-images/resolve/main/unidiffuser/unidiffuser_example_image.jpg"
response = requests.get(image_url)
init_image = Image.open(BytesIO(response.content)).convert("RGB")
init_image = init_image.resize((512, 512))

sample = pipe(image=init_image, num_inference_steps=20, guidance_scale=8.0)
i2t_text = sample.text[0]
print(i2t_text)

# Image variation can be performed with a image-to-text generation followed by a text-to-image generation:
sample = pipe(prompt=i2t_text, num_inference_steps=20, guidance_scale=8.0)
final_image = sample.images[0]
final_image.save("unidiffuser_image_variation_sample.png")

# Text variation can be performed with a text-to-image generation followed by a image-to-text generation:
sample = pipe(image=t2i_image, num_inference_steps=20, guidance_scale=8.0)
final_prompt = sample.text[0]
print(final_prompt)
```

## Model Details
- **Model type:** Diffusion-based multi-modal generation model
- **Language(s):** English
- **License:** agpl-3.0
- **Model Description:** This is a model that can perform image, text, text-to-image, image-to-text, and image-text pair generation. Its main component is a [U-ViT](https://github.com/baofff/U-ViT), which parameterizes the joint noise prediction network. Other components perform as encoders and decoders of different modalities, including a pretrained image autoencoder from [Stable Diffusion](https://github.com/CompVis/stable-diffusion), a pretrained [image ViT-B/32 CLIP encoder](https://github.com/openai/CLIP), a pretrained [text ViT-L CLIP encoder](https://huggingface.co/openai/clip-vit-large-patch14), and a [GPT-2](https://github.com/openai/gpt-2) text decoder finetuned by ourselves.
- **Resources for more information:** [GitHub Repository](https://github.com/thu-ml/unidiffuser), [Paper]().


## Direct Use 

_Note: Most of this section is taken from the [Stable Diffusion model card](https://huggingface.co/CompVis/stable-diffusion-v-1-4-original), but applies in the same way to UniDiffuser_.


The model should be used following the agpl-3.0 license. Possible usage includes

- Safe deployment of models which have the potential to generate harmful content.
- Probing and understanding the limitations and biases of generative models.
- Generation of artworks and use in design and other artistic processes.
- Applications in educational or creative tools.
- Research on generative models.

Excluded uses are described below.

### Misuse, Malicious Use, and Out-of-Scope Use


The model should not be used to intentionally create or disseminate images that create hostile or alienating environments for people. This includes generating images that people would foreseeably find disturbing, distressing, or offensive; or content that propagates historical or current stereotypes.
#### Out-of-Scope Use
The model was not trained to be factual or true representations of people or events, and therefore using the model to generate such content is out-of-scope for the abilities of this model.
#### Misuse and Malicious Use
Using the model to generate content that is cruel to individuals is a misuse of this model. This includes, but is not limited to:

- Generating demeaning, dehumanizing, or otherwise harmful representations of people or their environments, cultures, religions, etc.
- Intentionally promoting or propagating discriminatory content or harmful stereotypes.
- Impersonating individuals without their consent.
- Sexual content without consent of the people who might see it.
- Mis- and disinformation
- Representations of egregious violence and gore
- Sharing of copyrighted or licensed material in violation of its terms of use.
- Sharing content that is an alteration of copyrighted or licensed material in violation of its terms of use.