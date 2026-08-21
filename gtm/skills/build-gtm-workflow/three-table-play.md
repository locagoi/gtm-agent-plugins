# The three-table play

The canonical shape of a working campaign: **accounts → people → outreach**, with a scored
gate between each stage so you only pay to enrich what qualified, and only write copy for
who survived.

It is three tables rather than one because the grain changes. An account row is a company; a
contact row is a person; you find several people per qualified company. Forcing that into
one table means either duplicating company research per contact (expensive) or losing the
person grain (useless).

```
Table 1  Accounts          entity_binding: company
  source → icp_fit → signal → clean_name → value_prop        gate: icp_fit AND signal
                                    │
                                    ▼  create_lead column, target_table_id → Contacts
Table 2  Contacts          entity_binding: lead
  find_people → still_employed → persona → profile → hook    gate: persona relevant
                                    │
                                    ▼  relation or create_lead column
Table 3  Outreach          entity_binding: lead
  email_find → validate → copy_fills → ENROLL (terminal)
```

Table 3 can be folded into Table 2 for a small play. Keep it separate when several sequences
run off one contact pool, or when email discovery and validation have their own cost profile
you want to gate independently.

---

## Table 1 — Accounts

One row per company. This is where the money is saved: every company you disqualify here is
a contact you never enrich.

| # | Column | Kind | Job | Output |
|---|---|---|---|---|
| 1 | *(source)* | `source` | fill rows from a connected source | entity-bound rows |
| 2 | `company_profile` | `enrichment` | summarise industry, size, location, products in 3–5 sentences | short profile |
| 3 | `icp_fit` | `ai` | check against `{{asset.icp}}` — industry, size, region, stack | `{ fit: true\|false, reason }` |
| 4 | `signal` | `enrichment` | search news, postings, LinkedIn for a current trigger | `{ signal_type, evidence, observed_at }` |
| 5 | `signal_fresh` | `formula` | `observed_at` within 7 / 28 days | `hot` \| `warm` \| `cold` |
| 6 | `clean_name` | `formula` or `ai` | "Müller GmbH & Co. KG" → "Müller" | the name you address |
| 7 | `competitor` | `enrichment` | who they compare to | one name |
| 8 | `value_prop` | `ai` | which of your offers fits, and why | one of a **fixed list** |
| 9 | `create_contacts` | `tool` | hand qualified accounts to Table 2 | rows in Contacts |

**The gates:**

- `run_condition` on 4–8: `icp_fit.fit == true`. Nothing else runs on a company that failed.
- `run_condition` on 9: `icp_fit.fit == true AND signal_fresh != 'cold'`.

**`icp_fit` returns a reason, always.** A boolean alone is unauditable — when the fit rate
comes out at 30 % you need to read twenty reasons to know whether the ICP is wrong or the
source is. Its `output_schema`:

```json
{ "type": "object",
  "properties": {
    "fit": { "type": "boolean" },
    "reason": { "type": "string", "maxLength": 200 },
    "disqualifier": { "type": "string", "enum": ["size","industry","region","b2c","none"] }
  },
  "required": ["fit", "reason", "disqualifier"] }
```

The `enum` on `disqualifier` is the point. Free-text disqualification reasons aggregate into
nothing — on the platform, recorded objection texts are almost all unique, which makes them
unusable for exactly the question you want to ask: *what is disqualifying most of my list?*

**Health check:** ICP fit rate **≥ 60 %**. Below that, the ICP is too vague or the source
query is too broad — fix the input, do not widen the gate.

---

## Table 2 — Contacts

One row per person at a qualified company. Several rows per Table 1 row.

