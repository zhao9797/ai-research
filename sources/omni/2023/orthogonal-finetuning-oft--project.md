# Controlling Text-to-Image Diffusion by Orthogonal Finetuning
Source: https://oft.wyliu.com/
Controlling Text-to-Image Diffusion by Orthogonal Finetuning



# Controlling Text-to-Image Diffusion by Orthogonal Finetuning

[Zeju Qiu](https://github.com/Zeju1997)1,\*,

[Weiyang Liu](https://wyliu.com/)1,2,\*,⚑,

[Haiwen Feng](https://ps.is.mpg.de/person/hfeng)1,

[Yuxuan Xue](https://virtualhumans.mpi-inf.mpg.de/people/Xue.html)3,

[Yao Feng](https://github.com/yfeng95)1,

[Zhen Liu](http://itszhen.com/)1,4,

[Dan Zhang](https://scholar.google.de/citations?user=yazO-mMAAAAJ&hl=en)3,

[Adrian Weller](https://mlg.eng.cam.ac.uk/adrian/)2,5,

[Bernhard Schölkopf](https://is.mpg.de/~bs)1

1Max Planck Institute for Intelligent Systems - Tübingen,
2University of Cambridge,
3University of Tübingen,
4Mila, Université de Montréal,
5The Alan Turing Institute

\*Equal contribution,
⚑Project lead

[Paper](./static/files/oft_v2.pdf)

[arXiv](https://arxiv.org/abs/2306.07280)



[Code](https://github.com/Zeju1997/oft)

## Accepted to **NeurIPS 2023**!

![](./static/images/teaser.png)

## OFT can effectively and stably finetune text-to-image diffusion models.

## Abstract

Large text-to-image diffusion models have impressive capabilities in generating photorealistic images from text prompts. How to effectively guide or control these powerful models to perform different downstream tasks becomes an important open problem. To tackle this challenge, we introduce a principled finetuning method -- Orthogonal Finetuning (OFT), for adapting text-to-image diffusion models to downstream tasks. Unlike existing methods, OFT can provably preserve hyperspherical energy which characterizes the pairwise neuron relationship on the unit hypersphere. We find that this property is crucial for preserving the semantic generation ability of text-to-image diffusion models. To improve finetuning stability, we further propose Constrained Orthogonal Finetuning (COFT) which imposes an additional radius constraint to the hypersphere.

Specifically, we consider two important finetuning text-to-image tasks: subject-driven generation where the goal is to generate subject-specific images given a few images of a subject and a text prompt, and controllable generation where the goal is to enable the model to take in additional control signals. We empirically show that our OFT framework outperforms existing methods in generation quality and convergence speed.

## How OFT works

![](./static/images/oft_method.png)

The basic idea is to finetune the pretrained weight matrices with orthogonal transform. More specifically, we transform all the neurons in the same layer with one orthogonal matrix, such that the relative angle between any pairwise neurons stays unchanged. Such a property can perfectly preserve the hyperspherical energy among the neurons. The preservation of hyperspherical energy can effectively prevent model collapse.

## Qualitative results

### Subject-driven generation

![](./static/images/dreambooth.png)

  

![](./static/images/db_app-1.png)

  

### Controllable generation

![](./static/images/control.png)

  

![](./static/images/segm2img_app-1.png)

## BibTeX

```
@InProceedings{Qiu2023OFT,
      title = {Controlling Text-to-Image Diffusion by Orthogonal Finetuning},
      author = {Qiu, Zeju and Liu, Weiyang and Feng, Haiwen and Xue, Yuxuan and Feng, Yao and Liu, Zhen and Zhang, Dan and Weller, Adrian and Sch{\"o}lkopf, Bernhard},
      booktitle = {NeurIPS},
      year = {2023}
}
```

Website template from [here](https://github.com/nerfies/nerfies.github.io).
