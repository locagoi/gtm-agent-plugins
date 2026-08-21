---
name: sequences
description: Use when building or changing the touch plan a lead experiences over time — sequence steps and delays, the seven step kinds, slot copy, sender binding and daily limits, enrollment, branching, and the stop rules. Covers email, LinkedIn and WhatsApp. Read copy-patterns.md next to this file for the per-step copy structure. For the table that feeds the sequence use build-gtm-workflow; for how the handoff is wired use gtm-handoffs.
allowed-tools: Bash, Read, Grep, Glob
---

# The sequence: the touch plan a lead walks

A Sequenz is the **time** dimension of the three automation nouns — Tabelle is per row,
Workflow is per event, Sequenz is what one lead experiences over days. Ordered steps, delays
between them, copy with slots, and a per-lead enrollment state.

**Nothing sends when you create one.** Sends begin only on **enrollment**. This is the single
most useful fact about sequences and the one most often misread as "it isn't working".

## The shape

```bash
gtm call create_sequence --input '{
  "playbook_id": "<id>",
  "name": "Ops Lead — email 3 step",
  "channel": "email",
  "steps": [
    { "step_number": 1, "subject": "…", "body": "…", "delay_days": 0 },
    { "step_number": 2, "body": "…", "delay_days": 4 },
    { "step_number": 3, "body": "…", "delay_days": 9 }
  ]
}' --json
```

Facts that decide whether this call succeeds:

- **`playbook_id` is required.** A sequence always belongs to a playbook.
- **One sequence per playbook per channel.** A second email sequence on the same playbook is
  rejected by a unique constraint — edit the existing one with `update_sequence`, or use a
  different channel.
- **`status` is not an execution gate.** Draft, approved, active: the stepper walks any
  sequence its enrollments point at. **Enrollment existence decides, nothing else.** Setting a
  sequence back to draft does not stop it.
- **`delay_days` is measured from the previous step**, and `0` means "immediately on
  enrollment".
- **A stored branching graph does not run by itself.** `update_sequence({graph})` validates it,
  renders it on the canvas and lets you dry-run it with `get_sequence({simulate})` — but with
  `graph_mode` **off** it is authoring and preview only, and the linear `steps` stepper keeps
  walking. Flip `graph_mode` on and NEW enrollments snapshot the graph instead; in-flight leads
  keep the plan they started on. Read `get_sequence` to see which mode a sequence is in before
  telling anyone what a lead will experience.
- **Locked sequences**: one linked to an external vendor campaign cannot have its steps
  edited here, because the steps live in the vendor. Bindings stay editable.
- Changing steps on an **active** sequence with live enrollments requires the explicit
  confirmation flag — in-flight leads are walking the old plan.

## The seven step kinds

Every node does exactly one of these, and they fall into two classes that behave differently:

| Kind | Channel | Class | Needs |
|---|---|---|---|
| `email_message` | email | message | subject + body |
| `linkedin_invite` | linkedin | message | note **optional** |
| `linkedin_message` | linkedin | message | body |
| `linkedin_comment_post` | linkedin | engagement | body, acts on the lead's latest post |
| `linkedin_like_post` | linkedin | engagement | — |
| `linkedin_visit_profile` | linkedin | engagement | — |
| `whatsapp_message` | whatsapp | message | body |

**Message** steps land in the lead's inbox: the contactability gate applies, the sender pool
applies, and the compliance envelope (AI notice, unsubscribe) is attached. **Engagement**
steps are public or invisible actions — never a DM. They carry no messaging envelope and
consume no message quota, but they do consume the LinkedIn account's action budget.

That distinction is what makes a warm-up pattern possible: visit the profile, react to a
post, *then* invite. Three touches, one message quota.

**Leave the invite note empty on purpose.** An empty connection request is accepted more
often than one carrying a pitch, and on accounts without Sales Navigator a non-empty note
has its own constraints. If you write one, one sentence referencing the post.

## Cadence

Day **1 → 4 → 9 → 16 → 25**. Increasing gaps, **maximum five touches**. Every step carries a
new angle — an observation, an example, a real question. "Just following up" is not a step,
it is a nuisance with a delay in front of it.

Most replies do not come from the first message, and most senders quit after the second.
That gap is the opportunity, and it closes the moment repetition replaces new value.

**Stop rules, both mandatory:**

- A reply **pauses every channel** for that lead, immediately. Not just the channel that got
  the reply.
- No reply → **60–90 day cooldown**, and re-entry only on a **new** signal.

## Slots: how copy gets personalised

Copy carries slots that resolve per lead at send time. The canonical form is
**`{{cell.<column_key>}}`** — a value from the table column of that name.

