---
name: sourcing-topup
description: Use when a playbook or sequence is running low on qualified leads, or the user wants to refill the pipeline — check supply against what tomorrow's sends need, then top up sourcing and run enrichment and qualification within a hard credit cap. Reads and dry runs happen immediately; starting a source, a paid column run or a pool import waits for explicit confirmation. Part of the closed loop (see closed-loop); the first station, "find and enrich".
allowed-tools: Bash, Read, Grep, Glob
---

# Sourcing top-up

Station 1 of the closed loop: keep the sequences fed. A sequence with no qualified leads
waiting does not fail — it just goes quiet, and nobody notices until the reply count drops.

Obeys the rules in **`closed-loop`**: reads are free, every source start and paid run is
previewed and waits for a yes. Building the table and its columns in the first place is
**`build-gtm-workflow`**; ready-made motions and their sources are in **`plays`**.

## Inputs

- A playbook or sequence (name or id). If none is named, list the active ones and ask which.

## 1. How much is needed?

- Daily capacity of the sequence: the sum of its senders' limits (`list_senders`).
- A lead receives several steps over its lifetime, so new leads per day ≈ daily capacity ÷
  number of steps. That is the supply tomorrow's send window needs.

## 2. How much is there? (read immediately)

- `workspace_tables_list` / `workspace_table_get` — rows waiting behind the qualification gate
  and the enroll column, not yet enrolled.
- `list_runs` with `source: "table"` or `"sourcing"` — the latest source and column runs: status,
  counts, credits, error.
- `check_sourcing_progress` (needs a `playbook_id`) — only for runs started through the older
  playbook sourcing path; table sources are watched with `list_runs`.
- `workspace_capabilities` — which sources this workspace can run right now (`connected`) and
  which need a connection first (`requires`). A source that cannot run is not a broken source.

If the supply is enough, stop here and say so.

**A sourcing target of zero is often deliberate.** If a playbook's daily sourcing was switched
off, ask whether that is intended before turning it back on.

## 3. Choose the source

Work down your own source ladder: the cheapest and warmest source first, the next one only
when the previous is exhausted or empty. Typical order: your own warm signals (post engagers,
website visitors, inbound), then the workspace's existing data (CRM, lookalikes of won
customers), then the contact pool, then paid search. Write your ladder down once and reuse it —
see `plays` for what each source delivers.

For the contact pool, browse first, import second:

- `search_pool` — read-only filtering (industry, region, size, `has_email`,
  `has_personal_email`, `contact_roles`). Every delivered row counts against the workspace's
  daily pool quota.
- Check a sample of what you would import before importing it.

## 4. Top up (gated)

Mutations, each previewed and confirmed separately:

| Action | Tool |
|---|---|
| Add or schedule a source on a table | `workspace_table_add_source`, `workspace_table_schedule_source` |
| Import from the pool into a playbook | `source_from_pool` |
| Run enrichment / qualification on new rows | `workspace_table_run_column` |

Before every run:

1. `workspace_table_preflight` — the column graph has no dead end, inputs resolve.
2. `workspace_table_run_column` with `mode: "dry_run"` — free; rows and estimated credits.
3. Preview: `playbook · table · source or column · expected rows · estimated credits · cap`.
4. Wait for yes. Then run live with `max_credits` set. **A live paid run without a cap is
   refused by design — never work around it.**
5. Qualification before contact enrichment: the expensive column is gated on the cheap
   column's verdict. Do not enrich rows that will be rejected.
6. No `auto_run` on bulk rows you have not read.

## 5. Verify (the run saying `done` proves nothing)

- `workspace_table_run_health` — per column: succeeded, skipped, failed, and why.
- Read 10–20 rows: are the values real, are the qualification reasons ones you agree with?
- Compare credits used with the estimate. Zero spend on a paid column means nothing ran.
- If a run stalls, stop it (`workspace_table_stop_run`) and report — do not re-fire.

## Output

```
SUPPLY — <playbook / sequence>
  needed per day      <n>  (capacity <n> ÷ <steps> steps)
  waiting, qualified  <n>  (source: workspace_table_get)
  last run            <status> · <rows> · <credits>  (source: list_runs)

PROPOSED TOP-UP
  <source or column> · <expected rows> · est. <credits> · cap <credits>
  → waiting for your yes
```

After a run: rows added, rows qualified, rows rejected (top reasons), credits used, and the
cost per qualified lead.
