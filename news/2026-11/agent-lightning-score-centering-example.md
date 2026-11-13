# Agent Lightning score-centering example

**Rank:** 7  
**Release date:** 2026-11-03  
**Area:** Agentic AI & Harnesses  
**Primary source:** Microsoft Agent Lightning v1.0.3  
**Availability:** Public release and example source; the documented recipe requires a B200 GPU and a separately prepared quantized model.

## What Changed

The example adds a score-centering training path alongside a standard GRPO preset. At each generated position, it records the sampled token’s log probability and the top-K behavior-policy probabilities. The trainer scores those candidates under the current policy and applies a centering correction, approximating the unrecorded probability tail as proportional to the current policy.

Both presets use INT8 rollout weights and activations with an INT4 attention KV cache, while training uses BF16. Updated linear weights are requantized before synchronization to the rollout engine. ([microsoft.github.io](https://microsoft.github.io/agent-lightning/stable/85-example-score-centering/))

## Why It Matters

The recipe gives engineers a concrete way to investigate training stability when rollout and training precision differ. It also makes GRPO and score-centering runs possible under the same rollout-precision settings, although their objectives and loss reductions differ. ([microsoft.github.io](https://microsoft.github.io/agent-lightning/stable/85-example-score-centering/))

## Evidence

**Kind:** Public implementation and developer-reported training results  
**Independently validated:** no

Microsoft reports that both presets completed B200 smoke tests. In its reported math-training run, score-centering reward remained around 0.6 at later steps, while the GRPO baseline fell to zero around step 45. These are developer-reported training results, not an independent reproduction or evidence of improvement across other agent workloads. ([microsoft.github.io](https://microsoft.github.io/agent-lightning/stable/85-example-score-centering/))

## Links

- [Agent Lightning v1.0.3 release](https://github.com/microsoft/agent-lightning/releases/tag/v1.0.3) (release notes)
- [Score-centering example](https://microsoft.github.io/agent-lightning/stable/85-example-score-centering/) (documentation)
- [Implementation pull request](https://github.com/microsoft/agent-lightning/pull/651) (source)

## Assessment

- **Technical novelty:** meaningful — the implementation connects captured behavior-policy candidates to a tail-approximated centering correction in the training worker.
- **Practical significance:** medium — engineers studying low-precision RL rollouts can use the example as a starting point for controlled experiments.
- **Confidence:** medium — the release and documentation were checked; performance and smoke-test results remain developer-reported.

## GitHub signal

**Ideas worth investigating:**

- Capture top-K behavior probabilities separately from the sampled token’s log probability, without storing full-vocabulary rollout probabilities.
- Compare score-centering and GRPO under matched rollout precision, while accounting for their different objectives and reductions.
