# Inkling 2 Mini

**Rank:** 2  
**Release date:** 2026-11-20  
**Area:** Model Releases  
**Primary source:** Thinking Machines Lab  
**Availability:** Download Apache 2.0 mixed-precision weights from Hugging Face. The main model is also available for fine-tuning through Tinker; the variable-loop research model is open-weights only. ([huggingface.co](https://huggingface.co/thinkingmachines/Inkling-2-Mini?library=transformers&utm_source=openai))

## What Changed

Inkling 2 Mini is a multimodal, 26.4B-parameter mixture-of-experts model. Rather than traverse its 24 decoder layers once, it runs the middle 12 layers three times with shared weights. Depth-wise attention over block outputs lets layers read information from other blocks and loop passes, rather than relying on a single cumulative residual stream. ([thinkingmachines.ai](https://thinkingmachines.ai/news/inkling-2-mini/))

A separately trained research checkpoint permits one to five loop passes at inference. It was trained predominantly at three passes, so results at other depths do not isolate the effects of training specifically for those depths. ([huggingface.co](https://huggingface.co/thinkingmachines/TML-d24-varloop-research))

## Why It Matters

Weight reuse makes the research checkpoint useful for studying how additional inference computation affects capabilities and internal representations without changing the weights. Engineers can also test the serving implications of repeated layers. The main checkpoint itself has a fixed loop count.

## Evidence

**Kind:** Public weights, developer-reported benchmarks, and third-party interpretability analysis  
**Independently validated:** yes, for internal model analysis—not benchmark performance

Goodfire analyzed information flow across layers and loops using weights provided early by Thinking Machines. Thinking Machines’ benchmark results and efficiency claims remain developer-reported; Goodfire’s analysis is not a reproduction of those benchmarks. ([goodfire.com](https://www.goodfire.com/research/interpreting-inkling-2-mini/))

## Links

- [Inkling 2 Mini announcement](https://thinkingmachines.ai/news/inkling-2-mini/) (primary)
- [Inkling 2 Mini weights](https://huggingface.co/thinkingmachines/Inkling-2-Mini) (artifact)
- [Variable-loop research weights](https://huggingface.co/thinkingmachines/TML-d24-varloop-research) (artifact)
- [Goodfire interpretability analysis](https://www.goodfire.com/research/interpreting-inkling-2-mini/) (third-party research)

## Assessment

- **Technical novelty:** meaningful — shared middle-layer execution is combined with depth-wise attention across block outputs and a separately trained variable-loop checkpoint.
- **Practical significance:** high — researchers and serving engineers should try it for inference-depth and recurrent-computation experiments.
- **Confidence:** high for the released architecture and availability, supported by public artifacts and Goodfire’s measurements; benchmark and efficiency claims remain developer-reported.
