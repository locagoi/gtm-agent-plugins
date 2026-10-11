---
name: agents-loops-goals
description: Use to make a workspace run itself and to build it iteratively rather than in one pass — translate an outcome goal into a build and measurement loop, create workspace agents with scoped tools, and close the loops (scheduled sources, signal watches, event workflows, the await_rows return edge, reply triage, approval gates). Covers what a dry run actually simulates and which config is stored but never executed. Read after gtm-quickstart, when the first campaign runs and the question becomes "what keeps running without me".
allowed-tools: Bash, Read, Grep, Glob
---

# Goals, agents, loops

A workspace that needs a person for every step is a tool. A workspace that runs its own loops
and asks a human only where judgement is required is the product. This skill is how you get
from the first to the second, and how to build it **in slices** rather than in one pass.

Three primitives, and they are not interchangeable:

| | What it is | Use it for |
|---|---|---|
| **Goal** | a measurable outcome contract executed through Command and existing workspace tools | target, owner, deadline, baseline, review date and a running measurement loop |
| **Agent** | a named worker with its own prompt, model and tool allowlist | judgement inside a workflow step, or a triggered responder |
| **Loop** | a schedule, a watch or an event that fires without anyone | everything that must keep happening |

## Build it in slices, never in one pass

The fastest way to a working workspace is not to build the whole thing and then test it. It is
to get one thin slice running end to end, then widen it.

```
1. one source     → 20 rows, read them
2. one gate       → the qualification verdict, with reasons you agree with
3. one sequence   → 3 steps, dry-run, 20 messages read by a human
4. one enrollment → capped, watched
5. THEN a loop    → schedule the source, wire the trigger
6. THEN an agent  → hand over the judgement you have now seen it get right
```

Each numbered step is verifiable on its own, and each one is cheap to throw away. The common
failure is the reverse order: an agent wired into a scheduled loop over a source nobody read,
which produces confident output nobody checks until the credits are gone.

**Validate judgment against representative examples and explicit acceptance criteria.** Reuse evidence from approved templates and comparable evaluations. Record sample size, failures and uncertainty; a fixed number of human repetitions is not evidence of quality. Keep the first send and scale decisions gated.

---

## Goals: plan, build, observe, improve

An explicit goal is the mandate for reversible preparation within the named workspace, not blanket permission to spend or send. Discover `get_goal_plan` via `find_tools`, then inspect its schema:

```bash
gtm call find_tools --input '{"query":"get_goal_plan"}' --json
gtm call get_goal_plan --input '{"positives_week":5,"segment":"B2B SaaS","steps":3}' --json
```

The plan uses onboarding step-0 back-calculation: a combined meeting/positive goal takes the maximum, not the sum; email volume comes from the measured emails-per-positive rate (400 only as a labeled planning hypothesis), capacity from the actual touch count and conservative sender limits. Unknown preflight cost stays unknown. An email capacity scenario is not evidence that email is the right channel, a purchasing decision or a launch date.

**The tool is read-only and creates nothing. Continue in the same turn:**
1. Read setup, Wissen, ICP/persona, existing linked objects, sender health and product capabilities. Resolve an unambiguous scope; otherwise prepare an unbound draft and keep independent work moving. Never invent IDs or attach to an arbitrary workspace/object.
2. Follow `get_play` with `{"play_id":"full_gtm_chain"}`. Reuse the existing objects, build inert assets/tables/sources/columns and a sequence, and label assumptions. Derive LinkedIn search inputs from ICP through the current product source planner; never request a Sales Navigator URL as a prerequisite.
3. Use current product preflight before paid runs, with `max_credits` inside the existing approved budget. Budget not available: prepare the build and the cost decision, keep the paid step held. A balance is not authorization.
4. Validate the read-only measurement blueprint first with `get_timeline`, freeze the real playbook/sequence cohort and then create/reuse the scheduled workflow. Verify the first actual scheduled run through `get_workflow_history`. Configuration alone is not proof of a running loop; missing attribution remains unknown.
5. Present concrete copy, recipients, sender, volume and consequences for the **first send of new copy**. Retain money, legal, first-send, deletion and post-result scaling gates and existing per-action approvals. Do not re-ask for an already approved action within the same verifiable scope.
6. Incorporate feedback, release only within authorization, measure mature windows, propose stop/keep/scale, obtain the scale decision, then measure the revised version. Record owner, implementation deadline, baseline, target, review date and measured results in the operator's decision system.

