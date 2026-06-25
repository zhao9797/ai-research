# Imagen Video
Source: https://imagen.research.google/video/
Imagen Video


[](hdvideos/47.mp4)

Sprouts in the shape of text 'Imagen Video' coming out of a fairytale book.

[](hdvideos/40.mp4)

Incredibly detailed science fiction scene set on an alien planet, view of a marketplace. Pixel art.

[](hdvideos/16.mp4)

A panda eating bamboo on a rock.

[](hdvideos/15.mp4)

A panda bear driving a car.

[](hdvideos/41.mp4)

Melting ice cream dripping down the cone.

[](hdvideos/22.mp4)

A small hand-crafted wooden boat taking off to space.

[](hdvideos/43.mp4)

Pouring latte art into a silver cup with a golden spoon next to it.

[](hdvideos/7.mp4)

A cat on the left of a dog.

[](hdvideos/38.mp4)

Drone flythrough of a tropical jungle covered in snow

[](hdvideos/4.mp4)

A bunch of autumn leaves falling on a calm lake to form the text 'Imagen Video'. Smooth.

[](hdvideos/6.mp4)

A cat eating food out of a bowl, in style of van Gogh.

[](hdvideos/51.mp4)

Tiny plant sprout coming out of the ground.

[](hdvideos/19.mp4)

A sheep to the right of a wine glass.

[](hdvideos/45.mp4)

Sprouts in the shape of text 'Imagen Video' coming out of a fairytale book. Smooth animation.

[](hdvideos/42.mp4)

Melting pistachio ice cream dripping down the cone.

[](hdvideos/5.mp4)

A bunch of colorful candies falling into a tray in the shape of text 'Imagen Video'. Smooth video.

[](videos/fairytale.mp4)

# Imagen Video

## imagine · illustrate · inspire

# Imagen Video

## Google Research, Brain Team

# Abstract

We present Imagen Video, a text-conditional video generation system based on a cascade of video diffusion models. Given a text prompt, Imagen Video generates high definition videos using a base video generation model and a sequence of interleaved spatial and temporal video super-resolution models. We describe how we scale up the system as a high definition text-to-video model including design decisions such as the choice of fully-convolutional temporal and spatial super-resolution models at certain resolutions, and the choice of the v-parameterization of diffusion models. In addition, we confirm and transfer findings from previous work on diffusion-based image generation to the video generation setting. Finally, we apply progressive distillation to our video models with classifier-free guidance for fast, high quality sampling. We find Imagen Video not only capable of generating videos of high fidelity, but also having a high degree of controllability and world knowledge, including the ability to generate diverse videos and text animations in various artistic styles and with 3D object understanding.

[Research Paper](paper.pdf)

# Video Diffusion Models

## Cascaded Diffusion Models × 3D U-Net

[](videos/fairytale-2.mp4)

# High Definition 1280×768 24fps

# Cascaded Diffusion Models

## Spatial Super-Resolution × Temporal Super-Resolution

![](cdm-diagram.png)

