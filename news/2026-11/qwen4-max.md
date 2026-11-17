# Qwen4-Max

**Rank:** 7  
**Release date:** 2026-11-16  
**Area:** Model Releases  
**Primary source:** Alibaba Cloud  
**Availability:** Hosted API on QwenCloud as `qwen4-max`; weights are not publicly available.

## What Changed

Qwen4-Max is a native-vision sparse mixture-of-experts model. Alibaba reports 2.4 trillion total parameters and 71 billion activated per token, compared with more active parameters at the same total scale in Qwen3.8-Max. It also reports changes to attention, residual connections and embeddings. ([alibabacloud.com](https://www.alibabacloud.com/en/press-room/alibaba-unveils-qwen4-max?_p_lc=1))

An earlier open-weight Qwen4 architecture preview, Qwen3.8-Flash-Next, describes a hybrid of Gated DeltaNet and block-indexed sparse attention, gated residual streams, and n-gram embeddings. These details explain the architecture lineage but are not an independent inspection of Max’s closed implementation. ([alibabacloud.com](https://www.alibabacloud.com/blog/qwen3-8-flash-next-a-new-architecture-towardsultimate-cost-efficiency_603501))

## Why It Matters

Engineers can evaluate a new hosted model for visual reasoning, long-context retrieval and tool use. The documented context window is 1 million tokens, but maximum input is lower: 983,616 tokens with thinking enabled. Closed weights prevent direct architecture-level testing or self-hosting. ([docs.qwencloud.com](https://docs.qwencloud.com/developer-guides/getting-started/latest-model))

## Evidence

**Kind:** Developer release and third-party measurement  
**Independently validated:** yes

Artificial Analysis has independently measured Qwen4-Max on its Intelligence Index and reported inference time and cost. That measurement does not validate Alibaba’s architectural claims. ([artificialanalysis.ai](https://artificialanalysis.ai/models/qwen4-max))

On Alibaba’s proprietary Work360 benchmark, **developer-reported** results say Qwen4-Max used 35% fewer tokens and reduced average task cost by approximately 60% versus Qwen3.8-Max at high reasoning effort. ([alibabacloud.com](https://www.alibabacloud.com/en/press-room/alibaba-unveils-qwen4-max?_p_lc=1))

## Links

- [Alibaba release announcement](https://www.alibabacloud.com/en/press-room/alibaba-unveils-qwen4-max) (primary)
- [QwenCloud model documentation](https://docs.qwencloud.com/developer-guides/getting-started/latest-model) (documentation)
- [Qwen3.8-Flash-Next architecture preview](https://www.alibabacloud.com/blog/qwen3-8-flash-next-a-new-architecture-towardsultimate-cost-efficiency_603501) (technical background)
- [Artificial Analysis model measurements](https://artificialanalysis.ai/models/qwen4-max) (independent evaluation)

## Assessment

- **Technical novelty:** meaningful — the reported design combines sparse expert activation with changes to attention, residual flow and embeddings.
- **Practical significance:** medium — engineers building multimodal or long-running agents should test it against their own accuracy, latency and cost requirements.
- **Confidence:** medium — the release and API documentation were checked, and a third party measured performance; Max’s internal architecture and Alibaba’s Work360 comparison remain developer-reported.
