---
name: build-gtm-workflow
description: Use when building a repeatable GTM workflow (sourcing → enrichment → qualification → copy → enrollment, or any subset) as a workspace TABLE that an agent operates — via Command or Claude Code. Covers the build-time wiring (create table, add module columns, map inputs/outputs, set the cascade), the deterministic run, scale (bulk + budget), and saving the built workflow as a reusable TEMPLATE to replicate on any playbook/workspace. This is the agent-facing "build a play" workflow on the relational tables model.
allowed-tools: Bash, Read, Grep, Glob
---

# Build a GTM workflow as a table

Build a **repeatable, deterministic** GTM workflow as a workspace **table**: each column is a typed step, the dependency graph + cascade runs them in order, and every cell is a typed value or an explicit failure. You wire it ONCE (build-time); the engine replays it for any number of rows (run-time). Then save it as a **template** to replicate.

**Mental model (read once):** a *workflow* = the table's frozen column config. A *column* = a typed action per row (`source`/`enrichment`/`ai`/`tool`/`formula`/`relation`). *Inputs* = `{{cell.X}}` (sibling column) · `{{entity.X}}`/`{{company.X}}`/`{{lead.X}}` (linked entity) · `{{asset.X}}` (bound Wissen asset). *Output* = the column's `output_schema` (the predictability contract — every row conforms or is `failed`, never garbage). Build-time = the agent wires; run-time = deterministic replay, no agent, no guessing.

**Where the table lives:** the table is the deterministic-execution layer of a **Playbook** — the strategic paper that references its Wissen assets + Tabellen + automations. The surfaces around it are Playbook (strategy) · Tabellen (execution) · the prioritized lead surface · Wissen (knowledge). Qualification/copy columns should reference the playbook's Wissen assets via `{{asset.icp}}`/`{{asset.offer}}`/`{{asset.messaging_angle}}`; source columns can act on the **`signal` Wissen asset class** (buying signals referencing ICP/Offer) to keep the table filled with *hot* rows. See `draft-gtm-play` for the strategy-first sequencing.

All operations are the `workspace_table_*` / `wissen_*` MCP tools. Do them in order.

> **Start with the shape, not the tools:** `three-table-play.md` next to this file is the
> canonical layout — accounts → people → outreach, with a scored gate between each stage,
> column by column, with the thresholds and the build order. Read it before you create the
> first table. For the whole-workspace build order see `gtm-quickstart`; for the broader
> operating guide (CLI-vs-MCP, sourcing, paid-run guardrails) see `gtm-operate`.

## 0. Read the model first — NEVER guess

- `workspace_schema_get` FIRST — returns the connected model (tables, columns, relation edges) for this workspace. Read it before creating anything.
- `workspace_tables_list` to see existing tables. Reuse before you create.
- Decide `entity_binding`: `company` or `lead` (rows link to that entity spine) or none (standalone).

## 1. Create the table

`workspace_table_create({ name, entity_binding, description, columns? })`. Start minimal — you'll add module columns next. (Agent-facing create validates every column config; you can't create an invalid column.)

## 2. Get entity-bound ROWS in (never orphan rows)

Rows must carry `entity_id` (a lead/company) or a bound column's dry-run sees empty inputs.
- **From the playbook's existing companies/leads:** `workspace_table_import_from_playbook({ table, playbook, max_rows })` — materializes them as ENTITY-BOUND rows (idempotent by natural key).
- **From a source module** (maps/company search/social — whatever this workspace has): a `source` column / the source-run path fills rows entity-linked. `workspace_capabilities` lists the sources actually available here.
- `workspace_table_add_row` adds one row at a time; on a company-bound table it comes back with an `entity_id` and the `{{company.*}}` refs resolve (verified live). Fine for a controlled test, too slow for a real play.

## 3. Add the module columns (the workflow steps)

`workspace_table_add_column({ table, key, name, kind, data_type, config })`. Pick `kind` by what the step does:

| Step | kind | config essentials |
|---|---|---|
| Web research / enrichment | `enrichment` | category (e.g. `company_research`), instruction, **`output_schema`** |
| LLM-only (copy, classify, reason) | `ai` | `prompt` (with `{{...}}` refs), model, **`output_schema`** |
| Deterministic transform | `formula` | `expression` (uses `{{cell.X}}`) |
| Terminal action (CRM push, tool) | `tool` | `category`, `tool?`, `args_template` |
| Link to another table's row | `relation` | `target_table_id`, `display_column` |

**Write the sequence before this table.** The sequence defines which variables exist; this
table exists to fill exactly those. Take the inventory of its `{{...}}` slots first, then build
one column per slot and no others. See `sequences`.

**Start with the identity block.** Before any processing column, add the few fields that let a
person recognise the row: a company table shows name, country, industry, website and size; a
lead table shows full name, salutation and job title. Take what the source actually delivers,
drop the rest, and add at most one field specific to this play.

Then hold the line: every further column costs credits to fill and attention to read. Before
adding one, answer *who reads this and what do they do differently because of it?* "Might be
useful later" is not an answer.

