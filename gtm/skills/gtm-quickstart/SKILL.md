---
name: gtm-quickstart
description: Use to take a GTM Automation workspace from empty to a live, sending campaign in one working session — the complete build order: intake interview, Wissen assets, playbook, table (source → qualify → enrich → copy → enroll), sequence, workflow, first bounded run, and the measurement loop. Start here for "set up my workspace", "get me from zero to outreach", "build my first campaign". Each stage names the next skill to go deep on.
allowed-tools: Bash, Read, Grep, Glob
---

# Zero to a live campaign

This is the whole path, in order, with a checkpoint at the end of every stage. Follow it top
to bottom and a new workspace goes from empty to sending — deliberately, bounded, and
measurable.

**What this replaces.** Built by hand, this is a two-to-four week engagement: a discovery
call, a CRM analysis, an ICP workshop, persona mapping, value-prop drafting, sequence
writing, QA. The stages below are that same process, with the same quality bars, run by an
agent in a session. The bars did not move — you still cannot skip the interview, and a
campaign built on invented positioning still fails in week two.

**Nine stages, roughly 2–4 hours** if the human is available to answer questions:

| # | Stage | Output | Deep dive |
|---|---|---|---|
| 0 | Connect and orient | a verified connection, a read model | `setup` |
| 1 | Intake interview | answers you did not invent | `intake.md` (next to this file) |
| 2 | Wissen assets | ICP · persona · offer · proof · angle · signals | `draft-gtm-play` |
| 3 | Playbook | the strategy, bound | `draft-gtm-play` |
| 4 | Senders & channel | one channel, verified, within limits | `sequences` |
| 5 | The sequence | the touch plan, built-in slots first | `sequences` |
| 6 | The table | source → qualify → enrich → fill exactly those slots | `plays` · `build-gtm-workflow` |
| 7 | The enroll column | the one handoff that sends | `gtm-handoffs` |
| 8 | First bounded run | 20 rows read by a human | `outbound-playbook` |
| 9 | Measure and rebuild | the loop that compounds | `outbound-playbook` |

**Read `outbound-playbook` before stage 2.** It carries the decisions — ICP breadth, channel
choice, cadence, copy rules — with the numbers behind them. This skill is the build order;
that one is what to build.

---

## Stage 0 — Connect and orient

Follow **`setup`** to install the CLI and log in, then orient. Three calls, in this order,
before you create anything:

```bash
gtm whoami                      # the key works, and which workspace it points at
gtm call get_setup_status --json        # what this workspace still needs
gtm call workspace_schema_get --json    # the connected model: tables, columns, Wissen, handoffs
gtm call workspace_capabilities --json  # the sources/enrichments/tools actually available HERE
```

**On the tool list.** What you see listed is a curated core of roughly 70 verbs. The rest of
the catalogue is *not gone* — every tool stays callable by name; only the listing is
trimmed. `find_tools({query})` returns the names of the rest. So if a tool named in these
skills is not in your list — `create_playbook`, `playbook_asset_pin`, `add_workflow_step`,
`workspace_table_save_as_template` — call it anyway. It is there.

**Checkpoint:** you can name the workspace, its existing tables, and which sources it can
actually run. If `workspace_capabilities` lists no source you can use, stop and connect one
(stage 4) before building a table that has nothing to fill it.

---

## Stage 1 — The intake interview

**Never invent positioning.** A campaign built on what the agent guessed the customer sells
produces confident, specific, wrong copy — worse than generic, because it is wrong at
volume.

Work through **`intake.md`** next to this file. It is the discovery form condensed to what
the build actually consumes: offer in one sentence, ICP with good-fit *and* bad-fit
criteria, buying signals, case studies with real numbers, 2–4 personas with challenges and
benefits, channel preference, sender identities, blacklist.

Ask for what is missing. If the human cannot answer "which customer had the most striking
result, with the number", that is not a blocked build — it is the finding that the proof
asset will be weak, and you should say so.

**Checkpoint:** you can answer, from their words and not yours: who exactly, why now, what
you sell, what it produced for someone comparable, and who must not be contacted.

---

## Stage 2 — Wissen assets

Turn the interview into versioned knowledge. Every later stage references these instead of
re-typing them, which is the whole reason the campaign can improve later.

```bash
gtm call wissen_asset_create --input '{
  "kind": "icp",
  "name": "DACH mid-market packaging manufacturers",
  "content": { ... }
}' --json
```

Six assets, in this order — each builds on the one before:

