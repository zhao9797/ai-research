---
dataset_info:
  features:
  - name: questions
    list:
    - name: answer
      dtype: string
    - name: category
      dtype: string
    - name: question
      dtype: string
  - name: sonnet
    dtype: string
  - name: pg-captioner
    dtype: string
  - name: gpt-4o
    dtype: string
  - name: image
    dtype: image
  splits:
  - name: train
    num_bytes: 321322133.0
    num_examples: 200
  download_size: 320801009
  dataset_size: 321322133.0
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
---

# CapsBench

CapsBench is a captioning evaluation dataset designed to comprehensively assess the quality of the captions across 17 categories: general, 
image type, text, color, position, relation, relative position, entity, entity size, entity shape, count, emotion, blur, image artifacts, 
proper noun (world knowledge), color palette, and color grading.

There are 200 images and 2471 questions for them, resulting in 12 questions per image on average. Images represent a wide variety of 
types - film scenes, cartoon scenes, movie posters, invitations, advertisements, casual photography, street photography, 
landscape photography, interior photography. Diversity of questions and images enables comprehensive evaluation of image captioning systems.

Along with the question-answer pairs, the dataset also contains captions generated using PG Captioner, Claude-3.5 Sonnet, and GPT-4o. 
When generating captions with proprietary models, we used detailed instructions with output schema, few-shot prompting (by providing 
three examples of high-quality detailed captions) and chain-of-thought reasoning (perform written analysis of the image prior to 
generating the caption) to achieve the best results. The access date for both Claude-3.5 Sonnet and GPT-4o is August 30, 2024.

More details about the evaluation process and results can be found in the [paper](https://arxiv.org/abs/2409.10695).

## Contributor

Dataset curated by: [Playground](https://playground.com/) Research Team

## How to cite

Please cite us if you are using this benchmark:

```
@misc{liu2024playgroundv3improvingtexttoimage,
      title={Playground v3: Improving Text-to-Image Alignment with Deep-Fusion Large Language Models}, 
      author={Bingchen Liu, Ehsan Akhgari, Alexander Visheratin, Aleks Kamko, Linmiao Xu, Shivam Shrirao, Joao Souza, Suhail Doshi, Daiqing Li},
      year={2024},
      eprint={2409.10695},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2409.10695}, 
}
```