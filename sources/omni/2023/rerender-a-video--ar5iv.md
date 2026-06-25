# [2306.07954] Rerender A Video: Zero-Shot Text-Guided Video-to-Video Translation
Source: https://ar5iv.labs.arxiv.org/html/2306.07954
Rerender A Video: Zero-Shot Text-Guided Video-to-Video Translation
Shuai Yang      Yifan Zhou      Ziwei Liu      Chen Change Loy
✉

S-Lab, Nanyang Technological University {shuai.yang, yifan.zhou, ziwei.liu, ccloy}@ntu.edu.sg
Abstract

Large text-to-image diffusion models have exhibited impressive proficiency in generating high-quality images. However, when applying these models to video domain, ensuring temporal consistency across video frames remains a formidable challenge. This paper proposes a novel zero-shot text-guided video-to-video translation framework to adapt image models to videos. The framework includes two parts: key frame translation and full video translation. The first part uses an adapted diffusion model to generate key frames, with hierarchical cross-frame constraints applied to enforce coherence in shapes, textures and colors. The second part propagates the key frames to other frames with temporal-aware patch matching and frame blending. Our framework achieves global style and local texture temporal consistency at a low cost (without re-training or optimization). The adaptation is compatible with existing image diffusion techniques, allowing our framework to take advantage of them, such as customizing a specific subject with LoRA, and introducing extra spatial guidance with ControlNet. Extensive experimental results demonstrate the effectiveness of our proposed framework over existing methods in rendering high-quality and temporally-coherent videos. Code is available at our project page: https://www.mmlab-ntu.com/project/rerender/

Figure 1:We present a novel video-to-video translation framework that can render a source input video into a temporal-coherent video with the style specified by a target textual description.
1Introduction

Recent text-to-image diffusion models such as DALLE-2 [30], Imagen [34], Stable Diffusion [32] demonstrate exceptional ability in generating diverse and high-quality images guided by natural language. Based on it, a multitude of image editing methods have emerged, including model fine-tuning for customized object generation [33], image-to-image translation [23], image inpainting [1], and object editing [12]. These applications allow users to synthesize and edit images effortlessly, using natural language within a unified diffusion framework, greatly improving creation efficiency. As video content surges in popularity on social media platforms, the demand for more streamlined video creation tools has concurrently risen. Yet, a critical challenge remains: the direct application of existing image diffusion models to videos leads to severe flickering issues.

Researchers have recently turned to text-guided video diffusion models and proposed three solutions. The first solution involves training a video model on large-scale video data [14], which requires significant computing resources. Additionally, the re-designed video model is incompatible with existing off-the-shelf image models. The second solution is to fine-tune image models on a single video [40], which is less efficient for long videos. Overfitting to a single video may also degrade the performance of the original models. The third solution involves zero-shot methods [20] that require no training. During the diffusion sampling process, cross-frame constraints are imposed on the latent features for temporal consistency. The zero-shot strategy requires fewer computing resources and is mostly compatible with existing image models, showing promising potential. However, current cross-frame constraints are limited to global styles and are unable to preserve low-level consistency, e.g., the overall style may be consistent, but the local structures and textures may still flicker.

Achieving successful application of image diffusion models to the video domain is a challenging task. It requires 1) Temporal consistency: cross-frame constraints for low-level consistency; 2) Zero-shot: no training or fine-tuning required; 3) Flexibility: compatible with off-the-shelf image models for customized generation. As mentioned above, image models can be customized by fine-tuning on specific objects to capture the target style more precisely than general models. Figure 2 shows two examples. To take advantage of it, in this paper, we employ zero-shot strategy for model compatibility and aim to further solve the key issue of this strategy in maintaining low-level temporal consistency.

Figure 2:Customized model and ControlNet generate high-quality results with better consistency with both prompt and content. Our method is designed to be compatible with these existing image diffusion techniques, and thus can take advantage of them to strike a good balance between the style (prompt) and the content.

To achieve this goal, we propose novel hierarchical cross-frame constraints for pre-trained image models to produce coherent video frames. Our key idea is to use optical flow to apply dense cross-frame constraints, with the previous rendered frame serving as a low-level reference for the current frame and the first rendered frame acting as an anchor to regulate the rendering process to prevent deviations from the initial appearance. Hierarchical cross-frame constraints are realized at different stages of diffusion sampling. In addition to global style consistency, our method enforces consistency in shapes, textures and colors at early, middle and late stages, respectively. This innovative and lightweight modification achieves both global and local temporal consistency. Figure 1 presents our coherent video translation results over off-the-shelf image models customized for six unique styles.

Based on the insight, this paper introduces a novel zero-shot framework for text-guided video-to-video translation, consisting of two parts: key frame translation and full video translation. In the first part, we adapt pre-trained image diffusion models with hierarchical cross-frame constraints for generating key frames. In the second part, we propagate the rendered key frames to other frames using temporal-aware patch matching and frame blending. The diffusion-based generation is excellent at content creation, but its multi-step sampling process is inefficient. The patch-based propagation, on the other hand, can efficiently infer pixel-level coherent frames but is not capable of creating new content. By combining these two parts, our framework strikes a balance between quality and efficiency. To summarize, our main contributions are as follows:

• 

A novel zero-shot framework for text-guided video-to-video translation, which achieves both global and local temporal consistency, requires no training, and is compatible with pre-trained image diffusion models.

• 

Hierarchical cross-frame consistency constraints to enforce temporal consistency in shapes, textures and colors, which adapt image diffusion models to videos.

• 

Hybrid diffusion-based generation and patch-based propagation to strike a balance between quality and efficiency.

2Related Work
2.1Text Driven Image Generation

Generating images with descriptive sentences is intuitive and flexible. Early attempts explore GAN [44, 42, 46, 43] to synthesize realistic images. With the powerful expressivity of Transformer [38], autoregressive models [31, 9, 6] are proposed to model image pixels as a sequence with autoregressive dependency between each pixel. DALL-E [31] and CogView [6] train an autoregressive transformer on image and text tokens. Make-A-Scene [9] further considers segmentation masks as condition.

Recent studies focus on diffusion models [15] for text-to-image generation, where images are synthesized via a gradual denoising process. DALLE-2 [30] and Imagen [34] introduce pretrained large language models [29, 28] as text encoder to better align the image with text, and cascade diffusion models for high resolution image generation. GLIDE [26] introduces classifier-free guidance to improve text conditioning. Instead of applying denoising in the image space, Latent Diffusion Models [32] uses the low-resolution latent space of VQ-GAN [7] to improve the efficiency. We refer to [4] for a thorough survey.

In addition to diffusion models for general images, customized models are studied. Textual Inversion [10] and DreamBooth [33] learn special tokens to capture novel concepts and generate related images given a small number of example images. LoRA [17] accelerates the fine-tuning large models by learning low-rank weight matrices added to existing weights. ControlNet [45] fine-tunes a new control path to provide pixel-level conditions such as edge maps and pose, enabling fine-grained image generation. Our method does not alter the pre-trained model, thus is orthogonal to these existing techniques. This empowers our method to leverage DreamBooth and LoRA for better customized video translation and to use ControlNet for temporal-consistent structure guidance as in Fig. 2.

