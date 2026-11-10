# Clover-35B-A3B-Preview

**Rank:** 3  
**Release date:** 2026-10-30  
**Area:** Model Releases  
**Primary source:** DiffuSpace  
**Availability:** Apache-2.0 weights and a standalone Transformers inference implementation on Hugging Face; inference repository on GitHub.

## What Changed

Clover adapts the text-only Qwen3.6-35B-A3B hybrid Gated DeltaNet/full-attention MoE backbone for block diffusion rather than ordinary left-to-right generation. Prior context is compressed into recurrent Gated DeltaNet state; within the current block, tokens interact bidirectionally. The historical-state readout competes with block tokens in the same softmax, with learned calibration for block size. ([huggingface.co](https://huggingface.co/Diffuspace/Clover-35B-A3B-Preview))

The Hugging Face implementation starts each block masked and resolves sufficiently confident positions in parallel. If none meets the threshold, it fills the most confident position to ensure progress; the completed block then joins the causal prefix. ([huggingface.co](https://huggingface.co/Diffuspace/Clover-35B-A3B-Preview))

## Why It Matters

Engineers can test whether parallel block decoding improves end-to-end latency without sacrificing task success on their own coding and tool-use workloads. The model card warns that long generations can become repetitive and that numerical differences between backends can change outputs. ([huggingface.co](https://huggingface.co/Diffuspace/Clover-35B-A3B-Preview))

## Evidence

**Kind:** Primary release and public implementation  
**Independently validated:** no

DiffuSpace reports a **73.6 SWE-bench Verified score** and **680 tokens/s** on internal agent workloads, measured on one NVIDIA GB300 at BF16 and batch size one. These are developer-reported results, not an independent reproduction. The model card and repository document a public inference path. ([huggingface.co](https://huggingface.co/blog/Diffuspace/clover-35b-a3b-preview?utm_source=openai))

## Links

- [Technical release](https://huggingface.co/blog/Diffuspace/clover-35b-a3b-preview) (primary)
- [Model card and weights](https://huggingface.co/Diffuspace/Clover-35B-A3B-Preview) (weights)
- [Inference repository](https://github.com/DiffuSpace/Clover-35B-A3B-Preview) (repository)

## Assessment

- **Technical novelty:** meaningful — recurrent history and bidirectional block attention are combined through a shared softmax for diffusion decoding.
- **Practical significance:** high — engineers evaluating self-hosted coding agents should compare task success and end-to-end latency against autoregressive alternatives.
- **Confidence:** medium — the release, model card, and repository were checked; performance and speed remain developer-reported.

## GitHub signal

**Ideas worth investigating:**

- Confidence-threshold parallel unmasking with a fallback that guarantees progress.
- Recurrent historical memory combined with bidirectional intra-block attention.
- Block-level expert selection to limit the experts used during denoising. ([huggingface.co](https://huggingface.co/Diffuspace/Clover-35B-A3B-Preview))
