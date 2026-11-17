# pplx-decider-v1.3

**Rank:** 8  
**Release date:** 2026-11-12  
**Area:** Model Releases  
**Primary source:** Perplexity  
**Availability:** Decisions API, OpenRouter, and Apache-2.0-tagged Hugging Face weights. The model card says local checkpoint access requires an authorized Hugging Face token. ([community.perplexity.ai](https://community.perplexity.ai/t/were-rolling-out-pplx-decider-v1-3-and-pplx-decider-flash-v1-3-the-latest-version-of-our-open-weight-decision-models/6606))

## What Changed

Compared with v1.2, Decider v1.3 adds **Locate**, a typed extraction request that matches a label or instruction against text and returns verbatim spans with character offsets and scores. The local implementation loads an adapter for Locate; mixed extraction and decision requests require separate forward passes. A Flash variant is also available. ([community.perplexity.ai](https://community.perplexity.ai/t/were-rolling-out-pplx-decider-v1-3-and-pplx-decider-flash-v1-3-the-latest-version-of-our-open-weight-decision-models/6606))

## Why It Matters

Offsets let applications attach extracted evidence directly to the input rather than parse generated prose. Engineers building routing or document-processing pipelines should validate span quality and latency on their own inputs: Locate requires nonempty text and does not accept images in the local implementation. ([huggingface.co](https://huggingface.co/perplexity-ai/pplx-decider-v1.3))

## Evidence

**Kind:** Primary release and model card  
**Independently validated:** no

Perplexity publishes the request schema and local inference example. Its performance and agreement figures are **developer-reported**; the corroborating coverage reviewed the model card rather than independently reproducing the results. ([huggingface.co](https://huggingface.co/perplexity-ai/pplx-decider-v1.3))

## Links

- [Release announcement](https://community.perplexity.ai/t/were-rolling-out-pplx-decider-v1-3-and-pplx-decider-flash-v1-3-the-latest-version-of-our-open-weight-decision-models/6606) (primary)
- [Model card](https://huggingface.co/perplexity-ai/pplx-decider-v1.3) (weights and implementation)

## Assessment

- **Technical novelty:** Meaningful — an extraction adapter adds scored, offset-based spans to an existing structured decision interface.
- **Practical significance:** Medium — teams extracting evidence for routing or document workflows should test it against their own data and latency budget.
- **Confidence:** Medium — the announcement and model card corroborate the interface; performance and availability of authorized checkpoint access were not independently tested.
