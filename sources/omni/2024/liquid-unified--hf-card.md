---
license: mit
library_name: transformers
datasets:
- mlfoundations/dclm-baseline-1.0
- cerebras/SlimPajama-627B
- bigcode/starcoderdata
- JourneyDB/JourneyDB
language:
- en
base_model:
- google/gemma-7b
pipeline_tag: any-to-any
---

## Model Details

We present Liquid, an auto-regressive generation paradigm that seamlessly integrates visual comprehension and generation by tokenizing images into discrete codes and learning these code embeddings alongside text tokens within a shared feature space for both vision and language. Unlike previous multimodal large language model (MLLM), Liquid achieves this integration using a single large language model (LLM), eliminating the need for external pretrained visual embeddings such as CLIP. Liquid explores the scaling law of this multimodal hybrid model and discovers the phenomenon of mutual promotion between understanding and generation tasks. 



**Variations** Liquid comes in six sizes — 0.5B, 1B, 2B, 7B, 9B, 32B parameters (from multi modal families) in pre-trained variant, and 7B (from GEMMA) in instruction tuned variant.

**Input** Models input text and image.

**Output** Models generate text or generated image.

**Model Architecture** Liquid is an auto-regressive model extending from existing LLMs that uses an transformer architecture.


**Citation instructions** 

@article{wu2024liquid,

    title={Liquid: Language Models are Scalable Multi-modal Generators},
    
    author={Wu, Junfeng and Jiang, Yi and Ma, Chuofan and Liu, Yuliang and Zhao, Hengshuang and Yuan, Zehuan and Bai, Song and Bai, Xiang},
    
    journal={arXiv preprint arXiv:2412.04332},
    
    year={2024}
    
}