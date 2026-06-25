---
pipeline_tag: text-to-image
library_name: diffusers
license: apache-2.0
---

![Lumina-Image 2.0](./Demo.png)
Lumina-Image-2.0 is a 2 billion parameter flow-based diffusion transformer capable of generating images from text descriptions. For more information, visit our [GitHub](https://github.com/Alpha-VLLM/Lumina-Image-2.0).

## Gradio Demo

We provide an official [Gradio demo](http://47.100.29.251:10010/). You can use the link we provided to try it out.


## Usage

```python
import torch
from diffusers import Lumina2Pipeline

pipe = Lumina2Pipeline.from_pretrained("Alpha-VLLM/Lumina-Image-2.0", torch_dtype=torch.bfloat16)
pipe.enable_model_cpu_offload() #save some VRAM by offloading the model to CPU. Remove this if you have enough GPU power

prompt = "A serene photograph capturing the golden reflection of the sun on a vast expanse of water. The sun is positioned at the top center, casting a brilliant, shimmering trail of light across the rippling surface. The water is textured with gentle waves, creating a rhythmic pattern that leads the eye towards the horizon. The entire scene is bathed in warm, golden hues, enhancing the tranquil and meditative atmosphere. High contrast, natural lighting, golden hour, photorealistic, expansive composition, reflective surface, peaceful, visually harmonious."
image = pipe(
    prompt,
    height=1024,
    width=1024,
    guidance_scale=4.0,
    num_inference_steps=50,
    cfg_trunc_ratio=0.25,
    cfg_normalization=True,
    generator=torch.Generator("cpu").manual_seed(0)
).images[0]
image.save("lumina_demo.png")
```

This is a Hugging Face Diffusers implementation of the paper [Lumina-Image 2.0: A Unified and Efficient Image Generative Framework](https://arxiv.org/abs/2503.21758).

## Citation

If you find the provided code or models useful for your research, consider citing them as:

```bib
@misc{lumina2,
    author={Qi Qin and Le Zhuo and Yi Xin and Ruoyi Du and Zhen Li and Bin Fu and Yiting Lu and Xinyue Li and Dongyang Liu and Xiangyang Zhu and Will Beddow and Erwann Millon and Victor Perez,Wenhai Wang and Yu Qiao and Bo Zhang and Xiaohong Liu and Hongsheng Li and Chang Xu and Peng Gao},
    title={Lumina-Image 2.0: A Unified and Efficient Image Generative Framework},
    year={2025},
    eprint={2503.21758},
    archivePrefix={arXiv},
    primaryClass={cs.CV},
    url={https://arxiv.org/pdf/2503.21758}, 
}
```