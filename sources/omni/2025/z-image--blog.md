# Z-Image - Efficient Image Generation with Single-Stream Diffusion
Source: https://tongyi-mai.github.io/Z-Image-blog/
Z-Image - Efficient Image Generation with Single-Stream Diffusion




# Z-Image

Efficient Image Generation Model with Single-Stream Diffusion Transformer

单流扩散Transformer高效图像生成模型

![Team Icon](images/icons/team.jpg)
Z-Image Team, Tongyi MAI, Alibaba Group

![Arxiv Icon](images/icons/arxiv.jpg)
Arxiv

<https://www.arxiv.org/abs/2511.22699>

![GitHub Icon](images/icons/github.jpg)
GitHub

<https://github.com/Tongyi-MAI/Z-Image>

![ModelScope Icon](images/icons/modelscope.jpg)
ModelScope

<https://www.modelscope.cn/models/Tongyi-MAI/Z-Image-Turbo>

![HuggingFace Icon](images/icons/huggingface.jpg)
HuggingFace

<https://huggingface.co/Tongyi-MAI/Z-Image-Turbo>

## Introduction

Welcome to the official homepage for the Z-Image project! This is your central hub for everything related to the Z-Image model and its core technologies. We are pleased to introduce Z-Image, an efficient 6-billion-parameter foundation model for image generation. Through systematic optimization, it proves that top-tier performance is achievable without relying on enormous model sizes, delivering strong results in photorealistic generation and bilingual text rendering that are comparable to leading commercial models.

We are publicly releasing two specialized models on Z-Image: Z-Image-Turbo for generation and Z-Image-Edit for editing. The model code, weights, and an online demo are now publicly available to encourage community exploration and use. With this release, we aim to promote the development of generative models that are accessible, low-cost, and high-performance.

欢迎来到 Z-Image 项目的官方主页！我们很高兴地推出 Z-Image，一个高效的60亿参数图像生成基础模型。它通过系统性的优化证明了顶尖性能的实现无需依赖巨大规模，在照片级真实感图像生成和中英双语文本渲染方面效果突出，其品质可与顶级商业模型相媲美。

我们公开发布基于Z-Image的两个子模型：用于图像生成的Z-Image-Turbo和用于图像编辑的Z-Image-Edit。我们已将模型代码、权重及在线Demo公开发布，以鼓励社区的探索和使用。我们希望通过此次发布，推动开发兼具普惠性、低成本与高性能的生成模型。

## Core Features

A glance at the powerful capabilities of the Z-Image model.

### Photorealistic

Photography-level Realism

### 1 Second

Ultra-fast Inference Speed

### 6B+

Parameters

## Z-Image

Single-Stream Diffusion

### Bilingual Text

Accurate Text Rendering

### 16 GB

Efficient VRAM Usage

### World Knowledge

Deep Semantic Understanding

### Image Editing

Creative Single-image Edits

## Models

At just 6 billion parameters, the model produces photorealistic images on par with those from models an order of magnitude larger. It can run smoothly on consumer-grade graphics cards with less than 16GB of VRAM, making advanced image generation technology accessible to a wider audience.

仅以60亿参数的规模，该模型能生成与参数量大一个数量级的模型相媲美的照片级真实感图像。能够在16GB显存的消费级显卡上流畅运行，让顶尖的图像生成技术惠及普通大众。

🏛️

### Z-Image-Omni-Base

A foundation model designed for easy fine-tuning, which unifies the core capabilities of image generation and editing to unlock the community's potential for custom development and innovative applications.

一个易于微调的全能基础模型，它统一了图像生成与编辑两大核心功能，旨在为社区的定制化开发与创新应用释放全部潜力。

Easy to finetune
Unified T2I & I2I

🚀

### Z-Image-Turbo

A distilled version of Z-Image with strong capabilities in photorealistic image generation, accurate rendering of both Chinese and English text, and robust adherence to bilingual instructions. It achieves performance comparable to or exceeding leading competitors with only 8 steps.

Z-Image 的蒸馏版本，擅长生成逼真图像，能精准渲染中英文文本，并严格遵循双语指令。仅需 8步推理评估即可达到或超越主流竞品性能。

8 steps
Fast Inference
Photorealistic
Bilingual Text

✍

### Z-Image-Edit

A continued-training variant of Z-Image specialized for image editing. It excels at following complex instructions to perform a wide range of tasks, from precise local modifications to global style transformations, while maintaining high edit consistency.

Z-Image 的持续训练变体，专用于图像编辑。它精于遵循复杂指令，能够胜任从精准的局部修改到全局的风格变换等多种任务，并同时保持高度的编辑一致性。

Strong Instruction-Following
Creative Editing

## Architecture

The Z-Image model adopts a Single-Stream Diffusion Transformer architecture. This design unifies the processing of various conditional inputs (like text and image embeddings) with the noisy image latents into a single sequence, which is then fed into the Transformer backbone.

Z-Image 模型采用单流扩散 Transformer 架构。该设计将文本、图像嵌入等多种条件输入与带噪声的图像潜变量统一为单个序列，并送入 Transformer 主干网络进行处理。

