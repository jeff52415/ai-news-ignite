# Ling-3.1-flash-1019

**Rank:** 5  
**Release date:** 2026-10-27  
**Area:** Model Releases  
**Primary source:** inclusionAI model repository  
**Availability:** Downloadable FP8 weights under the MIT license.

## What Changed

Ling-3.1-flash-1019 is a **post-trained update** to Ling-3.1-flash, rather than a newly documented architecture. Both model cards describe a hybrid-linear mixture of experts with 560B total and 25B active parameters per token, using 63 KDA layers and nine gated MLA layers. The update retains the reported 1M-token context window. ([huggingface.co](https://huggingface.co/inclusionAI/Ling-3.1-flash-1019))

The card documents SGLang serving with MTP speculative decoding, but its example points to the **predecessor’s** model path; engineers testing this checkpoint should substitute the 1019 path. ([huggingface.co](https://huggingface.co/inclusionAI/Ling-3.1-flash-1019))

## Why It Matters

The checkpoint gives serving engineers a concrete target for measuring hybrid-state and attention-cache behavior, long-context performance, and speculative decoding. Those properties need workload-specific measurement; the release alone does not establish a serving advantage over conventional attention-based MoEs.

## Evidence

**Kind:** Public weights, developer-reported benchmarks, and third-party evaluation  
**Independently validated:** yes

The repository history records the weight upload on October 27. Artificial Analysis independently evaluated the model on its Intelligence Index; that is evidence of capability measurement, not validation of the proposed cache or decoding benefits. Vercel also announced hosted availability on October 30. ([huggingface.co](https://huggingface.co/inclusionAI/Ling-3.1-flash-1019/commits/main))

InclusionAI **developer-reports** improvements over the predecessor on agentic and scientific benchmarks; its comparative claims remain self-reported in the model card. ([huggingface.co](https://huggingface.co/inclusionAI/Ling-3.1-flash-1019))

## Links

- [Weights and model card](https://huggingface.co/inclusionAI/Ling-3.1-flash-1019) (primary)
- [Repository history](https://huggingface.co/inclusionAI/Ling-3.1-flash-1019/commits/main) (primary)
- [Artificial Analysis evaluation](https://artificialanalysis.ai/models/ling-3-1-flash-1019/) (third-party measurement)
- [Vercel hosted availability](https://vercel.com/changelog/ling-3-1-flash-1019-now-available-on-ai-gateway-for-free) (third-party deployment)

## Assessment

- **Technical novelty:** meaningful — the checkpoint combines KDA and gated MLA in a hybrid MoE, although that architecture is shared with its predecessor.
- **Practical significance:** medium — inference engineers should try it when evaluating long-context hybrid serving and MTP decoding.
- **Confidence:** high — the weights, repository history, independent capability evaluation, and hosted availability were checked; comparative post-training gains and serving advantages remain insufficiently verified.

## GitHub signal

**Ideas worth investigating:**

- Hybrid KDA and gated MLA state management across long contexts.
- MTP speculative decoding with SGLang’s `NEXTN` algorithm.
