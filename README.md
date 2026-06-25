# ai-research

个人 AI 技术调研仓库 —— **只收一手官方资料**（arXiv 原文 / 官方技术报告 / system card / 官方博客 / 官方 GitHub·HF·ModelScope model card），不含任何第三方解读、翻译或二手聚合。

每个工作都按统一维度精读（**数据 · 训练方法 · 模型架构 · 评测 benchmark · Infra** + 创新影响），**所有数字均经对抗式核查逐条对照一手源**（删串列 / 张冠李戴 / 杜撰）。

---

## 两大调研

### 📚 [`research/llm/`](research/llm/) — 大模型技术演进（GPT-3 2020-05 → 2026-06）
- 去重后 **525+ 条**一手来源；五大类：**预训练数据 · 架构 · AI infra · 后训练 · agentic 训练**
- 入口 → [`research/llm/00-SUMMARY.md`](research/llm/00-SUMMARY.md)　·　全量索引 → [`research/llm/01-INDEX.md`](research/llm/01-INDEX.md)
- 分类汇总 `sections/`　·　开源模型深挖 `deep-dive/`

### 🎨 [`research/omni/`](research/omni/) — 多模态 / 全模态「生成」演进（2020 → 2026-H1）
- **324 工作页 / ~322 条**一手来源；覆盖 **文生图 · 图像编辑 · 统一理解生成 · any-to-any omni · 视频 · 音频 · 3D · 使能方法**
- 入口 → [`research/omni/00-SUMMARY.md`](research/omni/00-SUMMARY.md)　·　全量索引 → [`research/omni/01-INDEX.md`](research/omni/01-INDEX.md)
- 6 横向章节 `sections/`（架构 / 数据 / 训练 / benchmark / infra / 统一omni 专题）　·　5 模型族 `deep-dive/`（SD-FLUX 谱系 / 中国系 T2I / 统一omni / 视频 / 编辑）

> 各 scope 的组织方式与"怎么读"详见 [`research/README.md`](research/README.md)。

---

## 目录结构

```
ai-research/
├── research/<scope>/      # 分析（你读的部分）
│   ├── 00-SUMMARY.md      #   主汇总（先读这个）
│   ├── 01-INDEX.md        #   全量来源索引（按年月，含每条原始 URL）
│   ├── 2020/ … 2026/      #   单工作结构化页（六维精读）
│   ├── sections/          #   横向分类汇总
│   └── deep-dive/         #   模型 / 家族横向深挖
└── sources/<scope>/       # 原始资料（落盘存档）
    └── 2020/ … 2026/      #   *.md/*.html 博客快照(入 git) + *.pdf(走 HF bucket)
```

## 存算分离

- **入 git**：`*.md` / `*.html` / `*.json`（官方博客·model card 快照，体积小、易失效，值得版本化）
- **不入 git**：`*.pdf`（数 GB，论文/技术报告原文）+ 大图 `*.png/*.jpg` —— 备份在 **HuggingFace private Storage Bucket** `hf://buckets/jaczhao/ai-research-sources/<scope>`，亦可按 `01-INDEX.md` 中每条的 arXiv/官方 URL 重新下载。详见 [`sources/README.md`](sources/README.md)。

## 怎么读（从"结论"到"原文"四层）

1. **主汇总** `00-SUMMARY.md` —— 脉络速览 + 统计 + 导读
2. **横向章节 / 深挖** `sections/` · `deep-dive/` —— 按主题或家族横向对比
3. **全量索引** `01-INDEX.md` —— 按年月可点开每一条
4. **单工作页** `<年>/<slug>.md` —— 六维精读；**原文**在 `sources/<scope>/<年>/`