![Z-Image Model Architecture](images/architecture.png)

## Arena

According to the Elo-based Human Preference Evaluation (on *Alibaba AI Arena*), Z-Image shows highly competitive performance against other leading models, while achieving state-of-the-art results among open-source models.

根据 Elo 人类偏好评估（在 *Alibaba AI Arena* 上），Z-Image 与其他领先模型相比表现出极强的竞争力，同时在开源模型中取得了最先进的结果。

![Z-Image Model Architecture](images/arena.jpg)

## Efficient Photorealistic Quality 极致高效的照片级真实感

Z-Image-Turbo excels at producing images with photography-level realism, demonstrating fine control over details, lighting, and textures. It balances high fidelity with strong aesthetic quality in composition and overall mood. The generated images are not only realistic but also visually appealing.

Z-Image-Turbo 擅长生成具有摄影级别真实感的图像，能够精细控制画面的细节、光影和纹理。它在保证高保真度的同时，兼顾了构图与整体氛围上的美学表现。这使其生成的图像不仅真实，还富有视觉吸引力。

[![Realistic Image 1](images/reality/1.png)](images/reality/1.png)

[![Realistic Image 2](images/reality/2.png)](images/reality/2.png)

[![Realistic Image 3](images/reality/3.png)](images/reality/3.png)

[![Realistic Image 4](images/reality/4.png)](images/reality/4.png)

[![Realistic Image 5](images/reality/5.png)](images/reality/5.png)

[![Realistic Image 6](images/reality/6.png)](images/reality/6.png)

[![Realistic Image 7](images/reality/7.png)](images/reality/7.png)

[![Realistic Image 8](images/reality/8.png)](images/reality/8.png)

[![Realistic Image 9](images/reality/9.png)](images/reality/9.png)

[![Realistic Image 10](images/reality/10.png)](images/reality/10.png)

[![Realistic Image 11](images/reality/11.png)](images/reality/11.png)

## Excellent Bilingual Text Rendering 卓越的中英双语文本渲染能力

Z-Image-Turbo can accurately render Chinese and English text while preserving facial realism and overall aesthetic composition, with results comparable to top-tier closed-source models. In poster design, it demonstrates strong compositional skills and a good sense of typography. It can render high-quality text even in challenging scenarios with small font sizes, delivering designs that are both textually precise and visually compelling.

Z-Image-Turbo 能准确渲染中英文文本，同时保持人脸真实性和画面美感，效果媲美顶尖闭源模型。在海报设计中，它展现了优秀的构图能力和良好的版式设计感。即使在小字号等高难度场景下，模型也能高质量地渲染文字，最终呈现出文本精准且富有视觉吸引力的设计。

[![Bilingual Text Image 1](images/bilingual/1.jpg)](images/bilingual/1.jpg)

[![Bilingual Text Image 2](images/bilingual/2.jpg)](images/bilingual/2.jpg)

[![Bilingual Text Image 3](images/bilingual/3.jpg)](images/bilingual/3.jpg)

[![Bilingual Text Image 4](images/bilingual/4.jpg)](images/bilingual/4.jpg)

[![Bilingual Text Image 5](images/bilingual/5.jpg)](images/bilingual/5.jpg)

[![Bilingual Text Image 6](images/bilingual/6.jpg)](images/bilingual/6.jpg)

[![Bilingual Text Image 7](images/bilingual/7.jpg)](images/bilingual/7.jpg)

[![Bilingual Text Image 8](images/bilingual/8.jpg)](images/bilingual/8.jpg)

[![Bilingual Text Image 9](images/bilingual/9.jpg)](images/bilingual/9.jpg)

[![Bilingual Text Image 10](images/bilingual/10.jpg)](images/bilingual/10.jpg)

## Rich World Knowledge and Cultural Understanding 广博的知识与文化理解

Z-Image possesses a vast understanding of world knowledge and diverse cultural concepts. This allows it to accurately generate a wide array of subjects, including famous landmarks, well-known characters, and specific real-world objects.

Z-Image 具备广博的世界知识与对多元文化的深刻理解。这使其能够精确生成各种主题，包括著名地标、知名人物和特定的现实世界物体。

[![World Knowledge Image 1](images/world-knowledge/1.png)](images/world-knowledge/1.png)

[![World Knowledge Image 2](images/world-knowledge/2.png)](images/world-knowledge/2.png)

[![World Knowledge Image 3](images/world-knowledge/3.png)](images/world-knowledge/3.png)

[![World Knowledge Image 4](images/world-knowledge/4.png)](images/world-knowledge/4.png)

[![World Knowledge Image 5](images/world-knowledge/5.png)](images/world-knowledge/5.png)

[![World Knowledge Image 6](images/world-knowledge/6.png)](images/world-knowledge/6.png)

[![World Knowledge Image 7](images/world-knowledge/7.png)](images/world-knowledge/7.png)

[![World Knowledge Image 8](images/world-knowledge/8.png)](images/world-knowledge/8.png)

[![World Knowledge Image 9](images/world-knowledge/9.png)](images/world-knowledge/9.png)

