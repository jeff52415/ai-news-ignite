# Gandalf: environment-aware agent verification

**Rank:** 2  
**Release date:** 2026-05-27  
**Area:** Agentic AI & Harnesses  
**Primary source:** Handshake AI Research  
**Availability:** Apache-2.0 repository, PyPI package, and runnable quickstart. The original release predates the paper’s November 17, 2026 submission. ([joinhandshake.com](https://joinhandshake.com/research/ai/gandalf-the-grader/))

## What Changed

Gandalf grades binary rubric criteria with a tool-using judge in the rollout environment. Unlike a final-answer or fixed-snapshot judge, it selects files and tool state to inspect during grading. It uses the OpenHands SDK and accepts natural-language domain guidance at runtime. ([github.com](https://github.com/Handshake-AI-Research/gandalf-the-grader))

## Why It Matters

This makes it practical to evaluate deliverables and side effects that a text response may not reveal, such as spreadsheet formulas or application state. Engineers can adapt the quickstart to test whether this additional evidence improves their own grading reliability. ([github.com](https://github.com/Handshake-AI-Research/gandalf-the-grader))

## Evidence

**Kind:** Open-source implementation and developer-reported benchmark  
**Independently validated:** no

The repository contains implementation, tests, and a quickstart. In the paper, the authors report evaluating against human-judged banking criteria and comparing verifier accuracy and cost; those comparative results remain developer-reported. An independent review examined the paper but did not run the full code or reproduce its experiments. ([github.com](https://github.com/Handshake-AI-Research/gandalf-the-grader))

## Links

- [Gandalf repository](https://github.com/Handshake-AI-Research/gandalf-the-grader) (repo)
- [Technical paper](https://arxiv.org/abs/2611.22841) (primary)
- [Release article](https://joinhandshake.com/research/ai/gandalf-the-grader/) (primary)
- [Independent paper review](https://daiwk.github.io/auto-research/agent-research/2611.22841-gandalf-bvb/README-en/) (review)

## Assessment

- **Technical novelty:** meaningful — reactive evidence collection combines environment access with runtime domain guidance.
- **Practical significance:** high — engineers grading artifacts or tool-side effects should try the quickstart against their own expert-labeled tasks.
- **Confidence:** medium — the repository and paper were checked, but comparative performance remains self-reported and the independent review did not reproduce it.

## GitHub signal

**Ideas worth investigating:**

- Select tools and evidence reactively for rubric criteria.
- Record criterion-level verdicts, reasoning, and evidence.
- Supply domain guidance without changing the verifier implementation.