1. **`icp`** — firmographics *plus* the disqualifiers. Concrete beats broad: "German
   Mittelstand manufacturers, 50–500 employees, complex B2B master data" outperforms
   "companies that need CRM". Keep it to ≤ 5 regions and ≤ 6 industries; the platform data
   is unambiguous that narrow lists reply roughly twice as often.
2. **`persona`** — role, what they are measured on, their pain in *their* words. 2–4 per ICP:
   one decision maker, one or two influencers.
3. **`offer`** — what you sell and the promise, in their language.
4. **`proof`** — case studies with a number and a timeframe. One strong proof per persona
   beats five vague ones.
5. **`messaging_angle`** — the hook connecting pain to offer.
6. **`signal`** — what makes an ICP company hot *now*: hiring, funding, a new decision maker,
   engagement. Reference the ICP and offer it matters for, and map it to a runtime signal
   type where one exists.

**Quality gate:** could a stranger read these six and pitch the company? If not, revise
before continuing. Full methodology and the per-asset detail: **`draft-gtm-play`**.

**Checkpoint:** `wissen_asset_list` returns six assets, and the ICP names its bad-fit
criteria, not only its good-fit ones.

---

## Stage 3 — The playbook

The playbook is the strategy paper: which assets, which channel, what runs by itself.

```bash
gtm call create_playbook --input '{"name":"DACH Packaging — Ops Lead","language":"de"}' --json
gtm call playbook_asset_pin --input '{"playbook_id":"<id>","asset_id":"<icp-id>"}' --json
```

Pin every asset. **Pinning is what makes `{{asset.icp}}` resolve** in a column prompt — without
it the reference resolves *empty*, the column still runs, and you get context-free text that
nobody recognises as broken. Pinning freezes which revision this play uses; the assets keep
evolving and the play chooses when to follow.

Then set the channel (`update_playbook` → `messaging_channels`) — **one** channel — and the
language and timezone.

**Checkpoint:** `playbook_assets_list` shows six pinned assets, and `messaging_channels` has
exactly one entry.

---

## Stage 4 — Senders and the channel

Nothing sends without an identity, and every channel has a hard operating limit that is not
a preference:

| Channel | Limit per sender per day | Before first send |
|---|---|---|
| Email | **15 cold sends** | SPF · DKIM · DMARC (`p=quarantine`), 3 weeks warmup, never from the main domain |
| LinkedIn | **20–25 connection requests** | a real account, connected — real ban risk |
| WhatsApp | **10–20 new conversations** | own number per campaign, ramp slowly |

```bash
gtm call list_integrations --json     # what is connected, by CATEGORY
gtm call list_senders --json          # the identities available
```

Resolve providers **by category**, never by vendor name — the connected adapter can change
under you. Reach grows by adding senders, never by raising per-sender volume. That single
rule is what keeps domains alive.

**Checkpoint:** at least one verified sender on your chosen channel, and you can state its
daily limit and what your planned volume is against it.

---

## Stage 5 — The sequence, before the table

**Write the sequence first.** It decides which variables exist; the table then fills exactly
those and nothing else. Build the table first and you get columns nobody references and
variables nobody filled.

```bash
gtm call create_sequence --input '{"playbook_id":"<id>","channel":"email","name":"Ops Lead — 3 step"}' --json
```

`playbook_id` is required, and there is **one sequence per playbook per channel**.

Four rules that decide whether this sequence is any good:

- **As short as possible.** 80 words for the opener, 50 for the follow-up, 30 for the break-up.
- **As few variables as possible.** Two is the target: `{{anrede}}` and `{{hook}}`. Everything
  else is fixed template text you wrote once and approved. More than three means the copy is
  over-personalised.
- **One form throughout: `Sie` or `Du`.** Decided once, held in every step, matched by the
  salutation column. Never mixed.
- **Variants from the first version**, testing different messaging angles. A sequence with one
  version cannot be improved, only replaced.

Cadence day 1 → 4 → 9 → 16 → 25, maximum five touches, each carrying a **different angle**. A
reply pauses every channel. Nothing sends on create.

**Use the built-in slots for now.** `{{first_name}}`, `{{company_name}}`, `{{industry}}`,
`{{location}}`, `{{sender_name}}` and friends work immediately. **`{{cell.<column>}}` does not
yet** — the platform refuses a placeholder nothing can fill, and the connection that makes cell
slots valid is the enroll column you add in stage 7. You come back here after that and finish
the copy with `update_sequence`.

Then take the inventory, because it is the input to the next stage:

