# XYBench

**Rank:** 9  
**Release date:** 2026-11-13  
**Area:** Agentic AI & Harnesses  
**Primary source:** Allen Institute for AI  
**Availability:** Public code; dataset access requires a Hugging Face login and acceptance of access conditions. Model generation and judging require configured provider access. ([huggingface.co](https://huggingface.co/datasets/allenai/XYBench-dataset))

## What Changed

XYBench evaluates responses to *XY problems*: a user asks for help with approach Y, although their underlying goal is X. Each example provides separate reference rubrics for the stated request, intended goal, and misconception.

Rather than assigning one correctness score, an LLM judge checks whether each solution appears, which receives emphasis, and whether the response redirects the user away from the misconception. The misconception label does not always require an explicit explanation: for some subsets, addressing X without entertaining Y can qualify. ([huggingface.co](https://huggingface.co/blog/allenai/xybench))

## Why It Matters

The separate measures can reveal an assistant that mentions a useful fix but buries it beneath advice for a misguided approach. Engineers can use them to test prompting or training changes, while reviewing judge disagreements—especially on emphasis—and checking whether gains transfer to multi-turn interactions.

## Evidence

**Kind:** Primary release and developer-reported evaluation  
**Independently validated:** no

Ai2 reports that two human reviewers assessed 500 responses. Their average agreement with the automated judge was **74.2–79.8% for emphasis**, lower than for the other reported dimensions. These figures are developer-reported, not an independent reproduction. ([huggingface.co](https://huggingface.co/blog/allenai/xybench))

The release article reports 8,115 questions, while the current repository and dataset card list 8,111 after additional filtering; results may therefore differ slightly from the paper. The benchmark is English-language and primarily procedural, with a single-turn main evaluation. ([huggingface.co](https://huggingface.co/blog/allenai/xybench))

## Links

- [XYBench technical introduction](https://huggingface.co/blog/allenai/xybench) (primary)
- [XYBench repository](https://github.com/allenai/XYBench) (code)
- [XYBench dataset](https://huggingface.co/datasets/allenai/XYBench-dataset) (data)

## Assessment

- **Technical novelty:** meaningful — separate rubrics distinguish solution presence, emphasis, and redirection from literal compliance.
- **Practical significance:** medium — teams evaluating troubleshooting assistants should try it alongside human review and conversational tests.
- **Confidence:** medium — the article, repository, and dataset card were checked; benchmark findings and reviewer agreement remain developer-reported.

## GitHub signal

**Ideas worth investigating:**

- Tag individual answer units as literal, goal-directed, or other before scoring whole-response emphasis.
- Compare the default query-only condition with the oracle-intent condition to distinguish intent inference from acting on supplied intent. ([github.com](https://github.com/allenai/XYBench))
