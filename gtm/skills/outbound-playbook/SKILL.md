---
name: outbound-playbook
description: Use when deciding WHAT to build in a GTM Automation workspace, not how — choosing an ICP, picking a channel, setting cadence and volume, writing copy that survives spam filters, and judging whether a campaign is working. The go-to-market method behind the mechanics, with the numbers it rests on (benchmarks.md). Read this before drafting Wissen assets or a sequence; read gtm-quickstart for the build order, sequences for the touch plan, draft-gtm-play for the asset-by-asset methodology.
allowed-tools: Bash, Read, Grep, Glob
---

# The outbound playbook

The platform will faithfully execute a bad campaign. This skill is what stops you building
one — the go-to-market decisions that determine whether a workspace produces meetings, in
the order you actually face them.

Every rule here has a number behind it. They live in **`benchmarks.md`** next to this file:
anonymous aggregates over ~36,500 contacted leads across all workspaces on the platform,
plus one operator's six years of published DACH outbound practice. Read it when a
stakeholder wants to argue with a rule — that is what it is for.

## The one decision that dominates everything

**Precision of the list beats quality of the text.** A good message to the wrong list stays
ineffective. In the platform data, playbooks naming ≤ 5 regions reply at 4.06 % against
2.23 % for broader ones — with the outlier campaign excluded from both sides.

So the first question is never "what do we write". It is *who exactly, and why now*.

### Detect demand, don't generate it

Classic outbound treats every account the same: same list, same sequence, same pitch. The
alternative is to find the demand that already exists and speak to the accounts where
something just happened.

Four signal families carry the most weight:

| Family | Examples |
|---|---|
| **Hiring** | posting for SDRs, a sales lead, the function you sell into |
| **Digital** | website visit, LinkedIn engagement, content download |
| **Structural** | funding, new leadership, expansion, a tech change |
| **CRM** | lookalikes to customers you already won |

**The freshness rule: a signal is hot for 3–7 days and cold after ~28.** Approaching late
reads as researched rather than relevant, and does more harm than staying silent. Build the
freshness rule into the table as a gate, not into somebody's memory.

If you cannot find a reason to write *this week*, the contact is not ready. That is a
finding, not a failure.

## Choose one channel and finish it

Playbooks running a single channel reply at 5.16 %; those running two at 1.84 %. That is not
an argument against multichannel — channels do reinforce each other — it is what a second
channel looks like when it is added without its own copy, cadence and sender.

| Channel | Where it wins | Hard limit |
|---|---|---|
| **Email** | scale and measurability; the backbone | 15 cold sends per inbox per day |
| **LinkedIn** | seniority, visibility, warm routes off engagement | 20–25 connection requests per account per day |
| **WhatsApp** | local and owner-led businesses, short cycles | 10–20 new conversations per number per day |

Those limits are not throttles you may raise. A connected LinkedIn or WhatsApp account is a
real account with real ban risk, and email volume per inbox is what burns domains. Reach
grows by adding senders, never by raising per-sender volume.

**Channel offset, when you do run two:** a LinkedIn connect without a pitch two days before
the first email. Face before pitch. Email leads, LinkedIn flanks.

## Cadence: five touches, increasing gaps

Day **1 → 4 → 9 → 16 → 25**. Every step carries a new angle — an observation, an example, a
real question — never "just following up". Most replies do not come from the first message,
and most senders quit after two.

**Stop rules, both mandatory:**
- A reply pauses **every** channel for that lead immediately.
- No reply → 60–90 day cooldown, and re-entry only on a **new** signal.

## Copy that survives the filter

Deliverability is a subtraction game: everything that makes a mail look like bulk costs you.
The rules that matter most, in order of effect:

1. **No links in the body.** No calendar link, no "learn more", no signature banner. The
   link goes in the reply, from a human or an approved draft. This feels like a lost
   conversion and is the single largest deliverability lever there is.
2. **No open tracking.** The pixel is trivially detectable. Consequence: open rate does not
   exist as a metric — which is fine, because it never measured anything useful.
3. **Plain text, ≤ 90 words.** No HTML, no caps blocks, no multiple exclamation marks.
4. **No filter vocabulary** — "free", "guaranteed", "offer". When a model writes the copy,
   that negative list belongs *in the prompt*, so the rule holds on every personalised
   variant rather than on the template you reviewed.
5. **Line one carries a real trigger.** Test it like this: *would this first line also fit
   the recipient's competitor?* If yes, it is not personalisation, it is a mail merge.
6. **Respect for the reader's time.** Write shorter than feels right. Delete every adjective
   that proves nothing. In DACH especially, pressure creates resistance and clarity creates
   trust.

