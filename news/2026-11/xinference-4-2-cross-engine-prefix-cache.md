# Xinference 4.2: Cross-engine prefix-cache sharing

**Rank:** 3  
**Release date:** 2026-11-07  
**Area:** Inference & Infrastructure  
**Primary source:** Xorbits  
**Availability:** Xinference 4.2.0 is available as a public release and source code. Enable Xavier and configure an engine per replica to use cross-engine sharing. ([github.com](https://github.com/xorbitsai/inference/releases/tag/v4.2.0))

## What Changed

Ordinary Xavier replicas can now reuse compatible prefix KV caches across vLLM, SGLang, TensorRT-LLM and MLX, without assigning prefill and decode roles. Engine adapters exchange complete, immutable 64-token pages through a bounded supervisor-owned CPU cache. Compatibility checks include the checkpoint, tokenizer, model semantics, context limit, dtype and request salt; misses fall back to local computation. Mixed-engine ordinary groups do not support LMCache storage in this implementation. ([github.com](https://github.com/xorbitsai/inference/pull/5917))

A separate lifecycle extension binds authenticated agent-session metadata to token-derived cache keys. Waiting sessions receive a **soft retention preference**; completion or expiry removes that preference without deleting shared pages. The extension covers additional engine adapters and storage tiers, but not prefill/decode lifecycle hints. ([github.com](https://github.com/xorbitsai/inference/pull/6018))

## Why It Matters

Mixed-engine deployments can avoid recomputing compatible prefixes even when requests land on different replicas. Advisory retention may also improve reuse after tool waits, though cache-transfer overhead and eviction pressure need workload-specific measurement.

## Evidence

**Kind:** Public implementation and developer-reported tests  
**Independently validated:** no

The implementation is public. The developer reports that a two-worker vLLM/SGLang test reused 640 of 673 prompt tokens in both directions. The lifecycle-extension developer also reports a single vLLM disk-restoration mechanism test; it is not a production throughput or latency benchmark. No independent reproduction was found. ([github.com](https://github.com/xorbitsai/inference/pull/5917))

## Links

- [Xinference 4.2.0 release notes](https://github.com/xorbitsai/inference/releases/tag/v4.2.0) (release notes)
- [Cross-engine prefix-cache implementation](https://github.com/xorbitsai/inference/pull/5917) (implementation)
- [Agent cache lifecycle extension](https://github.com/xorbitsai/inference/pull/6018) (implementation)
- [Xavier configuration guide](https://inference.readthedocs.io/en/v4.2.0/user_guide/vllm_enhancement.html) (documentation)

## Assessment

- **Technical novelty:** meaningful — canonical CPU-resident pages and compatibility checks extend prefix reuse to ordinary mixed-engine replicas.
- **Practical significance:** high — engineers operating mixed-engine or tool-using agent workloads should test reuse and transfer costs on their own traffic.
- **Confidence:** medium — release notes, implementation discussions and documentation were checked; runtime results remain developer-reported.

## GitHub signal

**Ideas worth investigating:**

- Canonicalize complete KV pages for exchange across engine adapters, with identity checks before reuse.
- Bind session lifecycle hints to actual cache keys and prefer—but do not pin—waiting-session pages.
