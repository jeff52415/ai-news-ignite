# Hy4 flash

**Rank:** 1  
**Release date:** 2026-11-16  
**Area:** Model Releases  
**Primary source:** Tencent model card  
**Availability:** Downloadable weights under the Tencent Hy License; also available through an API. The date is Tencent’s product release date, not a verified first weight-upload date. ([huggingface.co](https://huggingface.co/tencent/Hy4-flash))

## What Changed

Compared with Hy4, Hy4 flash interleaves sparse IndexPool attention with sliding-window attention, runs routed experts in a lower-dimensional latent space, and adds hashed bigram and trigram embeddings. Its built-in five-layer DFly2 speculative drafter shares the target’s KV cache and sparse-selection indices rather than maintaining a separate drafter cache. ([github.com](https://github.com/Tencent-Hunyuan/Hy4-flash))

## Why It Matters

Engineers can test a multimodal checkpoint and its serving recipes for long-context workloads. Cache and index sharing make the drafter an especially interesting candidate for measuring speculative-decoding latency and memory trade-offs; the benefit still needs measurement on the intended hardware and workload.

## Evidence

**Kind:** Independent application benchmark and developer-reported implementation  
**Independently validated:** yes

Plotly independently tested Hy4 flash on its data-analysis exam. That measures application performance, not DFly2’s efficiency. Tencent’s model card documents the architecture and deployment configurations; its efficiency claims remain developer-reported. ([plotly.com](https://plotly.com/blog/hy4-flash-plotly-data-analytics-bench/))

## Links

- [Model card and weights](https://huggingface.co/tencent/Hy4-flash) (weights)
- [Plotly data-analysis benchmark](https://plotly.com/blog/hy4-flash-plotly-data-analytics-bench/) (benchmark)
- [Hy4 flash repository](https://github.com/Tencent-Hunyuan/Hy4-flash) (implementation)
- [Tencent release announcement](https://www.tencent.com/tencent-launches-hy4-flash-to-power-high-speed-cost-efficient-ai-deployment-for-everyday-workflows/) (release date)

## Assessment

- **Technical novelty:** meaningful — the model combines latent-space experts and hybrid attention with a drafter that reuses target cache and sparse indices.
- **Practical significance:** high — serving engineers should test it where multimodal input, long context, and inference cost matter.
- **Confidence:** medium — the model card and Plotly’s independent benchmark were checked, but drafter efficiency remains self-reported.

## GitHub signal

**Ideas worth investigating:**

- Reuse target KV cache and sparse indices in speculative decoding.
- Interleave sparse and sliding-window attention.
- Route experts through a lower-dimensional latent space.
