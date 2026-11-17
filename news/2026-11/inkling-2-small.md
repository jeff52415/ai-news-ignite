# Inkling 2 Small

**Rank:** 3  
**Release date:** 2026-11-05  
**Area:** Model Releases  
**Primary source:** Thinking Machines Lab  
**Availability:** Hosted inference and fine-tuning APIs; Apache 2.0 weights downloadable from Hugging Face since November 12, 2026. ([thinkingmachines.ai](https://thinkingmachines.ai/news/inkling-2-small/?utm_source=openai))

## What Changed

Inkling 2 Small is a text-and-image-input mixture-of-experts model with 594B total parameters and 17B active per token. Its main post-training run jointly mixed coding, reasoning, vision, tool-use and safety tasks. The previous Inkling release instead combined separate reasoning and agentic RL runs through multi-teacher distillation. ([thinkingmachines.ai](https://thinkingmachines.ai/news/inkling-2-small/?utm_source=openai))

The joint run used task-specific rewards: unit tests for coding, rubric-based LLM judges for documents and tool use, reference answers for STEM and vision, and screenshot comparisons for web apps. Its asynchronous RL used a score-centering variant of StableReinforce; effort conditioning and a length penalty trained a speed–thoroughness tradeoff. ([thinkingmachines.ai](https://thinkingmachines.ai/news/inkling-2-small/))

## Why It Matters

The release gives engineers a checkpoint to serve or post-train and a concrete design for mixing heterogeneous agentic tasks in one RL run. The 17B active count is not the model’s total weight footprint, so self-hosting still requires substantial memory. ([huggingface.co](https://huggingface.co/thinkingmachines/Inkling-2-Small?utm_source=openai))

## Evidence

**Kind:** Public weights, developer training report and third-party benchmark  
**Independently validated:** yes

Plotly tested the model through a hosted endpoint on its data-analytics benchmark, reporting 39 correct answers out of 43 in one run. This independently measures a specific use case; it does not reproduce the training process. Thinking Machines’ training details and comparative benchmark results remain developer-reported. ([plotly.com](https://plotly.com/blog/inkling-2-small-plotly-data-analytics-bench/))

## Links

- [Announcement and training write-up](https://thinkingmachines.ai/news/inkling-2-small/) (primary)
- [Model card and weights](https://huggingface.co/thinkingmachines/Inkling-2-Small) (weights)
- [Plotly data-analytics benchmark](https://plotly.com/blog/inkling-2-small-plotly-data-analytics-bench/) (third-party measurement)

## Assessment

- **Technical novelty:** meaningful — a single asynchronous RL run combines distinct task families and graders instead of distilling separately trained specialists.
- **Practical significance:** high — engineers building multimodal agents or post-training pipelines should evaluate the checkpoint and reward-design choices.
- **Confidence:** high — the weights and a third-party measurement were checked; the training recipe and its claimed effects remain self-reported.
