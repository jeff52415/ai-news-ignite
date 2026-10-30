# Native PyTorch inference backends for TPU

**Rank:** 3  
**Release date:** 2026-10-20  
**Area:** Inference & Infrastructure  
**Primary source:** Google Developers Blog  
**Availability:** Open-source backends; install vLLM-TorchTPU on a Cloud TPU VM or use the SGLang-TorchTPU repository’s installation instructions.

## What Changed

The new backends run PyTorch model definitions on TorchTPU instead of using the existing JAX-based TPU backends. They retain the engines’ scheduler, worker model, KV-cache manager and API server while calling TPU-specific Pallas kernels as PyTorch custom operators inside compiled graphs. ([developers.googleblog.com](https://developers.googleblog.com/announcing-new-vllm-and-sglang-inference-engines-on-tpu/))

TPU Sync reads the device buffers behind PyTorch tensors without an extra host staging copy and transfers data on threads outside Python. It connects to vLLM through its KV connector interface and to SGLang through its disaggregation and HiCache backends. ([developers.googleblog.com](https://developers.googleblog.com/announcing-new-vllm-and-sglang-inference-engines-on-tpu/))

## Why It Matters

Teams already using these serving engines can evaluate TPU deployment without rewriting most model definitions. Direct KV transfers and tiered offload provide paths to test disaggregated prefill/decode and prefix reuse, though their benefits depend on workload and transfer overhead.

## Evidence

**Kind:** Primary release and public implementation  
**Independently validated:** no

Google and the project developers published the technical description and open repositories. Google reports a Qwen 3.5 result on Ironwood of **2.01 cents per million tokens** at high concurrency; this is developer-reported, not an independent reproduction. Google also reports production use, including a customer statement, but no independent verification was established in this check. ([developers.googleblog.com](https://developers.googleblog.com/en/announcing-new-vllm-and-sglang-inference-engines-on-tpu/?utm_source=openai))

## Links

- [Google Developers Blog: New vLLM and SGLang inference engines on TPU](https://developers.googleblog.com/announcing-new-vllm-and-sglang-inference-engines-on-tpu/) (primary)
- [Introducing vLLM TorchTPU](https://vllm.ai/blog/2026-10-20-vllm-torchtpu) (developer technical description)
- [vLLM-TorchTPU](https://github.com/vllm-project/vllm-torchtpu) (repository)
- [SGLang-TorchTPU](https://github.com/sgl-project/sglang-torchtpu) (repository)

## Assessment

- **Technical novelty:** meaningful — TPU operators and direct KV-buffer transfers are integrated beneath established PyTorch serving engines.
- **Practical significance:** high — TPU serving teams should test the backends against their own models, cache-hit patterns and latency targets.
- **Confidence:** medium — the primary description and public implementations were checked; performance and production claims remain self-reported.

## GitHub signal

**Ideas worth investigating:**

- Registering Pallas attention and mixture-of-experts kernels as PyTorch operators.
- Transferring KV buffers through vLLM’s connector interface, including resharding between prefill and decode layouts. ([vllm.ai](https://vllm.ai/blog/2026-10-20-vllm-torchtpu))
- Using TPU Sync as SGLang’s disaggregation and HiCache I/O backend.