```bash
gtm call get_sequence --input '{"sequence_id":"<id>"}' --json | grep -o '{{[^}]*}}' | sort -u
```

**Checkpoint:** `get_sequence` returns your steps with their delays, `graph_mode` matches the
plan you think is running, and you have a written list of the variables the table must fill.
An empty step list means the sequence does not exist in any useful sense.

Copy doctrine, the salutation prompt and the per-channel patterns: **`sequences`** and
`copy-patterns.md`.

## Stage 6 — The table that fills exactly those variables

**Check `plays` first.** If the motion has a name — local business outreach, post engagers,
keyword signals, job openings, inbound, website visitors, lost deals — there is a ready-made
template with its sources, columns, gates and tool calls already written.

The table is where the campaign is assembled: one row per company or lead, one column per step.
Build it with **`build-gtm-workflow`**; the canonical shape is `three-table-play.md` there.

**Columns left to right, in execution order**, each gated on a column to its left:

```
identity  →  cheap qualification  →  GATE  →  enrichment  →  variable fills  →  ENROLL
```

The identity block comes first so a person can read a row: a company table shows name, country,
industry, website, size; a lead table shows full name, salutation, job title. Take what the
source actually delivers.

Then **one column per variable from stage 5's inventory, and no others.** If the sequence uses
`{{anrede}}` and `{{hook}}`, you build two fill columns. Not five "might be useful" columns.

Five rules that decide whether this works at 4,000 rows:

- **`output_schema` on every ai/enrichment column.** Off-schema output makes the cell `failed`
  rather than garbage.
- **Reference, never re-type.** `{{asset.icp}}` for qualification, `{{cell.x}}` for a sibling,
  `{{company.name}}` for the entity.
- **Gate the expensive columns.** Contact enrichment costs 25 credits a row against 1 for
  qualification. The `run_condition` is where the bill is decided.
- **Closed lists, never free text**, for anything you will count later.
- **No empty variables.** Gate the enroll column on every fill:
  `{ "all": [ { "column": "anrede.confidence", "op": "gte", "value": 0.8 },
  { "column": "hook.usable", "op": "equals", "value": true } ] }`. The gate is a structured
  object, not an expression string, and dotted paths into a JSON cell do work. Prove it with a
  dry run: the response reports `rows_skipped_by_condition`.

**Checkpoint** — two calls, both free:

```bash
gtm call workspace_table_dependencies --input '{"table_id":"<id>"}' --json   # the graph you intended, no cycles
gtm call workspace_table_preflight --input '{"table":"<name-or-id>","expect":["fills_itself","enrolls_leads"]}' --json
```

`workspace_table_preflight` is read-only and free. One call, three answers: the findings on the
column graph, the cost of a full run, and the resolved inputs of the first rows.

**`expect` is what makes it sharp.** Without it the tool only reports defects it can prove;
name your goals — `fills_itself` · `runs_daily` · `enrolls_leads` · `complete_data` — and it
also reports what is *missing* for them. A freshly built table typically comes back with
`ziel_offen: die Tabelle hat keine Quelle` and `keine Outreach-Endspalte`, which is exactly the
list of what is left to do.

It is a report, never a gate: `verdict: 'blocker'` means "this run demonstrably burns", not
"you may not". A column combination it has no rule for produces no finding.

## Stage 7 — The enroll column: the one handoff that sends

A table hands leads to a sequence through **one terminal column**, and nothing else.

```bash
gtm call workspace_table_add_column --input '{
  "table":"Contacts", "key":"enroll", "name":"Enrollment",
  "data_type":"json", "kind":"tool",
  "config": { "channel":"email", "copy_mode":"template",
              "sequence_id":"<id>", "field_mapping": { ... } }
}' --json
```

Four properties of this column, all deliberate:

- It is the **last** column, never a middle one.
- It **sends only in its own run** — never on create.
- `auto_run: true` needs a `run_condition` beside it, or it is refused. Leave it off for the first
  campaign: enrollment should be a deliberate act until the qualification has proven itself.
- Every enrollment passes the contactability gates: unsubscribe and blacklist are checked
  first, and the check **fails closed** — if the lead cannot be loaded reliably, nothing goes
  out.

Handoffs that do **not** exist, and that agents routinely assume: a sequence writing results
back to a table · a playbook "activating" and starting a run · a workflow running a table's
cascade. Read **`gtm-handoffs`** before wiring anything unusual, and check
`workspace_schema_get` → `handoffs.dangling` for configured handoffs whose target is missing —
dead config that looks alive.

