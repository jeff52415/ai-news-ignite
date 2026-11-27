# Pydantic AI 2.71

**Rank:** 5  
**Release date:** 2026-11-18  
**Area:** Agentic AI & Harnesses  
**Primary source:** Pydantic AI release notes  
**Availability:** Open-source release and repository; install the harness with `pip install pydantic-ai-harness`.

## What Changed

`RequireVerification` tracks recognized edits and check results during an agent run. If the agent tries to finish after an edit without a passing check, it redirects the agent to verify its work. Redirects are bounded: an unverified run can still finish, with an event reporting that outcome. Custom edit tools may not be recognized. ([github.com](https://github.com/pydantic/pydantic-ai/releases/tag/v2.71.0))

`ToolBridge` replaces eligible tool definitions exposed to the model with fixed `tool_search`, `tool_describe`, and `tool_call` dispatchers. Tool descriptions and schemas are discovered through tool results rather than changing the provider-facing definitions as the underlying set changes. Some tools remain native. ([github.com](https://github.com/pydantic/pydantic-ai/releases/tag/v2.71.0))

## Why It Matters

The verification capability provides a reusable post-edit workflow, but it neither guarantees completion is blocked nor establishes that the chosen checks are sufficient. The bridge can reduce tool-definition churn that disrupts prompt caching, at the cost of discovery steps; provider-side strict schema validation does not apply to bridged arguments, although Pydantic AI validates them before execution. ([pydantic.dev](https://pydantic.dev/docs/ai/harness/require-verification/))

## Evidence

**Kind:** Public open-source implementation and developer documentation  
**Independently validated:** no

Pydantic’s release notes and documentation describe both mechanisms. No independent reliability or cache-hit measurement was identified. ([github.com](https://github.com/pydantic/pydantic-ai/releases/tag/v2.71.0))

## Links

- [Pydantic AI 2.71.0 release](https://github.com/pydantic/pydantic-ai/releases/tag/v2.71.0) (release notes)
- [Pydantic AI repository](https://github.com/pydantic/pydantic-ai) (repository)
- [Require Verification](https://pydantic.dev/docs/ai/harness/require-verification/) (documentation)
- [Tool Bridge](https://pydantic.dev/docs/ai/harness/tool-bridge/) (documentation)

## Assessment

- **Technical novelty:** meaningful — the harness packages edit-aware verification redirects and stable tool dispatch into reusable capabilities.
- **Practical significance:** medium — coding-agent and dynamic-toolset builders should try them while measuring their own verification coverage and cache behavior.
- **Confidence:** medium — the release and developer documentation were checked; performance benefits remain unmeasured independently.

## GitHub signal

**Ideas worth investigating:**

- Tracking edits and invalidating earlier check results.
- Dispatching changing tool sets through stable search, describe, and call interfaces.
- Handling unverified completion as an observable event rather than assuming verification succeeded.
