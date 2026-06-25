# CLIP Guided Diffusion HQ 512x512 Uncond.ipynb - Colab
Source: https://colab.research.google.com/drive/1QBsaDAZv8np29FPbvjffbE1eytoJcsgA
CLIP Guided Diffusion HQ 512x512 Uncond.ipynb - Colab

close

close

info

此笔记本是通过不公开输出项打开的。系统将不会保存输出项。您可以在[笔记本设置](#)
中停用此设置。

close

 

info

您的 Colab 版本过旧，请刷新以获取最新更新。

刷新以更新



CLIP Guided Diffusion HQ 512x512 Uncond.ipynb\_

文件

修改

视图

插入

代码执行程序

工具

帮助

settings


people
分享


spark
Gemini


[登录](https://accounts.google.com/ServiceLogin?passive=true&continue=https%3A%2F%2Fcolab.research.google.com%2Fdrive%2F1QBsaDAZv8np29FPbvjffbE1eytoJcsgA&ec=GAZAqQM)

 

命令

代码

文本




 

复制到云端硬盘


 








 
people


settings


expand\_less
expand\_more

format\_list\_bulleted

find\_in\_page

code

eye\_tracking

vpn\_key

folder

table

笔记本

more\_vert


close

---

spark
Gemini

keyboard\_arrow\_down

# Generates images from text prompts with CLIP guided diffusion.

By Katherine Crowson (<https://github.com/crowsonkb>, [https://twitter.com/RiversHaveWings](https://www.google.com/url?q=https%3A%2F%2Ftwitter.com%2FRiversHaveWings)). It uses a 512x512 unconditional ImageNet diffusion model fine-tuned from OpenAI's 512x512 class-conditional ImageNet diffusion model (<https://github.com/openai/guided-diffusion>) together with CLIP (<https://github.com/openai/CLIP>) to connect text prompts with images.

subdirectory\_arrow\_right
已隐藏 13 个单元格

---

spark
Gemini

keyboard\_arrow\_down

### Licensed under the MIT License

```
```
# @title Licensed under the MIT License  
  
# Copyright (c) 2021 Katherine Crowson  
  
# Permission is hereby granted, free of charge, to any person obtaining a copy  
# of this software and associated documentation files (the "Software"), to deal  
# in the Software without restriction, including without limitation the rights  
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell  
# copies of the Software, and to permit persons to whom the Software is  
# furnished to do so, subject to the following conditions:  
  
# The above copyright notice and this permission notice shall be included in  
# all copies or substantial portions of the Software.  
  
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,  
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER  
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN  
# THE SOFTWARE.
```
```

显示代码

---

spark
Gemini

Note: This notebook requires 16 GB of GPU memory to work, if you are unable to get a 16 GB GPU consistently, try the [256x256 version](https://colab.research.google.com/drive/12a_Wrfi2_gwwAuN3VvMTwVMz9TfqctNj).

subdirectory\_arrow\_right
已隐藏 0 个单元格

---

spark
Gemini

# Check the GPU

!nvidia-smi

---

spark
Gemini

# Install dependencies

!git clone https://github.com/openai/CLIP

!git clone https://github.com/crowsonkb/guided-diffusion

!pip install -e ./CLIP

!pip install -e ./guided-diffusion

!pip install lpips

---

spark
Gemini

```
```
# Download the diffusion model  
  
!curl -OL --http1.1 'https://the-eye.eu/public/AI/models/512x512_diffusion_unconditional_ImageNet/512x512_diffusion_uncond_finetune_008100.pt'
```
```

---

spark
Gemini

```
```
# Imports  
  
import gc  
import io  
import math  
import sys  
  
from IPython import display  
import lpips  
from PIL import Image  
import requests  
import torch  
from torch import nn  
from torch.nn import functional as F  
from torchvision import transforms  
from torchvision.transforms import functional as TF  
from tqdm.notebook import tqdm  
  
sys.path.append('./CLIP')  
sys.path.append('./guided-diffusion')  
  
import clip  
from guided_diffusion.script_util import create_model_and_diffusion, model_and_diffusion_defaults
```
```

---

spark
Gemini

```
```
# Define necessary functions  
  
def fetch(url_or_path):  
    if str(url_or_path).startswith('http://') or str(url_or_path).startswith('https://'):  
        r = requests.get(url_or_path)  
        r.raise_for_status()  
        fd = io.BytesIO()  
        fd.write(r.content)  
        fd.seek(0)  
        return fd  
    return open(url_or_path, 'rb')  
  
  
def parse_prompt(prompt):  
    if prompt.startswith('http://') or prompt.startswith('https://'):  
        vals = prompt.rsplit(':', 2)  
        vals = [vals[0] + ':' + vals[1], *vals[2:]]  
    else:  
        vals = prompt.rsplit(':', 1)  
    vals = vals + ['', '1'][len(vals):]  
    return vals[0], float(vals[1])  
  
  
class MakeCutouts(nn.Module):  
    def __init__(self, cut_size, cutn, cut_pow=1.):  
        super().__init__()  
        self.cut_size = cut_size  
        self.cutn = cutn  
        self.cut_pow = cut_pow  
  
    def forward(self, input):  
        sideY, sideX = input.shape[2:4]  
        max_size = min(sideX, sideY)  
        min_size = min(sideX, sideY, self.cut_size)  
        cutouts = []  
        for _ in range(self.cutn):  
            size = int(torch.rand([])**self.cut_pow * (max_size - min_size) + min_size)  
            offsetx = torch.randint(0, sideX - size + 1, ())  
            offsety = torch.randint(0, sideY - size + 1, ())  
            cutout = input[:, :, offsety:offsety + size, offsetx:offsetx + size]  
            cutouts.append(F.adaptive_avg_pool2d(cutout, self.cut_size))  
        return torch.cat(cutouts)  
  
  
def spherical_dist_loss(x, y):  
    x = F.normalize(x, dim=-1)  
    y = F.normalize(y, dim=-1)  
    return (x - y).norm(dim=-1).div(2).arcsin().pow(2).mul(2)  
  
  
def tv_loss(input):  
    """L2 total variation loss, as in Mahendran et al."""  
    input = F.pad(input, (0, 1, 0, 1), 'replicate')  
    x_diff = input[..., :-1, 1:] - input[..., :-1, :-1]  
    y_diff = input[..., 1:, :-1] - input[..., :-1, :-1]  
    return (x_diff**2 + y_diff**2).mean([1, 2, 3])  
  
  
def range_loss(input):  
    return (input - input.clamp(-1, 1)).pow(2).mean([1, 2, 3])
```
```

---

spark
Gemini

```
```
# Model settings  
  
model_config = model_and_diffusion_defaults()  
model_config.update({  
    'attention_resolutions': '32, 16, 8',  
    'class_cond': False,  
    'diffusion_steps': 1000,  
    'rescale_timesteps': True,  
    'timestep_respacing': '1000',  # Modify this value to decrease the number of  
                                   # timesteps.  
    'image_size': 512,  
    'learn_sigma': True,  
    'noise_schedule': 'linear',  
    'num_channels': 256,  
    'num_head_channels': 64,  
    'num_res_blocks': 2,  
    'resblock_updown': True,  
    'use_checkpoint': False,  
    'use_fp16': True,  
    'use_scale_shift_norm': True,  
})
```
```

---

spark
Gemini

```
```
# Load models  
  
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')  
print('Using device:', device)  
  
model, diffusion = create_model_and_diffusion(**model_config)  
model.load_state_dict(torch.load('512x512_diffusion_uncond_finetune_008100.pt', map_location='cpu'))  
model.requires_grad_(False).eval().to(device)  
if model_config['use_fp16']:  
    model.convert_to_fp16()  
  
clip_model = clip.load('ViT-B/16', jit=False)[0].eval().requires_grad_(False).to(device)  
clip_size = clip_model.visual.input_resolution  
normalize = transforms.Normalize(mean=[0.48145466, 0.4578275, 0.40821073],  
                                 std=[0.26862954, 0.26130258, 0.27577711])  
lpips_model = lpips.LPIPS(net='vgg').to(device)
```
```

---

spark
Gemini

keyboard\_arrow\_down

## Settings for this run:

subdirectory\_arrow\_right
已隐藏 3 个单元格

---

spark
Gemini

```
```
prompts = ['alien friend by Odilon Redon']  
image_prompts = []  
batch_size = 1  
clip_guidance_scale = 1000  # Controls how much the image should look like the prompt.  
tv_scale = 150              # Controls the smoothness of the final output.  
range_scale = 50            # Controls how far out of range RGB values are allowed to be.  
cutn = 32  
cutn_batches = 2  
cut_pow = 0.5  
n_batches = 1  
init_image = None   # This can be an URL or Colab local path and must be in quotes.  
skip_timesteps = 0  # This needs to be between approx. 200 and 500 when using an init image.  
                    # Higher values make the output look more like the init.  
init_scale = 0      # This enhances the effect of the init image, a good value is 1000.  
seed = 0
```
```

---

spark
Gemini

keyboard\_arrow\_down

### Actually do the run...

subdirectory\_arrow\_right
已隐藏 1 个单元格

---

spark
Gemini

```
```
def do_run():  
    if seed is not None:  
        torch.manual_seed(seed)  
  
    make_cutouts = MakeCutouts(clip_size, cutn, cut_pow)  
    side_x = side_y = model_config['image_size']  
  
    target_embeds, weights = [], []  
  
    for prompt in prompts:  
        txt, weight = parse_prompt(prompt)  
        target_embeds.append(clip_model.encode_text(clip.tokenize(txt).to(device)).float())  
        weights.append(weight)  
  
    for prompt in image_prompts:  
        path, weight = parse_prompt(prompt)  
        img = Image.open(fetch(path)).convert('RGB')  
        img = TF.resize(img, min(side_x, side_y, *img.size), transforms.InterpolationMode.LANCZOS)  
        batch = make_cutouts(TF.to_tensor(img).unsqueeze(0).to(device))  
        embed = clip_model.encode_image(normalize(batch)).float()  
        target_embeds.append(embed)  
        weights.extend([weight / cutn] * cutn)  
  
    target_embeds = torch.cat(target_embeds)  
    weights = torch.tensor(weights, device=device)  
    if weights.sum().abs() < 1e-3:  
        raise RuntimeError('The weights must not sum to 0.')  
    weights /= weights.sum().abs()  
  
    init = None  
    if init_image is not None:  
        init = Image.open(fetch(init_image)).convert('RGB')  
        init = init.resize((side_x, side_y), Image.LANCZOS)  
        init = TF.to_tensor(init).to(device).unsqueeze(0).mul(2).sub(1)  
  
    cur_t = None  
  
    def cond_fn(x, t, out, y=None):  
        n = x.shape[0]  
        fac = diffusion.sqrt_one_minus_alphas_cumprod[cur_t]  
        x_in = out['pred_xstart'] * fac + x * (1 - fac)  
        x_in_grad = torch.zeros_like(x_in)  
        for i in range(cutn_batches):  
            clip_in = normalize(make_cutouts(x_in.add(1).div(2)))  
            image_embeds = clip_model.encode_image(clip_in).float()  
            dists = spherical_dist_loss(image_embeds.unsqueeze(1), target_embeds.unsqueeze(0))  
            dists = dists.view([cutn, n, -1])  
            losses = dists.mul(weights).sum(2).mean(0)  
            x_in_grad += torch.autograd.grad(losses.sum() * clip_guidance_scale, x_in)[0] / cutn_batches  
        tv_losses = tv_loss(x_in)  
        range_losses = range_loss(x_in)  
        loss = tv_losses.sum() * tv_scale + range_losses.sum() * range_scale  
        if init is not None and init_scale:  
            init_losses = lpips_model(x_in, init)  
            loss = loss + init_losses.sum() * init_scale  
        x_in_grad += torch.autograd.grad(loss, x_in)[0]  
        grad = -torch.autograd.grad(x_in, x, x_in_grad)[0]  
        return grad  
  
    if model_config['timestep_respacing'].startswith('ddim'):  
        sample_fn = diffusion.ddim_sample_loop_progressive  
    else:  
        sample_fn = diffusion.p_sample_loop_progressive  
  
    for i in range(n_batches):  
        cur_t = diffusion.num_timesteps - skip_timesteps - 1  
  
        samples = sample_fn(  
            model,  
            (batch_size, 3, side_y, side_x),  
            clip_denoised=False,  
            model_kwargs={},  
            cond_fn=cond_fn,  
            progress=True,  
            skip_timesteps=skip_timesteps,  
            init_image=init,  
            randomize_class=True,  
            cond_fn_with_grad=True,  
        )  
  
        for j, sample in enumerate(samples):  
            if j % 100 == 0 or cur_t == 0:  
                print()  
                for k, image in enumerate(sample['pred_xstart']):  
                    filename = f'progress_{i * batch_size + k:05}.png'  
                    TF.to_pil_image(image.add(1).div(2).clamp(0, 1)).save(filename)  
                    tqdm.write(f'Batch {i}, step {j}, output {k}:')  
                    display.display(display.Image(filename))  
            cur_t -= 1  
  
gc.collect()  
do_run()
```
```

---

[Colab 付费产品](/signup?utm_source=footer&utm_medium=link&utm_campaign=footer_links)
-
[在此处取消合同](/cancel-subscription)



more\_vert


close

more\_vert


close



more\_vert


close

data\_object
变量
terminal
终端

打开云端硬盘中所在位置

在云端硬盘中新建笔记本

打开笔记本

上传笔记本

重命名

移动

移至回收站

在云端硬盘中保存一份副本

将副本另存为 GitHub Gist

在 GitHub 中保存一份副本

保存

保存并标记修订版本

修订历史记录

笔记本信息

下载
►

打印

下载 .ipynb

下载 .py

撤销

重做

选择所有单元格

剪切单元格或所选内容

复制单元格或所选内容

粘贴

删除所选单元格

查找和替换

查找下一个

查找上一个

笔记本设置

清除所有输出项

check

目录

代码执行历史记录

开始播放幻灯片

从头开始播放幻灯片

评论
►

收起段落

展开段落

保存收起的段落布局

显示/隐藏代码

显示/隐藏输出项

将焦点放在下个标签页上

将焦点放在上个标签页上

将标签页移到下一个窗格

将标签页移到上一个窗格

隐藏评论

最小化评论

展开评论

代码单元格

文本单元格

段落标题单元格

暂存代码单元格

代码段

添加表单字段

全部运行

运行当前单元格之前的所有单元格

运行光标所在的单元格

运行所选单元格的内容

运行当前单元格和下方的所有单元格

中断执行

重启会话

重启会话并运行所有单元

断开连接并删除运行时

更改运行时类型

管理会话

查看资源

查看运行时日志

部署到 Google Cloud Run

命令面板

设置

键盘快捷键

差异笔记本 （在新标签页中打开）

常见问题解答

查看版本说明

搜索代码段

报告错误

举报云端硬盘滥用行为

发送反馈

查看服务条款

查看英文版
