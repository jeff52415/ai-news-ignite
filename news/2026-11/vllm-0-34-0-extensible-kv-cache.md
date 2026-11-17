# vLLM 0.34.0: extensible KV cache by default

**Rank:** 1  
**Release date:** 2026-11-16  
**Area:** Inference & Infrastructure  
**Primary source:** vLLM release notes  
**Availability:** Open-source release on GitHub.

## What Changed

The extensible KV cache is enabled by default. Rather than relying on an earlier estimate, vLLM determines cache capacity from available GPU memory after warmup and CUDA graph capture. The release also removes the older GPU Model Runner V1 implementation.

## Why It Matters

Sizing after startup allocations can give operators a more representative cache capacity for the running configuration. Before upgrading, serving teams should test cache capacity and concurrency alongside decode latency, and check for dependencies on the removed runner.

## Evidence

**Kind:** Public open-source implementation  
**Independently validated:** no

The vLLM release notes and implementation pull requests document the default change, sizing mechanism, and runner removal. No independent performance reproduction was established for this briefing.

## Links

- [vLLM 0.34.0 release notes](https://github.com/vllm-project/vllm/releases/tag/v0.34.0) (release notes)
- [Extensible KV cache implementation](https://github.com/vllm-project/vllm/pull/56492) (implementation)
- [Remove GPU Model Runner V1](https://github.com/vllm-project/vllm/pull/63373) (implementation)

## Assessment

- **Technical novelty:** meaningful — Cache sizing moves to after warmup and graph capture, when startup allocations are known.
- **Practical significance:** high — vLLM operators should test the new default and runner removal against their serving configurations.
- **Confidence:** medium — The release and implementation were checked; performance effects were not independently reproduced.

## GitHub signal

**Ideas worth investigating:**

- Post-warmup, post-graph-capture KV-cache sizing.
- Migration away from GPU Model Runner V1.
