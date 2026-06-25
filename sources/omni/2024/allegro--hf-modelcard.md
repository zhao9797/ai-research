---
license: apache-2.0
language:
- en
library_name: diffusers
pipeline_tag: text-to-video
---
<p align="center">
<img src="https://huggingface.co/rhymes-ai/Allegro/resolve/main/banner_white.gif">
</p>
<p align="center">
 <a href="https://rhymes.ai/allegro_gallery" target="_blank"> Gallery</a> · <a href="https://github.com/rhymes-ai/Allegro" target="_blank">GitHub</a> · <a href="https://rhymes.ai/blog-details/allegro-advanced-video-generation-model" target="_blank">Blog</a> · <a href="https://arxiv.org/abs/2410.15458" target="_blank">Paper</a> · <a href="https://discord.com/invite/u8HxU23myj" target="_blank">Discord</a> · <a href="https://docs.google.com/forms/d/e/1FAIpQLSfq4Ez48jqZ7ncI7i4GuL7UyCrltfdtrOCDnm_duXxlvh5YmQ/viewform" target="_blank">Join Waitlist</a> (Try it on Discord!)  
   
</p> 

# Gallery
<img src="https://huggingface.co/rhymes-ai/Allegro/resolve/main/gallery.gif" width="1000" height="800"/>For more demos and corresponding prompts, see the [Allegro Gallery](https://rhymes.ai/allegro_gallery).


# Key Feature 

- **Open Source**: Full [model weights](https://huggingface.co/rhymes-ai/Allegro) and [code](https://github.com/rhymes-ai/Allegro) available to the community, Apache 2.0!
- **Versatile Content Creation**: Capable of generating a wide range of content, from close-ups of humans and animals to diverse dynamic scenes.
- **High-Quality Output**: Generate detailed 6-second videos at 15 FPS with 720x1280 resolution, which can be interpolated to 30 FPS with [EMA-VFI](https://github.com/MCG-NJU/EMA-VFI).
- **Small and Efficient**: Features a 175M parameter VideoVAE and a 2.8B parameter VideoDiT model. Supports multiple precisions (FP32, BF16, FP16) and uses 9.3 GB of GPU memory in BF16 mode with CPU offloading. Context length is 79.2K, equivalent to 88 frames.

# Model info 

<table>
  <tr>
    <th>Model</th>
    <td>Allegro</td>
  </tr>
  <tr>
    <th>Description</th>
    <td>Text-to-Video Generation Model</td>
  </tr>
  <tr>
    <th>Download</th>
    <td><a href="https://huggingface.co/rhymes-ai/Allegro">Hugging Face</a></td>
  </tr>
  <tr>
    <th rowspan="2">Parameter</th>
    <td>VAE: 175M</td>
  </tr>
  <tr>
    <td>DiT: 2.8B</td>
  </tr>
  <tr>
    <th rowspan="2">Inference Precision</th>
    <td>VAE: FP32/TF32/BF16/FP16 (best in FP32/TF32)</td>
  </tr>
  <tr>
    <td>DiT/T5: BF16/FP32/TF32</td>
  </tr>
  <tr>
    <th>Context Length</th>
    <td>79.2K</td>
  </tr>
  <tr>
    <th>Resolution</th>
    <td>720 x 1280</td>
  </tr>
  <tr>
    <th>Frames</th>
    <td>88</td>
  </tr>
  <tr>
    <th>Video Length</th>
    <td>6 seconds @ 15 FPS</td>
  </tr>
  <tr>
    <th>Single GPU Memory Usage</th>
    <td>9.3G BF16 (with cpu_offload)</td>
  </tr>
</table>


# Quick start

1. Install the necessary requirements.
     
   - Ensure Python >= 3.10, PyTorch >= 2.4, CUDA >= 12.4.
       
   - It is recommended to use Anaconda to create a new environment (Python >= 3.10) `conda create -n rllegro python=3.10 -y` to run the following example.
  
   - run `pip install git+https://github.com/huggingface/diffusers.git torch==2.4.1 transformers==4.40.1 accelerate sentencepiece imageio imageio-ffmpeg beautifulsoup4` 
 
2. Run inference.
    ```python
    import torch
    from diffusers import AutoencoderKLAllegro, AllegroPipeline
    from diffusers.utils import export_to_video
    vae = AutoencoderKLAllegro.from_pretrained("rhymes-ai/Allegro", subfolder="vae", torch_dtype=torch.float32)
    pipe = AllegroPipeline.from_pretrained(
        "rhymes-ai/Allegro", vae=vae, torch_dtype=torch.bfloat16
    )
    pipe.to("cuda")
    pipe.vae.enable_tiling()
    prompt = "A seaside harbor with bright sunlight and sparkling seawater, with many boats in the water. From an aerial view, the boats vary in size and color, some moving and some stationary. Fishing boats in the water suggest that this location might be a popular spot for docking fishing boats."
    
    positive_prompt = """
    (masterpiece), (best quality), (ultra-detailed), (unwatermarked), 
    {} 
    emotional, harmonious, vignette, 4k epic detailed, shot on kodak, 35mm photo, 
    sharp focus, high budget, cinemascope, moody, epic, gorgeous
    """
    
    negative_prompt = """
    nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, 
    low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry.
    """
    
    prompt = prompt.format(prompt.lower().strip())
    
    video = pipe(prompt, negative_prompt=negative_prompt, guidance_scale=7.5, max_sequence_length=512, num_inference_steps=100, generator = torch.Generator(device="cuda:0").manual_seed(42)).frames[0]
    export_to_video(video, "output.mp4", fps=15)
    ```
      
    Use `pipe.enable_sequential_cpu_offload()` to offload the model into CPU for less GPU memory cost (about 9.3G, compared to 27.5G if CPU offload is not enabled), but the inference time will increase significantly.

3. (Optional) Interpolate the video to 30 FPS.

    It is recommended to use [EMA-VFI](https://github.com/MCG-NJU/EMA-VFI) to interpolate the video from 15 FPS to 30 FPS.
  
    For better visual quality, please use imageio to save the video.

4. For faster inference such Context Parallel, PAB, please refer to our [github repo](https://github.com/rhymes-ai/Allegro). 

# License
This repo is released under the Apache 2.0 License.
