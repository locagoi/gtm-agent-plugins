---
name: gtm-handoffs
description: Use when connecting the pieces of a GTM Automation workspace — how Wissen assets, Playbooks, Quellen, Tabellen, Sequenzen and Workflows link to each other, which mechanism and tool creates each connection, how a Workflow actually runs (trigger → steps → dry run → live), and which connections do NOT exist. Read this before wiring a motion end-to-end, before extending an existing one, and whenever a build "looks finished" but nothing fires. To build the table itself, use build-gtm-workflow; to operate a workspace day to day, use gtm-operate.
allowed-tools: Bash, Read, Grep, Glob
---

# How the pieces connect

A workspace is a **Baukasten**. Building a brick is the easy half; the half that goes wrong is the **handoff** — the one place where a Tabelle hands rows to a Sequenz, or a Workflow hands rows to a Tabelle. Every handoff below is a real, stored piece of configuration. Nothing else connects anything.

The failure this skill prevents: an agent assumes a connection that does not exist, configures it anyway, and reports the motion as built. It looks finished. It never fires.

```
Wissen ──pin──▶ Playbook ──bindet──▶ Tabelle ──terminale Enroll-Spalte──▶ Sequenz
                    │                   ▲                                    ▲
                    └──▶ Sequenz        │                                    │
                                     Quelle                                  │
                                                                             │
   Trigger ──▶ Workflow ──add_table_rows──▶ Tabelle                          │
                  ├──────enroll_sequence───────────────────────────────────┘
                  └──────feed_notify──▶ Feed          Signal ──Bindung──▶ Sequenz
```

## The handoffs that exist

| From → To | What creates it | Tools (in order) |
|---|---|---|
| Wissen → Playbook | Pin the asset to the playbook | `wissen_asset_create` → `playbook_asset_pin` |
| Wissen → Tabelle | `{{asset.<kind>}}` in an ai/enrichment column prompt | `workspace_table_add_column` |
| Playbook → Tabelle | Bind the table to the playbook | `playbook_table_link` |
| Playbook → Sequenz | `playbook_id` when the sequence is created (required) | `create_sequence` |
| Quelle → Tabelle | Attach the source, prove it manually, then schedule | `workspace_table_add_source` → `workspace_table_run_source` → `workspace_table_schedule_source` |
| Tabelle → Tabelle | A `create_lead` column with `target_table_id` | `workspace_table_add_column` |
| Tabelle → Sequenz | The **terminal** enroll column (`kind: 'tool'`, `channel`, `sequence_id`) | `create_sequence` → `workspace_table_add_column` → `workspace_table_run_column` |
| Tabelle → external tool | Same column, `campaign_id` instead of `sequence_id` | `list_integrations` → `workspace_table_add_column` |
| Trigger → Workflow | `trigger_type` on create: `schedule` \| `event` \| `manual` \| `webhook` | `create_workflow` → `set_workflow_enabled` |
| Workflow → Tabelle | Step `add_table_rows` | `add_workflow_step` |
| Workflow → Sequenz | Step `enroll_sequence` | `add_workflow_step` |
| Workflow → Feed | Step `feed_notify` | `add_workflow_step` |
| Signal → Sequenz | `trigger_signal_types` on the sequence | `create_sequence` / `update_sequence` |

**The rules behind the table, in one pass:**

- **A Playbook binds, it does not start.** Its status is a statement about strategy, never a switch. Runs start in exactly three places: a column run, a source schedule, a workflow trigger.
- **`{{asset.x}}` needs the pin.** Without it the reference resolves *empty* and the column still runs — producing context-free text nobody recognizes as broken. Cell provenance records which asset **revision** was used, so a later rewrite does not retroactively invalidate old cells.
- **The enroll column is the LAST column, never a middle one.** It sends only in its own run, never on create, and `auto_run: true` is rejected for it. Enrollment is always a deliberate act.
- **A schedule turns a source into recurring cost.** Always: attach → one manual run with a small `max_results` → then the schedule.
- **External campaign targets are honest fog.** With `campaign_id` the target lives inside the vendor; the platform will not pretend to know its steps. That is a feature, not a gap.

## The handoffs that do NOT exist

| Assumed | Reality | Do this instead |
|---|---|---|
| Sequenz → Tabelle ("write results back") | A Sequenz knows only its enrollments and stops for a lead on reply | A Workflow on that event with an `add_table_rows` step |
| Playbook → Run ("activate to start") | A Playbook binds; it starts nothing | Column run · source schedule · workflow trigger |
| Workflow → Ablauf ("run the table's columns") | The Ablauf belongs to the Tabelle; no object remote-controls another's cascade | `add_table_rows`, then let the table's `auto_advance` compute |
| Tabelle → Send ("configured means sending") | Nothing sends on create | `workspace_table_run_column` with `max_credits`, after a dry run |
| Workspace → Workspace | No edge crosses the tenant boundary | Rebuild in the target workspace; `workspace_table_save_as_template` moves *structure* only — never rows or credentials |

## How a Workflow runs

A Workflow is the **event** dimension (Tabelle = per row, Sequenz = per lead over time). Deterministic by construction: same input → same steps → same output.

1. **Trigger** — `schedule`, `event`, `manual` or `webhook`, set on `create_workflow`. Without one it is a script nobody starts.
2. **Steps**, appended with `add_workflow_step`. The deterministic set: `http_request` (one templated API call; the response lands under `output_key` as `{{key.body}}`/`{{key.status}}`) · `add_table_rows` · `enroll_sequence` · `feed_notify` · `tool_call` (one named custom/registry tool — the integration node) · `wait` (hours/days, max 30d; the run parks and resumes on the tick, it never holds a worker). An **agent** step is for the cases that need judgment — bounded, and gated.
3. **Branch and control** — `set_workflow_step_condition`, `set_workflow_step_parallel_group`, `set_workflow_step_retry`, `set_workflow_max_concurrency`.
4. **Dry run before it goes live.** `run_workflow` with a dry run shows the steps it would take without side effects. Then `set_workflow_enabled`.
5. **Watch it** — `list_runs`, `get_workflow_history`, and `diagnose_workflow_run` for one failed run.

**Workflow or Agent?** *Can you write the steps down → Workflow. Does each case need judgment → an Agent step inside the Workflow, bounded and gated.*

## Building the Tabelle itself

The table is where the chain does its work: a source fills it, columns process each row, the terminal enroll column hands leads over. The full build — `entity_binding`, the column kinds, `output_schema` as the predictability contract, the cascade, saving as a template — is **`build-gtm-workflow`**. Read it for the inside of the brick; this skill is about the seams between bricks.

One correction worth carrying: the platform **does** send. Generic tool columns hard-refuse every send category (fail-closed, no adapter is even resolved) — but the dedicated **outreach terminal column** routes before that gate into the shipped, gated enroll machinery. "Tool columns cannot send" is true; "the platform cannot send" is not.

## Verify against the workspace, never against memory

This document is the map; the workspace is the territory. Two calls give you the live answer:

- **`workspace_schema_get`** → `handoffs.edges` (what is wired in THIS workspace) · `handoffs.dangling` (**configured handoffs whose target is missing or archived — dead config that looks alive**; check it before extending a motion) · `handoffs.legend` (the same matrix as above, served by the platform).
- **`explain_system`** → `handoffs` with every rule and every myth as structured data.

The platform's copy is generated from `src/lib/mcp/handoffs.ts` and guarded by a test that fails if a named tool disappears from the registry or an edge kind drifts. **Where this file and the tool disagree, the tool is right** — and the disagreement is a bug worth reporting.
