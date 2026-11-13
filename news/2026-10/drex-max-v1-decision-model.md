# Drex Max v1 decision model

**Rank:** 6  
**Release date:** 2026-10-30  
**Area:** Model Releases  
**Primary source:** Nace.AI  
**Availability:** Public weights on Hugging Face and loader on GitHub, under Nace.AI Open RAIL-M.

Nace announced the open-weight release on October 30. Its research page is dated November 6; the technical report was first submitted on November 5. ([teapaw.org](https://teapaw.org/NaceAI/status/2116163656480428220))

## What Changed

Drex Max is a dense 27B multimodal model that returns probabilities over supplied options rather than generating an answer. For each question, it encodes the context and options, then applies a 255-way linear readout to the final answer-marker state and normalizes over the supplied options.

Its Gated DeltaNet layers remain left-to-right, while its full-attention layers attend bidirectionally. The supplied loader applies that attention pattern; an ordinary causal forward pass does not reproduce the intended scores. Unlike the family’s causal pointer models, Max must re-encode the state for each question rather than reuse a cached state. ([arxiv.org](https://arxiv.org/html/2611.07854v1))

## Why It Matters

The bounded, single-pass output is worth testing for routing, tool selection and other decisions where an application can enumerate options. Engineers should measure calibration, option-order sensitivity and latency on their own workloads; avoiding generated text does not guarantee a correct decision.

## Evidence

**Kind:** Public weights, implementation, developer benchmarks and third-party measurement  
**Independently validated:** yes, with a checkpoint caveat

Nace provides the weights, loader and technical report. Its reported accuracy and latency comparisons remain **developer-reported**.

Separately, Shreyas Subramanian of Scale AI evaluated a hosted Drex Max endpoint on judging benchmarks. That is an independent measurement of the hosted model, not a verified reproduction of the local v1 checkpoint or its routing performance. ([huggingface.co](https://huggingface.co/nace-ai/drex-max-v1))

## Links

- [Nace research page](https://www.nace.ai/research/towards-foundation-decision-models) (primary)
- [Technical report](https://arxiv.org/abs/2611.07854) (primary)
- [Model card and weights](https://huggingface.co/nace-ai/drex-max-v1) (weights)
- [Drex decision models repository](https://github.com/nace-ai/drex-decision-models) (implementation)
- [Independent judging evaluation](https://arxiv.org/abs/2611.00505) (third-party measurement)
- [Open-weight announcement](https://teapaw.org/NaceAI/status/2116163656480428220) (release date)

## Assessment

- **Technical novelty:** meaningful — a bidirectional-attention readout scores supplied options without autoregressive generation.
- **Practical significance:** high — engineers building bounded-choice agents should test it against their existing routing or tool-selection stack.
- **Confidence:** medium — the architecture and artifacts are documented, and a hosted endpoint has third-party measurements; local-checkpoint equivalence and application-specific performance remain unverified.

## GitHub signal

**Ideas worth investigating:**

- Apply non-causal masks only to the backbone’s full-attention layers while preserving the DeltaNet recurrence.
- Read option logits from the final answer-marker state and normalize only across supplied choices.
