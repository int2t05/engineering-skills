# Prompt Architecture

Depth reference for the `prompt-engineering` skill. Component breakdown, few-shot patterns,
structured-output techniques, model selection, eval-harness setup, and the guardrail catalog.

## 1. Prompt component breakdown

Structure the prompt as labeled components, not a wall of text. Each component has one job:

| Component | Job | Stability |
|---|---|---|
| **System / role** | Who the model is; hard rules and constraints | Stable — cacheable |
| **Task instruction** | The operation, output format, edge-case handling | Stable — cacheable |
| **Few-shot examples** | 2-5 input→output pairs demonstrating the contract | Stable — cacheable |
| **Retrieved context / data** | The facts for this specific call | Variable — per-request |
| **User input** | The actual thing to process | Variable — per-request |

**Cache the stable prefix.** Place stable components (system, instruction, examples) before
variable components (retrieved context, user input) so prompt caching applies to the prefix.
Swapping the order breaks caching and multiplies cost.

### Component anti-patterns

- **Instruction buried in context** — the rule the model must follow is lost in a wall of
  retrieved text. Keep instructions at the top, separate from data.
- **Role mixed with task** — "You are a helpful assistant that summarizes..." conflates identity
  with operation. Split: role = "summarizer"; task = "produce a 3-bullet summary."
- **Examples after the input** — few-shot examples must precede the actual input; placing them
  after teaches the wrong pattern.
- **No output format spec** — "summarize this" without stating bullets/paragraph/JSON; the model
  guesses differently each call.

## 2. Few-shot patterns

Few-shot examples teach the contract — the input→output mapping the model should learn. 2-5
examples is the sweet spot; more isn't better (dilutes attention) and fewer under-specifies.

### Example selection

- **Happy path** — the common case (1-2 examples)
- **Edge case** — an input that would trip a zero-shot prompt (empty input, ambiguous input,
  maximum-length input) (1-2 examples)
- **Failure-mode demonstration** — if the model tends to hallucinate a field, include an example
  where the correct output omits or says "unknown" for that field

### Example formatting

Format examples so the boundary between input and output is unambiguous:

```
<example>
<input>Apple reports Q3 revenue of $81.4B, up 5% YoY.</input>
<output>{"company": "Apple", "metric": "revenue", "value": 81.4, "unit": "B", "period": "Q3", "yoy_change": 5}</output>
</example>

<input>{actual input here}</input>
<output>
```

### When few-shot isn't enough

