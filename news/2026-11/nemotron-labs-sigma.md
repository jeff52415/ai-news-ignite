# Nemotron-Labs-Sigma

**Rank:** 6  
**Release date:** 2026-11-12  
**Area:** Model Releases  
**Primary source:** NVIDIA  
**Availability:** Downloadable base and instruct weights under the NVIDIA Nemotron Open Model License. The model card specifies a CUDA-capable NVIDIA GPU with bfloat16; CPU inference is unsupported. ([huggingface.co](https://huggingface.co/nvidia/Nemotron-Labs-Sigma-3B))

## What Changed

Rather than decode text one token at a time, Sigma iteratively denoises Gaussian noise in a learned 16-dimensional token-embedding space, then commits discrete tokens in parallel blocks. Its denoiser and embeddings are trained jointly, and committed prefix tokens are reused through a KV cache. The base models support configurable DDPM or DDIM sampling; separately distilled checkpoints are trained for fixed step counts. ([huggingface.co](https://huggingface.co/nvidia/Nemotron-Labs-Sigma-3B))

## Why It Matters

The weights let inference researchers test block-parallel generation, trajectory steering and few-step distillation. A separate self-speculative variant uses a diffusion head to draft tokens and a shared autoregressive backbone to verify them. Fewer denoising steps can reduce latency, but the base-model card warns of noticeable quality loss at low step counts. ([research.nvidia.com](https://research.nvidia.com/labs/genair/sigma/))

## Evidence

**Kind:** Primary release and developer evaluation  
**Independently validated:** no

NVIDIA published model cards, weights and inference code. Its researchers **developer-report** a 3.46× average throughput speedup for the 8B self-speculative model over its autoregressive decoding on a GB200. This is not an independently reproduced result. ([huggingface.co](https://huggingface.co/nvidia/Nemotron-Labs-Sigma-3B))

## Links

- [Sigma 3B model card](https://huggingface.co/nvidia/Nemotron-Labs-Sigma-3B) (weights and implementation)
- [Sigma 8B model card](https://huggingface.co/nvidia/Nemotron-Labs-Sigma-8B) (weights)
- [Sigma 3B instruct](https://huggingface.co/nvidia/Nemotron-Labs-Sigma-3B-instruct) (weights)
- [Sigma 8B instruct](https://huggingface.co/nvidia/Nemotron-Labs-Sigma-8B-instruct) (weights)
- [Sigma 8B self-speculative](https://huggingface.co/nvidia/Nemotron-Labs-Sigma-distill-spec-8B) (weights)
- [Research project](https://research.nvidia.com/labs/genair/sigma/) (technical overview)
- [Large Language Continuous Diffusion Models](https://arxiv.org/abs/2610.02665) (paper)

## Assessment

- **Technical novelty:** meaningful — continuous embedding-space diffusion enables blockwise denoising and trajectory steering instead of discrete token-by-token generation.
- **Practical significance:** high — inference researchers should test the checkpoints against autoregressive baselines on their own hardware and workloads.
- **Confidence:** medium — the model cards, public artifacts and paper were checked; performance claims remain developer-reported.
