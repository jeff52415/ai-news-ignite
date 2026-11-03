# Charter v0.6.0

**Rank:** 1  
**Release date:** 2026-10-29  
**Area:** Agentic AI & Harnesses  
**Primary source:** Charter GitHub release  
**Availability:** Public source repository and tagged release; install with `pip install charter-ai==0.6.0`.

## What Changed

`FromContext()` marks a tool field as host-supplied rather than model-supplied. The field is absent from the model-facing schema but is available to typed validation rules. If required context is missing, Charter raises `ContextError` before those rules run. Context can remain rule-only or be sent in a request when paired with a wire-field annotation. ([github.com](https://github.com/r28ai/charter/releases/tag/v0.6.0))

The release also adds alternative OAuth scope declarations and diagnostics. `scopes_for` now reduces overlapping alternatives rather than simply returning every declared scope; scope selection changes the requested grant, not the calls a tool is allowed to make. ([github.com](https://github.com/r28ai/charter/releases/tag/v0.6.0))

## Why It Matters

Host-owned context gives engineers a way to enforce tenant-specific checks without trusting an identity value supplied in editable model arguments. The boundary is only as sound as the host’s context binding and the authorization rules it implements; the feature does not itself establish tenant ownership.

## Evidence

**Kind:** Public open-source implementation and documentation  
**Independently validated:** no

The Charter developers document the mechanism and provide a customer-order validation example. Agent Signal reviewed the release and documentation independently, but explicitly says it did not execute its proposed test. No independent reproduction or deployment was established. ([github.com](https://github.com/r28ai/charter?utm_source=openai))

## Links

- [Charter v0.6.0 release](https://github.com/r28ai/charter/releases/tag/v0.6.0) (release notes)
- [Charter repository](https://github.com/r28ai/charter) (source)
- [Agent Signal experiment](https://www.rittikabuilds.com/reports/2026-10-30/experiment/) (independent documentation review)

## Assessment

- **Technical novelty:** meaningful — trusted per-call context is injected into validation while withheld from the model-facing tool schema.
- **Practical significance:** medium — engineers building multi-tenant agents should evaluate the pattern alongside their existing identity and authorization controls.
- **Confidence:** medium — the release and corroborating documentation were checked, but runtime behavior and production security remain unverified independently.

## GitHub signal

**Ideas worth investigating:**

- Bind host-owned identity to each call and validate resource ownership against it.
- Fail before policy evaluation when required trusted context is missing.
- Use `egress_map` to review context fields withheld from the model.
