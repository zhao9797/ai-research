---
library_name: hunyuan-dit
license: other
license_name: tencent-hunyuan-community
license_link: https://huggingface.co/Tencent-Hunyuan/HunyuanDiT/blob/main/LICENSE.txt
language:
- en
- zh
---
# Hunyuan-DiT : A Powerful Multi-Resolution Diffusion Transformer with Fine-Grained Chinese Understanding

This repo contains PyTorch model definitions, pre-trained weights and inference/sampling code for our paper exploring Hunyuan-DiT. You can find more visualizations on our [project page](https://dit.hunyuan.tencent.com/).

> [**Hunyuan-DiT: A Powerful Multi-Resolution Diffusion Transformer with Fine-Grained Chinese Understanding**](https://arxiv.org/abs/2405.08748) <br>

> [**DialogGen: Multi-modal Interactive Dialogue System for Multi-turn Text-to-Image Generation**](https://arxiv.org/abs/2403.08857) <br>

## 🔥🔥🔥 News!!
* Jul 15, 2024: 🚀 HunYuanDiT and Shakker.Ai have jointly launched a fine-tuning event based on the HunYuanDiT 1.2 model. By publishing a lora or fine-tuned model based on HunYuanDiT, you can earn up to $230 bonus from Shakker.Ai. See [Shakker.Ai](https://www.shakker.ai/activitys/shaker-the-world-hunyuan) for more details.
* Jul 15, 2024: :tada: Update ComfyUI to support standardized workflows and compatibility with weights from t2i module and Lora training for versions 1.1/1.2, as well as those trained by Kohya or the official script. See [ComfyUI](https://github.com/Tencent/HunyuanDiT/tree/main/comfyui-hydit) for details.
* Jul 15, 2024: :zap: We offer Docker environments for CUDA 11/12, allowing you to bypass complex installations and play with a single click! See [dockers](https://github.com/Tencent/HunyuanDiT?tab=readme-ov-file#installation-guide-for-linux) for details. 
* Jul 08, 2024: :tada: HYDiT-v1.2 version is released. Please check [HunyuanDiT-v1.2](https://huggingface.co/Tencent-Hunyuan/HunyuanDiT-v1.2) and [Distillation-v1.2](https://huggingface.co/Tencent-Hunyuan/Distillation-v1.2) for more details.
* Jul 03, 2024: :tada: Kohya-hydit version now available for v1.1 and v1.2 models, with GUI for inference. Official Kohya version is under review. See [kohya](https://github.com/Tencent/HunyuanDiT/tree/main/kohya_ss-hydit) for details.
* Jun 27, 2024: :art: Hunyuan-Captioner is released, providing fine-grained caption for training data. See [mllm](https://github.com/Tencent/HunyuanDiT/tree/main/mllm) for details.
* Jun 27, 2024: :tada: Support LoRa and ControlNet in diffusers. See [diffusers](https://github.com/Tencent/HunyuanDiT/tree/main/diffusers) for details.
* Jun 27, 2024: :tada: 6GB GPU VRAM Inference scripts are released. See [lite](https://github.com/Tencent/HunyuanDiT/tree/main/lite) for details.
* Jun 19, 2024: :tada: ControlNet is released, supporting canny, pose and depth control. See [training/inference codes](https://github.com/Tencent/HunyuanDiT?tab=readme-ov-file#controlnet) for details.
* Jun 13, 2024: :zap: HYDiT-v1.1 version is released, which mitigates the issue of image oversaturation and alleviates the watermark issue. Please check [HunyuanDiT-v1.1](https://huggingface.co/Tencent-Hunyuan/HunyuanDiT-v1.1) and 
[Distillation-v1.1](https://huggingface.co/Tencent-Hunyuan/Distillation-v1.1) for more details.
* Jun 13, 2024: :truck: The training code is released, offering [full-parameter training](https://github.com/Tencent/HunyuanDiT?tab=readme-ov-file#full-parameter-training) and [LoRA training](https://github.com/Tencent/HunyuanDiT?tab=readme-ov-file#lora).
* Jun 06, 2024: :tada: Hunyuan-DiT is now available in ComfyUI. Please check [ComfyUI](https://github.com/Tencent/HunyuanDiT?tab=readme-ov-file#using-comfyui) for more details.
* Jun 06, 2024: 🚀 We introduce Distillation version for Hunyuan-DiT acceleration, which achieves **50%** acceleration on NVIDIA GPUs. Please check [Distillation](https://huggingface.co/Tencent-Hunyuan/Distillation) for more details.
* Jun 05, 2024: 🤗 Hunyuan-DiT is now available in 🤗 Diffusers! Please check the [example](https://github.com/Tencent/HunyuanDiT?tab=readme-ov-file#using--diffusers) below.
* Jun 04, 2024: :globe_with_meridians: Support Tencent Cloud links to download the pretrained models! Please check the [links](https://github.com/Tencent/HunyuanDiT?tab=readme-ov-file#-download-pretrained-models) below.
* May 22, 2024: 🚀 We introduce TensorRT version for Hunyuan-DiT acceleration, which achieves **47%** acceleration on NVIDIA GPUs. Please check [TensorRT-libs](https://huggingface.co/Tencent-Hunyuan/TensorRT-libs) for instructions.
* May 22, 2024: 💬 We support demo running multi-turn text2image generation now. Please check the [script](https://github.com/Tencent/HunyuanDiT?tab=readme-ov-file#using-gradio) below.