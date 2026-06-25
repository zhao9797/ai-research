---
license: cc-by-nc-4.0
task_categories:
- text-to-image
language:
- en
size_categories:
- 1M<n<10M
---

## SEED-Data-Edit
[![arXiv](https://img.shields.io/badge/arXiv-2405.04007-b31b1b.svg)](https://arxiv.org/abs/2405.04007)
[![Static Badge](https://img.shields.io/badge/Dataset-Huggingface-yellow)](https://huggingface.co/datasets/AILab-CVC/SEED-Data-Edit-Part1-Openimages)
[![Static Badge](https://img.shields.io/badge/Dataset-Huggingface-yellow)](https://huggingface.co/datasets/AILab-CVC/SEED-Data-Edit-Part1-Unsplash)
[![Static Badge](https://img.shields.io/badge/Dataset-Huggingface-yellow)](https://huggingface.co/datasets/AILab-CVC/SEED-Data-Edit-Part2-3)

![image](https://github.com/AILab-CVC/SEED-X/blob/main/demos/SEED-Data-Edit.jpg?raw=true)
SEED-Data-Edit is a hybrid dataset for **instruction-guided image editing** with a total of 3.7 image editing pairs, which comprises three distinct types of data: 

**Part-1**: Large-scale high-quality editing data produced by automated pipelines (3.5M editing pairs).

**Part-2**: Real-world scenario data collected from the internet (52K editing pairs). 

**Part-3**: High-precision multi-turn editing data annotated by humans (95K editing pairs, 21K multi-turn rounds with a maximum of 5 rounds). 

You can download them separately as below,

[SEED-Data-Edit-Part1-Openimages](https://huggingface.co/datasets/AILab-CVC/SEED-Data-Edit-Part1-Openimages)

[SEED-Data-Edit-Part1-Unsplash](https://huggingface.co/datasets/AILab-CVC/SEED-Data-Edit-Part1-Unsplash)

[SEED-Data-Edit-Part2-3](https://huggingface.co/datasets/AILab-CVC/SEED-Data-Edit-Part2-3)


## SEED-X-Edit
You can download the image editing model SEED-X-Edit in [Model](https://huggingface.co/AILab-CVC/SEED-X-17B/tree/main/seed_x_edit), 
which is instruction tuned from the pre-trained [SEED-X](https://arxiv.org/abs/2404.14396) with SEED-Data-Edit. 

For inference with SEED-X-Edit, you can refer to [SEED-X](https://github.com/AILab-CVC/SEED-X/tree/main).

![image](https://github.com/AILab-CVC/SEED-X/blob/main/demos/edit_comparison.jpg?raw=true)

## Citation
If you use this dataset, please consider citing:
```bash
@article{ge2024seed,
  title={SEED-Data-Edit Technical Report: A Hybrid Dataset for Instructional Image Editing},
  author={Ge, Yuying and Zhao, Sijie and Li, Chen and Ge, Yixiao and Shan, Ying},
  journal={arXiv preprint arXiv:2405.04007},
  year={2024}
}
```

## License
SEED-Data-Edit is released under the license CC-BY-NC-4.0 for non-commercial research purpose only.
Any use of the dataset for commercial purposes is strictly prohibited.

For Part-1, we use images from [Unsplash](https://github.com/unsplash/datasets) and [Openimages](https://arxiv.org/pdf/1811.00982).

For Part-2, we collect images from [Photoshopbattles](https://www.reddit.com/r/photoshopbattles/), [Photoshop gurus](https://www.photoshopgurus.com/forum/),
[Photoshoprequest](https://www.reddit.com/r/PhotoshopRequest/), and [Zhopped](http://zhopped.com/).

For Part-3, we use images from [Unsplash](https://github.com/unsplash/datasets), [SAM](https://arxiv.org/abs/2304.02643), and [JourneyDB](https://arxiv.org/abs/2307.00716).

Tencent does not hold the copyright for these images and the copyright belongs to the original owner. 

If any image in SEED-Data-Edit infringes upon your rights, please contact us immediately and we will promptly remove the corresponding data.


