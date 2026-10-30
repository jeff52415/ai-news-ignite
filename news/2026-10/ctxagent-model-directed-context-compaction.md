# CTXAgent: model-directed context compaction

**Rank:** 5  
**Release date:** 2026-10-25  
**Area:** Agentic AI & Harnesses  
**Primary source:** CTXAgent paper  
**Availability:** Public paper, repository, benchmark and result rows; the local agent requires Python and a model API key. ([arxiv.org](https://arxiv.org/abs/2610.34425))

## What Changed

Rather than relying only on threshold-triggered summarization, CTXAgent gives the model tools to decide when and what to compact. `compact_context` replaces earlier work with a model-written handoff; `curate_context` replaces selected tool outputs with short notes. Originals are archived for recall. Automatic context-management tiers remain as a safety net. ([github.com](https://github.com/MatthiasHBusch/CTXAgent))

## Why It Matters

The approach lets a model compact at task boundaries and retain information it expects to need. The accompanying benchmark provides a way to test whether that policy preserves task performance, facts and standing instructions while accounting for prompt-cache costs. Savings are not guaranteed: frequent compaction can increase other costs. ([arxiv.org](https://arxiv.org/abs/2610.34425))

## Evidence

**Kind:** Public implementation and author-reported benchmark  
**Independently validated:** no

Busch and coauthors measured seven models on mixed sessions of 35–212 turns. In their harness comparison, they reported that CTXAgent with Claude Opus 5.5 matched Claude Code’s task success at 34% lower cost than its explicit 200k-window configuration and 49% lower cost than its default. These are developer-reported, model- and configuration-dependent results, not an independent reproduction. ([arxiv.org](https://arxiv.org/abs/2610.34425))

## Links

- [CTXAgent paper](https://arxiv.org/abs/2610.34425) (primary)
- [CTXAgent repository](https://github.com/MatthiasHBusch/CTXAgent) (repository)

## Assessment

- **Technical novelty:** meaningful — combines model-directed handoffs and selective curation with recoverable archived content and automatic safeguards.
- **Practical significance:** medium — harness engineers should test it on long-running tasks with their own models, cache pricing and retention checks.
- **Confidence:** medium — the paper, repository and independent coverage were checked; effectiveness and cost claims remain author-reported. ([arxiv.org](https://arxiv.org/abs/2610.34425))

## GitHub signal

**Ideas worth investigating:**

- Model-written handoffs with selective retention.
- Tool-result curation and archived-content recall.
- Cache-stable safety tiers and compaction evaluation.
