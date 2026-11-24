# External Sandboxes for Coding Agents

**Rank:** 1  
**Release date:** 2026-11-17  
**Area:** Agentic AI & Harnesses  
**Primary source:** Prime Radiant  
**Availability:** Public repository, protocol specification, prototype backends, packages, and integration instructions. ([simonwillison.net](https://simonwillison.net/2026/Nov/17/external-sandboxes-for-coding-agents/))

## What Changed

Instead of running the entire coding agent inside a container, this design keeps the agent on the host and routes supported tool operations to a separate Linux sandbox over a common API. Prototype backends use v86/WebAssembly, Apple Containers, and Quicksand/QEMU. An optional allow-list proxy can replace placeholder credentials with host-side secrets. ([blog.primeradiant.com](https://blog.primeradiant.com/external-sandboxes-for-coding-agents/?utm_source=openai))

The boundary depends on the agent integration: Claude Code’s Bash commands go through the sandbox, but its native read and edit tools remain on the host. Codex and Pi route additional filesystem operations through their integrations. ([blog.primeradiant.com](https://blog.primeradiant.com/external-sandboxes-for-coding-agents/?utm_source=openai))

## Why It Matters

The protocol gives engineers a starting point for isolating agent-generated commands without moving the agent itself. Mount permissions and network rules still define what sandboxed code can affect; writable mounts remain exposed, and an allowed service could echo an injected credential. The developers describe the backends as experimental and not audited for sensitive workloads. ([blog.primeradiant.com](https://blog.primeradiant.com/external-sandboxes-for-coding-agents/?utm_source=openai))

## Evidence

**Kind:** Public implementation and developer-reported testing  
**Independently validated:** no

Prime Radiant publishes backend implementations, a protocol specification, a conformance tool, and agent integrations. Its article reports automated testing of the Codex integration; no independent security audit or reproduction was identified. Simon Willison’s discussion corroborates the release but is not independent validation: he worked on the project. ([github.com](https://github.com/prime-radiant-inc/external-sandbox))

## Links

- [Technical explanation](https://blog.primeradiant.com/external-sandboxes-for-coding-agents/) (primary)
- [External sandbox repository](https://github.com/prime-radiant-inc/external-sandbox) (repository)
- [Simon Willison’s discussion](https://simonwillison.net/2026/Nov/17/external-sandboxes-for-coding-agents/) (project collaborator)
- [New Runtime field note](https://newruntime.com/posts/prime-radiant-and-simon-willison-release-external-sandboxes-dac769/) (secondary)

## Assessment

- **Technical novelty:** meaningful — a shared execution interface separates host-side agent tooling from interchangeable sandbox backends.
- **Practical significance:** medium — engineers evaluating coding-agent isolation should try the prototypes against their own tool and filesystem threat models.
- **Confidence:** medium — the primary explanation, repository, and secondary coverage were checked; security and test claims remain developer-reported.

## GitHub signal

**Ideas worth investigating:**

- A host-side agent with separately sandboxed command execution.
- A common execution protocol with backend conformance tests.
- An allow-list proxy that replaces placeholder credentials outside the guest.
