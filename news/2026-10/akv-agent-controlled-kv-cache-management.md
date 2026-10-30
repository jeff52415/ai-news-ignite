# AKV: agent-controlled KV-cache management

**Rank:** 1  
**Release date:** 2026-10-20  
**Area:** Algorithms & Architectures  
**Primary source:** *Cache Engineering for Agents*  
**Availability:** Public paper and source repository; install the agent and SGLang-based serving system from the repository.

## What Changed

Instead of trimming or summarizing the conversation and re-prefilling retained text, AKV preserves the logical conversation while controlling which KV entries participate in future attention. `drop` excludes selected entries; `repos` compacts retained positions by adjusting cached keys’ rotary position encodings without recomputing their hidden states.

Because retained states depend on *when* earlier entries were dropped or repositioned, matching token prefixes alone is insufficient for safe reuse. AKV extends its radix-tree cache to account for operation history and uses segment-batch attention to restore missing states. Retained entries can still encode information from dropped history, so dropping KV is not equivalent to deleting the corresponding text. ([arxiv.org](https://arxiv.org/html/2610.28577v1))

## Why It Matters

Agent builders can test cache policies as an alternative to text summarization, potentially reducing active-context costs and avoiding re-prefill. This requires a compatible serving engine and careful evaluation: a dropped tool result is no longer directly available to subsequent attention, even though it remains in the submitted conversation. ([github.com](https://github.com/thu-nics/AKV))

## Evidence

**Kind:** Open-source implementation, author benchmarks, and limited independent client-interface test  
**Independently validated:** yes — client behavior only

The paper’s developers report that their rolling tool-response drop policy reduced average estimated cost by **27.7%** and improved average benchmark scores by **1.7 points** versus threshold-triggered summarization. These are developer-reported results, not an independent performance reproduction. ([arxiv.org](https://arxiv.org/html/2610.28577v1))

Cairn Commons’ Observer Agent independently tested a pinned AKV client against a synthetic loopback server. It reported that requests retained the full message history while carrying cache-operation metadata, and that a changed processed prefix was rejected. The test did **not** exercise an inference server, KV restoration, model quality, latency, or cost. ([cairncommons.dev](https://cairncommons.dev/post/c5c16611-d386-4131-a7d5-c30ae7fc6539))

## Links

- [Cache Engineering for Agents](https://arxiv.org/abs/2610.28577) (primary paper)
- [AKV source repository](https://github.com/thu-nics/AKV) (repository)
- [AKV client-interface lifecycle test](https://cairncommons.dev/post/c5c16611-d386-4131-a7d5-c30ae7fc6539) (independent test)

## Assessment

- **Technical novelty:** meaningful — agent-directed drop and position adjustment are coupled with operation-history-aware cache reuse and restoration.
- **Practical significance:** high — teams serving long-running agents should test it against their existing summarization policies and workloads.
- **Confidence:** medium — the paper, implementation, and independent client test were checked; server behavior and performance gains remain unreproduced independently.

## GitHub signal

**Ideas worth investigating:**

- Selectively drop KV entries for older tool responses while retaining the conversation.
- Use operation-history-aware prefix reuse and segment-batch restoration.
- Separate policy triggers, entry selection, and repositioning decisions.
