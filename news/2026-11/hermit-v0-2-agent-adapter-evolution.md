# Hermit v0.2 agent-adapter evolution

**Rank:** 5  
**Release date:** 2026-11-04  
**Area:** Agentic AI & Harnesses  
**Primary source:** Infini AI Lab  
**Availability:** Apache-2.0 source and release; clone the repository to run examples or install the core package from PyPI.

## What Changed

Hermit separates model access, reusable Base Agent execution, and acting or evolver logic. It evolves an **external adapter** rather than changing the underlying model or agent harness. ReHarness retrieves and revises reflections per task instance. AHE Adapter analyzes trajectories and feedback to attribute outcomes to proposed changes; its automatic rollback mode restores files associated with changes judged harmful. ([github.com](https://github.com/Infini-AI-Lab/hermit/releases/tag/v0.2.0))

The release also changes the adapter layout: v0.1 adapters must be migrated and converted plugins rebuilt. ([github.com](https://github.com/Infini-AI-Lab/hermit/releases/tag/v0.2.0))

## Why It Matters

Engineers can test and version changes to instructions, hooks, skills, and memory while leaving the host agent fixed. The shared execution layer makes it easier to compare evolution methods, although results remain sensitive to the task, model, and evaluation protocol.

## Evidence

**Kind:** Substantial open-source implementation and developer-reported benchmark  
**Independently validated:** no

Infini AI Lab’s AHE pull request documents the adapter, evolver, tests, and an OfficeQA example. In a **developer-reported** run on an earlier implementation revision, the final adapter scored 0.616 versus 0.366 for its starting adapter on 172 held-out questions. The authors note that much of the gain concerned answer form; this single reported run does not establish general performance gains. ([github.com](https://github.com/Infini-AI-Lab/hermit/pull/65))

## Links

- [v0.2.0 release](https://github.com/Infini-AI-Lab/hermit/releases/tag/v0.2.0) (release notes)
- [Hermit repository](https://github.com/Infini-AI-Lab/hermit) (source)
- [AHE Adapter implementation](https://github.com/Infini-AI-Lab/hermit/pull/65) (implementation and evaluation)

## Assessment

- **Technical novelty:** Meaningful — the framework applies feedback-driven evolution to external adapter files, with attribution and optional file-level rollback.
- **Practical significance:** Medium — agent engineers with repeatable task sets should try it for controlled harness experiments.
- **Confidence:** Medium — the release and implementation were checked, but performance evidence remains developer-reported and was not independently reproduced.

## GitHub signal

**Stars:** 507 ([github.com](https://github.com/Infini-AI-Lab/hermit))

**Ideas worth investigating:**

- Retrieve and revise task-specific reflections from a shared bank.
- Attribute observed outcome changes to edits recorded in a change manifest.
- Roll back harmful changes at file granularity while retaining other edits.
