---
license: mit
---
# VQ Diffusion

* [Paper](https://arxiv.org/abs/2205.16007.pdf)

* [Original Repo](https://github.com/microsoft/VQ-Diffusion)

* **Authors**: Shuyang Gu, Dong Chen, et al.


```python
#!pip install diffusers[torch] transformers
import torch
from diffusers import VQDiffusionPipeline

pipeline = VQDiffusionPipeline.from_pretrained("microsoft/vq-diffusion-ithq", torch_dtype=torch.float16)
pipeline = pipeline.to("cuda")

output = pipeline("teddy bear playing in the pool", truncation_rate=1.0)

image = output.images[0]
image.save("./teddy_bear.png")
```

![img](https://huggingface.co/datasets/patrickvonplaten/images/resolve/main/vq_diffusion_fp16.png)

**Contribution**: This model was contribution by [williamberman](https://huggingface.co/williamberman) in [VQ-diffusion](https://github.com/huggingface/diffusers/pull/658).
