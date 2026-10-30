# Agent Lightning v1.0: Reinforcement Learning Through Existing Harnesses

**Rank:** 3  
**Release date:** 2026-08-17  
**Area:** Agentic AI & Harnesses  
**Primary source:** Microsoft Research  
**Availability:** Public framework, documentation, and coding-agent training pipeline. The Microsoft Research blog was published on October 7, 2026, after the v1.0.0 release. ([github.com](https://github.com/microsoft/agent-lightning/releases/tag/v1.0.0))

## What Changed

Agent Lightning v1.0 was rebuilt around training with the deployment harness controlling tools, context, and execution, rather than reconstructing that loop inside the trainer. An OpenAI-compatible gateway proxies model calls and records token IDs and log probabilities against each rollout; a controller runs the agent locally or as a Kubernetes Job. ([raw.githubusercontent.com](https://raw.githubusercontent.com/microsoft/agent-lightning/main/docs/05-basics.md))

Because harnesses can retokenize or restructure context, one rollout can produce multiple training samples. The adapter merges calls only when their token histories are exactly continuous, computes advantages at rollout level, and supports rollout-level loss normalization. ([raw.githubusercontent.com](https://raw.githubusercontent.com/microsoft/agent-lightning/main/docs/05-basics.md))

## Why It Matters

Training against the harness intended for deployment reduces the need to maintain a separate approximation of its tool and context behavior. Rollout-level accounting also avoids giving extra weight solely to executions that split into more samples. ([microsoft.com](https://www.microsoft.com/en-us/research/blog/agent-lightning-v1-0-a-3500-line-lightweight-agentic-rl-framework-for-training-agents-with-real-harnesses/?lang=ja))

## Evidence

**Kind:** Open-source implementation and developer-reported benchmark  
**Independently validated:** no

Microsoft published the framework and a coding-agent training pipeline. Its developers report that RL improved Qwen3.5-9B pass@1 on SWE-bench Verified from 41.8% to 56.4%, using about 6,000 training examples. That result is developer-reported, not an independent reproduction. ([microsoft.com](https://www.microsoft.com/en-us/research/blog/agent-lightning-v1-0-a-3500-line-lightweight-agentic-rl-framework-for-training-agents-with-real-harnesses/?lang=ja))

## Links

- [Microsoft Research technical announcement](https://www.microsoft.com/en-us/research/blog/agent-lightning-v1-0-a-3500-line-lightweight-agentic-rl-framework-for-training-agents-with-real-harnesses/?lang=ja) (primary)
- [Agent Lightning repository](https://github.com/microsoft/agent-lightning) (repo)
- [Agent Lightning v1.0.0 release](https://github.com/microsoft/agent-lightning/releases/tag/v1.0.0) (release)
- [Architecture documentation](https://github.com/microsoft/agent-lightning/blob/main/docs/05-basics.md) (documentation)
- [Technical report](https://arxiv.org/abs/2608.17528) (paper)

## Assessment

- **Technical novelty:** meaningful — proxy-based capture connects a real harness to RL while the adapter handles fragmented token trajectories.
- **Practical significance:** high — engineers training tool-using agents should try it when deployment-harness fidelity matters.
- **Confidence:** medium — the release, architecture, and public pipeline were checked; the reported performance improvement remains developer-measured.

## GitHub signal

**Ideas worth investigating:**

- Capture token IDs and log probabilities through a rollout-specific API proxy.
- Merge model calls only when token histories are exactly continuous.
- Compute advantages and normalize loss at rollout level.
