# Dossier: Ria Kapoor (fictional)

Approved by the candidate: 2026-10-20. Every resume and cheat sheet is derived from this file.
Nothing goes on a document unless it is here.

## Contact
- Bengaluru, India. ria.kapoor@example.com. +91 90000 00000. example.com/ria

## Preferences
- Track: software-engineering. Seniority: individual contributor, targeting senior.
- Human layout: classic. Accent: navy. Photo: off.
- Confidential metrics: no. Numbers from her own work may appear.
- Location: Bengaluru or remote. Timeline: applying now.

## Roles
### Backend Engineer II, Tiffinly, Bengaluru. Jul 2023 to present
- Owns the order-dispatch service that assigns riders to orders in 14 cities. Python, PostgreSQL, Redis, Kafka, AWS.
- Added idempotency keys with a unique constraint to rider-assignment retries. Duplicate assignments during network timeouts stopped.
- Led the incident response for the Diwali-eve dispatch backlog. Wrote the postmortem and the Kafka consumer backpressure fix.
- Her Diwali-eve postmortem was adopted as the team's incident template.
- Cut p99 latency of the assignment API from 900 ms to 240 ms by moving rider lookups to a Redis geo index.
- Built the nightly reconciliation of rider payouts against the payouts ledger. Mismatches open a ticket with the rider ID and amount.

### Backend Engineer I, Tiffinly, Bengaluru. Jul 2021 to Jun 2023
- Built the refund flow for cancelled orders, including partial refunds when only some items were cancelled.
- Joined the on-call rotation in month six. Wrote four of the team's runbooks.

## Education
- B.Tech, Computer Science, Example Institute of Technology, 2021.

## Systems actually used
- Python, Go (reading level only, not production), PostgreSQL, Redis, Kafka, AWS (ECS, RDS, SQS), Docker, Grafana, PagerDuty.

## May not claim
- Production Go. Payment gateway integration. PCI-DSS work. Any certification.

## Stories for interviews
- **Duplicate rider assignment**: a retry after a timeout assigned two riders. Fix was an idempotency key per assignment intent with a unique constraint.
- **Diwali-eve backlog**: consumer lag hit 40 minutes. Fix was backpressure plus a priority lane for orders already paid.
- **Payout reconciliation**: three buckets, matched, ours only, theirs only. Every break gets a ticket with an age.

## In progress
- Go, through the Go tour and a small CLI. Started 2026-10.
- Payment systems and double-entry ledgers, through the topic cheat sheet.
