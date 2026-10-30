---
name: closed-loop
description: Use once a campaign is live and the question becomes "how do I keep it running and improving". The entry point to the closed outbound loop — find, enrich, enroll, handle replies, keep deliverability healthy, optimize, draft the next playbook from what won, and start again — and the rules every loop skill obeys (read freely, write only after confirmation, verify results instead of trusting job status). Routes to health-check, sourcing-topup, enroll-outreach, reply-triage, deliverability, optimize-outreach and playbook-from-winners.
allowed-tools: Bash, Read, Grep, Glob
---

# The closed outbound loop

`gtm-quickstart` gets a workspace to its first live campaign. This skill is what happens on
every day after that. A campaign that is not measured, refilled and rebuilt decays: the lead
supply runs dry, replies go unanswered, inboxes burn, and the copy that worked last quarter
keeps going out long after it stopped working.

The loop has seven stations. Each one is its own skill, works on the ONE workspace behind your
key, and can be run by hand or on a schedule.

```
        ┌──────────────────────────────────────────────────────────────────┐
        │                                                                  │
        ▼                                                                  │
  1 find + enrich ──► 2 enroll ──► 3 replies ──► 4 deliverability          │
  sourcing-topup      enroll-       reply-        deliverability           │
                      outreach      triage                                 │
                                                       │                   │
                                                       ▼                   │
                         6 next playbook ◄── 5 optimize                    │
                         playbook-from-       optimize-outreach            │
                         winners                                           │
                              │                                            │
                              └────────────────────────────────────────────┘

  health-check — the gauge you read before and after every turn of the loop
```

| Station | Skill | Answers | Mutates? |
|---|---|---|---|
| 0 | **`health-check`** | Is anything broken or silently stalled right now? | never |
| 1 | **`sourcing-topup`** | Will the sequences have enough qualified leads tomorrow? | gated |
| 2 | **`enroll-outreach`** | Who passed the gate and is ready to enter a sequence? | gated |
| 3 | **`reply-triage`** | Which replies need an answer, and what should it say? | sends gated |
| 4 | **`deliverability`** | Do our mails still land in the inbox? | gated |
| 5 | **`optimize-outreach`** | Which variant, step or source wins, and what should change? | proposals only |
| 6 | **`playbook-from-winners`** | What would the next playbook look like if built from what won? | gated (draft) |

Start with `health-check`. If it is red, fix that first — optimizing a sequence that is not
sending is wasted work.

## Rules every loop skill obeys

### 1. Read freely, write only after confirmation

- **Reads run immediately**: list, get, stats, previews, dry runs.
- **Every mutation is previewed, then waits for an explicit yes.** A mutation is anything that
  sends, enrolls, releases, pauses, resumes, archives, deletes, spends credits on a live run,
  or changes copy, limits or senders.
- The preview names: the object (name + id), the exact change, the blast radius (how many
  leads, which sender, which channel), and the cost if any.
- **One action, one yes.** Never bundle unrelated changes under one confirmation. An ambiguous
  or casual reply is not consent — ask again.
- **No automatic retries.** On failure, report and stop. A re-run is a deliberate act.
- **Partial success is reported exactly**: "12 of 40 enrolled, then the call failed" — never a
  bare "stopped".
- If your client offers a confirmation tool (`propose_plan` or similar), ask by calling the
  tool you intend to use and let the gate turn it into the button. Asking in prose is not
  asking.

Creating something inert — a draft playbook, a sequence nobody is enrolled in, a dry run —
needs no confirmation. **Approval sits at sending, not at building.**

### 2. Verify results, never trust the status

The most common failure mode of any automation is not an error. It is a run that reports
`done` and delivered nothing. After every run:

- read `skipped`, not only `failed` — a skipped row is a failure that does not call itself one
- compare credits used with what you expected — zero spend on a paid column means nothing ran
- read a sample of the actual cell values, not the job summary
- `processing` or `running` for a long time proves nothing; check when cells were last updated

And for outreach specifically:

- **"Enrolled" or "active" is not proof of sending.** Only a send record is
  (`list_runs` with `source: "sequence"`, `sequence_log`).
- **A weekend is not a stall.** Sequences send on weekdays; judge standstills on working days.
- **Cumulative is not daily.** Some stats tools return running totals; do not read a total as
  today's volume.
- **"Not measurable" is never 0.** If a tool is missing or returns nothing, say what could not
  be measured and why. An empty cell means "could not be determined", not "does not occur".

### 3. Never invent

Name the tool every number came from. A value that is not in a tool result is a value you do
not have. Tool names in these skills are the ones the workspace exposes; if one is not in your
advertised list, find it with `find_tools` and run it with `call_tool` (`gtm call <name>` from
a shell) — the catalogue is larger than the listing. If a question can only be answered by
something outside the product, that is a gap to report with `report_issue`, not a reason to
work around it.

### 4. Measure against your own bar, written down first

Every station has a verdict (green / yellow / red, keep / stop / unclear). Write down the bar
before you look at the numbers — reply rate you consider worth scaling, bounce rate you treat
as a stop signal, how much of the daily capacity a sequence should use. `outbound-playbook`
and its `benchmarks.md` give published reference points to start from. A bar invented after
seeing the data is not a bar.

Small samples are "unclear", never a win. Where a tool reports `low_sample` or an interval,
use it: a low-sample group is never a winner, and two arms whose intervals overlap are not
different.

### 5. One owner, one decision, one review date

Each proposal the loop produces carries what changes, the evidence, who decides, and when the
effect will be checked. Changes apply to new leads and new variants; leads already mid-sequence
are not rewritten.

## Running the loop on a schedule

Every station can run unattended as a scheduled workflow or agent — see
**`agents-loops-goals`**. The rule that survives automation: **reads and drafts may run on a
schedule; sends, enrollments into a new sequence, spend above the approved budget and changes
to live copy keep their human gate.** A loop that automates the gate away is no longer a loop
you control.

A sensible rhythm to start from, adjusted to your volume:

| When | Run |
|---|---|
| Every working day, before the send window | `health-check` → `sourcing-topup` → `enroll-outreach` |
| Several times a day | `reply-triage` |
| Daily | `deliverability` |
| Weekly, once enough sends have matured | `optimize-outreach` |
| When a motion has a clear winner, or a new audience opens | `playbook-from-winners` |
