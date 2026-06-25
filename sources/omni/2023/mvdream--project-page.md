# MVDream: Multi-view Diffusion for 3D Generation
Source: https://mv-dream.github.io/
MVDream: Multi-view Diffusion for 3D Generation



# **MVDream**: Multi-view Diffusion for 3D Generation

##### [Yichun Shi1](https://seasonsh.github.io/)

##### [Peng Wang1](https://pengwangucla.github.io/peng-wang.github.io/)

##### [Jianglong Ye2](https://jianglongye.com/)

##### [Long Mai1](https://mai-t-long.com/)

##### [Kejie Li1](https://likojack.github.io/kejieli/#/home)

##### Xiao Yang1

###### 1ByteDance

###### 2University of California San Diego

[Paper](https://arxiv.org/abs/2308.16512)
[Project](#)
[Code](https://github.com/bytedance/MVDream)
[Gallery (New)](gallery_0.html)

---

## Abstract

We introduce MVDream, a multi-view diffusion model that is able to generate consistent multi-view images from a given text prompt. Learning from both 2D and 3D data, a multi-view diffusion model can achieve the generalizability of 2D diffusion models and the consistency of 3D renderings. We demonstrate that such a multi-view prior can serve as a generalizable 3D prior that is agnostic to 3D representations. It can be applied to 3D generation via Score Distillation Sampling, significantly enhancing the consistency and stability of existing 2D-lifting methods. It can also learn new concepts from a few 2D examples, akin to DreamBooth, but for 3D generation.

![architecture](static/architecture.jpg)

---

## Multi-view Score Distillation

Our multi-view diffusion model can be applied as a 3D prior to 3D Generation with Score Distillation.



---

## Example generated objects

MVDream generates objects and scenes in a multi-view consistent way.

###### Flying Dragon, highly detailed, breathing fire

###### Viking axe, fantasy, weapon, blender, 8k, HD

###### mecha vampire girl chibi

###### higly detailed, majestic royal tall ship, ...

###### a cute fluffy dog, 4K, HD, raw

###### Gandalf smiling, white hair, ...

[Additional Examples](./gallery_0.html)

---

## Comparison Results

We collected 40 prompts from different sources to compare with other text-to-3D methods. A fixed default configuration is used for all prompts without hyper-paramter tuning with [threestudio](https://github.com/threestudio-project/threestudio).

Dreamfusion-IF

Magic3D-IF-SD

Text2Mesh-IF

ProlificDreamer

Ours

an astronaut riding a horse

baby yoda in the style of Mormookiee

Handpainted watercolor windmill, hand-painted

Darth Vader helmet, highly detailed

[Full Test Results](./test_0.html)

---

![dog](static/dreambooth/dog.png)

## MV DreamBooth

Like Dreambooth3D, multi-view diffusion model can be trained with few-shot data of the same subject for personalized generation with a much simpler strategy.

Left: "Photo of a [v] dog"

###### Photo of a [v] dog

###### Photo of a [v] dog jumping

###### Photo of a [v] dog sitting on a rainbow carpet

###### Photo of a [v] dog sleeping

[Additional Results](./gallery_db_0.html)



---

## Citation

`@article{shi2023MVDream,  
  author = {Shi, Yichun and Wang, Peng and Ye, Jianglong and Mai, Long and Li, Kejie and Yang, Xiao},  
  title = {MVDream: Multi-view Diffusion for 3D Generation},  
  journal = {arXiv:2308.16512},  
  year = {2023},  
}`

---

Website template from [DreamFusion](https://dreamfusion3d.github.io/). We thank the authors for the open-source code.
