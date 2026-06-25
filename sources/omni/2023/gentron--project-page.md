# GenTron
Source: https://www.shoufachen.com/gentron_website/
GenTron



# **GenTron: Diffusion Transformers for Image and Video Generation**

## **[[CVPR 2024]](http://arxiv.org/abs/2312.04557)**

[Shoufa Chen](https://www.shoufachen.com/)1, 2\* [Mengmeng Xu](https://mengmengxu.netlify.app/)2\* [Jiawei Ren](https://jiawei-ren.github.io/)2 [Yuren Cong](https://yrcong.github.io/)2  [Sen He](https://senhe.github.io/)2

[Yanping Xie](https://uk.linkedin.com/in/yanping-xie-53583428)2 [Animesh Sinha](http://animesh-sinha.com/)2 [Ping Luo](http://luoping.me/)1 [Tao Xiang](https://www.surrey.ac.uk/people/tao-xiang)2  [Juan-Manuel Perez-Rua](https://scholar.google.com/citations?user=Vbvimu4AAAAJ&hl=es)2
  
  
1 The University of Hong Kong2 Meta
  
\* Equal contribution

## GenTron-T2V

  

![](./assets/t2v_demo1.gif)


A fantasy landscape trending on Artstation, 4k


![](./assets/t2v_demo2.gif)


An astronaut flying in space, 4k high resolution


![](./assets/t2v_demo3.gif)


A panda standing on a surfboard in the ocean in sunset, 4k

  

![](./assets/t2v_demo4.gif)


An astronaut riding a horse high definition, 4k


![](./assets/t2v_demo5.gif)


Flying through a fantasy landscape, 4k high resolution


![](./assets/t2v_demo6.gif)


Traveler walking alone in the misty forest at sunset, 4k

## Abstract

In this study, we explore Transformer-based diffusion models for image and video generation.
Despite the dominance of Transformer architectures in various fields due to their flexibility and scalability, the visual generative domain primarily utilizes CNN-based U-Net architectures, particularly in diffusion-based models.
We introduce **GenTron**, a family of **Gen**erative models employing **Tr**ansformer-based diffusi**on**, to address this gap.
Our initial step was to adapt Diffusion Transformers (DiTs) from class to text conditioning, a process involving thorough empirical exploration of the conditioning mechanism.
We then scale GenTron from approximately 900M to over 3B parameters, observing significant improvements in visual quality.
Furthermore, we extend GenTron to text-to-video generation, incorporating novel motion-free guidance to enhance video quality.
In human evaluations against SDXL, GenTron achieves a 51.1% win rate in visual quality (with a 19.8% draw rate), and a 42.3% win rate in text alignment (with a 42.9% draw rate). GenTron also excels in the T2I-CompBench, underscoring its strengths in compositional generation. We believe this work will provide meaningful insights and serve as a valuable reference for future research.

## GenTron-T2I Results: T2I-CompBench

|  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Model | Attribute Binding | | | Object Relationship | | Complex | **Mean** |
| Color | Shape | Texture | Spatial | Non-spatial |
| SD v1.4 | 37.65 | 35.76 | 41.56 | 12.46 | 30.79 | 30.80 | 31.50 |
| SD v2 | 50.65 | 42.21 | 49.22 | 13.42 | 30.96 | 33.86 | 36.72 |
| Composable v2 | 40.63 | 32.99 | 36.45 | 8.00 | 29.80 | 28.98 | 29.47 |
| Structured v2 | 49.90 | 42.18 | 49.00 | 13.86 | 31.11 | 33.55 | 36.60 |
| Attn-Exct v2 | 64.00 | 45.17 | 59.63 | 14.55 | 31.09 | 34.01 | 41.41 |
| GORS | 66.03 | 47.85 | 62.87 | 18.15 | 31.93 | 33.28 | 43.35 |
| DALL·E 2 | 57.50 | 54.64 | 63.74 | 12.83 | 30.43 | 36.96 | 42.68 |
| SD XL | 63.69 | 54.08 | 56.37 | 20.32 | 31.10 | 40.91 | 44.41 |
| PixArt-alpha | 68.86 | 55.82 | 70.44 | 20.82 | 31.79 | 41.17 | 48.15 |
| **GenTron** | **76.74** | **57.00** | **71.50** | **20.98** | **32.02** | **41.67** | **49.99** |

We present the alignment evaluation outcomes derived from T2I-CompBench. Our methodology exhibits exceptional efficacy across various domains, notably in attribute binding, object relationships, and intricate compositions. This signifies an advanced capability in compositional generation, particularly excelling in color binding.

## GenTron-T2I Results: User Study

  
  
![](./assets/user_study.png)  

We illustrate the comparison of user preferences between our method and SDXL.
We generated 100 images using each method with standard prompts from [PartiPrompt2](https://github.com/google-research/parti/blob/main/PartiPrompts.tsv).
GenTron achieves a 51.1% win rate in visual quality (with a 19.8% draw rate), and a 42.3% win rate in text alignment (with a 42.9% draw rate).

## Approach

![](./assets/t2i_arch.png)


GenTron-T2I Architecture


![](./assets/t2v_arch.png)


GenTron-T2V Architecture

For GenTron-T2V, the temporal self-attention layer is inserted between the cross-attention and the MLPs. The motion-free mask, which is an identity matrix, will be utilized in the **TempSelfAttn** with a probability of pmotion\_free.

## Additional GenTron-T2I Results

  

![](./assets/t2i_demo05.png)


A cute happy Corgi playing in park, sunset, 4k


![](./assets/t2i_demo04.png)


A cute cat running


![](./assets/t2i_demo02.png)


A blue otter wearing a hat and dancing on the beach.

  

![](./assets/t2i_demo03.png)


A car moving slowly on an empty street, rainy evening, van Gogh painting.


![](./assets/t2i_demo07.png)


Snow mountain and tree reflection in the lake


![](./assets/t2i_demo08.png)


a tiger in a field

## BibTex

`@article{chen2023gentron,
title={GenTron: Delving Deep into Diffusion Transformers for Image and Video Generation},
author={Chen, Shoufa and Xu, Mengmeng and Ren, Jiawei and Cong, Yuren and He, Sen and Xie, Yanping and Sinha, Animesh and Luo, Ping and Xiang, Tao and Perez-Rua, Juan-Manuel},
journal={arXiv preprint arXiv:2312.04557},
year={2023}
}`

Acknowledgements:
The webpage template is borrowed from [DreamBooth](https://dreambooth.github.io/). We thank the authors for their codebase.
