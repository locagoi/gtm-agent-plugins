---
name: playbook-from-winners
description: Use when a new offer, audience or channel is about to be opened, or a motion has a clear winner worth repeating — mine what provably converts in this workspace (playbooks, sequences, variants, angles, the replies themselves), pick the closest analogous winner, distil the pattern and the reason it works, and draft a NEW playbook on that evidence. The playbook is created as an inert draft after an explicit yes and is never activated by this skill. Part of the closed loop (see closed-loop); the station that starts the next turn.
allowed-tools: Bash, Read, Grep, Glob
---

# Playbook from winners

Station 6 of the closed loop — and the start of the next turn. A new playbook built from
opinion repeats every mistake the workspace has already paid for. Built from what provably
converted, it starts where the last one ended.

Obeys the rules in **`closed-loop`**. The asset-by-asset method (ICP → persona → offer →
proof → angle → signals) is **`draft-gtm-play`**; treating the new playbook as a hypothesis
test is **`validate-gtm-theses`**.

## Inputs

- **Target**: the offer and the audience the new playbook is for, and the channel if fixed.
- If the target is vague, derive what you can from Wissen and existing playbooks first, then
  ask two or three sharp questions — not a questionnaire.

## 1. Mine the winners (read-only)

- `get_reply_rate_breakdown`, grouped by playbook first, then by sequence, variant and
  channel — positive rates with `n`, interval and `low_sample`.
- `list_playbooks`, `list_sequences` + `get_sequence` — ICP, offer, channel and sequence shape
  of each candidate.
- `list_messaging_angles` (per persona) — the angles that were tested, and which is default.
- `wissen_asset_list` / `wissen_asset_get` — ICP, persona, offer, proof, angle assets, and
  approved Learnings (what the system distilled from booked meetings and replies).
- `list_replies` / `list_conversations` — **what prospects actually said**: the pains they
  raised, the objections, the questions. This is the demand side, and often the richest one.
- `outbound-playbook/learnings.md` — cross-workspace patterns, each with its confound named.

**Trust floor.** A rate counts only when it stands on enough contacted leads and the tool does
not flag it `low_sample`. Write the floor down before mining.

## 2. Pick the winner — by analogy, explicitly

Score each candidate on three axes, in this order of weight:

1. **Offer shape** — what is promised and which main objection it removes. Heaviest.
2. **ICP and persona** — industry, size, seniority, decision-making power.
3. **Channel.**

Take the top one to three. **A channel mismatch alone does not disqualify a winner** — that is
the common case, handled in step 3. Your scale bar is a *watch criterion* for the new
playbook, not a selection filter: the best analogous winner is the structural seed even if it
sits below that bar.

If no candidate clears the trust floor, say so plainly and proceed as an **informed
experiment** — do not stall, and do not dress a guess as data.

## 3. Distil the pattern and the reason

For each chosen winner, one evidence block:

```
ICP · persona · channel · angle · sequence shape · lead magnet
numbers: reply rate · positive rate · n  (tool)
why it works: <e.g. a single research-led question as the opener; an easy-yes lead magnet
               instead of a meeting ask; the offer removes the main objection in line one>
```

Then the **demand ↔ supply check**: which pains do prospects raise that the offer does not
address yet (those lead the opener), and does the value proposition cover the pains it
already meets?

## 4. Draft the playbook (gated)

Preview, verbatim, then wait for an explicit yes:

```
PLAYBOOK DRAFT — <name>      status: draft, inert, manual release
ICP:          industries · size · regions · language
OFFER:        headline + one-line value proposition
CHANNEL(S):   <channel>
PERSONA:      titles · seniority · decision power · top challenges
ANGLE:        name · tone · CTA · core hook   [+ challenger, if this is an experiment]
SEQUENCE:     step-by-step shape, channel-native
LEAD MAGNET:  type — must already exist
GROUNDED IN:  winner(s) + numbers (rate, n, tool) + why
ADAPTATIONS:  what differs from the winner, and why it is an informed bet
WATCH:        the first metric to check, and the bar for scaling
```

After the yes:

- Stand on a template where one fits — `recommend_templates` / `apply_template` with a
  playbook bundle, or `create_playbook_from_template`; otherwise `create_playbook`. Every path
  creates the playbook as a **draft and inert**: nothing is sourced, nothing is sent.
- `create_messaging_angle` for the winning angle (and the challenger, if any).
- Pin or revise the Wissen assets it needs (`wissen_asset_create` / `wissen_asset_revise`).

**New channel = informed experiment.** When the winner's channel differs from the target
channel, port the angle and the structural principles, not the literal copy — a forwarded
email is not a LinkedIn message — and seed an A/B test on the riskiest element.

**Never activate.** Putting the playbook in service (`set_playbook_status`) and the first
enrollment are separate decisions, through **`gtm-quickstart`** stages 6–8 and
**`enroll-outreach`**.

## Guardrails

- Every recommendation cites its numbers and the tool behind them. No unevidenced "best
  practice".
- Never copy another motion's copy verbatim into a new audience; port the reason it worked.
- Claims in the new copy must be backed by a proof asset in Wissen.

## Output

The evidence blocks, the demand ↔ supply check, the draft preview — and after the yes, the
new playbook id with a one-line summary of what it stands on and what to watch first.
