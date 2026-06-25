# CogView-4 - 智谱AI开放文档
Source: https://docs.bigmodel.cn/cn/guide/models/image-generation/cogview-4
CogView-4 - 智谱AI开放文档
> ## Documentation Index
>
> Fetch the complete documentation index at: </llms.txt>
>
> Use this file to discover all available pages before exploring further.

[Skip to main content](#content-area)

[智谱AI开放文档 home page![light logo](https://cdn.bigmodel.cn/static/logo/dark.svg)![dark logo](https://cdn.bigmodel.cn/static/logo/light.svg)](https://bigmodel.cn/)

Search...

⌘K

* [控制台](https://bigmodel.cn/console/overview)
* [价格](https://bigmodel.cn/pricing)
* [财务](https://bigmodel.cn/finance/overview)
* [API Key](https://bigmodel.cn/usercenter/proj-mgmt/apikeys)
* [个人中心](https://bigmodel.cn/usercenter/settings/account)

Search...

Navigation

图像生成模型

CogView-4

[使用指南](/cn/guide/start/introduction)[API 文档](/cn/api/introduction)[场景示例](/cn/best-practice/latency-optimization)[编码套餐](/cn/coding-plan/overview)[更新日志](/cn/update/new-releases)[条款与协议](/cn/terms/user-agreement)[常见问题](/cn/faq/api-code)

### 开始使用

* [平台介绍](/cn/guide/start/introduction)
* [模型概览](/cn/guide/start/model-overview)
* [快速开始](/cn/guide/start/quick-start)
* [核心参数](/cn/guide/start/concept-param)
* 开发指南
* [迁移至 GLM-5.2](/cn/guide/start/migrate-to-glm-new)

### 模型介绍

* 文本模型
* 视觉理解模型
* 图像生成模型

  + [GLM-Image](/cn/guide/models/image-generation/glm-image)
  + [CogView-4](/cn/guide/models/image-generation/cogview-4)
* 视频生成模型
* 音视频模型
* 向量模型
* 角色模型
* 免费模型

### 模型能力

* [深度思考](/cn/guide/capabilities/thinking)
* [思考模式](/cn/guide/capabilities/thinking-mode)
* [流式消息](/cn/guide/capabilities/streaming)
* [工具流式输出](/cn/guide/capabilities/stream-tool)
* [工具调用](/cn/guide/capabilities/function-calling)
* [上下文缓存](/cn/guide/capabilities/cache)
* [结构化输出](/cn/guide/capabilities/struct-output)

### 模型工具

* [GLM in Excel（Beta）](/cn/guide/tools/glm-in-excel)
* [联网搜索](/cn/guide/tools/web-search)
* [模型部署](/cn/guide/tools/model-deploy)
* [模型微调](/cn/guide/tools/fine-tuning)
* [模型评测](/cn/guide/tools/evaluation)
* [批量处理](/cn/guide/tools/batch)
* 文件解析
* [OCR 服务](/cn/guide/tools/zhipu-ocr)

### GLM 全模态知识库

* [知识处理及检索](/cn/guide/tools/knowledge/multimodal-retrieval)
* [知识问答](/cn/guide/tools/knowledge/q&a)
* [知识库服务计费](/cn/guide/tools/knowledge/price)
* [上下文增强技术报告](/cn/guide/tools/knowledge/contextual)
* [对话调用知识库](/cn/guide/tools/knowledge/retrieval)

### 智能体

* [通用翻译](/cn/guide/agents/translation)
* [AI 绘图](/cn/guide/agents/aidrawing)
* [热门特效视频](/cn/guide/agents/specialeffectsvideos)
* [GLM PPT](/cn/guide/agents/glm-ppt)
* [客服话术质检](/cn/guide/agents/customer)
* [衣物识别](/cn/guide/agents/clothes)
* [票据识别](/cn/guide/agents/bill)
* [智能解题](/cn/guide/agents/solving)

### 平台服务

* [智能体开发平台](/cn/guide/platform/intelligent-agent)
* [提示词工程](/cn/guide/platform/prompt)
* [内容安全](/cn/guide/platform/securityaudit)
* [模型迁移](/cn/guide/platform/model-migration)
* [用户权益](/cn/guide/platform/equity-explain)
* [模型备案](/cn/guide/platform/filing)

## On this page

* [概览](#%E6%A6%82%E8%A7%88)
* [推荐场景](#%E6%8E%A8%E8%8D%90%E5%9C%BA%E6%99%AF)
* [使用资源](#%E4%BD%BF%E7%94%A8%E8%B5%84%E6%BA%90)
* [详细介绍](#%E8%AF%A6%E7%BB%86%E4%BB%8B%E7%BB%8D)
  + [发布时模型性能达到 SOTA](#%E5%8F%91%E5%B8%83%E6%97%B6%E6%A8%A1%E5%9E%8B%E6%80%A7%E8%83%BD%E8%BE%BE%E5%88%B0-sota)
  + [更好的中文理解与生成](#%E6%9B%B4%E5%A5%BD%E7%9A%84%E4%B8%AD%E6%96%87%E7%90%86%E8%A7%A3%E4%B8%8E%E7%94%9F%E6%88%90)
  + [任意分辨率，任意长度提示词](#%E4%BB%BB%E6%84%8F%E5%88%86%E8%BE%A8%E7%8E%87%EF%BC%8C%E4%BB%BB%E6%84%8F%E9%95%BF%E5%BA%A6%E6%8F%90%E7%A4%BA%E8%AF%8D)
* [应用示例](#%E5%BA%94%E7%94%A8%E7%A4%BA%E4%BE%8B)
* [调用示例](#%E8%B0%83%E7%94%A8%E7%A4%BA%E4%BE%8B)
* [用户并发权益](#%E7%94%A8%E6%88%B7%E5%B9%B6%E5%8F%91%E6%9D%83%E7%9B%8A)

图像生成模型

# CogView-4

Copy page

Copy page

## [​](#概览) 概览

CogView-4 是智谱首个支持生成汉字的开源文生图模型，在语义理解、图像生成质量、中英文字生成能力等方面全面提升，支持任意长度的中英双语输入，能够生成在给定范围内的任意分辨率图像。

## 价格

0.06 元 / 次

## 输入模态

文本

## 输出模态

图像

## [​](#推荐场景) 推荐场景

餐饮美食宣传

根据菜品名称、食材特点及风格要求，融入创意文字元素，生成色泽诱人、细节逼真的美食图片，适配菜单设计、外卖平台展示、线下海报等多场景使用。

电商产品配图

依据商品特点与卖点描述，快速生成高清商品展示图，添加中英促销文字，适配电商平台不同规格的商品页与活动图需求。

游戏素材创作

依据游戏世界观与角色设定，产出高分辨率、细节丰富的角色立绘、场景原画等素材，满足多分辨率制作需求。

教育资料配图

解析教学文本内容，自动生成匹配的插图、场景图，适配各类教育资料的排版与分辨率要求，助力知识可视化呈现。

文旅宣传制作

根据文旅主题，生成不同尺寸的宣传图像，将文字与地域特色视觉元素巧妙结合，提升文旅推广的吸引力。

## [​](#使用资源) 使用资源

[## 体验中心

快速测试模型在业务场景上的效果](https://www.bigmodel.cn/trialcenter/modeltrial/multimodal?modelCode=cogview-4-250304)

[## 接口文档

API 调用方式](/api-reference/%E6%A8%A1%E5%9E%8B-api/%E5%9B%BE%E5%83%8F%E7%94%9F%E6%88%90)

## [​](#详细介绍) 详细介绍

1

### 发布时模型性能达到 SOTA

DPG-Bench （Dense Prompt Graph Benchmark）是一个评估文本到图像生成模型的基准测试，主要关注模型在复杂语义对齐和指令跟随能力方面的表现。CogView-4 发布时期在 DPG-Bench 基准测试中综合评分排名第一，在开源文生图模型中达到 SOTA。![Description](https://cdn.bigmodel.cn/markdown/1749449849627DPG-Bench.png?attname=DPG-Bench.png)

2

### 更好的中文理解与生成

在技术实现上，CogView-4 将文本编码器从纯英文的 T5 encoder 换为具备双语能力的 GLM-4 encoder，并通过中英双语图文进行训练，使模型具备双语提示词输入能力。CogView-4 支持中英双语提示词输入，尤其擅长理解和遵循中文提示词，大幅降低使用者提示词门槛，是首个能够在画面中生成汉字的开源文生图模型，能更好地满足广告、短视频等领域的创意需求。

3

### 任意分辨率，任意长度提示词

CogView-4 实现了任意长度的文本描述（caption）和任意分辨率图像的混合训练范式。该模型支持输入任意长度提示词，能够生成范围内任意分辨率图像，不仅使用户创作更加自由，也提升了训练效率。

## [​](#应用示例) 应用示例

* 餐饮美食宣传
* 电商产品配图
* 游戏素材创作
* 文旅宣传制作

## Prompt

特写，商业美食摄影，强烈的室内光，极致的细节，圣诞餐桌，餐桌一角，一个长毛橘色虎斑猫头凑到盘子旁，正在贪婪地闻着圣诞大餐，表情沉醉。桌上有烤鸡、植物、沙拉，香槟酒，镶金边的瓷器茶具。下午的金色光线照向猫咪的侧脸，将食物和它的被毛染上了柔和的金色，背景也有圣诞树。突出食物的质感和猫咪的毛发质感，强烈的光感，温馨的圣诞节日氛围。

## 生成图片

![Description](https://cdn.bigmodel.cn/markdown/1753523666666cogview-1.jpg?attname=cogview-1.jpg)

## Prompt

2个白色不透明且不反光的奶茶杯上装饰着大小不一的复杂金色图案，图案是圣诞节日主体，包括驯鹿和松树，杯子之外是温暖的红色背景和闪烁的节日灯光，展示在微型雪景中，自然光线

## 生成图片

![Description](https://cdn.bigmodel.cn/markdown/1753523552952cogview-2.jpg?attname=cogview-2.jpg)

## Prompt

黑金色系。美少女战士塔罗牌，画面充满屏幕。动漫插画。色彩柔和，一个带着魔法帽的长发魔女低着头，驼着背，侧面对着镜头，提着一盏灯

## 生成图片

![Description](https://cdn.bigmodel.cn/markdown/1753523560520cogview-3.jpg?attname=cogview-3.jpg)

## Prompt

香港维多利亚港的璀璨夜景，采用双重曝光技术，将繁华的城市天际线与璀璨的烟花完美融合。夜空中多个烟花绽放，形成巨大的爱心形状，完全叠加在画面中央。烟花呈现出五彩斑斓的色彩，金色、红色、蓝色和紫色交织在一起，照亮了整个夜空。城市灯光在背景中闪烁，摩天大楼的轮廓清晰可见，街道上的霓虹灯映衬出城市的活力。画面整体呈现出一种梦幻而浪漫的氛围，令人仿佛置身于香港的璀璨夜色之中。

## 生成图片

![Description](https://cdn.bigmodel.cn/markdown/1753523569831cogview-4.jpg?attname=cogview-4.jpg)

## [​](#调用示例) 调用示例

* Python
* Java
* Python(旧)

**安装 SDK**

```
# 安装最新版本
pip install zai-sdk
# 或指定版本
pip install zai-sdk==0.2.3
```

**验证安装**

```
import zai
print(zai.__version__)
```

**调用示例**

```
from zai import ZhipuAiClient
client = ZhipuAiClient(api_key="your-api-key")  # 请填写您自己的 APIKey
response = client.images.generations(
    model="cogView-4-250304",  # 请填写您要调用的模型名称
    prompt="一只可爱的小猫咪，坐在阳光明媚的窗台上，背景是蓝天白云",
)
print(response.data[0].url)
```

**安装 SDK****Maven**

```
<dependency>
    <groupId>ai.z.openapi</groupId>
    <artifactId>zai-sdk</artifactId>
    <version>0.3.5</version>
</dependency>
```

**Gradle (Groovy)**

```
implementation 'ai.z.openapi:zai-sdk:0.3.5'
```

**调用示例**

```
import ai.z.openapi.ZhipuAiClient;
import ai.z.openapi.core.Constants;
import ai.z.openapi.service.image.CreateImageRequest;
import ai.z.openapi.service.image.ImageResponse;

public class CogView4Example {
    public static void main(String[] args) {
        ZhipuAiClient client = ZhipuAiClient.builder().ofZHIPU().apiKey("YOUR_API_KEY").build();
        // Create image generation request
        CreateImageRequest request = CreateImageRequest.builder()
            .model(Constants.ModelCogView4250304)
            .prompt("一只可爱的小猫咪，坐在阳光明媚的窗台上，背景是蓝天白云")
            .size("1024x1024")
            .build();
        ImageResponse response = client.images().createImage(request);
        System.out.println(response.getData());
    }
}
```

```
from zhipuai import ZhipuAI

client = ZhipuAI(api_key="your-api-key")

response = client.images.generations(
    model="cogView-4-250304", #填写需要调用的模型编码
    prompt="在干燥的沙漠环境中，一棵孤独的仙人掌在夕阳的余晖中显得格外醒目。这幅油画捕捉了仙人掌坚韧的生命力和沙漠中的壮丽景色，色彩饱满且表现力强烈。",
    size="1440x720"
)
print(response.data[0].url)
```

请注意，CogView-4 模型的输出是图片 URL，您需要通过 URL 下载图片。

## [​](#用户并发权益) 用户并发权益

API 调用会受到速率限制，当前我们限制的维度是请求并发数量（在途请求任务数量）。不同等级的用户并发保障如下。

| V0 | V1 | V2 | V3 |
| --- | --- | --- | --- |
| 5 | 10 | 15 | 20 |

Was this page helpful?

YesNo

[GLM-Image](/cn/guide/models/image-generation/glm-image)[CogVideoX-3](/cn/guide/models/video-generation/cogvideox-3)

⌘I

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=zhipu-ef7018ed)

![Description](https://cdn.bigmodel.cn/markdown/1749449849627DPG-Bench.png?attname=DPG-Bench.png)

![Description](https://cdn.bigmodel.cn/markdown/1753523666666cogview-1.jpg?attname=cogview-1.jpg)

![Description](https://cdn.bigmodel.cn/markdown/1753523552952cogview-2.jpg?attname=cogview-2.jpg)

![Description](https://cdn.bigmodel.cn/markdown/1753523560520cogview-3.jpg?attname=cogview-3.jpg)

![Description](https://cdn.bigmodel.cn/markdown/1753523569831cogview-4.jpg?attname=cogview-4.jpg)
