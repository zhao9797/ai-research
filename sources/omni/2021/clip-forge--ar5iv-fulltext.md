# [2110.02624] CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation
Source: https://ar5iv.labs.arxiv.org/html/2110.02624
[2110.02624] CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation



# CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation

Aditya Sanghi1           Hang Chu1           Joseph G. Lambourne1           Ye Wang2
  
Chin-Yi Cheng1              Marco Fumero1              Kamal Rahimi Malekshan1
  
1Autodesk AI Lab              2Autodesk Research
  
{aditya.sanghi,hang.chu,joseph.lambourne,ye.wang,chin-yi.cheng,marco.fumero,kamal.malekshan}@autodesk.com
  
 https://github.com/AutodeskAILab/Clip-Forge

###### Abstract

Generating shapes using natural language can enable new ways of imagining and creating the things around us. While significant recent progress has been made in text-to-image generation, text-to-shape generation remains a challenging problem due to the unavailability of paired text and shape data at a large scale. We present a simple yet effective method for zero-shot text-to-shape generation that circumvents such data scarcity. Our proposed method, named CLIP-Forge, is based on a two-stage training process, which only depends on an unlabelled shape dataset and a pre-trained image-text network such as CLIP. Our method has the benefits of avoiding expensive inference time optimization, as well as the ability to generate multiple shapes for a given text. We not only demonstrate promising zero-shot generalization of the CLIP-Forge model qualitatively and quantitatively, but also provide extensive comparative evaluations to better understand its behavior.

![[Uncaptioned image]](/html/2110.02624/assets/figures_arxiv/teaser.jpg)

Figure 1: We propose a zero-shot text-to-shape generation method named CLIP-Forge. Without training on any shape-text pairing labels, our method generates meaningful shapes that correctly reflect the common name, (sub-)category, and semantic attribute information.

## 1 Introduction

