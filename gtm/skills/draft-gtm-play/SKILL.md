---
name: draft-gtm-play
description: Use when starting a NEW GTM campaign/play from scratch, or when the user asks "how do I run a campaign here", "draft a play", "set up outreach for X". The methodology layer ABOVE build-gtm-workflow — guides drafting the STRATEGY first (the playbook as a strategic paper: ICP → persona → offer → proof → signals as Wissen assets), then channels + automations, and only then the deterministic table workflow. Ensures campaigns are grounded in referenced knowledge instead of ad-hoc config.
allowed-tools: Bash, Read, Grep, Glob
---

# Draft a successful GTM Play

A **play** is not a table with columns — it's a strategy that a table executes. The platform separates three layers, and successful plays are drafted in this order:

1. **Wissen (knowledge)** — WHO you target and WHY you win: ICP, Persona, Offer, Proof, Messaging, **Signals**. Versioned assets, referenced everywhere, never copy-pasted.
2. **Playbook (strategy paper)** — the named bundle: which assets, which channels, which automations. The foundation the tables build on.
3. **Table (deterministic execution)** — the data workflow: source → qualify → enrich → personalize → enroll. Built once, replayed for any number of rows.

**The core discipline: strategy before mechanics.** A play whose ICP lives in a chat message dies in week two. A play whose ICP is a versioned asset referenced by every qualification column improves with every revision.

> Operating basics (CLI/MCP usage, credits, guardrails): see **gtm-operate**. Table mechanics: see **build-gtm-workflow**. This skill is the campaign methodology that sequences them.

## Phase 1 — Draft the knowledge (Wissen assets)

Interview the user if the substance is missing — never invent positioning. Create with `wissen_asset_create`, revise with `wissen_asset_revise` (immutable versions).

Draft in this order (each builds on the previous):

1. **ICP** (`icp`) — firmographics + the qualifying/disqualifying criteria. Concrete beats broad: "German Mittelstand manufacturers, 50–500 employees, complex B2B master data" outperforms "companies that need CRM".
2. **Persona** (`persona`) — the decision-maker: role, pains, what they're measured on.
3. **Offer** (`offer`) — what you sell them and the promise, in their language.
4. **Proof** (`proof`) — case studies, numbers, references. One strong proof per persona beats five vague ones.
5. **Messaging angle** (`messaging_angle`) — the hook that connects pain → offer.
6. **Signals** (`signal`) — the buying signals that make an ICP company *hot now* (hiring for a role, a new decision-maker, job postings, engagement). A signal asset **references the ICP and Offer assets it matters for** (`icp_refs`, `offer_refs`) and can map to a runtime detection (`signal_type_key`) so the platform's signal sources feed it. Plays that lead with a signal ("you're hiring 5 SDRs") convert multiples of plays that lead with an intro.

Quality gate before moving on: could a stranger read these six assets and pitch the company? If not, revise.

## Phase 2 — The playbook (strategic paper)

Create the playbook (`create_playbook`) and make it the bundle:

- **Connect the assets** — pin each asset to its slot (`playbook_asset_pin`). Pinned = this play's frozen strategy; assets keep evolving, the play chooses when to follow.
- **Choose channels** — email / LinkedIn / WhatsApp (`update_playbook` → `messaging_channels`). Channel choice follows the persona, not preference.
- **Define the automations** — what runs by itself: the reply agent, which outreach tools serve each channel (resolved by category from the workspace's connected integrations — never hardcode a vendor), the messaging sequence, skip-existing-contacts, timezone.

The playbook now answers: *who, why us, where, and what runs automatically.* Nothing else belongs in it — data work is the table's job.

## Phase 3 — The deterministic table (execution)

Now — and only now — build the workflow. Follow **build-gtm-workflow** end-to-end. The strategy phase pays off here:

- Qualification columns reference `{{asset.icp}}` — not a re-typed prompt.
- Personalization/copy columns reference `{{asset.offer}}`, `{{asset.proof}}`, `{{asset.messaging_angle}}` — and use **template + variables** copy (a fixed template with generated `{hook}`/`{pain_point}` fills) rather than free-form generation.
- Source columns implement the signal strategy: schedule the sources that detect your signal assets (job changes, job postings, post engagers) so the table refills itself with *hot* companies, not cold lists.
- Link the table to the playbook (`playbook_table_link`) so the play is one navigable bundle.
- Enrollment terminal columns carry the campaign target + field mapping; every enrollment passes the contactability gates.

Save the built table as a template (`workspace_table_save_as_template`) — the play becomes replicable across playbooks and workspaces.

## Phase 4 — Run, measure, revise

- Run bounded first: 10–20 rows, review qualification verdicts and copy BEFORE scaling. Paid runs always carry a credit cap.
- Measure where it matters: replies land in the feed; **signal → positive-reply attribution** shows which signal converts; meetings land as conversion outcomes.
- Feed it back: a losing angle → revise the messaging asset (new version, history kept). A signal that converts → weight it. The play gets smarter because the strategy is versioned knowledge, not chat history.

## Anti-patterns (each has burned real campaigns)

- **Table first, strategy never** — columns with hand-typed prompts that drift apart. Reference assets.
- **1:1 free-form copy at scale** — unpredictable output; use template + variable fills.
- **Cold lists over signals** — sourcing 5,000 companies with no signal is spray-and-pray; let signal sources fill the table.
- **Unbounded first run** — never run 4,000 rows before reviewing 20.
- **Vendor-hardcoding** — always resolve tools by category; the play must survive a provider switch.
