---
license: mit
pipeline_tag: any-to-any
---
# VILA-U: a Unified Foundation Model Integrating Visual Understanding and Generation

## Abstract
VILA-U is a Unified foundation model that integrates Video, Image, Language understanding and generation. Traditional visual language models (VLMs) use separate modules for understanding and generating visual content, which can lead to misalignment and increased complexity. In contrast, VILA-U employs a single autoregressive next-token prediction framework for both tasks, eliminating the need for additional components like diffusion models. This approach not only simplifies the model but also achieves near state-of-the-art performance in visual language understanding and generation. The success of VILA-U is attributed to two main factors: the unified vision tower that aligns discrete visual tokens with textual inputs during pretraining, which enhances visual perception, and autoregressive image generation can achieve similar quality as diffusion models with high-quality dataset. This allows VILA-U to perform comparably to more complex models using a fully token-based autoregressive framework.

## Useful links

- Paper: https://arxiv.org/abs/2409.04429
- GitHub: https://github.com/mit-han-lab/vila-u
- Project: https://hanlab.mit.edu/projects/vila-u

## Citation

```bibtex
@article{wu2024vila,
  title={Vila-u: a unified foundation model integrating visual understanding and generation},
  author={Wu, Yecheng and Zhang, Zhuoyang and Chen, Junyu and Tang, Haotian and Li, Dacheng and Fang, Yunhao and Zhu, Ligeng and Xie, Enze and Yin, Hongxu and Yi, Li and others},
  journal={arXiv preprint arXiv:2409.04429},
  year={2024}
}
```