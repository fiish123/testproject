# Admin Console

A small Flask service used by the support team at a SaaS company. It bundles
the day-to-day tools the on-call operator needs: customer lookup, order
review, report-export preview, webhook testing, connectivity diagnostics, and
a lightweight login/session flow.

## Layout

- `web.py` — HTTP routes (the operator-facing API).
- `db.py` — customer and order database access.
- `storage.py` — report export file access.
- `clients.py` — outbound HTTP and diagnostic clients.
- `ops.py` — low-level shell wrappers for diagnostics.
- `auth.py` — session, credential, and feature-flag helpers.
- `config.py` — runtime settings and integration credentials.

## Run

    flask --app admin_console.web run

## Scan with the analyzer

    python -m analyzer.cli scan tests/admin_console
