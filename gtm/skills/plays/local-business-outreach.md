# Play: local business outreach

**Use when** the target is small, local, owner-led businesses in a defined region — trades,
installers, practices, agencies, retail. The play everyone starts with, and the one where the
cost gate matters most.

**Shape:** Maps → qualify company → find the decision maker → qualify them → find and validate
the email → write the copy → enroll.

**Why the order:** contact enrichment costs 25 credits a row against 1 for qualification.
Sourcing 2,000 Maps entries and enriching them all costs 50,000 credits; qualifying first and
enriching the ~400 that survive costs about 12,000. Same campaign, a quarter of the bill.

---

## 1 — Accounts table, filled from Maps

```bash
gtm call workspace_table_create --input '{
  "name": "Accounts", "entity_binding": "company",
  "description": "Local businesses, Maps-sourced"
}' --json

gtm call workspace_table_add_source --input '{
  "table": "Accounts", "source": "scraping",
  "query": "Dachdecker", "location": "Kassel",
  "max_results": 50, "max_credits": 15
}' --json
```

**Region small, trade narrow.** "Dachdecker, Kassel + 30 km" beats "Handwerk, Hessen" — and
narrow ICPs reply at roughly twice the rate. If the query needs a comma, it is two runs.

**Show the identity block first.** For a Maps-sourced table that is `company_name`, `country`,
`industry` and `website`; `size` is rarely present in Maps data, so leave it out rather than
showing an empty column. Add `city` here, because the whole play is local.

Watch it land, then read the rows:

```bash
gtm call list_runs --json
gtm call workspace_table_get --input '{"table":"Accounts","limit":20}' --json
```

## 2 — Qualify, cheaply

```bash
gtm call workspace_table_add_column --input '{
  "table": "Accounts", "key": "icp_fit", "name": "ICP-Fit",
  "data_type": "json", "kind": "enrichment",
  "config": {
    "category": "company_research",
    "args_template": {
      "name": "{{company.name}}", "domain": "{{company.domain}}",
      "instructions": "Bewerte anhand aktueller Web-Recherche, wie gut dieser Betrieb zum ICP passt. Gib fit_score (0-100), tier (A/B/C) und eine kurze Begründung zurück."
    },
    "output_schema": {
      "type": "object",
      "properties": { "fit_score": { "type": "number" }, "tier": { "type": "string" },
                      "reasoning": { "type": "string" } },
      "required": ["fit_score", "tier", "reasoning"]
    }
  }
}' --json
```

That is the `agent:icp_fit` preset, copied in — read it from `workspace_capabilities` rather
than retyping it, and keep `output_schema`: it is what makes `fit_score` a number you can gate
on. Pin the ICP asset to the playbook first or the research runs without your criteria.

Then, and only then, the play-specific columns. The Maps entry itself carries signal worth
keeping:

| Column | Kind | Reads | Says |
|---|---|---|---|
| `review_count` | `formula` | the Maps payload | few or old reviews → visibility problem |
| `has_website` | `formula` | the Maps payload | no site → digitalisation gap, and a hook |
| `owner_led` | `ai` | name + payload | owner-led → the mobile number is the decision maker's |

Those three cost nothing and they are the opener material. A first line built on "Sie haben
seit 2023 keine neue Bewertung" is specific in a way no LLM paraphrase of the company
description will be.

## 3 — The gate

```bash
gtm call workspace_table_update_column --input '{
  "table": "Accounts", "column": "find_contacts",
  "run_condition": { "column": "icp_fit.fit_score", "op": "gte", "value": 60 }
}' --json
```

Verify the gate **before** spending, with a free dry run — it reports exactly how many rows the
condition stops:

```bash
gtm call workspace_table_run_column --input '{"table":"Accounts","column_key":"owner","mode":"dry_run"}' --json
# → { rows: 12, rows_in_scope: 40, rows_skipped_by_condition: 28, estimated_credits: 12 }
```

Everything downstream carries this condition. This is the line that decides the bill.

## 4 — Find the decision maker

For local businesses the owner is rarely on LinkedIn but almost always in the imprint:

```bash
gtm call workspace_table_add_column --input '{
  "table": "Accounts", "key": "owner", "name": "Inhaber",
  "data_type": "json", "kind": "enrichment",
  "config": {
    "category": "research_people",
    "args_template": { "name": "{{company.name}}", "domain": "{{company.domain}}" }
  },
  "run_condition": { "column": "icp_fit.fit_score", "op": "gte", "value": 60 }
}' --json
```

`research_people` walks imprint → commercial register → LinkedIn — a real person search, not an
LLM guessing a name. 1 credit. For B2B targets that *are* on LinkedIn, use category
`find_leads` instead (job titles + locations as column-level lists, not per-row templates).

Then hand each found person to a contacts table as a linked lead:

```bash
gtm call workspace_table_add_column --input '{
  "table": "Accounts", "key": "create_contact", "name": "Kontakt anlegen",
  "data_type": "json", "kind": "enrichment",
  "config": {
    "category": "create_lead",
    "args_template": {},
    "target_table_id": "<Contacts table id>",
    "relation_column": "account",
    "owner_source_column": "owner"
  },
  "run_condition": { "column": "icp_fit.fit_score", "op": "gte", "value": 60 }
}' --json
```

`create_lead` costs 0 and starts the cascade in the target table. All three of
`target_table_id`, `relation_column` and `owner_source_column` are required: the target table,
the relation column on *that* table pointing back here, and the column whose value names the
person. Create the relation column on Contacts first, or this call has nothing to point at.
The owner data it reads wants **flat** `first_name` / `last_name` fields — a single `name`
string will not parse.

