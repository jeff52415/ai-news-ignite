# WePocketModel 1.0

**Rank:** 1  
**Release date:** 2026-11-23  
**Area:** Model Releases  
**Primary source:** Tencent  
**Availability:** Downloadable 2B and 4B weights, with Transformers, GGUF and MLX inference paths. The 4B weights and repository code are Apache 2.0 licensed. ([github.com](https://github.com/Tencent/WePocketModel))

## What Changed

WePocketModel uses one vision–language backbone for embeddings, autoregressive generation and structured decisions, rather than loading a separate specialist for each. Embedding and decision use separate learned slots and task heads.

Its visual budgeting divides a fixed token budget among global, regional and fine-grained views. Training combines teacher distillation with fixed task-loss weights and scheduled task exposure; sequential gradient accumulation reduces activation memory during joint updates. ([github.com](https://github.com/Tencent/WePocketModel))

## Why It Matters

A shared resident model could simplify local retrieval, response generation and routing while reducing duplicated model weights. Engineers should still validate decision quality and measure end-to-end memory and latency on their own hardware; weight size alone is not runtime memory. ([huggingface.co](https://huggingface.co/tencent/WePocketModel1.0-4B))

## Evidence

**Kind:** Public implementation and developer-reported evaluation  
**Independently validated:** no

Tencent published inference code, weights and a technical report. The developers report approximately 8 GB of BF16 weights for the 4B model versus approximately 21–43 GB for their compared specialist stacks; this is a weight-memory comparison, not a measurement of peak runtime memory. ByteForward reviewed the release but stated that it did not run the models. ([github.com](https://github.com/Tencent/WePocketModel))

## Links

- [WePocketModel repository](https://github.com/Tencent/WePocketModel) (repository)
- [4B model weights](https://huggingface.co/tencent/WePocketModel1.0-4B) (weights)
- [WePM technical report](https://arxiv.org/abs/2611.27365) (paper)
- [ByteForward GGUF guide](https://bytefwd.com/tencent-wepocketmodel-local-weights-gguf/) (independent coverage)

## Assessment

- **Technical novelty:** meaningful — the model combines shared task-specific slots with visual budgeting, distillation and scheduled multitask training.
- **Practical significance:** high — engineers building local multimodal retrieval and routing pipelines should test it against their existing specialist stack.
- **Confidence:** medium — the repository, model card and independent coverage were checked, but quality and memory comparisons remain developer-reported.

## GitHub signal

**Ideas worth investigating:**

- Separate learned embedding and decision slots on a shared backbone.
- Context-conditioned selection across a fixed multigranularity visual-token budget.
- Sequential gradient accumulation with scheduled task exposure.