WhatsApp has its own rules: 2–3 sentences, under 300 characters, a local hook, **no link in
the first message**, an explicit opt-out ("a short no is enough"), and the offer only in
message two after a reaction. Maximum one follow-up after 3–4 days.

## Volume follows from the target, not from ambition

```
contacts needed = meeting target / (reply rate × positive share × meeting rate)
```

Ten meetings a month at 5 % / 30 % / 50 % needs 1,334 contacts → ~3,300 emails → ~152 a day
→ ~10 inboxes → ~3 domains. Double the positive share and the contact requirement halves.

This is why targeting and message work are not "soft": every point of improvement upstream
removes infrastructure cost downstream. Volume is the most expensive and most dangerous
lever, and it is the one everybody reaches for first.

Never send from your main domain. Company mail — invoices, customer threads — has nothing to
do with cold volume, and the reputation damage there is business-critical.

## Measure replies, not activity

| Metric | What it tells you | Reference |
|---|---|---|
| **Unique replies per contacted lead** | the health *and* success metric | avg 3.9 %, best 11.9 % |
| **Positive share of replies** | whether targeting or copy is off | LinkedIn 28 % · WhatsApp 25 % · email 17 % |
| **Bounce rate** | early warning, before damage | target < 2 %, alarm at 3 % |
| **ICP fit rate of sourced companies** | whether the ICP is sharp enough | below ~60 % → the ICP is too vague |
| **Meeting-to-close rate** | whether the chain produces the *right* meetings | the north star |

Open rate is deliberately absent. So is "emails sent".

Expect roughly three no's per yes: across the platform, classified replies run 45 % negative,
26 % positive interest, 21 % neutral. A negative reply is a disqualification you did not have
to pay for. When the negative share collapses, that is usually a targeting failure — nobody
is engaged enough to bother saying no.

## Improve by rebuilding, not by scaling

The largest single gain in the platform data came from rebuilding a campaign on the *same*
audience: 5.28 % → 16.18 % reply rate, at half the volume. The list did not change. The
message did.

So when a campaign underperforms, the order of moves is:

1. **Is the list right?** ICP fit rate below 60 % → fix the ICP, not the copy.
2. **Is there a trigger?** No signal in line one → add one, or stop contacting these accounts.
3. **Is the message specific?** Apply the competitor test to line one.
4. **Only then**, more contacts.

## Close the loop or start from zero every month

Sourcing, sending and following up are the first three links. The three most teams skip:

- **Classify every reply** — intent, sentiment, objection. Unclassified replies mean the same
  mistakes repeat, only faster.
- **Rate every meeting** — outcome and the reason. Many meetings with a low close rate means
  the ICP or the qualification is too loose, and no amount of copy work fixes that.
- **Feed it back** — a losing angle becomes a revised messaging asset; a converting signal
  gets weighted up. Versioned knowledge, not a decision in a weekly meeting.

Without those, outbound is linear: volume in, meetings out, and every month starts near zero.
With them, the same effort compounds.

**Fix your vocabulary while you do it.** Objection reasons and industry labels recorded as
free text are unusable in aggregate — in the platform data the same industry appears under
four different names, and objection texts are almost all unique. Make the classifier choose
from a fixed list. One sentence in a prompt, and the difference between a measurable campaign
and an anecdote.

## Compliance is part of the method

- Both opt-out paths must actually work, and an unsubscribe must reach the send path — the
  platform enforces this before every send, and so should your copy.
- WhatsApp and DSGVO are two separate obligations: platform rules can cost you the number;
  DSGVO needs a documented legal basis, transparent data provenance and easy objection.
- The gates in the platform are deny-only and fail closed: if the lead cannot be loaded, the
  send does not happen. Do not build a motion that routes around them — and none of this is
  legal advice; check your case with your own counsel.

## Anti-patterns, each of which has cost somebody a quarter

- **Table first, strategy never** — columns with hand-typed prompts that drift apart.
- **A sequence with no steps** — 45 of 88 sequences on the platform are empty shells that
  look configured.
- **Free-form copy at scale** — use a fixed template with generated `{hook}` / `{pain_point}`
  fills, so output stays predictable at 40 rows and at 4,000.
- **Cold lists over signals** — 5,000 companies with no trigger is spray and pray.
- **An unbounded first run** — never run 4,000 rows before you have read 20.
- **Raising per-sender volume** to get reach.
- **Sending from the main domain.**
- **Chasing open rates.**

## Next

- Build order, zero to first live sequence → **gtm-quickstart**
- Asset-by-asset strategy drafting → **draft-gtm-play**
- Touch plans, senders, enrollment → **sequences**
- The table that executes it → **build-gtm-workflow**
