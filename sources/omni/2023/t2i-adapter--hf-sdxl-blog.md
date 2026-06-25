# Efficient Controllable Generation for SDXL with T2I-Adapters
Source: https://huggingface.co/blog/t2i-sdxl-adapters
 
Efficient Controllable Generation for SDXL with T2I-Adapters



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

      

[Back to Articles](/blog)

# Efficient Controllable Generation for SDXL with T2I-Adapters

Published
September 8, 2023

[Update on GitHub](https://github.com/huggingface/blog/blob/main/t2i-sdxl-adapters.md)

[Upvote

9](/login?next=%2Fblog%2Ft2i-sdxl-adapters)  

* [![](https://cdn-avatars.huggingface.co/v1/production/uploads/603bdba23249b99991dbcbc4/cxCnN1H-RXOhojHY3Wcxo.jpeg)](/tolgacangoz "tolgacangoz")
* [![](https://cdn-avatars.huggingface.co/v1/production/uploads/60e272ca6c78a8c122b12127/xldEGBzGrU-bX6IwAw0Ie.jpeg)](/Xintao "Xintao")
* [![](https://cdn-avatars.huggingface.co/v1/production/uploads/6266513d539521e602b5dc3a/7ZU_GyMBzrFHcHDoAkQlp.png)](/ameerazam08 "ameerazam08")
* [![](/avatars/de9792ea25076aec98712d4acf4a2e86.svg)](/jakobsal "jakobsal")
* [![](https://cdn-avatars.huggingface.co/v1/production/uploads/654bcb6fae75d15300d48205/T4L1RZUgCZgdik4ZhEWCq.jpeg)](/Steveeeeeeen "Steveeeeeeen")
* [![](/avatars/71764067260c9de7d7bf53795020a7b5.svg)](/Devin008 "Devin008")
* +3

[![ChongMou's avatar](/avatars/d13b35964c895f7aec69287390036a79.svg)](/Adapter) 

[ChongMou

Adapter 

Follow](/Adapter)

guest

[![Suraj Patil's avatar](https://cdn-avatars.huggingface.co/v1/production/uploads/1600014820272-5ec0135ded25d76864d553f1.jpeg)](/valhalla) 

[Suraj Patil

valhalla 

Follow](/valhalla)

[![Sayak Paul's avatar](https://cdn-avatars.huggingface.co/v1/production/uploads/1649681653581-5f7fbd813e94f16a85448745.jpeg)](/sayakpaul) 

[Sayak Paul

sayakpaul 

Follow](/sayakpaul)

[![Xintao Wang's avatar](https://cdn-avatars.huggingface.co/v1/production/uploads/60e272ca6c78a8c122b12127/xldEGBzGrU-bX6IwAw0Ie.jpeg)](/Xintao) 

[Xintao Wang

Xintao 

Follow](/Xintao)

guest

[![hysts's avatar](https://cdn-avatars.huggingface.co/v1/production/uploads/1643012094339-61914f536d34e827404ceb99.jpeg)](/hysts) 

[hysts

hysts 

Follow](/hysts)

 

This article is also available in Chinese [简体中文](/blog/zh/t2i-sdxl-adapters).

 

![](https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/blog/t2i-adapters-sdxl/hf_tencent.png)

* [Training T2I-Adapter-SDXL with `diffusers`](#training-t2i-adapter-sdxl-with-diffusers "Training T2I-Adapter-SDXL with <code>diffusers</code>")
* [Using T2I-Adapter-SDXL in `diffusers`](#using-t2i-adapter-sdxl-in-diffusers "Using T2I-Adapter-SDXL in <code>diffusers</code>")
* [Try out the Demo](#try-out-the-demo "Try out the Demo")
* [More Results](#more-results "More Results")
  + [Lineart Guided](#lineart-guided "Lineart Guided")
  + [Sketch Guided](#sketch-guided "Sketch Guided")
  + [Canny Guided](#canny-guided "Canny Guided")
  + [Depth Guided](#depth-guided "Depth Guided")
  + [OpenPose Guided](#openpose-guided "OpenPose Guided")

[T2I-Adapter](https://huggingface.co/papers/2302.08453) is an efficient plug-and-play model that provides extra guidance to pre-trained text-to-image models while freezing the original large text-to-image models. T2I-Adapter aligns internal knowledge in T2I models with external control signals. We can train various adapters according to different conditions and achieve rich control and editing effects.

As a contemporaneous work, [ControlNet](https://hf.co/papers/2302.05543) has a similar function and is widely used. However, it can be **computationally expensive** to run. This is because, during each denoising step of the reverse diffusion process, both the ControlNet and UNet need to be run. In addition, ControlNet emphasizes the importance of copying the UNet encoder as a control model, resulting in a larger parameter number. Thus, the generation is bottlenecked by the size of the ControlNet (the larger, the slower the process becomes).

T2I-Adapters provide a competitive advantage to ControlNets in this matter. T2I-Adapters are smaller in size, and unlike ControlNets, T2I-Adapters are run just once for the entire course of the denoising process.

| **Model Type** | **Model Parameters** | **Storage (fp16)** |
| --- | --- | --- |
| [ControlNet-SDXL](https://huggingface.co/diffusers/controlnet-canny-sdxl-1.0) | 1251 M | 2.5 GB |
| [ControlLoRA](https://huggingface.co/stabilityai/control-lora) (with rank 128) | 197.78 M (84.19% reduction) | 396 MB (84.53% reduction) |
| [T2I-Adapter-SDXL](https://huggingface.co/TencentARC/t2i-adapter-canny-sdxl-1.0) | 79 M (***93.69% reduction***) | 158 MB (***94% reduction***) |

Over the past few weeks, the Diffusers team and the T2I-Adapter authors have been collaborating to bring the support of T2I-Adapters for [Stable Diffusion XL (SDXL)](https://huggingface.co/papers/2307.01952) in [`diffusers`](https://github.com/huggingface/diffusers). In this blog post, we share our findings from training T2I-Adapters on SDXL from scratch, some appealing results, and, of course, the T2I-Adapter checkpoints on various conditionings (sketch, canny, lineart, depth, and openpose)!

[![Collage of the results](https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/blog/t2i-adapters-sdxl/results_collage.png)](https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/blog/t2i-adapters-sdxl/results_collage.png)

Compared to previous versions of T2I-Adapter (SD-1.4/1.5), [T2I-Adapter-SDXL](https://github.com/TencentARC/T2I-Adapter) still uses the original recipe, driving 2.6B SDXL with a 79M Adapter! T2I-Adapter-SDXL maintains powerful control capabilities while inheriting the high-quality generation of SDXL!

## Training T2I-Adapter-SDXL with `diffusers`

We built our training script on [this official example](https://github.com/huggingface/diffusers/blob/main/examples/t2i_adapter/README_sdxl.md) provided by `diffusers`.

Most of the T2I-Adapter models we mention in this blog post were trained on 3M high-resolution image-text pairs from LAION-Aesthetics V2 with the following settings:

* Training steps: 20000-35000
* Batch size: Data parallel with a single GPU batch size of 16 for a total batch size of 128.
* Learning rate: Constant learning rate of 1e-5.
* Mixed precision: fp16

We encourage the community to use our scripts to train custom and powerful T2I-Adapters, striking a competitive trade-off between speed, memory, and quality.

## Using T2I-Adapter-SDXL in `diffusers`

Here, we take the lineart condition as an example to demonstrate the usage of [T2I-Adapter-SDXL](https://github.com/TencentARC/T2I-Adapter/tree/XL). To get started, first install the required dependencies:

```
pip install -U git+https://github.com/huggingface/diffusers.git
pip install -U controlnet_aux==0.0.7 # for conditioning models and detectors
pip install transformers accelerate
```

The generation process of the T2I-Adapter-SDXL mainly consists of the following two steps:

1. Condition images are first prepared into the appropriate *control image* format.
2. The *control image* and *prompt* are passed to the [`StableDiffusionXLAdapterPipeline`](https://github.com/huggingface/diffusers/blob/0ec7a02b6a609a31b442cdf18962d7238c5be25d/src/diffusers/pipelines/t2i_adapter/pipeline_stable_diffusion_xl_adapter.py#L126).

Let's have a look at a simple example using the [Lineart Adapter](https://huggingface.co/TencentARC/t2i-adapter-lineart-sdxl-1.0). We start by initializing the T2I-Adapter pipeline for SDXL and the lineart detector.

```
import torch
from controlnet_aux.lineart import LineartDetector
from diffusers import (AutoencoderKL, EulerAncestralDiscreteScheduler,
                       StableDiffusionXLAdapterPipeline, T2IAdapter)
from diffusers.utils import load_image, make_image_grid

# load adapter
adapter = T2IAdapter.from_pretrained(
    "TencentARC/t2i-adapter-lineart-sdxl-1.0", torch_dtype=torch.float16, varient="fp16"
).to("cuda")

# load pipeline
model_id = "stabilityai/stable-diffusion-xl-base-1.0"
euler_a = EulerAncestralDiscreteScheduler.from_pretrained(
    model_id, subfolder="scheduler"
)
vae = AutoencoderKL.from_pretrained(
    "madebyollin/sdxl-vae-fp16-fix", torch_dtype=torch.float16
)
pipe = StableDiffusionXLAdapterPipeline.from_pretrained(
    model_id,
    vae=vae,
    adapter=adapter,
    scheduler=euler_a,
    torch_dtype=torch.float16,
    variant="fp16",
).to("cuda")

# load lineart detector
line_detector = LineartDetector.from_pretrained("lllyasviel/Annotators").to("cuda")
```

Then, load an image to detect lineart:

```
url = "https://huggingface.co/Adapter/t2iadapter/resolve/main/figs_SDXLV1.0/org_lin.jpg"
image = load_image(url)
image = line_detector(image, detect_resolution=384, image_resolution=1024)
```

[![Lineart Dragon](https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/blog/t2i-adapters-sdxl/lineart_dragon.png)](https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/blog/t2i-adapters-sdxl/lineart_dragon.png)

Then we generate:

```
prompt = "Ice dragon roar, 4k photo"
negative_prompt = "anime, cartoon, graphic, text, painting, crayon, graphite, abstract, glitch, deformed, mutated, ugly, disfigured"
gen_images = pipe(
    prompt=prompt,
    negative_prompt=negative_prompt,
    image=image,
    num_inference_steps=30,
    adapter_conditioning_scale=0.8,
    guidance_scale=7.5,
).images[0]
gen_images.save("out_lin.png")
```

[![Lineart Generated Dragon](https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/blog/t2i-adapters-sdxl/lineart_generated_dragon.png)](https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/blog/t2i-adapters-sdxl/lineart_generated_dragon.png)

There are two important arguments to understand that help you control the amount of conditioning.

1. `adapter_conditioning_scale`

   This argument controls how much influence the conditioning should have on the input. High values mean a higher conditioning effect and vice-versa.
2. `adapter_conditioning_factor`

   This argument controls how many initial generation steps should have the conditioning applied. The value should be set between 0-1 (default is 1). The value of `adapter_conditioning_factor=1` means the adapter should be applied to all timesteps, while the `adapter_conditioning_factor=0.5` means it will only applied for the first 50% of the steps.

For more details, we welcome you to check the [official documentation](https://huggingface.co/docs/diffusers/main/en/api/pipelines/stable_diffusion/adapter).

## Try out the Demo

You can easily try T2I-Adapter-SDXL in [this Space](https://huggingface.co/spaces/TencentARC/T2I-Adapter-SDXL) or in the playground embedded below:

You can also try out [Doodly](https://huggingface.co/spaces/TencentARC/T2I-Adapter-SDXL-Sketch), built using the sketch model that turns your doodles into realistic images (with language supervision):

## More Results

Below, we present results obtained from using different kinds of conditions. We also supplement the results with links to their corresponding pre-trained checkpoints. Their model cards contain more details on how they were trained, along with example usage.

### Lineart Guided

[![Lineart guided more results](https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/blog/t2i-adapters-sdxl/lineart_guided.png)](https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/blog/t2i-adapters-sdxl/lineart_guided.png)
*Model from [`TencentARC/t2i-adapter-lineart-sdxl-1.0`](https://huggingface.co/TencentARC/t2i-adapter-lineart-sdxl-1.0)*

### Sketch Guided

[![Sketch guided results](https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/blog/t2i-adapters-sdxl/sketch_guided.png)](https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/blog/t2i-adapters-sdxl/sketch_guided.png)
*Model from [`TencentARC/t2i-adapter-sketch-sdxl-1.0`](https://huggingface.co/TencentARC/t2i-adapter-sketch-sdxl-1.0)*

### Canny Guided

[![Sketch guided results](https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/blog/t2i-adapters-sdxl/canny_guided.png)](https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/blog/t2i-adapters-sdxl/canny_guided.png)
*Model from [`TencentARC/t2i-adapter-canny-sdxl-1.0`](https://huggingface.co/TencentARC/t2i-adapter-canny-sdxl-1.0)*

### Depth Guided

[![Depth guided results](https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/blog/t2i-adapters-sdxl/depth_guided.png)](https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/blog/t2i-adapters-sdxl/depth_guided.png)
*Depth guided models from [`TencentARC/t2i-adapter-depth-midas-sdxl-1.0`](https://huggingface.co/TencentARC/t2i-adapter-depth-midas-sdxl-1.0) and [`TencentARC/t2i-adapter-depth-zoe-sdxl-1.0`](https://huggingface.co/TencentARC/t2i-adapter-depth-zoe-sdxl-1.0) respectively*

### OpenPose Guided

[![OpenPose guided results](https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/blog/t2i-adapters-sdxl/pose_guided.png)](https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/blog/t2i-adapters-sdxl/pose_guided.png)
*Model from [`TencentARC/t2i-adapter-openpose-sdxl-1.0`](https://hf.co/TencentARC/t2i-adapter-openpose-sdxl-1.0)*

---

*Acknowledgements: Immense thanks to [William Berman](https://twitter.com/williamLberman) for helping us train the models and sharing his insights.*

## Models mentioned in this article 8

[![](https://cdn-avatars.huggingface.co/v1/production/uploads/1625552871844-60e272ca6c78a8c122b12127.png)

#### TencentARC/t2i-adapter-canny-sdxl-1.0

 

Image-to-Image •  Updated Sep 7, 2023  •  2.43k  •  54](/TencentARC/t2i-adapter-canny-sdxl-1.0)

[![](https://cdn-avatars.huggingface.co/v1/production/uploads/1625552871844-60e272ca6c78a8c122b12127.png)

#### TencentARC/t2i-adapter-depth-midas-sdxl-1.0

 

Image-to-Image •  Updated Sep 7, 2023  •  1.49k  •  35](/TencentARC/t2i-adapter-depth-midas-sdxl-1.0)

[![](https://cdn-avatars.huggingface.co/v1/production/uploads/1625552871844-60e272ca6c78a8c122b12127.png)

#### TencentARC/t2i-adapter-depth-zoe-sdxl-1.0

 

Image-to-Image •  Updated Sep 8, 2023  •  2.11k  •  29](/TencentARC/t2i-adapter-depth-zoe-sdxl-1.0)

[![](https://cdn-avatars.huggingface.co/v1/production/uploads/1625552871844-60e272ca6c78a8c122b12127.png)

#### TencentARC/t2i-adapter-lineart-sdxl-1.0

 

Image-to-Image •  Updated Sep 7, 2023  •  2.9k  •  80](/TencentARC/t2i-adapter-lineart-sdxl-1.0)

[![](https://cdn-avatars.huggingface.co/v1/production/uploads/1625552871844-60e272ca6c78a8c122b12127.png)

#### TencentARC/t2i-adapter-openpose-sdxl-1.0

 

Image-to-Image •  Updated Sep 7, 2023  •  2.09k  •  52](/TencentARC/t2i-adapter-openpose-sdxl-1.0)

[![](https://cdn-avatars.huggingface.co/v1/production/uploads/1625552871844-60e272ca6c78a8c122b12127.png)

#### TencentARC/t2i-adapter-sketch-sdxl-1.0

 

Image-to-Image •  Updated Sep 8, 2023  •  3.14k  •  77](/TencentARC/t2i-adapter-sketch-sdxl-1.0)

[![](https://cdn-avatars.huggingface.co/v1/production/uploads/1668178606778-602e6dee60e3dd96631c906e.jpeg)

#### diffusers/controlnet-canny-sdxl-1.0

 

Text-to-Image •  Updated Sep 19, 2023  •  27.5k  •  531](/diffusers/controlnet-canny-sdxl-1.0)

[![](https://cdn-avatars.huggingface.co/v1/production/uploads/643feeb67bc3fbde1385cc25/7vmYr2XwVcPtkLzac_jxQ.png)

#### stabilityai/control-lora

 

Text-to-Image •  Updated Aug 19, 2023    •  971](/stabilityai/control-lora)

  

## Spaces mentioned in this article 2

[Runtime error

Featured

 

290

 

#### T2I-Adapter-SDXL

🚀

290

Generate images from text prompts](/spaces/TencentARC/T2I-Adapter-SDXL)

[Runtime error

 

Agents

Featured

 

242

 

#### T2I Adapter SDXL Sketch

🚀

242](/spaces/TencentARC/T2I-Adapter-SDXL-Sketch)

 

## Papers mentioned in this article 3

[#### Adding Conditional Control to Text-to-Image Diffusion Models

Paper • 2302.05543 • Published Feb 10, 2023 •  58](/papers/2302.05543)

[#### T2I-Adapter: Learning Adapters to Dig out More Controllable Ability for Text-to-Image Diffusion Models

Paper • 2302.08453 • Published Feb 16, 2023 •  12](/papers/2302.08453)

[#### SDXL: Improving Latent Diffusion Models for High-Resolution Image Synthesis

Paper • 2307.01952 • Published Jul 4, 2023 •  92](/papers/2307.01952)

 

More Articles from our Blog

[![](/blog/assets/dreambooth_lora_sdxl/thumbnail.png)

guidecollaborationdiffusers

## LoRA training scripts of the world, unite!

* ![](https://cdn-avatars.huggingface.co/v1/production/uploads/638f308fc4444c6ca870b60a/Q11NK-8-JbiilJ-vk2LAR.png)
* ![](https://cdn-avatars.huggingface.co/v1/production/uploads/1649143001781-624bebf604abc7ebb01789af.jpeg)

linoyts, et. al.

79

 January 2, 2024

linoyts, multimodalart](/blog/sdxl_lora_advanced_script)

[![](/blog/assets/modular-diffusers/thumbnail.png)

open-sourcediffusersgenerative

## Introducing Modular Diffusers - Composable Building Blocks for Diffusion Pipelines

* ![](https://cdn-avatars.huggingface.co/v1/production/uploads/1677857909367-624ef9ba9d608e459387b34e.jpeg)
* ![](https://cdn-avatars.huggingface.co/v1/production/uploads/63df091910678851bb0cd0e0/FUXFt0C-rUFSppIAu5ZDN.png)
* ![](https://cdn-avatars.huggingface.co/v1/production/uploads/1630334896986-6126e46848005fa9ca5c578c.jpeg)
* ![](https://cdn-avatars.huggingface.co/v1/production/uploads/1649681653581-5f7fbd813e94f16a85448745.jpeg)

YiYiXu, et. al.

51

 March 5, 2026

YiYiXu, OzzyGT, et. al.](/blog/modular-diffusers)

 

### Community

EditPreview

Upload images, audio, and videos by dragging in the text input, pasting, or clicking here.

Tap or paste here to upload images

Comment

· [Sign up](/join?next=%2Fblog%2Ft2i-sdxl-adapters) or [log in](/login?next=%2Fblog%2Ft2i-sdxl-adapters) to comment

[Upvote

9](/login?next=%2Fblog%2Ft2i-sdxl-adapters)  

* [![](https://cdn-avatars.huggingface.co/v1/production/uploads/603bdba23249b99991dbcbc4/cxCnN1H-RXOhojHY3Wcxo.jpeg)](/tolgacangoz "tolgacangoz")
* [![](https://cdn-avatars.huggingface.co/v1/production/uploads/60e272ca6c78a8c122b12127/xldEGBzGrU-bX6IwAw0Ie.jpeg)](/Xintao "Xintao")
* [![](https://cdn-avatars.huggingface.co/v1/production/uploads/6266513d539521e602b5dc3a/7ZU_GyMBzrFHcHDoAkQlp.png)](/ameerazam08 "ameerazam08")
* [![](/avatars/de9792ea25076aec98712d4acf4a2e86.svg)](/jakobsal "jakobsal")
* [![](https://cdn-avatars.huggingface.co/v1/production/uploads/654bcb6fae75d15300d48205/T4L1RZUgCZgdik4ZhEWCq.jpeg)](/Steveeeeeeen "Steveeeeeeen")
* [![](/avatars/71764067260c9de7d7bf53795020a7b5.svg)](/Devin008 "Devin008")
* [![](https://cdn-avatars.huggingface.co/v1/production/uploads/6640bbd0220cfa8cbfdce080/wiAHUu5ewawyipNs0YFBR.png)](/John6666 "John6666")
* [![](/avatars/49041af5490097ba5a79a3882ef61ecf.svg)](/zgh36 "zgh36")
* [![](/avatars/2516c0f4c77ab840f6e8f5f2a3f6f7fa.svg)](/liawdaw "liawdaw")

## Models mentioned in this article 8

[![](https://cdn-avatars.huggingface.co/v1/production/uploads/1625552871844-60e272ca6c78a8c122b12127.png)

#### TencentARC/t2i-adapter-canny-sdxl-1.0

 

Image-to-Image •  Updated Sep 7, 2023  •  2.43k  •  54](/TencentARC/t2i-adapter-canny-sdxl-1.0)

[![](https://cdn-avatars.huggingface.co/v1/production/uploads/1625552871844-60e272ca6c78a8c122b12127.png)

#### TencentARC/t2i-adapter-depth-midas-sdxl-1.0

 

Image-to-Image •  Updated Sep 7, 2023  •  1.49k  •  35](/TencentARC/t2i-adapter-depth-midas-sdxl-1.0)

[![](https://cdn-avatars.huggingface.co/v1/production/uploads/1625552871844-60e272ca6c78a8c122b12127.png)

#### TencentARC/t2i-adapter-depth-zoe-sdxl-1.0

 

Image-to-Image •  Updated Sep 8, 2023  •  2.11k  •  29](/TencentARC/t2i-adapter-depth-zoe-sdxl-1.0)

[![](https://cdn-avatars.huggingface.co/v1/production/uploads/1625552871844-60e272ca6c78a8c122b12127.png)

#### TencentARC/t2i-adapter-lineart-sdxl-1.0

 

Image-to-Image •  Updated Sep 7, 2023  •  2.9k  •  80](/TencentARC/t2i-adapter-lineart-sdxl-1.0)

[![](https://cdn-avatars.huggingface.co/v1/production/uploads/1625552871844-60e272ca6c78a8c122b12127.png)

#### TencentARC/t2i-adapter-openpose-sdxl-1.0

 

Image-to-Image •  Updated Sep 7, 2023  •  2.09k  •  52](/TencentARC/t2i-adapter-openpose-sdxl-1.0)

[![](https://cdn-avatars.huggingface.co/v1/production/uploads/1625552871844-60e272ca6c78a8c122b12127.png)

#### TencentARC/t2i-adapter-sketch-sdxl-1.0

 

Image-to-Image •  Updated Sep 8, 2023  •  3.14k  •  77](/TencentARC/t2i-adapter-sketch-sdxl-1.0)

[![](https://cdn-avatars.huggingface.co/v1/production/uploads/1668178606778-602e6dee60e3dd96631c906e.jpeg)

#### diffusers/controlnet-canny-sdxl-1.0

 

Text-to-Image •  Updated Sep 19, 2023  •  27.5k  •  531](/diffusers/controlnet-canny-sdxl-1.0)

[![](https://cdn-avatars.huggingface.co/v1/production/uploads/643feeb67bc3fbde1385cc25/7vmYr2XwVcPtkLzac_jxQ.png)

#### stabilityai/control-lora

 

Text-to-Image •  Updated Aug 19, 2023    •  971](/stabilityai/control-lora)

  

## Spaces mentioned in this article 2

[Runtime error

Featured

 

290

 

#### T2I-Adapter-SDXL

🚀

290

Generate images from text prompts](/spaces/TencentARC/T2I-Adapter-SDXL)

[Runtime error

 

Agents

Featured

 

242

 

#### T2I Adapter SDXL Sketch

🚀

242](/spaces/TencentARC/T2I-Adapter-SDXL-Sketch)

 

## Papers mentioned in this article 3

[#### Adding Conditional Control to Text-to-Image Diffusion Models

Paper • 2302.05543 • Published Feb 10, 2023 •  58](/papers/2302.05543)

[#### T2I-Adapter: Learning Adapters to Dig out More Controllable Ability for Text-to-Image Diffusion Models

Paper • 2302.08453 • Published Feb 16, 2023 •  12](/papers/2302.08453)

[#### SDXL: Improving Latent Diffusion Models for High-Resolution Image Synthesis

Paper • 2307.01952 • Published Jul 4, 2023 •  92](/papers/2307.01952)

 

System theme

Company

[TOS](/terms-of-service) [Privacy](/privacy) [About](/huggingface) [Careers](https://apply.workable.com/huggingface/) 

Website

[Models](/models) [Datasets](/datasets) [Spaces](/spaces) [Pricing](/pricing) [Docs](/docs)