If discovery returns **no tool named get_goal_plan**, the release is not available on this workspace yet. Use the current `full_gtm_chain` house play with a clearly labeled local capacity draft; do not call removed mission tools or imply a background goal worker exists.

Evaluate **works / does not / unclear**. Small samples, changing cohorts, missing prices or immature replies mean unclear, never success. The default seven-day progress review is an assumption; outcome comparison starts at actual launch. Do not wait for a human to supply naming, language or a routine draft deadline.

## Agents

```bash
gtm call create_agent --input '{
  "name": "Lead Qualifier",
  "slug": "lead-qualifier",
  "description": "Prüft eingehende Leads gegen ICP und Persona",
  "system_prompt": "Du bist B2B-Qualifizierer. …",
  "allowed_tools": ["get_lead_intelligence", "wissen_asset_get", "research_company"],
  "temperature": 0.2,
  "max_tool_iterations": 6
}' --json
```

Four settings decide whether an agent is safe to leave running:

| Setting | Why it matters |
|---|---|
| `allowed_tools` | **an allowlist, always.** Empty means *all tools*, which is not a default you want on something that runs unattended |
| `denied_tools` | the explicit no, for anything that sends or spends |
| `max_tool_iterations` | the ceiling on a loop that has gone wrong. Keep it low; raise it when you have a reason |
| `temperature` | qualification and classification want it low. Copy wants a little more |

**Scope the allowlist to the job.** A qualifier needs to read leads and research companies. It
does not need to enrol, push to CRM, or create tables. An agent that can do everything will
eventually do something.

### Where an agent belongs, and where it does not

An agent step inside a workflow is for **judgement on a single case**: is this reply a meeting
request, does this company match the ICP, which case study fits. Everything else should be a
deterministic step:

- Reshaping data → `transform` (free, no model, same input same output)
- Narrowing a list → `filter`
- Choosing between branches on known values → `switch`
- Calling an API → `http_request` or `tool_call`

Reaching for an agent where a `transform` would do buys you cost, latency and variance in
exchange for nothing. *Can you write the rule down? Then it is not a judgement.*

### Make a text-only turn fail

```bash
gtm call update_workflow_step --input '{"step_id":"<id>","requires_tool_call":true}' --json
```

With `requires_tool_call`, a step where the agent only *talked* is recorded as **failed**
instead of passing as a green run that changed nothing. Set it on every agent step that is
supposed to do something. Silent no-ops are the hardest workflow bug to notice, because
everything looks fine.

---

## Loops

Four kinds, and the right one depends on what wakes it up.

### 1 · Scheduled sources: the list refills itself

```bash
gtm call workspace_table_schedule_source --input '{
  "table": "Accounts", "source": "social_listening",
  "config": { "playbook_id": "<id>", "keywords": ["…"] }, "cadence": "daily"
}' --json
```

`job_change`, `profile_posts` and `social_listening` are schedule-only — they *are* loops.
`pool`, `scraping`, `lead_sourcing` and `indeed_jobs` can be one-shot or scheduled.

**A schedule turns a source into recurring cost.** Always attach, run once small, read the
rows, and only then schedule.

### 2 · Signal watches: the target list watches itself

A watch re-reads pages named in a column and reports what is **new**. It never creates rows; it
writes the hit onto the matching row and fires `company_signal_detected`.

That event is only useful if something listens:

```bash
gtm call create_workflow --input '{
  "name": "Signal → Outreach", "trigger_type": "event",
  "config": { "event_name": "company_signal_detected", "filters": { "signal": "job_posting_open" } }
}' --json
```

**The filter is mandatory.** Without it the workflow fires on every signal type in the
workspace.

### 3 · Event triggers: something happened, someone should react

```bash
gtm call create_trigger --input '{
  "name": "Positive Antwort → Agent",
  "trigger_type": "event",
  "config": { "event": "lead_replied" },
  "agent_id": "<id>",
  "action_type": "invoke_agent",
  "cooldown_minutes": 5,
  "max_fires_per_day": 100
}' --json
```

`cooldown_minutes` and `max_fires_per_day` are the runaway brakes. Set them deliberately on
anything that costs money or writes outward; the defaults are generous.

