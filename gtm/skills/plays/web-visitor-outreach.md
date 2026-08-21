# Play: website visitor → outreach

**Use when** companies visit your site and do not fill in the form — which is almost all of
them. De-anonymisation turns that traffic into named accounts, and a visit is one of the
freshest signals available: they were thinking about the problem this morning.

**Shape:** de-anonymisation tool → webhook → qualify → email and LinkedIn, within 48 hours.

---

## 1 — The de-anonymisation tool is external

The platform does not de-anonymise traffic itself. You bring a visitor-identification tool that
does, and it POSTs to a webhook source:

```bash
gtm call create_webhook_source --input '{
  "name": "Website-Besucher",
  "target_playbook_id": "<id>",
  "field_mapping": {
    "name": "company.name",
    "domain": "company.domain",
    "industry": "company.industry",
    "employee_count": "company.employees"
  }
}' --json
```

Paste the returned URL and secret into the tool's webhook settings — directly, or through an
automation bridge if it has no native webhook.

> Signal watches also carry a `website_visitors` **detector**, which may or may not be
> available in a given workspace. Ask rather than assume: `create_signal_watch` rejects an
> unknown detector **with the list of available ones**, so the tool can never lie to you about
> what exists. Where it is unavailable, the webhook route above is the one that works.

## 2 — Keep what the visit means

Identity block first: `company_name`, `country`, `industry`, `website`, `size`.

Not every visit is a buying signal. What separates them:

| Column | Kind | Job |
|---|---|---|
| `pages_viewed` | from the payload | pricing page ≠ blog post |
| `visit_depth` | `formula` | one page = noise; four+ = research |
| `visited_at` | from the payload | the clock, and it runs fast |
| `intent_page` | `formula` | did they hit pricing, integrations, or a case study? |

**Pricing page plus three or more pages is the play.** A single blog visit from a shared IP is
not, and treating it as one produces the creepiest cold email in the genre.

## 3 — 48 hours, or not at all

Freshness matters more here than anywhere else. The signal is warm for 24–48 hours, stale after
a week, and useless after a month.

Gate the whole chain on `visited_at` within 48 hours, and schedule the workflow **hourly**
rather than daily — a daily loop turns a 6-hour-old signal into a 30-hour-old one.

## 4 — Find the person, since the visit is anonymous

You have a company, not a contact. Same chain as any account play, and the same order:

`agent:icp_fit` → gate → `base:find_leads` (target persona by title) → `agent:persona_fit` →
gate → `base:contact_enrichment` (25 credits — gated) → `base:email_validation`.

**Do not claim to know who visited.** You do not. The company visited; you are writing to the
person most likely to have been behind it.

## 5 — The copy problem, and the honest way through it

"I saw you visited our website" is the fastest way to be reported. It is also, in most
jurisdictions, a claim you should be careful making.

Reference the **topic**, not the visit:

> {{cell.salutation}}, das Thema {{cell.intent_topic}} kommt bei {{company.name}} gerade
> offenbar auf. {{cell.case_match}} stand vor derselben Frage. Das Ergebnis:
> {{cell.case_result}}. Ist das bei Ihnen ein Thema?

`intent_topic` is derived from the pages: pricing → cost and rollout; integrations → the stack;
a specific case study → that use case. The message is relevant because the topic is right, not
because you announced that you were watching.

## 6 — Two channels, offset

This is one of the few plays where a second channel earns its cost, because the window is short
and the same company may be reachable on one and not the other:

| Day | Action |
|---|---|
| 0 | LinkedIn connect, **no note** |
| 0 | Email step 1, referencing the topic |
| 2 | LinkedIn message if the connect was accepted |
| 4 | Email step 2, new proof |

Both channels stop on a reply on either. And each needs its own copy — a forwarded email is not
a LinkedIn message.

## 7 — Data protection

Visitor de-anonymisation is legally sensitive, and more so for individual-level tools than
company-level ones. You need a legal basis, transparent information about the processing, and
a working objection path. The provenance of the data must be documented — the platform's gates
enforce the suppression side, not your legal basis. Check your case with your own counsel;
neither this file nor the platform is legal advice.
