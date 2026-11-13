# REINFORCE Zero: asynchronous RL with aligned kernels

**Rank:** 4  
**Release date:** 2026-11-06  
**Area:** Algorithms & Architectures  
**Primary source:** vLLM Project  
**Availability:** Public technical post, paper, alignment skill, and Molt training framework. Molt’s README says the aligned kernels are being upstreamed from a reference branch; its main branch includes mismatch metrics, rollout replay, and the skill. ([github.com](https://github.com/vllm-project/vllm-project.github.io/blob/main/_posts/2026-11-06-zero-mismatch-async-rl.md))

## What Changed

REINFORCE Zero separates two sources of rollout-to-learner probability mismatch: **stale weights** and **different numerical execution at identical weights**. It aligns rollout and learner kernels to produce matching token log-probabilities for the same weights and history, then applies unclipped token-level importance ratios to the remaining policy lag.

The update uses a group-mean reward baseline and averages tokens within each response, without a value model or sample-rejection gates. This contrasts with approaches that use clipping or gates to manage off-policy mismatch. ([github.com](https://github.com/vllm-project/vllm-project.github.io/blob/main/_posts/2026-11-06-zero-mismatch-async-rl.md))

## Why It Matters

The separation lets engineers evaluate asynchronous rollout overlap without treating same-weight numerical drift as policy staleness. It may also reduce discarded samples and simplify the loss, though alignment has its own execution cost and does not guarantee stability for every workload. ([github.com](https://github.com/vllm-project/vllm-project.github.io/blob/main/_posts/2026-11-06-zero-mismatch-async-rl.md))

## Evidence

**Kind:** Public implementation and developer-reported experiments  
**Independently validated:** no

Jian Hu and coauthors report stable reasoning runs through 20,000 updates at nominal lags of 2 and 8. On 16 GPUs over 12,000 updates, they report 2.40× the training-step throughput of synchronous training with aligned kernels, at comparable quality. On a separate OSWorld workload, their aligned setup had a 6.8% longer mean step than a standard-kernel, sequence-gated baseline. These are developer-reported results, not independent reproductions. ([github.com](https://github.com/vllm-project/vllm-project.github.io/blob/main/_posts/2026-11-06-zero-mismatch-async-rl.md))

## Links

- [vLLM technical post](https://github.com/vllm-project/vllm-project.github.io/blob/main/_posts/2026-11-06-zero-mismatch-async-rl.md) (primary)
- [REINFORCE Zero paper and alignment skill](https://github.com/hijkzzz/REINFORCE-Zero) (research repository)
- [Molt training framework](https://github.com/NVIDIA-NeMo/labs-molt) (implementation)

## Assessment

- **Technical novelty:** meaningful — combines same-weight numerical alignment with unclipped token-level importance sampling in asynchronous REINFORCE.
- **Practical significance:** high — teams building asynchronous LLM RL should test the recipe against their own throughput, stability, and alignment overhead.
- **Confidence:** medium — the post, paper, and public framework were checked; performance and stability remain author-reported.

## GitHub signal

**Ideas worth investigating:**

- Use the alignment skill’s per-operator checks and rollout replay to diagnose mismatched token log-probabilities.
- Record rollout token log-probabilities and apply unclipped learner-to-rollout ratios with a group-mean reward baseline. ([github.com](https://github.com/hijkzzz/REINFORCE-Zero))