[![World Knowledge Image 10](images/world-knowledge/10.png)](images/world-knowledge/10.png)

[![World Knowledge Image 11](images/world-knowledge/11.png)](images/world-knowledge/11.png)

## Deep Semantic Understanding with Priori Knowledge 引入先验知识的深度语义理解

The powerful prompt enhancer (PE) uses a structured reasoning chain to inject logic and common sense, enabling the model to handle complex tasks like the "chicken-and-rabbit problem" or visualizing classical Chinese poetry. In editing tasks, even when faced with ambiguous user instructions, the model can apply its reasoning capabilities to infer the underlying intent and ensure a logically coherent result.

强大的提示词增强器（PE）通过结构化推理链注入逻辑与常识，使模型能处理诸如鸡兔同笼”或古诗可视化等复杂任务。在编辑任务中，即使用户指令模糊不清，模型也能运用其推理能力来推断用户的潜在意图，确保最终结果在逻辑上是连贯的。

[![Creative Editing Image 1](images/pe/1.jpg)](images/pe/1.jpg)

Given that chickens and rabbits are in the same cage, there are a total of 35 heads and 94 feet. Find the number of chickens and rabbits.

[![Creative Editing Image 2](images/pe/2.jpg)](images/pe/2.jpg)

帮我给《登科后》配图，最出名的两句

[![Creative Editing Image 3](images/pe/3.jpg)](images/pe/3.jpg)

泡普洱茶的步骤都有哪些

[![Creative Editing Image 4](images/pe/4.jpg)](images/pe/4.jpg)

Generate a photograph located at 30° 9'36"N, 120° 7' 12"E.

[![Creative Editing Image 5](images/pe/5.jpg)](images/pe/5.jpg)

提高孩子成绩的五个关键习惯都有哪些

[![Creative Editing Image 6](images/pe/6.jpg)](images/pe/6.jpg)

帮我规划一个杭州西湖的旅游计划，手帐

[![Creative Editing Image 7](images/pe/7.jpg)](images/pe/7.jpg)

半夜睡不着，苏轼去找张怀民一起在承天寺院子里散步、聊天、赏月，对话气泡中苏轼在作诗

[![Creative Editing Image 8](images/pe/8.jpg)](images/pe/8.jpg)

what is diffusion model?

## Strong Instruction-Following and Creative Editing 强大的指令遵循与创意编辑

Z-Image-Edit can precisely execute complex instructions, such as simultaneously modifying a character's expression and pose while adding specified text. It maintains strong consistency even during such significant transformations, demonstrating fine-grained control over every image element.

Z-Image-Edit 可精准执行复合指令，如同时修改人物的表情、动作并添加指定文字。即便在如此大幅的图像变换中，它也能保持极高的一致性，体现了对画面每一处元素的精细控制。

[![Creative Editing Image 1](images/image-editing/1.jpg)](images/image-editing/1.jpg)

表情变成开心的样子，眼睛从圆形变成弯曲的眯眯眼，嘴巴变成笑着的样子，增加气泡对话框，对话框内文字“是Z-Image，我们有救了”

[![Creative Editing Image 2](images/image-editing/2.jpg)](images/image-editing/2.jpg)

变成雪天

[![Creative Editing Image 3](images/image-editing/3.jpg)](images/image-editing/3.jpg)

变成烤玉米

[![Creative Editing Image 4](images/image-editing/4.jpg)](images/image-editing/4.jpg)

让它跑起来

[![Creative Editing Image 5](images/image-editing/5.jpg)](images/image-editing/5.jpg)

男生和女生头发变成粉红色，而且男生外套变成蓝色羽绒服，

[![Creative Editing Image 6](images/image-editing/6.jpg)](images/image-editing/6.jpg)

把所有出现的“鹅”字改成“猫”

## Summary 总结

In summary, we introduce Z-Image as an efficient, low-cost approach to image generation. It demonstrates that top-tier performance is not solely dependent on massive models and computational resources. This, in turn, lowers the technical and cost barriers for the broader community of researchers and developers, paving the way for more accessible and innovative applications.

We invite the community's active participation and feedback to help us build a generative AI ecosystem that is not only open and transparent but also more efficient, accessible, and sustainable.

总而言之，我们推出 Z-Image，为图像生成领域引入了一种高效、低成本的实现路径。它证明了顶尖性能并非只依赖于巨大的模型和计算资源。这反过来也为更广泛的研究者和开发者降低了技术与成本门槛，为更多普惠、创新的应用铺平了道路。

我们期待社区的积极参与和反馈，与我们共同构建一个不仅开放、透明，而且更加高效、普惠和可持续的生成式AI生态。

## Citation 引用

Welcome to cite our work. 欢迎引用我们的工作

```
@misc{z-image-2025,
    title={Z-Image: An Efficient Image Generation Foundation Model with Single-Stream Diffusion Transformer},
    author={Tongyi Lab},
    year={2025},
    publisher={GitHub},
    journal={GitHub repository},
    howpublished={\url{https://github.com/Tongyi-MAI/Z-Image}}
}
```



© 2025 Z-Image Project
