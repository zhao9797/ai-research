# Animate Anyone
Source: https://humanaigc.github.io/animate-anyone/
Animate Anyone




More Research

[OutfitAnyone](https://humanaigc.github.io/outfit-anyone/)
[Cloth2Tex](https://tomguluson92.github.io/projects/cloth2tex/)
[VividTalk](https://humanaigc.github.io/vivid-talk/)

# Animate Anyone: Consistent and Controllable Image-to-Video Synthesis for Character Animation

[Li Hu](https://scholar.google.com/citations?view_op=list_works&hl=zh-CN&user=Arz3iGUAAAAJ&gmla=AJsN-F72u4R_vwVl2Jc0Sy_qIYuSwExx8ilpfrd-w5Yfi5FYFP_WhbJtHbAK_c5w-3KNBgTRjWiTvEFLtJSV5ryd1JuNVQdMVDMuSJS5dfn7NWbZQQpGGyyxlrfoq6cv6S_23QTSUWWY),

[Xin Gao](https://scholar.google.com/citations?user=cze1sXQAAAAJ&hl=en),

[Peng Zhang](https://scholar.google.com/citations?user=QTgxKmkAAAAJ&hl=zh-CN),

[Ke Sun](https://dblp.org/pid/69/476-9.html),

[Bang Zhang](https://dblp.org/pid/11/4046.html),

[Liefeng Bo](https://scholar.google.com/citations?user=FJwtMf0AAAAJ&hl=zh-CN)

Institute for Intelligent Computing，Alibaba Group

[Paper](https://arxiv.org/pdf/2311.17117.pdf)


[video](https://www.youtube.com/watch?v=8PCn5hLKNu4)


[Code](https://github.com/HumanAIGC/AnimateAnyone)


[arXiv](https://arxiv.org/pdf/2311.17117.pdf)

[


](static/videos/teaser1.mp4)



## Abstract

Character Animation aims to generating character videos from still images through driving signals. Currently, diffusion models have become the mainstream in visual generation research, owing to their robust generative capabilities. However, challenges persist in the realm of image-to-video, especially in character animation, where temporally maintaining consistency with detailed information from character remains a formidable problem. In this paper, we leverage the power of diffusion models and propose a novel framework tailored for character animation. To preserve consistency of intricate appearance features from reference image, we design ReferenceNet to merge detail features via spatial attention. To ensure controllability and continuity, we introduce an efficient pose guider to direct character's movements and employ an effective temporal modeling approach to ensure smooth inter-frame transitions between video frames. By expanding the training data, our approach can animate arbitrary characters, yielding superior results in character animation compared to other image-to-video methods. Furthermore, we evaluate our method on benchmarks for fashion video and human dance synthesis, achieving state-of-the-art results.



## Video



## Method

![MY ALT TEXT](static/images/f2_img.png)

## The overview of our method. The pose sequence is initially encoded using Pose Guider and fused with multi-frame noise, followed by the Denoising UNet conducting the denoising process for video generation. The computational block of the Denoising UNet consists of Spatial-Attention, Cross-Attention, and Temporal-Attention, as illustrated in the dashed box on the right. The integration of reference image involves two aspects. Firstly, detailed features are extracted through ReferenceNet and utilized for Spatial-Attention. Secondly, semantic features are extracted through the CLIP image encoder for Cross-Attention. Temporal-Attention operates in the temporal dimension. Finally, the VAE decoder decodes the result into a video clip.



## Animating Various Characters

## Human

[\

](static/videos/demo6.mp4)

[\

](static/videos/demo5.mp4)

[\

](static/videos/demo4.mp4)

[


](static/videos/demo11.mp4)

[


](static/videos/demo12.mp4)

[\

](static/videos/demo13.mp4)

[\

](static/videos/demo15.mp4)

[\

](static/videos/demo17.mp4)

[\

](static/videos/demo18.mp4)

[\

](static/videos/demo6.mp4)

[\

](static/videos/demo5.mp4)

[\

](static/videos/demo4.mp4)

[


](static/videos/demo11.mp4)

[


](static/videos/demo12.mp4)

[\

](static/videos/demo13.mp4)

[\

](static/videos/demo15.mp4)

[\

](static/videos/demo17.mp4)

[\

](static/videos/demo18.mp4)

[\

](static/videos/demo6.mp4)

[\

](static/videos/demo5.mp4)

[\

](static/videos/demo4.mp4)

[


](static/videos/demo11.mp4)

[


](static/videos/demo12.mp4)



## Anime/Cartoon

[\

](static/videos/demo8.mp4)

[\

](static/videos/demo3.mp4)

[\

](static/videos/demo9.mp4)

[


](static/videos/demo2.mp4)

[


](static/videos/demo1.mp4)

[\

](static/videos/demo7.mp4)

[\

](static/videos/demo8.mp4)

[\

](static/videos/demo3.mp4)

[\

](static/videos/demo9.mp4)

[


](static/videos/demo2.mp4)

[


](static/videos/demo1.mp4)

[\

](static/videos/demo7.mp4)

[\

](static/videos/demo8.mp4)

[\

](static/videos/demo3.mp4)

[\

](static/videos/demo9.mp4)

[


](static/videos/demo2.mp4)

[


](static/videos/demo1.mp4)



## Humanoid

[


](static/videos/demo14.mp4)

[


](static/videos/demo10.mp4)

[


](static/videos/demo19.mp4)

[


](static/videos/demo14.mp4)

[


](static/videos/demo10.mp4)

[


](static/videos/demo19.mp4)

[


](static/videos/demo14.mp4)

[


](static/videos/demo10.mp4)

[


](static/videos/demo19.mp4)

[


](static/videos/demo14.mp4)

[


](static/videos/demo10.mp4)



## Comparisons

## Fashion Video Synthesis

[\

](static/videos/ubc5.mp4)

[\

](static/videos/ubc6.mp4)

[


](static/videos/ubc1.mp4)

[


](static/videos/ubc2.mp4)

[\

](static/videos/ubc3.mp4)

[\

](static/videos/ubc4.mp4)

[\

](static/videos/ubc5.mp4)

[\

](static/videos/ubc6.mp4)

[


](static/videos/ubc1.mp4)

[


](static/videos/ubc2.mp4)

[\

](static/videos/ubc3.mp4)

[\

](static/videos/ubc4.mp4)

[\

](static/videos/ubc5.mp4)

[\

](static/videos/ubc6.mp4)

[


](static/videos/ubc1.mp4)

## Fashion Video Synthesis aims to turn fashion photographs into realistic, animated videos using a driving pose sequence. Experiments are conducted on the UBC fashion video dataset with same training data.



## Human Dance Generation

[


](static/videos/tik2.mp4)

[\

](static/videos/tik3.mp4)

[


](static/videos/tik1.mp4)

[


](static/videos/tik2.mp4)

[\

](static/videos/tik3.mp4)

[


](static/videos/tik1.mp4)

[


](static/videos/tik2.mp4)

[\

](static/videos/tik3.mp4)

[


](static/videos/tik1.mp4)

## Human Dance Generation focuses on animating images in real-world dance scenarios. Experiments are conducted on the TikTok dataset with same training data.



## More Applications

## Animate Anyone + Outfit Anyone

[


](static/videos/outfit_anyone.mp4)

## [Outfit Anyone](https://humanaigc.github.io/outfit-anyone): Ultra-high quality virtual try-on for Any Clothing and Any Person.



## Image to talking-head video

[


](static/videos/animated_portrait_3.mp4)

## Image to video (like Gen2) + talking head generation (out internal project based on [VividTalk](https://humanaigc.github.io/vivid-talk/))



## Inference Acceleration

Animate Anyone video generation workloads are accelerated by DeepGPU (AIACC) of Alibaba Cloud with immense performance uplift compare to the original pytorch + xformers solution without hurting the quality of generated videos. This helps inference workloads reduce around 30% waiting time for end users as well as operating cost which makes a better user experience and cost-effective AI solution. The chart below shows some details of performance numbers on Animate Anyone inference that accelerated by DeepGPU. As observed from the chart, 32 frames 832x640 resolution video generation duration in 1 step reduces from 2.45s to 1.75s on A10 GPU when the inference is powered by DeepGPU acceleration which achieves 40% performance gain, while on RTX6000 GPU, the number reduces from 2.8s to 2.25s, nearly 25% advantages over pytorch.

![inference acceleration](static/images/inf_acc.png)



## BibTeX

```
@article{hu2023animateanyone,
      title={Animate Anyone: Consistent and Controllable Image-to-Video Synthesis for Character Animation},
      author={Li Hu and Xin Gao and Peng Zhang and Ke Sun and Bang Zhang and Liefeng Bo},
      journal={arXiv preprint arXiv:2311.17117},
      website={https://humanaigc.github.io/animate-anyone/},
      year={2023}
}
```

This page was built using the [Template](https://github.com/eliahuhorwitz/Academic-project-page-template) which was adopted from the [Nerfies](https://nerfies.github.io) project page.
