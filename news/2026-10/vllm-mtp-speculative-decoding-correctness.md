# vLLM MTP speculative-decoding correctness investigation

**Rank:** 1  
**Release date:** 2026-10-23 (investigation update; original publication day not specified)  
**Area:** Inference & Infrastructure  
**Primary source:** RadianVector  
**Availability:** Public investigation and proposed source patch in the upstream issue.

## What Changed

RadianVector identified an accepted-token bookkeeping failure in vLLM’s older V1 model runner. With a hybrid recurrent model, MTP, async scheduling, prefix caching in `align` mode, and concurrent request churn, accepted-token counts can move with their batch rows and then be remapped a second time. A request may consequently resume from the wrong recurrent-state position, repeating or skipping tokens. ([radianvector.com](https://radianvector.com/research/vllm-mtp-speculative-decoding-bug/))

The proposed patch waits for the device-to-host count copy before rows move, then reads counts in their current row order instead of applying `prev_positions` again. This is a proposed V1 fix, not a change to the MTP algorithm. ([radianvector.com](https://radianvector.com/research/vllm-mtp-speculative-decoding-bug/))

## Why It Matters

Serving teams should compare speculative and non-speculative outputs under realistic concurrency and batch churn, rather than relying on single-request tests or throughput alone. RadianVector did not observe the problem with the tested default V2 runner; for its vLLM 0.28 tests, disabling async scheduling or prefix caching also removed the repeated-token symptom. ([radianvector.com](https://radianvector.com/research/vllm-mtp-speculative-decoding-bug/))

## Evidence

**Kind:** Independent runtime evidence and developer-reported patch tests  
**Independently validated:** yes, for a related accepted-count ownership failure; not for RadianVector’s specific patch

An earlier vLLM-Ascend report by QwertyJack documented corrupted output under batch churn and a related mutable-row ownership failure. Its proposed snapshot-and-remap fix differs from RadianVector’s wait-and-read-current-rows patch. ([github.com](https://github.com/vllm-project/vllm-ascend/issues/13863))

**Developer-reported:** In RadianVector’s vLLM 0.28 MTP-depth-1 test, repeated-token replies fell from 29 to zero among 385 replies after its patch. Eleven replies still differed from the no-speculation run; the authors attribute remaining near-tie divergences to ordinary batching variation rather than claiming byte-for-byte equality. ([radianvector.com](https://radianvector.com/research/vllm-mtp-speculative-decoding-bug/))

## Links

- [Correctness investigation](https://radianvector.com/research/vllm-mtp-speculative-decoding-bug/) (primary)
- [Upstream issue and patch discussion](https://github.com/vllm-project/vllm/issues/51571) (repository issue)
- [Earlier vLLM-Ascend reproduction](https://github.com/vllm-project/vllm-ascend/issues/13863) (repository issue)

## Assessment

- **Technical novelty:** meaningful — the investigation isolates a double row-mapping failure and proposes an ordering fix.
- **Practical significance:** high — engineers serving hybrid recurrent models with V1 and MTP should test their exact concurrent configuration.
- **Confidence:** medium — the investigation, patch, and related independent runtime report were checked; the patch’s effects remain RadianVector-reported.

## GitHub signal

**Ideas worth investigating:**

- Concurrent output-equivalence tests with request arrivals and completions.
- Synchronization and ownership of accepted-token counts across batch-row moves.
- Recurrent-state restoration after speculative token acceptance.