2.2Video Editing with Diffusion Models

For text-to-video generation, Video Diffusion Model [16] proposes to extend the 2D U-Net in image model to a factorized space-time UNet. Imagen Video [14] scales up the Video Diffusion Model with a cascade of spatial and temporal video super-resolution models, which is further extended to video editing by Dreamix [25]. Make-A-Video [36] leverages video data in an unsupervised manner to learn the movement to drive the image model. Although promising, the above methods need large-scale video data for training.

Tune-A-Video [40] instead inflates an image diffusion model into a video model with cross-frame attention, and fine-tunes it on a single video to generate videos with related motion. Based on it, Edit-A-Video [35], Video-P2P [22] and vid2vid-zero [39] utilize Null-Text Inversion [24] for precise inversion to preserve the unedited region. However, these models need fine-tuning of the pre-trained model or optimization over the input video, which is less efficient.

Recent developments have seen the introduction of zero-shot methods that, by design, operate without any training phase. Thus, these methods are naturally compatible with pre-trained diffusion variants like InstructPix2Pix [2] or ControlNet to accept more flexible conditions like depth and edges. Based on the editing masks detected by Prompt2Prompt [12] to indicate the channel and spatial region to preserve, FateZero [27] blends the attention features before and after editing. Text2Video-Zero [20] translates the latent to directly simulate motions and Pix2Video [3] matches the latent of the current frame to that of the previous frame. All the above methods largely rely on cross-frame attention and early-step latent fusion to improve temporal consistency. However, as we will show later, these strategies predominantly cater to high-level styles and shapes, and being less effective in maintaining cross-frame consistency at the level of texture and detail. In contrast to these approaches, our method proposes a novel pixel-aware cross-frame latent fusion, which non-trivially achieves pixel-level temporal consistency.

Another zero-shot solution is to apply frame interpolation to infer the videos based on one or more diffusion-edited frames. The seminal work of image analogy [13] migrates the style effect from an exemplar pair to other images with patch matching. Fišer et al. [8] extend image analogy to facial video translation with the guidance of facial features. Later, Jamrivška et al. [19] propose an improved EbSynth for general video translation based on multiple exemplar frames with a novel temporal blending approach. Although these patch-based methods can preserve fine details, their temporal consistency largely relies on the coherence across the exemplar frames. Thus, our adapted diffusion model for generating coherent frames is well suited for these methods, as we will show later in Fig. 11. In this paper, we integrate the zero-shot EbSynth into our framework to achieve better temporal consistency and accelerate inference without any further training.

3Preliminary: Diffusion Models
Stable Diffusion

Stable Diffusion is a latent diffusion model operating in the latent space of an autoencoder 
𝒟
​
(
ℰ
​
(
⋅
)
)
, where 
ℰ
 and are the encoder and decoder, respectively. Specifically, for an image 
𝐼
 with its latent feature 
𝑥
0
=
ℰ
​
(
𝐼
)
, the diffusion forward process iteratively add noises to the latent

	
𝑞
​
(
𝑥
𝑡
|
𝑥
𝑡
−
1
)
=
𝒩
​
(
𝑥
𝑡
;
𝛼
𝑡
​
𝑥
𝑡
−
1
,
(
1
−
𝛼
𝑡
)
​
𝐈
)
,
		
(1)

where 
𝑡
=
1
,
…
,
𝑇
 is the time step, 
𝑞
​
(
𝑥
𝑡
|
𝑥
𝑡
−
1
)
 is the conditional density of 
𝑥
𝑡
 given 
𝑔
𝑡
−
1
, and 
𝛼
𝑡
 is hyperparameters. Alternatively, we can directly sample 
𝑥
𝑡
 at any time step from 
𝑥
0
 with,

	
𝑞
​
(
𝑥
𝑡
|
𝑥
0
)
=
𝒩
​
(
𝑥
𝑡
;
𝛼
¯
𝑡
​
𝑥
0
,
(
1
−
𝛼
¯
𝑡
)
​
𝐈
)
,
		
(2)

where 
𝛼
¯
𝑡
=
∏
𝑖
=
1
𝑡
𝛼
𝑖
.

Figure 3:Illustration of the interaction between different frames to impose temporal constraints in our framework.
Figure 4:Framework of the proposed zero-shot text-guided video translation. (a) We adapt the pre-trained image diffusion model (Stable Diffusion + ControlNet) with hierarchical cross-frame constraints to render coherent frames. The red dotted lines denote the sampling process of the original image diffusion model. The black lines denote our adapted process for video translation. (b) We apply different constraints at different sampling steps.

Then in the diffusion backward process, a U-Net 
𝜖
𝜃
 is trained to predict the noise of the latent to iteratively recover 
𝑥
0
 from 
𝑥
𝑇
. Given a large 
𝑇
, 
𝑥
0
 will be completely destroyed in the forward process so that 
𝑥
𝑇
 approximates a standard Gaussian distribution. Therefore, 
𝜖
𝜃
 correspondingly learns to infer valid 
𝑥
0
 from random Gaussian noises. Once trained, we can sample 
𝑥
𝑡
−
1
 based on 
𝑥
𝑡
 with a deterministic DDIM sampling [37]:

	
𝑥
𝑡
−
1
=
𝛼
𝑡
−
1
​
𝑥
^
𝑡
→
0
⏟
predicted
​
𝑥
0
+
1
−
𝛼
𝑡
−
1
​
𝜖
𝜃
​
(
𝑥
𝑡
,
𝑡
,
𝑐
𝑝
)
⏟
direction pointing to
​
𝑥
𝑡
−
1
,
		
(3)

where 
𝑥
^
𝑡
→
0
 is the predicted 
𝑥
0
 at time step 
𝑡
,

	
𝑥
^
𝑡
→
0
=
(
𝑥
𝑡
−
1
−
𝛼
𝑡
​
𝜖
𝜃
​
(
𝑥
𝑡
,
𝑡
,
𝑐
𝑝
)
)
/
𝛼
𝑡
,
		
(4)

and 
𝜖
𝜃
​
(
𝑥
𝑡
,
𝑡
,
𝑐
𝑝
)
 is the predicted noise of 
𝑥
𝑡
 based on the time step 
𝑡
 and the text prompt condition 
𝑐
𝑝
.

During inference, we can sample a valid 
𝑥
0
 from the standard Guassian noise 
𝑥
𝑇
=
𝑧
𝑇
,
𝑧
𝑇
∼
𝒩
​
(
0
,
𝐈
)
 with DDIM sampling, and decode 
𝑥
0
 to the final generated image 
𝐼
′
=
𝒟
​
(
𝑥
0
)
.

