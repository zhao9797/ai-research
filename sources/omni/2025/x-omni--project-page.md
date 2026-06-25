# X-Omni
Source: https://x-omni-team.github.io/
X-Omni



# X-Omni: Reinforcement Learning Makes Discrete Autoregressive Image Generative Models Great Again

Zigang Geng\*,
Yibing Wang\*,
Yeyao Ma,
Chen Li,
Yongming Rao,
Shuyang Gu,
Zhao Zhong,
Qinglin Lu,
Han Hu‡,
Xiaosong Zhang†,
Linus,
Di Wang,
Jie Jiang

Tencent Hunyuan X
  
\*Indicates Equal contribution
†Indicates Project Lead
‡Indicates Corresponding Author

[Paper](https://arxiv.org/pdf/2507.22058)


[Code](https://github.com/X-Omni-Team/X-Omni)


[![Hugging Face Model](https://huggingface.co/front/assets/huggingface_logo-noborder.svg)
Model](https://huggingface.co/collections/X-Omni/x-omni-models-6888aadcc54baad7997d7982)


[Space](https://huggingface.co/collections/X-Omni/x-omni-spaces-6888c64f38446f1efc402de7)


[![LongText-Bench](https://huggingface.co/front/assets/huggingface_logo-noborder.svg)
LongText-Bench](https://huggingface.co/datasets/X-Omni/LongText-Bench)

![MY ALT TEXT](static/images/fig2-1.png)



## Abstract

Numerous efforts have been made to extend the ``next token prediction'' paradigm to visual contents, aiming to create a unified approach for both image generation and understanding. Nevertheless, attempts to generate images through autoregressive modeling with discrete tokens have been plagued by issues such as low visual fidelity, distorted outputs, and failure to adhere to complex instructions when rendering intricate details. These shortcomings are likely attributed to cumulative errors during auto-regressive inference or information loss incurred during the discretization process. Probably due to this challenge, recent research has increasingly shifted toward jointly training image generation with diffusion objectives and language generation with auto-regressive objectives, moving away from unified modeling approaches. In this work, we demonstrate that reinforcement learning can effectively mitigate artifacts and largely enhance the generation quality of a discrete auto-regressive modeling method, thereby enabling seamless integration of image and language generation. Our framework comprises a semantic image tokenizer, a unified auto-regressive model for both language and images, and an offline diffusion decoder for image generation, termed X-Omni. X-Omni achieves state-of-the-art performance in image generation tasks using a 7B language model, producing images with high aesthetic quality while exhibiting strong capabilities in following instructions and rendering long texts.



## X-Omni is a unified discrete autoregressive model for both image and language modalities.

![MY ALT TEXT](static/images/fig5-1.png)



![MY ALT TEXT](static/images/fig1-1.png)



## BibTeX

```
    @article{geng25xomni,
      author       = {Zigang Geng and
                      Yibing Wang and
                      Yeyao Ma and
                      Chen Li and
                      Yongming Rao and
                      Shuyang Gu and
                      Zhao Zhong and
                      Qinglin Lu and
                      Han Hu and
                      Xiaosong Zhang and
                      Linus and
                      Di Wang and
                      Jie Jiang},
      title        = {X-Omni: Reinforcement Learning Makes Discrete Autoregressive Image Generative Models Great Again},
      journal      = {CoRR},
      volume       = {abs/2507.22058},
      year         = {2025},
    }
```



This page was built using the [Academic Project Page Template](https://github.com/eliahuhorwitz/Academic-project-page-template) which was adopted from the [Nerfies](https://nerfies.github.io) project page.
You are free to borrow the source code of this website, we just ask that you link back to this page in the footer.   
 This website is licensed under a [Creative
Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).
