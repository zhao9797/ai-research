# PIXART-α
Source: https://pixart-alpha.github.io/
PIXART-α



# PIXART-α: Fast Training of Diffusion Transformer for Photorealistic Text-to-Image Synthesis

# ICLR 2024 Spotlight

[Junsong
Chen](https://lawrence-cj.github.io/)1,2,3,\*,

[Jincheng
Yu](https://lovesykun.cn/about.html)1,4,\*,

[Chongjian
Ge](https://chongjiange.github.io)1,3,\*,

[Lewei
Yao](https://scholar.google.com/citations?user=hqDyTg8AAAAJ)1,4,\*,

[Enze Xie](https://xieenze.github.io/)1,‡,

[Yue Wu](https://yuewuhkust.github.io/)1,

[Zhongdao Wang](https://zhongdao.github.io/)1,

[James Kwok](https://www.cse.ust.hk/~jamesk/)4,

[Ping Luo](http://luoping.me/)3,

[Huchuan Lu](https://scholar.google.com/citations?hl=en&user=D3nE0agAAAAJ)2,

[Zhenguo
Li](https://scholar.google.com/citations?user=XboZC1AAAAAJ)1

1Huawei Noah's Ark Lab,
2Dalian University of Technology,
3The University of Hong Kong,
4The Hong Kong University of Science and
Technology
  
\*Equal contribution. Work done during the
internships of the four students at Huawei Noah's Ark Lab.
  
‡[Corresponding author.](mailto:xie.enze@huawei.com)

[Code](https://github.com/PixArt-alpha/PixArt-alpha)


[🤗
SAM-LLaVA-Captions](https://huggingface.co/datasets/PixArt-alpha/SAM-LLaVA-Captions10M)

[🧨
Diffusers](https://huggingface.co/docs/diffusers/main/en/api/pipelines/pixart)

[arXiv-PixArt-α](https://arxiv.org/abs/2310.00426)

[arXiv-PixArt-δ](https://arxiv.org/abs/2401.05252)

[Discord](https://discord.gg/rde6eaE5Ta)

[🤗
HF Demo: PixArt-α](https://huggingface.co/spaces/PixArt-alpha/PixArt-alpha)

[🤗
HF Demo: PixArt-LCM](https://huggingface.co/spaces/PixArt-alpha/PixArt-LCM)

[X
OpenXLab Demo: PixArt-α](https://openxlab.org.cn/apps/detail/PixArt-alpha/PixArt-alpha)

[X
OpenXLab Demo: PixArt-LCM](https://openxlab.org.cn/apps/detail/houshaowei/PixArt-LCM)

[Colab Demo](https://colab.research.google.com/drive/1jZ5UZXk7tcpTfVwnX33dDuefNMcnW9ME?usp=sharing)

![carousel6](static/images/carousel/carousel6.png)

Nature vs human nature, surreal, UHD, 8k, hyper
details, rich colors, photograph.

![carousel7](static/images/carousel/carousel7.png)

artistic

![carousel8](static/images/carousel/carousel8.png)

Bright scene, aerial view,ancient city, fantasy,
gorgeous light, mirror reflection, high detail, wide angle lens.

![carousel1](static/images/carousel/carousel1.png)

A small cactus with a happy face in the Sahara
desert.

![carousel2](static/images/carousel/carousel2.png)

A alpaca made of colorful building blocks,
cyberpunk.

![carousel3](static/images/carousel/carousel3.png)

Real beautiful woman.

![carousel4](static/images/carousel/carousel4.png)

Luffy from ONEPIECE, handsome face, fantasy.

![carousel5](static/images/carousel/carousel5.png)

Poster of a mechanical cat, techical Schematics
viewed from front.

![carousel6](static/images/carousel/carousel6.png)

Nature vs human nature, surreal, UHD, 8k, hyper
details, rich colors, photograph.

![carousel7](static/images/carousel/carousel7.png)

artistic

![carousel8](static/images/carousel/carousel8.png)

Bright scene, aerial view,ancient city, fantasy,
gorgeous light, mirror reflection, high detail, wide angle lens.

![carousel1](static/images/carousel/carousel1.png)

A small cactus with a happy face in the Sahara
desert.

![carousel2](static/images/carousel/carousel2.png)

A alpaca made of colorful building blocks,
cyberpunk.

![carousel3](static/images/carousel/carousel3.png)

Real beautiful woman.

![carousel4](static/images/carousel/carousel4.png)

Luffy from ONEPIECE, handsome face, fantasy.

![carousel5](static/images/carousel/carousel5.png)

Poster of a mechanical cat, techical Schematics
viewed from front.

![carousel6](static/images/carousel/carousel6.png)

Nature vs human nature, surreal, UHD, 8k, hyper
details, rich colors, photograph.

![carousel7](static/images/carousel/carousel7.png)

artistic

![carousel8](static/images/carousel/carousel8.png)

Bright scene, aerial view,ancient city, fantasy,
gorgeous light, mirror reflection, high detail, wide angle lens.

![carousel1](static/images/carousel/carousel1.png)

A small cactus with a happy face in the Sahara
desert.

![carousel2](static/images/carousel/carousel2.png)

A alpaca made of colorful building blocks,
cyberpunk.



## Abstract

The most advanced text-to-image (T2I) models require significant training costs (e.g.,
millions of GPU hours), seriously hindering the fundamental innovation for the AIGC
community while increasing CO2 emissions. This paper introduces PIXART-α, a
Transformer-based T2I diffusion model whose image generation quality is competitive with
state-of-the-art image generators (e.g., Imagen, SDXL, and even Midjourney), reaching
near-commercial application standards. Additionally, it supports high-resolution image
synthesis up to 1024px resolution with low training cost, as shown in Figure 1 and 2. To
achieve this goal, three core designs are proposed: (1) Training strategy decomposition: We
devise three distinct training steps that separately optimize pixel dependency, text-image
alignment, and image aesthetic quality; (2) Efficient T2I Transformer: We incorporate
cross-attention modules into Diffusion Transformer (DiT) to inject text conditions and
streamline the computation-intensive class-condition branch; (3) High-informative data: We
emphasize the significance of concept density in text-image pairs and leverage a large
Vision-Language model to auto-label dense pseudo-captions to assist text-image alignment
learning. As a result, PIXART-α's training speed markedly surpasses existing
large-scale T2I models, e.g., PIXART-α only takes 10.8% of Stable Diffusion v1.5's
training time (~675 vs. ~6,250 A100 GPU days), saving nearly $300,000 ($26,000 vs. $320,000)
and reducing 90% CO2 emissions. Moreover, compared with a larger SOTA model,
RAPHAEL, our
training cost is merely 1%. Extensive experiments demonstrate that PIXART-α excels in
image quality, artistry, and semantic control. We hope PIXART-α will provide new
insights to the AIGC community and startups to accelerate building their own high-quality
yet low-cost generative models from scratch.

## Online Demo

Error

**This space is experiencing an issue.**

Please contact the author of the page to let them know.

## Training Efficiency

Comparisons of CO2 emissions and training cost among T2I generators. PIXART-α
achieves an exceptionally low training cost of $26,000. Compared to RAPHAEL, our CO2
emissions
and training costs are merely 1.1% and 0.85%, respectively.

![efficiency](static/images/efficiency.svg)

## ControlNet

## ControlNet customization samples from PIXART-α. We use the reference images to generate the corresponding HED edge images and use them as the control signal for PIXART-α ControlNet.

![huawei](static/images/controlnet/controlnet_huawei.svg)
![lenna](static/images/controlnet/controlnet_lenna.svg)

## Dreambooth

## PIXART-α can be combined with Dreambooth. Given a few images and text prompts, PIXART-α can generate high-fidelity images, that exhibit natural interactions with the environment, precise modification of the object colors, demonstrating that PIXART-α can generate images with exceptional quality, and has a strong capability in customized extension.

![dog](static/images/dreambooth/dreambooth_dog.svg)
![Wenjie M5](static/images/dreambooth/dreambooth_m5.svg)

## More Samples

![](static/images/samples/1.png)

![sample1](static/images/samples/1.png)

8k uhd A man looks up at the starry sky, lonely and ethereal,
Minimalism, Chaotic
composition Op Art

![](static/images/samples/2.png)

![sample2](static/images/samples/2.png)

A baby painter trying to draw very simple picture, white
background

![](static/images/samples/3.png)

![sample3](static/images/samples/3.png)

A dog that has been meditating all the time

![](static/images/samples/4.png)

![sample4](static/images/samples/4.png)

A snowy mountain

![](static/images/samples/5.png)

![sample5](static/images/samples/5.png)

A worker that looks like a mixture of cow and horse is working
hard to type code

![](static/images/samples/6.png)

![sample6](static/images/samples/6.png)

Half human, half robot, repaired human

![](static/images/samples/7.png)

![sample7](static/images/samples/7.png)

knolling of a drawing tools for painter

![](static/images/samples/8.png)

![sample8](static/images/samples/8.png)

Van Gogh painting of a teacup on the desk

![](static/images/samples/9.png)

![sample9](static/images/samples/9.png)

Chinese painting of grapes

![](static/images/samples/10.png)

![sample10](static/images/samples/10.png)

Stars, water, brilliantly, gorgeous large scale scene

![](static/images/samples/11.png)

![sample11](static/images/samples/11.png)

A sureal parallel world where mankind avoid extinction

![](static/images/samples/12.png)

![sample12](static/images/samples/12.png)

Pirate ship trapped in a cosmic maelstrom nebula

## BibTeX

```
@misc{chen2023pixartalpha,
    title={PixArt-$\alpha$: Fast Training of Diffusion Transformer for Photorealistic Text-to-Image Synthesis}, 
    author={Junsong Chen and Jincheng Yu and Chongjian Ge and Lewei Yao and Enze Xie and Yue Wu and Zhongdao Wang and James Kwok and Ping Luo and Huchuan Lu and Zhenguo Li},
    year={2023},
    eprint={2310.00426},
    archivePrefix={arXiv},
    primaryClass={cs.CV}
}
```



This page was built using the [Academic Project Page Template](https://github.com/eliahuhorwitz/Academic-project-page-template) which was adopted from the [Nerfies](https://nerfies.github.io) project page.
You are free to borrow the of this website, we just ask that you link back to this page in
the footer.   
 This website is licensed under a [Creative
Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).

Total clicks: 219620
