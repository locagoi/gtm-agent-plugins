---
name: health-check
description: Use when the user asks "how is everything doing", wants a status snapshot of the workspace, or before any change to a running campaign. Read-only — reports active playbooks and sequences, what actually went out against capacity, silent failures (runs that say done and delivered nothing), sender and inbox health, reply flow and open platform issues, as one table with a green/yellow/red verdict per sequence. Never mutates; hands findings to the loop skill that owns the fix. Part of the closed loop (see closed-loop).
allowed-tools: Bash, Read, Grep, Glob
---

# Health check

The gauge of the closed loop. It answers one question — **is anything broken or silently
stalled right now?** — and changes nothing. Run it before acting on a live campaign and after
every change, so you can tell whether the change helped.

Obeys the rules in **`closed-loop`**. This skill is read-only: if the user wants to act on a
finding, hand off to the skill that owns that fix and its confirmation gate.

## Inputs

- Nothing → the whole workspace, all active playbooks and sequences.
- A playbook or sequence name → just that one.
- Window: last 7 days unless the user names another.

## Procedure

### 1. Inventory — complete, not truncated

- `list_playbooks` — what is in service. A playbook marked live whose sequence is archived or
  empty is a dead entry: note it, do not count it.
- `list_sequences` — compare the rows you received with the reported `total`. If they differ,
  stop and say the inventory is incomplete; never judge on a cut list.
- `get_sequence` per active sequence — channel, steps, sender, release mode. **A sequence with
  zero steps sends nothing and reports no error.** Check this every time.
- Use full ids from the tool results. A shortened id returns "not found", which is not the
  same as "does not exist".

### 2. Is it actually sending?

- `list_runs` with `source: "sequence"` — per dispatcher tick: what came due, what was sent,
  where the rest went (`resultCounts`). Check `dry_run`: a dry tick reports what it *would*
  have sent. No row means nothing was due **or** the dispatcher is not running —
  `list_enrollments` tells the two apart.
- `sequence_log` with `only_failures: true` — who failed, at which step, and why.
- `list_sequence_standstills` — LinkedIn sequences standing still, with the reason.
- `get_campaign_stats` — sends and replies, including campaigns of a connected outbound tool.
  It can be cumulative; do not read a total as a daily figure.
- Set what went out against capacity (sum of the sender limits from `list_senders`; for
  LinkedIn the weekly invite limit spread over the working days).

### 3. Silent failures — the ones that never raise an error

Count and name each:

- an enrollment finished or failed with an error (`list_enrollments` by status)
- unresolved `{{slots}}` in rendered copy — check `preview_sequence_for_lead` on two sample
  leads per sequence
- enrollments waiting for a manual release nobody gave
- a sender cooling down, disconnected or at its limit (`list_senders`,
  `get_sender_pool_health`)
- enrollments `active` with no progress over more than one send window
- a table column whose last run skipped most rows (`workspace_table_run_health`)

If a tool does not return the field you need (for example no error text, no step progress),
that is a measurement gap — report it as "not measurable", never as "0 errors".

### 4. Deliverability and replies, in one line each

- `get_deliverability_health` — inbox status, bounce and reply rates, and the domain block
  (SPF, DMARC, DKIM findings). Read the timestamp: the values are from the last monitoring run.
  The full diagnosis belongs to **`deliverability`**.
- `list_replies` — how many replies are waiting for a decision. The handling belongs to
  **`reply-triage`**.

### 5. What the platform already knows

- `list_system_issues` — defects the platform has recorded for this workspace (integration
  failures, enrollment errors, sync problems). Read before proposing a fix; it may already be
  named.
- `get_tool_health` — which tool calls are failing and whether the call was built wrong
  (`validation`) or the product is broken (`bug` → `report_issue`, do not retry).

## Verdict per sequence

Decide your bar before reading the numbers (see `closed-loop` rule 4), then:

- **green** — sending at the level you planned, no silent failures
- **yellow** — below plan with a named reason and a named next step
- **red** — a silent failure, or below plan with no explanation

## Output

```
HEALTH — <workspace> — <date> — window <n> days

NEEDS ATTENTION
  1. <finding> — <owning skill>
  2. …

SEQUENCE            CHANNEL   SENT / CAPACITY   SILENT FAILURES   VERDICT
<name> (<id>)       email     <n> / <n>          <n>: <top cause>  red
…

SENDERS        <healthy>/<total> healthy · <disconnected> disconnected · <cooling down>
DELIVERABILITY <one line from get_deliverability_health, with its timestamp>
REPLIES        <n> waiting for a decision
PLATFORM       <open issues> · <failing tools>
NOT MEASURABLE <what could not be read, and why>
```

Name the tool behind every number. List anything you skipped (and why) instead of silently
leaving it out.
