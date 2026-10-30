---
name: optimize-outreach
description: Use weekly, or when a campaign under-performs, to decide what to change — measure every sequence, step and A/B variant on real replies and positives, judge each against a bar fixed in advance (keep, stop, scale, unclear), and write at most three concrete proposals, each with its evidence, the exact change on yes and what we learn on no. This run changes nothing; proposals are executed only after approval. Part of the closed loop (see closed-loop).
allowed-tools: Bash, Read, Grep, Glob
---

# Optimize outreach

Station 5 of the closed loop. **This run measures, judges and proposes. It changes nothing.**
A human decides; only then is exactly the approved change made. With no approval, nothing
happens. A rejected proposal is still a result: it tells you which assumption was wrong.

Obeys the rules in **`closed-loop`**. The method behind "one variable per run" is
**`validate-gtm-theses`**; copy structure and the pre-send check are in
**`sequences/copy-patterns.md`**.

## Inputs

- Nothing → every active sequence in the workspace.
- A playbook or sequence → just that.
- Your bar, written down before you start (see step 2).

## 1. Measure — per sequence, step and variant

- `get_reply_rate_breakdown` — positive reply rate per playbook, sequence, step, A/B variant,
  channel or sender over the last N days. Use `group_by: "variant"` with a `sequence_id` to
  read an A/B test. Every group carries `n`, a 95 % interval and `low_sample`.
- `get_campaign_stats` — campaigns of a connected outbound tool, which the breakdown above does
  not cover. Can be cumulative; never read a total as a window.
- `list_replies` / `list_conversations` — the replies themselves, to check what "positive"
  actually said.
- `list_sequences`, `get_sequence`, `preview_sequence_for_lead` — which copy each variant
  really sends, with its slots rendered.

Count **real** replies: out-of-office and bounces are not replies; an accepted LinkedIn
invitation is not a positive. Recent sends have had less time to be answered — compare
mature windows.

Derived per sequence: sends, real replies, positives, **sends per positive**, bounces.
If a number cannot be read, it is "not measurable" with the reason — never estimated.

## 2. Judge — against the bar you fixed first

Write the bar down before reading the numbers. It answers, for your volume and market:

- the minimum sends per variant before any verdict (below it: **unclear**, keep running)
- when a variant with zero real replies is stopped
- when a variant is far enough ahead to become the default
- at what sends-per-positive the copy, offer or source is the problem — **not** the volume
- at what sends-per-positive it is worth adding volume

`outbound-playbook/benchmarks.md` gives published reference points to set it from.

Statistical floor, regardless of your bar: **a `low_sample` group is never a winner, and two
arms whose intervals overlap are not different.** Small numbers are "not reliable", not a
trend.

Verdicts: `unclear` · `stop` · `default` · `swap` (copy, offer or source) · `scale`.

## 3. Propose — at most three, most important first

Never two proposals on the same object. Each one:

```json
{
  "id": "opt-<yyyymmdd>-<n>",
  "kind": "pause_variant | new_challenger | set_default | swap_source | scale_up | reallocate",
  "object": "<sequence / variant / source, with id>",
  "change": "<one sentence>",
  "evidence": "<the numbers and n, with the tool they came from>",
  "on_yes": "<exactly which call(s) are made, and nothing else>",
  "learn_on_no": "<which assumption a rejection would refute>"
}
```

What the kinds mean:

- `pause_variant` — enough sends, no real replies.
- `new_challenger` — a new variant against the current winner. **Change exactly one variable**
  (angle *or* CTA *or* subject — never two), keep the winner's register, render every slot
  with `preview_sequence_for_lead`, run the pre-send check from `sequences/copy-patterns.md`.
  No unproven claims, no figures that are not in your Wissen.
- `set_default` — a variant clearly ahead with enough sends behind it.
- `swap_source` — the qualification gate passes too few, or the audience does not answer:
  move down the source ladder (`sourcing-topup`).
- `scale_up` / `reallocate` — good sends-per-positive and spare capacity. Volume comes from
  more senders or from shifting limits between sequences, never from raising one sender's
  limit.

A run without reliable data proposes nothing and says "unclear".

## 4. Execute — only what was approved

After a yes, make exactly the calls listed in `on_yes` — typically `update_sequence` for copy,
variants or pausing — then read the object back and confirm the change. Changes apply to
**new** leads and new variants; leads already mid-sequence are not rewritten.

## 5. Learn

For every verdict, including "unclear", keep one record:

```
date · sequence · variant · sends · real replies · positives · verdict · evidence
```

A pattern that holds across enough runs becomes a rule: propose it as a Wissen revision
(`wissen_asset_revise`) so it goes through the approval queue before it shapes future copy.
A rejected proposal is recorded with what it refuted.

## Output

At most eight lines of report, then the proposals:

```
SEQUENCE / VARIANT     SENDS   REAL REPLIES   POSITIVE   SENDS/POSITIVE   VERDICT
<name> / A             <n>     <n>            <n>        <n>              default
<name> / B             <n>     <n>            <n>        —                unclear (low_sample)

PROPOSALS (waiting for decision)
  1. <change> — evidence <x/n> — on yes: <call>
```
