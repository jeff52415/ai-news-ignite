# Inkling 2 Mini

**Rank:** 4  
**Release date:** 2026-11-20  
**Area:** Model Releases  
**Primary source:** Thinking Machines Lab model card  
**Availability:** Apache 2.0 open weights on Hugging Face; API access is also available through Tinker.

## What Changed

Inkling 2 Mini is a text-and-image-input, text-output model that reuses its middle transformer layers rather than storing a separate set of weights for every layer application. Its 24-layer decoder runs the middle 12 layers three times, producing 48 layer applications per token. Each MoE layer routes a token to 8 of 128 experts. The developer reports 26.4B total parameters and 3.4B active parameters; counting repeated applications gives 5.4B effective active parameters per token. ([thinkingmachines.ai](https://thinkingmachines.ai/model-card/inkling-2-mini/))

The model also uses attention over earlier block outputs and cross-loop attention that lets later passes read information from the preceding pass, rather than relying solely on a conventional cumulative residual stream. ([goodfire.com](https://www.goodfire.com/research/interpreting-inkling-2-mini/))

## Why It Matters

Weight sharing trades additional per-token computation for a smaller stored model. Engineers evaluating local coding or agent workloads can test that trade-off against latency, memory use, and task quality. The released Mini uses a fixed three-pass loop, so it is not itself a variable-depth inference control. ([thinkingmachines.ai](https://thinkingmachines.ai/news/inkling-2-mini/?utm_source=openai))

## Evidence

**Kind:** Public weights, developer benchmarks, and third-party interpretability analysis  
**Independently validated:** yes, for internal behavior; not for the reported coding benchmark

Goodfire analyzed the model’s weights and activations after receiving early access, measuring information flow across layers and loops. Separately, Thinking Machines **developer-reported** a 48.2% DeepSWE v1.1 score using mini-swe-agent v2.4.6; that score is not independently reproduced here. ([goodfire.com](https://www.goodfire.com/research/interpreting-inkling-2-mini/))

## Links

- [Model card](https://thinkingmachines.ai/model-card/inkling-2-mini/) (primary)
- [Model weights](https://huggingface.co/thinkingmachines/Inkling-2-Mini) (weights)
- [Goodfire interpretability analysis](https://www.goodfire.com/research/interpreting-inkling-2-mini/) (third-party analysis)

## Assessment

- **Technical novelty:** meaningful — shared middle layers, sparse experts, and cross-loop attention combine repeated computation with a smaller stored backbone.
- **Practical significance:** high — engineers serving coding or agent models locally should test the memory–latency trade-off on their own workloads.
- **Confidence:** medium — the model card, weights listing, and Goodfire’s analysis were checked; benchmark performance and deployment benefits remain developer-reported or workload-dependent.