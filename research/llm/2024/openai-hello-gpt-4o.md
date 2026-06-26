---
title: Hello GPT-4o
org: OpenAI
country: US
date: 2024-05
type: blog
categories: [架构, 后训练]
url: https://openai.com/index/hello-gpt-4o/
pdf_url:
github_url:
downloaded: [openai-hello-gpt-4o.md]
---

## 一句话定位
GPT-4o（"o"=omni）发布博客：OpenAI 首个真正端到端、单一神经网络处理文本/音频/图像/视频的全模态旗舰模型。

## 摘要
2024-05-13 发布。GPT-4o 能接受文本、音频、图像、视频任意组合输入，并生成文本、音频、图像任意组合输出，全部由同一个神经网络端到端处理。对音频输入最快 232 毫秒、平均 320 毫秒响应，接近人类对话响应时间。英文文本与代码性能与 GPT-4 Turbo 持平，非英语文本显著改进，API 更快且价格降低 50%，在视觉与音频理解上尤为出色。相比此前"语音模式"由三个独立模型串联（转录→GPT-4→TTS，平均延迟 GPT-3.5 2.8s / GPT-4 5.4s），GPT-4o 直接在单模型内完成全模态转换。

## 关键技术细节
- 架构：单一端到端神经网络统一处理全部模态（此前语音模式为 3 模型 pipeline，会丢失语气/多说话人/背景噪音信息）。
- 延迟：音频响应最快 232ms，平均 320ms（对比旧语音模式 2.8s/5.4s）。
- 性能：文本/推理/编码达 GPT-4 Turbo 水平；多语言、音频、视觉创新高。
- API：速度更快、价格便宜 50%。
- 新 tokenizer：对非英语语言压缩率大幅提升（如俄语 token 减少 1.7×：39→23；韩语 1.7×：45→27；以及阿拉伯语等）。
- 配套发布 GPT-4o System Card（风险评分卡）。

## 原始链接
- url: https://openai.com/index/hello-gpt-4o/
- system card: https://openai.com/index/gpt-4o-system-card/

## 一手源存档（sources/）
- [openai-hello-gpt-4o.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2024/openai-hello-gpt-4o.md)