**Now finish the sequence.** With the enroll column in place, `{{cell.<column>}}` becomes
valid — go back and `update_sequence` with the real copy:

```bash
gtm call update_sequence --input '{"sequence_id":"<id>","steps":[ … {{cell.anrede}} … {{cell.hook}} … ]}' --json
```

**Checkpoint:** the enroll column exists, is last, `auto_run` is off, the sequence carries its
`{{cell.*}}` slots, and `workspace_schema_get` → `handoffs.edges` shows the
`table → sequence via enroll_column` edge with `dangling: []`.

---

## Stage 8 — The first run is 20 rows

```bash
gtm column run Accounts icp_fit --mode dry_run --json      # free, no writes, returns cost
gtm column run Accounts icp_fit --max-credits 5 --json     # live, hard cap
gtm table get Accounts --limit 20 --json                   # READ THE RESULTS
```

A live run of a paid column **requires** `max_credits`; without it the tool refuses and hands
back the estimate. Over the cap, remaining cells are skipped cleanly. There are no automatic
retries — a re-run is a deliberate act.

Then a human reads 20 qualification verdicts and 20 generated first lines, before anything
is enrolled. Apply the competitor test to each first line: *would this also fit the
recipient's competitor?* If yes, it is a mail merge, not personalisation.

**Never run 4,000 rows before someone has read 20.** This is the most expensive mistake
available in the product, and the easiest to avoid.

And before you put a **schedule** on the source, run `workspace_table_preflight` once more. From
that moment rows arrive without anybody watching, and a chain that quietly does nothing looks
identical to a chain with nothing to do.

**Checkpoint:** a human has approved the sample. Only now run the enroll column, capped.

---

## Stage 9 — Measure, then rebuild

```bash
gtm call get_funnel --json
gtm call get_campaign_stats --json
gtm call get_recommendations --json     # what the system is proposing in the Feed
```

Watch four numbers, and no others:

| Metric | Healthy | If it is off |
|---|---|---|
| ICP fit rate of sourced companies | ≥ 60 % | the ICP is too vague — fix stage 2 |
| Bounce rate | < 2 % (alarm at 3 %) | validate the list before import |
| Unique reply rate | 3–5 % is normal, 10 %+ is excellent | fix the list before the copy |
| Positive share of replies | ~20–28 % | if it collapses, targeting is off |

Open rate is deliberately absent — it is not measured, because measuring it costs
deliverability.

Then close the loop, which is the part almost everyone skips: classify every reply, rate
every meeting with its reason, and feed both back into the assets. A losing angle becomes a
revised `messaging_angle` (new version, history kept); a converting signal gets weighted up.

**When a campaign underperforms, rebuild the message before adding contacts.** The largest
improvements in the platform data come from rebuilding a campaign on the same audience —
several times the reply rate, at lower volume.

**Checkpoint:** the workspace produces a number you can act on, and one change is queued
based on it.

Then close the loops so it keeps producing without you: reply triage first, then reply to
meeting, then blacklist reconciliation, then one sourcing loop. Order matters, and
**agents-loops-goals** has it.

---

## Save the play so the next one takes an hour

```bash
gtm call workspace_table_save_as_template --input '{"table":"Accounts","name":"ICP scoring v1"}' --json
```

The template freezes the column config — structure only, no rows, no cells, no credentials.
`workspace_table_from_template` recreates it on any other playbook or workspace. Build once,
replay everywhere: that is what turns the second campaign into an hour of work.

## The guardrails, in one place

- Paid runs need `max_credits`; `dry_run` first, always.
- No automatic retries, ever.
- The enroll column is terminal and never auto-runs.
- Sends pass contactability, deny-only, fail closed.
- Everything is scoped to one workspace — there is no cross-workspace read.
- Resolve integrations by category, never by vendor name.
- A green enqueue is not a green result: read the cells back before claiming done.

## Where to go next

| You want to | Read |
|---|---|
| Decide what to build, with the numbers | **outbound-playbook** (+ `benchmarks.md`) |
| Draft the strategy asset by asset | **draft-gtm-play** |
| Build a named motion from a template | **plays** — nine of them |
| Build the table properly | **build-gtm-workflow** (+ `three-table-play.md`) |
| Write the touch plan and the copy | **sequences** (+ `copy-patterns.md`) |
| Understand how the pieces connect | **gtm-handoffs** |
| Make it run without you | **agents-loops-goals** |
| Operate it day to day | **gtm-operate** |
