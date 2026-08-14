# OAuth2 / OIDC Flows

Reference for the `auth-implementation` skill. Covers the flows you will actually
implement: Authorization Code + PKCE (SPAs / mobile), Client Credentials
(service-to-service), why Implicit is deprecated, and Token Exchange for
delegation. Language-agnostic; library and provider names are examples.

## Contents

- [Authorization Code + PKCE (SPAs, mobile)](#authorization-code--pkce-spas-mobile)
- [Client Credentials (service-to-service)](#client-credentials-service-to-service)
- [Implicit flow — deprecated](#implicit-flow--deprecated)
- [Token Exchange (RFC 8693)](#token-exchange-rfc-8693)
- [OIDC: authentication vs OAuth2 authorization](#oidc-authentication-vs-oauth2-authorization)

## Authorization Code + PKCE (SPAs, mobile)

The only correct flow for browser and mobile apps that cannot keep a client
secret. Two legs: the user authorizes at the authorization server (AS), the app
receives a temporary **code**, then exchanges the code for tokens at the token
endpoint.

```
1. App generates code_verifier (random 43-128 chars) + code_challenge = SHA256(verifier)
2. Redirect:  https://as/authorize?response_type=code&client_id=...&redirect_uri=...
              &code_challenge=...&code_challenge_method=S256&scope=openid+profile
3. User logs in at AS, consents -> AS redirects back with ?code=XYZ
4. App POSTs to token endpoint:
     grant_type=authorization_code
     code=XYZ
     redirect_uri=...
     client_id=...
     code_verifier=<original verifier>      # AS checks SHA256(verifier) == stored challenge
5. AS returns: { access_token, refresh_token, id_token (OIDC) }
```

**Why PKCE:** without it, a malicious app on the same device can intercept the
`code` from the redirect and exchange it (it knows the public `client_id`). PKCE
proves the code-exchanger is the same party that started the flow — only the
originator knows `code_verifier`.

- `client_id` is public for SPAs. **No `client_secret` in the browser** — it cannot be kept secret.
- Validate `redirect_uri` exactly (no wildcard) — it is the binding that prevents code injection.
- Use `state` (CSRF protection for the redirect) and `nonce` (replay protection for the `id_token`).

## Client Credentials (service-to-service)

Machine-to-machine, no user. The service is the resource owner.

```
POST /token
  grant_type=client_credentials
  client_id=service-a
  client_secret=...            # or mTLS / JWT assertion (private_key_jwt)
  scope=read:metrics
-> { access_token (no refresh_token, no id_token) }
```

- No user → no `refresh_token`, no `id_token`. The access token represents the service itself.
- **Secret rotation:** secrets leak. Prefer `private_key_jwt` (asymmetric) or mTLS over shared secrets — a stolen public key is useless, a stolen shared secret is not.
- **Scope:** grant the minimum the service needs. `read:metrics`, not `*`.

## Implicit flow — deprecated

Implicit (`response_type=token`) returned the access token directly in the URL
fragment of the redirect. **Do not use it.** Deprecated in OAuth 2.1 and OIDC
because:

- Tokens in URLs leak via browser history, `Referer`, and server logs.
- No PKCE — no proof the token recipient started the flow.
- No refresh tokens — every expiry needs a full re-auth.

Replace with Authorization Code + PKCE for all browser and mobile clients.

## Token Exchange (RFC 8693)

Delegation: exchange one token for another with reduced scope or a different
audience. "I have a token for Service A; I need a token for Service B."

```
POST /token
  grant_type=urn:ietf:params:oauth:grant-type:token-exchange
  subject_token=<A's token>
  subject_token_type=urn:ietf:params:oauth:token-type:access_token
  audience=service-b
  scope=read:service-b
-> { access_token (for Service B, scoped down) }
```

Use cases:

- **Token trading:** frontend calls a gateway → gateway exchanges for a downstream service token.
- **Scope reduction:** broad token in → narrow token out (least privilege per hop).
- **Cross-system:** external IdP token → internal service token.

## OIDC: authentication vs OAuth2 authorization

OAuth2 is authorization (delegated access to APIs). OIDC is authentication (who
is the user) layered on OAuth2 — it adds the `id_token` (a JWT with user
identity claims) and the `/userinfo` endpoint.

- **`id_token`:** JWT with `sub`, `email`, `name`, `email_verified`. Validate `iss`, `aud`, `exp`, and `nonce` before trusting it.
- **`access_token`:** for calling APIs (authorization). Do not parse it as user identity — use `id_token` / `/userinfo` for that.
- **`refresh_token`:** for getting new access tokens. Treat as a long-lived credential; store server-side or in secure storage.

Confusing the access token for identity (parsing its payload to get the user) is
a common bug — an access token authorizes an API call, it does not prove who the
user is. Use `id_token` or `/userinfo` for identity.
