---
name: validate-gtm-theses
description: Use BEFORE drafting a play or building a table, whenever a new motion, vertical or audience is being opened — and whenever the user says "test what works", "which hypothesis", "A/B", "validate", "we're not sure this is the right audience". The methodology layer ABOVE draft-gtm-play: a campaign is one cycle of a hypothesis test, not a delivery. Plural competing theses, one variable per run, first contact as a measuring instrument, and a decision about the thesis as the exit criterion.
allowed-tools: Bash, Read, Grep, Glob
---

# The campaign is an experiment

`draft-gtm-play` answers *how do we reach them*. This skill answers the question underneath it:
**which of our guesses about them is actually true.** Skip it and you build a complete,
well-referenced play on top of an assumption nobody checked — and the first thing you learn is
also the most expensive thing you could have learned: four weeks in, at volume.

> **Where this sits:** `gtm-quickstart` calls `draft-gtm-play` at stage 2. This wraps around
> that call. `draft-gtm-play` produces **one** play; this decides which theses deserve one, in
> which order, and when to bury one. Copy mechanics: `sequences/copy-patterns.md`. Numbers and
> channel decisions: `outbound-playbook`.

**The unit of work is a thesis, not a campaign.** A campaign is what one thesis costs to test.
Rename it in your head and most of the wrong decisions stop being tempting.

## Phase 0 — Theses in the plural

Out of the intake come not *the* pain and *the* angle, but **3–5 competing guesses** about why
someone would react. Each one stated so it **can be false**:

| Not a thesis | A thesis |
|---|---|
| "Mittelständler haben Nachfolgeprobleme." | "Bei Inhabern über 60 ohne eingetragene zweite Geschäftsführung ist die Übernahme ungeregelt — und drückend genug, dass sie auf eine Frage danach antworten." |
| "Unsere Zielgruppe braucht bessere Daten." | "Die Auswertung scheitert nicht am Tool, sondern daran, dass niemand die Stammdaten pflegt — und der Leiter Vertrieb weiss das." |

Two parts make it testable: **a condition you can detect from outside**, and **a claimed
intensity** ("drückend genug, dass sie antworten"). Without the second half you have a
description, and a description cannot fail.

Write them down before the first list is built. Theses invented after the numbers arrive are
explanations, not hypotheses.

## Phase 1 — One signal per thesis, and the signal is the list

Each thesis needs the signal that makes it checkable from outside. That signal determines the
list — which is why **different theses are different segments, not arms of one split.** Two
theses about two different populations cannot be A/B-tested against each other; they are two
cycles running in parallel.

If a thesis has no detectable signal, that is a finding: either sharpen it until it has one, or
park it. An untestable thesis consumes the same volume and returns nothing.

## Phase 2 — Two to three angles per thesis

Only here does splitting inside one list begin. Same audience, same thesis, different framing
of the same pain.

## Phase 3 — First contact as a measuring instrument

The stance is **uncertainty about whether you have landed in the right place** — and the mail
validates the thesis instead of selling against it.

- The uncertainty points at **their** situation, never at your own subject. *"Von aussen ist
  nicht zu erkennen, ob das bei Ihnen ansteht"* is right. *"Vielleicht können wir helfen"* is
  worthless — uncertainty about your own offer disqualifies you.
- It must be **nameable**: the specific thing that cannot be seen from outside. Not a hedging
  phrase.
- Offer a cheap exit — *"Wenn ich danebenliege, sagen Sie kurz Bescheid."* The exit is what
  earns the answer.
- **No proof, no case study, no numbers in message 1.** They answer a question nobody has
  asked yet, and they turn a validation into a pitch. Proof moves to message 2, after the
  thesis is confirmed. The proof-forward template in `sequences/copy-patterns.md` describes the
  **sequence**, not the single mail.
- CTA validates, never asks for time. No calendar link in message 1.

This matters most where the thesis touches something personal — succession, a failed project,
a departure. Asserting it is presumptuous and shuts the door; marking it openly as a guess
opens it.

## Phase 4 — The test design, written before the send

### One level per run

| Level | Where it splits | Volume it needs |
|---|---|---|
| **Thesis** | separate segments, parallel cycles | one list each |
| **Angle** | inside one list, whole body changes | moderate |
| **CTA / one line** | inside one list, one sentence changes | the most |

Vary thesis, angle and CTA at once and you end up with a winning variant and no idea which part
won. That is volume, not knowledge.

### The arithmetic that decides what you can test

At a 5 % reply-rate baseline, two-sided, 80 % power:

