# TokenFlow: Consistent Diffusion Features for Consistent Video Editing
Source: https://diffusion-tokenflow.github.io/
TokenFlow: Consistent Diffusion Features for Consistent Video Editing



# TokenFlow: Consistent Diffusion Features for Consistent Video Editing

[Michal Geyer](https://michalgeyer.my.canva.site/)\*,

[Omer Bar-Tal](https://omerbt.github.io)\*,

[Shai Bagon](https://www.weizmann.ac.il/math/bagon/home),

[Tali Dekel](https://www.weizmann.ac.il/math/dekel/)

Weizmann institute of science
  
\*Indicates Equal Contribution

ICLR 2024

[Paper](./TokenFlow_Arxiv.pdf)


[Supplementary](sm/supp.html)


[Code](https://github.com/omerbt/TokenFlow)


[![Hugging Face Demo](static/images/hf.png)
Demo](https://huggingface.co/spaces/weizmannscience/tokenflow)


[arXiv](https://arxiv.org/abs/2307.10373)

[



](final_very_compressed.mp4)



## Abstract

The generative AI revolution has been recently expanded
to videos. Nevertheless, current state-of-the-art video models are still lagging behind image models in terms of visual
quality and user control over the generated content. In this
work, we present a framework that harnesses the power of
a text-to-image diffusion model for the task of text-driven
video editing. Specifically, given a source video and a target
text-prompt, our method generates a high-quality video that
adheres to the target text, while preserving the spatial layout and dynamics of the input video. Our method is based
on our key observation that consistency in the edited video
can be obtained by enforcing consistency in the diffusion
feature space. We achieve this by explicitly propagating
diffusion features based on inter-frame correspondences,
readily available in the model. Thus, our framework does
not require any training or fine-tuning, and can work in conjunction with any off-the-shelf text-to-image editing method.
We demonstrate state-of-the-art editing results on a variety
of real-world videos.



## Method

|  |  |  |
| --- | --- | --- |
| We observe that the level of temporal consistency of a video is tightly related to the temporal consistency of its feature representation, as can be seen in the feature visualization below. The features of a natural video have a shared, temporally consistent representation. When editing the video per frame, this consistency breaks. Our method ensures the same level of feature consistency as in the original video features. | | |
| Original | Per Frame Editing | Ours |
|  |  |  |
|  |  |  |
| Our key finding is that a temporally-consistent edit can be achieved by enforcing consistency on the internal diffusion features across frames during the editing process. We achieve this by propagating a small set of edited features across frames, using the correspondences between the original video features. Given an input video I, we invert each frame, extract its tokens (i.e., output features from the self-attention modules), and extract inter-frame feature correspondences using a nearest-neighbor (NN) search. At each denoising step:   (I) We sample keyframes from the noisy video J\_t and jointly edit them using an extended-attention block. The set of resulting edited tokens is T\_base.   (II) We propagate the edited tokens across the video according to the pre-computed correspondences of the original video features. To denoise J\_t, we feed each frame to the network and replace the generated tokens with the tokens obtained from the propagation step (II). | | |

![](pics/pipeline.png)



## TokenFlow Editing results

Hover over the videos to see the original video and text prompts.

[ ](videos/results/bread/input_fps20.mp4)
[](videos/results/bread/result_fps_20.mp4)

an ice sculpture

[ ](videos/results/wolf-part/input_fps20.mp4)
[](videos/results/wolf-part/result_fps_20.mp4)

a robotic wolf

[ ](videos/results/woman-running/input_fps30.mp4)
[](videos/results/woman-running/marble.mp4)

a marble sculpture

  

[ ](videos/results/poodle_2/input_fps30.mp4)
[](videos/results/poodle_2/result_fps_30.mp4)

Van Gogh painting

[ ](videos/results/stork/origami.mp4)
[](videos/results/stork/input_fps30.mp4)

an origami of a stork

  

[ ](videos/results/tesla/result_fps_30.mp4)
[](videos/results/tesla/input_fps30.mp4)

a car made of ice on an icy road

[ ](videos/results/gen1-face/input_fps30.mp4)
[](videos/results/gen1-face/result_fps30.mp4)

Van Gogh painting

  

[ ](videos/results/man_basket/result_fps_30.mp4)
[](videos/results/man_basket/input_fps30.mp4)

a robot spinning a silver ball

[ ](videos/results/kittens/input_fps30.mp4)
[](videos/results/kittens/result_fps_30.mp4)

colorful crochet kittens



## Comparisons

Input video

Ours

Text-to-video [[1]](#ref-txt2vid)

Tune-a-video [[2]](#ref-TAV)

Gen-1 [[3]](#ref-gen1)

Per frame PnP[[4]](#ref-pnp)

Fate-Zero[[5]](#ref-fatezero)

Rerender-a-video[[6]](#ref-rerender)

[


](videos/compare/bread/input_fps20.mp4)
[


](videos/compare/bread/result_fps_20.mp4)
[


](videos/compare/bread/txt2vid_fps20.mp4)
[


](videos/compare/bread/tav_fps20.mp4)
[


](videos/compare/bread/gen1_fps20.mp4)
[


](videos/compare/bread/pnp_per_frame_baseline_fps_20.mp4)
[


](./sm/assets/bread/a shiny metal scultpture/fatezero_20_fps.mp4)
[


](./sm/assets/bread/a shiny metal scultpture/rerender_fps_20.mp4)

[


](videos/compare/poodle/input_fps30.mp4)
[


](videos/compare/poodle/result_fps_30.mp4)
[


](videos/compare/poodle/txt2vid_fps30.mp4)
[


](videos/compare/poodle/tav_fps30.mp4)
[


](videos/compare/poodle/gen1_fps30.mp4)
[


](videos/compare/poodle/pnp_per_frame_baseline_fps_30.mp4)
[


](./sm/assets/poodle/a dog with a rainbow texture/fatezero_30_fps.mp4)
[


](./sm/assets/poodle/a dog with a rainbow texture/rerender_fps_30.mp4)



## BibTeX

```
@article{tokenflow2023,
        title = {TokenFlow: Consistent Diffusion Features for Consistent Video Editing},
        author = {Geyer, Michal and Bar-Tal, Omer and Bagon, Shai and Dekel, Tali},
        journal={arXiv preprint arxiv:2307.10373},
        year={2023}
        }
```

[1] Levon Khachatryan, Andranik Movsisyan, Vahram Tadevosyan, Roberto Henschel, Zhangyang Wang, Shant Navasardyan, and Humphrey Shi. Text2video-zero: Text-to-image diffusion models are zero-shot video generators. arXiv preprint arXiv:2303.13439, 2023.

[2] Jay Zhangjie Wu, Yixiao Ge, Xintao Wang, Stan Weixian
Lei, Yuchao Gu, Wynne Hsu, Ying Shan, Xiaohu Qie, and
Mike Zheng Shou. Tune-a-video: One-shot tuning of image
diffusion models for text-to-video generation. arXiv preprint
arXiv:2212.11565, 2022

[3] Patrick Esser, Johnathan Chiu, Parmida Atighehchian,
Jonathan Granskog, and Anastasis Germanidis. Structure
and content-guided video synthesis with diffusion models.
arXiv preprint arXiv:2302.03011, 2023

[4] Narek Tumanyan, Michal Geyer, Shai Bagon, and
Tali Dekel. Plug-and-play diffusion features for text-
driven image-to-image translation. Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2023

This page was built using the [Academic Project Page Template](https://github.com/eliahuhorwitz/Academic-project-page-template).
You are free to borrow the of this website, we just ask that you link back to this page in the footer.   
 This website is licensed under a [Creative
Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).
