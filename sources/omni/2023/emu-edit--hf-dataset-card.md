---
configs:
- config_name: default
  data_files:
  - split: validation
    path: data/validation-*
  - split: test
    path: data/test-*
dataset_info:
  features:
  - name: instruction
    dtype: string
  - name: image
    dtype: image
  - name: task
    dtype: string
  - name: split
    dtype: string
  - name: idx
    dtype: int64
  - name: hash
    dtype: string
  - name: input_caption
    dtype: string
  - name: output_caption
    dtype: string
  splits:
  - name: validation
    num_bytes: 766327032.29
    num_examples: 2022
  - name: test
    num_bytes: 1353530752.0
    num_examples: 3589
  download_size: 1904598290
  dataset_size: 2119857784.29
---

# Dataset Card for the Emu Edit Test Set


## Table of Contents
- [Table of Contents](#table-of-contents)
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
- [Additional Information](#additional-information)
  - [Licensing Information](#licensing-information)
  - [Citation Information](#citation-information)

## Dataset Description

- **Homepage: https://emu-edit.metademolab.com/**
- **Paper: https://emu-edit.metademolab.com/assets/emu_edit.pdf**

### Dataset Summary

To create a benchmark for image editing we first define seven different categories of potential image editing operations: background alteration (background), comprehensive image changes (global), style alteration (style), object removal (remove), object addition (add), localized modifications (local), and color/texture alterations (texture).
Then, we utilize the diverse set of input images from the [MagicBrush benchmark](https://huggingface.co/datasets/osunlp/MagicBrush), and for each editing operation, we task crowd workers to devise relevant, creative, and challenging instructions.
Moreover, to increase the quality of the collected examples, we apply a post-verification stage, in which crowd workers filter examples with irrelevant instructions.
Finally, to support evaluation for methods that require input and output captions (e.g. prompt2prompt and pnp), we additionally collect an input caption and output caption for each example. 
When doing so, we ask annotators to ensure that the captions capture both important elements in the image, and elements that should change based on the instruction.
Additionally, to support proper comparison with Emu Edit with publicly release the model generations on the test set [here](https://huggingface.co/datasets/facebook/emu_edit_test_set_generations).
For more details please see our [paper](https://emu-edit.metademolab.com/assets/emu_edit.pdf) and [project page](https://emu-edit.metademolab.com/).


### Licensing Information

Licensed with CC-BY-NC 4.0 License available [here](https://creativecommons.org/licenses/by-nc/4.0/legalcode?fbclid=IwAR2SYZjLRywwUMblkWg0LyAxHVVTloIFlvC-ju3BthIYtOM2jpQHgbeXOsM).

### Citation Information
```
@inproceedings{Sheynin2023EmuEP,
  title={Emu Edit: Precise Image Editing via Recognition and Generation Tasks},
  author={Shelly Sheynin and Adam Polyak and Uriel Singer and Yuval Kirstain and Amit Zohar and Oron Ashual and Devi Parikh and Yaniv Taigman},
  year={2023},
  url={https://api.semanticscholar.org/CorpusID:265221391}
}
```