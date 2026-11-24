# Agentic Evals

**Rank:** 7  
**Release date:** 2026-11-23  
**Area:** Agentic AI & Harnesses  
**Primary source:** Hugging Face  
**Availability:** Public walkthrough, task dataset, scripts, and rollout traces.

## What Changed

The authors adapted Terminal-Bench’s two-peak Raman-fitting task into an eight-spectrum development set requiring three fitted peaks and a D-to-G intensity ratio. A shortcut that read peak heights directly and guessed widths returned the expected ratio without fitting. The final verifier adds checks on each fitted peak and rejects that shortcut. ([huggingface.co](https://huggingface.co/blog/agentic-evals))

## Why It Matters

A plausible final answer can conceal failure to perform the intended computation. Evaluation engineers can test for this by running reference, no-op, and shortcut baselines before trusting scores. Trace inspection, pinned serving conditions, and repeated trials help distinguish grading, environment, harness, and model failures. ([huggingface.co](https://huggingface.co/blog/agentic-evals))

## Evidence

**Kind:** Public implementation and developer-reported benchmark  
**Independently validated:** no

Hugging Face reports that its shortcut returned the expected ratio on all eight tasks but failed the strengthened verifier. In one development run, the authors reported success at least once on seven of eight tasks, but success on all three trials for only one task. The public repository contains scripts and traces; the small development set does not support broad model rankings. ([huggingface.co](https://huggingface.co/blog/agentic-evals))

## Links

- [Agentic evaluations walkthrough](https://huggingface.co/blog/agentic-evals) (primary)
- [Raman-lab tasks](https://huggingface.co/datasets/burtenshaw/raman-lab) (dataset)
- [Raman-lab evaluation repository](https://github.com/burtenshaw/raman-lab-evals) (code and results)
- [Raman-lab rollout traces](https://huggingface.co/datasets/burtenshaw/raman-lab-runs) (traces)

## Assessment

- **Technical novelty:** meaningful — adversarially testing the verifier exposes a shortcut that a ratio-only check would accept.
- **Practical significance:** medium — teams building terminal-agent regression tests should try the reference, no-op, and shortcut checks.
- **Confidence:** medium — the walkthrough and public artifacts were checked; benchmark outcomes remain developer-reported.

## GitHub signal

**Ideas worth investigating:**

- Run a peak-height shortcut alongside the oracle and no-op baselines.
- Inspect trajectories for premature completion and missing dependencies.
- Compare retry success with consistency across all trials.
