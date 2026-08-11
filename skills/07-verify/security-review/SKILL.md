---
name: security-review
description: Use when reviewing changes for security — secrets, auth, injection, access control, and hardening. Triggers on "security review", "check for vulnerabilities", "安全审查", "安全审计", "漏洞检查".
---

## When to use

- Reviewing a change that touches user input, auth, or data storage
- A feature accepts untrusted data, manages sessions, or integrates with external services
- Adding file uploads, webhooks, callbacks, or payment/PII handling
- Before merge on any security-sensitive change
- Triggers on "security review", "check for vulnerabilities", "安全审查", "安全审计", "漏洞检查"

**Not for:** general code quality review (use `code-review`); performance profiling (use `performance`).

## Steps

### 1. Threat model first

Controls bolted on without a threat model are guesses. Before reviewing hardening, spend five minutes thinking like an attacker:

1. **Map trust boundaries** — HTTP requests, form fields, file uploads, webhooks, third-party APIs, message queues, **LLM output**. Every boundary is attack surface.
2. **Name the assets** — credentials, PII, payment data, admin actions, money movement.
3. **Run STRIDE** per boundary — Spoofing (auth, signature verification), Tampering (integrity, parameterized queries, HTTPS), Repudiation (audit logging), Information disclosure (encryption, field allowlists, generic errors), Denial of service (rate limiting, size caps, timeouts), Elevation of privilege (authorization checks, least privilege).
4. **Write abuse cases next to use cases** — "how would I misuse this?" is your first test.

If you can't name the trust boundaries for a feature, it's not ready to secure (OWASP A04: Insecure Design — most breaches begin in design, not code).

### 2. Check the three-tier boundary system

