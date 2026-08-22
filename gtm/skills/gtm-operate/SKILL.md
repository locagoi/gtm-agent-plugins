---
name: gtm-operate
description: Use when an AI agent (Claude Code, Codex, a customer's own agent) needs to OPERATE a GTM Automation workspace over its tools — read tables/Wissen, source and enrich rows, run columns, spend credits safely — via either the `gtm` CLI (shell) or the workspace MCP tools (docked at /api/mcp/<key>). The agent operating guide: the object model, CLI-vs-MCP choice, exact commands/tool names/args, copyable recipes, and the guardrails (paid runs need max_credits, sends are gated, never cross workspaces). To BUILD a repeatable workflow-as-a-table (create table → columns → cascade → template), use build-gtm-workflow instead.
allowed-tools: Bash, Read, Grep, Glob
---

# Operate a GTM Automation workspace

You are an agent driving ONE workspace of the GTM Automation platform. Everything you touch — tables, columns, cells, Wissen — is scoped to that single workspace. This guide gets you from "connected" to "did the thing" without guessing.

**Setting a workspace up from scratch?** Read `gtm-quickstart` — the complete build order from empty to a live campaign. **Building a repeatable play** as a table? `build-gtm-workflow`. **Writing the touch plan?** `sequences`. **Deciding what to build at all?** `outbound-playbook`. This skill is the broader *operating* guide — discover, read, source, enrich, run, spend — and the CLI-vs-MCP choice.

## Two things to do first (current model)
- **Discover, don't guess** — call `workspace_capabilities` (also in the CLI-advertised set): it returns the exact catalog this workspace can build (sources · enrichments · tools · agents, each with connected state + its create tool). Anything shippable is listed there — use it before reaching for a tool name.
- **Read a lead holistically** — `get_lead_intelligence` returns ONE complete lead+company picture (profile · firmographics · signals + provenance · score/heat · enrichment · engagement · conversations + sentiment · CRM/deal · relevant Wissen). Prefer it over the older `get_lead_context` (a thin subset). Every surface — call-hints, meeting-prep, copy, and the lead brain — reasons over this same object; so should you.

## The tool list is curated — the catalogue is not

What `gtm tools` (and an MCP client's tool list) shows is a **curated core** of roughly 70
verbs. Everything else the workspace has is still **callable by name** — only the listing is
trimmed, so nothing lost reachability:

- `find_tools({query})` — search the unadvertised rest, returns names + descriptions
- `call_tool({name, args})` — execute any of them (the CLI's `gtm call <name>` does the same)

Practical consequence: if a skill names a tool that is not in your list — `create_playbook`,
`playbook_asset_pin`, `playbook_table_link`, `add_workflow_step`,
`workspace_table_save_as_template`, `wissen_asset_revise` — **call it anyway**. Do not
conclude the feature is missing because the verb is not advertised.

## Workspaces differ — read, never assume
Not every workspace exposes the same surface: which modules, sources and integrations are available depends on what that workspace has connected and enabled. `gtm tools` and `workspace_capabilities` are the answer for the workspace you are in. Never hardcode the assumption that a tool exists because it existed somewhere else.

## The object model (9 primitives, short)

- **Workspace** — the tenant boundary. Every call is scoped to one.
- **Wissen** — the workspace knowledge base: versioned **Assets** (ICP, Persona, Offer, Positioning, Messaging Angle, Proof, Signal), **Learnings** (structured insights the system distills from what actually books meetings and gets replies — copy patterns, objection handling, ICP/signal/channel effects — each proposed into an approval queue and only injected into prompts once approved), and a self-maintaining memory of how the workspace operates. The Sales Blueprint is the onboarding hub: it ingests documents, CRM analytics and outreach signals, plus any connected knowledge integration, and proposes Wissen assets through the same approval queue.
- **Tabelle / Spalte / Zelle** (table / column / cell) — a column is a typed action per row; a cell carries value, status, cost, provenance. The platform's core operating surface.
- **Workflow** — a deterministic, named, dry-run-able process (same input → same steps → same output).
- **Run** — one record shape for every execution (pipeline/chain/job/sourcing): status, item counts, credits.
- **Integration** — an adapter resolved by CATEGORY (email, LinkedIn, CRM, calendar…), never by vendor name.
- **Playbook** — a named bundle of pinned Wissen-Assets + Tabelle segments + Workflow config.
- **Agent** — bounded, gated judgment on a single case, always inside a Workflow.
- **Command** — the one chat surface (Command Center for clients; the MCP connection for operators + external agents).

Object model in one line: *Sources fill Tabellen; Playbooks bind Tabelle segments + pinned Wissen; Workflows/columns/Agents process rows; outreach executes through Integrations; outcomes land on the Run and the Tabelle; Learnings propose Asset revisions back into Wissen.*

## Which surface: CLI vs MCP

Both speak to the SAME workspace endpoint (`/api/mcp/<key>`) and expose the SAME tools. Pick by where you run:

| You are… | Use | Why |
|---|---|---|
| A **shell-capable** agent (Claude Code, Codex, a script) | the **`gtm` CLI** | one command per step, `--json` for parseable output, discoverable via `--help`, no SDK to import |
| An agent **docked at the MCP endpoint** (Command Center, an MCP client) | the **MCP tools** directly | the tools are already in your toolset; no shell needed |

Same tools underneath — a CLI verb like `gtm column run` just calls the `workspace_table_run_column` tool. If one path is available to you, you don't need the other.

## Using the `gtm` CLI (shell agents)

`gtm --help` is the full reference. The essentials:

```bash
# Discover — always start here
gtm --help                 # command groups + global flags
gtm <command> --help       # per-command flags
gtm tools                  # every tool on THIS workspace (name + description)
gtm tools --json           # machine-readable

# Auth (key from workspace settings → MCP integration; Starter plan+)
gtm login --key <key>      # stored in ~/.gtm/config.json (0600)
gtm whoami                 # verify key + show workspace, no credits spent

# Ergonomic verbs for the common table/Wissen ops
gtm tables list                          # every Tabelle
gtm table get <tableId|name> [--limit 20 --offset 40]
gtm table schema [tableId|name]          # data model (tables/columns/relations) + Wissen assets
gtm column run <tableId|name> <columnKey> --mode dry_run     # FREE cost preview
gtm column run <tableId|name> <columnKey> --max-credits 10   # live paid run (hard cap)
gtm wissen list [--kind icp]
gtm wissen get <assetId>

# Generic escape hatch — ANY tool from `gtm tools`, even without an ergonomic verb
gtm call research_company --input '{"company_name":"Acme GmbH","domain":"acme.io"}' --json
gtm call find_companies --query "solar installers" --limit 5    # key/val pairs, server coerces types
```

Rules of the road:
- `--input` (alias `--args`) carries the tool PAYLOAD as a JSON object; `--json` only ever controls OUTPUT format. So you can send JSON in and get JSON back on one call.
- Use `--json` everywhere for stable, parseable output.
- Exit codes let you branch: `0` ok · `2` usage · `3` no creds · `4` bad key (401) · `5` plan-gated (403) · `6` rate-limited (429) · `7` network · `8` the tool ran but returned an error.
- Credentials resolve: `--key`/`--url` flags → `GTM_API_KEY`/`GTM_BASE_URL` env → `~/.gtm/config.json`.

## Using the MCP tools (docked agents)

Discovery-first, same as the CLI. Then the core surface:

**Read the model — never guess:**
- `workspace_schema_get` — the connected model (tables → columns → relation edges) AND Wissen `assets` (id, kind, name, status, revision). Optional `table` narrows to one. **Call this before creating or running anything.** Don't invent table ids or column keys.
- `workspace_tables_list` — every Tabelle (id, name, entity_binding, row_count). Reuse before you create.
- `workspace_table_get({ table, limit?, offset? })` — a table's columns + a page of rows (limit default 50, cap 200).

**Write rows / cells:**
- `workspace_table_add_row({ table, values })` — one row; `values` keys must already exist as columns (an unknown key is rejected with the list of valid ones). On a **company-bound** table the row does come back with an `entity_id` and `{{company.name}}`/`{{company.domain}}` resolve from it (verified live) — so it is usable for a real test, not only a dummy. For bulk entity-bound rows still use `workspace_table_import_from_playbook({ table, playbook, max_rows })` or a source column.
- `workspace_table_update_cell({ table, row_id, column_key, value })` — only `manual`/`relation` cells; computed cells (ai/enrichment/formula/tool/system) are refused so you can't overwrite a run's output.

**Run columns (the paid contract):**
- `workspace_table_run_column({ table, column_key, mode?, max_credits?, row_ids? })`:
  - `mode: 'dry_run'` → **free, synchronous, no writes**; returns `{ rows, estimated_credits, sample_inputs }`. Always do this first for `ai`/`enrichment` columns.
  - `mode: 'live'` (default) → executes. **A live run of a paid (ai/enrichment) column REQUIRES `max_credits`** (> 0, a hard per-run cap). Without it the tool refuses and hands back the estimate. Live runs are async (returns a `job_id` — poll with `workspace_table_get`). Over the cap, remaining cells are skipped `max_credits_reached` and the run finalizes cleanly. **No automatic retries.**

**Wissen (read as context, review the Learnings queue):**
- `wissen_asset_list({ kind?, status? })` — metadata only (id, kind, name, status, revision). Pass `status: 'proposed'` to find Learnings the system has distilled from booked meetings and replies and queued for approval.
- `wissen_asset_get({ asset_id })` — the current revision's typed content + history.
- `wissen_asset_create` / `wissen_asset_revise` — author or version an Asset (immutable revisions).
- `wissen_asset_approve({ asset_id, decision: 'approve' | 'reject' })` — the gate: a proposed Learning only starts feeding prompts (qualification, copy) once approved; `reject` discards it. Nothing distilled is injected into a prompt automatically — a human (or you, on their behalf) reviews the queue first.

**Author tables/columns** (build-time — see build-gtm-workflow for the full flow): `workspace_table_create`, `workspace_table_add_column`, `workspace_table_update_column` (run_condition + config), `workspace_table_update`, `workspace_table_delete_column`, `workspace_table_dependencies`, `workspace_table_cascade_preview`.

`explain_system` re-fetches the whole orientation as structured JSON any time.

## Recipes (copy, adapt)

Shown as CLI; the MCP equivalent is the tool named in each `gtm call`/verb.

### 1. Orient, then read a table
```bash
gtm tools --json                      # what's available here
gtm table schema --json               # tables, columns, relations, Wissen assets
gtm table get Leads --limit 20 --json # a page of rows
```

### 2. Enrich a column — preview cost, then spend within a cap
```bash
# 1) FREE preview — how many rows, how many credits
gtm column run Leads email_enrich --mode dry_run --json
# 2) live run, hard-capped; returns a job id, poll the table for results
gtm column run Leads email_enrich --max-credits 25 --json
gtm table get Leads --limit 50 --json      # verify cells: values present, status succeeded
```
> A green enqueue is NOT a green result — read the cells back before claiming done.

### 3. Source rows, then enrich them (entity-bound)
```bash
# bring a playbook's existing companies/leads in as entity-bound rows (idempotent)
gtm call workspace_table_import_from_playbook --input '{"table":"Leads","playbook":"DACH Solar","max_rows":200}' --json
# then run the enrichment column on the fresh rows (preview → capped live), as in recipe 2
```

### 4. Check a sequence actually has steps
```bash
gtm call list_sequences --json
gtm call get_sequence --input '{"sequence_id":"<id>"}' --json   # READ the step list
```
> A sequence with ZERO steps — created, wired to an enroll column, believed to be live — is
> one of the most common build faults there is. It sends nothing and reports no error.

### 5. Read Wissen for context
```bash
gtm wissen list --kind icp --json
gtm wissen get <assetId> --json       # current ICP revision content
```

### 6. Review the Learnings approval queue
```bash
gtm call wissen_asset_list --input '{"status":"proposed"}' --json          # what the system distilled, awaiting review
gtm call wissen_asset_get --input '{"asset_id":"<id>"}' --json             # read the proposed content before deciding
gtm call wissen_asset_approve --input '{"asset_id":"<id>","decision":"approve"}' --json   # or "decision":"reject"
```
> A proposed Learning sits inert until approved — approval is what lets it start feeding qualification/copy prompts. Confirm the workspace has Wissen available (`workspace_capabilities`) before relying on it being there.

## Guardrails (non-negotiable)

- **Paid runs need a budget.** A live `ai`/`enrichment` run without `max_credits` is refused by design. Preview with `dry_run` first. Never run an unbounded paid column.
- **No auto-retry.** Runs never silently retry and burn credits — a re-run is a deliberate act.
- **Sends are gated, not absent.** A GENERIC `tool` column hard-refuses every send category (fail-closed — no adapter is even resolved). Sending runs through the dedicated **outreach terminal column**, which routes into the shipped, gated enroll machinery before that refusal applies: contactability (unsubscribe + blacklist) is checked deny-only and fails closed, and it sends only in its own run (`auto_run` on it is opt-in and requires a `run_condition`). "A tool column cannot send" is true; "the platform cannot send" is not. See **sequences** and **gtm-handoffs**.
- **Mutations are proposals.** Any live, paid, or external-write action assumes a human approves consequential changes. The same applies to Learnings: a distilled insight is a proposal until `wissen_asset_approve` accepts it.
- **Never cross workspaces.** Every call is scoped to the workspace behind your key. There is no `{{marketplace.*}}`/`{{platform.*}}`; a column only ever sees THIS workspace's data.
- **Resolve integrations by CATEGORY, never a vendor id** — the connected adapter can change under you.
- **Verify before claiming done** — read the cells/rows back; check status, not just a queued job.
