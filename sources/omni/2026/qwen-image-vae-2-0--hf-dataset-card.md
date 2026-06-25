---
license: apache-2.0
task_categories:
  - image-to-image
language:
  - en
  - zh
tags:
  - VAE
  - text-rich document
  - text-reconstruction
  - benchmark
size_categories:
  - 1K<n<10K
pretty_name: OmniDoc-TokenBench
---

<div align="center">

<h2>OmniDoc-TokenBench</h2>

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-OmniDoc--TokenBench-181717?logo=github)](https://github.com/alibaba/OmniDoc-TokenBench)
[![arXiv](https://img.shields.io/badge/arXiv-QwenImageVAE2.0-B31B1B?logo=arxiv&logoColor=white)](https://arxiv.org/abs/2605.13565)

</div>

---

## 📄 Overview

### Introduction

We propose **OmniDoc-TokenBench** in [Qwen-Image-VAE-2.0](https://arxiv.org/abs/2605.13565), a curated benchmark specifically designed to evaluate VAE reconstruction on text-rich document images. It contains ~3K samples spanning nine categories (*book*, *slides*, *color textbook*, *exam paper*, *academic paper*, *magazine*, *financial report*, *newspaper*, *note*) in both English and Chinese, alongside an evaluation toolkit supporting PSNR, SSIM, LPIPS, FID, and OCR-based NED metrics.

<div align="center">
  <img src="assets/bench.png" alt="OmniDoc-TokenBench" width="80%" />
</div>

We develop OmniDoc-TokenBench based on [OmniDocBench](https://github.com/opendatalab/OmniDocBench). We crop each sample from a text block and resize it to 256×256, then filter for a character count range ([200, 600] for Chinese, [300, 600] for English) to ensure a reference font size of approximately 16px and 10px, respectively. We deduplicate via n-gram overlap and manually inspect for quality.


### Evaluation Metric

Beyond traditional metrics (PSNR, SSIM, LPIPS, FID), we use **NED** (Normalized Edit Distance) as the primary text-fidelity metric. NED directly measures text preservation by comparing recognized character sequences between original and reconstructed images using Levenshtein distance:

$$
\mathrm{NED} = \frac{1}{N}\sum_{i=1}^{N}\left(1 - \frac{d_{\mathrm{edit}}(s_{\mathrm{gt}}^{(i)}, s_{\mathrm{recon}}^{(i)})}{\max(|s_{\mathrm{gt}}^{(i)}|, |s_{\mathrm{recon}}^{(i)}|)}\right)
$$

NED is sensitive to semantic corruption such as character substitutions, making it a necessary complementary metric when traditional metrics alone are insufficient.

---

## 📊 Performance

We conduct a comprehensive evaluation on OmniDoc-TokenBench (~3K text-rich images, 256×256 resolution). Models are grouped by spatial compression factor and sorted by NED within each group.

<div align="center">
  <img src="assets/results.png" alt="Eval-Results" width="65%" />
</div>

Our Qwen-Image-VAE-2.0 achieves state-of-the-art reconstruction across all compression ratios. The f16c128 variant attains SSIM **0.9706** and PSNR **30.45 dB**, surpassing the best f8 baseline (FLUX.1-dev at 0.9364 / 26.24 dB) despite 2× higher spatial compression. In terms of text fidelity (NED), f16c128 reaches **0.9617**, exceeding all evaluated VAEs. Even under extreme f32 compression, our f32c192 achieves NED **0.8555**, surpassing multiple f16 baselines.

---

## ⚡ Evaluation

For evaluation scripts and usage, see our [GitHub Repository](https://github.com/alibaba/OmniDoc-TokenBench)

---

## 📝 Citation

If you use OmniDoc-TokenBench or this evaluation toolkit in your research, please cite:

```bibtex
@misc{zhang2026qwenimagevae20technicalreport,
      title={Qwen-Image-VAE-2.0 Technical Report}, 
      author={Zekai Zhang and Deqing Li and Kuan Cao and Yujia Wu and Chenfei Wu and Yu Wu and Liang Peng and Hao Meng and Jiahao Li and Jie Zhang and Kaiyuan Gao and Kun Yan and Lihan Jiang and Ningyuan Tang and Shengming Yin and Tianhe Wu and Xiao Xu and Xiaoyue Chen and Yan Shu and Yanran Zhang and Yilei Chen and Yixian Xu and Yuxiang Chen and Zhendong Wang and Zihao Liu and Zikai Zhou and Yiliang Gu and Yi Wang and Xiaoxiao Xu and Lin Qu},
      year={2026},
      eprint={2605.13565},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2605.13565}, 
}
```

---

## Acknowledgements

OmniDoc-TokenBench is a derivative dataset based on [OmniDocBench](https://github.com/opendatalab/OmniDocBench), Thanks for their great work.

## License

This dataset is developed by the Qwen Team at Alibaba Group, and licensed under the [Apache License 2.0](LICENSE).