Few-shot teaches pattern, not policy. If the task requires following a complex rule (e.g. "never
infer a value not present in the input"), state the rule explicitly in the instruction AND
demonstrate it in an example. The example without the rule, or the rule without the example,
both under-perform.

## 3. Structured-output techniques

When the downstream system parses the output, use structured output — never parse free text.

### JSON mode / structured output

Most model APIs offer a structured-output mode (JSON mode, function calling, response schema).
Use it. It constrains the output to valid JSON conforming to a schema, eliminating parse
failures.

```
schema = {
  "type": "object",
  "properties": {
    "company": {"type": "string"},
    "metric": {"type": "string"},
    "value": {"type": "number"}
  },
  "required": ["company", "metric", "value"]
}
```

### Output validation (even with structured output)

Structured output guarantees syntactic validity (valid JSON), not semantic validity (the values
are correct). Still validate:

- Required fields present and non-null
- Enum values in the allowed set
- Numeric values in plausible range
- String values under length limits

On validation failure: retry (with the validation error fed back), or fall back — don't pass
invalid output downstream.

## 4. Model selection matrix

Match the model to the task. Don't default to the most capable model — it over-serves simple
tasks and costs 10-100× more.

| Task type | Model tier | Rationale |
|---|---|---|
| Complex reasoning (multi-step logic, code generation, planning) | Frontier / most capable | Needs the reasoning depth; latency and cost justified |
| Generation (long-form writing, creative) | Frontier or upper-mid | Quality matters; cost amortized over output length |
| Classification / categorization | Mid-tier or small | Few categories, clear input — small models classify accurately |
| Extraction (key-value, entity) | Mid-tier or small | Structured output; small models handle defined schemas |
| Routing / triage (which handler?) | Small / fast | Low-latency decision; route to the right specialized model |
| Summarization | Mid-tier | Coherence matters but not frontier-level reasoning |
| High-volume, low-stakes (bulk labeling, dedup) | Smallest viable | Cost dominates; quality bar is "good enough" |

### Cascaded / routed architecture

For mixed workloads, route by complexity:

1. **Fast model** handles the request (cheap, fast)
2. **Confidence check** — if the fast model is uncertain (low logprob, validation fail, explicit
   "I don't know"), escalate to a stronger model
3. **Strong model** handles only the hard minority

This cuts cost dramatically (80% of traffic on the cheap model, 20% on the expensive) while
keeping quality (the hard cases get the strong model).

## 5. Eval-harness setup

The eval harness is the test suite for prompts. Without it, prompt changes are vibes-driven.

### Dataset construction

- **50-200 examples minimum** — smaller sets have too much variance per change
- **Real production inputs** where possible (sampled, PII-stripped)
- **Synthesized adversarial cases** for gaps — inputs designed to trigger known failure modes
- **Class balance** — if 95% of inputs are the happy path, the eval can't measure edge-case
  performance; oversample the edge cases

### Metrics

| Metric | When to use | Automated? |
|---|---|---|
| Exact match | Classification, extraction with a ground truth | Yes |
| JSON schema validity | Structured output | Yes |
| Precision / recall / F1 | Classification with labeled set | Yes |
| BLEU / ROUGE | Generation against a reference | Yes (but weak signal) |
| LLM-as-judge (rubric-scored) | Quality dimensions automation can't score | Semi (requires judge prompt + spot-check) |
| Human review | The ground truth for quality | No — sample, don't score everything |

**LLM-as-judge caveat:** a judge model scoring outputs is useful but biased (prefers outputs
that look like its own style). Spot-check 10-20% of judge scores against human review to
calibrate.

### Regression discipline

- The eval harness runs on every prompt or model change
- A change that improves one case but regresses three is a bug — reject it
- Track the scorecard over time: dataset, prompt version, model, scores per metric
- Version the dataset — adding examples is a change that affects scores; note it

## 6. Guardrail catalog

Guardrails are defenses the prompt itself cannot provide. Layer them at the application boundary.

### Input guardrails

| Guardrail | What it catches | Failure behavior |
|---|---|---|
| **Input validation** (schema, length, charset) | Malformed, oversized, injection-attempt inputs | Reject with 400 before model call |
| **Content classifier** (safety) | Harmful, abusive, or policy-violating input | Reject or route to safe response |
| **PII detection + redaction** | SSN, email, phone in input | Redact before model; log redacted only |
| **Rate limit / cost cap** | Abuse, runaway loops | 429 or hard stop at per-user/aggregate threshold |
| **Prompt-injection filter** | "Ignore previous instructions..." patterns | Sanitize or reject |

### Output guardrails

| Guardrail | What it catches | Failure behavior |
|---|---|---|
| **Schema validation** | Malformed JSON, missing fields | Retry (with error fed back) or fallback |
| **Content classifier** (safety) | Harmful output the model produced | Filter, fallback, log for review |
| **PII filter** (output) | Model leaked PII from context into output | Redact or reject |
| **Hallucination check** | Output asserts a fact not in the source context | Flag or regenerate with stricter grounding |
| **Length / format cap** | Output exceeds downstream limits | Truncate (safely) or regenerate |

### Failure behavior rules

Every guardrail has a defined failure behavior — silent pass-through is not a guardrail:
- **Reject** — return an error, don't call the model (input) or don't return the output (output)
- **Retry** — feed the validation error back to the model and retry once; if it fails again,
  fall back
- **Fallback** — return a safe default ("I can't process this") or route to a human
- **Log** — every guardrail trigger is logged with the input (redacted), the trigger, and the
  action taken — this is how you tune thresholds and find attack patterns