```
{{cell.salutation}},

Ich sah {{cell.signal}}. Spielt {{cell.pain_point}} bei {{company.name}} eine Rolle?
```

Three rules that prevent the most common failure:

1. **A slot with no value does not fail loudly.** It resolves empty and the message still
   goes out, reading like a broken mail merge. Verify against a real row before enrolling.
2. **Generate the fills, not the message.** A fixed template with generated `{hook}` /
   `{pain_point}` values is predictable at 4,000 rows; free-form generation per lead is not.
   The copy engine is yours — the provider is only the rail.
3. **One variable, one argument.** Two slots stacked in one sentence read as generated even
   when each is correct.
4. **The greeting is a slot too.** `{{cell.salutation}}` resolves to the complete, correctly
   gendered line (`Sehr geehrter Herr Meier`, or `Hi Max` for an informal campaign) and is
   produced by its own prompt column. Gate the send on its confidence rather than letting a
   guess go out. See `copy-patterns.md`.
5. **No dashes as sentence connectors.** An em dash joining two clauses is the loudest signal
   that a model wrote the line. Two short sentences instead, and put the rule in the
   generation prompt.

Per-channel structure, length limits and the step-by-step patterns are in
**`copy-patterns.md`** next to this file.

## Senders and limits

The channel rail hangs off the **sender**, not the sequence. Bind a sender that is actually
verified for the channel, and respect the limit — it is not a throttle you may raise:

| Channel | Per sender per day |
|---|---|
| Email | **15 cold sends** (account limit ~100; stay well under it) |
| LinkedIn | **20–25 connection requests** |
| WhatsApp | **10–20 new conversations**, ramped up slowly |

Reach comes from **more senders**, never from more volume per sender. Thirty inboxes at
fifteen mails is 450 clean sends a day; one inbox at 450 is a dead domain by Thursday.

A daily limit of `0` on a sender means **unconfigured**, not unlimited — check it before you
trust it.

## Enrollment: the only thing that sends

Three ways in, and the first is the one you will use:

1. **The terminal enroll column on a Tabelle** — a `tool` column carrying `channel` and
   `sequence_id`. It is the last column, sends only in its own run, and `auto_run` is
   rejected for it.
2. **A workflow `enroll_sequence` step** — for event-driven entry.
3. **Direct** — `enroll_linkedin_sequence` for one lead, mostly for testing.

Two gates decide whether an enrollment happens, and **`enroll_preflight` checks neither** —
do not treat a clean preflight as permission:

- **Contactability**: unsubscribe and blacklist, deny-only, **fail closed**. If the lead
  cannot be loaded reliably, nothing goes out.
- **Deduplication**: an existing enrollment blocks a second one — but the terminal states
  `cancelled`, `failed`, `skipped` and `expired` **release** the lead. A lead you thought was
  finished can be re-enrolled.

## Signal binding

`trigger_signal_types` on the sequence routes leads in when a matching buying signal is
detected. This is how a campaign becomes reactive rather than batch: the signal fires, the
lead enters, the first message references the signal that put them there.

Freshness is the whole point — a signal is hot for 3–7 days and cold after ~28. A sequence
bound to a signal type but enrolled three weeks late reads as researched, not relevant.

## Verify before you believe it

```bash
gtm call get_sequence --input '{"sequence_id":"<id>"}' --json
```

**Check the step list is not empty.** A sequence with zero steps — created, named, wired to
an enroll column, believed to be live — is one of the most common build faults there is.
Nothing sends, nothing errors, and the motion looks finished.

Then check, in this order:

- [ ] Steps exist, with the delays you intended
- [ ] `graph_mode` matches the plan you think is running
- [ ] A real row resolves every slot in every step — no empty fills
- [ ] The sender is verified, and your volume fits its daily limit
- [ ] The enroll column is last and `auto_run` is off
- [ ] `workspace_schema_get` → `handoffs.dangling` is empty for this playbook

## Common failures

- **An empty sequence wired to an enroll column** — the motion looks built and never sends.
  Check the step list; this one is common.
- **Two channels, one copy** — a forwarded email is not a LinkedIn message. Playbooks running
  two channels reply at a fraction of the rate of those running one properly.
- **A slot that resolves empty at scale** — always previewed against one row, never against
  the row that has no value.
- **Editing an active sequence** without realising in-flight leads are mid-plan.
- **Raising a sender's daily limit** to get more reach.
- **A break-up step that is a guilt trip.** Close the door politely and leave it unlocked;
  the opt-out rate is a metric and it is watching you.
