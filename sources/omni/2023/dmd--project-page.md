# One-step Diffusion with Distribution Matching Distillation
Source: https://tianweiy.github.io/dmd/
One-step Diffusion with Distribution Matching Distillation



# One-step Diffusion with Distribution Matching Distillation

[Tianwei Yin](https://tianweiy.github.io/)1,

[Michaël Gharbi](http://mgharbi.com)2,

[Richard Zhang](http://richzhang.github.io)2,

[Eli Shechtman](https://research.adobe.com/person/eli-shechtman/)2,
  

[Frédo Durand](http://people.csail.mit.edu/fredo/)1,

[William T. Freeman](https://billf.mit.edu/)1,

[Taesung Park](https://taesung.me)2

1Massachusetts Institute of Technology,
2Adobe Research

CVPR 2024

Also check out DMD2 at <https://tianweiy.github.io/dmd2/>

[Paper](https://arxiv.org/abs/2311.18828)

[Video](https://mitprod-my.sharepoint.com/:v:/g/personal/tianweiy_mit_edu/EXBhFvm4fA5Ag1VYhXnHlh4BhYPjw0ElCr3x_A6SuZMo2g?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0RpcmVjdCJ9fQ&e=uU19gS)

[Slides](https://mitprod-my.sharepoint.com/:p:/g/personal/tianweiy_mit_edu/EdlzKshA-rhCh3i_dvQwxrcBCRYJlXCIIZ3bGjfUBMK75A?e=CerLTz)

[Poster](https://mitprod-my.sharepoint.com/:b:/g/personal/tianweiy_mit_edu/EeoXKgQ73HhGj3ufoNuVax0BhUimk3G_MIuFlfnek0HAMA?e=iFQLoc)

Our one-step generator achieves comparable image quality with StableDiffusion v1.5 while being 30x faster.

Diffusion models are known to approximate the score function of the distribution they are trained on.
In other words, an unrealistic synthetic image can be directed toward higher probability density region through the denoising process (see [SDS](https://dreamfusion3d.github.io)).
Our core idea is training two diffusion models to estimate not only the score function of the target real distribution, but also that of the fake distribution.
We construct a gradient update to our generator as the difference between the two scores, essentially nudging the generated images toward higher realism as well as lower fakeness (see [VSD](https://ml.cs.tsinghua.edu.cn/prolificdreamer/)).
Our method is similar to GANs in that a critic is jointly trained with the generator to minimize a divergence between the real and fake distributions, but differs in that our training does not play an adversarial game that may cause training instability, and our critic can fully leverage the weights of a pretrained diffusion model.
Combined with a simple regression loss to match the output of the multi-step diffusion model, our method outperforms all published few-step diffusion approaches, reaching 2.62 FID on ImageNet 64x64 and 11.49 FID on zero-shot COCO-30k, comparable to Stable Diffusion but orders of magnitude faster.
Utilizing FP16 inference, our model generates images at 20 FPS on modern hardware.

## DMD Method Overview

  
  
![Method Overview](images/overview.png)
  
  

We train one-step generator **Gθ** to map random noise **z** into a realistic image.
To match the multi-step sampling outputs of the diffusion model, we pre-compute a collection of noise--image pairs, and occasionally load the noise from the collection and enforce LPIPS
regression loss between our one-step generator and the diffusion output.
Furthermore, we provide **distribution matching gradient ∇θ DKL** to the fake image to enhance realism.
We inject a random amount of noise to the fake image and pass it to two diffusion models, one pretrained on the real data and the other continually trained on the fake images with a
diffusion loss, to obtain its denoised versions. The denoising scores (visualized as mean prediction in the plot) indicate directions to make the images more realistic or fake. The difference between the two represents the direction toward more realism and less fakeness and is backpropagated to the one-step generator.

  
  

## Comparison to Stable Diffusion

  
  

Medium shot side profile portrait photo of a warrior
chief, sharp facial features, with tribal panther makeup
in blue on red, looking away, serious but clear eyes,
50mm portrait, photography, hard rim lighting photography

  
 

![Instaflow Image](images/teaser/teaser2_Page_1_Image_0010.png)

**SD (50 steps)   
 2590ms**

![DMD Image](images/teaser/teaser2_Page_1_Image_0004.png)

**Ours (1 step)   
 90ms**

  
  

a hyperrealistic photo of a fox astronaut; perfect face,
artstation

  
 

![Instaflow Image](images/teaser/teaser2_Page_1_Image_0006.png)

**SD (50 steps)   
 2590ms**

![DMD Image](images/teaser/teaser2_Page_1_Image_0007.png)

**Ours (1 step)   
 90ms**

  
  

a DSLR photo of a golden retriever in heavy snow

  
 

![Instaflow Image](images/teaser/teaser2_Page_1_Image_0009.png)

**SD (50 steps)   
 2590ms**

![DMD Image](images/teaser/teaser2_Page_1_Image_0008.png)

**Ours (1 step)   
 90ms**

  
  

a Lightshow at the Dolomities

  
 

![Instaflow Image](images/teaser/teaser2_Page_1_Image_0001.png)

**SD (50 steps)   
 2590ms**

![DMD Image](images/teaser/teaser2_Page_1_Image_0005.png)

**Ours (1 step)   
 90ms**

  
  

the giant magical deer god of the forest, sniffing flowers on the forest floor. Fireflies evereywhere. A spring of water. Long moss hanging from the
tree branches. Moonlight. Photorealism, cinematic shot, cinematic lighting, National Geographic, analagous colors, Award-winning photography

  
 

![Instaflow Image](images/laion3/laion3_Page_1_Image_0017.png)

**SD (50 steps)   
 2590ms**

![DMD Image](images/laion3/laion3_Page_1_Image_0023.png)

**Ours (1 step)   
 90ms**

  
  

3D render baby parrot, Chibi, adorable big eyes. In a garden with butterflies, greenery, lush, whimsical and soft, magical, octane render, fairy dust

  
 

![Instaflow Image](images/laion1/laion1_Page_1_Image_0003.png)

**SD (50 steps)   
 2590ms**

![DMD Image](images/laion1/laion1_Page_1_Image_0009.png)

**Ours (1 step)   
 90ms**

  
  

## Comparison to Other Diffusion Distillation Methods

  
  

close-up photo of a unicorn in a forest, in a style of movie still

  
 

![SD Image](images/gallery2/gallery2_Page_1_Image_0006.png)

**SD (50 steps)   
 2590ms**

![Instaflow Image](images/gallery2/gallery2_Page_1_Image_0003.png)

**Instaflow (1 step)   
 90ms**

![LCM-LoRA Image](images/gallery2/gallery2_Page_1_Image_0005.png)

**LCMv1.5 (2 steps)   
 120ms**

![DMD Image](images/gallery2/gallery2_Page_1_Image_0001.png)

**Ours (1 step)   
 90ms**

  
  

amazing photograph of a labrador retriever chasing a tennis ball under water, fisheye lens, close up portrait, crazy image

  
 

![SD Image](images/gallery2/gallery2_Page_1_Image_0012.png)

**SD (50 steps)   
 2590ms**

![Instaflow Image](images/gallery2/gallery2_Page_1_Image_0009.png)

**Instaflow (1 step)   
 90ms**

![LCM-LoRA Image](images/gallery2/gallery2_Page_1_Image_0011.png)

**LCMv1.5 (2 steps)   
 120ms**

![DMD Image](images/gallery2/gallery2_Page_1_Image_0007.png)

**Ours (1 step)   
 90ms**

  
  

wise old man with a white beard in the enchanted and magical forest

  
 

![SD Image](images/gallery2/gallery2_Page_1_Image_0018.png)

**SD (50 steps)   
 2590ms**

![Instaflow Image](images/gallery2/gallery2_Page_1_Image_0015.png)

**Instaflow (1 step)   
 90ms**

![LCM-LoRA Image](images/gallery2/gallery2_Page_1_Image_0017.png)

**LCMv1.5 (2 steps)   
 120ms**

![DMD Image](images/gallery2/gallery2_Page_1_Image_0013.png)

**Ours (1 step)   
 90ms**

  
  

macro photo of a miniature toy sloth drinking a soda, shot on a light pastel cyclorama

  
 

![SD Image](images/gallery2/gallery2_Page_1_Image_0024.png)

**SD (50 steps)   
 2590ms**

![Instaflow Image](images/gallery2/gallery2_Page_1_Image_0021.png)

**Instaflow (1 step)   
 90ms**

![LCM-LoRA Image](images/gallery2/gallery2_Page_1_Image_0023.png)

**LCMv1.5 (2 steps)   
 120ms**

![DMD Image](images/gallery2/gallery2_Page_1_Image_0019.png)

**Ours (1 step)   
 90ms**

  
  

Astronaut on a camel on mars

  
 

![SD Image](images/gallery2/gallery2_Page_1_Image_0042.png)

**SD (50 steps)   
 2590ms**

![Instaflow Image](images/gallery2/gallery2_Page_1_Image_0039.png)

**Instaflow (1 step)   
 90ms**

![LCM-LoRA Image](images/gallery2/gallery2_Page_1_Image_0041.png)

**LCMv1.5 (2 steps)   
 120ms**

![DMD Image](images/gallery2/gallery2_Page_1_Image_0037.png)

**Ours (1 step)   
 90ms**

  
  

a high-resolution photo of an orange Porsche under sunshine

  
 

![SD Image](images/gallery2/gallery2_Page_1_Image_0030.png)

**SD (50 steps)   
 2590ms**

![Instaflow Image](images/gallery2/gallery2_Page_1_Image_0027.png)

**Instaflow (1 step)   
 90ms**

![LCM-LoRA Image](images/gallery2/gallery2_Page_1_Image_0029.png)

**LCMv1.5 (2 steps)   
 120ms**

![DMD Image](images/gallery2/gallery2_Page_1_Image_0025.png)

**Ours (1 step)   
 90ms**

  
  

an underwater photo portrait of a beautiful fluffy white cat, hair floating. In a dynamic swimming pose.
The sun rays filters through the water. High-angle shot. Shot on Fujifilm X

  
 

![SD Image](images/more_results/more_results_Page_1_Image_0018.png)

**SD (50 steps)   
 2590ms**

![Instaflow Image](images/more_results/more_results_Page_1_Image_0015.png)

**Instaflow (1 step)   
 90ms**

![LCM-LoRA Image](images/more_results/more_results_Page_1_Image_0017.png)

**LCMv1.5 (2 steps)   
 120ms**

![DMD Image](images/more_results/more_results_Page_1_Image_0013.png)

**Ours (1 step)   
 90ms**

  
  

3D animation cinematic style young caveman kid, in its natural environment

  
 

![SD Image](images/more_results/more_results_Page_1_Image_0030.png)

**SD (50 steps)   
 2590ms**

![Instaflow Image](images/more_results/more_results_Page_1_Image_0027.png)

**Instaflow (1 step)   
 90ms**

![LCM-LoRA Image](images/more_results/more_results_Page_1_Image_0029.png)

**LCMv1.5 (2 steps)   
 120ms**

![DMD Image](images/more_results/more_results_Page_1_Image_0025.png)

**Ours (1 step)   
 90ms**

## BibTeX

```
@inproceedings{yin2024onestep,
      title={One-step Diffusion with Distribution Matching Distillation},
      author={Yin, Tianwei and Gharbi, Micha{\"e}l and Zhang, Richard and Shechtman, Eli and Durand, Fr{\'e}do and Freeman, William T and Park, Taesung},
      booktitle={CVPR},
      year={2024}
    }
```

Website source based on [this source code](https://github.com/nerfies/nerfies.github.io).