**Always do (no exceptions):**
- Validate all external input at the system boundary (API routes, form handlers)
- Parameterize all database queries — never concatenate user input into SQL
- Encode output to prevent XSS (use framework auto-escaping, don't bypass it)
- HTTPS for all external communication
- Hash passwords with bcrypt/scrypt/argon2 (salt rounds ≥ 12, never plaintext)
- Security headers: CSP, HSTS, X-Frame-Options, X-Content-Type-Options
- httpOnly, secure, sameSite cookies for sessions
- Run the package manager's native audit against the committed lockfile before every release

**Ask first (human approval):** new auth flows or auth-logic changes; new sensitive-data categories (PII, payment); new external service integrations; CORS config changes; file upload handlers; rate-limiting/throttling changes; elevated permissions or roles.

**Never do:** commit secrets to version control; log sensitive data (passwords, tokens, full card numbers); trust client-side validation as a security boundary; disable security headers for convenience; `eval()` or `innerHTML` with user-provided data; store sessions in client-accessible storage (localStorage for auth tokens); expose stack traces or internal error details to users.

### 3. Walk the OWASP Top 10 prevention patterns

For each, check the diff for the bad pattern and confirm the good one is in place:

- **Injection** (SQL/NoSQL/OS command) — parameterized queries or ORM with parameterized input. No string concatenation of user input into queries or shell commands.
- **Broken authentication** — bcrypt/scrypt/argon2 hash and compare; session secret from environment (not code); httpOnly + secure + sameSite cookies with explicit maxAge; password reset tokens expire.
- **XSS** — framework auto-escaping (React escapes by default); if you must render HTML, sanitize first (DOMPurify). No `innerHTML` with user data.
- **Broken access control** — check authorization, not just authentication. Verify resource ownership (`task.ownerId !== req.user.id` → 403). Admin actions require admin role verification. Users can only access their own resources.
- **Security misconfiguration** — helmet for headers; CSP with tight directives (`defaultSrc 'self'`); CORS restricted to known origins (never wildcard `*` with credentials). No default credentials.
- **Sensitive data exposure** — field allowlist in API responses (strip `passwordHash`, `resetToken`); secrets from environment variables; PII encrypted at rest if applicable.
- **SSRF** — for server-side URL fetches (webhooks, import-from-URL, image proxies, link previews): allowlist scheme + host, reject if any resolved IP is private/reserved (covers loopback, link-local `169.254.169.254` cloud metadata, private, unique-local across IPv4/IPv6), forbid redirects. TOCTOU gap remains — for high-risk surfaces, pin the resolved IP or use a filtering agent (`request-filtering-agent`).

### 4. Input validation + file uploads

Schema validation at boundaries (e.g. zod): validate at the route handler, return 422 with `VALIDATION_ERROR` on failure. File uploads: restrict MIME types and size; don't trust the file extension — check magic bytes if critical.

### 5. Rate limiting

General API rate limit (e.g. 100 req / 15 min). Stricter limit on auth endpoints (e.g. 10 attempts / 15 min). `standardHeaders: true`, `legacyHeaders: false`.

### 6. Dependency + supply-chain hygiene

Find the installation boundary first: use the workspace root that owns the lockfile; corroborate `packageManager` (when present), the lockfile, and CI; stop on disagreement or competing lockfiles.

Triage audit findings by **reachability** and **fix risk**, not just severity:

- Critical/high + reachable in runtime/build/deploy → fix immediately (update, patch, or replace).
- Critical/high + confirmed unused across all paths → fix soon, not a blocker.
- Moderate + reachable in prod → next release cycle. Dev-only → backlog.
- Low → track and fix during regular dependency updates.

Never `npm audit fix --force` (or equivalent) — preview the remediation, read changelogs, test each upgrade; forced fixes may cross declared dependency ranges. Verify registry signatures/provenance where supported (`npm audit signatures`); treat absence as a signal to investigate. Review new dependencies, lockfile diffs, and script-policy changes together — ownership, maintenance, release age, provenance, transitive graph, typosquats (`cross-env` vs `crossenv`, OWASP A06, LLM03). Block dependency install scripts unless explicitly approved; bootstrap with scripts disabled.

### 7. Secrets management

`.env.example` committed (template with placeholders); `.env` / `.env.local` NOT committed and in `.gitignore` (`*.pem`, `*.key` too). Before committing, check staged diff for `password|secret|api_key|token`. **If a secret is ever committed, rotate it** — deleting the line or rewriting history is not enough. Revoke and reissue the key first, then purge it from history. Assume it's compromised the moment it reaches a remote.

### 8. AI / LLM features (if present)

Map to the OWASP Top 10 for LLM Applications:

- **LLM05** (Improper Output Handling) — treat all model output as untrusted input. No `eval`, SQL, shell, `innerHTML`, or file path from model output without validation and encoding. Parse defensively, validate against a schema, then encode.
- **LLM01** (Prompt Injection) — assume prompts can be hijacked. Untrusted text in the context window can carry instructions. The system prompt is not a security boundary; enforce permissions in code.
- **LLM02 / LLM07** — keep secrets and other users' data out of prompts. Anything in the context can be echoed back.
- **LLM06** (Excessive Agency) — scope tool/agent permissions to the minimum; require confirmation for destructive or irreversible actions; validate every tool argument.
- **LLM10** (Unbounded Consumption) — cap tokens, request rate, and loop/recursion depth.
- **LLM08** (Vector and Embedding Weaknesses) — in RAG, partition embeddings per tenant so one user can't retrieve another's data; validate documents before indexing.

## Red flags

- User input passed directly to database queries, shell commands, or HTML rendering
- Secrets in source code or commit history
- API endpoints without authentication or authorization checks
- Missing CORS configuration or wildcard (`*`) origins with credentials
- No rate limiting on authentication endpoints
- Stack traces or internal errors exposed to users
- Dependencies with known critical vulnerabilities; competing lockfiles at one installation boundary; non-reproducible installs; blanket-approved install scripts
- Server fetches user-supplied URLs without an allowlist (SSRF)
- LLM/model output passed into a query, the DOM, a shell, or `eval`
- Secrets, PII, or the full system prompt placed inside an LLM context window

**Output:** `docs/security-report.md` — findings by severity, with runtime/build/deploy reachability and the fix or accept rationale per finding.

## Verify

- [ ] Native audit has no unmitigated reachable critical/high findings; CI preserves the authoritative lockfile and blocks unreviewed dependency scripts
- [ ] No secrets in source code or git history
- [ ] All user input validated at system boundaries
- [ ] Authentication and authorization checked on every protected endpoint
- [ ] Security headers present in response (CSP, HSTS, X-Frame-Options, X-Content-Type-Options)
- [ ] Error responses don't expose internal details / stack traces
- [ ] Rate limiting active on auth endpoints
- [ ] Server-side URL fetches validated against an allowlist (no SSRF)
- [ ] LLM/model output validated and encoded before use (if AI features present)

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — discipline every skill shares
- [references/owasp-patterns.md](references/owasp-patterns.md) — OWASP Top 10 prevention code examples (injection, auth, XSS, access control, SSRF, validation, rate limiting, LLM output).
