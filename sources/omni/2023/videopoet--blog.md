# VideoPoet – Google Research
Source: https://sites.research.google/videopoet/
VideoPoet – Google Research



[VideoPoet](/videopoet/)

[VideoPoet](/videopoet/)

[Text-to-Video](/videopoet/text-to-video/)[Image-to-Video](/videopoet/image-to-video/)[Video Editing](/videopoet/video-editing/)[Stylization](/videopoet/stylization/)[Inpainting](/videopoet/inpainting/)

[Text-to-Video](/videopoet/text-to-video/)[Image-to-Video](/videopoet/image-to-video/)[Video Editing](/videopoet/video-editing/)[Stylization](/videopoet/stylization/)[Inpainting](/videopoet/inpainting/)

# VideoPoet

### A large language model for zero-shot video generation

[

](https://storage.googleapis.com/googwebreview.appspot.com/grow-ext-cloud-images-uploads/ryzlk7wp5wkm-4jLzeQ74y8obz368S6CrWA-d29039d269d486adf3408f2fdf8bb2e9-008_headphones_743EB6DB.mp4)

A dog listening to music with headphones, highly detailed, 8k.

[

](https://storage.googleapis.com/googwebreview.appspot.com/grow-ext-cloud-images-uploads/ryzlk7wp5wkm-55zNkVz2Ws28FGUjznvReZ-693e25f192dfd423a04d9e17562805f1-003_paint_CD8173E2.mp4)

A large blob of exploding splashing rainbow paint, with an apple emerging, 8k

[

](https://storage.googleapis.com/googwebreview.appspot.com/grow-ext-cloud-images-uploads/ryzlk7wp5wkm-6mmaKzomn59IGgLbQ4i9W4-bd05d89af2b38325ca43cbc1cfb53595-083_robot_cat_2_C2FB5EC1.mp4)

A robot cat eating spaghetti, digital art.

[

](https://storage.googleapis.com/googwebreview.appspot.com/grow-ext-cloud-images-uploads/ryzlk7wp5wkm-7sYcqsUgmsSYot38z6FAyM-59fec83c50b749855c38d9debccc30dc-124_pumpkin_explosion_2_7A7101BD.mp4)

A pumpkin exploding, slow motion.

[

](https://storage.googleapis.com/googwebreview.appspot.com/grow-ext-cloud-images-uploads/ryzlk7wp5wkm-2MQ3VPgyhlNFOrP9apwyrc-c88810720624f8d97018e2d92f638e08-002_panda_10261DD3.mp4)

Two pandas playing cards.

[

](https://storage.googleapis.com/googwebreview.appspot.com/grow-ext-cloud-images-uploads/ryzlk7wp5wkm-1BlazIIXhUWloSSs6JpN9p-d19b6626fe5eb888f5f818b002707703-084_vaporwave_dog_372A07E9.mp4)

A vaporwave fashion dog in Miami looks around and barks, digital art.

[

](https://storage.googleapis.com/googwebreview.appspot.com/grow-ext-cloud-images-uploads/ryzlk7wp5wkm-5fG5eS5rX9XYJMZwjpRzPe-51ef8fd6babcd608066afab4dcd1d2e6-110_astronaut_horse_9E70EDB0.mp4)

An astronaut riding a galloping horse.

[

](https://storage.googleapis.com/googwebreview.appspot.com/grow-ext-cloud-images-uploads/ryzlk7wp5wkm-5syOEtbGNoKYu3F1TscERJ-26545ce27cd16a259e3e6ba53bdada2d-139_cabin_90FD75EF.mp4)

A family of raccoons living in a small cabin, tilt shift, arc shot.

[

](https://storage.googleapis.com/googwebreview.appspot.com/grow-ext-cloud-images-uploads/ryzlk7wp5wkm-aVYUfOW7LvbSG4O0aG2tz-a36f0c9bc0f3ad63104c713bf3c52222-152_cyberpunk_fpv_4DDE598F.mp4)

A golden retriever wearing VR goggles and eating pizza in Paris.

[

](https://storage.googleapis.com/googwebreview.appspot.com/grow-ext-cloud-images-uploads/ryzlk7wp5wkm-4pjPQHCZJaVCqZQiswSQys-1b6fc60090ec66c1982b4d7c4cc9c7f1-079_tree_6DB2EA13.mp4)

A tree walking through the forest, tilt shift.

A walking figure made out of water

A shark with a laser beam coming out of its mouth.

Teddy bears holding hands, walking down rainy 5th ave

A chicken lifting weights.

An origami fox walking through the forest.

Robot emerging from a large column of billowing black smoke, high quality.

A t-rex jumping over a cactus, with water gushing after the t-rex falls.

A mouse eating cheese in a royal dress, arc shot.

An alien enjoys food, 8k.

A lion with a mane made out of yellow dandelion petals roars.

A massive explosion on the surface of the earth.

A horse galloping through Van Gogh's 'starry night'.

A squirrel in armor riding a goose, action shot.

A panda taking a selfie.

An octopus attacks New York.

A bear with the head of an owl screeches loudly

An astronaut typing on a keyboard, arc shot.

A rabbit eating grass, soft lighting.

Flag of the US on top of a tall white mountain, rotating panorama.

Motorcyclist on a racing track, highly detailed.

A massive tidal wave crashes dramatically against a rugged coastline, digital art.

Humans building a highway on Mars, cinematic.

A skeleton drinking a glass of soda.

The orient express driving through a fantasy landscape, animated oil on canvas.

VideoPoet can output high-motion variable length videos given a text prompt.

#### Video-to-audio

VideoPoet can also output audio to match an input video without using any text as guidance. Unmute the videos to play the audio.

A dog eating popcorn at the cinema.

A teddy bear with a cap, sunglasses, and leather jacket playing drums.

A teddy bear in a leather jacket, baseball cap, and sunglasses playing guitar in front of a waterfall.

A pink cat playing piano in the forest.

The orient express driving through a fantasy landscape, oil on canvas.

A dragon breathing fire, cinematic.

### Using generative models to tell visual stories

To showcase VideoPoet's capabilities, we have produced a short movie composed of many short clips generated by the model. For the script, we asked [Bard](https://bard.google.com/) to write a series of prompts to detail a short story about a traveling raccoon. We then generated video clips for each prompt, and stitched together all resulting clips to produce the final [YouTube Short](https://www.youtube.com/shorts/70wZKfx6Ylk) below.

## Introduction

VideoPoet is a simple modeling method that can convert any autoregressive language model or large language model (LLM) into a high-quality video generator. It contains a few simple components:

* A pre-trained [MAGVIT V2](https://magvit.cs.cmu.edu/v2/) video tokenizer and a [SoundStream](https://blog.research.google/2021/08/soundstream-end-to-end-neural-audio.html) audio tokenizer transform images, video, and audio clips with variable lengths into a sequence of discrete codes in a unified vocabulary. These codes are compatible with text-based language models, facilitating an integration with other modalities, such as text.
* An [autoregressive language model](https://en.wikipedia.org/wiki/Autoregressive_model) learns across video, image, audio, and text modalities to autoregressively predict the next video or audio token in the sequence.
* A mixture of multimodal generative learning objectives are introduced into the LLM training framework, including text-to-video, text-to-image, image-to-video, video frame continuation, video inpainting and outpainting, video stylization, and video-to-audio. Furthermore, such tasks can be composed together for additional zero-shot capabilities (e.g., text-to-audio).

This simple recipe shows that language models can synthesize and edit videos with a high degree of temporal consistency. VideoPoet demonstrates state-of-the-art video generation, in particular in producing a wide range of large, interesting, and high-fidelity motions. The VideoPoet model supports generating videos in square orientation, or portrait to tailor generations towards short-form content, as well as supporting audio generation from a video input.

### Resources

[Paper](https://arxiv.org/abs/2312.14125)[Research Blog](https://blog.research.google/2023/12/videopoet-large-language-model-for-zero.html)

[

](https://storage.googleapis.com/googwebreview.appspot.com/grow-ext-cloud-images-uploads/ryzlk7wp5wkm-1mtsV1LWXSHTiEABiYXKQx-70d96a247aff751b96c4ae79cf93ff8c-videopoet_header_video_3662C1DB.mp4)

*An overview of the VideoPoet model, which is capable of multitasking on a variety of video-centric inputs and outputs. The LLM can optionally take text as input to guide generation for text-to-video, image-to-video, stylization, and outpainting tasks. Resources used:* [*Wikimedia Commons*](https://commons.wikimedia.org/wiki/Main_Page) *and* [*DAVIS*](https://davischallenge.org/)*.*

---

### Quick Links

To view additional results, please also visit our other pages:

[Text-to-Video](http://sites.research.google/videopoet/text-to-video) - [Image-to-Video](http://sites.research.google/videopoet/image-to-video) - [Video Editing](http://sites.research.google/videopoet/video-editing) - [Stylization](http://sites.research.google/videopoet/stylization) - [Inpainting](http://sites.research.google/videopoet/inpainting)

### Visual narratives

Prompts can be changed over time to tell visual stories.

Input Video

A walking figure made out of water.

Extended Video

A walking figure made out of water. Lightning flashes in the background. Purple smoke emits from the figure of water.

Input Video

Two raccoons on motorbikes on a mountain road surrounded by pine trees, 8k.

Extended Video

Two raccoons on motorbikes. A meteor shower falls behind the raccoons. The meteors impact the earth and explode.

See the [Video Editing](http://sites.research.google/videopoet/video-editing) page for additional results.

### Long(er) video generation

By default, VideoPoet outputs 2-second videos. But the model is also capable of long video generation by predicting 1 second of video output given an input of a 1-second video clip. This process can be repeated indefinitely to produce a video of any duration. Despite the short input context, the model shows strong object identity preservation not seen in prior works, as demonstrated in these longer duration clips.

An astronaut starts dancing on Mars as colorful fireworks explode in the background.

FPV drone footage of a very sharp elven city of stone in the jungle with a brilliant blue river, waterfall, and large steep vertical cliff faces.

Teddy bears holding hands, walking down rainy 5th ave

FPV drone footage entering a cyberpunk city at night with many neon lights and reflective surfaces.

A large blob of exploding splashing rainbow paint, with an apple emerging, 8k

FPV drone footage of an ancient city in autumn.

See the [Video Editing](http://sites.research.google/videopoet/video-editing) page for additional results.

### Controllable video editing

The VideoPoet model can edit a subject to follow different motions, such as dance styles. In the example below, the model processes an the same input clip with different prompts.

Input Video

A raccoon dancing in Times Square.

A raccoon dancing [the robot](https://en.wikipedia.org/wiki/Robot_(dance)) in Times Square.

A raccoon dancing [the griddy](https://en.wikipedia.org/wiki/Griddy) in Times Square.

A raccoon dancing [freestyle](https://en.wikipedia.org/wiki/Dance_improvisation) in Times Square.

See the [Video Editing](http://sites.research.google/videopoet/video-editing) page for additional results.

### Interactive video editing

Interactive editing is also possible, extending input videos a short duration and selecting from a list of examples. By selecting the best video from a list of candidates, we can finely control the types of desired motion from a larger generated video. Here we generate three samples without text conditioning and the final one with text conditioning.

Input Video

Closeup of an adorable rusty broken-down steampunk robot covered in moss moist and budding vegetation, surrounded by tall grass.

Sample 1 (no prompt)

Sample 2 (no prompt)

Sample 3 (no prompt)

Powering up with smoke in the background.

See the [Video Editing](http://sites.research.google/videopoet/video-editing) page for additional results.

### Image to video generation

VideoPoet can take any input image and generate a video matching a given text prompt.

![](https://lh3.googleusercontent.com/QF-7PqiW8tdqLc7ZinvLGifr_XSi4OUuwdrIpaRq--qbXE0gMWlV_wA9TQUNTdulWMYo1hs12U73s0dKVcB_Cl5BUYPb3Ga9OFRRL7BC=w2880-e365-pa-nu)

Image

Video

A geyser spraying water into the air.

![](https://lh3.googleusercontent.com/K0EIYB4lxoOx96_CtgUuXkM1RJqrm_DhVud5HjvcH8Nzv67gTASzCKFSWChu5Hj5xObPL5T5SNqZxJHMFyS12xxCtvrSlvc_qEsIa-Mg=w2880-e365-pa-nu)

Image

Video

Flying through a nebula with many twinkling stars.

![](https://lh3.googleusercontent.com/AXWNOca-Xyqb8fBdsbDCdL6jZYPy7ovo9wgLBgFHQ5uamor_E6iU-vx5d15V9bWroGecJu5kwuiAILlhkLbBbCNuWC1bfn7w5q3R8BY=w2880-e365-pa-nu)

Image

Video

White milk splashing in a ring, a drop above the ring falls down, making a splash.

![](https://lh3.googleusercontent.com/YQ_a0hb2dSgHe0N_Q-UZxZTNa4T2SkV0LICr5pyPqmnmOa1ovX_ClAEWIEIQvSy5uoXM3kbnRp55nsmn2GURDa7-aAX73PfbtT_09wA=w2880-e365-pa-nu)

Image

Video

A ship navigating the rough seas with several passengers on board, thunderstorm and lightning, animated oil on canvas.

![](https://lh3.googleusercontent.com/-Bt3YIUMYgkUebubTf2xlhv5vm83uI5J045zpQyzKxNdPYvRfDznJFTm6e7y5_kEQ_SZJloAqAfuxKGxuEFBpUvzsXARixQDTmhu3rA=w2880-e365-pa-nu)

Image

Video

A green man riding a green horse with the wind blowing.

![](https://lh3.googleusercontent.com/Si7o4HbxCwV0yZmhhalKvqZPUYwbj6LTikPoMSDbXdQgstL6Blo-fKxrBxrk2Hb8uJLX1zbzH2dDj2YFLDBCxznzqeXy_58xcyUSsrA=w2880-e365-pa-nu)

Image

Video

Soldiers raising the united states flag on a windy day.

![](https://lh3.googleusercontent.com/Ab4rtZURQJHXKTK25qhyBNGx48lFTZQUCjnDNkNB4AfiyX39Wyp1fXA98NDb9ksykKmyCwwmjwrWXgi7K3aMLKa8E99Yv359Wljgzg=w2880-e365-pa-nu)

Image

Video

A wanderer on a cliff with a cane looking down at the swirling sea fog below on a windy day.

![](https://lh3.googleusercontent.com/Rtvhx0KVhmzmS1HTBmyPVASbYLL9wFwsWjVc-n7vWGp2ubk9emJrLTIf-sA2b6u1py9P9WTZUKvsuxpx1Ybyil6EW0JmvDbhWhvrwZU=w2880-e365-pa-nu)

Image

Video

A woman yawning.

Images source: [Wikimedia Commons](https://commons.wikimedia.org/wiki/Main_Page), see footnote\*\*

### Zero-shot stylization

VideoPoet is also capable of stylizing input videos guided by a text prompt, and demonstrates stylistically pleasing prompt adherence.

Input

Stylized

Wombat wearing sunglasses holding a beach ball on a sunny beach.

Input

Stylized

Teddy bears ice skating on a crystal clear frozen lake.

Input

Stylized

A metal lion roaring in the light of a forge.

Input

Stylized

A pink and blue confetti geyser with candy coated tress.

Input

Stylized

A red and white woodcut print of a man overlooking a stormy sea.

Input

Stylized

A magical snow-covered forest of dense pine trees.

See the [Stylization](http://sites.research.google/videopoet/stylization) page for additional results.

### Applying Visual Styles and Effects

Styles and effects can easily be composed in text-to-video generation. We start with a base prompt and append a style to it.

Prompt: "An astronaut riding a horse in a lush forest".

Photorealistic

Digital art

Pencil art

Ink wash

Double exposure

Small world

See the [Stylization](http://sites.research.google/videopoet/stylization) page for additional results.

### Zero-shot controllable camera motions

One emergent property of VideoPoet's pre-training is that a large degree of high-quality camera motion customization is possible by specifying the type of camera shot in the text prompt.

Prompt: "Adventure game concept art of a sunrise over a snowy mountain by a crystal clear river."

Zoom out

Dolly zoom

Pan left

Arc shot

Crane shot

FPV drone shot

### Quick Links

To view additional results, please also visit our other pages:

[Text-to-Video](http://sites.research.google/videopoet/text-to-video) - [Image-to-Video](http://sites.research.google/videopoet/image-to-video) - [Video Editing](http://sites.research.google/videopoet/video-editing) - [Stylization](http://sites.research.google/videopoet/stylization) - [Inpainting](http://sites.research.google/videopoet/inpainting)

### Authors

Dan Kondratyuk\*, Lijun Yu\*, Xiuye Gu\*, José Lezama\*, Jonathan Huang, Rachel Hornung, Hartwig Adam, Hassan Akbari, Yair Alon, Vighnesh Birodkar, Yong Cheng, Ming-Chang Chiu, Josh Dillon, Irfan Essa, Agrim Gupta, Meera Hahn, Anja Hauth, David Hendon, Alonso Martinez, David Minnen, David Ross, Grant Schindler, Mikhail Sirotenko, Kihyuk Sohn, Krishna Somandepalli, Huisheng Wang, Jimmy Yan, Ming-Hsuan Yang, Xuan Yang, Bryan Seybold\*, Lu Jiang\*

---

\*Equal technical contribution

### Acknowledgements

*We give special thanks to Alex Siegman, Victor Gomes, and Brendan Jou for managing computing resources. We also give thanks to Aren Jansen, Marco Tagliasacchi, Neil Zeghidour, John Hershey for audio tokenization and processing, Angad Singh for storyboarding in “Rookie the Raccoon”, Cordelia Schmid for research discussions, David Salesin, Tomas Izo, and Rahul Sukthankar for their support, and Jay Yagnik as architect of the initial concept.*

---

*\*\*Referenced works:*

* [Old Faithful](https://commons.wikimedia.org/wiki/File:Bierstadt_Albert_Old_Faithful.jpg), public domain.
* [Pillars of Creation](https://commons.wikimedia.org/wiki/File:Pillars_of_creation_2014_HST_WFC3-UVIS_full-res.jpg), public domain.
* [Milk Drop Coronet](https://www.artic.edu/artworks/120885/milk-drop-coronet), [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/).
* [The Storm on the Sea of Galilee](https://commons.wikimedia.org/wiki/File:Rembrandt_Christ_in_the_Storm_on_the_Lake_of_Galilee.jpg), public domain.
* [George III Statue](https://commons.wikimedia.org/wiki/File:George_III_Statue.jpg), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.en).
* [Raising the Flag on Iwo Jima](https://en.wikipedia.org/wiki/File:Raising_the_Flag_on_Iwo_Jima,_larger_-_edit1.jpg), public domain.
* [Wanderer above the Sea of Fog](https://commons.wikimedia.org/wiki/File:Caspar_David_Friedrich_-_Wanderer_above_the_Sea_of_Fog.jpeg), public domain.
* [Mona Lisa](https://commons.wikimedia.org/wiki/File:Mona_Lisa,_by_Leonardo_da_Vinci,_from_C2RMF_retouched.jpg), public domain.

[About Google](https://about.google/)[Privacy](https://policies.google.com/privacy)[Terms](https://policies.google.com/terms)
