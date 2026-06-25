

<div align='center'>
<h1>Emu: An Open Multimodal Generalist</h1h1>
<h3><a href="https://arxiv.org/abs/2307.05222">Generative Pretraining in Multimodality</a></h3>

[Quan Sun](https://github.com/Quan-Sun)<sup>1*</sup>, [Qiying Yu](https://yqy2001.github.io)<sup>2,1*</sup>, [Yufeng Cui]()<sup>1*</sup>, [Fan Zhang]()<sup>1*</sup>, [Xiaosong Zhang](https://github.com/zhangxiaosong18)<sup>1*</sup>, [Yueze Wang]()<sup>1</sup>, [Hongcheng Gao]()<sup>1</sup>, [Jingjing Liu](https://air.tsinghua.edu.cn/en/info/1046/1194.htm)<sup>2</sup>, [Tiejun Huang](https://scholar.google.com/citations?user=knvEK4AAAAAJ&hl=en)<sup>1,3</sup>, [Xinlong Wang](https://www.xloong.wang/)<sup>1</sup>
	
<sup>1</sup> [BAAI](https://www.baai.ac.cn/english.html), <sup>2</sup> [THU](https://air.tsinghua.edu.cn), <sup>3</sup> [PKU](https://english.pku.edu.cn/) <br><sup>*</sup> Equal Contribution

|  [Paper](https://arxiv.org/abs/2307.05222) | [Demo(tmp)](http://218.91.113.230:9002/) |
</div>

**Emu** is a Large Multimodal Model (LMM) trained with a unified autoregressive objective, *i.e.*, predict-the-next-element, including both visual embeddings and textual tokens. Trained under this objective, **Emu** can serve as a generalist interface for diverse multimodal tasks, such as image captioning, image/video question answering, and text-to-image generation, together with new abilities like in-context text and image generation, and image blending.

## Setup

Clone the github repository and install required packages:

```shell
git clone https://github.com/baaivision/Emu
cd Emu

pip install -r requirements.txt
```

## Model Weights

We release the pretrained and instruction-tuned weights of **Emu**. Our weights are subject to LLaMA's [license](https://github.com/facebookresearch/llama/blob/main/LICENSE).

| Model name | Weight                                                  |
| ---------- | ------------------------------------------------------- |
| **Emu**    | [🤗 HF link](https://huggingface.co/BAAI/Emu/blob/main/Emu-pretrain.pt) (27GB) |
| **Emu-I**  | [🤗 HF link](https://huggingface.co/BAAI/Emu/blob/main/Emu-instruct.pt) (27GB) |

## Model Usage

At present, we provide inference code for image captioning and visual question answering:

```sh
python emu_inference.py --instruct --ckpt-path $Instruct_CKPT_PATH
```

## Acknowledgement

We thank the great work from [LLaMA](https://github.com/facebookresearch/llama), [BLIP-2](https://github.com/salesforce/LAVIS), [Stable Diffusion](https://github.com/CompVis/stable-diffusion), and [FastChat](https://github.com/lm-sys/FastChat).

## Citation

If you find Emu useful for your your research and applications, please consider citing:

```
@article{Emu,
  title={Generative Pretraining in Multimodality},
  author={Sun, Quan and Yu, Qiying and Cui, Yufeng and Zhang, Fan and Zhang, Xiaosong and Wang, Yueze and Gao, Hongcheng and Liu, Jingjing and Huang, Tiejun and Wang, Xinlong},
  publisher={arXiv:2307.05222},
  year={2023},
}

