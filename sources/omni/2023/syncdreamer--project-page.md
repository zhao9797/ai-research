# SyncDreamer: Generating Multiview-consistent Images from a Single-view Image
Source: https://liuyuan-pal.github.io/SyncDreamer/
SyncDreamer: Generating Multiview-consistent Images from a Single-view Image




## SyncDreamer: Generating Multiview-consistent Images from a Single-view Image

#### ICLR 2024 (Spotlight)

---

###### [Yuan Liu](https://liuyuan-pal.github.io/)1,2\*, [Cheng Lin](https://clinplayer.github.io/)2\*, Zijiao Zeng2, [Xiaoxiao Long](https://www.xxlong.site/)1†, [Lingjie Liu](https://lingjie0206.github.io/)3, [Taku Komura](https://homepages.inf.ed.ac.uk/tkomura/)1, [Wenping Wang](https://engineering.tamu.edu/cse/profiles/Wang-Wenping.html)4†

1The University of Hong Kong   
2Tencent Games    
3University of Pennsylvania     
4Texas A&M University
  
\*The first two authors contribute equally.   
†Corresponding authors.

[Paper](https://arxiv.org/abs/2309.03453)

[Code](https://github.com/liuyuan-pal/SyncDreamer)

[Model](https://connecthkuhk-my.sharepoint.com/:f:/g/personal/yuanly_connect_hku_hk/EjYHbCBnV-VPjBqNHdNulIABq9sYAEpSz4NPLDI72a85vw)

[Live Demo](https://huggingface.co/spaces/liuyuan-pal/SyncDreamer)

### Abstract

---

###### SyncDreamer is able to directly generate multiview consistent images, which allows 3D reconstruction by NeuS or NeRF without SDS loss.

[

](video/teaser.mp4)
  

In this paper, we present a novel diffusion model called SyncDreamer that generates multiview-consistent images from a single-view image. Using pretrained large-scale 2D diffusion models, recent work Zero123 demonstrates the ability to generate plausible novel views from a single-view image of an object. However, maintaining consistency in geometry and colors for the generated images remains a challenge. To address this issue, we propose a synchronized multiview diffusion model that models the joint probability distribution of multiview images, enabling the generation of multiview-consistent images in a single reverse process. SyncDreamer synchronizes the intermediate states of all the generated images at every step of the reverse process through a 3D-aware feature attention mechanism that correlates the corresponding features across different views. Experiments show that SyncDreamer generates images with high consistency across different views, thus making it well-suited for various 3D generation tasks such as novel-view-synthesis, text-to-3D, and image-to-3D.

[

](video/progress_low.mp4)

Reverse process of SyncDreamer's multiview diffusion.

  

## Results on the Google Scanned Object dataset

---

[

](video/gso.mp4)

  

## Text to image to 3D model

---

[

](video/t2i.mp4)

  

## 2D design to 3D model

---

[

](video/drawings.mp4)

SyncDreamer enables generating 3D models from 2D designs and hand drawings including skectches, Chinese ink paintings, oil paintings and so on.

  

## Multiple instance generation

---

[

](video/multiple.mp4)

Given the same single-view image, SynDreame allows generating different instances using different random seeds.

  

## More results

---

[

](video/more_results.mp4)

Test images are downloaded from the Internet and some of them are from [Genshin Impact Wiki](https://wiki.biligame.com/ys/%E9%A6%96%E9%A1%B5).

  


### Citation

---

```
@article{liu2023syncdreamer,
  title={SyncDreamer: Generating Multiview-consistent Images from a Single-view Image},
  author={Liu, Yuan and Lin, Cheng and Zeng, Zijiao and Long, Xiaoxiao and Liu, Lingjie and Komura, Taku and Wang, Wenping},
  journal={arXiv preprint arXiv:2309.03453},
  year={2023}
}
```

---

Thanks to [Lior Yariv](https://lioryariv.github.io/) for the website template.
