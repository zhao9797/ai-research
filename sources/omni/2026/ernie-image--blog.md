# Introducing ERNIE-Image
Source: https://yiyan.baidu.com/blog/posts/ernie-image
Introducing ERNIE-Image



[![Wenxin](./wenxin-color.svg)ERNIE-Image](#)

OverviewShowcasesModel ResultsPrompt Enhancer (PE)Conclusion

[Get Started](https://huggingface.co/Baidu/ERNIE-Image)

OverviewShowcasesModel ResultsPrompt Enhancer (PE)Conclusion

[Get Started](https://huggingface.co/Baidu/ERNIE-Image)

# Introducing ERNIE‑Image

ERNIE-Image Team, Baidu

![ERNIE-Image Mosaic](http://bj.bcebos.com/ibox-thumbnail98/1af6663a4bb0f2e9bf1ac99b11677cf5)

## 1. Overview

**ERNIE-Image** is an open text-to-image model from the ERNIE-Image team at Baidu. Built on a single-stream Diffusion Transformer (DiT) with 8B parameters in a latent diffusion (LDM) framework, it ships with a lightweight Prompt Enhancer that expands brief inputs into richer, more structured prompts to better unlock the model's capabilities. With only 8B DiT parameters, ERNIE-Image achieves state-of-the-art performance among open weights text-to-image models — and it is built not just for visual appeal, but for controllability: accurate content depiction matters as much as aesthetics. In practice, it excels at complex instruction following, precise text rendering, and structured image generation — areas where many existing open weights models still fall short.

### Key Features

* •**Competitive performance at compact scale**: With only 8B DiT parameters, ERNIE-Image remains competitive with substantially larger models and achieves leading performance among open weights models on several challenging benchmarks.
* •**Precise text rendering**: ERNIE-Image handles dense, long-form, and layout-sensitive text especially well, producing readable and faithful results in Chinese, English, and other languages.
* •**Robust instruction following**: The model reliably handles complex prompts, multi-object relations, and knowledge-intensive descriptions, making it well suited for tasks that demand fine-grained control.
* •**Structured visual generation**: ERNIE-Image is especially effective on images with clear layout or narrative structure — posters, manga/anime storyboards, multi-panel compositions, and cohesive multi-element visuals.
* •**Broad stylistic range**: Beyond clean graphic design and illustration-style outputs, the model supports realistic photography and distinctive stylized aesthetics, including softer, more cinematic and film-like tones.
* •**Easy to deploy and adapt**: Thanks to its compact size, ERNIE-Image runs on consumer-grade hardware (24G VRAM), bringing high-quality image generation within reach for research and production use. The moderate parameter count also makes fine-tuning and adaptation straightforward for researchers and developers.

### Released Versions

[![ERNIE](./wenxin-color.svg)ERNIE-Image

Our **SFT model** — stronger general-purpose quality and instruction fidelity, typically in **50 inference steps**.

🤗 huggingface.co/Baidu/ERNIE-Image](https://huggingface.co/Baidu/ERNIE-Image)[![ERNIE](./wenxin-color.svg)ERNIE-Image-Turbo

Our **Turbo model**, optimized with **DMD and RL** for faster generation and stronger aesthetics in just **8 inference steps**.

🤗 huggingface.co/Baidu/ERNIE-Image-Turbo](https://huggingface.co/Baidu/ERNIE-Image-Turbo)

## 2. Showcases

The examples below highlight domains where ERNIE-Image stands out. Rather than focusing on generic image quality, we emphasize scenarios that demand text accuracy, structured composition, narrative organization, and distinctive visual style — settings where the gap between open weights models is most visible in practice. Click any image to view its full generation prompt. For more examples, visit our [Prompt Gallery](https://ernieimageprompt.com).

![Information Design sample 1](http://bj.bcebos.com/ibox-thumbnail98/7000b60f64715150f8807ebab4898303)

![Portrait & Lifestyle sample 2](http://bj.bcebos.com/ibox-thumbnail98/9cc6c5296afe2faf9bf4c929a1a26e3f)

![Information Design sample 3](http://bj.bcebos.com/ibox-thumbnail98/93172d3d5721317d6f8d3df306f795a5)

![Information Design sample 4](http://bj.bcebos.com/ibox-thumbnail98/671660418393ca08d1cd360ffbc9dbc2)

![Concept & Imagination sample 4](http://bj.bcebos.com/ibox-thumbnail98/b1ea7cd599d58c4cdc39e7bbbbf0b57e)

![Posters & Character Worlds sample 4](http://bj.bcebos.com/ibox-thumbnail98/2873c3e1b8a6b8c03873b98c1b6c1740)

![Narrative Illustration sample 5](http://bj.bcebos.com/ibox-thumbnail98/9dc15dba81fc51e4fe12ac986cddb13f)

![Posters & Character Worlds sample 5](http://bj.bcebos.com/ibox-thumbnail98/69396cb3ea589297b4772c849d5ad3e1)

![Portrait & Lifestyle sample 6](http://bj.bcebos.com/ibox-thumbnail98/32be7485dcf509539e1bb2501038d10d)

![Posters & Character Worlds sample 6](http://bj.bcebos.com/ibox-thumbnail98/483261e983f279eb63c8e0d05c6f7294)

![Narrative Illustration sample 7](http://bj.bcebos.com/ibox-thumbnail98/7d0130d2dd82c4e495c8c21c2a90163e)

![Posters & Character Worlds sample 7](http://bj.bcebos.com/ibox-thumbnail98/a4c6aa3d5048923e945e1f64cef5cceb)

![Concept & Imagination sample 8](http://bj.bcebos.com/ibox-thumbnail98/43c27a4ed5b2457bcb5b40c5f34a9253)

![Posters & Character Worlds sample 9](http://bj.bcebos.com/ibox-thumbnail98/5d6ec1e7bf4f8a7e4b4c1a2911d15c51)

![Portrait & Lifestyle sample 10](http://bj.bcebos.com/ibox-thumbnail98/b2479ac7df5b505bb389703a8398ad74)

![Information Design sample 11](http://bj.bcebos.com/ibox-thumbnail98/f2aec037112d762bcb62097ff35ba646)

![Narrative Illustration sample 11](http://bj.bcebos.com/ibox-thumbnail98/61aad010d6fe58fae8a0cf85413d0534)

![Information Design sample 12](http://bj.bcebos.com/ibox-thumbnail98/3cbdfe5ba564400511372a94781e29a2)

![Concept & Imagination sample 12](http://bj.bcebos.com/ibox-thumbnail98/c94977f06eff74bf02281e2c242745da)

![Information Design sample 13](http://bj.bcebos.com/ibox-thumbnail98/3522b471218109fed1f48666700b1c8d)

![Concept & Imagination sample 13](http://bj.bcebos.com/ibox-thumbnail98/96114d664a371f9ea250e85d90c6da47)

![Portrait & Lifestyle sample 14](http://bj.bcebos.com/ibox-thumbnail98/68778efc3de9dbaafcc0505e0b30cb51)

![Posters & Character Worlds sample 15](http://bj.bcebos.com/ibox-thumbnail98/0dc2d871e40bc7829393ea833d0fefbe)

![Portrait & Lifestyle sample 17](http://bj.bcebos.com/ibox-thumbnail98/e2be95ec50f8be86b0d79a1f89e13596)

![Information Design sample 19](http://bj.bcebos.com/ibox-thumbnail98/05b461ce2b851f9666cdfbad7421e9df)

![Information Design sample 21](http://bj.bcebos.com/ibox-thumbnail98/b5e0317618a1ea42094edd85f73ddefd)

![Information Design sample 23](http://bj.bcebos.com/ibox-thumbnail98/c60a6fb634f4fb9da21c9c161a234372)

![Portrait & Lifestyle sample 24](http://bj.bcebos.com/ibox-thumbnail98/f2f84996ff4c803955e22611fde1447d)

![Portrait & Lifestyle sample 25](http://bj.bcebos.com/ibox-thumbnail98/41019a3580e19f61eb493d6289bc00cd)

![Information Design sample 27](http://bj.bcebos.com/ibox-thumbnail98/579caf40e231bcb962b7b5ab65f4cb66)

![Information Design sample 1](http://bj.bcebos.com/ibox-thumbnail98/7000b60f64715150f8807ebab4898303)

![Portrait & Lifestyle sample 2](http://bj.bcebos.com/ibox-thumbnail98/9cc6c5296afe2faf9bf4c929a1a26e3f)

![Information Design sample 3](http://bj.bcebos.com/ibox-thumbnail98/93172d3d5721317d6f8d3df306f795a5)

![Information Design sample 4](http://bj.bcebos.com/ibox-thumbnail98/671660418393ca08d1cd360ffbc9dbc2)

![Concept & Imagination sample 4](http://bj.bcebos.com/ibox-thumbnail98/b1ea7cd599d58c4cdc39e7bbbbf0b57e)

![Posters & Character Worlds sample 4](http://bj.bcebos.com/ibox-thumbnail98/2873c3e1b8a6b8c03873b98c1b6c1740)

![Narrative Illustration sample 5](http://bj.bcebos.com/ibox-thumbnail98/9dc15dba81fc51e4fe12ac986cddb13f)

![Posters & Character Worlds sample 5](http://bj.bcebos.com/ibox-thumbnail98/69396cb3ea589297b4772c849d5ad3e1)

![Portrait & Lifestyle sample 6](http://bj.bcebos.com/ibox-thumbnail98/32be7485dcf509539e1bb2501038d10d)

![Posters & Character Worlds sample 6](http://bj.bcebos.com/ibox-thumbnail98/483261e983f279eb63c8e0d05c6f7294)

![Narrative Illustration sample 7](http://bj.bcebos.com/ibox-thumbnail98/7d0130d2dd82c4e495c8c21c2a90163e)

![Posters & Character Worlds sample 7](http://bj.bcebos.com/ibox-thumbnail98/a4c6aa3d5048923e945e1f64cef5cceb)

![Concept & Imagination sample 8](http://bj.bcebos.com/ibox-thumbnail98/43c27a4ed5b2457bcb5b40c5f34a9253)

![Posters & Character Worlds sample 9](http://bj.bcebos.com/ibox-thumbnail98/5d6ec1e7bf4f8a7e4b4c1a2911d15c51)

![Portrait & Lifestyle sample 10](http://bj.bcebos.com/ibox-thumbnail98/b2479ac7df5b505bb389703a8398ad74)

![Information Design sample 11](http://bj.bcebos.com/ibox-thumbnail98/f2aec037112d762bcb62097ff35ba646)

![Narrative Illustration sample 11](http://bj.bcebos.com/ibox-thumbnail98/61aad010d6fe58fae8a0cf85413d0534)

![Information Design sample 12](http://bj.bcebos.com/ibox-thumbnail98/3cbdfe5ba564400511372a94781e29a2)

![Concept & Imagination sample 12](http://bj.bcebos.com/ibox-thumbnail98/c94977f06eff74bf02281e2c242745da)

![Information Design sample 13](http://bj.bcebos.com/ibox-thumbnail98/3522b471218109fed1f48666700b1c8d)

![Concept & Imagination sample 13](http://bj.bcebos.com/ibox-thumbnail98/96114d664a371f9ea250e85d90c6da47)

![Portrait & Lifestyle sample 14](http://bj.bcebos.com/ibox-thumbnail98/68778efc3de9dbaafcc0505e0b30cb51)

![Posters & Character Worlds sample 15](http://bj.bcebos.com/ibox-thumbnail98/0dc2d871e40bc7829393ea833d0fefbe)

![Portrait & Lifestyle sample 17](http://bj.bcebos.com/ibox-thumbnail98/e2be95ec50f8be86b0d79a1f89e13596)

![Information Design sample 19](http://bj.bcebos.com/ibox-thumbnail98/05b461ce2b851f9666cdfbad7421e9df)

![Information Design sample 21](http://bj.bcebos.com/ibox-thumbnail98/b5e0317618a1ea42094edd85f73ddefd)

![Information Design sample 23](http://bj.bcebos.com/ibox-thumbnail98/c60a6fb634f4fb9da21c9c161a234372)

![Portrait & Lifestyle sample 24](http://bj.bcebos.com/ibox-thumbnail98/f2f84996ff4c803955e22611fde1447d)

![Portrait & Lifestyle sample 25](http://bj.bcebos.com/ibox-thumbnail98/41019a3580e19f61eb493d6289bc00cd)

![Information Design sample 27](http://bj.bcebos.com/ibox-thumbnail98/579caf40e231bcb962b7b5ab65f4cb66)

![Information Design sample 1](http://bj.bcebos.com/ibox-thumbnail98/7000b60f64715150f8807ebab4898303)

![Portrait & Lifestyle sample 2](http://bj.bcebos.com/ibox-thumbnail98/9cc6c5296afe2faf9bf4c929a1a26e3f)

![Information Design sample 3](http://bj.bcebos.com/ibox-thumbnail98/93172d3d5721317d6f8d3df306f795a5)

![Information Design sample 4](http://bj.bcebos.com/ibox-thumbnail98/671660418393ca08d1cd360ffbc9dbc2)

![Concept & Imagination sample 4](http://bj.bcebos.com/ibox-thumbnail98/b1ea7cd599d58c4cdc39e7bbbbf0b57e)

![Posters & Character Worlds sample 4](http://bj.bcebos.com/ibox-thumbnail98/2873c3e1b8a6b8c03873b98c1b6c1740)

![Narrative Illustration sample 5](http://bj.bcebos.com/ibox-thumbnail98/9dc15dba81fc51e4fe12ac986cddb13f)

![Posters & Character Worlds sample 5](http://bj.bcebos.com/ibox-thumbnail98/69396cb3ea589297b4772c849d5ad3e1)

![Portrait & Lifestyle sample 6](http://bj.bcebos.com/ibox-thumbnail98/32be7485dcf509539e1bb2501038d10d)

![Posters & Character Worlds sample 6](http://bj.bcebos.com/ibox-thumbnail98/483261e983f279eb63c8e0d05c6f7294)

![Narrative Illustration sample 7](http://bj.bcebos.com/ibox-thumbnail98/7d0130d2dd82c4e495c8c21c2a90163e)

![Posters & Character Worlds sample 7](http://bj.bcebos.com/ibox-thumbnail98/a4c6aa3d5048923e945e1f64cef5cceb)

![Concept & Imagination sample 8](http://bj.bcebos.com/ibox-thumbnail98/43c27a4ed5b2457bcb5b40c5f34a9253)

![Posters & Character Worlds sample 9](http://bj.bcebos.com/ibox-thumbnail98/5d6ec1e7bf4f8a7e4b4c1a2911d15c51)

![Portrait & Lifestyle sample 10](http://bj.bcebos.com/ibox-thumbnail98/b2479ac7df5b505bb389703a8398ad74)

![Information Design sample 11](http://bj.bcebos.com/ibox-thumbnail98/f2aec037112d762bcb62097ff35ba646)

![Narrative Illustration sample 11](http://bj.bcebos.com/ibox-thumbnail98/61aad010d6fe58fae8a0cf85413d0534)

![Information Design sample 12](http://bj.bcebos.com/ibox-thumbnail98/3cbdfe5ba564400511372a94781e29a2)

![Concept & Imagination sample 12](http://bj.bcebos.com/ibox-thumbnail98/c94977f06eff74bf02281e2c242745da)

![Information Design sample 13](http://bj.bcebos.com/ibox-thumbnail98/3522b471218109fed1f48666700b1c8d)

![Concept & Imagination sample 13](http://bj.bcebos.com/ibox-thumbnail98/96114d664a371f9ea250e85d90c6da47)

![Portrait & Lifestyle sample 14](http://bj.bcebos.com/ibox-thumbnail98/68778efc3de9dbaafcc0505e0b30cb51)

![Posters & Character Worlds sample 15](http://bj.bcebos.com/ibox-thumbnail98/0dc2d871e40bc7829393ea833d0fefbe)

![Portrait & Lifestyle sample 17](http://bj.bcebos.com/ibox-thumbnail98/e2be95ec50f8be86b0d79a1f89e13596)

![Information Design sample 19](http://bj.bcebos.com/ibox-thumbnail98/05b461ce2b851f9666cdfbad7421e9df)

![Information Design sample 21](http://bj.bcebos.com/ibox-thumbnail98/b5e0317618a1ea42094edd85f73ddefd)

![Information Design sample 23](http://bj.bcebos.com/ibox-thumbnail98/c60a6fb634f4fb9da21c9c161a234372)

![Portrait & Lifestyle sample 24](http://bj.bcebos.com/ibox-thumbnail98/f2f84996ff4c803955e22611fde1447d)

![Portrait & Lifestyle sample 25](http://bj.bcebos.com/ibox-thumbnail98/41019a3580e19f61eb493d6289bc00cd)

![Information Design sample 27](http://bj.bcebos.com/ibox-thumbnail98/579caf40e231bcb962b7b5ab65f4cb66)

![Portrait & Lifestyle sample 1](http://bj.bcebos.com/ibox-thumbnail98/6aaf503a33d3a9f58b54dd2a7f2fe027)

![Concept & Imagination sample 1](http://bj.bcebos.com/ibox-thumbnail98/736df3ebc85988603d9348e735d55515)

![Information Design sample 2](http://bj.bcebos.com/ibox-thumbnail98/fc09581c9c8d26a6f17d8bffae75d9be)

![Concept & Imagination sample 2](http://bj.bcebos.com/ibox-thumbnail98/07df5b3e65ccf6f8d1a0b6487a20065f)

![Posters & Character Worlds sample 2](http://bj.bcebos.com/ibox-thumbnail98/25a2b329979279b7e42159c67bf64f64)

![Posters & Character Worlds sample 3](http://bj.bcebos.com/ibox-thumbnail98/5fec5a162ae10e8baf1b0ac269a770c5)

![Narrative Illustration sample 4](http://bj.bcebos.com/ibox-thumbnail98/620984571a5a64255e6d7390048997a0)

![Portrait & Lifestyle sample 5](http://bj.bcebos.com/ibox-thumbnail98/0f10a97fa46dc6e5fdb3d96f2880f222)

![Information Design sample 6](http://bj.bcebos.com/ibox-thumbnail98/ecaefd430359a726be2043762510221e)

![Concept & Imagination sample 6](http://bj.bcebos.com/ibox-thumbnail98/f7681776a958c786b7e4509dd0344ed5)

![Information Design sample 7](http://bj.bcebos.com/ibox-thumbnail98/cd1f5fe1b355e502ec45ace2d81fd2da)

![Information Design sample 8](http://bj.bcebos.com/ibox-thumbnail98/25caf3d5bd5a4224b6722543384dc788)

![Portrait & Lifestyle sample 8](http://bj.bcebos.com/ibox-thumbnail98/4bd8d5381ef7885935534ed5cf3aeea5)

![Posters & Character Worlds sample 8](http://bj.bcebos.com/ibox-thumbnail98/373fea8c126c3b16adeec23279d468b2)

![Portrait & Lifestyle sample 9](http://bj.bcebos.com/ibox-thumbnail98/b013abf696f9a5205a5ba763a31d5b22)

![Concept & Imagination sample 9](http://bj.bcebos.com/ibox-thumbnail98/a817c712de129dbaa1593cc4f5bdd2a1)

![Concept & Imagination sample 10](http://bj.bcebos.com/ibox-thumbnail98/c62f94db9067598be9c3361438403a30)

![Portrait & Lifestyle sample 11](http://bj.bcebos.com/ibox-thumbnail98/4bbefbabca6ca04d88ac10091aa9457a)

![Concept & Imagination sample 11](http://bj.bcebos.com/ibox-thumbnail98/600c796dffc8fd93111d1adaaa1f1998)

![Portrait & Lifestyle sample 12](http://bj.bcebos.com/ibox-thumbnail98/42ac0b640fbd07d207e3be3a2bd04d68)

![Posters & Character Worlds sample 12](http://bj.bcebos.com/ibox-thumbnail98/707d7f1db3dafb02b455df41adfe274d)

![Information Design sample 14](http://bj.bcebos.com/ibox-thumbnail98/bee72ef4583a1d1edfdd637816e394c0)

![Posters & Character Worlds sample 14](http://bj.bcebos.com/ibox-thumbnail98/d94590e6bc9d95ff29930f148d5bca68)

![Portrait & Lifestyle sample 15](http://bj.bcebos.com/ibox-thumbnail98/dd1230463e3c252fd167d2f739bbb6f3)

![Information Design sample 16](http://bj.bcebos.com/ibox-thumbnail98/afb28d7955fdef91b264c2e5405e06d6)

![Posters & Character Worlds sample 16](http://bj.bcebos.com/ibox-thumbnail98/8146ac46b55fc003ead6cdb95e4f8166)

![Posters & Character Worlds sample 17](http://bj.bcebos.com/ibox-thumbnail98/10ffe3a3e368a4a436bb34b3c92c27b7)

![Information Design sample 18](http://bj.bcebos.com/ibox-thumbnail98/014e0c5788cde80749413265c8f4160e)

![Portrait & Lifestyle sample 20](http://bj.bcebos.com/ibox-thumbnail98/fee45d79afe857f1b7a6d17d1cebaba5)

![Portrait & Lifestyle sample 21](http://bj.bcebos.com/ibox-thumbnail98/1c6d331c3d64cf65c94cdb50713ad6ad)

![Portrait & Lifestyle sample 22](http://bj.bcebos.com/ibox-thumbnail98/90f525091f0319aa52c8e88171094ea0)

![Information Design sample 24](http://bj.bcebos.com/ibox-thumbnail98/06955a6d3d0105650cfdf64a87a31e11)

![Information Design sample 26](http://bj.bcebos.com/ibox-thumbnail98/bb96acd6b391258ca8046befe76b635c)

![Portrait & Lifestyle sample 27](http://bj.bcebos.com/ibox-thumbnail98/1360c975b5a35bf95ce9ead5b7135534)

![Information Design sample 29](http://bj.bcebos.com/ibox-thumbnail98/d7b0c329044e18de8f912a5ba970bbe6)

![Portrait & Lifestyle sample 1](http://bj.bcebos.com/ibox-thumbnail98/6aaf503a33d3a9f58b54dd2a7f2fe027)

![Concept & Imagination sample 1](http://bj.bcebos.com/ibox-thumbnail98/736df3ebc85988603d9348e735d55515)

![Information Design sample 2](http://bj.bcebos.com/ibox-thumbnail98/fc09581c9c8d26a6f17d8bffae75d9be)

![Concept & Imagination sample 2](http://bj.bcebos.com/ibox-thumbnail98/07df5b3e65ccf6f8d1a0b6487a20065f)

![Posters & Character Worlds sample 2](http://bj.bcebos.com/ibox-thumbnail98/25a2b329979279b7e42159c67bf64f64)

![Posters & Character Worlds sample 3](http://bj.bcebos.com/ibox-thumbnail98/5fec5a162ae10e8baf1b0ac269a770c5)

![Narrative Illustration sample 4](http://bj.bcebos.com/ibox-thumbnail98/620984571a5a64255e6d7390048997a0)

![Portrait & Lifestyle sample 5](http://bj.bcebos.com/ibox-thumbnail98/0f10a97fa46dc6e5fdb3d96f2880f222)

![Information Design sample 6](http://bj.bcebos.com/ibox-thumbnail98/ecaefd430359a726be2043762510221e)

![Concept & Imagination sample 6](http://bj.bcebos.com/ibox-thumbnail98/f7681776a958c786b7e4509dd0344ed5)

![Information Design sample 7](http://bj.bcebos.com/ibox-thumbnail98/cd1f5fe1b355e502ec45ace2d81fd2da)

![Information Design sample 8](http://bj.bcebos.com/ibox-thumbnail98/25caf3d5bd5a4224b6722543384dc788)

![Portrait & Lifestyle sample 8](http://bj.bcebos.com/ibox-thumbnail98/4bd8d5381ef7885935534ed5cf3aeea5)

![Posters & Character Worlds sample 8](http://bj.bcebos.com/ibox-thumbnail98/373fea8c126c3b16adeec23279d468b2)

![Portrait & Lifestyle sample 9](http://bj.bcebos.com/ibox-thumbnail98/b013abf696f9a5205a5ba763a31d5b22)

![Concept & Imagination sample 9](http://bj.bcebos.com/ibox-thumbnail98/a817c712de129dbaa1593cc4f5bdd2a1)

![Concept & Imagination sample 10](http://bj.bcebos.com/ibox-thumbnail98/c62f94db9067598be9c3361438403a30)

![Portrait & Lifestyle sample 11](http://bj.bcebos.com/ibox-thumbnail98/4bbefbabca6ca04d88ac10091aa9457a)

![Concept & Imagination sample 11](http://bj.bcebos.com/ibox-thumbnail98/600c796dffc8fd93111d1adaaa1f1998)

![Portrait & Lifestyle sample 12](http://bj.bcebos.com/ibox-thumbnail98/42ac0b640fbd07d207e3be3a2bd04d68)

![Posters & Character Worlds sample 12](http://bj.bcebos.com/ibox-thumbnail98/707d7f1db3dafb02b455df41adfe274d)

![Information Design sample 14](http://bj.bcebos.com/ibox-thumbnail98/bee72ef4583a1d1edfdd637816e394c0)

![Posters & Character Worlds sample 14](http://bj.bcebos.com/ibox-thumbnail98/d94590e6bc9d95ff29930f148d5bca68)

![Portrait & Lifestyle sample 15](http://bj.bcebos.com/ibox-thumbnail98/dd1230463e3c252fd167d2f739bbb6f3)

![Information Design sample 16](http://bj.bcebos.com/ibox-thumbnail98/afb28d7955fdef91b264c2e5405e06d6)

![Posters & Character Worlds sample 16](http://bj.bcebos.com/ibox-thumbnail98/8146ac46b55fc003ead6cdb95e4f8166)

![Posters & Character Worlds sample 17](http://bj.bcebos.com/ibox-thumbnail98/10ffe3a3e368a4a436bb34b3c92c27b7)

![Information Design sample 18](http://bj.bcebos.com/ibox-thumbnail98/014e0c5788cde80749413265c8f4160e)

![Portrait & Lifestyle sample 20](http://bj.bcebos.com/ibox-thumbnail98/fee45d79afe857f1b7a6d17d1cebaba5)

![Portrait & Lifestyle sample 21](http://bj.bcebos.com/ibox-thumbnail98/1c6d331c3d64cf65c94cdb50713ad6ad)

![Portrait & Lifestyle sample 22](http://bj.bcebos.com/ibox-thumbnail98/90f525091f0319aa52c8e88171094ea0)

![Information Design sample 24](http://bj.bcebos.com/ibox-thumbnail98/06955a6d3d0105650cfdf64a87a31e11)

![Information Design sample 26](http://bj.bcebos.com/ibox-thumbnail98/bb96acd6b391258ca8046befe76b635c)

![Portrait & Lifestyle sample 27](http://bj.bcebos.com/ibox-thumbnail98/1360c975b5a35bf95ce9ead5b7135534)

![Information Design sample 29](http://bj.bcebos.com/ibox-thumbnail98/d7b0c329044e18de8f912a5ba970bbe6)

![Portrait & Lifestyle sample 1](http://bj.bcebos.com/ibox-thumbnail98/6aaf503a33d3a9f58b54dd2a7f2fe027)

![Concept & Imagination sample 1](http://bj.bcebos.com/ibox-thumbnail98/736df3ebc85988603d9348e735d55515)

![Information Design sample 2](http://bj.bcebos.com/ibox-thumbnail98/fc09581c9c8d26a6f17d8bffae75d9be)

![Concept & Imagination sample 2](http://bj.bcebos.com/ibox-thumbnail98/07df5b3e65ccf6f8d1a0b6487a20065f)

![Posters & Character Worlds sample 2](http://bj.bcebos.com/ibox-thumbnail98/25a2b329979279b7e42159c67bf64f64)

![Posters & Character Worlds sample 3](http://bj.bcebos.com/ibox-thumbnail98/5fec5a162ae10e8baf1b0ac269a770c5)

![Narrative Illustration sample 4](http://bj.bcebos.com/ibox-thumbnail98/620984571a5a64255e6d7390048997a0)

![Portrait & Lifestyle sample 5](http://bj.bcebos.com/ibox-thumbnail98/0f10a97fa46dc6e5fdb3d96f2880f222)

![Information Design sample 6](http://bj.bcebos.com/ibox-thumbnail98/ecaefd430359a726be2043762510221e)

![Concept & Imagination sample 6](http://bj.bcebos.com/ibox-thumbnail98/f7681776a958c786b7e4509dd0344ed5)

![Information Design sample 7](http://bj.bcebos.com/ibox-thumbnail98/cd1f5fe1b355e502ec45ace2d81fd2da)

![Information Design sample 8](http://bj.bcebos.com/ibox-thumbnail98/25caf3d5bd5a4224b6722543384dc788)

![Portrait & Lifestyle sample 8](http://bj.bcebos.com/ibox-thumbnail98/4bd8d5381ef7885935534ed5cf3aeea5)

![Posters & Character Worlds sample 8](http://bj.bcebos.com/ibox-thumbnail98/373fea8c126c3b16adeec23279d468b2)

![Portrait & Lifestyle sample 9](http://bj.bcebos.com/ibox-thumbnail98/b013abf696f9a5205a5ba763a31d5b22)

![Concept & Imagination sample 9](http://bj.bcebos.com/ibox-thumbnail98/a817c712de129dbaa1593cc4f5bdd2a1)

![Concept & Imagination sample 10](http://bj.bcebos.com/ibox-thumbnail98/c62f94db9067598be9c3361438403a30)

![Portrait & Lifestyle sample 11](http://bj.bcebos.com/ibox-thumbnail98/4bbefbabca6ca04d88ac10091aa9457a)

![Concept & Imagination sample 11](http://bj.bcebos.com/ibox-thumbnail98/600c796dffc8fd93111d1adaaa1f1998)

![Portrait & Lifestyle sample 12](http://bj.bcebos.com/ibox-thumbnail98/42ac0b640fbd07d207e3be3a2bd04d68)

![Posters & Character Worlds sample 12](http://bj.bcebos.com/ibox-thumbnail98/707d7f1db3dafb02b455df41adfe274d)

![Information Design sample 14](http://bj.bcebos.com/ibox-thumbnail98/bee72ef4583a1d1edfdd637816e394c0)

![Posters & Character Worlds sample 14](http://bj.bcebos.com/ibox-thumbnail98/d94590e6bc9d95ff29930f148d5bca68)

![Portrait & Lifestyle sample 15](http://bj.bcebos.com/ibox-thumbnail98/dd1230463e3c252fd167d2f739bbb6f3)

![Information Design sample 16](http://bj.bcebos.com/ibox-thumbnail98/afb28d7955fdef91b264c2e5405e06d6)

![Posters & Character Worlds sample 16](http://bj.bcebos.com/ibox-thumbnail98/8146ac46b55fc003ead6cdb95e4f8166)

![Posters & Character Worlds sample 17](http://bj.bcebos.com/ibox-thumbnail98/10ffe3a3e368a4a436bb34b3c92c27b7)

![Information Design sample 18](http://bj.bcebos.com/ibox-thumbnail98/014e0c5788cde80749413265c8f4160e)

![Portrait & Lifestyle sample 20](http://bj.bcebos.com/ibox-thumbnail98/fee45d79afe857f1b7a6d17d1cebaba5)

![Portrait & Lifestyle sample 21](http://bj.bcebos.com/ibox-thumbnail98/1c6d331c3d64cf65c94cdb50713ad6ad)

![Portrait & Lifestyle sample 22](http://bj.bcebos.com/ibox-thumbnail98/90f525091f0319aa52c8e88171094ea0)

![Information Design sample 24](http://bj.bcebos.com/ibox-thumbnail98/06955a6d3d0105650cfdf64a87a31e11)

![Information Design sample 26](http://bj.bcebos.com/ibox-thumbnail98/bb96acd6b391258ca8046befe76b635c)

![Portrait & Lifestyle sample 27](http://bj.bcebos.com/ibox-thumbnail98/1360c975b5a35bf95ce9ead5b7135534)

![Information Design sample 29](http://bj.bcebos.com/ibox-thumbnail98/d7b0c329044e18de8f912a5ba970bbe6)

![Narrative Illustration sample 1](http://bj.bcebos.com/ibox-thumbnail98/e931ae5d6ac3de318b5dde86bdc806e1)

![Posters & Character Worlds sample 1](http://bj.bcebos.com/ibox-thumbnail98/f7ff11b1dc93de1708084cf0f4e0471c)

![Narrative Illustration sample 2](http://bj.bcebos.com/ibox-thumbnail98/9159b3bc6f93b9e3d56a2ae53bff0ad7)

![Portrait & Lifestyle sample 3](http://bj.bcebos.com/ibox-thumbnail98/7832595d1ce0081b717328ea293023b2)

![Narrative Illustration sample 3](http://bj.bcebos.com/ibox-thumbnail98/20eb26724ffef8ae40e8481aefe3bf6b)

![Concept & Imagination sample 3](http://bj.bcebos.com/ibox-thumbnail98/5d5129022ff190a541f2e893b3c1e9ca)

![Portrait & Lifestyle sample 4](http://bj.bcebos.com/ibox-thumbnail98/71f774737c28e2cce405eeba3c4ee40e)

![Information Design sample 5](http://bj.bcebos.com/ibox-thumbnail98/a351c6d6ca5160570d5f061d72648c54)

![Concept & Imagination sample 5](http://bj.bcebos.com/ibox-thumbnail98/24038d69ab396ea6059e6630cb0f86ff)

![Narrative Illustration sample 6](http://bj.bcebos.com/ibox-thumbnail98/ebe7b1d4b2b96252801d4624151e6e38)

![Portrait & Lifestyle sample 7](http://bj.bcebos.com/ibox-thumbnail98/7f1ea9b35cbc2ec30af086f1b0589adb)

![Concept & Imagination sample 7](http://bj.bcebos.com/ibox-thumbnail98/65324e0e9a97bf945a6d18d6a84a5f4f)

![Narrative Illustration sample 8](http://bj.bcebos.com/ibox-thumbnail98/a3fb66411f492bb02f57e1bf2de1d250)

![Information Design sample 9](http://bj.bcebos.com/ibox-thumbnail98/f0cce2b427a832744bd619e0a2a5d63a)

![Narrative Illustration sample 9](http://bj.bcebos.com/ibox-thumbnail98/db7b0fe7c05c4aa4b2172f8d1ee69664)

![Information Design sample 10](http://bj.bcebos.com/ibox-thumbnail98/169afc1e8c3685023a7445227bcfebb9)

![Narrative Illustration sample 10](http://bj.bcebos.com/ibox-thumbnail98/dfcc01139c7d99a3e520a05ae9f3fe8b)

![Posters & Character Worlds sample 10](http://bj.bcebos.com/ibox-thumbnail98/46a5d7d567ed6f4819f4ba88e4af784c)

![Posters & Character Worlds sample 11](http://bj.bcebos.com/ibox-thumbnail98/a3af30ef037b118b88a3b5196ff6f0f1)

![Narrative Illustration sample 12](http://bj.bcebos.com/ibox-thumbnail98/a484731fead684400c7ea57374fae931)

![Portrait & Lifestyle sample 13](http://bj.bcebos.com/ibox-thumbnail98/d30182a7859d2b43597f40ecd5a819f9)

![Posters & Character Worlds sample 13](http://bj.bcebos.com/ibox-thumbnail98/1723cfeab0f68e488befcc5d58c03c0f)

![Information Design sample 15](http://bj.bcebos.com/ibox-thumbnail98/953a405ea15582479ede6f4c5a281e22)

![Portrait & Lifestyle sample 16](http://bj.bcebos.com/ibox-thumbnail98/3da6082a4b93b8723b5cfe6bf024e4d8)

![Information Design sample 17](http://bj.bcebos.com/ibox-thumbnail98/940885440a052ac44d6e9b6589d9369d)

![Portrait & Lifestyle sample 18](http://bj.bcebos.com/ibox-thumbnail98/cdfee157c825afe1a58f23e047503726)

![Portrait & Lifestyle sample 19](http://bj.bcebos.com/ibox-thumbnail98/766fbcb06c6781e2833525dc4aa7913b)

![Information Design sample 20](http://bj.bcebos.com/ibox-thumbnail98/cb8510169b2e0f0d32dba318740d7bb5)

![Information Design sample 22](http://bj.bcebos.com/ibox-thumbnail98/181bbf038401e312fac0e476439e1a37)

![Portrait & Lifestyle sample 23](http://bj.bcebos.com/ibox-thumbnail98/6bdbeaf6c8c7a56e3402566fb16624c2)

![Information Design sample 25](http://bj.bcebos.com/ibox-thumbnail98/89fca45c2c938d67c2acc9c964ad5643)

![Portrait & Lifestyle sample 26](http://bj.bcebos.com/ibox-thumbnail98/ba6018bf0c762c057c6a7c06dcb0d240)

![Information Design sample 28](http://bj.bcebos.com/ibox-thumbnail98/090f9a19efe18af8a2eb54c67aaab78d)

![Information Design sample 30](http://bj.bcebos.com/ibox-thumbnail98/e9c2184ff9298c7b57e86e34c17ee447)

![Narrative Illustration sample 1](http://bj.bcebos.com/ibox-thumbnail98/e931ae5d6ac3de318b5dde86bdc806e1)

![Posters & Character Worlds sample 1](http://bj.bcebos.com/ibox-thumbnail98/f7ff11b1dc93de1708084cf0f4e0471c)

![Narrative Illustration sample 2](http://bj.bcebos.com/ibox-thumbnail98/9159b3bc6f93b9e3d56a2ae53bff0ad7)

![Portrait & Lifestyle sample 3](http://bj.bcebos.com/ibox-thumbnail98/7832595d1ce0081b717328ea293023b2)

![Narrative Illustration sample 3](http://bj.bcebos.com/ibox-thumbnail98/20eb26724ffef8ae40e8481aefe3bf6b)

![Concept & Imagination sample 3](http://bj.bcebos.com/ibox-thumbnail98/5d5129022ff190a541f2e893b3c1e9ca)

![Portrait & Lifestyle sample 4](http://bj.bcebos.com/ibox-thumbnail98/71f774737c28e2cce405eeba3c4ee40e)

![Information Design sample 5](http://bj.bcebos.com/ibox-thumbnail98/a351c6d6ca5160570d5f061d72648c54)

![Concept & Imagination sample 5](http://bj.bcebos.com/ibox-thumbnail98/24038d69ab396ea6059e6630cb0f86ff)

![Narrative Illustration sample 6](http://bj.bcebos.com/ibox-thumbnail98/ebe7b1d4b2b96252801d4624151e6e38)

![Portrait & Lifestyle sample 7](http://bj.bcebos.com/ibox-thumbnail98/7f1ea9b35cbc2ec30af086f1b0589adb)

![Concept & Imagination sample 7](http://bj.bcebos.com/ibox-thumbnail98/65324e0e9a97bf945a6d18d6a84a5f4f)

![Narrative Illustration sample 8](http://bj.bcebos.com/ibox-thumbnail98/a3fb66411f492bb02f57e1bf2de1d250)

![Information Design sample 9](http://bj.bcebos.com/ibox-thumbnail98/f0cce2b427a832744bd619e0a2a5d63a)

![Narrative Illustration sample 9](http://bj.bcebos.com/ibox-thumbnail98/db7b0fe7c05c4aa4b2172f8d1ee69664)

![Information Design sample 10](http://bj.bcebos.com/ibox-thumbnail98/169afc1e8c3685023a7445227bcfebb9)

![Narrative Illustration sample 10](http://bj.bcebos.com/ibox-thumbnail98/dfcc01139c7d99a3e520a05ae9f3fe8b)

![Posters & Character Worlds sample 10](http://bj.bcebos.com/ibox-thumbnail98/46a5d7d567ed6f4819f4ba88e4af784c)

![Posters & Character Worlds sample 11](http://bj.bcebos.com/ibox-thumbnail98/a3af30ef037b118b88a3b5196ff6f0f1)

![Narrative Illustration sample 12](http://bj.bcebos.com/ibox-thumbnail98/a484731fead684400c7ea57374fae931)

![Portrait & Lifestyle sample 13](http://bj.bcebos.com/ibox-thumbnail98/d30182a7859d2b43597f40ecd5a819f9)

![Posters & Character Worlds sample 13](http://bj.bcebos.com/ibox-thumbnail98/1723cfeab0f68e488befcc5d58c03c0f)

![Information Design sample 15](http://bj.bcebos.com/ibox-thumbnail98/953a405ea15582479ede6f4c5a281e22)

![Portrait & Lifestyle sample 16](http://bj.bcebos.com/ibox-thumbnail98/3da6082a4b93b8723b5cfe6bf024e4d8)

![Information Design sample 17](http://bj.bcebos.com/ibox-thumbnail98/940885440a052ac44d6e9b6589d9369d)

![Portrait & Lifestyle sample 18](http://bj.bcebos.com/ibox-thumbnail98/cdfee157c825afe1a58f23e047503726)

![Portrait & Lifestyle sample 19](http://bj.bcebos.com/ibox-thumbnail98/766fbcb06c6781e2833525dc4aa7913b)

![Information Design sample 20](http://bj.bcebos.com/ibox-thumbnail98/cb8510169b2e0f0d32dba318740d7bb5)

![Information Design sample 22](http://bj.bcebos.com/ibox-thumbnail98/181bbf038401e312fac0e476439e1a37)

![Portrait & Lifestyle sample 23](http://bj.bcebos.com/ibox-thumbnail98/6bdbeaf6c8c7a56e3402566fb16624c2)

![Information Design sample 25](http://bj.bcebos.com/ibox-thumbnail98/89fca45c2c938d67c2acc9c964ad5643)

![Portrait & Lifestyle sample 26](http://bj.bcebos.com/ibox-thumbnail98/ba6018bf0c762c057c6a7c06dcb0d240)

![Information Design sample 28](http://bj.bcebos.com/ibox-thumbnail98/090f9a19efe18af8a2eb54c67aaab78d)

![Information Design sample 30](http://bj.bcebos.com/ibox-thumbnail98/e9c2184ff9298c7b57e86e34c17ee447)

![Narrative Illustration sample 1](http://bj.bcebos.com/ibox-thumbnail98/e931ae5d6ac3de318b5dde86bdc806e1)

![Posters & Character Worlds sample 1](http://bj.bcebos.com/ibox-thumbnail98/f7ff11b1dc93de1708084cf0f4e0471c)

![Narrative Illustration sample 2](http://bj.bcebos.com/ibox-thumbnail98/9159b3bc6f93b9e3d56a2ae53bff0ad7)

![Portrait & Lifestyle sample 3](http://bj.bcebos.com/ibox-thumbnail98/7832595d1ce0081b717328ea293023b2)

![Narrative Illustration sample 3](http://bj.bcebos.com/ibox-thumbnail98/20eb26724ffef8ae40e8481aefe3bf6b)

![Concept & Imagination sample 3](http://bj.bcebos.com/ibox-thumbnail98/5d5129022ff190a541f2e893b3c1e9ca)

![Portrait & Lifestyle sample 4](http://bj.bcebos.com/ibox-thumbnail98/71f774737c28e2cce405eeba3c4ee40e)

![Information Design sample 5](http://bj.bcebos.com/ibox-thumbnail98/a351c6d6ca5160570d5f061d72648c54)

![Concept & Imagination sample 5](http://bj.bcebos.com/ibox-thumbnail98/24038d69ab396ea6059e6630cb0f86ff)

![Narrative Illustration sample 6](http://bj.bcebos.com/ibox-thumbnail98/ebe7b1d4b2b96252801d4624151e6e38)

![Portrait & Lifestyle sample 7](http://bj.bcebos.com/ibox-thumbnail98/7f1ea9b35cbc2ec30af086f1b0589adb)

![Concept & Imagination sample 7](http://bj.bcebos.com/ibox-thumbnail98/65324e0e9a97bf945a6d18d6a84a5f4f)

![Narrative Illustration sample 8](http://bj.bcebos.com/ibox-thumbnail98/a3fb66411f492bb02f57e1bf2de1d250)

![Information Design sample 9](http://bj.bcebos.com/ibox-thumbnail98/f0cce2b427a832744bd619e0a2a5d63a)

![Narrative Illustration sample 9](http://bj.bcebos.com/ibox-thumbnail98/db7b0fe7c05c4aa4b2172f8d1ee69664)

![Information Design sample 10](http://bj.bcebos.com/ibox-thumbnail98/169afc1e8c3685023a7445227bcfebb9)

![Narrative Illustration sample 10](http://bj.bcebos.com/ibox-thumbnail98/dfcc01139c7d99a3e520a05ae9f3fe8b)

![Posters & Character Worlds sample 10](http://bj.bcebos.com/ibox-thumbnail98/46a5d7d567ed6f4819f4ba88e4af784c)

![Posters & Character Worlds sample 11](http://bj.bcebos.com/ibox-thumbnail98/a3af30ef037b118b88a3b5196ff6f0f1)

![Narrative Illustration sample 12](http://bj.bcebos.com/ibox-thumbnail98/a484731fead684400c7ea57374fae931)

![Portrait & Lifestyle sample 13](http://bj.bcebos.com/ibox-thumbnail98/d30182a7859d2b43597f40ecd5a819f9)

![Posters & Character Worlds sample 13](http://bj.bcebos.com/ibox-thumbnail98/1723cfeab0f68e488befcc5d58c03c0f)

![Information Design sample 15](http://bj.bcebos.com/ibox-thumbnail98/953a405ea15582479ede6f4c5a281e22)

![Portrait & Lifestyle sample 16](http://bj.bcebos.com/ibox-thumbnail98/3da6082a4b93b8723b5cfe6bf024e4d8)

![Information Design sample 17](http://bj.bcebos.com/ibox-thumbnail98/940885440a052ac44d6e9b6589d9369d)

![Portrait & Lifestyle sample 18](http://bj.bcebos.com/ibox-thumbnail98/cdfee157c825afe1a58f23e047503726)

![Portrait & Lifestyle sample 19](http://bj.bcebos.com/ibox-thumbnail98/766fbcb06c6781e2833525dc4aa7913b)

![Information Design sample 20](http://bj.bcebos.com/ibox-thumbnail98/cb8510169b2e0f0d32dba318740d7bb5)

![Information Design sample 22](http://bj.bcebos.com/ibox-thumbnail98/181bbf038401e312fac0e476439e1a37)

![Portrait & Lifestyle sample 23](http://bj.bcebos.com/ibox-thumbnail98/6bdbeaf6c8c7a56e3402566fb16624c2)

![Information Design sample 25](http://bj.bcebos.com/ibox-thumbnail98/89fca45c2c938d67c2acc9c964ad5643)

![Portrait & Lifestyle sample 26](http://bj.bcebos.com/ibox-thumbnail98/ba6018bf0c762c057c6a7c06dcb0d240)

![Information Design sample 28](http://bj.bcebos.com/ibox-thumbnail98/090f9a19efe18af8a2eb54c67aaab78d)

![Information Design sample 30](http://bj.bcebos.com/ibox-thumbnail98/e9c2184ff9298c7b57e86e34c17ee447)

The images above are shown solely to demonstrate model capabilities and do not imply any commercial use or endorsement. The model is intended for non-commercial personal derivative creation.

### Posters and Design Layouts

ERNIE-Image excels at **posters and other layout-critical images**, combining strong visual focal points with reliable title placement, supporting text, and overall composition. Where many open weights models can produce a "poster-like" image but fall apart on typography or layout control, ERNIE-Image gets much closer to a usable design draft.

### Anime and Storyboards

ERNIE-Image handles **anime-style and storyboard generation** well — the challenge here goes beyond drawing appealing characters to maintaining expressions, action clarity, scene transitions, and panel-level organization. Its outputs read more like actual manga pages than disconnected illustrations, making it a good fit for narrative visual content.

### Multi-panel Visual Expression

Beyond single images, ERNIE-Image can produce **grouped and sequential visuals** — multi-panel compositions, meme-style image sets, and emotionally coherent grouped outputs. This cross-frame consistency is valuable when a task calls for pacing, progression, or repeated visual motifs rather than one isolated image.

### Multilingual Text Rendering

ERNIE-Image is especially good at **rendering readable, faithful multilingual text** in visually complex images — both **Chinese and English**, covering dense paragraphs, layout-sensitive titles, callout annotations, anime dialogue, and poster copy. In practice, text quality often decides whether an image is merely plausible or genuinely usable, which is what makes this one of the model's most consequential capabilities.

### Stylized and Film-like Aesthetics

Beyond clean graphic outputs, ERNIE-Image handles **distinctive stylized aesthetics** well — softer cinematic tones, film-like grain, and mood-driven visual expression. Many strong image models converge toward a similar high-saturation "AI look"; ERNIE-Image covers a broader aesthetic range with more recognizable stylistic character.

## 3. Model Results

We evaluate ERNIE-Image on four widely-used text-to-image generation benchmarks: **GenEval** (compositional generation), **OneIG-EN / OneIG-ZH** (open-domain image generation in English and Chinese), and **LongTextBench** (long-text rendering fidelity).

#### OneIG-EN

| model | Open Weights | Alignment | Text | Reasoning | Style | Diversity | Overall ↑ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Nano Banana 2.0🥇 | – | 0.8880 | 0.9440 | 0.3340 | 0.4810 | 0.2450 | 0.5780 |
| Seedream 4.5🥈 | – | 0.8910 | 0.9980 | 0.3500 | 0.4340 | 0.2070 | 0.5760 |
| ERNIEERNIE-Image (w/ PE)🥉 | ✓ | 0.8678 | 0.9788 | 0.3566 | 0.4309 | 0.2411 | 0.5750 |
| Seedream 4.0 | – | 0.8920 | 0.9830 | 0.3470 | 0.4530 | 0.1910 | 0.5730 |
| ERNIEERNIE-Image-Turbo (w/ PE) | ✓ | 0.8676 | 0.9666 | 0.3537 | 0.4191 | 0.2212 | 0.5656 |
| ERNIEERNIE-Image (w/o PE) | ✓ | 0.8909 | 0.9668 | 0.2950 | 0.4471 | 0.1687 | 0.5537 |
| Z-Image | ✓ | 0.8810 | 0.9870 | 0.2800 | 0.3870 | 0.1940 | 0.5460 |
| Qwen-Image | ✓ | 0.8820 | 0.8910 | 0.3060 | 0.4180 | 0.1970 | 0.5390 |
| ERNIEERNIE-Image-Turbo (w/o PE) | ✓ | 0.8795 | 0.9488 | 0.2913 | 0.4277 | 0.1232 | 0.5341 |
| GPT Image 1 [High] | – | 0.8510 | 0.8570 | 0.3450 | 0.4620 | 0.1510 | 0.5330 |
| FLUX.2-klein-9B | ✓ | 0.8871 | 0.8657 | 0.3117 | 0.4417 | 0.1560 | 0.5324 |
| Seedream 3.0 | – | 0.8180 | 0.8650 | 0.2750 | 0.4130 | 0.2770 | 0.5300 |
| Qwen-Image-2512 | ✓ | 0.8760 | 0.9900 | 0.2920 | 0.3380 | 0.1510 | 0.5300 |
| GLM-Image | ✓ | 0.8050 | 0.9690 | 0.2980 | 0.3530 | 0.2130 | 0.5280 |
| Z-Image-Turbo | ✓ | 0.8400 | 0.9940 | 0.2980 | 0.3680 | 0.1390 | 0.5280 |
| HiDream-I1-Full | ✓ | 0.8290 | 0.7070 | 0.3170 | 0.3470 | 0.1860 | 0.4770 |
| Kolors 2.0 | ✓ | 0.8200 | 0.4270 | 0.2620 | 0.3600 | 0.3000 | 0.4340 |
| BAGEL | ✓ | 0.7690 | 0.2440 | 0.1730 | 0.3670 | 0.2510 | 0.3610 |
| BLIP3-o | ✓ | 0.7110 | 0.1330 | 0.2230 | 0.3610 | 0.2290 | 0.3070 |
| Janus-Pro | ✓ | 0.5530 | 0.0010 | 0.1390 | 0.2760 | 0.3650 | 0.2670 |

#### OneIG-ZH

| model | Open Weights | Alignment | Text | Reasoning | Style | Diversity | Overall ↑ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Nano Banana 2.0🥇 | – | 0.8430 | 0.9830 | 0.3110 | 0.4610 | 0.2360 | 0.5670 |
| ERNIEERNIE-Image (w/ PE)🥈 | ✓ | 0.8299 | 0.9539 | 0.3056 | 0.4342 | 0.2478 | 0.5543 |
| Seedream 4.0🥉 | – | 0.8360 | 0.9860 | 0.3040 | 0.4430 | 0.2000 | 0.5540 |
| Seedream 4.5 | – | 0.8320 | 0.9860 | 0.3000 | 0.4260 | 0.2130 | 0.5510 |
| Qwen-Image | ✓ | 0.8250 | 0.9630 | 0.2670 | 0.4050 | 0.2790 | 0.5480 |
| ERNIEERNIE-Image-Turbo (w/ PE) | ✓ | 0.8258 | 0.9386 | 0.3043 | 0.4208 | 0.2281 | 0.5435 |
| Z-Image | ✓ | 0.7930 | 0.9880 | 0.2660 | 0.3860 | 0.2430 | 0.5350 |
| Seedream 3.0 | – | 0.7930 | 0.9280 | 0.2810 | 0.3970 | 0.2430 | 0.5280 |
| ERNIEERNIE-Image (w/o PE) | ✓ | 0.8421 | 0.8979 | 0.2656 | 0.4212 | 0.1772 | 0.5208 |
| Qwen-Image-2512 | ✓ | 0.8230 | 0.9830 | 0.2720 | 0.3420 | 0.1570 | 0.5150 |
| GLM-Image | ✓ | 0.7380 | 0.9760 | 0.2840 | 0.3350 | 0.2210 | 0.5110 |
| Z-Image-Turbo | ✓ | 0.7820 | 0.9820 | 0.2760 | 0.3610 | 0.1340 | 0.5070 |
| ERNIEERNIE-Image-Turbo (w/o PE) | ✓ | 0.8326 | 0.9086 | 0.2580 | 0.4002 | 0.1316 | 0.5062 |
| GPT Image 1 [High] | – | 0.8120 | 0.6500 | 0.3000 | 0.4490 | 0.1590 | 0.4740 |
| FLUX.2-klein-9B | ✓ | 0.8201 | 0.4920 | 0.2599 | 0.4166 | 0.1625 | 0.4302 |
| Kolors 2.0 | ✓ | 0.7380 | 0.5020 | 0.2260 | 0.3310 | 0.3330 | 0.4260 |
| BAGEL | ✓ | 0.6720 | 0.3650 | 0.1860 | 0.3570 | 0.2680 | 0.3700 |
| HiDream-I1-Full | ✓ | 0.6200 | 0.2050 | 0.2560 | 0.3040 | 0.3000 | 0.3370 |
| BLIP3-o | ✓ | 0.6080 | 0.0920 | 0.2130 | 0.3690 | 0.2330 | 0.3030 |
| Janus-Pro | ✓ | 0.3240 | 0.1480 | 0.1040 | 0.2640 | 0.3580 | 0.2400 |

#### LongTextBench

| model | Open Weights | LongText-Bench-EN | LongText-Bench-ZH | Overall ↑ |
| --- | --- | --- | --- | --- |
| Seedream 4.5🥇 | – | 0.9890 | 0.9873 | 0.9882 |
| ERNIEERNIE-Image (w/ PE)🥈 | ✓ | 0.9804 | 0.9661 | 0.9733 |
| GLM-Image🥉 | ✓ | 0.9524 | 0.9788 | 0.9656 |
| ERNIEERNIE-Image-Turbo (w/ PE) | ✓ | 0.9675 | 0.9636 | 0.9655 |
| Nano Banana 2.0 | – | 0.9808 | 0.9491 | 0.9650 |
| ERNIEERNIE-Image-Turbo (w/o PE) | ✓ | 0.9602 | 0.9675 | 0.9639 |
| ERNIEERNIE-Image (w/o PE) | ✓ | 0.9679 | 0.9594 | 0.9636 |
| Qwen-Image-2512 | ✓ | 0.9561 | 0.9647 | 0.9604 |
| Qwen-Image | ✓ | 0.9430 | 0.9460 | 0.9445 |
| Z-Image | ✓ | 0.9350 | 0.9360 | 0.9355 |
| Seedream 4.0 | – | 0.9214 | 0.9261 | 0.9238 |
| Z-Image-Turbo | ✓ | 0.9170 | 0.9260 | 0.9215 |
| Seedream 3.0 | – | 0.8960 | 0.8780 | 0.8870 |
| GPT Image 1 [High] | – | 0.9560 | 0.6190 | 0.7875 |
| FLUX.2-klein-9B | ✓ | 0.8642 | 0.2183 | 0.5413 |
| BAGEL | ✓ | 0.3730 | 0.3100 | 0.3415 |
| Kolors 2.0 | ✓ | 0.2580 | 0.3290 | 0.2935 |
| HiDream-I1-Full | ✓ | 0.5430 | 0.0240 | 0.2835 |
| BLIP3-o | ✓ | 0.0210 | 0.0180 | 0.0195 |
| Janus-Pro | ✓ | 0.0190 | 0.0060 | 0.0125 |

#### GenEval

| model | Open Weights | Single Object | Two Object | Counting | Colors | Position | Attribute Binding | Overall ↑ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ERNIEERNIE-Image (w/o PE)🥇 | ✓ | 1.0000 | 0.9596 | 0.7781 | 0.9282 | 0.8550 | 0.7925 | 0.8856 |
| ERNIEERNIE-Image (w/ PE)🥈 | ✓ | 0.9906 | 0.9596 | 0.8187 | 0.8830 | 0.8625 | 0.7225 | 0.8728 |
| Qwen-Image🥉 | ✓ | 0.9900 | 0.9200 | 0.8900 | 0.8800 | 0.7600 | 0.7700 | 0.8683 |
| ERNIEERNIE-Image-Turbo (w/o PE) | ✓ | 1.0000 | 0.9621 | 0.7906 | 0.9202 | 0.7975 | 0.7300 | 0.8667 |
| ERNIEERNIE-Image-Turbo (w/ PE) | ✓ | 0.9938 | 0.9419 | 0.8375 | 0.8351 | 0.7950 | 0.7025 | 0.8510 |
| FLUX.2-klein-9B | ✓ | 0.9313 | 0.9571 | 0.8281 | 0.9149 | 0.7175 | 0.7400 | 0.8481 |
| Seedream 3.0 | – | 0.9900 | 0.9600 | 0.9100 | 0.9300 | 0.4700 | 0.8000 | 0.8433 |
| Z-Image | ✓ | 1.0000 | 0.9400 | 0.7800 | 0.9300 | 0.6200 | 0.7700 | 0.8400 |
| GPT Image 1 | – | 0.9900 | 0.9200 | 0.8500 | 0.9200 | 0.7500 | 0.6100 | 0.8400 |
| HiDream-I1-Full | ✓ | 1.0000 | 0.9800 | 0.7900 | 0.9100 | 0.6000 | 0.7200 | 0.8333 |
| Z-Image-Turbo | ✓ | 1.0000 | 0.9500 | 0.7700 | 0.8900 | 0.6500 | 0.6800 | 0.8233 |
| Janus-Pro-7B | ✓ | 0.9900 | 0.8900 | 0.5900 | 0.9000 | 0.7900 | 0.6600 | 0.8000 |
| SD3.5-Large | ✓ | 0.9800 | 0.8900 | 0.7300 | 0.8300 | 0.3400 | 0.4700 | 0.7100 |
| FLUX.1 [Dev] | ✓ | 0.9800 | 0.8100 | 0.7400 | 0.7900 | 0.2200 | 0.4500 | 0.6600 |
| JanusFlow | ✓ | 0.9700 | 0.5900 | 0.4500 | 0.8300 | 0.5300 | 0.4200 | 0.6300 |
| SD3 Medium | ✓ | 0.9800 | 0.7400 | 0.6300 | 0.6700 | 0.3400 | 0.3600 | 0.6200 |
| Emu3-Gen | ✓ | 0.9800 | 0.7100 | 0.3400 | 0.8100 | 0.1700 | 0.2100 | 0.5400 |
| Show-o | ✓ | 0.9500 | 0.5200 | 0.4900 | 0.8200 | 0.1100 | 0.2800 | 0.5300 |
| PixArt-α | ✓ | 0.9800 | 0.5000 | 0.4400 | 0.8000 | 0.0800 | 0.0700 | 0.4800 |

### Key Findings

* •**Competitive with the best.** ERNIE-Image consistently places in the top 3 across all four benchmarks: **#1** on GenEval (0.8856), **#2** on OneIG-ZH (0.5543) and LongTextBench (0.9733), and **#3** on OneIG-EN (0.5750), going head-to-head with leading closed-source models such as Nano Banana 2.0 and Seedream 4.5.
* •**Strongest open weights model.** ERNIE-Image ranks **#1 among all open weights models** on every benchmark by a clear margin. These results come from just an **8B-parameter DiT backbone** — one of the most parameter-efficient architectures at this performance level.
* •**Excellent text rendering.** ERNIE-Image ranks **#2** on LongTextBench with strong performance in both English and Chinese long-text rendering, and posts highly competitive Text scores on both OneIG-EN and OneIG-ZH — underscoring its edge in multilingual text generation.

## 4. Prompt Enhancer (PE)

ERNIE-Image works best with long, detailed, well-structured prompts — richer descriptions tend to produce better generation quality, tighter instruction fidelity, and more faithful rendering of complex layouts or narrative content. In practice, though, users typically type a short sentence rather than the kind of detailed prompt that plays to the model's strengths.

To bridge this gap, we release a built-in **3B Prompt Enhancer** that expands short user inputs into more detailed, structured prompts better suited to ERNIE-Image. The goal is not to change the user's intent, but to translate concise requests into a form that gets more out of the model — especially for posters, anime, webpage layouts, game screenshots, and other structured visual tasks.

The examples below illustrate this effect. Without prompt enhancement, the model tends to interpret short prompts literally and incompletely. With our 3B Prompt Enhancer, prompts become more descriptive and structured, noticeably improving results in many scenarios. We also find that stronger LLMs can push this even further — a sign that prompt enhancement is a practical lever for getting more out of ERNIE-Image's long-prompt generation ability.

Solve AIME ProblemComic Strip StorytellingHD-2D RPG ScreenshotLLM Webpage

Source Prompt

Solve this problem on the whiteboard:
Find the number of positive integer palindromes written in base 10 with no zero digits, whose digits sum to 13. For example, 42124 has these properties. Recall that a palindrome is a number whose representation reads the same from left to right as from right to left.

w/o pe

![w/o pe](http://bj.bcebos.com/ibox-thumbnail98/04e1f589f13784849ae28d91bc60e5dd)

w/ peOur 3B Model

![w/ pe](http://bj.bcebos.com/ibox-thumbnail98/349d8a77fe24a9dd97c50993f61f7029)

w/ pe (LLMs)gemini-3.1-pro-preview

![w/ pe (LLMs)](http://bj.bcebos.com/ibox-thumbnail98/a2e24e984a91870515778414757cffe6)

Analysis

The source prompt asks the model to solve an AIME problem on a whiteboard. Without PE, the model simply copies the problem statement verbatim — with multiple spelling errors (e.g. "interger", "palindrimes") — and makes no attempt at a solution. With the 3B PE, a structured solution layout emerges — step decomposition, palindrome representation, combination enumeration — but the final answer is wrong (24; correct: 62), limited by the small model's reasoning capacity. With LLM enhancement, the whiteboard shows a complete, rigorous derivation: parity analysis, central-digit enumeration, the composition theorem, and the correct answer of 62, rendered in multi-color with professional formatting.

w/o pe

#### Without Prompt Enhancement

Given a brief prompt, ERNIE-Image tends toward a literal, surface-level interpretation — it faithfully renders the elements mentioned but won't inject domain knowledge, refine the layout, or fill in missing detail on its own. For tasks that need knowledge or complex structural planning, this literal reading falls short.

w/ pe

#### With Our 3B Prompt Enhancer

We release a lightweight prompt enhancement model based on a **fine-tuned Ministral 3B**. It expands brief user prompts into detailed, structured descriptions, noticeably lifting generation quality in many scenarios. At 3B parameters, though, it can fall short on tasks that demand deep domain knowledge (e.g., mathematical reasoning) or exceptionally rich world knowledge.

w/ pe (LLMs)

#### With Large LLM Enhancement

We find that using an LLM such as **gemini-3.1-pro-preview** for zero-shot prompt enhancement yields markedly better results across the board. With deeper world knowledge and stronger reasoning, the LLM produces information-dense, structurally precise prompts that bring out ERNIE-Image's full generation potential.

## 5. Conclusion

ERNIE-Image shows that a compact 8B model can rival much larger open weights text-to-image systems while staying practical for real-world use. Across the examples and benchmarks in this blog, the model demonstrates particular strengths in text rendering, complex instruction following, structured visual integrity, and stylistically diverse image generation. These capabilities matter most for high-value tasks like posters, anime, multi-panel layouts, and other scenarios where both visual quality and controllability count. We hope the released ERNIE-Image and ERNIE-Image-Turbo checkpoints serve as a useful open foundation for research, development, and creative applications.

### Get Started with ERNIE-Image

[#### ERNIE-Image

Main model on HuggingFace

Learn More](https://huggingface.co/Baidu/ERNIE-Image)[#### ERNIE-Image-Turbo

Fast 8-step distilled version

Learn More](https://huggingface.co/Baidu/ERNIE-Image-Turbo)[#### Prompt Gallery

Browse curated generation examples

Learn More](https://ernieimageprompt.com)

Copyright © 2025 Baidu, Inc. All Rights Reserved.
