# dsh-superagent research prototype

**Rank:** 1  
**Release date:** 2026-10-31  
**Area:** Trending GitHub  
**Primary source:** DeepSeek Harness Team  
**Availability:** MIT-licensed source; requires DeepSeek Harness and operator configuration.

## What Changed

The prototype adds a persistent orchestration layer around DeepSeek Harness for one GitHub repository. GitHub and optional Feishu events enter an engine that applies authorization policy and turns accepted requests into tickets. Each ticket gets its own agent session and working directory; results return through the originating conversation. Unlike a prompt-only coding session, the engine also tracks follow-ups, worker reports and durable side effects. ([github.com](https://github.com/deepseek-ai/dsh-superagent-prototype))

Explicitly authorized requests and inferred work have different admission paths: inferred acceptance requires an enabled matching rule and auto mode. Separate directories are **not a security sandbox**; workers retain the host user’s operating-system access. ([github.com](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/main/docs/007-architecture.md))

## Why It Matters

The implementation gives agent engineers a concrete design for separating incoming context from authority, maintaining task state and resuming interrupted work. It is useful for studying long-running workflows, but requires separate isolation and review before exposure to real repositories. The authors describe it as research code, not production-ready software. ([github.com](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/main/docs/007-architecture.md))

## Evidence

**Kind:** Independent operational reproduction  
**Independently validated:** yes

GitHub user **mikel38487** reported running the prototype against a real repository and finding service-process detection and missed-notification defects. **Wanke15** subsequently reported independently reproducing the notification-loss defect on a scratch repository and testing a fix. These reports support the existence of that operational failure mode; they do not establish agent quality or performance. ([github.com](https://github.com/deepseek-ai/deepseek-harness/discussions/11700))

## Links

- [Prototype repository](https://github.com/deepseek-ai/dsh-superagent-prototype) (repo)
- [Implementation architecture](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/main/docs/007-architecture.md) (documentation)
- [Operational defects and independent reproduction](https://github.com/deepseek-ai/deepseek-harness/discussions/11700) (independent report)

## Assessment

- **Technical novelty:** meaningful — policy-gated tickets combine persistent event routing with per-task sessions and durable effects.
- **Practical significance:** high — engineers building repository agents should study the orchestration and authorization model, then test in an isolated environment.
- **Confidence:** medium — the public implementation and an independent defect reproduction were checked; broader reliability and agent effectiveness remain unvalidated.

## GitHub signal

**Ideas worth investigating:**

- Record the authorization basis for each ticket and revalidate it as policy changes.
- Use durable effects and an outbox to separate transactional state changes from external actions.
- Route follow-ups to per-ticket sessions and resume interrupted assignments.
