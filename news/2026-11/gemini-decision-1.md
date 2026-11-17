# Gemini Decision 1

**Rank:** 9  
**Release date:** 2026-11-11  
**Area:** Model Releases  
**Primary source:** Google  
**Availability:** Gemini Decisions API via Google AI Studio; API key required.

## What Changed

Gemini Decision 1 scores supplied options in a single forward pass instead of generating answer text token by token. One request can evaluate up to 1,000 independent questions against shared multimodal input, mixing yes/no decisions, multiple-choice selection and ordered rubric scoring. Responses include probabilities or confidence scores. ([blog.google](https://blog.google/innovation-and-ai/technology/developers-tools/gemini-decisions-api/))

## Why It Matters

A closed-set scoring interface could replace generative calls for routing, tool selection and grading. Shared input also lets engineers evaluate several checks without repeating the input for each one. Confidence thresholds can route uncertain cases to a fallback, but should be calibrated on the application’s own data.

## Evidence

**Kind:** Primary release and independent benchmark  
**Independently validated:** yes

Google documents the API and provides a Python example. Google reports 150–250 ms end-to-end latency under its stated conditions; that figure is developer-reported. Artificial Analysis independently measured decision quality and latency on its Decision Index, though its results do not validate every modality or Google’s latency claim. ([blog.google](https://blog.google/innovation-and-ai/technology/developers-tools/gemini-decisions-api/))

## Links

- [Gemini Decisions API announcement](https://blog.google/innovation-and-ai/technology/developers-tools/gemini-decisions-api/) (primary)
- [Artificial Analysis: Gemini Decision 1](https://artificialanalysis.ai/decision-models/gemini-decision-1) (independent benchmark)

## Assessment

- **Technical novelty:** meaningful — direct option scoring and shared-input decisions offer a different serving primitive from free-form generation.
- **Practical significance:** medium — engineers building latency-sensitive routing or grading pipelines should test it against their existing classifiers and generative calls.
- **Confidence:** medium — the interface and an independent benchmark were checked; Google’s architecture and its broader performance claims remain developer-reported.
