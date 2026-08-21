# Play: CRM ↔ blacklist reconciliation

**Use when** outbound and sales share a market — which is always. This is the play that stops
the single most expensive mistake in the product: cold outreach to a company your colleague is
closing.

It produces no pipeline. It protects all of it.

---

## What must never be written to

| Category | Where it lives | Why |
|---|---|---|
| Open deals | CRM | your colleague is mid-negotiation |
| Existing customers | CRM | outbound to a customer reads as incompetence |
| Recently lost | CRM | too soon — see `lost-deal-reactivation.md` for the timing |
| Explicit opt-outs | platform blacklist | legally binding, non-negotiable |
| Partners, suppliers, competitors | usually nowhere | the list nobody maintains |

Only the fourth is enforced automatically. The other four are your job, and they change daily.

## 1 — What the blacklist accepts

```bash
gtm call add_blacklist --input '{"entries":[
  {"type":"domain","value":"kunde-gmbh.de","reason":"Bestandskunde"},
  {"type":"domain","value":"wettbewerb.de","reason":"Wettbewerber"},
  {"type":"email","value":"person@firma.de","reason":"Opt-out 2026-08-14"}
]}' --json
```

Five types: `domain` · `email` · `company` · `phone` · `linkedin_url`. Batch adds are supported.

**There is no name-based block.** To suppress a *person* you need an identity — email, phone or
LinkedIn URL. "Block Herr Müller" is not expressible, and assuming it worked is how a
suppression silently fails.

**Prefer `domain` for company-level suppression.** An email block stops one address; the
colleague you have not met at the same company is still reachable.

## 2 — The reconciliation workflow

Standing, daily, before the day's sends:

```bash
gtm call create_workflow --input '{
  "name": "CRM → Blacklist Abgleich",
  "trigger_type": "schedule",
  "config": { "cron": "0 5 * * *" }
}' --json
```

Steps:

1. **`tool_call`** — read the CRM: open deals, customers, and anything closed in the last N
   months. Resolve by CRM **category**, never by vendor name; the connected adapter can change.
2. **`agent` step** — diff against `list_blacklist`. Judgment belongs here: a domain that
   appears as both a customer and a new inbound lead is a *cross-sell*, not a suppression.
3. **`tool_call`** — `add_blacklist` for the new suppressions, with a reason that says where it
   came from (`"HubSpot: offener Deal"`), so the next person can tell an automatic entry from a
   hand-made one.
4. **`feed_notify`** — report what was added, and flag anything ambiguous for a human.

**Never auto-*remove* a blacklist entry.** Additions are safe and reversible by a person;
automatic removals turn one bad CRM sync into an outreach incident. Removal is a human act.

## 3 — Check at enrollment, not only at build time

Reconciliation runs daily; deals open hourly. Both layers are needed:

- The platform's contactability gate checks unsubscribe and blacklist on **every** enrollment,
  deny-only, and **fails closed** — if the lead cannot be loaded, nothing goes out.
- Your own gate covers what the platform cannot know: an open deal that nobody has blacklisted
  yet. A `formula` column against a `list_deals` lookup, gated before the enroll column.

Note that `enroll_preflight` checks **neither** blacklist nor contactability. A clean preflight
is not permission.

## 4 — Feed the loop back

Suppression is not only inbound from the CRM. Two paths back:

- **A negative reply** — "nehmen Sie mich raus", "kein Interesse" — should become a blacklist
  entry, not just a closed card. Wire it into your reply-triage workflow.
- **A new customer** — when a deal closes won, the domain belongs on the list. This is the one
  people forget, and it produces the most embarrassing send there is.

## 5 — Verify it actually blocks

```bash
gtm call list_blacklist --json
gtm call enroll_preflight --input '{"lead_id":"<a blacklisted lead>"}' --json
```

Then try an actual enrollment on a test row and confirm it is refused. A blacklist entry you
have not seen block something is a belief, not a control.

## Why it belongs in every workspace

Every other play in this folder ends in an enrollment. This is the one that decides which
enrollments must not happen. Build it before the first campaign goes live, not after the first
complaint.
