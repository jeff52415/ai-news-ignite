# vLLM v0.33.0 speculative decoding and prefix caching

**Rank:** 2  
**Release date:** 2026-11-02  
**Area:** Inference & Infrastructure  
**Primary source:** vLLM  
**Availability:** Public source and PyPI wheels. The GitHub release is titled v0.33.0 but points to `v0.33.0rc3`; verify the source tag and wheel before deployment. ([github.com](https://github.com/vllm-project/vllm/releases/tag/v0.33.0rc3))

## What Changed

**XPress** adds a causal refinement head to block-diffusion drafters such as DFlash. It combines draft hidden states, a block summary and preceding tokens, then iteratively refines draft logits rather than decoding each position independently. ([github.com](https://github.com/vllm-project/vllm/pull/54448))

**FLy** is an opt-in, lossy verification policy. It can accept an otherwise rejected draft token at a high-entropy position if subsequent tokens pass native verification. Unlike standard speculative verification, it does not preserve the target distribution. ([github.com](https://github.com/vllm-project/vllm/pull/53987))

**Lookahead block hashes** include the token after a cache block for EAGLE-style and MTP drafters. This allows a matching local prefix-cache hit to retain a trailing block previously discarded because its draft KV depended on that next token. The original implementation retains legacy behavior when a KV connector is configured. ([github.com](https://github.com/vllm-project/vllm/pull/61589))

## Why It Matters

Serving teams can test whether better draft acceptance and longer cache hits reduce decoding or prefill work. FLy requires a separate output-quality evaluation: greater throughput is not evidence of equivalent outputs. Cache-event consumers should also account for lookahead tokens in block hashes. ([github.com](https://github.com/vllm-project/vllm/pull/53987))

## Evidence

**Kind:** Open-source implementation and developer-reported benchmarks  
**Independently validated:** no

XPress contributor ZKBig reported **18.5% higher throughput** than the bare DFlash drafter in a Qwen3-8B evaluation on one H200. FLy contributor eecspan reported **1.041–1.310× decode throughput** over standard speculative decoding across the stated ModelRunner V2 configurations on MI355X and B300; the associated quality measurements were single-pass tests, not a quality guarantee. These are developer-reported results, not independent reproductions. ([github.com](https://github.com/vllm-project/vllm/pull/54448))

## Links

- [vLLM release notes](https://github.com/vllm-project/vllm/releases/tag/v0.33.0rc3) (release notes)
- [vLLM 0.33.0 on PyPI](https://pypi.org/project/vllm/0.33.0/) (package)
- [XPress implementation](https://github.com/vllm-project/vllm/pull/54448) (repository)
- [FLy implementation](https://github.com/vllm-project/vllm/pull/53987) (repository)
- [Lookahead block hashes](https://github.com/vllm-project/vllm/pull/61589) (repository)
- [Release-tag mismatch issue](https://github.com/vllm-project/vllm/issues/65662) (issue)

## Assessment

- **Technical novelty:** Meaningful — causal draft refinement, relaxed verification and lookahead-aware cache keys address distinct sources of speculative-serving overhead.
- **Practical significance:** High — inference teams using compatible drafters or repeated prefixes should benchmark the changes on their own traffic, with quality checks for FLy.
- **Confidence:** Medium — the release, implementation changes and package listing were checked; performance and quality results remain developer-reported.

## GitHub signal

**Ideas worth investigating:**

- Causal refinement of block-diffusion drafts using iterative updates.
- Entropy-gated deferral of speculative-token rejection.
- Lookahead tokens in prefix-cache keys for draft-KV correctness.
