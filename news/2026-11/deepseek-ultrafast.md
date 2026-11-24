# DeepSeek Ultrafast

**Rank:** 5  
**Release date:** 2026-11-13  
**Area:** Inference & Infrastructure  
**Primary source:** Baseten  
**Availability:** Source available under Elastic License 2.0; requires DeepSeek-V4.1-Flash weights, CUDA 13, and supported multi-GPU Blackwell systems. ([github.com](https://github.com/basetenlabs/deepseek-ultrafast))

## What Changed

DeepSeek Ultrafast retains recent conversational KV caches in host memory. When a later turn reaches another replica, Redis identifies the owner and the receiving server fetches the cache host-to-host over RDMA, avoiding prefix recomputation. This reduces reliance on routing each conversation back to its original replica. ([github.com](https://github.com/basetenlabs/deepseek-ultrafast))

The model-specific Rust/CUDA engine also uses speculative decoding: each step drafts and verifies a block of tokens rather than generating only one token per step. Cache exchange requires compatible replica configurations; supported GPU configurations are not automatically interchangeable. ([yuxiaoba.github.io](https://yuxiaoba.github.io/tech/en/deepseek-ultrafast/))

## Why It Matters

Movable KV state can improve load-balancing flexibility for long, multi-turn agent workloads. Direct deployment is specialized, however: the engine targets one model and particular Blackwell configurations. A third-party code review also found that each replica processes one job at a time, making the engine more directly relevant to single-stream latency than batched throughput. ([ai.satyajit.si](https://ai.satyajit.si/articles/baseten-deepseek-engine))

## Evidence

**Kind:** Public implementation and developer-reported benchmark  
**Independently validated:** no

Baseten reports **1,740 decode tokens/s** on four GB300 GPUs for a specific Tetris-coding prompt. This is a developer-reported single-workload result, not a general throughput measurement. An independent source-code review examined the execution path but did not run the engine. ([github.com](https://github.com/basetenlabs/deepseek-ultrafast))

## Links

- [DeepSeek Ultrafast repository](https://github.com/basetenlabs/deepseek-ultrafast) (primary implementation)
- [DeepSeek Ultrafast technical analysis](https://yuxiaoba.github.io/tech/en/deepseek-ultrafast/) (independent analysis)
- [Source-code review](https://ai.satyajit.si/articles/baseten-deepseek-engine) (independent analysis)

## Assessment

- **Technical novelty:** meaningful — Redis ownership tracking and RDMA transfer make conversational KV state movable across replicas.
- **Practical significance:** medium — inference engineers serving long conversations on supported hardware should evaluate it against their own latency and concurrency needs.
- **Confidence:** medium — the implementation and independent code analyses were checked; performance and operational reliability remain unverified by an independent run.

## GitHub signal

**Ideas worth investigating:**

- Host-memory KV transfer between replicas over RDMA.
- Redis ownership revisions and stale-claim handling.
- Configuration fingerprints that prevent incompatible cache exchange. ([yuxiaoba.github.io](https://yuxiaoba.github.io/tech/en/deepseek-ultrafast/))
