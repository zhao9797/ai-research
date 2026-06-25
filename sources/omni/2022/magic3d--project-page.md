# Magic3D: High-Resolution Text-to-3D Content Creation — Cosmos Lab
Source: https://research.nvidia.com/labs/cosmos-lab/magic3d/
Magic3D: High-Resolution Text-to-3D Content Creation — Cosmos Lab





[![NVIDIA](https://research.nvidia.com/labs/cosmos-lab/assets/nvidia-logo-horiz-rgb-wht-no-reg-for-screen.png)](https://www.nvidia.com)
[Cosmos Lab](https://research.nvidia.com/labs/cosmos-lab/)



[Products](https://research.nvidia.com/labs/cosmos-lab/)
[Press](https://research.nvidia.com/labs/cosmos-lab/)
[Publications](https://research.nvidia.com/labs/cosmos-lab/)




# Magic3D: High-Resolution Text-to-3D Content Creation

Chen-Hsuan Lin\* · Jun Gao\* · Luming Tang\* · Towaki Takikawa\* · Xiaohui Zeng\* · Xun Huang · Karsten Kreis · Sanja Fidler · Ming-Yu Liu · Tsung-Yi Lin

CVPR 2023Highlight

[Paper](https://arxiv.org/abs/2211.10440)[Video](https://research.nvidia.com/labs/dir/magic3d/assets/video.mp4)

## Abstract

(best viewed with Google Chrome on a desktop/laptop)

DreamFusion has recently demonstrated the utility of a pre-trained
text-to-image diffusion model to optimize Neural Radiance Fields (NeRF),
achieving remarkable text-to-3D synthesis results. However, the method
has two inherent limitations: (a) extremely slow optimization of NeRF
and (b) low-resolution image space supervision on NeRF, leading to
low-quality 3D models with a long processing time. In this paper, we
address these limitations by utilizing a two-stage optimization
framework. First, we obtain a coarse model using a low-resolution
diffusion prior and accelerate with a sparse 3D hash grid structure.
Using the coarse representation as the initialization, we further
optimize a textured 3D mesh model with an efficient differentiable
renderer interacting with a high-resolution latent diffusion model. Our
method, dubbed Magic3D, can create high quality 3D mesh models in 40
minutes, which is 2× faster than DreamFusion (reportedly taking 1.5
hours on average), while also achieving higher resolution. User studies
show 61.7% raters to prefer our approach over DreamFusion. Together with
the image-conditioned generation capabilities, we provide users with new
ways to control 3D synthesis, opening up new avenues to various creative
applications.

## Video

[

](https://research.nvidia.com/labs/cosmos-lab/magic3d/assets/video.mp4)

## High-Resolution 3D Meshes

Magic3D can create high-quality 3D textured mesh models from input
text prompts. It utilizes a coarse-to-fine strategy leveraging both
low- and high-resolution diffusion priors for learning the 3D
representation of the target content. Magic3D synthesizes 3D content
with 8× higher-resolution supervision than
[DreamFusion](http://dreamfusion3d.github.io/) while also
being 2× faster.

**[...]** indicates helper captions added to improve quality, e.g. "A DSLR photo of".

[](assets/main/hstack-320x320/005.mp4)

Reveal 3D mesh!

[Download 3D mesh!](assets/selected_glb_files/005.glb)

A beautiful dress made out of garbage bags, on a mannequin. Studio lighting, high quality, high resolution.



[](assets/main/hstack-320x320/009.mp4)

Reveal 3D mesh!

[Download 3D mesh!](assets/selected_glb_files/009.glb)

A blue poison-dart frog sitting on a water lily.



[](assets/main/hstack-320x320/048.mp4)

Reveal 3D mesh!

[Download 3D mesh!](assets/selected_glb_files/048.glb)

[...] a car made out of sushi.



[](assets/main/hstack-320x320/034.mp4)

Reveal 3D mesh!

[Download 3D mesh!](assets/selected_glb_files/034.glb)

[...] a bagel filled with cream cheese and lox.



[](assets/main/hstack-320x320/115.mp4)

Reveal 3D mesh!

[Download 3D mesh!](assets/selected_glb_files/115.glb)

[...] an ice cream sundae.



[](assets/main/hstack-320x320/130.mp4)

Reveal 3D mesh!

[Download 3D mesh!](assets/selected_glb_files/130.glb)

[...] a peacock on a surfboard.



[](assets/main/hstack-320x320/137.mp4)

Reveal 3D mesh!

[Download 3D mesh!](assets/selected_glb_files/137.glb)

[...] a plate piled high with chocolate chip cookies.



[](assets/main/hstack-320x320/210.mp4)

Reveal 3D mesh!

[Download 3D mesh!](assets/selected_glb_files/210.glb)

[...] Neuschwanstein Castle, aerial view.



[](assets/main/hstack-320x320/211.mp4)

Reveal 3D mesh!

[Download 3D mesh!](assets/selected_glb_files/211.glb)

[...] the Imperial State Crown of England.



[](assets/main/hstack-320x320/212.mp4)

Reveal 3D mesh!

[Download 3D mesh!](assets/selected_glb_files/212.glb)

[...] the leaning tower of Pisa, aerial view.



[](assets/main/hstack-320x320/276.mp4)

Reveal 3D mesh!

[Download 3D mesh!](assets/selected_glb_files/276.glb)

A ripe strawberry.



[](assets/main/hstack-320x320/279.mp4)

Reveal 3D mesh!

[Download 3D mesh!](assets/selected_glb_files/279.glb)

A silver platter piled high with fruits.



[](assets/main/hstack-320x320/387.mp4)

Reveal 3D mesh!

[Download 3D mesh!](assets/selected_glb_files/387.glb)

[...] a silver candelabra sitting on a red velvet tablecloth, only one candle is lit.



[](assets/main/hstack-320x320/400.mp4)

Reveal 3D mesh!

[Download 3D mesh!](assets/selected_glb_files/400.glb)

[...] Sydney opera house, aerial view.



[](assets/main/hstack-320x320/405.mp4)

Reveal 3D mesh!

[Download 3D mesh!](assets/selected_glb_files/405.glb)

Michelangelo style statue of an astronaut.

## Editing Capabilities

### Prompt-based Editing

Given a coarse model generated with a base text prompt, we can modify
parts of the text in the prompt, and then fine-tune the NeRF and 3D
mesh models to obtain an edited high-resolution 3D mesh.

![](images/arrow.png)

[](assets/prompt-based/squirrel-256x256-a/bunny-scooter_hstack.mp4)

[](assets/prompt-based/squirrel-256x256-a/fairy-bike_hstack.mp4)

[](assets/prompt-based/squirrel-256x256-a/steampunk_squirrel-horse_hstack.mp4)

A
squirrel wearing a leather jacket
riding a motorcycle.

A bunny riding a
scooter.

A fairy riding a
bike.

A steampunk squirrel riding a
horse.

![](images/arrow.png)

[](assets/prompt-based/bunny-256x256-a/lego_bunny-a_stack_of_books_hstack.mp4)

[](assets/prompt-based/bunny-256x256-a/metal_bunny-a_stack_of_broccoli_hstack.mp4)

[](assets/prompt-based/bunny-256x256-a/metal_bunny-_hstack.mp4)

A baby bunny sitting on top of a stack
of pancakes.

A lego bunny sitting on top of a stack
of books.

A metal bunny sitting on top of a
stack of broccoli.

A metal bunny sitting on top of a
stack of chocolate cookies.

### Other Capabilities

Given input images for a subject instance, we can fine-tune the
diffusion models with
[DreamBooth](https://dreambooth.github.io/) and optimize
the 3D models with the given prompts. The identity of the subject can
be well-preserved in the 3D models.

![DreamBooth result 1](assets/dreambooth/static1.png)
![DreamBooth result 2](assets/dreambooth/static2.png)

We can also condition the diffusion model (eDiff-I) on an input image
to transfer its style to the output 3D model.

![Style transfer result](assets/style_transfer-a.png)

## Approach

We utilize a two-stage coarse-to-fine optimization framework for fast
and high-quality text-to-3D content creation. In the first stage, we
obtain a coarse model using a low-resolution diffusion prior and
accelerate this with a hash grid and sparse acceleration structure. In
the second stage, we use a textured mesh model initialized from the
coarse neural representation, allowing optimization with an efficient
differentiable renderer interacting with a high-resolution latent
diffusion model.

![Magic3D approach diagram](assets/diagram.jpg)

## Presentation

## Citation

```
@inproceedings{lin2023magic3d,
  title={Magic3D: High-Resolution Text-to-3D Content Creation},
  author={Lin, Chen-Hsuan and Gao, Jun and Tang, Luming and Takikawa, Towaki and Zeng, Xiaohui and Huang, Xun and Kreis, Karsten and Fidler, Sanja and Liu, Ming-Yu and Lin, Tsung-Yi},
  booktitle={IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  year={2023}
}
```

Copy

Top

![NVIDIA](https://research.nvidia.com/labs/cosmos-lab/assets/nvidia-logo-horiz-rgb-wht-no-reg-for-screen.png)

* [Privacy Policy](https://www.nvidia.com/en-us/about-nvidia/privacy-policy/)
* [Your Privacy Choices](https://www.nvidia.com/en-us/about-nvidia/privacy-center/)
* [Terms of Service](https://www.nvidia.com/en-us/about-nvidia/terms-of-service/)
* [Accessibility](https://www.nvidia.com/en-us/about-nvidia/accessibility/)
* [Corporate Policies](https://www.nvidia.com/en-us/about-nvidia/company-policies/)
* [Product Security](https://www.nvidia.com/en-us/product-security/)
* [Contact](https://www.nvidia.com/en-us/contact/)

Copyright © 2026 NVIDIA Corporation
