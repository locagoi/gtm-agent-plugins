# Play: inbound lead qualification

**Use when** something outside the platform produces leads — a website form, a chatbot, a
partner feed, an event list, a spreadsheet another team maintains. Inbound is warmer than anything you source, and it
is routinely wasted by arriving unqualified in an inbox nobody reads within the hour.

**Shape:** webhook → qualified in seconds → routed by what it is → the rep gets a card, or the
sequence starts.

---

## 1 — The ingest URL

```bash
gtm call create_webhook_source --input '{
  "name": "Website-Formular",
  "target_playbook_id": "<id>",
  "field_mapping": {
    "name": "company.name",
    "domain": "company.website",
    "industry": "company.industry",
    "employee_count": "company.size"
  }
}' --json
```

Returns the ingest URL and a secret to paste into the external tool. Each POST is mapped to a
company and enters the playbook as `pending`.

`field_mapping` values are **dot-paths into the POST body**, so send one real payload first and
map against what actually arrives. At least `name` or `domain` must be mappable. Supported
fields: `name`, `domain`, `industry`, `country`, `city`, `linkedin_url`, `phone`,
`employee_count`.

**The alternative target** is a workflow: `target_chain_id` instead of `target_playbook_id`
fires a workflow per POST, with the whole body available as `{{webhook.<field>}}`. Use that
when the payload is not company-shaped — an event registration, a support ticket, a partner
referral.

Exactly one of the two targets. Not both.

## 2 — Qualify in seconds, not overnight

Inbound decays fast: someone who filled a form ten minutes ago is a different prospect from
the same person tomorrow. Keep the qualification chain **short and cheap**:

| Column | Kind | Job |
|---|---|---|
| `icp_fit` | `enrichment` | `agent:icp_fit` — score, tier, reasoning |
| `intent_level` | `ai` | from what they submitted: `demo` · `pricing` · `content` · `support` — a **fixed enum** |
| `is_competitor` | `formula` | domain against your own blacklist and competitor list |
| `route` | `formula` | the decision, derived from the three above |

`base:contact_enrichment` is usually unnecessary here — inbound already gave you the address.
Skip 25 credits a row.

## 3 — Route by what it is

| Situation | Route |
|---|---|
| ICP fit + demo/pricing intent | **Feed card, immediately** — a human calls today |
| ICP fit + content intent | nurture sequence |
| No fit | polite auto-reply, no sequence |
| Competitor or existing customer | drop, and log why |

The Feed card is the point of the fast path:

```bash
gtm call create_feed_action --input '{
  "lead_id": "<id>", "type": "call_now", "priority": 9,
  "reasoning": "Demo-Anfrage über das Formular, ICP-Fit 82, vor 6 Minuten eingegangen"
}' --json
```

A qualified inbound lead should be a card with a reason on it, not a row someone finds on
Thursday.

## 4 — Existing customers and open deals

The one mistake that costs more than a missed lead: writing outbound copy to a company sales is
already closing. Check before routing:

```bash
gtm call list_deals --json         # is there an open deal on this domain?
gtm call list_blacklist --json     # is the domain suppressed?
```

Wire it as a `formula` gate, not as a habit. See **`crm-blacklist-sync.md`** for keeping that
reconciliation standing rather than manual.

## 5 — Test it before you trust it

```bash
curl -X POST '<ingest url>' -H 'Content-Type: application/json' \
  -d '{"company":{"name":"Test GmbH","website":"test-gmbh.de","size":42}}'
gtm call workspace_table_get --input '{"table":"Inbound","limit":5}' --json
```

If the row arrives with an empty name, the mapping is wrong, not the webhook. The most common
cause is a payload nested one level deeper than assumed.
