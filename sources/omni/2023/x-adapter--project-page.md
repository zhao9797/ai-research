# X-Adapter
Source: https://showlab.github.io/X-Adapter/
X-Adapter




# X-Adapter: Adding Universal Compatibility of Plugins for Upgraded Diffusion Model

Lingmin Ran1,

[Xiaodong Cun](https://vinthony.github.io/academic/)3,

[Jia-Wei Liu](https://jia-wei-liu.github.io/)1,

[Rui Zhao](https://ruizhaocv.github.io/)1,

Song Zijie4,

[Xintao Wang](https://xinntao.github.io/)3,

[Jussi Keppo](https://www.jussikeppo.com/)2

[Mike Zheng Shou](https://sites.google.com/view/showlab)1

1Show Lab,
2National University of Singapore,
3Tencent AI Lab,
4Fudan University

[Paper](./static/Paper/X_Adapter_Arxiv.pdf)

[arXiv](https://arxiv.org/abs/2312.02238)




[Code](https://github.com/showlab/X-Adapter)

TL;DR: X-Adapter enable plugins pretrained on old version (e.g. SD1.5) directly work with the upgraded Model (e.g., SDXL) without
further retraining

![](./static/image_X/xadapter_teaser_v8_page-0001.jpg)

## Abstract

We introduce X-Adapter, a universal upgrader to enable the pretrained plug-and-play modules
(e.g., ControlNet, LoRA) to work directly with the upgraded text-to-image diffusion model (e.g., SD-XL) without further retraining.

We achieve this goal by training an additional network to control the frozen upgraded model with the new text-image data pairs.
In detail, X-Adapter keeps a frozen copy of the old model to preserve the connectors of different plugins.
Additionally, X-Adapter adds trainable mapping layers that bridge the decoders from models of different versions for feature remapping.
The remapped features will be used as guidance for the upgraded model.
To enhance the guidance ability of X-Adapter, we employ a null-text training strategy for the upgraded model.
After training, we also introduce a two-stage denoising strategy to align the initial latents of X-Adapter and the upgraded model.

Thanks to our strategies, X-Adapter demonstrates universal compatibility with various plugins and also enables plugins of different versions to work together,
thereby expanding the functionalities of diffusion community. To verify the effectiveness of the proposed method,
we conduct extensive experiments and the results show that X-Adapter may facilitate wider application in the upgraded foundational diffusion model.

## Pipeline


![](./static/image_X/xadapter_pipeline_v5.png)

Left, Training: 
We add different noises to both the upgraded model and X-Adapter under the latent domain of
base and upgraded model. By setting the prompt of the upgraded model to empty and training the mapping layers, X-Adapter learns to
guide the upgraded mode

Right, Inference: 
We provide two inference settings: (a) We can directly apply the plugins on the X-Adapter for the upgraded model. (b) A two-stage
influence scheme is introduced to improve image quality.

## Results

The showcases of different results on SDXL and SD 2.1 based on the proposed X-Adapter and pre-rained SD 1.5 plugins.
X-Adapter shows wide support for different plugins and foundation models.

![](./static/image_X/QualitativeResult.png)

We also provide extensive results:

![](./static/image_X/Supplemantary_v2_page-0001.jpg)

## BibTeX

```
@article{ran2023xadapter,
  author    = {Lingmin Ran and Xiaodong Cun and Jia-Wei Liu and Rui Zhao and Song Zijie and Xintao Wang and Jussi Keppo and Mike Zheng Shou},
  title     = {X-Adapter: Adding Universal Compatibility of Plugins for Upgraded Diffusion Model},
  journal   = {arXiv preprint arxiv:2312.02238},
  year      = {2023},
}
```

This website is borrowed from [nerfies](https://github.com/nerfies/nerfies.github.io/tree/main). We are very grateful for their work.
