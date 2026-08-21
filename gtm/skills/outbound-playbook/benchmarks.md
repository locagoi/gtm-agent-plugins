# Benchmarks: what the numbers actually say

Two sources, kept apart on purpose.

**A — Platform patterns.** Directional findings from campaigns running on GTM Automation,
aggregated across all workspaces. Reported as ratios and rounded rates only: no per-customer
figures, no campaign volumes, no dataset counts. Nothing here is attributable to any
workspace, campaign or contact.

**B — Operator data.** cegtec's own published outbound practice
([cegtec.net/academy](https://www.cegtec.net/academy)) — one operator's numbers, six years
of DACH B2B outbound.

Neither is a promise. They are the reference points to argue with when someone says
"let's just send more".

---

## A1 — Narrow beats broad, by roughly 2×

Playbooks whose ICP names **five regions or fewer reply at roughly twice the rate** of those
naming more — about 4 % against about 2 %. The gap holds with the strongest-performing
campaign excluded from both sides, so it is not one outlier carrying the result. Including it,
the gap is wider still.

The same pattern shows up for industry breadth and for company-size windows. The mechanism is
not mysterious: a narrow ICP is one you can write a specific first line for.

**Rule:** name ≤ 5 regions and ≤ 6 industries per playbook. If the list needs more, that is
two playbooks, not one.

## A2 — One channel done properly beats two done partly

Playbooks running a **single channel reply at roughly 2–3× the rate** of those running two.

Read this as a warning about *split attention*, not as proof that multichannel is wrong — the
academy's own guidance is that channels reinforce each other. What the pattern shows is that
a second channel added without its own copy, its own cadence and its own sender performs
worse than not adding it.

**Rule:** ship one channel end to end. Add the second when the first has a measured reply
rate, and give it its own copy — not a forwarded email.

## A3 — Rebuilding beats scaling

The largest improvements observed come from rebuilding a campaign on the **same** audience —
same ICP, same industries, same region — with revised copy and a tighter company-size window.
A rebuild of that kind can **multiply the reply rate several times over at lower volume**.
Nothing about the list changes; the message does.

**Rule:** when a campaign underperforms, the next move is a rebuild of the message, not more
contacts. Volume is the most expensive lever and the only one that damages the infrastructure.

## A4 — Half-built sequences are the most common silent failure

A sequence created, named, wired to an enroll column — and containing **no steps**. It sends
nothing and it errors never, so the motion looks finished. This is one of the most frequent
build faults there is, and it survives precisely because nothing complains.

**Rule:** a sequence without steps is not a sequence. Call `get_sequence` and read the step
list before you call a motion built.

## A5 — Reply mix: expect roughly three no's per yes

Across classified inbound replies, the rough shape is: **~45 % negative · ~25 % positive
interest · ~20 % neutral**, with the remainder objections and auto-replies. Positive share of
replies runs highest on LinkedIn, then WhatsApp, then email.

A negative reply is a *good* outcome compared to silence: it is a disqualification you did not
have to pay for. Campaigns whose negative share collapses usually have a targeting problem,
not a copy win — nobody is engaged enough to say no.

## A6 — Fix your vocabulary at ingest

The most common reason a campaign cannot be analysed later is not missing data — it is
uncontrolled vocabulary. Industry labels, persona names, disqualification reasons and
objection types recorded as free text fragment into near-unique strings: the same industry
ends up spelled four different ways, and every per-industry comparison silently splits.

**Rule:** pick one label per industry, one key per signal type, one name per persona, and make
every classifying column choose from that fixed list — never free text. This costs one
sentence in a prompt and is the difference between a measurable campaign and an anecdote.
Decide it before the first run; it is not recoverable afterwards.

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
