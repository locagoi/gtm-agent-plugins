# Play: own-post engagers

**Use when** someone on the team posts on LinkedIn and people react to it. Every reaction is a
person who raised their hand in public — the warmest list you will ever get for free.

**Shape:** watch one profile's posts → everyone who engaged becomes a lead → qualify →
LinkedIn sequence that references the post they engaged with.

**Why it beats cold:** the opener writes itself and it is true. Reply rates on this route run
above the cold LinkedIn baseline, because the approach connects to something the person
actually did this week.

---

## 1 — Schedule the watch

`profile_posts` is **schedule-only** — it is a loop, not an import:

```bash
gtm call workspace_table_schedule_source --input '{
  "table": "Engagers",
  "source": "profile_posts",
  "config": {
    "playbook_id": "<id>",
    "profile_url": "https://www.linkedin.com/in/<the-poster>",
    "max_posts": 5
  },
  "cadence": "daily"
}' --json
```

It reads that one profile's **own posts** and returns everyone who engaged, as **leads**. Free
— it runs on the connected LinkedIn account, which is also the constraint: it consumes that
account's action budget.

**Whose profile:** the founder or the subject-matter voice, not the company page. People react
to people. If nobody on the team posts, this play has no fuel — say so rather than building it.

## 2 — Keep the context that makes it warm

Show the lead identity block first: `full_name`, `salutation`, `job_title`, plus
`company_name` so you can see where they work. Nothing else about the person.

The engagement itself is the hook, and it decays. Four columns:

| Column | Kind | Job |
|---|---|---|
| `engaged_post` | from the source | which post, and what it was about |
| `engagement_type` | from the source | reaction · comment · repost — a comment is worth far more |
| `engaged_at` | from the source | the freshness clock |
| `fresh` | `formula` | `engaged_at` within 7 days → `hot`, 28 → `warm`, else `cold` |

**Gate everything downstream on `fresh != 'cold'`.** A message referencing a post someone
liked five weeks ago reads as surveillance, not attention.

## 3 — Qualify

```bash
gtm call workspace_table_add_column --input '{
  "table": "Engagers", "key": "persona_fit", "kind": "ai",
  "config": { "module": "agent:persona_fit" }
}' --json
```

Engagement is not fit. Plenty of reactions come from peers, competitors and job seekers —
`agent:persona_fit` separates them, and the ICP check on the employer separates the rest.

## 4 — The sequence: connect, then reference

Four touches, and the first one carries no pitch:

| # | Step kind | Content |
|---|---|---|
| 1 | `linkedin_invite` | **empty note** — accepted more often than any pitch |
| 2 | `linkedin_message` | thanks + the post + a validating question, ≤ 150 chars |
| 3 | `linkedin_message` | problem → proof → possibility → soft ask, ≤ 250 chars |
| 4 | `linkedin_message` | break-up, ≤ 100 chars |

Touch 2 is where the play pays off:

> Danke fürs Annehmen, Herr {{lead.last_name}}. Sie hatten auf den Beitrag zu
> {{cell.engaged_post}} reagiert. Spielt {{cell.pain_point}} bei {{company.name}} gerade eine
> Rolle?

**Respect the limit: 20–25 connection requests per account per day.** A connected LinkedIn
account is a real account with real ban risk, and this play is capped by that, not by supply.

## 5 — Or install it

The platform ships this chain as a workflow template:

```bash
gtm call install_workflow_template --input '{
  "slug": "post-engagers-to-linkedin-outreach", "playbook_id": "<id>"
}' --json
```

It scans engagement daily, writes engagers as rows, runs the qualification and copy columns,
and enrolls the qualified ones — skipping cleanly when there are no new engagers and when
nothing qualified. Install it unless you need a shape it does not have.

## Variant: one specific post

For a single post that went well, use the one-shot source instead of the schedule:

```bash
gtm call workspace_table_add_source --input '{
  "table": "Engagers", "source": "post_engagers",
  "post_url": "https://www.linkedin.com/posts/…", "max_engagers": 200
}' --json
```

This one returns the **employer companies** behind the engagers rather than the people — use
it when the account, not the individual, is the unit you sell to.
