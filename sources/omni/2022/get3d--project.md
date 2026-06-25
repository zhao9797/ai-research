# GET3D: A Generative Model of High Quality 3D Textured Shapes Learned from Images
Source: https://research.nvidia.com/labs/toronto-ai/GET3D/
[![](assets/nvidia.svg)](https://www.nvidia.com/)
[**Toronto AI Lab**](https://nv-tlabs.github.io/)


GET3D: A Generative Model of High Quality 3D Textured Shapes Learned from Images



# GET3D: A Generative Model of High Quality 3D Textured Shapes Learned from Images

[Jun Gao](http://www.cs.toronto.edu/~jungao/)1,2,3

[Tianchang Shen](http://www.cs.toronto.edu/~shenti11/)1,2,3

[Zian Wang](http://www.cs.toronto.edu/~zianwang/)1,2,3

[Wenzheng Chen](http://www.cs.toronto.edu/~wenzheng/)1,2,3

[Kangxue Yin](https://kangxue.org/)1

[Daiqing Li](https://scholar.google.ca/citations?user=8q2ISMIAAAAJ&hl=en)1

[Or Litany](https://orlitany.github.io/)1

[Zan Gojcic](https://zgojcic.github.io/)1

[Sanja Fidler](https://www.cs.toronto.edu/~fidler/)1,2,3

1NVIDIA

2University of Toronto

3Vector Institute

**NeurIPS 2022**

[description 
Paper](assets/paper.pdf)
[description 
BibTeX](assets/bib.txt)
[description 
Code](https://github.com/nv-tlabs/GET3D)

[![](assets/get3d_model.png)](assets/get3d_model.png)

We generate a 3D SDF and a texture field via two latent codes. We utilize DMTet to extract a 3D surface mesh from the SDF, and query the texture field at surface points to get colors. We train with adversarial losses defined on 2D images. In particular, we use a rasterization-based differentiable renderer to obtain RGB images and silhouettes. We utilize two 2D discriminators, each on RGB image, and silhouette, respectively, to classify whether the inputs are real or fake. The whole model is end-to-end trainable.

  

[

Your browser does not support the video tag.
](assets/teaser-rotate.mp4)

GET3D is able to generate diverse shapes with arbitrary topology, high-quality geometry and texture.

## Abstract

---

As several industries are moving towards modeling massive 3D virtual worlds, the need for content creation tools that can scale in terms of the quantity, quality, and diversity of 3D content is becoming evident. In our work, we aim to train performant 3D generative models that synthesize textured meshes which can be directly consumed by 3D rendering engines, thus immediately usable in downstream applications. Prior works on 3D generative modeling either lack geometric details, are limited in the mesh topology they can produce, typically do not support textures, or utilize neural renderers in the synthesis process, which makes their use in common 3D software non-trivial. In this work, we introduce GET3D, a Generative model that directly generates Explicit Textured 3D meshes with complex topology, rich geometric details, and high fidelity textures. We bridge recent success in the differentiable surface modeling, differentiable rendering as well as 2D Generative Adversarial Networks to train our model from 2D image collections. GET3D is able to generate high-quality 3D textured meshes, ranging from cars, chairs, animals, motorbikes and human characters to buildings, achieving significant improvements over previous methods.

## Paper

---

[![](assets/get3d_paper_figure.png)](assets/paper.pdf)

**GET3D: A Generative Model of High Quality 3D Textured Shapes Learned from Images**

Jun Gao, Tianchang Shen, Zian Wang, Wenzheng Chen, Kangxue Yin, Daiqing Li, Or Litany, Zan Gojcic, Sanja Fidler

description  [PDF](assets/paper.pdf)

description  [arXiv version](https://arxiv.org/abs/2209.11163)

insert\_comment  [BibTeX](assets/bib.txt)

## Generated 3D Assets

---


[

Your browser does not support the video tag.
](assets/six-category-1x1.mp4)

[

Your browser does not support the video tag.
](assets/full-scene-slide-1x1.mp4)

Qualitative results on unconditional 3D generation. We highlight the diversity and quality of our generated 3D meshes with textures, including: 1. wheels on the legs of the chairs; 2. wheels, all the lights and windows for the cars; 3. mouse, ears, horns for the animals; 4. back mirrors, wireframes on the tires for the motorbike, 5. the high-heeled shoes, cloths for humans

## Disentanglement between Geometry and Texture

---


[

Your browser does not support the video tag.
](assets/combined_car_swap.mp4)

In each row, we show shapes generated from the same geometry latent code, while changing the texture latent code. In each column, we show shapes generated from the same texture latent code, while changing the geometry code. Our model achieves a good disentanglement between geometry and texture.


[

Your browser does not support the video tag.
](assets/car_swap_interpolate.mp4)

In each row, we show shapes generated from the same texture latent code, while interpolating the geometry latent code from left to right. In each column, we show shapes generated from the same geometry latent code, while interpolating the texture code from top to bottom. This result demonstrates a meaningful interpolation for each of them.

## Latent Code Interpolation

---


[

Your browser does not support the video tag.
](assets/latent-interpolation.mp4)

In each subfigure, we apply a random walk in the latent space and generate corresponding 3D shapes. GET3D is able to generate a smooth transition between different shapes for all categories.

## Generating Novel Shapes

---


[

Your browser does not support the video tag.
](assets/local-variation-3x3.mp4)

In each row, we locally perturb the latent code by adding a small noise. In this way, GET3D is able to generate similar looking shapes with slight difference locally.

## Unsupervised Material Generation

---


[

Your browser does not support the video tag.
](assets/material-prediction.mp4)

Combined with [DIBR++](https://nv-tlabs.github.io/DIBRPlus/), GET3D is able to generate materials and produce meaningful view-dependent lighting effects in a completely unsupervised manner.

## Text-guided Shape Generation

---


[

Your browser does not support the video tag.
](assets/text2mesh-car.mp4)
[

Your browser does not support the video tag.
](assets/text2mesh-animal.mp4)
[

Your browser does not support the video tag.
](assets/text2mesh-house.mp4)

Text-guided shape generation. We follow recent work [StyleGAN-NADA](https://stylegan-nada.github.io/) , where users provide a text and we finetune our 3D generator by computing the directional CLIP loss on the rendered 2D images and the provided texts from the users. Our model generates a large amount of meaningful shapes with text prompts from the users.

## Citation

---

```
@inproceedings{gao2022get3d,
    title={GET3D: A Generative Model of High Quality 3D Textured Shapes Learned from Images},
    author={Jun Gao and Tianchang Shen and Zian Wang and Wenzheng Chen and Kangxue Yin 
        and Daiqing Li and Or Litany and Zan Gojcic and Sanja Fidler},
    booktitle={Advances In Neural Information Processing Systems},
    year={2022}
}
```

## Further Information

---

GET3D builds upon several previous works:

* [Learning Deformable Tetrahedral Meshes for 3D Reconstruction (NeurIPS 2020)](https://nv-tlabs.github.io/DefTet/)
* [Deep Marching Tetrahedra: a Hybrid Representation for High-Resolution 3D Shape Synthesis (NeurIPS 2021)](https://nv-tlabs.github.io/DMTet/)
* [Extracting Triangular 3D Models, Materials, and Lighting From Images (CVPR 2022)](https://nvlabs.github.io/nvdiffrec/)
* [EG3D: Efficient Geometry-aware 3D Generative Adversarial Networks (CVPR 2022)](https://nvlabs.github.io/eg3d/)
* [DIB-R++: Learning to Predict Lighting and Material with a Hybrid Differentiable Renderer (NeurIPS 2021)](https://nv-tlabs.github.io/DIBRPlus/)
* [Nvdiffrast 鈥� Modular Primitives for High-Performance Differentiable Rendering (SIGRAPH Asia 2020)](https://nvlabs.github.io/nvdiffrast/)

Please also consider citing these papers if you follow our work.

```
@inproceedings{dmtet,
    title = {Deep Marching Tetrahedra: a Hybrid Representation for High-Resolution 3D Shape Synthesis},
    author = {Tianchang Shen and Jun Gao and Kangxue Yin and Ming-Yu Liu and Sanja Fidler},
    year = {2021},
    booktitle = {Advances in Neural Information Processing Systems}
}
@inproceedings{nvdiffrec,
    title={Extracting Triangular 3D Models, Materials, and Lighting From Images},
    author={Munkberg, Jacob and Hasselgren, Jon and Shen, Tianchang and Gao, Jun and Chen, Wenzheng and 
    Evans, Alex and M{\"u}ller, Thomas and Fidler, Sanja},
    booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition},
    pages={8280--8290},
    year={2022}
}
```

## Business Inquiries

---

For business inquiries, please visit our website and submit the form: [NVIDIA Research Licensing](https://www.nvidia.com/en-us/research/inquiries/)
