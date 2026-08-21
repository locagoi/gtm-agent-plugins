# Play: lost deal reactivation

**Use when** the CRM has a graveyard. Every closed-lost deal is a company that had the problem,
evaluated a solution, and had a *reason* not to buy. Reasons expire. Nobody else on the market
knows these accounts as well as you do, and reactivation is the cheapest pipeline available —
there is no sourcing cost at all.

**Shape:** read lost deals → filter by why and when → find out what changed → a message that
names the old reason.

---

## 1 — Read the graveyard

```bash
gtm call list_deals --input '{"status":"lost"}' --json
gtm call list_deal_pipelines --json
```

Pipelines are configurable, so **never infer meaning from a stage key**. Read the pipeline
definition and use what the stage says it means; a stage called `closed_lost` in one workspace
is `verloren` in the next, and neither key is a contract.

## 2 — Filter, hard

Most lost deals should stay lost. Three filters:

| Filter | Keep | Why |
|---|---|---|
| **Age** | 6–24 months | under 6 the reason still holds; over 24 nobody remembers you |
| **Loss reason** | timing, budget, priority, no decision | these expire |
| **Loss reason** | *not* product gap, *not* bad fit, *not* competitor won | these do not, unless something changed |
| **Contact** | still employed | the champion is often gone — and that can be the opening |

"No decision" is the best segment in the list. They did not choose someone else; they ran out
of momentum.

## 3 — Find what changed

There has to be a reason to write **now**, or this is just a cold email with an awkward
history. Two columns:

```bash
gtm call workspace_table_add_column --input '{
  "table": "Reactivation", "key": "whats_new", "kind": "enrichment",
  "config": { "category": "company_research", "module": "agent:buying_signals" }
}' --json
```

`agent:buying_signals` returns `signals[]`, `signal_strength` and a `summary`. Then:

| Column | Kind | Job |
|---|---|---|
| `contact_changed` | `enrichment` | is the old contact still there? Is there a new decision maker? |
| `reason_expired` | `ai` | given the old loss reason and what is new: has the blocker plausibly gone? `yes` · `no` · `unclear` |

Gate on `reason_expired != 'no'`. If nothing changed, do not write.

**A new decision maker is the strongest reactivation trigger there is.** The person who said no
has left; the successor has no attachment to that decision and often an interest in revisiting
it.

## 4 — The message names the reason

Reactivation copy is different from cold copy in one specific way: pretending there is no
history is the mistake. They remember. Name it, briefly, then move on.

> {{cell.salutation}}, wir hatten {{cell.deal_age}} über {{cell.original_topic}} gesprochen.
> Damals war {{cell.loss_reason}} der Grund, es nicht zu machen. Seitdem
> {{cell.whats_new_short}}. Falls sich die Lage geändert hat, melde ich mich gern nochmal.
> Sonst lasse ich Sie in Ruhe.

Four properties that make it work: short, honest about the history, one line on what changed,
and an explicit exit. No "just checking in", no pretending the last conversation did not
happen, no pressure.

**If the contact changed**, write to the successor and reference the company's history, not the
person's: "Ihr Vorgänger und wir hatten … besprochen."

## 5 — Two touches, then stop

| Day | Step |
|---|---|
| 1 | the reactivation message |
| 8 | one follow-up with a new piece of proof — ideally a case from a company that *did* solve the old blocker |

Then stop. These are people who already said no once; a five-touch sequence turns a warm
relationship into a complaint.

## 6 — The gates still apply

Everything in the graveyard runs through the same checks: unsubscribe, blacklist, an open deal
on the domain. A lost deal that has since been reopened by sales must **not** get outbound —
check `list_deals` for an open deal on the same company before enrolling, and see
**`crm-blacklist-sync.md`** for making that standing rather than manual.

## Why it is worth doing first

No sourcing cost, no enrichment cost worth mentioning, contact data you already have, and a
list that is by definition ICP-fit — they got far enough to become a deal. If a workspace has
a CRM with history, this is the highest-return play in the folder and it is usually the last
one anybody builds.
