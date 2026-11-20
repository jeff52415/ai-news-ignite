# Granite 4.1 LLMON previews

**Rank:** 4  
**Release date:** 2026-11-12  
**Area:** Model Releases  
**Primary source:** IBM Granite  
**Availability:** Public 3B and 8B preview checkpoints on Hugging Face; both model cards specify Apache 2.0. ([huggingface.co](https://huggingface.co/ibm-granite/granite-4.1-3b-llmon-preview?utm_source=openai))

## What Changed

Instead of relying on a conventional chat template to imply instruction and data boundaries, LLMON uses six reserved delimiter tokens to mark typed, addressable blocks. An `exec` block references the instruction, inputs, requirements, and output. The shipped chat template renders these bindings from structured message fields. ([huggingface.co](https://huggingface.co/blog/ibm-granite/llmon-an-llm-native-markup-language-now-in-granite))

IBM post-trained the previews from Granite 4.1 **base** checkpoints, including examples with unbound decoy instructions and data, followed by reinforcement learning and preference training. The intended boundary is learned model behavior, not a hard execution guarantee. ([huggingface.co](https://huggingface.co/blog/ibm-granite/llmon-an-llm-native-markup-language-now-in-granite))

## Why It Matters

Agent engineers can test explicit instruction/data binding when processing retrieved text or tool outputs. The previews offer a defense layer against indirect prompt injection, but should be evaluated alongside authorization and other controls; IBM describes them as experimental, not production-ready. ([huggingface.co](https://huggingface.co/blog/ibm-granite/llmon-an-llm-native-markup-language-now-in-granite))

## Evidence

**Kind:** Public checkpoints, developer benchmarks, and a small third-party test  
**Independently validated:** yes

IBM’s **developer-reported** paper measured attack success on OPI and ASB; for the 3B preview it reported 0.1% and 5.6%, respectively. These results cover the tested attack sets, not a guarantee against adaptive attacks. ([arxiv.org](https://arxiv.org/abs/2610.38120))

Kortress independently tested ten mostly Korean indirect-injection cases: the 3B LLMON preview followed none of the injected commands. This was a single, small test, and some outputs had quality issues despite resisting the injection. ([kortress.com](https://kortress.com/en/archive/granite-llmon-korean-injection-test))

## Links

- [Technical introduction](https://huggingface.co/blog/ibm-granite/llmon-an-llm-native-markup-language-now-in-granite) (primary)
- [3B preview checkpoint](https://huggingface.co/ibm-granite/granite-4.1-3b-llmon-preview) (weights)
- [8B preview checkpoint](https://huggingface.co/ibm-granite/granite-4.1-8b-llmon-preview) (weights)
- [LLMON toolkit](https://github.com/generative-computing/llmon) (implementation)
- [Post-training paper](https://arxiv.org/abs/2610.38120) (developer research)
- [Korean injection test](https://kortress.com/en/archive/granite-llmon-korean-injection-test) (third-party measurement)

## Assessment

- **Technical novelty:** meaningful — Reserved structural tokens and identifier-based execution bindings are taught through post-training rather than enforced by a new architecture.
- **Practical significance:** high — RAG and agent builders should test the previews against their own untrusted-input workloads, without treating them as production-ready.
- **Confidence:** medium — The artifacts, developer paper, and a narrow independent test were checked; broad robustness and adaptive-attack resistance remain insufficiently validated.

## GitHub signal

**Ideas worth investigating:**

- Convert structured JSON into typed, addressable LLMON blocks.
- Use execution bindings to associate instructions with specific inputs and outputs.
- Train with unbound decoy instructions and data to reinforce the intended boundary. ([github.com](https://github.com/generative-computing/llmon))
