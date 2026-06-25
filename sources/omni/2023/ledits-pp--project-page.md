# LEDITS++: Limitless Image Editing using Text-to-Image Models
Source: https://leditsplusplus-project.static.hf.space/index.html
 LEDITS++: Limitless Image Editing using Text-to-Image Models 




# LEDITS++: Limitless Image Editing using Text-to-Image Models

[Manuel Brack](https://scholar.google.com/citations?user=kJ9Abf8AAAAJ&hl=en)¹²⁺,

[Felix Friedrich](https://www.ml.informatik.tu-darmstadt.de/people/ffriedrich/index.html)²³⁺,

[Katharina Kornmeier](https://huggingface.co/KatharinaK)²⁺,

[Linoy Tsaban](https://twitter.com/linoy_tsaban)⁴,

[Patrick Schramowski](https://scholar.google.com/citations?user=GD481RkAAAAJ&hl=de)¹²³⁶,

[Kristian Kersting](https://ml-research.github.io/people/kkersting/)¹²³⁵,

[Apolinário Passos](https://twitter.com/multimodalart)⁴

¹ German Research Center for Artificial Intelligence (DFKI),
² Computer Science Department, TU Darmstadt,
³ Hessian.AI,
⁴ Hugging Face 🤗,
⁵ Centre for Cognitive Science, TU Darmstadt,
⁶ LAION,
⁺ equal contribution

[arXiv](https://arxiv.org/abs/2311.16711)


[🤗 Demo](https://huggingface.co/spaces/editing-images/ledtisplusplus)


[Code](https://github.com/huggingface/diffusers/tree/main/src/diffusers/pipelines/ledits_pp)

[

](static/videos/faces.mp4)

##

### Awards

We were rewarded with a Meta Quest 3 for being second place at the [GenAI Media Generation Challenge Workshop @ CVPR](https://gamgc.github.io/)!

## Abstract

Text-to-image diffusion models have recently received a lot of interest for their
astonishing ability to produce high-fidelity images from text only. Subsequent
research efforts are aiming to exploit the capabilities of these models and leverage
them for intuitive, textual image editing. However, existing methods often require
time-consuming fine-tuning and lack native support for performing multiple edits
simultaneously. To address these issues, we introduce LEDITS++ , an efficient yet
versatile technique for image editing using text-to-image models. LEDITS++ re-
quires no tuning nor optimization, runs in a few diffusion steps, natively supports
multiple simultaneous edits, inherently limits changes to relevant image regions,
and is architecture agnostic.

![ledits++ teaser](static/images/teaser.png)

## LEDITS++: Efficient and Versatile Textual Image Editing

To ease textual image editing, we present LEDITS++, a novel method for efficient and versatile image
editing using text-to-image diffusion models. Firstly, LEDITS++ sets itself apart as a parameter-free
solution requiring no fine-tuning nor any optimization. We derive characteristics of an edit-friendly
noise space with a perfect input reconstruction, which were previously proposed for the DDPM
sampling scheme, for a significantly faster multistep stochastic differential-equation (SDE)
solver. This novel invertibility of the DPM-solver++ facilitates editing with LEDITS++ in as
little as 20 total diffusion steps for inversion and inference combined.
Moreover, LEDITS++ places a strong emphasis on semantic grounding to enhance the visual and
contextual coherence of the edits. This ensures that changes are limited to the relevant regions in the
image, preserving the original image’s fidelity as much as possible. LEDITS++ also provides users
with the flexibility to combine multiple edits seamlessly, opening up new creative possibilities for
intricate image manipulations. Finally, the approach is architecture-agnostic and compatible with any
diffusion model, whether latent or pixel-based.

![examples](static/images/variations.png)

![examples](static/images/smile_progression.png)

![examples](static/images/qualitative_car.png)

## Methodology

The methodology of LEDITS++ can be broken down into three components: (1) efficient image
inversion, (2) versatile textual editing, and (3) semantic grounding of image changes.

## Component 1: Perfect Inversion

Utilizing T2I models for editing real images is usually done by inverting the sampling
process to identify a noisy xT that will be denoised to the input image x0.
We draw characteristics from [edit friendly DDPM inversion](https://inbarhub.github.io/DDPM_inversion/) and propose
an efficient
inversion method that greatly reduces the required number
of steps while maintaining no reconstruction error.
DDPM can be viewed as a first-order
SDE solver when formulating the reverse diffusion process as an SDE. This
SDE can be solved more efficiently—in fewer steps—
using a higher-order differential equation solver, hence we derive a new, faster
technique - **dpm-solver++ Inversion**.

![](static/images/inversion.png)

## Component 2: Textual Editing

After creating our re-construction sequence, we can edit the image by manipulating
the noise estimate εθ based on a set of edit instructions. We devise a dedicated
guidance term for each concept based on conditioned and unconditioned estimate. We
define LEDITS++ guidance such that it both reflects the direction of the edit (if we
want
to push away from/towards the edit concept) and maximizes fine-grained control over
the effect of the desired edit.

![](static/images/textual_editing.png)

## Component 3: Semantic Grounding

In our defined LEDITS++ guidance, we include a masking term composed of the
intersection between the mask generated from
the U-Net’s cross-attention layers and a mask derived from
the noise estimate - yielding a mask both focused on relevant image
regions and of fine granularity.
We empirically demonstrate that these maps can also capture regions
of an image relevant to an editing concept that is not already present.
Specifically for multiple edits, calculating a
dedicated mask for each edit prompt ensures that the corresponding
guidance terms remain largely isolated, limiting
interference between them.

![](static/images/semantic_grounding.png)

## Properties of LEDITS++

**Efficiency.**
As a parameter-free approach, LEDITS++ does not require any fine-tuning or optimization.
In addition we use a recent, fast scheduler altogether making LEDITS++ six times faster than
recent DDPM inversion.

**Versatility.**
LEDITS++ facilitates fine-grained edits and holistic changes such as style transfer.
To the best of our knowledge, LEDITS++ is the only diffusion-based image editing method
inherently supporting multiple edits in isolation.

**Precision.**
LEDITS++’s methodology keeps edits concise and avoids unnecessary deviations
from the input image through prefect inversion and use of implict masking
(specifically important for editing multiple concepts simultaneously).

[

](static/videos/objects_styles.mp4)

## Interactive Demo

Loading...
















## BibTeX

```
@inproceedings{brack2024ledits,
          year = { 2024 }, 
          booktitle = { Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) }, 
          author = { Manuel Brack and Felix Friedrich and Katharina Kornmeier and Linoy Tsaban and Patrick Schramowski and Kristian Kersting and Apolinaros Passos }, 
          title = { LEDITS++: Limitless Image Editing using Text-to-Image Models }
}
```

This website is licensed under a [Creative
Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).

This page was built using the source code of:
[nerfies.github.io](https://github.com/nerfies/nerfies.github.io)
