# Play: keyword and competitor signals

**Use when** your buyers discuss the problem publicly — under a competitor's posts, in a
topic's hashtag, around an industry debate. You did not need to write the post; you only need
to notice who engaged with it.

**Shape:** keyword watch → engaged companies and leads → qualify → warm approach that
references what they said.

---

## 1 — Choose keywords like a buyer, not like a marketer

Keywords are the whole play. Three kinds work:

| Kind | Example | Why |
|---|---|---|
| **Problem language** | "Leadqualifizierung", "Datenqualität CRM" | how they describe the pain |
| **Competitor terms** | a competitor's product name, their campaign hashtag | people engaging are in-market and comparing |
| **Trigger vocabulary** | "wir stellen ein SDR", "Markteintritt DACH" | the event that creates the need |

What does not work: your own category name. Nobody with the problem searches for the label you
gave the solution.

## 2 — Schedule the watch

`social_listening` is **schedule-only**:

```bash
gtm call workspace_table_schedule_source --input '{
  "table": "Signals",
  "source": "social_listening",
  "config": {
    "playbook_id": "<id>",
    "keywords": ["Leadqualifizierung", "<Wettbewerber>", "SDR einstellen"],
    "min_engagement": 3,
    "max_posts": 20
  },
  "cadence": "daily"
}' --json
```

`min_engagement` is the noise filter: a post nobody reacted to produces no useful engagers.
Free, and it runs on the connected LinkedIn account — so its budget is the ceiling.

Returns **engaged companies plus leads**, not just posts.

## 3 — Separate engagement from intent

Identity block first: `full_name`, `salutation`, `job_title`, `company_name`, `industry`.

Someone commenting under a competitor's post might be a buyer, a rival, or an employee.

| Column | Kind | Returns |
|---|---|---|
| `relation_to_topic` | `ai` | one of a **fixed enum**: `buyer` · `competitor` · `employee` · `commentator` |
| `stance` | `ai` | `frustrated` · `interested` · `defending` · `neutral` |
| `quote` | `ai` | their own words, ≤ 20 words, verbatim — no paraphrase |

Gate on `relation_to_topic == 'buyer'`. The enum matters: as free text these come back as
forty different phrasings and the gate cannot be written.

`stance == 'frustrated'` under a competitor's post is the single strongest signal this play
produces. Route those first.

## 4 — The approach references what they said

The whole advantage is that you can quote them:

> {{cell.salutation}}, Sie schrieben unter dem Beitrag von {{cell.post_author}}:
> „{{cell.quote}}". Genau daran arbeiten wir mit {{cell.case_match}}. Spielt das bei
> {{company.name}} auch eine Rolle?

Two rules that keep this from turning creepy:

1. **Quote, never paraphrase.** A paraphrase of someone's comment reads as if you skimmed it.
2. **Never name the competitor as a competitor.** Reference the topic, not the rivalry.
   "I saw you commented on X's post about Y" is fine; "since you're unhappy with X" is not.

## 5 — Freshness

Same clock as every signal play: hot 3–7 days, cold after ~28. A comment from six weeks ago is
not a conversation opener. Gate on it, and let cold rows fall out rather than accumulate.

## Related

- **`own-post-engagers.md`** — the same mechanic on your own posts, warmer but lower volume.
- Deeper watching of a *fixed* target list — career pages, pricing pages, newsrooms — is
  `job-openings.md`, which uses a signal watch rather than a source.
