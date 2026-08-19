---
name: auth-implementation
description: Use when implementing authentication — login, sessions, JWT, OAuth2/OIDC, password hashing, and RBAC/ABAC authorization. Language-agnostic patterns for building auth correctly the first time. Triggers on "implement auth", "password hashing", "OAuth integration", "实现认证", "实现登录", "OAuth 集成", "token 轮换". Not for auditing existing auth for vulnerabilities (use security-review) or designing auth architecture at system level (use architecture).
---

# Auth Implementation

Build authentication correctly the first time. Auth is the #1 place engineers
introduce security holes — this skill gives language-agnostic patterns for
sessions, tokens, OAuth, password hashing, and authorization. It builds what
`security-review` later audits; align terminology with that skill.

## When to use

- Implementing login, session management, token issuance, or password hashing
- Adding OAuth2/OIDC (social login, SSO) or service-to-service authentication
- Building RBAC/ABAC authorization checks (verify ownership, not just auth)
- Choosing session-vs-token strategy and refresh-token rotation for a new app

**Not for:** auditing existing auth for vulnerabilities (use `security-review`); designing the auth architecture at system level (use `architecture`); general implementation workflow (use `implement` — this skill supplies the auth-domain patterns, not the slice/TDD loop).

## Steps

### 1. Choose session vs token

First-party web app with a server you control → **server-side sessions** (httpOnly cookie). API-first, microservices, or cross-domain → **JWT** (stateless). Hybrid (session cookie + access token for API calls) is common and fine. See the decision matrix in [references/token-patterns.md](references/token-patterns.md). Never store tokens in `localStorage`.

### 2. Hash passwords correctly

bcrypt (cost ≥ 12), argon2id (preferred for new systems), or scrypt. These algorithms generate and embed a per-password salt internally — do not roll your own salt. Verify with the library's constant-time compare (`bcrypt.compare`, not `===`). Never MD5, SHA-1, or SHA-256 for passwords — they are too fast to resist brute force.

### 3. Session management (if session-based)

- Cookie flags: `httpOnly` (no JS access), `secure` (HTTPS only), `sameSite=Lax` (or `Strict` for same-site forms).
- Rotate the session ID on login and on any privilege change.
- Set absolute + idle timeout; extend idle on activity.
- Server-side invalidation on logout — delete the session record, do not just clear the cookie.

### 4. JWT (if token-based)

- Claims: `sub` (user id), `exp` (expiry), `iat` (issued), `aud` (audience), `iss` (issuer). Keep claims minimal — the token is visible to the holder.
- Access-token expiry ≤ 15 min. Never put secrets in a JWT payload — it is base64, not encrypted.
- Refresh tokens: long-lived, server-side state, rotated on every use. **Reuse detection**: if a refresh token is presented twice, invalidate the entire chain (both tokens are compromised). See [references/token-patterns.md](references/token-patterns.md).
- Revocation: maintain a denylist (`jti`) for logout-before-expiry and breach response. Stateless JWT cannot be revoked without server state — plan for this.

### 5. OAuth2 / OIDC flows

- **SPAs and mobile:** Authorization Code + PKCE. No client secret in the browser.
- **Service-to-service:** Client Credentials grant, with `private_key_jwt` or mTLS over shared secrets.
- **Implicit flow is deprecated** — do not use it. Token Exchange (RFC 8693) delegates access across services. See [references/oauth-flows.md](references/oauth-flows.md).
- Keep tokens server-side when possible; for SPAs, use a backend-for-frontend (BFF) so tokens stay off the client.

### 6. Authorization checks

Authentication ≠ authorization. "Who are you?" vs "are you allowed?". On every protected endpoint:

- Verify resource ownership: `if (task.ownerId !== req.user.id) return 403` — not just `if (!req.user) return 401`.
- RBAC for role-gated actions (`admin`, `editor`); ABAC when ownership + role are insufficient (e.g., "edit reports in your department").
- Check at the data layer too — never assume the route guard covered it. IDOR (insecure direct object reference) is the #1 access-control bug.

### 7. CSRF and common pitfalls

- **CSRF** (cookie-based auth): send a per-session CSRF token in a header; validate on state-changing requests. `sameSite` reduces but does not eliminate CSRF. Token-based auth (Authorization header) is not CSRF-vulnerable by default.
- **Timing attacks**: use constant-time compare for tokens and secrets. `===` leaks length via response time.
- **Refresh-token reuse**: rotate + detect reuse (Step 4). No reuse detection = a stolen refresh token works forever.
- **Token in URL**: never — URLs land in logs, browser history, and `Referer` headers. Use headers or POST body.
- **Rate-limit auth endpoints**: login, register, password-reset (e.g., 10 / 15 min).
- **Error messages**: "invalid username or password" — do not reveal which field is wrong (user enumeration).

## Verify

- [ ] Passwords hashed with bcrypt / argon2id / scrypt (never plaintext, MD5, or SHA)
- [ ] Tokens and sessions never stored in `localStorage` or client-accessible JS
- [ ] Session cookies carry `httpOnly` + `secure` + `sameSite`
- [ ] Session ID rotated on login and on any privilege change; absolute + idle timeout set; server-side invalidation on logout (delete the session record, not just clear the cookie)
- [ ] Access tokens short-lived (≤ 15 min); refresh tokens rotated with reuse detection
- [ ] Authorization (ownership or role) checked on every protected endpoint — not just authentication
- [ ] Auth endpoints rate-limited; error messages do not leak which field failed
- [ ] OAuth uses Authorization Code + PKCE (or Client Credentials for M2M), never Implicit
- [ ] No tokens in URL parameters or logs

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — discipline every skill shares
- [references/token-patterns.md](references/token-patterns.md) — session-vs-token decision matrix, JWT structure, refresh-token rotation + reuse detection, revocation strategies
- [references/oauth-flows.md](references/oauth-flows.md) — Authorization Code + PKCE, Client Credentials, Implicit deprecation, Token Exchange (RFC 8693)
