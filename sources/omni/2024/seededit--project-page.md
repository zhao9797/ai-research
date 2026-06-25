# ByteDance Seed
Source: https://seed.bytedance.com/en/seededit
ByteDance Seed 

[Home](/?view_from=homepage_tab)[Models](/models?view_from=homepage_tab)[Blog & Publication](/research?view_from=homepage_tab)[Join Us](/career?view_from=homepage_tab)

EN

中文

[Home](/?view_from=homepage_tab)[Models](/models?view_from=homepage_tab)[Blog & Publication](/research?view_from=homepage_tab)[Join Us](/career?view_from=homepage_tab)

June 06, 2025

SeedEdit

Fast and High-Quality Generative Image Editing

We are officially launching SeedEdit 3.0. This model demonstrates significant advancements in accurately following edit instructions and effectively preserving image content (such as ID/IP and fine details), particularly with real-world images.

Read Tech Report

Try now

![](https://lf3-static.bytednsdoc.com/obj/eden-cn/bdeh7uhpsuht/SeedEdit-主KV1920x1080_.png)

Overview

Core contributions are: First, we develop an enhanced data curation pipeline with a meta-info paradigm and meta-info embedding strategy that helps mix images from multiple data sources and connect Vision-Language Models (VLMs) with Diffusion models. Second, we introduce a joint learning pipeline for computing diffusion loss and reward models. Finally, we compare our model with SeedEdit 1.6, GPT-4o, and Gemini 2.0 using our real image testing benchmarks, yielding the best trade-off and a satisfactory score among all these models.

![](https://lf3-static.bytednsdoc.com/obj/eden-cn/bdeh7uhpsuht/seededit0001.jpg)

Human evaluation: Comparing SeedEdit 3.0 with other SOTA methods across various metrics.

Data Approach

Specifically, we primarily collected data from multiple sources. These sources include: synthesized datasets, inputs from editing specialists, results from traditional edit operators, and image pairs derived from video frames and multiple short clips. This diverse data collection helps the diffusion model to interleave the space of image editing for both real and synthetic input-output.

To effectively merge these different data sources, we propose a multi-granularity label strategy for combining various types of image editing data. This strategy utilizes data-level task labels, text-level recaption, and pixel-level tagging. This structured meta-information is then integrated into our training pipeline to enhance model learning.

![](https://lf3-static.bytednsdoc.com/obj/eden-cn/bdeh7uhpsuht/seededit0002.jpg)

Training pipeline for SeedEdit 3.0. Meta-information (meta-info) is collected from multiple data sources and incorporated into the training process by fusing multiple losses.

Models

Our model architecture consists of two main components. At the bottom, a Vision-Language Model (VLM) infers high-level semantic information from the image. At the top, a causal diffusion network reuses the diffusion process as an image encoder to capture fine-grained details. Between these components, a connector module is introduced. Its purpose is to align the editing intent—such as task type and editing tag information—with our diffusion model.

![](https://lf3-static.bytednsdoc.com/obj/eden-cn/bdeh7uhpsuht/seededit0003.jpg)

Model architecture featuring meta-info embedding that connects Vision-Language Models (VLMs) with causal diffusion models.

Performance Evaluation

To rigorously evaluate SeedEdit 3.0, we curated a challenging test set of several hundred images, encompassing both real-world and generated visuals.

This collection, developed by our internal QA team, features a broad spectrum of editing tasks—from common operations like stylization, adding, replacing, and deleting elements, to more complex instructions involving camera movements, object shifts, and scene changes. This diverse benchmark is designed to be more demanding than most publicly available ones and closely reflects the types of edits our users perform daily.

Our comprehensive testing shows that SeedEdit 3.0 achieves an optimal balance across various crucial editing metrics, delivering high-quality results that effectively meet user expectations.

![](https://lf3-static.bytednsdoc.com/obj/eden-cn/bdeh7uhpsuht/seededit0004.jpg)

Speed and usability rate comparison. Dot size roughly indicates model size. Hypothesized sizes for GPT-4o and Gemini 2.0, based on their speed, are also illustrated for reference.

Editing Demos

![](https://lf3-static.bytednsdoc.com/obj/eden-cn/bdeh7uhpsuht/edit10.png)![](https://lf3-static.bytednsdoc.com/obj/eden-cn/bdeh7uhpsuht/edit11.png)

Make the girl realistic

![](https://lf3-static.bytednsdoc.com/obj/eden-cn/bdeh7uhpsuht/edit20.jpg)![](https://lf3-static.bytednsdoc.com/obj/eden-cn/bdeh7uhpsuht/edit21.png)

Change ”STOP” to “WARM”

![](https://lf3-static.bytednsdoc.com/obj/eden-cn/bdeh7uhpsuht/edit30.png)![](https://lf3-static.bytednsdoc.com/obj/eden-cn/bdeh7uhpsuht/edit31.png)

The cat is held in its owner's arm

![](https://lf3-static.bytednsdoc.com/obj/eden-cn/bdeh7uhpsuht/edit40.png)![](https://lf3-static.bytednsdoc.com/obj/eden-cn/bdeh7uhpsuht/edit411.png)

Curly rainbow short hair

![](https://lf3-static.bytednsdoc.com/obj/eden-cn/bdeh7uhpsuht/1111.png)![](https://lf3-static.bytednsdoc.com/obj/eden-cn/bdeh7uhpsuht/upscalemedia-transformed.png)

Center person only

![](https://lf3-static.bytednsdoc.com/obj/eden-cn/bdeh7uhpsuht/edit60.png)![](https://lf3-static.bytednsdoc.com/obj/eden-cn/bdeh7uhpsuht/edit61.png)

Change ”LOVE” to “SEED”

![](https://lf3-static.bytednsdoc.com/obj/eden-cn/bdeh7uhpsuht/951a7fee-4354-457a-9644-0b3659752771.png)![](https://lf3-static.bytednsdoc.com/obj/eden-cn/bdeh7uhpsuht/6f5eb224-31b6-41d8-aaa0-7648b2d55461.png)

Transform the bubble into a heart shape

![](https://lf3-static.bytednsdoc.com/obj/eden-cn/bdeh7uhpsuht/edit90.jpg)![](https://lf3-static.bytednsdoc.com/obj/eden-cn/bdeh7uhpsuht/edit91.png)

Change the scene to daytime

Models

[Seed2.0](/en/seed2)[Seedance 2.0](/en/seedance2_0)[Seedream 5.0 Lite](/en/seedream5_0_lite)[Seeduplex](/en/seeduplex)[Seed GR-RL](/en/gr_rl)

Teams

[LLM](/en/direction/llm)[Infrastructures](/en/direction/infrastructures)[Vision](/en/direction/vision)[Speech](/en/direction/speech)[Multimodal Interaction
& World Model](/en/direction/multimodal)[AI for Science](/en/direction/ai_for_science)[Robotics](/en/direction/robotics)[Responsible AI](/en/direction/responsible_ai)

Learn More

[Blog](/en/blog)[Seed Edge](/en/seed-edge)[Seed Campus Recruitment](/en/seedearlycareer)

Models

[Seed2.0](/en/seed2)

[Seedance 2.0](/en/seedance2_0)

[Seedream 5.0 Lite](/en/seedream5_0_lite)

[Seeduplex](/en/seeduplex)

[Seed GR-RL](/en/gr_rl)

Teams

[LLM](/en/direction/llm)

[Infrastructures](/en/direction/infrastructures)

[Vision](/en/direction/vision)

[Speech](/en/direction/speech)

[Multimodal Interaction
& World Model](/en/direction/multimodal)

[AI for Science](/en/direction/ai_for_science)

[Robotics](/en/direction/robotics)

[Responsible AI](/en/direction/responsible_ai)

Learn More

[Blog](/en/blog)

[Seed Edge](/en/seed-edge)

[Seed Campus Recruitment](/en/seedearlycareer)

Advancing the frontier of intelligence,
in service of humanity

![](//lf-flow-web-cdn.doubao.com/obj/flow-doubao/deploy/flow/ai_official_website/88329/static/image/new_qr_code.fb5e7d6b.png)

Join ByteDance Seed

Copyright © 2026 Bytedance Seed

[Disclaimer](/disclaimer)

[Contact us : seed.feedback@bytedance.com](mailto:seed.feedback@bytedance.com)

![](//lf-flow-web-cdn.doubao.com/obj/flow-doubao/deploy/flow/ai_official_website/88329/static/image/new_qr_code.fb5e7d6b.png)

Join ByteDance Seed

Copyright © 2026 Bytedance Seed[Disclaimer](/disclaimer)
