# Harness Leaderboard evaluation corrections

**Rank:** 2  
**Release date:** 2026-11-18  
**Area:** Agentic AI & Harnesses  
**Primary source:** Harness Leaderboard changelog  
**Availability:** Public leaderboard, changelog, and Hugging Face Space repository.

## What Changed

The November 18 correction enabled OpenClaw’s setting to resend earlier model reasoning to an unrecognized OpenAI-compatible provider, then replaced its results with full reruns. The earlier behavior was an OpenClaw provider-compatibility default, not simply an adapter deleting a field. ([huggingface.co](https://huggingface.co/spaces/joelniklaus/harness-leaderboard/blob/main/CHANGELOG.md?utm_source=openai))

The leaderboard also changed its Claude Code proxy to pass images through instead of substituting a text note, and reran affected trials. The text-only endpoints still either discard the image or reject the request; the change did not give those models vision. On November 22, the board added Inkling 2 Mini, including an OpenClaw rerun with reasoning replay enabled. ([huggingface.co](https://huggingface.co/spaces/joelniklaus/harness-leaderboard/blob/main/CHANGELOG.md))

## Why It Matters

Agent scores can reflect conversation serialization, modality handling, tool-call parsing, network isolation, and infrastructure failures—not just model capability. Evaluation builders should record these settings and rerun affected trials when they change.

## Evidence

**Kind:** Public benchmark and implementation  
**Independently validated:** no

Leaderboard developer Joël Niklaus reports three attempts on each of 198 tasks across 12 harnesses for Inkling 2 Mini. He also reports trajectory checks for answer leakage and documents the correction reruns. ([huggingface.co](https://huggingface.co/spaces/joelniklaus/harness-leaderboard/blob/main/CHANGELOG.md))

Honesty.Tools independently checked an earlier version’s published aggregates against its API and results snapshot, but did not rerun the benchmark or validate these later corrections. ([honesty.tools](https://www.honesty.tools/blog/niklaus-harness-leaderboard-reading-note/))

## Links

- [Leaderboard changelog](https://huggingface.co/spaces/joelniklaus/harness-leaderboard/blob/main/CHANGELOG.md) (primary)
- [Harness Leaderboard](https://huggingface.co/spaces/joelniklaus/harness-leaderboard) (benchmark)
- [Harness settings](https://huggingface.co/spaces/joelniklaus/harness-leaderboard/blob/main/docs/harness-settings.md) (implementation documentation)
- [Honesty.Tools aggregate check](https://www.honesty.tools/blog/niklaus-harness-leaderboard-reading-note/) (independent check of earlier release)

## Assessment

- **Technical novelty:** meaningful — the corrections expose how reasoning replay and image translation alter the effective agent harness.
- **Practical significance:** high — engineers building agent evaluations should test these boundaries and preserve enough traces to audit failures.
- **Confidence:** medium — the changelog and settings documentation were checked; the correction results remain developer-reported and have not been independently reproduced.

## GitHub signal

The implementation is published as a Hugging Face Space repository; no GitHub star count was verified.

**Ideas worth investigating:**

- Preserve prior reasoning in the provider’s expected field across tool-use turns.
- Audit trajectories for reference solutions and hidden tests, including numbered file views.
- Distinguish malformed model output from server-parser and infrastructure failures.
