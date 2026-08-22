---
name: plays
description: Use when the user names a motion to build — local business outreach, LinkedIn post engagers, keyword/social signals, job-opening scraping, inbound lead qualification, website-visitor outreach, lost-deal reactivation, CRM blacklist reconciliation, reply-to-meeting, or mining a CRM for the ICP. Ships nine ready-to-run play templates, each with the exact sources, columns, gates and tool calls, plus the shared catalogue of what a workspace can source and what each column costs. Run a play end to end without asking the user which tool to use.
allowed-tools: Bash, Read, Grep, Glob
---

# Plays: ready-to-run motions

Nine templates. Each is a complete build — sources, columns, gates, sequence, enrollment —
with the tool calls written out, so you can take a named motion from "build me X" to running
without stopping to ask which module does what.

| Play | Trigger | File |
|---|---|---|
| **Local business outreach** | you have a region and a trade | `local-business-outreach.md` |
| **Own-post engagers** | someone posts on LinkedIn and people react | `own-post-engagers.md` |
| **Keyword / competitor signals** | a topic is being discussed publicly | `keyword-signals.md` |
| **Job openings** | hiring is the buying signal | `job-openings.md` |
| **Inbound lead qualification** | a form, a chatbot, a partner feed | `inbound-qualification.md` |
| **Website visitor outreach** | someone visits and does not fill the form | `web-visitor-outreach.md` |
| **Lost deal reactivation** | the CRM has a graveyard | `lost-deal-reactivation.md` |
| **CRM blacklist reconciliation** | sales must never be shadowed by outbound | `crm-blacklist-sync.md` |
| **CRM mining for the ICP** | won deals already know who buys | `crm-mining.md` |

**Reply-to-meeting is not in this list** — the platform ships it as an installable workflow
template. See "Install, do not build" below.

## Before any play: read the workspace

```bash
gtm call workspace_capabilities --json
```

This is the live catalogue for **this** workspace: every source with `paid` / `connected` /
`suggested`, every column module with its `cost_per_row` and the `create_tool` that makes it.
Never assume a source exists — the list differs per workspace, and `connected: false` on a
paid source means it will refuse.

### The eleven sources

| Source | Fills with | Paid | How |
|---|---|---|---|
| `pool` | companies from the platform pool | free | `workspace_table_add_source` |
| `lookalike` | companies resembling your own winners | free | `workspace_table_add_source` |
| `scraping` | Google Maps businesses | **paid** | `workspace_table_add_source` |
| `lead_sourcing` | LinkedIn company search | **paid** | `workspace_table_add_source` |
| `indeed_jobs` | companies with matching job postings | **paid** | `workspace_table_add_source` |
| `generic_actor` | any catalog scraper actor (needs `actor_id` + `field_mapping`) | **paid** | `workspace_table_add_source` |
| `post_engagers` | companies behind the reactions to one post | free | `workspace_table_add_source` |
| `job_change` | new decision makers | free | **schedule only** |
| `profile_posts` | everyone engaging with ONE profile's own posts | free | **schedule only** |
| `social_listening` | companies engaging with your keywords | free | **schedule only** |
| `webhook` | whatever an external tool POSTs | free | `create_webhook_source` |

**Three are schedule-only** — `job_change`, `profile_posts`, `social_listening` take
`workspace_table_schedule_source`, not `add_source`. They are loops, not imports.

**Every paid source requires `max_credits`.** Without it the call refuses and hands back an
estimate. Attach → run once small → *then* schedule. A schedule turns a source into recurring
cost.

### Every add-column call needs four things

`workspace_table_add_column` requires **`table`, `name` and `data_type`** — and, for anything
that is not a plain manual field, **`kind` plus a `config` that is complete for that kind**.
A call missing one of them is refused before anything is created:

| Field | | Notes |
|---|---|---|
| `table` | **required** | name or id |
| `name` | **required** | the human-readable column label |
| `data_type` | **required** | `text` · `number` · `boolean` · `datetime` · `json` |
| `key` | optional | derived from `name` when omitted |
| `kind` | optional | `manual` (default) · `ai` · `enrichment` · `relation` · `formula` · `tool` |
| `config` | per kind | required for `ai`, `enrichment`, `relation` and `tool` |
| `run_condition` | optional | the gate — must name a column that already exists |

`data_type` is `json` for every column that returns an object — which is every agent column
below, and the reason you can gate on `icp_fit.fit_score` at all. A typed verdict in a `text`
cell is a string, and a `gte` gate on a string does not do what you want.

What each `kind` needs in `config`:

| Kind | `config` must carry |
|---|---|
| `ai` | `prompt` (non-empty). Optional `model`, `output_schema`, `role` |
| `enrichment` | `category` **and** `args_template`. Research instructions go in `args_template.instructions` — a `prompt` key here is **rejected** |
| `relation` | `target_table_id`, `display_column` |
| `tool` | `category`, or for the outreach terminal: `channel` + `sequence_id`/`campaign_id` |

