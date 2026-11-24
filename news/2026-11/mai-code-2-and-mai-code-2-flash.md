# MAI Code 2 and MAI Code 2 Flash

**Rank:** 8  
**Release date:** 2026-11-17  
**Area:** Model Releases  
**Primary source:** Microsoft model card  
**Availability:** Both models are available through Copilot. Flash is also available through Microsoft Foundry; weights are closed.

## What Changed

Microsoft describes two vision-enabled sparse mixture-of-experts coding models trained from scratch. Both underwent reinforcement learning in the Copilot CLI and VS Code agent harnesses. Flash additionally uses logit distillation from a larger teacher. This places agent-tool interactions in post-training, rather than relying solely on training outside the target agent environment.

## Why It Matters

Training in the intended harness may help align a coding model with the tools and interaction patterns it encounters in use. Engineers evaluating the models should nevertheless test them in their own harnesses and workflows: developer-reported benchmark results do not establish equivalent performance across environments.

## Evidence

**Kind:** Primary release and developer-reported benchmarks  
**Independently validated:** no

Microsoft published the model card and hosted the models. Its coding benchmark results are developer-reported; no independent reproduction of those results was established during this check. The card contains conflicting parameter totals, so they are omitted here.

## Links

- [MAI Code 2 and MAI Code 2 Flash model card](https://microsoft.ai/pdf/MAI-Code-2-And-MAI-Code-2-Flash-Model-Card.pdf) (primary)
- [MAI Code 2 Flash in Microsoft Foundry](https://ai.azure.com/catalog/models/mai-code-2-flash) (hosted artifact)
- [MAI Code 2 launch report](https://foundermag.co/launches/mai-code-2/) (corroborating report)

## Assessment

- **Technical novelty:** meaningful — reinforcement learning in the intended coding-agent harnesses targets tool-use behavior directly.
- **Practical significance:** medium — coding-agent engineers using Copilot or Foundry should test the models against their own tasks and harnesses.
- **Confidence:** medium — the model card and corroborating reporting were checked; performance claims remain developer-reported.
