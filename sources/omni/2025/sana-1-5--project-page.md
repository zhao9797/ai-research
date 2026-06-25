# SANA-1.5
Source: https://nvlabs.github.io/Sana/Sana-1.5/
SANA-1.5


![Logo](https://huggingface.co/datasets/Efficient-Large-Model/Sana-assets/resolve/main/Sana-1.5/asset/logo.jpg)

# SANA-1.5

## Efficient Scaling of Training-Time and Inference-Time Compute in Linear Diffusion Transformer

Exploring the Frontiers of Efficient Generative Foundation Models

ICML 2025

[Enze Xie](https://xieenze.github.io/)1\*,
[Junsong Chen](https://lawrence-cj.github.io/)1\*,
[Yuyang Zhao](https://yuyangzhao.com/)1†,
[Jincheng Yu](https://github.com/yujincheng08)1†,
[Ligeng Zhu](https://lzhu.me//)1†,
[Chengyue We](https://hills-code.github.io/)6,
[Yujun Lin](https://yujunlin.com//)2,  
[Zhekai Zhang](https://hanlab.mit.edu/team/zhekai-zhang/)2,
[Muyang Li](https://lmxyy.me//)2,
[Junyu Chen](https://scholar.google.com.hk/citations?hl=zh-CN&user=mWdYMZ8AAAAJ)3,
[Han Cai](https://han-cai.github.io//)1,
[Bingchen Liu](https://scholar.google.com/citations?user=uKdv6SUAAAAJ&hl=en)4,
[Daquan Zhou](https://zhoudaquan.github.io/homepage.io/index.html)5,
[Song Han](https://hanlab.mit.edu/songhan/)1,2

1NVIDIA,  2MIT,  3Tsinghua University,  4Playground,  5 Peking University 6 HKU
  
\*Equal contribution   †Core contributor

[![NVIDIA Logo](https://nv-tlabs.github.io/3DStyleNet/assets/nvidia.svg)](https://www.nvidia.com/)
[![MIT Logo](https://huggingface.co/datasets/Efficient-Large-Model/Sana-assets/resolve/main/Sana-1.5/asset/mit_han.png)](https://hanlab.mit.edu/)

[📄
Paper](https://arxiv.org/abs/2501.18427)
[💻
Code](https://github.com/NVlabs/Sana)
[📖
Docs](https://nvlabs.github.io/Sana/docs/sana/)
[🚀
Demo](https://sana.hanlab.ai/)

![Image 1](https://huggingface.co/datasets/Efficient-Large-Model/Sana-assets/resolve/main/Sana-1.5/asset/samples/11.png)

![Image 2](https://huggingface.co/datasets/Efficient-Large-Model/Sana-assets/resolve/main/Sana-1.5/asset/samples/12.jpg)

![Image 3](https://huggingface.co/datasets/Efficient-Large-Model/Sana-assets/resolve/main/Sana-1.5/asset/samples/13.png)

![Image 4](https://huggingface.co/datasets/Efficient-Large-Model/Sana-assets/resolve/main/Sana-1.5/asset/samples/15.jpg)

![Image 5](https://huggingface.co/datasets/Efficient-Large-Model/Sana-assets/resolve/main/Sana-1.5/asset/samples/16.jpg)

![Image 6](https://huggingface.co/datasets/Efficient-Large-Model/Sana-assets/resolve/main/Sana-1.5/asset/samples/17.png)

![Image 7](https://huggingface.co/datasets/Efficient-Large-Model/Sana-assets/resolve/main/Sana-1.5/asset/samples/18.png)

![Image 8](https://huggingface.co/datasets/Efficient-Large-Model/Sana-assets/resolve/main/Sana-1.5/asset/samples/6.jpg)

![Image 9](https://huggingface.co/datasets/Efficient-Large-Model/Sana-assets/resolve/main/Sana-1.5/asset/samples/3.png)

![Image 10](https://huggingface.co/datasets/Efficient-Large-Model/Sana-assets/resolve/main/Sana-1.5/asset/samples/9.jpg)

![Image 11](https://huggingface.co/datasets/Efficient-Large-Model/Sana-assets/resolve/main/Sana-1.5/asset/samples/10.png)

![Image 12](https://huggingface.co/datasets/Efficient-Large-Model/Sana-assets/resolve/main/Sana-1.5/asset/samples/14.png)

![Image 13](https://huggingface.co/datasets/Efficient-Large-Model/Sana-assets/resolve/main/Sana-1.5/asset/samples/5.png)

## About SANA-1.5

This paper presents SANA-1.5, a linear Diffusion Transformer for efficient scaling in text-to-image generation.
Building upon SANA-1.0, we introduce three key innovations:  
**(1) Efficient Training Scaling:** A depth-growth paradigm that enables scaling from 1.6B to 4.8B parameters with significantly reduced computational resources,
combined with a memory-efficient 8-bit optimizer.
**(2) Model Depth Pruning:** A block importance analysis technique for efficient model compression to arbitrary sizes with minimal quality loss.
**(3) Inference-time Scaling:** A repeated sampling strategy that trades computation for model capacity,
enabling smaller models to match larger model quality at inference time. Through these strategies,
SANA-1.5 achieves a text-image alignment score of **0.81** on GenEval,
which can be further improved to **0.96** through inference scaling,
establishing a new SoTA on GenEval benchmark. These innovations enable efficient model scaling across different compute budgets while maintaining high quality,
making high-quality image generation more accessible. Our code and pre-trained models will be released.

![Pipeline for SANA-1.5](https://huggingface.co/datasets/Efficient-Large-Model/Sana-assets/resolve/main/Sana-1.5/asset/content/pipeline.png)

## Several Core Design Details for Efficiency

    •   **Efficient Training Scaling:** 
We scale the model size of Linear DiT by initializing the first 18 layers of the 4.8B Sana-1.5 model using the 1.6B Sana-1.0 pre-trained model,
leveraging a Partial Preservation initialization strategy. This approach allows the 4.8B model to achieve superior GenEval performance while reducing training time by 60% compared to training from scratch.
Additionally, we introduce the first 8-bit CAME optimizers, which significantly reduce GPU memory usage, enabling efficient scaling for larger diffusion models.

![model growth performance on GenEval](https://huggingface.co/datasets/Efficient-Large-Model/Sana-assets/resolve/main/Sana-1.5/asset/content/geneval_comparison.png)
![8-bit optimizer](https://huggingface.co/datasets/Efficient-Large-Model/Sana-assets/resolve/main/Sana-1.5/asset/content/optimizer_loss_comparison_with_ema.png)
![model growth strategy for SANA-1.5](https://huggingface.co/datasets/Efficient-Large-Model/Sana-assets/resolve/main/Sana-1.5/asset/content/model-init.png)

•   **Model Depth Pruning:** 
We employ Block Importance Analysis (Figure (a)) to guide the pruning of model depth.
By removing less important layers, the model retains most of its semantic capabilities while temporarily losing its ability to generate high-frequency details.
This loss, however, can be effectively restored through a brief retraining process (typically with 100 iterations on a single GPU).

![main techs](https://huggingface.co/datasets/Efficient-Large-Model/Sana-assets/resolve/main/Sana-1.5/asset/content/bi-scores.png)
![main techs](https://huggingface.co/datasets/Efficient-Large-Model/Sana-assets/resolve/main/Sana-1.5/asset/content/viz-prune-sft-together.png)

•   **Inference-time Scaling:** 
[NVILA-2B](https://github.com/NVlabs/VILA) as the judge: With fine-tuned NVILA-2B to automatically compare and judge generated images,
we run a tournament-style comparison several rounds until we determine the top-N candidates, as illustrated in the below Figure (a).
We demonstrate that with inference scaling:   
1. Sana-1.5 (4.8B) achieves a **SoTA 0.96 GenEval score**, as shown in Figure (b).   
2. Smaller models can outperform larger ones, with performance improvements observed consistently across all model sizes, shown in Figure (c).

![main techs](https://huggingface.co/datasets/Efficient-Large-Model/Sana-assets/resolve/main/Sana-1.5/asset/content/scaling_teaser.png)
![main techs](https://huggingface.co/datasets/Efficient-Large-Model/Sana-assets/resolve/main/Sana-1.5/asset/content/scaling_curve.png)

## Overall Performance

SANA-1.5 is an efficient model with scaling of training-time and inference time techniques.
SANA delivers: efficient model growth from 1.6B Sana-1.0 model to 4.8B, achieving similar or better performance than training from scratch and saving 60% training cost;
efficient model depth pruning, slimming any model size as you want; powerful VLM selection based inference scaling,
smaller model+inference scaling > larger model; Top-notch GenEval & DPGBench results. Detailed results are shown in the below table.

![Sana performance](https://huggingface.co/datasets/Efficient-Large-Model/Sana-assets/resolve/main/Sana-1.5/asset/content/main_table.jpg)
![Sana performance](https://huggingface.co/datasets/Efficient-Large-Model/Sana-assets/resolve/main/Sana-1.5/asset/content/inference_scaling_table.jpg)

## Our Mission

Our mission is to develop **efficient, lightweight, and accelerated**
AI technologies that address practical challenges and deliver fast, open-source solutions.

## BibTeX

```
@misc{xie2025sana,
      title={SANA 1.5: Efficient Scaling of Training-Time and Inference-Time Compute in Linear Diffusion Transformer},
      author={Xie, Enze and Chen, Junsong and Zhao, Yuyang and Yu, Jincheng and Zhu, Ligeng and Wu, Chengyue and Lin, Yujun and Zhang, Zhekai and Li, Muyang and Chen, Junyu and Cai, Han and others},
      year={2025},
      eprint={2501.18427},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2501.18427},
    }
```




This website is licensed under a [Creative
Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).

Total clicks: 173242
