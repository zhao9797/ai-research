# NextStep-1.1: Stable Post-Training Delivers Comprehensive Improvements
Source: https://stepfun-ai.github.io/NextStep-1/nextstep_1p1_blog/
NextStep-1.1: Stable Post-Training Delivers Comprehensive Improvements



[StepFun](https://stepfun.ai)

Feb 13th, 2026

# NextStep-1.1: Stable Post-Training Delivers Comprehensive Improvements

Stable post-training and NextStep-GRPO for autoregressive image generation.

Open Source: [Github](https://github.com/stepfun-ai/NextStep-1)|[Hugging Face](https://huggingface.co/collections/stepfun-ai/nextstep-1-689d80238a01322b93b8a3dc)

As shown in Fig. 1, NextStep-1.1 effectively addresses the visualization failure cases observed in NextStep-1 and delivers substantial improvements in overall image quality through extended training schedules and stable post-training.

![Visualization results across different training stages](assets/fig_1.png)


Fig. 1 — Visualization results across different training stages.

## Extended Training Steps

Initialized from the NextStep-1 (256px) checkpoint, we perform continued pre-training for 300K steps at 256 resolution with a learning rate of 1e-4. This is followed by 20K steps at 512 resolution to enhance high-resolution generation capability. Finally, we conduct a 20K-step annealing phase using high-quality curated data, resulting in the NextStep-1.1-Pretrain model.

Tab. 1 — Comparisons of training schedules between NextStep-1 and NextStep-1.1.

| Training Steps | Pre-Training Stage1 256px | Pre-Training Stage2 512px | Pre-Training Annealing | Post-Training SFT | Post-Training DPO / GRPO |
| --- | --- | --- | --- | --- | --- |
| NextStep-1 | 200K | 100K | 20K | 10K | 300 (DPO) |
| NextStep-1.1 | 500K | 20K | 20K | 0K | 1000 (GRPO) |

## Stable Post-training with NextStep-GRPO

Starting from the NextStep-1.1-Pretrain model, we adopt full-parameter fine-tuning using FlowGRPO [1], with a composite reward model consisting of PickScore [3] (Human Preference Alignment) and OCR-based supervision [4] (Text Rendering).

As shown in Fig. 2, the original FlowGRPO configuration exhibits instability when applied to the autoregressive-like NextStep-1.1-Pretrain model. This instability manifests as gradient norm spikes and occasional collapse, reward hacking behaviors in generated images, and a consistent decline in PickScore reward during training.

![Training dynamics comparison between FlowGRPO and NextStep-GRPO](assets/fig_2.png)


Fig. 2 — Training dynamics comparison between FlowGRPO and NextStep-GRPO.

To address these issues, we introduce a stabilized post-training strategy tailored for the autoregressive generation paradigm. As shown in Fig. 3, the resulting **NextStep-GRPO** framework significantly improves optimization stability, mitigates reward hacking, and maintains sustained reward growth throughout training. Empirically, this leads to better alignment, improved text rendering fidelity, and enhanced visual coherence.

![Stabilized Reward Dynamics Under NextStep-GRPO](assets/fig_3.png)


Fig. 3 — Stabilized Reward Dynamics Under NextStep-GRPO.

## On-Policy Training: Stabilizing GRPO for Autoregressive NextStep-1.1

While FlowGRPO has demonstrated strong empirical performance in diffusion models [5], directly applying it to the autoregressive NextStep-1 architecture introduces substantial instability. The root cause lies in several off-policy behaviors and numerical mismatches that become amplified under sequential generation. To resolve these challenges, we move from FlowGRPO to NextStep-GRPO, a strictly on-policy formulation that shifts the focus from aggressive convergence to stable optimization, controlled reward learning, and long-term performance scalability.

* **1. Re-computation for Training-Inference Consistency:** Autoregressive models under BF16 precision suffer from accumulated numerical errors: token-by-token sampling diverges from the parallel processing used during training. To bridge this gap, we implement a two-stage sampling mechanism. We first generate the image token-by-token, then feed the complete text-image sequence back into the LLM backbone to recompute log-probabilities in parallel. This ensures that the log-probability computation aligns strictly with the parallel training paradigm, eliminating numerical discrepancies caused by sequential sampling.
* **2. Disabling CFG for Stability and Exploration:** Classifier-Free Guidance (CFG) acts as an amplifier for BF16 numerical errors by scaling the delta between conditional and unconditional logits. Furthermore, CFG reduces output variance, thereby shrinking the exploration space essential for GRPO. Consequently, we disable CFG during training. As shown in Fig. 2, while this lowers the initial performance baseline, it significantly stabilizes the optimization trajectory and ultimately yields higher final rewards.
* **3. Strictly On-Policy Optimization:** The original FlowGRPO enables multiple weight updates per epoch across different timesteps, causing the model weights to drift from the sampling snapshot—a technically off-policy behavior. To enforce strict on-policy consistency, we restrict optimization to a single timestep per iteration, adhering to a "one sampling step, one weight update" protocol.
* **4. Numerical Stability via FlowCPS:** FlowGRPO involves division by small floating-point values in its log-probability computation, making it susceptible to gradient explosion when processing outlier samples. To mitigate this, we adopt the FlowCPS [2] formulation for computing log-probabilities, which offers superior numerical stability.
* **5. Online Rejection Sampling:** To maximize sample efficiency, NextStep-GRPO implements online rejection sampling. We discard prompt groups where the reward distribution exhibits either a high mean (indicating trivial samples) or a low standard deviation (indicating collapsed exploration), as these fail to provide the necessary contrastive signals for effective reinforcement learning.

## Effectiveness of NextStep-GRPO in Diffusion Models

As shown in Tab. 2, we evaluate NextStep-GRPO in a standard diffusion setting using the same base model (SD3.5-Medium [5]) and identical reward models as FlowGRPO. The results demonstrate that the stabilized NextStep-GRPO achieves performance comparable to FlowGRPO, while maintaining its improved training stability properties. Notably, NextStep-GRPO slightly outperforms FlowGRPO on both PickScore and OCR metrics, indicating that the proposed stabilization strategies do not compromise performance when applied to diffusion architectures.

Tab. 2 — Comparison between FlowGRPO and NextStep-GRPO in a diffusion model setting. PickScore measures the alignment of generated images with human preferences, while OCR evaluates text rendering accuracy.

| Method | PickScore [3] | OCR [4] |
| --- | --- | --- |
| FlowGRPO | 23.31 | 0.92 |
| **NextStep-GRPO** | **23.66** | **0.96** |

## Citation (BibTeX)

If you find NextStep useful for your research and applications, please consider starring this repository and citing:

Copy

```
@article{nextstepteam2025nextstep1,
  title={NextStep-1: Toward Autoregressive Image Generation with Continuous Tokens at Scale},
  author={NextStep Team and Chunrui Han and Guopeng Li and Jingwei Wu and Quan Sun and Yan Cai and Yuang Peng and Zheng Ge and Deyu Zhou and Haomiao Tang and Hongyu Zhou and Kenkun Liu and Ailin Huang and Bin Wang and Changxin Miao and Deshan Sun and En Yu and Fukun Yin and Gang Yu and Hao Nie and Haoran Lv and Hanpeng Hu and Jia Wang and Jian Zhou and Jianjian Sun and Kaijun Tan and Kang An and Kangheng Lin and Liang Zhao and Mei Chen and Peng Xing and Rui Wang and Shiyu Liu and Shutao Xia and Tianhao You and Wei Ji and Xianfang Zeng and Xin Han and Xuelin Zhang and Yana Wei and Yanming Xu and Yimin Jiang and Yingming Wang and Yu Zhou and Yucheng Han and Ziyang Meng and Binxing Jiao and Daxin Jiang and Xiangyu Zhang and Yibo Zhu},
  journal={arXiv preprint arXiv:2508.10711},
  year={2025}
}
```

## References

* [1] Liu, Jie, et al. "Flow-GRPO: Training flow matching models via online rl." arXiv preprint arXiv:2505.05470 (2025).
* [2] Wang, Feng, and Zihao Yu. "Coefficients-Preserving Sampling for Reinforcement Learning with Flow Matching." arXiv preprint arXiv:2509.05952 (2025).
* [3] Kirstain, Yuval, et al. "Pick-a-pic: An open dataset of user preferences for text-to-image generation." Advances in neural information processing systems 36 (2023): 36652-36663.
* [4] Cui, Cheng, et al. "Paddleocr 3.0 technical report." arXiv preprint arXiv:2507.05595 (2025).
* [5] <https://stability.ai/news/introducing-stable-diffusion-3-5>

From StepFun-AI NextStep Team. Topic: NextStep-1.1 and stable post-training.