| Effect to detect | Contacts **per arm** |
|---|---|
| 5 % → 8 % (+60 % relative — very large) | ~1,000 |
| 5 % → 6 % | ~8,000 |

A 400-row list split in two gives about ten replies per arm. The difference between 9 and 11 is
noise, however cleanly the test was set up.

### At small N, test the big levers

This inverts the usual advice — and the note in `copy-patterns.md` that the CTA is the cheapest
thing to test. Cheap to *build*, yes. But only an effect large enough to roughly double the
reply rate is visible at two-digit reply counts, and a different CTA line almost never is,
while a different thesis or angle can be. **Spend scarce volume on the levers big enough to
show up.** Save CTA tests for the lists that can carry them.

Where significance is out of reach, replace it — do not fake it:

1. **A decision rule, fixed in advance.** *"Arm under X replies after Y days is switched off."*
   Declared as a heuristic, it is honest and it works. Criteria set afterwards are not criteria.
2. **Accumulate across cycles.** The same angle tested five times builds the N that one campaign
   cannot. This is exactly what Learnings with confidence / reinforcement / decay are for. An
   angle test evaluated once and then forgotten throws away the only path to a number you can
   trust.

## Phase 5 — Four reply classes

Classify every reply into exactly one:

| Class | What it tells you |
|---|---|
| **Yes** | thesis holds, and this one is workable |
| **No, because…** | **the actual yield** — *why* the thesis does not carry |
| **Wrong person** | routing problem, says nothing about the thesis |
| **No reaction** | weakest signal; only readable in aggregate |

Keeping "wrong person" apart from "no, because" is the one distinction people skip, and it
kills good theses for the wrong reason. A mail that reached the assistant did not test anything.

## Phase 6 — Write the learning back

Confirmed → revise the asset (new version, history kept). Refuted → close the segment **and
record why**. Both belong in Wissen. A refuted thesis that only lives in someone's memory gets
retested next quarter by someone else.

## Phase 7 — Next cycle

Next level on the same thesis, or the next thesis. Then back to Phase 4.

## What is unfamiliar about this

A cycle's success is measured in **theses validated or buried**, not in meetings. Meetings are a
by-product. A cycle that cleanly kills a thesis succeeded: it answered the most expensive open
question more cheaply than another round of guessing would have.

The uncomfortable consequence: **switching a segment off is a result, not a failure.** Without
that reframing the process does not run, because nobody volunteers to bury a thesis that a
quarterly target is hanging on.

## Worked example: the succession play

An advisory selling to owner-managed Mittelstand. Four competing theses, four segments:

| # | Thesis | Signal that makes it checkable |
|---|---|---|
| T1 | Succession is unsettled and the owner knows it | owner-manager, no second managing director in the commercial register |
| T2 | Succession is settled, but the valuation is unclear | recent change in management, no advisory mandate visible |
| T3 | The owner does not want to sell but to hand over shares | company growing, second generation present in the register |
| T4 | The owner is the wrong address — the tax adviser is | small company, no advisory board |

T1 and T4 differ only in *who* gets contacted, not in the claim — that pair is the cheapest
first cycle, because it separates a routing question from a thesis question before either is
scaled.

Message 1 for T1, three paragraphs, no proof, cheap exit:

```
{{anrede}},

{{hook}}

bei inhabergeführten Betrieben Ihrer Grösse hängt die Übergabe oft an einer
einzigen Person — und von aussen ist nicht zu erkennen, ob das bei Ihnen
schon geregelt ist oder noch aussteht.

Liege ich falsch, ist die Sache erledigt — dann sagen Sie mir das gern kurz.

{{signatur}}
```

The angle variant keeps hook and structure and changes only the framing of the pain — dependency
on one person (above) against the tax-driven timeline of a transfer. The CTA test comes later,
on whichever segment turns out to carry volume.

**One caution on this example:** signals derived from a person's age or family situation are
regulated and, more practically, read as invasive when they surface in the copy. Detect on
company facts from the register; never write the inferred personal fact into the message.

## Anti-patterns

- **One thesis, treated as the premise** — the play is built, the mechanics are clean, and the
  assumption underneath was never a question. This is the default failure and the reason this
  skill exists.
- **Theses written after the results** — those are explanations. Fix them in writing beforehand.
- **Three variables at once** — a winner with no attribution.
- **Significance theatre at N = 20** — a decision rule fixed in advance is honest; a p-value on
  ten replies is not.
- **Discarding negative replies** — "no, because" is what you actually bought with the send.
- **Proof in message 1** — turns the measuring instrument back into a pitch.
- **Scaling the first thesis that produced a meeting** — one meeting is not a validated thesis,
  and the cycle that would have found the better segment never runs.