## 5 — Contacts: qualify, then enrich

In the Contacts table, in this order and not the other:

```bash
# 1. persona check — an ai column, 1 credit, references {{asset.persona}}
gtm call workspace_table_add_column --input '{
  "table": "Contacts", "key": "persona_fit", "name": "Persona-Fit",
  "data_type": "json", "kind": "ai",
  "config": {
    "prompt": "Prüfe, ob dieser Kontakt zur Ziel-Persona passt.\n\nKontakt: {{lead.first_name}} {{lead.last_name}} — Position: {{lead.title}}\nUnternehmen: {{company.name}}\nZiel-Persona: {{asset.persona}}\n\nAntworte als JSON mit matches_persona (boolean), confidence (0-1) und reasoning.",
    "output_schema": {
      "type": "object",
      "properties": { "matches_persona": { "type": "boolean" },
                      "confidence": { "type": "number" }, "reasoning": { "type": "string" } },
      "required": ["matches_persona", "confidence"]
    }
  }
}' --json

# 2. ONLY THEN the expensive column, gated
gtm call workspace_table_add_column --input '{
  "table": "Contacts", "key": "contact_data", "name": "Kontaktdaten",
  "data_type": "json", "kind": "enrichment",
  "config": { "category": "contact_enrichment", "args_template": {} },
  "run_condition": { "column": "persona_fit.matches_persona", "op": "equals", "value": true }
}' --json

# 3. validate before you ever send
gtm call workspace_table_add_column --input '{
  "table": "Contacts", "key": "email_valid", "name": "E-Mail geprüft",
  "data_type": "text", "kind": "enrichment",
  "config": { "category": "email_validation", "args_template": {} },
  "run_condition": { "column": "contact_data.email", "op": "is_not_empty" }
}' --json
```

Validation is not optional: validated versus unvalidated lists bounce at 0.4 % against 7.7 %
on identical infrastructure, and a domain is spent at 8 %.

Then a `resolve_contact` column writes the final sending address onto the lead: the personal
address from `personal_email_column` first, optionally a company fallback via
`company_email_fallback` + `company_email_prefix` (`info`). For local businesses that fallback is often
the only address there is; decide deliberately whether `info@` is worth writing to.

## 6 — Copy fills, not messages

Four small typed columns, each gated on `email_valid == 'valid'`:

| Column | Returns |
|---|---|
| `salutation` | the complete greeting, gendered: `Sehr geehrter Herr Müller` |
| `hook` | one sentence from the local signal, ≤ 140 chars, no question |
| `pain_point` | 3–4 words, from trade and size |
| `case_match` | one name **from a fixed enum** of your case studies |
| `quick_win` | what changes for them, in six words |

The sequence template is fixed; only these fills vary. That is what keeps 400 messages
readable and debuggable: when the copy is weak you can see *which column* produced the weak
fill.

Gate the enroll column on `salutation.confidence >= 0.8`. A row whose gender could not be
determined is held back rather than greeted with a guess. The prompt for that column is in
`sequences/copy-patterns.md`.

## 7 — Sequence and enrollment

```bash
gtm call create_sequence --input '{
  "playbook_id": "<id>", "channel": "email", "name": "Local — 3 step",
  "steps": [
    { "step_number": 1, "subject": "…", "body": "…", "delay_days": 0 },
    { "step_number": 2, "body": "…", "delay_days": 4 },
    { "step_number": 3, "body": "…", "delay_days": 9 }
  ]
}' --json
```

Then the terminal enroll column, last, gated on `email_valid == 'valid'`, `auto_run` off.
See **sequences** for the step structure and `copy-patterns.md` for what goes in each step.

**If the business has a mobile number**, WhatsApp usually beats email for this audience — the
number in a Maps entry for an owner-led business is normally the owner's. Route on it: mobile
prefix present → WhatsApp sequence, otherwise email. WhatsApp rules are stricter (2–3
sentences, under 300 characters, no link in message one, explicit opt-out, one follow-up
maximum) and both the platform rules and data protection apply.

## 8 — First run

```bash
gtm call workspace_table_preflight --input '{"table":"Accounts","expect":["fills_itself","enrolls_leads"]}' --json
```

Free and deterministic: it tells you whether a new row runs through the chain at all before you
spend anything on rows. Then 25 rows sourced → read the fit reasons → a fit rate below 60 %
means the query or the ICP is wrong, not the volume. Then 20 generated messages, read by a
human. Then enroll, capped.

Run the preflight again before scheduling the source.

```bash
gtm call workspace_table_save_as_template --input '{"table":"Accounts","name":"Local outreach — accounts"}' --json
```

The next region is then a new source run against the same template.

## Cost sketch

| Stage | Rows | Credits/row | Total |
|---|---|---|---|
| Maps source | 500 | ~0.3 | ~150 |
| `icp_fit` (company_research) | 500 | 1 | 500 |
| `research_people` (gated, ~40 %) | 200 | 1 | 200 |
| `contact_enrichment` (gated, ~60 % of those) | 120 | **up to 25** | **≤ 3,000** |
| validation | 120 | 1 | 120 |
| copy fills | 120 | ~1 | ~120 |

~4,100 credits worst case for ~120 contactable, qualified, validated leads — less in
practice, because enrichment bills only what it finds (10 for an email, 15 for a phone), but
budget the worst case or the cap stops the run half way. Ungated, the same 500 rows
through contact enrichment alone would be 12,500 — for a list that is 60 % wrong.
