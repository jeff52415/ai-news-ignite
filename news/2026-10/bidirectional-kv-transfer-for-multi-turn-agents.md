# Bidirectional KV transfer for multi-turn agents

**Rank:** 2  
**Release date:** 2026-10-12  
**Area:** Inference & Infrastructure  
**Primary source:** vLLM blog  
**Availability:** Public NIXL connector support, example proxy and reproduction instructions. The published reproduction applies a patch to return transfer metadata in streaming responses.

## What Changed

In disaggregated prefill/decode serving, KV blocks previously moved from prefill to decode. With bidirectional transfer enabled, decode retains eligible blocks after a turn; on the next turn, prefill can read them back using NIXL rather than recomputing that context.

A stateful proxy records decode’s block-location metadata by `conversation_id` and passes it to prefill. KV tensors move directly between nodes, not through the proxy. Prefill first checks its local prefix cache, then pulls remote blocks when the reusable remainder meets a configurable threshold; otherwise it recomputes. Retained decode blocks expire after a configurable lifetime. ([vllm.ai](https://vllm.ai/blog/2026-10-12-bidirectional-kvxfer-multiturn-agentic-workload))

## Why It Matters

Long agent conversations can repeatedly process growing histories when prefill nodes lack the relevant KV state. Remote reuse trades network transfer and decode-side cache memory for less prefill computation. Engineers should measure that tradeoff on their own model, interconnect and turn patterns.

The router must also guard against changed conversation prefixes: the documentation warns that stripping reasoning traces between turns can make reused KV correspond to incorrect token positions. ([docs.vllm.ai](https://docs.vllm.ai/en/stable/features/nixl_connector_usage/))

## Evidence

**Kind:** Public implementation and developer-reported benchmark  
**Independently validated:** no

AWS author Sunita Nadampalli reports up to **1.6× lower time to first token** for Qwen3-32B and **3.3×** for GLM-5-FP8 at the longest tested prompts, on an EFA-connected prefill/decode deployment. These are developer-reported results; prefill prefix caching was disabled to emulate an evicted-cache scenario. The example proxy and reproduction instructions are public. ([vllm.ai](https://vllm.ai/blog/2026-10-12-bidirectional-kvxfer-multiturn-agentic-workload))

## Links

- [Design and reproduction](https://vllm.ai/blog/2026-10-12-bidirectional-kvxfer-multiturn-agentic-workload) (primary)
- [Multi-turn proxy](https://github.com/vllm-project/vllm/blob/main/examples/disaggregated/disaggregated_serving/disagg_proxy_multiturn.py) (repository)
- [NIXL connector usage guide](https://docs.vllm.ai/en/stable/features/nixl_connector_usage/) (documentation)

## Assessment

- **Technical novelty:** meaningful — reverses the existing KV-read path across conversation turns, coordinated by retained blocks and proxy metadata.
- **Practical significance:** high — engineers serving long multi-turn workloads with disaggregated prefill and decode should test it against local recomputation.
- **Confidence:** medium — the design, proxy and documentation were checked; performance remains developer-reported, with no independent reproduction found.

## GitHub signal

**Ideas worth investigating:**

- Conversation-keyed, single-use transfer metadata in the proxy.
- Decode-block retention lifetime versus accelerator-memory pressure.
- Remote-read threshold tuning versus local recomputation.
