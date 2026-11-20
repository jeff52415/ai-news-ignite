# Reef Python harness adapter

**Rank:** 6  
**Release date:** 2026-11-07  
**Area:** Agentic AI & Harnesses  
**Primary source:** Human-Agent-Society Reef pull request #1242  
**Availability:** Open-source change merged into Reef’s main branch. ([github.com](https://github.com/Human-Agent-Society/reef/pull/1242))

## What Changed

Reef’s new `python` adapter represents the harness as a program tree containing `program/main.py` and its imported modules. Unlike the existing coding-agent adapters, whose agents own the loop and model calls, the program can own both. Reef runs it once per task with `uv`. ([github.com](https://github.com/Human-Agent-Society/reef/pull/1242))

The deployment’s model binding is rendered separately into `program/model.json`, rather than stored in the served tree. Validation requires an entry point, rejects modules that do not compile and checks for secret-shaped text. Changes to program parts wait for human activation. ([github.com](https://github.com/Human-Agent-Society/reef/pull/1242))

## Why It Matters

Engineers can modify and evaluate loop-level behavior as a versioned harness artifact rather than being limited to a coding agent’s built-in loop. Reef’s documented evolution flow compares candidate and current trees on tasks before selecting a snapshot. Validation is not a guarantee that generated code is safe or correct. ([github.com](https://github.com/Human-Agent-Society/reef/blob/main/docs/user-guide/evolve-your-harness.rst))

## Evidence

**Kind:** Public implementation and developer-reported checks  
**Independently validated:** no

PR author BobbyZhouZijian reports tests for validation, binding rendering and installation, plus a local container check. The reported full test run had failures and errors; the author compared them with an unchanged baseline. A Harbor trial using this adapter and remote environments were not verified. ([github.com](https://github.com/Human-Agent-Society/reef/pull/1242))

## Links

- [Merged pull request #1242](https://github.com/Human-Agent-Society/reef/pull/1242) (implementation)
- [Evolve your harness guide](https://github.com/Human-Agent-Society/reef/blob/main/docs/user-guide/evolve-your-harness.rst) (documentation)

## Assessment

- **Technical novelty:** meaningful — the adapter makes the execution loop and model calls part of the evolvable program tree.
- **Practical significance:** medium — engineers experimenting with task-evaluated harness changes should try it locally, while treating remote execution as unvalidated.
- **Confidence:** medium — the merged implementation and documentation were checked; execution results remain developer-reported.

## GitHub signal

**Ideas worth investigating:**

- Evolve a Python program tree rather than only prompts or agent configuration.
- Render model bindings separately from the served artifact.
- Run each task through the program and collect optional JSONL session logs. ([github.com](https://github.com/Human-Agent-Society/reef/pull/1242))
