# Road to Together Compiler

**Rank:** 6  
**Release date:** 2026-11-16  
**Area:** Inference & Infrastructure  
**Primary source:** Together AI  
**Availability:** Public technical explanation and paper; organizations can contact Together AI for compiler early access. ([together.ai](https://www.together.ai/blog/road-to-together-compiler?utm_source=openai))

## What Changed

Together Compiler uses agents to rewrite and optimize forward-pass code for a particular model, hardware target, and traffic shape. Rather than relying on a fixed registry of optimized kernels or a single hand-written megakernel, it searches across kernel implementations and fusion choices. The developers report that splitting operations can sometimes outperform keeping them fused. ([together.ai](https://www.together.ai/blog/road-to-together-compiler?utm_source=openai))

A tiered persistent engine hot-reloads candidates: a smaller execution tier supports rapid iteration, while a larger tier tests whether improvements hold with more representative data. This addresses the tradeoff between misleading isolated-kernel timings and the cost of repeatedly launching a full inference engine. ([fandai.donguapan.workers.dev](https://fandai.donguapan.workers.dev/https/www.together.ai/blog/together-compiler-continual-compilation-for-ai-inference?utm_source=openai))

## Why It Matters

Inference teams evaluating decode optimizations should measure candidates in context. Launch and benchmark-harness overhead can distort microsecond-scale kernel timings, while synthetic inputs can misrepresent data-dependent MoE routing. A faster isolated kernel need not yield a faster forward pass. ([together.ai](https://www.together.ai/blog/road-to-together-compiler))

## Evidence

**Kind:** Developer technical explanation and benchmark  
**Independently validated:** no

Together AI reports that, on a Llama 1B output projection, the Triton kernel selected by Inductor ran in **7.4 µs** in the live forward pass versus **6.4 µs** for cuBLAS. Together also reports that random inputs overstated GLM 5.3 MoE grouped-GEMM latency by **4–21%** relative to realistic inputs. These are **developer-reported measurements**, not independent reproductions. ([together.ai](https://www.together.ai/blog/road-to-together-compiler))

The accompanying paper describes the persistent-engine design. Together reports production use, but the available sources do not independently verify that deployment or the performance claims. ([arxiv.org](https://arxiv.org/abs/2611.14681))

## Links

- [The road to Together Compiler](https://www.together.ai/blog/road-to-together-compiler) (primary)
- [Together Compiler: Continual Compilation for AI Inference](https://arxiv.org/abs/2611.14681) (developer paper)

## Assessment

- **Technical novelty:** meaningful — agents optimize forward-pass code using tiered, persistent measurements rather than only isolated kernel benchmarks.
- **Practical significance:** medium — inference teams should try representative-input and forward-pass measurements when assessing kernel changes.
- **Confidence:** medium — the primary explanation and paper were checked; performance and production-use claims remain developer-reported.
