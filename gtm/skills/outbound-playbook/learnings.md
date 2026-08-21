# Cross-workspace learnings

Patterns from every campaign running on the platform, aggregated and de-identified. Ratios and
directions only: no per-customer figures, no volumes, nothing attributable to any workspace.

Each entry is a **pattern with what to do about it**. Where a finding is confounded, the
confound is named rather than hidden, because a pattern you cannot trust is worse than no
pattern at all.

---

## Targeting

### T1 · Narrow beats broad, roughly 2×

Playbooks whose ICP names five regions or fewer reply at about twice the rate of those naming
more. The gap survives excluding the strongest campaign from both sides. The same direction
shows for industry breadth and size windows.

**Do:** at most 5 regions and 6 industries per playbook, one vertical. If the list needs more,
that is two playbooks.

### T2 · One channel done properly beats two done partly

Single-channel playbooks reply at roughly 2 to 3 times the rate of two-channel ones.

**Confound worth naming:** this is not evidence against multichannel as such. It measures what
a second channel looks like when it is added without its own copy, its own cadence and its own
sender.

**Do:** ship one channel end to end. Add the second only when the first has a measured reply
rate, and give it its own copy.

### T3 · The industry axis is usually broken before it is analysed

The same industry appears under many spellings at once: a German label, an English label, a
compound label, and a near-synonym. Any per-industry comparison silently splits into four
weaker ones.

**Do:** fix one label per industry at ingest, and make the classifying column choose from that
closed list. This is not recoverable afterwards.

### T4 · Automated ICP learnings are noise below real volume

The system distils per-industry insights automatically. At current volumes most of them rest on
three to five replies, several contradict each other for the same industry, and the confidence
field does not track the sample size.

**Do:** before acting on any learning, read its denominator. Under ~30 replies in a segment it
is an anecdote. Treat the confidence score as a sorting aid, never as evidence, and never let
a 0-out-of-3 result kill a segment.

---

## Copy

### C1 · Shorter correlates with better, monotonically

Within a channel, positive reply share falls as messages get longer. On email the gradient runs
cleanly across four length buckets, and messages under 50 words reach roughly 2.5 times the
positive share of messages over 150. WhatsApp shows the same direction.

**Confound worth naming:** the email cohort mixes cold sends with thread replies, so the
absolute rates in it are far too high to quote. The *gradient within* the cohort is the
finding, because only length differs across the buckets.

**Do:** 80 words for a cold opener, 50 for a follow-up, 30 for a break-up. Three paragraphs.

### C2 · A question in the message beats no question

Among cold messages carrying no link, those containing a question reach a materially higher
positive share than those without. Strong on email, marginal on LinkedIn.

**Do:** end on a question. Make it validating ("does this play a role for you?") rather than
calendar-seeking. Then A/B which question, not whether to have one.

### C3 · The link correlation runs backwards

Messages containing a link show a much higher positive share than messages without. This is
reverse causation: you send the calendar link *because* someone replied positively. Reading it
forwards would mean putting links in cold bodies, which costs deliverability.

**Do:** no links in a cold body. Keep the link for the reply. And treat any metric where the
outcome could have caused the input with the same suspicion.

### C4 · An angle without volume is an opinion

Most messaging angles that exist in the platform never received meaningful traffic, and fewer
produced a measurable result. Teams create angles far faster than they test them.

**Do:** two variants at a time, one difference between them, split by row, and wait for roughly
100 leads per variant before reading anything into the difference. Retire the loser explicitly,
with its evidence.

### C5 · Free-text classification destroys its own analysis

Objection reasons, disqualification reasons and persona labels recorded as free text come back
almost entirely unique. The obvious question, *what disqualifies most of my list*, then cannot
be answered at all.

**Do:** every column whose output you will later count returns an `enum`. Decide the vocabulary
before the first run.

---

## Sequences

### S1 · Half-built sequences are the most common silent failure

A large share of sequences configured across the platform contain no steps at all: created,
named, wired to an enroll column, believed to be live. Nothing sends and nothing errors.

**Do:** `get_sequence` and read the step list before calling a motion built.

### S2 · Step attribution is not available, campaign attribution is

Recorded conversions almost never carry the sequence step they came from. So "which step books
the meeting" cannot be answered from the data, only "which campaign does".

**Do:** design experiments at campaign or variant level, where the data supports a conclusion.
Do not build a strategy on which step "works" until the step is actually recorded.

### S3 · Expect roughly three no's per yes

Classified replies run about 45 % negative, 25 % positive interest, 20 % neutral, the rest
objections and auto-replies. Positive share is highest on LinkedIn, then WhatsApp, then email.

**Do:** treat a negative reply as a free disqualification. Watch for the negative share
*collapsing* — that usually means nobody is engaged enough to say no, which is a targeting
failure wearing a calm face.

---

## Improvement

### I1 · Rebuilding beats scaling

The largest observed improvements come from rebuilding a campaign on the *same* audience with
revised copy and a tighter size window: several times the reply rate at lower volume. The list
did not change.

**Do:** when a campaign underperforms, the order is (1) is the list right, (2) is there a
trigger, (3) is the message specific, and only then (4) more contacts.

### I2 · Cost is decided by the gate, not by the price list

Contact enrichment costs 25 credits a row against 1 for qualification. A play that enriches
before it qualifies costs roughly twenty times what it needs to, for a list that is mostly
wrong.

**Do:** cheap verdict first, `run_condition` on everything expensive, enrichment last before
copy.

---

## How to read any of this

1. **Find the denominator.** No denominator, no finding.
2. **Ask what else changed.** T2 and C1 both carry confounds that are named above; the ones
   nobody named are the dangerous ones.
3. **Ask whether the outcome could have caused the input.** C3 is the worked example.
4. **Prefer a direction over a number.** "Roughly twice" survives a new quarter of data;
   "4.06 % versus 2.23 %" does not.
5. **Re-derive rather than inherit.** These are patterns across all workspaces. Yours is one
   workspace, and the only numbers that should change your behaviour are the ones from your own
   funnel once it has volume.
