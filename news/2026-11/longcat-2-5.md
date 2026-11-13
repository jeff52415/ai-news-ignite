# LongCat-2.5

**Rank:** 10  
**Release date:** 2026-11-02  
**Area:** Model Releases  
**Primary source:** LongCat API changelog  
**Availability:** Hosted API and public MIT-licensed weights on Hugging Face.

## What Changed

LongCat-2.5 is a multimodal mixture-of-experts model whose vision pipeline converts visual features into discrete tokens aligned with text, rather than relying solely on continuous visual embeddings. Its documented training also combines long-horizon agent reinforcement learning with learning from multiple teachers. The November 2 date is the documented API availability date.

## Why It Matters

Engineers can test both the released model and its training ideas on visual coding and multi-step agent tasks. Discrete visual tokens are also worth investigating as an approach to integrating visual and text representations.

## Evidence

**Kind:** Primary release and public model artifact  
**Independently validated:** no

LongCat’s changelog documents API availability, and its model card provides weights and benchmark results. Those benchmark results are **developer-reported**; an independent reproduction or third-party measurement was not established in this check.

## Links

- [API changelog](https://longcat.chat/platform/docs/ChangeLog.html) (release notes)
- [Model card and weights](https://huggingface.co/meituan-longcat/LongCat-2.5) (weights)
- [LongCat-2.5 overview](https://longcat.ai/blog/longcat-2.5) (developer overview)

## Assessment

- **Technical novelty:** meaningful — discrete visual tokens and agent-focused training combine established ideas in a multimodal MoE.
- **Practical significance:** medium — engineers working on visual coding or multi-step agents should evaluate it against their own tasks.
- **Confidence:** medium — availability and the public artifact were checked, but performance claims remain developer-reported.
