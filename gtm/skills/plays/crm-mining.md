# Play: mine the CRM for the ICP

**Use when** the workspace has CRM history. Won deals already know who buys — the ICP does not
need to be guessed in a workshop when it can be derived from what closed.

**Shape:** read won deals → find what they share → write it as Wissen → find more like them.

This is the play that runs *before* the others. An hour here is worth a week of copy work.

---

## 1 — What closed, and what it had in common

```bash
gtm call list_deals --input '{"status":"won"}' --json
gtm call get_icp_performance --json
gtm call get_funnel --json
```

Then look for the pattern across the won set:

| Dimension | Question |
|---|---|
| Industry | which two or three actually close — not which appear |
| Size | the employee window where the cycle is shortest |
| Region | where you win, versus where you merely sell |
| Trigger | what was happening when they bought |
| Persona | which title signed, and which title blocked |
| Cycle & value | which segment is worth the effort at all |

**Compare won against lost, not won against nothing.** "80 % of our customers are
manufacturers" means nothing if 80 % of everyone contacted was a manufacturer. The signal is
where the win *rate* differs, not where the count is highest.

## 2 — Let the platform do the analysis

```bash
gtm call analyze_icp --json                    # derive ICP characteristics from the data
gtm call find_similar_to_converted --json      # companies resembling those that converted
gtm call seed_blueprint_from_crm --json        # propose Wissen assets from CRM analytics
```

`seed_blueprint_from_crm` proposes assets into the approval queue rather than writing them
directly — read what it proposes before approving. A proposal derived from twelve deals is a
hypothesis, not a fact.

## 3 — Write the findings as Wissen, not as notes

The point of the analysis is that everything downstream can reference it:

```bash
gtm call wissen_asset_create --input '{
  "kind": "icp",
  "name": "ICP aus Gewinn-Analyse 2026",
  "content": { "industries": ["…"], "employee_range": "50-250",
               "regions": ["DACH"], "disqualifiers": ["B2C", "<20 MA"],
               "evidence": "abgeleitet aus N Gewonnen-Deals, Abschlussquote X% vs Y% Rest" }
}' --json
```

Record the **evidence** in the asset. Six months later, "why is the size window 50–250?" has an
answer, and the next revision is an argument with data rather than a matter of taste.

Then the personas, from who actually signed — including the blocker role, which is usually
missing from ICPs written in a workshop.

## 4 — The free lookalike source

Once the ICP exists, the cheapest sourcing there is:

```bash
gtm call workspace_table_add_source --input '{
  "table": "Accounts", "source": "lookalike", "max_results": 100
}' --json
```

Free, and it runs on **your own** data — companies resembling the ones that converted. Start
here before paying for Maps or a lead database.

## 5 — Objections and questions are copy material

Lost deals and won deals both carry the objections that came up and the questions that got
asked. Those are the highest-quality copy input available, because they are in the buyer's
words rather than yours:

- A recurring objection belongs in the sequence as a **pre-emption**, in step two.
- A recurring question means the offer asset is unclear — fix the asset, not the email.

**Record them from a fixed list.** Free-text objection reasons fragment into near-unique
strings and become uncountable — the exact failure that makes "what objection costs us most
deals?" unanswerable. Give the classifier an enum.

## 6 — Where it goes next

| Finding | Feeds |
|---|---|
| ICP + personas as Wissen | every qualification column via `{{asset.icp}}` |
| Winning triggers | the `signal` assets and the watches in `job-openings.md` |
| Objections | sequence step 2 in `sequences/copy-patterns.md` |
| Lookalikes | the `lookalike` source, free |
| Old lost deals | `lost-deal-reactivation.md` |

## The honest limit

Under roughly 20 closed deals, this is pattern-matching on noise. Say so rather than producing
a confident ICP from four data points — and fall back to the interview in
`gtm-quickstart/intake.md`, using whatever CRM history exists as one input among several.
