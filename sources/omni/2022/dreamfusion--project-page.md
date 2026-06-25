# DreamFusion: Text-to-3D using 2D Diffusion
Source: https://dreamfusion3d.github.io/
DreamFusion: Text-to-3D using 2D Diffusion



[![

](https://dreamfusion-cdn.ajayj.com/sept28/banner_1x6_customhue_A.jpg)](https://dreamfusion-cdn.ajayj.com/sept28/banner_1x6_customhue_A.mp4)

# **DreamFusion**: Text-to-3D using 2D Diffusion

##### [Ben Poole](https://cs.stanford.edu/~poole/)

###### Google Research

##### [Ajay Jain](https://ajayj.com)

###### UC Berkeley

##### [Jonathan T. Barron](https://jonbarron.info/)

###### Google Research

##### [Ben Mildenhall](https://bmild.github.io/)

###### Google Research

[Paper](https://arxiv.org/abs/2209.14988)
[Project](#)
[Gallery](/gallery.html)

---

## Abstract

Recent breakthroughs in text-to-image synthesis have been driven by diffusion models trained on billions of image-text pairs. Adapting this approach to 3D synthesis would require large-scale datasets of labeled 3D assets and efficient architectures for denoising 3D data, neither of which currently exist. In this work, we circumvent these limitations by using a pretrained 2D text-to-image diffusion model to perform text-to-3D synthesis. We introduce a loss based on probability density distillation that enables the use of a 2D diffusion model as a prior for optimization of a parametric image generator. Using this loss in a DeepDream-like procedure, we optimize a randomly-initialized 3D model (a Neural Radiance Field, or NeRF) via gradient descent such that its 2D renderings from random angles achieve a low loss. The resulting 3D model of the given text can be viewed from any angle, relit by arbitrary illumination, or composited into any 3D environment. Our approach requires no 3D training data and no modifications to the image diffusion model, demonstrating the effectiveness of pretrained image diffusion models as priors.

[![

](https://dreamfusion-cdn.ajayj.com/sept28/wipe_opposite_6x4_smoothstep.jpg)](https://dreamfusion-cdn.ajayj.com/sept28/wipe_opposite_6x4_smoothstep.mp4)

![

](https://dreamfusion-cdn.ajayj.com/sept28/shaded_3x3_smoothstep.jpg)

###### Given a caption, DreamFusion generates relightable 3D objects with high-fidelity appearance, depth, and normals. Objects are represented as a Neural Radiance Field and leverage a pretrained text-to-image diffusion prior such as Imagen.

---

## Generate 3D from text yourself!

a DSLR photo of a squirrelan intricate wooden carving of a squirrela highly detailed metal sculpture of a squirrel

[...]wearing a kimonowearing a medieval suit of armorwearing a purple hoodiewearing an elegant ballgown

[...]reading a bookriding a motorcycleplaying the saxophonechopping vegetablessitting at a pottery wheel shaping a clay bowlriding a skateboardwielding a katanaeating a hamburgerdancing

[
](https://dreamfusion-cdn.ajayj.com/journey_sept28/cropped/full_continuous/a_DSLR_photo_of_a_squirrel___rgbdn_hq_15000.mp4)

---

## Example generated objects

DreamFusion generates objects and scenes from diverse captions. [Search through hundreds of generated assets in our full gallery.](/gallery.html)

[Search assets](/gallery.html)

[](https://dreamfusion-cdn.ajayj.com/gallery_sept28/crf20/a_wide_angle_DSLR_photo_of_a_colorful_rooster.mp4)

###### [...] a colorful rooster

[](https://dreamfusion-cdn.ajayj.com/gallery_sept28/crf20/a_metal_sculpture_of_a_lion's_head,_highly_detailed.mp4)

###### a metal sculpture of a lion's head, highly detailed

[](https://dreamfusion-cdn.ajayj.com/gallery_sept28/crf20/a_DSLR_photo_of_a_pug_wearing_a_bee_costume.mp4)

###### [...] a pug wearing a bee costume

---

## Composing objects into a scene

[![

](https://dreamfusion-cdn.ajayj.com/carouselx24_128tall.jpg)](https://dreamfusion-cdn.ajayj.com/carouselx24_128tall.mp4)

---

## Mesh exports

Our generated NeRF models can be exported to meshes using the marching cubes algorithm for easy integration into 3D renderers or modeling software.

Load 3D model

[...] frog wearing a sweater

Load 3D model

[...] eggshell broken in two with an adorable chick standing next to it

Load 3D model

[...] ghost eating a hamburger

Load 3D model

a pig wearing a backpack

Load 3D model

a bald eagle carved out of wood

Load 3D model

a crab, low poly

Load 3D model

a lemur taking notes in a journal

Load 3D model

a plush toy of a corgi nurse

---

## How does DreamFusion work?

Given a caption, DreamFusion uses a text-to-image generative model called Imagen to optimize a 3D scene. We propose **Score Distillation Sampling (SDS)**, a way to generate samples from a diffusion model by optimizing a loss function. SDS allows us to optimize samples in an arbitrary parameter space, such as a 3D space, as long as we can map back to images differentiably. We use a 3D scene parameterization similar to Neural Radiance Fields, or NeRFs, to define this differentiable mapping. SDS alone produces reasonable scene appearance, but DreamFusion adds additional regularizers and optimization strategies to improve geometry. The resulting trained NeRFs are coherent, with high-quality normals, surface geometry and depth, and are relightable with a Lambertian shading model.

![

](https://dreamfusion-cdn.ajayj.com/dreamfusion_overview.jpg)

---

## Citation

`@article{poole2022dreamfusion,  
  author = {Poole, Ben and Jain, Ajay and Barron, Jonathan T. and Mildenhall, Ben},  
  title = {DreamFusion: Text-to-3D using 2D Diffusion},  
  journal = {arXiv},  
  year = {2022},  
}`