Imagen Video generates high resolution videos with [Cascaded Diffusion Models](https://cascaded-diffusion.github.io/). The first step is to take an input text prompt and encode it into textual embeddings with a [T5](https://ai.googleblog.com/2020/02/exploring-transfer-learning-with-t5.html) text encoder. A base [Video Diffusion Model](https://video-diffusion.github.io/) then generates a 16 frame video at 40×24 resolution and 3 frames per second; this is then followed by multiple Temporal Super-Resolution (TSR) and Spatial Super-Resolution (SSR) models to upsample and generate a final 128 frame video at 1280×768 resolution and 24 frames per second -- resulting in 5.3s of high definition video!

# Cascaded Diffusion Models

## Spatial Super-Resolution × Temporal Super-Resolution

Sprouts in the shape of text 'Imagen' coming out of a fairytale book.

Text Prompt

# →

[](videos/cdm-1.mp4)

Base 16×40×24 3fps

# →

[](videos/cdm-2.mp4)

TSR 32×40×24 6fps

# →

[](videos/cdm-3.mp4)

SSR 32×80×48 6fps

# →

[](videos/cdm-4.mp4)

SSR 32×320×192 6fps

# →

[](videos/cdm-5.mp4)

TSR 64×320×192 12fps

# →

[](videos/cdm-6.mp4)

TSR 128×320×192 24fps

# →

[](videos/fairytale.mp4)

SSR 128×1280×768 24fps

Imagen Video generates high resolution videos with [Cascaded Diffusion Models](https://cascaded-diffusion.github.io/). The first step is to take an input text prompt and encode it into textual embeddings with a [T5](https://ai.googleblog.com/2020/02/exploring-transfer-learning-with-t5.html) text encoder. A base [Video Diffusion Model](https://video-diffusion.github.io/) then generates a 16 frame video at 40×24 resolution and 3 frames per second; this is then followed by multiple Temporal Super-Resolution (TSR) and Spatial Super-Resolution (SSR) models to upsample and generate a final 128 frame video at 1280×768 resolution and 24 frames per second -- resulting in 5.3s of high definition video!

# Video U-Net

## Spatial Fidelity × Temporal Dynamics

![](video-unet.png)

Imagen Video uses the [Video U-Net](https://video-diffusion.github.io) architecture to capture spatial fidelity and temporal dynamics. Temporal self-attention (shown in the diagram) is used in the base video diffusion model, while temporal convolutions (not shown in the diagram) are used in the temporal and spatial super-resolution models. The Video U-Net architecture empowers Imagen Video to model long-term temporal dynamics!

# Video U-Net

## Spatial Fidelity × Temporal Dynamics

Spatial Convolutions

↓

Spatial Self-Attention

↓

Temporal Attention

Spatial Convolutions

↓

Spatial Self-Attention

↓

Temporal Attention

Spatial Convolutions

↓

Spatial Self-Attention

↓

Temporal Attention

Spatial Convolutions

Spatial Self-Attention

Temporal Self-Attention

Imagen Video uses the [Video U-Net](https://video-diffusion.github.io) architecture to capture spatial fidelity and temporal dynamics. Temporal self-attention (shown in the diagram) is used in the base video diffusion model, while temporal convolutions (not shown in the diagram) are used in the temporal and spatial super-resolution models. The Video U-Net architecture empowers Imagen Video to model long-term temporal dynamics!

# Limitations

Generative modeling has made tremendous progress, especially in recent text-to-image models. Imagen Video is another step forward in generative modelling capabilities, advancing text-to-video AI systems. Video generative models can be used to positively impact society, for example by amplifying and augmenting human creativity. However, these generative models may also be misused, for example to generate fake, hateful, explicit or harmful content. We have taken multiple steps to minimize these concerns, for example in internal trials, we apply input text prompt filtering, and output video content filtering. However, there are several important safety and ethical challenges remaining. Imagen Video and its frozen T5-XXL text encoder were trained on problematic data. While our internal testing suggest much of explicit and violent content can be filtered out, there still exists social biases and stereotypes which are challenging to detect and filter. We have decided not to release the Imagen Video model or its source code until these concerns are mitigated.

# Imagen Video

## imagine · illustrate · inspire

# Authors

Jonathan Ho\*, William Chan\*, Chitwan Saharia\*, Jay Whang\*, Ruiqi Gao, Alexey Gritsenko, Diederik P. Kingma, Ben Poole, Mohammad Norouzi, David Fleet, Tim Salimans\*

\*Equal Contribution.

# Special Thanks

We give special thanks to Jordi Pont-Tuset and Shai Noy for engineering support. We also give thanks to our artist friends, Alexander Chen, Irina Blok, Ian Muldoon, Daniel Smith, and Pedro Vergani for helping us test Imagen Video and lending us their amazing creativity. We are extremely grateful for the support from Erica Moreira for compute resources. Finally, we give thanks to Elizabeth Adkison, James Bradbury, Nicole Brichtova, Tom Duerig, Douglas Eck, Dumitru Erhan, Zoubin Ghahramani, Kamyar Ghasemipour, Victor Gomes, Blake Hechtman, Jonathan Heek, Yash Katariya, Sarah Laszlo, Sara Mahdavi, Anusha Ramesh, Tom Small, and Tris Warkentin for their support.
