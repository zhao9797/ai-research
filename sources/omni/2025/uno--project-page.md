# Less-to-More Generalization: Unlocking More Controllability by In-Context Generation
Source: https://bytedance.github.io/UNO/
Less-to-More Generalization: Unlocking More Controllability by In-Context Generation



# Icon **UNO** **Less-to-More** **Generalization:** **Unlocking More Controllability by In-Context Generation** Shaojin Wu  Mengqi Huang\*  Wenxu Wu  Yufeng Cheng  Fei Ding+  Qian He Intelligent Creation Team, ByteDance [Paper](https://huggingface.co/papers/2504.02160) [arXiv](https://arxiv.org/abs/2504.02160) [Code](https://github.com/bytedance/UNO) [SVG Icon Model](https://huggingface.co/bytedance-research/UNO) [SVG Icon Demo](https://huggingface.co/spaces/bytedance-research/UNO-FLUX)

![Image 0](static/uno_files/teaser/1.webp)
![Image 0](static/uno_files/teaser/2.webp)
![Image 0](static/uno_files/teaser/3.webp)
![Image 0](static/uno_files/teaser/4.webp)
![Image 0](static/uno_files/teaser/5.webp)
![Image 0](static/uno_files/teaser/6.webp)
![Image 0](static/uno_files/teaser/7.webp)
![Image 0](static/uno_files/teaser/8.webp)

![Image 0](static/uno_files/teaser/1.webp)
![Image 0](static/uno_files/teaser/2.webp)
![Image 0](static/uno_files/teaser/3.webp)
![Image 0](static/uno_files/teaser/4.webp)
![Image 0](static/uno_files/teaser/5.webp)
![Image 0](static/uno_files/teaser/6.webp)
![Image 0](static/uno_files/teaser/7.webp)
![Image 0](static/uno_files/teaser/8.webp)

We introduce **UNO**, a universal framework that evolves from single-subject to multi-subject customization. **UNO** demonstrates strong generalization capabilities and is capable of unifying diverse tasks under **one model**.

## **What can UNO do?**

  

[

](static/uno_files/teaser/teaser_medium.mp4)

  

## **Abstract**

  

Although subject-driven generation has been extensively explored
in image generation due to its wide applications, it still has challenges
in data scalability and subject expansibility. For the first challenge, moving
from curating single-subject datasets to multiple-subject ones and scaling
them is particularly difficult. For the second, most recent methods center
on single-subject generation, making it hard to apply when dealing with
multi-subject scenarios. In this study, we propose a highly-consistent data
synthesis pipeline to tackle this challenge. This pipeline harnesses the
intrinsic in-context generation capabilities of diffusion transformers and
generates high-consistency multi-subject paired data. Additionally, we
introduce **UNO**, which consists of progressive cross-modal alignment and
universal rotary position embedding. It is a multi-image conditioned subject-to-image
model iteratively trained from a text-to-image model. Extensive experiments show that
our method can achieve high consistency while ensuring controllability in both single-subject
and multi-subject driven generation.

  

## **How does it work?**

  
![](static/uno_files/method/uno.webp)
  

It introduces two pivotal enhancements to the model:
progressive cross-modal alignment and universal rotary position embedding(UnoPE).
The progressive cross-modal alignment is divided into two stages. In the Stage I,
we use single-subject in-context generated data to finetune the pretrained T2I model
into an S2I model. In the Stage II, we continue training on generated
multiple-subject data pairs. The UnoPE can effectively equip UNO with the capability
of mitigating the attribute confusion issue when scaling visual subject controls.

  

## **Generalization Capabilities**

  


![Image 1](static/uno_files/slider/general/1.webp)
![Image 2](static/uno_files/slider/general/2.webp)
![Image 3](static/uno_files/slider/general/3.webp)
![Image 4](static/uno_files/slider/general/4.webp)
![Image 5](static/uno_files/slider/general/5.webp)
![Image 6](static/uno_files/slider/general/6.webp)
![Image 7](static/uno_files/slider/general/7.webp)
![Image 8](static/uno_files/slider/general/8.webp)

![Image 1](static/uno_files/slider/general/1.webp)
![Image 2](static/uno_files/slider/general/2.webp)
![Image 3](static/uno_files/slider/general/3.webp)
![Image 4](static/uno_files/slider/general/4.webp)
![Image 5](static/uno_files/slider/general/5.webp)
![Image 6](static/uno_files/slider/general/6.webp)
![Image 7](static/uno_files/slider/general/7.webp)
![Image 8](static/uno_files/slider/general/8.webp)

![Image 1](static/uno_files/slider/stylize/1.webp)
![Image 2](static/uno_files/slider/stylize/2.webp)
![Image 3](static/uno_files/slider/stylize/3.webp)
![Image 4](static/uno_files/slider/stylize/4.webp)
![Image 5](static/uno_files/slider/stylize/5.webp)
![Image 6](static/uno_files/slider/stylize/6.webp)

