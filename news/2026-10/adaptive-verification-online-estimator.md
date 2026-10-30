# Adaptive verification with an online acceptance estimator

**Rank:** 7
**Release date:** 2026-10-14 (dossier-reported; unverified)
**Area:** Inference & Infrastructure
**Primary source:** vLLM blog (unverified)
**Availability:** The dossier reports a public implementation and an
`enable_adaptive_verification` option; both require verification.

## What Changed

The dossier describes an online estimator that predicts draft-token
acceptance from the drafter's maximum-token log-odds. It reportedly fits
a logistic model with a shared slope and per-position intercepts, then
uses its predictions to trim draft sequences before target verification,
rather than using a fixed verification policy.

## Why It Matters

If confirmed, the approach could let engineers test adaptive verification
with existing draft models without training a separate confidence head.
The dossier also says that conditioning trimming on the sampled token's
probability can bias the output distribution.

## Evidence

**Kind:** Dossier-reported public implementation and developer benchmarks
**Independently validated:** no

The implementation, technical explanation, and benchmark results have not
been independently checked for this draft. Any benchmark results remain
developer-reported.

## Links

No links have been verified for inclusion.

## Assessment

- **Technical novelty:** meaningful — the reported mechanism calibrates
  acceptance online by draft position.
- **Practical significance:** medium — inference engineers using speculative
  decoding may want to investigate it after verifying availability.
- **Confidence:** low — the release date, implementation, mechanism, and
  benchmark evidence still need source verification.
