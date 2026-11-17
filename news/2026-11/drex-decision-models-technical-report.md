# Drex decision models: technical report

**Rank:** 5  
**Release date:** 2026-11-05  
**Area:** Algorithms & Architectures  
**Primary source:** Nace.AI, *Towards Foundation Decision Models: Drex*  
**Availability:** Public weights and runtime; check the license for each checkpoint.

## What Changed

Drex scores supplied options directly rather than generating an answer token by token. Its DLM, v1.5 and v2.0 models use a pointer head that compares a question’s decision state with each option’s hidden state. Drex Max instead uses a linear option-code readout and partially bidirectional attention; it processes each question separately, so it cannot reuse the state cache across questions. ([arxiv.org](https://arxiv.org/html/2611.07854))

Supervised training includes option-shuffling and consistency losses. For the pointer models, “reinforcement learning from adjusted feedback” directly optimizes soft targets formed from teacher distributions and verified outcomes; Max uses a different, KL-regularized variant. ([arxiv.org](https://arxiv.org/html/2611.07854))

## Why It Matters

The structured interface avoids answer parsing and exposes probabilities for classification, routing and judging. Engineers should test calibration and option-order sensitivity on their own data; Max’s per-question re-encoding may also matter for long contexts with many questions. ([arxiv.org](https://arxiv.org/html/2611.07854))

## Evidence

**Kind:** Public implementation, developer-reported ablations and third-party measurement  
**Independently validated:** yes

Nace.AI reports that its adjusted-feedback and consistency objectives improved performance and robustness; those training ablations remain developer-reported. Separately, Scale AI researcher Shreyas Subramanian evaluated Drex Max as an LLM judge across established benchmarks. That measurement supports its judging capability, but does not independently reproduce the training ablations. ([arxiv.org](https://arxiv.org/html/2611.07854))

## Links

- [Technical report](https://arxiv.org/abs/2611.07854) (primary)
- [Runtime and model documentation](https://github.com/nace-ai/drex-decision-models) (repository)
- [Model collection](https://huggingface.co/collections/nace-ai/drex) (weights)
- [Independent judging evaluation](https://arxiv.org/abs/2611.00505) (third-party measurement)

## Assessment

- **Technical novelty:** meaningful — direct option scoring is combined with adjusted soft targets and consistency regularization.
- **Practical significance:** high — engineers building routing, classification or judging pipelines should test the released checkpoints against task-specific baselines.
- **Confidence:** medium — the artifacts and an independent judging evaluation were checked; training-method ablations remain self-reported.

## GitHub signal

**Ideas worth investigating:**

- Pointer-based option scoring with cached state encoding.
- Permutation-consistency losses for option ordering.
- Direct optimization of verified, teacher-adjusted probability targets.
