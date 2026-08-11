# Code Explanation and Codebase Tours

Sub-guide for the `context-engineering` skill. Use when the goal is helping a
**person** understand existing code — not feeding the agent for implementation.

## When to use this sub-guide

- "Explain how this module works."
- "Walk me through the codebase."
- "What does this function do, and why is it written this way?"
- Onboarding a new contributor to an unfamiliar area.

## When NOT to use

- Feeding context to the agent itself for implementation — that's the main
  `context-engineering` flow, not explanation.
- Changing the domain model or ubiquitous language — use `domain-modeling`.
- Deepening or refactoring modules — use `codebase-design`.

## Steps

1. **Ask what level the reader needs.** "Architecture overview" (how parts
   fit) vs "mechanism" (how a specific function behaves) vs "intent" (why it
   exists this way). Default to architecture, then drill down where asked.
2. **Trace entry points, not every file.** Start from the system boundary —
   the HTTP handler, CLI entry, or event subscriber — and follow the main path
   to the data store. Name the functions you pass through, with file:line.
3. **Build a map before the narration.** A short ASCII or mermaid diagram of
   the components and their dependencies anchors the reader before prose.
4. **Explain the why, not just the what.** Surface non-obvious decisions:
   why a queue sits between two services, why a field is denormalized, why a
   retry lives here and not there. If the reason isn't discoverable from code,
   say so — don't invent it.
5. **Clarify jargon inline.** First use of a domain or framework term gets a
   one-line plain-language explanation.
6. **Connect to the domain model.** If the codebase has a `CONTEXT.md` or
   ubiquitous-language doc, link terms to it. If a term in code conflicts with
   the domain model, flag it — that's a `domain-modeling` issue.

## Output shape

- A map (diagram) up top.
- A numbered trace through the main path, each step naming the function and
  its file.
- A short "why it's this way" section for non-obvious decisions.
- Pointers to deeper material (ADRs, specs) by path, not summaries of them.

## When to escalate

- The reader wants to *change* the model → `domain-modeling`.
- The reader wants to *refactor* the structure → `codebase-design`.
- The explanation reveals a bug → `debugging`.

## Verify

- The reader can name the main path from entry point to data store.
- Every function in the trace has a file:line reference.
- Non-obvious decisions have a stated reason (or are marked "reason unclear").
- No invented rationale — gaps are named, not filled.
