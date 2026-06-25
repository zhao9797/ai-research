# ProlificDreamer: High-Fidelity and Diverse Text-to-3D Generation with Variational Score Distillation
Source: https://ml.cs.tsinghua.edu.cn/prolificdreamer/
ProlificDreamer: High-Fidelity and Diverse Text-to-3D Generation with Variational Score Distillation



# ProlificDreamer: High-Fidelity and Diverse Text-to-3D Generation with Variational Score Distillation

[Zhengyi Wang](https://thuwzy.github.io)\*1,3,

[Cheng Lu](https://luchengthu.github.io)\*1,

[Yikai Wang](https://yikaiw.github.io)1,

[Fan Bao](https://baofff.github.io)1,3,

[Chongxuan Li](https://zhenxuan00.github.io)2,

[Hang Su](http://suhangss.me)1,

[Jun Zhu](https://ml.cs.tsinghua.edu.cn/~jun/)1,3

\*Equal contribution.

1Tsinghua University,
2Renmin University of China,
3ShengShu

NeurIPS 2023 (Spotlight)

[Paper](https://arxiv.org/pdf/2305.16213.pdf)

[arXiv](https://arxiv.org/abs/2305.16213)

[Slides](./static/prolificdreamer.ppsx)




[Code](https://github.com/thu-ml/prolificdreamer)

## Abstract

Score distillation sampling (SDS) has shown great promise in text-to-3D
generation by distilling pretrained large-scale text-to-image diffusion models,
but suffers from over-saturation, over-smoothing, and low-diversity problems.
In this work, we propose to model the 3D parameter as a random variable instead
of a constant as in SDS and present *variational score distillation* (VSD),
a principled particle-based variational framework to explain and
address the aforementioned issues in text-to-3D generation. We show
that SDS is a special case of VSD and leads to poor samples with both
small and large CFG weights. In comparison, VSD works well with various
CFG weights as ancestral sampling from diffusion models and simultaneously
improves the diversity and sample quality with a common CFG weight (i.e., 7.5).
We further present various improvements in the design space for text-to-3D
such as distillation time schedule and density initialization, which are
orthogonal to the distillation algorithm yet not well explored. Our overall
approach, dubbed *ProlificDreamer*, can generate high rendering resolution
(i.e., 512x512) and high-fidelity NeRF with rich structure and complex effects
(e.g., smoke and drops). Further, initialized from NeRF, meshes fine-tuned by
VSD are meticulously detailed and photo-realistic.

---

## Generated Textured Meshes

[

](./static/myvideos/dog.mp4)

Michelangelo style statue of dog reading news on a cellphone.

[

](./static/myvideos/croissant.mp4)

A delicious croissant.

[

](./static/myvideos/elephant.mp4)

An elephant skull.

[

](./static/myvideos/tulip.mp4)

A blue tulip.

[

](./static/myvideos/cactus.mp4)

A small saguaro cactus planted in a clay pot.

[

](./static/myvideos/pineapple.mp4)

A pineapple.

[

](./static/myvideos/snail.mp4)

A snail on a leaf.

[

](./static/myvideos/roof.mp4)

A 3D model of an adorable cottage with a thatched roof.

[

](./static/myvideos/loaf.mp4)

A sliced loaf of fresh bread.

[

](./static/myvideos/spider.mp4)

A tarantula, highly detailed.

## Generated NeRFs

[

](./static/myvideos/smart.mp4)

Inside of a smart home, realistic detailed photo, 4k.

[

](./static/myvideos/iso.mp4)

Small lavender isometric room, soft lighting, unreal engine render, voxels.

[

](./static/myvideos/hamburger.mp4)

A DSLR photo of a hamburger inside a resturant.

[

](./static/myvideos/ice.mp4)

A DSLR photo of an icecream sundae inside a shopping mall.

[

](./static/myvideos/high-nerf.mp4)

High-fidelity generated NeRFs.

[

](./static/myvideos/comp-nerf.mp4)

Complex generated NeRFs.

## Diverse Results

[

](./static/myvideos/sand.mp4)

A highly detailed sand castle.

[

](./static/myvideos/tutu.mp4)

A hotdog in a tutu skirt.

## Related Links

There are a lot of excellent works that are related to ProlificDreamer.

[DreamFusion: Text-to-3D using 2D Diffusion](https://dreamfusion3d.github.io/)

[Score Jacobian Chaining: Lifting Pretrained 2D Diffusion Models for 3D Generation](https://pals.ttic.edu/p/score-jacobian-chaining)

[Magic3D: High-Resolution Text-to-3D Content Creation](https://research.nvidia.com/labs/dir/magic3d/)

[Fantasia3D: Disentangling Geometry and Appearance for High-quality Text-to-3D Content Creation](https://fantasia3d.github.io/)

[Latent-NeRF for Shape-Guided Generation of 3D Shapes and Textures](https://github.com/eladrich/latent-nerf)

[DreamCraft3D: Hierarchical 3D Generation with Bootstrapped Diffusion Prior](https://mrtornado24.github.io/DreamCraft3D/)

## BibTeX

```
@article{wang2023prolificdreamer,
      title={ProlificDreamer: High-Fidelity and Diverse Text-to-3D Generation with Variational Score Distillation},
      author={Zhengyi Wang and Cheng Lu and Yikai Wang and Fan Bao and Chongxuan Li and Hang Su and Jun Zhu},
      journal={arXiv preprint arXiv:2305.16213},
      year={2023}
}
```

This website is constructed using the source code provided by [Nerfies](https://github.com/nerfies/nerfies.github.io), and we are grateful for their template.
