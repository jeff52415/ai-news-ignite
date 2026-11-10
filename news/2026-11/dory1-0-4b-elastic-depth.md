# Dory1.0-4B elastic-depth technical report

**Rank:** 6  
**Release date:** 2026-11-02  
**Area:** Algorithms & Architectures  
**Primary source:** NVIDIA technical report  
**Availability:** Public BF16 and quantized checkpoints under the OpenMDW 1.1 model license. ([arxiv.org](https://arxiv.org/abs/2611.03998))

## What Changed

Dory applies a shared recurrent transformer block a configurable number of times between input and output blocks. One checkpoint can therefore trade compute per token for depth without retraining or swapping models.

Optional **last-loop KV caching** replaces separate caches for each recurrent pass with one cache per recurrent attention layer. Previously processed tokens contribute final-loop keys and values; tokens in the current forward step use current-loop entries. This keeps the attention KV footprint at its one-loop size, but changes what earlier-loop queries attend to compared with per-loop caching.

During RLVR post-training, a difficulty-aware curriculum preferentially assigns harder prompts to deeper-loop rollout workers. This is a training policy, not an automatic inference-time router. ([arxiv.org](https://arxiv.org/html/2611.03998))

## Why It Matters

Serving engineers can test loop count and cache policy independently on their workloads. Deeper loops add compute per generated token; fewer generated tokens may offset some of that cost, but do not by themselves establish lower end-to-end latency. Last-loop caching offers a memory tradeoff that should be evaluated for quality as well as throughput. ([arxiv.org](https://arxiv.org/html/2611.03998))

## Evidence

**Kind:** Primary report, public checkpoint and serving implementation  
**Independently validated:** no

NVIDIA’s **developer-reported** evaluations found that four loops generated 1.3–2.5× fewer output tokens per attempt than one loop across four agentic benchmarks. Its four-loop cache comparison found score changes from −2.12 to +0.42 points when replacing per-loop with last-loop caching. These are not independent reproductions. ([arxiv.org](https://arxiv.org/html/2611.03998))

The vLLM Dory implementation, including last-loop cache support, was merged into its main branch on October 25, 2026. Integration is not validation of the benchmark claims. ([github.com](https://github.com/vllm-project/vllm/pull/60149))

## Links

- [Technical report](https://arxiv.org/abs/2611.03998) (primary)
- [BF16 checkpoint](https://huggingface.co/nvidia/NVIDIA-Nemotron-Labs-Dory1.0-4B-BF16) (weights)
- [vLLM Dory implementation](https://github.com/vllm-project/vllm/pull/60149) (repository)

## Assessment

- **Technical novelty:** meaningful — shared recurrent depth is combined with a difficulty-aware training curriculum and an optional single-cache serving policy.
- **Practical significance:** medium — engineers investigating small-model serving should test quality, latency and memory across loop counts and cache modes.
- **Confidence:** medium — the report, checkpoint and merged serving implementation were checked; the performance comparisons remain developer-reported.

## GitHub signal

**Ideas worth investigating:**

- Configurable recurrent loop count in the serving implementation.
- Last-loop cache overwrites versus separate per-loop KV caches.
