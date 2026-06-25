# InstantBooth: Personalized Text-to-Image Generation without Test-Time Finetuning
Source: https://jshi31.github.io/InstantBooth/
InstantBooth: Personalized Text-to-Image Generation without Test-Time Finetuning

  

InstantBooth: Personalized Text-to-Image Generation without Test-Time Finetuning

|  |  |  |  |
| --- | --- | --- | --- |
| [Jing Shi\*](https://www.cs.rochester.edu/u/jshi31/) | [Wei Xiong\*](https://wxiong.me/) | [Zhe Lin](https://sites.google.com/site/zhelin625/) | [Hyun Joon Jung](https://polaris79.wixsite.com/hjung/) |

|  |
| --- |
| [Adobe](https://research.adobe.com/) |

\* Equal Contribution
  
  


---

  

|  |
| --- |
|  |
| Personalized text-to-image generation: given a set of images consisting of the same concept, the model can generate new scenes based on the input concept while following the input prompts. |

  
  

  
  


---



# Abstract



Recent advances in personalized image generation allow a pre-trained text-to-image model to learn a new concept from a set of images. However, existing personalization approaches usually require test-time finetuning for each concept, which is time-consuming and difficult to scale. We propose InstantBooth, a novel approach built upon pre-trained text-to-image models that enables instant text-guided image personalization without test-time finetuning. We achieve this with several major components. First, we learn the general concept of the input images by converting them to a textual token with a learnable image encoder. Second, to keep the fine details of the identity, we learn rich visual feature representation by introducing a few adapter layers to the pre-trained model. We train our components only on text-image pairs without using paired images of the same concept. Compared to test-time finetuning-based methods like DreamBooth and Textual-Inversion, our model can generate competitive results on unseen concepts concerning language-image alignment, image fidelity, and identity preservation while being 100 times faster.
  
  


---









# Model Structure

|  |
| --- |
| An overview of our approach. We first inject a unique identifier V̂ V^ to the original input prompt to obtain "Photo of a V̂ V^ person", where V̂ V^ represents the input concept. Then we use the concept image encoder to convert the input images to a compact textual embedding and use a frozen Text encoder to map the other words to form the final prompt embeddings. We extract rich patch feature tokens from the input images with a patch encoder and then inject them to the adapter layers for better identity preservation. The U-Net of the pre-trained diffusion model takes the prompt embeddings and the rich visual feature as conditions to generate new images of the input concept. During training, only the image encoders and the adapter layers are trainable, the other parts are frozen. The model is optimized with only the reconstruction loss of the diffusion model. (We omit the object masks of the input images for simplicity.). |

  
  


---



# Visual comparison with other methods

  

|  |
| --- |
| Visualization for comparison of our method with Textual Inversion and DreamBooth |

  
  


---



# More Visual Result



|  |
| --- |
|  |



# Paper

|  |  |
| --- | --- |
|  | Jing Shi, Wei Xiong, Zhe Lin, Hyun Joon Jung  InstantBooth: Personalized Text-to-Image Generation without Test-Time Finetuning  ([ArXiv](https://arxiv.org/pdf/2304.03411.pdf)) |

  
  


---

|  |
| --- |
| Acknowledgements We thank Qing Liu for dataset preparation and He Zhang for object mask computation. The template of this webpage is borrowed from [Richard Zhang](https://richzhang.github.io/colorization/). |

  
  


---

|  |
| --- |
| Contact For further questions and suggestions, please contact Jing Shi and Wei Xiong ([jingshi@adobe.com](mailto:jingshi@adobe.com), [wxiong@adobe.com](mailto:wxiong@adobe.com)). |

  
  
