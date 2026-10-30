# llm-d 1.0

**Rank:** 2  
**Release date:** 2026-10-20  
**Area:** Inference & Infrastructure  
**Primary source:** llm-d v1.0.0 release notes  
**Availability:** Open-source Kubernetes inference stack, components, and release notes on GitHub.

## What Changed

llm-d 1.0 coordinates serving features rather than introducing a new caching or disaggregation algorithm. Its router publishes per-session state for agent-aware routing, uses turn-priority scoring and fairness-aware flow control, and can favor replicas holding relevant KV state. The router configuration API graduates to `llm-d.ai/v1`. ([github.com](https://github.com/llm-d/llm-d/releases/tag/v1.0.0))

For disaggregated serving, `DisaggregatedSet` manages prefill and decode replicas as a logical unit, including coordinated rollouts and readiness checks. Router high availability adds a hot standby and safer updates. ([github.com](https://github.com/llm-d/llm-d/releases/tag/v1.0.0))

## Why It Matters

Teams serving multi-turn agents can evaluate session locality and cache reuse alongside overload protection, rather than optimizing routing in isolation. The operational changes also give Kubernetes operators a more structured way to upgrade disaggregated deployments.

## Evidence

**Kind:** Primary release and public implementation  
**Independently validated:** no

The llm-d release notes and router release describe the implementation and configuration changes. Production performance and reliability benefits remain developer-reported; no independent reproduction was identified in the sources reviewed. ([github.com](https://github.com/llm-d/llm-d/releases/tag/v1.0.0))

## Links

- [llm-d v1.0.0 release](https://github.com/llm-d/llm-d/releases/tag/v1.0.0) (release notes)
- [llm-d router v1.0.0 release](https://github.com/llm-d/llm-d-router/releases/tag/v1.0.0) (component release notes)

## Assessment

- **Technical novelty:** meaningful — the contribution is coordination of session-aware routing, flow control, and deployment operations around existing serving techniques.
- **Practical significance:** high — Kubernetes teams running multi-turn or mixed-priority inference workloads should test it against their own traffic.
- **Confidence:** medium — the public release and component notes were checked, but production performance and reliability claims were not independently validated.

## GitHub signal

**Ideas worth investigating:**

- Publish session turn and in-flight state to inform routing decisions.
- Combine turn-priority scoring with fairness-aware flow control.
- Coordinate prefill and decode replica rollouts through `DisaggregatedSet`.
