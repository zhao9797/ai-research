# Ming-Omni
Source: https://lucaria-academy.github.io/Ming-Omni/
Ming-Omni



# Ming-Omni: A Unified Multimodal Model for Perception and Generation

[Inclusion AI, Ant Group](https://github.com/inclusionAI)∗

∗See the Contributions section of our Technical Report for the complete author list.

[Technical Report](https://arxiv.org/abs/2506.09344)




[Code](https://github.com/inclusionAI/Ming/tree/main)

[🤗
Hugging Face](https://huggingface.co/inclusionAI/Ming-Lite-Omni)

[🤖
ModelScope](https://www.modelscope.cn/models/inclusionAI/Ming-Lite-Omni)

![teaser](static/images/teaser.jpg)



## Abstract

We propose Ming-Omni, a unified multimodal model capable of processing images, text, audio, and
video, while demonstrating strong proficiency in both speech and image generation. Ming-Omni
employs dedicated encoders to extract tokens from different modalities, which are then processed
by Ling, an MoE architecture equipped with newly proposed modality-specific routers. This design
enables a single model to efficiently process and fuse multimodal inputs within a unified framework,
thereby facilitating diverse tasks without requiring separate models, task-specific fine-tuning, or
structural redesign. Importantly, Ming-Omni extends beyond conventional multimodal models by
supporting audio and image generation. This is achieved through the integration of an advanced
audio decoder for natural-sounding speech and Ming-Lite-Uni for high-quality image generation,
which also allow the model to engage in context-aware chatting, perform text-to-speech conversion,
and conduct versatile image editing. Our experimental results showcase Ming-Omni offers a powerful
solution for unified perception and generation across all modalities. Notably, our proposed Ming-Omni
is the first open-source model we are aware of to match GPT-4o in modality support, and we
release all code and model weights to encourage further research and development in the community.



## Overall Framework of Ming-Omni

![method](static/images/method.jpg)

## The overall framework of Ming-Omni. Ming-Omni extracts visual and audio tokens with dedicated encoders. These tokens are then combined with text tokens and processed through Ling (MoE architecture with modality-specific routers). Subsequently, it generates speech through an audio decoder and enables image generation via a diffusion model.



## Unified Intelligence, Versatile Applications

[

](https://cloud.video.taobao.com/vod/8gvM_l85vmdlvM3csJ459NfoajYdkvTprH3fGPoaJLc.mp4)

### Basic Chatting

[

](https://cloud.video.taobao.com/vod/2dQWYEW_HH-2-Rgfc2u1-6eNpKybnLqHK_FilA0eb08.mp4)

### Visual Positioning

[

](https://cloud.video.taobao.com/vod/T7Y5e1Wr7ofENFEx-5_g8y5f5bInkpKP0eODI-sVAHs.mp4)

### Mathematics

[

](https://cloud.video.taobao.com/vod/Szp0rqz2e1lpX3pkUDp4EFSC-KRMIuHZcqtxlx4rfjk.mp4)

### Mobile Phone Interaction

## Generation and Understanding, All in One Model

[

](https://cloud.video.taobao.com/vod/swhIKM_X4z_Mzn0Y2H-vxODDdg9cEZaWY1Mx-eQLSbQ.mp4)

### Image

[

](https://cloud.video.taobao.com/vod/YiuzWc4invH0V--IOwmW8zznDDa902Exop3sHPu-aMI.mp4)

### Image

[

](https://cloud.video.taobao.com/vod/DulRhChUz7pN_5-3vZtkSVUMU5RfsJZOx0K6aswnJHg.mp4)

### Video (This video contains audio)

[

](https://cloud.video.taobao.com/vod/NKyLG8dx2wODx9j4lidW9IA-BBJ5dR3wlAj40vCHgIQ.mp4)

### Video (This video contains audio)

## Fluid Transition Between Speech and Text

|  |  |  |
| --- | --- | --- |
| Dialect Understanding | Input:    Output: "[方言-粤语] 你在干什么, 是不是不想聊天" | Input:    Output: "[方言-上海话] 我们考试还没定下来呢" |
| Input:    Output: "[方言-闽南语] 宝贝, 早点休息, 晚安" | Input:    Output: "[方言-川渝方言] 我难受的很, 别人都睡了" |
| Voice Cloning | Input1:    Input2: "全球每年有超过一百三十五万人，因交通事故而死亡"  Output: | Input1:    Input2: "The stained glass offered a hypnotic atmosphere"  Output: |
| Spoken Chatting | Input:    Output: | Input:    Output: |

## Reference

```
@article{Mingomni2025,
  title   = {Ming-Omni: A Unified Multimodal Model for Perception and Generation},
  author  = {Inclusion AI, Ant Group},
  journal = {Technical Report},
  year    = {2025}
}
@article{Mingunify2025,
  title   = {Ming-Lite-Uni: Advancements in Unified Architecture for Natural Multimodal Interaction},
  author  = {Inclusion AI, Ant Group},
  journal = {Technical Report, arXiv:2505.02471},
  year    = {2025}
}
```
