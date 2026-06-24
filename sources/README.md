# sources — 原始资料

按 `research/llm` 的 scope 镜像组织：`sources/llm/<年份|themes/专题|deep-dive>/<原文件>`。

## 入 git 的部分
- `*.html`（官方博客快照）、`*.json`、各 README —— 体积小、易失效，随仓库版本化。

## 不入 git 的部分（PDF，约 2.5GB）
存算分离：PDF 原文不进 git，存放于 **HuggingFace Storage Bucket**。

获取方式二选一：
1. 从 bucket 同步：`hf buckets sync hf://buckets/<owner>/<bucket>/llm ./sources/llm`
2. 按 URL 重下：`research/llm/01-INDEX.md` 每条都带 arXiv/官方 PDF 链接。
