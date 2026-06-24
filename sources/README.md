# sources — 原始资料

按 `research/llm` 的 scope 镜像组织：`sources/llm/<年份|themes/专题|deep-dive>/<原文件>`。

## 入 git 的部分
- `*.html`（官方博客快照）、`*.json`、各 README —— 体积小、易失效，随仓库版本化。

## 不入 git 的部分（PDF，约 2.5GB）
存算分离：PDF 原文不进 git，备份在 **HuggingFace Storage Bucket（private）**：
`hf://buckets/jaczhao/ai-research-sources/llm`

前置：`pip install -U "huggingface_hub[hf_xet]"` 并 `export HF_TOKEN=...`（或 `hf auth login`）。

- **拉取**（从 bucket 同步到本地）：
  `hf buckets sync hf://buckets/jaczhao/ai-research-sources/llm ./sources/llm`
- **回传**（本地变更同步回 bucket）：
  `hf buckets sync ./sources/llm hf://buckets/jaczhao/ai-research-sources/llm`
- **或按 URL 重下**：`research/llm/01-INDEX.md` 每条都带 arXiv/官方 PDF 链接。
