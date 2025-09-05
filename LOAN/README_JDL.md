# LOAN Notification JDL

This folder contains a JHipster JDL to generate a backend monolith for the LOAN notification and reminder features. The frontend is developed separately, so generation skips the client code.

## Sources Analyzed

Derived from:
- https://github.com/PNTSOL/LMA_BACKEND/issues/7: unique email as login, Google sign-in metadata, registered vs. guest users.
- https://github.com/PNTSOL/LMA_BACKEND/issues/4: campaigns, multi-channel (Email | Push | In-app), templates, activation, send-now flows, history logging, device tokens with platform.
- https://github.com/PNTSOL/LMA_BACKEND/issues/5: daily scheduled reminder before due date, configurable schedule and limits, template caching, logging history.

## Model Overview

Key enums:
- `NotificationChannel`: EMAIL, PUSH, IN_APP
- `SendStatus`: PENDING, SUCCESS, FAILED
- `Platform`: ANDROID, IOS, WEB
- `AudienceType`: REGISTERED, UNREGISTERED

Key entities and relations:
- `CustomerProfile` 1–1 `User` (JHipster built-in user), holds profile and registration markers.
- `DeviceToken` many per `CustomerProfile`, stores device/platform and optional email/username/loanCode snapshots to detect registration per rules.
- `NotificationCampaign` with activation flags per channel and template fields per channel, 1–many `NotificationHistory`.
- `NotificationHistory` stores per-send record with recipient snapshots and channel/status.
- `ReminderConfig` stores scheduler parameters (enabled, run time, daysBeforeDue, maxReminders).
- `ReminderHistory` stores reminder sends with template snapshots, linked to `CustomerProfile` and `NotificationCampaign`.

See `loan-notification.jdl` for full spec.

## Generation Instructions

Backend (monolith, skip client):

```bash
jhipster import-jdl loan-notification.jdl
```

Notes:
- `skipClient true` in the JDL keeps the frontend separate.
- Authentication set to `jwt` by default; adjust if using OAuth2.
- Database defaults to Postgres in prod and H2 for dev.

## Mapping from Business Rules
- Unique email as login: handled by `User`; `CustomerProfile` links 1–1 to `User`.
- Registered vs. unregistered: `AudienceType` in campaigns; `DeviceToken` includes `email/username/loanCode` to infer registration.
- Channels and template constraints: per-channel fields in `NotificationCampaign`; `imageUrl` supports media when applicable.
- Send history and reminder history: `NotificationHistory` and `ReminderHistory` capture channel, status, timestamps, and snapshots.
- Scheduler parameters: `ReminderConfig` holds schedule and limits.

## Next Steps
- Implement schedulers and messaging/integration logic in service layer after generation.
- Integrate Firebase/APNs for push and email provider for email.
- Expose APIs required by separate frontend.