ControlNet

Although flexible, natural language has limited spatial control over the output. To improve spatial controllability, [45] introduce a side path called ControlNet to Stable Diffusion to accept extra conditions like edges, depth and human pose. Let 
𝑐
𝑓
 be the extra condition, the noise prediction of U-Net with ControlNet becomes 
𝜖
𝜃
​
(
𝑥
𝑡
,
𝑡
,
𝑐
𝑝
,
𝑐
𝑓
)
. Compared to InstructPix2Pix, ControlNet is orthogonal to customized Stable Diffusion models. To build a general zero-shot V2V framework, we use ControlNet to provide structure guidance from the input video to improve temporal consistency.

4Zero-Shot Text-Guided Video Translation

Given a video with 
𝑁
 frames 
{
𝐼
𝑖
}
𝑖
=
0
𝑁
, our goal is to render it into a new video 
{
𝐼
𝑖
′
}
𝑖
=
0
𝑁
 in another artistic expression specified by text prompts and/or off-the-shelf customized Stable Diffusion models. Our framework consists of two parts: Key Frame Translation (Sec. 4.1) and Full Video Translation (Sec. 4.2). In the first part, we introduce four hierarchical cross-frame constraints into pre-trained image diffusion models, guiding the rendering of coherent key frames using anchor and previous key frames, as as illustrated in Fig. 3. Then in the second part, non-key frames are interpolated based on their neighboring two key frames. Thus our framework can fully exploit the relationship between different frames to enhance temporal consistency of the outputs.

Table 1:Notation summary.
Notation	Description

ℰ
, 
𝒟
 	image encoder and decoder of Stable Diffusion

ℰ
∗
	the proposed fidelity-oriented image encoder

𝐼
𝑖
	the 
𝑖
-th key frame (Sec. 4.1); the 
𝑖
-th video frame (Sec. 4.2)

𝐼
𝑖
′
	translation result of 
𝐼
𝑖
 with the proposed method

𝐼
¯
𝑖
′
	translation result of 
𝐼
𝑖
 without PA fusion (Fig. 11(b))

𝐼
~
𝑖
′
, 
𝑀
𝑖
 	result of warping 
𝐼
0
′
 and 
𝐼
𝑖
−
1
′
 to 
𝐼
𝑖
, and its occlusion mask

𝐼
𝑖
′
⁣
𝑗
	result of propagating the translated key frame 
𝐼
𝑗
′
 to 
𝐼
𝑖


𝑥
0
𝑖
	latent feature of 
𝐼
𝑖
 encoded by 
ℰ


𝑥
𝑡
𝑖
	latent feature of 
𝐼
𝑖
 at the diffusion backward denoising step 
𝑡


𝑥
^
𝑡
→
0
𝑖
	estimated 
𝑥
0
𝑖
 of 
𝐼
𝑖
 at the diffusion backward denoising step 
𝑡


𝑥
~
𝑡
𝑖
	latent feature of 
𝐼
~
𝑖
′
 at the diffusion forward sampling step 
𝑡


𝑤
𝑗
𝑖
, 
𝑀
𝑗
𝑖
 	optical flow and occlusion mask from 
𝐼
𝑗
 to 
𝐼
𝑖
4.1Key Frame Translation

Figure 4 illustrates the 
𝑇
-step sampling pipeline for the key frame translation. Following SDEdit [23], the pipeline begins with 
𝑥
𝑇
=
𝛼
¯
𝑇
​
𝑥
0
+
(
1
−
𝛼
¯
𝑇
)
​
𝑧
𝑇
,
𝑧
𝑇
∼
𝒩
​
(
0
,
𝐈
)
, the noisy latent code of the input video frame rather than the pure Gaussian noise. It enables users to determine how much detail of the input frame is preserved in the output by adjusting 
𝑇
, i.e., smaller 
𝑇
 retain more detail. Then, during sampling each frame, we use the first frame as anchor frame and its previous frame to constrain global style consistency and local temporal consistency.

Specifically, cross-frame attention [40] is applied to all sampling steps for global style consistency (Sec. 4.1.1). In addition, in early steps, we fuse the latent feature with the aligned latent feature of previous frame to achieve rough shape alignments (Sec. 4.1.2). Then in mid steps, we use the latent feature with the encoded warped anchor and previous outputs to realize fine texture alignments (Sec. 4.1.3). Finally, in late steps, we adjust the latent feature distribution for color consistency (Sec. 4.1.4). For simplicity, we will use 
{
𝐼
𝑖
}
𝑖
=
0
𝑁
 to refer to the key frames in this section. We summarize important notations in Table 1.

4.1.1Style-aware cross-frame attention

Similar to other zero-shot video editing methods [20, 3], we replace self-attention layers in the U-Net with cross-frame attention layers to regularize the global style of 
𝐼
𝑖
′
 to match that of 
𝐼
1
′
 and 
𝐼
𝑖
−
1
′
. In Stable Diffusion, each self-attention layer receives the latent feature 
𝑣
𝑖
 (for simplicity we omit the time step 
𝑡
) of 
𝐼
𝑖
, and linearly projects 
𝑣
𝑖
 into query, key and value 
𝑄
, 
𝐾
, 
𝑉
 to produce the output by 
Self_Attn
​
(
𝑄
,
𝐾
,
𝑉
)
=
Softmax
​
(
𝑄
​
𝐾
𝑇
𝑑
)
⋅
𝑉
 with

	
𝑄
=
𝑊
𝑄
​
𝑣
𝑖
,
𝐾
=
𝑊
𝐾
​
𝑣
𝑖
,
𝑉
=
𝑊
𝑉
​
𝑣
𝑖
,
		
(5)

where 
𝑊
𝑄
, 
𝑊
𝐾
, 
𝑊
𝑉
 are pre-trained matrices for feature projection. Cross-frame attention, by comparison, uses the key 
𝐾
′
 and value 
𝑉
′
 from other frames (we use the first and previous frames), i.e., 
CrossFrame_Attn
​
(
𝑄
,
𝐾
′
,
𝑉
′
)
=
Softmax
​
(
𝑄
​
𝐾
′
⁣
𝑇
𝑑
)
⋅
𝑉
′
 with

	
𝑄
=
𝑊
𝑄
​
𝑣
𝑖
,
𝐾
′
=
𝑊
𝐾
​
[
𝑣
1
;
𝑣
𝑖
−
1
]
,
𝑉
′
=
𝑊
𝑉
​
[
𝑣
1
;
𝑣
𝑖
−
1
]
.
		
(6)

Intuitively, self-attention can be thought as patch matching and voting within a single frame, while cross-frame attention seeks similar patches and fuses the corresponding patches from other frames, meaning the style of 
𝐼
𝑖
′
 will inherit that of 
𝐼
1
′
 and 
𝐼
𝑖
−
1
′
.

4.1.2Shape-aware cross-frame latent fusion

