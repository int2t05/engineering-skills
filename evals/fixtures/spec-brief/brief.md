# Notification system — product brief

We want to add user notifications. When a user receives a message, they should
get notified. That's the core of it.

## What we know
- Users have a mailbox (already exists).
- We already send transactional email (password reset, etc.) via our email
  provider.
- The app has both a web client and a mobile app.

## Unknowns (do not resolve these by assumption — surface them)
- Which channels? Email, push, in-app, SMS — some combination, unclear which.
- Delivery guarantees: is "best effort" acceptable, or must notifications be
  durable/retried?
- User preferences: can users mute specific notification types? Per-channel?
- Frequency: do we batch/digest, or send each notification immediately?
- Scaling: current user base is 50k; do we need to design for 10x?
- What counts as a "message"? DMs only, or also @mentions, group activity?

## Constraints
- Must not block the existing mailbox write path.
- Email provider has a 100 msg/sec rate limit.

Produce a spec. Surface the decisions above; do not implement them by assumption.
