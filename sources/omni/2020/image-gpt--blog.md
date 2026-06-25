# Image GPT | OpenAI
Source: https://openai.com/index/image-gpt/
Image GPT | OpenAI

[Skip to main content](#main)

* [Research](/research/index/)
* Products
* [Business](/business/)
* [Developers](/api/)
* [Company](/about/)
* [Foundation(opens in a new window)](https://openaifoundation.org/)

Log in[Try ChatGPT(opens in a new window)](https://chatgpt.com/?openaicom-did=b48edf5c-6ea6-49ba-b9c3-0b1e8ed17c37&openaicom_referred=true)

* Research
* Products
* Business
* Developers
* Company
* [Foundation(opens in a new window)](https://openaifoundation.org/)

Image GPT | OpenAI

June 17, 2020

[Publication](/research/index/publication/)

# Image GPT

[Read paper(opens in a new window)](https://cdn.openai.com/papers/Generative_Pretraining_from_Pixels_V2.pdf)[View code(opens in a new window)](https://github.com/openai/image-gpt)[ICML 2020 Paper (V1)(opens in a new window)](https://cdn.openai.com/papers/Generative_Pretraining_from_Pixels_V1_ICML.pdf)

![Image GPT](https://images.ctfassets.net/kftzwdyauwt9/5ae77333-6ec9-4b5b-345335df9dfe/be9cfca3194bf819fbd8f45fd49a5185/image_127.png?w=3840&q=90&fm=webp)

Illustration: Ben Barry

Listen to article

17:13

Share

Introduction

* [Introduction](#introduction)
* [From language GPT to image GPT](#from-language-gpt-to-image-gpt)
* [Towards general unsupervised learning](#towards-general-unsupervised-learning)
* [Approach](#approach)
* [Experimental results](#experimental-results)
* [Limitations](#limitations)
* [Conclusion](#conclusion)

Table of contents

* [Introduction](#introduction)
* [From language GPT to image GPT](#from-language-gpt-to-image-gpt)
* [Towards general unsupervised learning](#towards-general-unsupervised-learning)
* [Approach](#approach)
* [Experimental results](#experimental-results)
* [Limitations](#limitations)
* [Conclusion](#conclusion)

We find that, just as a large transformer model trained on language can generate coherent text, the same exact model trained on pixel sequences can generate coherent image [completions⁠](/index/image-gpt/#completions) and [samples⁠](/index/image-gpt/#samples). By establishing a correlation between sample quality and image classification accuracy, we show that our best generative model also contains features competitive with top convolutional nets in the unsupervised setting.

## Introduction

Unsupervised and self-supervised learning,[1](#citation-bottom-1) or learning without human-labeled data, is a longstanding challenge of machine learning. Recently, it has seen incredible success in language, as transformer[2](#citation-bottom-2) models like BERT,[3](#citation-bottom-3) GPT‑2,[4](#citation-bottom-4) RoBERTa,[5](#citation-bottom-5) T5,[6](#citation-bottom-6) and other variants[7](#citation-bottom-7), [8](#citation-bottom-8), [9](#citation-bottom-9), [10](#citation-bottom-10) have achieved top performance on a wide array of language tasks. However, the same broad class of models has not been successful in producing strong features for image classification.[11](#citation-bottom-11) Our work aims to understand and bridge this gap.

Transformer models like BERT and GPT‑2 are domain agnostic, meaning that they can be directly applied to 1-D sequences of any form. When we train GPT‑2 on images unrolled into long sequences of pixels, which we call iGPT, we find that the model appears to understand 2-D image characteristics such as object appearance and category. This is evidenced by the diverse range of coherent image samples it generates, even without the guidance of human provided labels. As further proof, features from the model achieve state-of-the-art performance on a number of classification datasets and near state-of-the-art unsupervised accuracy[A](#citation-bottom-A) on ImageNet.

| Evaluation | Dataset | Our Result | Best non-iGPT Result |
| --- | --- | --- | --- |
| Logistic regression on learned features (linear probe) | CIFAR-10 | **96.3** iGPT‑L 32x32 w/ 1536 features | 95.3 SimCLR[12⁠](/research/image-gpt/#fn-12) w/ 8192 features |
|  | CIFAR-100 | **82.8** iGPT‑L 32x32 w/ 1536 features | 80.2 SimCLR w/ 8192 features |
|  | STL-10 | **95.5** iGPT‑L 32x32 w/ 1536 features | 94.2 AMDIM[13⁠](/research/image-gpt/#fn-13) w/ 8192 features |
|  | ImageNet | 72.0 iGPT‑XL[a⁠](/research/image-gpt/#igpt-xl) 64x64 w/ 15360 features | **76.5** SimCLR w/ 8192 features |
| Full fine-tune | CIFAR-10 | **99.0** iGPT‑L 32x32, trained on ImageNet | **99.0**[b⁠](/research/image-gpt/#bit-l) GPipe,[14⁠](/research/image-gpt/#fn-14) trained on ImageNet |
|  | ImageNet 32x32 | 66.3 iGPT‑L 32x32 | **70.2** Isometric Nets[15⁠](/research/image-gpt/#fn-15) |

1. We only show ImageNet linear probe accuracy for iGPT‑XL since other experiments did not finish before we needed to transition to different supercomputing facilities.
2. Bit-L, trained on JFT (300M images with 18K classes), achieved a result of 99.3.

To highlight the potential of generative[17](#citation-bottom-17), [18](#citation-bottom-18) sequence modeling[19](#citation-bottom-19), [20](#citation-bottom-20), [21](#citation-bottom-21), [22](#citation-bottom-22) as a general purpose unsupervised learning algorithm, we deliberately use the same transformer architecture as GPT‑2 in language. As a consequence, we require significantly more compute in order to produce features competitive with those from top unsupervised convolutional nets.[13](#citation-bottom-13), [23](#citation-bottom-23), [24](#citation-bottom-24), [25](#citation-bottom-25), [12](#citation-bottom-12) However, our results suggest that when faced with a new domain where the correct model priors are unknown, a large GPT‑2 can learn excellent features without the need for domain-specific[26](#citation-bottom-26), [27](#citation-bottom-27), [28](#citation-bottom-28) architectural design choices.

# Completions

* [Favorites](#)
* [Animals](#)
* [Painted landscapes](#)
* [Sports](#)
* [Architecture](#)
* [ImageNet-R](#)
* [Movie posters](#)
* [Popular memes](#)
* [Landscapes](#)
* [Album covers](#)
* [Common English words](#)
* [US & state flags](#)
* [OpenAI research covers](#)
* [OpenAI Pets](#)
* [OpenAI Cooking](#)

Model input

Completions

Original

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-2-orig.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-2-0.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-2-1.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-2-2.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-2-3.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-2-orig.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-29-orig.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-29-0.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-29-1.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-29-2.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-29-3.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-29-orig.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-17-orig.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-17-0.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-17-1.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-17-2.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-17-3.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-17-orig.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-10-orig.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-10-0.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-10-1.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-10-2.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-10-3.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-10-orig.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-12-orig.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-12-0.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-12-1.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-12-2.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-12-3.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-12-orig.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-32-orig.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-32-0.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-32-1.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-32-2.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-32-3.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-32-orig.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-33-orig.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-33-0.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-33-1.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-33-2.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-33-3.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-33-orig.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-16-orig.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-16-0.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-16-1.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-16-2.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-16-3.png)

![](https://cdn.openai.com/image-gpt/completions/igpt-xl-miscellaneous-16-orig.png)

Model-generated completions of human-provided half-images. We sample the remaining halves with temperature 1 and without tricks like beam search or nucleus sampling. While we showcase our favorite completions in the first panel, we do not cherry-pick images or completions in all following panels.

# Samples

![](https://cdn.openai.com/image-gpt/samples/igpt-xl-322.png)

![](https://cdn.openai.com/image-gpt/samples/igpt-xl-599.png)

![](https://cdn.openai.com/image-gpt/samples/igpt-xl-76.png)

![](https://cdn.openai.com/image-gpt/samples/igpt-xl-456.png)

![](https://cdn.openai.com/image-gpt/samples/igpt-xl-207.png)

![](https://cdn.openai.com/image-gpt/samples/igpt-xl-452.png)

![](https://cdn.openai.com/image-gpt/samples/igpt-xl-424.png)

![](https://cdn.openai.com/image-gpt/samples/igpt-xl-522.png)

![](https://cdn.openai.com/image-gpt/samples/igpt-xl-222.png)

![](https://cdn.openai.com/image-gpt/samples/igpt-xl-241.png)

![](https://cdn.openai.com/image-gpt/samples/igpt-xl-290.png)

![](https://cdn.openai.com/image-gpt/samples/igpt-xl-588.png)

![](https://cdn.openai.com/image-gpt/samples/igpt-xl-579.png)

![](https://cdn.openai.com/image-gpt/samples/igpt-xl-169.png)

![](https://cdn.openai.com/image-gpt/samples/igpt-xl-506.png)

![](https://cdn.openai.com/image-gpt/samples/igpt-xl-77.png)

![](https://cdn.openai.com/image-gpt/samples/igpt-xl-85.png)

![](https://cdn.openai.com/image-gpt/samples/igpt-xl-80.png)

![](https://cdn.openai.com/image-gpt/samples/igpt-xl-83.png)

![](https://cdn.openai.com/image-gpt/samples/igpt-xl-490.png)

![](https://cdn.openai.com/image-gpt/samples/igpt-xl-340.png)

![](https://cdn.openai.com/image-gpt/samples/igpt-xl-215.png)

![](https://cdn.openai.com/image-gpt/samples/igpt-xl-161.png)

![](https://cdn.openai.com/image-gpt/samples/igpt-xl-414.png)

View more samples

Model-generated image samples. We sample these images with temperature 1 and without tricks like beam search or nucleus sampling. All of our samples are shown, with no cherry-picking. Nearly all generated images contain clearly recognizable objects.

Scale: 1.5x

## From language GPT to image GPT

In language, unsupervised learning algorithms that rely on word prediction (like GPT‑2 and BERT) have been extremely successful, achieving top performance on a wide array of language tasks. One possible reason for this success is that instances of downstream language tasks appear naturally in text: questions are often followed by answers (which could help with question-answering) and passages are often followed by summaries (which could help with summarization). In contrast, sequences of pixels do not clearly contain labels for the images they belong to.

Even without this explicit supervision, there is still a reason why GPT‑2 on images might work: a sufficiently large transformer trained on next pixel prediction might eventually learn to generate diverse[B](#citation-bottom-B) samples with clearly recognizable objects. Once it learns to do so, an idea known as “Analysis by Synthesis”[29](#citation-bottom-29), [30](#citation-bottom-30), [C](#citation-bottom-C) suggests that the model will also know about object categories. Many early generative models[31](#citation-bottom-31), [32](#citation-bottom-32), [33](#citation-bottom-33), [34](#citation-bottom-34), [35](#citation-bottom-35), [36](#citation-bottom-36) were motivated by this idea, and more recently, BigBiGAN[37](#citation-bottom-37) was an example which produced encouraging samples and features. In our work, we first show that better generative models achieve stronger classification performance. Then, through optimizing GPT‑2 for generative capabilities, we achieve top-level classification performance in many settings, providing further evidence for analysis by synthesis.

## Towards general unsupervised learning

Generative sequence modeling is a universal unsupervised learning algorithm: since all data types can be represented as sequences of bytes, a transformer can be directly applied to any data type without additional engineering. Our work tests the power of this generality by directly applying the architecture used to train GPT‑2 on natural language to image generation. We deliberately chose to forgo hand coding any image specific knowledge in the form of convolutions[38](#citation-bottom-38) or techniques like relative attention,[39](#citation-bottom-39) sparse attention,[40](#citation-bottom-40) and 2-D position embeddings.[27](#citation-bottom-27)

As a consequence of its generality, our method requires significantly more compute to achieve competitive performance in the unsupervised setting. Indeed, contrastive methods[41](#citation-bottom-41), [42](#citation-bottom-42), [43](#citation-bottom-43), [44](#citation-bottom-44), [45](#citation-bottom-45), [13](#citation-bottom-13), [23](#citation-bottom-23), [24](#citation-bottom-24), [25](#citation-bottom-25), [12](#citation-bottom-12) are still the most computationally efficient methods for producing high quality features from images. However, in showing that an unsupervised transformer model is competitive with the best unsupervised convolutional nets,[24](#citation-bottom-24), [25](#citation-bottom-25), [12](#citation-bottom-12) we provide evidence that it is possible to trade off hand coded domain knowledge for compute. In new domains,[46](#citation-bottom-46), [47](#citation-bottom-47) where there isn’t much knowledge to hand code, scaling compute seems an appropriate technique to test.

## Approach

We train iGPT‑S, iGPT‑M, and iGPT‑L, transformers containing 76M, 455M, and 1.4B parameters respectively, on ImageNet. We also train iGPT‑XL[D](#citation-bottom-D), a 6.8 billion parameter transformer, on a mix of ImageNet and images from the web. Due to the large computational cost of modeling long sequences with dense attention, we train at the low resolutions of 32x32, 48x48, and 64x64.

While it is tempting to work at even lower resolutions to further reduce compute cost, prior work has demonstrated that human performance on image classification begins to drop rapidly below these sizes.[48](#citation-bottom-48) Instead, motivated by early color display palettes,[49](#citation-bottom-49) we create our own 9-bit color palette to represent pixels. Using this palette yields an input sequence length 3 times shorter than the standard (R, G, B) palette, while still encoding color faithfully.

## Experimental results

There are two methods we use to assess model performance, both of which involve a downstream classification task. The first, which we refer to as a linear probe, uses the trained model to extract features[E](#citation-bottom-E) from the images in the downstream dataset, and then fits a logistic regression to the labels. The second method fine-tunes[F](#citation-bottom-F) the entire model on the downstream dataset.

Since next pixel prediction is not obviously relevant to image classification, features from the final layer may not be the most predictive of the object category. Our first result shows that feature quality is a sharply increasing, then mildly decreasing function of depth. This behavior suggests that a transformer generative model operates in two phases: in the first phase, each position gathers information from its surrounding context in order to build a contextualized image feature. In the second phase, this contextualized feature is used to solve the conditional next pixel prediction task. The observed two stage performance of our linear probes is reminiscent of another unsupervised neural net, the bottleneck autoencoder, which is manually designed so that features in the middle are used.

Feature quality depends heavily on the layer we choose to evaluate. In contrast with supervised models, the best features for these generative models lie in the middle of the network.

Our next result establishes the link between generative performance and feature quality. We find that both increasing the scale of our models and training for more iterations result in better generative performance, which directly translates into better feature quality.

Each line tracks a model throughout generative pre-training: the dotted markers denote checkpoints at steps 131K, 262K, 524K, and 1000K. The positive slopes suggest a link between improved generative performance and improved feature quality. Larger models also produce better features than smaller models. iGPT-XL is not included because it was trained on a different dataset.

When we evaluate our features using linear probes on CIFAR-10, CIFAR-100, and STL-10, we outperform features from all supervised and unsupervised transfer algorithms. Our results are also compelling in the full fine-tuning setting.

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  |  | **Pre-trained on ImageNet** |  |
| **Evaluation** | **Model** | **Accuracy** | **w/o labels** | **w/ labels** |
| CIFAR-10  Linear Probe | ResNet-152[50](#citation-bottom-50) | 94.0 |  | ✔ |
|  | SimCLR[12](#citation-bottom-12) | 95.3 | ✔ |  |
|  | iGPT‑L 32x32 | **96.3** | ✔ | ✔ |
| CIFAR-100  Linear Probe | ResNet-152 | 78.0 |  | ✔ |
|  | SimCLR | 80.2 | ✔ |  |
|  | iGPT‑L 32x32 | **82.8** | ✔ |  |
| STL-10  Linear Probe | AMDIM-L | 94.2 | ✔ |  |
|  | iGPT‑L 32x32 | **95.5** | ✔ |  |
| CIFAR-10  Fine-tune | AutoAugment | 98.5 |  |  |
|  | SimCLR | 98.6 | ✔ |  |
|  | GPipe | **99.0** |  | ✔ |
|  | iGPT‑L | **99.0** | ✔ |  |
| CIFAR-100  Fine-tune | iGPT‑L | 88.5 | ✔ |  |
|  | SimCLR | 89.0 | ✔ |  |
|  | AutoAugment | 89.3 |  |  |
|  | EfficientNet[52](#citation-bottom-52) | **91.7** |  | ✔ |

A comparison of linear probe and fine-tune accuracies between our models and top performing models which utilize either unsupervised or supervised ImageNet transfer. We also include AutoAugment, the best performing model trained end-to-end on CIFAR.

Given the resurgence of interest in unsupervised and self-supervised learning on ImageNet, we also evaluate the performance of our models using linear probes on ImageNet. This is an especially difficult setting, as we do not train at the standard ImageNet input resolution. Nevertheless, a linear probe on the 1536 features from the best layer of iGPT‑L trained on 48x48 images yields 65.2% top-1 accuracy, outperforming AlexNet.

Contrastive methods typically report their best results on 8192 features, so we would ideally evaluate iGPT with an embedding dimension of 8192 for comparison. However, training such a model is prohibitively expensive, so we instead concatenate features from multiple layers as an approximation. Unfortunately, our features tend to be correlated across layers, so we need more of them to be competitive. Taking 15360 features from 5 layers in iGPT‑XL yields 72.0% top-1 accuracy, outperforming AMDIM, MoCo, and CPC v2, but still underperforming SimCLR by a decent margin.

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| **Method** | **Input Resolution** | **Features** | **Parameters** | **Accuracy** |
| Rotation[53](#citation-bottom-53) | original | 8192 | 86M | 55.4 |
| iGPT‑L | 32x32 | 1536 | 1362M | 60.3 |
| BigBiGAN[37](#citation-bottom-37) | original | 16384 | 86M | 61.3 |
| iGPT‑L | 48x48 | 1536 | 1362M | 65.2 |
| AMDIM[13](#citation-bottom-13) | original | 8192 | 626M | 68.1 |
| MoCo[24](#citation-bottom-24) | original | 8192 | 375M | 68.6 |
| iGPT‑XL | 64x64 | 3072 | 6801M | 68.7 |
| SimCLR[12](#citation-bottom-12) | original | 2048 | 24M | 69.3 |
| CPC v2[25](#citation-bottom-25) | original | 4096 | 303M | 71.5 |
| iGPT‑XL | 64x64 | 3072 x 5 | 6801M | 72.0 |
| SimCLR | original | 8192 | 375M | **76.5** |

A comparison of linear probe accuracies between our models and state-of-the-art self-supervised models. We achieve competitive performance while training at much lower input resolutions, though our method requires more parameters and compute.

Because masked language models like BERT have outperformed generative models on most language tasks, we also evaluate the performance of BERT on our image models. Instead of training our model to predict the next pixel given all preceding pixels, we mask out 15% of the pixels and train our model to predict them from the unmasked ones. We find that though linear probe performance on BERT models is significantly worse, they excel during fine-tuning:

CIFAR-10

Linear probeFine-tune

ImageNet

Linear probeFine-tune

Comparison of generative pre-training with BERT pre-training using iGPT-L at an input resolution of 322 × 3. Bold colors show the performance boost from ensembling BERT masks. We see that generative models produce much better features than BERT models after pre-training, but BERT models catch up after fine-tuning.

While unsupervised learning promises excellent features without the need for human-labeled data, significant recent progress has been made under the more forgiving framework of semi-supervised learning, which allows for limited amounts of human-labeled data. Successful semi-supervised methods often rely on clever techniques such as consistency regularization, data augmentation, or pseudo-labeling, and purely generative-based approaches[54](#citation-bottom-54), [55](#citation-bottom-55) have not been competitive for years. We evaluate iGPT‑L[G](#citation-bottom-G) on a competitive benchmark for this sub-field and find that a simple linear probe on features from non-augmented images outperforms Mean Teacher[56](#citation-bottom-56) and MixMatch,[57](#citation-bottom-57) though it underperforms FixMatch.[59](#citation-bottom-59)

|  |  |  |  |
| --- | --- | --- | --- |
| Model | 40 labels | 250 labels | 4000 labels |
| Improved GAN[55](#citation-bottom-55) | — | — | 81.4 ± 2.3 |
| Mean Teacher[56](#citation-bottom-56) | — | 67.7 ± 2.3 | 90.8 ± 0.2 |
| MixMatch[57](#citation-bottom-57) | 52.5 ± 11.5 | 89.0 ± 0.9 | 93.6 ± 0.1 |
| iGPT‑L | 73.2 ± 01.5 | 87.6 ± 0.6 | 94.3 ± 0.1 |
| UDA[58](#citation-bottom-58) | 71.0 ± 05.9 | 91.2 ± 1.1 | 95.1 ± 0.2 |
| FixMatch[59](#citation-bottom-59) RA | 86.2 ± 03.4 | 94.9 ± 0.7 | **95.7 ± 0.1** |
| FixMatch CTA | **88.6 ± 03.4** | **94.9 ± 0.3** | 95.7 ± 0.2 |

A comparison of performance on low-data CIFAR-10. By leveraging many unlabeled ImageNet images, iGPT‑L is able to outperform methods such as Mean Teacher and MixMatch but still underperforms the state of the art methods. Our approach to semi-supervised learning is very simple since we only fit a logistic regression classifier on iGPT‑L's features without any data augmentation or fine-tuning—a significant difference from specially designed semi-supervised approaches.

## Limitations

While we have shown that iGPT is capable of learning powerful image features, there are still significant limitations to our approach. Because we use the generic sequence transformer used for GPT‑2 in language, our method requires large amounts of compute: iGPT‑L was trained for roughly 2500 V100-days while a similarly performing MoCo[24⁠](/index/image-gpt/#rf24) model can be trained in roughly 70 V100-days.

Relatedly, we model low resolution inputs using a transformer, while most self-supervised results use convolutional-based encoders which can easily consume inputs at high resolution. A new architecture, such as a domain-agnostic multiscale transformer, might be needed to scale further. Given these limitations, our work primarily serves as a proof-of-concept demonstration of the ability of large transformer-based language models to learn excellent unsupervised representations in novel domains, without the need for hardcoded domain knowledge. However, the significant resource cost to train these models and the greater accuracy of convolutional neural-network based methods precludes these representations from practical real-world applications in the vision domain.

Finally, generative models can exhibit biases that are a consequence of the data they’ve been trained on. Many of these biases are useful, like assuming that a combination of brown and green pixels represents a branch covered in leaves, then using this bias to continue the image. But some of these biases will be harmful, when considered through a lens of fairness and representation. For instance, if the model develops a visual notion of a scientist that skews male, then it might consistently complete images of scientists with male-presenting people, rather than a mix of genders. We expect that developers will need to pay increasing attention to the data that they feed into their systems and to better understand how it relates to biases in trained models.

## Conclusion

We have shown that by trading off 2-D knowledge for scale[60](#citation-bottom-60) and by choosing predictive features from the middle of the network, a sequence transformer can be competitive with top convolutional nets for unsupervised image classification. Notably, we achieved our results by directly applying the GPT‑2 language model to image generation. Our results suggest that due to its simplicity and generality, a sequence transformer given sufficient compute might ultimately be an effective way to learn excellent features in many domains.

If you’re excited to work with us on this area of research, [we’re hiring⁠](/careers/)!

* [GPT](/research/index/?tags=gpt)
* [Transformers](/research/index/?tags=transformers)
* [Generative Models](/research/index/?tags=generative-models)

## Footnotes

1. A

   Measured through logistic regression on learned features (linear probe).
2. B

   A transformer is trained to maximize the likelihood, and thus is mode covering, which automatically ensures the diversity of its samples.
3. C

   The original analysis by synthesis idea is more an argument for generative models with latent variables, but because generative models without latent variables were so much better at modeling the data distribution, we thought the analysis-by-synthesis conjecture should hold for them as well.
4. D

   We only show linear probe accuracy on ImageNet for iGPT-XL since other experiments did not finish before we needed to transition to different supercomputing facilities.
5. E

   To extract features for a linear probe, we take the post layernorm attention block inputs at some layer and average pool over the sequence dimension.
6. F

   To fine-tune, we take the post layernorm transformer output and average pool over the sequence dimension as input for the classification head.
7. G

   A generative model which learns features in a purely unsupervised fashion.

## References

1. 1

   LeCun, Y. (2017). “[Predictive Learning⁠(opens in a new window)](https://channel9.msdn.com/events/Neural-Information-Processing-Systems-Conference/Neural-Information-Processing-Systems-Conference-NIPS-2016/Predictive-Learning).”
2. 2

   Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A., Kaiser, L., & Polosukhin, I. “[Attention is All you Need⁠(opens in a new window)](http://papers.nips.cc/paper/7181-attention-is-all-you-need).” In NeurIPS 2017.
3. 3

   Devlin, J., Chang, M., Lee, K., & Toutanova, K. (2018). “[BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding⁠(opens in a new window)](https://arxiv.org/abs/1810.04805).” arXiv preprint.
4. 4

   Radford, A., Wu, J., Child, R., Luan, D., Amodei, D., & Sutskever, I. (2019). “[Language Models are Unsupervised Multitask Learners⁠(opens in a new window)](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf).” Technical Report, OpenAI.
5. 5

   Liu, Y., Ott, M., Goyal, N., Du, J., Joshi, M., Chen, D., Levy, O., Lewis, M., Zettlemoyer, L., & Stoyanov, V. (2019). “[RoBERTa: A Robustly Optimized BERT Pretraining Approach⁠(opens in a new window)](https://arxiv.org/abs/1907.11692).” arXiv preprint.
6. 6

   Raffel, C., Shazeer, N., Roberts, A., Lee, K., Narang, S., Matena, M., Zhou, Y., Li, W., & Liu, P. (2019). “[Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer⁠(opens in a new window)](https://arxiv.org/abs/1910.10683).” arXiv preprint.
7. 7

   Dai, A., Le, Q. V. (2015). “[Semi-supervised sequence learning⁠(opens in a new window)](http://papers.nips.cc/paper/5949-semi-supervised-sequence).” In NeurIPS 2015.
8. 8

   Peters, M., Neumann, M., Iyyer, M., Gardner, M., Clark, C., Lee, K., & Zettlemoyer, L. (2018). “[Deep Contextualized Word Representations⁠(opens in a new window)](https://arxiv.org/abs/1802.05365).” In NAACL 2018.
9. 9

   Howard, J., Ruder, S. (2018). “[Universal Language Model Fine-tuning for Text Classification⁠(opens in a new window)](https://arxiv.org/abs/1801.06146).” In ACL 2018.
10. 10

    Radford, A., Narasimhan, K., Salimans, T., & Sutskever, I. (2018). “[Improving language understanding by generative pre-training⁠(opens in a new window)](https://www.cs.ubc.ca/~amuham01/LING530/papers/radford2018improving.pdf).” Technical Report, OpenAI.
11. 11

    Ke N., Goyal, A., Bilaniuk,O., Binas, J., Mozer, M., Pal, C., Bengio, Y (2018). “[Sparse attentive backtracking: Temporal credit assignment through reminding⁠(opens in a new window)](http://papers.nips.cc/paper/7991-sparse-attentive-backtracking-temporal-credit-assignment-through-reminding).” In NeurIPS 2018.
12. 12

    Chen, T., Kornblith, S., Norouzi, M., Hinton, G. (2020). “[A Simple Framework for Contrastive Learning of Visual Representations⁠(opens in a new window)](https://arxiv.org/abs/2002.05709).” arXiv preprint.
13. 13

    Bachman, P., Hjelm, R., & Buchwalter, W. (2019). “[Learning representations by maximizing mutual information across views⁠(opens in a new window)](http://papers.nips.cc/paper/9686-learning-representations-by-maximizing-mutual-information-across-views).” In NeurIPS 2019.
14. 14

    Kolesnikov, A. & Beyer, L. & Zhai, X., Puigcerver, J., Yung, J., Gelly, S., Houlsby, N. (2019). “[Big Transfer (BiT): General Visual Representation Learning⁠(opens in a new window)](https://arxiv.org/abs/1912.11370).” arXiv preprint.
15. 15

    Huang, Y., Cheng, Y., Bapna, A., Firat, O., Chen, D., Chen, M., Lee, H., Ngiam, J., Le, Q. V., Wu, Y., & Chen, Z. (2019) “[GPipe: Efficient Training of Giant Neural Networks using Pipeline Parallelism⁠(opens in a new window)](http://papers.nips.cc/paper/8305-gpipe-efficient-training-of-giant-neural-networks-using-pipeline-parallelism).” In NeurIPS 2019.
16. 16

    Sandler, M., Baccash, J., Zhmoginov, A., & Howard, A. (2019). “[Non-discriminative data or weak model? On the relative importance of data and model resolution⁠(opens in a new window)](https://arxiv.org/abs/1909.03205).” In ICCV 2019.
17. 17

    Lasserre, J., Bishop, C., & Minka, T. P. (2006). “[Principled Hybrids of Generative and Discriminative Models⁠(opens in a new window)](https://ieeexplore.ieee.org/document/1640745).” In CVPR 2006.
18. 18

    Erhan, D., Bengio, Y., Courville, A., Manzagol, P., Vincent, P., Bengio, S. (2010). “[Why does unsupervised pre-training help deep learning?⁠(opens in a new window)](http://www.jmlr.org/papers/v11/erhan10a.html).” In JMLR 2010.
19. 19

    Elman, J. (1990). “[Finding Structure in Time⁠(opens in a new window)](https://onlinelibrary.wiley.com/doi/abs/10.1207/s15516709cog1402_1).” In Cognitive Science 1990.
20. 20

    Mikolov, T., Karafiat, M., Burget, L., Cernocky, J., Khudanpur, S. (2010). “[Recurrent neural network based language model⁠(opens in a new window)](https://www.isca-speech.org/archive/interspeech_2010/i10_1045.html).” In INTERSPEECH-2010.
21. 21

    Larochelle, H., Murray, I. (2011). “[The neural autoregressive distribution estimator⁠(opens in a new window)](http://proceedings.mlr.press/v15/larochelle11a/larochelle11a.pdf).” In AISTATS 2011.
22. 22

    Graves, A. (2013). “[Generating sequences with recurrent neural networks⁠(opens in a new window)](https://arxiv.org/abs/1308.0850).” arXiv preprint.
23. 23

    Tian, Y., Krishnan, D., & Isola, P. (2019). “[Contrastive multiview coding⁠(opens in a new window)](https://arxiv.org/abs/1906.05849).” arXiv preprint.
24. 24

    He, K., Fan, H., Wu, Y., Xie, S., & Girshick, R. (2019). “[Momentum Contrast for Unsupervised Visual Representation Learning⁠(opens in a new window)](https://arxiv.org/abs/1911.05722).” arXiv preprint.
25. 25

    Henaff, O., Srinivas, A., De Fauw, J., Razavi, A., Doersch, C., Eslami, S., Oord, A. (2019). “[Data-Efficient Image Recognition with Contrastive Predictive Coding⁠(opens in a new window)](https://arxiv.org/abs/1905.09272) .” arXiv preprint.
26. 26

    Oord, A., Kalchbrenner, N., Kavukcuoglu, K. (2016). “[Pixel recurrent neural networks⁠(opens in a new window)](https://arxiv.org/abs/1601.06759).” arXiv preprint.
27. 27

    Parmar, N., Vaswani, A., Uszkoreit, J., Kaiser, L., Shazeer, N., Ku, A., & Tran, D. (2018). “[Image transformer⁠(opens in a new window)](https://arxiv.org/abs/1802.05751).” In ICML 2018.
28. 28

    Menick, J., Kalchbrenner, N. (2018). “[Generating High Fidelity Images with Subscale Pixel Networks and Multidimensional Upscaling⁠(opens in a new window)](https://arxiv.org/abs/1812.01608).” arXiv preprint.
29. 29

    Mumford, D. (1992). “[On the computational architecture of the neocortex⁠(opens in a new window)](https://link.springer.com/article/10.1007/BF00198477).” In Biol. Cybern.
30. 30

    Rao, R., Ballard, D. (1999). “[Predictive coding in the visual cortex: a functional interpretation of some extra-classical receptive-field effects⁠(opens in a new window)](https://www.nature.com/articles/nn0199_79).” In Nature Neuroscience.
31. 31

    Smolensky, P. (1986). “[Information processing in dynamical systems: Foundations of harmony theory⁠(opens in a new window)](https://apps.dtic.mil/docs/citations/ADA620727).”
32. 32

    Hinton, G. (2002). “[Training Products of Experts by Minimizing Contrastive Divergence⁠(opens in a new window)](https://www.mitpressjournals.org/doi/abs/10.1162/089976602760128018).” In MIT Press.
33. 33

    Hinton, G., Osindero, S., & Teh, Y. (2006). “[A fast learning algorithm for deep belief nets⁠(opens in a new window)](https://www.mitpressjournals.org/doi/abs/10.1162/neco.2006.18.7.1527).” In Neural Computation.
34. 34

    Vincent, P., Larochelle, H., Bengio, Y., & Manzagol, P. (2008). “[Extracting and composing robust features with denoising autoencoders⁠(opens in a new window)](https://dl.acm.org/doi/abs/10.1145/1390156.1390294).” In ICML 2008.
35. 35

    Coates, A., Lee, H., & Ng, A. Y. (2011). “[An analysis of single-layer networks in unsupervised feature learning⁠(opens in a new window)](http://proceedings.mlr.press/v15/coates11a/coates11a.pdf).” In AISTATS 2011.
36. 36

    Le, Q. V., Ranzato, M., Monga, R., Devin, M., Chen, K., Corrado, G., Dean, J. & Ng, A. Y. (2012). “[Building high-level features using large scale unsupervised learning⁠(opens in a new window)](https://icml.cc/2012/papers/73.pdf).” In ICML 2012.
37. 37

    Donahue, J., Simonyan, K. (2019). “[Large scale adversarial representation learning⁠(opens in a new window)](http://papers.nips.cc/paper/9240-large-scale-adversarial-representation-learning).” In NeurIPS 2019.
38. 38

    Ciresan, D., Meier, U., Gambardella, L. & Schmidhuber, J. (2010). “[Deep Big Simple Neural Nets Excel on Handwritten Digit Recognition⁠(opens in a new window)](https://arxiv.org/pdf/1003.0358.pdf).” In CoRR 2010.
39. 39

    Shaw, P., Uszkoreit, J., & Vaswani A. (2018). “[Self-attention with relative position representations⁠(opens in a new window)](https://arxiv.org/abs/1803.02155).” In NAACL 2018.
40. 40

    Child, R., Gray, S., Radford, A., & Sutskever, I. (2019). “[Generating long sequences with sparse transformers⁠(opens in a new window)](https://arxiv.org/abs/1904.10509).” arXiv preprint.
41. 41

    Becker, S., Hinton, G. (1991). “[Self-organizing neural network that discovers surfaces in random-dot stereograms⁠(opens in a new window)](https://www.nature.com/articles/355161a0).” In Nature.
42. 42

    Bromley, J., Guyon, I., LeCun, Y., Sackinger, E., & Shah, R. (1994). “[Signature verification using a” siamese” time delay neural network⁠(opens in a new window)](http://papers.nips.cc/paper/769-signature-verification-using-a-siamese-time-delay-neural-network.pdf).” In NeurIPS 1994.
43. 43

    Mikolov, T., Sutskever, I., Chen, K., Corrado, G., & Dean, J. (2013). “[Distributed Representations of Words and Phrases and their Compositionality⁠(opens in a new window)](http://papers.nips.cc/paper/5021-distributed-representations-of-words-and-phrases-and-their-compositionality) .” In NeurIPS 2013.
44. 44

    Oord, A., Li, Y., Vinyals, O. (2018). “[Representation Learning with Contrastive Predictive Coding⁠(opens in a new window)](https://arxiv.org/abs/1807.03748) .” arXiv preprint.
45. 45

    Hjelm, R., Fedorov, A., Lavoie-Marchildon, S., Grewal, K., Bachman, P., Trischler, A., & Bengio, Y. (2018). “[Learning deep representations by mutual information estimation and maximization⁠(opens in a new window)](https://arxiv.org/abs/1808.06670).” In ICLR 2019.
46. 46

    Alley, E., Khimulya, G., Biswas, S., AlQuraishi, M., Church, G. (2019). “[Unified rational protein engineering with sequence-only deep representation learning⁠(opens in a new window)](https://www.biorxiv.org/content/10.1101/589333v1).” In Nature Methods.
47. 47

    Rives, A., Goyal, S., Meier, J., Guo, D., Ott, M., Zitnick, C., Ma, J., Fergus, R. (2019). “[Biological Structure and Function Emerge from Scaling Unsupervised Learning to 250 Million Protein Sequences⁠(opens in a new window)](https://www.biorxiv.org/content/10.1101/622803v1).” bioRxiv preprint.
48. 48

    Torralba, A., Fergus, R., Freeman, W. (2008). “[80 million tiny images: A large data set for nonparametric object and scene recognition⁠(opens in a new window)](https://ieeexplore.ieee.org/abstract/document/4531741).” In IEEE transactions on pattern analysis and machine intelligence.
49. 49

    “[List of 8-Bit Computer Hardware Graphics⁠(opens in a new window)](https://en.wikipedia.org/wiki/List_of_8-bit_computer_hardware_graphics).” Wikipedia, 8 May 2020
50. 50

    Kornblith, S., Shlens, J., & Le, Q. V. (2019). “[Do Better ImageNet Models Transfer Better?⁠(opens in a new window)](http://openaccess.thecvf.com/content_CVPR_2019/html/Kornblith_Do_Better_ImageNet_Models_Transfer_Better_CVPR_2019_paper.html).” In CVPR 2019.
51. 51

    Cubuk, E., Zoph, B., Mane, D., Vasudevan, V., & Le, Q. V. (2019). “[AutoAugment: Learning Augmentation Strategies From Data⁠(opens in a new window)](http://openaccess.thecvf.com/content_CVPR_2019/html/Cubuk_AutoAugment_Learning_Augmentation_Strategies_From_Data_CVPR_2019_paper.html).” In CVPR 2019.
52. 52

    Tan, M., Le, Q. V. (2019). “[EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks⁠(opens in a new window)](https://arxiv.org/abs/1905.11946).” In ICML 2019.
53. 53

    Gidaris, S., Singh, P., & Komodakis, N. (2018). “[Unsupervised Representation Learning by Predicting Image Rotations⁠(opens in a new window)](https://arxiv.org/abs/1803.07728).” In ICLR 2018.
54. 54

    Kingma, D., Rezende, D. J., Mohamed, S., & Welling, M. (2014). “[Semi-Supervised Learning with Deep Generative Models⁠(opens in a new window)](https://arxiv.org/pdf/1406.5298.pdf).” In NeurIPS 2014.
55. 55

    Salimans, T., Goodfellow, I., Zaremba, W., Cheung, V., Radford, A., Chen, X. (2016). “[Improved techniques for training gans⁠(opens in a new window)](http://papers.nips.cc/paper/6124-improved-techniques-for-training-gans).” In NeurIPS 2016.
56. 56

    Tarvainen, A., Valpola, H. (2017). “[Mean teachers are better role models: Weight-averaged consistency targets improve semi-supervised deep learning results⁠(opens in a new window)](https://papers.nips.cc/paper/6719-mean-teachers-are-better-role-models-weight-averaged-consistency-targets-improve-semi-supervised-deep-learning-results).” In NeurIPS 2017.
57. 57

    Berthelot, D., Carlini, N., Goodfellow, I., Papernot, N., Oliver, A., Raffel, C. (2019). “[MixMatch: A Holistic Approach to Semi-Supervised Learning⁠(opens in a new window)](http://papers.nips.cc/paper/8749-mixmatch-a-holistic-approach-to-semi-supervised-learning).” In NeurIPS 2019.
58. 58

    Xie, Q., Dai, Z., Hovy, E., Luong, M., & Le, Q. V. (2019). “[Unsupervised Data Augmentation for Consistency Training⁠(opens in a new window)](https://arxiv.org/abs/1904.12848).” arXiv preprint.
59. 59

    Sohn, K., Berthelot, D., Li, C., Zhang, Z., Carlini, N., Cubuk, E., Kurakin, A., Zhang, H., Raffel, C. (2020). “[Fixmatch: Simplifying semi-supervised learning with consistency and confidence⁠(opens in a new window)](https://arxiv.org/abs/2001.07685).” arXiv preprint.
60. 60

    Sutton, R. (2019). “[The Bitter Lesson⁠(opens in a new window)](http://www.incompleteideas.net/IncIdeas/BitterLesson.html).”

## Authors

Mark Chen, Alec Radford, Ilya Sutskever

## Acknowledgments

Foremost, we would like to acknowledge our paper co-authors Rewon Child, Jeff Wu, Heewoo Jun, Prafulla Dhariwal, and David Luan.

Thanks to the following for their feedback on this work and contributions to this release: Vedant Misra, Noah Golmant, Johannes Otterbach, Pranav Shyam, Aditya Ramesh, Yura Burda, Harri Edwards, Chris Hallacy, Jeff Clune, Jack Clark, Irene Solaiman, Ryan Lowe, Greg Brockman, Kelly Sims, David Farhi, Will Guss, Quoc V. Le, and Ashish Vaswani.

Editor: Ashley Pilipiszyn

Design: Justin Jay Wang

Cover artwork: Ben Barry

## Related articles

[View all](/news/)

![Point E A System For Generating 3d Point Clouds From Complex Prompts](https://images.ctfassets.net/kftzwdyauwt9/7e4ba260-7655-4049-5a2568c94158/2f2af956a356ee2b507296d01e45e766/image-5.webp?w=3840&q=90&fm=webp)

[Point-E: A system for generating 3D point clouds from complex prompts

PublicationDec 16, 2022](/index/point-e/)

![An aerial view of a crowd of people facing away, wearing hats and bearing flags](https://images.ctfassets.net/kftzwdyauwt9/d22f177f-5116-4b3b-5ddcdbe54569/b657a1299069351973db72804b5811d1/image_131.png?w=3840&q=90&fm=webp)

[DALL·E 2 pre-training mitigations

PublicationJun 28, 2022](/index/dall-e-2-pre-training-mitigations/)

![Screenshot of a scene from Minecraft](https://images.ctfassets.net/kftzwdyauwt9/ef9fc360-1a5a-4ca3-5c25b83b3564/50c07940455cc86ef84d91526d9cf3e0/vpt.jpg?w=3840&q=90&fm=webp)

[Learning to play Minecraft with Video PreTraining

ConclusionJun 23, 2022](/index/vpt/)

Research

* [Research Index](/research/index/)
* [Research Overview](/research/)
* [Economic Research](/signals/)

Latest Advancements

* [GPT-5.5](/index/introducing-gpt-5-5/)
* [GPT-5.4](/index/introducing-gpt-5-4/)
* [GPT-5.3 Instant](/index/gpt-5-3-instant/)

Safety

* [Safety Approach](/safety/)
* [Deployment Safety(opens in a new window)](https://deploymentsafety.openai.com/)
* [Security & Privacy](/security-and-privacy/)
* [Trust & Transparency](/trust-and-transparency/)

Products

* [ChatGPT(opens in a new window)](https://chatgpt.com/?openaicom-did=b48edf5c-6ea6-49ba-b9c3-0b1e8ed17c37&openaicom_referred=true)
* [ChatGPT Business(opens in a new window)](https://chatgpt.com/business/?openaicom-did=b48edf5c-6ea6-49ba-b9c3-0b1e8ed17c37&openaicom_referred=true)
* [ChatGPT Enterprise(opens in a new window)](https://chatgpt.com/business/enterprise/?openaicom-did=b48edf5c-6ea6-49ba-b9c3-0b1e8ed17c37&openaicom_referred=true)
* [ChatGPT for Education(opens in a new window)](https://chatgpt.com/business/education/?openaicom-did=b48edf5c-6ea6-49ba-b9c3-0b1e8ed17c37&openaicom_referred=true)
* [Codex](/codex/)
* [Release Notes](/products/release-notes/)

API Platform

* [Overview](/api/)
* [API Log In(opens in a new window)](https://platform.openai.com/login)
* [Docs(opens in a new window)](https://developers.openai.com/api/docs)

Business

* [Overview](/business/)
* [Solutions](/solutions/)
* [Resources](/business/learn/)
* [Contact Sales](/contact-sales/)

Developers

* [Apps SDK(opens in a new window)](https://developers.openai.com/apps-sdk)
* [Open Models](/open-models/)
* [Docs(opens in a new window)](https://developers.openai.com/)
* [Resources(opens in a new window)](https://developers.openai.com/learn)
* [Developer Forum(opens in a new window)](https://community.openai.com/)

Company

* [About Us](/about/)
* [Our Charter](/charter/)
* [Careers](/careers/)
* [News](/news/)

Support

* [Help Center(opens in a new window)](https://help.openai.com/)

More

* [Stories](/stories/)
* [Academy](/academy/)
* [Livestreams](/live/)
* [Podcast](/podcast/)
* [RSS](/news/rss.xml)

Terms & Policies

* [Terms of Use](/policies/terms-of-use/)
* [Privacy Policy](/policies/privacy-policy/)
* [Other Policies](/policies/)

[(opens in a new window)](https://x.com/OpenAI)[(opens in a new window)](https://www.youtube.com/OpenAI)[(opens in a new window)](https://www.linkedin.com/company/openai)[(opens in a new window)](https://github.com/openai)[(opens in a new window)](https://www.instagram.com/openai/)[(opens in a new window)](https://www.tiktok.com/@openai)[(opens in a new window)](https://discord.gg/openai)

OpenAI © 2015–2026Manage Cookies

EnglishUnited States

We use cookies

We use cookies to help this site function, understand service usage, and support marketing efforts. Visit Manage Cookies to change preferences anytime. View our [Cookie Policy](/policies/cookie-policy/) for more info.

Manage CookiesReject non-essentialAccept all
