# SDEdit Project Page
Source: https://sde-image-editing.github.io/
SDEdit Project Page



# SDEdit: Guided Image Synthesis and Editing with Stochastic Differential Equations



## [Chenlin Meng](https://cs.stanford.edu/~chenlin/)    [Yutong He](http://web.stanford.edu/~kellyyhe/)    [Yang Song](https://yang-song.github.io/)    [Jiaming Song](http://tsong.me/)    [Jiajun Wu](https://jiajunwu.com/)    [Jun-Yan Zhu](https://www.cs.cmu.edu/~junyanz/)    [Stefano Ermon](https://cs.stanford.edu/~ermon/)



## Stanford University     Carnegie Mellon University



## In ICLR 2022



## **[Paper](https://arxiv.org/abs/2108.01073) | [GitHub](https://github.com/ermongroup/SDEdit) | [Colab](https://colab.research.google.com/drive/1KkLS53PndXKQpPlS1iK-k1nRQYmlb4aO?usp=sharing)**

  

SDEdit is an image synthesis and editing framework based on stochastic differential equations (SDEs) or diffusion models. SDEdit allows stroke-based image synthesis, stroke-based image editing and image compositing without task specific optimization. SDEdit can be directly plugged into off-the-shelf pre-trained score-based or diffusion models. Recently, SDEdit has also been applied to text-guided image editing with large-scale text-to-image models. Notable examples include [Stable Diffusion](https://en.wikipedia.org/wiki/Stable_Diffusion)'s img2img function (see [here](https://github.com/CompVis/stable-diffusion#image-modification-with-stable-diffusion)), [GLIDE](https://arxiv.org/abs/2112.10741), and [distilled-SD](https://arxiv.org/abs/2210.03142).

[![](images/teaser.jpg)](images/teaser.jpg)

[![](images/text_guided_img2img.png)](images/text_guided_img2img.png)

  
  

## Abstract

Guided image synthesis enables everyday users to create and edit photo-realistic images with minimum effort. The key challenge is balancing faithfulness to the user input (e.g., hand-drawn colored strokes) and realism of the synthesized image. Existing GAN-based methods attempt to achieve such balance using either conditional GANs or GAN inversions, which are challenging and often require additional training data or loss functions for individual applications. To address these issues, we introduce a new image synthesis and editing method, Stochastic Differential Editing (SDEdit), based on a diffusion model generative prior, which synthesizes realistic images by iteratively denoising through a stochastic differential equation (SDE). Given an input image with user guide of any type, SDEdit first adds noise to the input, then subsequently denoises the resulting image through the SDE prior to increase its realism. SDEdit does not require task-specific training or inversions and can naturally achieve the balance between realism and faithfulness. SDEdit significantly outperforms state-of-the-art GAN-based methods by up to 98.09% on realism and 91.72% on overall satisfaction scores, according to a human perception study, on multiple tasks, including stroke-based image synthesis and editing as well as image compositing.

[![paper thumbnail](images/paper_thumbnail.jpg)](https://arxiv.org/abs/2108.01073)
  

## Paper

[arXiv 2108.01073](https://arxiv.org/abs/2108.01073), 2021.

## Citation

Chenlin Meng, Yutong He, Yang Song, Jiaming Song, Jiajun Wu, Jun-Yan Zhu and Stefano Ermon. "SDEdit: Guided Image Synthesis and Editing with Stochastic Differential Equations". In International Conference on Learning Representations (ICLR) 2022.
  
[Bibtex](sdedit_bibtek.txt)

  
  
  

## Introducing SDEdit: a powerful image synthesis and editing technique

|  |
| --- |
| The key intuition of SDEdit is to "hijack" the reverse stochastic process of SDE-based generative models, as illustrated in the figure below. Given an input image for editing, such as a stroke painting or an image with strokes, we can add a suitable amount of noise to make its artifacts undetectable, while still preserving the overall structure of the image. We then initialize the reverse SDE with this noisy input, and simulate the reverse process to obtain a denoised image of high quality. Because the denoised image and the input resembles each other with noise perturbations, they also share the overall image structure. |
|  |

## Synthesizing images from strokes with SDEdit

|  |
| --- |
| Given an input stroke painting, our goal is to generate a realistic image that shares the same structure as the input when no paired data is available. We present stroke-based image synthesis with SDEdit on LSUN bedroom, LSUN church and CelebA-HQ datasets. We notice that SDEdit can generate multiple diverse images for each stroke painting. |
|  |

## Scribble-based image editing with SDEdit

|  |
| --- |
| Given an input with user added strokes, we want to generate a realistic image based on the user's edit. We observe that our method can generate image edits that are both realistic and faithful (to the user edit), while avoid making undesired modifications. (See the figure below.) |
|  |

## Image compositing with SDEdit

|  |
| --- |
| Given an image, users can specify how they want the edited image to look like using pixel patches copied from other reference images. Our goal is to generate a realistic image based on the user's edit. In the figure below, "original" stands for the orignal image, and "input" stands for an input designed by users. We observe that SDEdit can generate both faithful and realistic images with much lower LPIPS scores compared to GAN baselines. |
|  |

  
  

## Related Work

* Song, Yang, Jascha Sohl-Dickstein, Diederik P. Kingma, Abhishek Kumar, Stefano Ermon, and Ben Poole [**"Score-Based Generative Modeling through Stochastic Differential Equations"**](https://arxiv.org/abs/2011.13456), ICLR 2021.
* Song, Jiaming, Chenlin Meng, and Stefano Ermon [**"Denoising Diffusion Implicit Models"**](https://arxiv.org/abs/2010.02502), ICLR 2021.
* Song, Yang, and Stefano Ermon [**"Generative Modeling by Estimating Gradients of the Data Distribution"**](https://arxiv.org/abs/1907.05600),
  NeurIPS 2019.
* Song, Yang, and Stefano Ermon [**"Improved Techniques for Training Score-Based Generative Models"**](https://arxiv.org/abs/2006.09011),
  NeurIPS 2020.
* Ho, Jonathan, Ajay Jain, and Pieter Abbeel [**"Denoising Diffusion Probabilistic Models"**](https://arxiv.org/abs/2006.11239), NeurIPS 2020.
