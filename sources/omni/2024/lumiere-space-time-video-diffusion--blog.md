# Lumiere
Source: https://lumiere-video.github.io/
Lumiere



[Text-to-Video](#section_text_to_video)
[Image-to-Video](#section_image_to_video)
[Stylized Generation](#section_stylized_generation)
[Video Stylization](#section_video_stylization)
[Cinemagraphs](#section_magic_animator)
[Inpainting](#section_inpainting)

Google Research

# LUMIERE

A Space-Time Diffusion Model for Video Generation

[Read Paper](https://arxiv.org/abs/2401.12945)

# Text-to-Video

\* Hover over the video to see the input prompt.

Aerial Around Young Hiker Man Standing on Mountain Peak Summit At Sunrise

Aurora Borealis Green Loop Winter Mountain Ridges Northern Lights

Astronaut on the planet Mars making a detour around his base

A dog driving a car on a suburban street wearing funny sunglasses

Back view on young woman dressed in a bright yellow jacket walk in outdoor forest

Golden retriever puppy running in the park. Autumn. Beautiful leaves on the ground.

Chocolate syrup pouring on vanilla ice cream

Bloomming cherry tree in the garden beautiful sun light

Sailboat sailing on a sunny day in a mountain lake

A young couple walking in a heavy rain

A panda eating bamboo on a rock

A musk ox grazing on a beautiful wildflowers

A knight riding on a horse through the countryside

Flying through a temple in ruins

Camera moving through dry grass at autumn morning

Aerial view of colorful fireworks exploding in the night sky

US flag waving on massive sunrise clouds

Beer pouring into glass

Funny cute pug dog feeling good listening to music with big headphones and swinging head

Sunset timelapse at the beach

Yellow flowers swing in the wind

Jack russel terrier snowboarding. GoPro shot.

A red lamborghini aventador coming around abend in a mountain road

Bright underwater world orange fish

Confident teddy bear surfer rides the wave in the tropics

Toy poodle dog rides a penny board outdoors

Chocolate muffin video clip

A cute mouse typing on a keyboard

360 camera shot of a sushi roll in a restaurant

Colorful fish swimming underwater

Panda play ukelele at home

Silhouette of a wolf against a twilight sky

# Image-to-Video

\* Hover over the video to see the input image and prompt.

A sad cat in a striped navy blue shirt

A teddybear dancing in the snow

A spooky skeleton

A turtle swimming

Flying through an intense battle between pirate ships in a stormy ocean

An escaped panda eating popcorn in the park

A bee holding a jar of honey

A monkey drinking coffee while working on his laptop

Campfire at night in a snowy forest with starry sky in the background

Bigfoot walking through the woods

A factory robot assembling intricate electronic components with precision

A teddy bear running in New York city

A panda eating bamboo on a rock

A giraffe eating grass

A relaxed ocean waves video

A car driving on the beach

Sailboat sailing on a sunny day in a mountain lake

A panda bear driving a car

A happy elephant wearing a birthday hat walking under the sea

A snowflake falls from the sky

Melting pistachio ice cream dripping down the cone

A teddy bear skating in Times Square

A fluffy baby sloth with an orange knitted hat trying to figure out a laptop

A cat playing the piano

A girl winking and smiling

A man smiling and waving

Soldiers raising the united states flag on a windy day.

Zooming through a nebula with many twinkling stars

A timelapse oil painting of a starry night with clouds moving

A big ocean wave

A woman looking tired and yawning

Ancient pharaoh smiling and shaking his head

# Stylized Generation

Using a single reference image, Lumiere can generate videos in the target style by utilizing fine-tuned text-to-image model weights.   
\* Hover over the video to see the prompt.

![](images/20710341_3wjw_xfps_210629.jpg)

A family of ducks swimming in a pond

A butterfly fluttering from flower to flower

A colorful parrot showing off its vibrant feathers

An owl perched on a branch

A koala munching on eucalyptus leaves

A cute bunny nibbling on a carrot

A squirrel gathering acorns

A fox frolicking in the forest

Style reference image

"Sticker"

![](images/reference_image.jpg)

An owl perched on a branch

A flower blooming

A dolphin leaping out of the water

A swan swimming in a lake

A chubby panda munching on bamboo shoots

A drifting dandelion seed in the breeze

A lion with a majestic mane

An elephant trumpeting joyfully

Style reference image

"3D Melting Gold"

![](images/flat_cartoon_reference_image.jpg)

A bear twirling with delight

A cute bunny nibbling on a carrot

A dolphin leaping out of the water

A sunflower blooming

A hot air balloon inflating and taking off

A wise owl perched on a tree branch

A group of penguins waddling in the snow

A family of ducks swimming in a pond

Style reference image

"Flat cartoon"

![](images/3d_ref.jpg)

A bear dancing

A colorful parrot showing off its vibrant feathers

An owl perched on a branch

A bunny hopping in a meadow

A butterfly fluttering from flower to flower

A family of ducks swimming in a pond

A dolphin leaping out of the water

A graceful swan griding across a serene lake

Style reference image

"3D Rendering"

![](images/cartoon_line_drawing_reference_image.jpg)

An owl perched on a branch

A lion with a majestic mane

A koala munching on eucalyptus leaves

A fox frolicking in the forest

A squirrrel gathering acorns

A majestic horse

A bear

A monkey

Style reference image

"Line drawing"

![](images/glow_ref.jpeg)

A colorful parrot showing off its vibrant feathers

A bear dancing

A butterfly fluttering from flower to flower

A horse galloping

A dragon

A penguin dancing

A giraffe

A lion with a majestic mane roaring

Style reference image

"Glowing"

![](images/watercolor_reference_image.jpg)

A raccoon dancing

A cat drinking milk from a bowl

A chubby panda munching on bamboo shoots

A horse galloping across a field

A girl with a beanie dancing

A family of ducks swimming in a pond

A dog walking

A dolphin leaping out of the water

Style reference image

"Watercolor painting"

# Introduction

We introduce Lumiere -- a text-to-video diffusion model designed for synthesizing videos that portray realistic, diverse and coherent motion -- a pivotal challenge in video synthesis. To this end, we introduce a Space-Time U-Net architecture that generates the entire temporal duration of the video at once, through a single pass in the model. This is in contrast to existing video models which synthesize distant keyframes followed by temporal super-resolution -- an approach that inherently makes global temporal consistency difficult to achieve. By deploying both spatial and (importantly) temporal down- and up-sampling and leveraging a pre-trained text-to-image diffusion model, our model learns to directly generate a full-frame-rate, low-resolution video by processing it in multiple space-time scales. We demonstrate state-of-the-art text-to-video generation results, and show that our design easily facilitates a wide range of content creation tasks and video editing applications, including image-to-video, video inpainting, and stylized generation.

![](images/architecture.png)

# Video Stylization

With Lumiere, off-the-shelf text-based image editing methods can be used for consistent video editing.

Source Video

"Made of wooden blocks"

"Origami folded paper art"

"Made of colorful toy bricks"

"Made of flowers"

Source Video

"Made of stacked wooden blocks"

"Origami folded paper art"

"Made of colorful toy bricks"

"Made of flowers"

Source Video

"Made of stacked wooden blocks"

"Origami folded paper art"

"Made of colorful toy bricks"

"Made of flowers"

Source Video

"Made of stacked wooden blocks"

"Origami folded paper art"

"Made of colorful toy bricks"

"Made of flowers"

# Cinemagraphs

The Lumiere model is able to animate the content of an image within a specific user-provided region.

Input Image + Mask

Output Video

Input Image + Mask

Output Video

![](images/butterfly_with_mask.jpg)

![](images/fire_with_mask.jpg)

![](images/lake_with_mask.jpg)

![](images/train_with_mask.jpg)

# Video Inpainting

Source Masked Video

Output Video

Source Masked Video

Output Video

Source Video

"wearing a gold strapless gown"

"wearing a striped strapless dress"

"wearing a purple strapless dress"

"wearing a black strapless gown"

Source Video

"wearing a crown"

"wearing sunglasses"

"wearing a red scarf"

"wearing a purple tie"

Source Video

"wearing a bath robe"

"wearing a party hat"

"Standing on a stool"

"wearing rain boots"

# Authors

[Omer Bar-Tal\*,1,2](https://omerbt.github.io/)
[Hila Chefer\*,1,3](https://hila-chefer.github.io/)
[Omer Tov\*,1](https://scholar.google.com/citations?user=lbo_R54AAAAJ&hl=en)
[Charles Herrmann†,1](https://scholar.google.com/citations?user=LQvi5XAAAAAJ&hl=en)
[Roni Paiss†,1](https://scholar.google.com/citations?user=-KSDNZQAAAAJ&hl=en)

[Shiran Zada†,1](https://scholar.google.com/citations?hl=en&user=I2qheksAAAAJ)
[Ariel Ephrat†,1](https://scholar.google.com/citations?user=n4dxd1YAAAAJ&hl=en)
[Junhwa Hur†,1](https://scholar.google.com/citations?hl=en&user=z4dNJdkAAAAJ)
[Guanghui Liu1](https://www.linkedin.com/in/gl676c)
[Amit Raj1](https://amitraj93.github.io/)

[Yuanzhen Li1](https://scholar.google.com/citations?hl=en&user=k1eaag4AAAAJ)
[Michael Rubinstein1](https://people.csail.mit.edu/mrub/)
[Tomer Michaeli1,4](https://tomer.net.technion.ac.il/)
[Oliver Wang1](https://scholar.google.com/citations?user=0B8uuBkAAAAJ&hl=en)

[Deqing Sun1](https://scholar.google.com/citations?hl=en&user=t4rgICIAAAAJ)
[Tali Dekel1,2](https://www.weizmann.ac.il/math/dekel/home)
[Inbar Mosseri†,1](https://inbar-mosseri.github.io/)

1Google Research

2Weizmann Institute

3Tel-Aviv University

4Technion

(\*): Equal first co-author, (†) Core technical contribution  
Work was done while O. Bar-Tal, H. Chefer were interns at Google.

# Acknowledgements

*We would like to thank Ronny Votel, Orly Liba, Hamid Mohammadi, April Lehman, Bryan Seybold, David Ross, Dan Goldman, Hartwig Adam, Xuhui Jia, Xiuye Gu, Mehek Sharma, Keyu Zhang, Rachel Hornung, Oran Lang, Jess Gallegos, William T. Freeman and David Salesin for their collaboration, helpful discussions, feedback and support.  
We thank owners of images and videos used in our experiments (*[***links***](https://github.com/lumiere-video/lumiere-video.github.io/blob/main/assets/media_attributions.md) *for attribution) for sharing their valuable assets.*

*\* References:*
[*Mona Lisa*](https://commons.wikimedia.org/wiki/File:Mona_Lisa,_by_Leonardo_da_Vinci,_from_C2RMF_retouched.jpg)*, public domain.*
[*Pillars of Creation*](https://commons.wikimedia.org/wiki/File:Pillars_of_creation_2014_HST_WFC3-UVIS_full-res.jpg)*, public domain.*
[*Raising the Flag on Iwo Jima*](https://en.wikipedia.org/wiki/File:Raising_the_Flag_on_Iwo_Jima,_larger_-_edit1.jpg)*, public domain.*
[*Mask of Tutankhamun*](https://en.wikipedia.org/wiki/File:Raising_the_Flag_on_Iwo_Jima,_larger_-_edit1.jpg)*,* 
[*CC BY-SA 3.0*](https://creativecommons.org/licenses/by-sa/3.0)*.*
[*Girl with a Pearl Earring*](https://commons.wikimedia.org/wiki/File:1665_Girl_with_a_Pearl_Earring.jpg)*, public domain.*
[*Isaac Newton*](https://commons.wikimedia.org/wiki/Isaac_Newton#/media/File:Portrait_of_Sir_Isaac_Newton,_1689.jpg)*, public domain.*
[*Starry Night*](https://commons.wikimedia.org/wiki/File:Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg)*, public domain.*
[*The Great Wave of Kanagava*](https://commons.wikimedia.org/wiki/File:The_Great_Wave_of_Kanagava.jpg)*, public domain.  
‍*

# Societal Impact

Our primary goal in this work is to enable novice users to generate visual content in an creative and flexible way. However, there is a risk of misuse for creating fake or harmful content with our technology, and we believe that it is crucial to develop and apply tools for detecting biases and malicious use cases in order to ensure a safe and fair use.
