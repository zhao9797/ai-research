---
license: mit
library_name: transformers
pipeline_tag: any-to-any
---

# MMaDA-8B-Base

We introduce MMaDA, a novel class of multimodal diffusion foundation models designed to achieve superior performance across diverse domains such as textual reasoning, multimodal understanding, and text-to-image generation. MMaDA is distinguished by three key innovations:

1. MMaDA adopts a unified diffusion architecture with a shared probabilistic formulation and a modality-agnostic design, eliminating the need for modality-specific components.
2. MMaDA introduces a mixed long chain-of-thought (CoT) fine-tuning strategy that curates a unified CoT format across modalities.
3. MMaDA adopts a unified policy-gradient-based RL algorithm, which we call UniGRPO, tailored for diffusion foundation models. Utilizing diversified reward modeling, UniGRPO unifies post-training across both reasoning and generation tasks, ensuring consistent performance improvements.

[Paper](https://arxiv.org/abs/2505.15809) | [Code](https://github.com/Gen-Verse/MMaDA) | [Demo](https://huggingface.co/spaces/Gen-Verse/MMaDA)

# Citation

```
@article{yang2025mmada,
  title={MMaDA: Multimodal Large Diffusion Language Models},
  author={Yang, Ling and Tian, Ye and Li, Bowen and Zhang, Xinchen and Shen, Ke and Tong, Yunhai and Wang, Mengdi},
  journal={arXiv preprint arXiv:2505.15809},
  year={2025}
}
```

