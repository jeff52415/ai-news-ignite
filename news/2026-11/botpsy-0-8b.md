# BotPsy-0.8B

**Rank:** 8  
**Release date:** 2026-11-11  
**Area:** Model Releases  
**Primary source:** QVAC model card  
**Availability:** Apache 2.0 weights on Hugging Face: BF16 safetensors and BF16, Q8_0, and Q4_K_M GGUF files. ([huggingface.co](https://huggingface.co/qvac/BotPsy-0.8B))

## What Changed

BotPsy post-trains Qwen3.5-0.8B for text-based tool use rather than introducing a new architecture. Supervised fine-tuning on tool-use trajectories is followed by on-policy distillation: the student generates responses and receives token-level feedback from a routed specialist teacher. Two reinforcement-learning rounds then use rule- and verifier-based rewards. ([huggingface.co](https://huggingface.co/blog/qvac/botpsy))

## Why It Matters

The checkpoint gives engineers a small local baseline for testing tool selection, argument generation and multi-step recovery. The model card recommends enabling thinking mode, which is **off by default** in the chat template. Evaluate it against application-specific tasks before allowing consequential actions. ([huggingface.co](https://huggingface.co/qvac/BotPsy-0.8B))

## Evidence

**Kind:** Public weights and developer-reported benchmarks  
**Independently validated:** no

QVAC reports BFCL v4 accuracy of 44.0 for BotPsy versus 23.4 for its base model. These are developer-reported results, not an independent reproduction. The weights and training outline are public, but the training code and data are not included. ([tether.io](https://tether.io/news/tethers-800m-ai-agent-beats-models-2-5x-its-size-on-everyday-phone-tasks/?utm_source=openai))

## Links

- [Model card and BF16 weights](https://huggingface.co/qvac/BotPsy-0.8B) (weights)
- [GGUF weights](https://huggingface.co/qvac/BotPsy-0.8B-GGUFs) (weights)
- [Training methodology and evaluation](https://huggingface.co/blog/qvac/botpsy) (primary)
- [Independent release coverage](https://modelsatwork.news/article/tether-botpsy-0-8b-open-tool-calling-model-on-device-apache-2) (secondary)

## Assessment

- **Technical novelty:** meaningful — combines trajectory imitation, specialist-teacher on-policy distillation and verifier-rewarded reinforcement learning.
- **Practical significance:** medium — engineers building local agents should test it against their own tools, failure cases and hardware constraints.
- **Confidence:** medium — the public artifacts and methodology were checked; performance and training claims remain developer-reported.
