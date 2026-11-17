# KServe 0.21: scale-to-zero and kernel-cache tooling

**Rank:** 2  
**Release date:** 2026-09-25  
**Area:** Inference & Infrastructure  
**Primary source:** KServe  
**Availability:** Open-source release and installation assets on GitHub.

## What Changed

`LLMInferenceService` can now configure KEDA directly through `spec.scaling.keda`; previously, KEDA scaling went through the Workload Variant Autoscaler (WVA). The controller creates a `ScaledObject` from user-defined triggers. Direct KEDA and WVA are mutually exclusive, and prefill and decode workloads must use the same scaling mode. Both paths accept `idleReplicaCount: 0`. CPU or memory triggers alone cannot scale to zero; an appropriate non-resource trigger is needed. ([kserve.github.io](https://kserve.github.io/website/blog/kserve-0.21-release))

The release also includes initial kernel-cache tooling: the MCV CLI and API build cache images, extract caches and run preflight checks. A verification framework and certificate-mode signature verification provide security components; this is initial tooling, not a claim of automatic cache deployment. ([kserve.github.io](https://kserve.github.io/website/blog/kserve-0.21-release))

## Why It Matters

Inference teams can test scaling GPU workloads down during idle periods without routing KEDA through WVA. Reusing compatible compiled kernels may reduce work at startup, but teams should measure cold starts and validate cache compatibility in their own environments.

## Evidence

**Kind:** Public implementation and maintainer tests  
**Independently validated:** no

KServe’s release lists the implementation changes. The scale-to-zero pull request reports unit and integration tests for propagating the zero idle count; its author identified a live-cluster scale-to-zero test as follow-up work. KServe describes reduced startup time as an expected benefit, not an independently established measurement. ([github.com](https://github.com/kserve/kserve/releases/tag/v0.21.0))

## Links

- [KServe 0.21 release announcement](https://kserve.github.io/website/blog/kserve-0.21-release) (release notes)
- [KServe v0.21.0 release](https://github.com/kserve/kserve/releases/tag/v0.21.0) (release)
- [Scale-to-zero implementation](https://github.com/kserve/kserve/pull/5996) (implementation)
- [Initial kernel-cache tooling](https://github.com/kserve/kserve/pull/5590) (implementation)
- [Certificate-mode signature verification](https://github.com/kserve/kserve/pull/6103) (implementation)

## Assessment

- **Technical novelty:** meaningful — direct KEDA reconciliation and reusable kernel-cache artifacts integrate existing techniques into KServe.
- **Practical significance:** high — Kubernetes inference teams with intermittent GPU demand should test the scaling and cache paths.
- **Confidence:** medium — release contents and maintainer tests were checked; startup gains and live scale-to-zero remain unverified independently.

## GitHub signal

**Ideas worth investigating:**

- Reconcile user-defined KEDA triggers into `ScaledObject` resources while allowing a zero idle count.
- Build and extract kernel-cache images with preflight checks and certificate-mode signature verification.

The GitHub release is dated September 25, 2026; November 4 is the announcement’s publication date. ([github.com](https://github.com/kserve/kserve/releases/tag/v0.21.0))
