# Tencent Hy4

**Rank:** 3  
**Release date:** 2026-11-20  
**Area:** Model Releases  
**Primary source:** Tencent  
**Availability:** Downloadable instruct, FP8, and pretrained base weights under the Tencent Hy License; the model card documents vLLM and SGLang serving recipes. ([huggingface.co](https://huggingface.co/tencent/Hy4))

## What Changed

Hy4’s weights are now public, following its earlier API release. Its multimodal language backbone has 770B total parameters and activates 49B per text token; those counts exclude the vision encoder, adapter, and drafter. ([huggingface.co](https://huggingface.co/tencent/Hy4))

The model combines gated DeepSeek Sparse Attention with IndexCache, which reuses sparse-attention indices across layers. Its separate DFly2 speculative drafter shares each corresponding target layer’s KV cache and selected sparse indices, rather than maintaining its own KV cache and indexer. ([huggingface.co](https://huggingface.co/tencent/Hy4))

## Why It Matters

The weights and serving recipes give systems engineers a large-scale artifact for investigating index reuse and speculative decoding with shared inference state. The design may reduce drafting overhead, but its actual throughput and acceptance rates need workload-specific measurement. ([huggingface.co](https://huggingface.co/tencent/Hy4))

## Evidence

**Kind:** Primary release and public implementation  
**Independently validated:** no

Tencent’s model card describes the architecture, weights, deployment recipes, and developer-reported benchmarks. The public commit history records an update on November 20. No independent reproduction of the model’s performance or drafting efficiency was established here. ([huggingface.co](https://huggingface.co/tencent/Hy4))

## Links

- [Hy4 model card and weights](https://huggingface.co/tencent/Hy4) (weights)
- [Model repository commit history](https://huggingface.co/tencent/Hy4/commits/main) (primary)
- [Official Hy4 repository](https://github.com/Tencent-Hunyuan/Hy4) (repository)
- [IndexCache paper](https://arxiv.org/abs/2603.12201) (research)

## Assessment

- **Technical novelty:** meaningful — the model combines cross-layer sparse-index reuse with a drafter that shares target KV state and selected indices.
- **Practical significance:** high — serving and inference-systems researchers should try the released weights and recipes, subject to available hardware.
- **Confidence:** medium — the artifacts, model card, and commit history were checked; performance and efficiency claims remain developer-reported.

## GitHub signal

**Ideas worth investigating:**

- Cross-layer sparse-index reuse with gated sparse attention.
- Speculative drafting that shares target-layer KV caches and selected positions.
