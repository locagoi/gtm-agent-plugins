# Play: job openings as the buying signal

**Use when** hiring reveals the need: a company posting for SDRs is investing in go-to-market,
one posting for a data engineer has a data problem, one posting five roles at once has a
scaling problem. The clearest public signal there is, and it comes with a date.

Two routes, and they answer different questions:

| Route | Question | Mechanism |
|---|---|---|
| **Discover** | who is hiring for this role anywhere? | `indeed_jobs` source — pulls new companies in |
| **Watch** | which of *my* target accounts started hiring? | signal watch on their career pages |

Run both: discovery fills the funnel, the watch guards the accounts you already care about.

---

## Route A — Discovery via Indeed

```bash
gtm call workspace_table_add_source --input '{
  "table": "Hiring", "source": "indeed_jobs",
  "query": "Sales Development Representative", "location": "Deutschland",
  "max_results": 100, "max_credits": 30
}' --json
```

Paid, so `max_credits` is required. The job title *is* the ICP filter — "SDR" finds companies
building outbound; "Vertriebsleiter" finds companies replacing leadership. Different plays,
different copy.

Keep from the posting itself:

| Column | Kind | Job |
|---|---|---|
| `job_title` · `posted_at` | from the source | the signal and its clock |
| `fresh` | `formula` | ≤ 7 days `hot`, ≤ 28 `warm`, else `cold` |
| `role_count` | `formula` | several open roles → scaling, a different pitch |
| `job_excerpt` | `ai` | the sentence naming the responsibility, ≤ 25 words, verbatim |

`job_excerpt` is the opener. "In Ihrer Ausschreibung steht, dass die Person ‚den Outbound-Kanal
von Grund auf aufbauen' soll" is specific in a way no summary is.

Then the normal chain: `agent:icp_fit` → gate → `base:find_leads` (the hiring manager, not the
posted role) → `agent:persona_fit` → gate → contact enrichment → validation → copy → enroll.

**Write to the hiring manager, never to the vacancy.** The person posting the SDR role is the
one who owns the problem.

## Route B — Watch your own target list

A signal watch re-reads the career pages of companies already in a table and reports what is
**new**:

```bash
gtm call create_signal_watch --input '{
  "label": "Stellen DACH-Zielkunden",
  "target_table_id": "<Accounts table id>",
  "signal_name": "job_posting_open",
  "detector": "page_diff",
  "url_field": "karriere_url",
  "match": ["Sales Development", "Vertriebsmitarbeiter", "Business Development"],
  "cadence": "daily"
}' --json
```

Four things to know, all of which trip people up:

1. **It never creates rows.** It watches companies that are already there. To pull companies
   in, use a source.
2. **It writes onto the matched row.** On the first hit it auto-creates `signal`,
   `signal_grund` (the new block — the actual reason) and `signal_am`. `{{cell.signal_grund}}`
   is then readable in a copy column, which means the opener can quote the exact new text.
3. **The first run only learns.** It has nothing to diff against. Changes are reported from the
   second run on — do not conclude it is broken.
4. **`signal_name` is yours to define.** Name what was *measured* (`job_posting_open`), never
   what you hope it means (`ready_to_buy`).

You need a `karriere_url` column first — `base:web_research` can fill it.

## The event, and what listens to it

A hit fires `company_signal_detected` with `{ signal, company_id, domain, evidence }`. Pair the
watch with a workflow, or the signal sits in the grid and nobody acts:

```bash
gtm call create_workflow --input '{
  "name": "Stellenanzeige → Outreach",
  "trigger_type": "event",
  "config": { "event_name": "company_signal_detected", "filters": { "signal": "job_posting_open" } }
}' --json
```

Steps: qualify → find the hiring manager → enroll. **The filter is mandatory** — without it the
workflow fires on every signal type in the workspace.

## Cadence

`daily` for a list you are actively working; `thrice_daily` only when the signal is genuinely
time-critical and the list is small. Every look costs, and a career page rarely changes twice
a day.

## The copy

The signal goes in line one and nowhere else:

> Sie suchen aktuell {{cell.job_title}} — {{cell.job_excerpt}}. Genau dabei unterstützen wir
> {{cell.case_match}}: {{cell.case_result}}. Spielt das bei Ihnen gerade eine Rolle?

What kills this play: writing four weeks after the posting went up. Gate on `fresh`, and let
the cold ones go.
