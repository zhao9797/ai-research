---
license: cc-by-nc-sa-4.0
---

# AudioLDM 2

AudioLDM 2 is a latent text-to-audio diffusion model capable of generating realistic audio samples given any text input. 
It is available in the 🧨 Diffusers library from v0.21.0 onwards.

# Model Details

AudioLDM 2 was proposed in the paper [AudioLDM 2: Learning Holistic Audio Generation with Self-supervised Pretraining](https://arxiv.org/abs/2308.05734) by Haohe Liu et al.

AudioLDM takes a text prompt as input and predicts the corresponding audio. It can generate text-conditional sound effects, 
human speech and music.

# Checkpoint Details

This is the original, **base** version of the AudioLDM 2 model, also referred to as **audioldm2-full**. 

There are three official AudioLDM 2 checkpoints. Two of these checkpoints are applicable to the general task of text-to-audio 
generation. The third checkpoint is trained exclusively on text-to-music generation. All checkpoints share the same 
model size for the text encoders and VAE. They differ in the size and depth of the UNet. See table below for details on 
the three official checkpoints:

| Checkpoint                                                      | Task          | UNet Model Size | Total Model Size | Training Data / h |
|-----------------------------------------------------------------|---------------|-----------------|------------------|-------------------|
| [audioldm2](https://huggingface.co/cvssp/audioldm2)             | Text-to-audio | 350M            | 1.1B             | 1150k             |
| [audioldm2-large](https://huggingface.co/cvssp/audioldm2-large) | Text-to-audio | 750M            | 1.5B             | 1150k             |
| [audioldm2-music](https://huggingface.co/cvssp/audioldm2-music) | Text-to-music | 350M            | 1.1B             | 665k              |

## Model Sources

- [**Original Repository**](https://github.com/haoheliu/audioldm2)
- [**🧨 Diffusers Pipeline**](https://huggingface.co/docs/diffusers/api/pipelines/audioldm2)
- [**Paper**](https://arxiv.org/abs/2308.05734)
- [**Demo**](https://huggingface.co/spaces/haoheliu/audioldm2-text2audio-text2music)

# Usage

First, install the required packages:

```
pip install --upgrade diffusers transformers accelerate
```

## Text-to-Audio

For text-to-audio generation, the [AudioLDM2Pipeline](https://huggingface.co/docs/diffusers/api/pipelines/audioldm2) can be 
used to load pre-trained weights and generate text-conditional audio outputs:

```python
from diffusers import AudioLDM2Pipeline
import torch

repo_id = "cvssp/audioldm2"
pipe = AudioLDM2Pipeline.from_pretrained(repo_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda")

prompt = "The sound of a hammer hitting a wooden surface"
audio = pipe(prompt, num_inference_steps=200, audio_length_in_s=10.0).audios[0]
```

The resulting audio output can be saved as a .wav file:
```python
import scipy

scipy.io.wavfile.write("techno.wav", rate=16000, data=audio)
```

Or displayed in a Jupyter Notebook / Google Colab:
```python
from IPython.display import Audio

Audio(audio, rate=16000)
```

## Tips

Prompts:
* Descriptive prompt inputs work best: you can use adjectives to describe the sound (e.g. "high quality" or "clear") and make the prompt context specific (e.g., "water stream in a forest" instead of "stream").
* It's best to use general terms like 'cat' or 'dog' instead of specific names or abstract objects that the model may not be familiar with.

Inference:
* The _quality_ of the predicted audio sample can be controlled by the `num_inference_steps` argument: higher steps give higher quality audio at the expense of slower inference.
* The _length_ of the predicted audio sample can be controlled by varying the `audio_length_in_s` argument.

When evaluating generated waveforms:

* The quality of the generated waveforms can vary significantly based on the seed. Try generating with different seeds until you find a satisfactory generation
* Multiple waveforms can be generated in one go: set `num_waveforms_per_prompt` to a value greater than 1. Automatic scoring will be performed between the generated waveforms and prompt text, and the audios ranked from best to worst accordingly.

The following example demonstrates how to construct a good audio generation using the aforementioned tips:

```python
import scipy
import torch
from diffusers import AudioLDM2Pipeline

# load the pipeline
repo_id = "cvssp/audioldm2"
pipe = AudioLDM2Pipeline.from_pretrained(repo_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda")

# define the prompts
prompt = "The sound of a hammer hitting a wooden surface"
negative_prompt = "Low quality."

# set the seed
generator = torch.Generator("cuda").manual_seed(0)

# run the generation
audio = pipe(
    prompt,
    negative_prompt=negative_prompt,
    num_inference_steps=200,
    audio_length_in_s=10.0,
    num_waveforms_per_prompt=3,
).audios

# save the best audio sample (index 0) as a .wav file
scipy.io.wavfile.write("techno.wav", rate=16000, data=audio[0])
```

# Citation

**BibTeX:**
```
@article{liu2023audioldm2,
  title={"AudioLDM 2: Learning Holistic Audio Generation with Self-supervised Pretraining"},
  author={Haohe Liu and Qiao Tian and Yi Yuan and Xubo Liu and Xinhao Mei and Qiuqiang Kong and Yuping Wang and Wenwu Wang and Yuxuan Wang and Mark D. Plumbley},
  journal={arXiv preprint arXiv:2308.05734},
  year={2023}
}
```
