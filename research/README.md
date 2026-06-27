# research/ — 调研分析

> 🌐 **English**: [README.en.md](README.en.md)

两个独立 scope，**同构组织**（都遵循下面的"四层阅读模型"）。这里是导航；具体内容进各 scope 的 `00-SUMMARY.md`。

| scope | 主题 | 跨度 | 规模 | 入口 |
|---|---|---|---|---|
| [`llm/`](llm/) | 大模型技术演进（预训练数据 / 架构 / AI infra / 后训练 / agentic） | GPT-3 2020-05 → 2026-06 | **525+** 一手源 | [00-SUMMARY](llm/00-SUMMARY.md) · [01-INDEX](llm/01-INDEX.md) |
| [`omni/`](omni/) | 多模态/全模态生成（文生图 / 编辑 / 统一理解生成 / any-to-any omni / 视频 / 音频 / 3D / 使能方法） | 2020 → 2026-H1 | **324 工作页 / ~322 源** | [00-SUMMARY](omni/00-SUMMARY.md) · [01-INDEX](omni/01-INDEX.md) |

## 每个 scope 的结构

```
<scope>/
├── 00-SUMMARY.md     # 主汇总：脉络速览 + 统计 + 导读（先读这个）
├── 01-INDEX.md       # 全量来源索引：按年月分组，每条带原始 URL，可点开
├── 2020/ … 2026/     # 单工作结构化页（一工作一文件，kebab-case slug）
├── sections/         # 横向分类/主题汇总
└── deep-dive/        # 模型或家族的横向深挖对比
```

## 四层阅读模型（从"结论"到"原文"）

1. **`00-SUMMARY.md`** —— 想要脉络与导读，只读这一页。
2. **`sections/` · `deep-dive/`** —— 想看某主题（架构演进、训练方法、benchmark…）或某家族（SD-FLUX、Qwen、统一 omni…）的横向对比。
3. **`01-INDEX.md`** —— 想按时间线浏览全部条目、找某条的原始链接。
4. **`<年>/<slug>.md`** —— 想看单个工作的六维精读（数据 / 训练 / 架构 / benchmark / Infra + 创新影响）；其**下载原文**在 `../sources/<scope>/<年>/`。

## 页面约定

- 每页顶部为 YAML frontmatter（`title / org / country / date / type / category / url / …`）。
- 正文用 Obsidian 风格 `[[slug]]` 内链互相串联（slug = 文件名去 `.md`）。
- 单工作页统一六维结构；数字均来自一手源并经对抗式 verify 核对。

## 维护

维护脚本在仓库 `scripts/` 目录（纯 Python 标准库、无依赖；用法见 `scripts/README.md`）：
- `build_index.py` / `build_index_omni.py` —— 从各页 frontmatter 重生成对应 scope 的 `01-INDEX.md`
- `normalize_wikilinks.py` —— 归一化 omni 内链别名（如 `[[dit]]`→`[[dit-scalable-diffusion-transformers]]`）
- `fix_frontmatter.py` —— 修复 YAML frontmatter
- `lint.py` —— 健检（重复页 / frontmatter / 死内链 / 目录-日期一致），CI 每次 push/PR 运行

新增或删除来源页后重跑 `build_index*.py` 刷新索引；提交前跑 `lint.py` 自检。
