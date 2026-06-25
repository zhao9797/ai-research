---
license: mit
pipeline_tag: text-to-video
library_name: diffusers
---

<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github.com/kandinskylab/kandinsky-5/raw/main/assets/KANDINSKY_LOGO_1_WHITE.png">
    <source media="(prefers-color-scheme: light)" srcset="https://github.com/kandinskylab/kandinsky-5/raw/main/assets/KANDINSKY_LOGO_1_BLACK.png">
    <img alt="Kandinsky Logo" src="https://user-images.githubusercontent.com/25423296/163456779-a8556205-d0a5-45e2-ac17-42d089e3c3f8.png">
  </picture>
</div>


<div align="center">
  <a href="https://habr.com/ru/companies/sberbank/articles/951800/">Habr</a> | <a href="https://kandinskylab.ai/">Project Page</a> | <a href="https://arxiv.org/abs/2511.14993">Technical Report</a> | 🤗 <a href=https://huggingface.co/collections/kandinskylab/kandinsky-50-video-lite> Video Lite </a> / <a href=https://huggingface.co/collections/kandinskylab/kandinsky-50-video-pro> Video Pro </a> / <a href=https://huggingface.co/collections/kandinskylab/kandinsky-50-image-lite> Image Lite </a> | <a href="https://huggingface.co/docs/diffusers/main/en/api/pipelines/kandinsky5"> 🤗 Diffusers </a>  | <a href="https://github.com/kandinskylab/kandinsky-5/blob/main/comfyui/README.md">ComfyUI</a>
</div>

<h1>Kandinsky 5.0: A family of diffusion models for Video & Image generation</h1>

In this repository, we provide a family of diffusion models to generate a video or an image given a textual prompt and/or image.



https://github.com/user-attachments/assets/b06f56de-1b05-4def-a611-1a3159ed71b0



## Kandinsky 5.0 Video Pro

Kandinsky 5.0 Video Pro is a line-up of 19B models that generates high-quality HD videos from English and Russian prompts with controllable camera motion.

We provide several Text-to-Video model variants, each optimized for different use cases:

* SFT model — delivers the highest generation quality;

* Pretrain model — designed for fine-tuning by researchers and enthusiasts.

All models are available in two versions: for generating 5-second and 10-second videos.

Additionally, we provide Image-to-Video model capable to generate video given input image and text prompt.

### Model Zoo

