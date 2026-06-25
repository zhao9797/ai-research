# HyperHuman: Hyper-Realistic Human Generation with Latent Structural Diffusion
Source: https://snap-research.github.io/HyperHuman/
HyperHuman: Hyper-Realistic Human Generation with Latent Structural Diffusion





HyperHuman: Hyper-Realistic Human Generation with Latent Structural Diffusion

[Xian Liu](https://alvinliu0.github.io/)1,2   
[Jian Ren](https://alanspike.github.io/)1   
[Aliaksandr Siarohin](https://aliaksandrsiarohin.github.io/aliaksandr-siarohin-website/)1   
[Ivan Skorokhodov](https://universome.github.io/)1   
[Yanyu Li](https://scholar.google.com/citations?user=XUj8koUAAAAJ&hl=en)1   
  
[Dahua Lin](http://dahua.site/)2   
[Xihui Liu](https://xh-liu.github.io/)3   
[Ziwei Liu](https://liuziwei7.github.io/)4   
[Sergey Tulyakov](http://www.stulyakov.com/)1

1Snap Inc.   
2CUHK   
3HKU   
4NTU

[Paper](./content/hyperhuman.pdf)

[arXiv](https://arxiv.org/abs/2310.08579)


[Short Demo (3min)](https://www.youtube.com/watch?v=eRPZW1pwxog)

[Long Demo (10min)](https://www.youtube.com/watch?v=CxGfbwZOcyU)


[Github](https://github.com/snap-research/HyperHuman)

![](./content/examples/a girl with blue.png)

A girl with blue hair is taking a self portrait.

![](./content/examples/a man wearing a helmet.png)

A man wearing a helmet is sitting on his blue motorcycle.

![](./content/examples/a person dressed up.png)

A person dressed up taking a picture at a street with his fist up.

![](./content/examples/baby girl.png)

A baby girl with beautiful blue eyes standing next to a brown teddy bear.

![](./content/examples/little girl.png)

A little girl with wavy hair and smile holding a teddy bear.

![](./content/examples/A man and woman.png)

A man and woman seated at a table in a restaurant.

![](./content/examples/A cow laying.png)

A cow laying on the grass behind a man holding a cup of coffee.

![](./content/examples/A young kid.png)

A young kid stands before a birthday cake decorated with captain America.

![](./content/examples/A man who is sitting.png)

A man who is sitting in a bus looking away from the window.

![](./content/examples/a man in a red.png)

A man in a red shirt is holding a skate board up over his head.

![](./content/examples/two mean who are.png)

Two men who are sitting next to each other with a large pizza in front of them.

![](./content/examples/two children.png)

Two children carry an enormous stuffed teddy bear.

![](./content/examples/the upper half.png)

The upper half of a man posing for a photograph wearing a suit with a blue tie and matching pocket corner.

![](./content/examples/an older man.png)

An older man is wearing a funny hat in his dining room.

![](./content/examples/young man.png)

Young man on top of a snowboard wearing maroon jacket.

![](./content/examples/man seating.png)

Man sitting on brick covered ground, appearing dirty and tired.

![](./content/examples/a man wearing.png)

A man wearing a purple neck tie and glasses while sitting in a car.

![](./content/examples/a man standing.png)

A man standing on grassy area next to trees.

![](./content/examples/a girl with blue.png)

A girl with blue hair is taking a self portrait.

![](./content/examples/a man wearing a helmet.png)

A man wearing a helmet is sitting on his blue motorcycle.

![](./content/examples/a person dressed up.png)

A person dressed up taking a picture at a street with his fist up.

![](./content/examples/baby girl.png)

A baby girl with beautiful blue eyes standing next to a brown teddy bear.

![](./content/examples/little girl.png)

A little girl with wavy hair and smile holding a teddy bear.

![](./content/examples/A man and woman.png)

A man and woman seated at a table in a restaurant.

![](./content/examples/A cow laying.png)

A cow laying on the grass behind a man holding a cup of coffee.

![](./content/examples/A young kid.png)

A young kid stands before a birthday cake decorated with captain America.

![](./content/examples/A man who is sitting.png)

A man who is sitting in a bus looking away from the window.

![](./content/examples/a man in a red.png)

A man in a red shirt is holding a skate board up over his head.

![](./content/examples/two mean who are.png)

Two men who are sitting next to each other with a large pizza in front of them.

![](./content/examples/two children.png)

Two children carry an enormous stuffed teddy bear.

![](./content/examples/the upper half.png)

The upper half of a man posing for a photograph wearing a suit with a blue tie and matching pocket corner.

![](./content/examples/an older man.png)

An older man is wearing a funny hat in his dining room.

![](./content/examples/young man.png)

Young man on top of a snowboard wearing maroon jacket.

![](./content/examples/man seating.png)

Man sitting on brick covered ground, appearing dirty and tired.

![](./content/examples/a man wearing.png)

A man wearing a purple neck tie and glasses while sitting in a car.

![](./content/examples/a man standing.png)

A man standing on grassy area next to trees.

![](./content/examples/a girl with blue.png)

A girl with blue hair is taking a self portrait.

![](./content/examples/a man wearing a helmet.png)

A man wearing a helmet is sitting on his blue motorcycle.

![](./content/examples/a person dressed up.png)

A person dressed up taking a picture at a street with his fist up.

![](./content/examples/baby girl.png)

A baby girl with beautiful blue eyes standing next to a brown teddy bear.

![](./content/examples/little girl.png)

A little girl with wavy hair and smile holding a teddy bear.




Short Demo Video (3min)

We present a short demo video, mostly with visualization results and a very quick overview of our framework.

Long Demo Video (10min)

We present a long demo video with detailed elaborations on the motivations and framework designs.

Abstract

Despite significant advances in large-scale text-to-image models, achieving hyper-realistic human image generation remains a desirable yet unsolved task.
Existing models like Stable Diffusion and DALL·E 2 tend to generate human images with incoherent parts or unnatural poses.
To tackle these challenges, our key insight is that human image is inherently structural over multiple granularities, from the coarse-level body skeleton to the fine-grained spatial geometry.
Therefore, capturing such correlations between the explicit appearance and latent structure in one model is essential to generate coherent and natural human images.
To this end, we propose a unified framework, **HyperHuman**, that generates in-the-wild human images of high realism and diverse layouts.
Specifically, **1)** we first build a large-scale human-centric dataset, named *HumanVerse*, which consists of 340M images with comprehensive annotations like human pose, depth, and surface-normal.
**2)** Next, we propose a *Latent Structural Diffusion Model* that simultaneously denoises the depth and surface-normal along with the synthesized RGB image. Our model enforces the joint learning of image appearance, spatial relationship, and geometry in a unified network, where each branch in the model complements to each other with both structural awareness and textural richness.
**3)** Finally, to further boost the visual quality, we propose a *Structure-Guided Refiner* to compose the predicted conditions for more detailed generation of higher resolution.
Extensive experiments demonstrate that our framework yields the state-of-the-art performance, generating hyper-realistic human images under diverse scenarios.

![](./content/teaser/t11.jpg)

![](./content/teaser/t12.jpg)

![](./content/teaser/t1.jpg)

![](./content/teaser/t2.jpg)

![](./content/teaser/t3.jpg)

![](./content/teaser/t4.jpg)

![](./content/teaser/t5.jpg)

![](./content/teaser/t6.jpg)

![](./content/teaser/t7.jpg)

![](./content/teaser/t8.jpg)

![](./content/teaser/t9.jpg)

![](./content/teaser/t10.jpg)

![](./content/teaser/t11.jpg)

![](./content/teaser/t12.jpg)

![](./content/teaser/t1.jpg)

![](./content/teaser/t2.jpg)

![](./content/teaser/t3.jpg)

![](./content/teaser/t4.jpg)

![](./content/teaser/t5.jpg)

![](./content/teaser/t6.jpg)

![](./content/teaser/t7.jpg)

![](./content/teaser/t8.jpg)

![](./content/teaser/t9.jpg)

![](./content/teaser/t10.jpg)

![](./content/teaser/t11.jpg)

![](./content/teaser/t12.jpg)

![](./content/teaser/t1.jpg)

![](./content/teaser_half.png)

*Top:* The proposed **HyperHuman** simultaneously generates the coarse RGB, depth, normal, and high-resolution images conditioned on text and skeleton.
Both photo-realistic images and stylistic renderings can be created. *Bottom:* We compare with recent T2I models, showing better realism, quality, diversity, and controllability.
Note that in each 2x2 grid (**left**), the upper-left is *input* skeleton, while the others are jointly denoised normal, depth, and coarse RGB of 512x512.
With full model, we synthesize images up to 1024x1024 (**right**).

Framework Overview

|  |
| --- |
|  |

**Overview of HyperHuman Framework.** In *Latent Structural Diffusion Model* (purple), the image **x**, depth **d**, and surface-normal **n** are jointly denoised conditioning on caption **c** and pose skeleton **p**. In *Structure-Guided Refiner* (blue), we compose the predicted conditions for higher-resolution generation. Note that the grey images refer to randomly dropout conditions for more robust training.

Quantitative Results

|  |
| --- |
|  |

**Zero-Shot Evaluation on MS-COCO 2014 Validation Human.** We compare our model with recent SOTA general T2I models (Stable Diffusion v1.5, v2.0, v2.1; SDXL; DeepFloyd-IF) and controllable methods (ControlNet; T2I-Adapter; HumanSD). Note that SDXL generates artistic style in 512x512, and IF only creates fixed-size images, we first generate 1024x1024 results, then resize back to 512x512 for these two methods. We bold the **best** and underline the second results for clarity. Our improvements over the second method are shown in red.
  
  

|  |
| --- |
|  |

**Evaluation Curves on MS-COCO 2014 Validation Human Subset.** We show FID-CLIP (*left*) and FIDCLIP-CLIP (*right*) curves with CFG scale ranging from 4.0 to 20.0 for all methods.
  
  

|  |
| --- |
|  |

**User Preference Comparisons.** We report the ratio of users prefer our model to baselines.



More Comparisons (1024x1024)

![](./content/comparison/com11.jpg)

![](./content/comparison/com12.jpg)

![](./content/comparison/com1.jpg)

![](./content/comparison/com2.jpg)

![](./content/comparison/com3.jpg)

![](./content/comparison/com4.jpg)

![](./content/comparison/com5.jpg)

![](./content/comparison/com6.jpg)

![](./content/comparison/com7.jpg)

![](./content/comparison/com8.jpg)

![](./content/comparison/com9.jpg)

![](./content/comparison/com10.jpg)

![](./content/comparison/com11.jpg)

![](./content/comparison/com12.jpg)

![](./content/comparison/com1.jpg)

![](./content/comparison/com2.jpg)

![](./content/comparison/com3.jpg)

![](./content/comparison/com4.jpg)

![](./content/comparison/com5.jpg)

![](./content/comparison/com6.jpg)

![](./content/comparison/com7.jpg)

![](./content/comparison/com8.jpg)

![](./content/comparison/com9.jpg)

![](./content/comparison/com10.jpg)

![](./content/comparison/com11.jpg)

![](./content/comparison/com12.jpg)

![](./content/comparison/com1.jpg)










BibTeX

```
@article{liu2023hyperhuman,
    title={HyperHuman: Hyper-Realistic Human Generation with Latent Structural Diffusion},
    author={Liu, Xian and Ren, Jian and Siarohin, Aliaksandr and Skorokhodov, Ivan and Li, Yanyu and Lin, Dahua and Liu, Xihui and Liu, Ziwei and Tulyakov, Sergey},
    journal={arXiv preprint arXiv:2310.08579},
    year={2023}
}
```
