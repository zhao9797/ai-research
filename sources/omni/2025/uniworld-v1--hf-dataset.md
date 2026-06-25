---
license: mit
---

<p style="color:red; font-size:25px">
The Geneval-style dataset is sourced from <a href="https://huggingface.co/datasets/BLIP3o/BLIP3o-60k" style="color:red">BLIP3o-60k</a>.
</p>


This dataset is presented in the paper: [UniWorld: High-Resolution Semantic Encoders for Unified Visual Understanding and Generation](https://huggingface.co/papers/2506.03147)

More details can be found in [UniWorld-V1](https://github.com/PKU-YuanGroup/UniWorld-V1)


### Data preparation

Download the data from [LanguageBind/UniWorld-V1](https://huggingface.co/datasets/LanguageBind/UniWorld-V1). The dataset consists of two parts: source images and annotation JSON files.

Prepare a `data.txt` file in the following format:

1. The first column is the root path to the image.

2. The second column is the corresponding annotation JSON file.

3. The third column indicates whether to enable the region-weighting strategy. We recommend setting it to True for edited data and False for others.

```
data/BLIP3o-60k,json/blip3o_t2i_58859.json,false
data/coco2017_caption_canny-236k,coco2017_canny_236574.json,false
data/imgedit,json/imgedit/laion_add_part0_edit.json,true
```
We have prepared a `data.txt` file about ImgEdit for your reference.

```
data/imgedit/action/action,json/imgedit/pandam_action_edit.json,true
data/imgedit/action/action_part2,json/imgedit/pandam2_action_edit.json,true
data/imgedit/action/action_part3,json/imgedit/pandam3_action_edit.json,true
data/imgedit/action/action_part4,json/imgedit/pandam4_action_edit.json,true
data/imgedit/add/add_part0,json/imgedit/laion_add_part0_edit.json,true
data/imgedit/add/add_part1,json/imgedit/laion_add_part1_edit.json,true
data/imgedit/add/add_part4,json/imgedit/results_add_laion_part4_edit.json,true
data/imgedit/add/add_part5,json/imgedit/results_add_laion_part5_edit.json,true
data/imgedit/adjust/adjust_part0,json/imgedit/results_adjust_canny_laion_part0_edit.json,true
data/imgedit/adjust/adjust_part2,json/imgedit/results_adjust_canny_laion_part2_edit.json,true
data/imgedit/adjust/adjust_part3,json/imgedit/results_adjust_canny_laion_part3_edit.json,true
data/imgedit/adjust/adjust_part4,json/imgedit/laion_adjust_canny_part4_edit.json,true
data/imgedit/background/background_part0,json/imgedit/results_background_laion_part0_edit.json,true
data/imgedit/background/background_part2,json/imgedit/results_background_laion_part2_edit.json,true
data/imgedit/background/background_part3,json/imgedit/laion_background_part3_edit.json,true
data/imgedit/background/background_part5,json/imgedit/laion_background_part5_edit.json,true
data/imgedit/background/background_part7,json/imgedit/laion_background_part7_edit.json,true
data/imgedit/compose/compose_part0,json/imgedit/results_compose_part0_edit.json,false
data/imgedit/compose/compose_part2,json/imgedit/results_compose_part2_edit.json,false
data/imgedit/compose/compose_part6,json/imgedit/results_compose_part6_fix_edit.json,false
data/imgedit/refine_replace/refine_replace_part1,json/imgedit/results_extract_ref_part1_refimg_edit.json,true
data/imgedit/remove/remove_part0,json/imgedit/laion_remove_part0_edit.json,true
data/imgedit/remove/remove_part1,json/imgedit/results_remove_laion_part1_edit.json,true
data/imgedit/remove/remove_part4,json/imgedit/results_remove_laion_part4_edit.json,true
data/imgedit/remove/remove_part5,json/imgedit/results_remove_laion_part5_edit.json,true
data/imgedit/replace/replace_part0,json/imgedit/laion_replace_part0_edit.json,true
data/imgedit/replace/replace_part1,json/imgedit/laion_replace_part1_edit.json,true
data/imgedit/replace/replace_part4,json/imgedit/results_replace_laion_part4_edit.json,true
data/imgedit/replace/replace_part5,json/imgedit/results_replace_laion_part5_edit.json,true
data/imgedit/transfer/transfer,json/imgedit/results_style_transfer_edit.json,false
data/imgedit/transfer/transfer_part0,json/imgedit/results_style_transfer_part0_cap36472_edit.json,false
```


### Data details

Text-to-Image Generation
    
- [BLIP3o-60k](https://huggingface.co/datasets/BLIP3o/BLIP3o-60k): We add text-to-image instructions to half of the data. [108 GB storage usage.]
- [OSP1024-286k](https://huggingface.co/datasets/LanguageBind/UniWorld-V1/tree/main/data/OSP1024-286k): Sourced from internal data of the [Open-Sora Plan](https://github.com/PKU-YuanGroup/Open-Sora-Plan), with captions generated using [Qwen2-VL-72B](https://huggingface.co/Qwen/Qwen2-VL-72B-Instruct). Images have an aspect ratio between 3:4 and 4:3, aesthetic score ≥ 6, and a short side ≥ 1024 pixels. [326 GB storage usage.]

Image Editing
    
- [imgedit-724k](https://huggingface.co/datasets/sysuyy/ImgEdit/tree/main): Data is filtered using GPT-4o, retaining approximately half. [2.8T storage usage.]
- [OmniEdit-368k](https://huggingface.co/datasets/TIGER-Lab/OmniEdit-Filtered-1.2M): For image editing data, samples with edited regions smaller than 1/100 were filtered out; images have a short side ≥ 1024 pixels. [204 GB storage usage.]
- [SEED-Data-Edit-Part1-Openimages-65k](https://huggingface.co/datasets/AILab-CVC/SEED-Data-Edit-Part1-Openimages): For image editing data, samples with edited regions smaller than 1/100 were filtered out. Images have a short side ≥ 1024 pixels. [10 GB storage usage.]
- [SEED-Data-Edit-Part2-3-12k](https://huggingface.co/datasets/AILab-CVC/SEED-Data-Edit-Part2-3): For image editing data, samples with edited regions smaller than 1/100 were filtered out. Images have a short side ≥ 1024 pixels. [10 GB storage usage.]
- [PromptfixData-18k](https://huggingface.co/datasets/yeates/PromptfixData): For image restoration data and some editing data, samples with edited regions smaller than 1/100 were filtered out. Images have a short side ≥ 1024 pixels. [9 GB storage usage.]
- [StyleBooth-11k](https://huggingface.co/scepter-studio/stylebooth): For transfer style data, images have a short side ≥ 1024 pixels. [4 GB storage usage.]
- [Ghibli-36k](https://huggingface.co/datasets/LanguageBind/UniWorld-V1/tree/main/data/Ghibli-36k): For transfer style data, images have a short side ≥ 1024 pixels. **Warning: This data has not been quality filtered.** [170 GB storage usage.]


Extract & Try-on
    
- [viton_hd-23k](https://huggingface.co/datasets/forgeml/viton_hd): Converted from the source data into an instruction dataset for product extraction. [1 GB storage usage.]
- [deepfashion-27k](https://huggingface.co/datasets/lirus18/deepfashion): Converted from the source data into an instruction dataset for product extraction. [1 GB storage usage.]
- [shop_product-23k](https://huggingface.co/datasets/LanguageBind/UniWorld-V1/tree/main/data/shop_product-23k): Sourced from internal data of the [Open-Sora Plan](https://github.com/PKU-YuanGroup/Open-Sora-Plan), focusing on product extraction and virtual try-on, with images having a short side ≥ 1024 pixels. [12 GB storage usage.]


Image Perception
    
- [coco2017_caption_canny-236k](https://huggingface.co/datasets/gebinhui/coco2017_caption_canny): img->canny & canny->img [25 GB storage usage.]
- [coco2017_caption_depth-236k](https://huggingface.co/datasets/gebinhui/coco2017_caption_depth): img->depth & depth->img [8 GB storage usage.]
- [coco2017_caption_hed-236k](https://huggingface.co/datasets/gebinhui/coco2017_caption_hed): img->hed & hed->img [13 GB storage usage.]
- [coco2017_caption_mlsd-236k](https://huggingface.co/datasets/gebinhui/coco2017_caption_mlsd): img->mlsd & mlsd->img [ GB storage usage.]
- [coco2017_caption_normal-236k](https://huggingface.co/datasets/gebinhui/coco2017_caption_normal): img->normal & normal->img [10 GB storage usage.]
- [coco2017_caption_openpose-62k](https://huggingface.co/datasets/wangherr/coco2017_caption_openpose): img->pose & pose->img [2 GB storage usage.]
- [coco2017_caption_sketch-236k](https://huggingface.co/datasets/wangherr/coco2017_caption_sketch): img->sketch & sketch->img [15 GB storage usage.]
- [unsplash_canny-20k](https://huggingface.co/datasets/wtcherr/unsplash_10k_canny): img->canny & canny->img [2 GB storage usage.]
- [open_pose-40k](https://huggingface.co/datasets/raulc0399/open_pose_controlnet): img->pose & pose->img [4 GB storage usage.]
- [mscoco-controlnet-canny-less-colors-236k](https://huggingface.co/datasets/hazal-karakus/mscoco-controlnet-canny-less-colors): img->canny & canny->img [13 GB storage usage.]
- [coco2017_seg_box-448k](https://huggingface.co/datasets/LanguageBind/UniWorld-V1/tree/main/data/coco2017_seg_box-448k): img->detection & img->segmentation (mask), instances with regions smaller than 1/100 were filtered out. We visualise masks on the original image as gt-image. [39 GB storage usage.]
- [viton_hd-11k](https://huggingface.co/datasets/forgeml/viton_hd): img->pose [1 GB storage usage.]
- [deepfashion-13k](https://huggingface.co/datasets/lirus18/deepfashion): img->pose [1 GB storage usage.]

