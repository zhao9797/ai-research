# FramePack
Source: https://lllyasviel.github.io/frame_pack_gitpage/
FramePack



![](img/logo.png)

  

# Frame Context Packing and Drift Prevention in Next-Frame-Prediction Video Diffusion Models

[Lvmin Zhang](https://github.com/lllyasviel)

[Shengqu Cai](https://primecai.github.io/)

[Muyang Li](https://lmxyy.me/)

[Gordon Wetzstein](https://stanford.edu/~gordonwz/)

[Maneesh Agrawala](https://graphics.stanford.edu/~maneesh/)

Stanford University, MIT

[Paper](https://arxiv.org/abs/2504.12626)
[Code](https://github.com/lllyasviel/FramePack)
[FramePack-P1 Preview](https://lllyasviel.github.io/frame_pack_gitpage/p1)

# FramePack

* Diffuse thousands of frames at full fps-30 with 13B models using 6GB laptop GPU memory.
* Finetune 13B video model at batch size 64 on a single 8xA100/H100 node for personal/lab
  experiments.
* Personal RTX 4090 generates at speed 2.5 seconds/frame (unoptimized) or 1.5 seconds/frame
  (teacache).
* No timestep distillation.
* **Video diffusion, but feels like image diffusion.**

# Understand FramePack in 5 seconds

A next-frame (or next-frame-section) prediction model looks like this:

![](img/nfp.png)

  

So we have many input frames and want to diffuse some new frames.

The idea is that we can encode the input frames to some GPU layout like this:

![](img/gpu.png)

  

This chart shows the logical **GPU memory layout** - frames images are not stitched.

Or, say the context length of each input frame.

Each frame is encoded with different patchifying kernel to achieve this.

For example, in HunyuanVideo, a 480p frame is likely 1536 tokens if using (1, 2, 2) patchifying
kernel.

Then, if changed to (2, 4, 4) patchifying kernel, a frame is 192 tokens.

In this way, we can change the context length of each frame.

The "more important" frames are given more GPU resources (context length) - in this example, F0 is
the most important as it is the nearest frame to the "next-frame prediction" target.

This is O(1) computation complexity for streaming - Yes, a constant, not even O(nlogn) or O(n).

# But wait, what if ...

The above idea is a very brief concept - many questions can be asked like:

What if the importance of frames does not follow this simple pattern?

What if I want different compression rate?

If I want image-to-video, isn't the first frame most important?

What if I have some user frames and I want those frames to be more important?

...

Great - In fact these are **FramePack Scheduling**, like these:

![](img/ab.png)

  

So one can get different compression patterns.

One can even make the starting frames equally important so image-to-video will be happier.

And all those schedulings are O(1).

We have a detailed evaluation of many schedulings in the paper!

# Anti-drifting Sampling

Drifting is a common problem of any next-what-what prediction model.

Drifting refers to the quality degradation as the video becomes longer.

Sometimes the problem is also called error accumulation or exposure bias.

To see an example, you can find an arbitrary image-to-video model and
try to generate long videos by repeatedly using the last generated frame as inputs. The result will
mess up quickly after you do this 5 or 6 times, and everything will severely degrade after you do
this about 10 times.

See also our paper for some experiments on existing methods like history noise augmentation, special cfg
guidance, rolling diffusion timesteps, and so on. We find out that, to solve drifting
fundamentally, we need to break causality and make the sampling bi-directional.

Consider these sampling methods:

![](img/sample.png)

(the shadowed squares are the frames generated in each streaming inference)

Note that only the "vanilla sampling" is causal.

Both the "anti-drifting sampling" and "inverted anti-drifting sampling" are bi-directional.

The "inverted anti-drifting sampling" is important. This method is the only one that always treats
the first frame as an approximation target in all inferences. This method is very suitable for
image-to-video.

# Image-to-5-Seconds (30fps, 150 frames)

All results are computed by RTX 3060 6GB laptop with 13B HY variant. (Videos compressed by h264crf18
to fit in GitHub repos.)

![](short/250413_161404_333_9374.png)

[

](short/250413_161404_333_9374_37.mp4)

![](short/250413_162544_300_6887.png)

[

](short/250413_162544_300_6887_37.mp4)

![](short/250413_163713_287_6141.png)

[

](short/250413_163713_287_6141_37.mp4)

![](short/250413_164153_018_3707.png)

[

](short/250413_164153_018_3707_37.mp4)

![](short/250413_165330_476_4350.png)

[

](short/250413_165330_476_4350_37.mp4)

![](short/250413_171501_349_5557.png)

[

](short/250413_171501_349_5557_37.mp4)

![](short/250413_171845_794_5710.png)

[

](short/250413_171845_794_5710_37.mp4)

![](short/250413_172227_789_1156.png)

[

](short/250413_172227_789_1156_37.mp4)

![](short/250413_172857_135_4041.png)

[

](short/250413_172857_135_4041_37.mp4)

![](short/250413_174656_495_6007.png)

[

](short/250413_174656_495_6007_37.mp4)

![](short/250413_175022_873_9919.png)

[

](short/250413_175022_873_9919_37.mp4)

![](short/250413_175839_722_4670.png)

[

](short/250413_175839_722_4670_37.mp4)

![](short/250413_180317_651_14.png)

[

](short/250413_180317_651_14_37.mp4)

![](short/250413_181002_054_8480.png)

[

](short/250413_181002_054_8480_37.mp4)

![](short/250413_182531_529_4247.png)

[

](short/250413_182531_529_4247_37.mp4)

![](short/250413_183049_986_4301.png)

[

](short/250413_183049_986_4301_37.mp4)

# Image-to-60-Seconds (30fps, 1800 frames)

All results are computed by RTX 3060 laptop 6GB with 13B HY variant. (Videos compressed by h264crf18
to fit in GitHub repos.)

![](long/250415_173937_297_5230.png)

[

](long/250415_173937_297_5230_451.mp4)

0:00 / 0:00

![](long/250415_182916_672_932.png)

[

](long/250415_182916_672_932_451.mp4)

0:00 / 1:00

![](long/250415_192014_068_6988.png)

[

](long/250415_192014_068_6988_451.mp4)

0:00 / 1:00

![](long/250415_204057_909_7054.png)

[

](long/250415_204057_909_7054_451.mp4)

0:00 / 0:00

![](long/250415_223642_164_2957.png)

[

](long/250415_223642_164_2957_451.mp4)

0:00 / 0:00

![](long/250416_054034_292_5971.png)

[

](long/250416_054034_292_5971_451.mp4)

0:00 / 0:00

# BibTeX

```
@inproceedings{zhang2025framepack,
    title={Frame Context Packing and Drift Prevention in Next-Frame-Prediction Video Diffusion Models},
    author={Lvmin Zhang and Shengqu Cai and Muyang Li and Gordon Wetzstein and Maneesh Agrawala},
    booktitle={The Thirty-ninth Annual Conference on Neural Information Processing Systems},
    year={2025},
}

@article{zhang2025framepackv1,
    title={Packing Input Frame Contexts in Next-Frame Prediction Models for Video Generation},
    author={Lvmin Zhang and Maneesh Agrawala},
    journal={Arxiv},
    year={2025}
}
```

# See also

[Pretraining Frame Preservation in Autoregressive Video Memory Compression](https://arxiv.org/abs/2512.23851)
  
Lvmin Zhang, Shengqu Cai, Muyang Li, Chong Zeng, Beijia Lu, Anyi Rao, Song Han, Gordon Wetzstein, Maneesh Agrawala

Thanks DSINE for the website template. Most input images are from Midjourney.