| Model                               | config | video duration | NFE | Checkpoint | Latency* |
|-------------------------------------|--------|----------------|-----|------------|----------------|
| Kandinsky 5.0 T2V Pro SFT 5s HD       | configs/k5_pro_t2v_5s_sft_hd.yaml | 5s             | 100 |🤗 [HF](https://huggingface.co/kandinskylab/Kandinsky-5.0-T2V-Pro-sft-5s) |      1241     |
| Kandinsky 5.0 T2V Pro SFT 10s HD     |configs/k5_pro_t2v_10s_sft_hd.yaml| 10s            | 100 |🤗 [HF](https://huggingface.co/kandinskylab/Kandinsky-5.0-T2V-Pro-sft-10s) |      -     |
| Kandinsky 5.0 T2V Pro SFT 5s SD       | configs/k5_pro_t2v_5s_sft_sd.yaml | 5s             | 100 |🤗 [HF](https://huggingface.co/kandinskylab/Kandinsky-5.0-T2V-Pro-sft-5s) |      560     |
| Kandinsky 5.0 T2V Pro SFT 10s SD     |configs/k5_pro_t2v_10s_sft_sd.yaml| 10s            | 100 |🤗 [HF](https://huggingface.co/kandinskylab/Kandinsky-5.0-T2V-Pro-sft-10s) |      1158     |
| Kandinsky 5.0 T2V Pro pretrain 5s HD     |-| 5s            | 100 |🤗 [HF](https://huggingface.co/kandinskylab/Kandinsky-5.0-T2V-Pro-pretrain-5s) |      1241     |
| Kandinsky 5.0 T2V Pro pretrain 10s HD     |-| 10s            | 100 |🤗 [HF](https://huggingface.co/kandinskylab/Kandinsky-5.0-T2V-Pro-pretrain-10s) |      -     |
| Kandinsky 5.0 T2V Pro pretrain 5s SD     |-| 5s            | 100 |🤗 [HF](https://huggingface.co/kandinskylab/Kandinsky-5.0-T2V-Pro-pretrain-5s) |      560     |
| Kandinsky 5.0 T2V Pro pretrain 10s SD     |-| 10s            | 100 |🤗 [HF](https://huggingface.co/kandinskylab/Kandinsky-5.0-T2V-Pro-pretrain-10s) |      1158     |
| Kandinsky 5.0 I2V Pro HD 5s       | configs/k5_pro_i2v_5s_sft_hd.yaml | 5s             | 100 |🤗 [HF](https://huggingface.co/kandinskylab/Kandinsky-5.0-I2V-Pro-sft-5s) |      -     |
| Kandinsky 5.0 I2V Pro SD 5s       | configs/k5_pro_i2v_5s_sft_sd.yaml | 5s             | 100 |🤗 [HF](https://huggingface.co/kandinskylab/Kandinsky-5.0-I2V-Pro-sft-5s) |      -     |

*Latency was measured after the second inference run. The first run of the model can be slower due to the compilation process. Inference was measured on an NVIDIA H100 GPU with 80 GB of memory, using CUDA 12.8.1 and PyTorch 2.8. For 5-second models Flash Attention 3 was used.

### Examples:

<table border="0" style="width: 100; text-align: left; margin-top: 20px;">
  <tr>
      <td>
          <video src="https://cdn-uploads.huggingface.co/production/uploads/678781c9e3c3c0163db4f99c/9sB-kQpsICq-dcVIajiyI.mp4" width=100 controls autoplay loop></video>
      </td>
      <td>
          <video src="https://cdn-uploads.huggingface.co/production/uploads/678781c9e3c3c0163db4f99c/GpRobj3LvOHtbtqLNz9mC.mp4" width=100 controls autoplay loop></video>
      </td>
      <td>
          <video src="https://cdn-uploads.huggingface.co/production/uploads/678781c9e3c3c0163db4f99c/tXdz7zzTD0jnZRoNnwy53.mp4" width=100 controls autoplay loop></video>
      </td>
     
  </tr>
  <tr>
      <td>
          <video src="https://cdn-uploads.huggingface.co/production/uploads/678781c9e3c3c0163db4f99c/7M4h8Q8r4aBQIB9I_Nm0B.mp4" width=100 controls autoplay loop></video>
      </td>
      <td>
          <video src="https://cdn-uploads.huggingface.co/production/uploads/678781c9e3c3c0163db4f99c/cCiLiFxBdFLekFro6qokX.mp4" width=100 controls autoplay loop></video>
      </td>
      <td>
          <video src="https://cdn-uploads.huggingface.co/production/uploads/678781c9e3c3c0163db4f99c/wBvOFtckxOiY0-NkT7MHK.mp4" width=100 controls autoplay loop></video>
      </td>
  </tr>
  <tr>
      <td>
          <video src="https://cdn-uploads.huggingface.co/production/uploads/678781c9e3c3c0163db4f99c/b0VOCqS6elgqh59mkw2XA.mp4" width=100 controls autoplay loop></video>
      </td>
      <td>
          <video src="https://cdn-uploads.huggingface.co/production/uploads/678781c9e3c3c0163db4f99c/NXiimel04zauXjcE1vf90.mp4" width=100 controls autoplay loop></video>
      </td>
      <td>
          <video src="https://cdn-uploads.huggingface.co/production/uploads/678781c9e3c3c0163db4f99c/T6bRN55KURwF25zO7TgkY.mp4" width=100 controls autoplay loop></video>
      </td>
  </tr>

</table>

### Results:

#### Side-by-Side evaluation

<table border="0" style="width: 200; text-align: left; margin-top: 20px;">
  <tr>
      <td>
          <img width="200" alt="image" src="https://cdn-uploads.huggingface.co/production/uploads/678781c9e3c3c0163db4f99c/5IMS5n1daytAJjmIiETjW.png" /></img>
      </td>
      <td>
         <img width="200" alt="image" src="https://cdn-uploads.huggingface.co/production/uploads/678781c9e3c3c0163db4f99c/sy-SGNlgg91HqFM4ASYXp.png" /></img>
      </td>

  <tr>
      <td>
          Comparison with Veo 3 
      </td>
      <td>
          Comparison with Veo 3 fast
      </td>
  <tr>
      <td>
          <img width="200" alt="image" src="https://cdn-uploads.huggingface.co/production/uploads/678781c9e3c3c0163db4f99c/l1u3fHIcCDhYC8j-AuqqK.png" /></img>
      </td>
      <td>
          <img width="200" alt="image" src="https://cdn-uploads.huggingface.co/production/uploads/678781c9e3c3c0163db4f99c/dUqLsyT5ADHRNqWsYpVPf.png" /></img>
      </td>
  <tr>
      <td>
          Comparison with Wan 2.2 A14B Text-to-Video mode
      </td>
      <td>
          Comparison with Wan 2.2 A14B Image-to-Video mode
      </td>

</table>



## Quickstart

#### Installation
Clone the repo:
```sh
git clone https://github.com/kandinskylab/kandinsky-5.git
cd kandinsky-5
```

Install dependencies:
```sh
pip install -r requirements.txt
```

To improve inference performance on NVidia Hopper GPUs, we recommend installing [Flash Attention 3](https://github.com/Dao-AILab/flash-attention/?tab=readme-ov-file#flashattention-3-beta-release).

#### Model Download
```sh
python download_models.py
```
use `models` argument to download some specific models, otherwise all models will be downloaded

example to download only `kandinskylab/Kandinsky-5.0-T2V-Lite-sft-5s` and `kandinskylab/Kandinsky-5.0-T2V-Pro-sft-5s`:
```sh
python download_models.py --models kandinskylab/Kandinsky-5.0-T2V-Lite-sft-5s,kandinskylab/Kandinsky-5.0-T2V-Pro-sft-5s
```

#### Run Kandinsky 5.0 T2V Lite SFT 5s

```sh
python test.py --prompt "A dog in red hat"
```

#### Run Kandinsky 5.0 T2V Lite SFT 10s 

```sh
python test.py --config ./configs/k5_lite_t2v_10s_sft_sd.yaml --prompt "A dog in red hat" --video_duration 10 
```


#### Run Kandinsky 5.0 I2V Lite 5s

```sh
python test.py --config ./configs/k5_lite_i2v_5s_sft_sd.yaml --prompt "The bear plays balalaika." --image "./assets/test_image.jpg" --video_duration 5
```


### T2V Inference

```python
import torch
from kandinsky import get_T2V_pipeline

device_map = {
    "dit": torch.device('cuda:0'), 
    "vae": torch.device('cuda:0'), 
    "text_embedder": torch.device('cuda:0')
}

pipe = get_T2V_pipeline(device_map, conf_path="configs/k5_lite_t2v_5s_sft_sd.yaml")

images = pipe(
    seed=42,
    time_length=5,
    width=768,
    height=512,
    save_path="./test.mp4",
    text="A cat in a red hat",
)
```

### I2V Inference

```python
import torch
from kandinsky import get_I2V_pipeline

device_map = {
    "dit": torch.device('cuda:0'), 
    "vae": torch.device('cuda:0'), 
    "text_embedder": torch.device('cuda:0')
}

pipe = get_I2V_pipeline(device_map, conf_path="configs/k5_lite_i2v_5s_sft_sd.yaml")

images = pipe(
    seed=42,
    time_length=5,
    save_path='./test.mp4',
    text="The bear plays balalaika.",
    image = "assets/test_image.jpg",
)
```


Please, refer to examples folder in github for more examples in various notebooks.

### Distributed Inference

For a faster inference, we also provide the capability to perform inference in a distributed way:
```
NUMBER_OF_NODES=1
NUMBER_OF_DEVICES_PER_NODE=1 / 2 / 4
python -m torch.distributed.launch --nnodes $NUMBER_OF_NODES --nproc-per-node $NUMBER_OF_DEVICES_PER_NODE test.py
```

### Optimized Inference

#### Offloading
For less memory consumption you can use **offloading** of the models.
```sh
python test.py --prompt "A dog in red hat" --offload
```

#### Magcache
Also we provide [Magcache](https://github.com/Zehong-Ma/MagCache) inference for faster generations (now available for sft 5s and sft 10s checkpoints).

```sh
python test.py --prompt "A dog in red hat" --magcache
```

#### Qwen encoder quantization
To reduce GPU memory needed for Qwen encoder we provide option to use NF4-quantized version from [bitsandbytes](https://github.com/bitsandbytes-foundation/bitsandbytes).

```sh
python test.py --prompt "A dog in red hat" --qwen_quantization
```

#### Attention engine selection
Depending on your hardware you can use the follwing full attention algorithm implementation:
* PyTorch [SDPA](https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html)
* [Flash Attention 2](https://github.com/Dao-AILab/flash-attention)
* [Flash Attention 3](https://github.com/Dao-AILab/flash-attention/tree/main/hopper)
* [Sage Attention](https://github.com/thu-ml/SageAttention)

The attention algorithm can be selected using an option "--attention_engine" of test.py script for 5 second (and less) video generation. For 10-second generation we use sparse attention algorithm [NABLA](https://arxiv.org/abs/2507.13546).

Note that currently (19 Oct. 2025) version build from source contains a bug and produces noisy output. A temporary workaround to fix it is decribed [here](https://github.com/thu-ml/SageAttention/issues/277).

```sh
python test.py --prompt "A dog in red hat" --attention_engine=flash_attention_3
```

```sh
python test.py --prompt "A dog in red hat" --attention_engine=flash_attention_2
```

```sh
python test.py --prompt "A dog in red hat" --attention_engine=sdpa
```

```sh
python test.py --prompt "A dog in red hat" --attention_engine=sage
```

By default we use option --attention_engine=auto which enables automatic selection of the most optimal algorithm installed in your system.


### CacheDiT

cache-dit offers Fully Cache Acceleration support for Kandinsky-5 with DBCache, TaylorSeer and Cache CFG. Visit their [example](https://github.com/vipshop/cache-dit/blob/main/examples/pipeline/run_kandinsky5_t2v.py) for more details.

### Beta testing
You can apply to participate in the beta testing of the Kandinsky Video Lite via the [telegram bot](https://t.me/kandinsky_access_bot).


# Authors


<B>Core Contributors</B>:
- <B>Video</B>: Alexey Letunovskiy, Maria Kovaleva, Lev Novitskiy, Denis Koposov, Dmitrii
Mikhailov, Anastasiia Kargapoltseva, Anna Dmitrienko, Anastasia Maltseva
- <B>Image & Editing</B>: Nikolai Vaulin, Nikita Kiselev, Alexander Varlamov
- <B>Pre-training Data</B>: Ivan Kirillov, Andrey Shutkin, Nikolai Vaulin, Ilya Vasiliev
- <B>Post-training Data</B>: Julia Agafonova, Anna Averchenkova, Olga Kim
- <B>Research Consolidation & Paper</B>: Viacheslav Vasilev, Vladimir Polovnikov
  
<B>Contributors</B>: Yury Kolabushin, Kirill Chernyshev, Alexander Belykh, Mikhail Mamaev, Anastasia Aliaskina, Kormilitsyn Semen, Tatiana Nikulina, Olga Vdovchenko, Polina Mikhailova, Polina
Gavrilova, Nikita Osterov, Bulat Akhmatov

<B>Track Leaders</B>: Vladimir Arkhipkin, Vladimir Korviakov, Nikolai Gerasimenko, Denis
Parkhomenko

<B>Project Supervisor</B>: Denis Dimitrov


# Citation

```
@misc{arkhipkin2025kandinsky50familyfoundation,
      title={Kandinsky 5.0: A Family of Foundation Models for Image and Video Generation}, 
      author={Vladimir Arkhipkin and Vladimir Korviakov and Nikolai Gerasimenko and Denis Parkhomenko and Viacheslav Vasilev and Alexey Letunovskiy and Nikolai Vaulin and Maria Kovaleva and Ivan Kirillov and Lev Novitskiy and Denis Koposov and Nikita Kiselev and Alexander Varlamov and Dmitrii Mikhailov and Vladimir Polovnikov and Andrey Shutkin and Julia Agafonova and Ilya Vasiliev and Anastasiia Kargapoltseva and Anna Dmitrienko and Anastasia Maltseva and Anna Averchenkova and Olga Kim and Tatiana Nikulina and Denis Dimitrov},
      year={2025},
      eprint={2511.14993},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2511.14993}, 
}

@misc{mikhailov2025nablanablaneighborhoodadaptiveblocklevel,
      title={$\nabla$NABLA: Neighborhood Adaptive Block-Level Attention}, 
      author={Dmitrii Mikhailov and Aleksey Letunovskiy and Maria Kovaleva and Vladimir Arkhipkin
              and Vladimir Korviakov and Vladimir Polovnikov and Viacheslav Vasilev
              and Evelina Sidorova and Denis Dimitrov},
      year={2025},
      eprint={2507.13546},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2507.13546}, 
}
```

# Acknowledgements

We gratefully acknowledge the open-source projects and research that made Kandinsky 5.0 possible:

- [PyTorch](https://pytorch.org/) — for model training and inference.  
- [FlashAttention 3](https://github.com/Dao-AILab/flash-attention) — for efficient attention and faster inference.  
- [Qwen2.5-VL](https://github.com/QwenLM/Qwen3-VL) — for providing high-quality text embeddings.  
- [CLIP](https://github.com/openai/CLIP) — for robust text–image alignment.  
- [HunyuanVideo](https://huggingface.co/tencent/HunyuanVideo) — for video latent encoding and decoding.  
- [MagCache](https://github.com/Zehong-Ma/MagCache) — for accelerated inference.
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI) — for integration into node-based workflows.  

We deeply appreciate the contributions of these communities and researchers to the open-source ecosystem.

