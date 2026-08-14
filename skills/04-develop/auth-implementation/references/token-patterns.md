# Token & Session Patterns

Reference for the `auth-implementation` skill. Covers the session-vs-token
decision, JWT structure, refresh-token rotation with reuse detection, and
revocation strategies. Language-agnostic; library names (bcrypt, jsonwebtoken,
jose) are examples, not endorsements.

## Contents

- [Session vs token decision matrix](#session-vs-token-decision-matrix)
- [JWT structure](#jwt-structure)
- [Refresh-token rotation + reuse detection](#refresh-token-rotation--reuse-detection)
- [Revocation strategies](#revocation-strategies)
- [Storage: where tokens live](#storage-where-tokens-live)

## Session vs token decision matrix

| Factor | Server-side session | JWT (stateless) |
|---|---|---|
| State | Server store (DB / Redis) | None — claims carry state |
| Scaling | Needs shared session store behind LB | Works across services, no shared store |
| Revocation | Delete session record — immediate | Needs denylist (jti) — partial state |
| Best for | First-party web app, single server | API-first, microservices, cross-domain |
| CSRF risk | Yes — needs CSRF token | No (Authorization header) |
| Logout | Server-side delete + clear cookie | Delete client token + denylist jti |
| Size | Cookie ~20 bytes | JWT 500–1000+ bytes |

**Hybrid:** session cookie for the web UI + short-lived JWT access token for API
calls from the same origin. Common and fine — the cookie authenticates the
browser session, the token authorizes API requests.

## JWT structure

Three base64url parts separated by `.`: `header.payload.signature`.

```
header    = { "alg": "RS256", "typ": "JWT" }
payload   = { "sub": "u123", "exp": 1700000000, "iat": 1699999100,
              "aud": "api", "iss": "auth.example.com", "jti": "..." }
signature = RS256(header + "." + payload, private_key)
```

- **alg**: RS256 / ES256 (asymmetric, preferred) or HS256 (shared secret). Reject `alg: none` — unsigned tokens are a known vulnerability; verify the algorithm on decode, do not trust the header.
- **sub**: user identifier. **jti**: unique token id (for revocation). Keep claims minimal — the payload is base64, readable by anyone holding the token.
- **exp / iat**: expiry and issued-at (epoch seconds). **aud / iss**: audience and issuer — validate both on receipt to prevent a token minted for one service being replayed against another.
- The payload is **not encrypted**. Never put secrets, PII, or passwords in a JWT. If confidentiality is required, encrypt separately (JWE) — but usually you do not need to; keep sensitive data server-side and look it up by `sub`.

## Refresh-token rotation + reuse detection

Access tokens are short-lived (≤ 15 min). Refresh tokens are long-lived
(days–weeks) and exchange for new access tokens. **Rotation** means every
refresh issues a new refresh token and invalidates the old one.

```
client --(old refresh token)--> server
server: verify → issue (new access + new refresh) → invalidate old refresh
client <--(new access + new refresh)-- server
```

**Reuse detection:** if the same refresh token is presented twice, the first use
already rotated it. The second presentation means an attacker stole a copy.
Action: invalidate the **entire chain** — every refresh token descended from the
original login session — because you cannot distinguish the legitimate user from
the attacker at that point.

Server-side state required:

1. Store refresh tokens in a table: `(token_hash, user_id, family_id, rotated_to, revoked)`. Hash the token — never store it plaintext.
2. On refresh: verify `token_hash` matches an unrevoked row; issue a new pair; set the old row `rotated_to = new_jti`, `revoked = true`.
3. On reuse: a presented token whose row is already `revoked` (and `rotated_to` exists) → revoke every token sharing that `family_id`.

Without reuse detection, a stolen refresh token works until natural expiry.

## Revocation strategies

Stateless JWT cannot be revoked without server state. Options, weakest first:

- **Short expiry + accept the gap.** 15-min access tokens. On logout, delete the client token. The exposure window after logout is ≤ 15 min. Acceptable for low-security surfaces.
- **Denylist (jti).** Maintain a set of revoked `jti`s with TTL = remaining token lifetime. Check on every request. O(1) lookup; the set is small (only logout-before-expiry + breach tokens).
- **Token versioning.** Store a `token_version` on the user record; bump it on password change or forced logout. The JWT carries the version; mismatch → reject. Invalidates all of a user's tokens at once.
- **Refresh-token revocation.** Refresh tokens have server state — revoke the row directly. This is the primary lever; access-token revocation is secondary.

## Storage: where tokens live

- **httpOnly cookie:** preferred for browser apps. No JS access → survives XSS token theft. Requires CSRF protection.
- **Authorization header (`Bearer`):** preferred for API / mobile. Not in URL, not in logs (if you redact). Client must store securely (OS keychain / secure storage, or an httpOnly cookie via a BFF).
- **Never `localStorage` / `sessionStorage`:** readable by any JS on the page → XSS steals tokens. This is the most common JWT mistake.
- **Never URL query param:** URLs land in server logs, browser history, and `Referer` headers.
