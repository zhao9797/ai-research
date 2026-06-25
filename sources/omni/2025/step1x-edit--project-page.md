# Step1X-Edit: A Practical Framework for General Image Editing
Source: https://step1x-edit.github.io/
Step1X-Edit: A Practical Framework for General Image Editing



# Step1X-Edit: A Practical Framework for General Image Editing

Step1X-Image Team

StepFun

[arXiv](https://arxiv.org/pdf/2504.17761)


[Code](https://github.com/stepfun-ai/Step1X-Edit)

[![Hugging Face Logo](https://huggingface.co/front/assets/huggingface_logo.svg)
Model](https://huggingface.co/stepfun-ai/Step1X-Edit)

[![Hugging Face Logo](https://huggingface.co/front/assets/huggingface_logo.svg)
GEdit-Bench](https://huggingface.co/datasets/stepfun-ai/GEdit-Bench)

[](./assets/Step1X-Edit-demo.mp4)

**Step1X-Edit** is a unified image editing model performs impressively on various genuine user instructions.

### Edited Examples

[

](./assets/samples/001.mp4)

Add wings

[

](./assets/samples/002.mp4)

Add a necklace

[

](./assets/samples/003.mp4)

Remove the girl

[

](./assets/samples/004.mp4)

Remove the wings

[

](./assets/samples/005.mp4)

Replace the mooncake to Baozi

[

](./assets/samples/006.mp4)

Change to dark theme

[

](./assets/samples/007.mp4)

Make Pixel-art Style

[

](./assets/samples/008.mp4)

Beautify the man

[

](./assets/samples/009.mp4)

Make the color bright

[

](./assets/samples/010.mp4)

Make it colorful

[

](./assets/samples/011.mp4)

Change the background to mountain

[

](./assets/samples/012.mp4)

Change the water to ice

[

](./assets/samples/013.mp4)

Make ice gold

[

](./assets/samples/014.mp4)

Change hair color to white

[

](./assets/samples/015.mp4)

Make him thumbs up

[

](./assets/samples/016.mp4)

Make her cry

[

](./assets/samples/017.mp4)

Change the word to 'StepFun'

[

](./assets/samples/018.mp4)

Open the bride's eyes

[

](./assets/samples/019.mp4)

Alter 'STEAM' to 'StepFun'

[

](./assets/samples/020.mp4)

Put a wreath on her

[

](./assets/samples/021.mp4)

Change to clay material

[

](./assets/samples/022.mp4)

Paint an oil painting

[

](./assets/samples/023.mp4)

Remove texts

[

](./assets/samples/024.mp4)

Make it to Hayao Miyazaki style

[

](./assets/samples/026.mp4)

Make the leaves golden

[

](./assets/samples/027.mp4)

Replace the pizza with pasta

[

](./assets/samples/028.mp4)

Make them in a kitchen

[

](./assets/samples/029.mp4)

Cover with snow

[

](./assets/samples/030.mp4)

Adopt a Genshin-style aesthetic

❮
❯

## GEdit-Bench

### EN - Full Set - GPT4o Evaluation

### EN - Full Set - Qwen2.5-VL-72B Evaluation

### CN - Full Set - GPT4o Evaluation

### CN - Full Set - Qwen2.5-VL-72B Evaluation

### Full Set - User Study

### Intersection Set - User Study

## Leaderboard (Models & Scores for Each Metrics)

EN - Full Set - GPT4o Evaluation

| Models▲ | Background Change▲ | Color Alteration▲ | Material Modification▲ | Motion Change▲ | Portrait Beautification▲ | Style Transfer▲ | Subject Addition▲ | Subject Removal▲ | Subject Replacement▲ | Text Modification▲ | Tone Transformation▲ | Avg▲ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AnyEdit | 4.308 | 4.250 | 2.644 | 0.673 | 1.897 | 1.947 | 3.723 | 3.749 | 3.228 | 0.766 | 4.214 | 2.854 |
| MagicBrush | 6.171 | 5.413 | 4.745 | 1.545 | 2.898 | 4.103 | 5.533 | 4.130 | 5.099 | 1.330 | 5.069 | 4.185 |
| Instruct-Pix2Pix | 3.937 | 5.404 | 3.521 | 1.265 | 2.623 | 4.393 | 3.066 | 1.497 | 3.477 | 1.126 | 5.096 | 3.219 |
| OmniGen | 5.228 | 5.927 | 5.441 | 3.115 | 3.168 | 4.881 | 6.331 | 6.348 | 5.344 | 4.309 | 4.962 | 5.005 |
| Step1X-Edit | 7.033 | 6.264 | 6.455 | 3.661 | 5.233 | 7.236 | 7.168 | 6.424 | 7.391 | 7.399 | 6.616 | 6.444 |
| Gemini | 7.105 | 7.135 | 6.473 | 5.667 | 3.991 | 4.945 | 8.118 | 6.887 | 7.414 | 6.852 | 7.010 | 6.509 |
| Doubao | 8.073 | 7.363 | 7.198 | 5.381 | 6.284 | 7.203 | 8.049 | 7.713 | 7.870 | 4.006 | 7.674 | 6.983 |
| GPT-4o | 6.960 | 6.854 | 7.099 | 5.409 | 6.742 | 7.441 | 7.508 | 8.729 | 8.551 | 8.453 | 8.689 | 7.494 |
| Bagel | 7.437 | 6.985 | 6.255 | 5.093 | 4.816 | 6.041 | 7.943 | 7.369 | 7.308 | 7.156 | 6.165 | 6.597 |
| Bagel-thinking | 7.217 | 7.244 | 6.685 | 7.118 | 6.029 | 6.169 | 7.931 | 7.435 | 7.450 | 3.608 | 6.360 | 6.659 |
| Step1X-Edit(v1.1) | 7.449 | 7.382 | 6.948 | 4.730 | 4.698 | 7.106 | 8.197 | 7.592 | 7.795 | 7.907 | 6.852 | 6.969 |

EN - Full Set - Qwen2.5-VL-72B Evaluation

| Models▲ | Background Change▲ | Color Alteration▲ | Material Modification▲ | Motion Change▲ | Portrait Beautification▲ | Style Transfer▲ | Subject Addition▲ | Subject Removal▲ | Subject Replacement▲ | Text Modification▲ | Tone Transformation▲ | Avg▲ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AnyEdit | 5.427 | 4.787 | 2.755 | 2.003 | 4.066 | 1.212 | 4.472 | 4.876 | 4.015 | 1.456 | 4.922 | 3.636 |
| MagicBrush | 6.722 | 6.545 | 5.952 | 5.854 | 5.420 | 4.500 | 6.698 | 4.680 | 7.137 | 2.337 | 5.291 | 5.558 |
| Instruct-Pix2Pix | 5.250 | 6.275 | 5.255 | 3.867 | 4.821 | 4.552 | 5.036 | 3.908 | 5.322 | 1.588 | 4.485 | 4.578 |
| OmniGen | 6.939 | 7.220 | 5.991 | 5.750 | 5.564 | 5.694 | 6.908 | 7.055 | 6.779 | 5.997 | 5.981 | 6.353 |
| Step1X-Edit | 7.408 | 7.295 | 7.106 | 6.101 | 6.753 | 7.263 | 7.333 | 6.627 | 7.578 | 7.496 | 6.775 | 7.067 |
| Gemini | 7.620 | 7.165 | 6.758 | 6.753 | 6.279 | 5.915 | 7.860 | 6.810 | 7.285 | 7.560 | 6.681 | 6.971 |
| Doubao | 7.861 | 7.240 | 7.159 | 7.280 | 7.195 | 6.882 | 7.653 | 7.837 | 7.830 | 4.839 | 7.760 | 7.231 |
| GPT-4o | 7.502 | 7.304 | 7.314 | 7.908 | 7.599 | 7.400 | 7.877 | 7.854 | 7.847 | 8.140 | 7.870 | 7.692 |
| Bagel | 7.490 | 7.188 | 6.877 | 7.038 | 6.530 | 6.560 | 7.751 | 7.833 | 7.605 | 7.560 | 7.014 | 7.222 |
| Bagel-thinking | 7.658 | 7.167 | 7.074 | 7.365 | 6.503 | 6.694 | 7.790 | 7.254 | 7.267 | 4.372 | 6.959 | 6.918 |
| Step1X-Edit(v1.1) | 7.246 | 7.566 | 7.149 | 7.368 | 6.589 | 7.319 | 7.599 | 7.155 | 7.544 | 8.028 | 7.240 | 7.346 |

CN - Full Set - GPT4o Evaluation

| Models▲ | Background Change▲ | Color Alteration▲ | Material Modification▲ | Motion Change▲ | Portrait Beautification▲ | Style Transfer▲ | Subject Addition▲ | Subject Removal▲ | Subject Replacement▲ | Text Modification▲ | Tone Transformation▲ | Avg▲ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Step1X-Edit | 7.017 | 6.336 | 6.652 | 3.905 | 5.562 | 7.350 | 7.367 | 7.339 | 7.202 | 7.809 | 6.700 | 6.658 |
| Step1X-Edit(v1.1) | 7.396 | 7.356 | 6.933 | 4.553 | 5.081 | 7.207 | 8.092 | 7.603 | 7.395 | 8.177 | 7.018 | 6.983 |
| Gemini | 6.435 | 6.467 | 3.534 | 3.027 | 3.977 | 3.815 | 7.384 | 3.967 | 5.625 | 5.736 | 6.603 | 5.143 |
| Doubao | 8.044 | 7.780 | 6.804 | 4.778 | 6.439 | 6.780 | 8.087 | 6.918 | 7.936 | 3.817 | 7.827 | 6.837 |
| GPT-4o | 6.693 | 6.675 | 6.888 | 5.176 | 6.688 | 7.524 | 6.965 | 7.626 | 8.531 | 8.739 | 8.806 | 7.301 |

CN - Full Set - Qwen2.5-VL-72B Evaluation

| Models▲ | Background Change▲ | Color Alteration▲ | Material Modification▲ | Motion Change▲ | Portrait Beautification▲ | Style Transfer▲ | Subject Addition▲ | Subject Removal▲ | Subject Replacement▲ | Text Modification▲ | Tone Transformation▲ | Avg▲ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Step1X-Edit | 7.639 | 7.190 | 7.386 | 6.187 | 6.809 | 7.430 | 7.460 | 6.959 | 7.600 | 7.685 | 6.987 | 7.212 |
| Step1X-Edit(v1.1) | 7.324 | 7.553 | 7.131 | 6.849 | 6.475 | 7.237 | 7.493 | 7.128 | 7.388 | 7.994 | 7.073 | 7.240 |
| Gemini | 6.515 | 6.856 | 3.996 | 4.750 | 5.113 | 3.718 | 7.305 | 3.783 | 5.631 | 6.922 | 6.186 | 5.525 |
| Doubao | 7.489 | 7.901 | 6.557 | 7.232 | 7.498 | 6.846 | 7.628 | 6.145 | 7.809 | 4.559 | 7.771 | 7.040 |
| GPT-4o | 7.780 | 7.490 | 6.995 | 7.526 | 7.242 | 7.243 | 7.593 | 7.194 | 7.973 | 8.212 | 7.819 | 7.552 |

Full Set - User Study

| Models▲ | Background Change▲ | Color Alteration▲ | Material Modification▲ | Motion Change▲ | Portrait Beautification▲ | Style Transfer▲ | Subject Addition▲ | Subject Removal▲ | Subject Replacement▲ | Text Modification▲ | Tone Transformation▲ | Avg▲ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Step1X-Edit | 6.876 | 6.692 | 7.562 | 6.344 | 7.338 | 7.484 | 6.584 | 6.508 | 6.578 | 7.862 | 6.506 | 6.939 |
| GPT-4o | 5.574 | 5.784 | 6.690 | 8.040 | 7.820 | 7.208 | 6.850 | 7.340 | 7.492 | 7.994 | 7.684 | 7.134 |
| Gemini | 6.554 | 7.328 | 6.624 | 6.580 | 7.186 | 7.158 | 6.018 | 6.276 | 6.742 | 4.858 | 7.308 | 6.603 |
| Doubao | 6.548 | 5.516 | 5.684 | 5.574 | 4.914 | 4.616 | 6.374 | 5.860 | 6.082 | 6.264 | 5.028 | 5.678 |
| OmniGen | 4.172 | 3.822 | 3.554 | 3.954 | 3.632 | 3.532 | 4.078 | 4.006 | 2.970 | 3.006 | 3.622 | 3.668 |

Intersection Set - User Study

| Models▲ | Background Change▲ | Color Alteration▲ | Material Modification▲ | Motion Change▲ | Portrait Beautification▲ | Style Transfer▲ | Subject Addition▲ | Subject Removal▲ | Subject Replacement▲ | Text Modification▲ | Tone Transformation▲ | Avg▲ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Step1X-Edit | 6.642 | 6.784 | 7.446 | 5.292 | 6.732 | 7.302 | 6.206 | 5.866 | 6.290 | 7.766 | 5.656 | 6.544 |
| GPT-4o | 5.394 | 5.758 | 6.386 | 7.808 | 7.574 | 7.014 | 6.454 | 7.278 | 7.286 | 7.948 | 7.670 | 6.961 |
| Gemini | 7.358 | 7.460 | 7.316 | 7.106 | 7.516 | 7.504 | 6.876 | 6.736 | 7.500 | 5.136 | 7.696 | 7.109 |
| Doubao | 7.084 | 6.558 | 5.812 | 6.850 | 5.620 | 4.900 | 7.050 | 6.698 | 6.362 | 6.438 | 6.148 | 6.320 |
| OmniGen | 3.470 | 3.622 | 2.970 | 2.914 | 2.544 | 3.204 | 3.436 | 3.468 | 2.574 | 2.776 | 2.800 | 3.071 |

## BibTeX

```
@article{liu2025step1x-edit,
  title={Step1X-Edit: A Practical Framework for General Image Editing}, 
  author={Shiyu Liu and Yucheng Han and Peng Xing and Fukun Yin and Rui Wang and Wei Cheng and Jiaqi Liao and Yingming Wang and Honghao Fu and Chunrui Han and Guopeng Li and Yuang Peng and Quan Sun and Jingwei Wu and Yan Cai and Zheng Ge and Ranchen Ming and Lei Xia and Xianfang Zeng and Yibo Zhu and Binxing Jiao and Xiangyu Zhang and Gang Yu and Daxin Jiang},
  journal={arXiv preprint arXiv:2504.17761},
  year={2025}
}
```

Source code mainly borrowed from [Keunhong Park](https://keunhong.com/)'s [Nerfies website](https://nerfies.github.io/).
