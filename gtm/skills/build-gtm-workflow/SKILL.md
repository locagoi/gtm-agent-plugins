---
name: build-gtm-workflow
description: Use when building a repeatable GTM workflow (sourcing → enrichment → qualification → copy → enrollment, or any subset) as a workspace TABLE that an agent operates — via Command or Claude Code. Covers the build-time wiring (create table, add module columns, map inputs/outputs, set the cascade), the deterministic run, scale (bulk + budget), and saving the built workflow as a reusable TEMPLATE to replicate on any playbook/workspace. This is the agent-facing "build a play" workflow on the relational tables model.
allowed-tools: Bash, Read, Grep, Glob
---

# Build a GTM workflow as a table

Build a **repeatable, deterministic** GTM workflow as a workspace **table**: each column is a typed step, the dependency graph + cascade runs them in order, and every cell is a typed value or an explicit failure. You wire it ONCE (build-time); the engine replays it for any number of rows (run-time). Then save it as a **template** to replicate.

**Mental model (read once):** a *workflow* = the table's frozen column config. A *column* = a typed action per row (`source`/`enrichment`/`ai`/`tool`/`formula`/`relation`). *Inputs* = `{{cell.X}}` (sibling column) · `{{entity.X}}`/`{{company.X}}`/`{{lead.X}}` (linked entity) · `{{asset.X}}` (bound Wissen asset). *Output* = the column's `output_schema` (the predictability contract — every row conforms or is `failed`, never garbage). Build-time = the agent wires; run-time = deterministic replay, no agent, no guessing.

All operations are the `workspace_table_*` / `wissen_*` MCP tools (flag `workspace_tables_enabled`). Do them in order.

> For the broader **operating** guide — the CLI-vs-MCP choice, the `gtm` CLI commands (`cli/README.md`), reading/sourcing/enriching, and the paid-run guardrails — see the **gtm-operate** skill. This skill is the narrower "build a repeatable play as a table → save as template" flow.

## 0. Read the model first — NEVER guess

- `workspace_schema_get` FIRST — returns the connected model (tables, columns, relation edges) for this workspace. Read it before creating anything.
- `workspace_tables_list` to see existing tables. Reuse before you create.
- Decide `entity_binding`: `company` or `lead` (rows link to that entity spine) or none (standalone).

## 1. Create the table

`workspace_table_create({ name, entity_binding, description, columns? })`. Start minimal — you'll add module columns next. (Agent-facing create validates every column config; you can't create an invalid column.)

## 2. Get entity-bound ROWS in (never orphan rows)

Rows must carry `entity_id` (a lead/company) or a bound column's dry-run sees empty inputs.
- **From the playbook's existing companies/leads:** `workspace_table_import_from_playbook({ table, playbook, max_rows })` — materializes them as ENTITY-BOUND rows (idempotent by natural key).
- **From a source module** (GMaps/Apify etc.): a `source` column / the source-run path fills rows entity-linked.
- `workspace_table_add_row` exists but creates an UNBOUND row — only for a quick manual test, not for a real play.

## 3. Add the module columns (the workflow steps)

`workspace_table_add_column({ table, key, name, kind, data_type, config })`. Pick `kind` by what the step does:

| Step | kind | config essentials |
|---|---|---|
| Web research / enrichment | `enrichment` | category (e.g. `company_research`), instruction, **`output_schema`** |
| LLM-only (copy, classify, reason) | `ai` | `prompt` (with `{{...}}` refs), model, **`output_schema`** |
| Deterministic transform | `formula` | `expression` (uses `{{cell.X}}`) |
| Terminal action (CRM push, tool) | `tool` | `category`, `tool?`, `args_template` |
| Link to another table's row | `relation` | `target_table_id`, `display_column` |

**Rules that matter:**
- **`output_schema` is mandatory for predictability** on ai/enrichment — it's the typed contract sent to the provider (jsonMode) + validated on return; off-schema → cell `failed`, never garbage. Same shape at 40 or 4000 rows.
- **Inputs via `{{...}}`** — reference upstream columns (`{{cell.owner}}`), the linked entity (`{{company.name}}`), or a bound Wissen asset (`{{asset.icp}}`). The dependency graph reads these → cascade order. Only referenced keys are injected (cheap).
- **Adapter-agnostic** — resolve by CATEGORY, never a vendor id. Outreach/enrichment/CRM EXECUTION runs through the connected **provider MCP** (Instantly/HeyReach/FullEnrich/…); our columns orchestrate.
- **Bind Wissen for context** — pin an asset to the playbook (`playbook_asset_pin`) so `{{asset.icp}}` resolves the versioned ICP; provenance records the revision.

## 4. Wire the cascade (make it run itself)

- `workspace_table_update_column({ ..., auto_run: true })` per column that should run automatically.
- `workspace_table_update_column({ ..., run_condition })` — a Domino gate (e.g. run copy only if `icp_score` ≥ X).
- `workspace_table_update({ table, auto_advance: true })` — a NEW row auto-runs the entry columns → the whole chain cascades.
- `workspace_table_dependencies({ table })` — inspect the derived graph (edges, entry columns, cycles) before enabling.

## 5. Preview cost + cascade BEFORE a live paid run

- `workspace_table_cascade_preview` — worst-case rows × per-cell cost.
- A live paid run REQUIRES a `max_credits` ceiling; cells over the cap are skipped `max_credits_reached`, the run finalizes cleanly. Money-audit is built in — never run an unbounded paid column.
- Scale: for large N, prefer the provider's BULK path where available (bulk enrichment is a fast-follow). The job queue batches + is resumable (per-cell status; re-run only touches pending/failed; no auto-retry).

## 6. Run it

- Add rows (step 2) → with `auto_advance` the cascade runs. Or run one column: `workspace_table_run_column({ table, column, max_credits })` (enqueues a job; poll the grid / `list_jobs`).

## 7. Save as a TEMPLATE → replicate

Once the workflow is clean:
- `workspace_table_save_as_template({ table, name, description })` — freezes the column config (structure only, no rows/cells/credentials).
- `workspace_table_from_template({ template, new_table_name, entity_binding?, relation_table_map? })` — recreates the workflow on any playbook/workspace, validated. Relation columns need a `relation_table_map` or are skipped with a warning.
- `workspace_table_templates_list()` — the workspace's saved templates.

This is the replicability loop: **build once → save_as_template → from_template → identical deterministic workflow.**

## Gotchas (learned from shipping)

- **Read `workspace_schema_get` first.** Don't invent column keys or table ids.
- **Formula stores its template in `config.expression`** (not `config.formula`) — the dependency graph + cascade read `expression`.
- **`{{asset.X}}` needs a bound/pinned Wissen asset** on the playbook, else it resolves empty.
- **Cross-workspace insights are admin-only** — no `{{marketplace.*}}`/`{{platform.*}}`; a column only ever sees THIS workspace's data.
- **Deleting a referenced column is blocked** — remove the `{{cell.X}}`/run_condition references first (`workspace_table_delete_column` enforces this).
- **Terminal SEND is gated** — the tool sink refuses send categories without the contactability path (Phase-1 is non-sending; CRM/neutral only).
- **Verify before claiming done** — check the cells actually succeeded (values present, status succeeded) via the grid or a query; a green enqueue is not a green result.

## The two surfaces

This skill drives **Claude Code** (operator/builder — full power). **Command Center** (customer chat) operates the SAME primitives but gets this guidance as injected context (no filesystem/CLI). Same tools, same tables, one substrate. For day-to-day operating (not building) over either surface, see **gtm-operate**.
