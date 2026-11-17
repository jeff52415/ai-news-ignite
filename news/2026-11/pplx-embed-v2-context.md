# pplx-embed-v2-context

**Rank:** 6  
**Release date:** 2026-11-03  
**Area:** Model Releases  
**Primary source:** Perplexity  
**Availability:** Open weights and usage examples on Hugging Face; the 9B checkpoint is MIT-licensed. Loading the models uses custom code with `trust_remote_code=True`.

## What Changed

Rather than embedding each chunk independently, the models encode document chunks together and return a vector for each chunk with surrounding context in view. They also support isolated text and contextual image chunks. ([huggingface.co](https://huggingface.co/perplexity-ai/pplx-embed-v2-context-9b))

The 9B model is trained using graded chunk relevance distilled from a query-aware compression model, rather than treating every non-answer chunk as a negative. The 0.6B model is distilled from the 9B model into a compatible space: use the 9B model’s **1024-dimensional prefix** when mixing sizes. Both produce unnormalized int8 embeddings. ([arxiv.org](https://arxiv.org/abs/2610.38854))

## Why It Matters

Retrieval engineers can test whether context-aware chunk vectors surface both answers and supporting evidence, while using the smaller model for queries against a 9B-built index. Use non-overlapping document chunks, `encode_queries` for queries, and cosine similarity—or normalize vectors before dot-product comparison. ([huggingface.co](https://huggingface.co/perplexity-ai/pplx-embed-v2-context-0.6b))

## Evidence

**Kind:** Public implementation and developer-reported benchmarks  
**Independently validated:** no

Perplexity and its research collaborators report retrieval evaluations in the technical report; the model cards provide weights, implementation code, and examples. The reported quality comparisons remain developer-reported, not an independent reproduction. ([arxiv.org](https://arxiv.org/abs/2610.38854))

## Links

- [Release announcement](https://community.perplexity.ai/t/introducing-pplx-embed-v2-context-open-weight-vision-language-embedding-models-in-9b-and-0-6b/6466) (primary)
- [9B model card](https://huggingface.co/perplexity-ai/pplx-embed-v2-context-9b) (weights)
- [0.6B model card](https://huggingface.co/perplexity-ai/pplx-embed-v2-context-0.6b) (weights)
- [Contextual Embeddings Beyond the Gold Chunk](https://arxiv.org/abs/2610.38854) (technical report)

## Assessment

- **Technical novelty:** meaningful — graded relevance distillation trains contextual chunk retrieval without assuming only one useful chunk per document.
- **Practical significance:** high — retrieval engineers working with long or visual documents should test it against their own chunking and latency requirements.
- **Confidence:** medium — the announcement, model cards, and technical report were checked; retrieval-quality claims remain developer-reported.