Cross-frame attention is limited to global style. To constrain the cross-frame local shape and texture consistency, we use optical flow to warp and fuse the latent features. Let 
𝑤
𝑗
𝑖
 and 
𝑀
𝑗
𝑖
 denote the optical flow and occlusion mask from 
𝐼
𝑗
 to 
𝐼
𝑖
, respectively. Let 
𝑥
𝑡
𝑖
 be the latent feature for 
𝐼
𝑖
′
 at time step 
𝑡
. We update the predicted 
𝑥
^
𝑡
→
0
 in Eq. (3) by

	
𝑥
^
𝑡
→
0
𝑖
←
𝑀
𝑗
𝑖
⋅
𝑥
^
𝑡
→
0
𝑖
+
(
1
−
𝑀
𝑗
𝑖
)
⋅
𝑤
𝑗
𝑖
​
(
𝑥
^
𝑡
→
0
𝑗
)
.
		
(7)

𝑤
 and 
𝑀
 are downsampled to match the resolution of 
𝑥
 (we omit the downsampling operation for simplicity in this paper). For the reference frame 
𝐼
𝑗
, we experimentally find that the anchor frame (
𝑗
=
0
) provides better guidance than the previous frame (
𝑗
=
𝑖
−
1
). We observe that interpolating elements in the latent space can lead to blurring and shape distortion in the late steps. Therefore, we limit the fusion to only early steps for rough shape guidance.

Figure 5:Fidelity-oriented image encoding.
Figure 6:Pipeline of the fidelity-oriented image encoding.
4.1.3Pixel-aware cross-frame latent fusion

To constrain the low-level texture features in mid steps, instead warping the latent feature, we can alternatively warp previous frames and encode them back to the latent space for fusion in an inpainting manner. However, the lossy autoencoder introduces distortions and color bias that easily accumulate along the frame sequence. Figure 5(b) shows an example of the distorted result after encoding and decoding 10 times. [1] solved this problem by fine-tuning the decoder’s weights to fit each image, which is impractical for long videos. To efficiently solve this problem, we propose a novel fidelity-oriented zero-shot image encoding method.

Fidelity-oriented image encoding

Our key insight is the observation that the amount of information lost each time in the iterative auto-encoding process is consistent. Therefore, we can predict the information loss for compensation. Specifically, for arbitrary image 
𝐼
, we encode and decode it twice, obtaining 
𝑥
0
𝑟
=
ℰ
​
(
𝐼
)
,
𝐼
𝑟
=
𝒟
​
(
𝑥
0
𝑟
)
 and 
𝑥
0
𝑟
​
𝑟
=
ℰ
​
(
𝐼
𝑟
)
,
𝐼
𝑟
​
𝑟
=
𝒟
​
(
𝑥
0
𝑟
​
𝑟
)
. We assume the loss from the target lossless 
𝑥
0
 to 
𝑥
0
𝑟
 is linear to that from 
𝑥
0
𝑟
 to 
𝑥
0
𝑟
​
𝑟
. Then we define the encoding 
ℰ
′
 with compensation as

	
ℰ
′
​
(
𝐼
)
:=
𝑥
0
𝑟
+
𝜆
ℰ
​
(
𝑥
0
𝑟
−
𝑥
0
𝑟
​
𝑟
)
,
		
(8)

where we find the linear coefficient 
𝜆
ℰ
=
1
 works well. We further add a mask 
𝑀
ℰ
 to prevent the possible artifacts introduced by compensation (e.g., blue artifact near the eyes in Fig. 5(c)). 
𝑀
ℰ
 indicates where the error between 
𝐼
 and 
𝒟
​
(
ℰ
′
​
(
𝐼
)
)
 is under a pre-defined threshold. Then, our novel fidelity-oriented image encoding 
ℰ
∗
 takes the form of

	
ℰ
∗
​
(
𝐼
)
:=
𝑥
0
𝑟
+
𝑀
ℰ
⋅
𝜆
ℰ
​
(
𝑥
0
𝑟
−
𝑥
0
𝑟
​
𝑟
)
.
		
(9)

The encoding pipeline is summarized in Fig. 6. As shown in Fig. 5(d), our method preserves image information well even after encoding and decoding 10 times.

Figure 7:Pipeline of the pixel-aware latent fusion.
Structure-guided inpainting

As illustrated in Fig. 7, for pixel-level coherence, we warp the anchor frame 
𝐼
0
′
 and the previous frame 
𝐼
𝑖
−
1
′
 to the 
𝑖
-th frame and overlay them on a rough rendered frame 
𝐼
¯
𝑖
′
 obtained without the pixel-aware cross-frame latent fusion as

	
𝑀
0
𝑖
⋅
(
𝑀
𝑖
−
1
𝑖
⋅
𝐼
¯
𝑖
′
+
(
1
−
𝑀
𝑖
−
1
𝑖
)
⋅
𝑤
𝑖
−
1
𝑖
​
(
𝐼
𝑖
−
1
′
)
)
+
(
1
−
𝑀
0
𝑖
)
⋅
𝑤
0
𝑖
​
(
𝐼
0
′
)
		
(10)

The resulting fused frame 
𝐼
~
𝑖
′
 provides pixel reference for the sampling of 
𝐼
𝑖
′
, i.e., we would like 
𝐼
𝑖
′
 to match 
𝐼
~
𝑖
′
 outside the mask area 
𝑀
𝑖
=
𝑀
0
𝑖
∩
𝑀
𝑖
−
1
𝑖
 and to match the structure guidance from ControlNet inside 
𝑀
𝑖
. We formulate it as a structure-guided inpainting task and follow [1] to update 
𝑥
𝑡
−
1
𝑖
 in Eq. (3) as

	
𝑥
𝑡
−
1
𝑖
←
𝑀
𝑖
⋅
𝑥
𝑡
−
1
𝑖
+
(
1
−
𝑀
𝑖
)
⋅
𝑥
~
𝑡
−
1
𝑖
,
		
(11)

where 
𝑥
~
𝑡
−
1
𝑖
 is the sampled 
𝑥
𝑡
−
1
 from 
𝑥
0
=
ℰ
∗
​
(
𝐼
~
𝑖
′
)
 based on Eq. (2).

4.1.4Color-aware adaptive latent adjustment

Finally, we apply AdaIN [18] to 
𝑥
^
𝑡
→
0
𝑖
 to match its channel-wise mean and variance to 
𝑥
^
𝑡
→
0
1
 in the late steps. It can further keep the color style coherent throughout the whole key frames.

4.2Full Video Translation

For frames with similar content, existing frame interpolation methods like Ebsynth  [19] can generate plausible results by propagating the rendered frames to their neighbors efficiently. However, compared to diffusion models, frame interpolation cannot create new content. To balance between quality and efficiency, we propose a hybrid framework to render key frames and other frames with the adapted diffusion model and Ebsynth, respectively.

Specifically, we sample the key frames uniformly for every 
𝐾
 frame, i.e., 
