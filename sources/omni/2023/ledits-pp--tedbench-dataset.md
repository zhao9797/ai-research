---
license: apache-2.0
task_categories:
- image-to-image
- text-to-image
pretty_name: TEdBench++
size_categories:
- n<1K
---

# TEdBench++

This dataset contains the TEdBench++ an image-to-image benchmark for text-based generative models. It contains original images (originals) and edited images (LEdits++) for benchmarking. ``tedbench++.csv`` contains the text-based edit instructions for the respective original image and parameters to reproduce the edited images with LEdits++.

consider citing our work

```bibtex
@inproceedings{brack2024ledits,
  year = { 2024 },
  booktitle = { Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) },
  author = { Manuel Brack and Felix Friedrich and Katharina Kornmeier and Linoy Tsaban and Patrick Schramowski and Kristian Kersting and Apolinaros Passos },
  title = { LEDITS++: Limitless Image Editing using Text-to-Image Models }
}
```