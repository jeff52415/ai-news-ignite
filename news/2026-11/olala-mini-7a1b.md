# Olala mini 7A1B

**Rank:** 3  
**Release date:** 2026-11-19  
**Area:** Model Releases  
**Primary source:** OVHcloud model card  
**Availability:** Apache 2.0 checkpoints, hosted API, and runtime forks. ([huggingface.co](https://huggingface.co/OVHaiLLM/Olala-v1.0-mini-7A1B))

## What Changed

Instead of using attention in every layer, Olala combines 29 Mamba-3 recurrent layers with seven attention layers. Each of its 36 layers is followed by a mixture-of-experts block; only the attention layers maintain a KV cache. The model has 6.8 billion total parameters and approximately one billion active per token. Base, supervised-fine-tuned, and final post-trained checkpoints allow comparisons across training stages. ([huggingface.co](https://huggingface.co/OVHaiLLM/Olala-v1.0-mini-7A1B))

## Why It Matters

The architecture lets engineers test the quality and serving tradeoffs of recurrent state plus a smaller attention KV cache. OVHcloud recommends float32 Mamba state in its vLLM fork: it reports that the default bf16 state can produce repetition loops during long generations. The model can still repeat, so generation limits and task-specific testing remain important. ([huggingface.co](https://huggingface.co/OVHaiLLM/Olala-v1.0-mini-7A1B))

## Evidence

**Kind:** Primary release and developer evaluation  
**Independently validated:** no

OVHai LLM published the weights, implementation and evaluation methodology. In its own evaluation, the final checkpoint scored **59.6% on BFCL V3**; this is developer-reported, not an independent measurement. The model card dates the release November 19; OVHcloud’s endpoint catalog lists November 18, so the dates differ. ([huggingface.co](https://huggingface.co/OVHaiLLM/Olala-v1.0-mini-7A1B))

## Links

- [Model card and weights](https://huggingface.co/OVHaiLLM/Olala-v1.0-mini-7A1B) (weights)
- [GGUF files and quantization guidance](https://huggingface.co/OVHaiLLM/Olala-v1.0-mini-7A1B-GGUF) (weights)
- [OVHcloud AI endpoint](https://www.ovhcloud.com/en/public-cloud/ai-endpoints/catalog/olala-v1-0-mini-7a1b/) (hosted API)
- [vLLM fork](https://github.com/OVHai-LLM/vllm) (runtime)

## Assessment

- **Technical novelty:** meaningful — Mamba-3, sparse attention and MoE are combined in a deployable small model.
- **Practical significance:** high — engineers evaluating compact tool-using models or hybrid inference should try it, accounting for forked-runtime requirements.
- **Confidence:** medium — the model card, endpoint and public artifacts were checked; benchmark and runtime-quality claims remain developer-reported.

## GitHub signal

**Ideas worth investigating:**

- Compare recurrent-state precision and long-generation repetition in the vLLM fork.
- Measure KV-cache and recurrent-state memory against an attention-only baseline.
- Compare base, SFT and post-trained checkpoints on the same tool-use workload.