𝐼
0
,
𝐼
𝐾
,
𝐼
2
​
𝐾
,
…
 and render them to 
𝐼
0
′
,
𝐼
𝐾
′
,
𝐼
2
​
𝐾
′
,
…
 by our adapted diffusion model. We then render the remaining non-key frames. Taking 
𝐼
𝑖
 (
0
<
𝑖
<
𝐾
) for example, we adopt Ebsynth to interpolate 
𝐼
𝑖
′
 with its neighboring stylized key frames 
𝐼
0
′
 and 
𝐼
𝐾
′
. Ebsynth has two steps of frame propagation and frame blending. In the following, we will briefly introduce the main idea of these two steps and discuss how we adapt Ebsynth to our framework. For implementation details, please refer to [19].

4.2.1Single key frame propagation

Frame propagation aims to warp the stylized key frame to its neighboring non-key frames based on their dense correspondences. We directly follow Ebsynth to adopt a guided path-matching algorithm with color, positional, edge, and temporal guidance for dense correspondence prediction and frame warping. Our framework propagates each key frame to its preceding 
𝐾
−
1
 and succeeding 
𝐾
−
1
 frames. We denote the result of propagating 
𝐼
𝑗
′
 to 
𝐼
𝑖
 as 
𝐼
𝑖
′
⁣
𝑗
. For 
𝐼
𝑖
 (
0
<
𝑖
<
𝐾
), we will obtain two results 
𝐼
𝑖
′
⁣
0
 and 
𝐼
𝑖
′
⁣
𝐾
 from its nearby key frames 
𝐼
0
′
 and 
𝐼
𝐾
′
.

4.2.2Temporal-aware blending

Frame blending aims to blend 
𝐼
𝑖
′
⁣
0
 and 
𝐼
𝑖
′
⁣
𝐾
 to a final result 
𝐼
𝑖
′
. Ebsynth proposes a three-step blending scheme: 1) Combining colors and gradients of 
𝐼
𝑖
′
⁣
0
 and 
𝐼
𝑖
′
⁣
𝐾
 by selecting the ones with lower errors during patch matching (Sec. 4.2.1) for each location; 2) Using the combined color image as a histogram reference for contrast-preserving blending [11] over 
𝐼
𝑖
′
⁣
0
 and 
𝐼
𝑖
′
⁣
𝐾
 to generate an initial blended image; 3) Employing the combined gradient as a gradient reference for screened Poisson blending [5] over the initial blended image to obtain the final result. Differently, our framework only adopts the first two blending steps and uses the initial blended image as 
𝐼
𝑖
′
. We do not apply Poisson blending, which we find sometimes causes artifacts in non-flat regions and is relatively time-consuming.

Figure 8:Visual comparison with zero-shot video translation methods. The magenta box indicates the inconsistent region. For Text2Video-Zero and our method, we further enlarge the region to better visualize the pixel-level consistency.
5Experimental Results
5.1Implementation Details

The experiment is conducted on one NVIDIA Tesla V100 GPU. We employ the fine-tuned and LoRA models based on Stable Diffusion 1.5 from https://civitai.com/. We use Stable Diffusion originally uses 
𝑇
𝑚
​
𝑎
​
𝑥
=
1000
 steps. For the sampling pipeline in Fig. 4(b), by default, we set 
𝑇
𝑠
=
0.1
​
𝑇
𝑚
​
𝑎
​
𝑥
, 
𝑇
𝑝
​
0
=
0.5
​
𝑇
𝑚
​
𝑎
​
𝑥
, 
𝑇
𝑝
​
1
=
0.8
​
𝑇
𝑚
​
𝑎
​
𝑥
 and 
𝑇
𝑎
=
0.8
​
𝑇
𝑚
​
𝑎
​
𝑥
 and use 20 steps of DDIM sampling. We tune 
𝑇
 for each video. ControlNet [45] is used to provide structure guidance in terms of edges, with the control weight tuned for each video. We use GMFlow [41] for optical flow estimation and compute the occlusion masks by forward-backward consistency check. For full video translation, by default, we sample key frames for every 
𝐾
=
10
 frames. The testing videos are from https://www.pexels.com/ and https://pixabay.com/, with their short side resized to 512.

In terms of running time for 512
×
512 videos, key frame and non-key frame translations take about 14.23s and 1.49s per frame, respectively. Overall, a full video translation takes about 
(
14.23
+
1.49
​
(
𝐾
−
1
)
)
/
𝐾
=
1.49
+
12.74
/
𝐾
s per frame.

We will release our code upon publication of the paper.

5.2Comparison with State-of-the-Art Methods

We compare with four recent zero-shot methods: vid2vid-zero [39], FateZero [27], Pix2Video [3], Text2Video-Zero [20] on key frame translation with 
𝐾
=
5
. The official code of the first three methods does not support ControlNet, and when loading customized models, we find they fail to generate plausible results, e.g., vid2vid-zero will generate frames totally different from the input. Therefore, only Text2Video-Zero and our method use the customized model with ControlNet. Figure 8 and Figure 9 present the visual results. FateZero successfully reconstructs the input frame but fails to adjust it to match the prompt. On the other hand, vid2vid-zero and Pix2Video excessively modify the input frame, leading to significant shape distortion and discontinuity across frames. While each frame generated by Text2Video-Zero exhibits high quality, they lack coherence in local textures as indicated by the black boxes. Finally, our proposed method demonstrates clear superiority in terms of output quality, content and prompt matching and temporal consistency.

For quantitative evaluation, we follow FateZero and Pix2Video to report Fram-Acc (CLIP-based frame-wise editing accuracy), Tmp-Con (CLIP-based cosine similarity between consecutive frames), Pixel-MSE (averaged mean-squared pixel error between aligned consecutive frames) in Table 2. Our method achieves the best temporal consistency and the second best frame editing accuracy. We further conduct a user study with 30 participants. The participants are asked to select the best results among the five methods based on three criteria: 1) how well the result balance between the prompt and the input frame, 2) the temporal consistency of the result, and 3) the overall quality of the video translation. Table 2 presents the average preference rates across 8 testing videos, and our method achieves the highest rates in all three metrics.

Table 2:Quantitative comparison and user preference rates.
Metric	v2v-zero	FateZero	Pix2Video	T2V-Zero	Ours
Fram-Acc	0.862	0.556	0.995	0.963	0.979
Tem-Con	0.975	0.979	0.953	0.983	0.983
Pixel-MSE	0.098	0.085	0.216	0.084	0.069
User-Balance	3.8%	5.9%	9.2%	15.4%	65.8%
User-Temporal	3.8%	9.6%	4.2%	10.8%	71.6%
User-Overall	2.9%	4.2%	4.2%	15.0%	73.7%
Figure 9:Visual comparison with Text2Video-Zero. Text2Video-Zero and our method use the same customized model and ControlNet for a fair comparison. Our method outperforms Text2Video-Zero in terms of local texture temporal consistency. The red box indicates the inconsistent region.
Figure 10:Effect of the proposed hierarchical cross-frame constraints. (a) Input frames #1, #55, #94. (b) Image diffusion model renders each frame independently. (c) Cross frame attention keeps the overall style consistent. (d) AdaIN preserves the hair color. (e) Shape-aware latent fusion keeps the overall movement of the objects coherent. (f) Pixel-aware latent fusion achieves pixel-level temporal consistency.
5.3Ablation Study
Hierarchical cross-frame consistency constraints

