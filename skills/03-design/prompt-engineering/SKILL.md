---
name: prompt-engineering
description: Use when designing prompts, evals, or LLM-powered features — prompt architecture, model selection, guardrails, and eval harnesses for prompt-as-product surfaces. Triggers on "prompt engineering", "LLM feature", "eval harness", "prompt design", "提示词工程", "LLM 特性", "prompt 设计".
---

# Prompt Engineering

Design prompts and evals as a first-class engineering deliverable. `context-engineering`
assembles context for a coding agent; this skill designs the prompt-as-product surface — the
prompts, model choices, guardrails, and eval harnesses behind LLM-powered features. A prompt
without an eval is an opinion; an eval without a prompt is a benchmark. Ship neither blind.

## When to use

- Designing an LLM-powered feature (chat, summarization, extraction, classification, generation)
- Building or refining a prompt for production use
- Creating an eval harness to measure prompt/model quality
- Selecting a model for a specific task against cost/latency/quality trade-offs
- Triggers on "prompt engineering", "LLM feature", "eval harness", "prompt design", "提示词工程", "LLM 特性"

**Not for:** assembling context for a coding agent (use `context-engineering`); general research
on a topic (use `research`); API contract design for non-LLM endpoints (use `api-design`).

## Steps

### 1. Define the task and success criteria

State the task in one sentence, then define measurable success criteria — without these, prompt
iteration is vibes-driven. Pull from the product spec:

- Input space: what inputs will the prompt receive? (vary by length, language, edge case, adversarial)
- Output contract: structured output (JSON schema), free text, or classification?
- Quality bar: accuracy %, format adherence %, hallucination rate, latency target, cost per call
- Failure modes to prevent: what must the model NEVER do? (leak PII, invent facts, refuse valid input)

_Verify: success criteria are written as measurable thresholds, not "good responses."_

### 2. Design the prompt architecture

Structure the prompt as components, not a wall of text — each component has a job:

- **System / role:** who the model is, what it must and must not do (guardrails live here)
- **Task instruction:** the operation, stated precisely with the output format
- **Context / retrieved data:** only the facts the model needs (not the whole knowledge base —
  context bloat degrades accuracy and raises cost)
- **Few-shot examples:** 2–5 input→output pairs covering the happy path and an edge case; place
  before the actual input, after the instruction
- **Output format:** explicit schema or template; use structured output (JSON mode / function
  calling) when the downstream system parses the result

Separate stable parts (system, format) from variable parts (user input, retrieved context) so
prompt caching applies to the stable prefix. _Verify: each prompt component is labeled and serves
one purpose; no component is duplicated._

### 3. Select the model

Match the model to the task's quality, latency, and cost profile — don't default to the most
capable model for every call:

- **Complex reasoning / generation:** most capable model, accept higher latency and cost
- **Classification / extraction / routing:** smaller, faster, cheaper model — these tasks are
  over-served by frontier models
- **High-volume, low-stakes:** the cheapest model that meets the quality bar; route edge cases to
  a stronger model (cascaded / routed architecture)
- Evaluate multiple models against the eval harness (step 4) before committing — model choice is
  empirical, not reputational

_Verify: model choice is documented with the eval comparison and the cost/latency/quality
trade-off that justified it._

### 4. Build the eval harness

An eval harness is the test suite for prompts. It runs the prompt against a labeled dataset and
scores the output against the success criteria:

- **Dataset:** 50–200 examples minimum, covering happy path, edge cases, and known failure modes.
  Use real production inputs where possible; synthesize adversarial cases for gaps.
- **Metrics:** automated where possible (exact match, JSON schema validity, BLEU/ROUGE for
  generation, classifier-based safety); human review for quality dimensions automation can't score.
- **Regression suite:** the eval harness runs on every prompt or model change — a prompt tweak
  that improves one case but regresses three others is a bug, not an improvement.

_Verify: the eval harness runs from one command, produces a scorecard, and is committed alongside
the prompt._

### 5. Add guardrails

Production prompts need defenses the prompt itself cannot provide:

- **Input validation:** reject malformed, oversized, or disallowed inputs before they reach the model
- **Output validation:** parse and schema-check model output; reject and retry (or fallback) on
  malformed output
- **Content filters:** safety classifiers for harmful content (input and output)
- **PII redaction:** strip sensitive data from prompts before logging; never log raw user input
  that may contain PII to a shared prompt-logging system
- **Rate limits and cost caps:** bound per-user and aggregate spend; a prompt bug that loops can
  burn a budget in minutes

_Verify: every guardrail has a defined failure behavior (reject, retry, fallback) — silent
pass-through is not a guardrail._

### 6. Iterate against evals

Iterate the prompt against the eval harness — change one variable at a time (instruction,
examples, model, temperature), re-run evals, keep the change only if the scorecard improves
without regression. Document prompt versions and their eval scores alongside the prompt, the way
code commits pair with test results.

**Output:** `docs/design/PROMPT.md` — the prompt design document: task definition, success
criteria, prompt architecture (component breakdown), model selection rationale, eval harness
description and dataset, guardrails, and version history with eval scores.

## Verify

- [ ] Task stated in one sentence; success criteria are measurable thresholds
- [ ] Prompt structured into labeled components (system, instruction, context, examples, format)
- [ ] Stable and variable parts separated for prompt caching
- [ ] Model selected via eval comparison, not reputation; trade-off documented
- [ ] Eval harness: 50+ examples, automated metrics, runs from one command, committed
- [ ] Guardrails on input, output, content, PII, and cost — each with a failure behavior
- [ ] Prompt changes paired with eval re-runs; no regression accepted
- [ ] `docs/design/PROMPT.md` produced with architecture + eval + guardrails + version history

**Red flags:** a single wall-of-text prompt with no structure; choosing the most expensive model
for a classification task; shipping a prompt with no eval; logging raw prompts with user PII; no
output schema validation (trusting the model to always return valid JSON); prompt iteration by
vibes without a scorecard; no cost cap on a production prompt.

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — shared discipline (surface assumptions, verify don't assume, goal-driven execution)
- [references/prompt-architecture.md](references/prompt-architecture.md) — prompt component breakdown, few-shot patterns, structured-output techniques, model selection matrix, eval-harness setup, guardrail catalog