Generating 3D shapes from text input has been a challenging and interesting research problem with both significant scientific and applied value [[20](#bib.bib20), [35](#bib.bib35), [23](#bib.bib23), [24](#bib.bib24)].
In the artificial intelligence and cognitive science research communities, researchers have long sought to bridge the two modalities of natural language and geometric shape [[56](#bib.bib56), [4](#bib.bib4)].
In practice, text-to-shape generation models are a key enabling component to new smart tools in creative design and manufacture as well as animation and games [[7](#bib.bib7)].

Significant progress has been made to connect text and image modalities [[19](#bib.bib19), [55](#bib.bib55), [28](#bib.bib28), [27](#bib.bib27), [11](#bib.bib11), [53](#bib.bib53)]. Recently, DALL-E [[50](#bib.bib50)] and its associated pre-trained visual-textual embedding model CLIP [[49](#bib.bib49)] has shown promising results on the problem of text-to-image generation [[45](#bib.bib45)]. Notably, they have demonstrated strong zero-shot generalization while evaluated on tasks the model has not been specifically trained on. Shape generation is a more fundamental problem than image generation, because images are projections and renderings of the inherently 3D physical world. Therefore, one may wonder if the success in 2D can be transferred to the 3D domain. This turns out to be a non-trivial problem. Unlike the text-to-image case, where paired data is abundant, it is impractical to acquire huge paired datasets of texts and shapes.

Leveraging the progress of text-to-image generation, we present CLIP-Forge. As shown in Figure [2](#S1.F2 "Figure 2 ‣ 1 Introduction ‣ CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation"),
we overcome the limitation of shape-text pair data scarcity via a simple and effective approach. We exploit the fact that 3D shapes can be easily and automatically rendered into images using standard graphics pipelines. We then utilize pre-trained image-text joint embedding models such as [[49](#bib.bib49), [26](#bib.bib26)],
which bring text and image embeddings in a similar latent space so that they can be used interchangeably. Hence, we can train a model using image embeddings, but at inference time replace it with text embeddings.

In CLIP-Forge, we first obtain a latent space for shapes via training an autoencoder, and we then train a normalizing flow network [[13](#bib.bib13)] to model the distribution of shape embeddings conditioned on the image features obtained from the pre-trained image encoder [[49](#bib.bib49)].
We use the renderings of 3D shapes and hence, no labels are required for training our model.
During inference, we obtain text features of the given text query via the pre-trained text encoder. We then condition the normalizing flow network with text features to generate a shape embedding, which is converted into 3D shape through the shape decoder. In this process, CLIP-Forge requires no text labels for shapes, which means it can be extended easily to larger datasets. Since our method is fully feed-forward, it also has the advantage of avoiding the expensive inference time optimizations as employed in existing 2D approaches [[18](#bib.bib18), [57](#bib.bib57)].

![Refer to caption](/html/2110.02624/assets/figures_arxiv/concept.jpg)


Figure 2: Illustration of the main idea. It is difficult to directly learn text-to-shape generation due to the lack of paired data. Instead, we use renderings of shapes with a pre-trained image-text joint embedding model to bridge the data gap between 3D shapes and natural language.

The main contributions of this paper are as follows:

* •

  We present a new method, CLIP-Forge, that generates 3D shapes directly from text as shown in Figure [1](#S0.F1 "Figure 1 ‣ CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation"), without requiring paired text-shape labels.
* •

  Our method has an efficient generation process requiring no inference time optimization, can generate multiple shapes for a given text and can be easily extended to multiple 3D representation.
* •

  We provide extensive evaluation of our method in various zero-shot generation settings qualitatively and quantitatively.

## 2 Related Work

Zero-Shot Learning. Zero-shot learning is an important paradigm of machine learning, which typically aims to make predictions on classes that have never been observed during training, by exploiting certain external knowledge source.
The literature originates from the image classification problem [[42](#bib.bib42), [33](#bib.bib33)], and has been recently extended to generative models, in particular, the task of synthesizing images from text [[50](#bib.bib50)].
As far as our best knowledge, our method is the first to bring this paradigm to the 3D shape domain, which enables efficient shape generation from natural language text input.

Applications of CLIP. A major building block of our method is CLIP [[49](#bib.bib49)], which shows groundbreaking zero-shot capability using a mechanism to connect text and image by bringing them closer in the latent space.
Previous work such as ALIGN [[26](#bib.bib26)], has used a similar framework on noisy datasets. Recently, pre-trained CLIP has been used for several zero-shot downstream applications [[26](#bib.bib26), [16](#bib.bib16), [54](#bib.bib54), [45](#bib.bib45), [18](#bib.bib18), [41](#bib.bib41)]. The most similar previous work to ours is zero-shot image and drawing synthesis [[45](#bib.bib45), [18](#bib.bib18)]. Typically, these methods involve iteratively optimizing a random image to increase certain CLIP activations. There is still no clear way to apply them to 3D due to the significantly higher complexity. Our approach conditions a shape prior network with CLIP features, which has the advantages of significant speed-up and the capability to generate multiple shapes from a single text.

3D Shape Generation and Language.
Recently, there has been tremendous progress in 3D shape generating in different data formats such as point cloud [[3](#bib.bib3), [34](#bib.bib34), [59](#bib.bib59)], voxel [[58](#bib.bib58)], implicit representation [[37](#bib.bib37), [44](#bib.bib44), [8](#bib.bib8)] and mesh [[39](#bib.bib39)].
While our method is not limited to produce one 3D data format, we mainly adopt the implicit representation in this work due to their simplicity and superior quality.
More recently, methods that use text to localize objects in 3D scene have been explored [[6](#bib.bib6), [2](#bib.bib2)].
A metric learning method for text-to-shape generation is presented in [[7](#bib.bib7)].
The main difference and advantage of our approach is its zero-shot capability which requires no text-shape labels.

Multi-Stage Training. In this work we follow a multi-stage training approach, where we first learn the embeddings of the target data and then learn a probabilistic encoding model for the learned embeddings. Such an approach as been explored in image generation [[40](#bib.bib40), [36](#bib.bib36), [15](#bib.bib15)] and 3D shape generation [[3](#bib.bib3), [8](#bib.bib8)]. Concretely for CLIP-Forge, we first train a 3D shape autoencoder and then model the embeddings using normalizing flow.

![Refer to caption](/html/2110.02624/assets/figures_arxiv/diagrams.jpg)


Figure 3: An overview of the CLIP-Forge method. The top row shows the two training stages of shape autoencoder training, and the conditional normalizing flow training. The bottom row shows how text-to-shape inference is conducted.

Normalizing Flow. Generative models have extensive use cases such as content creation and editing. Flow-based generative networks [[51](#bib.bib51), [13](#bib.bib13), [12](#bib.bib12)] is able to perform exact likelihood evaluation, while being efficient to sample from.
They have been widely applied to a variety of tasks ranging from image generation [[31](#bib.bib31)], audio synthesis [[29](#bib.bib29)] and video generation [[32](#bib.bib32)]. Recently, normalizing flow has been brought to the 3D domain enabling fast generation of point clouds [[59](#bib.bib59), [47](#bib.bib47)]. In this paper, we employ a normalizing flow model [[13](#bib.bib13)] to model the conditional distribution of latent shape representations given text and image embeddings.

## 3 Method

Our method requires a collection of 3D shapes without any associated text labels, which takes the format of 𝒮={(𝐈n,𝐕n,𝐏n,𝐎n)}n=1N𝒮superscriptsubscriptsubscript𝐈𝑛subscript𝐕𝑛subscript𝐏𝑛subscript𝐎𝑛𝑛1𝑁\mathcal{S}=\{(\mathbf{I}\_{n},\mathbf{V}\_{n},\mathbf{P}\_{n},\mathbf{O}\_{n})\}\_{n=1}^{N}. Each shape in the collection 𝒮𝒮\mathcal{S} is comprised of a rendered image 𝐈nsubscript𝐈𝑛\mathbf{I}\_{n}, a voxel grid 𝐕nsubscript𝐕𝑛\mathbf{V}\_{n}, a set of query points in the 3D space 𝐏nsubscript𝐏𝑛\mathbf{P}\_{n}, and space occupancies 𝐎nsubscript𝐎𝑛\mathbf{O}\_{n}. As an overview, the CLIP-Forge training has two stages. In the first stage, we train an autoencoder with a voxel encoder and an implicit decoder. Once the autoencoder training is completed we obtain a shape embedding 𝐞nsubscript𝐞𝑛\mathbf{e}\_{n} for each 3D shape in 𝒮𝒮\mathcal{S}. In the second stage, we train a conditioned normalizing flow network to model and generate 𝐞nsubscript𝐞𝑛\mathbf{e}\_{n}, which is conditioned with image features obtained from the CLIP image encoder using 𝐈nsubscript𝐈𝑛\mathbf{I}\_{n}.
During inference, we first convert the text to the interchangeable text-image latent space using the CLIP text encoder. We then condition the normalizing flow network with the given text features and a random vector sampled from the uniform Gaussian distribution to obtain a shape embedding. Finally, this shape embedding is converted to a 3D shape using the implicit decoder. The overall architecture is shown in Figure [3](#S2.F3 "Figure 3 ‣ 2 Related Work ‣ CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation").

### 3.1 Stage 1: Shape Autoencoder

The autoencoder consists of an encoder and a decoder.
We use an encoder fVsubscript𝑓𝑉f\_{V} to extract the shape embedding 𝐞nsubscript𝐞𝑛\mathbf{e}\_{n} for the training shape collection, using 𝐕nsubscript𝐕𝑛\mathbf{V}\_{n} of resolution 323superscript32332^{3} as the input.
We use a simple voxel network that comprises of a series of batch-normalized 3D convolution layers followed by linear layers.
This can be written as:

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | 𝐞n=fV​(𝐕n)+ϵ,whereϵ∼𝒩​(0,0.1)\displaystyle\begin{split}\mathbf{e}\_{n}=f\_{V}(\mathbf{V}\_{n})+\epsilon,\quad\text{where}\quad\epsilon\sim\mathcal{N}(0,0.1)\end{split} | |  | (1) |

where 𝐞nsubscript𝐞𝑛\mathbf{e}\_{n} is augmented with a Gaussian noise. We find empirically injecting this noise improves the generation quality as later shown in the ablation study. This is also theoretically verified to improve results for conditional density estimation [[52](#bib.bib52)].
We then pass 𝐞nsubscript𝐞𝑛\mathbf{e}\_{n} through an implicit decoder. Our decoder architecture is inspired by the Occupancy Networks [[37](#bib.bib37)], which takes concatenated 𝐞nsubscript𝐞𝑛\mathbf{e}\_{n} and 𝐏nsubscript𝐏𝑛\mathbf{P}\_{n} as input. Our implicit decoder consists of linear layers with residual connections and predicts 𝐎nsubscript𝐎𝑛\mathbf{O}\_{n}. We use a mean squared error loss between the predicted occupancy and the ground truth occupancy.
Our framework is flexible and can be adapted to different forms of architectures. To showcase this,
we use a PointNet [[48](#bib.bib48)] as the encoder and a FoldingNet [[60](#bib.bib60)] as the decoder that generates point clouds instead of occupancies,
which are trained with a Chamfer loss [[3](#bib.bib3)].

### 3.2 Stage 2: Conditional Normalizing Flow

We train a normalizing flow network using 𝐞nsubscript𝐞𝑛\mathbf{e}\_{n} and its corresponding rendered images 𝐈nsubscript𝐈𝑛\mathbf{I}\_{n}.
Note that each 𝐈nsubscript𝐈𝑛\mathbf{I}\_{n} can include multiple images of the same shape from different rendering settings, such as changing camera viewpoints.
We model the conditional distribution of 𝐞nsubscript𝐞𝑛\mathbf{e}\_{n} using a RealNVP network [[13](#bib.bib13)] with five layers, which transforms the distribution of 𝐞nsubscript𝐞𝑛\mathbf{e}\_{n} into a normal distribution.
We obtain the condition vector 𝐜nsubscript𝐜𝑛\mathbf{c}\_{n} by passing 𝐈nsubscript𝐈𝑛\mathbf{I}\_{n} through the ViT [[14](#bib.bib14)] based CLIP image encoder fIsubscript𝑓𝐼f\_{I}, whose weights are frozen after pre-training. 𝐜nsubscript𝐜𝑛\mathbf{c}\_{n} is concatenated with the transformed feature vector at each scale and translation coupling layers of RealNVP:

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝐜n=fI​(𝐈n)​,𝐳n1:d=𝐞n1:dandformulae-sequencesubscript𝐜𝑛subscript𝑓𝐼subscript𝐈𝑛,superscriptsubscript𝐳𝑛:1𝑑  superscriptsubscript𝐞𝑛:1𝑑and\mathbf{c}\_{n}=f\_{I}(\mathbf{I}\_{n})\text{,}\quad\mathbf{z}\_{n}^{1:d}=\mathbf{e}\_{n}^{1:d}\quad\text{and} |  | (2) |

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝐳nd+1:D=𝐞nd+1:D⊙exp⁡(s​([𝐜n;𝐞n1:d]))+t​([𝐜n;𝐞n1:d])superscriptsubscript𝐳𝑛:𝑑1𝐷direct-productsuperscriptsubscript𝐞𝑛:𝑑1𝐷𝑠  subscript𝐜𝑛superscriptsubscript𝐞𝑛:1𝑑𝑡  subscript𝐜𝑛superscriptsubscript𝐞𝑛:1𝑑\mathbf{z}\_{n}^{d+1:D}=\mathbf{e}\_{n}^{d+1:D}\odot\exp\big{(}s([\mathbf{c}\_{n};\mathbf{e}\_{n}^{1:d}])\big{)}+t([\mathbf{c}\_{n};\mathbf{e}\_{n}^{1:d}]) |  | (3) |

where s𝑠s and t𝑡t stand for the scale and translation function parameterized by a neural network.
The intuition here is we split the object embedding 𝐞nsubscript𝐞𝑛\mathbf{e}\_{n} into two parts where one part is modified using a neural network that is simple to invert, but still dependent on the remainder part in a non-linear manner. The splitting can be done in several ways by using a binary mask [[13](#bib.bib13)].
In particular, we investigate two strategies: checkerboard masking and dimension-wise masking.
The checkerboard masking has value 1 where the sum of spatial coordinates is odd, and 0 otherwise.
The dimension-wise mask has value 1 for the first half of latent vector, and 0 for the second half.
The masks are reversed after every layer.
Finally, we impose a density estimation loss on the shape embeddings as:

|  |  |  |
| --- | --- | --- |
|  | log⁡(p​(𝐞n))=log⁡(p​(𝐳n))+log⁡(|det(∂f​(𝐞n)∂𝐳nT)|)𝑝subscript𝐞𝑛𝑝subscript𝐳𝑛𝑓subscript𝐞𝑛superscriptsubscript𝐳𝑛𝑇\displaystyle\log\left(p(\mathbf{e}\_{n})\right)=\log\Big{(}p\big{(}\mathbf{z}\_{n}\big{)}\Big{)}+\log\left(\left|\det\left(\frac{\partial f(\mathbf{e}\_{n})}{\partial\mathbf{z}\_{n}^{T}}\right)\right|\right) |  |

where f𝑓f is the normalizing flow model, and ∂f​(𝐞n)/∂𝐳nT𝑓subscript𝐞𝑛superscriptsubscript𝐳𝑛𝑇\partial f(\mathbf{e}\_{n})/\partial\mathbf{z}\_{n}^{T} is the Jacobian of f𝑓f at 𝐞nsubscript𝐞𝑛\mathbf{e}\_{n} [[13](#bib.bib13)]. We model the latent distribution p​(𝐳n)𝑝subscript𝐳𝑛p(\mathbf{z}\_{n}) as an unit Gaussian distribution.

### 3.3 Inference

During the inference phase, we convert a text query t into the text embedding using the CLIP text encoder, fTsubscript𝑓𝑇f\_{T}. As the CLIP image and text encoders are trained to bring the image and text embeddings in a joint latent space, we can simply use the text embedding as the condition vector for the normalizing flow model, i.e. 𝐜𝐜\mathbf{c}=fT​(t)subscript𝑓𝑇tf\_{T}(\textbf{t}).
Once we obtain the condition vector we can sample a vector from the normal distribution and use the reverse path of the flow model to obtain a shape embedding in p​(𝐞n)𝑝subscript𝐞𝑛p(\mathbf{e}\_{n}).
The normal distribution allows us to sample multiple times to obtain multiple shape embeddings for a given text query.
We obtain the mean shape embedding by using the mean of the normal distribution. The mean shape embedding represents the prototype for a given text query.
These shape embeddings are then converted to 3D shapes using the implicit decoder trained in stage 1.

## 4 Experiments

In this section, we first describe the experimental setup and then show qualitative and quantitative results. More results can be found in the supplementary material.

Dataset. For all of our experiments, we use the ShapeNet(v2) dataset [[5](#bib.bib5)] which consists of 13 rigid object classes. We use the processed version of the data which consists of rendered images, voxel grids, query points and their occupancies from shapes as provided in [[10](#bib.bib10), [37](#bib.bib37)].

Implementation Details. For both training stages, we use the Adam optimizer [[30](#bib.bib30)] with a learning rate of 1e-4 and a batch size of 32. We train the stage 1 autoencoder for 300 epochs whereas we train the stage 2 conditional normalizing flow model for 100 epochs. For all the experiments below we use a latent size of 128 with a BatchNorm [[25](#bib.bib25)] based voxel encoder and a ResNet based decoder inspired by the Occupancy Network [[37](#bib.bib37)]. We use a RealNVP [[13](#bib.bib13)] based network with dimension-wise masking for the flow model. The design decisions are discussed in the ablation study section and further details are provided in the supplemental material.

Evaluation Metrics. To evaluate our method thoroughly, we consider four criteria and several metrics for those criteria respectively. Furthermore, for some criteria we manually define a set of 234 text queries (or prompts). These queries include direct hyponyms for the ShapeNet categories from the WordNet [[17](#bib.bib17)] taxonomy, sub-categories and relevant shape attributes for a given category (e.g. a round chair, a square table, etc.) across the ShapeNet(v2) dataset. The text queries are listed in the appendix. The criteria are as follows:

1. 1.

   Reconstruction Quality. This criteria is mainly used to check the reconstruction capabilities of the stage 1 autoencoder on the test set. We use two metrics: Mean Square Error (MSE) on 30,000 sample query points and Intersection over Union (IOU) with 323superscript32332^{3} voxel shapes.
2. 2.

   Generation Quality. We use this criteria to evaluate the quality of generated shapes on text queries. We consider two metrics: Fréchet inception distance (FID) [[22](#bib.bib22)] and Maximum Measure Distance (MMD) using IOU . To calculate FID and MMD, we first take 224 text queries as mentioned above and generate a mean shape embedding for each text query. We then generate 323superscript32332^{3} resolution 3D objects for all the text queries. For FID, we compare the generated 3D shapes with the test dataset of ShapeNet. FID depends on a pre-trained network, for which we train a voxel classifier on the 13 ShapeNet classes and use the feature vector from the fourth layer. We provide more details in the appendix. In the case of MMD, for each generated shape we match a shape in the test dataset based on the highest IOU. We then average the IOU across all the text queries. Note, MMD is a variation of the Minimum Measure Distance as described in [[3](#bib.bib3)], which we believe is more suitable for implicit representations as we do not need to sample the surface.
3. 3.

   Diversity Across Categories. To make sure we generate shapes across categories we design a new criteria. First, we generate the shapes based on the text queries as mentioned above. For each text query we have an assigned label. We then pass the generated voxels through the same classifier used to calculate the FID metric. We then report the accuracy based on the assigned label. We refer to this metric as Acc. throughout the text. Also note that the FID metric gives a good measure for diversity as we compare it with the test distribution.
4. 4.

   Human Perceptual Evaluation. To evaluate CLIP-Forge’s ability to provide control over the generated shape using attribute, common name, and sub-category information from the text prompt, we conducted a perceptual evaluation using Amazon SageMaker Ground Truth and crowd workers from Mechanical Turk [[38](#bib.bib38)]. More detail is provided in section [4.3](#S4.SS3 "4.3 Human Perceptual Evaluation ‣ 4 Experiments ‣ CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation").

### 4.1 Comparison with Supervised Models

| method | FID↓↓\downarrow | MMD↑↑\uparrow | Acc.↑↑\uparrow |
| --- | --- | --- | --- |
| text2shape-CMA [[7](#bib.bib7)] | 16078.05 | 0.4992 | 4.27 |
| text2shape-supervised [[7](#bib.bib7)] | 14881.96 | 0.1418 | 6.84 |
| ‘CLIP-Forge (ours) | 2425.25 | 0.6607 | 83.33 |

Table 1: Comparing CLIP-Forge with supervised models using the text2shape dataset.

We compare CLIP-Forge with text-to-shape generation models that are trained with direct supervision signals. The only existing paired text-shape dataset is provided by Text2Shape [[7](#bib.bib7)], which contains 56,399 natural language descriptions for ShapeNet objects within the chair and table categories. We train two supervised models using the Text2Shape dataset: text2shape-CMA uses the cross-modality alignment loss described in [[7](#bib.bib7)] and text2shape-supervised uses a direct MSE loss in the embedding space. For both supervised baseline methods, we use the same CLIP text encoder and occupancy network shape encoder and decoder to ensure fair comparison. Table [1](#S4.T1 "Table 1 ‣ 4.1 Comparison with Supervised Models ‣ 4 Experiments ‣ CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation") shows the result on our text query set. It can be seen that CLIP-Forge significantly outperforms both supervised baselines in all evaluation metrics. In particular, we observe that text2shape-CMA generates generic shapes such as boxes and spheres that do not resemble specific objects. The text2shape-supervised baseline fails to generalize and tends to generate chair- and table- like shapes that it is trained on, despite the text query is irrelevant to these two categories.

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “a chair” | | | “a plane” | | |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “a truck” | | | “a square table” | | |

Figure 4:  Our method can generate multiple examples given a text query. In this case, we are generating 3 shapes for a given text prompt.



|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “a pistol” | “an ak-47” | “a yacht” | “a dressing table” | “a beach wagon” | “a van” |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “a throne” | “a stool” | “a sofa” | “a telly” | “a table lamp” | “a delta wing” |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “a monster truck” | “a muscle car” | “a speedboat” | “a sail boat” | “a bar stool” | “a wing chair” |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “a table” | “a circular table” | “a rectangular table” | “a square table” | “a thick table” | “a thin table” |

Figure 5: Illustrating our method can generate shapes via text containing common names, sub-category and attribute. The first two rows show shape generation based on using common names to describe an object. The next row shows two shapes for sub-category in car, boat and chair category. The final row illustrates the different shape attributes (circular, square, etc.) for the table class.

### 4.2 Qualitative Results

We qualitatively evaluate generative capabilities of our method.
First, in Figure [19](#A9.F19 "Figure 19 ‣ Appendix I Additional Qualitative Results ‣ CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation") we show that our network can generate multiple and diverse shapes using a single text query. This can be useful in a design process for imagining new variations.
Next, we show that our network can generate shapes based on category, sub-category, common semantic words, and common shape attributes as shown in Figure [5](#S4.F5 "Figure 5 ‣ 4.1 Comparison with Supervised Models ‣ 4 Experiments ‣ CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation"). It can be seen that our network captures semantic notion of the text query.
Finally, we show the generated shapes from interpolation between two text inputs in Figure [20](#A9.F20 "Figure 20 ‣ Appendix I Additional Qualitative Results ‣ CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation"). The interpolation results imply that the conditioning space is smooth.

### 4.3 Human Perceptual Evaluation

In this study we measure whether providing additional detail in the text prompt gives rise to semantically appropriate changes in the generated shape. To evaluate if the shape changes are semantically correct, we used human evaluators from Amazon Mechanical Turk [[38](#bib.bib38)]. The human evaluators were presented with pairs of images as shown in Figure [6](#S4.F6 "Figure 6 ‣ 4.3 Human Perceptual Evaluation ‣ 4 Experiments ‣ CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation")(a). One image was generated using the ShapeNet(v2) category name (for example “a car”) while the other was generated using text which described a sub-category or shape attribute (for example “a truck” or “a round car”). The human evaluators were asked to identify which image best matched the sub-category or attribute text prompt. Each image pair was shown to 9 independent human evaluators. We record the fraction of image pairs for which more than half of the evaluators selected the image generated using the sub-category or attribute augmented prompt.

The results of the perceptual study are shown in Figure [6](#S4.F6 "Figure 6 ‣ 4.3 Human Perceptual Evaluation ‣ 4 Experiments ‣ CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation")(b). The human evaluators correctly identified the model generated by the detailed prompt for 70.83% of the image pairs, showing that our method is able to utilize attribute and sub-category information in a way which is recognizable for humans. We see the attribute prompts produced shapes which were more easily identified than those from the sub-category prompts. One reason for this result is that the attribute augmented prompts give a clear description of how the object should look, while many of the sub-categories are less easily recognized given the quality of generation. For example “A circular bench” was correctly identified by 8/9 evaluators while “A laboratory bench” was not recognized by any of the 9 humans.

![Refer to caption](/html/2110.02624/assets/figures_arxiv/perceptual.jpg)


Figure 6: a) An example of an image pair and text prompt shown to the human evaluators. b) The percentage of image pairs for which the model generated by the text prompt was correctly identified.

### 4.4 Choice of Prefix in Text Prompt

Designing a prompt can be challenging as small changes in words can potentially have a impact on our downstream task. In this experiment, we investigate how much does prompt selection effect the performance of our method. We specifically investigate what prefix to choose before a text query. The investigations are shown in Table [2](#S4.T2 "Table 2 ‣ 4.4 Choice of Prefix in Text Prompt ‣ 4 Experiments ‣ CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation"). We find that prefix selection indeed has a effect on generation quality and diversity. A interesting avenue of future research would be to investigate prompt engineering [[61](#bib.bib61)].

| prefix | FID↓↓\downarrow | MMD↑↑\uparrow | Acc.↑↑\uparrow |
| --- | --- | --- | --- |
| “a”/“an” | 2425.25 | 0.6607 | 83.33 |
| “a photo of” | 2400.36 | 0.6490 | 78.63 |
| “a photo of a” | 2484.49 | 0.6620 | 80.77 |
| “a picture of a” | 2560.98 | 0.6681 | 81.20 |
| “a rendering of” | 3029.92 | 0.6311 | 76.50 |
| “a photo of one” | 2715.45 | 0.6597 | 82.48 |
| “one” | 3142.07 | 0.6608 | 87.18 |

Table 2: Different Prompts and their effect.

### 4.5 CLIP-Forge for Point Cloud

In this section, we investigate if our method can be simply applied to a different representation, namely, a point cloud. As stated earlier we use the PointNet encoder [[48](#bib.bib48)] and FoldingNet decoder [[60](#bib.bib60)]. We use the same flow architecture as mentioned above. We train the network on the ShapeNet(v2) dataset. The results are shown in Fig [8](#S4.F8 "Figure 8 ‣ 4.5 CLIP-Forge for Point Cloud ‣ 4 Experiments ‣ CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation"). It can be seen that our method does a satisfactory job in generating 3D point clouds using text queries while using off the shelf point cloud encoders and decoders.

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “a truck” →→\rightarrow “a sports car” | | | | |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “a cabinet” →→\rightarrow “a table” | | | | |

Figure 7: Interpolation results between two text queries.



|  |  |  |
| --- | --- | --- |
| Refer to caption | Refer to caption | Refer to caption |
| “an f-16 ” | “a bench” | “a desk” |
| Refer to caption | Refer to caption | Refer to caption |
| “a lamp” | “a billiard table” | “a thin car” |
| Refer to caption | Refer to caption | Refer to caption |
| “a round table” | “a supersonic plane” | “a sailing boat” |

Figure 8: CLIP-Forge point cloud generations.

## 5 Ablation Studies

In this section, we discuss how different components of our algorithm affect our model. For all our ablation studies, we use the above mentioned hyperparameters for the autoencoder unless otherwise stated. For the flow model, we use RealNVP model with Checkerboard masking for most experiments unless otherwise stated.

### 5.1 Stage 1 Autoencoder Design Choice

In Table [3](#S5.T3 "Table 3 ‣ 5.1 Stage 1 Autoencoder Design Choice ‣ 5 Ablation Studies ‣ CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation"), we experiment with different parts of the autoencoder architecture. The first subsection of Table [3](#S5.T3 "Table 3 ‣ 5.1 Stage 1 Autoencoder Design Choice ‣ 5 Ablation Studies ‣ CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation") investigates how adding noise in the latent space helps our model. Empirically it can be seen from the table that adding noise not only helps the reconstruction but also improves the generation and diversity of the shapes generated. Next we investigate the size of the latent space and find that our model works reasonably well while using a smaller latent size of 128. Finally, we explore different encoders and decoders for our model. The results indicate that our model can take different representations, point cloud, as the input to the encoder. We provide more details regarding the encoder and decoder in appendix.

| noise | latent | encoder | decoder | IOU↑↑\uparrow | MSE↓↓\downarrow | FID↓↓\downarrow | MMD↑↑\uparrow | Acc.↑↑\uparrow |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ×\times | 128 | VoxEnc | RN-OccNet | 0.7275 | 0.01120 | 3871.48 | 0.6559 | 71.94 |
| ✓ | 0.7374 | 0.01159 | 2688.72 | 0.6732 | 79.34 |
| ✓ | 256 | VoxEnc | RN-OccNet | 0.7375 | 0.01158 | 3177.92 | 0.6535 | 78.77 |
| 512 | 0.7362 | 0.01155 | 3577.72 | 0.6374 | 74.50 |
| ✓ | 128 | PointNet | RN-OccNet | 0.7082 | 0.01051 | 2646.93 | 0.6746 | 76.50 |
| ResVoxEnc | RN-OccNet | 0.7371 | 0.01075 | 3146.94 | 0.6509 | 74.64 |
| VoxEnc | CBN-OccNet | 0.7674 | 0.01025 | 2956.78 | 0.6645 | 78.77 |

Table 3: Effects of different autoencoder design choices in stage 1, including the usage of Gaussian noise, the latent vector size, as well as various encoder and decoder architectures.

### 5.2 Stage 2 Prior Design Choice

In this section, we investigate the design choice for the prior network. First, we investigate different conditioning mechanisms, namely, conditioning the affine coupling layers and conditioning the prior network. From Table [4](#S5.T4 "Table 4 ‣ 5.2 Stage 2 Prior Design Choice ‣ 5 Ablation Studies ‣ CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation"), it can be seen the choice of conditioning matters and conditioning the affine layers is the most effective. This intuitively makes sense as we are conditioning multiple times as we are concatenating each coupling layer whereas we just condition the prior once. A similar phenomena is observed in the case of an architectures like [[44](#bib.bib44), [8](#bib.bib8)], where they concatenated the condition vector multiple times.

In Table [4](#S5.T4 "Table 4 ‣ 5.2 Stage 2 Prior Design Choice ‣ 5 Ablation Studies ‣ CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation"), we also investigate different masking techniques (Dimension masking and Checkered masking) [[13](#bib.bib13)] and a distinct flow architecture: Masked Autoregressive Flow (MAF) [[43](#bib.bib43)].
It can be seen from the table that both masking techniques are effective but Dimension masking (RealNVP-D) seems to be more effective than Checkered masking (RealNVP-C). Furthermore, we find that MAF flow prior network is not as effective as RealNVP. For the remainder of the ablation studies we use the Dimension Masking for RealNVP.

| condition | prior | FID↓↓\downarrow | MMD↑↑\uparrow | Acc.↑↑\uparrow |
| --- | --- | --- | --- | --- |
| affine coupling | RealNVP-C | 2688.72 | 0.6732 | 79.34 |
| prior network | 5227.32 | 0.6600 | 62.39 |
| affine coupling | RealNVP-D | 2591.87 | 0.6751 | 82.19 |
| MAF [[43](#bib.bib43)] | 6052.62 | 0.6273 | 59.40 |

Table 4: Effects of different conditional normalizing flow design choices in stage 2.

### 5.3 Number of Renderings

Next, we evaluate if using more views helps the generation quality and diversity. We report the results in Table [5](#S5.T5 "Table 5 ‣ 5.4 CLIP Architecture ‣ 5 Ablation Studies ‣ CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation"). The views are randomly selected from the renderings as prepared in [[10](#bib.bib10)]. It can be seen that using more views in general help improve the generation quality and diversity. As we are using a pre-trained CLIP model which is trained on natural images from different viewpoints, training using multiple views of shape renderings allows us to better capture the output distribution of CLIP model.

### 5.4 CLIP Architecture

In this section, we evaluate using different CLIP models to see how increasing the size of CLIP model and using ResNet [[21](#bib.bib21)] or ViT [[14](#bib.bib14)] based clip model effects our downstream task. We empirically observe from Table [5](#S5.T5 "Table 5 ‣ 5.4 CLIP Architecture ‣ 5 Ablation Studies ‣ CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation") that increasing the size of the model, i.e from ViT-B/32 to ViT-B/16, does not effect the text based generation too much. A more surprising result is that ResNet based CLIP model performs inferior to Visual Transformers. We hypothesize that patch based methods such as ViT focus more on the foreground object rather than the background. This is especially helpful in the case of image renderings.

| rendering | CLIP | FID↓↓\downarrow | MMD↑↑\uparrow | Acc.↑↑\uparrow |
| --- | --- | --- | --- | --- |
| 1 | ViT-B/32 | 2983.72 | 0.6586 | 79.77 |
| 5 | 2776.28 | 0.6655 | 80.20 |
| 10 | 2622.71 | 0.6652 | 80.63 |
| 20 | ViT-B/32 | 2591.87 | 0.6751 | 82.19 |
| ViT-B/16 | 2515.81 | 0.6573 | 80.48 |
| RN50x16 | 2906.75 | 0.6591 | 75.93 |

Table 5: Effects of different numbers of renderings and CLIP architectures.

## 6 Limitations and Future Work

We believe our method can be improved in several ways. Firstly, the quality of generation is still lacking and we believe a novel future avenue would be to combine ideas from local implicit methods [[46](#bib.bib46), [9](#bib.bib9)]. Furthermore, our work currently focuses on geometry and it would be interesting to integrate texture to our model. Finally, we are limited by CLIP’s trained data distribution and a potential future direction would be to fine tune it for a specfic dataset.

In terms of potential negative impact, language-driven 3D modeling tools enabled by CLIP-Forge might lower the technical barriers to 3D modeling and potentially reduce some tedious 3D modeling tasks for 3D modelers and animators. However, it brings a greater benefit of democratizing 3D content creation to the general public, similar to that everyone can take photos and make videos today.

## 7 Conclusion

We presented a method, CLIP-Forge, that can efficiently generate multiple 3D shapes while preserving the semantic meaning from a given text prompt.
Our method requires no text-shape labels as training data, offering an opportunity to leverage shape-only datasets such as ShapeNet.
Finally, we showed that our model can generate results on other representations such as point clouds and we thoroughly studied different components of the method.

Supplementary Material

## Appendix A Architecture and Experiment Details

For all our experiments in the ablation section of the main paper, we run the second stage network with 3 different seeds and report the mean in the main paper. We take the best seed for the experiment section in the main paper to report the qualitative and quantitative results. The text queries (or prompts) used for classification FID, MMD, and Acc. are shown in Table [6](#A1.T6 "Table 6 ‣ Appendix A Architecture and Experiment Details ‣ CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation").
Note that these text queries are mostly taken from WordNet [[17](#bib.bib17)] with added common synonyms and shape attributes.
In Table [8](#A3.T8 "Table 8 ‣ Appendix C Category-wise Accuracy Results ‣ CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation"), we show category-wise accuracy results of CLIP-Forge in the main paper’s Table 1.
For our visualizations, we output a shape with 643superscript64364^{3} resolution and use the rendering script inspired by [[1](#bib.bib1)]. We use a set of different thresholds values and pick the threshold for different category that yields the best visual result.

In the main paper, we refer to the batch normalization based voxel encoder as VoxEnc, whereas when we add residual connection to VoxEnc we refer it to as ResVoxEnc. For both of these encoders, we have 4 3D convolution layers followed by a linear layer. The input to these encoder is a 323superscript32332^{3} voxel representation based shape. We also experiment with a point cloud based encoder which is inspired by PointNet. The PointNet encoder has 5 linear layers followed by a max pooling operation. We then use an MLP followed by a final linear layer to project it to the latent size. The input to this encoder is a point cloud with 2048 sampled points.
For the decoder, we refer to the residual connection based network as RN-OccNet. In this model, we concatenate the query locations with the latent code and pass it through a 5 block ResNet based decoder. We also experiment with conditioning the batchnorm of the decoder instead of concatenating it, which we refer to as CBN-OccNet. Both these decoders are inspired by OccNet [[37](#bib.bib37)]. For our point cloud based generation experiments, we use a FoldingNet [[60](#bib.bib60)] based decoder, where we use two folding based operations with a single square grid.

Finally, we use RealNVP [[13](#bib.bib13)] for the prior model. We use 5 blocks of coupling layer containing translation and scale along with batch norm, where the masking is inverted after each block. Each network comprises of a 2-layer MLP followed by a linear layer. A 1024 hidden vector size is used. For the MAF [[43](#bib.bib43)] model, we also use the same number of blocks and hidden vectors.

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| “a triangular airplane” | “an airplane” | “a jet” | “a fighter plane” | “a biplane” |
| “a seaplane” | “a space shuttle” | “a supersonic plane” | “a rocket plane” | “a delta wing” |
| “a swept wing plane” | “a straight wing plane” | “a propeller plane” | “a boeing” | “an airbus” |
| “an f-16” | “a plane” | “an aeroplane” | “an aircraft” | “a commercial plane” |
| “a square bench” | “a round bench” | “a circular bench” | “a rectangular bench” | “a thick bench” |
| “a thin bench” | “a bench” | “a pew” | “a flat bench” | “a settle” |
| “a back bench” | “a laboratory bench” | “a storage bench” | “a park bench” | “a cuboid cabinet” |
| “a round cabinet” | “a rectangular cabinet” | “a thick cabinet” | “a thin cabinet” | “a cabinet” |
| “a garage cabinet” | “a desk cabinet” | “a dresser” | “a cupboard” | “a container” |
| “a case” | “a locker” | “a cupboard” | “a closet” | “a sideboard” |
| “a square car” | “a round car” | “a rectangular car” | “a thick car” | “a thin car” |
| “a car” | “a bus” | “a shuttle-bus” | “a pickup car” | “a truck” |
| “a suv” | “a sports car” | “a limo” | “a jeep” | “a van” |
| “a gas guzzler” | “a race car” | “a monster truck” | “an armored” | “an atv” |
| “a microbus” | “a muscle car” | “a retro car” | “a wagon car” | “a hatchback” |
| “a sedan” | “an ambulance” | “a roadster car” | “a beach wagon” | “an auto” |
| “an automobile” | “a motor car” | “a square chair” | “a round chair” | “a rectangular chair” |
| “a thick chair” | “a thin chair” | “a chair” | “an arm chair” | “a bowl chair” |
| “a rocking chair” | “an egg chair” | “a swivel chair” | “a bar stool” | “a ladder back chair” |
| “a throne” | “an office chair” | “a wheelchair” | “a stool” | “a barber chair” |
| “a folding chair” | “a lounge chair” | “a vertical back chair” | “a recliner” | “a wing chair” |
| “a sling” | “a seat” | “a cathedra” | “a square monitor” | “a round monitor” |
| “a rectangular monitor” | “a thick monitor” | “a thin monitor” | “a monitor” | “a crt monitor” |
| “a TV” | “a digital display” | “a flat panel display” | “a screen” | “a television” |
| “a telly” | “a video” | “a square lamp” | “a round lamp” | “a rectangular lamp” |
| “a cuboid lamp” | “a circular lamp” | “a thick lamp” | “a thin lamp” | “a lamp” |
| “a street lamp” | “a fluorescent lamp” | “a gas lamp” | “a bulb” | “a lantern” |
| “a table lamp” | “a torch” | “a square loudspeaker” | “a round loudspeaker” | “a rectangular loudspeaker” |
| “a circular loudspeaker” | “a thick loudspeaker” | “a thin loudspeaker” | “a loudspeaker” | “a subwoofer speaker” |
| “a speaker” | “a speaker unit” | “a tannoy” | “a thick gun” | “a thin gun” |
| “a gun” | “a machine gun” | “a sniper rifle” | “a pistol” | “a shotgun” |
| “an ak-47” | “an uzi” | “an M1 Garand” | “a M-16” | “a firearm” |
| “a shooter” | “a weapon” | “a square sofa” | “a round sofa” | “a rectangular sofa” |
| “a thick sofa” | “a thin sofa” | “a sofa” | “a double couch” | “a love seat” |
| “a chesterfield” | “a convertible sofa” | “an L shaped sofa” | “a settee sofa” | “a daybed” |
| “a sofa bed” | “an ottoman” | “a couch” | “a lounge” | “a divan” |
| “a futon” | “a square table” | “a round table” | “a circular table” | “a rectangular table” |
| “a thick table” | “a thin table” | “a table” | “a dressing table” | “a desk” |
| “a refactory table” | “a counter” | “an operating table” | “a stand” | “a billiard table” |
| “a pool table” | “a ping-pong table” | “a console table” | “an altar table” | “a worktop” |
| “a workbench” | “a square phone” | “a rectangular phone” | “a thick phone” | “a thin phone” |
| “a phone” | “a desk phone” | “a flip-phone” | “a telephone” | “a telephone set” |
| “a cellular telephone” | “a cellular phone” | “a cellphone” | “a cell” | “a mobile phone” |
| “an iphone” | “a square boat” | “a round boat” | “a rectangular boat” | “a thick boat” |
| “a thin boat” | “a boat” | “a war ship” | “a sail boat” | “a speedboat” |
| “a cabin cruiser” | “a yacht” | “a rowing boat” | “a watercraft” | “a ship” |
| “a canal boat” | “a ferry” | “a steamboat” | “a barge” |  |
| 0/9 | 1/9 | 2/9 | 3/9 | 4/9 |
| 5/9 | 6/9 | 7/9 | 8/9 | 9/9 |

Table 6: The full list of text queries. The colors show the results of the human perceptual evaluation study as described in section [J](#A10 "Appendix J Human Perceptual Evaluation ‣ CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation"). Green indicates queries which gave rise to distinctive and recognisable shapes, while red indicates the shapes could not be distinguished from those generated using the ShapeNet category name. The key at the bottom shows the fraction of the nine crowd workers who found the generated shape recognisable. White indicates the query was not rated in the perceptual study.

## Appendix B Comparison with Supervised Models

| method | dataset | FID↓↓\downarrow | MMD↑↑\uparrow | Acc.↑↑\uparrow |
| --- | --- | --- | --- | --- |
| sup. | T2S [[7](#bib.bib7)] | 14881.96 | 0.1418 | 6.84 |
| ours | 14746.90 | 0.5412 | 30.77 |
| sup. | SN13 [[10](#bib.bib10)] | 19896.11 | 0.1805 | 14.10 |
| ours | 2425.25 | 0.6607 | 83.33 |

Table 7: Additional detailed comparisons with supervised models, where sup. stands for the supervised model.

In this section, we provide a more detailed comparison
between CLIP-Forge and supervised methods. Note, it is
not clear how to compare our zero-shot model with supervised models. As our end goal is to generate shapes across categories and text queries, we decide to use our original text query subset (mentioned above) and Shapenet (v2) test dataset as the test set. This test set ensures we test
on commonly described words for different shape category as mentioned in WordNet [[17](#bib.bib17)]. We consider two datasets: T2S is the annotated text-shape description dataset from text2shape [[7](#bib.bib7)] which mainly contains information regarding texture, and SN13 is the ShapeNet (v2) subset containing 13 categories from [[10](#bib.bib10)].

T2S dataset [[7](#bib.bib7)] has text labels only for chair and tableclass, so we train a supervised baseline model that has a linear layer connecting a pre-trained CLIP text encoder [[49](#bib.bib49)] and a pre-trained occupancy network decoder [[37](#bib.bib37)] using an L2 loss in the latent space. We use the same text encoder and shape decoder in this baseline to ensure a fair comparison. We compare the baseline model with our model which does not have use any supervision from text labels and is also trained on T2S shape dataset (chair and table only).
The results are shown in the first part of Table [7](#A2.T7 "Table 7 ‣ Appendix B Comparison with Supervised Models ‣ CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation"). It can be seen from the table that our model can generate shapes in chair and table categories based on common words with higher quality despite not using any text label information.

To test baseline models on all of ShapeNet subset
(SN13), as there is no text label data, we create a simple supervision signal by directly using the category name as the text for training the supervised model. The results are shown in second part of Table [7](#A2.T7 "Table 7 ‣ Appendix B Comparison with Supervised Models ‣ CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation"). It can be seen that our model outperforms the supervised method, demonstrating its stronger zero-shot generalization ability. This results also indicate that our model scales better with more data without requiring text-shape labels. In Figure [22](#A9.F22 "Figure 22 ‣ Appendix I Additional Qualitative Results ‣ CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation"), we show
qualitative results of the supervised baselines, where the model fails to generate cars when trained on T2S, and fails to capture the details of sports car when trained with SN13.

## Appendix C Category-wise Accuracy Results

We also report category-wise accuracy results obtained from our classifier for our method in Table [8](#A3.T8 "Table 8 ‣ Appendix C Category-wise Accuracy Results ‣ CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation"). It can be generally noted that our method can generate shapes across all categories of Shapenet. However, accuracy across some categories such as airplane and car are higher than other categories such as boat and loudspeaker. We hypothesize that this may be due to some categories having larger data points during training compared to others.

|  |  |  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Airplane | Bench | Cabinet | Car | Chair | Monitor | Lamp | Loudspeaker | Gun | Sofa | Table | Phone | Boat |
| 95.00 | 64.29 | 87.50 | 96.88 | 96.15 | 92.86 | 93.33 | 45.45 | 92.86 | 89.47 | 75.00 | 60.00 | 61.11 |

Table 8: Category-wise accuracy results

.

## Appendix D Comparison with Text2Img+Img2Shape

In this section, we compare our method to off-the-shelf networks that simply generate an image from text first and then generate a 3D shape from the image. We use pre-trained DALLE-mini for converting a text to image and use a pre-trained occupancy network with image encoder to convert an image to 3D shape. The results are shown in Fig. [9](#A4.F9 "Figure 9 ‣ Appendix D Comparison with Text2Img+Img2Shape ‣ CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation"). It can be seen that the resulting shapes suffer from poor quality. This is mainly due to the domain gap between generated images and natural images such as distortion artifacts and unclean background.

|  |  |  |  |
| --- | --- | --- | --- |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption |

Figure 9: Text2Img+Img2Shape baseline intermediate and final results: “a monster truck”, “a round chair”.

## Appendix E Effect of Threshold Parameter

Our results are strongly affected by the threshold used to create the occupancy value. We use a constant threshold value of 0.050.050.05 for our metrics (Acc., FID and MMD) and human perceptual evaluations. However, for our visual results we do a grid search and choose the best threshold value. Figure [10](#A5.F10 "Figure 10 ‣ Appendix E Effect of Threshold Parameter ‣ CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation"), shows the visual results of different thresholds. It can be seen that different shapes require different threshold which depends on the category and local details of the shape. We believe that our metrics and human evaluation results can be further improved if a better technique is discovered for threshold tuning.

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| Threshold = 0.025 | Threshold = 0.050 | Threshold = 0.075 | Threshold = 0.1 | Threshold = 0.2 | Threshold = 0.3 |

Figure 10: Effect of different thresholds for text: ”a lamp”, ”a sniper rifle”, ”a round table” and ”a swivel chair”.

## Appendix F Out of Distribution Generation

We also conduct experiments to see if the network can generate shapes based on text queries which are out of distribution from its training data. The results are shown in Figure [11](#A6.F11 "Figure 11 ‣ Appendix F Out of Distribution Generation ‣ CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation"). It can be seen from the results that the method tries to generate the desired shape based on its training dataset. We believe extending our method to generalize on out of distribution samples might be interesting avenue to explore for future work.

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “a circle” | “a rectangle” | “a square” | “a cuboid” | “a sphere” | “an ellipsoid” |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “a shoe” | “a piano” | “a bed” | “an xbox” | “a tower” | “a human” |

Figure 11: Results using text queries that are semantically outside the dataset.

## Appendix G Visual Results for Different Prefixes

In Figure [12](#A7.F12 "Figure 12 ‣ Appendix G Visual Results for Different Prefixes ‣ CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation"), we show results for different prefixes. They indicate that for different prefixes there are small variations in generated shape. Moreover, in some prefixes such as “a rendering of”, the visual results are worse. It would be interesting to investigate other prompts or do prompt tuning as future work.

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “bar stool” | “space shuttle” | “table lamp” | “television” | “beach wagon” |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “a picture of a bar stool” | “a picture of a space shuttle” | “a picture of a table lamp” | “a picture of a television” | “a picture of a beach wagon” |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “a photo of bar stool” | “a photo of space shuttle” | “a photo of table lamp” | “a photo of television” | “a photo of beach wagon” |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “a rendering of bar stool” | “a rendering of space shuttle” | “a rendering of table lamp” | “ a rendering of television” | “ a rendering of beach wagon” |

Figure 12: Results of varying the prefix for a given text query.

## Appendix H Visual Results for more Descriptive Texts

We show additional results using text queries that are longer and more descriptive in Figure [21](#A9.F21 "Figure 21 ‣ Appendix I Additional Qualitative Results ‣ CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation"). It can be seen that CLIP-Forge is able to capture certain shape-related attributes. Non-shape related descriptions such as color is not captured but could potentially bias the generation. We believe that combining our method with semi-supervised learning can enable more fine control of shape generation using text.

## Appendix I Additional Qualitative Results

In this part, we show more visual results for shape generation conditioned with text based on sub-category (Figure [13](#A9.F13 "Figure 13 ‣ Appendix I Additional Qualitative Results ‣ CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation") and Figure [14](#A9.F14 "Figure 14 ‣ Appendix I Additional Qualitative Results ‣ CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation")), synonyms (Figure [15](#A9.F15 "Figure 15 ‣ Appendix I Additional Qualitative Results ‣ CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation")), shape attributes (Figure [16](#A9.F16 "Figure 16 ‣ Appendix I Additional Qualitative Results ‣ CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation") and Figure [17](#A9.F17 "Figure 17 ‣ Appendix I Additional Qualitative Results ‣ CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation")) and common names (Figure [18](#A9.F18 "Figure 18 ‣ Appendix I Additional Qualitative Results ‣ CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation")). Moreover, we also show more visuals for text based multiple shape generation (Figure [19](#A9.F19 "Figure 19 ‣ Appendix I Additional Qualitative Results ‣ CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation")) and interpolation (Figure [20](#A9.F20 "Figure 20 ‣ Appendix I Additional Qualitative Results ‣ CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation")). It can be seen from all these results that our method is good at generating 3D shapes based on text queries. However, in same cases for example “a swivel chair”, it cannot construct all the details. Furthermore, on some sub-categories such as “an operating table” it cannot generate accurate shapes.

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “a hatchback” | “a suv” | “a sedan” | “a van” | “a sports car” | “a truck” |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “a muscle car” | “a retro car” | “a roadster car” | “a limo” | “a jeep” | “a bus” |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “a monster truck” | “a shuttle-bus” | “an arm chair” | “a swivel chair” | “a bar stool” | “a wing chair” |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “a vertical back chair” | “a bowl chair” | “a lounge chair” | “a cathedra’ | “a rocking chair” | “a recliner” |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “a sling” | “n ladder back chair” | “an egg chair” | “a stool’ | “a commercial plane” | “a jet” |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “a delta wing” | “a seaplane” | “a straight wing plane” | “a swept wing plane’ | “a biplane” | “a fighter plane” |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “a military drone” | “a supersonic plane” | “a rocket plane” | “a cabinet’ | “a garage cabinet” | “a desk cabinet” |

Figure 13: Additional shape generation results using sub-category text queries of CLIP-Forge.



|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “a monitor” | “a crt monitor” | “a flat panel display” | “a television’ | “a mobile phone” | “a flip-phone” |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “a desk phone” | “a back bench” | “a pew” | “a storage bench’ | “a laboratory bench” | “a flat bench” |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “a refectory table” | “a desk” | “a dressing table” | “a counter’ | “a console table” | “an operating table” |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “a war ship” | “a cabin cruiser” | “a speedboat” | “a sail boat’ | “a yacht” | “a mega yacht” |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “a chesterfield” | “a love seat” | “an ottoman” | “a sniper rifle’ | “a pistol” | “a shotgun” |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “a machine gun” | “a lamp” | “a street lamp” | “a LED table lamp’ | “a swing arm lamp” | “a subwoofer speaker” |

Figure 14: Additional shape generation results using sub-category text queries of CLIP-Forge (continued).



|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “an aeroplane” | “a plane” | “an airplane” | “a container” | “a dresser” | “an auto” |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “an automobile” | “a motor car” | “a seat” | “a digital display” | “a screen” | “a weapon” |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “a shooter” | “a firearm” | “a lounge” | “a couch” | “an altar table” | “a workbench” |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “a cellphone” | “a cellular phone” | “a ferry” | “a ship” | “a torch” | ‘a tannoy” |

Figure 15: Additional shape generation results using category and synonyms based text queries of CLIP-Forge.



|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “a rectangular car” | “a square car” | “a round car” | “a rectangular monitor” | “a square monitor” | “a round monitor” |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “a rectangular bench” | “a circular bench” | “a rectangular sofa” | “a round sofa” | “a square loudspeaker” | “a round loudspeaker” |

Figure 16: Additional shape generation results using attribute-based text queries of CLIP-Forge.



|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “a thin car” | “a thick car” | “a thin chair” | “a thick chair” | “a thin sofa” | “a thick sofa” |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “a thin gun” | “a thick gun” | “a thin cabinet” | “a thick cabinet” | “a thin boat” | “a thick boat” |

Figure 17: Additional shape generation results using attribute-based text queries of CLIP-Forge (continued).



|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “an auto” | “a honda” | “a toyota” | “an ambulance” | “a lamborghini” | “a tesla” |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “an Airbus A380plus” | “a boeing 747” | “a Lockheed SR-71 blackbird” | “a private jet” | ‘a M-16” | “a M1 Garand” |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “a billiard table” | “a locker” | “a gas guzzler” | “an iphone” | “a worktop” | “a park bench” |

Figure 18: Additional shape generation results using common name text queries of CLIP-Forge.



|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “a car” | | | “a limo” | | |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “a rocking chair” | | | “a round stool” | | |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “a round table” | | | “a round chair” | | |

Figure 19: Additional results for multiple shapes generation.



|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “a car” →→\rightarrow “a plane” | | | | |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “an ak-47” →→\rightarrow “a rifle” | | | | |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| “a round chair” →→\rightarrow “a rectangular chair” | | | | |

Figure 20: Additional Interpolation results between two text queries.



|  |  |  |  |
| --- | --- | --- | --- |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption |

Figure 21: Descriptive CLIP-Forge results: “a brown table with four legs”, “an armless chair with curved rectangular back”, “an armed chair with curved rectangular back”, “big sofa having two legs of black color, backrest, armrest, and sitting of black color”.



|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| CMA-T2S | | supervised-T2S | | supervised-SN13 | |

Figure 22: Qualitative results for supervised baselines using “a sports car” and “a vertical back chair”.

## Appendix J Human Perceptual Evaluation

In the human perceptual evaluation described in section 4.3 of the main paper, crowd workers recruited through Amazon Mechanical Turk [[38](#bib.bib38)] were shown pairs of images, one generated from the ShapeNet(v2) category name (see the first column of Figure [23](#A10.F23 "Figure 23 ‣ Appendix J Human Perceptual Evaluation ‣ CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation")) and the other from a detailed text prompt containing either subcategory or attribute information. The crowd workers were shown the detailed text prompt and asked to identify which of the two images it best describes. Nine crowd workers viewed each image pair and we record the number of times the model from the detailed text prompt is selected. For each detailed text prompt, this gives us a score from 0 to 9 indicating how effectively Clip-Forge can produce distinctive shapes which differ from the ShapeNet categories in a way which humans find semantically meaningful. In Table [6](#A1.T6 "Table 6 ‣ Appendix A Architecture and Experiment Details ‣ CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation") the human evaluation scores are shown as colors for each query text for which the evaluation was conducted. Figure [23](#A10.F23 "Figure 23 ‣ Appendix J Human Perceptual Evaluation ‣ CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation") shows a few examples in more detail. The second column of Figure [23](#A10.F23 "Figure 23 ‣ Appendix J Human Perceptual Evaluation ‣ CLIP-Forge: Towards Zero-Shot Text-to-Shape Generation") shows text prompts which produced distinctive shapes and the third column shows cases where the shapes were not as easily identified based on the text.
We see that when the prompt elicited a very distinctive shape (‘A monster truck”, “A fighter plane”) a high fraction of the human raters were able to identify the correct model.
In some cases the low score reflects a lack of resolution (for example “A swivel chair”, “A billiard table” and “A seaplane”). In the case of “A wheelchair”, Clip-Forge was unable to generate round wheels, but as the bottom of the legs were joined up this gave enough of an impression of wheels for humans to select the model. In the case of “A muscle car” Clip-Forge attempted to create the shape of a low form of a sports car, however the shape was not far enough from the generic car for the crowd workers to select it.

|  |  |  |
| --- | --- | --- |
| Refer to caption | Refer to caption | Refer to caption |
| “A car” | “A monster truck” 8/9 | “A muscle car” 2/9 |
| Refer to caption | Refer to caption | Refer to caption |
| “A gun” | “A sniper rifle” 8/9 | “A shotgun” 3/9 |
| Refer to caption | Refer to caption | Refer to caption |
| “A chair” | “A wheelchair” 8/9 | “A swivel chair” 4/9 |
| Refer to caption | Refer to caption | Refer to caption |
| “A table” | “A refactory table” 5/9 | “A billiard table” 2/9 |
| Refer to caption | Refer to caption | Refer to caption |
| “An airplane” | “A fighter plane” 9/9 | “A seaplane” 2/9 |

Figure 23: Images shown to the crowd workers in the human evaluation. The first column shows results generated using the ShapeNet(v2) category name. The second column shows examples of models which the crowd workers found easiest to identify based on the detailed text prompt and the third column shows the hardest. The fraction of the nine crowd workers who chose the model generated with the detailed text prompt is also shown.

## References

* [1]

  Blender Voxel Rendering.
  <https://blender.stackexchange.com/questions/115847/algorithm-for-turning-voxels-into-triangle-mesh>.
* [2]

  Panos Achlioptas, Ahmed Abdelreheem, Fei Xia, Mohamed Elhoseiny, and Leonidas
  Guibas.
  Referit3d: Neural listeners for fine-grained 3d object identification
  in real-world scenes.
  In European Conference on Computer Vision, pages 422–440.
  Springer, 2020.
* [3]

  Panos Achlioptas, Olga Diamanti, Ioannis Mitliagkas, and Leonidas Guibas.
  Learning representations and generative models for 3d point clouds.
  In International conference on machine learning, pages 40–49.
  PMLR, 2018.
* [4]

  Panos Achlioptas, Judy Fan, Robert X. D. Hawkins, Noah D. Goodman, and
  Leonidas J. Guibas.
  Learning to refer to 3d objects with natural language.
  2018.
* [5]

  Angel X. Chang, Thomas Funkhouser, Leonidas Guibas, Pat Hanrahan, Qixing Huang,
  Zimo Li, Silvio Savarese, Manolis Savva, Shuran Song, Hao Su, Jianxiong Xiao,
  Li Yi, and Fisher Yu.
  Shapenet: An information-rich 3d model repository, 2015.
  cite arxiv:1512.03012.
* [6]

  Dave Zhenyu Chen, Angel X Chang, and Matthias Nießner.
  Scanrefer: 3d object localization in rgb-d scans using natural
  language.
  In Computer Vision–ECCV 2020: 16th European Conference,
  Glasgow, UK, August 23–28, 2020, Proceedings, Part XX 16, pages 202–221.
  Springer, 2020.
* [7]

  Kevin Chen, Christopher B Choy, Manolis Savva, Angel X Chang, Thomas
  Funkhouser, and Silvio Savarese.
  Text2shape: Generating shapes from natural language by learning joint
  embeddings.
  In Asian Conference on Computer Vision, pages 100–116.
  Springer, 2018.
* [8]

  Zhiqin Chen and Hao Zhang.
  Learning implicit fields for generative shape modeling.
  Proceedings of IEEE Conference on Computer Vision and Pattern
  Recognition (CVPR), 2019.
* [9]

  Julian Chibane, Thiemo Alldieck, and Gerard Pons-Moll.
  Implicit functions in feature space for 3d shape reconstruction and
  completion.
  In Proceedings of the IEEE/CVF Conference on Computer Vision and
  Pattern Recognition, pages 6970–6981, 2020.
* [10]

  Christopher B Choy, Danfei Xu, JunYoung Gwak, Kevin Chen, and Silvio Savarese.
  3d-r2n2: A unified approach for single and multi-view 3d object
  reconstruction.
  In European conference on computer vision, pages 628–644.
  Springer, 2016.
* [11]

  Karan Desai and Justin Johnson.
  Virtex: Learning visual representations from textual annotations.
  In Proceedings of the IEEE/CVF Conference on Computer Vision and
  Pattern Recognition, pages 11162–11173, 2021.
* [12]

  Laurent Dinh, David Krueger, and Yoshua Bengio.
  Nice: Non-linear independent components estimation, 2015.
* [13]

  Laurent Dinh, Jascha Sohl-Dickstein, and Samy Bengio.
  Density estimation using real nvp.
  arXiv preprint arXiv:1605.08803, 2016.
* [14]

  Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, Dirk Weissenborn,
  Xiaohua Zhai, Thomas Unterthiner, Mostafa Dehghani, Matthias Minderer, Georg
  Heigold, Sylvain Gelly, et al.
  An image is worth 16x16 words: Transformers for image recognition at
  scale.
  arXiv preprint arXiv:2010.11929, 2020.
* [15]

  Patrick Esser, Robin Rombach, and Bjorn Ommer.
  Taming transformers for high-resolution image synthesis.
  In Proceedings of the IEEE/CVF Conference on Computer Vision and
  Pattern Recognition, pages 12873–12883, 2021.
* [16]

  Han Fang, Pengfei Xiong, Luhui Xu, and Yu Chen.
  Clip2video: Mastering video-text retrieval via image clip.
  arXiv preprint arXiv:2106.11097, 2021.
* [17]

  Christiane Fellbaum.
  WordNet: An Electronic Lexical Database.
  The MIT Press, 05 1998.
* [18]

  Kevin Frans, L. B. Soros, and Olaf Witkowski.
  Clipdraw: Exploring text-to-drawing synthesis through language-image
  encoders, 2021.
* [19]

  Andrea Frome, Greg Corrado, Jonathon Shlens, Samy Bengio, Jeffrey Dean,
  Marc’Aurelio Ranzato, and Tomas Mikolov.
  Devise: A deep visual-semantic embedding model.
  2013.
* [20]

  Zhizhong Han, Mingyang Shang, Xiyang Wang, Yu-Shen Liu, and Matthias Zwicker.
  Y2seq2seq: Cross-modal representation learning for 3d shape and text
  by joint reconstruction and prediction of view and word sequences.
  Proceedings of the AAAI Conference on Artificial Intelligence,
  33(01):126–133, Jul. 2019.
* [21]

  Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun.
  Deep residual learning for image recognition.
  In Proceedings of the IEEE conference on computer vision and
  pattern recognition, pages 770–778, 2016.
* [22]

  Martin Heusel, Hubert Ramsauer, Thomas Unterthiner, Bernhard Nessler, and Sepp
  Hochreiter.
  Gans trained by a two time-scale update rule converge to a local nash
  equilibrium.
  Advances in neural information processing systems, 30, 2017.
* [23]

  Pin-Hao Huang, Han-Hung Lee, Hwann-Tzong Chen, and Tyng-Luh Liu.
  Text-guided graph neural networks for referring 3d instance
  segmentation.
  Proceedings of the AAAI Conference on Artificial Intelligence,
  35(2):1610–1618, May 2021.
* [24]

  Faria Huq, Anindya Iqbal, and Nafees Ahmed.
  Holistic static and animated 3d scene generation from diverse text
  descriptions.
  CoRR, abs/2010.01549, 2020.
* [25]

  Sergey Ioffe and Christian Szegedy.
  Batch normalization: Accelerating deep network training by reducing
  internal covariate shift.
  In International conference on machine learning, pages
  448–456. PMLR, 2015.
* [26]

  Chao Jia, Yinfei Yang, Ye Xia, Yi-Ting Chen, Zarana Parekh, Hieu Pham, Quoc V
  Le, Yunhsuan Sung, Zhen Li, and Tom Duerig.
  Scaling up visual and vision-language representation learning with
  noisy text supervision.
  arXiv preprint arXiv:2102.05918, 2021.
* [27]

  Armand Joulin, Laurens Van Der Maaten, Allan Jabri, and Nicolas Vasilache.
  Learning visual features from large weakly supervised data.
  In European Conference on Computer Vision, pages 67–84.
  Springer, 2016.
* [28]

  Andrej Karpathy, Armand Joulin, and Li Fei-Fei.
  Deep fragment embeddings for bidirectional image sentence mapping.
  arXiv preprint arXiv:1406.5679, 2014.
* [29]

  Sungwon Kim, Sang gil Lee, Jongyoon Song, Jaehyeon Kim, and Sungroh Yoon.
  Flowavenet : A generative flow for raw audio, 2019.
* [30]

  Diederik P Kingma and Jimmy Ba.
  Adam: A method for stochastic optimization.
  arXiv preprint arXiv:1412.6980, 2014.
* [31]

  Diederik P. Kingma and Prafulla Dhariwal.
  Glow: Generative flow with invertible 1x1 convolutions, 2018.
* [32]

  Manoj Kumar, Mohammad Babaeizadeh, Dumitru Erhan, Chelsea Finn, Sergey Levine,
  Laurent Dinh, and Durk Kingma.
  Videoflow: A conditional flow-based model for stochastic video
  generation, 2020.
* [33]

  Christoph Lampert, Hannes Nickisch, and Stefan Harmeling.
  Learning to detect unseen object classes by between-class attribute
  transfer.
  06 2009.
* [34]

  Chun-Liang Li, Manzil Zaheer, Yang Zhang, Barnabas Poczos, and Ruslan
  Salakhutdinov.
  Point cloud gan.
  arXiv preprint arXiv:1810.05795, 2018.
* [35]

  Angela S. Lin, Lemeng Wu, Rodolfo Corona, Kevin W. H. Tai, Qixing Huang, and
  Raymond J. Mooney.
  Generating animated videos of human activities from natural language
  descriptions.
  2018.
* [36]

  Jinlin Liu, Yuan Yao, and Jianqiang Ren.
  An acceleration framework for high resolution image synthesis.
  arXiv preprint arXiv:1909.03611, 2019.
* [37]

  Lars Mescheder, Michael Oechsle, Michael Niemeyer, Sebastian Nowozin, and
  Andreas Geiger.
  Occupancy networks: Learning 3d reconstruction in function space.
  In Proceedings IEEE Conf. on Computer Vision and Pattern
  Recognition (CVPR), 2019.
* [38]

  Abhishek Mishra.
  Machine learning in the aws cloud: Add intelligence to applications
  with amazon sagemaker and amazon rekognition, 2019.
* [39]

  Charlie Nash, Yaroslav Ganin, S. M. Ali Eslami, and Peter W. Battaglia.
  Polygen: An autoregressive generative model of 3d meshes.
  ICML, 2020.
* [40]

  Aaron van den Oord, Oriol Vinyals, and Koray Kavukcuoglu.
  Neural discrete representation learning.
  arXiv preprint arXiv:1711.00937, 2017.
* [41]

  Daniil Pakhomov, Sanchit Hira, Narayani Wagle, Kemar E Green, and Nassir Navab.
  Segmentation in style: Unsupervised semantic image segmentation with
  stylegan and clip.
  arXiv preprint arXiv:2107.12518, 2021.
* [42]

  Mark Palatucci, Dean Pomerleau, Geoffrey E Hinton, and Tom M Mitchell.
  Zero-shot learning with semantic output codes.
  In Y. Bengio, D. Schuurmans, J. Lafferty, C. Williams, and A.
  Culotta, editors, Advances in Neural Information Processing Systems,
  volume 22. Curran Associates, Inc., 2009.
* [43]

  George Papamakarios, Theo Pavlakou, and Iain Murray.
  Masked autoregressive flow for density estimation.
  arXiv preprint arXiv:1705.07057, 2017.
* [44]

  Jeong Joon Park, Peter Florence, Julian Straub, Richard Newcombe, and Steven
  Lovegrove.
  Deepsdf: Learning continuous signed distance functions for shape
  representation.
  In The IEEE Conference on Computer Vision and Pattern
  Recognition (CVPR), June 2019.
* [45]

  Or Patashnik, Zongze Wu, Eli Shechtman, Daniel Cohen-Or, and Dani Lischinski.
  Styleclip: Text-driven manipulation of stylegan imagery.
  arXiv preprint arXiv:2103.17249, 2021.
* [46]

  Songyou Peng, Michael Niemeyer, Lars Mescheder, Marc Pollefeys, and Andreas
  Geiger.
  Convolutional occupancy networks.
  In Computer Vision–ECCV 2020: 16th European Conference,
  Glasgow, UK, August 23–28, 2020, Proceedings, Part III 16, pages 523–540.
  Springer, 2020.
* [47]

  Albert Pumarola, Stefan Popov, Francesc Moreno-Noguer, and Vittorio Ferrari.
  C-flow: Conditional generative flow models for images and 3d point
  clouds, 2020.
* [48]

  Charles R Qi, Hao Su, Kaichun Mo, and Leonidas J Guibas.
  Pointnet: Deep learning on point sets for 3d classification and
  segmentation.
  In Proceedings of the IEEE conference on computer vision and
  pattern recognition, pages 652–660, 2017.
* [49]

  Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh,
  Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark,
  Gretchen Krueger, and Ilya Sutskever.
  Learning transferable visual models from natural language
  supervision, 2021.
* [50]

  Aditya Ramesh, Mikhail Pavlov, Gabriel Goh, Scott Gray, Chelsea Voss, Alec
  Radford, Mark Chen, and Ilya Sutskever.
  Zero-shot text-to-image generation, 2021.
* [51]

  Danilo Rezende and Shakir Mohamed.
  Variational inference with normalizing flows.
  In International conference on machine learning, pages
  1530–1538. PMLR, 2015.
* [52]

  Jonas Rothfuss, Fabio Ferreira, Simon Boehm, Simon Walther, Maxim Ulrich, Tamim
  Asfour, and Andreas Krause.
  Noise regularization for conditional density estimation.
  arXiv preprint arXiv:1907.08982, 2019.
* [53]

  Mert Bulent Sariyildiz, Julien Perez, and Diane Larlus.
  Learning visual representations with caption annotations.
  In Computer Vision–ECCV 2020: 16th European Conference,
  Glasgow, UK, August 23–28, 2020, Proceedings, Part VIII 16, pages 153–170.
  Springer, 2020.
* [54]

  Sheng Shen, Liunian Harold Li, Hao Tan, Mohit Bansal, Anna Rohrbach, Kai-Wei
  Chang, Zhewei Yao, and Kurt Keutzer.
  How much can clip benefit vision-and-language tasks?
  arXiv preprint arXiv:2107.06383, 2021.
* [55]

  Richard Socher, Andrej Karpathy, Quoc V Le, Christopher D Manning, and Andrew Y
  Ng.
  Grounded compositional semantics for finding and describing images
  with sentences.
  Transactions of the Association for Computational Linguistics,
  2:207–218, 2014.
* [56]

  Chuan Tang, Xi Yang, Bojian Wu, Zhizhong Han, and Yi Chang.
  Part2word: Learning joint embedding of point clouds and text by
  matching parts to words, 2021.
* [57]

  Nanyang Wang, Yinda Zhang, Zhuwen Li, Yanwei Fu, Wei Liu, and Yu-Gang Jiang.
  Pixel2mesh: Generating 3d mesh models from single rgb images.
  In ECCV, 2018.
* [58]

  Jiajun Wu, Chengkai Zhang, Tianfan Xue, William T. Freeman, and Joshua B.
  Tenenbaum.
  Learning a probabilistic latent space of object shapes via 3d
  generative-adversarial modeling.
  In Proceedings of the 30th International Conference on Neural
  Information Processing Systems, NIPS’16, page 82–90, Red Hook, NY, USA,
  2016. Curran Associates Inc.
* [59]

  Guandao Yang, Xun Huang, Zekun Hao, Ming-Yu Liu, Serge Belongie, and Bharath
  Hariharan.
  Pointflow: 3d point cloud generation with continuous normalizing
  flows.
  In Proceedings of the IEEE/CVF International Conference on
  Computer Vision, pages 4541–4550, 2019.
* [60]

  Yaoqing Yang, Chen Feng, Yiru Shen, and Dong Tian.
  Foldingnet: Point cloud auto-encoder via deep grid deformation.
  In Proceedings of the IEEE Conference on Computer Vision and
  Pattern Recognition, pages 206–215, 2018.
* [61]

  Kaiyang Zhou, Jingkang Yang, Chen Change Loy, and Ziwei Liu.
  Learning to prompt for vision-language models.
  arXiv preprint arXiv:2109.01134, 2021.

[◄](/html/2110.02623)
[![ar5iv homepage](/assets/ar5iv.png)](/)
[Feeling  
lucky?](/feeling_lucky)

[Conversion  
report](/log/2110.02624)
[Report  
an issue](https://github.com/dginev/ar5iv/issues/new?template=improve-article--arxiv-id-.md&title=Improve+article+2110.02624)
[View original  
on arXiv](https://arxiv.org/abs/2110.02624)[►](/html/2110.02625)

[Copyright](https://arxiv.org/help/license)
[Privacy Policy](https://arxiv.org/help/policies/privacy_policy)

Generated on Tue Mar 19 14:53:29 2024 by [LaTeXML](http://dlmf.nist.gov/LaTeXML/)
