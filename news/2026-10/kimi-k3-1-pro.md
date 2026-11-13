# Kimi K3.1 Pro

**Rank:** 1  
**Release date:** 2026-10-24  
**Area:** Model Releases  
**Primary source:** Moonshot AI  
**Availability:** Public weights on Hugging Face under the Kimi K3.1 Pro License; review its commercial conditions. The model also launched through Kimi’s products and API. ([huggingface.co](https://huggingface.co/moonshotai/Kimi-K3.1-Pro))

## What Changed

Compared with Kimi K3, K3.1 Pro retains 69 Kimi Delta Attention layers and 24 latent-attention layers, but adds a sparse indexer to each latent-attention layer. The indexer scores the history and selects up to 2,048 tokens per query for attention. Routed experts remain in MXFP4. Moonshot also describes K3.1 Pro as post-trained from K3 using large-scale joint reinforcement learning. ([vllm-project.github.io](https://vllm-project.github.io/2026/11/04/kimi-k31-pro.html))

## Why It Matters

The design reduces the amount of latent-cache data read during long-context decoding, while still scanning index keys across the history. It is a useful serving design to study, though the released checkpoint requires substantial accelerator capacity. ([vllm-project.github.io](https://vllm-project.github.io/2026/11/04/kimi-k31-pro.html))

## Evidence

**Kind:** Third-party serving implementation and measurement  
**Independently validated:** yes

Inferact and the vLLM team published a serving implementation and their own performance measurements. They report, for example, faster decode with their specialized sparse-attention path on eight GB300 GPUs. These are **developer-reported serving results**, not independent validation of Moonshot’s capability benchmarks. ([vllm-project.github.io](https://vllm-project.github.io/2026/11/04/kimi-k31-pro.html))

## Links

- [Model card and weights](https://huggingface.co/moonshotai/Kimi-K3.1-Pro) (weights)
- [Moonshot launch announcement](https://www.kimi.com/news/kimi-k3-1-pro) (announcement)
- [vLLM serving implementation and measurements](https://vllm-project.github.io/2026/11/04/kimi-k31-pro.html) (implementation and benchmark)

## Assessment

- **Technical novelty:** meaningful — sparse indexing is added to the existing hybrid attention architecture rather than replacing it.
- **Practical significance:** high — engineers operating large-scale inference should investigate the sparse-attention and cache design.
- **Confidence:** medium — the model card and third-party serving account were checked; broad capability claims remain primarily self-reported.