![Image 1](static/uno_files/slider/stylize/1.webp)
![Image 2](static/uno_files/slider/stylize/2.webp)
![Image 3](static/uno_files/slider/stylize/3.webp)
![Image 4](static/uno_files/slider/stylize/4.webp)
![Image 5](static/uno_files/slider/stylize/5.webp)
![Image 6](static/uno_files/slider/stylize/6.webp)

![Image 1](static/uno_files/slider/tryon/1.webp)
![Image 2](static/uno_files/slider/tryon/2.webp)
![Image 3](static/uno_files/slider/tryon/3.webp)
![Image 4](static/uno_files/slider/tryon/4.webp)
![Image 5](static/uno_files/slider/tryon/5.webp)
![Image 6](static/uno_files/slider/tryon/6.webp)
![Image 7](static/uno_files/slider/tryon/7.webp)
![Image 8](static/uno_files/slider/tryon/8.webp)
![Image 9](static/uno_files/slider/tryon/9.webp)

![Image 1](static/uno_files/slider/tryon/1.webp)
![Image 2](static/uno_files/slider/tryon/2.webp)
![Image 3](static/uno_files/slider/tryon/3.webp)
![Image 4](static/uno_files/slider/tryon/4.webp)
![Image 5](static/uno_files/slider/tryon/5.webp)
![Image 6](static/uno_files/slider/tryon/6.webp)
![Image 7](static/uno_files/slider/tryon/7.webp)
![Image 8](static/uno_files/slider/tryon/8.webp)
![Image 9](static/uno_files/slider/tryon/9.webp)

![Image 1](static/uno_files/slider/identity/1.webp)
![Image 2](static/uno_files/slider/identity/2.webp)
![Image 3](static/uno_files/slider/identity/3.webp)
![Image 4](static/uno_files/slider/identity/4.webp)
![Image 5](static/uno_files/slider/identity/5.webp)
![Image 6](static/uno_files/slider/identity/6.webp)

![Image 1](static/uno_files/slider/identity/1.webp)
![Image 2](static/uno_files/slider/identity/2.webp)
![Image 3](static/uno_files/slider/identity/3.webp)
![Image 4](static/uno_files/slider/identity/4.webp)
![Image 5](static/uno_files/slider/identity/5.webp)
![Image 6](static/uno_files/slider/identity/6.webp)

![Image 7](static/uno_files/slider/combined/7.webp)
![Image 8](static/uno_files/slider/combined/8.webp)
![Image 9](static/uno_files/slider/combined/9.webp)
![Image 1](static/uno_files/slider/combined/1.webp)
![Image 2](static/uno_files/slider/combined/2.webp)
![Image 3](static/uno_files/slider/combined/3.webp)
![Image 4](static/uno_files/slider/combined/4.webp)
![Image 5](static/uno_files/slider/combined/5.webp)
![Image 6](static/uno_files/slider/combined/6.webp)

![Image 7](static/uno_files/slider/combined/7.webp)
![Image 8](static/uno_files/slider/combined/8.webp)
![Image 9](static/uno_files/slider/combined/9.webp)
![Image 1](static/uno_files/slider/combined/1.webp)
![Image 2](static/uno_files/slider/combined/2.webp)
![Image 3](static/uno_files/slider/combined/3.webp)
![Image 4](static/uno_files/slider/combined/4.webp)
![Image 5](static/uno_files/slider/combined/5.webp)
![Image 6](static/uno_files/slider/combined/6.webp)

  

## **Comparison with State-of-the-Art Methods**

  
![](static/uno_files/comparison/singleIP.webp)
  
  
![](static/uno_files/comparison/multiIP.webp)
  
  
![](static/uno_files/comparison/multiIPmore.webp)

## **Disclaimer**

  

We open-source this project for academic research. The vast majority of images
used in this project are either generated or licensed. If you have any concerns,
please contact us, and we will promptly remove any inappropriate content.
Our code is released under the Apache 2.0 License,, while our models are under
the CC BY-NC 4.0 License. Any models related to [FLUX.1-dev](https://huggingface.co/black-forest-labs/FLUX.1-dev)
base model must adhere to the original licensing terms.
  
  
This research aims to advance the field of generative AI. Users are free to
create images using this tool, provided they comply with local laws and exercise
responsible usage. The developers are not liable for any misuse of the tool by users.

### BibTex

  

@article{wu2025less,  
  title={Less-to-More Generalization: Unlocking More Controllability by In-Context Generation},  
  author={Wu, Shaojin and Huang, Mengqi and Wu, Wenxu and Cheng, Yufeng and Ding, Fei and He, Qian},  
  journal={arXiv preprint arXiv:2504.02160},  
  year={2025}  
}

  
  

Source code of the project page can be found in
[UNO Github Pages](https://github.com/bytedance/UNO/tree/gh-pages).

  
