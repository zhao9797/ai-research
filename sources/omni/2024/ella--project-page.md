# ELLA: Equip Diffusion Models with LLM for Enhanced Semantic Alignment
Source: https://ella-diffusion.github.io/
ELLA: Equip Diffusion Models with LLM for Enhanced Semantic Alignment



# ELLA: Equip Diffusion Models with LLM for Enhanced Semantic Alignment

[Xiwei Hu\*](https://openreview.net/profile?id=~Xiwei_Hu1),

[Rui Wang\*](https://wrong.wang/),

[Yixiao Fang\*](https://openreview.net/profile?id=~Yixiao_Fang1),

[Bin Fu\*](https://openreview.net/profile?id=~BIN_FU2),

[Pei Cheng](https://openreview.net/profile?id=~Pei_Cheng1),

[Gang Yu✦](https://www.skicyyu.org/),

Tencent

(\* Equal contributions, ✦ Corresponding Author)

[PDF](https://arxiv.org/pdf/2403.05135)

[Arxiv](https://arxiv.org/abs/2403.05135)


[Code](https://github.com/TencentQQGYLab/ELLA)

[Benchmark](https://github.com/TencentQQGYLab/ELLA)

![teaser](static/images/teaser_3img.png)
![teaser](static/images/teaser1_raccoon.png)

## Comparison to SDXL and DALL-E 3. The prompts originate from PartiPrompts (colored text denotes critical entities or attributes).

## Abstract

Diffusion models have demonstrated remarkable performance in the domain of text-to-image generation.
However, the majority of these models still employ CLIP as their text encoder, which constrains their
ability to comprehend dense prompts, which encompass multiple objects, detailed attributes, complex
relationships, long-text alignment, etc.
In this paper, We introduce an **E**fficient **L**arge **L**anguage Model **A**dapter, termed
**ELLA**, which equips text-to-image diffusion models with powerful Large Language
Models (LLM) to enhance text alignment
*without training of either U-Net or LLM*.
To seamlessly bridge two pre-trained models, we investigate a range of semantic alignment connector
designs and propose a novel module, the Timestep-Aware Semantic Connector (TSC), which dynamically
extracts timestep-dependent conditions from LLM.
Our approach adapts semantic features at different stages of the denoising process, assisting diffusion
models in interpreting lengthy and intricate prompts over sampling timesteps.
Additionally, ELLA can be readily incorporated with community models and
tools to improve their prompt-following capabilities.
To assess text-to-image models in dense prompt following, we introduce Dense Prompt Graph Benchmark
(DPG-Bench), a challenging benchmark consisting of 1K dense prompts.
Extensive experiments demonstrate the superiority of ELLA in dense prompt following compared to
state-of-the-art methods,
particularly in multiple object compositions involving diverse attributes and relationships.

## Method

We propose a novel lightweight approach ELLA to equip existing CLIP-based diffusion models with powerful
LLM.
Without training of U-Net and LLM, ELLA improves prompt-following abilities and enables long dense text
comprehension of text-to-image models.

We design a Time-Aware Semantic Connector to extract timestep-dependent conditions from the pre-trained
LLM at various denoising stages. Our proposed TSC dynamically adapts semantics features over sampling time
steps, which effectively conditions the frozen U-Net at distinct semantic levels.

  

![arch](static/images/ella_arch1.png)


The overview of ELLA.

## Results

### Comparison

![comparison](static/images/comparison.jpg)


The comparison between ELLA, SDXL, PixArt-alpha, Playground v2 and
DALL-E 3. The left four columns only contain 1 or 2 entities, but the right four correspond to dense
prompts with more than 2 entities. All prompts originate from PartiPrompts.


![exp_pic2](static/images/exp_pic2.jpg)


The comparison between SDXL, ELLA, and DALL-E 3 reveals their performance
across varying levels of prompt complexity. Prompts range from simple to intricate from top to bottom.
The results demonstrate that our model is capable of following both simple and complex prompts and
generating fine-grained detail.

### Compatibility with Downstream Tools.

Once trained, ELLA can seamlessly integrate community models and downstream tools such as
LoRA and ControlNet, improving their text-image alignment.

![Compatibility](static/images/Compatibility.jpg)


Qualitative results about ELLA(SD1.5) with personalized models. We selected representative
personalized models from CivitAI, equipping them with ELLA to improve
their prompt following ability.



This website use template from [Nerfies](https://github.com/nerfies/nerfies.github.io)

This website is licensed under a [Creative
Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).

This means you are free to borrow the [source
code](https://github.com/ella-diffusion/ella-diffusion.github.io) of this website,
we just ask that you link back to this page in the footer.
Please remember to remove the analytics code included in the header of the website which
you do not want on your website.
