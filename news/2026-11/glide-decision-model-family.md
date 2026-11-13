# GLiDE decision-model family

**Rank:** 9  
**Release date:** 2026-11-05  
**Area:** Model Releases  
**Primary source:** Fastino  
**Availability:** Downloadable weights under the Fastino Community License; GLiDE 27B is also available through Fastino’s API. ([fastino.ai](https://fastino.ai/blog/glide-decision-model-family))

## What Changed

GLiDE scores supplied options in a forward pass and returns probabilities rather than generating answer or reasoning tokens. The family has five sizes, from 0.4B to 27B. Unlike the smaller shipped variants, both 9B and 27B repeat middle layers with shared weights, adding fixed computation without adding parameters. In 27B, two middle-layer bands each run twice. ([fastino.ai](https://fastino.ai/blog/glide-decision-model-family))

## Why It Matters

The interface is suited to bounded decisions such as routing and tool selection, where engineers can apply thresholds to option probabilities rather than parse generated text. Recurrent depth offers a quality–latency trade-off without expanding the weights; teams should test calibration and routing errors on their own traffic. ([fastino.ai](https://fastino.ai/blog/glide-decision-model-family))

## Evidence

**Kind:** Public weights, developer ablation, and third-party implementation  
**Independently validated:** yes, for implementation behavior; not for the loop ablation

Fastino reports that, on its 27B loop ablation, the public-suite score rose from 72.1 to 72.5 while median latency increased from 83 to 112 ms. These are **developer-reported** measurements. ([fastino.ai](https://fastino.ai/blog/glide-decision-model-family?utm_source=openai))

Separately, NetProjects ported GLiDE 27B to Apple’s MLX framework and compared its quantized implementation with Fastino’s PyTorch implementation. Its 8-bit build matched the original’s top answer on 203 of 204 questions. That comparison does not independently establish the benefit of looping. ([netprojects.com](https://netprojects.com/insights/fastino-glide-decision-model-on-apple-silicon-mlx))

## Links

- [Technical release](https://fastino.ai/blog/glide-decision-model-family) (primary)
- [Model collection](https://huggingface.co/collections/fastino/glide) (weights)
- [NetProjects MLX implementation and measurements](https://netprojects.com/insights/fastino-glide-decision-model-on-apple-silicon-mlx) (third-party implementation)

## Assessment

- **Technical novelty:** meaningful — repeated shared-weight layers add latent computation within a non-generative decision model.
- **Practical significance:** medium — engineers building bounded routing or tool-selection pipelines should test it against their existing classifiers.
- **Confidence:** medium — the release and an independent implementation were checked, but the claimed loop-ablation benefit remains developer-reported.