The enrichment categories are `contact_enrichment`, `email_validation`, `company_research`,
`solar_analysis`, `geocode`, `find_leads`, `create_lead`, `research_people`, `resolve_contact`.
`create_lead` additionally requires all three of `target_table_id`, `relation_column` and
`owner_source_column`.

### Use the prebuilt agent columns

Three presets ship with a tested prompt and output schema. They are what
`workspace_capabilities` returns in the `agents` group, each carrying a `preset` block with
the prompt, the `output_schema` and (for research agents) the `args_template`.

| Preset id | Kind | Category | Returns |
|---|---|---|---|
| `agent:icp_fit` | `enrichment` | `company_research` | `fit_score` 0–100 · `tier` A/B/C · `reasoning` · matched/missing criteria |
| `agent:buying_signals` | `enrichment` | `company_research` | `signals[]` · `signal_strength` · `summary` |
| `agent:persona_fit` | `ai` | — | `matches_persona` · `confidence` · `reasoning` |

**A preset is content you copy, not an id you reference.** There is no `module` field in a
column config — read the preset from `workspace_capabilities` and pass its parts through:

```bash
# 1. read the preset for this workspace
gtm call workspace_capabilities --json    # → columns[].preset for id "agent:icp_fit"

# 2. create the column FROM that preset
gtm call workspace_table_add_column --input '{
  "table": "Accounts", "key": "icp_fit", "name": "ICP-Fit",
  "data_type": "json", "kind": "enrichment",
  "config": {
    "category": "company_research",
    "depth": "standard",
    "args_template": {
      "name": "{{company.name}}",
      "domain": "{{company.domain}}",
      "instructions": "<the preset prompt, plus anything specific to this play>"
    },
    "output_schema": {
      "type": "object",
      "properties": {
        "fit_score": { "type": "number" }, "tier": { "type": "string" },
        "reasoning": { "type": "string" },
        "matched_criteria": { "type": "array" }, "missing_criteria": { "type": "array" }
      },
      "required": ["fit_score", "tier", "reasoning"]
    }
  }
}' --json
```

Copying rather than referencing is what lets you edit the instruction per play — which you
will, because "fits our ICP" means something different for a roofer than for a SaaS buyer.

**`output_schema` is only accepted for `company_research`.** It is also what makes the column
predictable: without it the provider returns prose, and every gate downstream reads nothing.

**Always set `depth: "standard"` on a research column.** `company_research` defaults to
`quick`, and the engine's own note on that setting reads: *shallow enough that a flash model
can hallucinate*. It costs 2 credits instead of 1 and it is the difference between research
about this company and confident prose about a company with a similar name. `research_people`
already defaults to `standard` — which is why it costs **2**, not the 1 the catalog label
suggests.

`agent:persona_fit` is an `ai` column and its prompt references `{{asset.persona}}` — pin the
persona asset to the playbook or the slot resolves empty and the model qualifies against
nothing.

### The entity namespace follows the binding

A table's `entity_binding` decides which slots resolve, and the ones that do not resolve fail
**silently** — empty string, no error, a model qualifying against nothing.

| On a table bound to | These resolve | These do **not** |
|---|---|---|
| `company` | `{{company.name}}` · `.domain` · `.industry` · `.employee_count` · `.location` · `.country` · `.linkedin_url` | every `{{lead.*}}` |
| `lead` | `{{lead.first_name}}` · `.last_name` · `.full_name` · `.job_title` · `.email` · `.phone` · `.linkedin_url` · `.salutation` · **`.company_name`** · **`.company_domain`** | every `{{company.*}}` |

Two traps live in that table. The lead field is **`job_title`**, not `title`. And a lead-bound
table reaches its company through **`{{lead.company_name}}`** — `{{company.name}}` is blank
there, because the `company` namespace is only populated when the binding *is* company.

### Know what a row costs before you run it

| Module | Credits per row |
|---|---|
| `base:contact_enrichment` (email + phone) | **up to 25** — 10 per email found, 15 per phone found |
| `base:solar_analysis` · `base:research_people` (depth `standard` by default) · `base:web_research` at `depth: "standard"` | 2 |
| `base:web_research` at the `quick` default · `base:find_leads` · `base:email_validation` · `base:geocode` · an `ai` column | 1 |
| `base:create_lead` · `base:resolve_contact` · formula · relation · manual | 0 |

Every one of these is **success-only**: a miss costs nothing, and a contact that yields an
email but no phone costs 10, not 25. Budget with 25 anyway — that is the number the run
reserves per row, and a cap set to the average gets the run cut off half way through.

Contact enrichment is up to 25× the cost of qualification. **That single fact decides the
shape of every play in this folder:** qualify first, enrich last, and gate the enrichment
column on the qualification verdict. A play that enriches before it qualifies costs roughly
twenty times what it needs to.

## Install, do not build

The platform ships five workflow templates. Installing one is a single call and beats
rebuilding it:

