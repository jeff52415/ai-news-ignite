# llama.cpp 1.0

**Rank:** 3  
**Release date:** 2026-11-13  
**Area:** Inference & Infrastructure  
**Primary source:** llama.cpp release notes  
**Availability:** Open-source repository and tagged public release. ([github.com](https://github.com/ggml-org/llama.cpp/releases/tag/v1.0.0))

## What Changed

The release adds `f8_e4m3` KV-cache storage with optional **static** per-tensor scales. Scaling is applied at the graph level, rather than by modifying the flash-attention operation. ([github.com](https://github.com/ggml-org/llama.cpp/releases/tag/v1.0.0))

For MoE models whose expert weights reside in host memory, the cache keeps frequently used experts in device memory for small batches. Once it is full, a configurable share of misses can be computed on the CPU while other misses are uploaded; replacement uses an LRFU/ClassLRU-like policy. The release also moves the NextN speculative API from `llama-ext.h` into `llama.h` and removes deprecated public APIs. ([github.com](https://github.com/ggml-org/llama.cpp/blob/v1.0.0/docs/moe-cache.md))

## Why It Matters

Engineers can evaluate FP8 KV-cache memory savings against output quality and backend compatibility. For memory-constrained MoE serving, the cache and CPU-share controls offer a way to trade device capacity, upload bandwidth and CPU work; the best settings depend on the machine and model. API consumers should also check for removed or renamed interfaces. ([github.com](https://github.com/ggml-org/llama.cpp/blob/v1.0.0/docs/moe-cache.md))

## Evidence

**Kind:** Public implementation and developer tests  
**Independently validated:** no

The release notes and tagged MoE-cache documentation describe the implementation. FP8 contributor ORippler reports end-to-end tests for loading, context shifts and scaled-cache correctness; MoE-cache contributor am17an reports machine-specific tuning measurements. Neither is an independent general performance validation. ([github.com](https://github.com/ggml-org/llama.cpp/blob/v1.0.0/docs/moe-cache.md))

## Links

- [llama.cpp 1.0 release](https://github.com/ggml-org/llama.cpp/releases/tag/v1.0.0) (release notes)
- [llama.cpp repository](https://github.com/ggml-org/llama.cpp) (repository)
- [MoE cache documentation at v1.0.0](https://github.com/ggml-org/llama.cpp/blob/v1.0.0/docs/moe-cache.md) (documentation)
- [FP8 KV-cache implementation](https://github.com/ggml-org/llama.cpp/pull/28392) (pull request)

## Assessment

- **Technical novelty:** meaningful — FP8 cache storage and CPU-assisted expert-cache misses extend existing inference memory-management techniques.
- **Practical significance:** high — engineers serving long-context or memory-constrained MoE models should test the options on their own workloads.
- **Confidence:** medium — the release, tagged documentation and implementation pull request were checked; performance and quality effects remain workload-dependent and developer-reported.

## GitHub signal

**Ideas worth investigating:**

- Graph-level static scaling for FP8 KV caches.
- Device-side expert caching with configurable CPU execution of misses.
- The public NextN speculative-decoding API.
