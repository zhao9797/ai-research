# ai-research

个人 AI 技术调研仓库（一手官方资料）。

## research/llm — 大模型技术演进调研（GPT-3 2020-05 → 2026-06）
- 去重后 **525 条**一手官方来源，五大类：预训练数据 / 架构 / AI infra / 后训练 / agentic 训练
- 入口：[`research/llm/00-SUMMARY.md`](research/llm/00-SUMMARY.md)
- 全量索引（按年月，含全部原始 URL）：[`research/llm/01-INDEX.md`](research/llm/01-INDEX.md)
- 分类汇总：`research/llm/sections/`；开源模型深挖：`research/llm/deep-dive/`

## sources/ — 原始资料（存算分离）
- `*.html` / `*.json` / `README`：随仓库提交（博客快照等，易失效，值得版本化存档）
- `*.pdf`：**不入 git**（约 2.5GB），备份在 HuggingFace Storage Bucket（见 [`sources/README.md`](sources/README.md）），亦可按 `01-INDEX.md` 的 URL 重新下载

> 只收 arXiv 原文 / 官方技术报告 / system card / 官方博客 / 官方 GitHub·model card，不含第三方解读。