```bash
gtm call list_workflow_templates --json
gtm call install_workflow_template --input '{"slug":"reply-to-meeting","playbook_id":"<id>"}' --json
```

| Slug | What it does |
|---|---|
| `reply-to-meeting` | classifies a reply, drafts the meeting proposal, books it — the whole reply→meeting path |
| `reply-triage` | classifies inbound replies and routes them |
| `post-engagers-to-linkedin-outreach` | the daily engager → table → qualify → LinkedIn enrollment chain |
| `crm-auto-enrich` | enriches CRM records as they appear |
| `deliverability-watch` | watches sender health and proposes a pause in the Feed |

There are also six house plays as structured data: `get_play(id)` for `lead_list_to_outreach`,
`recurring_source`, `enrich_existing_list`, `event_to_action`, `thought_leader_engagement`,
`external_api_to_column`.

## What every table shows

Before the first processing column, every table carries a small block of identity columns.
Not because the grid needs decoration, but because a person has to be able to look at a row
and know who it is without opening anything.

**A company-bound table shows, in this order:**

| Column | Source |
|---|---|
| `company_name` | `{{company.name}}` |
| `country` | `{{company.country}}` |
| `industry` | `{{company.industry}}` |
| `website` | `{{company.domain}}` |
| `size` | `{{company.employee_count}}` |

**A lead-bound table shows:**

| Column | Source |
|---|---|
| `full_name` | `{{lead.first_name}} {{lead.last_name}}` |
| `salutation` | the greeting column (see `sequences/copy-patterns.md`) |
| `job_title` | `{{lead.job_title}}` |

Those are the defaults, not a contract. Take what the source actually gives you and drop what
it does not: a Maps-sourced table has no `employee_count` worth showing, a post-engager table
has no `country`. Add the one field that is specific to *this* play, if there is one, and stop
there.

**Then be strict.** Every further column costs money to fill, space to read, and attention to
maintain. Before adding one, answer: *who reads this, and what do they do differently because
of it?* If the answer is "it might be useful later", it is not a column, it is clutter. A
table a person can scan beats a table that knows everything.

## Columns run left to right

**Build the columns in the order they execute, and gate each one on the column to its left.**
The grid is then readable as the process itself: identity, then the cheap verdict, then the
gate, then the expensive work, then the copy, then the enrollment. A person scanning left to
right sees where each row stopped and why.

```
identity  →  cheap qualification  →  GATE  →  enrichment  →  copy fills  →  ENROLL
company_name   icp_fit                       contact_data   anrede         enroll
country        signal                        email_valid    hook           (terminal)
industry       persona_fit
website
size
```

Every column after the first verdict carries a `run_condition` referring to a column to its
**left**, never to its right. Three consequences worth stating:

- **Cost follows the gate.** A row that fails qualification never reaches the 25-credit column.
- **Failure is visible.** An empty cell in column six with a filled gate in column three means
  the gate held, not that something broke.
- **The dependency graph matches the layout.** `workspace_table_dependencies` derives the run
  order from the `{{cell.x}}` references; when the visual order and the derived order agree,
  the table is comprehensible. When they disagree, somebody will misread it.

Never place a column left of the one it depends on, and never gate on a column further right.

## The shape every play shares

```
source  →  qualify (cheap)  →  GATE  →  enrich (expensive)  →  fill vars  →  ENROLL (terminal)
```

**And the sequence is written before any of it.** The sequence decides which variables exist;
the table fills exactly those. Write it first, take the inventory of its `{{...}}` slots, then
build one column per slot and no others. Building the table first produces columns nobody
references and variables nobody filled.

The seven rules that hold in all nine plays:

1. **Sequence first, then its variables.** Two is the target, three the ceiling. Write it with
   built-in slots, add the enroll column, then `update_sequence` to put `{{cell.*}}` in — the
   platform only accepts cell slots once an enroll column can feed them.
2. **Gate before you spend.** `run_condition` on every column that costs more than 1 credit.
3. **No empty variables.** Gate the enroll column on every fill — a structured
   `{ column, op, value }` object, not an expression string — and prove it with a free dry run,
   which reports `rows_skipped_by_condition`. Then read 20 rows including a sparse one.
4. **Closed lists, never free text**, for anything you will count later.
5. **Preflight before you schedule.** `workspace_table_preflight` answers, deterministically
   and for free, whether a new row runs through at all. The dry run prices one column; this
   says whether the chain moves and stops in the right place.
6. **Twenty rows, read by a human**, before the first enrollment.
7. **The enroll column is last**, sends only in its own run.

## Running a play

1. Read the play file end to end before the first call.
2. Check `workspace_capabilities` for the sources and modules it needs.
3. Build it. Run 20 rows. Read them.
4. Save it: `workspace_table_save_as_template` — the second workspace takes an hour.

Deep dives: table mechanics in **build-gtm-workflow**, touch plans in **sequences**, the
strategy layer in **draft-gtm-play**, and what to build at all in **outbound-playbook**.
