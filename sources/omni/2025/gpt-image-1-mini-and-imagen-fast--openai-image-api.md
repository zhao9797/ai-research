# 介绍我们最新的图像生成模型在 API 中的应用 | OpenAI
Source: https://openai.com/zh-Hans-CN/index/image-generation-api/
介绍我们最新的图像生成模型在 API 中的应用 | OpenAI

[跳至主要内容](#main)

* [研究](/zh-Hans-CN/research/index/)
* 产品
* [企业](/zh-Hans-CN/business/)
* [开发人员](/zh-Hans-CN/api/)
* [公司](/zh-Hans-CN/about/)
* [基金会（在新窗口中打开）](https://openaifoundation.org/zh-Hans-CN/)

登录[试用 ChatGPT（在新窗口中打开）](https://chatgpt.com/?openaicom-did=d9e79e3b-f725-4d25-a85e-84c2b9dac923&openaicom_referred=true)

* 研究
* 产品
* 企业
* 开发人员
* 公司
* [基金会（在新窗口中打开）](https://openaifoundation.org/zh-Hans-CN/)

介绍我们最新的图像生成模型在 API 中的应用 | OpenAI

2025年4月23日

[产品](/zh-Hans-CN/news/product-releases/)

# 介绍我们最新的图像生成模型在 API 中的应用

[在 Playground 中试用（在新窗口中打开）](http://platform.openai.com/playground/images?preset=sunglasses-sun)

分享

安全性

* [安全性](#an-quan-xing)
* [定价](#ding-jie)
* [开始使用](#kai-shi-shi-yong)

目录

* [安全性](#an-quan-xing)
* [定价](#ding-jie)
* [开始使用](#kai-shi-shi-yong)

上月我们在 ChatGPT 中推出图像生成功能后，该功能迅速成为最受欢迎的功能之一：全球超过 1.3 亿用户在[首周⁠（在新窗口中打开）](https://www.linkedin.com/posts/bradlightcap_very-crazy-first-week-for-images-in-chatgpt-activity-7313616345667878912-RBzt/)内生成超过 7 亿张图片。

今日，我们通过 `gpt-image-1` 将驱动 ChatGPT 该功能的原生多模态模型引入 API，使开发者和企业能够轻松将高质量、专业级图像生成功能直接集成到自有工具和平台中。该模型的灵活性使其能够生成多种风格的图片、严格遵循自定义指南、利用世界知识，并准确渲染文本——在多个领域开启无数实用应用场景。

来自创意工具、电子商务、教育、企业软件、游戏等行业的领先企业和初创公司已在其产品和体验中应用图像生成技术。我们很高兴分享以下部分案例。

AdobeAirtableFigmaGammaHeyGenOpusClipQuoraWixPhotoroomPlayground

**Adobe** 的创意工具生态系统（包括 Firefly 和 Express 应用）将提供对 OpenAI 图像生成功能的访问权限，为创作者提供选择和灵活性，以实验不同的美学风格——这是商业专业人士、消费者和创作者在生成新创意时都重视的。

我们还继续与开发者和企业合作，探索 API 中的图像生成技术如何更好地服务于他们的具体需求，包括：

**设计与编辑：Canva** 正在探索将 OpenAI 的 `gpt-image-1` 集成到其 Canva AI 和 Magic Studio 工具中，以突破设计生成和编辑的界限。通过 `gpt-image-1` 的功能，如将粗略草图转化为令人惊叹的图形元素，以及实现高保真视觉编辑，Canva 将进一步赋能其 2.3 亿用户以全新方式将创意变为现实。

**创建和编辑徽标：GoDaddy** 正在积极实验将图像生成功能集成到其平台中，以便客户能够轻松创建可编辑的徽标、去除背景并生成专业字体。此外，作为 GoDaddy Airo® 的新体验，团队正致力于让客户能够创建反映其独特品牌身份的社交媒体帖子和营销资产，这些内容可通过提示生成原创产品和品牌内容。

**制作营销材料：HubSpot** 正在探索 OpenAI 的新 AI 图像生成功能如何帮助客户创建营销和销售材料。随着 HubSpot 继续添加新的 AI 驱动工具以帮助企业扩展业务，这些图像生成功能有望改变客户制作高质量图片的方式，从而用于社交媒体、电子邮件营销和着陆页，而无需专业的设计技能。

**生成食谱和购物清单：Instacart** 正在测试利用 API 进行图像生成的全新方式，包括食谱和购物清单的图像生成。

**视频编辑：invideo** 使数百万用户能够借助 AI 将创意转化为视频。通过集成 `gpt-image-1`，该平台现提供改进的文本生成功能、精细化编辑控制以及高级风格指导。

## 安全性

API 中的 `gpt-image-1` 模型采用了与 ChatGPT 中 4o 图像生成相同的安全防护措施，包括限制模型生成有害图片的防护措施，以及在生成的图片中包含 C2PA 元数据——您可以在[此处](/zh-Hans-CN/index/introducing-4o-image-generation/)我们的过去博客文章中了解更多详情。此外，开发者可通过审核参数控制审核敏感度，该参数默认设置为**自动**（默认），用于标准过滤，也可设置为**低**，用于宽松过滤。更多信息，请参阅我们的[文档⁠（在新窗口中打开）](https://platform.openai.com/docs/api-reference/images)。

默认情况下，我们从不使用客户 API 数据进行训练，且所有图片输入和输出均受我们的 [API 使用政策](/policies/usage-policies/)约束。

## 定价

`gpt-image-1` 的使用按令牌计费，文本和图片令牌分别定价：

* **文本输入令牌（提示文本）：**每 100 万令牌 5 美元
* **图片输入令牌（输入图片）：**每 100 万令牌 10 美元
* **图片输出令牌（生成的图片）：**每 100 万令牌 40 美元

实际使用中，这相当于低、中、高品质正方形图片分别约为每张 0.02 美元、0.07 美元和 0.19 美元。有关按图片质量和大小的详细定价，请参阅[文档⁠（在新窗口中打开）](https://platform.openai.com/docs/pricing)。

## 开始使用

`gpt-image-1` 模型现已通过图片 API 全球开放，回复 API 的支持功能即将推出。部分开发者可能需要[验证⁠（在新窗口中打开）](https://help.openai.com/en/articles/10910291-api-organization-verification)其⁠组织权限后才能使用该模型。请查看[组织设置⁠（在新窗口中打开）](https://platform.openai.com/settings/organization/limits)以确认是否已具备访问权限。

要开始使用，请在 [Playground⁠（在新窗口中打开）](https://platform.openai.com/playground/images) 中探索模型的功能，并查看我们的[图像生成指南⁠⁠（在新窗口中打开）](https://platform.openai.com/docs/guides/image-generation)。我们期待看到您创建的作品。

* [2025 年](/zh-Hans-CN/news/?tags=2025)
* [API 平台](/zh-Hans-CN/news/?tags=api-platform)

## 作者

OpenAI

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

* [ChatGPT（在新窗口中打开）](https://chatgpt.com/?openaicom-did=d9e79e3b-f725-4d25-a85e-84c2b9dac923&openaicom_referred=true)
* [ChatGPT Business（在新窗口中打开）](https://chatgpt.com/business/?openaicom-did=d9e79e3b-f725-4d25-a85e-84c2b9dac923&openaicom_referred=true)
* [ChatGPT Enterprise（在新窗口中打开）](https://chatgpt.com/zh-Hans-CN/business/enterprise/?openaicom-did=d9e79e3b-f725-4d25-a85e-84c2b9dac923&openaicom_referred=true)
* [ChatGPT for Education（在新窗口中打开）](https://chatgpt.com/zh-Hans-CN/business/education/?openaicom-did=d9e79e3b-f725-4d25-a85e-84c2b9dac923&openaicom_referred=true)
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

![](https://bat.bing.com/action/0?ti=187204252&Ver=2&mid=a811cfdf-a818-44c9-8d67-572a5478f1c3&bo=1&sid=7d99feb0706511f1a6736bc5df141779&vid=7d99fa60706511f19d07012bf5385135&vids=1&msclkid=N&pi=918639831&lg=zh-CN&sw=1440&sh=900&sc=24&tl=%E4%BB%8B%E7%BB%8D%E6%88%91%E4%BB%AC%E6%9C%80%E6%96%B0%E7%9A%84%E5%9B%BE%E5%83%8F%E7%94%9F%E6%88%90%E6%A8%A1%E5%9E%8B%E5%9C%A8%20API%20%E4%B8%AD%E7%9A%84%E5%BA%94%E7%94%A8%20%7C%20OpenAI&p=https%3A%2F%2Fopenai.com%2Fzh-Hans-CN%2Findex%2Fimage-generation-api%2F&r=&lt=1664&evt=pageLoad&sv=2&cdb=AQAQ&rn=857949)
