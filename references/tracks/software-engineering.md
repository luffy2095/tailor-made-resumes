# Track: software engineering

Backend, frontend, full-stack, platform, data and infrastructure engineers.

## Defaults
- Human layout: classic. Photo: off.
- Section order: Summary, Experience, Skills, Education, Professional Development. Projects go after Experience only when experience is under three years or the projects are stronger than the jobs.
- Numbers recruiters expect: latency (p50, p99), throughput, error rate, uptime, cost, team size, scale (users, requests, rows, cities).

## Proof to ask for in discovery
- What did you own end to end? What broke on your watch and what did you change?
- One design decision you would defend, and the alternative you rejected.
- On-call: how often, worst incident, what you changed afterwards.
- Public proof: GitHub, talks, posts, open-source contributions.

## Keyword bank by specialisation
- **Backend**: distributed systems, API design, idempotency, caching, queues, event streaming, PostgreSQL, data modelling, concurrency, observability.
- **Frontend**: React, TypeScript, accessibility, performance (Core Web Vitals), design systems, state management, testing.
- **Platform and infrastructure**: Kubernetes, Terraform, CI/CD, SRE, SLOs, incident response, cost optimisation, security hardening.
- **Data**: ETL, data warehouse, dbt, Spark, Airflow, data quality, streaming, SQL performance.

## Cheat sheet focus
- **What this job is**: the system they own and its failure modes.
- **Core metrics**: SLOs, error budgets, latency percentiles, through one on-call morning.
- **Worked story**: a design trade-off with numbers (two options, the cost of each).
- **FAQs**: one system design question, one debugging story, one behavioural, one on the company's domain.
- **TRAPs**: averages instead of percentiles, check-then-insert races, retries without idempotency, "it scales" without a number.

## Common LEARN gaps and topic sheets
- A language the JD prefers (Go, Rust, Java): "<language> for <current language> engineers".
- Domain knowledge (payments, ads, healthcare data): a domain topic sheet in the candidate's own system terms.
- System design at the next level: "System design through your own service".
