# LFM3-1.7B

**Rank:** 3  
**Release date:** 2026-10-27  
**Area:** Model Releases  
**Primary source:** Liquid AI  
**Availability:** Downloadable base and post-trained weights on Hugging Face under the LFM Open License v1.0. ([huggingface.co](https://huggingface.co/LiquidAI/LFM3-1.7B))

## What Changed

LFM3 extends LFM2’s convolution-and-attention hybrid by adding sliding-window attention. Its 24 layers comprise 13 gated short-convolution layers, five attention layers with a 256-token sliding window, and six global-attention layers. It also increases the convolution kernel from three to seven, gates attention outputs per head, and applies partial RoPE in global-attention layers. ([liquid.ai](https://www.liquid.ai/blog/lfm3))

The text model has 1.73B parameters and a 256K-token context covering input and output. The base checkpoint is intended for substantial adaptation; the post-trained checkpoint targets chat and tool use. ([huggingface.co](https://huggingface.co/LiquidAI/LFM3-1.7B))

## Why It Matters

The layer mix offers a small, downloadable model for testing local tool calling, structured output, and domain adaptation. Engineers should evaluate those tasks on their own workloads: Liquid cautions against using the model for agentic coding or complex multistep reasoning. ([huggingface.co](https://huggingface.co/LiquidAI/LFM3-1.7B))

## Evidence

**Kind:** Primary release and public model artifacts  
**Independently validated:** no

Liquid AI published the base and post-trained checkpoints and model cards. Its capability, memory, and inference-performance claims are developer-reported; no independent reproduction or measurement was identified for this section. A third-party model directory corroborates the release date and basic specifications, but is not an independent performance evaluation. ([liquid.ai](https://www.liquid.ai/blog/lfm3))

## Links

- [LFM3 announcement](https://www.liquid.ai/blog/lfm3) (primary)
- [Post-trained weights and model card](https://huggingface.co/LiquidAI/LFM3-1.7B) (weights)
- [Base weights and model card](https://huggingface.co/LiquidAI/LFM3-1.7B-Base) (weights)

## Assessment

- **Technical novelty:** meaningful — sliding-window attention adds a third sequence operator to an existing convolution-and-attention hybrid.
- **Practical significance:** medium — engineers building narrow local agents or specialized models should test the checkpoint against their own reliability and latency requirements.
- **Confidence:** medium — the release, architecture, and artifacts were checked, but performance and capability claims remain developer-reported.
