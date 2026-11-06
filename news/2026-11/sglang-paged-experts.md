# SGLang Paged Experts

**Rank:** 1  
**Release date:** 2026-11-02  
**Area:** Inference & Infrastructure  
**Primary source:** SGLang v0.5.23 release notes  
**Availability:** Open-source SGLang v0.5.23; enable with `--enable-paged-experts`. Optionally set `--paged-experts-num-resident`. ([github.com](https://github.com/sgl-project/sglang/releases/tag/v0.5.23))

## What Changed

Paged Experts keeps routed expert weights in pinned host memory and a bounded set of experts resident on the GPU. When routing selects a nonresident expert, its weights are copied to the GPU, where the existing fused MoE kernel executes them. This differs from SGLang’s CPU-offload path, which streams offloaded weights on each forward pass regardless of routing. ([github.com](https://github.com/sgl-project/sglang/pull/42557))

The implementation uses LRU residency management. Steps exceeding the resident capacity can run in waves; a device-side paging path permits eligible decode steps to be captured in CUDA graphs. ([github.com](https://github.com/sgl-project/sglang/pull/42557))

## Why It Matters

The path makes some oversized MoE models practical on a single consumer GPU, trading GPU expert residency against KV-cache capacity. Performance depends on routing locality, host–GPU bandwidth, prompt length, and concurrency. The expert store must also fit in pinnable host memory. Engineers should measure first-token latency and tail inter-token latency on representative traffic. ([github.com](https://github.com/sgl-project/sglang/pull/42557))

## Evidence

**Kind:** Public implementation and developer benchmarks  
**Independently validated:** no

Implementation author N3mezis reported bit-identical log probabilities for the tested BF16 and FP8 cases against an unpaged server; GPTQ results were within the stated tolerance. In one developer-reported Qwen3-30B-A3B FP8 test on a 16 GB RTX 5070 Ti, single-stream decode reached 87.7 tokens/s with paging versus 2.9 tokens/s with SGLang CPU offload. Results are workload-specific, not an independent reproduction. ([github.com](https://github.com/sgl-project/sglang/pull/42557))

## Links

- [SGLang v0.5.23 release notes](https://github.com/sgl-project/sglang/releases/tag/v0.5.23) (release notes)
- [Paged Experts implementation and tests](https://github.com/sgl-project/sglang/pull/42557) (implementation)
- [Paged Experts quantization-format support](https://github.com/sgl-project/sglang/pull/45787) (implementation)

## Assessment

- **Technical novelty:** meaningful — demand paging applies a GPU working-set cache to routed expert weights while keeping expert computation on the GPU.
- **Practical significance:** high — engineers serving MoE models constrained by GPU memory should test it against their existing offload configuration.
- **Confidence:** medium — the release and implementation were checked; performance and accuracy measurements remain developer-reported.

## GitHub signal

**Ideas worth investigating:**

- GPU-side LRU decisions and gathers from pinned host memory for CUDA-graph-compatible decode.
- Wave-based execution when a step routes to more experts than fit in the resident slots.
