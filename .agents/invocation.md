# Invocation

- Model-invoked skills: the host may select them when their concise intent matches the task; the human can also invoke them.
- User-invoked skills: `disable-model-invocation: true` in SKILL.md pairs with `policy.allow_implicit_invocation: false` in the generated Codex adapter.

`brainstorm` and `handoff` are user-invoked. Do not initiate an interview or transfer simply because a task could benefit from one.
Claude Code uses `/skill-name` (or its plugin-qualified name); Codex uses `$skill-name`. Other hosts follow their own invocation mechanism.
Read an applicable skill's instructions using the tools the host provides. Do not require a specific Skill or Agent API in portable workflow instructions.

## Resources

Source skills link their references relative to their actual folder. Shared files live at the repository root; the standalone installer bundles reachable dependencies and rewrites links.
Cross-skill references provide optional knowledge; they do not authorize independent tasks, new documents, delegation, commits or remote publication.
Keep metadata and adapters synchronized with `python scripts/gen-agents-yaml.py` and verify actual installation with the test suite.
