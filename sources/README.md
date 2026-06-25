# sources — 原始资料

按 `research/<scope>` 镜像组织：`sources/<scope>/<年份|themes/专题|deep-dive>/<原文件>`。
现有 scope：`sources/llm/` 与 `sources/omni/`。

## 入 git 的部分
- `*.html`（官方博客快照）、`*.md`（cloakbrowser 渲染的博客/model card 快照）、`*.json`、各 README —— 体积小、易失效，随仓库版本化。

## 不入 git 的部分
存算分离：`*.pdf`（论文/技术报告原文，数 GB）与大图 `*.png/*.jpg` 不进 git，备份在 **HuggingFace Storage Bucket（private）** `hf://buckets/jaczhao/ai-research-sources/`，按 scope 分子目录（`llm/`、`omni/`）。

前置：`pip install -U "huggingface_hub[hf_xet]"`（或 `uvx --from "huggingface_hub[hf_xet]" hf …`）并 `export HF_TOKEN=...`（或 `hf auth login`）。

```bash
# 拉取（bucket → 本地），以 omni 为例（llm 同理替换 scope）
hf buckets sync hf://buckets/jaczhao/ai-research-sources/omni ./sources/omni
# 回传（本地 → bucket）
hf buckets sync ./sources/omni hf://buckets/jaczhao/ai-research-sources/omni
```

- **或按 URL 重下**：`research/<scope>/01-INDEX.md` 每条都带 arXiv/官方 PDF 链接，可直接从源头重新下载。
- bucket 为 **private**（含第三方版权 PDF，不公开再分发）；对外分享请走本仓库的分析页（已公开）。