| # | Column | Kind | Job | Output |
|---|---|---|---|---|
| 1 | `find_people` | `source` / `tool` | people at the company, filtered by title | rows, lead-bound |
| 2 | `still_employed` | `enrichment` | are they actually still there? | `true` \| `false` |
| 3 | `persona` | `ai` | classify against your persona assets | one of a **fixed list** |
| 4 | `influence` | `ai` | decision authority | `high` \| `medium` \| `low` |
| 5 | `recent_activity` | `enrichment` | last 2–3 posts or mentions | short summary |
| 6 | `hook` | `ai` | one-sentence icebreaker from role, post or project | ≤ 140 chars, no question |
| 7 | `salutation` | `formula` | correct formal address from name and gender | `Herr Müller` |

**`still_employed` earns its cost.** Job-change rates in B2B mean a list bought or scraped
three months ago has a meaningful share of people who left. Writing to them wastes the send
*and* burns the account.

**`persona` must choose from a closed list** — the persona names from your Wissen assets.
Free text here produces "Head of Sales", "Sales Lead", "VP Sales" and "Vertriebsleiter" as
four different personas, and every per-persona comparison afterwards is noise.

**Gate:** `run_condition` on 5–7: `still_employed == true AND influence != 'low'`.

---

## Table 3 — Outreach

One row per contact you will actually write to.

| # | Column | Kind | Job |
|---|---|---|---|
| 1 | `email_find` | `enrichment` | find the address |
| 2 | `email_valid` | `enrichment` | validate it |
| 3 | `pain_point` | `ai` | likely challenge from size, industry, persona — 3–4 words |
| 4 | `case_match` | `ai` | pick the case study, from a **fixed list** |
| 5 | `case_result` | `formula` | the number belonging to that case |
| 6 | `quick_win` | `ai` | what changes for them, in six words |
| 7 | `enroll` | `tool` | **terminal** — hands the lead to the sequence |

**Validation before enrollment is not optional.** Validated versus unvalidated lists measured
on the same infrastructure: **0.4 % versus 7.7 % bounce**, a factor of 19. Domain damage
starts around 5 % and a domain is effectively spent at 8 %.

**Gate on 7:** `email_valid == 'valid'`. And the enroll column is last, sends only in its own
run, and `auto_run` is rejected for it.

---

## Quality gates

Score, then act on the score. The thresholds matter less than having them written down:

| Score | Meaning | Action |
|---|---|---|
| 80–100 | strong fit, fresh signal | enroll first, best sender |
| 60–79 | good fit | standard sequence |
| 40–59 | weak fit | LinkedIn-only, or nurture |
| < 40 | no fit | do not contact |

Build the score as a `formula` column over the typed outputs above rather than asking a model
for a number. A model asked "score this 0–100" returns a plausible number with no mechanism
behind it; a formula over `icp_fit`, `signal_fresh`, `influence` and `email_valid` is
inspectable, reproducible, and adjustable when you learn which input actually predicted
replies.

## Expected volumes

Order-of-magnitude, for planning a month:

| Stage | Typical |
|---|---|
| Companies sourced | 2,000 |
| Qualified companies (~40 %) | 800 |
| People found (~4 per company) | 3,200 |
| Qualified contacts (~25 %) | 800 |
| Final outreach list, after dedup and blacklist | ~500 |

At 15 cold mails per inbox per day, 500 contacts over a 2.5-step average is roughly 1,250
sends — about four inboxes across a month. Work that backwards from your meeting target with
the capacity formula in `outbound-playbook/benchmarks.md` before buying infrastructure.

## Build order

1. Table 1 with the source and `icp_fit` only. Run **20 rows**, read the reasons.
2. Fit rate below 60 %? Fix the ICP or the source query. Do not proceed.
3. Add the remaining Table 1 columns, gated. Run 20 again.
4. Table 2, gated on Table 1's verdict. Run for **5 accounts** and read the people.
5. Table 3, ending at `copy_fills`. Read **20 generated messages** with a human.
6. Only then the enroll column, capped.
7. `workspace_table_save_as_template` on each — the next campaign is an hour of work.

Every step of that order exists because skipping it is expensive: an unbounded first run is
the most costly mistake available in the product, and a copy column running on 4,000
unqualified rows is how a credit budget disappears in an afternoon.
