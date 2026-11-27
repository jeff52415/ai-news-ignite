# Kolibri 1.1

**Rank:** 4  
**Release date:** 2026-11-23  
**Area:** Model Releases  
**Primary source:** Aleph Alpha  
**Availability:** Apache 2.0 weights and model card on Hugging Face.

## What Changed

Kolibri 1.1 converts the existing Kolibri 1 mixture-of-experts model to sparse attention through continued training. Instead of relying on dense attention throughout, it interleaves sliding-window attention with sparse attention: sparse layers select up to 2,048 keys per query, and subsequent layers reuse key-value representations and sparse selections. The configuration is 75 billion total parameters and 3.44 billion active parameters per token.

## Why It Matters

The release offers an example of adapting an existing MoE for more efficient long-context processing without training a new model from scratch. Its native context is 262,144 tokens; longer inputs are extrapolations, for which the model card advises caution on complex tasks. Sparse prefill speedups do not necessarily translate into equivalent decoding or KV-cache savings.

## Evidence

**Kind:** Public weights, implementation documentation, and developer-reported benchmarks  
**Independently validated:** no

Aleph Alpha reports up to a **14× prefill speedup** over Kolibri 1 at a one-million-token input on H100 hardware. That is a developer-reported result at an extrapolated context length, not an independent measurement or a general decoding-speed claim.

## Links

- [Kolibri 1.1 model card and weights](https://huggingface.co/Aleph-Alpha/Kolibri-1.1) (weights and model card)
- [Kolibri 1.1 Transformers documentation](https://huggingface.co/docs/transformers/main/model_doc/kolibri1_1) (implementation documentation)
- [Sparse attention in Kolibri 1.1](https://aleph-alpha.com/en/blog/sparse-attention-in-kolibri-1-1/) (developer technical description)

## Assessment

- **Technical novelty:** meaningful — continued training combines sparse key selection with cross-layer KV sharing in an existing MoE.
- **Practical significance:** high — engineers building long-context inference systems should test the public weights against their own workloads and context-length requirements.
- **Confidence:** medium — the model card, technical description, and implementation documentation were checked; performance and quality claims remain developer-reported.