**Rules that matter:**
- **`output_schema` is mandatory for predictability** on ai/enrichment — it's the typed contract sent to the provider (jsonMode) + validated on return; off-schema → cell `failed`, never garbage. Same shape at 40 or 4000 rows.
- **Inputs via `{{...}}`** — reference upstream columns (`{{cell.owner}}`), the linked entity (`{{company.name}}`), or a bound Wissen asset (`{{asset.icp}}`). The dependency graph reads these → cascade order. Only referenced keys are injected (cheap).
- **Adapter-agnostic** — resolve by CATEGORY, never a vendor id. Outreach/enrichment/CRM EXECUTION runs through whichever **provider is connected for that category** in this workspace; our columns orchestrate. Call `list_integrations` to see what that is here — never hardcode a provider.
- **Bind Wissen for context** — pin an asset to the playbook (`playbook_asset_pin`) so `{{asset.icp}}` resolves the versioned ICP; provenance records the revision.
- **Closed lists, never free text.** Any column whose output you will later count — a
  qualification verdict, a disqualification reason, an industry label, a persona name, a case
  study pick — must choose from an `enum` in its `output_schema`. Free text aggregates into
  nothing: reasons fragment into near-unique strings and one industry ends up spelled several
  ways, so the obvious question ("what disqualifies most of my list?") cannot be answered at
  all.
- **Verdict columns return a reason.** A bare boolean is unauditable — when the fit rate comes
  back at 30 % you need twenty reasons to know whether the ICP or the source is wrong.
- **Gate the expensive columns.** A `run_condition` on enrichment (`icp_fit.fit == true`) is
  where the credit bill is actually decided — you only pay to enrich what qualified.

## 3b. Order the columns left to right

Build them in the order they execute, and gate each on a column to its **left**: identity →
cheap verdict → gate → expensive enrichment → copy fills → enroll. A person scanning the grid
left to right then sees where each row stopped and why, and the visual order matches the order
`workspace_table_dependencies` derives from the `{{cell.x}}` references. Never place a column
left of the one it depends on, and never gate on a column further right.

## 4. Wire the cascade (make it run itself)

- `workspace_table_update_column({ ..., auto_run: true })` per column that should run automatically.
- `workspace_table_update_column({ ..., run_condition })` — the Domino gate. **It is a structured
  object, not an expression string** (verified against a live workspace):

  ```json
  { "column": "icp_fit.fit_score", "op": "gte", "value": 60 }
  ```

  Ops: `is_empty` · `is_not_empty` · `equals` · `not_equals` · `contains` · `gt` · `lt` · `gte` ·
  `lte`. Combine with `{ "all": [...] }` or `{ "any": [...] }`, nestable three levels.

  **Dotted sub-field paths into a JSON cell work** — `icp_fit.fit_score` reads into the cell's
  JSON, confirmed in both directions on live data. But note that an unknown path is **accepted
  at write time** and simply never matches, so a typo becomes a gate that silently stops every
  row. Prove it with a dry run: the response reports `rows_skipped_by_condition`.

  A `run_condition` also creates a **dependency edge** — gating `enroll` on `icp_fit` makes
  `icp_fit` upstream of `enroll` in `workspace_table_dependencies`, even with no `{{cell.x}}`
  reference between them.
- `workspace_table_update({ table, auto_advance: true })` — a NEW row auto-runs the entry columns → the whole chain cascades.
- `workspace_table_dependencies({ table })` — inspect the derived graph (edges, entry columns, cycles) before enabling.

## 5. Preview cost + cascade BEFORE a live paid run

- `workspace_table_cascade_preview` — worst-case rows × per-cell cost.
- A live paid run REQUIRES a `max_credits` ceiling; cells over the cap are skipped `max_credits_reached`, the run finalizes cleanly. Money-audit is built in — never run an unbounded paid column.
- Scale: for large N, prefer the provider's BULK path where available. The job queue batches and is resumable (per-cell status; a re-run only touches pending/failed; no auto-retry).

## 6. Run it

- Add rows (step 2) → with `auto_advance` the cascade runs. Or run one column: `workspace_table_run_column({ table, column, max_credits })` (enqueues a job; poll the grid / `list_jobs`).
- **The first run is 20 rows, and a human reads the output.** Then 20 generated messages,
  read before anything is enrolled. An unbounded first run is the most expensive mistake
  available in the product.

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
- **No cross-workspace reads** — there is no `{{marketplace.*}}`/`{{platform.*}}`; a column only ever sees THIS workspace's data.
- **Deleting a referenced column is blocked** — remove the `{{cell.X}}`/run_condition references first (`workspace_table_delete_column` enforces this).
- **Terminal SEND is gated, not absent** — a GENERIC tool column hard-refuses every send category (fail-closed: no adapter is even resolved). Sending runs through the dedicated **outreach terminal column**, which routes into the shipped, gated enroll machinery before that refusal applies. It sends only in its own run, never on create, and `auto_run` is rejected for it.
- **The seams between the bricks are their own guide** — which handoffs exist (Wissen → Playbook → Tabelle → Sequenz, the Workflow's three), what creates each, and which ones do NOT exist: see **gtm-handoffs**, or read `handoffs.legend` from `workspace_schema_get` for the live version.
- **Verify before claiming done** — check the cells actually succeeded (values present, status succeeded) via the grid or a query; a green enqueue is not a green result.

## The two surfaces

This skill drives **Claude Code** (operator/builder — full power). **Command Center** (customer chat) operates the SAME primitives but gets this guidance as injected context (no filesystem/CLI). Same tools, same tables, one substrate. For day-to-day operating (not building) over either surface, see **gtm-operate**.
