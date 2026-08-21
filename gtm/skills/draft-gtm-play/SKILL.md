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

> **Where this sits:** `gtm-quickstart` is the build order for a whole workspace and calls
> this skill at stage 2. `outbound-playbook` carries the go-to-market decisions and the
> numbers behind them — read it first if you are choosing an ICP or a channel. Table
> mechanics: `build-gtm-workflow`. Touch plans: `sequences`. Operating basics: `gtm-operate`.

**Never invent the substance.** Interview the human for anything missing —
`gtm-quickstart/intake.md` is the question list. A play built on guessed positioning produces
copy that is specific, confident and wrong, at volume. That is worse than generic.

## Phase 1 — Draft the knowledge (Wissen assets)

Interview the user if the substance is missing — never invent positioning. Create with `wissen_asset_create`, revise with `wissen_asset_revise` (immutable versions).

Draft in this order (each builds on the previous):

1. **ICP** (`icp`) — firmographics + the qualifying/disqualifying criteria. Concrete beats broad: "German Mittelstand manufacturers, 50–500 employees, complex B2B master data" outperforms "companies that need CRM".
2. **Persona** (`persona`) — the decision-maker: role, pains, what they're measured on.
3. **Offer** (`offer`) — what you sell them and the promise, in their language.
4. **Proof** (`proof`) — case studies with a named customer, a number carrying a unit, and a
   timeframe. One strong proof per persona beats five vague ones. **This asset is the only
   source of numbers in outbound copy.** A model asked to "make it concrete" invents a
   plausible percentage, and an invented number is the one thing a prospect can check.
5. **Messaging angle** (`messaging_angle`) — the hook that connects pain → offer.
6. **Signals** (`signal`) — the buying signals that make an ICP company *hot now* (hiring for a role, a new decision-maker, job postings, engagement). A signal asset **references the ICP and Offer assets it matters for** (`icp_refs`, `offer_refs`) and can map to a runtime detection (`signal_type_key`) so the platform's signal sources feed it. Plays that lead with a signal ("you're hiring 5 SDRs") convert multiples of plays that lead with an intro.

**The quality bars** (the same ones a two-to-four week manual playbook engagement uses):

| Level | Minimum |
|---|---|
| Per workspace | 1+ offer · **1–3 ICPs** — more than three is an absence of strategy |
| Per ICP | 1–3 case studies · **3–5 buying signals** · 8–15 qualification questions · **2–4 personas** |
| Per persona | 4–6 challenges · 4–6 benefits · 1–2 value props · 1 sequence |

Formats that survive contact with a reader:
- Pain point: `[process] [negative verb] [consequence]` — "Manual research cycles slow down
  response times"
- Benefit: `[verb] [metric] by [amount]` — "Reduce research time by 60–70 %"
- Offer name: `[benefit] for [ICP]`

**Bad-fit criteria are not optional.** An ICP that only says who qualifies cannot disqualify,
and the qualification column will pass almost everything. Name the disqualifiers — B2C,
below/above the size window, wrong region — as explicit checks.

**Fix the vocabulary now.** Industry labels, persona names, signal types: one spelling each,
reused everywhere. On the platform the same industry appears as four different strings, which
silently splits every per-industry comparison into four. This costs one decision here and is
unrecoverable later.

Quality gate before moving on: could a stranger read these six assets and pitch the company?
If not, revise.

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
- Every cold message is trying to earn the **five relevance proofs**: *show me you know me ·
  know my business · know my challenges · solved this for someone like me · give me value
  first.* Three of five earns a reply. The per-step patterns are in
  `sequences/copy-patterns.md`.
- Source columns implement the signal strategy: schedule the sources that detect your signal assets (job changes, job postings, post engagers) so the table refills itself with *hot* companies, not cold lists.
- Link the table to the playbook (`playbook_table_link`) so the play is one navigable bundle.
- Enrollment terminal columns carry the campaign target + field mapping; every enrollment passes the contactability gates.

Save the built table as a template (`workspace_table_save_as_template`) — the play becomes replicable across playbooks and workspaces.

## Phase 4 — Run, measure, revise

- Run bounded first: 20 rows, and a **human reads** the qualification verdicts and the
  generated first lines BEFORE anything is enrolled. Paid runs always carry a credit cap.
- Watch the **ICP fit rate** of sourced companies: below ~60 % the ICP is too vague — fix the
  asset, do not widen the gate.
- Measure where it matters: replies land in the feed; **signal → positive-reply attribution** shows which signal converts; meetings land as conversion outcomes.
- Feed it back: a losing angle → revise the messaging asset (new version, history kept). A signal that converts → weight it. The play gets smarter because the strategy is versioned knowledge, not chat history.

## Anti-patterns (each has burned real campaigns)

- **Table first, strategy never** — columns with hand-typed prompts that drift apart. Reference assets.
- **1:1 free-form copy at scale** — unpredictable output; use template + variable fills.
- **Cold lists over signals** — sourcing 5,000 companies with no signal is spray-and-pray; let signal sources fill the table.
- **Unbounded first run** — never run 4,000 rows before reviewing 20.
- **A second channel without its own copy** — playbooks running two channels reply at less
  than half the rate of those running one properly.
- **Scaling a weak campaign instead of rebuilding it** — the largest measured improvements on
  the platform come from rebuilding the message on the *same* audience: several times the
  reply rate at lower volume.
- **Vendor-hardcoding** — always resolve tools by category; the play must survive a provider switch.
