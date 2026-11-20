# Harness-specific LoRA adapters

**Rank:** 5  
**Release date:** 2026-11-06  
**Area:** Algorithms & Architectures  
**Primary source:** Hugging Face Harness Hub  
**Availability:** Public recipe, supporting code, and adapter checkpoints.

## What Changed

Rather than relying on one base model to behave equally well across agent harnesses, the recipe trains a separate LoRA adapter for each model–harness pair using reinforcement learning on verifiable tasks. Training runs inside unmodified harnesses.

A `safeagents` reverse proxy sits between the harness and model server. It inspects proposed tool calls before the harness executes them, blocks rule-detected shortcuts, and replaces blocked calls with a notice. Any rollout containing such a notice receives zero reward; the attempted tokens remain in training so GRPO can penalize them. Correct rollouts also receive a small tool-efficiency bonus. ([huggingface.co](https://huggingface.co/blog/harness-hub/harness-adapters))

## Why It Matters

Engineers can adapt a shared base model to a harness’s particular tools and control flow without modifying the harness. The proxy provides a concrete place to block known evaluator shortcuts, but its rules do not guarantee coverage of all reward hacking. Teams should test both missed attacks and false positives in their own environments. ([huggingface.co](https://huggingface.co/blog/harness-hub/harness-adapters))

## Evidence

**Kind:** Primary release and public implementation  
**Independently validated:** no

The Harness Hub authors report that smoke-test adapters used fewer tool calls on held-out tasks while maintaining or improving accuracy. These comparisons are **developer-reported**. The public Hermes adapter card includes serving instructions and evaluation trajectories. Independent reproduction was not identified in this check. ([huggingface.co](https://huggingface.co/blog/harness-hub/harness-adapters))

## Links

- [Technical write-up](https://huggingface.co/blog/harness-hub/harness-adapters) (primary)
- [Hermes adapter](https://huggingface.co/harness-hub/Qwen3.8-27B-hermes-adapted) (weights)
- [safeagents](https://github.com/huggingface/safeagents) (implementation)
- [Repo2RLEnv](https://github.com/huggingface/Repo2RLEnv) (implementation)

## Assessment

- **Technical novelty:** meaningful — harness-specific LoRA training is combined with tool-call interception and a penalty for detected shortcuts.
- **Practical significance:** high — agent-training teams should try the recipe when adapting a base model to a specific harness.
- **Confidence:** medium — the recipe, code, and checkpoint were checked; performance and guard effectiveness remain developer-reported.

## GitHub signal

**Ideas worth investigating:**

- Inspect tool calls with rule-based detectors before execution, while preserving attempted tokens for the RL update.
- Generate verifiable training environments from repository and agent-session material.
