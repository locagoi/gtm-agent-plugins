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

### Use the prebuilt agent columns

Three columns ship with a tested prompt and output schema. Use them instead of writing your
own — they are what `workspace_capabilities` returns under `prebuilt_agent: true`, and their
`preset` block carries the prompt, the `output_schema` and the `args_template`:

| Module id | Does | Returns |
|---|---|---|
| `agent:icp_fit` | live web research against the ICP | `fit_score` 0–100 · `tier` A/B/C · `reasoning` · matched/missing criteria |
| `agent:buying_signals` | current triggers for the company | `signals[]` · `signal_strength` · `summary` |
| `agent:persona_fit` | is this contact the target persona | `matches_persona` · `confidence` · `reasoning` |

`agent:persona_fit` already references `{{asset.persona}}` — so pin the persona asset to the
playbook or it resolves empty.

### Know what a row costs before you run it

| Module | Credits per row |
|---|---|
| `base:contact_enrichment` (email + phone) | **25** |
| `base:solar_analysis` | 2 |
| `agent:icp_fit` · `agent:buying_signals` · `base:web_research` · `base:find_leads` · `base:email_validation` · `base:geocode` | 1 |
| `base:create_lead` · `base:resolve_contact` · formula · relation · manual | 0 |

Contact enrichment is 25× the cost of qualification. **That single fact decides the shape of
every play in this folder:** qualify first, enrich last, and gate the enrichment column on the
qualification verdict. A play that enriches before it qualifies costs roughly twenty times
what it needs to.

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
| `job_title` | `{{lead.title}}` |

Those are the defaults, not a contract. Take what the source actually gives you and drop what
it does not: a Maps-sourced table has no `employee_count` worth showing, a post-engager table
has no `country`. Add the one field that is specific to *this* play, if there is one, and stop
there.

**Then be strict.** Every further column costs money to fill, space to read, and attention to
maintain. Before adding one, answer: *who reads this, and what do they do differently because
of it?* If the answer is "it might be useful later", it is not a column, it is clutter. A
table a person can scan beats a table that knows everything.

## The shape every play shares

```
source  →  qualify (cheap)  →  GATE  →  enrich (expensive)  →  copy  →  ENROLL (terminal)
```

And the four rules that hold in all nine:

1. **Gate before you spend.** `run_condition` on every column that costs more than 1 credit.
2. **Closed lists, never free text**, for anything you will count later.
3. **Twenty rows, read by a human**, before the first enrollment.
4. **The enroll column is last**, sends only in its own run, and `auto_run` is rejected.

## Running a play

1. Read the play file end to end before the first call.
2. Check `workspace_capabilities` for the sources and modules it needs.
3. Build it. Run 20 rows. Read them.
4. Save it: `workspace_table_save_as_template` — the second workspace takes an hour.

Deep dives: table mechanics in **build-gtm-workflow**, touch plans in **sequences**, the
strategy layer in **draft-gtm-play**, and what to build at all in **outbound-playbook**.
