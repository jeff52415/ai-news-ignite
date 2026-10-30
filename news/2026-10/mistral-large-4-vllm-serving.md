# Mistral Large 4: sparse multimodal MoE and vLLM serving

**Rank:** 4  
**Release date:** 2026-10-29  
**Area:** Model Releases  
**Primary source:** vLLM and Mistral  
**Availability:** Downloadable FP8 and NVFP4 weights and a dedicated vLLM serving image. The Mistral Ecosystem Open-Weight License requires a separate commercial license for model-as-a-service businesses. ([vllm.ai](https://vllm.ai/blog/2026-10-29-mistral-large-4))

## What Changed

The October 29 release provides weights and serving support for a model first offered in public preview on October 6. Its MoE selects feed-forward experts per token, while a separate sparse-attention indexer selects which earlier positions each query attends to. Nine layers reuse another layer’s latent KV cache rather than writing their own. A Pixtral encoder handles image inputs; the embedded DSpark drafter proposes token blocks for verification by the target model. ([docs.mistral.ai](https://docs.mistral.ai/models/mistral-large-4-0?trk=public_post_comment-text&utm_source=openai))

The dedicated vLLM image supports context parallelism, disaggregated prefill and decode, and HiSparse host-memory KV offload. HiSparse retains a GPU working set and fetches selected KV rows from host memory on a miss. Some cross-layer KV and DSpark features are still being upstreamed. ([vllm.ai](https://vllm.ai/blog/2026-10-29-mistral-large-4))

## Why It Matters

Engineers can evaluate a self-hosted, multimodal long-context stack with distinct levers for KV capacity and decoding throughput. These levers have tradeoffs: vLLM reports that decode context parallelism can add per-token latency when KV capacity is not the bottleneck. ([vllm.ai](https://vllm.ai/blog/2026-10-29-mistral-large-4))

## Evidence

**Kind:** Primary release and public implementation  
**Independently validated:** no

The model card lists the weights, and vLLM documents the serving image and implementation. In **developer-reported** tests, the vLLM and Mistral team measured roughly 1.9–2.1× FP8 output throughput with DSpark at the same concurrency, using tensor parallelism across eight GPUs. These serving results have not been independently reproduced here. ([huggingface.co](https://huggingface.co/mistralai/Mistral-Large-4-1T-A52B))

## Links

- [vLLM serving guide](https://vllm.ai/blog/2026-10-29-mistral-large-4) (primary)
- [Model card and FP8 weights](https://huggingface.co/mistralai/Mistral-Large-4-1T-A52B) (weights)
- [Hugging Face architecture and inference overview](https://huggingface.co/blog/mistral-large4) (corroborating overview)

## Assessment

- **Technical novelty:** meaningful — sparse MLA, cross-layer KV reuse and an embedded drafter are combined in a model-specific serving implementation.
- **Practical significance:** high — teams with suitable accelerator capacity should test the serving configurations against their own long-context and multimodal workloads.
- **Confidence:** medium — the primary guide, model card and corroborating overview were checked; performance remains developer-reported.

## GitHub signal

**Ideas worth investigating:**

- Reuse sparse-indexer selections across layers and share latent KV across designated layers.
- Keep the full latent KV cache in host memory while fetching selected rows into a GPU working set.
- Use a parallel DSpark drafter with sliding-window MLA and target-model verification.
