---
license: apache-2.0
language:
- en
pipeline_tag: image-to-image
tags:
- multimodal
library_name: transformers
---

## 🔥🔥🔥 News!!
* Apr 25, 2025: 👋 We release the inference code and model weights of Step1X-Edit. [inference code](https://github.com/stepfun-ai/Step1X-Edit)
* Apr 25, 2025: 🎉 We have made our technical report available as open source. [Read](https://arxiv.org/abs/2504.17761)

<!-- ## Image Edit Demos -->

<div align="center">
<img width="720" alt="demo" src="assets/image_edit_demo.gif">
<p><b>Step1X-Edit:</b> a unified image editing model performs impressively on various genuine user instructions. </p>
</div>


## Model introduction
<div align="center">
<img width="720" alt="demo" src="assets/arch.png">
</div>

Framework of Step1X-Edit. Step1X-Edit leverages the image understanding capabilities
of MLLMs to parse editing instructions and generate editing tokens, which are then decoded into
images using a DiT-based network.More details please refer to our [technical report](https://arxiv.org/abs/2504.17761).


## Benchmark
We release [GEdit-Bench](https://huggingface.co/datasets/stepfun-ai/GEdit-Bench) as a new benchmark, grounded in real-world usages is developed to support more authentic and comprehensive evaluation. This benchmark, which is carefully curated to reflect actual user editing needs and a wide range of editing scenarios, enables more authentic and comprehensive evaluations of image editing models. Part results of the benchmark are shown below:
<div align="center">
<img width="1080" alt="results" src="assets/eval_res_en.png">
</div>

## Citation
```
@article{liu2025step1x-edit,
      title={Step1X-Edit: A Practical Framework for General Image Editing}, 
      author={Shiyu Liu and Yucheng Han and Peng Xing and Fukun Yin and Rui Wang and Wei Cheng and Jiaqi Liao and Yingming Wang and Honghao Fu and Chunrui Han and Guopeng Li and Yuang Peng and Quan Sun and Jingwei Wu and Yan Cai and Zheng Ge and Ranchen Ming and Lei Xia and Xianfang Zeng and Yibo Zhu and Binxing Jiao and Xiangyu Zhang and Gang Yu and Daxin Jiang},
      journal={arXiv preprint arXiv:2504.17761},
      year={2025}
}
```