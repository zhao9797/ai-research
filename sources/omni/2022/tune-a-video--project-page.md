# Tune-A-Video
Source: https://tuneavideo.github.io/
Tune-A-Video



Tune-A-Video: One-Shot Tuning of Image Diffusion Models for Text-to-Video Generation

ICCV 2023

[Jay Zhangjie Wu](https://zhangjiewu.github.io/)1

[Yixiao Ge](https://geyixiao.com/)3

[Xintao Wang](https://xinntao.github.io/)3

Stan Weixian Lei1

[Yuchao Gu](https://ycgu.site/)1

Yufei Shi1

[Wynne Hsu](https://www.comp.nus.edu.sg/~whsu/)2

[Ying Shan](https://scholar.google.com/citations?user=4oXBp9UAAAAJ&hl=en)3

[Xiaohu Qie](https://scholar.google.com/citations?user=mk-F69UAAAAJ&hl=en)4

[Mike Zheng Shou](https://sites.google.com/view/showlab)1

1[Show Lab](https://sites.google.com/view/showlab),2National University of Singapore
3[ARC Lab](https://arc.tencent.com/en/index),4Tencent PCG

[[Paper (arXiv)]](https://arxiv.org/abs/2212.11565)
[[Code (Github)]](https://github.com/showlab/Tune-A-Video)
[[Demo (Colab)]](https://colab.research.google.com/github/showlab/Tune-A-Video/blob/main/notebooks/Tune-A-Video.ipynb)
[[Demo (Hugging Face)]](https://huggingface.co/spaces/Tune-A-Video-library/Tune-A-Video-inference)

![](./assets/data/rabbit-watermelon.gif)
→
![](./assets/results/tuneavideo/rabbit-watermelon/puppy.gif)

  

"A puppy is eating a cheeseburger on the table, comic style"

  

"A cat with sunglasses is eating a watermelon on the beach"

  

"A rabbit is ~~eating a watermelon~~ on the table"

![](./assets/data/man-basketball.gif)
→
![](./assets/results/tuneavideo/man-basketball/lego.gif)

  

"A lego man in a black suit is dribbling a basketball"

  

"James Bond is dribbling a basketball on the beach"

  

"An astronaut is dribbling a basketball, cartoon style"

![](./assets/data/car-turn.gif)
→
![](./assets/results/tuneavideo/car-turn/car-cartoon.gif)

  

"A jeep car is moving on the road, cartoon style"

  

"A Porsche car is moving on the beach"

  

"A jeep car is moving on the snow"

![](./assets/results/tuneavideo/man-skiing/train.gif)
→
![](./assets/results/tuneavideo/man-skiing/spiderman-beach.gif)

  

“Spider Man is skiing on the beach, cartoon style”

  

"Wonder Woman, wearing a cowboy hat, is skiing"

  

"A man, wearing pink clothes, is skiing at sunset"

![](./assets/results/tuneavideo/lion-roaring/train.gif)
→
![](./assets/results/tuneavideo/lion-roaring/lion-vangogh.gif)

  

"A lion is roaring, Van Gogh style"

  

"A tiger is roaring"

  

"A wolf is roaring in New York City"

[Previous](#imageCarousel)
[Next](#imageCarousel)

  

|
|  |
|
|

**Abstract**

To replicate the success of text-to-image (T2I) generation, recent works employ large-scale video datasets
to train a text-to-video (T2V) generator. Despite their promising results, such paradigm is computationally
expensive. In this work, we propose a new T2V generation setting—One-Shot Video Tuning, where only one
text-video pair is presented. Our model is built on state-of-the-art T2I diffusion models pre-trained on
massive image data. We make two key observations: 1) T2I models can generate still images that represent
verb terms; 2) extending T2I models to generate multiple images concurrently exhibits surprisingly good
content consistency. To further learn continuous motion, we introduce Tune-A-Video, which involves a tailored
spatio-temporal attention mechanism and an efficient one-shot tuning strategy. At inference, we employ DDIM
inversion to provide structure guidance for sampling. Extensive qualitative and numerical experiments
demonstrate the remarkable ability of our method across various applications.

**Method**

![](./assets/method.png)

Given a text-video pair (e.g., “a man is skiing”) as input, our method leverages the pretrained T2I diffusion
models for T2V generation. During fine-tuning, we update the projection matrices in attention blocks using the
standard diffusion training loss. During inference, we sample a novel video from the latent noise inverted
from the input video, guided by an edited prompt (e.g., “Spider Man is surfing on the beach, cartoon style”).

**Results**

![](./assets/teaser.gif)

  

Pretrained T2I (Stable Diffusion)

|  |  |  |  |
| --- | --- | --- | --- |
| "A brown bear walking on some rocks" | ~~on some rocks~~ | some rocks → snow | + cartoon style |

|  |  |  |  |
| --- | --- | --- | --- |
| "A man dressed as Santa Claus riding a motorcycle" | Santa Claus → Spider Man | motorcycle → sleigh car | + cartoon style |

|  |  |  |  |
| --- | --- | --- | --- |
| "A car is drifting on a track with smoke coming out of it" | ~~with smoke out of it~~ | car → white van | track → desert |

[Previous](#resultCarousel1)
[Next](#resultCarousel1)

  

Pretrained T2I (personalized)

![](./assets/results/tuneavideo/anything-v4/anything-v4.png)

|  |  |  |  |
| --- | --- | --- | --- |
| "A bear is playing guitar" | bear → a girl + on the street | bear → a boy + in the coffee shop | bear → a girl + on the beach |

![](./assets/results/tuneavideo/mr-potato-head/mr-potato-head.png)

|  |  |  |  |
| --- | --- | --- | --- |
| "A bear is playing guitar" | bear → Mr Potato Head + made of lego | bear → Mr Potato Head + wearing sunglasses + on the beach | bear → Mr Potato Head + in the starry night + Van Gogh style |

![](./assets/results/tuneavideo/modern-disney/modern-disney.png)

|  |  |  |  |
| --- | --- | --- | --- |
| "A bear is playing guitar" | bear → rabbit + modern disney style | bear → prince + modern disney style | bear → princess + with sunglasses + modern disney style |

[Previous](#resultCarousel2)
[Next](#resultCarousel2)

  

Pretrained T2I (pose control)

![](./assets/data/man-basketball.gif)
→
![](./assets/results/tuneavideo/pose/man-basketball/ironman.gif)

| → | → |
| --- | --- |
| "Iron Man is dancing on the beach" | "Iron Man is running on the beach" |

[Previous](#resultCarousel3)
[Next](#resultCarousel3)



**Bibtex**

```
    @inproceedings{wu2023tune,
        title={Tune-a-video: One-shot tuning of image diffusion models for text-to-video generation},
        author={Wu, Jay Zhangjie and Ge, Yixiao and Wang, Xintao and Lei, Stan Weixian and Gu, Yuchao and Shi, Yufei and Hsu, Wynne and Shan, Ying and Qie, Xiaohu and Shou, Mike Zheng},
        booktitle={Proceedings of the IEEE/CVF International Conference on Computer Vision},
        pages={7623--7633},
        year={2023}
    }       
			
```

This page was adapted from [this](https://github.com/pnp-diffusion/pnp-diffusion.github.io) source code.
