# Vertex AI / Gemini Enterprise — Veo 2 Generate 001 (veo-2.0-generate-001) 技术规范
Source: https://cloud.google.com/vertex-ai/generative-ai/docs/models/veo/2-0-generate-001
Fetched: 2026-06-25 via cloakbrowser (page redirected to docs.cloud.google.com/gemini-enterprise-agent-platform, zh-CN render)
Note: 这是 veo-2.0-generate-001 GA 端点的规格快照（发布阶段：正式版；发布日期 2025-05-27；终止日期 2026-06-30）。原 2024-12 preview 端点 veo-2.0-generate-preview/exp 已并入此页历史版本。

## 提取的核心规格表（veo-2.0-generate-001, 正式版）
Veo 2 是我们稳定的视频生成模型系列。本页面介绍了 Veo 2 的功能和特性。

[2.0 Generate 001](#2.0-generate-001)[2.0 Generate](#2.0-generate-experimental)[2.0 Generate](#2.0-generate-preview)
更多

| 模型 ID | veo-2.0-generate-001 | |
| --- | --- | --- |
| 支持的输入和输出 | * 输入： 文本 * 输出： 视频 | |
| 功能 | * 支持  + [文本转视频](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/generate-videos-from-text?hl=zh-cn) + [图片转视频](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/generate-videos-from-an-image?hl=zh-cn) + [重写提示](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/turn-the-prompt-rewriter-off?hl=zh-cn) + [参考样式图片](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/use-reference-images-to-guide-video-generation?hl=zh-cn#use-style-images) + [参考素材资源图片](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/use-reference-images-to-guide-video-generation?hl=zh-cn#use-subject-images) + [将对象插入视频](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/insert-objects-into-videos?hl=zh-cn)    preview   预览版功能 + [从视频中移除对象](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/remove-objects-from-videos?hl=zh-cn)    preview   预览版功能 + [Content Credentials (C2PA)](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/content-credentials?hl=zh-cn)  * 不支持  + [延长视频](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/extend-a-veo-video?hl=zh-cn) + [根据第一帧和最后一帧生成视频](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/generate-videos-from-first-and-last-frames?hl=zh-cn) | |
| 使用类型 | * 支持  + [固定配额](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/quotas?hl=zh-cn)  * 不支持  + [预配吞吐量](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/provisioned-throughput?hl=zh-cn) + [标准按需付费](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/standard-paygo?hl=zh-cn) | |
| 技术规范 |
| **视频** | * 视频时长：   5 到 8 秒 * 每个提示的输出视频数量上限：   4 * 图片转视频的最大输入图片大小：   20 MB * 支持的宽高比：   9:16、16:9 * 支持的输出分辨率：   720p * 支持的输入分辨率：   720p * 支持的帧速率：   24 FPS * 支持的 MIME 类型： `video/mp4` |
| 版本 | * `veo-2.0-generate-001`  + 发布阶段：正式版 + 发布日期：2025 年 5 月 27 日 + 终止日期：2026 年 6 月 30 日 | |
| 提示语言 | * 英语 |
| 配额 | * 每个基本模型每分钟的区域级在线预测请求数：10 | |

