# Benchmarks: what the numbers actually say

Two sources, kept apart on purpose.

**A — Platform data.** Aggregates over every campaign running on GTM Automation:
15 workspaces, 74 playbooks, ~36,500 contacted leads, 1,635 recorded conversions.
Anonymous and aggregated; no workspace, campaign or contact is identifiable.

**B — Operator data.** cegtec's own published outbound practice
([cegtec.net/academy](https://www.cegtec.net/academy)) — one operator's numbers, six years
of DACH B2B outbound.

Neither is a promise. They are the reference points to argue with when someone says
"let's just send more".

---

## A1 — Narrow beats broad, by roughly 2×

Reply rate by how many regions the playbook's ICP names:

| ICP region scope | Contacted | Reply rate |
|---|---|---|
| ≤ 5 regions | 18,437 | **4.06 %** |
| > 5 regions | 18,015 | **2.23 %** |

The outlier workspace (one LinkedIn motion far above every other) is excluded from both
rows, so this is not one campaign carrying the result. Include it and the gap widens to
7.20 % vs 2.22 %.

The same holds for industry breadth and for company-size windows. The mechanism is not
mysterious: a narrow ICP is one you can write a specific first line for.

**Rule:** name ≤ 5 regions and ≤ 6 industries per playbook. If the list needs more, that
is two playbooks, not one.

## A2 — One channel done properly beats two done partly

| Channels on the playbook | Contacted | Reply rate |
|---|---|---|
| 1 | 11,953 | **5.16 %** |
| 2 | 21,196 | **1.84 %** |
| 3 | 3,303 | 4.33 % |

Read this as a warning about *split attention*, not as proof that multichannel is wrong —
the academy's own guidance is that channels reinforce each other. What the data shows is
that a second channel added without its own copy, its own cadence and its own sender
performs worse than not adding it.

**Rule:** ship one channel end to end. Add the second when the first has a measured reply
rate, and give it its own copy — not a forwarded email.

## A3 — Rebuilding beats scaling

The largest single improvement in the dataset came from rebuilding a campaign on the
*same* audience — same ICP, same industries, same region — with revised copy and a
tightened company-size window:

| | Contacted | Reply rate |
|---|---|---|
| First version | 871 | 5.28 % |
| Rebuilt version | 445 | **16.18 %** |

Three times the reply rate at half the volume. Nothing about the list changed; the
message did.

**Rule:** when a campaign underperforms, the next move is a rebuild of the message, not
more contacts. Volume is the most expensive lever and the only one that damages the
infrastructure.

## A4 — Most sequences are never finished

Of 88 sequences configured across all workspaces, **45 contain zero steps** — created,
named, and never filled. Of those that do have steps:

| Channel | Typical steps |
|---|---|
| Email | 3–4 |
| LinkedIn | 3–4 (max 6) |
| WhatsApp | 1–2 |

An empty sequence is not inert in a bad way — nothing sends, so nothing breaks. It is
worse than that: it looks configured. Somebody built the table, wired the enroll column,
and believes the motion is live.

**Rule:** a sequence without steps is not a sequence. Verify with `get_sequence` before
wiring anything to it.

## A5 — Reply mix: expect three no's per yes

Classified inbound replies across all workspaces (n = 2,830):

| Category | Share |
|---|---|
| Negative | 44.6 % |
| Positive interest | 25.6 % |
| Neutral | 20.5 % |
| Objection | 5.7 % |
| Auto-reply | 3.5 % |

Positive share of replies by channel: **LinkedIn 28.2 % · WhatsApp 24.7 % · email 17.4 %**.

A negative reply is a *good* outcome compared to silence: it is a disqualification you did
not have to pay for. Campaigns whose negative share collapses usually have a targeting
problem, not a copy win — nobody is engaged enough to say no.

## A6 — What the platform cannot yet tell you

Two measurement gaps, stated plainly because a guide that hides them wastes your time:

- **Step attribution.** Of 1,635 recorded conversions, **one** carries the sequence step it
  came from. So "which step books the meeting" is not answerable from the data — only
  "which campaign does".
- **Industry labels.** The same industry appears as `Banking`, `Bankwesen`,
  `Financial Services` and `Finanzdienstleistungen`. Any per-industry comparison silently
  splits into four.

**Rule:** fix your vocabulary at ingest. Pick one label per industry and one signal-type
key per signal, and make the qualification column choose from that fixed list — never free
text. This costs one sentence in a prompt and is the difference between a measurable
campaign and an anecdote.

---

## B1 — Email infrastructure (operator data)

| Setting | Value |
|---|---|
| Cold sends per inbox per day | **15** (account limit ~100, deliberately under it) |
| Warmup before the first campaign send | **3 weeks**, then never switched off |
| Inboxes per domain | 3–5 |
| Provider mix | ~44 % Google · ~40 % Microsoft · ~16 % IMAP |
| Accounts in error status at any moment | **~25 %** — plan redundancy, not perfection |

Scale horizontally: 30 inboxes × 15 mails = 450 clean sends a day. Raising per-inbox
volume is what burns domains.

## B2 — Bounce is the early-warning metric

| List | Bounce rate |
|---|---|
| Validated before import | **0.4 %** |
| Unvalidated import | **7.7 %** |

Same workspace, same domains, same setup — a factor of 19 from one validation step.
DACH market context: **> 5 %** starts domain damage, **> 8 %** and the domain is spent.
Target under 2 %; alarm at 3 %.

## B3 — Copy constraints that survive contact with filters

- Plain text, **≤ 90 words**, no HTML.
- **No open tracking** (the pixel is a visible spam signal) and **no links in the body** —
  no calendar link, no "learn more", no signature banner. The link goes in the *reply*.
- No filter vocabulary ("free", "guaranteed", "offer"), no caps blocks, no multiple
  exclamation marks. When a model writes the copy, put that negative list in the prompt.
- Open rate is not measured, because measuring it costs deliverability.

## B4 — Reply-rate reference points

| Metric | Value |
|---|---|
| Unique replies per contacted lead, average | **3.9 %** |
| Best campaign | **11.9 %** (regional, sharply defined target profile) |
| LinkedIn warm route (post-engagement) | above the cold LinkedIn baseline of 26.2 % |

## B5 — Per-channel operating limits

| Channel | Limit |
|---|---|
| Email | 15 cold sends per inbox per day |
| LinkedIn | **20–25 connection requests per account per day** — a connected account is a real account with real ban risk |
| WhatsApp | **10–20 new conversations per number per day**, ramping slowly; own number per campaign |

## B6 — Cadence

Day **1 → 4 → 9 → 16 → 25**. Increasing gaps, **max 5 touches**, every step carrying a new
angle rather than "just following up". Stop rules: a reply pauses every channel
immediately; no reply means a 60–90 day cooldown and re-entry only on a new signal.

Signal freshness: hot for **3–7 days**, cold after **~28**. A late approach reads as
researched rather than relevant and does more damage than no approach.

## B7 — The capacity formula

```
contacts needed = meeting target / (reply rate × positive share × meeting rate)
```

Worked example — 10 meetings a month at 5 % / 30 % / 50 %:

```
0.05 × 0.30 × 0.50 = 0.0075        →  10 / 0.0075 = 1,334 contacts/month
1,334 × 2.5 sent steps             =  3,335 emails/month
3,335 / 22 sending days            =  152 emails/day
152 / 15 per inbox                 =  ~10 inboxes  →  ~3 domains
```

Double the positive share and the contact requirement halves. That is why A1–A3 matter
more than any volume decision: every improvement upstream removes infrastructure cost
downstream.
