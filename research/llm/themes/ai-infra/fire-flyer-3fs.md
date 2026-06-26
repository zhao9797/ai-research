---
title: 3FS (Fire-Flyer File System) — High-performance Distributed File System for AI
org: DeepSeek-AI
country: China
date: 2025-02
type: github
categories: [AI infra]
url: https://github.com/deepseek-ai/3FS
github_url: https://github.com/deepseek-ai/3FS
downloaded: [3fs-readme.md]
---

## 一句话定位
DeepSeek 开源的面向 AI 训练/推理的高性能分布式文件系统，基于 SSD + RDMA，提供数据准备、dataloader、checkpoint、推理 KVCache 的统一高吞吐存储层。

## 摘要（3-6 句）
3FS（Fire-Flyer File System）用现代 NVMe SSD 与 RDMA 网络构建共享存储层，采用解耦架构聚合数千 SSD 与数百存储节点的带宽，提供位置无关访问。它用 CRAQ（Chain Replication with Apportioned Queries）实现强一致，元数据服务无状态、后端为事务 KV 存储（如 FoundationDB），保留标准文件接口。面向数据准备、随机访问 dataloader（免预取/shuffle）、大规模并行 checkpoint、推理 KVCache 二级缓存等场景。180 节点集群读吞吐约 6.6 TiB/s。

## 关键技术细节
- 架构：disaggregated（解耦计算与存储），CRAQ 强一致，stateless metadata + 事务 KV（FoundationDB）。
- 峰值吞吐：180 存储节点（每节点 2×200Gbps IB + 16×14TiB NVMe）+ 500+ 客户端，读吞吐约 6.6 TiB/s（含训练背景流量）。
- GraySort：25 存储 + 50 计算节点，110.5 TiB 数据 8192 分区 30 分 14 秒完成，3.66 TiB/min。
- KVCache 缓存：读吞吐峰值 40 GiB/s，作为 DRAM 之外的低成本大容量 KV 二级缓存。
- USRBIO 用户态零拷贝 I/O API；配套 smallpond 数据处理框架。

## 原始链接
- url: https://github.com/deepseek-ai/3FS
- github_url: https://github.com/deepseek-ai/3FS

## 一手源存档（sources/）
- [3fs-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/themes/ai-infra/3fs-readme.md)
