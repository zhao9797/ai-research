# Controlling Text-to-Image Diffusion by Orthogonal Finetuning
Source: https://arxiv.org/html/2306.07280v3
Controlling Text-to-Image Diffusion by Orthogonal Finetuning



[![logo](https://services.dev.arxiv.org/html/static/arxiv-logomark-small-white.svg)
Back to arXiv](https://arxiv.org/)

[![logo](https://services.dev.arxiv.org/html/static/arxiv-logo-one-color-white.svg)
Back to arXiv](https://arxiv.org/)

This is **experimental HTML** to improve accessibility. We invite you to report rendering errors. Use Alt+Y to toggle on accessible reporting links and Alt+Shift+Y to toggle off. Learn more [about this project](https://info.arxiv.org/about/accessible_HTML.html) and [help improve conversions](https://info.arxiv.org/help/submit_latex_best_practices.html).

[Why HTML?](https://info.arxiv.org/about/accessible_HTML.html)
[Report Issue](#myForm)
[Back to Abstract](https://arxiv.org/abs/2306.07280v3)
[Download PDF](https://arxiv.org/pdf/2306.07280v3)

## Table of Contents

1. Controlling Text-to-Image Diffusion by Orthogonal Finetuning
   1. [1 Introduction](https://arxiv.org/html/2306.07280v3#S1 "1 Introduction ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")
   2. [2 Related Work](https://arxiv.org/html/2306.07280v3#S2 "2 Related Work ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")
   3. [3 Orthogonal Finetuning](https://arxiv.org/html/2306.07280v3#S3 "3 Orthogonal Finetuning ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")
      1. [3.1 Why Does Orthogonal Transformation Make Sense?](https://arxiv.org/html/2306.07280v3#S3.SS1 "3.1 Why Does Orthogonal Transformation Make Sense? ‣ 3 Orthogonal Finetuning ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")
      2. [3.2 General Framework](https://arxiv.org/html/2306.07280v3#S3.SS2 "3.2 General Framework ‣ 3 Orthogonal Finetuning ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")
      3. [3.3 Efficient Orthogonal Parameterization](https://arxiv.org/html/2306.07280v3#S3.SS3 "3.3 Efficient Orthogonal Parameterization ‣ 3 Orthogonal Finetuning ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")
      4. [3.4 Constrained Orthogonal Finetuning](https://arxiv.org/html/2306.07280v3#S3.SS4 "3.4 Constrained Orthogonal Finetuning ‣ 3 Orthogonal Finetuning ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")
      5. [3.5 Re-scaled Orthogonal Finetuning](https://arxiv.org/html/2306.07280v3#S3.SS5 "3.5 Re-scaled Orthogonal Finetuning ‣ 3 Orthogonal Finetuning ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")
   4. [4 Intriguing Insights and Discussions](https://arxiv.org/html/2306.07280v3#S4 "4 Intriguing Insights and Discussions ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")
   5. [5 Experiments and Results](https://arxiv.org/html/2306.07280v3#S5 "5 Experiments and Results ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")
      1. [5.1 Subject-driven Generation](https://arxiv.org/html/2306.07280v3#S5.SS1 "5.1 Subject-driven Generation ‣ 5 Experiments and Results ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")
      2. [5.2 Controllable Generation](https://arxiv.org/html/2306.07280v3#S5.SS2 "5.2 Controllable Generation ‣ 5 Experiments and Results ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")
   6. [6 Concluding Remarks and Open Problems](https://arxiv.org/html/2306.07280v3#S6 "6 Concluding Remarks and Open Problems ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")
   7. [Appendix](https://arxiv.org/html/2306.07280v3#Pt1 "Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning") 
      1. [A Experimental Details](https://arxiv.org/html/2306.07280v3#A1 "Appendix A Experimental Details ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")
         1. [Data and Model.](https://arxiv.org/html/2306.07280v3#A1.SS0.SSS0.Px1 "Data and Model. ‣ Appendix A Experimental Details ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")
         2. [Subject-driven generation.](https://arxiv.org/html/2306.07280v3#A1.SS0.SSS0.Px2 "Subject-driven generation. ‣ Appendix A Experimental Details ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")
         3. [Controllable generation.](https://arxiv.org/html/2306.07280v3#A1.SS0.SSS0.Px3 "Controllable generation. ‣ Appendix A Experimental Details ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")
         4. [Evaluation.](https://arxiv.org/html/2306.07280v3#A1.SS0.SSS0.Px4 "Evaluation. ‣ Appendix A Experimental Details ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")
      2. [B Effect of Different Number of Diagonal Blocks](https://arxiv.org/html/2306.07280v3#A2 "Appendix B Effect of Different Number of Diagonal Blocks ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")
      3. [C Experiments on Re-scaled OFT](https://arxiv.org/html/2306.07280v3#A3 "Appendix C Experiments on Re-scaled OFT ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")
      4. [D Applying OFT to Convolution Layers](https://arxiv.org/html/2306.07280v3#A4 "Appendix D Applying OFT to Convolution Layers ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")
      5. [E Comparison between COFT and OFT](https://arxiv.org/html/2306.07280v3#A5 "Appendix E Comparison between COFT and OFT ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")
      6. [F More Qualitative Results](https://arxiv.org/html/2306.07280v3#A6 "Appendix F More Qualitative Results ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")
         1. [F.1 Subject-driven Generation](https://arxiv.org/html/2306.07280v3#A6.SS1 "F.1 Subject-driven Generation ‣ Appendix F More Qualitative Results ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")
         2. [F.2 Controllable Generation](https://arxiv.org/html/2306.07280v3#A6.SS2 "F.2 Controllable Generation ‣ Appendix F More Qualitative Results ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")
            1. [F.2.1 Segmentation to Image](https://arxiv.org/html/2306.07280v3#A6.SS2.SSS1 "F.2.1 Segmentation to Image ‣ F.2 Controllable Generation ‣ Appendix F More Qualitative Results ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")
            2. [F.2.2 Canny Edge to Image](https://arxiv.org/html/2306.07280v3#A6.SS2.SSS2 "F.2.2 Canny Edge to Image ‣ F.2 Controllable Generation ‣ Appendix F More Qualitative Results ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")
            3. [F.2.3 Landmark to Face](https://arxiv.org/html/2306.07280v3#A6.SS2.SSS3 "F.2.3 Landmark to Face ‣ F.2 Controllable Generation ‣ Appendix F More Qualitative Results ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")
      7. [G More Controllable Generation Tasks](https://arxiv.org/html/2306.07280v3#A7 "Appendix G More Controllable Generation Tasks ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")
         1. [G.1 Dense Pose to Human Body](https://arxiv.org/html/2306.07280v3#A7.SS1 "G.1 Dense Pose to Human Body ‣ Appendix G More Controllable Generation Tasks ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")
         2. [G.2 Sketch to Image](https://arxiv.org/html/2306.07280v3#A7.SS2 "G.2 Sketch to Image ‣ Appendix G More Controllable Generation Tasks ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")
         3. [G.3 Depth to Image](https://arxiv.org/html/2306.07280v3#A7.SS3 "G.3 Depth to Image ‣ Appendix G More Controllable Generation Tasks ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")
      8. [H Human Evaluation](https://arxiv.org/html/2306.07280v3#A8 "Appendix H Human Evaluation ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")
      9. [I Style Transfer by Adapting Stable Diffusion with Orthogonal Finetuning](https://arxiv.org/html/2306.07280v3#A9 "Appendix I Style Transfer by Adapting Stable Diffusion with Orthogonal Finetuning ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")
      10. [J Failure Cases](https://arxiv.org/html/2306.07280v3#A10 "Appendix J Failure Cases ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")
          1. [J.1 Failure Cases in Subject-driven Generation](https://arxiv.org/html/2306.07280v3#A10.SS1 "J.1 Failure Cases in Subject-driven Generation ‣ Appendix J Failure Cases ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")
          2. [J.2 Failure Cases in Controllable Generation](https://arxiv.org/html/2306.07280v3#A10.SS2 "J.2 Failure Cases in Controllable Generation ‣ Appendix J Failure Cases ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")

Report issue for preceding element

HTML conversions [sometimes display errors](https://info.dev.arxiv.org/about/accessibility_html_error_messages.html) due to content that did not convert correctly from the source. This paper uses the following packages that are not yet supported by the HTML conversion tool. Feedback on these issues are not necessary; they are known and are being worked on.

Report issue for preceding element

* failed: stackengine
* failed: tocloft
* failed: minitoc

Authors: achieve the best HTML results from your LaTeX submissions by following these [best practices](https://info.arxiv.org/help/submit_latex_best_practices.html).

Report issue for preceding element

License: arXiv.org perpetual non-exclusive license

arXiv:2306.07280v3 [cs.CV] 14 Mar 2024

\doparttoc\faketableofcontents

# Controlling Text-to-Image Diffusion by Orthogonal Finetuning

Report issue for preceding element

Zeju Qiu1,\*    Weiyang Liu1,2,\*,†    Haiwen Feng1    Yuxuan Xue3    Yao Feng1    Zhen Liu1,4
  
Dan Zhang3,5    Adrian Weller2,6    Bernhard Schölkopf1
  
1MPI for Intelligent Systems - Tübingen    2University of Cambridge    3University of Tübingen
  
4Mila, Université de Montréal    5Bosch Center for Artificial Intelligence    6The Alan Turing Institute
  
\*Equal contribution     †Project lead     [oft.wyliu.com](https://oft.wyliu.com)

Report issue for preceding element

###### Abstract

Report issue for preceding element

Large text-to-image diffusion models have impressive capabilities in generating photorealistic images from text prompts. How to effectively guide or control these powerful models to perform different downstream tasks becomes an important open problem. To tackle this challenge, we introduce a principled finetuning method – Orthogonal Finetuning (OFT), for adapting text-to-image diffusion models to downstream tasks. Unlike existing methods, OFT can provably preserve hyperspherical energy which characterizes the pairwise neuron relationship on the unit hypersphere. We find that this property is crucial for preserving the semantic generation ability of text-to-image diffusion models. To improve finetuning stability, we further propose Constrained Orthogonal Finetuning (COFT) which imposes an additional radius constraint to the hypersphere. Specifically, we consider two important finetuning text-to-image tasks: subject-driven generation where the goal is to generate subject-specific images given a few images of a subject and a text prompt, and controllable generation where the goal is to enable the model to take in additional control signals. We empirically show that our OFT framework outperforms existing methods in generation quality and convergence speed.

Report issue for preceding element

††This work was finished when ZQ was a research intern hosted by WL at MPI for Intelligent Systems.

### 1 Introduction

Report issue for preceding element

Recent text-to-image diffusion models [[53](https://arxiv.org/html/2306.07280v3#bib.bib53), [45](https://arxiv.org/html/2306.07280v3#bib.bib45), [50](https://arxiv.org/html/2306.07280v3#bib.bib50)] achieve impressive performance in text-guided control for high-fidelity image generation. Despite strong results, text guidance can still be ambiguous and insufficient to provide fine-grained and accurate control to the generated images. To address this shortcoming, we target two types of text-to-image generation tasks in this paper:

Report issue for preceding element

* •

  Subject-driven generation [[51](https://arxiv.org/html/2306.07280v3#bib.bib51)]: Given just a few images of a subject, the task is to generate images of the same subject in a different context using the guidance of a text prompt.

  Report issue for preceding element
* •

  Controllable generation [[68](https://arxiv.org/html/2306.07280v3#bib.bib68), [38](https://arxiv.org/html/2306.07280v3#bib.bib38)]: Given an additional control signal (*e.g.*, canny edges, segmentation maps), the task is to generate images following such a control signal and a text prompt.

  Report issue for preceding element

Both tasks essentially boil down to how to effectively finetune text-to-image diffusion models without losing the pretraining generative performance. We summarize the desiderata for an effective finetuning method as: (1) *training efficiency*: having fewer trainable parameters and number of training epochs, and (2) *generalizability preservation*: preserving the high-fidelity and diverse generative performance. To this end, finetuning is typically done either by updating the neuron weights by a small learning rate (*e.g.*, [[51](https://arxiv.org/html/2306.07280v3#bib.bib51)]) or by adding a small component with re-parameterized neuron weights (*e.g.*, [[22](https://arxiv.org/html/2306.07280v3#bib.bib22), [68](https://arxiv.org/html/2306.07280v3#bib.bib68)]). Despite simplicity, neither finetuning strategy is able to guarantee the preservation of pretraining generative performance. There is also a lack of principled understanding towards designing a good finetuning strategy and finding suitable hyperparameters such as the number of training epochs. A key difficulty is the lack of a measure for quantifying the preservation of pretrained generative ability. Existing finetuning methods implicitly assume that a smaller Euclidean distance between the finetuned model and the pretrained model indicates better preservation of the pretrained ability. Due to the same reason, finetuning methods typically work with a very small learning rate. While this assumption may occasionally hold, we argue that the Euclidean difference to the pretrained model alone is unable to fully capture the degree of semantic preservation, and therefore a more structural measure to characterize the difference between the finetuned model and the pretrained model can greatly benefit the preservation of pretraining performance as well as finetuning stability.

Report issue for preceding element

Inspired by the empirical observation that hyperspherical similarity encodes semantic information well [[36](https://arxiv.org/html/2306.07280v3#bib.bib36), [35](https://arxiv.org/html/2306.07280v3#bib.bib35), [7](https://arxiv.org/html/2306.07280v3#bib.bib7)], we use hyperspherical energy [[32](https://arxiv.org/html/2306.07280v3#bib.bib32)] to characterize the pairwise relational structure among neurons. Hyperspherical energy is defined as the sum of hyperspherical similarity (*e.g.*, cosine similarity) between all pairwise neurons in the same layer, capturing the level of neuron uniformity on the unit hypersphere [[34](https://arxiv.org/html/2306.07280v3#bib.bib34)]. We hypothesize that a good finetuned model should have a minimal difference in hyperspherical energy compared to the pretrained model. A naive way is to add a regularizer such that the hyperspherical energy remains the same during the finetuning stage, but there is no guarantee that the hyperspherical energy difference can be well minimized. Therefore, we take advantage of an invariance property of hyperspherical energy – the pairwise hyperspherical similarity is provably preserved if we apply the same orthogonal transformation for all neurons. Motivated by such an invariance, we propose Orthogonal Finetuning (OFT) which adapts large text-to-image diffusion models to a downstream task without changing its hyperspherical energy. The central idea is to learn a layer-shared orthogonal transformation for neurons such that their pairwise angles are preserved. OFT can also be viewed as adjusting the canonical coordinate system for the neurons in the same layer. By jointly taking into consideration that smaller Euclidean distance between the finetuned model and the pretrained model implies better preservation of pretraining performance, we further propose an OFT variant – Constrained Orthogonal Finetuning (COFT) which constrains the finetuned model within the hypersphere of a fixed radius centered on the pretrained neurons.

Report issue for preceding element

![Refer to caption](x1.png)


Figure 1: (a) Subject-driven generation: OFT preserves the hyperspherical energy and yields more stable finetuning performance across different number of iterations, while both DreamBooth [[51](https://arxiv.org/html/2306.07280v3#bib.bib51)] and LoRA [[22](https://arxiv.org/html/2306.07280v3#bib.bib22)] do not. OFT can preserve hyperspherical energy and perform stable finetuning, while both LoRA and DreamBooth are unable. (b) Controllable generation: OFT is more sample-efficient in training and converges well with only 5% of the original dataset, while both ControlNet [[68](https://arxiv.org/html/2306.07280v3#bib.bib68)] and LoRA [[22](https://arxiv.org/html/2306.07280v3#bib.bib22)] cannot converge until 50% of the data is present. The hyperspherical energy comparison between LoRA and OFT is fair, since they finetune the same layers. ControlNet uses a different layer finetuning strategy, so its hyperspherical energy is not comparable. The detailed settings are given in the experiment section and Appendix [A](https://arxiv.org/html/2306.07280v3#A1 "Appendix A Experimental Details ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning").

Report issue for preceding element

The intuition for why orthogonal transformation works for finetuning neurons partially comes from 2D Fourier transform, with which an image can be decomposed as magnitude and phase spectrum. The phase spectrum, which is angular information between input and basis, preserves the major part of semantics. For example, the phase spectrum of an image, along with a random magnitude spectrum, can still reconstruct the original image without losing its semantics. This phenomenon suggests that changing the neuron directions is the key to semantically modifying the generated image (which is the goal of both subject-driven and controllable generation). However, changing neuron directions with a large degree of freedom will inevitably destroy the pretraining generative performance. To constrain the degree of freedom, we propose to preserve the angle between any pair of neurons, largely based on the hypothesis that the angles between neurons are crucial for representing the knowledge of neural networks. With this intuition, it is natural to learn layer-shared orthogonal transformation for neurons in each layer such that the hyperspherical energy stays unchanged.

Report issue for preceding element

We also draw inspiration from orthogonal over-parameterized training [[33](https://arxiv.org/html/2306.07280v3#bib.bib33)] which trains classification neural networks from scratch by orthogonally transforming a randomly initialized neural network. This is because a randomly initialized neural network yields a provably small hyperspherical energy in expectation and the goal of [[33](https://arxiv.org/html/2306.07280v3#bib.bib33)] is to keep hyperspherical energy small during training (small energy leads to better generalization in classification [[32](https://arxiv.org/html/2306.07280v3#bib.bib32), [30](https://arxiv.org/html/2306.07280v3#bib.bib30)]). [[33](https://arxiv.org/html/2306.07280v3#bib.bib33)] shows that orthogonal transformation is sufficiently flexible to train generalizable neural networks for classification problems. In contrast, we focus on finetuning text-to-image diffusion models for better controllability and stronger downstream generative performance. We emphasize the difference between OFT and [[33](https://arxiv.org/html/2306.07280v3#bib.bib33)] in two aspects. First, while [[33](https://arxiv.org/html/2306.07280v3#bib.bib33)] is designed to minimize the hyperspherical energy, OFT aims to preserve the same hyperspherical energy as the pretrained model so that the intrinsic pretrained structure will not be destroyed by finetuning. In the case of finetuning diffusion models, minimizing hyperspherical energy could destroy the original semantic structures. Second, OFT seeks to minimize the deviation from the pretrained model, which leads to the constrained variant. In contrast, [[33](https://arxiv.org/html/2306.07280v3#bib.bib33)] imposes no such constraints. The key to finetuning is to find a good trade-off between flexibility and stability, and we argue that our OFT framework effectively achieves this goal. Our contributions are listed below:

Report issue for preceding element

* •

  We propose a novel finetuning method – Orthogonal Finetuning for guiding text-to-image diffusion models towards better controllability. To further improve stability, we propose a constrained variant which limits the angular deviation from the pretrained model.

  Report issue for preceding element
* •

  Compared to existing finetuning methods, OFT performs model finetuning while provably preserving the hyperspherical energy, which we empirically find to be an important measure of the generative semantic preservation of the pretrained model.

  Report issue for preceding element
* •

  We apply OFT to two tasks: subject-driven generation and controllable generation. We conduct a comprehensive empirical study and demonstrate significant improvement over prior work in terms of generation quality, convergence speed and finetuning stability. Moreover, OFT achieves better sample efficiency, as it converges well with a much smaller number of training images and epochs.

  Report issue for preceding element
* •

  For controllable generation, we introduce a new control consistency metric to evaluate the controllability. This core idea is to estimate the control signal from the generated image and then compare it with the origin control signal. The metric further validates the strong controllability of OFT.

  Report issue for preceding element

### 2 Related Work

Report issue for preceding element

Text-to-image diffusion models. Tremendous progress [[53](https://arxiv.org/html/2306.07280v3#bib.bib53), [45](https://arxiv.org/html/2306.07280v3#bib.bib45), [50](https://arxiv.org/html/2306.07280v3#bib.bib50), [16](https://arxiv.org/html/2306.07280v3#bib.bib16), [39](https://arxiv.org/html/2306.07280v3#bib.bib39)] has been made in text-to-image generation, largely thanks to the rapid development in diffusion-based generative models [[20](https://arxiv.org/html/2306.07280v3#bib.bib20), [56](https://arxiv.org/html/2306.07280v3#bib.bib56), [55](https://arxiv.org/html/2306.07280v3#bib.bib55), [12](https://arxiv.org/html/2306.07280v3#bib.bib12)] and vision-language representation learning [[57](https://arxiv.org/html/2306.07280v3#bib.bib57), [37](https://arxiv.org/html/2306.07280v3#bib.bib37), [44](https://arxiv.org/html/2306.07280v3#bib.bib44), [61](https://arxiv.org/html/2306.07280v3#bib.bib61), [29](https://arxiv.org/html/2306.07280v3#bib.bib29), [28](https://arxiv.org/html/2306.07280v3#bib.bib28), [1](https://arxiv.org/html/2306.07280v3#bib.bib1), [54](https://arxiv.org/html/2306.07280v3#bib.bib54)]. GLIDE [[39](https://arxiv.org/html/2306.07280v3#bib.bib39)] and Imagen [[53](https://arxiv.org/html/2306.07280v3#bib.bib53)] train diffusion models in the pixel space. GLIDE trains the text encoder jointly with a diffusion prior using paired text-image data, while Imagen uses a frozen pretrained text encoder. Stable Diffusion [[50](https://arxiv.org/html/2306.07280v3#bib.bib50)] and DALL-E2 [[45](https://arxiv.org/html/2306.07280v3#bib.bib45)] train diffusion models in the latent space. Stable Diffusion uses VQ-GAN [[14](https://arxiv.org/html/2306.07280v3#bib.bib14)] to learn a visual codebook as its latent space, while DALL-E2 adopts CLIP [[44](https://arxiv.org/html/2306.07280v3#bib.bib44)] to construct a joint latent embedding space for representing images and text. Other than diffusion models, generative adversarial networks [[48](https://arxiv.org/html/2306.07280v3#bib.bib48), [67](https://arxiv.org/html/2306.07280v3#bib.bib67), [65](https://arxiv.org/html/2306.07280v3#bib.bib65), [27](https://arxiv.org/html/2306.07280v3#bib.bib27)] and autoregressive models [[46](https://arxiv.org/html/2306.07280v3#bib.bib46), [13](https://arxiv.org/html/2306.07280v3#bib.bib13), [62](https://arxiv.org/html/2306.07280v3#bib.bib62), [66](https://arxiv.org/html/2306.07280v3#bib.bib66)] have also been studied in text-to-image generation. OFT is inherently a model-agnostic finetuning approach and can be applied to any text-to-image diffusion model.

Report issue for preceding element

Subject-driven generation. To prevent subject modification, [[2](https://arxiv.org/html/2306.07280v3#bib.bib2), [39](https://arxiv.org/html/2306.07280v3#bib.bib39)] consider a given mask from users as an additional condition. Inversion methods [[8](https://arxiv.org/html/2306.07280v3#bib.bib8), [12](https://arxiv.org/html/2306.07280v3#bib.bib12), [45](https://arxiv.org/html/2306.07280v3#bib.bib45), [15](https://arxiv.org/html/2306.07280v3#bib.bib15)] can be applied to modify the context without changing the subject. [[18](https://arxiv.org/html/2306.07280v3#bib.bib18)] can perform local and global editing without input masks. The methods above are unable to well preserve identity-related details of the subject. In Pivotal Tuning [[49](https://arxiv.org/html/2306.07280v3#bib.bib49)], a generator is finetuned around an initial inverted latent code with an additional regularization to preserve the identity. Similarly, [[41](https://arxiv.org/html/2306.07280v3#bib.bib41)] learns a personalized generative face prior from a collection of a person’s face images. [[6](https://arxiv.org/html/2306.07280v3#bib.bib6)] can generate difference variations of an instance, but it may lose the instance-specific details. With a customized token and a few subject images, DreamBooth [[51](https://arxiv.org/html/2306.07280v3#bib.bib51)] finetunes the text-to-image diffusion model using a reconstruction loss and a class-specific prior preservation loss. OFT adopts the DreamBooth framework, but instead of performing naive finetuning with a small learning rate, OFT finetunes the model with orthogonal transformations.

Report issue for preceding element

Controllable generation. The task of image-to-image translation can be viewed as a form of controllable generation, and previous methods mostly adopt conditional generative adversarial networks [[23](https://arxiv.org/html/2306.07280v3#bib.bib23), [71](https://arxiv.org/html/2306.07280v3#bib.bib71), [60](https://arxiv.org/html/2306.07280v3#bib.bib60), [42](https://arxiv.org/html/2306.07280v3#bib.bib42), [9](https://arxiv.org/html/2306.07280v3#bib.bib9)]. Diffusion models are also used for image-to-image translation [[52](https://arxiv.org/html/2306.07280v3#bib.bib52), [58](https://arxiv.org/html/2306.07280v3#bib.bib58), [59](https://arxiv.org/html/2306.07280v3#bib.bib59)]. More recently, ControlNet [[68](https://arxiv.org/html/2306.07280v3#bib.bib68)] proposes to control a pretrained diffusion model by finetuning and adapting it to additional control signals and achieves impressive controllable generation performance. Another concurrent and similar work, T2I-Adapter [[38](https://arxiv.org/html/2306.07280v3#bib.bib38)], also finetunes a pretrained diffusion model in order to gain stronger controllability for the generated images. Following the same task setting in [[68](https://arxiv.org/html/2306.07280v3#bib.bib68), [38](https://arxiv.org/html/2306.07280v3#bib.bib38)], we apply OFT to finetune pretrained diffusion models, yielding consistently better controllability with fewer training data and less finetuning parameters. More significantly, OFT does not introduce any additional computational overhead during test-time inference.

Report issue for preceding element

Model finetuning. Finetuning large pretrained models on downstream tasks has been increasingly popular nowadays [[11](https://arxiv.org/html/2306.07280v3#bib.bib11), [3](https://arxiv.org/html/2306.07280v3#bib.bib3), [17](https://arxiv.org/html/2306.07280v3#bib.bib17)]. As a form of finetuning, adaptation methods (*e.g.*, [[22](https://arxiv.org/html/2306.07280v3#bib.bib22), [21](https://arxiv.org/html/2306.07280v3#bib.bib21), [43](https://arxiv.org/html/2306.07280v3#bib.bib43)]) are heavily studied in natural language processing. LoRA [[22](https://arxiv.org/html/2306.07280v3#bib.bib22)] is the most relevant work to OFT, and it assumes a low-rank structure for the additive weight update during finetuning. In contrast, OFT uses layer-shared orthogonal transformation to update neuron weights in a multiplicative manner, and it provably preserves the pair-wise angles among neurons in the same layer, yielding better stability.

Report issue for preceding element

### 3 Orthogonal Finetuning

Report issue for preceding element

#### 3.1 Why Does Orthogonal Transformation Make Sense?

Report issue for preceding element

We start by discussing why orthogonal transformation is desirable in finetuning text-to-image diffusion models. We decompose this question into two smaller ones: (1) why we want to finetune the angle of neurons (*i.e.*, direction), and (2) why we adopt orthogonal transformation to finetune angles.

Report issue for preceding element

![Refer to caption](x2.png)


Figure 2: A toy experiment to demonstrate the importance of angular information. The autoencoder is trained in a standard way using inner product activation, and (a) shows the standard reconstruction. In testing, the angular information of neurons alone can well recover the input image, even if the autoencoder is not trained with angles.

Report issue for preceding element

For the first question, we draw inspiration from the empirical observation in [[35](https://arxiv.org/html/2306.07280v3#bib.bib35), [7](https://arxiv.org/html/2306.07280v3#bib.bib7)] that angular feature difference well characterizes the semantic gap. SphereNet [[36](https://arxiv.org/html/2306.07280v3#bib.bib36)] shows that training a neural network with all neurons normalized onto a unit hypersphere yields comparable capacity and even better generalizability, implying that the direction of neurons can fully capture the most important information from data. To better demonstrate the importance of neuron angles, we conduct a toy experiment in Figure [2](https://arxiv.org/html/2306.07280v3#S3.F2 "Figure 2 ‣ 3.1 Why Does Orthogonal Transformation Make Sense? ‣ 3 Orthogonal Finetuning ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning") where we train a standard convolutional autoencoder on some flower images. In the training stage, we use the standard inner product to produce the feature map (z𝑧zitalic\_z denotes the element output of the convolution kernel 𝒘𝒘\bm{w}bold\_italic\_w and 𝒙𝒙\bm{x}bold\_italic\_x is the input in the sliding window). In the testing stage, we compare three ways to generate the feature map: (a) the inner product used in training, (b) the magnitude information, and (c) the angular information. The results in Figure [2](https://arxiv.org/html/2306.07280v3#S3.F2 "Figure 2 ‣ 3.1 Why Does Orthogonal Transformation Make Sense? ‣ 3 Orthogonal Finetuning ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning") show that the angular information of neurons can almost perfectly recover the input images, while the magnitude of neurons contains no useful information. We emphasize that we do not apply the cosine activation (c) during training, and the training is done only based on inner product. The results imply that the angles (directions) of neurons play the major role in storing the semantic information of the input images. In order to modify the semantic information of images, finetuning the neuron directions will likely be more effective.

Report issue for preceding element

![Refer to caption](x3.png)


Figure 3: Controllable generation with or without orthogonality. Middle column is from the original OFT, and the right column is given by OFT without the orthogonality constraint.

Report issue for preceding element

For the second question, the simplest way to finetune direction of neurons is to simultaneously rotate / reflect all the neurons (in the same layer), which naturally brings in orthogonal transformation. It may be more flexible to use some other angular transformation that rotates different neurons with different angles, but we find that orthogonal transformation is a sweet spot between flexibility and regularity. Moreover, [[33](https://arxiv.org/html/2306.07280v3#bib.bib33)] shows that orthogonal transformation is sufficiently powerful for learning neural networks. To support our argument, we perform an experiment to demonstrate the effective regularization induced by the orthogonality constraint. We perform the controllable generation experiment using the setting of ControlNet [[68](https://arxiv.org/html/2306.07280v3#bib.bib68)], and the results are given in Figure [3](https://arxiv.org/html/2306.07280v3#S3.F3 "Figure 3 ‣ 3.1 Why Does Orthogonal Transformation Make Sense? ‣ 3 Orthogonal Finetuning ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning"). We can observe that our standard OFT performs quite stably and achieves accurate control after the training is finished (epoch 20). In comparison, OFT without the orthogonality constraint fails to generate any realistic image and achieve no control effect. The experiment validates the importance of the orthogonality constraint in OFT.

Report issue for preceding element

#### 3.2 General Framework

Report issue for preceding element

The conventional finetuning strategy typically uses gradient descent with a small learning rate to update a model (or certain layers of a model). The small learning rate implicitly encourages a small deviation from the pretrained model, and the standard finetuning essentially aims to train the model while implicitly minimizing ‖𝑴−𝑴0‖norm𝑴superscript𝑴0\|\bm{M}-\bm{M}^{0}\|∥ bold\_italic\_M - bold\_italic\_M start\_POSTSUPERSCRIPT 0 end\_POSTSUPERSCRIPT ∥ where 𝑴𝑴\bm{M}bold\_italic\_M is the finetuned model weights and 𝑴0superscript𝑴0\bm{M}^{0}bold\_italic\_M start\_POSTSUPERSCRIPT 0 end\_POSTSUPERSCRIPT is the pretrained model weights. This implicit constraint makes intuitive sense, but it can still be too flexible for finetuning a large model. To address this, LoRA introduces an additional low-rank constraint for the weight update, *i.e.*, rank⁢(𝑴−𝑴0)=r′rank𝑴superscript𝑴0superscript𝑟′\text{rank}(\bm{M}-\bm{M}^{0})=r^{\prime}rank ( bold\_italic\_M - bold\_italic\_M start\_POSTSUPERSCRIPT 0 end\_POSTSUPERSCRIPT ) = italic\_r start\_POSTSUPERSCRIPT ′ end\_POSTSUPERSCRIPT where r′superscript𝑟′r^{\prime}italic\_r start\_POSTSUPERSCRIPT ′ end\_POSTSUPERSCRIPT is set to be some small number. Different from LoRA, OFT introduces a constraint for the pair-wise neuron similarity: ‖HE⁢(𝑴)−HE⁢(𝑴0)‖=0normHE𝑴HEsuperscript𝑴00\|\text{HE}(\bm{M})-\text{HE}(\bm{M}^{0})\|=0∥ HE ( bold\_italic\_M ) - HE ( bold\_italic\_M start\_POSTSUPERSCRIPT 0 end\_POSTSUPERSCRIPT ) ∥ = 0 where HE⁢(⋅)HE⋅\text{HE}(\cdot)HE ( ⋅ ) denotes hyperspherical energy of a weight matrix. As an illustrative example, we consider a fully connected layer 𝑾={𝒘1,⋯,𝒘n}∈ℝd×n𝑾subscript𝒘1⋯subscript𝒘𝑛superscriptℝ𝑑𝑛\bm{W}=\{\bm{w}\_{1},\cdots,\bm{w}\_{n}\}\in\mathbb{R}^{d\times n}bold\_italic\_W = { bold\_italic\_w start\_POSTSUBSCRIPT 1 end\_POSTSUBSCRIPT , ⋯ , bold\_italic\_w start\_POSTSUBSCRIPT italic\_n end\_POSTSUBSCRIPT } ∈ blackboard\_R start\_POSTSUPERSCRIPT italic\_d × italic\_n end\_POSTSUPERSCRIPT where 𝒘i∈ℝdsubscript𝒘𝑖superscriptℝ𝑑\bm{w}\_{i}\in\mathbb{R}^{d}bold\_italic\_w start\_POSTSUBSCRIPT italic\_i end\_POSTSUBSCRIPT ∈ blackboard\_R start\_POSTSUPERSCRIPT italic\_d end\_POSTSUPERSCRIPT is the i𝑖iitalic\_i-th neuron (𝑾0superscript𝑾0\bm{W}^{0}bold\_italic\_W start\_POSTSUPERSCRIPT 0 end\_POSTSUPERSCRIPT is the pretrained weights). The output vector 𝒛∈ℝn𝒛superscriptℝ𝑛\bm{z}\in\mathbb{R}^{n}bold\_italic\_z ∈ blackboard\_R start\_POSTSUPERSCRIPT italic\_n end\_POSTSUPERSCRIPT of this fully connected layer is computed by 𝒛=𝑾⊤⁢𝒙𝒛superscript𝑾top𝒙\bm{z}=\bm{W}^{\top}\bm{x}bold\_italic\_z = bold\_italic\_W start\_POSTSUPERSCRIPT ⊤ end\_POSTSUPERSCRIPT bold\_italic\_x where 𝒙∈ℝd𝒙superscriptℝ𝑑\bm{x}\in\mathbb{R}^{d}bold\_italic\_x ∈ blackboard\_R start\_POSTSUPERSCRIPT italic\_d end\_POSTSUPERSCRIPT is the input vector. OFT can be interpreted as minimizing the hyperspherical energy difference between the finetuned model and the pretrained model:

Report issue for preceding element

|  |  |  |  |
| --- | --- | --- | --- |
|  | min𝑾⁡‖HE⁢(𝑾)−HE⁢(𝑾0)‖⇔min𝑾⁡‖∑i≠j‖𝒘^i−𝒘^j‖−1−∑i≠j‖𝒘^i0−𝒘^j0‖−1‖⇔subscript𝑾normHE𝑾HEsuperscript𝑾0subscript𝑾normsubscript𝑖𝑗superscriptnormsubscript^𝒘𝑖subscript^𝒘𝑗1subscript𝑖𝑗superscriptnormsubscriptsuperscript^𝒘0𝑖subscriptsuperscript^𝒘0𝑗1\footnotesize\min\_{\bm{W}}\left\|\text{HE}(\bm{W})-\text{HE}(\bm{W}^{0})\right% \|~{}~{}\Leftrightarrow~{}~{}\min\_{\bm{W}}\bigg{\|}\sum\_{i\neq j}\|\hat{\bm{w}% }\_{i}-\hat{\bm{w}}\_{j}\|^{-1}-\sum\_{i\neq j}\|\hat{\bm{w}}^{0}\_{i}-\hat{\bm{w}% }^{0}\_{j}\|^{-1}\bigg{\|}roman\_min start\_POSTSUBSCRIPT bold\_italic\_W end\_POSTSUBSCRIPT ∥ HE ( bold\_italic\_W ) - HE ( bold\_italic\_W start\_POSTSUPERSCRIPT 0 end\_POSTSUPERSCRIPT ) ∥ ⇔ roman\_min start\_POSTSUBSCRIPT bold\_italic\_W end\_POSTSUBSCRIPT ∥ ∑ start\_POSTSUBSCRIPT italic\_i ≠ italic\_j end\_POSTSUBSCRIPT ∥ over^ start\_ARG bold\_italic\_w end\_ARG start\_POSTSUBSCRIPT italic\_i end\_POSTSUBSCRIPT - over^ start\_ARG bold\_italic\_w end\_ARG start\_POSTSUBSCRIPT italic\_j end\_POSTSUBSCRIPT ∥ start\_POSTSUPERSCRIPT - 1 end\_POSTSUPERSCRIPT - ∑ start\_POSTSUBSCRIPT italic\_i ≠ italic\_j end\_POSTSUBSCRIPT ∥ over^ start\_ARG bold\_italic\_w end\_ARG start\_POSTSUPERSCRIPT 0 end\_POSTSUPERSCRIPT start\_POSTSUBSCRIPT italic\_i end\_POSTSUBSCRIPT - over^ start\_ARG bold\_italic\_w end\_ARG start\_POSTSUPERSCRIPT 0 end\_POSTSUPERSCRIPT start\_POSTSUBSCRIPT italic\_j end\_POSTSUBSCRIPT ∥ start\_POSTSUPERSCRIPT - 1 end\_POSTSUPERSCRIPT ∥ |  | (1) |

where 𝒘^i:=𝒘i/‖𝒘i‖assignsubscript^𝒘𝑖subscript𝒘𝑖normsubscript𝒘𝑖\hat{\bm{w}}\_{i}:=\bm{w}\_{i}/\|\bm{w}\_{i}\|over^ start\_ARG bold\_italic\_w end\_ARG start\_POSTSUBSCRIPT italic\_i end\_POSTSUBSCRIPT := bold\_italic\_w start\_POSTSUBSCRIPT italic\_i end\_POSTSUBSCRIPT / ∥ bold\_italic\_w start\_POSTSUBSCRIPT italic\_i end\_POSTSUBSCRIPT ∥ denotes the i𝑖iitalic\_i-th normalized neuron, and the hyperspherical energy of a fully connected layer 𝑾𝑾\bm{W}bold\_italic\_W is defined as HE⁢(𝑾):=∑i≠j‖𝒘^i−𝒘^j‖−1assignHE𝑾subscript𝑖𝑗superscriptnormsubscript^𝒘𝑖subscript^𝒘𝑗1\text{HE}(\bm{W}):=\sum\_{i\neq j}\|\hat{\bm{w}}\_{i}-\hat{\bm{w}}\_{j}\|^{-1}HE ( bold\_italic\_W ) := ∑ start\_POSTSUBSCRIPT italic\_i ≠ italic\_j end\_POSTSUBSCRIPT ∥ over^ start\_ARG bold\_italic\_w end\_ARG start\_POSTSUBSCRIPT italic\_i end\_POSTSUBSCRIPT - over^ start\_ARG bold\_italic\_w end\_ARG start\_POSTSUBSCRIPT italic\_j end\_POSTSUBSCRIPT ∥ start\_POSTSUPERSCRIPT - 1 end\_POSTSUPERSCRIPT. One can easily observe that the attainable minimum is zero for Eq. ([1](https://arxiv.org/html/2306.07280v3#S3.E1 "1 ‣ 3.2 General Framework ‣ 3 Orthogonal Finetuning ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")). The minimum can be achieved as long as 𝑾𝑾\bm{W}bold\_italic\_W and 𝑾0superscript𝑾0\bm{W}^{0}bold\_italic\_W start\_POSTSUPERSCRIPT 0 end\_POSTSUPERSCRIPT differ only up to a rotation or reflection, *i.e.*, 𝑾=𝑹⁢𝑾0𝑾𝑹superscript𝑾0\bm{W}=\bm{R}\bm{W}^{0}bold\_italic\_W = bold\_italic\_R bold\_italic\_W start\_POSTSUPERSCRIPT 0 end\_POSTSUPERSCRIPT in which 𝑹∈ℝd×d𝑹superscriptℝ𝑑𝑑\bm{R}\in\mathbb{R}^{d\times d}bold\_italic\_R ∈ blackboard\_R start\_POSTSUPERSCRIPT italic\_d × italic\_d end\_POSTSUPERSCRIPT is an orthogonal matrix (The determinant 1111 or −11-1- 1 means rotation or reflection, respectively). This is exactly the idea of OFT, that we only need to finetune the neural network by learning layer-shared orthogonal matrices to transform neurons in each layer. Formally, OFT seeks to optimize the orthogonal matrix 𝑹∈ℝd×d𝑹superscriptℝ𝑑𝑑\bm{R}\in\mathbb{R}^{d\times d}bold\_italic\_R ∈ blackboard\_R start\_POSTSUPERSCRIPT italic\_d × italic\_d end\_POSTSUPERSCRIPT for a pretrained fully connected layer 𝑾0∈ℝd×nsuperscript𝑾0superscriptℝ𝑑𝑛\bm{W}^{0}\in\mathbb{R}^{d\times n}bold\_italic\_W start\_POSTSUPERSCRIPT 0 end\_POSTSUPERSCRIPT ∈ blackboard\_R start\_POSTSUPERSCRIPT italic\_d × italic\_n end\_POSTSUPERSCRIPT, changing the forward pass from 𝒛=(𝑾0)⊤⁢𝒙𝒛superscriptsuperscript𝑾0top𝒙\bm{z}=(\bm{W}^{0})^{\top}\bm{x}bold\_italic\_z = ( bold\_italic\_W start\_POSTSUPERSCRIPT 0 end\_POSTSUPERSCRIPT ) start\_POSTSUPERSCRIPT ⊤ end\_POSTSUPERSCRIPT bold\_italic\_x to

Report issue for preceding element

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝒛=𝑾⊤⁢𝒙=(𝑹⋅𝑾0)⊤⁢𝒙,s.t.⁢𝑹⊤⁢𝑹=𝑹⁢𝑹⊤=𝑰formulae-sequence𝒛superscript𝑾top𝒙superscript⋅𝑹superscript𝑾0top𝒙s.t.superscript𝑹top𝑹𝑹superscript𝑹top𝑰\footnotesize\bm{z}=\bm{W}^{\top}\bm{x}=(\bm{R}\cdot\bm{W}^{0})^{\top}\bm{x},~% {}~{}~{}\text{s.t.}~{}\bm{R}^{\top}\bm{R}=\bm{R}\bm{R}^{\top}=\bm{I}bold\_italic\_z = bold\_italic\_W start\_POSTSUPERSCRIPT ⊤ end\_POSTSUPERSCRIPT bold\_italic\_x = ( bold\_italic\_R ⋅ bold\_italic\_W start\_POSTSUPERSCRIPT 0 end\_POSTSUPERSCRIPT ) start\_POSTSUPERSCRIPT ⊤ end\_POSTSUPERSCRIPT bold\_italic\_x , s.t. bold\_italic\_R start\_POSTSUPERSCRIPT ⊤ end\_POSTSUPERSCRIPT bold\_italic\_R = bold\_italic\_R bold\_italic\_R start\_POSTSUPERSCRIPT ⊤ end\_POSTSUPERSCRIPT = bold\_italic\_I |  | (2) |

where 𝑾𝑾\bm{W}bold\_italic\_W denotes the OFT-finetuned weight matrix and 𝑰𝑰\bm{I}bold\_italic\_I is an identity matrix. OFT is illustrated in Figure [4](https://arxiv.org/html/2306.07280v3#S3.F4 "Figure 4 ‣ 3.3 Efficient Orthogonal Parameterization ‣ 3 Orthogonal Finetuning ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning"). Similar to the zero initialization in LoRA, we need to ensure OFT to finetune the pretrained model exactly from 𝑾0superscript𝑾0\bm{W}^{0}bold\_italic\_W start\_POSTSUPERSCRIPT 0 end\_POSTSUPERSCRIPT. To achieve this, we initialize the orthogonal matrix 𝑹𝑹\bm{R}bold\_italic\_R to be an identity matrix so that the finetuned model starts with the pretrained weights. To guarantee the orthogonality of the matrix 𝑹𝑹\bm{R}bold\_italic\_R, we can use differential orthogonalization strategies discussed in [[33](https://arxiv.org/html/2306.07280v3#bib.bib33), [26](https://arxiv.org/html/2306.07280v3#bib.bib26)]. We will discuss how to guarantee the orthogonality in a computationally efficient way.

Report issue for preceding element

#### 3.3 Efficient Orthogonal Parameterization

Report issue for preceding element
![Refer to caption](x4.png)


Figure 4: (a) Original OFT without a diagonal structure. (b) OFT with r𝑟ritalic\_r diagonal blocks of the same size. When r=1𝑟1r=1italic\_r = 1, the case of (b) recovers the case of (a).

Report issue for preceding element

Standard orthogonalization such as Gram-Schmidt method, despite differentiable, is often too expensive to compute in practice [[33](https://arxiv.org/html/2306.07280v3#bib.bib33)]. For better efficiency, we adopt Cayley parameterization to generate the orthogonal matrix. Specifically, we construct the orthogonal matrix with 𝑹=(𝑰+𝑸)⁢(I−𝑸)−1𝑹𝑰𝑸superscript𝐼𝑸1\bm{R}=(\bm{I}+\bm{Q})(I-\bm{Q})^{-1}bold\_italic\_R = ( bold\_italic\_I + bold\_italic\_Q ) ( italic\_I - bold\_italic\_Q ) start\_POSTSUPERSCRIPT - 1 end\_POSTSUPERSCRIPT where 𝑸𝑸\bm{Q}bold\_italic\_Q is a skew-symmetric matrix satisfying 𝑸=−𝑸⊤𝑸superscript𝑸top\bm{Q}=-\bm{Q}^{\top}bold\_italic\_Q = - bold\_italic\_Q start\_POSTSUPERSCRIPT ⊤ end\_POSTSUPERSCRIPT. Such an efficiency comes at a small price – the Cayley parameterization can only produce orthogonal matrices with determinant 1111 which belongs to the special orthogonal group. Fortunately, we find that such a limitation does not affect the performance in practice. Even if we use Cayley transform to parameterize the orthogonal matrix, 𝑹𝑹\bm{R}bold\_italic\_R can still be very parameter-inefficient with a large d𝑑ditalic\_d. To address this, we propose to represent 𝑹𝑹\bm{R}bold\_italic\_R with a block-diagonal matrix with r𝑟ritalic\_r blocks, leading to the following form:

Report issue for preceding element

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝑹=diag⁢(𝑹1,𝑹2,⋯,𝑹r)=[𝑹1∈O⁢(dr)⋱𝑹r∈O⁢(dr)]∈O⁢(d)𝑹diagsubscript𝑹1subscript𝑹2⋯subscript𝑹𝑟matrixsubscript𝑹1O𝑑𝑟missing-subexpressionmissing-subexpressionmissing-subexpression⋱missing-subexpressionmissing-subexpressionmissing-subexpressionsubscript𝑹𝑟O𝑑𝑟O𝑑\footnotesize\bm{R}=\text{diag}(\bm{R}\_{1},\bm{R}\_{2},\cdots,\bm{R}\_{r})=% \begin{bmatrix}\bm{R}\_{1}\in\text{O}(\frac{d}{r})&&\\ &\ddots&\\ &&\bm{R}\_{r}\in\text{O}(\frac{d}{r})\end{bmatrix}\in\text{O}(d)bold\_italic\_R = diag ( bold\_italic\_R start\_POSTSUBSCRIPT 1 end\_POSTSUBSCRIPT , bold\_italic\_R start\_POSTSUBSCRIPT 2 end\_POSTSUBSCRIPT , ⋯ , bold\_italic\_R start\_POSTSUBSCRIPT italic\_r end\_POSTSUBSCRIPT ) = [ start\_ARG start\_ROW start\_CELL bold\_italic\_R start\_POSTSUBSCRIPT 1 end\_POSTSUBSCRIPT ∈ O ( divide start\_ARG italic\_d end\_ARG start\_ARG italic\_r end\_ARG ) end\_CELL start\_CELL end\_CELL start\_CELL end\_CELL end\_ROW start\_ROW start\_CELL end\_CELL start\_CELL ⋱ end\_CELL start\_CELL end\_CELL end\_ROW start\_ROW start\_CELL end\_CELL start\_CELL end\_CELL start\_CELL bold\_italic\_R start\_POSTSUBSCRIPT italic\_r end\_POSTSUBSCRIPT ∈ O ( divide start\_ARG italic\_d end\_ARG start\_ARG italic\_r end\_ARG ) end\_CELL end\_ROW end\_ARG ] ∈ O ( italic\_d ) |  | (3) |

where O⁢(d)O𝑑\text{O}(d)O ( italic\_d ) denotes the orthogonal group in dimension d𝑑ditalic\_d, and 𝑹∈ℝd×d𝑹superscriptℝ𝑑𝑑\bm{R}\in\mathbb{R}^{d\times d}bold\_italic\_R ∈ blackboard\_R start\_POSTSUPERSCRIPT italic\_d × italic\_d end\_POSTSUPERSCRIPT and 𝑹i∈ℝd/r×d/r,∀isubscript𝑹𝑖

superscriptℝ𝑑𝑟𝑑𝑟for-all𝑖\bm{R}\_{i}\in\mathbb{R}^{d/r\times d/r},\forall ibold\_italic\_R start\_POSTSUBSCRIPT italic\_i end\_POSTSUBSCRIPT ∈ blackboard\_R start\_POSTSUPERSCRIPT italic\_d / italic\_r × italic\_d / italic\_r end\_POSTSUPERSCRIPT , ∀ italic\_i are orthogonal matrices. When r=1𝑟1r=1italic\_r = 1, then the block-diagonal orthogonal matrix becomes a standard unconstrained one. For an orthogonal matrix with size d×d𝑑𝑑d\times ditalic\_d × italic\_d, the number of parameters is d⁢(d−1)/2𝑑𝑑12d(d-1)/2italic\_d ( italic\_d - 1 ) / 2, resulting in a complexity of 𝒪⁢(d2)𝒪superscript𝑑2\mathcal{O}(d^{2})caligraphic\_O ( italic\_d start\_POSTSUPERSCRIPT 2 end\_POSTSUPERSCRIPT ). For an r𝑟ritalic\_r-block diagonal orthogonal matrix, the number of parameter is d⁢(d/r−1)/2𝑑𝑑𝑟12d(d/r-1)/2italic\_d ( italic\_d / italic\_r - 1 ) / 2, resulting in a complexity of 𝒪⁢(d2/r)𝒪superscript𝑑2𝑟\mathcal{O}(d^{2}/r)caligraphic\_O ( italic\_d start\_POSTSUPERSCRIPT 2 end\_POSTSUPERSCRIPT / italic\_r ). We can optionally share the block matrix to further reduce the number of parameters, *i.e.*, 𝑹i=𝑹j,∀i≠jformulae-sequencesubscript𝑹𝑖subscript𝑹𝑗for-all𝑖𝑗\bm{R}\_{i}=\bm{R}\_{j},\forall i\neq jbold\_italic\_R start\_POSTSUBSCRIPT italic\_i end\_POSTSUBSCRIPT = bold\_italic\_R start\_POSTSUBSCRIPT italic\_j end\_POSTSUBSCRIPT , ∀ italic\_i ≠ italic\_j. This reduces the parameter complexity to 𝒪⁢(d2/r2)𝒪superscript𝑑2superscript𝑟2\mathcal{O}(d^{2}/r^{2})caligraphic\_O ( italic\_d start\_POSTSUPERSCRIPT 2 end\_POSTSUPERSCRIPT / italic\_r start\_POSTSUPERSCRIPT 2 end\_POSTSUPERSCRIPT ). Despite all these strategies to improve parameter efficiency, we note that the resulting matrix 𝑹𝑹\bm{R}bold\_italic\_R remains orthogonal, so there is no sacrifice in preserving hyperspherical energy.

Report issue for preceding element

We discuss how OFT compares to LoRA in terms of parameter efficiency. For LoRA with a low-rank parameter r′superscript𝑟′r^{\prime}italic\_r start\_POSTSUPERSCRIPT ′ end\_POSTSUPERSCRIPT, we have its number of trainable parameters as r′⁢(d+n)superscript𝑟′𝑑𝑛r^{\prime}(d+n)italic\_r start\_POSTSUPERSCRIPT ′ end\_POSTSUPERSCRIPT ( italic\_d + italic\_n ). If we consider both r𝑟ritalic\_r and r′superscript𝑟′r^{\prime}italic\_r start\_POSTSUPERSCRIPT ′ end\_POSTSUPERSCRIPT to be dependent on the neuron dimension d𝑑ditalic\_d (*e.g.*, r=r′=α⁢d𝑟superscript𝑟′𝛼𝑑r=r^{\prime}=\alpha ditalic\_r = italic\_r start\_POSTSUPERSCRIPT ′ end\_POSTSUPERSCRIPT = italic\_α italic\_d where 0<α≤10𝛼10<\alpha\leq 10 < italic\_α ≤ 1 is some constant), then the parameter complexity of LoRA becomes 𝒪⁢(d2+d⁢n)𝒪superscript𝑑2𝑑𝑛\mathcal{O}(d^{2}+dn)caligraphic\_O ( italic\_d start\_POSTSUPERSCRIPT 2 end\_POSTSUPERSCRIPT + italic\_d italic\_n ) and the parameter complexity of OFT becomes 𝒪⁢(d)𝒪𝑑\mathcal{O}(d)caligraphic\_O ( italic\_d ). We illustrate the difference in complexity between OFT and LoRA with a concrete example. Suppose we have a weight matrix with size 128×128128128128\times 128128 × 128, LoRA has 2,048

20482,0482 , 048 trainable parameters with r′=8superscript𝑟′8r^{\prime}=8italic\_r start\_POSTSUPERSCRIPT ′ end\_POSTSUPERSCRIPT = 8, while OFT has 960960960960 trainable parameters with r=8𝑟8r=8italic\_r = 8 (no block sharing is applied).

Report issue for preceding element

#### 3.4 Constrained Orthogonal Finetuning

Report issue for preceding element

We can further limit the flexibility of original OFT by constraining the finetuned model to be within a small neighborhood of the pretrained model. Specifically, COFT uses the following forward pass:

Report issue for preceding element

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝒛=𝑾⊤⁢𝒙=(𝑹⋅𝑾0)⊤⁢𝒙,s.t.⁢𝑹⊤⁢𝑹=𝑹⁢𝑹⊤=𝑰,∥𝑹−𝑰∥≤ϵformulae-sequence𝒛superscript𝑾top𝒙superscript⋅𝑹superscript𝑾0top𝒙s.t.superscript𝑹top𝑹𝑹superscript𝑹top𝑰delimited-∥∥𝑹𝑰italic-ϵ\footnotesize\bm{z}=\bm{W}^{\top}\bm{x}=(\bm{R}\cdot\bm{W}^{0})^{\top}\bm{x},~% {}~{}~{}\text{s.t.}~{}\bm{R}^{\top}\bm{R}=\bm{R}\bm{R}^{\top}=\bm{I},~{}\left% \lVert\bm{R}-\bm{I}\right\rVert\leq\epsilonbold\_italic\_z = bold\_italic\_W start\_POSTSUPERSCRIPT ⊤ end\_POSTSUPERSCRIPT bold\_italic\_x = ( bold\_italic\_R ⋅ bold\_italic\_W start\_POSTSUPERSCRIPT 0 end\_POSTSUPERSCRIPT ) start\_POSTSUPERSCRIPT ⊤ end\_POSTSUPERSCRIPT bold\_italic\_x , s.t. bold\_italic\_R start\_POSTSUPERSCRIPT ⊤ end\_POSTSUPERSCRIPT bold\_italic\_R = bold\_italic\_R bold\_italic\_R start\_POSTSUPERSCRIPT ⊤ end\_POSTSUPERSCRIPT = bold\_italic\_I , ∥ bold\_italic\_R - bold\_italic\_I ∥ ≤ italic\_ϵ |  | (4) |

which has an orthogonality constraint and an ϵitalic-ϵ\epsilonitalic\_ϵ-deviation constraint to an identity matrix. The orthogonality constraint can be achieved with the Cayley parameterization introduced in Section [3.3](https://arxiv.org/html/2306.07280v3#S3.SS3 "3.3 Efficient Orthogonal Parameterization ‣ 3 Orthogonal Finetuning ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning"). However, it is nontrivial to incorporate the ϵitalic-ϵ\epsilonitalic\_ϵ-deviation constraint to the Cayley-parameterized orthogonal matrix. To gain more insights on the Cayley transform, we apply the Neumann series to approximate 𝑹=(𝑰+𝑸)⁢(I−𝑸)−1𝑹𝑰𝑸superscript𝐼𝑸1\bm{R}=(\bm{I}+\bm{Q})(I-\bm{Q})^{-1}bold\_italic\_R = ( bold\_italic\_I + bold\_italic\_Q ) ( italic\_I - bold\_italic\_Q ) start\_POSTSUPERSCRIPT - 1 end\_POSTSUPERSCRIPT as 𝑹≈𝑰+2⁢𝑸+𝒪⁢(𝑸2)𝑹𝑰2𝑸𝒪superscript𝑸2\bm{R}\approx\bm{I}+2\bm{Q}+\mathcal{O}(\bm{Q}^{2})bold\_italic\_R ≈ bold\_italic\_I + 2 bold\_italic\_Q + caligraphic\_O ( bold\_italic\_Q start\_POSTSUPERSCRIPT 2 end\_POSTSUPERSCRIPT ) (under the assumption that the Neumann

Report issue for preceding element

![Refer to caption](x5.png)


Figure 5: How ϵitalic-ϵ\epsilonitalic\_ϵ affects the flexibility of COFT in subject-driven generation.

Report issue for preceding element

series converges in the operator norm). Therefore, we can move the constraint ‖𝑹−𝑰‖≤ϵnorm𝑹𝑰italic-ϵ\|\bm{R}-\bm{I}\|\leq\epsilon∥ bold\_italic\_R - bold\_italic\_I ∥ ≤ italic\_ϵ inside the Cayley transform, and the equivalent constraint is ‖𝑸−𝟎‖≤ϵ′norm𝑸0superscriptitalic-ϵ′\|\bm{Q}-\bm{0}\|\leq\epsilon^{\prime}∥ bold\_italic\_Q - bold\_0 ∥ ≤ italic\_ϵ start\_POSTSUPERSCRIPT ′ end\_POSTSUPERSCRIPT where 𝟎0\bm{0}bold\_0 denotes an all-zero matrix and ϵ′superscriptitalic-ϵ′\epsilon^{\prime}italic\_ϵ start\_POSTSUPERSCRIPT ′ end\_POSTSUPERSCRIPT is another error hyperparameter (different than ϵitalic-ϵ\epsilonitalic\_ϵ). The new constraint on the matrix 𝑸𝑸\bm{Q}bold\_italic\_Q can be easily enforced by projected gradient descent. To achieve identity initialization for the orthogonal matrix 𝑹𝑹\bm{R}bold\_italic\_R, we initialize 𝑸𝑸\bm{Q}bold\_italic\_Q as an all-zero matrix. COFT can be viewed as a combination of two explicit constraints: minimal hyperspherical energy difference and constrained deviation from the pretrained model. The second constraint is usually implicitly used by existing finetuning methods, but COFT makes it an explicit one. Despite the excellent performance of OFT, we observe that COFT yields even better finetuning stability than OFT due to this explicit deviation constraint. Figure [5](https://arxiv.org/html/2306.07280v3#S3.F5 "Figure 5 ‣ 3.4 Constrained Orthogonal Finetuning ‣ 3 Orthogonal Finetuning ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning") provides an example on how ϵitalic-ϵ\epsilonitalic\_ϵ affects the performance of COFT. We can observe that ϵitalic-ϵ\epsilonitalic\_ϵ controls the flexibility of finetuning. With larger ϵitalic-ϵ\epsilonitalic\_ϵ, the COFT-finetuned model resembles the OFT-finetuned model. With smaller ϵitalic-ϵ\epsilonitalic\_ϵ, the COFT-finetuned model behaves increasingly similar to the pretrained text-to-image diffusion model.

Report issue for preceding element

#### 3.5 Re-scaled Orthogonal Finetuning

Report issue for preceding element

We propose a simple extension to the original OFT by additionally learning a magnitude scaling coefficient for each neuron. This is motivated by the fact that re-scaling neurons does not change the hyperspherical energy (the magnitude will be normalized out). Specifically, we use the forward pass: 𝒛=(𝑹⁢𝑾0⁢𝑫)⊤⁢𝒙𝒛superscript𝑹superscript𝑾0𝑫top𝒙\bm{z}=(\bm{R}\bm{W}^{0}\bm{D})^{\top}\bm{x}bold\_italic\_z = ( bold\_italic\_R bold\_italic\_W start\_POSTSUPERSCRIPT 0 end\_POSTSUPERSCRIPT bold\_italic\_D ) start\_POSTSUPERSCRIPT ⊤ end\_POSTSUPERSCRIPT bold\_italic\_x111Errata: In the NeurIPS camera ready version, the forward pass of re-scaled OFT is mistakenly written as 𝒛=(𝑫⁢𝑹⁢𝑾0)⊤⁢𝒙𝒛superscript𝑫𝑹superscript𝑾0top𝒙\bm{z}=(\bm{D}\bm{R}\bm{W}^{0})^{\top}\bm{x}bold\_italic\_z = ( bold\_italic\_D bold\_italic\_R bold\_italic\_W start\_POSTSUPERSCRIPT 0 end\_POSTSUPERSCRIPT ) start\_POSTSUPERSCRIPT ⊤ end\_POSTSUPERSCRIPT bold\_italic\_x. The original implementation is correct, so the results in Appendix [C](https://arxiv.org/html/2306.07280v3#A3 "Appendix C Experiments on Re-scaled OFT ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning") are unaffected. where 𝑫=diag⁢(s1,⋯,sn)∈ℝn×n𝑫diagsubscript𝑠1⋯subscript𝑠𝑛superscriptℝ𝑛𝑛\bm{D}=\text{diag}(s\_{1},\cdots,s\_{n})\in\mathbb{R}^{n\times n}bold\_italic\_D = diag ( italic\_s start\_POSTSUBSCRIPT 1 end\_POSTSUBSCRIPT , ⋯ , italic\_s start\_POSTSUBSCRIPT italic\_n end\_POSTSUBSCRIPT ) ∈ blackboard\_R start\_POSTSUPERSCRIPT italic\_n × italic\_n end\_POSTSUPERSCRIPT is a learnable diagonal matrix with all the diagonal element s1,⋯,sn

subscript𝑠1⋯subscript𝑠𝑛s\_{1},\cdots,s\_{n}italic\_s start\_POSTSUBSCRIPT 1 end\_POSTSUBSCRIPT , ⋯ , italic\_s start\_POSTSUBSCRIPT italic\_n end\_POSTSUBSCRIPT larger than zero. In contrast to OFT’s original forward pass in Eq. ([2](https://arxiv.org/html/2306.07280v3#S3.E2 "2 ‣ 3.2 General Framework ‣ 3 Orthogonal Finetuning ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")) where only 𝑹𝑹\bm{R}bold\_italic\_R is learnable, we have both the diagonal matrix 𝑫𝑫\bm{D}bold\_italic\_D and the orthogonal matrix 𝑹𝑹\bm{R}bold\_italic\_R learnable. The re-scaled OFT further improves the flexibility of OFT with a neglectable number of additional parameters. We stick to the original OFT in the experiment to show the effectiveness of orthogonal transformation alone, but we find that the re-scaled OFT is generally better (see Appendix [C](https://arxiv.org/html/2306.07280v3#A3 "Appendix C Experiments on Re-scaled OFT ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")).

Report issue for preceding element

### 4 Intriguing Insights and Discussions

Report issue for preceding element

OFT is agnostic to different architectures. We can apply OFT to any type of neural network in principle. For Transformers, LoRA is typically applied to the attention weights [[22](https://arxiv.org/html/2306.07280v3#bib.bib22)]. To compare fairly to LoRA, we only apply OFT to finetune the attention weights in our experiments. Besides fully connected layers, OFT is also well suited for finetuning convolution layers, because the block-diagonal structure of 𝑹𝑹\bm{R}bold\_italic\_R has interesting interpretations in convolution layers (unlike LoRA). When we use the same number of blocks as the number of input channels, each block only transforms a unique neuron channel, similar to learning depth-wise convolution kernels [[10](https://arxiv.org/html/2306.07280v3#bib.bib10)]. When all the blocks in 𝑹𝑹\bm{R}bold\_italic\_R are shared, OFT transforms the neurons with an orthogonal matrix shared across channels. We conduct a preliminary study on finetuning convolution layers with OFT in Appendix [D](https://arxiv.org/html/2306.07280v3#A4 "Appendix D Applying OFT to Convolution Layers ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")

Report issue for preceding element

Connection to LoRA. By adding a low-rank matrix, LoRA prevents the information in the pretrained weight matrix from shifting dramatically. In contrast, OFT controls the transform that applies to the pretrained weight matrix to be orthogonal (full-rank), which prevents the transform to destroy the pretraining information. We can rewrite OFT’s forward pass as 𝒛=(𝑹⁢𝑾0)⊤⁢𝒙=(𝑾0+(𝑹−𝑰)⁢𝑾0)⊤⁢𝒙𝒛superscript𝑹superscript𝑾0top𝒙superscriptsuperscript𝑾0𝑹𝑰superscript𝑾0top𝒙\bm{z}=(\bm{R}\bm{W}^{0})^{\top}\bm{x}=(\bm{W}^{0}+(\bm{R}-\bm{I})\bm{W}^{0})^%
{\top}\bm{x}bold\_italic\_z = ( bold\_italic\_R bold\_italic\_W start\_POSTSUPERSCRIPT 0 end\_POSTSUPERSCRIPT ) start\_POSTSUPERSCRIPT ⊤ end\_POSTSUPERSCRIPT bold\_italic\_x = ( bold\_italic\_W start\_POSTSUPERSCRIPT 0 end\_POSTSUPERSCRIPT + ( bold\_italic\_R - bold\_italic\_I ) bold\_italic\_W start\_POSTSUPERSCRIPT 0 end\_POSTSUPERSCRIPT ) start\_POSTSUPERSCRIPT ⊤ end\_POSTSUPERSCRIPT bold\_italic\_x where (𝑹−𝑰)⁢𝑾0𝑹𝑰superscript𝑾0(\bm{R}-\bm{I})\bm{W}^{0}( bold\_italic\_R - bold\_italic\_I ) bold\_italic\_W start\_POSTSUPERSCRIPT 0 end\_POSTSUPERSCRIPT is analogous to LoRA’s low-rank weight update. Since 𝑾0superscript𝑾0\bm{W}^{0}bold\_italic\_W start\_POSTSUPERSCRIPT 0 end\_POSTSUPERSCRIPT is typically full-rank, OFT also performs low-rank weight update when 𝑹−𝑰𝑹𝑰\bm{R}-\bm{I}bold\_italic\_R - bold\_italic\_I is low-rank. Similar to LoRA that has a rank parameter r′superscript𝑟′r^{\prime}italic\_r start\_POSTSUPERSCRIPT ′ end\_POSTSUPERSCRIPT, OFT has a diagonal block parameter r𝑟ritalic\_r to reduce the number of trainable parameters. More interestingly, LoRA and OFT represent two distinct ways to be parameter-efficient. LoRA exploits the low-rank structure to reduce the number of trainable parameters, while OFT takes a different route by exploiting the sparsity structure (*i.e.*, block-diagonal orthogonality).

Report issue for preceding element

Why OFT converges faster. On one hand, we can see from Figure [2](https://arxiv.org/html/2306.07280v3#S3.F2 "Figure 2 ‣ 3.1 Why Does Orthogonal Transformation Make Sense? ‣ 3 Orthogonal Finetuning ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning") that the most effective update to modify the semantics is to change neuron directions, which is exactly what OFT is designed for. On the other hand, OFT can be viewed as finetuning neurons on a smooth hypersphere manifold, which yields better optimization landscape. This is also empirically verified in [[33](https://arxiv.org/html/2306.07280v3#bib.bib33)].

Report issue for preceding element

Why not minimize hyperspherical energy. A key difference to [[33](https://arxiv.org/html/2306.07280v3#bib.bib33)] is that we do not aim to minimize hyperspherical energy. In classification problems, neurons without redundancy are desired. The minimum hyperspherical energy means all neurons are uniformly spaced around the hypersphere. This is not a meaningful objective for finetuning, as it may destroy the pretraining information.

Report issue for preceding element

Trade-off between flexibility and regularity in finetuning. We discover an underlying trade-off between flexibility and regularity. Standard finetuning is the most flexible method, but it yields poor stability and easily causes model collapse. Being surprisingly simple, OFT finds a good balance between flexibility and regularity by preserving the pairwise neuron angles. The block-diagonal parameterization can also be viewed as a stronger regularization of the orthogonal matrix.

Report issue for preceding element

No additional inference overhead. Unlike ControlNet, our OFT framework introduces no additional inference overhead to the finetuned model. In the inference stage, we can simply multiply the learned orthogonal matrix 𝑹𝑹\bm{R}bold\_italic\_R into the pretrained weight matrix 𝑾0superscript𝑾0\bm{W}^{0}bold\_italic\_W start\_POSTSUPERSCRIPT 0 end\_POSTSUPERSCRIPT and obtain an equivalent weight matrix 𝑾=𝑹⁢𝑾0𝑾𝑹superscript𝑾0\bm{W}=\bm{R}\bm{W}^{0}bold\_italic\_W = bold\_italic\_R bold\_italic\_W start\_POSTSUPERSCRIPT 0 end\_POSTSUPERSCRIPT. Thus the inference speed is the same as the pretrained model.

Report issue for preceding element

### 5 Experiments and Results

Report issue for preceding element

General settings. In the experiment, we use Stable Diffusion v1.5 [[50](https://arxiv.org/html/2306.07280v3#bib.bib50)] as the pretrained text-to-image model.
For fairness, we randomly pick generated images from each method. For subject-driven generation, we generally follow DreamBooth [[51](https://arxiv.org/html/2306.07280v3#bib.bib51)]. For controllable generation, we generally follow ControlNet [[68](https://arxiv.org/html/2306.07280v3#bib.bib68)] and T2I-Adapter [[38](https://arxiv.org/html/2306.07280v3#bib.bib38)]. To ensure a fair comparison to LoRA, we only apply OFT or COFT to the same layer where LoRA is used. More results and details are given in Appendix [A](https://arxiv.org/html/2306.07280v3#A1 "Appendix A Experimental Details ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning").

Report issue for preceding element

#### 5.1 Subject-driven Generation

Report issue for preceding element
![Refer to caption](x6.png)


Figure 6: Generated images across different iterations.

Report issue for preceding element

Settings. We use DreamBooth [[51](https://arxiv.org/html/2306.07280v3#bib.bib51)] and LoRA [[22](https://arxiv.org/html/2306.07280v3#bib.bib22)] as the baselines. All the methods adopt the same loss function as in DreamBooth. For DreamBooth and LoRA, we generally follow the original paper and use the best hyperparameter setup. More results are provided in Appendix [A](https://arxiv.org/html/2306.07280v3#A1 "Appendix A Experimental Details ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning"),[E](https://arxiv.org/html/2306.07280v3#A5 "Appendix E Comparison between COFT and OFT ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning"),[F](https://arxiv.org/html/2306.07280v3#A6 "Appendix F More Qualitative Results ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning"),[J](https://arxiv.org/html/2306.07280v3#A10 "Appendix J Failure Cases ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning").

Report issue for preceding element

Finetuning stability and convergence. We first evaluate the finetuning stability and the convergence speed for DreamBooth, LoRA, OFT and COFT. Results are given in Figure [1](https://arxiv.org/html/2306.07280v3#S1.F1 "Figure 1 ‣ 1 Introduction ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning") and Figure [6](https://arxiv.org/html/2306.07280v3#S5.F6 "Figure 6 ‣ 5.1 Subject-driven Generation ‣ 5 Experiments and Results ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning"). We can observe that both COFT and OFT are able to finetune the diffusion model quite stably. After 400 iterations, both DreamBooth and OFT variants achieve good control, while LoRA fails to preserve the subject identity. After 2000 iterations, DreamBooth starts to generate collapsed images, and LoRA fails to generate yellow shirt (and instead generates yellow fur). In contrast, both OFT and COFT are still able to achieve stable and consistent control over the generated image. These results validate the fast yet stable convergence of our OFT framework in subject-driven generation. We note that the insensitivity to the number of finetuning iteration is quite important, since it can effectively alleviate the trouble of tuning the iteration number for different subjects. For both OFT and COFT, we can directly set a relatively large iteration number without carefully tuning it. For COFT with a proper ϵitalic-ϵ\epsilonitalic\_ϵ, both the learning rate and the iteration number become effortless to set.

Report issue for preceding element

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| Method | DINO ↑↑\uparrow↑ | CLIP-I ↑↑\uparrow↑ | CLIP-T ↑↑\uparrow↑ | LPIPS ↑↑\uparrow↑ |
| Real Images | 0.703 | 0.864 | - | 0.695 |
| DreamBooth | 0.614 | 0.778 | 0.239 | 0.737 |
| LoRA | 0.613 | 0.765 | 0.237 | 0.744 |
| COFT | 0.630 | 0.783 | 0.235 | 0.744 |
| OFT | 0.632 | 0.785 | 0.237 | 0.746 |

Table 1: Quantitative comparison of subject fidelity (DINO, CLIP-I), prompt fidelity (CLIP-T) and diversity metric (LPIPS). The evaluation images and prompts are the same as [[51](https://arxiv.org/html/2306.07280v3#bib.bib51)] (25 subjects with 30 text prompts each subject).

Report issue for preceding element
![Refer to caption](x7.png)


Figure 7: Qualitative comparison of subject-driven generation among DreamBooth, LoRA, COFT and OFT. Results are generated with the same finetuned model from each method. All examples are randomly picked. The figure is best viewed digitally, in color and significantly zoomed in.

Report issue for preceding element

Quantitative comparison. Following [[51](https://arxiv.org/html/2306.07280v3#bib.bib51)], we conduct a quantitative comparison to evaluate subject fidelity (DINO [[5](https://arxiv.org/html/2306.07280v3#bib.bib5)], CLIP-I [[44](https://arxiv.org/html/2306.07280v3#bib.bib44)]), text prompt fidelity (CLIP-T [[44](https://arxiv.org/html/2306.07280v3#bib.bib44)]) and sample diversity (LPIPS [[69](https://arxiv.org/html/2306.07280v3#bib.bib69)]). CLIP-I computes the average pairwise cosine similarity of CLIP embeddings between generated and real images. DINO is similar to CLIP-I, except that we use ViT S/16 DINO embeddings. CLIP-T is the average cosine similarity of CLIP embeddings between text prompt and generated images. We also evaluate average LPIPS cosine similarity between generated images of the same subject with the same text prompt. Table [1](https://arxiv.org/html/2306.07280v3#S5.T1 "Table 1 ‣ 5.1 Subject-driven Generation ‣ 5 Experiments and Results ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning") show that both COFT and OFT outperforms DreamBooth and LoRA in the DINO and CLIP-I metrics by a considerable margin, while achieving slightly better or comparable performance in prompt fidelity and diversity metric. For each method, we repeatedly finetune the same pretrained model with 30 different random seeds to minimize randomness. The results show that our OFT framework not only achieves better convergence and stability, but also yields consistently better final performance.

Report issue for preceding element

Qualitative comparison. To have a more intuitive understanding of OFT’s benefits, we show some randomly picked examples for subject-driven generation in Figure [7](https://arxiv.org/html/2306.07280v3#S5.F7 "Figure 7 ‣ 5.1 Subject-driven Generation ‣ 5 Experiments and Results ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning"). For a fair comparison, all the examples are generated from the same finetuned model using each method, so no text prompt will be separately optimized for its final results. For each method, we select the model that achieves the best validation CLIP metrics. From the results in Figure [7](https://arxiv.org/html/2306.07280v3#S5.F7 "Figure 7 ‣ 5.1 Subject-driven Generation ‣ 5 Experiments and Results ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning"), we can observe that both OFT and COFT deliver excellent semantic subject preservation, while LoRA often fails to preserve the subject identity (*e.g.*, LoRA completely loses the subject identity in the bowl example). In the meantime, both OFT and COFT have much more accurate control using text prompts, while DreamBooth, despite its preservation of subject identity, often fails to generate the image following the text prompt (*e.g.*, the first row of the bowl example). The qualitative comparison demonstrates that our OFT framework achieves better controllability and subject preservation at the same time. Moreover, the number of iterations is not sensitive in OFT, so OFT performs well even with a large number of iterations, while neither DreamBooth nor LoRA can. More qualitative examples are given in Appendix [F](https://arxiv.org/html/2306.07280v3#A6 "Appendix F More Qualitative Results ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning"). Moreover, we conduct a human evaluation in Appendix [H](https://arxiv.org/html/2306.07280v3#A8 "Appendix H Human Evaluation ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning") which further validates the superiority of OFT.

Report issue for preceding element

#### 5.2 Controllable Generation

Report issue for preceding element

Settings. We use ControlNet [[68](https://arxiv.org/html/2306.07280v3#bib.bib68)], T2I-Adapter [[38](https://arxiv.org/html/2306.07280v3#bib.bib38)] and LoRA [[22](https://arxiv.org/html/2306.07280v3#bib.bib22)] as the baselines. We consider three challenging controllable generation tasks in the main paper: Canny edge to image (C2I) on the COCO dataset [[31](https://arxiv.org/html/2306.07280v3#bib.bib31)], segmentation map to image (S2I) on the ADE20K dataset [[70](https://arxiv.org/html/2306.07280v3#bib.bib70)] and landmark to face (L2F) on the CelebA-HQ dataset [[25](https://arxiv.org/html/2306.07280v3#bib.bib25), [63](https://arxiv.org/html/2306.07280v3#bib.bib63)]. All the methods are used to finetune Stable Diffusion (SD) v1.5 on these three datasets for 20 epochs. More results are given in Appendix [F](https://arxiv.org/html/2306.07280v3#A6 "Appendix F More Qualitative Results ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning"),[G](https://arxiv.org/html/2306.07280v3#A7 "Appendix G More Controllable Generation Tasks ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning"),[J](https://arxiv.org/html/2306.07280v3#A10 "Appendix J Failure Cases ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning").

Report issue for preceding element

![Refer to caption](x8.png)


Figure 8: Face landmark error.

Report issue for preceding element

Convergence. We evaluate the convergence speed of ControlNet, T2I-Adapter, LoRA and COFT on the L2F task. We provide both quantitative and qualitative evaluation. Specifically for the evaluation metric, we compute the mean ℓ2subscriptℓ2\ell\_{2}roman\_ℓ start\_POSTSUBSCRIPT 2 end\_POSTSUBSCRIPT distance between control face landmarks and predicted face landmarks. In Figure [8](https://arxiv.org/html/2306.07280v3#S5.F8 "Figure 8 ‣ 5.2 Controllable Generation ‣ 5 Experiments and Results ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning"), we plot the face landmark error obtained by the model finetuned with different number of epochs. We can observe that both COFT and OFT achieve significantly faster convergence. It takes 20 epochs for LoRA to converge to the performance of our OFT framework at the 8-th epoch. We note that OFT and COFT use a similar number of trainable parameters to LoRA (much fewer than ControlNet), while being much more efficient to converge than existing methods. On the other hand, the fast convergence of OFT is also validated by the results in Figure [1](https://arxiv.org/html/2306.07280v3#S1.F1 "Figure 1 ‣ 1 Introduction ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning"). The right example in Figure [1](https://arxiv.org/html/2306.07280v3#S1.F1 "Figure 1 ‣ 1 Introduction ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning") shows that OFT is much more data-efficient than ControlNet and LoRA, since OFT can converge well with only 5% of the ADE20K dataset. For qualitative results, we focus on comparing OFT, COFT and ControlNet, because ControlNet achieves the closest landmark error to ours. Results in Figure [9](https://arxiv.org/html/2306.07280v3#S5.F9 "Figure 9 ‣ 5.2 Controllable Generation ‣ 5 Experiments and Results ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning") show that both OFT and COFT converge stably and the generated face pose is gradually aligned with the control landmarks. In contrast to our stable and smooth convergence, the controllability in ControlNet suddenly emerges after the 8-th epoch, which perfectly matches the sudden convergence phenomenon observed in [[68](https://arxiv.org/html/2306.07280v3#bib.bib68)]. Such a convergence stability makes our OFT framework much easier to use in practice, since the training dynamics of OFT is far more smooth and predictable. Thus it will be easier to find good OFT’s hyperparameters.

Report issue for preceding element

![Refer to caption](x9.png)


Figure 9: Qualitative examples with different number of epochs.

Report issue for preceding element

Quantitative comparison. We introduce a control consistency metric to evaluate the performance of controllable generation. The basic idea is to compute the control signal from the generated image and then compare it with the original input control signal. For the C2I task, we compute IoU and F1 score. For the S2I task, we compute mean IoU, mean and overall accuracy. For the L2F task, we compute the mean ℓ2subscriptℓ2\ell\_{2}roman\_ℓ start\_POSTSUBSCRIPT 2 end\_POSTSUBSCRIPT distance between control landmarks and predicted landmarks. More details regarding the consistency metrics are given in Appendix [A](https://arxiv.org/html/2306.07280v3#A1 "Appendix A Experimental Details ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning"). For all the compared method, we use the best possible hyperparameter settings. Results in Table [2](https://arxiv.org/html/2306.07280v3#S5.T2 "Table 2 ‣ 5.2 Controllable Generation ‣ 5 Experiments and Results ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning") show that both OFT and COFT yield much stronger and accurate control than the other methods. We observe that the adapter-based approaches (*e.g.*, T2I-Adapter and ControlNet) converge slowly and also yield worse final results. Compared to ControlNet, LoRA performs better in the S2I task and worse in the C2I and L2F tasks. In general, we find that the performance ceiling of LoRA is relatively low, even if we have carefully tuned its hyperparameters. As a comparison, the performance of our OFT framework has not yet saturated, since we empirically find that it still gets better as the number of trainable parameters gets large. We emphasize that our quantitative evaluation in controllable generation is one of our novel contributions, since it can accurately evaluate the control performance of the finetuned models (up to the accuracy of the off-the-shelf segmentation/detection model).

Report issue for preceding element

![Refer to caption](x10.png)


Figure 10: Qualitative comparison of controllable generation. The figure is best viewed digitally, in color and significantly zoomed in.

Report issue for preceding element


|  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Task | Metric | SD | ControlNet | T2I-Adapter | LoRA | COFT | OFT |
| C2I | IoU ↑↑\uparrow↑ | 0.049 | 0.189 | 0.078 | 0.168 | 0.195 | 0.193 |
| F1 ↑↑\uparrow↑ | 0.093 | 0.317 | 0.143 | 0.286 | 0.325 | 0.323 |
| S2I | mIoU ↑↑\uparrow↑ | 7.72 | 20.88 | 16.38 | 22.98 | 26.92 | 27.06 |
| mAcc ↑↑\uparrow↑ | 14.40 | 30.91 | 26.31 | 35.52 | 40.08 | 40.09 |
| aAcc ↑↑\uparrow↑ | 33.61 | 61.42 | 51.63 | 58.03 | 62.96 | 62.42 |
| L2F | Error ↓↓\downarrow↓ | 146.19 | 7.61 | 23.75 | 7.68 | 6.92 | 7.07 |

Table 2: Quantitative comparison of control signal consistency for three control tasks (Canny edge to image, segmentation to image and landmark to face).

Report issue for preceding element

Qualitative comparison. We also qualitatively compare OFT and COFT to current state-of-the-art methods, including ControlNet, T2I-Adapter and LoRA. Randomly generated images in Figure [10](https://arxiv.org/html/2306.07280v3#S5.F10 "Figure 10 ‣ 5.2 Controllable Generation ‣ 5 Experiments and Results ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning") show that OFT and COFT not only yield high-fidelity and realistic image quality, but also achieve accurate control. In the S2I task, we can see that LoRA completely fails to generate images following the input segmentation map, while ControlNet, OFT and COFT can well control the generated images. In contrast to ControlNet, both OFT and COFT are able to generate high-fidelity images with more vivid details and more reasonable geometric structures with far less model parameters. In the C2I task, both OFT and COFT are able to hallucinate semantically similar images based on a rough Canny edges, while T2I-Adapter and LoRA perform much worse. In the L2F task, our method produces the most accurate pose control for the generated faces even under challenging face poses. In all three control tasks, we show that both OFT and COFT produce qualitatively better images than the state-of-the-art baselines, demonstrating the effectiveness of our OFT framework in controllable generation. To give a more comprehensive qualitative comparison, we provide more qualitative examples for all the three control tasks in Appendix [F.2](https://arxiv.org/html/2306.07280v3#A6.SS2 "F.2 Controllable Generation ‣ Appendix F More Qualitative Results ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning"), and moreover, we demonstrate OFT can perform well on more control tasks (including dense pose to human body, sketch to image and depth to image) in Appendix [G](https://arxiv.org/html/2306.07280v3#A7 "Appendix G More Controllable Generation Tasks ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning").

Report issue for preceding element

### 6 Concluding Remarks and Open Problems

Report issue for preceding element

Motivated by the observation that angular information among neurons crucially determines visual semantics, we propose a simple yet effective finetuning method – orthogonal finetuning for controlling text-to-image diffusion models. Specifically, we target two text-to-image applications: subject-driven generation and controllable generation. Compared to existing methods, OFT demonstrates stronger controllability and finetuning stability with fewer number of finetuning parameters. More importantly, OFT does not introduce additional inference overhead, leading to an efficient deployable model.

Report issue for preceding element

OFT also introduces a few interesting open problems. First, OFT guarantees the orthogonality via Cayley parametrization which involves a matrix inverse. It slightly limits the scalability of OFT. Although we address this limitation using block diagonal parametrization, how to speed up this matrix inverse in a differentiable way remains a challenge. Second, OFT has unique potential in compositionality, in the sense that the orthogonal matrices produced by multiple OFT finetuning tasks can be multiplied together and remains an orthogonal matrix. Whether this set of orthogonal matrices preserve the knowledge of all the downstream tasks remains an interesting direction to study. Finally, the parameter efficiency of OFT is largely dependent on the block diagonal structure which inevitably introduces additional biases and limits the flexibility. How to improve the parameter efficiency in a more effective and less biased way remains an important open problem.

Report issue for preceding element

### Acknowledgement

Report issue for preceding element

The authors would like to sincerely thank Luigi Gresele, Yandong Wen, Yuliang Xiu and many other colleagues at Max Planck Institute for Intelligent Systems for many helpful suggestions.

Report issue for preceding element

This work was supported by the German Federal Ministry of Education and Research (BMBF): Tubingen AI Center, FKZ: 01IS18039B, and by the Machine Learning Cluster of Excellence, EXC number 2064/1 – Project number 390727645. WL was supported by the German Research Foundation (DFG): SFB 1233, Robust Vision: Inference Principles and Neural Mechanisms, TP XX, project number: 276693517. AW acknowledges support from a Turing AI Fellowship under grant EP/V025279/1, The Alan Turing Institute, and the Leverhulme Trust via CFI.

Report issue for preceding element

### References

Report issue for preceding element

* [1]↑

  Jean-Baptiste Alayrac, Jeff Donahue, Pauline Luc, Antoine Miech, Iain Barr,
  Yana Hasson, Karel Lenc, Arthur Mensch, Katherine Millican, Malcolm Reynolds,
  et al.
  Flamingo: a visual language model for few-shot learning.
  In NeurIPS, 2022.
* [2]↑

  Omri Avrahami, Ohad Fried, and Dani Lischinski.
  Blended latent diffusion.
  arXiv preprint arXiv:2206.02779, 2022.
* [3]↑

  Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla
  Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell,
  et al.
  Language models are few-shot learners.
  In NeurIPS, 2020.
* [4]↑

  Adrian Bulat and Georgios Tzimiropoulos.
  How far are we from solving the 2d & 3d face alignment problem? (and
  a dataset of 230,000 3d facial landmarks).
  In ICCV, 2017.
* [5]↑

  Mathilde Caron, Hugo Touvron, Ishan Misra, Hervé Jégou, Julien Mairal,
  Piotr Bojanowski, and Armand Joulin.
  Emerging properties in self-supervised vision transformers.
  In ICCV, 2021.
* [6]↑

  Arantxa Casanova, Marlene Careil, Jakob Verbeek, Michal Drozdzal, and Adriana
  Romero Soriano.
  Instance-conditioned gan.
  In NeurIPS, 2021.
* [7]↑

  Beidi Chen, Weiyang Liu, Zhiding Yu, Jan Kautz, Anshumali Shrivastava, Animesh
  Garg, and Animashree Anandkumar.
  Angular visual hardness.
  In ICML, 2020.
* [8]↑

  Jooyoung Choi, Sungwon Kim, Yonghyun Jeong, Youngjune Gwon, and Sungroh Yoon.
  Ilvr: Conditioning method for denoising diffusion probabilistic
  models.
  In ICCV, 2021.
* [9]↑

  Yunjey Choi, Minje Choi, Munyoung Kim, Jung-Woo Ha, Sunghun Kim, and Jaegul
  Choo.
  Stargan: Unified generative adversarial networks for multi-domain
  image-to-image translation.
  In CVPR, 2018.
* [10]↑

  François Chollet.
  Xception: Deep learning with depthwise separable convolutions.
  In CVPR, 2017.
* [11]↑

  Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova.
  Bert: Pre-training of deep bidirectional transformers for language
  understanding.
  arXiv preprint arXiv:1810.04805, 2018.
* [12]↑

  Prafulla Dhariwal and Alexander Nichol.
  Diffusion models beat gans on image synthesis.
  In NeurIPS, 2021.
* [13]↑

  Ming Ding, Zhuoyi Yang, Wenyi Hong, Wendi Zheng, Chang Zhou, Da Yin, Junyang
  Lin, Xu Zou, Zhou Shao, Hongxia Yang, et al.
  Cogview: Mastering text-to-image generation via transformers.
  In NeurIPS, 2021.
* [14]↑

  Patrick Esser, Robin Rombach, and Bjorn Ommer.
  Taming transformers for high-resolution image synthesis.
  In CVPR, 2021.
* [15]↑

  Rinon Gal, Yuval Alaluf, Yuval Atzmon, Or Patashnik, Amit H Bermano, Gal
  Chechik, and Daniel Cohen-Or.
  An image is worth one word: Personalizing text-to-image generation
  using textual inversion.
  arXiv preprint arXiv:2208.01618, 2022.
* [16]↑

  Shuyang Gu, Dong Chen, Jianmin Bao, Fang Wen, Bo Zhang, Dongdong Chen, Lu Yuan,
  and Baining Guo.
  Vector quantized diffusion model for text-to-image synthesis.
  In CVPR, 2022.
* [17]↑

  Kaiming He, Xinlei Chen, Saining Xie, Yanghao Li, Piotr Dollár, and Ross
  Girshick.
  Masked autoencoders are scalable vision learners.
  In CVPR, 2022.
* [18]↑

  Amir Hertz, Ron Mokady, Jay Tenenbaum, Kfir Aberman, Yael Pritch, and Daniel
  Cohen-Or.
  Prompt-to-prompt image editing with cross attention control.
  arXiv preprint arXiv:2208.01626, 2022.
* [19]↑

  Martin Heusel, Hubert Ramsauer, Thomas Unterthiner, Bernhard Nessler, and Sepp
  Hochreiter.
  Gans trained by a two time-scale update rule converge to a local nash
  equilibrium.
  In NeurIPS, 2017.
* [20]↑

  Jonathan Ho, Ajay Jain, and Pieter Abbeel.
  Denoising diffusion probabilistic models.
  In NeurIPS, 2020.
* [21]↑

  Neil Houlsby, Andrei Giurgiu, Stanislaw Jastrzebski, Bruna Morrone, Quentin
  De Laroussilhe, Andrea Gesmundo, Mona Attariyan, and Sylvain Gelly.
  Parameter-efficient transfer learning for nlp.
  In ICML, 2019.
* [22]↑

  Edward J Hu, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang,
  Weizhu Chen, et al.
  Lora: Low-rank adaptation of large language models.
  In ICLR, 2022.
* [23]↑

  Phillip Isola, Jun-Yan Zhu, Tinghui Zhou, and Alexei A Efros.
  Image-to-image translation with conditional adversarial networks.
  In CVPR, 2017.
* [24]↑

  Yuming Jiang, Shuai Yang, Haonan Qiu, Wayne Wu, Chen Change Loy, and Ziwei Liu.
  Text2human: Text-driven controllable human image generation.
  ACM Transactions on Graphics (TOG), 41(4):1–11, 2022.
* [25]↑

  Tero Karras, Timo Aila, Samuli Laine, and Jaakko Lehtinen.
  Progressive growing of gans for improved quality, stability, and
  variation.
  In ICLR, 2018.
* [26]↑

  Mario Lezcano-Casado and David Martınez-Rubio.
  Cheap orthogonal constraints in neural networks: A simple
  parametrization of the orthogonal and unitary group.
  In ICML, 2019.
* [27]↑

  Bowen Li, Xiaojuan Qi, Thomas Lukasiewicz, and Philip Torr.
  Controllable text-to-image generation.
  In NeurIPS, 2019.
* [28]↑

  Junnan Li, Dongxu Li, Silvio Savarese, and Steven Hoi.
  Blip-2: Bootstrapping language-image pre-training with frozen image
  encoders and large language models.
  arXiv preprint arXiv:2301.12597, 2023.
* [29]↑

  Junnan Li, Dongxu Li, Caiming Xiong, and Steven Hoi.
  Blip: Bootstrapping language-image pre-training for unified
  vision-language understanding and generation.
  In ICML, 2022.
* [30]↑

  Rongmei Lin, Weiyang Liu, Zhen Liu, Chen Feng, Zhiding Yu, James M Rehg,
  Li Xiong, and Le Song.
  Regularizing neural networks via minimizing hyperspherical energy.
  In CVPR, 2020.
* [31]↑

  Tsung-Yi Lin, Michael Maire, Serge Belongie, James Hays, Pietro Perona, Deva
  Ramanan, Piotr Dollár, and C Lawrence Zitnick.
  Microsoft coco: Common objects in context.
  In ECCV, 2014.
* [32]↑

  Weiyang Liu, Rongmei Lin, Zhen Liu, Lixin Liu, Zhiding Yu, Bo Dai, and Le Song.
  Learning towards minimum hyperspherical energy.
  In NeurIPS, 2018.
* [33]↑

  Weiyang Liu, Rongmei Lin, Zhen Liu, James M Rehg, Liam Paull, Li Xiong,
  Le Song, and Adrian Weller.
  Orthogonal over-parameterized training.
  In CVPR, 2021.
* [34]↑

  Weiyang Liu, Rongmei Lin, Zhen Liu, Li Xiong, Bernhard Schölkopf, and
  Adrian Weller.
  Learning with hyperspherical uniformity.
  In AISTATS, 2021.
* [35]↑

  Weiyang Liu, Zhen Liu, Zhiding Yu, Bo Dai, Rongmei Lin, Yisen Wang, James M
  Rehg, and Le Song.
  Decoupled networks.
  In CVPR, 2018.
* [36]↑

  Weiyang Liu, Yan-Ming Zhang, Xingguo Li, Zhiding Yu, Bo Dai, Tuo Zhao, and
  Le Song.
  Deep hyperspherical learning.
  In NIPS, 2017.
* [37]↑

  Jiasen Lu, Dhruv Batra, Devi Parikh, and Stefan Lee.
  Vilbert: Pretraining task-agnostic visiolinguistic representations
  for vision-and-language tasks.
  In NeurIPS, 2019.
* [38]↑

  Chong Mou, Xintao Wang, Liangbin Xie, Jian Zhang, Zhongang Qi, Ying Shan, and
  Xiaohu Qie.
  T2i-adapter: Learning adapters to dig out more controllable ability
  for text-to-image diffusion models.
  arXiv preprint arXiv:2302.08453, 2023.
* [39]↑

  Alexander Quinn Nichol, Prafulla Dhariwal, Aditya Ramesh, Pranav Shyam, Pamela
  Mishkin, Bob Mcgrew, Ilya Sutskever, and Mark Chen.
  Glide: Towards photorealistic image generation and editing with
  text-guided diffusion models.
  In ICML, 2022.
* [40]↑

  Maria-Elena Nilsback and Andrew Zisserman.
  Automated flower classification over a large number of classes.
  In Indian Conference on Computer Vision, Graphics & Image
  Processing, 2008.
* [41]↑

  Yotam Nitzan, Kfir Aberman, Qiurui He, Orly Liba, Michal Yarom, Yossi
  Gandelsman, Inbar Mosseri, Yael Pritch, and Daniel Cohen-Or.
  Mystyle: A personalized generative prior.
  ACM Transactions on Graphics (TOG), 41(6):1–10, 2022.
* [42]↑

  Taesung Park, Ming-Yu Liu, Ting-Chun Wang, and Jun-Yan Zhu.
  Semantic image synthesis with spatially-adaptive normalization.
  In CVPR, 2019.
* [43]↑

  Jonas Pfeiffer, Aishwarya Kamath, Andreas Rücklé, Kyunghyun Cho, and
  Iryna Gurevych.
  Adapterfusion: Non-destructive task composition for transfer
  learning.
  arXiv preprint arXiv:2005.00247, 2020.
* [44]↑

  Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh,
  Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark,
  et al.
  Learning transferable visual models from natural language
  supervision.
  In ICML, 2021.
* [45]↑

  Aditya Ramesh, Prafulla Dhariwal, Alex Nichol, Casey Chu, and Mark Chen.
  Hierarchical text-conditional image generation with clip latents.
  arXiv preprint arXiv:2204.06125, 2022.
* [46]↑

  Aditya Ramesh, Mikhail Pavlov, Gabriel Goh, Scott Gray, Chelsea Voss, Alec
  Radford, Mark Chen, and Ilya Sutskever.
  Zero-shot text-to-image generation.
  In ICML, 2021.
* [47]↑

  René Ranftl, Katrin Lasinger, David Hafner, Konrad Schindler, and Vladlen
  Koltun.
  Towards robust monocular depth estimation: Mixing datasets for
  zero-shot cross-dataset transfer.
  IEEE transactions on pattern analysis and machine intelligence,
  44(3):1623–1637, 2020.
* [48]↑

  Scott Reed, Zeynep Akata, Xinchen Yan, Lajanugen Logeswaran, Bernt Schiele, and
  Honglak Lee.
  Generative adversarial text to image synthesis.
  In ICML, 2016.
* [49]↑

  Daniel Roich, Ron Mokady, Amit H Bermano, and Daniel Cohen-Or.
  Pivotal tuning for latent-based editing of real images.
  ACM Transactions on Graphics, 42(1):1–13, 2022.
* [50]↑

  Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, and Björn
  Ommer.
  High-resolution image synthesis with latent diffusion models.
  In CVPR, 2022.
* [51]↑

  Nataniel Ruiz, Yuanzhen Li, Varun Jampani, Yael Pritch, Michael Rubinstein, and
  Kfir Aberman.
  Dreambooth: Fine tuning text-to-image diffusion models for
  subject-driven generation.
  In CVPR, 2023.
* [52]↑

  Chitwan Saharia, William Chan, Huiwen Chang, Chris Lee, Jonathan Ho, Tim
  Salimans, David Fleet, and Mohammad Norouzi.
  Palette: Image-to-image diffusion models.
  In SIGGRAPH 2022, pages 1–10, 2022.
* [53]↑

  Chitwan Saharia, William Chan, Saurabh Saxena, Lala Li, Jay Whang, Emily L
  Denton, Kamyar Ghasemipour, Raphael Gontijo Lopes, Burcu Karagol Ayan, Tim
  Salimans, et al.
  Photorealistic text-to-image diffusion models with deep language
  understanding.
  In NeurIPS, 2022.
* [54]↑

  Christoph Schuhmann, Romain Beaumont, Richard Vencu, Cade Gordon, Ross
  Wightman, Mehdi Cherti, Theo Coombes, Aarush Katta, Clayton Mullis, Mitchell
  Wortsman, et al.
  Laion-5b: An open large-scale dataset for training next generation
  image-text models.
  arXiv preprint arXiv:2210.08402, 2022.
* [55]↑

  Jiaming Song, Chenlin Meng, and Stefano Ermon.
  Denoising diffusion implicit models.
  In ICLR, 2021.
* [56]↑

  Yang Song, Jascha Sohl-Dickstein, Diederik P Kingma, Abhishek Kumar, Stefano
  Ermon, and Ben Poole.
  Score-based generative modeling through stochastic differential
  equations.
  In ICLR, 2021.
* [57]↑

  Weijie Su, Xizhou Zhu, Yue Cao, Bin Li, Lewei Lu, Furu Wei, and Jifeng Dai.
  Vl-bert: Pre-training of generic visual-linguistic representations.
  In ICLR, 2020.
* [58]↑

  Andrey Voynov, Kfir Aberman, and Daniel Cohen-Or.
  Sketch-guided text-to-image diffusion models.
  arXiv preprint arXiv:2211.13752, 2022.
* [59]↑

  Tengfei Wang, Ting Zhang, Bo Zhang, Hao Ouyang, Dong Chen, Qifeng Chen, and
  Fang Wen.
  Pretraining is all you need for image-to-image translation.
  arXiv preprint arXiv:2205.12952, 2022.
* [60]↑

  Ting-Chun Wang, Ming-Yu Liu, Jun-Yan Zhu, Andrew Tao, Jan Kautz, and Bryan
  Catanzaro.
  High-resolution image synthesis and semantic manipulation with
  conditional gans.
  In CVPR, 2018.
* [61]↑

  Zirui Wang, Jiahui Yu, Adams Wei Yu, Zihang Dai, Yulia Tsvetkov, and Yuan Cao.
  Simvlm: Simple visual language model pretraining with weak
  supervision.
  arXiv preprint arXiv:2108.10904, 2021.
* [62]↑

  Chenfei Wu, Jian Liang, Lei Ji, Fan Yang, Yuejian Fang, Daxin Jiang, and Nan
  Duan.
  Nüwa: Visual synthesis pre-training for neural visual world
  creation.
  In ECCV, 2022.
* [63]↑

  Weihao Xia, Yujiu Yang, Jing-Hao Xue, and Baoyuan Wu.
  Tedigan: Text-guided diverse face image generation and manipulation.
  In CVPR, 2021.
* [64]↑

  Enze Xie, Wenhai Wang, Zhiding Yu, Anima Anandkumar, Jose M Alvarez, and Ping
  Luo.
  Segformer: Simple and efficient design for semantic segmentation with
  transformers.
  In NeurIPS, 2021.
* [65]↑

  Tao Xu, Pengchuan Zhang, Qiuyuan Huang, Han Zhang, Zhe Gan, Xiaolei Huang, and
  Xiaodong He.
  Attngan: Fine-grained text to image generation with attentional
  generative adversarial networks.
  In CVPR, 2018.
* [66]↑

  Jiahui Yu, Yuanzhong Xu, Jing Yu Koh, Thang Luong, Gunjan Baid, Zirui Wang,
  Vijay Vasudevan, Alexander Ku, Yinfei Yang, Burcu Karagol Ayan, et al.
  Scaling autoregressive models for content-rich text-to-image
  generation.
  Transactions on Machine Learning Research, 2022.
* [67]↑

  Han Zhang, Tao Xu, Hongsheng Li, Shaoting Zhang, Xiaogang Wang, Xiaolei Huang,
  and Dimitris N Metaxas.
  Stackgan: Text to photo-realistic image synthesis with stacked
  generative adversarial networks.
  In ICCV, 2017.
* [68]↑

  Lvmin Zhang and Maneesh Agrawala.
  Adding conditional control to text-to-image diffusion models.
  arXiv preprint arXiv:2302.05543, 2023.
* [69]↑

  Richard Zhang, Phillip Isola, Alexei A Efros, Eli Shechtman, and Oliver Wang.
  The unreasonable effectiveness of deep features as a perceptual
  metric.
  In CVPR, 2018.
* [70]↑

  Bolei Zhou, Hang Zhao, Xavier Puig, Sanja Fidler, Adela Barriuso, and Antonio
  Torralba.
  Scene parsing through ade20k dataset.
  In CVPR, 2017.
* [71]↑

  Jun-Yan Zhu, Richard Zhang, Deepak Pathak, Trevor Darrell, Alexei A Efros,
  Oliver Wang, and Eli Shechtman.
  Toward multimodal image-to-image translation.
  In NeurIPS, 2017.

## Appendix

Report issue for preceding element
\parttoc

### Appendix A Experimental Details

Report issue for preceding element

To verify the effectiveness of our Orthogonal Fine-tuning (OFT) method, we extensively evaluate the performance of our method in two common text-to-image generation tasks: subject-driven generation and controllable generation. More specifically, we use the exact same task setting as ControlNet [[68](https://arxiv.org/html/2306.07280v3#bib.bib68)] and Dreambooth [[51](https://arxiv.org/html/2306.07280v3#bib.bib51)] and the baseline implementations were sourced from the GitHub repository Diffusers222<https://github.com/huggingface/diffusers> and ControlNet333<https://github.com/lllyasviel/ControlNet>.

Report issue for preceding element

###### Data and Model.

Report issue for preceding element

For training the convolutional autoencoder from Figure [2](https://arxiv.org/html/2306.07280v3#S3.F2 "Figure 2 ‣ 3.1 Why Does Orthogonal Transformation Make Sense? ‣ 3 Orthogonal Finetuning ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning"), we use 1000 random images from the Oxford 102 Flower dataset [[40](https://arxiv.org/html/2306.07280v3#bib.bib40)]. For the task of subject-driven generation, we use the official DreamBooth dataset, which consists of 30 subjects from 15 different classes. For each subject, there are several images and 25 different text prompts. For generating the image-control-caption combinations, we use BLIP [[29](https://arxiv.org/html/2306.07280v3#bib.bib29)] to automatically caption the images (pre-trained model weight and code for captioning based on the GitHub repository BLIP444<https://github.com/salesforce/BLIP>). Note, although COCO provides captions for the training and validation split, to be consistent with other image-control-caption combinations, we instead use the BLIP-generated captions as text prompts. For the C2I task, we use the whole COCO 2017 dataset [[31](https://arxiv.org/html/2306.07280v3#bib.bib31)] with in total of 180K images; we generate canny edge images as the control signal using the same canny edge detector as ControlNet. For the S2I task, we use the semantic segmentation dataset ADE20K [[70](https://arxiv.org/html/2306.07280v3#bib.bib70)] with in total of 24K image-segmentation mask pairs. For the L2F dataset, we use the CelebA-HQ dataset [[25](https://arxiv.org/html/2306.07280v3#bib.bib25)], which contains 30K images. Additionally, we demonstrate that OFT also works well in other controllable generation tasks, including depth-to-image (D2I), densepose-to-image (P2I), and sketch-to-image (Sk2I). For the D2I task, we also use the COCO dataset and employ MiDaS [[47](https://arxiv.org/html/2306.07280v3#bib.bib47)] to generate depth maps; the pre-trained weights are obtained from the GitHub repository MiDaS555<https://github.com/isl-org/MiDaS>. For the P2I task, we use the DeepFashion-MultiModal dataset [[24](https://arxiv.org/html/2306.07280v3#bib.bib24)] with in total of 44K clothed human images with the corresponding densepose. For the Sk2I task, we use a subset of the LAION-Aesthetics dataset with approximately 350K images to learn sketch-guided image generation. We use the Stable Diffusion v1.5666<https://huggingface.co/runwayml/stable-diffusion-v1-5/blob/main/v1-5-pruned.ckpt> as the base model.

Report issue for preceding element

###### Subject-driven generation.

Report issue for preceding element

For training our subject-driven generation diffusion model, we follow the training objective of Dreambooth. More specifically, we use the class-specific prior preservation loss to fine-tune our orthogonal matrices:

Report issue for preceding element

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝔼𝒙,𝒄,ϵ,ϵ′,t⁢[wt⁢‖𝒙^θ⁢(αt⁢𝒙+σt⁢ϵ,𝒄)−𝒙‖22+λ⁢wt′⁢‖𝒙^θ⁢(αt′⁢𝒙pr+σt′⁢ϵ′,𝒄pr)−𝒙pr‖22],subscript𝔼  𝒙𝒄bold-italic-ϵsuperscriptbold-italic-ϵ′𝑡delimited-[]subscript𝑤𝑡subscriptsuperscriptnormsubscript^𝒙𝜃subscript𝛼𝑡𝒙subscript𝜎𝑡bold-italic-ϵ𝒄𝒙22𝜆subscript𝑤superscript𝑡′subscriptsuperscriptnormsubscript^𝒙𝜃subscript𝛼superscript𝑡′subscript𝒙prsubscript𝜎superscript𝑡′superscriptbold-italic-ϵ′subscript𝒄prsubscript𝒙pr22\mathbb{E}\_{\bm{x},\bm{c},\bm{\epsilon},\bm{\epsilon}^{\prime},t}[w\_{t}\|\hat{% \bm{x}}\_{\theta}(\alpha\_{t}\bm{x}+\sigma\_{t}\bm{\epsilon},\bm{c})-\bm{x}\|^{2}% \_{2}+\lambda w\_{t^{\prime}}\|\hat{\bm{x}}\_{\theta}(\alpha\_{t^{\prime}}\bm{x}\_{% \text{pr}}+\sigma\_{t^{\prime}}\bm{\epsilon}^{\prime},\bm{c}\_{\text{pr}})-\bm{x% }\_{\text{pr}}\|^{2}\_{2}],blackboard\_E start\_POSTSUBSCRIPT bold\_italic\_x , bold\_italic\_c , bold\_italic\_ϵ , bold\_italic\_ϵ start\_POSTSUPERSCRIPT ′ end\_POSTSUPERSCRIPT , italic\_t end\_POSTSUBSCRIPT [ italic\_w start\_POSTSUBSCRIPT italic\_t end\_POSTSUBSCRIPT ∥ over^ start\_ARG bold\_italic\_x end\_ARG start\_POSTSUBSCRIPT italic\_θ end\_POSTSUBSCRIPT ( italic\_α start\_POSTSUBSCRIPT italic\_t end\_POSTSUBSCRIPT bold\_italic\_x + italic\_σ start\_POSTSUBSCRIPT italic\_t end\_POSTSUBSCRIPT bold\_italic\_ϵ , bold\_italic\_c ) - bold\_italic\_x ∥ start\_POSTSUPERSCRIPT 2 end\_POSTSUPERSCRIPT start\_POSTSUBSCRIPT 2 end\_POSTSUBSCRIPT + italic\_λ italic\_w start\_POSTSUBSCRIPT italic\_t start\_POSTSUPERSCRIPT ′ end\_POSTSUPERSCRIPT end\_POSTSUBSCRIPT ∥ over^ start\_ARG bold\_italic\_x end\_ARG start\_POSTSUBSCRIPT italic\_θ end\_POSTSUBSCRIPT ( italic\_α start\_POSTSUBSCRIPT italic\_t start\_POSTSUPERSCRIPT ′ end\_POSTSUPERSCRIPT end\_POSTSUBSCRIPT bold\_italic\_x start\_POSTSUBSCRIPT pr end\_POSTSUBSCRIPT + italic\_σ start\_POSTSUBSCRIPT italic\_t start\_POSTSUPERSCRIPT ′ end\_POSTSUPERSCRIPT end\_POSTSUBSCRIPT bold\_italic\_ϵ start\_POSTSUPERSCRIPT ′ end\_POSTSUPERSCRIPT , bold\_italic\_c start\_POSTSUBSCRIPT pr end\_POSTSUBSCRIPT ) - bold\_italic\_x start\_POSTSUBSCRIPT pr end\_POSTSUBSCRIPT ∥ start\_POSTSUPERSCRIPT 2 end\_POSTSUPERSCRIPT start\_POSTSUBSCRIPT 2 end\_POSTSUBSCRIPT ] , |  | (5) |

with 𝒄prsubscript𝒄pr\bm{c}\_{\text{pr}}bold\_italic\_c start\_POSTSUBSCRIPT pr end\_POSTSUBSCRIPT being the class conditioning vector. For calculating the prior-preservation loss, we additionally need to generate 200 images using the subject’s class prompt. Similar to LoRA, we inject our trainable orthogonal matrices into the attention modules of the stable diffusion model. To be comparable with LoRA, we choose the exact same linear layers as LoRA to affect upon: the linear layers 𝑾qsubscript𝑾𝑞\bm{W}\_{q}bold\_italic\_W start\_POSTSUBSCRIPT italic\_q end\_POSTSUBSCRIPT, 𝑾ksubscript𝑾𝑘\bm{W}\_{k}bold\_italic\_W start\_POSTSUBSCRIPT italic\_k end\_POSTSUBSCRIPT, 𝑾vsubscript𝑾𝑣\bm{W}\_{v}bold\_italic\_W start\_POSTSUBSCRIPT italic\_v end\_POSTSUBSCRIPT and 𝑾osubscript𝑾𝑜\bm{W}\_{o}bold\_italic\_W start\_POSTSUBSCRIPT italic\_o end\_POSTSUBSCRIPT. We perform training on 1 Tesla V100-SXM2-32GB GPU using a learning rate of 6×10−56superscript1056\times 10^{-5}6 × 10 start\_POSTSUPERSCRIPT - 5 end\_POSTSUPERSCRIPT, batch size of 1, and train for approximately 1000 iterations. In the case of COFT, we use ϵ=6×10−5italic-ϵ6superscript105\epsilon=6\times 10^{-5}italic\_ϵ = 6 × 10 start\_POSTSUPERSCRIPT - 5 end\_POSTSUPERSCRIPT to constrain the orthogonal matrices.

Report issue for preceding element

###### Controllable generation.

Report issue for preceding element

Apart from injecting the trainable OFT weights into the stable diffusion model, we need to add a small encoding model to stable diffusion to encode the control signal. To be comparable with ControlNet [[68](https://arxiv.org/html/2306.07280v3#bib.bib68)], we use the same encoding module, which is a shallow 8-layer convolutional network with Scaled Exponential Linear Unit (SELU) activation functions. We also the same training objective as ControlNet. The control signal is encoded and concatenated once with the input to the stable diffusion U-Net. For the LoRA baseline, we use the same encoding module to encode the control signal. For S2I, L2I and P2I, we fine-tune the model for 20 epochs; for C2I and D2I we fine-tune the model for 10 epochs; for Sk2I we fine-tune the model for 8888 epochs. We perform training on 4444 NVIDIA A100-SXM4-80GB GPUs using a learning rate of 1×10−51superscript1051\times 10^{-5}1 × 10 start\_POSTSUPERSCRIPT - 5 end\_POSTSUPERSCRIPT, batch size of 4444 for L2I and batch size of 16161616 for the rest of tasks. For fine-tuning with COFT, we use ϵ=1×10−3italic-ϵ1superscript103\epsilon=1\times 10^{-3}italic\_ϵ = 1 × 10 start\_POSTSUPERSCRIPT - 3 end\_POSTSUPERSCRIPT.

Report issue for preceding element

###### Evaluation.

Report issue for preceding element

When evaluating the effectiveness of controllable generation, we primarily focus on evaluating the controllability. Using the consistency metrics introduced in the main paper, we can effectively compute the difference between the control signal and the generated image. For the C2I task, we apply the identical canny filter on the generated image to determine a canny image of the predicted image. Both the control signal canny image and the canny image obtained from the generated images are black-and-white images, with pixel values being either 0 or 1. We evaluate the pixel-wise Intersection over Union (IoU) and F1 score between these two canny predictions. For the S2I task, we compute mean IoU, mean and overall accuracy by deploying a pre-trained semantic segmentation model. More specifically, we use the Segformer777<https://github.com/NVlabs/SegFormer> [[64](https://arxiv.org/html/2306.07280v3#bib.bib64)] model, which is trained on ADE20K (Segformer-B4), to perform semantic segmentation on our generated images. We use the segmentation accuracy as an indication for the overall semantically and structural resemblance of the generated images to the ground truth image.
For the L2F task, we compute the mean ℓ2subscriptℓ2\ell\_{2}roman\_ℓ start\_POSTSUBSCRIPT 2 end\_POSTSUBSCRIPT distance between the input control landmarks and the landmarks estimated from generated images using facial landmark detector [[4](https://arxiv.org/html/2306.07280v3#bib.bib4)].

Report issue for preceding element

We also evaluate the generation performance by calculating Fréchet Inception Distance (FID) [[19](https://arxiv.org/html/2306.07280v3#bib.bib19)], we use the default setting of the GitHub repository pytorch-fid888<https://github.com/mseitzer/pytorch-fid>. The FID is a metric quantifying the similarity between two image dataset. It utilizes 2048-dimensional features, which are derived from the final average pooling layer of a pretrained InceptionV3 network trained on ImageNet dataset. A lower FID score indicates a higher similarity between the datasets.

Report issue for preceding element

### Appendix B Effect of Different Number of Diagonal Blocks

Report issue for preceding element

We note that the number of diagonal blocks r𝑟ritalic\_r is an important hyperparameter that effectively controls the number of trainable parameters. It is necessary to perform a sensitivity study on this hyperparameter. Following the same settings as the main paper, we evaluate how r𝑟ritalic\_r affects OFT in the S2I task. Results in Table [3](https://arxiv.org/html/2306.07280v3#A2.T3 "Table 3 ‣ Appendix B Effect of Different Number of Diagonal Blocks ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning") show that smaller r𝑟ritalic\_r (closer to recovering the standard orthogonal matrix) generally works better than larger r𝑟ritalic\_r. However, we find that a good trade-off between flexibility and parameter-efficiency indeed exists. Empirically, we find that we can use a much bigger r𝑟ritalic\_r if the dataset is simple, leading to better parameter-efficiency and faster convergence. In the main paper, we always use r=4𝑟4r=4italic\_r = 4 because we find that r=4𝑟4r=4italic\_r = 4 works well across datasets and tasks. Note that, in terms of the number of inference parameters, both LoRA and OFT have the exact same number of parameters, which is equal to the number of parameters of the underlying stable diffusion model, while ControlNet has an additional control model with 361M parameters.

Report issue for preceding element

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  | ControlNet | r=2𝑟2r=2italic\_r = 2 | r=4𝑟4r=4italic\_r = 4 | r=8𝑟8r=8italic\_r = 8 | r=16𝑟16r=16italic\_r = 16 |
| Trainable Parameters | 361.3 M | 29.5 M | 16.3 M | 9.7 M | 6.4 M |
| Inference Parameters | 1.42 B | 1.06 B | 1.06 B | 1.06 B | 1.06 B |
| mIoU ↑↑\uparrow↑ | 20.88 | 27.18 | 27.06 | 24.09 | 21.0 |
| mAcc ↑↑\uparrow↑ | 30.91 | 39.39 | 40.09 | 36.95 | 32.55 |
| aAcc ↑↑\uparrow↑ | 61.42 | 65.24 | 62.96 | 60.25 | 55.5 |

Table 3: How the number of diagonal blocks affects the control capability of OFT.

Report issue for preceding element

### Appendix C Experiments on Re-scaled OFT

Report issue for preceding element

Since both OFT and COFT transform neurons with orthogonal matrices and do not affect the magnitude of neurons, their magnitude may be sub-optimal with their updated orientations. To address this issue, we propose a re-scaled OFT where the neuron magnitude is refined using the same set of data in the downstream task. Specifically, re-scaled OFT further finetunes the magnitude of neurons without changing their directions. re-scaled OFT can be performed in two manners: (1) *joint fitting*: magnitude fitting can be used simultaneously with OFT or COFT, and (2) *Post-stage fitting*: magnitude fitting can be used after OFT or COFT is finished. An important motivation for re-scaled OFT comes from Figure [2](https://arxiv.org/html/2306.07280v3#S3.F2 "Figure 2 ‣ 3.1 Why Does Orthogonal Transformation Make Sense? ‣ 3 Orthogonal Finetuning ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning"), where we observe that constructing images only with angular information perfectly preserves visual structures, but it also results in a certain degree of color distortion. We hypothesize that this minor color distortion is caused by magnitude loss and fixing this issue can potentially improve the visual quality of generated images.

Report issue for preceding element

Notably, re-scaled OFT does not change the hyperspherical energy since it does not change the direction of neurons - all the nice properties of OFT and COFT on hyperspherical energy are still perfectly preserved. Therefore, the advantage of structural preservation is also inherited.

Report issue for preceding element

To simplify the experiments and validate the effectiveness of re-scaled OFT, we perform post-stage magnitude fitting on the COFT model and compare the FID between the original validation images and the generated images (using the control signals extracted from validation images). The reason we use FID here is that FID is more sensitive to color distortion, while the consistency metric only measures the structural preservation. Table [4](https://arxiv.org/html/2306.07280v3#A3.T4 "Table 4 ‣ Appendix C Experiments on Re-scaled OFT ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning") shows that magnitude fitting can indeed improve the FID of COFT and is beneficial to COFT.

Report issue for preceding element

Magnitude fitting is lightweight and can be implemented easily by simply adding one trainable parameter for each layer we modify; the parameter has the shape of (N×1𝑁1N\times 1italic\_N × 1), with N𝑁Nitalic\_N corresponds to the number of neurons in that specific layer. The performance gain illustrated in Table [4](https://arxiv.org/html/2306.07280v3#A3.T4 "Table 4 ‣ Appendix C Experiments on Re-scaled OFT ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning") is achieved by performing *Post-stage fitting* on a COFT-fine-tuned model for only one additional epoch. Moreover, we expect that the joint fitting re-scaled OFT can lead to better performance.

Report issue for preceding element

|  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |
|  | SD | ControlNet | T2I | LoRA | COFT | Re-scaled COFT |
| FID ↓↓\downarrow↓ | 41.2 | 30.9 | 33.1 | 30.9 | 30.8 | 30.2 |

Table 4: FID on the segmentation to image task (ADE20K). r=4𝑟4r=4italic\_r = 4 is used here.

Report issue for preceding element

### Appendix D Applying OFT to Convolution Layers

Report issue for preceding element

In the original setting [[22](https://arxiv.org/html/2306.07280v3#bib.bib22)], LoRA is only applied to the linear layers of the attention modules. To be a fair comparison, we also apply OFT to these weights. However, OFT is not limited to linear layers but can easily be adapted to convolution layers by transforming the convolutional neurons. We highlight the compatibility of OFT and COFT for finetuning convolution layers. More interestingly, sharing the parameters of diagonal blocks in 𝑹𝑹\bm{R}bold\_italic\_R becomes interpretable in convolution layers. With a suitable setup, orthogonal matrices with sharing diagonal blocks can transform the convolution kernel in a channel-sharing manner (or in a spatial manner), implying that the same orthogonal transformation is applied to all channels. This shares similar intuition with depth-wise convolution.

Report issue for preceding element

For this ablation experiment, we study the performance of applying OFT to the convolution layers in the ResNet blocks of the stable diffusion model. In this experiment, we use COFT as the baseline method and consider the controllable generation (segmentation to image) as an example. We have both quantitative (Table [5](https://arxiv.org/html/2306.07280v3#A4.T5 "Table 5 ‣ Appendix D Applying OFT to Convolution Layers ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")) and qualitative results (Figure [11](https://arxiv.org/html/2306.07280v3#A4.F11 "Figure 11 ‣ Appendix D Applying OFT to Convolution Layers ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning")). We can empirically observe that by only fine-tuning the convolutional layers, we can also achieve some degree of control. By simultaneously fine-tuning both linear and convolutional layers, we achieve a slightly better FID score. Note, for fine-tuning convolutional layers, we let r𝑟ritalic\_r be equal to the number of channels of convolutional neurons in that layer.

Report issue for preceding element

|  |  |  |  |
| --- | --- | --- | --- |
|  | COFT (attention) | COFT (conv) | COFT (extended) |
| FID ↓↓\downarrow↓ | 30.8 | 39.8 | 30.4 |

Table 5: FID results of applying COFT to different types of layers. (with r=4𝑟4r=4italic\_r = 4)

Report issue for preceding element
![Refer to caption](x11.png)


Figure 11: Controllable generation results of applying COFT to different types of layers.

Report issue for preceding element

### Appendix E Comparison between COFT and OFT

Report issue for preceding element

We have already provided many qualitative examples for COFT and OFT in the main paper. One may question the fundamental difference between OFT and COFT. Based on the intuition behind COFT, the deviation constraint is introduced to improve the training stability. We demonstrate the training stability of COFT with a qualitative example in subject-driven generation. Results in Figure [12](https://arxiv.org/html/2306.07280v3#A5.F12 "Figure 12 ‣ Appendix E Comparison between COFT and OFT ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning") and Figure [13](https://arxiv.org/html/2306.07280v3#A5.F13 "Figure 13 ‣ Appendix E Comparison between COFT and OFT ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning") show that, despite being much more stable than existing methods, OFT will eventually generate collapsed images at the 9000-th iteration. In contrast, COFT still produces visually appealing images. We train both OFT and COFT with a learning rate of 1×10−51superscript1051\times 10^{-5}1 × 10 start\_POSTSUPERSCRIPT - 5 end\_POSTSUPERSCRIPT and constrain COFT with ϵ=1×10−5italic-ϵ1superscript105\epsilon=1\times 10^{-5}italic\_ϵ = 1 × 10 start\_POSTSUPERSCRIPT - 5 end\_POSTSUPERSCRIPT.

Report issue for preceding element

![Refer to caption](x12.png)


Figure 12: Qualitative comparison between COFT and OFT on subject-driven generation.

Report issue for preceding element
![Refer to caption](x13.png)


Figure 13: Qualitative comparison between COFT and OFT on subject-driven generation.

Report issue for preceding element

### Appendix F More Qualitative Results

Report issue for preceding element

#### F.1 Subject-driven Generation

Report issue for preceding element
![Refer to caption](x14.png)


Figure 14: More qualitative results on subject-driven generation.

Report issue for preceding element
![Refer to caption](x15.png)


Figure 15: More qualitative results on subject-driven generation.

Report issue for preceding element

#### F.2 Controllable Generation

Report issue for preceding element

##### F.2.1 Segmentation to Image

Report issue for preceding element
![Refer to caption](x16.png)


Figure 16: More qualitative results of OFT and COFT on the segmentation to image generation task.

Report issue for preceding element
![Refer to caption](x17.png)


Figure 17: More qualitative results of OFT and COFT on the segmentation to image generation task.

Report issue for preceding element
![Refer to caption](x18.png)


Figure 18: More qualitative results of OFT and COFT on the segmentation to image generation task.

Report issue for preceding element

##### F.2.2 Canny Edge to Image

Report issue for preceding element
![Refer to caption](x19.png)


Figure 19: More qualitative results of OFT and COFT on the Canny edge to image generation task.

Report issue for preceding element
![Refer to caption](x20.png)


Figure 20: More qualitative results of OFT and COFT on the Canny edge to image generation task.

Report issue for preceding element
![Refer to caption](x21.png)


Figure 21: More qualitative results of OFT and COFT on the Canny edge to image generation task.

Report issue for preceding element

##### F.2.3 Landmark to Face

Report issue for preceding element
![Refer to caption](x22.png)


Figure 22: More qualitative results of OFT and COFT on the landmark to face generation task.

Report issue for preceding element
![Refer to caption](x23.png)


Figure 23: More qualitative results of OFT and COFT on the landmark to face generation task.

Report issue for preceding element
![Refer to caption](x24.png)


Figure 24: More qualitative results of OFT and COFT on the landmark to face generation task.

Report issue for preceding element

### Appendix G More Controllable Generation Tasks

Report issue for preceding element

#### G.1 Dense Pose to Human Body

Report issue for preceding element
![Refer to caption](x25.png)


Figure 25: Qualitative comparison among different methods on the dense pose to human body generation task.

Report issue for preceding element
![Refer to caption](x26.png)


Figure 26: More qualitative results of COFT and OFT on the dense pose to human body task.

Report issue for preceding element

#### G.2 Sketch to Image

Report issue for preceding element
![Refer to caption](x27.png)


Figure 27: Qualitative comparison among different methods on the sketch to image generation task.

Report issue for preceding element![Refer to caption](x28.png)


Figure 28: More qualitative comparison on the sketch to image generation task.

Report issue for preceding element

#### G.3 Depth to Image

Report issue for preceding element
![Refer to caption](x29.png)


Figure 29: Qualitative comparison among different methods on the depth to image generation task.

Report issue for preceding element![Refer to caption](x30.png)


Figure 30: More qualitative comparison on the depth to image generation task.

Report issue for preceding element

### Appendix H Human Evaluation

Report issue for preceding element

Human evaluation settings. We also carried out a structured human evaluation for the subject-driven generation task, involving 50 participants. Here’s a breakdown of our evaluation process:

Report issue for preceding element

* •

  Selection of subjects: we picked 7 subjects from the DreamBooth dataset999<https://github.com/google/dreambooth> at random.

  Report issue for preceding element
* •

  Image and prompt: for every subject, 4 unique text prompts were chosen at random. This resulted in a total of 28 distinct subject-prompt combinations. For every single one of the 28 tasks, we randomly sampled an image generated by each of the three methods - DreamBooth, LoRA, and OFT.

  Report issue for preceding element

Every participant was asked to answer three single-selection questions for each task:

Report issue for preceding element

* •

  Subject fidelity: which image best preserves the identity of the subject? In other words, which generated image resembles the most the original subject?

  Report issue for preceding element
* •

  Text alignment: which image matches the given text description the best?

  Report issue for preceding element
* •

  Overall image quality: out of the options, which image has the best overall quality?

  Report issue for preceding element

The methods were assessed at two specific points during their fine-tuning phase: at the 1000th iteration, a checkpoint where these methods typically exhibit best performance, and at the 10,000th iteration, a checkpoint used to measure the stability of the finetuning process over an extended period.

Report issue for preceding element

Results. The results are given in Table [6](https://arxiv.org/html/2306.07280v3#A8.T6 "Table 6 ‣ Appendix H Human Evaluation ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning"), indicating the proportion of participants who chose a particular method based on the above criteria. We can see that OFT is more favored after finetuning Stable Diffusion with 1000 iterations and after 10000 iterations. We note that OFT delivers significantly better image quality and text-following ability than both DreamBooth and LoRA after a relatively large number of finetuning iterations.

Report issue for preceding element

|  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |
|  | Iteration 1000 | | | Iteration 10000 | | |
| Metric | DreamBooth | LoRA | OFT | DreamBooth | LoRA | OFT |
| Subject Fidelity | 42.0% | 15.4% | 42.6% | 22.4% | 1.4% | 76.2% |
| Text Alignment | 18.6% | 24.7% | 56.7% | 2.6% | 1.4% | 96.0% |
| Overall Image Quality | 35.7% | 19.2% | 45.1% | 11.6% | 0.8% | 87.6% |

Table 6: Participant voting percentages for subject fidelity, text alignment and overall image quality.

Report issue for preceding element

### Appendix I Style Transfer by Adapting Stable Diffusion with Orthogonal Finetuning

Report issue for preceding element

Stable Diffusion can generate images based on the input text prompts. Without any adaptation, inputting text prompts to a pre-trained Stable Diffusion model will result in images that resemble natural images. We can finetune the pre-trained Stable Diffusion model on a custom dataset, to adapt the style of the generated images to the custom dataset. To demonstrate the effectiveness of orthogonal finetuning, we show qualitative results of adapting Stable Diffusion on the Sketch Scene dataset101010<https://huggingface.co/datasets/zoheb/sketch-scene> after finetuning for 20000 iterations in Figure [31](https://arxiv.org/html/2306.07280v3#A9.F31 "Figure 31 ‣ Appendix I Style Transfer by Adapting Stable Diffusion with Orthogonal Finetuning ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning") and on the Wikiart dataset111111<https://huggingface.co/datasets/fusing/wikiart_captions> after finetuning for 30000 iterations in Figure [32](https://arxiv.org/html/2306.07280v3#A9.F32 "Figure 32 ‣ Appendix I Style Transfer by Adapting Stable Diffusion with Orthogonal Finetuning ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning"). We train on a single NVIDIA A100-SXM4-80GB GPU using a learning rate of 1×10−41superscript1041\times 10^{-4}1 × 10 start\_POSTSUPERSCRIPT - 4 end\_POSTSUPERSCRIPT, batch size of 1111, and 4444 as the number of gradient accumulation steps.

Report issue for preceding element

![Refer to caption](x31.png)


Figure 31: Direct OFT Finetuning of Stable Diffusion on the sketch-scene dataset.

Report issue for preceding element
![Refer to caption](x32.png)


Figure 32: Direct OFT Finetuning of Stable Diffusion on the wikiart-caption dataset.

Report issue for preceding element

### Appendix J Failure Cases

Report issue for preceding element

We also show a few failure cases of OFT and COFT. Figure [33](https://arxiv.org/html/2306.07280v3#A10.F33 "Figure 33 ‣ J.1 Failure Cases in Subject-driven Generation ‣ Appendix J Failure Cases ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning") gives three failure cases in subject-driven generation. Figure [34](https://arxiv.org/html/2306.07280v3#A10.F34 "Figure 34 ‣ J.2 Failure Cases in Controllable Generation ‣ Appendix J Failure Cases ‣ Appendix ‣ Controlling Text-to-Image Diffusion by Orthogonal Finetuning") gives three failure cases in controllable generation.

Report issue for preceding element

#### J.1 Failure Cases in Subject-driven Generation

Report issue for preceding element

In subject-driven generation, OFT and COFT will sometimes fail to ground the text attribute to the intended object. In the cat example, both OFT and COFT will sometimes generate other red objects, instead of generating a red cat.

Report issue for preceding element

![Refer to caption](x33.png)


Figure 33: Some failure cases in subject-driven generation.

Report issue for preceding element

#### J.2 Failure Cases in Controllable Generation

Report issue for preceding element

Both OFT and COFT will sometimes hallucinate complicated structural details in a large region with the same semantics. Despite still being visually plausible, these generated images cannot match the original segmentation maps.

Report issue for preceding element

![Refer to caption](x34.png)


Figure 34: Some failure cases in controllable generation.

Report issue for preceding element

Generated by
[L
A
T
E
xml](https://math.nist.gov/~BMiller/LaTeXML/)

## Instructions for reporting errors

We are continuing to improve HTML versions of papers, and your feedback helps enhance accessibility and mobile support. To report errors in the HTML that will help us improve conversion and rendering, choose any of the methods listed below:

* Click the "Report Issue" button.
* Open a report feedback form via keyboard, use "**Ctrl + ?**".
* Make a text selection and click the "Report Issue for Selection" button near your cursor.
* You can use Alt+Y to toggle on and Alt+Shift+Y to toggle off accessible reporting links at each section.

Our team has already identified [the following issues](https://github.com/arXiv/html_feedback/issues). We appreciate your time reviewing and reporting rendering errors we may not have found yet. Your efforts will help us improve the HTML versions for all readers, because disability should not be a barrier to accessing research. Thank you for your continued support in championing open access for all.

Have a free development cycle? Help support accessibility at arXiv! Our collaborators at LaTeXML maintain a [list of packages that need conversion](https://github.com/brucemiller/LaTeXML/wiki/Porting-LaTeX-packages-for-LaTeXML), and welcome [developer contributions](https://github.com/brucemiller/LaTeXML/issues).

Report Issue

##### Report GitHub Issue

Title:

Content selection saved. Describe the issue below:

Description:

Submit without GitHubSubmit in GitHub

Report Issue for Selection
