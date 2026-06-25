# Emu Edit
Source: https://emu-edit.metademolab.com/
Emu Edit


* [Emu Edit](./index.html)
* [Paper](https://emu-edit.metademolab.com/assets/emu_edit.pdf)
* [Benchmark](https://huggingface.co/datasets/facebook/emu_edit_test_set)
* [Blogpost](https://ai.meta.com/blog/emu-text-to-video-generation-image-editing-research/)
* [Emu Video](https://emu-video.metademolab.com/)

[Emu Edit](https://emu-edit.metademolab.com/)

Research by AI at Meta

* [Emu Edit](./index.html)
* [Paper](https://emu-edit.metademolab.com/assets/emu_edit.pdf)
* [Benchmark](https://huggingface.co/datasets/facebook/emu_edit_test_set)
* [Blogpost](https://ai.meta.com/blog/emu-text-to-video-generation-image-editing-research/)
* [Emu Video](https://emu-video.metademolab.com/)

## Emu Edit: Precise Image Editing via Recognition and Generation Tasks

###### We present Emu Edit, a multi-task image editing model which sets a new state-of-the-art in instruction-based image editing. To develop Emu Edit we adapt its architecture for multi-task learning and train it an unprecedented range of tasks, such as region-based editing, free-form editing, and computer vision tasks such as detection and segmentation - all formulated as generative tasks.

[Get Started](#emu-edit-in-action)

[Read the Paper](https://emu-edit.metademolab.com/assets/emu_edit.pdf)

## Emu Edit in Action

[![Sorry, your browser doesn't support embedded videos.](assets/images/juice.webp)](/assets/videos/juice.mp4)

[![Sorry, your browser doesn't support embedded videos.](assets/images/deer.webp)](/assets/videos/deer.mp4)

[![Sorry, your browser doesn't support embedded videos.](assets/images/avocado.webp)](/assets/videos/avocado.mp4)

[![Sorry, your browser doesn't support embedded videos.](assets/images/car.webp)](/assets/videos/car.mp4)

[![Sorry, your browser doesn't support embedded videos.](assets/images/cute.webp)](/assets/videos/cute.mp4)

[![Sorry, your browser doesn't support embedded videos.](assets/images/birthday.webp)](/assets/videos/birthday.mp4)

[![Sorry, your browser doesn't support embedded videos.](assets/images/hands.webp)](/assets/videos/hands.mp4)

[![Sorry, your browser doesn't support embedded videos.](assets/images/woman2.webp)](/assets/videos/woman2.mp4)

[![Sorry, your browser doesn't support embedded videos.](assets/images/robot.webp)](/assets/videos/robot.mp4)

[![Sorry, your browser doesn't support embedded videos.](assets/images/romantic.webp)](/assets/videos/romantic.mp4)

[![Sorry, your browser doesn't support embedded videos.](assets/images/emu.webp)](/assets/videos/emu.mp4)

[![Sorry, your browser doesn't support embedded videos.](assets/images/view.webp)](/assets/videos/view.mp4)

[![Sorry, your browser doesn't support embedded videos.](assets/images/cat.webp)](/assets/videos/cat.mp4)

[![Sorry, your browser doesn't support embedded videos.](assets/images/banana.webp)](/assets/videos/banana.mp4)

[![Sorry, your browser doesn't support embedded videos.](assets/images/scary.webp)](/assets/videos/scary.mp4)

[![Sorry, your browser doesn't support embedded videos.](assets/images/dog.webp)](/assets/videos/dog.mp4)

[![Sorry, your browser doesn't support embedded videos.](assets/images/anth.webp)](/assets/videos/anth.mp4)

[![Sorry, your browser doesn't support embedded videos.](assets/images/ana_cat.webp)](/assets/videos/ana_cat.mp4)

## Approach

###### In order to create a robust and accurate image editing model we train Emu Edit to multi-task across a wide range of image editing tasks. These tasks span region-based editing tasks, free-form editing tasks, computer vision tasks, and more, all formulated as generative tasks. Additionally, to process this wide array of tasks effectively, we introduce the concept of learned task embeddings, which are used to steer the generation process toward the correct generative task. We demonstrate that both multi-task training, and utilizing learned task embeddings significantly enhance the ability of our model to accurately execute the editing instruction.

![The data distribution of our multi-task training dataset.](/assets/images/data_dist.webp)

The data distribution of our multi-task training dataset.

## Few-Shot Learning

Equipped with a robust model trained across a broad spectrum of tasks and guided by learned task embeddings, we explore few-shot adaptation to unseen tasks via task inversion. In this process, we keep the model weights frozen, and solely update a task embedding to fit the new task. Our experiments demonstrate that Emu Edit can swiftly adapt to new tasks, such as super-resolution, contour detection, and others. This makes task inversion with Emu Edit particularly advantageous in scenarios where labeled examples are limited, or when the compute budget is low.

**Instruction: Mark the drinks**

![Input Image](/assets/images/contours_input.webp)

Input Image

![Output Image](/assets/images/contours_output.webp)

Output Image

**Instruction: Upsample the resolution**

![Input Image](/assets/images/sr_input.webp)

Input Image

![Output Image](/assets/images/sr_output.webp)

Output Image

## Benchmark

To support rigorous and informed evaluation of instruction-based image editing models we collect and publicly release a new benchmark that includes seven different image editing tasks: background alteration (background), comprehensive image changes (global), style alteration (style), object removal (remove), object addition (add), localized modifications (local), and color/texture alterations (texture) Additionally, to allow proper comparison against Emu Edit, we release Emu Edit’s generations on the dataset.

[Download the Benchmark](https://huggingface.co/datasets/facebook/emu_edit_test_set)

[Download Emu Edit's generations](https://huggingface.co/datasets/facebook/emu_edit_test_set_generations)

## Authors

Shelly Sheynin\*

Adam Polyak\*

Uriel Singer\*

Yuval Kirstain\*

Amit Zohar\*

Oron Ashual

Devi Parikh

Yaniv Taigman

(\*): equal contribution

## Acknowledgements

We extend our gratitude to the following people for their contributions (alphabetical order): Andrew Brown, Ankit Ramchandani, Guan Pang, Ishan Misra, Mannat Singh, Ning Zhang, Parveen Krishnan, Peizhao Zhang, Peter Vajda, Rohit Girdhar, Roshan Sumbaly, Tong Xiao, Vladan Petrovic, Xide Xia.

## Citation

```
@inproceedings{Sheynin2023EmuEP,
  title={Emu Edit: Precise Image Editing via Recognition and Generation Tasks},
  author={Shelly Sheynin and Adam Polyak and Uriel Singer and Yuval Kirstain and Amit Zohar and Oron Ashual and Devi Parikh and Yaniv Taigman},
  year={2023},
  url={https://api.semanticscholar.org/CorpusID:265221391}
}
```

©2023 Meta