Figure 10 compares the results with and without different cross-frame consistency constraints. We demonstrate the efficacy of our approach on a video containing simple translational motion in the first half and complex 3D rotation transformations in the latter half. To better evaluate the temporal consistency, we encourage readers to watch the videos on the project webpage. The cross-frame attention ensures consistency in global style, while the adaptive latent adjustment in Sec. 4.1.4 maintains the same hair color as the first frame, or the hair color will follow the input frame to turn dark. Note that the adaptive latent adjustment is optional to allow users to decide which color to follow. The above two global constraints cannot capture local movement. The shape-aware latent fusion (SA fusion) in Sec. 4.1.2 addresses this by translating the latent features to translate the neck ring, but cannot maintain pixel-level consistency for complex motion. Only the proposed pixel-aware latent fusion (PA fusion) can coherently render local details such as hair styles and acne.

We provide additional examples in Figs. 11-12 to demonstrate the effectiveness of PA fusion. While ControlNet can guide the structure well, the inherent randomness introduced by noise addition and denoising makes it difficult to maintain coherence in local textures, resulting in missing elements and altered details. The proposed PA fusion restores these details by utilizing the corresponding pixel information from previous frames. Moreover, such consistency between key frames can effectively reduce the ghosting artifacts in interpolated non key frames.

Figure 11:Effect of the pixel-aware latent fusion on frame propagation. The proposed pixel-aware latent fusion helps generate consistent key frames. Without it, the pixel level inconsistency between key frames leads to ghosting artifacts on the non-key frames during the frame blending.
Figure 12:Effect of the pixel-aware latent fusion. Prompts (from top to bottom): ‘Arcane style, a handsome man’, ‘Loving Vincent, hiking, grass’, ‘Disco Elysium, street view’. Local regions are enlarged and shown in the top right.
Figure 13:The fidelity-oriented image encoding on two VAEs.
Figure 14:Quantitative evaluation of image encoding schemes.
Fidelity-oriented image encoding

We present a detailed analysis of our fidelity-oriented image encoding in Figs. 13-15, in addition to Fig. 5. Two Stable Diffusion’s officially released autoencoders, the fine-tuned f8-ft-MSE VAE and the original more lossy kl-f8 VAE, are used for testing our method. The fine-tuned VAE introduces artifacts and the original VAE results in great color bias as in Fig. 13(b). Our proposed fidelity-oriented image encoding effectively alleviates these issues. For quantitative evaluation, we report the MSE between the input image and the reconstructed result after multiple encoding and decoding in Fig. 14, using the first 1,000 images of the MS-COCO [21] validation set. The results are consistent with the visual observations: our proposed method significantly reduces error accumulation compared to raw encoding methods. Finally, we validate our encoding method in the video translation process in Fig. 15(b)(c), where we use only the previous frame without the anchor frame in Eq. (10) to better visualize error accumulation. Our method mostly reduces the loss of details and color bias caused by lossy encoding. Besides, our pipeline includes an anchor frame and adaptive latent adjustment to further regulate the translation, as shown in Fig. 15(d), where no obvious errors are observed.

Figure 15:Different constraints to prevent error accumulation.
Frequency of key frames 
𝐾

We report the quantitative full video translation results of Fig. 10(a) under different 
𝐾
 in Table 3. With large 
𝐾
, more frame interpolation improves pixel-level temporal consistency, which however harms the quality, leading to low Fram-Acc. A broad range of 
𝐾
∈
[
5
,
20
]
 is recommended for balance.

Table 3:Effect of key frame sampling interval 
𝐾
Metric	
𝐾
=
1
	
𝐾
=
5
	
𝐾
=
10
	
𝐾
=
20
	
𝐾
=
50
	
𝐾
=
100

Fram-Acc	1.000	1.000	1.000	1.000	0.990	0.890
Tem-Con	0.992	0.993	0.994	0.994	0.993	0.993
Pixel-MSE	0.037	0.028	0.025	0.022	0.020	0.020
Figure 16:Effect of the initialization of 
𝑥
𝑇
. Prompt: a traditional mountain in Chinese ink wash painting. The proposed framework enables flexible content and color control by adjusting 
𝑇
 and color correction.
5.4More Results
Flexible structure and color control

The proposed pipeline allows flexible control over content preservation through the initialization of 
𝑥
𝑇
. Rather than setting 
𝑥
𝑇
 to a Gaussian noise (Fig. 16(b)), we use a noisy latent version of the input frame to better preserve details (Fig. 16(c)). Users can adjust the value of 
𝑇
 to balance content and prompt. Moreover, if the input frame introduces unwanted color bias (e.g., blue sky in Chinese ink painting), a color correction option is provided: the input frame is adjusted to match the color histogram of the frame generated by 
𝑥
𝑇
=
𝑧
𝑇
 (Fig. 16(b)). With the adjusted frame as input (bottom row of Fig. 16(a)), the rendered results (bottom row of Figs. 16(c)-(f)) better match the color indicated by the prompt.

Figure 17:Applications of the proposed method.
Figure 18:Applications: text-guided virtual character generation. Results are generated with a single image diffusion model.
Figure 19:Applications: video stylization. Thanks to the compatible design, our method can use off-the-shelf pre-trained image models customized for different styles to accurately stylize videos.
Applications

Figure 17 shows some applications of our method. With prompts ‘a cute cat/fox/hamster/rabbit’, we can perform text-guided editing to translate a dog into other kinds of pets in Fig. 17(a). By using customized modes for generating cartoons or photos, we can achieve non-photorealistic and photorealistic rendering in Fig. 17(b) and Figs. 17(c)(d), respectively. In Fig. 18, we present our synthesized dynamic virtual characters of novels and manga, based on a real human video and a prompt to describe the appearance. Additional results are shown in Fig. 19.

5.5Limitations

Figures 20-22 illustrate typical failure cases of our method. First, our method relies on optical flow and therefore, inaccurate optical flow can lead to artifacts. In Fig. 20, our method can only preserve the embroidery if the cross-frame correspondence is available. Otherwise, the proposed PA fusion will have no effect. Second, our method assumes the optical flow remains unchanged before and after translation, which may not hold true for significant appearance changes as in Fig. 21(b), where the resulting movement may be wrong. Although setting a smaller 
𝑇
 can address this issue, it may compromise the desired styles. Meanwhile, the mismatches of the optical flow mean the mismatches in the translated key frames, which may lead to ghosting artifacts (Fig. 21(d)) after temporal-aware blending. Also, we find that small details and subtle motions like accessories and eye movement cannot be well preserved during the translation. Lastly, we uniformly sample the key frames, which may not optimal. Ideally, the key frames should contain all unique objects; otherwise, the propagation cannot create unseen content such as the hand in Fig. 22(b). One potential solution is user-interactive translation, where users can manually assign new key frames based on the previous results.

