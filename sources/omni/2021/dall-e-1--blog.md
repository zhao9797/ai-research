# DALL·E：从文本创建图片 | OpenAI
Source: https://openai.com/zh-Hans-CN/index/dall-e/
DALL·E：从文本创建图片 | OpenAI

[跳至主要内容](#main)

* [研究](/zh-Hans-CN/research/index/)
* 产品
* [企业](/zh-Hans-CN/business/)
* [开发人员](/zh-Hans-CN/api/)
* [公司](/zh-Hans-CN/about/)
* [基金会（在新窗口中打开）](https://openaifoundation.org/zh-Hans-CN/)

登录[试用 ChatGPT（在新窗口中打开）](https://chatgpt.com/?openaicom-did=7a7e97a7-5b44-4eea-b313-b1f324ad16ea&openaicom_referred=true)

* 研究
* 产品
* 企业
* 开发人员
* 公司
* [基金会（在新窗口中打开）](https://openaifoundation.org/zh-Hans-CN/)

DALL·E：从文本创建图片 | OpenAI

2021年1月5日

[里程碑](/research/index/milestone/)

# DALL·E：从文本创建图片

我们训练了一个名为 DALL·E 的神经网络，它能根据文本标题创建图片，并能用自然语言表达各种概念。

![DALL·E](https://images.ctfassets.net/kftzwdyauwt9/ed21faee-ce44-4d91-f5cc39941d47/bdd3983530857e93d205304e219e2d95/dall-e.jpg?w=3840&q=90&fm=webp)

插图： 贾斯汀·杰·王

聆听文章

分享

概述

* [概述](#gai-shu)
* [功能](#gong-neng)

  + [控制属性](#kong-zhi-shu-xing)
  + [绘制多个对象](#hui-zhi-duo-ge-dui-xiang)
  + [透视和三维可视化](#tou-shi-he-san-wei-ke-shi-hua)
  + [内部和外部结构可视化](#nei-bu-he-wai-bu-jie-gou-ke-shi-hua)
* [推断背景细节](#tui-duan-bei-jing-xi-jie)

  + [前述能力的应用](#qian-shu-neng-li-de-ying-yong)
  + [组合不相关的概念](#zu-he-bu-xiang-guan-de-gai-nian)
* [动物插图](#dong-wu-cha-tu)

  + [零样本视觉推理](#ling-yang-ben-shi-jue-tui-li)
  + [地理知识](#di-li-zhi-shi)
  + [时间知识](#shi-jian-zhi-shi)
* [方法和前期工作总结](#fang-fa-he-qian-qi-gong-zuo-zong-jie)

目录

* [概述](#gai-shu)
* [功能](#gong-neng)

  + [控制属性](#kong-zhi-shu-xing)
  + [绘制多个对象](#hui-zhi-duo-ge-dui-xiang)
  + [透视和三维可视化](#tou-shi-he-san-wei-ke-shi-hua)
  + [内部和外部结构可视化](#nei-bu-he-wai-bu-jie-gou-ke-shi-hua)
* [推断背景细节](#tui-duan-bei-jing-xi-jie)

  + [前述能力的应用](#qian-shu-neng-li-de-ying-yong)
  + [组合不相关的概念](#zu-he-bu-xiang-guan-de-gai-nian)
* [动物插图](#dong-wu-cha-tu)

  + [零样本视觉推理](#ling-yang-ben-shi-jue-tui-li)
  + [地理知识](#di-li-zhi-shi)
  + [时间知识](#shi-jian-zhi-shi)
* [方法和前期工作总结](#fang-fa-he-qian-qi-gong-zuo-zong-jie)

DALL·E 是一个 120 亿参数版本的 [GPT‑3⁠（在新窗口中打开）](https://arxiv.org/abs/2005.14165)，经过训练后可以使用文本图片对数据集，根据文本描述生成图片。我们发现它具有多种功能，包括创建拟人化版本的动物和物体、以合理的方式组合不相关的概念、渲染文本以及对现有图片进行转换。

*另请参见：* [*DALL·E 2*⁠](/zh-Hans-CN/index/dall-e-2/) *能生成更逼真、更精确的图片，分辨率是原来的 4 倍。*

Text Prompt

an illustration of a baby daikon radish in a tutu walking a dog

AI Generated images

![](https://cdn.openai.com/dall-e/v2/samples/anthropomorphism/091432009673a3a126fdec860933cdce_1.png)

![](https://cdn.openai.com/dall-e/v2/samples/anthropomorphism/091432009673a3a126fdec860933cdce_2.png)

![](https://cdn.openai.com/dall-e/v2/samples/anthropomorphism/091432009673a3a126fdec860933cdce_10.png)

![](https://cdn.openai.com/dall-e/v2/samples/anthropomorphism/091432009673a3a126fdec860933cdce_26.png)

![](https://cdn.openai.com/dall-e/v2/samples/anthropomorphism/091432009673a3a126fdec860933cdce_14.png)

Edit prompt or view more images

Text Prompt

an armchair in the shape of an avocado. . . .

AI Generated images

![](https://cdn.openai.com/dall-e/v2/samples/product_design/YW4gYXJtY2hhaXIgaW4gdGhlIHNoYXBlIG9mIGFuIGF2b2NhZG8uIGFuIGFybWNoYWlyIGltaXRhdGluZyBhbiBhdm9jYWRvLg==_4.png)

![](https://cdn.openai.com/dall-e/v2/samples/product_design/YW4gYXJtY2hhaXIgaW4gdGhlIHNoYXBlIG9mIGFuIGF2b2NhZG8uIGFuIGFybWNoYWlyIGltaXRhdGluZyBhbiBhdm9jYWRvLg==_7.png)

![](https://cdn.openai.com/dall-e/v2/samples/product_design/YW4gYXJtY2hhaXIgaW4gdGhlIHNoYXBlIG9mIGFuIGF2b2NhZG8uIGFuIGFybWNoYWlyIGltaXRhdGluZyBhbiBhdm9jYWRvLg==_11.png)

![](https://cdn.openai.com/dall-e/v2/samples/product_design/YW4gYXJtY2hhaXIgaW4gdGhlIHNoYXBlIG9mIGFuIGF2b2NhZG8uIGFuIGFybWNoYWlyIGltaXRhdGluZyBhbiBhdm9jYWRvLg==_17.png)

![](https://cdn.openai.com/dall-e/v2/samples/product_design/YW4gYXJtY2hhaXIgaW4gdGhlIHNoYXBlIG9mIGFuIGF2b2NhZG8uIGFuIGFybWNoYWlyIGltaXRhdGluZyBhbiBhdm9jYWRvLg==_15.png)

Edit prompt or view more images

Text Prompt

a store front that has the word ‘openai’ written on it. . . .

AI Generated images

![](https://cdn.openai.com/dall-e/v2/samples/text_rendering/e45259de88f6361db852504739eb9255_0.png)

![](https://cdn.openai.com/dall-e/v2/samples/text_rendering/e45259de88f6361db852504739eb9255_1.png)

![](https://cdn.openai.com/dall-e/v2/samples/text_rendering/e45259de88f6361db852504739eb9255_4.png)

![](https://cdn.openai.com/dall-e/v2/samples/text_rendering/e45259de88f6361db852504739eb9255_10.png)

![](https://cdn.openai.com/dall-e/v2/samples/text_rendering/e45259de88f6361db852504739eb9255_19.png)

Edit prompt or view more images

Text Prompt

the exact same cat on the top as a sketch on the bottom

AI Generated images

![](https://cdn.openai.com/dall-e/v2/samples/im2im_animal/555bab3964e21adc8bb8807c556ede1f_2.png)

![](https://cdn.openai.com/dall-e/v2/samples/im2im_animal/555bab3964e21adc8bb8807c556ede1f_7.png)

![](https://cdn.openai.com/dall-e/v2/samples/im2im_animal/555bab3964e21adc8bb8807c556ede1f_9.png)

![](https://cdn.openai.com/dall-e/v2/samples/im2im_animal/555bab3964e21adc8bb8807c556ede1f_12.png)

![](https://cdn.openai.com/dall-e/v2/samples/im2im_animal/555bab3964e21adc8bb8807c556ede1f_13.png)

Edit prompt or view more images

GPT‑3 表明，语言可用于指导大型神经网络执行各种文本生成任务。 [Image GPT⁠](/index/image-gpt/) 显示，同样类型的神经网络也可用于生成高保真图片。我们对这些发现进行了扩展，表明通过语言操纵视觉概念已指日可待。

## 概述

与 GPT‑3 一样，DALL·E 也是一种转换语言模型。它以包含多达 1,280 个令牌的单一数据流的形式接收文本和图片，并使用最大似然法进行训练，以逐个生成所有令牌。[A](#citation-bottom-A)

通过这种训练程序，DALL·E 不仅能从头开始生成图片，还能以与文本提示一致的方式，重新生成现有图片中延伸至右下角的任何矩形区域。

我们认识到，涉及生成模型的工作有可能产生重大而广泛的社会影响。未来，我们计划分析像 DALL·E 这样的模型与社会问题的关系，如对某些工作流程和职业的经济影响、模型输出中可能出现的偏差，以及这项技术带来的长期伦理挑战。

## 功能

我们发现，DALL·E 能够为各种句子创建可信的图片，从而探索语言的组成结构。我们将在下一节中使用一系列交互式视觉效果来说明这一点。视觉效果中显示的每个标题的样本都是通过 [CLIP⁠](/index/clip/) 重新排序后，从 512 个样本中选取前 32 个样本得到的，但我们并没有使用任何人工筛选的方法，除了外部出现的缩略图和独立图片。[B](#citation-bottom-B)

### 控制属性

我们测试了 DALL·E 修改对象属性以及出现次数的能力。

Click to edit text prompt or view more AI-generated images

a pentagonal green click. a green clock in the shape of a pentagon.

![](https://cdn.openai.com/dall-e/v2/samples/shape/209f951d45fd17b3ad1134466d9946c7_26.png)

Text Prompt

AI generated images

We find that DALL·E can render familiar objects in polygonal shapes that are sometimes unlikely to occur in the real world. For some objects, such as “picture frame” and “plate,” DALL·E can reliably draw the object in any of the polygonal shapes except heptagon. For other objects, such as “manhole cover” and “stop sign,” DALL·E’s success rate for more unusual shapes, such as “pentagon,” is considerably lower.  
  
For several of the visuals in this post, we find that repeating the caption, sometimes with alternative phrasings, improves the consistency of the results.

a cube made of porcupine. a cube with the texture of a porcupine.

![](https://cdn.openai.com/dall-e/v2/samples/material/YSBjdWJlIG1hZGUgb2YgcG9yY3VwaW5lLiBhIGN1YmUgd2l0aCB0aGUgdGV4dHVyZSBvZiBhIHBvcmN1cGluZS4=_1.png)

Text Prompt

AI generated images

We find that DALL·E can map the textures of various plants, animals, and other objects onto three dimensional solids. As in the preceding visual, we find that repeating the caption with alternative phrasing improves the consistency of the results.

a collection of glasses is sitting on a table

![](https://cdn.openai.com/dall-e/v2/samples/multiple_copies/YSBjb2xsZWN0aW9uIG9mIGdsYXNzZXMgaXMgc2l0dGluZyBvbiBhIHRhYmxl_22.png)

Text Prompt

AI generated images

We find that DALL·E is able to draw multiple copies of an object when prompted to do so, but is unable to reliably count past three. When prompted to draw nouns for which there are multiple meanings, such as “glasses,” “chips,” and “cups” it sometimes draws both interpretations, depending on the plural form that is used.

### 绘制多个对象

同时控制多个对象及其属性和空间关系是一项新的挑战。例如，思考一下“一只戴着红色帽子、黄色手套、蓝色衬衫和绿色裤子的刺猬”这句话。要正确理解这句话，DALL·E 不仅要将每件衣服与动物正确地组合在一起，还要形成（帽子，红色)、（手套，黄色)、（衬衫，蓝色)和（裤子，绿色)的联想，而不能将它们混淆。[C](#citation-bottom-C)

 我们测试 DALL·E 在相对定位、堆叠物体和控制多个属性方面的能力。

a small red block sitting on a large green block

![](https://cdn.openai.com/dall-e/v2/samples/relative_positions/YSBzbWFsbCByZWQgYmxvY2sgc2l0dGluZyBvbiBhIGxhcmdlIGdyZWVuIGJsb2Nr_25.png)

Text Prompt

AI generated images

We find that DALL·E correctly responds to some types of relative positions, but not others. The choices “sitting on” and “standing in front of” sometimes appear to work, “sitting below,” “standing behind,” “standing left of,” and “standing right of” do not. DALL·E also has a lower success rate when asked to draw a large object sitting on top of a smaller one, when compared to the other way around.

a stack of 3 cubes. a red cube is on the top, sitting on a green cube. the green cube is in the middle, sitting on a blue cube. the blue cube is on the bottom.

![](https://cdn.openai.com/dall-e/v2/samples/stacking_snap/YSBzdGFjayBvZiAzIGN1YmVzLiBhIHJlZCBjdWJlIGlzIG9uIHRoZSB0b3AsIHNpdHRpbmcgb24gYSBncmVlbiBjdWJlLiB0aGUgZ3JlZW4gY3ViZSBpcyBpbiB0aGUgbWlkZGxlLCBzaXR0aW5nIG9uIGEgYmx1ZSBjdWJlLiB0aGUgYmx1ZSBjdWJlIGlzIG9uIHRoZSBib3R0b20u_28.png)

Text Prompt

AI generated images

We find that DALL·E typically generates an image with one or two of the objects having the correct colors. However, only a few samples for each setting tend to have exactly three objects colored precisely as specified.

an emoji of a baby penguin wearing a blue hat, red gloves, green shirt, and yellow pants

![](https://cdn.openai.com/dall-e/v2/samples/multiple_attributes/YW4gZW1vamkgb2YgYSBiYWJ5IHBlbmd1aW4gd2VhcmluZyBhIGJsdWUgaGF0LCByZWQgZ2xvdmVzLCBncmVlbiBzaGlydCwgYW5kIHllbGxvdyBwYW50cw==_3.png)

Text Prompt

AI generated images

We find that DALL·E typically generates an image with two or three articles of clothing having the correct colors. However, only a few of the samples for each setting tend to have all four articles of clothing with the specified colors.

虽然 DALL·E 在一定程度上可以控制少量物体的属性和位置，但成功率取决于标题的措辞。当引入的物体越多，DALL·E 就越容易混淆物体与其颜色之间的关联，成功率也会急剧下降。我们还注意到，在这些情况下，DALL·E 对标题的重新表述很不灵活：其他语义等同的标题往往不会产生正确的解释。

### 透视和三维可视化

我们发现，DALL·E 还可以控制场景的视角和场景渲染的三维样式。

an extreme close-up view of a capybara sitting in a field

![](https://cdn.openai.com/dall-e/v2/samples/camera_angles/YW4gZXh0cmVtZSBjbG9zZS11cCB2aWV3IG9mIGEgY2FweWJhcmEgc2l0dGluZyBpbiBhIGZpZWxk_3.png)

Text Prompt

AI generated images

We find that DALL·E can draw each of the animals in a variety of different views. Some of these views, such as “aerial view” and “rear view,” require knowledge of the animal’s appearance from unusual angles. Others, such as “extreme close-up view,” require knowledge of the fine-grained details of the animal’s skin or fur.

a capybara made of voxels sitting in a field

![](https://cdn.openai.com/dall-e/v2/samples/three_d_views/YSBjYXB5YmFyYSBtYWRlIG9mIHZveGVscyBzaXR0aW5nIGluIGEgZmllbGQ=_6.png)

Text Prompt

AI generated images

We find that DALL·E is often able to modify the surface of each of the animals according to the chosen 3D style, such as “claymation” and “made of voxels,” and render the scene with plausible shading depending on the location of the sun. The “x-ray” style does not always work reliably, but it shows that DALL·E can sometimes orient the bones within the animal in plausible (though not anatomically correct) configurations.

为了进一步验证这一点，我们测试了 DALL·E 从一连串间隔相等的角度重复绘制一个知名人物的头部的能力，结果发现我们可以恢复出流畅的头部旋转动画。

a photograph of a bust of homer

![](https://cdn.openai.com/dall-e/v2/samples/rotating_head/1980579866_1.png)

Text Prompt

Image Prompt

AI generated images

We prompt DALL·E with both a caption describing a well-known figure and the top region of an image showing a hat drawn at a particular angle. Then, we ask DALL·E to complete the remaining part of the image given this contextual information. We do this repeatedly, each time rotating the hat a few more degrees, and find that we are able to recover smooth animations of several well-known figures, with each frame respecting the precise specification of angle and ambient lighting.

正如我们在“鱼眼镜头视图”和“球形全景”选项中看到的那样，DALL·E 似乎能够对场景进行某些类型的光学变形。这促使我们探索它产生反射的能力。

a plain white cube looking at its own reflection in a mirror. a plain white cube gazing at itself in a mirror.

![](https://cdn.openai.com/dall-e/v2/samples/rotating_mirror/4070014681_3.png)

Text Prompt

Image Prompt

AI generated images

We prompt DALL·E with both a caption describing a well-known figure and the top region of an image showing a hat drawn at a particular angle. Then, we ask DALL·E to complete the remaining part of the image given this contextual information. We do this repeatedly, each time rotating the hat a few more degrees, and find that we are able to recover smooth animations of several well-known figures, with each frame respecting the precise specification of angle and ambient lighting.

### 内部和外部结构可视化

从“极特写视图”和“X 射线”风格的样本中，我们进一步探索了 DALL·E 通过横截面视图呈现内部结构和通过微距照片呈现外部结构的能力。

a cross-section view of a walnut

![](https://cdn.openai.com/dall-e/v2/samples/cross_sections/YSBjcm9zcy1zZWN0aW9uIHZpZXcgb2YgYSB3YWxudXQ=_0.png)

Text Prompt

AI generated images

We find that DALL·E is able to draw the interiors of several different kinds of objects.

a macro photograph of brain coral

![](https://cdn.openai.com/dall-e/v2/samples/macro_photos/YSBtYWNybyBwaG90b2dyYXBoIG9mIGJyYWluIGNvcmFs_2.png)

Text Prompt

AI generated images

We find that DALL·E is able to draw the fine-grained external details of several different kinds of objects. These details are only apparent when the object is viewed up close.

## 推断背景细节

将文本翻译成图片的任务不够明确：一个标题通常对应无数个似是而非的图片，因此图片并不是唯一确定的。例如，考虑标题“一幅日出时坐在田野上的水豚画”。根据水豚的朝向，可能需要画出一个影子，尽管这个细节从未被明确提及。我们探讨了 DALL·E 在以下三种情况下解决规格不足问题的能力：改变风格、背景和时间；在各种不同的情况下绘制同一个对象；生成一个写有特定文字的对象图片。

a painting of a capybara sitting in a field at sunrise

![](https://cdn.openai.com/dall-e/v2/samples/location_and_setting/YSBwYWludGluZyBvZiBhIGNhcHliYXJhIHNpdHRpbmcgaW4gYSBmaWVsZCBhdCBzdW5yaXNl_1.png)

Text Prompt

AI generated images

We find that DALL·E is able to render the same scene in a variety of different styles, and can adapt the lighting, shadows, and environment based on the time of day or season.

a stained glass window with an image of a blue strawberry

![](https://cdn.openai.com/dall-e/v2/samples/unusual_media/YSBzdGFpbmVkIGdsYXNzIHdpbmRvdyB3aXRoIGFuIGltYWdlIG9mIGEgYmx1ZSBzdHJhd2JlcnJ5_3.png)

Text Prompt

AI generated images

We find that DALL·E is able to flexibly adapt the representation of the object based on the medium on which it is being drawn. For “a mural,” “a soda can,” and “a teacup,” DALL·E must change how it draws the object based on the angle and curvature of the drawing surface. For “a stained glass window” and “a neon sign,” it must alter the appearance of the object from how it usually appears.

a store front that has the word ‘openai’ written on it. a store front that has the word ‘openai’ written on it. a store front that has the word ‘openai’ written on it. ‘openai’ store front.

![](https://cdn.openai.com/dall-e/v2/samples/text_rendering/e45259de88f6361db852504739eb9255_4.png)

Text Prompt

AI generated images

We find that DALL·E is able to draw the fine-grained external details of several different kinds of objects. These details are only apparent when the object is viewed up close.

凭借不同程度的可靠性，DALL·E 可以通过自然语言访问三维渲染引擎的部分功能。它可以独立控制少量物体的属性，并在一定程度上控制物体的数量和相互排列方式。它还能控制渲染场景的位置和角度，并能根据角度和照明条件的精确规格生成已知对象。

与三维渲染引擎不同的是，三维渲染引擎的输入必须明确且详细，而 DALL·E 通常能够“填补空白”，当字幕暗示图片必须包含某些未明确说明的细节时，DALL·E 就能“填补空白”。

### 前述能力的应用

接下来，我们将探讨如何在时装和室内设计中使用上述能力。

a male mannequin dressed in an orange and black flannel shirt

![](https://cdn.openai.com/dall-e/v2/samples/male_fashion_design/4209119978_14.png)

Text Prompt

Image Prompt

![](https://cdn.openai.com/dall-e/v2/image_prompts/male_fashion_design.png)

AI generated images

We explore DALL·E’s ability to render male mannequins in a variety of different outfits. When prompted with two colors, e.g., “an orange and white bomber jacket” and “an orange and black turtleneck sweater,” DALL·E often exhibits a range of possibilities for how both colors can be used for the same article of clothing.  
  
DALL·E also seems to occasionally confuse less common colors with other neighboring shades. For example, when prompted to draw clothes in “navy,” DALL·E sometimes uses lighter shades of blue, or shades very close to black. Similarly, DALL·E sometimes confuses “olive” with shades of brown or brighter shades of green.

a female mannequin dressed in a black leather jacket and gold pleated skirt

![](https://cdn.openai.com/dall-e/v2/samples/female_fashion_design/4812f86ace1b658bdaab902b7822a4fc_28.png)

Text Prompt

Image Prompt

![](https://cdn.openai.com/dall-e/v2/image_prompts/female_fashion_design.png)

AI generated images

We explore DALL·E’s ability to render female mannequins in a variety of different outfits. We find that DALL·E is able to portray unique textures such as the sheen of a “black leather jacket” and “gold” skirts and leggings. As before, we see that DALL·E occasionally confuses less common colors, such as “navy” and “olive,” with other neighboring shades.

a living room with two white armchairs and a painting of the colosseum. the painting is mounted above a modern fireplace.

![](https://cdn.openai.com/dall-e/v2/samples/living_room_design/9e80c37dfc4d27a820be73bc2e85d655_1.png)

Text Prompt

Image Prompt

![](https://cdn.openai.com/dall-e/v2/image_prompts/living_room_design.png)

AI generated images

We explore DALL·E’s ability to generate images of rooms with several details specified. We find that it can generate paintings of a wide range of different subjects, including real-world locations such as “the colosseum” and fictional characters like “yoda.” For each subject, DALL·E exhibits a variety of interpretations. While the painting is almost always present in the scene, DALL·E sometimes fails to draw the fireplace or the correct number of armchairs.

a loft bedroom with a white bed next to a nightstand. there is a fish tank beside the bed.

![](https://cdn.openai.com/dall-e/v2/samples/bedroom_design/612f04083eb75a32a167e6d26e89e650_2.png)

Text Prompt

Image Prompt

![](https://cdn.openai.com/dall-e/v2/image_prompts/bedroom_design.png)

AI generated images

We explore DALL·E’s ability to generate bedrooms with several details specified. Despite the fact that we do not tell DALL·E what should go on top of the nightstand or shelf beside the bed, we find that it sometimes decides to place the other specified object on top. As before, we see that it often fails to draw one or more of the specified objects.

### 组合不相关的概念

语言的构成特性允许我们将概念组合在一起，以描述真实和想象的事物。我们发现，DALL·E 也有能力将不同的概念组合在一起，合成出现实世界中不可能存在的物体。我们通过两个实例来探讨这种能力：将各种概念的特质转移到动物身上，以及从毫不相关的概念中汲取灵感设计产品。

a snail made of harp. a snail with the texture of a harp.

![](https://cdn.openai.com/dall-e/v2/samples/animal_concept_transfer/YSBzbmFpbCBtYWRlIG9mIGhhcnAuIGEgc25haWwgd2l0aCB0aGUgdGV4dHVyZSBvZiBhIGhhcnAu_13.png)

Text Prompt

AI generated images

We find that DALL·E can generate animals synthesized from a variety of concepts, including musical instruments, foods, and household items. While not always successful, we find that DALL·E sometimes takes the forms of the two objects into consideration when determining how to combine them. For example, when prompted to draw “a snail made of harp,” it sometimes relates the pillar of the harp to the spiral of the snail’s shell.  
  
In a previous section, we saw that as more objects are introduced into the scene, DALL·E is liable to confuse the associations between the objects and their specified attributes. Here, we see a different sort of failure mode: sometimes, rather than binding some attribute of the specified concept (say, “a faucet”) to the animal (say, “a snail”), DALL·E just draws the two as separate items.

an armchair in the shape of an avocado. an armchair imitating an avocado.

![](https://cdn.openai.com/dall-e/v2/samples/product_design/YW4gYXJtY2hhaXIgaW4gdGhlIHNoYXBlIG9mIGFuIGF2b2NhZG8uIGFuIGFybWNoYWlyIGltaXRhdGluZyBhbiBhdm9jYWRvLg==_4.png)

Text Prompt

AI generated images

In the preceding visual, we explored DALL·E’s ability to generate fantastical objects by combining two unrelated ideas. Here, we explore its ability to take inspiration from an unrelated idea while respecting the form of the thing being designed, ideally producing an object that appears to be practically functional. We found that prompting DALL·E with the phrases “in the shape of,” “in the form of,” and “in the style of” gives it the ability to do this.  
  
When generating some of these objects, such as “an armchair in the shape of an avocado”, DALL·E appears to relate the shape of a half avocado to the back of the chair, and the pit of the avocado to the cushion. We find that DALL·E is susceptible to the same kinds of mistakes mentioned in the previous visual.

## 动物插图

在上一节中，我们探讨了 DALL·E 在生成现实世界物体图片时结合不相关概念的能力。下面，我们将针对三种插图：动物和物体的拟人化版本、动物嵌合体和表情符号，在艺术的背景下探讨这种能力。

an illustration of a baby daikon radish in a tutu walking a dog

![](https://cdn.openai.com/dall-e/v2/samples/anthropomorphism/091432009673a3a126fdec860933cdce_26.png)

Text Prompt

AI generated images

We find that DALL·E is sometimes able to transfer some human activities and articles of clothing to animals and inanimate objects, such as food items. We include “pikachu” and “wielding a blue lightsaber” to explore DALL·E’s ability to incorporate popular media.  
  
We find it interesting how DALL·E adapts human body parts onto animals. For example, when asked to draw a daikon radish blowing its nose, sipping a latte, or riding a unicycle, DALL·E often draws the kerchief, hands, and feet in plausible locations.

a professional high quality illustration of a giraffe turtle chimera. a giraffe imitating a turtle. a giraffe made of turtle.

![](https://cdn.openai.com/dall-e/v2/samples/animal_chimeras/YSBwcm9mZXNzaW9uYWwgaGlnaCBxdWFsaXR5IGlsbHVzdHJhdGlvbiBvZiBhIGdpcmFmZmUgdHVydGxlIGNoaW1lcmEuIGEgZ2lyYWZmZSBpbWl0YXRpbmcgYSB0dXJ0bGUuIGEgZ2lyYWZmZSBtYWRlIG9mIHR1cnRsZS4=_0.png)

Text Prompt

AI generated images

We find that DALL·E is sometimes able to combine distinct animals in plausible ways. We include “pikachu” to explore DALL·E’s ability to incorporate knowledge of popular media, and “robot” to explore its ability to generate animal cyborgs. Generally, the features of the second animal mentioned in the caption tend to be dominant.  
  
We also find that inserting the phrase “professional high quality” before “illustration” and “emoji” sometimes improves the quality and consistency of the results.

a professional high quality emoji of a lovestruck cup of boba

![](https://cdn.openai.com/dall-e/v2/samples/emojis/YSBwcm9mZXNzaW9uYWwgaGlnaCBxdWFsaXR5IGVtb2ppIG9mIGEgbG92ZXN0cnVjayBjdXAgb2YgYm9iYQ==_8.png)

Text Prompt

AI generated images

We find that DALL·E is sometimes able to combine distinct animals in plausible ways. We include “pikachu” to explore DALL·E’s ability to incorporate knowledge of popular media, and “robot” to explore its ability to generate animal cyborgs. Generally, the features of the second animal mentioned in the caption tend to be dominant.  
  
We also find that inserting the phrase “professional high quality” before “illustration” and “emoji” sometimes improves the quality and consistency of the results.

### 零样本视觉推理

GPT‑3 可以在不进行任何额外训练的情况下，仅根据描述和提示完成多种任务，并生成提示中提供的答案。例如，当提示“下面是‘一个人在公园里遛狗’这句话的法语翻译：”时，GPT‑3 会回答“un homme qui promène son chien dans le parc”。这种能力被称为*零样本推理。* 我们发现，DALL·E 将这种能力扩展到了视觉领域，并能在正确的提示下完成多种图片到图片的翻译任务。

the exact same cat on the top as a sketch on the bottom

![](https://cdn.openai.com/dall-e/v2/samples/im2im_animal/555bab3964e21adc8bb8807c556ede1f_12.png)

Text Prompt

Image Prompt

AI generated images

We find that DALL·E is able to apply several kinds of image transformations to photos of animals, with varying degrees of reliability. The most straightforward ones, such as “photo colored pink” and “photo reflected upside-down,” also tend to be the most reliable, although the photo is often not copied or reflected exactly. The transformation “animal in extreme close-up view” requires DALL·E to recognize the breed of the animal in the photo, and render it up close with the appropriate details. This works less reliably, and for several of the photos, DALL·E only generates plausible completions in one or two instances.  
  
Other transformations, such as “animal with sunglasses” and “animal wearing a bow tie,” require placing the accessory on the correct part of the animal’s body. Those that only change the color of the animal, such as “animal colored pink,” are less reliable, but show that DALL·E is sometimes capable of segmenting the animal from the background. Finally, the transformations “a sketch of the animal” and “a cell phone case with the animal” explore the use of this capability for illustrations and product design.

the exact same teapot on the top with ’gpt’ written on it on the bottom

![](https://cdn.openai.com/dall-e/v2/samples/im2im_object/0d624be9447b6f20cec1b93674708710_1.png)

Text Prompt

Image Prompt

AI generated images

We find that DALL·E is able to apply several different kinds of image transformations to photos of teapots, with varying degrees of reliability. Aside from being able to modify the color of the teapot (e.g., “colored blue”) or its pattern (e.g., “with stripes”), DALL·E can also render text (e.g., “with ‘gpt’ written on it”) and map the letters onto the curved surface of the teapot in a plausible way. With much less reliability, it can also draw the teapot in a smaller size (for the “tiny” option) and in a broken state (for the “broken” option).

我们没有预料到这种能力会出现，也没有为鼓励这种能力而对神经网络或训练程序进行任何修改。受这些结果的启发，我们用瑞文渐进矩阵 (Raven's progressive matrices) 测试了 DALL·E 在类比推理问题上的能力，这是一种在 20 世纪被广泛使用的视觉智商测试。

a sequence of geometric shapes.

![](https://cdn.openai.com/dall-e/v2/samples/rpm/set_b_masked_3.png)

Text Prompt

Image Prompt

AI generated images

Rather than treating the IQ test a multiple-choice problem as originally intended, we ask DALL·E to complete the bottom-right corner of each image using argmax sampling, and consider its completion to be correct if it is a close visual match to the original.  
  
DALL·E is often able to solve matrices that involve continuing simple patterns or basic geometric reasoning, such as those in sets B and C. It is sometimes able to solve matrices that involve recognizing permutations and applying boolean operations, such as those in set D. The instances in set E tend to be the most difficult, and DALL·E gets almost none of them correct.  
  
For each of the sets, we measure DALL·E’s performance on both the original images, and the images with the colors inverted. The inversion of colors should pose no additional difficulty for a human, yet does generally impair DALL·E’s performance, suggesting its capabilities may be brittle in unexpected ways.

### 地理知识

我们发现，DALL·E 已经了解了地理事实、地标和街区。它对这些概念的认识在某些方面出奇地精确，而在另一些方面却有缺陷.

a photo of the food of china

![](https://cdn.openai.com/dall-e/v2/samples/countries/752777209_15.png)

Text Prompt

AI generated images

We test DALL·E’s understanding of simple geographical facts, such as country flags, cuisines, and local wildlife. While DALL·E successfully answers many of these queries, such as those involving national flags, it often reflects superficial stereotypes for choices like “food” and “wildlife,” as opposed to representing the full diversity encountered in the real world.

a photo of alamo square, san francisco, from a street at night

![](https://cdn.openai.com/dall-e/v2/samples/neighborhood/3693640717_8.png)

Text Prompt

AI generated images

We find that DALL·E is sometimes capable of rendering semblances of certain locations in San Francisco. For locations familiar to the authors, such as San Francisco, they evoke a sense of déjà vu—eerie simulacra of streets, sidewalks and cafes that remind us of very specific locations that do not exist.

a photo of san francisco’s golden gate bridge

![](https://cdn.openai.com/dall-e/v2/samples/landmarks/2116608761_11.png)

Text Prompt

Image Prompt

AI generated images

We can also prompt DALL·E to draw famous landmarks. In fact, we can even dictate when the photo was taken by specifying the first few rows of the sky. When the sky is dark, for example, DALL·E recognizes it is night, and turns on the lights in the buildings.

### 时间知识

除了探究 DALL·E 对空间概念的认识，我们还探究了它对时间概念的认识。

a photo of a phone from the 20s

![](https://cdn.openai.com/dall-e/v2/samples/timelines/1701264660_0.png)

Text Prompt

Image Prompt

AI generated images

We find that DALL·E has learned about basic stereotypical trends in design and technology over the decades. Technological artifacts appear to go through periods of explosion of change, dramatically shifting for a decade or two, then changing more incrementally, becoming refined and streamlined.

## 方法和前期工作总结

DALL·E 是一种简单的解码器转换器，它以 1,280 个令牌（文本为 256 个，图片为 1,024 个)的单一流接收文本和图片，并对所有令牌进行自回归建模。64 个自我注意层中每个层的注意掩码允许每个图片令牌注意所有文本令牌。DALL·E 对文本令牌使用标准因果掩码，对图片令牌使用稀疏注意，并根据层的不同采用行、列或卷积注意模式。我们将在[论文⁠（在新窗口中打开）](https://arxiv.org/abs/2102.12092)中提供有关架构和训练过程的更多细节。

自瑞德 (Reed) 等人的开创性工作以来，文本到图片的合成一直是一个活跃的研究领域。[1](#citation-bottom-1)该方法使用的是以文本嵌入为条件的 GAN。嵌入是由使用对比损失 (Contrastive Loss) 预训练的编码器生成的，这与 CLIP 并无不同。StackGAN[3](#citation-bottom-3) 和 StackGAN++[4](#citation-bottom-4) 使用多尺度 GAN 来扩大图片分辨率，提高视觉保真度。AttnGAN[5](#citation-bottom-5) 在文本和图片特征之间加入了注意力，并提出了一个对比性文本图片特征匹配损失作为辅助目标。这与我们使用 CLIP 进行的重新排序（离线完成)进行了有趣的比较。其他工作[2](#citation-bottom-2)、[6](#citation-bottom-6)、[7](#citation-bottom-7)在训练过程中加入了额外的监督来源，以提高图片质量。最后，阮 (Nguyen) 等人[8](#citation-bottom-8) 和赵 (Cho) 等人[9](#citation-bottom-9) 利用预先训练的多模态判别模型，探索了基于采样的图像生成策略。

与 [VQVAE-2⁠（在新窗口中打开）](https://arxiv.org/abs/1906.00446) 中使用的剔除抽样类似，我们使用 [CLIP⁠](/index/clip/) 对所有交互式视觉效果中每个标题的 512 个样本中的前 32 个样本进行重新排序。这一过程也可被视为一种语言引导搜索[16](#citation-bottom-16)，可对样本质量产生巨大影响。

an illustration of a baby daikon radish in a tutu walking a dog [caption 1, best 8 of 2048]

![](https://cdn.openai.com/dall-e/v2/samples/clip/0_top_8_of_2048_rank_5.png)

Text Prompt

AI generated images

Reranking the samples from DALL·E using CLIP can dramatically improve consistency and quality of the samples.

* [DALL·E](/zh-Hans-CN/research/index/?tags=dall-e)
* [生成式模型](/zh-Hans-CN/research/index/?tags=generative-models)
* [语言](/zh-Hans-CN/research/index/?tags=language)
* [Transformer](/zh-Hans-CN/research/index/?tags=transformers)

## 脚注

1. A

   令牌是指离散词汇中的任何符号；对于人类来说，每个英文字母都是 26 个字母表中的一个令牌。DALL·E 的词汇中包含文本和图片概念的令牌。具体来说，每个图片标题最多使用 256 个 BPE 编码的令牌来表示，词汇量为 16,384 个；图片使用 1,024 个令牌来表示，词汇量为 8,192 个。

在训练过程中，图片被预处理为 256x256 分辨率。与 VQVAE 类似，我们使用离散 VAE 将每幅图片压缩为 32x32 格的离散潜码，并使用连续松弛对其进行预训练。我们发现，使用松弛训练无需明确的编码本、EMA 损失或死码恢复等技巧，而且可以扩展到大词汇量。

1. B

   更多细节将在[后续章节⁠](/zh-Hans-CN/index/dall-e/#summary)提供。
2. 17

   这项任务被称为变量绑定，已有大量文献对此进行了研究。

## 参考文献

1. 1

   Reed, S., Akata, Z., Yan, X., Logeswaran, L., Schiele, B., Lee, H.（2016 年）。“[生成对抗式文本到图片合成⁠（在新窗口中打开）](https://arxiv.org/abs/1605.05396)”⁠。ICML 2016 会议论文。
2. 2

   Reed, S., Akata, Z., Mohan, S., Tenka, S., Schiele, B., Lee, H.（2016 年）。“[学习绘制内容与位置⁠（在新窗口中打开）](https://arxiv.org/abs/1610.02454)”。NIPS 2016 会议论文。
3. 3

   Zhang, H., Xu, T., Li, H., Zhang, S., Wang, X., Huang X., Metaxas, D.（2016 年）。“[StackGAN：通过堆叠生成对抗式网络实现文本到照片级图片合成⁠（在新窗口中打开）](https://arxiv.org/abs/1612.03242)”⁠。ICCV 2017 会议论文。
4. 4

   Zhang, H., Xu, T., Li, H., Zhang, S., Wang, X., Huang, X., Metaxas, D.（2017 年）。“[StackGAN++：通过堆叠生成对抗式网络实现真实图片合成⁠（在新窗口中打开）](https://arxiv.org/abs/1710.10916)”⁠。IEEE TPAMI 2018 期刊论文。
5. 5

   Xu, T., Zhang, P., Huang, Q., Zhang, H., Gan, Z., Huang, X., He, X.（2017 年）。“[AttnGAN：基于注意力生成对抗式网络的精细文本到图像生成⁠（在新窗口中打开）](https://arxiv.org/abs/1711.10485)”⁠。
6. 6

   Li, W., Zhang, P., Zhang, L., Huang, Q., He, X., Lyu, S., Gao, J.（2019 年）。“[通过对抗训练实现对象驱动的文本到图片合成⁠（在新窗口中打开）](https://arxiv.org/abs/1902.10740)”⁠。CVPR 2019 会议论文。
7. 7

   Koh, J. Y., Baldridge, J., Lee, H., Yang, Y.（2020 年）。“[基于精细用户注意力的文本到图像生成⁠（在新窗口中打开）](https://arxiv.org/abs/2011.03775)”⁠。WACV 2021会议论文。
8. 8

   Nguyen, A., Clune, J., Bengio, Y., Dosovitskiy, A., Yosinski, J.（2016 年）。“[即插即用生成网络：潜空间中的条件迭代图像生成⁠（在新窗口中打开）](https://arxiv.org/abs/1612.00005)”⁠。
9. 9

   Cho, J., Lu, J., Schwen, D., Hajishirzi, H., Kembhavi, A.（2020 年）。“[X-LXMERT：用多模态 Transformer 进行绘画、描述和问答⁠（在新窗口中打开）](https://arxiv.org/abs/2009.11278)”⁠。EMNLP 2020 会议论文。
10. 10

    Kingma、Diederik P. 和 Max Welling。“[自动编码变分贝叶斯⁠（在新窗口中打开）](https://arxiv.org/abs/1312.6114)”⁠。arXiv 预印本（2013 年）。
11. 11

    Rezende、Danilo Jimenez、Shakir Mohamed 和 Daan Wierstra。“[深度生成模型中的随机反向传播与近似推理⁠（在新窗口中打开）](https://arxiv.org/abs/1401.4082)”。arXiv 预印本（2014 年）。
12. 12

    Jang, E., Gu, S., Poole, B.（2016 年）。“[使用 Gumbel-softmax 进行类别重新参数化⁠（在新窗口中打开）](https://arxiv.org/abs/1611.01144)”⁠。
13. 13

    Maddison, C., Mnih, A., Teh, Y. W.（2016 年）。“[Concrete 分布：离散随机变量的连续松弛⁠（在新窗口中打开）](https://arxiv.org/abs/1611.00712)”⁠。
14. 14

    van den Oord, A., Vinyals, O., Kavukcuoglu, K.（2017 年）。“[神经离散表示学习⁠（在新窗口中打开）](https://arxiv.org/abs/1711.00937)”⁠。
15. 15

    Razavi, A., van der Oord, A., Vinyals, O.（2019 年）。“[使用VQ-VAE-2生成多样化高保真图片⁠（在新窗口中打开）](https://arxiv.org/abs/1906.00446)”⁠。
16. 16

    Andreas, J., Klein, D., Levine, S.（2017 年）。“[潜在语言学习⁠（在新窗口中打开）](https://arxiv.org/abs/1711.00482)”⁠。
17. 17

    Smolensky, P.（1990 年）。“[张量积变量绑定与联结主义系统中的符号结构表示⁠（在新窗口中打开）](http://www.lscp.net/persons/dupoux/teaching/AT1_2014/papers/Smolensky_1990_TensorProductVariableBinding.AI.pdf)”⁠。
18. 18

    Plate, T.（1995 年）。“[全息缩减表示：组合分布式表示的卷积代数⁠（在新窗口中打开）](https://www.ijcai.org/Proceedings/91-1/Papers/006.pdf)”⁠。
19. 19

    Gayler, R.（1998 年）。“[乘法绑定、表示运算符与类比⁠（在新窗口中打开）](http://cogprints.org/502/)”⁠。
20. 20

    Kanerva, P.（1997 年）。“[完全分布式表示⁠（在新窗口中打开）](http://www.cap-lore.com/RWC97-kanerva.pdf)”⁠。

## 主要作者

Aditya Ramesh、Mikhail Pavlov、Gabriel Goh、Scott Gray

## 协作作者

Mark Chen、Rewon Child、Vedant Misra、Pamela Mishkin、Gretchen Krueger、Sandhini Agarwal、Ilya Sutskever

## 相关文章

[查看全部](/zh-Hans-CN/news/)

![Whisper](https://images.ctfassets.net/kftzwdyauwt9/13c810cb-0592-442d-190ab7378bef/a7cb2299d034abe93023f662f8d32263/Speech_Rec_16_9.png?w=3840&q=90&fm=webp)

[Whisper 简介

发布2022年9月21日](/zh-Hans-CN/index/whisper/)

![An aerial view of a crowd of people facing away, wearing hats and bearing flags](https://images.ctfassets.net/kftzwdyauwt9/d22f177f-5116-4b3b-5ddcdbe54569/b657a1299069351973db72804b5811d1/image_131.png?w=3840&q=90&fm=webp)

[DALL·E 2 pre-training mitigations

刊发2022年6月28日](/index/dall-e-2-pre-training-mitigations/)

![Hierarchical Text Conditional Image Generation With Clip Latents](https://images.ctfassets.net/kftzwdyauwt9/7c44eedc-3563-4438-c613706c52b1/fcfc38b26fd4878a3c6b4ca8d1d73b17/hierarchical-text-conditional-image-generation-with-clip-latents.jpg?w=3840&q=90&fm=webp)

[Hierarchical text-conditional image generation with CLIP latents

刊发2022年4月13日](/index/hierarchical-text-conditional-image-generation-with-clip-latents/)

研究

* [研究索引](/zh-Hans-CN/research/index/)
* [研究概览](/zh-Hans-CN/research/)
* [经济研究](/zh-Hans-CN/signals/)

最新进展

* [GPT-5.5](/zh-Hans-CN/index/introducing-gpt-5-5/)
* [GPT-5.4](/zh-Hans-CN/index/introducing-gpt-5-4/)
* [GPT-5.3 Instant](/zh-Hans-CN/index/gpt-5-3-instant/)

安全

* [安全措施](/zh-Hans-CN/safety/)
* [部署安全（在新窗口中打开）](https://deploymentsafety.openai.com/)
* [安全与隐私](/zh-Hans-CN/security-and-privacy/)
* [信任与透明度](/zh-Hans-CN/trust-and-transparency/)

ChatGPT

* [ChatGPT（在新窗口中打开）](https://chatgpt.com/?openaicom-did=7a7e97a7-5b44-4eea-b313-b1f324ad16ea&openaicom_referred=true)
* [ChatGPT Business（在新窗口中打开）](https://chatgpt.com/business/?openaicom-did=7a7e97a7-5b44-4eea-b313-b1f324ad16ea&openaicom_referred=true)
* [ChatGPT Enterprise（在新窗口中打开）](https://chatgpt.com/zh-Hans-CN/business/enterprise/?openaicom-did=7a7e97a7-5b44-4eea-b313-b1f324ad16ea&openaicom_referred=true)
* [ChatGPT for Education（在新窗口中打开）](https://chatgpt.com/zh-Hans-CN/business/education/?openaicom-did=7a7e97a7-5b44-4eea-b313-b1f324ad16ea&openaicom_referred=true)
* [Codex](/zh-Hans-CN/codex/)
* [发布说明](/products/release-notes/)

API 平台

* [平台概览](/zh-Hans-CN/api/)
* [API 登录（在新窗口中打开）](https://platform.openai.com/login)
* [文档（在新窗口中打开）](https://developers.openai.com/api/docs)

Business

* [概览](/zh-Hans-CN/business/)
* [解决方案](/zh-Hans-CN/solutions/)
* [资源](/zh-Hans-CN/business/learn/)
* [联系销售团队](/zh-Hans-CN/contact-sales/)

开发者

* [Apps SDK（在新窗口中打开）](https://developers.openai.com/apps-sdk)
* [开放模型](/zh-Hans-CN/open-models/)
* [文档（在新窗口中打开）](https://developers.openai.com/)
* [资源（在新窗口中打开）](https://developers.openai.com/learn)
* [开发者论坛（在新窗口中打开）](https://community.openai.com/)

公司

* [关于我们](/zh-Hans-CN/about/)
* [我们的宪章](/charter/)
* [工作机会](/careers/)
* [新闻](/zh-Hans-CN/news/)

支持

* [帮助中心（在新窗口中打开）](https://help.openai.com/)

更多

* [客户案例](/zh-Hans-CN/stories/)
* [Academy](/academy/)
* [直播](/zh-Hans-CN/live/)
* [播客](/zh-Hans-CN/podcast/)
* [RSS](/news/rss.xml)

条款与政策

* [使用条款](/zh-Hans-CN/policies/terms-of-use/)
* [隐私政策](/zh-Hans-CN/policies/privacy-policy/)
* [其他政策](/zh-Hans-CN/policies/)

[（在新窗口中打开）](https://x.com/OpenAI)[（在新窗口中打开）](https://www.youtube.com/OpenAI)[（在新窗口中打开）](https://www.linkedin.com/company/openai)[（在新窗口中打开）](https://github.com/openai)[（在新窗口中打开）](https://www.instagram.com/openai/)[（在新窗口中打开）](https://www.tiktok.com/@openai)[（在新窗口中打开）](https://discord.gg/openai)

OpenAI © 2015–2026你的隐私选择

中文中国

![](https://bat.bing.com/action/0?ti=187204252&Ver=2&mid=df914072-a2d4-4e00-8f8c-ab733a9a4615&bo=1&sid=6ddec400702911f1912259ef95f34e78&vid=6ddec220702911f18ddbc573032dfa78&vids=1&msclkid=N&pi=918639831&lg=zh-CN&sw=1440&sh=900&sc=24&tl=DALL%C2%B7E%EF%BC%9A%E4%BB%8E%E6%96%87%E6%9C%AC%E5%88%9B%E5%BB%BA%E5%9B%BE%E7%89%87%20%7C%20OpenAI&p=https%3A%2F%2Fopenai.com%2Fzh-Hans-CN%2Findex%2Fdall-e%2F&r=&lt=3541&evt=pageLoad&sv=2&cdb=AQAA&rn=833006)
