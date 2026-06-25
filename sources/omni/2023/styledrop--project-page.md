# StyleDrop: Text-to-Image Generation in Any Style
Source: https://styledrop.github.io/
StyleDrop: Text-to-Image Generation in Any Style



![](./images/logo_jpgs/row03_col02_logo.jpg)


A logo with letters "StyleDrop" in 3d rendering style.

![](./images/logo_jpgs/row03_col03_logo.jpg)


A transparent waterdrop in glowing 3d rendering style.

(A style reference image is in white inset box)

# *StyleDrop:* Text-To-Image Generation in Any Style

Kihyuk Sohn, Nataniel Ruiz, Kimin Lee, Daniel Castro Chin, Irina Blok, Huiwen Chang, Jarred Barber, Lu Jiang, Glenn Entis, Yuanzhen Li, Yuan Hao, Irfan Essa, Michael Rubinstein, Dilip Krishnan

  

![Google Research](https://research.google/static/images/google_research_lockup-121987c06c0aa0ab26ca8716a0f2e7945d1cbf82077bbab9f914dac0a0bf099f.svg)

We present *StyleDrop* that enables the generation of images that faithfully follow a specific style,
powered by [Muse](https://muse-model.github.io/), a text-to-image generative
vision transformer.
*StyleDrop* is extremely versatile and captures nuances and details of a user-provided style, such as color
schemes, shading, design patterns, and local and global effects. *StyleDrop* works by efficiently learning
a new style by fine-tuning very few trainable parameters (less than 1% of total model parameters), and improving
the quality via iterative training with either human or automated feedback. Better yet, *StyleDrop* is able
to deliver impressive results even when the user supplies only a *single* image specifying the desired
style. An extensive study shows that, for the task of style tuning text-to-image models, Styledrop on [Muse](https://muse-model.github.io/) convincingly outperforms other methods,
including [DreamBooth](https://dreambooth.github.io/) and [Textual
Inversion](https://textual-inversion.github.io/) on [Imagen](https://imagen.research.google/) or [Stable Diffusion](https://stability.ai/stable-diffusion).

[Research Paper](https://arxiv.org/abs/2306.00983)

# Stylized Text-to-image Generation from a Single Image

***StyleDrop*** generates high-quality images from text prompts in
any style described by a *single* reference image. A style descriptor in natural language (e.g., "*in melting golden 3d rendering style*") is appended to the content descriptors both at training and generation.

![](./images/styledrop_merge/01_0102.jpg)

"watercolor painting"

![](./images/styledrop_merge/02_0102.jpg)

"watercolor painting"

![](./images/styledrop_merge/03_0102.jpg)

"watercolor painting"

![](./images/styledrop_merge/04_0102.jpg)

"watercolor painting"

![](./images/styledrop_merge/05_0102.jpg)

"oil painting"

![](./images/styledrop_merge/06_0102.jpg)

"line drawing"

![](./images/styledrop_merge/07_0102.jpg)

"oil painting"

![](./images/styledrop_merge/08_0102.jpg)

"oil painting"

![](./images/styledrop_merge/09_0102.jpg)

"cartoon line drawing"

![](./images/styledrop_merge/10_0102.jpg)

"flat cartoon illustration"

![](./images/styledrop_merge/11_0102.jpg)

"flat cartoon illustration"

![](./images/styledrop_merge/12_0102.jpg)

"sticker"

![](./images/styledrop_merge/13_0102.jpg)

"abstract rainbow colored flowing smoke wave design"

![](./images/styledrop_merge/14_0102.jpg)

"glowing"

![](./images/styledrop_merge/15_0102.jpg)

"well lit haunted"

![](./images/styledrop_merge/16_0102.jpg)

"beautifully lit mythical photo"

![](./images/styledrop_merge/17_0102.jpg)

"3d rendering"

![](./images/styledrop_merge/18_0102.jpg)

"3d rendering"

![](./images/styledrop_merge/19_0102.jpg)

"glowing 3d rendering"

![](./images/styledrop_merge/20_0102.jpg)

"3d rendering"

![](./images/styledrop_merge/21_0102.jpg)

"kid crayon drawing"

![](./images/styledrop_merge/22_0102.jpg)

"glowing metal sculpture"

![](./images/styledrop_merge/23_0102.jpg)

"melting golden 3d rendering"

![](./images/styledrop_merge/24_0102.jpg)

"wooden sculpture"

❮
❯

  
  


# Stylized Character Rendering

***StyleDrop*** generates images of alphabets with a consistent style
described by a *single* reference image. A style descriptor in natural language (e.g., "*in abstract rainbow colored flowing smoke wave design*") is appended to the content descriptors both at training and generation.

![](./images/styledrop_char/01_char_01.jpg)

"watercolor painting"

![](./images/styledrop_char/02_char_01.jpg)

"watercolor painting"

![](./images/styledrop_char/03_char_01.jpg)

"watercolor painting"

![](./images/styledrop_char/04_char_01.jpg)

"watercolor painting"

![](./images/styledrop_char/05_char_01.jpg)

"oil painting"

![](./images/styledrop_char/06_char_01.jpg)

"line drawing"

![](./images/styledrop_char/07_char_01.jpg)

"oil painting"

![](./images/styledrop_char/08_char_01.jpg)

"oil painting"

![](./images/styledrop_char/09_char_01.jpg)

"cartoon line drawing"

![](./images/styledrop_char/10_char_01.jpg)

"flat cartoon illustration"

![](./images/styledrop_char/11_char_01.jpg)

"flat cartoon illustration"

![](./images/styledrop_char/12_char_01.jpg)

"sticker"

![](./images/styledrop_char/13_char_01.jpg)

"abstract rainbow colored flowing smoke wave design"

![](./images/styledrop_char/14_char_01.jpg)

"glowing"

![](./images/styledrop_char/15_char_01.jpg)

"well lit haunted"

![](./images/styledrop_char/16_char_01.jpg)

"beautifully lit mythical photo"

![](./images/styledrop_char/17_char_01.jpg)

"3d rendering"

![](./images/styledrop_char/18_char_01.jpg)

"3d rendering"

![](./images/styledrop_char/19_char_01.jpg)

"glowing 3d rendering"

![](./images/styledrop_char/20_char_01.jpg)

"3d rendering"

![](./images/styledrop_char/21_char_01.jpg)

"kid crayon drawing"

![](./images/styledrop_char/22_char_01.jpg)

"glowing metal sculpture"

![](./images/styledrop_char/23_char_01.jpg)

"melting golden 3d rendering"

![](./images/styledrop_char/24_char_01.jpg)

"wooden sculpture"

❮
❯

  
  


# Collaborate with Your Style Assistant

***StyleDrop*** is easy to train with your own brand assets and helps
you to quickly prototype ideas in your own style. A style descriptor in natural language is appended to the content descriptors both at training and generation.

![](./images/styledrop_design/01_design_01.jpg)

![](./images/styledrop_design/02_design_01.jpg)

![](./images/styledrop_design/03_design_01.jpg)

![](./images/styledrop_design/04_design_01.jpg)

❮
❯

  
  

# My Subject in My Style

We combine ***StyleDrop*** and [DreamBooth](https://dreambooth.github.io/) to generate an image of "**my subject**" in "**my style**".

![](./images/combo/content1_style1/00002.png)

  

Subject (select one)  
![content1](https://github.com/google/dreambooth/blob/main/dataset/teapot/04.jpg?raw=true)
![content2](https://github.com/google/dreambooth/blob/main/dataset/vase/04.jpg?raw=true)
![content3](https://github.com/google/dreambooth/blob/main/dataset/dog6/04.jpg?raw=true)
![content4](https://github.com/google/dreambooth/blob/main/dataset/cat/04.jpg?raw=true)

Style (select one)  
![style1](https://images.unsplash.com/photo-1612760721786-a42eb89aba02?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=735&q=80)
![style2](https://images.unsplash.com/photo-1578927107994-75410e4dcd51?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=729&q=80)
![style3](https://upload.wikimedia.org/wikipedia/commons/6/66/VanGogh-starry_night_ballance1.jpg)
![style4](https://upload.wikimedia.org/wikipedia/commons/thumb/a/aa/Vincent_van_Gogh_-_Self-portrait_with_grey_felt_hat_-_Google_Art_Project.jpg/1024px-Vincent_van_Gogh_-_Self-portrait_with_grey_felt_hat_-_Google_Art_Project.jpg)
![style5](https://images.unsplash.com/photo-1654648663068-0093ade5069e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1160&q=80)
![style6](https://img.freepik.com/free-psd/three-dimensional-real-estate-icon-mock-up_23-2149729145.jpg?w=996&t=st=1685117577~exp=1685118177~hmac=2d789df87b156c2e5578c8ddb69e4a3b3176206f81b774d9faea7492a4eafc0f)
![style7](https://images.unsplash.com/photo-1630476504743-a4d342f88760?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1895&q=80)
![style8](https://images.unsplash.com/photo-1637234852730-677079a9d718?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=735&q=80)

# Comparison to Fine-tuning of Diffusion Models

***StyleDrop*** on Muse, a discrete-token based vision transformer, convincingly outperforms in style-tuning over existing methods based on diffusion (Imagen, Stable Diffusion) models.

![](./images/more/comparison_style_supp_4col.jpg)

# Acknowledgment

First of all, we thank owners of images for sharing their valuable assets. We provide [links](https://github.com/styledrop/styledrop.github.io/blob/main/images/assets/data.md) to image assets used in our experiments.
We thank Varun Jampani, Jason Baldridge, Forrester Cole, José Lezama, Steven Hickson, Kfir Aberman for their valuable feedback on our manuscript.
