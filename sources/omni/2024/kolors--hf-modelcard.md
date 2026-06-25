---
license: apache-2.0
language:
  - zh
  - en
tags:
  - text-to-image
  - stable-diffusion
  - kolors
---
# Kolors: Effective Training of Diffusion Model for Photorealistic Text-to-Image Synthesis
<div align="center" style="display: flex; justify-content: center; flex-wrap: wrap;">
  <a href="https://github.com/Kwai-Kolors/Kolors"><img src="https://img.shields.io/static/v1?label=Kolors Code&message=Github&color=blue&logo=github-pages"></a> &ensp;
  <a href="https://kwai-kolors.github.io/"><img src="https://img.shields.io/static/v1?label=Team%20Page&message=Page&color=green"></a> &ensp;
  <a href="https://github.com/Kwai-Kolors/Kolors/blob/master/imgs/Kolors_paper.pdf"><img src="https://img.shields.io/static/v1?label=Tech Report&message=Arxiv:Kolors&color=red&logo=arxiv"></a> &ensp;
  <a href="https://kolors.kuaishou.com/"><img src="https://img.shields.io/static/v1?label=Official Website&message=Page&color=green"></a>
</div>
<figure>
  <img src="imgs/head_final3.png">
</figure>
<br>

## 📖 Introduction
Kolors is a large-scale text-to-image generation model based on latent diffusion, developed by the Kuaishou Kolors team. Trained on billions of text-image pairs, Kolors exhibits significant advantages over both open-source and proprietary models in visual quality, complex semantic accuracy, and text rendering for both Chinese and English characters. Furthermore, Kolors supports both Chinese and English inputs, demonstrating strong performance in understanding and generating Chinese-specific content. For more details, please refer to this <a href="https://github.com/Kwai-Kolors/Kolors/blob/master/imgs/Kolors_paper.pdf">technical report</a></b>.


## 🚀 Quick Start
### Requirements

* Python 3.8 or later
* PyTorch 1.13.1 or later
* Transformers 4.26.1 or later
* Recommended: CUDA 11.7 or later
<br>

1. Repository cloning and dependency installation

```bash
apt-get install git-lfs
git clone https://github.com/Kwai-Kolors/Kolors
cd Kolors
conda create --name kolors python=3.8
conda activate kolors
pip install -r requirements.txt
python3 setup.py install
```
2. Weights download（[link](https://huggingface.co/Kwai-Kolors/Kolors)）：
```bash
huggingface-cli download --resume-download Kwai-Kolors/Kolors --local-dir weights/Kolors
```
or
```bash
git lfs clone https://huggingface.co/Kwai-Kolors/Kolors weights/Kolors
```
3. Inference：
```bash
python3 scripts/sample.py "一张瓢虫的照片，微距，变焦，高质量，电影，拿着一个牌子，写着“可图”"
# The image will be saved to "scripts/outputs/sample_test.jpg"
```

### Using with Diffusers
Please refer to https://huggingface.co/Kwai-Kolors/Kolors-diffusers.

## 📜 License&Citation
### License
Kolors are fully open-sourced for academic research. For commercial use, please fill out this [questionnaire](https://github.com/Kwai-Kolors/Kolors/blob/master/imgs/可图KOLORS模型商业授权申请书.docx) and sent it to kwai-kolors@kuaishou.com for registration.

We open-source Kolors to promote the development of large text-to-image models in collaboration with the open-source community. The code of this project is open-sourced under the Apache-2.0 license. We sincerely urge all developers and users to strictly adhere to the [open-source license](MODEL_LICENSE), avoiding the use of the open-source model, code, and its derivatives for any purposes that may harm the country and society or for any services not evaluated and registered for safety. Note that despite our best efforts to ensure the compliance, accuracy, and safety of the data during training, due to the diversity and combinability of generated content and the probabilistic randomness affecting the model, we cannot guarantee the accuracy and safety of the output content, and the model is susceptible to misleading. This project does not assume any legal responsibility for any data security issues, public opinion risks, or risks and liabilities arising from the model being misled, abused, misused, or improperly utilized due to the use of the open-source model and code.


### Citation
If you find our work helpful, please cite it!

```
@article{kolors,
  title={Kolors: Effective Training of Diffusion Model for Photorealistic Text-to-Image Synthesis},
  author={Kolors Team},
  journal={arXiv preprint},
  year={2024}
}
```

### Acknowledgments
- Thanks to [Diffusers](https://github.com/huggingface/diffusers) for providing the codebase.
- Thanks to [ChatGLM3](https://github.com/THUDM/ChatGLM3) for providing the powerful Chinese language model.
<br>

### Contact Us

If you want to leave a message for our R&D team and product team, feel free to join our [WeChat group](https://github.com/Kwai-Kolors/Kolors/blob/master/imgs/wechat.png). You can also contact us via email (kwai-kolors@kuaishou.com).
