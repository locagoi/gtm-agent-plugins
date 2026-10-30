---
name: enroll-outreach
description: Use when qualified leads are waiting and should enter a sequence — review who is ready, prove each lead passes the enrollment gate (suppression, history, rendered copy, pre-send checks), fit the batch to sender capacity, and enroll after an explicit yes. Enrollment is real outbound to real people, so every enrollment and every manual release is previewed and confirmed. Part of the closed loop (see closed-loop); the station between sourcing and replies.
allowed-tools: Bash, Read, Grep, Glob
---

# Enroll outreach

Station 2 of the closed loop: move leads that passed qualification into a running sequence.
**Enrollment is the act that sends.** Creating a sequence sends nothing; enrolling a lead into
an auto-release sequence starts real messages to a real person.

Obeys the rules in **`closed-loop`**. How sequences, the enroll column and dedup work in
detail: **`sequences`** and **`gtm-handoffs`**.

## Inputs

- A sequence (or the playbook that owns it). Default scope: rows that passed the qualification
  gate and are not yet enrolled.

## 1. Who is ready? (read immediately)

- `get_sequence` — channel, steps (**zero steps = nothing will send**), sender, release mode.
- `workspace_table_get` — rows past the gate with the enroll column still empty.
- `list_enrollments` for the sequence — who is already in. Never enroll the same lead twice.

## 2. The gate — four proofs per lead, read at the real data

Only a lead that passes all four is enrollable. Count against the actual cell or record, not
a proxy field.

1. **Suppression clean** — not unsubscribed, not blacklisted (`list_blacklist`). The send path
   checks this again and fails closed, but you should not hand it leads you know will bounce
   off the gate.
2. **History checked** — no earlier conversation, no open deal, not an existing customer
   (`get_lead_intelligence`). Copy never claims a shared history it cannot prove.
3. **Every slot rendered** — `preview_sequence_for_lead` on the lead: no `{{…}}` left, no
   empty fill, no instruction text echoed into the message, salutation correct.
4. **Pre-send checks passed** — `enroll_preflight` for channel readiness and sender
   resolution. A clean preflight is necessary, not sufficient: it does not check suppression
   or dedup.

Report rejections by reason. A lead that fails a proof is held, never "fixed" by loosening
the gate.

## 3. Does it fit the capacity?

- `list_senders` (and `get_sender_pool_health` for LinkedIn) — connected senders, their daily
  limits, what was already sent today.
- If the batch exceeds what the senders can carry in the coming send windows, say so and
  enroll only what fits, unless the user decides otherwise. Reach comes from more senders,
  never from raising a sender's limit.

## 4. Enroll (gated)

Preview, verbatim:

```
ENROLL PREVIEW — <sequence> (<id>)
  channel        <email | linkedin | whatsapp | multichannel>
  sender         <name> · limit <n>/day · used today <n>
  leads          <n> pass the gate · <n> held (reasons)
  release mode   <auto: sending starts on enrollment | manual: enrollments wait for release>
  first send     <when the first step goes out>
  → waiting for your yes
```

Then, after the yes:

| Path | Tool |
|---|---|
| Rows of a table (preferred for batches) | run the terminal enroll column with `workspace_table_run_column` |
| A list of lead ids, any channel | `enroll_sequence` |
| LinkedIn, explicit steps or a single test lead | `enroll_linkedin_sequence` |

On a **manual-release** sequence every enrollment is born paused; that is normal, not a
failure. Releasing (`release_sequence_leads`) is a second, separate send decision — preview
and confirm it on its own.

Pausing or resuming a single enrollment (`set_enrollment_state`) is a mutation too.

## 5. Verify

- Read the enroll cell and `list_enrollments` back — the lead status field can lag.
- `enrolled` / `skipped` / `failed` from the enroll result: `skipped` means already enrolled;
  `failed` names the reason per group. A failure is never a skip.
- Watch the first send window: `list_runs` with `source: "sequence"` and `sequence_log`.
  "Enrolled" is not "sent".

## Output

Eligibility first, then the result:

```
SEQUENCE        PAST GATE   ALREADY IN   HELD (reason)        ENROLLABLE   FITS CAPACITY
<name> (<id>)   <n>         <n>          <n> (suppressed: 3)  <n>          <n>

RESULT  enrolled <n> · skipped <n> (already in) · failed <n> (<reason>)
```
