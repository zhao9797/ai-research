# ByteDance Seed
Source: https://seed.bytedance.com/en/seed3d_2_0
ByteDance Seed 

[Home](/?view_from=homepage_tab)[Models](/models?view_from=homepage_tab)[Blog & Publication](/research?view_from=homepage_tab)[Join Us](/career?view_from=homepage_tab)

EN

中文

[Home](/?view_from=homepage_tab)[Models](/models?view_from=homepage_tab)[Blog & Publication](/research?view_from=homepage_tab)[Join Us](/career?view_from=homepage_tab)

April 23, 2026

Seed3D 2.0

State-of-the-art (SOTA) performance in both geometry and texture & material generation

Tech Report

Tech Blog

Try Now

![](https://lf3-static.bytednsdoc.com/obj/eden-cn/lapzild-tss/ljhwZthlaukjlkulzlp/user-upload/4og2ymo755bto.png)

Overview

Last year, Seed3D 1.0 explored end-to-end generation from a single image to high-quality 3D models and made notable progress in texture generation. Today, we are officially releasing Seed3D 2.0, a new-generation 3D foundation model with improved precision. Seed3D 2.0 introduces architectural upgrades focused on geometric precision and material quality.

Seed3D 2.0 introduces a Coarse-to-Fine two-stage generation strategy that decouples "overall structure" from "fine details", allowing them to be optimized separately. This breakthrough tackles major geometry generation challenges, such as sharp edges, thin-walled structures, and complex topologies.

![](https://lf3-static.bytednsdoc.com/obj/eden-cn/lapzild-tss/ljhwZthlaukjlkulzlp/user-upload/4og2ymo6oe71o.jpeg)

Full geometry generation pipeline of Seed3D 2.0

Meanwhile, Seed3D 2.0 adopts a unified PBR generative model to jointly model the full set of PBR maps. It adopts an MoE architecture to improve high-resolution material details and boundary precision. In addition, we incorporate VLM priors to enhance the stability and accuracy of material decomposition under unknown lighting conditions.

![](https://lf3-static.bytednsdoc.com/obj/eden-cn/lapzild-tss/ljhwZthlaukjlkulzlp/user-upload/4og2ymo6t6owu.jpeg)

Texture generation pipeline of Seed3D 2.0

Beyond geometry and texture, Seed3D 2.0 can be applied to part-level segmentation and completion, articulated asset generation, and flexible scene composition based on images, videos, or text, supporting the deployment of generative 3D models in real-world applications.

![](https://lf3-static.bytednsdoc.com/obj/eden-cn/lapzild-tss/ljhwZthlaukjlkulzlp/user-upload/4og2ymo6tt3oi.jpeg)

Simulatable scene generation pipeline of Seed3D 2.0

Model Evaluations

We conducted a systematic user study to evaluate the generation quality of Seed3D 2.0, recruiting 60 human raters with experience in 3D modeling to perform pairwise blind comparisons between Seed3D 2.0 and six baseline models.

![](https://lf3-static.bytednsdoc.com/obj/eden-cn/lapzild-tss/ljhwZthlaukjlkulzlp/user-upload/4og2ymo6u4glo.jpeg)

The evaluation consists of two parts: comparisons of geometry generation and textured 3D generation.

Seed3D 2.0 demonstrates a notable advantage in comparative tests of geometry generation, achieving higher preference rates than all other 3D generation models, as measured by the share of human raters who rated its outputs as of higher quality. This validates the improvements in geometry quality brought by its architectural innovations.

In human evaluation of textured 3D content generation, Seed3D 2.0 also outperforms other baseline methods, achieving a preference rate of over 69% against current mainstream models in the field.

Downstream Task Exploration

Part-Level Generation

Many downstream scenarios require 3D assets to be decomposed into functional components. For instance, interactive systems demand independently manipulable object modules, while simulation environments rely on articulated part structures for kinematic movement. To meet these needs, Seed3D 2.0 enhances modeling flexibility, enabling seamless assembly and decomposition of individual parts.

Articulated Generation

On top of part segmentation, Seed3D 2.0 further introduces articulated modeling capabilities. This process integrates multimodal understanding and generation technologies. The model first leverages VLMs to decompose parts into kinematic components and identify joint types (e.g., revolute parts vs. fixed structures), and then estimates joint axes via geometric priors. To ensure the physical plausibility of the motion, the model also introduces an image-to-video model to generate motion references, optimizing the range of motion for articulated parts. Ultimately, the model outputs 3D content with complete joint information in standard formats like URDF, achieving compatibility with mainstream physics simulation engines such as Isaac Sim.

Scene Composition

Seed3D 2.0's single-object generation capabilities can also be extended to scene generation. For text inputs, it utilizes a fine-tuned LLM for spatial reasoning and layout generation; for multi-view image or video inputs, the model additionally leverages visual signals like depth estimation, along with capabilities such as instance segmentation and occlusion inpainting, to infer the scene's spatial layout. Once the layout is obtained, Seed3D 2.0 can generate 3D content individually and assemble them according to their spatial relationships to construct a rich and complete scene.

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
