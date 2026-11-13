# Ripple-65B Preview

**Rank:** 2  
**Release date:** 2026-11-04  
**Area:** Model Releases  
**Primary source:** Ricursive Intelligence model card  
**Availability:** Apache 2.0 base and instruction-tuned weights on Hugging Face; an NVFP4 instruction checkpoint is also available.

## What Changed

Ripple-65B is a dense Transformer that mixes predominantly sliding-window attention layers with less frequent global-attention layers, rather than applying global attention uniformly. It also uses gated attention, global layers without positional embeddings (NoPE), and value residuals. The model card states support for contexts up to one million tokens. 

## Why It Matters

The layout gives engineers a dense-model alternative to compare with mixture-of-experts models for long-context inference. The local/global mix is worth testing for its effects on memory use, throughput, and retrieval quality; the published architecture alone does not establish those tradeoffs for a particular serving stack.

## Evidence

**Kind:** Third-party task testing and developer-reported benchmarks  
**Independently validated:** yes

GMI Cloud reports running its own agent tests involving bugs, tools, and planted traps. It also hosts the model, so its results should not be treated as independent validation of every model-card benchmark. The model-card benchmark results remain developer-reported. 

## Links

- [Instruction model card and weights](https://huggingface.co/ricursiveAI/Ripple-65B-Preview) (model)
- [Base model and weights](https://huggingface.co/ricursiveAI/Ripple-65B-Base-Preview) (model)
- [NVFP4 instruction checkpoint](https://huggingface.co/ricursiveAI/Ripple-65B-Preview-NVFP4) (quantized weights)
- [GMI Cloud agent tests](https://www.gmicloud.ai/en/blog/we-tested-ripple-65b-preview-with-real-bugs-live-tools-and-planted-traps-here-is-what-held-up) (third-party testing)

## Assessment

- **Technical novelty:** meaningful — the model combines mostly local attention with periodic global attention, gating, NoPE, and value residuals.
- **Practical significance:** high — engineers evaluating self-hosted long-context models should test it against their own workloads and MoE baselines.
- **Confidence:** medium — the model card and GMI’s tests were checked, but broader benchmark claims remain developer-reported and serving tradeoffs need workload-specific measurement.

## GitHub signal

**Ideas worth investigating:**

- The sliding-window/global-attention layer mix and its effect on long-context serving.
- Gated attention and value residuals.
- The NVFP4 checkpoint’s quality and throughput tradeoffs.