Trigger types: `event` · `schedule` · `webhook` · `keyword` · `threshold` · `pipeline`.
Actions: invoke an agent, notify, update a record, or start a workflow.

### 4 · The return edge: how a workflow fans out and gets results back

A workflow **branches, it does not loop** — per-item repetition is the Tabelle's dimension. The
bridge between them is `await_rows` on an `add_table_rows` step:

```bash
gtm call update_workflow_step --input '{
  "step_id": "<id>", "await_rows": true, "await_timeout_hours": 24
}' --json
```

Instead of only handing rows over, the run **parks** until those rows exist and none of their
cells is still pending, then continues with the finished rows under `{{key.rows}}` and
`{{key.row_count}}`. That is how a workflow fans work out per row and gets the results back.

Parking is free — the run is woken by the same tick as `wait` and approval steps, and holds
nothing while it waits. On timeout the step fails **named**, and `continue_on_failure` decides
whether the run goes on. A run never waits forever.

`field_mapping` on the same step is mandatory in practice: a row without a name is dropped
before the domain is even looked at, so a wrong path silently drops the whole batch. The step
counts unusable rows and refuses outright when none are usable.

### The human gate belongs in the loop

```bash
gtm call add_workflow_step --input '{
  "workflow_id": "<id>", "type": "approval",
  "message_template": "80 Leads für {{playbook}} freigeben? Kosten: {{estimate}}"
}' --json
```

The run parks, a card lands in the Feed's Freigeben lane, approving continues with
`{{key.approved}}` in context, declining ends the run as aborted. Set `deadline_hours` or an
undecided card waits indefinitely — which is deliberate, because **a gate that opens itself
after two hours is not a gate**. It never auto-approves.

Put one in front of anything consequential: bulk sends, spend, irreversible writes.

---

## Two things that will bite you

### A dry run is not a safe run

`run_workflow({dry_run:true})` no-ops only a **short, named list** of tools — the
send/book/escalate family. **Every other side-effecting tool an agent step calls executes for
real during the rehearsal.** Pausing sequences, writing to a CRM, spending on enrichment: all
real.

```bash
gtm call automation_capabilities --json    # → dry_run.simulated_tools, the current list
```

Read that list before rehearsing anything that writes. And prefer an allowlist on the agent
that makes the dangerous call impossible in the first place.

### Some config is stored but never executed

`automation_capabilities` also returns `stored_but_not_executed` — fields you can write that
the runtime ignores today, with the reason. Two that matter:

- **Sequence `status`** is a label, **not an execution gate**. The stepper walks any sequence
  its enrollments point at, including `draft`. Enrollment existence decides. Setting a sequence
  back to draft does not stop it.
- **A branching sequence `graph`** is authoring and preview only while `graph_mode` is off. The
  linear `steps` keep running. Do not present the graph as the plan a lead will experience
  until you have checked the mode.

**Call `automation_capabilities` before you build, not after something behaves oddly.** It is
read-only, free, and it is the contract.

---

## The loops worth having, in order

1. **Reply triage** — every inbound reply classified and routed. Install
   `reply-triage`; without it every later measurement is guesswork.
2. **Reply to meeting** — install `reply-to-meeting`. The path from a positive reply to a booked
   slot is the one place where speed converts directly.
3. **Blacklist reconciliation** — daily, before the day's sends. See `plays/crm-blacklist-sync.md`.
4. **One sourcing loop** — the schedule or watch that fits your play.
5. **Deliverability watch** — install `deliverability-watch`. It proposes a pause in the Feed
   rather than stopping anything by itself.
6. **Learning approval** — read what the system distilled and approve or reject it. A proposed
   learning sits inert until approved.

Note the order. Measurement loops first, sourcing loops after. A workspace that sources faster
than it learns just makes the same mistake at higher volume.

## Verify a loop is actually looping

```bash
gtm call list_runs --json                              # did it fire at all?
gtm call get_workflow_history --input '{"workflow_id":"<id>"}' --json
gtm call diagnose_workflow_run --input '{"run_id":"<id>"}' --json
```

`diagnose_workflow_run` is the first stop when a run **succeeded but changed nothing** — it
shows per-step status, the resolved prompt, the actual tool calls and the error. A green run
with no tool calls is the failure mode `requires_tool_call` exists to prevent.

And check `workspace_schema_get` → `handoffs.dangling` for configured handoffs whose target is
gone: dead config that looks alive.