Figure 20:Limitation: failure optical flow due to large motions. Our method is not suitable for processing videos where it is difficult to estimate the optical flow.
Figure 21:Limitation: trade-off between content and prompt.
Figure 22:Limitation: failed propagation w/o good key frames.
6Conclusion

This paper presents a zero-shot framework to adapt image diffusion models for video translation. Our method utilizes hierarchical cross-frame constraints to enforce temporal consistency in both global style and low-level textures, leveraging the key optical flow. The compatibility with existing image diffusion techniques indicates that our idea might be applied to other text-guided video editing tasks, such as video super-resolution and inpainting. Additionally, our proposed fidelity-oriented image encoding could benefit existing diffusion-based methods. We believe that our approach can facilitate the creation of high-quality and temporally-coherent videos and inspire further research in this field.

Acknowledgments. This study is supported under the RIE2020 Industry Alignment Fund Industry Collaboration Projects (IAF-ICP) Funding Initiative, as well as cash and in-kind contribution from the industry partner(s). It is also supported by Singapore MOE AcRF Tier 2 (MOE-T2EP20221-0011, MOE-T2EP20221-0012) and NTU NAP.

References
[1]	Omri Avrahami, Ohad Fried, and Dani Lischinski.Blended latent diffusion.arXiv preprint arXiv:2206.02779, 2022.
[2]	Tim Brooks, Aleksander Holynski, and Alexei A Efros.InstructPix2Pix: Learning to follow image editing instructions.arXiv preprint arXiv:2211.09800, 2022.
[3]	Duygu Ceylan, Chun-Hao Paul Huang, and Niloy J Mitra.Pix2video: Video editing using image diffusion.arXiv preprint arXiv:2303.12688, 2023.
[4]	Florinel-Alin Croitoru, Vlad Hondru, Radu Tudor Ionescu, and Mubarak Shah.Diffusion models in vision: A survey.IEEE Transactions on Pattern Analysis and Machine Intelligence, 2023.
[5]	Soheil Darabi, Eli Shechtman, Connelly Barnes, Dan B Goldman, and Pradeep Sen.Image melding: Combining inconsistent images using patch-based synthesis.ACM Transactions on Graphics, 31(4):82–1, 2012.
[6]	Ming Ding, Zhuoyi Yang, Wenyi Hong, Wendi Zheng, Chang Zhou, Da Yin, Junyang Lin, Xu Zou, Zhou Shao, Hongxia Yang, et al.Cogview: Mastering text-to-image generation via transformers.In Advances in Neural Information Processing Systems, volume 34, pages 19822–19835, 2021.
[7]	Patrick Esser, Robin Rombach, and Bjorn Ommer.Taming transformers for high-resolution image synthesis.In Proc. IEEE Int’l Conf. Computer Vision and Pattern Recognition, pages 12873–12883, 2021.
[8]	Jakub Fišer, Ondřej Jamriška, David Simons, Eli Shechtman, Jingwan Lu, Paul Asente, Michal Lukáč, and Daniel Sỳkora.Example-based synthesis of stylized facial animations.ACM Transactions on Graphics (TOG), 36(4):1–11, 2017.
[9]	Oran Gafni, Adam Polyak, Oron Ashual, Shelly Sheynin, Devi Parikh, and Yaniv Taigman.Make-a-scene: Scene-based text-to-image generation with human priors.In Proc. European Conf. Computer Vision, pages 89–106. Springer, 2022.
[10]	Rinon Gal, Yuval Alaluf, Yuval Atzmon, Or Patashnik, Amit H Bermano, Gal Chechik, and Daniel Cohen-Or.An image is worth one word: Personalizing text-to-image generation using textual inversion.arXiv preprint arXiv:2208.01618, 2022.
[11]	Eric Heitz and Fabrice Neyret.High-performance by-example noise using a histogram-preserving blending operator.Proceedings of the ACM on Computer Graphics and Interactive Techniques, 1(2):1–25, 2018.
[12]	Amir Hertz, Ron Mokady, Jay Tenenbaum, Kfir Aberman, Yael Pritch, and Daniel Cohen-Or.Prompt-to-prompt image editing with cross attention control.arXiv preprint arXiv:2208.01626, 2022.
[13]	Aaron Hertzmann, Charles E. Jacobs, Nuria Oliver, Brian Curless, and David H. Salesin.Image analogies.In Proc. Conf. Computer Graphics and Interactive Techniques, pages 327–340, 2001.
[14]	Jonathan Ho, William Chan, Chitwan Saharia, Jay Whang, Ruiqi Gao, Alexey Gritsenko, Diederik P Kingma, Ben Poole, Mohammad Norouzi, David J Fleet, et al.Imagen video: High definition video generation with diffusion models.arXiv preprint arXiv:2210.02303, 2022.
[15]	Jonathan Ho, Ajay Jain, and Pieter Abbeel.Denoising diffusion probabilistic models.In Advances in Neural Information Processing Systems, volume 33, pages 6840–6851, 2020.
[16]	Jonathan Ho, Tim Salimans, Alexey A Gritsenko, William Chan, Mohammad Norouzi, and David J Fleet.Video diffusion models.In Advances in Neural Information Processing Systems, 2022.
[17]	Edward J Hu, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, Weizhu Chen, et al.Lora: Low-rank adaptation of large language models.In Proc. Int’l Conf. Learning Representations, 2021.
[18]	Xun Huang and Serge Belongie.Arbitrary style transfer in real-time with adaptive instance normalization.In Proc. Int’l Conf. Computer Vision, pages 1510–1519, 2017.
[19]	Ondřej Jamriška, Šárka Sochorová, Ondřej Texler, Michal Lukáč, Jakub Fišer, Jingwan Lu, Eli Shechtman, and Daniel Sỳkora.Stylizing video by example.ACM Transactions on Graphics, 38(4):1–11, 2019.
[20]	Levon Khachatryan, Andranik Movsisyan, Vahram Tadevosyan, Roberto Henschel, Zhangyang Wang, Shant Navasardyan, and Humphrey Shi.Text2video-zero: Text-to-image diffusion models are zero-shot video generators.arXiv preprint arXiv:2303.13439, 2023.
[21]	Tsung-Yi Lin, Michael Maire, Serge Belongie, James Hays, Pietro Perona, Deva Ramanan, Piotr Dollár, and C Lawrence Zitnick.Microsoft coco: Common objects in context.In Proc. European Conf. Computer Vision, pages 740–755. Springer, 2014.
[22]	Shaoteng Liu, Yuechen Zhang, Wenbo Li, Zhe Lin, and Jiaya Jia.Video-p2p: Video editing with cross-attention control.arXiv preprint arXiv:2303.04761, 2023.
[23]	Chenlin Meng, Yutong He, Yang Song, Jiaming Song, Jiajun Wu, Jun-Yan Zhu, and Stefano Ermon.Sdedit: Guided image synthesis and editing with stochastic differential equations.In Proc. Int’l Conf. Learning Representations, 2021.
[24]	Ron Mokady, Amir Hertz, Kfir Aberman, Yael Pritch, and Daniel Cohen-Or.Null-text inversion for editing real images using guided diffusion models.arXiv preprint arXiv:2211.09794, 2022.
[25]	Eyal Molad, Eliahu Horwitz, Dani Valevski, Alex Rav Acha, Yossi Matias, Yael Pritch, Yaniv Leviathan, and Yedid Hoshen.Dreamix: Video diffusion models are general video editors.arXiv preprint arXiv:2302.01329, 2023.
[26]	Alexander Quinn Nichol, Prafulla Dhariwal, Aditya Ramesh, Pranav Shyam, Pamela Mishkin, Bob Mcgrew, Ilya Sutskever, and Mark Chen.Glide: Towards photorealistic image generation and editing with text-guided diffusion models.In Proc. IEEE Int’l Conf. Machine Learning, pages 16784–16804, 2022.
[27]	Chenyang Qi, Xiaodong Cun, Yong Zhang, Chenyang Lei, Xintao Wang, Ying Shan, and Qifeng Chen.Fatezero: Fusing attentions for zero-shot text-based video editing.arXiv preprint arXiv:2303.09535, 2023.
[28]	Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, et al.Learning transferable visual models from natural language supervision.In Proc. IEEE Int’l Conf. Machine Learning, pages 8748–8763. PMLR, 2021.
[29]	Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael Matena, Yanqi Zhou, Wei Li, and Peter J Liu.Exploring the limits of transfer learning with a unified text-to-text transformer.The Journal of Machine Learning Research, 21(1):5485–5551, 2020.
[30]	Aditya Ramesh, Prafulla Dhariwal, Alex Nichol, Casey Chu, and Mark Chen.Hierarchical text-conditional image generation with clip latents.arXiv preprint arXiv:2204.06125, 2022.
[31]	Aditya Ramesh, Mikhail Pavlov, Gabriel Goh, Scott Gray, Chelsea Voss, Alec Radford, Mark Chen, and Ilya Sutskever.Zero-shot text-to-image generation.In Proc. IEEE Int’l Conf. Machine Learning, pages 8821–8831, 2021.
[32]	Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, and Björn Ommer.High-resolution image synthesis with latent diffusion models.In Proc. IEEE Int’l Conf. Computer Vision and Pattern Recognition, pages 10684–10695, 2022.
[33]	Nataniel Ruiz, Yuanzhen Li, Varun Jampani, Yael Pritch, Michael Rubinstein, and Kfir Aberman.Dreambooth: Fine tuning text-to-image diffusion models for subject-driven generation.arXiv preprint arXiv:2208.12242, 2022.
[34]	Chitwan Saharia, William Chan, Saurabh Saxena, Lala Li, Jay Whang, Emily L Denton, Kamyar Ghasemipour, Raphael Gontijo Lopes, Burcu Karagol Ayan, Tim Salimans, et al.Photorealistic text-to-image diffusion models with deep language understanding.In Advances in Neural Information Processing Systems, volume 35, pages 36479–36494, 2022.
[35]	Chaehun Shin, Heeseung Kim, Che Hyun Lee, Sang-gil Lee, and Sungroh Yoon.Edit-a-video: Single video editing with object-aware consistency.arXiv preprint arXiv:2303.07945, 2023.
[36]	Uriel Singer, Adam Polyak, Thomas Hayes, Xi Yin, Jie An, Songyang Zhang, Qiyuan Hu, Harry Yang, Oron Ashual, Oran Gafni, et al.Make-a-video: Text-to-video generation without text-video data.In Proc. Int’l Conf. Learning Representations, 2023.
[37]	Jiaming Song, Chenlin Meng, and Stefano Ermon.Denoising diffusion implicit models.In Proc. Int’l Conf. Learning Representations, 2021.
[38]	Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin.Attention is all you need.In Advances in Neural Information Processing Systems, volume 30, 2017.
[39]	Wen Wang, Kangyang Xie, Zide Liu, Hao Chen, Yue Cao, Xinlong Wang, and Chunhua Shen.Zero-shot video editing using off-the-shelf image diffusion models.arXiv preprint arXiv:2303.17599, 2023.
[40]	Jay Zhangjie Wu, Yixiao Ge, Xintao Wang, Weixian Lei, Yuchao Gu, Wynne Hsu, Ying Shan, Xiaohu Qie, and Mike Zheng Shou.Tune-a-video: One-shot tuning of image diffusion models for text-to-video generation.arXiv preprint arXiv:2212.11565, 2022.
[41]	Haofei Xu, Jing Zhang, Jianfei Cai, Hamid Rezatofighi, and Dacheng Tao.Gmflow: Learning optical flow via global matching.In Proc. IEEE Int’l Conf. Computer Vision and Pattern Recognition, pages 8121–8130, 2022.
[42]	Tao Xu, Pengchuan Zhang, Qiuyuan Huang, Han Zhang, Zhe Gan, Xiaolei Huang, and Xiaodong He.Attngan: Fine-grained text to image generation with attentional generative adversarial networks.In Proc. IEEE Int’l Conf. Computer Vision and Pattern Recognition, pages 1316–1324, 2018.
[43]	Han Zhang, Jing Yu Koh, Jason Baldridge, Honglak Lee, and Yinfei Yang.Cross-modal contrastive learning for text-to-image generation.In Proc. IEEE Int’l Conf. Computer Vision and Pattern Recognition, pages 833–842, 2021.
[44]	Han Zhang, Tao Xu, Hongsheng Li, Shaoting Zhang, Xiaogang Wang, Xiaolei Huang, and Dimitris N Metaxas.StackGAN: Text to photo-realistic image synthesis with stacked generative adversarial networks.In Proceedings of the IEEE international conference on computer vision, pages 5907–5915, 2017.
[45]	Lvmin Zhang and Maneesh Agrawala.Adding conditional control to text-to-image diffusion models.arXiv preprint arXiv:2302.05543, 2023.
[46]	Minfeng Zhu, Pingbo Pan, Wei Chen, and Yi Yang.DM-GAN: Dynamic memory generative adversarial networks for text-to-image synthesis.In Proc. IEEE Int’l Conf. Computer Vision and Pattern Recognition, pages 5802–5810, 2019.
◄  Feeling
lucky? Conversion
report Report
an issue View original
on arXiv►
Copyright Privacy Policy Generated on Wed Feb 28 22:00:52 2024 by LaTeXML
