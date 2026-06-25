# MaskGIT: Masked Generative Image Transformer
Source: https://masked-generative-image-transformer.github.io/
MaskGIT: Masked Generative Image Transformer

# MaskGIT: Masked Generative Image Transformer CVPR 2022

## [Huiwen Chang](https://research.google/people/107664/), Han Zhang, Lu Jiang, Ce Liu, [Bill Freeman](https://research.google/people/WilliamTFreeman/) Google Research

---

![](imgs/thumbnail.png)

Class-conditional Image Editing by MaskGIT

### Abstract

Image generative transformers typically treat an image as a sequence of tokens, and decode an image sequentially following the raster scan ordering (i.e. line-by-line).

This paper proposes a novel image synthesis paradigm using a bidirectional transformer decoder, which we term MaskGIT. During training, MaskGIT learns to predict randomly masked tokens by attending to tokens in all directions. At inference time, the model begins with generating all tokens of an image simultaneously, and then refines the image iteratively conditioned on the previous generation.

Our experiments demonstrate that MaskGIT significantly outperforms the state-of-the-art transformer model on the ImageNet dataset, and accelerates autoregressive decoding by up to 64x. Besides, MaskGIT can be easily extended to various image editing tasks, such as inpainting, extrapolation, and image manipulation.

  

![](imgs/sampling.gif)

Autoregressive decoding vs MaskGIT's parallel decoding visualized at the same playback speed (0.1s per step).

### Paper

[![](imgs/paper.png)](https://arxiv.org/pdf/2202.04200.pdf)

MaskGIT: Masked Generative Image Transformer  
Huiwen Chang, Han Zhang, Lu Jiang, Ce Liu, and Bill Freeman  
*CVPR 2022*  
[[arXiv](https://arxiv.org/abs/2202.04200)] [[GitHub](https://github.com/google-research/maskgit)] [[Demo Colab](https://colab.research.google.com/github/google-research/maskgit/blob/main/MaskGIT_demo.ipynb)]

### Applications

Horizontal image extrapolation:

![](imgs/panorama_0.png)

![](imgs/panorama_1.png)

![](imgs/panorama_2.png)

![](imgs/panorama_3.png)

![](imgs/panorama_4.png)

![](imgs/panorama_5.png)

![](imgs/panorama_6.png)

![](imgs/panorama_7.png)

![](imgs/panorama_8.png)

❮
❯

Inpainting results on 512x512 Places2 images:

![](imgs/inpaint_0.png)

![](imgs/inpaint_1.png)

![](imgs/inpaint_2.png)

![](imgs/inpaint_3.png)

![](imgs/inpaint_4.png)

![](imgs/inpaint_5.png)

![](imgs/inpaint_6.png)

![](imgs/inpaint_7.png)

❮
❯

  
Class-conditional image editing results:
![](imgs/class-conditional_image_editing.gif)

### BibTeX

@InProceedings{chang2022maskgit,
title = {MaskGIT: Masked Generative Image Transformer},
author={Huiwen Chang and Han Zhang and Lu Jiang and Ce Liu and William T. Freeman},
booktitle = {The IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
month = {June},
year = {2022}
}

### Acknowledgement

Webpage template from Richard Tucker.
